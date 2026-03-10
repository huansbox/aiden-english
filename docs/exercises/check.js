/* ── Interactive exercise checker ─────────────── */

document.addEventListener("DOMContentLoaded", () => {
  const checkBtn = document.getElementById("check-btn");
  const resetBtn = document.getElementById("reset-btn");
  const scoreEl = document.getElementById("score");

  checkBtn.addEventListener("click", checkAnswers);
  resetBtn.addEventListener("click", resetAll);

  function normalize(s) {
    return s.trim().toLowerCase().replace(/\s+/g, " ");
  }

  function checkAnswers() {
    const questions = document.querySelectorAll(".q[data-type]");
    let total = 0;
    let correct = 0;

    questions.forEach((q) => {
      // Clear previous state
      q.classList.remove("correct", "wrong", "open-answered");

      const type = q.dataset.type;
      const answer = q.dataset.answer || "";

      if (type === "open") {
        // Open-ended: just show reference answer, don't score
        q.classList.add("open-answered");
        return;
      }

      total++;
      let userAnswer = "";
      let isCorrect = false;

      if (type === "input") {
        const input = q.querySelector("input[type='text']");
        userAnswer = normalize(input ? input.value : "");
        // Accept multiple valid answers separated by |
        const accepted = answer.split("|").map(normalize);
        isCorrect = accepted.includes(userAnswer);
      } else if (type === "radio") {
        const checked = q.querySelector("input[type='radio']:checked");
        userAnswer = checked ? normalize(checked.value) : "";
        isCorrect = normalize(answer) === userAnswer;
      } else if (type === "checkbox") {
        const checked = Array.from(q.querySelectorAll("input[type='checkbox']:checked"));
        const userSet = new Set(checked.map((c) => normalize(c.value)));
        const answerSet = new Set(answer.split(",").map(normalize));
        isCorrect = userSet.size === answerSet.size && [...answerSet].every((a) => userSet.has(a));
      } else if (type === "select") {
        const sel = q.querySelector("select");
        userAnswer = normalize(sel ? sel.value : "");
        isCorrect = normalize(answer) === userAnswer;
      } else if (type === "order") {
        const inputs = Array.from(q.querySelectorAll("input[type='number']"));
        const userVals = inputs.map((i) => i.value.trim());
        const answerVals = answer.split(",").map((a) => a.trim());
        isCorrect = userVals.length === answerVals.length && userVals.every((v, i) => v === answerVals[i]);
      }

      q.classList.add(isCorrect ? "correct" : "wrong");
      if (isCorrect) correct++;
    });

    scoreEl.textContent = `${correct} / ${total} correct`;
    scoreEl.className = "visible";
    scoreEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function resetAll() {
    const questions = document.querySelectorAll(".q[data-type]");
    questions.forEach((q) => {
      q.classList.remove("correct", "wrong", "open-answered");
      q.querySelectorAll("input[type='text']").forEach((i) => (i.value = ""));
      q.querySelectorAll("input[type='radio']").forEach((i) => (i.checked = false));
      q.querySelectorAll("input[type='checkbox']").forEach((i) => (i.checked = false));
      q.querySelectorAll("input[type='number']").forEach((i) => (i.value = ""));
      q.querySelectorAll("select").forEach((s) => (s.selectedIndex = 0));
    });
    scoreEl.className = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
});
