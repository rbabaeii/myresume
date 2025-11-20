
let menu = document.querySelector("#menu-btn");
let header = document.querySelector(".header");

menu.onclick = () => {
  menu.classList.toggle("fa-times");
  header.classList.toggle("active");
  document.body.classList.toggle("no-scroll", header.classList.contains("active"));
};

let themeToggler = document.querySelector("#theme-toggler");

themeToggler.onclick = () => {
  themeToggler.classList.toggle("fa-sun");
  if (themeToggler.classList.contains("fa-sun")) {
    document.body.classList.add("active");
    localStorage.setItem("theme", "dark");
  } else {
    document.body.classList.remove("active");
    localStorage.removeItem("theme");
  }
};

// Load theme on page load
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("active");
  themeToggler.classList.add("fa-sun");
}
