// Real-Time Counter Simulation (counters.js)
document.addEventListener("DOMContentLoaded", function () {
  let globalDeaths = 937;
  let soughtAI = 281;
  let abandoned = 70;

  const elGlobal = document.getElementById("global-deaths");
  const elSought = document.getElementById("sought-ai");
  const elAbandoned = document.getElementById("abandoned");

  function update() {
    globalDeaths += Math.floor(Math.random() * 3) + 1; // +1..3
    soughtAI += Math.floor(Math.random() * 2); // +0..1
    abandoned += 1; // critical failure rate

    if (elGlobal) elGlobal.textContent = globalDeaths;
    if (elSought) elSought.textContent = soughtAI;
    if (elAbandoned) elAbandoned.textContent = abandoned;
  }

  // initial DOM values (in case HTML didn't have them)
  if (elGlobal) elGlobal.textContent = globalDeaths;
  if (elSought) elSought.textContent = soughtAI;
  if (elAbandoned) elAbandoned.textContent = abandoned;

  setInterval(update, 5000);
});
