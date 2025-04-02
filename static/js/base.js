const burger = document.querySelector(".burger");
const side_nav = document.querySelector(".side-navigation");
const close = document.getElementById("close");

burger.addEventListener("click", () => {
  side_nav.classList.add("show-side-nav");
});

close.addEventListener("click", () => {
  side_nav.classList.remove("show-side-nav");
});

window.addEventListener("scroll", () => {
  side_nav.classList.remove("show-side-nav");
});

const account = document.querySelector(".account-info");
const bookings = document.querySelector(".bookings");

account.addEventListener("click", () => {
  bookings.classList.toggle("show-bookings");
});
