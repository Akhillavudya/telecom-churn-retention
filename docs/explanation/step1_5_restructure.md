# Step 1.5 — Restructuring the project into an industry-standard layout

> Beginner explainer for **Task 1.5** of `docs/final_plan.md`.
> New words are defined the first time they appear; the full list lives in
> [`GLOSSARY.md`](./GLOSSARY.md). Goal: after reading this you could redo the step yourself.

---

## 1. Big Picture — why this step exists

Before this step, **every file lived in one flat folder** — the Python scripts, the notebook, the PDF
slide deck, the raw data files, the 11 chart images, and the planning documents were all piled at the
top level together.

The code *ran* fine like that. So why change it? Because a project isn't just for the computer — it's
for **people**: a recruiter glancing at your GitHub, a teammate, or you in six months. In a flat pile,
nobody can tell at a glance which files are **input data**, which are **code**, and which are
**generated output** (things the code produced and could re-make at any time).

Professional data projects fix this with a **standard folder layout**. There's a well-known template
called *Cookiecutter Data Science* that most data analysts recognise on sight. Using it sends a quiet
signal: *"I've worked in a real codebase before."*

**What this step solved:** made the project readable at a glance — *without changing what it does.*

> **Key idea:** organisation is a feature. The same code in a tidy, conventional structure is worth
> more (to a human reader) than in a messy one.

---

## 2. Core concepts, explained simply

- **Separation of concerns** — a design rule: give each folder *one job*. `data/` = inputs, `src/` =
  code, `reports/` = generated outputs. You never have to guess what a file is, because its folder
  already tells you.

- **Raw vs. generated data.** `data/raw/` holds the *original* input files — you never edit these by
  hand, and (later) you won't even commit them to a public repo. Everything the code *produces*
  (charts, the deck, the notebook) is **regenerable**: you could delete it all and rebuild it by
  re-running the scripts. Regenerable things live apart, under `reports/`.

- **A "path" is a file's address, and relative paths have a starting point.** An *absolute* path starts
  at the drive (`C:\Users\...`). A *relative* path is measured from somewhere — and **which** somewhere
  is the whole ballgame:
  - `Path.cwd()` → the **current working directory** = wherever you *launched* the program from. This
    is fragile: launch the same script from a different folder and the path silently points elsewhere.
  - `Path(__file__)` → the location of **the script itself**. Stable: the script always knows where it
    lives, no matter where you ran it from.

- **`.parent` walks up one folder.** So `Path(__file__).resolve().parent.parent` means "two folders up
  from this script." Because our scripts now sit inside `src/`, two levels up is the **project root** —
  the single anchor we hang every other path off. (`.resolve()` just turns it into a clean absolute
  path first.)

- **matplotlib backend** — the "engine" that turns a chart into pixels. `Agg` **saves image files** and
  opens no window (what a plotting script wants). `TkAgg` opens an interactive **GUI window**. Picking
  the wrong one caused our one real error — see §4.

*(All of these are also in [`GLOSSARY.md`](./GLOSSARY.md) if you want the one-line version.)*

---

## 3. File-by-file — what changed and why

### The folder moves (before → after)

| Before (everything flat) | After (organised) |
|---|---|
| `analysis.py`, `build_notebook.py`, `make_slides.py` | `src/` |
| `telecom/Client.csv`, `telecom/Record.csv` | `data/raw/` |
| `figures/*.png` (×11) | `reports/figures/` |
| `LavudyaAkhil31.pdf` | `reports/slides.pdf` |
| `LavudyaAkhil31.ipynb` | `notebooks/churn_analysis.ipynb` |
| `tutorial.ipynb` | `notebooks/tutorial.ipynb` |
| `final_plan.md`, `extract.md`, `REFERENCES_AND_ASSUMPTIONS.md`, `README.docx` | `docs/` |
| `ENG_Company _A_ Dataset Overview.docx` | `data/data_dictionary_source.docx` |

Two empty folders were created for later tasks: **`data/sample/`** (a small shareable data sample,
Task 1) and **`reports/quarto/`** (the deployable report, Tasks 5–6).

Renames were deliberate: `LavudyaAkhil31.*` → descriptive names (`churn_analysis.ipynb`, `slides.pdf`)
because a stranger should understand a filename without knowing your username.

### `src/analysis.py` — the main pipeline

1. **Re-anchored all paths to the project root.** Added one line —
   `ROOT = Path(__file__).resolve().parent.parent` — then pointed the figures output at
   `ROOT / "reports" / "figures"` and the input CSVs at `ROOT / "data" / "raw"`. This replaced a
   *mixture*: figures had used `Path("figures")` (relative to the working directory — fragile) while
   the CSVs used the script folder. Now **everything** is anchored to the script, so the pipeline gives
   identical output no matter where you launch it.
