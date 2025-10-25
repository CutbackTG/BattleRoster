// Toggle dice roller panel

function toggleDiceRoller() {
  const panel = document.getElementById("dice-roller-panel");
  panel.classList.toggle("open");
}

// Roll a single die
function rollSingle(i) {
  i = parseInt(i, 10);
  const select = document.getElementById('die' + i);
  if (!select) return;

  const sides = parseInt(select.value, 10);
  if (isNaN(sides)) return;

  const roll = Math.floor(Math.random() * sides) + 1;
  updateResults(i, roll, sides);
}

// Roll all dice
function rollAll() {
  for (let i = 1; i <= 3; i++) {
    const select = document.getElementById(`die${i}`);
    const sides = parseInt(select.value, 10);
    const roll = Math.floor(Math.random() * sides) + 1;
    updateResults(i, roll, sides);
  }
}


// Update individual die result
function updateResults(dieNum, value, sides) {
  const list = document.getElementById("dice-results-list");
  let li = list.querySelector(`#roll-${dieNum}`);

  if (!li) {
    li = document.createElement("li");
    li.id = `roll-${dieNum}`;
    list.appendChild(li);
  }

  li.textContent = `Die ${dieNum} (${sides}): ${value}`;
  li.classList.remove("critical");

  // Critical D20 natural 20
  if (sides === 20 && value === 20) {
    li.classList.add("critical");
    document.getElementById("dice-total").classList.add("critical");
    spawnSparkles(li, 12);
  }

  updateTotalFromList();
}

// Recalculate total from list items
function updateTotalFromList() {
  const list = document.getElementById("dice-results-list");
  const rolls = Array.from(list.children)
    .map(li => parseInt(li.textContent.split(": ").pop(), 10))
    .filter(n => !isNaN(n));
  
  const total = rolls.reduce((a, b) => a + b, 0);
  const totalEl = document.getElementById("dice-total");
  totalEl.textContent = `Total: ${total}`;
  totalEl.classList.remove("critical");
}

// Sparkle effect for criticals
function spawnSparkles(targetEl, count = 8) {
  for (let i = 0; i < count; i++) {
    const sparkle = document.createElement("div");
    sparkle.classList.add("sparkle");

    const x = (Math.random() - 0.5) * 80;
    const y = (Math.random() - 0.5) * 60;
    const size = 4 + Math.random() * 4;
    sparkle.style.width = `${size}px`;
    sparkle.style.height = `${size}px`;
    sparkle.style.setProperty('--x', `${x}px`);
    sparkle.style.setProperty('--y', `${y}px`);

    const colors = ['gold', 'goldenrod', 'white'];
    sparkle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

    const rect = targetEl.getBoundingClientRect();
    sparkle.style.top = `${rect.top + window.pageYOffset + rect.height / 2}px`;
    sparkle.style.left = `${rect.left + window.pageXOffset + rect.width / 2}px`;

    document.body.appendChild(sparkle);
    sparkle.addEventListener("animationend", () => sparkle.remove());
  }
}

// Event bindings
document.querySelectorAll('.btn-small').forEach(btn => {
  btn.addEventListener('click', function() {
    const i = parseInt(this.dataset.die, 10);
    rollSingle(i);
  });
});
