"""Build a portable cookbook page from Markdown recipe notes (no dependencies)."""
from html import escape
from pathlib import Path
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
INLINE = re.compile(r'\[\[([^\[\]\n]+)\]\]|\[([^\]\n]+)\]\((https?://[^\s<>"\)]+)\)|(https?://[^\s<>"\]]+)')


def recipe_paths():
    return [path for path in sorted((ROOT / 'cook-book').rglob('*.md'))
            if not any(part.startswith('.') for part in path.relative_to(ROOT / 'cook-book').parts)]


def recipe_key(path):
    return path.relative_to(ROOT / 'cook-book').with_suffix('').as_posix()


def recipe_slug(path):
    return quote(recipe_key(path), safe='')


def resolve_recipe(target, paths, source):
    target = target.strip().removesuffix('.md')
    # A folder-qualified name resolves exactly; a short name must be unique.
    matches = [path for path in paths
               if (recipe_key(path) if '/' in target else path.stem).casefold() == target.casefold()]
    if len(matches) != 1:
        reason = 'missing' if not matches else 'ambiguous'
        raise ValueError(f'{source}: {reason} recipe link [[{target}]]; use a unique recipe name or folder-qualified path')
    return matches[0]


def inline(text, paths, source):
    """Escape prose and allow only recipe links and HTTP(S) source links."""
    parts = []
    cursor = 0
    for match in INLINE.finditer(text):
        parts.append(escape(text[cursor:match.start()]))
        wiki, label, url, bare_url = match.groups()
        if wiki is not None:
            target, separator, alias = wiki.partition('|')
            linked = resolve_recipe(target, paths, source)
            label = alias.strip() if separator else target.strip()
            url = '#' + recipe_slug(linked)
        else:
            url = url or bare_url
            label = label or url
        parts.append(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>')
        cursor = match.end()
    parts.append(escape(text[cursor:]))
    return ''.join(parts)


def recipe(path, paths=None):
    paths = recipe_paths() if paths is None else paths
    title = path.stem
    sections = {name: [] for name in ('ingredients', 'instructions', 'notes', 'source')}
    section = None
    tags = []
    for line in path.read_text().splitlines():
        line = line.strip()
        heading = re.match(r'^#{1,6}\s+(.+)$', line)
        if heading:
            section = heading[1].lower()
        elif re.fullmatch(r'#[\w-]+(?:\s+#[\w-]+)*', line):
            tags.extend(re.findall(r'#([\w-]+)', line))
        elif section in sections and line:
            sections[section].append(re.sub(r'^(?:[-*+]\s+|\d+[.)]\s+)', '', line))
    if not sections['ingredients'] or not sections['instructions']:
        raise ValueError(f'{path}: recipes need Ingredients and Instructions sections')
    slug = recipe_slug(path)
    ingredients = ''.join(f'<li><label><input type="checkbox"><span>{inline(item, paths, path)}</span></label></li>' for item in sections['ingredients'])
    steps = ''.join(f'<li>{inline(item, paths, path)}</li>' for item in sections['instructions'])
    extras = ''.join(
        f'<section class="recipe-extra"><h3>{name.title()}</h3>'
        + ''.join(f'<p>{inline(item, paths, path)}</p>' for item in sections[name])
        + '</section>'
        for name in ('notes', 'source') if sections[name]
    )
    badges = ''.join(f'<span class="tag">{escape(tag)}</span>' for tag in dict.fromkeys(tags))
    search = escape(' '.join([title, *tags, *sections['ingredients']]).lower(), quote=True)
    return f'''<article class="recipe" id="{slug}" data-search="{search}">
      <header class="recipe-header"><div><h2 tabindex="-1"><a href="#{slug}">{escape(title)}</a></h2><div class="tags">{badges}</div></div>
      <a class="permalink" href="#{slug}" aria-label="Link to {escape(title, quote=True)}">Recipe link</a></header>
      <div class="recipe-body"><section class="ingredients"><h3>Ingredients <span>{len(sections['ingredients']):02}</span></h3><ul>{ingredients}</ul></section>
      <div class="method"><section><h3>Instructions</h3><ol>{steps}</ol></section>{extras}</div></div></article>'''


def main():
    paths = recipe_paths()
    recipes = [recipe(path, paths) for path in paths]
    template = (ROOT / 'web/template.html').read_text()
    page = template.replace('<!-- RECIPES -->', '\n'.join(recipes)).replace('{{COUNT}}', str(len(recipes)))
    (ROOT / 'index.html').write_text(page)
    print(f'Built index.html with {len(recipes)} recipe(s)')


if __name__ == '__main__':
    main()
