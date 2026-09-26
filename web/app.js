const search = document.querySelector("#search");
const recipes = [...document.querySelectorAll(".recipe")];
const count = document.querySelector("#count");

function filterRecipes() {
  const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let visible = 0;
  recipes.forEach((recipe) => {
    recipe.hidden = !terms.every((term) =>
      recipe.dataset.search.includes(term),
    );
    if (!recipe.hidden) visible++;
  });
  count.textContent = `${visible} ${visible === 1 ? "recipe" : "recipes"}`;
  document.querySelector("#empty").hidden = visible !== 0;
}

document.querySelector("#search-controls").hidden = false;
document.querySelector("#print").hidden = false;
search.addEventListener("input", filterRecipes);
document.querySelector("#clear").addEventListener("click", () => {
  search.value = "";
  filterRecipes();
  search.focus();
});
document
  .querySelector("#print")
  .addEventListener("click", () => window.print());
filterRecipes();
