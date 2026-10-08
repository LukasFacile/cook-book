# Cook Book

My personal cookbook, with a searchable recipe collection. Select a recipe to
focus on its ingredients and instructions, then use **Back to recipes** to return
to the collection. Recipe links open directly to the selected recipe and can be
bookmarked or shared.

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

Recipes live in `cook-book/` as Markdown notes. Copy [the recipe template](templates/Recipe.md)
into that folder and rename it to the recipe title. Fill in `# Ingredients` with
bullet-point ingredients and `# Instructions` with numbered steps. Both sections
must contain text. Use optional `# Notes` for tips or substitutions and `# Source`
for attribution and links; empty optional sections are omitted. No yield or time
fields are needed. Optional tags such as `#korean #stew` go on their own line.
The filename becomes the recipe title.

Link to component recipes anywhere in Ingredients, Instructions, Notes, or Source
using Obsidian wiki links: `[[Caesar Dressing]]` or
`[[Caesar Dressing|the dressing]]`. Clicking opens that recipe's focused view;
the browser Back button returns to the previous recipe. A `.md` suffix is also
accepted. Recipe names are matched without case sensitivity and must be unique.
For duplicate names in subfolders, use a path relative to `cook-book/`, such as
`[[Sauces/Caesar Dressing|the dressing]]`. Missing or ambiguous links fail the
build with the originating filename so broken navigation is caught before publishing.
Heading links and embedded notes are not supported.

Source can contain plain attribution, a bare `https://…` URL, or a Markdown link
such as `[Original recipe](https://example.com/recipe)`. Only HTTP(S) web links
are supported. Each nonempty Notes or Source line becomes a paragraph. Text is
escaped safely; the page supports this simple recipe format rather than general
Markdown or embedded HTML. Templates stay outside `cook-book/` so they are not
published as recipes.

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
and tags; returning to the collection preserves your search. Printing includes
the selected recipe, or all matching recipes when browsing the collection.

Personal Obsidian settings are ignored. Recipe notes remain usable in Obsidian.
