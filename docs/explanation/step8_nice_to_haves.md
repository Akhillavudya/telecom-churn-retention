# Step 8 — Interpretability & deliverables (SHAP, segment ROI, target-list export)

> Beginner explainer for the three **§6 "nice-to-have"** items of `docs/final_plan.md`.
> New words are defined the first time they appear.

---

## 1. Big Picture — why this step exists

The core project already answered *who will churn* and *is it worth acting*. These three additions make
it **CV-ready** by closing the gaps a hiring manager pokes at:

1. **"Why did the model flag *this* customer?"** → a **SHAP** panel (per-customer explanations).
2. **"Where exactly should the budget go?"** → a **segment-level ROI** breakdown.
3. **"Can I actually *use* the output?"** → a **downloadable target list** (CSV) in the report.

None of them change the model. They turn a good analysis into a *decision-ready* one — which is the
whole job of a data analyst.

---

## 2. Core concepts, explained simply

- **Global vs. local explanation.** The feature-importance bar chart (fig 09) is *global*: which
  features matter **on average**. It cannot tell you why one specific customer scored high. A *local*
  explanation does that, customer by customer.

- **SHAP (SHapley Additive exPlanations).** A method that splits a single prediction into a sum of
  per-feature contributions. It borrows the **Shapley value** from cooperative game theory: imagine the
  features are teammates who together produce the churn score, and you want to pay each one fairly for
  its contribution. SHAP computes that fair share for every feature, for every customer. For tree models
  like XGBoost there's an exact, fast version (`TreeExplainer`).

- **Beeswarm plot.** The standard SHAP picture. One **row per feature**; one **dot per customer**. A
  dot's horizontal position is that feature's SHAP value for that customer (right = pushed the score
  toward churn, left = away). The dot's **colour** is the feature's raw value (red = high, blue = low).
  So "red dots clustered on the right" reads as *high values of this feature increase churn risk*.

- **Value-weighted targeting (why segments matter).** Retention value is **risk × dollar value**, not
  risk alone. A segment can churn a lot yet be low-value, so chasing raw churn probability can send the
  budget to the *least* profitable customers. Splitting the ROI by segment exposes that.

- **Client-side download.** The report is a static page with no server. To still offer a file download,
  the browser builds the CSV *in memory* from data already embedded in the page (`Blob` +
  `URL.createObjectURL`) and hands it to an `<a download>` link. Nothing is uploaded or fetched.

- **Anonymised deliverable.** The target list ships model **output only** — a sequential `CUST-#####`
  reference (never the real `Customer_ID`), the risk score, decile, ARPU, and a priority band. That way
  a genuinely useful artifact can be published without redistributing a single raw customer row.

---

## 3. File-by-file — what changed and why

### `requirements.txt` (edited)
Added `shap==0.51.0`, pinned like everything else so a clean clone reproduces the beeswarm.

### `src/analysis.py` (edited) — new "Section 6: Interpretability & segmentation"
- **6a. SHAP beeswarm → `12_shap_beeswarm.png`.** Transforms the held-out test set with the *same*
  preprocessing the XGBoost pipeline used, subsamples 3,000 rows (fixed seed, for speed/readability),
  runs `shap.TreeExplainer`, and saves the beeswarm.
- **6b. Segment ROI → `13_segment_roi.png`.** A small `segment_roi()` function runs the **same
  top-20%-by-risk campaign inside each equipment-age third** and returns its economics, so every
  segment's ROI is comparable to the 2.1× headline. (First draft blanket-contacted whole segments — see
  Issue #2.)
- **Target list → `data.json`.** Builds an anonymised top-2,000-by-risk table and adds it under a new
  `"targets"` key in the JSON the report already loads.

### `reports/quarto/index.qmd` (edited) — three new sections
- **"What drives each customer's score — SHAP"** (after model comparison): the beeswarm + how to read it.
- **"Where to point the budget — segment-level ROI"** (after the ROI case): the fig + a 3-row table +
  the risk-vs-value twist.
- **"Download the target list"** (after the calculator): an OJS cell that builds the CSV client-side and
  a `Blob`-backed download link, plus an `Inputs.table` preview of the first 10 rows.

### `reports/quarto/data.json` (regenerated)
Now includes the `targets` array alongside the existing `curve` and `defaults`.

---

## 4. Issues hit while building

### Issue #1 — the "smoke test on the sample" was actually a real-data run
- **What happened:** I ran `analysis.py` expecting the synthetic sample, but it printed `Wrote calculator
  data` and the real $2.07M headline. That only happens when `USING_RAW` is true.
- **Why:** the real CSVs *are* present in `data/raw/` on this machine, and the loader prefers real data
  when it exists. So the run used real data and produced the real, deployable figures + `data.json`.
- **Lesson:** always read the run's own log (`Data source: raw` vs `sample`) instead of assuming which
  branch of a fallback fired. The printout exists precisely so you're never guessing.

### Issue #2 — the first segment ROI was both weak and mislabelled
- **What happened:** the first version computed the ROI of contacting an **entire** equipment-age third
  (no risk targeting). That gave ROI ≈ 1× (much worse than the 2.1× headline, which *is* risk-targeted),
  and the "Old handsets repay best" title was contradicted by the data (Mid won).
- **Why:** comparing a blanket campaign against a targeted headline is apples-to-oranges; and asserting a
  direction ("Old best") before reading the numbers is how you ship a wrong claim.
- **How we fixed it:** switched to **risk-targeting within each segment** (comparable to the headline),
  then read the real result *before* writing the caption. The honest finding is the opposite and more
  interesting: old handsets churn most, but **new-handset churners are worth the most** ($72 vs $52
  ARPU), so the newer segment gives the best ROI (2.4× vs 1.8×).
- **Lesson:** make comparisons like-for-like, and let the computed numbers write the headline — never the
  other way around.

### Issue #3 — the CSV text isn't findable in the rendered HTML
- **What happened:** grepping the built `index.html` for `CUST-00001` returned nothing, which looked like
  the target list didn't embed.
- **Why:** with `embed-resources: true`, the `data.json` FileAttachment is inlined **base64-encoded**, so
  its plaintext strings aren't searchable. The download cell decodes it at runtime.
- **Lesson:** "not found by grep" ≠ "not present" for embedded/encoded assets. Verify the *source*
  (`data.json` has 2,000 targets) and that the page references the attachment, not the decoded text.

---

## 5. Where things stand + what's next

**All three §6 nice-to-haves are done and verified**, on real data:
- SHAP beeswarm (`12_shap_beeswarm.png`) and segment ROI (`13_segment_roi.png`) generated.
- `data.json` carries 2,000 anonymised targets; the report offers a client-side CSV download + preview.
- The report renders to a self-contained single HTML with zero external requests.

With §3–§5 (the must-do tasks) already complete, the project is now **CV-ready**: reproducible from a
clean clone, deployed, interactive, interpretable, segment-actionable, and it ships a usable deliverable.
The only remaining descoped item is a live model-scoring API — deliberately *not* built (see
`final_plan.md` §6), to keep the project static, free, and secret-free.
