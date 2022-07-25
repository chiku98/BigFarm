window.addEventListener("scroll", () => {
  const indicatorBar = document.querySelector(".scroll-indicator-bar");

  const pageScroll = document.body.scrollTop || document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const scrollValue = (pageScroll / height) * 100;

  indicatorBar.style.width = scrollValue + "%";
});

//Responsive landing_navigation menu toggle
const menuBtn = document.querySelector(".nav-menu-btn");
const closeBtn = document.querySelector(".nav-close-btn");
const landing_navigation = document.querySelector(".landing_navigation");

menuBtn.addEventListener("click", () => {
  landing_navigation.classList.add("active");
});

closeBtn.addEventListener("click", () => {
  landing_navigation.classList.remove("active");
});