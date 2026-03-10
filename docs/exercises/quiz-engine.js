/* ── Quiz Engine v2 ───────────────────── */

document.addEventListener("DOMContentLoaded", () => {
  const data = JSON.parse(document.getElementById("quiz-data").textContent);
  const questions = data.questions;
  const cardArea = document.querySelector(".card-area");
  const progress = document.querySelector(".progress");
  const btnPrev = document.querySelector(".btn-prev");
  const btnNext = document.querySelector(".btn-next");
  const feedbackEl = document.querySelector(".feedback");
  const feedbackInner = feedbackEl.querySelector(".feedback-inner");

  let current = 0;
  let answers = new Array(questions.length).fill(null); // user answers
  let checked = new Array(questions.length).fill(false); // already checked?
  let score = 0;

  // ── Build cards ──────────────────────
  questions.forEach((q, i) => {
    const card = document.createElement("div");
    card.className = "card";
    card.dataset.index = i;
    card.dataset.type = q.type;

    // Section label
    if (q.section) {
      const sec = document.createElement("div");
      sec.className = "section-label";
      sec.textContent = q.section;
      card.appendChild(sec);
    }

    // Prompt
    const prompt = document.createElement("div");
    prompt.className = "prompt";
    prompt.textContent = q.prompt;
    card.appendChild(prompt);

    // Build type-specific UI
    if (q.type === "vocab" || q.type === "select") {
      buildSingleSelect(card, q, i);
    } else if (q.type === "synonym") {
      buildMultiSelect(card, q, i);
    } else if (q.type === "radio") {
      buildSingleSelect(card, q, i);
    } else if (q.type === "wordbank") {
      buildWordBank(card, q, i);
    } else if (q.type === "order") {
      buildOrder(card, q, i);
    }

    cardArea.appendChild(card);
  });

  // Summary card
  const summaryCard = document.createElement("div");
  summaryCard.className = "card summary";
  summaryCard.innerHTML = `
    <div class="prompt">All done!</div>
    <div class="score-big"></div>
    <button class="btn-restart">Try Again</button>
  `;
  summaryCard.querySelector(".btn-restart").addEventListener("click", restart);
  cardArea.appendChild(summaryCard);

  showCard(0);

  // ── Single select (vocab, radio, select) ──
  function buildSingleSelect(card, q, idx) {
    const opts = document.createElement("div");
    opts.className = "options";
    q.options.forEach(opt => {
      const btn = document.createElement("button");
      btn.className = "opt-btn";
      btn.textContent = opt;
      btn.addEventListener("click", () => {
        if (checked[idx]) return;
        opts.querySelectorAll(".opt-btn").forEach(b => b.classList.remove("selected"));
        btn.classList.add("selected");
        answers[idx] = opt;
      });
      opts.appendChild(btn);
    });
    card.appendChild(opts);
  }

  // ── Multi select (synonym — pick N) ──
  function buildMultiSelect(card, q, idx) {
    const opts = document.createElement("div");
    opts.className = "options";
    answers[idx] = new Set();
    q.options.forEach(opt => {
      const btn = document.createElement("button");
      btn.className = "opt-btn";
      btn.textContent = opt;
      btn.addEventListener("click", () => {
        if (checked[idx]) return;
        if (answers[idx].has(opt)) {
          // Deselect this one
          answers[idx].delete(opt);
          btn.classList.remove("selected");
        } else {
          if (answers[idx].size >= (q.pick || 2)) {
            // Deselect the oldest (first inserted in Set)
            const oldest = [...answers[idx]][0];
            answers[idx].delete(oldest);
            // Find the button matching the oldest value and deselect it
            opts.querySelectorAll(".opt-btn").forEach(b => {
              if (b.textContent === oldest) b.classList.remove("selected");
            });
          }
          answers[idx].add(opt);
          btn.classList.add("selected");
        }
      });
      opts.appendChild(btn);
    });
    card.appendChild(opts);
  }

  // ── Word Bank ──────────────────────────
  function buildWordBank(card, q, idx) {
    answers[idx] = new Array(q.sentences.length).fill(null);

    const bank = document.createElement("div");
    bank.className = "word-bank";
    q.words.forEach(w => {
      const btn = document.createElement("button");
      btn.className = "wb-word";
      btn.textContent = w;
      btn.addEventListener("click", () => {
        if (checked[idx]) return;
        // Fill first empty slot
        const slotIdx = answers[idx].indexOf(null);
        if (slotIdx === -1) return;
        answers[idx][slotIdx] = w;
        btn.classList.add("used");
        renderSlots();
      });
      bank.appendChild(btn);
    });
    card.appendChild(bank);

    const sentencesDiv = document.createElement("div");
    sentencesDiv.className = "wb-sentences";
    q.sentences.forEach((s, si) => {
      const row = document.createElement("div");
      row.className = "wb-sentence";
      // Split sentence on ___ placeholder
      const parts = s.text.split("___");
      row.appendChild(document.createTextNode(parts[0]));
      const slot = document.createElement("span");
      slot.className = "wb-slot";
      slot.dataset.slotIndex = si;
      slot.addEventListener("click", () => {
        if (checked[idx]) return;
        const word = answers[idx][si];
        if (!word) return;
        answers[idx][si] = null;
        // Return word to bank
        bank.querySelectorAll(".wb-word").forEach(b => {
          if (b.textContent === word) b.classList.remove("used");
        });
        renderSlots();
      });
      row.appendChild(slot);
      if (parts[1]) row.appendChild(document.createTextNode(parts[1]));
      sentencesDiv.appendChild(row);
    });
    card.appendChild(sentencesDiv);

    function renderSlots() {
      sentencesDiv.querySelectorAll(".wb-slot").forEach((slot, si) => {
        slot.textContent = answers[idx][si] || "";
      });
    }
  }

  // ── Order (click-to-sort) ──────────────
  function buildOrder(card, q, idx) {
    answers[idx] = [];

    const pool = document.createElement("div");
    pool.className = "order-pool";
    const sorted = document.createElement("div");
    sorted.className = "order-sorted";

    q.items.forEach(item => {
      const btn = document.createElement("div");
      btn.className = "order-item";
      btn.textContent = item;
      btn.addEventListener("click", () => {
        if (checked[idx]) return;
        if (btn.parentElement === pool) {
          // Move to sorted
          answers[idx].push(item);
          sorted.appendChild(btn);
        } else {
          // Move back to pool
          answers[idx] = answers[idx].filter(a => a !== item);
          pool.appendChild(btn);
        }
      });
      pool.appendChild(btn);
    });

    card.appendChild(pool);
    card.appendChild(sorted);
  }

  // ── Navigation ─────────────────────────
  btnPrev.addEventListener("click", () => {
    if (current > 0) showCard(current - 1);
  });

  btnNext.addEventListener("click", () => {
    if (current >= questions.length) return;

    if (!checked[current]) {
      // Check answer first
      const isCorrect = checkAnswer(current);
      checked[current] = true;
      if (isCorrect) score++;
      showFeedback(isCorrect, () => {
        if (current < questions.length - 1) {
          showCard(current + 1);
        } else {
          showSummary();
        }
      });
    } else {
      // Already checked, just navigate
      if (current < questions.length - 1) {
        showCard(current + 1);
      } else {
        showSummary();
      }
    }
  });

  // ── Check answer logic ─────────────────
  function checkAnswer(idx) {
    const q = questions[idx];
    const card = cardArea.querySelector(`.card[data-index="${idx}"]`);
    const userAns = answers[idx];

    if (q.type === "vocab" || q.type === "radio" || q.type === "select") {
      const correct = norm(q.answer) === norm(userAns || "");
      card.querySelectorAll(".opt-btn").forEach(btn => {
        if (norm(btn.textContent) === norm(q.answer)) btn.classList.add("correct");
        else if (btn.classList.contains("selected")) btn.classList.add("wrong");
        btn.style.pointerEvents = "none";
      });
      return correct;
    }

    if (q.type === "synonym") {
      const answerSet = new Set(q.answer.map(norm));
      const userSet = new Set([...(userAns || [])].map(norm));
      const correct = answerSet.size === userSet.size && [...answerSet].every(a => userSet.has(a));
      card.querySelectorAll(".opt-btn").forEach(btn => {
        const v = norm(btn.textContent);
        if (answerSet.has(v) && userSet.has(v)) btn.classList.add("correct");
        else if (answerSet.has(v) && !userSet.has(v)) btn.classList.add("missed");
        else if (!answerSet.has(v) && userSet.has(v)) btn.classList.add("wrong");
        btn.style.pointerEvents = "none";
      });
      return correct;
    }

    if (q.type === "wordbank") {
      const slots = card.querySelectorAll(".wb-slot");
      let allCorrect = true;
      q.sentences.forEach((s, si) => {
        const correct = norm(userAns?.[si] || "") === norm(s.answer);
        slots[si].classList.add(correct ? "correct" : "wrong");
        if (!correct) {
          allCorrect = false;
          slots[si].textContent = s.answer; // Show correct answer
        }
      });
      card.querySelectorAll(".wb-word").forEach(b => b.style.pointerEvents = "none");
      card.querySelectorAll(".wb-slot").forEach(s => s.style.pointerEvents = "none");
      return allCorrect;
    }

    if (q.type === "order") {
      const correct = q.correctOrder.length === (userAns || []).length &&
        q.correctOrder.every((item, i) => norm(item) === norm(userAns[i]));
      const sortedEl = card.querySelector(".order-sorted");
      sortedEl.querySelectorAll(".order-item").forEach((el, i) => {
        if (norm(el.textContent) === norm(q.correctOrder[i])) el.classList.add("correct");
        else el.classList.add("wrong");
        el.style.pointerEvents = "none";
      });
      card.querySelector(".order-pool").querySelectorAll(".order-item").forEach(el => {
        el.style.pointerEvents = "none";
      });
      return correct;
    }

    return false;
  }

  function norm(s) { return (s || "").trim().toLowerCase(); }

  // ── Feedback flash ─────────────────────
  function showFeedback(isCorrect, callback) {
    feedbackInner.className = "feedback-inner " + (isCorrect ? "is-correct" : "is-wrong");
    feedbackInner.textContent = isCorrect ? "Correct!" : "Not quite...";
    feedbackEl.classList.add("show");
    setTimeout(() => {
      feedbackEl.classList.remove("show");
      callback();
    }, 1200);
  }

  // ── Show/hide cards ────────────────────
  function showCard(idx) {
    current = idx;
    cardArea.querySelectorAll(".card").forEach(c => c.classList.remove("active"));
    cardArea.querySelector(`.card[data-index="${idx}"]`).classList.add("active");
    btnPrev.disabled = idx === 0;
    btnNext.textContent = idx === questions.length - 1 ? "Finish" : "Next \u2192";
    btnNext.disabled = false;
    progress.textContent = `${idx + 1} / ${questions.length}`;
  }

  function showSummary() {
    current = questions.length; // past last
    cardArea.querySelectorAll(".card").forEach(c => c.classList.remove("active"));
    summaryCard.classList.add("active");
    summaryCard.querySelector(".score-big").textContent = `${score} / ${questions.length}`;
    btnNext.disabled = true;
    btnPrev.disabled = true;
    progress.textContent = "Done!";
  }

  function restart() {
    location.reload();
  }
});
