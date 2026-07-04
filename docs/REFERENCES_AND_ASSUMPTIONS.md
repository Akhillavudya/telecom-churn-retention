# References & Assumptions — fill before submitting

The notebook and slides contain `[CITE]` markers. Omnicampus requires a **References**
field that matches on-slide citations. Replace every bracketed item below with a real,
citable source, and copy the final list into the Omnicampus References field.

## Market-context claims to cite (Section 1 of notebook / slides)
- "Acquiring a subscriber costs several times more than retaining one." → cite a telecom
  retention study or industry report (e.g. a named consulting/industry source).
- "Mature telecom markets grow via retention / ARPU, not new-market expansion." → cite a
  market-size / growth report for your chosen country/region.
- Local market picture (major players, regulation, new entrants) → cite a recent,
  citable source for the specific market you describe.

## Method / tooling citations
- XGBoost: Chen & Guestrin (2016), "XGBoost: A Scalable Tree Boosting System", KDD.
- scikit-learn: Pedregosa et al. (2011), JMLR.
- Dataset: Company A telecom dataset provided with the GCI World 2026 assignment.

## Business-case ASSUMPTIONS (must be justified/cited on the slide)
These drive the dollar figures — show them transparently. Current values in the notebook:

| Assumption | Value used | Justify with |
|---|---|---|
| Retention offer cost / customer | $50 | handset-subsidy or bill-credit benchmark `[CITE]` |
| Offer success rate (churners retained) | 30% | A/B-test or published retention-uplift figure `[CITE]` |
| Value horizon for a saved customer | 12 months | stated assumption (state explicitly) |
| Target slice | top 20% by predicted risk | model-derived (cumulative-gains curve) |

> If you cannot cite a number, state it clearly as an **assumption** and show the
> **sensitivity chart** (notebook fig `11_sensitivity.png`) so the case does not rest on
> a single guessed value.

## If you used generative AI
Omnicampus requires the **chat URL** in the References field if any generative AI was used
to discuss the proposal, make diagrams, etc.

## Reproduced model results (quote on the slide — rubric requirement 3)
- Model: **XGBoost** (gradient-boosted trees)
- Evaluation metric: **ROC-AUC** (primary), Accuracy / F1 (secondary)
- Score (held-out 30% test): **ROC-AUC ≈ 0.70, Accuracy ≈ 0.64, F1 ≈ 0.64**
- Baseline: random = 0.50; compared against Logistic Regression and Random Forest.
