# Cook Book

My personal cookbook, with a searchable, printable recipe page.

View the cookbook at <https://lukasfacile.github.io/cook-book/>.

GitHub Actions builds and publishes the page whenever changes are pushed to
`main`. Edit or add a Markdown recipe and push it (or edit it on GitHub); the
website updates automatically after the deployment finishes. There is no need
to rebuild or commit `index.html` for publishing. Local edits must be pushed
to GitHub before they appear on the website.

Open `index.html` in a browser, or preview at <http://localhost:8000>:

```sh
python3 -m http.server 8000
```

Recipes live in `cook-book/` as Markdown notes. Add a note with `# Ingredients`
and `# Instructions` headings, bullet-point ingredients, numbered steps, and
optional tags such as `#korean #stew`. The filename becomes the recipe title.
The page supports this simple recipe format; it does not render general Markdown.

For a local preview, rebuild the page after editing or adding recipes:

```sh
python3 scripts/build.py
```

The checked-in `index.html` is a preview snapshot; the published page is always
generated from the latest notes. Deployments can be checked or rerun under
GitHub Actions → Build and publish cookbook. A failed build leaves the previous
successful deployment live.

The builder uses only Python's standard library. Page layout, styles, and search
live in `web/`. No frontend install or external service is required. Ingredient
checkboxes are for the current page session. Search matches titles, ingredients,
and tags; printing includes the currently visible recipes.

Personal Obsidian settings are ignored. Recipe notes remain usable in Obsidian.
