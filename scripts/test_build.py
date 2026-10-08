"""Regression checks for recipe parsing and safe component links."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.patch = patch.object(build, 'ROOT', self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.component = self.note('Caesar Dressing', '# Ingredients\n* Lemon\n# Instructions\n1. Mix.')

    def note(self, name, text):
        path = self.root / 'cook-book' / (name + '.md')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_optional_sections_and_source_links(self):
        path = self.note('Salad', '# Ingredients\n* [[Caesar Dressing|dressing]]\n# Instructions\n1. Toss with [[Caesar Dressing.md]].\n# Notes\nKeep <cold> & covered.\n# Source\n[Original](https://example.com/?a=1&b=2)\nhttps://example.com/recipe\n#salad #side')
        html = build.recipe(path)
        self.assertIn('href="#Caesar%20Dressing">dressing</a>', html)
        self.assertIn('href="#Caesar%20Dressing">Caesar Dressing.md</a>', html)
        self.assertIn('<h3>Notes</h3><p>Keep &lt;cold&gt; &amp; covered.</p>', html)
        self.assertIn('<h3>Source</h3>', html)
        self.assertIn('href="https://example.com/?a=1&amp;b=2">Original</a>', html)
        self.assertIn('href="https://example.com/recipe"', html)
        self.assertNotIn('<p>#salad', html)

    def test_optional_sections_omitted_and_required_sections_validated(self):
        html = build.recipe(self.component)
        self.assertNotIn('<h3>Notes</h3>', html)
        self.assertNotIn('<h3>Source</h3>', html)
        bad = self.note('Empty', '# Ingredients\n* Salt\n# Notes\nNo instructions')
        with self.assertRaisesRegex(ValueError, 'need Ingredients and Instructions'):
            build.recipe(bad)

    def test_missing_and_ambiguous_links(self):
        paths = build.recipe_paths()
        with self.assertRaisesRegex(ValueError, 'missing recipe link'):
            build.inline('[[Unknown]]', paths, self.component)
        self.note('Sauces/Caesar Dressing', '# Ingredients\n* Lemon\n# Instructions\n1. Mix.')
        paths = build.recipe_paths()
        with self.assertRaisesRegex(ValueError, 'ambiguous recipe link'):
            build.inline('[[Caesar Dressing]]', paths, self.component)
        self.assertIn('href="#Sauces%2FCaesar%20Dressing"',
                      build.inline('[[sauces/caesar dressing.md|Sauce]]', paths, self.component))

    def test_escaping_and_disallowed_link_schemes(self):
        paths = build.recipe_paths()
        html = build.inline('<script>alert(1)</script> [[Caesar Dressing|<img onerror=x>]] [bad](javascript:alert(1))', paths, self.component)
        self.assertNotIn('<script>', html)
        self.assertNotIn('<img', html)
        self.assertNotIn('href="javascript:', html)
        self.assertIn('&lt;img onerror=x&gt;</a>', html)
        path = self.note('A "B" & C', '# Ingredients\n* "x" < y\n# Instructions\n1. Mix.')
        html = build.recipe(path)
        self.assertIn('id="A%20%22B%22%20%26%20C"', html)
        self.assertIn('A &quot;B&quot; &amp; C', html)

    def test_hidden_notes_are_not_recipes(self):
        self.note('.templates/Hidden', 'not a recipe')
        self.assertEqual(build.recipe_paths(), [self.component])


if __name__ == '__main__':
    unittest.main()
