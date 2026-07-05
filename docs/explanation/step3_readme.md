# Step 3 — Writing the `README.md`

## 1. Big Picture — why this step exists

The README is the **front door** of the repo. Most recruiters and reviewers read *only* this file —
they decide in ~30 seconds whether the project is worth a closer look. A great analysis with no README
looks like an unfinished pile of scripts; the same analysis with a clear README reads as "this person
can communicate results to a business audience," which is the actual job of a Data Analyst.

So the README is not documentation-as-afterthought — it's the **highest-leverage hour** in the whole
project. Its job is to answer, fast: *what is this, does it work, what did it find, and can I trust the
numbers?*

## 2. Core concepts, explained simply

- **README** — the file GitHub auto-renders on a repo's landing page. Written in **Markdown** (`.md`),
  a plain-text format where `#` = heading, `|...|` = table, `![alt](path)` = embedded image.
- **The "inverted pyramid"** — put the conclusion first. A reviewer should get the headline result in
  the first screen (the TL;DR table), *then* optionally read the how and why below. This is the
  opposite of how you *did* the work (data → model → result), and it's deliberate.
- **Relative image paths** — `![](reports/figures/10_cumulative_gains.png)` points to a file *inside
  the repo*. GitHub renders it inline. Relative (not absolute `C:\...`) paths are essential so the
  images work for anyone who clones the repo, on any machine.
- **Reproducibility block** — the copy-paste "How to run" section. If a reviewer can't rebuild your
  results in four commands, the project isn't really reproducible, no matter how good the code is.
- **The honesty box** — an explicit statement of what's *measured* vs *projected*. Counterintuitively,
  admitting the model is "modest" (AUC 0.70) and the ROI is "projected" makes the project **more**
  credible, not less — it signals you understand the difference, which is exactly what separates an
  analyst from someone quoting numbers they can't defend.

## 3. File-by-file — what changed

**`README.md`** — went from a 2-line stub (a duplicated title) to a full front-door document. Sections,
and the purpose of each:

| Section | Why it's there |
|---|---|
| Title + one-line pitch | Tells a skimmer what the project *does* in one sentence. |
| Live links row | Deck + (soon) live report — the "clickable proof" recruiters want. |
| **TL;DR results table** | The inverted pyramid — the three headline numbers, up top, framed as questions a business would ask. |
| Business problem | Frames it as *value-weighted targeting*, not just "predict churn" — the DA angle. |
| Data | Scale (100K × 2 tables) + the licensing note (raw data not shipped). |
| **How to run** | Copy-paste reproducibility, now referencing the venv + `requirements.txt` from Task 2. |
| Approach | The 5-step method, so a reviewer sees the workflow without reading code. |
| Key results | The **3 embedded figures** the plan specifies (cumulative gains, churn-by-equipment, model comparison). |
| Assumptions | The four ROI inputs, stated openly and linked to the full assumptions doc. |
| Repo structure | The clean Cookiecutter-style tree from Task 1.5, so the layout reads as intentional. |
| **Honesty & provenance** | Real-vs-projected, and the GCI-assignment origin — the credibility anchor. |
| Tech stack | Fast skim of the toolset; links back to the pinned requirements. |

**The numbers are locked, not invented.** Every figure in the README (AUC 0.70, 79.5% top decile, ~30%
of churners in the top 20%, $3.07M / $2.07M / 2.1×, $58 ARPU, the $50 / 30% / 12-mo assumptions) comes
straight from the "locked headline numbers" in `docs/final_plan.md §5`, which trace back to the real
pipeline output. A README must never introduce a number the analysis can't reproduce.

**The 3 embedded figures** were chosen deliberately:
- `10_cumulative_gains.png` — the DA headline (targeting power).
- `04_churn_by_eqp_decile.png` — the single most convincing driver (churn rises with equipment age).
- `06_model_comparison.png` — evidence the model choice was earned, not assumed.

## 4. Issues hit while building

- **Empty `reports/` glob → had to list the real tree.** My first search for the figures
  (`reports/**/*`) returned "No files found," which looked alarming.
  - **What happened:** the glob pattern didn't match, so it *looked* like the figures were missing.
  - **Why:** a matching-tool quirk, not a real absence — a direct file listing immediately showed all
    11 PNGs plus `slides.pdf` present.
  - **Transferable lesson:** when one search says "nothing here," confirm with a second method before
    concluding a file is missing. Absence of evidence isn't evidence of absence — especially with glob
    patterns.
- **Placeholders for things that don't exist yet.** The public GitHub repo URL and the live Quarto
  report URL are created in **Task 7**, so they can't be real links yet.
  - **How it's handled:** the live-report line is marked _"coming soon (Task 7)"_ rather than faking a
    dead link. **A broken link in a README is worse than an honest "coming soon."**
  - **To finish later:** swap in the real Quarto URL after `quarto publish gh-pages`, and pin it at the
    very top.

## 5. Where things stand & what's next

- **Done:** a complete, honest, reviewer-ready `README.md` with the locked numbers, 3 embedded figures,
  reproducible run steps, and an explicit honesty box.
- **One placeholder pending Task 7:** the live Quarto report URL (and, optionally, a repo badge row)
  once the site is published.
- **Next (Task 4):** clean up `docs/REFERENCES_AND_ASSUMPTIONS.md` — resolve or remove the `[CITE]`
  markers and any "fill before submitting" language so no internal to-do leaks into the public repo.
