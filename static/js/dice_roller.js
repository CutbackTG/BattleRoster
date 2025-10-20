// ----------------------
// Toggle dice roller panel
// ----------------------
function toggleDiceRoller() {
  const panel = document.getElementById("dice-roller-panel");
  panel.classList.toggle("open");
}

// Roll a single die
function rollSingle(i) {
  i = parseInt(i, 10); // convert string to number

  const select = document.getElementById('die' + i);
  if (!select) return; // Safety check

  const sides = parseInt(select.value, 10);
  if (isNaN(sides)) return;

  const result = rollDie(sides);

  const resultList = document.getElementById('dice-results-list');
  let li = document.getElementById('result-item-' + i);
  if (!li) {
    li = document.createElement('li');
    li.id = 'result-item-' + i;
    resultList.appendChild(li);
  }
  li.textContent = `Die ${i} (${sides}): ${result}`;

  updateTotal();
}

// ----------------------
// Roll all dice
// ----------------------
function rollAll() {
  const results = [];
  for (let i = 1; i <= 3; i++) {
    const select = document.getElementById(`die${i}`);
    const sides = parseInt(select.value);
    const roll = Math.floor(Math.random() * sides) + 1;
    results.push({ value: roll, sides });
    updateResults(i, roll, sides);
  }
  updateTotal(results.map(r => r.value));
  scrollToResults();
}

// ----------------------
// Update individual die result
// ----------------------
function updateResults(dieNum, value, sides) {
  const list = document.getElementById("dice-results-list");
  let li = list.querySelector(`#roll-${dieNum}`);
  
  if (!li) {
    li = document.createElement("li");
    li.id = `roll-${dieNum}`;
    list.appendChild(li);
  }
  
  li.textContent = `Roll ${dieNum}: ${value}`;
  li.classList.remove("critical");

  // Critical glow + sparkles for D20 natural 20
  if (sides === 20 && value === 20) {
    li.classList.add("critical");
    document.getElementById("dice-total").classList.add("critical");
    spawnSparkles(li, 12); // 12 sparkles
  }

  updateTotalFromList();
  scrollToResults();
}

// ----------------------
// Update total from results
// ----------------------
function updateTotal(results) {
  const total = results.reduce((a, b) => a + b, 0);
  const totalEl = document.getElementById("dice-total");
  totalEl.textContent = `Total: ${total}`;
  totalEl.classList.remove("critical"); // remove old critical if any
}

// ----------------------
// Recalculate total from list items
// ----------------------
function updateTotalFromList() {
  const list = document.getElementById("dice-results-list");
  const rolls = Array.from(list.children)
                     .map(li => parseInt(li.textContent.split(": ")[1]));
  const total = rolls.reduce((a, b) => a + b, 0);
  const totalEl = document.getElementById("dice-total");
  totalEl.textContent = `Total: ${total}`;
}

// ----------------------
// Scroll to dice results smoothly
// ----------------------
function scrollToResults() {
  const resultsDiv = document.getElementById("dice-results");
  const offset = 80;
  const top = resultsDiv.getBoundingClientRect().top + window.pageYOffset - offset;
  window.scrollTo({ top, behavior: "smooth" });
}

// ----------------------
// Sparkle effect for criticals
// ----------------------
function spawnSparkles(targetEl, count = 8) {
  for (let i = 0; i < count; i++) {
    const sparkle = document.createElement("div");
    sparkle.classList.add("sparkle");

    // Random movement and size
    const x = (Math.random() - 0.5) * 80; // px
    const y = (Math.random() - 0.5) * 60; // px
    const size = 4 + Math.random() * 4; // 4-8px
    sparkle.style.width = `${size}px`;
    sparkle.style.height = `${size}px`;
    sparkle.style.setProperty('--x', `${x}px`);
    sparkle.style.setProperty('--y', `${y}px`);

    // Random color: gold / goldenrod / white
    const colors = ['gold', 'goldenrod', 'white'];
    sparkle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

    // Position relative to target
    const rect = targetEl.getBoundingClientRect();
    sparkle.style.top = `${rect.top + window.pageYOffset + rect.height/2}px`;
    sparkle.style.left = `${rect.left + window.pageXOffset + rect.width/2}px`;

    document.body.appendChild(sparkle);

    // Remove after animation
    sparkle.addEventListener("animationend", () => sparkle.remove());
  }
}

document.querySelectorAll('.btn-small').forEach(btn => {
  btn.addEventListener('click', function() {
    const i = parseInt(this.dataset.die, 10);
    rollSingle(i);
  });
});
