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

  const toggler = document.querySelector('.custom-toggler');

  toggler.addEventListener('click', () => {
    toggler.classList.toggle('active');
  });


  // Calculate D&D ability modifier
  function calculateModifier(score) {
    return Math.floor((score - 10) / 2);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.attribute-input');

    inputs.forEach(input => {
      const modifierDisplay = input.parentElement.querySelector('.modifier-display');

      const updateModifier = () => {
        const value = parseInt(input.value) || 10;
        const mod = calculateModifier(value);
        modifierDisplay.textContent = (mod >= 0 ? '+' : '') + mod;
      };

      input.addEventListener('input', updateModifier);
      updateModifier(); // initialize on load
    });
  });


  // Footer social links hover effect logging
  const socialLinks = document.querySelectorAll("#social-networks a");
  socialLinks.forEach(link => {
    link.addEventListener("mouseenter", () => {
      console.log(`Hovering on ${link.getAttribute("aria-label")}`);
    });
  });
});

// === Party system JS ===
document.addEventListener("DOMContentLoaded", () => {
  // Helper to show toast-like alert
  const flashMessage = (text, type = "info") => {
    const div = document.createElement("div");
    div.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3 shadow`;
    div.style.zIndex = 1055;
    div.textContent = text;
    document.body.appendChild(div);
    setTimeout(() => div.remove(), 2500);
  };

  // --- Invite handler ---
  const inviteForm = document.querySelector("#invite-form");
  if (inviteForm) {
    inviteForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = inviteForm.username.value.trim();
      if (!username) return flashMessage("Enter a username!", "warning");

      const partyId = inviteForm.dataset.party;
      const formData = new FormData();
      formData.append("username", username);

      const res = await fetch(`/party/${partyId}/invite/`, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": getCSRFToken() },
      });
      const data = await res.json();
      if (data.ok) {
        flashMessage(data.message, "success");
        const li = document.createElement("li");
        li.className = "list-group-item bg-dark text-light added";
        li.textContent = `@${username} — Pending`;
        document.querySelector("#invite-list")?.prepend(li);
        inviteForm.reset();
      } else {
        flashMessage(data.message || "Invite failed.", "danger");
      }
    });
  }

  // --- Remove member handler ---
  document.querySelectorAll(".remove-member").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const userId = btn.dataset.user;
      const partyId = document.querySelector("#invite-form")?.dataset.party;
      if (!partyId || !userId) return;

      if (!confirm("Remove this member?")) return;
      const fd = new FormData();
      fd.append("user_id", userId);
      const res = await fetch(`/party/${partyId}/remove-member/`, {
        method: "POST",
        body: fd,
        headers: { "X-CSRFToken": getCSRFToken() },
      });
      const data = await res.json();
      if (data.ok) {
        flashMessage("Member removed.", "success");
        document.querySelector(`#member-${userId}`)?.remove();
      } else {
        flashMessage("Failed to remove member.", "danger");
      }
    });
  });

  // --- Character select handler ---
  document.querySelectorAll("form.select-character").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const cid = form.querySelector("select").value;
      const partyId = form.dataset.party;
      if (!cid) return;
      const fd = new FormData();
      fd.append("character_id", cid);
      const res = await fetch(`/party/${partyId}/select-character/`, {
        method: "POST",
        body: fd,
        headers: { "X-CSRFToken": getCSRFToken() },
      });
      const data = await res.json();
      if (data.ok) {
        flashMessage(`Active character: ${data.character.name}`, "success");
      } else {
        flashMessage("Failed to update character.", "danger");
      }
    });
  });

  // --- CSRF helper ---
  function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (let c of cookies) {
      const [key, val] = c.trim().split("=");
      if (key === name) return decodeURIComponent(val);
    }
    return "";
  }
});
