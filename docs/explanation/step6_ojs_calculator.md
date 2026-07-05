# Step 6 — The interactive ROI calculator (Observable JS)

> Beginner explainer for **Task 6** of `docs/final_plan.md`.
> New words are defined the first time they appear; the full list lives in
> [`GLOSSARY.md`](./GLOSSARY.md). Goal: after reading this you could rebuild the calculator yourself.

---

## 1. Big Picture — why this step exists

The Quarto report from Step 5 tells the ROI story with **one fixed scenario**: offer $50, 30% success,
12-month horizon, contact the top 20%. But those four numbers are *assumptions*, not measured facts. A
sharp reviewer immediately asks: *"what if the offer costs more?"* or *"what if only 15% are actually
saved?"*

A static chart can't answer that — you'd have to re-run `analysis.py` for every "what if." So this step
turns the fixed scenario into a **live calculator**: four sliders the reader drags, and the customers
saved / net benefit / ROI recompute instantly in their browser.

The clever part: **no server is involved.** The heavy work (training the model, ranking 100,000
customers) was already done offline and boiled down to a small table of numbers (`data.json`). The
calculator only does *arithmetic* on that table, which a browser can do in microseconds. So the "app"
is just a static web page — free to host, nothing to break, no secrets.

> **Key idea:** precompute the expensive stuff offline; ship only the cheap arithmetic to the browser.
> That is how you get an "interactive demo" without a backend.

---

## 2. Core concepts, explained simply

- **Observable JS (OJS)** — a flavour of JavaScript built into Quarto for making interactive web pages.
  Its superpower is **reactivity**: it works like a spreadsheet. If cell B says `=A+1`, changing A
  updates B automatically. In OJS, if one cell reads a slider, it *re-runs itself* the instant you move
  that slider — you never write "when the slider changes, do X" by hand.

- **`viewof` — a slider that is also a variable.** Writing
  `viewof success_rate = Inputs.range(...)` does two things at once: it puts a slider on the page **and**
  makes `success_rate` a normal variable holding the slider's current value. Any cell that mentions
  `success_rate` is now wired to that slider.

- **`FileAttachment(...).json()`** — how an OJS page reads a local file. We use it to load `data.json`
  (the gains curve + default assumptions) into the page. Because the report is built with
  `embed-resources: true`, Quarto **inlines** that JSON straight into the HTML — so the finished
  `index.html` is one self-contained file that works with no network at all.

- **The gains curve (`data.json`)** — a 100-row table. Row *k* answers: *"if I contact the top k% by
  risk, how many customers do I contact (`contacted_full`), how many churners do I catch
  (`churners_caught_full`), and what's their average monthly revenue (`arpu_caught`)?"* Everything the
  calculator shows is arithmetic on one row of this table.

- **`Plot`** — Observable's charting library (bundled into Quarto). `Plot.line` draws the curve,
  `Plot.dot` marks your current choice, `Plot.ruleY([0])` draws the break-even line at $0.

- **`d3.format`** — a number-formatting helper. `d3.format("$,.0f")(2074033)` → `"$2,074,033"`
  (dollar sign, thousands commas, no decimals). Saves us writing formatting by hand.

---

## 3. File-by-file — what changed and why

### `reports/quarto/index.qmd` — the report page (before → after)

The old file ended the ROI section with a `callout-tip` box that literally said *"Coming next:
sliders…"* — a promise. This step **replaces that placeholder** with a working
`## Interactive ROI calculator` section made of OJS cells:

1. **One data cell** — `data = FileAttachment("data.json").json()` loads the aggregates.
2. **Four slider cells** — `viewof offer_cost / success_rate / horizon_months / target_fraction`, each
   seeded with the report's default from `data.defaults` so the page opens on the headline scenario.
3. **Two function cells** — `rowAt(t)` picks the gains-curve row nearest a target fraction; `economics(...)`
   turns one set of assumptions into the full result. **`economics` mirrors `analysis.py:305-320`
   exactly** — same formulas, so the browser and the Python pipeline can never disagree:

   ```
   saved   = churners_caught * success_rate
   revenue = saved * arpu * horizon_months
   cost    = contacted * offer_cost
   net     = revenue - cost
   roi     = net / cost
   ```
4. **One result-cards cell** — a grid of six live boxes; the "Net benefit" box turns **red** if the
   campaign loses money, green if it profits.
5. **One chart cell** — `Plot` draws net benefit ($M) across *every* targeting depth for the current
   slider settings, with a red dot on your chosen fraction. Drag any slider and the whole curve redraws.

Nothing else in the report changed — the narrative, figures, and tables from Step 5 are untouched.

### `reports/quarto/data.json` — unchanged, but now doing double duty

Step 5 already exported this file (the full gains curve + defaults). Step 6 adds **no new data** — it
just proves the export was designed right: the calculator needs exactly `contacted_full`,
`churners_caught_full`, and `arpu_caught` per fraction, which are already there.

---

## 4. Issues hit while building

### Issue #1 — "will the sliders survive a self-contained render?"
- **What happened (the worry):** with `embed-resources: true`, Quarto crushes the whole report into one
  HTML file. Would the OJS runtime and the JSON still be inside it, or would the calculator quietly load
  nothing once the page left our machine?
- **Why it matters:** if `FileAttachment` resolved to a *path* instead of inlined *content*, the
  deployed page would show empty sliders — broken in front of a recruiter.
- **How we checked:** after `quarto render`, we grepped the built `_site/index.html` and confirmed the
  OJS runtime scripts, the slider variable names, **and** the `data.json` contents (`total_churners_full`,
  `churners_caught_full`) were all physically inside the 3.3 MB self-contained file.
- **Lesson (transferable):** an interactive page has two truths — *"it rendered"* and *"the interactive
  bits are actually embedded."* Verify the second by inspecting the built artifact, not just the render
  log. A clean render log does **not** prove the JavaScript has data to run on.

### Issue #2 — keeping the browser math honest against the Python
- **What happened:** the calculator re-implements the ROI formula in JavaScript. Two copies of a formula
  can drift apart silently.
- **How we solved it:** we hard-mirrored `analysis.py:305-320` line for line, then did a one-off check —
  at the default sliders the JS returns **$2,074,033 net / 2.1× ROI**, matching the report's locked
  headline. If it hadn't matched, the JS formula (or the JSON export) would be wrong.
- **Lesson (transferable):** whenever the same calculation lives in two languages, pin them together with
  a shared reference value. Reproduce one known-good number in both, and you've caught 90% of drift.

---

## 5. Where things stand + what's next

**Done and verified.** The Quarto report now carries a live, browser-only ROI calculator: four sliders →
six live result cards + a reactive net-benefit curve, all arithmetic on the precomputed gains curve, all
self-contained in one HTML file. The default scenario reproduces the locked headline ($2.07M / 2.1×).

**Next up — Task 7 (the last step):** commit the Task 2–6 work, push the public GitHub repo, then
`quarto publish gh-pages` to put the report online and pin its URL at the top of `README.md`.
