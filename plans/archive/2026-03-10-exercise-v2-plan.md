# Exercise v2 Prototype Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build p.95 exercise page as an interactive, one-question-at-a-time quiz optimized for landscape tablet.

**Architecture:** Single HTML page with embedded quiz data as JSON. A shared `quiz-engine.js` handles navigation, answer checking, and 6 question types. `style-v2.css` provides landscape-first card layout. New files — do not modify v1.

**Tech Stack:** Vanilla HTML/CSS/JS, zero dependencies.

**Design Doc:** `docs/plans/2026-03-10-exercise-v2-design.md`

---

### Task 1: Create `docs/exercises/style-v2.css`

**Files:**
- Create: `docs/exercises/style-v2.css`

**Step 1: Write the CSS file**

Landscape-first card layout:

```css
/* ── Reset & Base ─────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 20px;
  line-height: 1.5;
  margin: 0;
  padding: 0;
  background: #f8f9fa;
  color: #1a1a1a;
  /* Landscape: fill viewport height */
  height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* No scrolling — one card at a time */
}

/* ── Header ───────────────────────────── */
.quiz-header {
  padding: 0.8rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}
.quiz-header h1 { font-size: 1.1rem; margin: 0; }
.quiz-header .back { color: #7c3aed; text-decoration: none; font-size: 0.95rem; }
.section-label {
  font-size: 0.8rem;
  color: #7c3aed;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

/* ── Card area (fills remaining space) ── */
.card-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  overflow-y: auto;
}

.card {
  display: none; /* JS shows active card */
  width: 100%;
  max-width: 800px;
  background: #fff;
  border-radius: 16px;
  padding: 2rem 2.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.card.active { display: block; }

.card .prompt {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

/* ── Option buttons (single/multi select) */
.options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}
.options .opt-btn {
  padding: 0.8rem 1.6rem;
  font-size: 1.1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  transition: all 0.15s;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}
.opt-btn:active { transform: scale(0.97); }
.opt-btn.selected {
  background: #f3f0ff;
  border-color: #7c3aed;
  color: #7c3aed;
  font-weight: 600;
}
.opt-btn.correct {
  background: #ecfdf5 !important;
  border-color: #10b981 !important;
  color: #065f46 !important;
}
.opt-btn.wrong {
  background: #fef2f2 !important;
  border-color: #ef4444 !important;
  color: #991b1b !important;
}
.opt-btn.missed {
  /* Correct answer the user didn't pick */
  background: #ecfdf5 !important;
  border-color: #10b981 !important;
  color: #065f46 !important;
  opacity: 0.7;
}
.opt-btn.disabled { pointer-events: none; opacity: 0.5; }

/* ── Word Bank ────────────────────────── */
.word-bank {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}
.word-bank .wb-word {
  padding: 0.6rem 1.2rem;
  font-size: 1.05rem;
  border: 2px solid #7c3aed;
  border-radius: 10px;
  background: #f3f0ff;
  color: #7c3aed;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.15s;
}
.wb-word.used {
  opacity: 0.3;
  pointer-events: none;
  border-color: #ccc;
  color: #999;
  background: #f9fafb;
}
.wb-sentences { display: flex; flex-direction: column; gap: 0.8rem; }
.wb-sentence {
  font-size: 1.05rem;
  line-height: 1.6;
}
.wb-slot {
  display: inline-block;
  min-width: 100px;
  padding: 0.3rem 0.8rem;
  border-bottom: 2px solid #7c3aed;
  text-align: center;
  cursor: pointer;
  font-weight: 600;
  color: #7c3aed;
  transition: background 0.15s;
  border-radius: 4px;
}
.wb-slot:empty { color: transparent; }
.wb-slot:empty::after { content: "___"; color: #ccc; font-weight: 400; }
.wb-slot.correct { background: #ecfdf5; border-color: #10b981; color: #065f46; }
.wb-slot.wrong { background: #fef2f2; border-color: #ef4444; color: #991b1b; }

/* ── Order (click-to-sort) ────────────── */
.order-pool, .order-sorted {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  min-height: 3rem;
}
.order-sorted { margin-top: 1rem; border-top: 2px dashed #e5e7eb; padding-top: 1rem; }
.order-item {
  padding: 0.7rem 1.2rem;
  font-size: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  transition: all 0.15s;
}
.order-item:active { transform: scale(0.98); }
.order-sorted .order-item {
  border-color: #7c3aed;
  background: #f3f0ff;
}
.order-sorted .order-item::before {
  font-weight: 700;
  color: #7c3aed;
  margin-right: 0.5rem;
}
.order-sorted .order-item:nth-child(1)::before { content: "\u2460 "; }
.order-sorted .order-item:nth-child(2)::before { content: "\u2461 "; }
.order-sorted .order-item:nth-child(3)::before { content: "\u2462 "; }
.order-sorted .order-item:nth-child(4)::before { content: "\u2463 "; }
.order-item.correct { background: #ecfdf5 !important; border-color: #10b981 !important; }
.order-item.wrong { background: #fef2f2 !important; border-color: #ef4444 !important; }

/* ── Feedback overlay ─────────────────── */
.feedback {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.15);
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.feedback.show { display: flex; }
.feedback-inner {
  background: #fff;
  border-radius: 20px;
  padding: 2rem 3rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}
.feedback-inner.is-correct { color: #059669; }
.feedback-inner.is-wrong { color: #dc2626; }

/* ── Nav bar ──────────────────────────── */
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 1.5rem;
  background: #fff;
  border-top: 1px solid #e5e7eb;
  flex-shrink: 0;
}
.nav-bar button {
  padding: 0.7rem 1.8rem;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}
.nav-bar .btn-prev { background: #e5e7eb; color: #374151; }
.nav-bar .btn-next { background: #7c3aed; color: #fff; }
.nav-bar .btn-prev:disabled,
.nav-bar .btn-next:disabled { opacity: 0.3; pointer-events: none; }
.nav-bar .progress { font-size: 1rem; color: #6b7280; font-weight: 600; }

/* ── Summary card ─────────────────────── */
.summary { text-align: center; }
.summary .score-big {
  font-size: 3rem;
  font-weight: 800;
  color: #7c3aed;
  margin: 1rem 0;
}
.summary .btn-restart {
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  background: #7c3aed;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

/* ── Responsive: portrait fallback ────── */
@media (max-width: 768px) {
  body { font-size: 17px; }
  .card { padding: 1.5rem; }
  .card .prompt { font-size: 1.15rem; }
  .card-area { padding: 0.8rem 1rem; }
}
```

