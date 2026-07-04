# Final Plan — Value-Weighted Telecom Churn Retention (CV-Ready)

**Project:** Value-Weighted Churn-Retention Proposal — Company A (Telecom) — GCI World 2026 final assignment.
**Primary target role:** **Data Analyst (DA)** — this is your DA CV project #2 (rated 8), behind Customer Segmentation.
**One-line goal:** Turn a completed-but-local GCI assignment into a reproducible, documented, **publicly demoable** DA/analytics portfolio piece — deployed on a platform that *diversifies* the portfolio, not one that repeats it.

> **This document is the authoritative build guide.** It builds on the audit in `extract.md` (already accurate) — read that for the verified inventory; read this for what to actually do and ship.

---

## 0. The one strategic decision (read first): where this deploys

`extract.md` §7 floated **Streamlit/HF-Spaces** for a live demo. **Do not use it here.** Across your 10-project portfolio, ~5 projects already resolve to Python + Streamlit/HF-Spaces, and your other deploys are already routed:

| Platform | Already claimed by |
|---|---|
| Streamlit / HF-Spaces | RAG, Legal AI, DSA (monoculture — avoid) |
| Tableau Public + dbt/DuckDB | **Customer Segmentation** (your DA project #1) |
| Modal + W&B | NFL Draft |
| FastAPI + React (Render/Vercel) | Verdex, Materia, RAG |

**So this project must introduce something new.** Route it to:

### **Quarto report/dashboard + Observable JS (OJS) → GitHub Pages (or Cloudflare Pages).**

- **Quarto** publishes your existing notebook/analysis into a polished, recognizable **analytics report website** — the project *is* a business proposal, so this is the honest, native format (not a shoehorned app).
- **Observable JS cells** (built into Quarto, run client-side, no server) turn your static sensitivity chart into a **live ROI calculator**: sliders for offer cost / success rate / value horizon / target fraction → recomputed *customers saved, net benefit, ROI* in real time. The math is pure arithmetic on precomputed aggregates (`analysis.py:299–325`), so it runs entirely in the browser — no model hosting, no backend, no secrets.
- **GitHub Pages / Cloudflare Pages** — free, guaranteed-public URL, static host **not used anywhere else** in your portfolio.

**Net:** one project introduces **Quarto + OJS + a static-site host** — three fresh, currently-popular analytics tools — while staying $0, serverless, and truthful about what the project is.

> **Do NOT** build a "upload-CSV → live model scoring" app. That needs the XGBoost model served (Modal is taken by NFL; FastAPI is triple-booked). Precompute the scores offline; keep the deployed layer static + interactive-via-OJS. If you later want a serving demo, it's a §6 nice-to-have, not the CV requirement.

---

## 1. Current State (from `extract.md`, verified)

**Done and genuinely strong:** reproducible `analysis.py` (339 LOC) + `build_notebook.py` + `make_slides.py` (1,225 LOC total, single seed), 42-cell notebook, **11 figures**, a 15-slide PDF deck (`LavudyaAkhil31.pdf`), two 100K-row CSVs joined on `Customer_ID`. Three models benchmarked (LogReg / RandomForest / **XGBoost** selected), model-family-specific preprocessing, leak-free imputation, 6 domain features, decile lift table + cumulative-gains + expected-value ROI with **sensitivity analysis**.

**Blockers to "shippable":**
- **No `README.md`** (only `README.docx`, not web-renderable).
- **No `requirements.txt`** — deps unpinned (only in author's local env: sklearn 1.9, xgboost 3.2, pandas 3.0, etc.).
- **Not a git repo, not public** — nothing clickable.
- **`REFERENCES_AND_ASSUMPTIONS.md`** still has unresolved `[CITE]` markers and "fill before submitting" — internal to-do leaking into a public repo.
- **Data-licensing risk** — the CSVs are the provided GCI dataset; redistribution rights unconfirmed.
- **No live demo / public URL.**

**Verdict:** the differentiating analysis is done and above-average. This is a ~1-day packaging + deploy job, not a rebuild.

---

## 2. Definition of "CV-Ready Done"

Done when **all** are true:
1. **Runs from a clean clone** — `python analysis.py` regenerates figures/metrics with one documented command; deps pinned.
2. **Public GitHub repo** with a real `README.md`: pitch, dataset, how-to-run, **the honest headline numbers**, embedded key figures, links to the deck + live report.
3. **A clickable public demo** — the **Quarto report URL** (with the interactive OJS ROI calculator) pinned at the top of the README.
4. **`requirements.txt`** present and pinned.
5. **Provenance + honesty are explicit** — labeled as a GCI assignment; ROI stated as *projected from assumptions*; AUC ≈ 0.70 framed as modest-but-honest; citations resolved or removed.
6. **Data-licensing resolved** — CSVs either confirmed redistributable, sampled, or `.gitignore`'d with a download note.
7. **Industry-standard repo layout** — files organized into a conventional DA folder structure (§2A), not a flat root; hard-coded paths updated; pipeline still regenerates all 11 figures from a clean run.

---

## 2A. Target Repository Structure (industry-standard DA layout — do this EARLY)

Right now every file lives flat at the repo root, so a reviewer can't tell data from code from output. Reorganize into the **Cookiecutter-Data-Science-style** layout recruiters recognize on sight:

```
churn-retention-telecom/          # repo root (rename from "Final Assignment")
│
├── README.md                     # front door — pitch, results, run steps (Task 3)
├── requirements.txt              # pinned deps (Task 2)
├── .gitignore
├── LICENSE                       # optional — MIT for your own code
│
├── data/
│   ├── raw/                      # Client.csv, Record.csv — original, NEVER edited, git-ignored
│   ├── sample/                   # small committed sample_*.csv so the pipeline runs (Task 1)
│   └── data_dictionary.md        # column meanings (from the .docx dataset overview)
│
├── src/                          # the reproducible code ("production" scripts)
│   ├── analysis.py
│   ├── build_notebook.py
│   └── make_slides.py
│
├── notebooks/
│   └── churn_analysis.ipynb      # renamed from LavudyaAkhil31.ipynb
│
├── reports/                      # GENERATED artifacts (regenerable, not hand-made)
│   ├── figures/                  # the 11 PNGs
│   ├── slides.pdf                # renamed from LavudyaAkhil31.pdf
│   └── quarto/                   # index.qmd, _quarto.yml, data.json (Tasks 5–6)
│
└── docs/                         # process + provenance (kept out of the root)
    ├── final_plan.md
    ├── extract.md
    └── REFERENCES_AND_ASSUMPTIONS.md
```

**Why this layout (the reasoning, not just the rule):**
- **Separation of concerns** — data, code, and outputs each have one obvious home; a reviewer navigates the repo in seconds without reading any file. This mirrors the widely-used *Cookiecutter Data Science* convention, so it reads as "this person has shipped before."
- **`data/raw/` is sacred and git-ignored** — raw inputs are never modified and never committed (licensing + repo size); the committed `data/sample/` keeps the clone runnable.
- **`src/` vs `notebooks/`** — separating reproducible scripts from exploratory notebooks signals engineering maturity (the notebook explores; the scripts are the pipeline of record).
- **`reports/` = generated output** — figures, deck, and the deployable Quarto site sit together, clearly labeled as artifacts you can regenerate, not artisan one-offs.
- **`docs/` = process** — planning + assumptions live here so the **root stays clean**: the root should contain only the front-door files (README, requirements, license) a reviewer opens first.

**The gotcha — this WILL break paths.** `analysis.py` reads `telecom/*.csv` and writes `figures/*.png`; `build_notebook.py` / `make_slides.py` reference the same. After moving files you MUST update those path constants (that's app code — do it yourself) and re-run `python src/analysis.py` from the repo root to confirm all 11 figures regenerate into `reports/figures/`. **Do this restructure before Tasks 3, 5, 7** so the README and Quarto paths are written once, correctly.

---

## 3. MUST-DO — ordered

| # | Task | Files | Effort | Why |
|---|------|-------|--------|-----|
| 1 | **Resolve data licensing FIRST.** Confirm the GCI CSVs are redistributable. If unsure: `.gitignore` `telecom/*.csv`, commit a **small sampled/synthetic `telecom/sample_*.csv`** (e.g. 2–5K rows) so the pipeline still runs, and add a README note on obtaining the full data. | `.gitignore`, new `telecom/sample_*.csv` | S | A public repo redistributing someone else's dataset is a real risk. Gate before pushing. |
| 1.5 | **Restructure into the industry-standard DA layout** (see §2A). Create `data/{raw,sample}/`, `src/`, `notebooks/`, `reports/{figures,quarto}/`, `docs/`; move existing files in; rename `LavudyaAkhil31.ipynb` → `notebooks/churn_analysis.ipynb` and `LavudyaAkhil31.pdf` → `reports/slides.pdf`; update the hard-coded paths in `analysis.py`/`build_notebook.py`/`make_slides.py`; re-run to confirm all 11 figures regenerate. | repo root, `src/*.py` | S–M | Recruiters skim structure before code; a clean, conventional tree reads as "shipped before." Do it **before** Tasks 3/5/7 so README + Quarto paths are written once. |
| 2 | **Pin the environment.** `requirements.txt` with the versions in `extract.md` §3 (sklearn 1.9, xgboost 3.2, pandas 3.0, numpy 2.4, matplotlib 3.10, seaborn 0.13). | new `requirements.txt` | S | Reproducibility; needed for the Quarto render + clean clone. |
| 3 | **Write `README.md`.** Pitch (2 lines) → business problem → data (2×100K joined) → how-to-run (`pip install -r requirements.txt && python analysis.py`) → **honest headline numbers** (§5) → embed 3 key figures (`10_cumulative_gains`, `04_churn_by_eqp_decile`, `06_model_comparison`) → link to deck PDF + live Quarto report → **explicit honesty box** (ROI projected; AUC modest; GCI assignment). | new `README.md` | M | Highest-leverage hour; most recruiters read only this. |
| 4 | **Clean up provenance artifacts.** Resolve or delete the `[CITE]` markers in `REFERENCES_AND_ASSUMPTIONS.md` (fill real citations for the market claims, or cut the market-context section for the public version). Remove any "fill before submitting" to-do language. | `REFERENCES_AND_ASSUMPTIONS.md` | S | An unfinished internal to-do in a public repo reads as sloppy. |
| 5 | **Build the Quarto report.** `quarto create`; author `index.qmd` that tells the story with your existing figures + narrative: problem → data → churn drivers → model comparison → **decile lift + cumulative gains** → the ROI case. Export the small set of precomputed aggregates the calculator needs (`churners_caught_full`, `arpu_target`, `contacted_full`, baseline cost) to a JSON the page reads. | new `report/index.qmd`, `report/_quarto.yml`, `report/data.json` | **M** | This is the deployable artifact and the portfolio-diversifying centerpiece. |
| 6 | **Add the interactive OJS ROI calculator** inside the Quarto page: sliders for `offer_cost`, `success_rate`, `horizon_months`, `target_fraction`; recompute `saved / revenue_retained / campaign_cost / net_benefit / ROI` live (mirror `analysis.py:305–312`) and render a reactive net-benefit chart. | `report/index.qmd` (OJS cells) | **M** | Converts the static sensitivity chart into a live, defensible interactive — the "wow" without a backend. |
| 7 | **Init git + push public; deploy the report.** `.gitignore` (`figures/` optional-keep, `__pycache__/`, large CSVs per Task 1, `report/_site/`, `.quarto/`). `quarto publish gh-pages` (or Cloudflare Pages pointing at `report/`). Pin the live URL at README top. | repo root | S | No repo + no URL = no CV link. |

**That's the whole must-do list.**

---

## 4. Deployment Plan (Quarto → GitHub Pages, primary)

### Exact steps
1. Confirm repo is public and contains `report/index.qmd`, `report/_quarto.yml`, `report/data.json`, `requirements.txt`.
2. Install Quarto (free). `cd report && quarto render` locally to verify the site + OJS calculator work.
3. `quarto publish gh-pages` → live at `https://<you>.github.io/<repo>/`.
   - **Alt host (still diversifying):** push, then connect the repo to **Cloudflare Pages** (build command `quarto render report`, output `report/_site`).
4. Paste the URL at the top of the README; embed the report's title screenshot.

### Secrets / cost
- **None.** Fully static, client-side OJS, no model hosting, no API keys. **$0** (Quarto, GitHub Pages / Cloudflare Pages, all libraries free). No GPU, no paid infra.

### Guaranteed fallback (ship regardless)
- The **11 figures + PDF deck embedded in the README** are the non-negotiable fallback. If Quarto publishing stalls, the README still shows the full analysis + deck; the report is an enhancement, not a single point of failure.

---

## 5. Headline Numbers — LOCK THESE (real, held-out test set)

Use only these on the CV/README, **with the honesty labels**:
- **Model (XGBoost, best of 3):** ROC-AUC **≈ 0.70**, Accuracy **0.64**, F1 **0.64** vs 0.50 random baseline. *(Label AUC as "modest but honestly reported.")*
- **Targeting power (the DA headline):** top risk **decile = 79.5% churn rate**; contacting the **top 20% by risk captures ~30% of all churners** (cumulative-gains).
- **Projected business impact (100K book, stated assumptions):** **$3.07M revenue retained/yr**, **$2.07M net benefit/yr**, **2.1× ROI** on ~$1.0M spend; avg ARPU of targeted churners ≈ **$58/mo**.
- **Scale:** 100,000 customers / 200,000 rows / ~50-50 churn balance / 6 engineered features / 3 models.
- **Assumptions (must show):** offer $50/cust, 30% success rate, 12-mo horizon → robustness via sensitivity analysis (now the live OJS calculator).

> **Framing rule:** model metrics are **real**; the dollar ROI is a **projection from assumptions**, not a measured campaign result. Say "projected/modeled," never "achieved/delivered." This is easy to defend when labeled — a red flag if oversold.

---

## 6. NICE-TO-HAVE (only after §3–§4 ship)

Ranked by impact-per-effort:
1. **SHAP explanation panel** in the Quarto report (beeswarm on the XGBoost model) — modern, recognizable interpretability signal; strengthens the "why these customers" story. *M.*
2. **Segment-level ROI breakdown** — split the lift table by a key driver (equipment age / overage) so the recommendation is actionable per segment. *S–M, pure DA value.*
3. **A downloadable "target list" export** in the report (top-N risk-ranked customers as CSV, from precomputed scores). *S.*

**Explicitly descoped:** a live model-scoring API/app (backend collides with Modal/FastAPI already used; adds hosting cost + secrets for little CV gain here). Keep this project static + interactive-via-OJS.

---

## 7. What to CUT / fix before public

- **`README.docx`** → replace with `README.md` (don't ship the .docx).
- **`[CITE]` markers + "fill before submitting"** in `REFERENCES_AND_ASSUMPTIONS.md` → resolve or remove (Task 4).
- **Raw GCI CSVs** → don't push until licensing is confirmed (Task 1).
- **Do not build a Streamlit app** (see §0).
- **Personal/program tags** (`LavudyaAkhil31`, "Omnicampus") — fine to keep (it's you + real provenance); just don't over-expose grading-rubric internals.

---

## 8. Resume Bullet (Data Analyst — from real work)

> **Analyzed 100K telecom customers (200K rows, 2 joined tables) to isolate churn drivers (equipment age, overage exposure, support friction), then built a decile lift table and cumulative-gains analysis showing the top 20% risk segment captures ~30% of churners — translating XGBoost risk scores (ROC-AUC 0.70) into a projected $2.07M/yr net-benefit retention strategy (2.1× ROI) with a published interactive ROI calculator.**

Alt DS-flavored line (if space on a DS CV): *"Engineered 6 domain features, benchmarked LogReg/RandomForest/XGBoost on a stratified 70/30 split, and converted predicted-risk rankings into an expected-value targeting model with sensitivity analysis over retention assumptions."*

**Honesty guardrails:** "projected"/"modeled" for the $ figures; never claim a delivered campaign result. Keep the GCI-assignment provenance truthful — do not relabel it as industry/consulting work.

---

## 9. Effort

| Bucket | Effort |
|--------|--------|
| Restructure into industry-standard layout + fix paths + re-run (Task 1.5) | ~0.5–1 h |
| Licensing + `requirements.txt` + provenance cleanup (Tasks 1,2,4) | ~1–1.5 h |
| `README.md` (Task 3) | ~1 h |
| Quarto report + OJS calculator (Tasks 5,6) | ~3–4 h |
| Git push + deploy (Task 7) | ~0.5–1 h |
| **Total to CV-ready + deployed** | **~6–7.5 focused hours** |

**Bare-minimum path** (time-boxed): Tasks 1, 2, 3 (README with figures), 7 (push, no Quarto) ≈ **~2.5 h** to "presentable public repo." Add the Quarto+OJS report (Tasks 5–6) for the diversifying live demo — that's the piece that makes it stand out and justifies the DA-CV slot.

---

## 10. Build Checklist

- [ ] Confirm/handle GCI data licensing; sample or `.gitignore` the CSVs (Task 1)
- [x] Restructure into industry-standard DA layout — `data/`, `src/`, `notebooks/`, `reports/`, `docs/`; update hard-coded paths; re-run `analysis.py` to confirm all 11 figures regenerate (Task 1.5, §2A) — **done; all 3 scripts reproduce end-to-end, see `docs/explanation/step1_5_explanation.md`**
- [ ] `requirements.txt` pinned (Task 2)
- [ ] `README.md` — pitch, run steps, locked numbers, 3 embedded figures, honesty box (Task 3)
- [ ] Resolve `[CITE]`s / strip internal to-do language (Task 4)
- [ ] Quarto `index.qmd` telling the story from existing figures + `data.json` aggregates (Task 5)
- [ ] Interactive OJS ROI calculator (sliders → live net benefit / ROI) (Task 6)
- [ ] `git init`, `.gitignore`, push public GitHub (Task 7)
- [ ] `quarto publish gh-pages` (or Cloudflare Pages); pin URL at README top (Task 7)
- [ ] Re-confirm AUC 0.70 / 79.5% decile / $2.07M / 2.1× before publishing; label ROI as projected
</content>
