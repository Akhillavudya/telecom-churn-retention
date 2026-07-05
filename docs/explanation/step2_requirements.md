# Step 2 — Pinning the environment (`requirements.txt`)

## 1. Big Picture — why this step exists

Your code depends on other people's libraries (pandas, scikit-learn, xgboost, …). Those libraries
keep changing: a function that exists in `scikit-learn 1.9` might be renamed or behave differently in
`1.10`. If someone clones your repo next year and runs `pip install pandas` with no version, they get
*whatever the latest version is that day* — which may not match what your code was written against.
The result is the classic "but it works on my machine" failure.

`requirements.txt` is the fix: a plain-text list of **exactly which versions** your project needs.
Anyone (including future-you) runs one command and gets the identical environment you built and tested
against. This is the foundation of **reproducibility** — the promise that the analysis produces the
same numbers no matter who runs it or when.

## 2. Core concepts, explained simply

- **Dependency** — a library your code imports but didn't write itself (e.g. `import pandas`). Your
  project *depends on* it being installed.
- **`requirements.txt`** — the conventional filename Python developers and recruiters expect at a
  repo's root. `pip` reads it and installs everything listed in one shot.
- **Pinning** — writing `pandas==3.0.3` (with `==`) instead of just `pandas`. The `==` locks the
  version. Without it, `pip` grabs the newest release, which can silently break your code.
  - `pandas` → "any version, newest wins" (fragile).
  - `pandas>=3.0` → "3.0 or higher" (looser, still drifts).
  - `pandas==3.0.3` → "exactly this one" (reproducible — what we want here).
- **`pip install -r requirements.txt`** — the `-r` flag means "read requirements from this file."
- **Transitive dependencies** — the libraries your libraries need (e.g. `xgboost` needs `scipy`).
  We don't list those; `pip` resolves them automatically. We only pin what our code *directly*
  imports. (A stricter, fully-frozen alternative is `pip freeze`, which pins *everything* including
  transitive deps — more locked-down but noisier and harder to read. For a portfolio project, pinning
  our direct deps is the readable, standard choice.)

## 3. File-by-file — what changed

**New file: `requirements.txt`** (at the repo root — the front-door location reviewers expect).

Six packages, each pinned to the exact version already installed on this machine, which also matches
the versions recorded in `extract.md §3`:

| Package | Version | Why it's here |
|---|---|---|
| `numpy` | 2.4.4 | numerical arrays; underpins pandas |
| `pandas` | 3.0.3 | loads and joins the two 100K-row CSVs |
| `scikit-learn` | 1.9.0 | pipelines, preprocessing, LogReg/RandomForest, metrics |
| `xgboost` | 3.2.0 | the selected model (`XGBClassifier`) |
| `matplotlib` | 3.10.9 | all 11 figures **and** the PDF slide deck (via `PdfPages`) |
| `seaborn` | 0.13.2 | statistical plot styling on top of matplotlib |

**How the list was verified (not guessed):** I grepped every `import` across `src/analysis.py`,
`src/build_notebook.py`, and `src/make_slides.py`, then cross-checked each third-party package's
installed version with `importlib.metadata`. The only imports beyond these six are Python's own
**standard library** (`os`, `json`, `warnings`, `pathlib`) — those ship with Python itself, so they
are *not* dependencies and must **not** go in `requirements.txt`.

**Why `jupyter`/`nbformat` are deliberately absent:** you might expect them, since the project produces
a notebook. But `build_notebook.py` writes the `.ipynb` by hand as raw `json` — it never imports
`nbformat` or `jupyter`. Listing a package we don't actually import would be a false dependency, so we
leave them out.

## 3b. The virtual environment (`.venv`) — the companion to the pin file

Pinning versions only helps if those versions install somewhere they can't be disturbed. That's what a
**virtual environment** gives us.

- **The problem it solves:** by default every `pip install` lands in your **system Python** — one
  shared package folder used by *every* project on the machine. If Project A needs `pandas==3.0.3` and
  Project B needs `pandas==2.1`, they fight over that one folder and one of them breaks. This is
  "dependency hell."
- **What a venv is:** `python -m venv .venv` creates a `.venv/` folder holding a private copy of
  Python with its **own** `site-packages`. Installs into it are invisible to other projects and to
  system Python — each project gets an isolated sandbox.
- **How this project's venv was built:**
  1. `python -m venv .venv` — created the sandbox.
  2. `.venv\Scripts\python.exe -m pip install --upgrade pip` — upgraded pip **inside the venv only**
     (24.0 → 26.1.2); system pip was untouched, which is isolation working as intended.
  3. `.venv\Scripts\python.exe -m pip install -r requirements.txt` — installed the 6 pins (plus their
     transitive deps) into the empty sandbox. Verified: all 6 report the exact pinned versions.
- **Using it day-to-day:** activate with `.\.venv\Scripts\Activate.ps1` (prompt shows `(.venv)`); then
  plain `python`/`pip` mean the venv's. `deactivate` exits. Or skip activation and call the full path
  `.\.venv\Scripts\python.exe` directly.
- **Why it's git-ignored:** `.venv/` is large, machine-specific, and fully rebuildable from
  `requirements.txt`, so it lives in `.gitignore` and is never committed. A collaborator just re-runs
  the two commands above to reproduce it.
- **Transferable lesson:** `requirements.txt` says *what* versions; the venv is *where* they live in
  isolation. You want both — the pin file is the recipe, the venv is the clean kitchen you cook it in.

## 4. Issues hit while building

- **`importlib.metadata.PackageNotFoundError: ... 'jupyter'`** while I was probing versions.
  - **What happened:** my version-check command asked for `jupyter`'s version and crashed.
  - **Why:** `jupyter` isn't installed as a distributable package here — and, more importantly, the
    scripts don't import it. The error was the correct answer to a wrong question.
  - **How it's handled:** confirmed the scripts never need it, so it stays out of `requirements.txt`.
  - **Transferable lesson:** pin what your code **imports**, verified from the source — not what you
    *assume* a project "should" have. An unused pin is noise at best and a broken install at worst.

## 5. Where things stand & what's next

- **Done:** `requirements.txt` pinned at the repo root **and** an isolated `.venv` created with all 6
  pinned versions installed and verified. A clean clone rebuilds the exact environment with
  `python -m venv .venv` → activate → `pip install -r requirements.txt`.
- **Next (Task 3):** write the real `README.md` — pitch, how-to-run (now referencing this file),
  locked headline numbers, three embedded figures, and the honesty box.