**Step 2: Commit**

```bash
git add docs/exercises/style-v2.css
git commit -m "feat: add v2 exercise stylesheet (landscape, card-based)"
```

---

### Task 2: Create `docs/exercises/quiz-engine.js`

**Files:**
- Create: `docs/exercises/quiz-engine.js`

**Step 1: Write the quiz engine**

The engine reads quiz data from a `<script id="quiz-data" type="application/json">` block in the HTML. It handles 6 question types: `vocab`, `synonym`, `wordbank`, `radio`, `order`, `select`.

```javascript
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

  // ── Multi select (synonym — pick 2) ──
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
          answers[idx].delete(opt);
          btn.classList.remove("selected");
        } else {
          if (answers[idx].size >= (q.pick || 2)) {
            // Deselect oldest
            const first = [...answers[idx]][0];
            answers[idx].delete(first);
            opts.querySelector(`.opt-btn.selected`).classList.remove("selected");
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
    btnNext.textContent = idx === questions.length - 1 ? "Finish" : "Next →";
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
    current = 0;
    score = 0;
    answers = new Array(questions.length).fill(null);
    checked = new Array(questions.length).fill(false);
    // Remove all cards and rebuild
    cardArea.innerHTML = "";
    // Re-run build (simplest: reload page)
    location.reload();
  }
});
```

**Step 2: Commit**

```bash
git add docs/exercises/quiz-engine.js
git commit -m "feat: add quiz engine v2 (6 question types, one-at-a-time)"
```

---

### Task 3: Create `docs/exercises/95_v2.html`

**Files:**
- Create: `docs/exercises/95_v2.html`

**Step 1: Write the HTML with embedded quiz data**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Exercise: The Skunks' Present</title>
  <link rel="stylesheet" href="style-v2.css">
