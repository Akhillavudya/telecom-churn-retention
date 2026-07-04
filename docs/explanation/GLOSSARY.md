# Glossary — every term in this project, in plain language

> You're a beginner, so this file defines **every** piece of jargon we use, grouped by topic.
> When a step doc mentions a term, look it up here. Terms are written for someone who has *never*
> seen them before. New terms get added here as the project grows.

---

## A. The business / data-analysis words

- **Churn** — when a customer *leaves* (cancels their subscription). "Churn rate" = the fraction of
  customers who leave. Our whole project is about predicting *who will churn* so the company can try
  to keep them.
- **Retention** — the opposite of churn: keeping a customer. A "retention campaign" is spending money
  (a discount, an offer) to stop someone leaving.
- **ARPU** — **A**verage **R**evenue **P**er **U**ser: how much money one customer brings in, usually
  per month. A high-ARPU customer leaving hurts more, so ARPU is why we do *value-weighted* targeting
  (weighing risk **and** revenue), not just "who's most likely to leave."
- **Target** (a.k.a. **label**) — the thing we're trying to predict. Here it's the `churn` column:
  1 = the customer left, 0 = they stayed.
- **Feature** — an input column the model learns from (tenure, monthly bill, equipment age, …). If the
  target is the answer, features are the clues.
- **Feature engineering** — creating *new*, smarter columns out of existing ones because they capture
  signal a raw column can't. Example from our code: `overage_share` = how much of the bill is overage
  charges (bill-shock exposure) — a churn hint no single raw column gives directly.
- **Decile** — one tenth of the data after sorting it. We sort customers by predicted churn risk and
  cut them into 10 groups of 10%. "Top decile" = the riskiest 10%.
- **Lift** — how much better a group is than random. "The top decile has 1.6× lift" means the riskiest
  10% churn 1.6× more than the average customer — proof the model's ranking is useful.
- **Cumulative gains** — a chart answering "if I contact the top X% by risk, what % of *all* churners
  do I catch?" Our headline: contacting the top 20% catches ~30% of churners.
- **Baseline** — the "no-skill" comparison. A random guess gives 0.50 ROC-AUC; beating it proves the
  model learned something. Always compare results to a baseline.
- **ROI** — **R**eturn **O**n **I**nvestment: (money gained − money spent) ÷ money spent. "2.1× ROI"
  means every $1 spent returns $2.10. **Note:** our ROI is *projected from assumptions*, not a real
  measured result — always say "projected," never "achieved."

---

## B. The machine-learning words

- **Model** — a program that *learns patterns from data* instead of being explicitly programmed. You
  show it features + known answers (training), and it learns to predict answers for new rows.
- **Classifier** — a model that predicts a *category* (here: churn / not-churn). It also outputs a
  **probability** (e.g. "0.82 likely to churn"), which is what we rank customers by.
- **Logistic Regression / Random Forest / XGBoost** — three different *kinds* of model we compared.
  Logistic Regression is the simple linear one; Random Forest and XGBoost are "tree ensembles" (they
  combine many decision trees). We benchmarked all three and **XGBoost won** (best ROC-AUC).
- **Training / test split** — we split the data: the model *learns* on the training part (70%) and is
  *graded* on the unseen test part (30%). Grading on unseen data is the only honest measure.
- **`random_state` / seed** — a fixed number (we use `42`) that makes "random" steps repeatable, so
  everyone who runs the code gets the *exact same* split and results. Key to reproducibility.
- **Imputation** — filling in missing values (blanks) so the model can use the row. We impute *inside*
  the pipeline so information from the test set never leaks into training ("leak-free").
- **Missingness** — how much data is blank. Columns that are >40% blank we *drop* instead of impute,
  to avoid inventing fake signal.
- **ROC-AUC** — the main score we pick models by. Read it as: *the probability the model ranks a random
  churner above a random non-churner.* 0.5 = coin flip (useless), 1.0 = perfect. Ours ≈ **0.70** —
  "modest but honestly reported."
- **Accuracy / Precision / Recall / F1** — other grades. Accuracy = % predicted correctly. Precision =
  of those we *flagged* as churners, how many really were. Recall = of all *actual* churners, how many
  we caught. F1 = a balance of precision and recall.
- **Confusion matrix** — a 2×2 table of right/wrong predictions (true positives, false positives, etc.)
  — the raw material behind precision and recall.
- **Pipeline / ColumnTransformer** — scikit-learn tools that bundle preprocessing + model into one
  object, so the *same* steps run identically on training and new data (prevents leakage and mistakes).
- **Encoding / Scaling** — preparing columns for a model. *Encoding* turns text categories into numbers;
  *scaling* squashes numeric columns to a comparable range (needed by Logistic Regression, not by trees).

---

## C. The code, files & tooling words

- **Repository ("repo")** — the project folder, especially once it's tracked by **git** and pushed to
  GitHub. "Public repo" = anyone can view it (the clickable thing on your CV).
- **Reproducibility** — the property that *anyone* can re-run your project and get the *same* results.
  Achieved via a fixed seed + pinned dependencies + a documented run command.
- **Path** — a file's address. **Absolute** starts at the drive (`C:\Users\...`). **Relative** is
  measured from a starting point — and the starting point matters (see next two).
- **Current working directory (CWD)** — the folder you *launched the program from*. `Path.cwd()` uses
  it, which is fragile: run the script elsewhere and relative paths point somewhere else.
- **`__file__`** — a variable Python fills with the *script's own location*. Anchoring paths to
  `Path(__file__)` is stable — the script always knows where it lives regardless of where you ran it.
- **`.parent`** — moves *up* one folder in a path. `Path(__file__).parent.parent` = two folders up.
  We used it to reach the project **root** from inside `src/`.
- **matplotlib** — the Python library that draws our charts.
- **Backend** (matplotlib) — the rendering engine. **`Agg`** = non-interactive, just saves image files
  (what we want). **`TkAgg`** = interactive, opens a GUI window (caused the `tkinter` error in Step 1.5).
- **Figure** — one saved chart image (a `.png` in `reports/figures/`).
- **Virtual environment (venv)** — an isolated, per-project Python install so this project's library
  versions don't clash with other projects'. (We'll create one in Task 2.)
- **`requirements.txt` / pinning** — a list of the exact library versions the project needs
  (`pandas==3.0.3`). "Pinning" = fixing exact versions so the project is reproducible.
- **Notebook (`.ipynb`)** — a file mixing code, its output, and notes in one document (Jupyter). Great
  for *exploring* and *presenting*; we keep it separate from the `src/` scripts.
- **Git** — the tool that tracks every change to your files (version history) and lets you push to
  GitHub. **Commit** = a saved snapshot; **push** = upload snapshots to GitHub.
- **Quarto** — a tool that turns a document (text + code + charts) into a polished website or report.
  Our deploy target (Tasks 5–6).
- **Observable JS (OJS)** — small JavaScript snippets that run *in the reader's browser*, letting us
  add live sliders (the ROI calculator) with no server needed.
- **GitHub Pages** — free hosting that serves a website straight from your GitHub repo — where the
  Quarto report will go live (Task 7).

---

*See the per-step docs (`step*_*.md`) for how these terms show up in practice.*
