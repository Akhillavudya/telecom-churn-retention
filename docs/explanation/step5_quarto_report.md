# Step 5 — Building the Quarto report

## 1. Big Picture — why this step exists

Everything so far produced *artifacts* (figures, a notebook, a deck) but nothing a stranger can open in
a browser. This step turns the analysis into a **published, recognizable analytics report website** —
the portfolio-diversifying centerpiece (`final_plan.md §0`). A business proposal *is* a report, so a
Quarto report is the honest, native format for it (not a shoehorned app). It's also a fresh tool on the
CV: Quarto + a static host, not used anywhere else in the portfolio.

This step builds the **static report**; the live interactive calculator is Step 6 (Task 6).

## 2. Core concepts, explained simply

- **Quarto** — a free command-line publishing tool. You write a `.qmd` file (Markdown + optional code +
  narrative), run `quarto render`, and it produces a polished HTML site (or PDF). Think "Markdown that
  can run code and publish a website."
- **`.qmd` file** — the source: a **YAML front-matter** block at the top (title, date, options between
  `---` fences) followed by Markdown body. Ours is pure narrative + images — it does **not** re-run the
  pipeline, so rendering is instant and needs no data or model. The heavy compute already happened in
  `analysis.py`; the report just tells the story with the outputs.
- **`_quarto.yml`** — project-level config (theme, table of contents, output folder) that applies to
  every `.qmd` in the folder, so you set it once.
- **`embed-resources: true`** — the key choice here. It **inlines every asset** (images as base64 text,
  CSS, JS) into a **single self-contained `index.html`**. No `figures/` folder to ship alongside, no
  broken-image risk on the host. We confirmed it: 6 images inlined, 0 external references.
- **`data.json`** — a small precomputed dataset the (Step 6) calculator reads in the browser. Exporting
  aggregates once, offline, is what lets the "live" calculator run with **no server and no model
  hosting** — it's just arithmetic on numbers we baked ahead of time.
- **Cumulative-gains curve** — "if I contact the top X% by risk, what fraction of churners do I catch?"
  Exporting the *whole curve* (not one point) is what will let the calculator's `target_fraction`
  slider move — see the data-shape note below.

## 3. File-by-file — what changed

**`src/analysis.py` — added a JSON export block** (app code; edited directly this session with your
go-ahead). After the business-impact section (where the risk-sorted `order` table already exists), it
writes `reports/quarto/data.json`. Keeping the export *inside* the same pipeline means the JSON numbers
can never drift from the printed headline numbers — one source of truth. Also added `import json`.

  - **Why the whole curve, not four numbers?** The plan lists four aggregates
    (`churners_caught_full`, `arpu_target`, `contacted_full`, baseline cost) — but those are frozen at
    "top 20%." The Step-6 calculator has a **`target_fraction` slider**, and at 15% or 30% the churners
    caught and their ARPU are *different*. So the export walks 100 points of the gains curve (1%→100%
    contacted), each with `contacted_full`, `churners_caught_full`, and `arpu_caught`. The calculator
    interpolates at whatever fraction you choose. The 20% row still reproduces the locked numbers
    exactly (20,000 / 14,730 / $57.97 → $3.07M / $2.07M / 2.1×) — verified.

**`reports/quarto/_quarto.yml` — new.** Project config: `cosmo` theme, left-hand table of contents,
`embed-resources: true` for the single-file output.

**`reports/quarto/index.qmd` — new.** The report itself, following the analyst workflow: headline
callout → business problem → data → churn drivers (figs 03, 04 + decile table) → model comparison
(figs 06, 07) → targeting / cumulative gains (fig 10) → the ROI case (fig 11 + a results table) → a
placeholder callout for the Step-6 calculator → an honesty/provenance section. Figures are referenced
with relative paths (`../figures/*.png`) and inlined at render time.

**`reports/quarto/data.json` — generated** by the `analysis.py` run (not hand-written).

**`reports/quarto/_site/` — generated** by `quarto render` (git-ignored, rebuildable).

## 4. Issues hit while building

- **The Quarto install timed out mid-download.** `winget install` was killed at the 7-minute mark while
  pulling the ~100 MB installer from GitHub.
  - **Why:** a large download over a slow link exceeded the foreground command budget; the kill
    (exit 143) aborted the install before it finished — nothing landed on disk.
  - **Fix:** re-ran it as a **background task**, which has no such budget, and it completed cleanly
    (exit 0, Quarto 1.9.38). Verified with `quarto --version` after refreshing the PATH.
  - **Transferable lesson:** long-running installs/downloads belong in the background, not a
    time-boxed foreground call. Also: after any installer changes your PATH, a **fresh shell** (or a
    manual PATH refresh) is needed before the new command is visible.
- **PATH not updated in the same session.** Right after install, `quarto` wasn't found until the PATH
  was refreshed from the machine/user environment.
  - **Lesson:** installers edit the *persistent* PATH; already-open shells keep their old copy until
    restarted.

## 5. Where things stand & what's next

- **Done:** a self-contained `index.html` report renders from `index.qmd` with all figures inlined, plus
  a verified `data.json` of precomputed aggregates. Preview locally with `quarto preview` in
  `reports/quarto/`, or just open `reports/quarto/_site/index.html`.
- **Next (Task 6):** add the **Observable JS ROI calculator** to `index.qmd` — sliders for offer cost,
  success rate, horizon, and target fraction that read `data.json` and recompute customers saved, net
  benefit, and ROI live, with a reactive chart. Then Task 7: push public + `quarto publish gh-pages`.