2. **Forced the `Agg` backend** (`matplotlib.use("Agg")`, placed *before* `import matplotlib.pyplot`) —
   the fix for the error in §4.
3. **Fixed a lying print** that still said `./figures/`; it now prints the real output folder.

### `src/build_notebook.py` — the tricky one

This file *builds a notebook*, so some path text inside it is **code that runs now**, and some is
**text baked into a cell of the notebook it generates**. Those need different fixes:
- Added `ROOT` (and the missing `from pathlib import Path`) for the code that actually runs.
- Pointed the real output write at `ROOT / "notebooks" / "churn_analysis.ipynb"`.
- Changed the *embedded* data path (a string that becomes a cell in the built notebook) from
  `Path.cwd() / "telecom"` to `Path("..") / "data" / "raw"`, so the generated notebook — which lives in
  `notebooks/` — still finds the data one level up.

### `src/make_slides.py` — the deck builder

- Swapped its old `HERE`-based paths for `ROOT`, pointing figures at `reports/figures/` and the deck at
  `reports/slides.pdf`. It **already** used `matplotlib.use("Agg")` — which is exactly how we knew
  `Agg` was the correct fix for `analysis.py`.

---

## 4. Issues hit while building

### Issue #1 — moving files broke the hard-coded paths *(expected — it's the whole point)*
- **What happened:** after the move, the scripts couldn't find `telecom/` or write to `figures/`.
- **Why:** those folder names were **hard-coded** to the old flat layout, and some paths were even
  relative to the *working directory* (`Path.cwd()`) rather than the script — fragile even before we
  moved anything.
- **How we fixed it:** defined one `ROOT = Path(__file__).resolve().parent.parent` and rebuilt every
  path from it (`ROOT / "data" / "raw" / ...`).
- **Lesson (transferable):** never scatter path text through a codebase. Anchor **one** root to
  `__file__` and derive all other paths from it. Then moving folders is a one-line change, and the code
  runs correctly from anywhere.

### Issue #2 — a wall of `tkinter` / `Tcl_AsyncDelete` errors from `analysis.py`
- **What happened:** running `analysis.py` printed dozens of
  `RuntimeError: main thread is not in main loop` and
  `Tcl_AsyncDelete: async handler deleted by the wrong thread` — **even though the charts saved fine and
  the numbers were correct.**
- **Why:** `analysis.py` never chose a matplotlib **backend**, so it defaulted to the *interactive*
  `TkAgg`, which fires up your operating system's Tk GUI toolkit. We only ever *save* charts (never show
  a window), so Tk was started for nothing and then errored while Python shut it down. The proof:
  `make_slides.py` produced **zero** such errors — because it already sets `Agg`.
- **How we fixed it:** added `import matplotlib; matplotlib.use("Agg")` **before** importing `pyplot`.
  Re-running gave perfectly clean output.
- **Lesson (transferable):** any script whose only job is to *save* plots should force the
  non-interactive `Agg` backend, set **before** `import matplotlib.pyplot`. Bonus debugging habit we
  practised: when errors flood the screen, first check whether the *actual work* still succeeded (here,
  the 11 figures) before assuming the whole run failed.

---

## 5. Where things stand + what's next

**Done and verified.** The repo now has a clean, conventional layout (`data/`, `src/`, `notebooks/`,
`reports/`, `docs/`). All three scripts run **end-to-end from any working directory**, and every output
lands in the right folder:

| Script | Produces | Lands in |
|---|---|---|
| `analysis.py` | 11 figures | `reports/figures/` |
| `build_notebook.py` | `churn_analysis.ipynb` (42 cells) | `notebooks/` |
| `make_slides.py` | `slides.pdf` (15 slides) | `reports/` |

The headline numbers are **unchanged** (ROC-AUC ≈ 0.70, top decile 79.5% churn, $3.07M retained, $2.07M
net benefit, 2.1× ROI) — confirming the restructure changed *organisation only*, not results.

**Next up (from `docs/final_plan.md`):**
- **Task 1** — resolve GCI data licensing; add a small `data/sample/` CSV so the pipeline runs even
  without the full (possibly non-shareable) dataset.
- **Task 2** — pin `requirements.txt` to exact library versions + (recommended) create a virtual
  environment.
- **Task 3** — write the real `README.md`.

Each of those will get its own `stepN_*.md` file here as we complete it.
