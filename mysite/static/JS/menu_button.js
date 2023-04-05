var menu = document.querySelector(".menu");
var menuButton = document.querySelector(".icon");
var outclick = document.querySelector(".main-section");
var headerclick = document.querySelector(".header");
var shop = document.querySelector(".grid-section");

menuButton.addEventListener("click", to_remove_hidden);

outclick.addEventListener("click", to_add_hidden);

shop.addEventListener("click", to_add_hidden);

function to_add_hidden() {
  menu.classList.add("hidden");
}
function to_remove_hidden() {
  menu.classList.remove("hidden");
}
