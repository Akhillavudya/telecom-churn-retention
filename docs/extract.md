# Project Profile — extract.md

> Auto-extracted from the repo for CV / portfolio use. Items not determinable from the
> repo are flagged `NOT FOUND IN REPO — I'll fill this in`.

---

## 1. Identity

- **Project name:** Value-Weighted Churn-Retention Proposal — Company A (Telecom)
- **One-line description (CV header):** End-to-end telecom churn model that ranks 100K customers by risk and quantifies a $2M/yr retention ROI.
- **Timeframe:** Spring 2026 (titled "GCI World 2026 Spring"; all source files last modified 19 Jun 2026). No git history exists to date first/last commit — *not a git repo*.
- **Type:** Coursework / competitive data-science program — final assignment for the **GCI** program (University of Tokyo Matsuo-Iwasawa Lab data-science course, submitted via the **Omnicampus** platform; references to a grading rubric and References field confirm this).
- **Status:** **Completed.** Reproducible pipeline (`analysis.py`), generated 15-slide PDF deck (`LavudyaAkhil31.pdf`), a built notebook (`LavudyaAkhil31.ipynb`, 42 cells) and 11 figures are all present and consistent.

---

## 2. The Problem

A wireless operator ("Company A", ~100,000 customers, **no in-house ML capability**) is losing
subscribers in a saturated mobile market (framed against India) where retention — not new
acquisition — is the cheaper growth lever. The project answers a single business question:
**which existing customers should the operator spend its limited retention budget on, and what
is the expected dollar return of doing so?** It moves beyond "predict churn" to a
*value-weighted* targeting strategy that ranks customers by risk **and** revenue.

- **User/audience:** Retention / marketing decision-makers at the telecom operator (the deck is a
  business proposal, not a research write-up). Secondary audience: the GCI/Omnicampus graders.

---

## 3. Technical Stack (verified from actual source files)

