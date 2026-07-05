# Step 1 — Making the repo runnable from a clean clone (synthetic sample data)

> Beginner explainer for **Task 1** of `docs/final_plan.md`.
> New words are defined the first time they appear; the full list lives in
> [`GLOSSARY.md`](./GLOSSARY.md).

---

## 1. Big Picture — why this step exists

The whole analysis depends on two big CSV files (`Client.csv`, `Record.csv`). But those files are the
**GCI-provided dataset**, and we have **no confirmed right to republish someone else's data**. So they
are deliberately kept out of the public repo (`data/raw/*.csv` is git-ignored — see [git-ignored](#2-core-concepts-explained-simply)).

That creates a problem: a recruiter or teammate who clones the public repo has the *code* but **no data
to run it on**. `python src/analysis.py` would crash on the very first line with "file not found." A
portfolio project that can't be run is a weak portfolio project.

**What this step solved:** it makes the repo run **out of the box** — with zero data download — by
shipping a small, **synthetic** (computer-generated, fake) stand-in dataset, while never redistributing
a single real customer record.

> **Key idea:** you can prove the *pipeline works* without shipping the *real data*. Ship a fake dataset
> with the same shape; keep the real one private.

---

## 2. Core concepts, explained simply

- **git-ignored** — files listed in `.gitignore` that git deliberately refuses to track or upload. Our
  `data/raw/*.csv` line means "these CSVs stay on my laptop; never commit them." That is how the real
  data stays private even though the repo is public.

- **Synthetic data** — data a program *invents* to look like the real thing, containing no real records.
  Ours matches the real files **column for column**, copies each column's **type** (number vs. text),
  its **range** (min/max), and its **missingness** (what fraction of cells are blank) — but every value
  is freshly drawn from a distribution, so no real customer's row survives. Safe to publish.

- **A distribution / "drawing from" one** — a description of how a column's values are spread out (e.g.
  "average revenue is ~$58 with some spread"). "Drawing" a value means rolling a weighted die shaped
  like that spread. Do it 3,000 times and you get a fake column that *looks* like the real one in bulk
  but matches no individual.

- **Missingness** — the share of empty cells in a column. Real-world data is full of blanks; the pipeline
  even **drops** columns that are >40% empty. So to be a faithful stand-in, the sample must reproduce
  each column's blank rate — otherwise different columns would get dropped and the run wouldn't match.

- **A fallback path** — code that tries plan A, and quietly uses plan B if A isn't there. Our loader
  tries `data/raw/` (real data); if it's absent, it falls back to `data/sample/` (synthetic). Same code
  runs on your machine (real) and on a stranger's clone (sample) with no edits.

---

## 3. File-by-file — what changed and why

### `src/make_sample_data.py` — the generator (new)
Reads the real CSVs **locally** and writes a 3,000-row synthetic copy into `data/sample/`. For each
column it measures type, range, and missing rate, then draws fresh values matching those. Two special
cases:
- **`Customer_ID`** — a shared set of IDs written into *both* files so the join (`merge on Customer_ID`)
  still lines up.
- **`churn`** (the thing we predict) — assigned ~50/50, with a **mild, deliberately weak** built-in
  signal (older equipment + falling usage → slightly more likely to churn). That mild signal is enough
  for the sample to produce a *non-degenerate* lift curve, so a clone-runner sees the workflow actually
  do something — without pretending to reproduce the real effect sizes.

The generator itself contains **no real data**, so committing it is safe and even *documents* how the
sample was made (good for trust).

### `src/analysis.py` — the fallback + a safety guard (edited)
1. **`data_path()` fallback** — returns the raw file if it exists, else the sample. Added a `USING_RAW`
   flag and a printed line (`Data source: raw (full dataset)` vs `sample (synthetic stand-in)`) so you
   always know which data a given run used.
2. **Guarded the `data.json` write** — the pipeline exports `reports/quarto/data.json` (the numbers
   behind the live ROI calculator). That write now happens **only** when running on the real data, so an
   accidental sample run can't overwrite the real calculator data behind the published report.

### `README.md` — the instructions (edited)
Rewrote "How to run" to say the repo runs out of the box on the sample, told readers the sample's numbers
are *not* the headline results, and explained how to drop in the real CSVs to reproduce them.

### `data/sample/Client.csv`, `data/sample/Record.csv` — the committed sample (new)
The 3,000-row synthetic tables (≈1.2 MB + 2.0 MB). These are the only data files in the public repo.

---

## 4. Issues hit while building

### Issue #1 — the verification run silently overwrote the real committed figures
- **What happened:** to prove the "clean clone" path, we hid `data/raw/` and ran `analysis.py` on the
  sample. It worked — but `analysis.py` **regenerates the 11 figures in `reports/figures/`**, so the run
  replaced the *real* charts with *synthetic-sample* charts. `git status` showed all 11 PNGs modified.
- **Why it happened:** the pipeline always writes figures to the same folder regardless of data source.
  Running it on the sample is indistinguishable, output-wise, from running it on the real data — it just
  overwrites.
- **How we solved it:** because the real figures were already committed, we restored them in one command
  — `git checkout -- reports/figures` — which resets tracked files to their last committed (real) state.
- **Lesson (transferable):** any script that *writes into tracked files* will dirty your repo when you
  run it for a test. Before a throwaway run, know what it writes; afterward, check `git status` and
  restore anything you didn't mean to change. Git is your undo button *only for files already committed*.

### Issue #2 — protecting the real calculator data from a sample run
- **What happened (anticipated):** `analysis.py` also writes `reports/quarto/data.json`. A sample run
  would have overwritten the real, published calculator numbers with degenerate synthetic ones.
- **How we solved it:** guarded that single write behind `if USING_RAW:` — the sample run now *skips* it
  and prints that it kept the real file. We verified with an md5 checksum that `data.json` was byte-for-byte
  unchanged after the sample run.
- **Lesson (transferable):** when one script has both a "safe to regenerate anywhere" output (figures)
  and a "only correct from the real inputs" output (the published `data.json`), gate the sensitive output
  so it can't be produced from the wrong inputs. Verify with a checksum, not by eyeballing.

---

## 5. Where things stand + what's next

**Done and verified.** The public repo now runs from a clean clone with no data download:
`python src/analysis.py` detects there's no raw data, falls back to the committed synthetic sample,
and executes the *entire* pipeline (EDA → features → 3 models → business impact → all 11 figures). The
real data stays private and git-ignored; the real calculator data (`data.json`) is protected from
accidental overwrite.

This closes the last open item on the `docs/final_plan.md` must-do checklist — **every task (1–7) is now
complete.** The remaining `final_plan.md` §6 items (SHAP panel, segment-level ROI, downloadable target
list) are optional enhancements, not required for CV-ready.
