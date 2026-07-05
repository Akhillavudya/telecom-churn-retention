# References & Assumptions

This project's model metrics are **measured** on a held-out test set; the business-case dollar figures
are **projected** from the stated assumptions below (not a delivered campaign result). The assumptions
are shown transparently and stress-tested with a sensitivity analysis so the case does not rest on any
single guessed value.

## Business-case assumptions

These four inputs drive the projected ROI. Each is stated openly; the first two are **assumptions**
(reasonable planning values, not measured for this dataset), which is why the analysis includes a
sensitivity chart that recomputes the outcome as they vary.

| Assumption | Value used | Basis |
|---|---|---|
| Retention offer cost / customer | $50 | Planning assumption — order-of-magnitude of a handset subsidy or bill credit. |
| Offer success rate (churners retained) | 30% | Planning assumption — a conservative retention-uplift figure. |
| Value horizon for a saved customer | 12 months | Stated assumption (one year of retained ARPU). |
| Target slice | Top 20% by predicted risk | Model-derived, from the cumulative-gains curve. |

> Because the offer cost and success rate are assumptions rather than measured values, the ROI is
> validated with the **sensitivity analysis** (`reports/figures/11_sensitivity.png`) — and, in the live
> report, with an interactive calculator that recomputes net benefit and ROI as these inputs change.

## Model results (measured, held-out 30% test set)

- **Model:** XGBoost (gradient-boosted trees), selected over Logistic Regression and Random Forest.
- **Primary metric:** ROC-AUC; secondary: Accuracy, F1.
- **Scores:** ROC-AUC ≈ 0.70, Accuracy ≈ 0.64, F1 ≈ 0.64 (random baseline = 0.50).

## Method & tooling citations

- **XGBoost** — Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System.* KDD '16.
- **scikit-learn** — Pedregosa et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR 12.

## Dataset

Company A telecom dataset, provided with the **GCI World 2026** assignment. Redistribution rights are
unconfirmed, so the raw CSVs are not committed to this repository (see the README for how to obtain
the data).
