const search = document.querySelector("#search");
const recipes = [...document.querySelectorAll(".recipe")];
const count = document.querySelector("#count");
const collection = document.querySelector("#recipes");
const back = document.querySelector("#back");
const searchControls = document.querySelector("#search-controls");
const print = document.querySelector("#print");
let selectedRecipe = null;
let previousRecipe = null;

function filterRecipes() {
  const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  recipes.forEach((recipe) => {
    recipe.hidden = selectedRecipe
      ? recipe !== selectedRecipe
      : !terms.every((term) => recipe.dataset.search.includes(term));
    if (!recipe.hidden) visible++;
  });
  count.textContent = `${visible} ${visible === 1 ? "recipe" : "recipes"}`;
  document.querySelector("#empty").hidden = visible !== 0;
}

function showRoute(moveFocus = false) {
  // Match the generated IDs exactly: recipe slugs already contain URL escapes.
  selectedRecipe = recipes.find((recipe) => `#${recipe.id}` === location.hash) || null;
  collection.classList.toggle("browsing", !selectedRecipe);
  back.hidden = !selectedRecipe;
  count.hidden = !!selectedRecipe;
  searchControls.hidden = !!selectedRecipe;
  print.textContent = selectedRecipe ? "Print recipe" : "Print recipes";
  document.title = selectedRecipe
    ? `${selectedRecipe.querySelector("h2").textContent} · cook book.`
    : "cook book.";
  recipes.forEach((recipe) => {
    recipe.querySelector(".permalink").textContent = selectedRecipe ? "Recipe link" : "View recipe →";
  });
  filterRecipes();
  if (moveFocus) {
    const target = selectedRecipe?.querySelector("h2")
      || (!previousRecipe?.hidden && previousRecipe?.querySelector("h2 a"))
      || search;
    target.focus();
  }
  previousRecipe = selectedRecipe;
}

print.hidden = false;
search.addEventListener("input", filterRecipes);
document.querySelector("#clear").addEventListener("click", () => {
  search.value = "";
  filterRecipes();
  search.focus();
});
document
  .querySelector("#print")
  .addEventListener("click", () => window.print());
window.addEventListener("hashchange", () => showRoute(true));
showRoute();
