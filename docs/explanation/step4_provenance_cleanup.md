# Step 4 — Cleaning up provenance artifacts

## 1. Big Picture — why this step exists

The analysis was originally built as a graded **submission** (GCI World 2026 / Omnicampus). So its
supporting files were written for a grader: "fill before submitting," "Omnicampus requires the
References field," "rubric requirement 3," and `[CITE]` placeholders waiting to be replaced.

None of that belongs in a **public portfolio repo**. To an outside reviewer, a leftover internal to-do
reads as "this person forgot to finish" — it quietly undercuts an otherwise solid project. Task 4
strips that submission scaffolding so the public version looks intentional and complete, and — just as
important — so it stays **honest**: no unsourced claim is left dressed up as if it had a citation.

## 2. Core concepts, explained simply

- **Provenance** — the origin/history of the work: where the data came from, what the project was
  built for. Stating it honestly (a GCI assignment, not consulting work) is good practice. Leaking the
  *grading mechanics* of that provenance (rubric numbers, submission-portal instructions) is not.
- **`[CITE]` marker** — a placeholder meaning "a real citation goes here later." Shipping it unresolved
  is the tell that a claim is unsupported.
- **The cardinal rule: never fabricate a citation.** Inventing a source to silence a `[CITE]` is
  dishonest and easily exposed. There are only three legitimate options for an unsourced claim:
  1. **Cut it.**
  2. **Find a real, verifiable source.**
  3. **Relabel it honestly** as an assumption / unverified context.
- **Assumption vs. measurement** — a *measured* number comes from the data (e.g. ROC-AUC 0.70 on the
  test set). An *assumption* is a planning input you chose (e.g. "$50 offer cost"). The honest way to
  ship an assumption is to (a) label it as one and (b) show a **sensitivity analysis** proving the
  conclusion survives reasonable changes to it — which this project already has (`11_sensitivity.png`).

## 3. File-by-file — what changed

**`docs/REFERENCES_AND_ASSUMPTIONS.md` — rewritten** (this is a doc, edited directly):
- **Removed** all submission scaffolding: the "fill before submitting" title, the Omnicampus
  References-field instructions, the generative-AI-chat-URL requirement, and "rubric requirement 3."
- **Cut** the three market-context claims ("acquisition costs more than retention," "mature markets
  grow via retention," "local market picture"). They needed sources we won't fabricate, and they were
  submission-narrative rather than part of the analysis — so, by decision, cut for the public version.
- **Kept and reframed** the four business-case assumptions as clearly-labeled assumptions, explicitly
  pointing at the sensitivity chart as their defense. Removed both `[CITE]` markers this way — not by
  inventing sources, but by honestly calling the numbers assumptions.
- **Kept** the two real method citations (XGBoost = Chen & Guestrin 2016 KDD; scikit-learn =
  Pedregosa et al. 2011 JMLR) — these are genuine and verifiable.
- **Kept** the measured model results and the truthful GCI-dataset provenance + licensing note.

**`src/build_notebook.py` (line 335) — one phrase removed** (this is *app code*, so per the project
rules the change is handed over for the human to paste, not edited directly):
- `"...explicitly (rubric requirement 3) and inspect"` → `"...explicitly, and inspect"`.
- Then `python src/build_notebook.py` is re-run so the change flows into the generated
  `notebooks/churn_analysis.ipynb`. The notebook is an **artifact**, never hand-edited — you fix the
  script and regenerate.

**Left as-is on purpose:** the `Omnicampus: LavudyaAkhil31 · GCI World 2026` tag on the slide title
(`make_slides.py:115`). Per the plan (§7) this is truthful personal provenance — keeping it is honest,
not a leak. The line between "honest provenance" (keep) and "grading mechanics" (cut) is the whole
judgment call of this step.

## 4. Issues hit while building

- **A grep for the to-do language matched six files — most were false alarms.**
  - **What happened:** searching for `[CITE]` / `Omnicampus` / `rubric` lit up `final_plan.md`,
    `extract.md`, `step3_readme.md`, `make_slides.py`, `build_notebook.py`, and the notebook.
  - **Why:** the *planning/audit docs* legitimately **discuss** these markers (that's their job —
    describing the cleanup task); only the *shipped artifacts* actually **contain** them as content.
  - **How it was resolved:** inspected each hit in context. The docs' mentions are meta and fine; the
    only real leak was "(rubric requirement 3)" living in the notebook's own text.
  - **Transferable lesson:** a search hit is a *lead*, not a verdict. Read each match in context — a
    file that *talks about* a problem is different from a file that *has* it.

## 5. Where things stand & what's next

- **Done:** `REFERENCES_AND_ASSUMPTIONS.md` is now a clean, honest public reference (assumptions
  labeled, real citations kept, unsourced market claims cut, submission scaffolding gone).
- **One human action pending:** apply the one-line `build_notebook.py` edit and re-run it to refresh
  `churn_analysis.ipynb`.
- **Next (Task 5):** build the Quarto report (`index.qmd`) that tells the story from the existing
  figures, plus the `data.json` of precomputed aggregates the ROI calculator will read.