- **Languages:** Python (3 scripts, 1,225 LOC total) + Jupyter notebook.
- **Frameworks / libraries:** (No `requirements.txt`/`pyproject.toml` in repo — versions below are
  from the local environment that runs it, **not pinned in the repo**)
  - `scikit-learn` 1.9.0 — `Pipeline`, `ColumnTransformer`, `SimpleImputer`, `StandardScaler`, `OrdinalEncoder`, `LogisticRegression`, `RandomForestClassifier`, metrics
  - `xgboost` 3.2.0 — `XGBClassifier`
  - `pandas` 3.0.3, `numpy` 2.4.4
  - `matplotlib` 3.10.9, `seaborn` 0.13.2 (all figures + the PDF slide deck are rendered with matplotlib's PdfPages)
- **Databases/storage:** None — flat-file. Two CSVs joined on `Customer_ID`: `telecom/Client.csv` (100,000 rows, account/demographic/equipment fields) and `telecom/Record.csv` (100,000 rows, usage/billing/call-quality + `churn` target).
- **Infra/deployment:** None. No Docker, no cloud config, no CI. Runs locally via `python analysis.py`.
- **APIs/external services:** None integrated.
- **ML/AI components:** Classic supervised ML (binary churn classification). Three models compared —
  **Logistic Regression** (L2, `C=0.5`), **Random Forest** (300 trees, `max_depth=14`), and
  **XGBoost** (400 trees, `lr=0.05`, `max_depth=6`, subsample/colsample 0.9). No deep learning, no
  LLMs, no RAG/agents. Primary selection metric: **ROC-AUC**.

---

## 4. Architecture & Key Technical Decisions

- **Two-track preprocessing by model family** (`analysis.py:150-163`): a `pre_linear`
  `ColumnTransformer` (median-impute → standard-scale → ordinal-encode) for Logistic Regression,
  and a separate `pre_tree` transformer (passthrough numerics, ordinal-encode categoricals) for the
  tree models — a deliberate choice so each model gets the representation it actually needs rather
  than one-size-fits-all.
- **Business-intuition feature engineering** (`analysis.py:129-136`): six derived ratio/delta
  features encoding signal no single raw column captures — `eqp_per_month` (handset age vs tenure),
  `rev_per_min` (price intensity), `overage_share` (bill-shock exposure), `care_intensity` (support
  friction), `usage_decline` (recent drop flag), `active_ratio` (share of active lines).
- **Missing-data discipline:** columns with >40% missingness are dropped automatically
  (`analysis.py:124`) rather than imputed, avoiding fabricated signal; the rest are imputed inside
  the pipeline so there is no train/test leakage (stratified 70/30 split, `random_state=42`).
- **Value-weighted decision layer, not just a classifier** (`analysis.py:257-336`): the model's
  probability output feeds a decile lift table, a cumulative-gains curve, and an explicit
  expected-value model (offer cost, success rate, value horizon) that converts model recall into a
  dollar ROI — with a **sensitivity analysis** over the success-rate assumption so the case doesn't
  rest on one guessed number.
- **Fully reproducible & self-contained:** one seed throughout; `make_slides.py` and
  `build_notebook.py` regenerate the deck and notebook from the same logic — deliverables are
  generated artifacts, not hand-edited.
- **Scale indicators:** **1,225 lines** of Python across 3 scripts (`analysis.py` 339,
  `build_notebook.py` 517, `make_slides.py` 369); 42-cell notebook; **200,000 source rows**
  (2 × 100K CSVs); 11 generated figures. **No automated tests** in repo.

---

## 5. Quantifiable Results / Impact

All numbers are produced by the repo (slides/notebook/`analysis.py`), held-out 30% test set:

- **Model performance (XGBoost, best of 3):** ROC-AUC **0.696 (~0.70)**, Accuracy **0.64**, F1 **0.64** vs a 0.50 random baseline.
- **Targeting power:** top risk decile has a **79.5% churn rate**; contacting the **top 20%** by risk **captures ~30% of all churners**.
- **Business impact (scaled to full 100K book, stated assumptions):** **$3.07M revenue retained/yr**, **$2.07M net benefit/yr**, **2.1× ROI** on ~$1.0M campaign spend; avg ARPU of targeted churners ≈ **$58/month**.
- **Scale:** 100,000 customers / 200,000 rows processed; ~50/50 churn balance.
- **Assumptions behind the $ figures** (flagged in `REFERENCES_AND_ASSUMPTIONS.md`, not empirical): offer cost $50/customer, 30% offer success rate, 12-month value horizon — robustness shown via sensitivity chart (`figures/11_sensitivity.png`).

> Note: model metrics are **real** (computed on held-out data). The dollar ROI rests on **planning
> assumptions**, not measured campaign outcomes — describe it as "projected/modeled," not achieved.

---

## 6. Role-Specific Angles

**SDE**
> Built a reproducible end-to-end ML pipeline (1,200+ LOC, scikit-learn `Pipeline`/`ColumnTransformer`) processing 200K rows across 2 joined tables, with model-family-specific preprocessing and leak-free imputation, auto-generating an 11-figure report and a 15-slide PDF deck from a single seeded codebase.

**Data Analyst**
> Analyzed 100K telecom customers to isolate churn drivers (equipment age, overage exposure, support friction), then built a decile lift table and cumulative-gains analysis showing the top 20% risk segment captures ~30% of churners — translating model output into a $2.07M/yr net-benefit retention recommendation (2.1× ROI).

**Data Scientist**
> Engineered 6 domain-driven features and benchmarked Logistic Regression, Random Forest, and XGBoost on a stratified 70/30 split, selecting XGBoost (ROC-AUC 0.70 vs 0.50 baseline) and converting predicted-risk rankings into an expected-value targeting model with sensitivity analysis over retention-success assumptions.

---

## 7. For the Portfolio Website

- **Card title:** Value-Weighted Telecom Churn Retention
- **Card summary:** An end-to-end ML system that ranks 100,000 telecom customers by churn risk and revenue, then turns model output into a concrete retention strategy. Projects a $2.07M/yr net benefit (2.1× ROI) by targeting the top 20% highest-risk customers.
- **Live demo:** No demo currently. Could be hosted as a **Streamlit/Gradio app on Hugging Face Spaces** (upload-CSV → risk scores + lift table) or a static write-up on **Vercel/GitHub Pages**. The figures + PDF deck make a strong static showcase even without a live app.
- **Screenshot-worthy visuals:** Yes — `figures/10_cumulative_gains.png` (targeting works), `figures/04_churn_by_eqp_decile.png` (clear business lever), `figures/06_model_comparison.png`, and the slide-deck metric cards in `LavudyaAkhil31.pdf` (0.70 AUC / 79.5% / $2.07M / 2.1×). Lead with the cumulative-gains chart or the deck title slide.
- **GitHub status:** **Not a git repo and not public** — would need to be `git init`'d and pushed first.
- **README:** There is no markdown README — only `README.docx` (not web-renderable). `REFERENCES_AND_ASSUMPTIONS.md` exists but is an internal to-do list with unfilled `[CITE]` markers. **Needs a proper `README.md` before linking publicly.**

---

## 8. Gaps / Cleanup Needed Before Using Publicly

- **Secrets/keys:** ✅ **None found.** Grep across `.py`/`.md` for api keys / tokens / passwords / secrets returned nothing. No external services are called.
- **Missing README:** Convert `README.docx` → a real `README.md` (problem, data, how to run, results, figures). Add a `requirements.txt` / `pyproject.toml` — dependencies are currently **unpinned** (versions only exist in the author's local env).
- **Unfinished citations:** `REFERENCES_AND_ASSUMPTIONS.md` still has unresolved `[CITE]` markers and the line "fill before submitting" — clean this up or remove it before going public.
- **Data licensing:** `telecom/Client.csv` + `Record.csv` are the provided GCI assignment dataset — confirm you're allowed to redistribute before pushing the CSVs to a public repo (consider sampling or `.gitignore`-ing them).
- **Framing honesty:** Make explicit on any public page that the **$ ROI is a projection from stated assumptions**, not a measured result, and that AUC ≈ 0.70 is modest — easy to defend if labeled correctly, a red flag if oversold.
- **Personal identifiers:** Filenames/author tags embed `LavudyaAkhil31` and "Omnicampus" — fine for a portfolio (it's you), just be aware they're program-specific.
