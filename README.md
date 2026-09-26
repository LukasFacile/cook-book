# Cook Book

My personal cookbook, with a searchable, printable recipe page.

Open `index.html` in a browser, or preview at <http://localhost:8000>:

```sh
python3 -m http.server 8000
```

Recipes live in `cook-book/` as Markdown notes. Add a note with `# Ingredients`
and `# Instructions` headings, bullet-point ingredients, numbered steps, and
optional tags such as `#korean #stew`. The filename becomes the recipe title.
The page supports this simple recipe format; it does not render general Markdown.

After editing or adding recipes, rebuild the page and commit the generated HTML:

```sh
python3 scripts/build.py
```

The builder uses only Python's standard library. Page layout, styles, and search
live in `web/`. No frontend install or external service is required. Ingredient
checkboxes are for the current page session. Search matches titles, ingredients,
and tags; printing includes the currently visible recipes.

Personal Obsidian settings are ignored. Recipe notes remain usable in Obsidian.