</head>
<body>
  <div class="quiz-header">
    <a class="back" href="index.html">&larr; Back</a>
    <h1>The Skunks' Present</h1>
  </div>

  <div class="card-area"></div>

  <div class="feedback"><div class="feedback-inner"></div></div>

  <div class="nav-bar">
    <button class="btn-prev" disabled>&larr; Prev</button>
    <span class="progress">1 / 12</span>
    <button class="btn-next">Next &rarr;</button>
  </div>

  <script id="quiz-data" type="application/json">
  {
    "title": "The Skunks' Present",
    "questions": [
      {
        "type": "vocab",
        "section": "Knowing the Words",
        "prompt": "Black and white animal (Par. 1)",
        "options": ["skunk", "insects", "flag", "bush", "bunny"],
        "answer": "skunk"
      },
      {
        "type": "vocab",
        "section": "Knowing the Words",
        "prompt": "Small animals such as bees and ants (Par. 3)",
        "options": ["insects", "skunk", "flag", "bush", "bunny"],
        "answer": "insects"
      },
      {
        "type": "synonym",
        "section": "Knowing the Words",
        "prompt": "Pick the two synonyms:",
        "options": ["begin", "stop", "call", "start"],
        "answer": ["begin", "start"],
        "pick": 2
      },
      {
        "type": "synonym",
        "section": "Knowing the Words",
        "prompt": "Pick the two synonyms:",
        "options": ["bird", "rabbit", "skunk", "bunny"],
        "answer": ["rabbit", "bunny"],
        "pick": 2
      },
      {
        "type": "synonym",
        "section": "Knowing the Words",
        "prompt": "Pick the two synonyms:",
        "options": ["listen", "catch", "see", "look"],
        "answer": ["see", "look"],
        "pick": 2
      },
      {
        "type": "synonym",
        "section": "Knowing the Words",
        "prompt": "Pick the two synonyms:",
        "options": ["run", "car", "hurry", "dog"],
        "answer": ["run", "hurry"],
        "pick": 2
      },
      {
        "type": "wordbank",
        "section": "Learning to Study",
        "prompt": "Fill in the blanks using the words above:",
        "words": ["patch", "skunk", "bee", "turn", "flag", "bush"],
        "sentences": [
          { "text": "On my way to the carrot ___ one morning...", "answer": "patch" },
          { "text": "Behind her were six little ___s, waving their tails.", "answer": "skunk" },
          { "text": "We are on our way to look for insects like ___s and ants.", "answer": "bee" },
          { "text": "I heard an angry growl. I ___ed around.", "answer": "turn" }
        ]
      },
      {
        "type": "wordbank",
        "section": "Learning to Study",
        "prompt": "Fill in the blanks using the words above:",
        "words": ["carrot", "growl", "happen", "safe", "branches", "morning"],
        "sentences": [
          { "text": "On my way to the ___ patch one morning...", "answer": "carrot" },
          { "text": "I heard an angry ___ behind me.", "answer": "growl" },
          { "text": "The branches will keep us ___.", "answer": "safe" },
          { "text": "I should have guessed what would ___.", "answer": "happen" }
        ]
      },
      {
        "type": "radio",
        "section": "Reading and Thinking",
        "prompt": "What is the story mostly about?",
        "options": [
          "how rabbits hide under berry bushes",
          "a frightened dog",
          "how skunks keep safe"
        ],
        "answer": "how skunks keep safe"
      },
      {
        "type": "order",
        "section": "Reading and Thinking",
        "prompt": "Tap the sentences in the order they happened:",
        "items": [
          "The skunks danced.",
          "Uncle Bunny heard a growl.",
          "The dog ran away.",
          "Uncle Bunny met the skunks."
        ],
        "correctOrder": [
          "Uncle Bunny met the skunks.",
          "Uncle Bunny heard a growl.",
          "The skunks danced.",
          "The dog ran away."
        ]
      },
      {
        "type": "select",
        "section": "Reading and Thinking",
        "prompt": "We heard the band and wanted to ___.",
        "options": ["read", "dance", "believe"],
        "answer": "dance"
      },
      {
        "type": "select",
        "section": "Reading and Thinking",
        "prompt": "The dog ___ at the loud noise.",
        "options": ["growled", "worked", "laughed"],
        "answer": "growled"
      }
    ]
  }
  </script>
  <script src="quiz-engine.js"></script>
</body>
</html>
```

**Step 2: Commit**

```bash
git add docs/exercises/95_v2.html
git commit -m "feat: add p.95 exercise v2 prototype"
```

---

### Task 4: Push and verify

**Step 1: Push**

```bash
git push
```

**Step 2: Verify locally**

Open `docs/exercises/95_v2.html` in browser. Check:
- Landscape layout fills viewport
- One card visible at a time
- All 6 question types work (vocab, synonym, wordbank, radio, order, select)
- Next → checks answer, shows feedback, advances
- Prev ← navigates back (already-checked cards show results)
- Word bank: click word fills slot, click slot returns word
- Order: click sentence moves to sorted, click sorted returns
- Summary shows score at end
- Try Again resets

**Step 3: Report completion**

Report which question types work and any issues found.
