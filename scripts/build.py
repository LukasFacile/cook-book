"""Build a portable cookbook page from the Markdown recipe notes (no dependencies)."""
from html import escape
from pathlib import Path
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def recipe(path):
    title = path.stem
    sections = {"ingredients": [], "instructions": []}
    section = None
    tags = []
    for line in path.read_text().splitlines():
        line = line.strip()
        heading = re.match(r"^#{1,6}\s+(.+)$", line)
        if heading:
            section = heading[1].lower()
        elif re.match(r"^#[\w-]+", line):
            tags.extend(re.findall(r"#([\w-]+)", line))
        elif section in sections and line:
            sections[section].append(re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", line))
    if not all(sections.values()):
        raise ValueError(f"{path}: recipes need Ingredients and Instructions sections")
    slug = quote(path.relative_to(ROOT / "cook-book").with_suffix("").as_posix(), safe="")
    ingredients = "".join(f'<li><label><input type="checkbox"><span>{escape(item)}</span></label></li>' for item in sections['ingredients'])
    steps = "".join(f"<li>{escape(item)}</li>" for item in sections['instructions'])
    badges = "".join(f'<span class="tag">{escape(tag)}</span>' for tag in dict.fromkeys(tags))
    search = escape(" ".join([title, *tags, *sections['ingredients']]).lower(), quote=True)
    return f'''<article class="recipe" id="{slug}" data-search="{search}">
      <header class="recipe-header"><div><p class="eyebrow">FROM THE RECIPE BOX</p><h2>{escape(title)}</h2><div class="tags">{badges}</div></div>
      <a class="permalink" href="#{slug}" aria-label="Link to {escape(title, quote=True)}">Recipe link ↗</a></header>
      <div class="recipe-body"><section class="ingredients"><h3>Ingredients <span>{len(sections['ingredients']):02}</span></h3><p class="hint">Check things off as you go.</p><ul>{ingredients}</ul></section>
      <section class="method"><h3>Let’s cook.</h3><ol>{steps}</ol></section></div></article>'''


def main():
    recipes = [recipe(path) for path in sorted((ROOT / 'cook-book').rglob('*.md')) if not any(part.startswith('.') for part in path.relative_to(ROOT / 'cook-book').parts)]
    template = (ROOT / 'web/template.html').read_text()
    page = template.replace('<!-- RECIPES -->', '\n'.join(recipes)).replace('{{COUNT}}', str(len(recipes)))
    (ROOT / 'index.html').write_text(page)
    print(f"Built index.html with {len(recipes)} recipe(s)")


if __name__ == '__main__':
    main()
