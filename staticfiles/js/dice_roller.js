function toggleDiceRoller() {
  const panel = document.getElementById("dice-roller-panel");
  panel.classList.toggle("open");
}

document.addEventListener("DOMContentLoaded", () => {
  const resultsBox = document.querySelector(".dice-results");
  const totalBox = document.querySelector(".dice-results h4");

  // Only run if results exist
  if (resultsBox) {
    // Glow animation for all rolls
    resultsBox.classList.remove("active");
    void resultsBox.offsetWidth;
    resultsBox.classList.add("active");

    // Auto-open the panel
    document.getElementById("dice-roller-panel").classList.add("open");

    // Detect if any D20 roll = 20 (critical success)
    const rolls = Array.from(resultsBox.querySelectorAll("li")).map(li => li.textContent);
    const hasNat20 = rolls.some(text => text.includes("D20") && text.match(/20\b/));

    if (hasNat20 && totalBox) {
      totalBox.classList.add("critical");
      setTimeout(() => totalBox.classList.remove("critical"), 2000);
    }
  }
});
