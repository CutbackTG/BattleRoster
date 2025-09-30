// main.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("BattleRoster site loaded ✅");

  // Navbar active link highlight
  const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
  navLinks.forEach(link => {
    link.addEventListener("click", function () {
      navLinks.forEach(l => l.classList.remove("active"));
      this.classList.add("active");
    });
  });

  // Navbar toggler (hamburger) color toggle when menu is open
  const navbarToggler = document.querySelector(".navbar-toggler");
  const navbarCollapse = document.getElementById("navMenu");

  if (navbarToggler && navbarCollapse) {
    navbarCollapse.addEventListener("shown.bs.collapse", () => {
      navbarToggler.classList.add("open"); // Add a class when menu opens
    });

    navbarCollapse.addEventListener("hidden.bs.collapse", () => {
      navbarToggler.classList.remove("open"); // Remove when menu closes
    });
  }

  // Footer social links hover effect logging
  const socialLinks = document.querySelectorAll("#social-networks a");
  socialLinks.forEach(link => {
    link.addEventListener("mouseenter", () => {
      console.log(`Hovering on ${link.getAttribute("aria-label")}`);
    });
  });
});
