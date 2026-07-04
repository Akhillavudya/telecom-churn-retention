"""
GCI World 2026 Spring - Final Assignment
Company A (Telecom) - Value-Weighted Churn Retention Proposal

Reproducible end-to-end analysis:
  load -> EDA -> feature engineering -> model comparison -> evaluation -> business impact

Run:  python analysis.py
Figures are written to ./figures/ and key numbers printed to stdout.
"""

import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # save figures to files, never open a GUI window
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve,
)
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


# make it:
# repo root = two levels up from this file (src/ -> project root)
ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")
PALETTE = {"stayed": "#4C72B0", "churned": "#C44E52"}


def savefig(name):
    plt.tight_layout()
    plt.savefig(FIG_DIR / name, dpi=150, bbox_inches="tight")
    plt.close()


# ----------------------------------------------------------------------------
# 1. LOAD & MERGE
# ----------------------------------------------------------------------------
here = Path(__file__).resolve().parent
client = pd.read_csv(ROOT / "data" / "raw" / "Client.csv")
record = pd.read_csv(ROOT / "data" / "raw" / "Record.csv")
df = record.merge(client, on="Customer_ID", how="inner")
print(f"Client {client.shape} | Record {record.shape} | Merged {df.shape}")

# ----------------------------------------------------------------------------
# 2. EDA
# ----------------------------------------------------------------------------
churn_rate = df["churn"].mean()
print(f"\nChurn rate: {churn_rate:.3f}  (n_churn={int(df['churn'].sum())})")

# 2a. Target balance
plt.figure(figsize=(6, 4))
counts = df["churn"].value_counts().sort_index()
plt.bar(["stayed (0)", "churned (1)"], counts.values, color=[PALETTE["stayed"], PALETTE["churned"]])
plt.title("Churn is near-balanced (~50/50)")
plt.ylabel("Customers")
savefig("01_churn_balance.png")

# 2b. Missingness
miss = (df.isna().mean() * 100).sort_values(ascending=False).head(20)
plt.figure(figsize=(8, 7))
sns.barplot(x=miss.values, y=miss.index, color="#937860")
plt.xlabel("% missing")
plt.title("Top 20 columns by missingness")
savefig("02_missingness.png")
print("\nTop missing columns (%):")
print(miss.head(8).round(1).to_string())

# 2c. Equipment age vs churn
plt.figure(figsize=(8, 5))
for k, lbl in [(0, "stayed"), (1, "churned")]:
    plt.hist(df.loc[df.churn == k, "eqpdays"].clip(upper=1500), bins=40,
             alpha=0.55, label=lbl, color=PALETTE[lbl])
plt.xlabel("Equipment age (days)")
plt.ylabel("Customers")
plt.title("Churners skew toward older handsets")
plt.legend()
savefig("03_eqpdays_churn.png")
print(f"\nMean eqpdays  stayed={df.loc[df.churn==0,'eqpdays'].mean():.0f} "
      f"churned={df.loc[df.churn==1,'eqpdays'].mean():.0f}")

# 2d. Churn rate by equipment-age decile (monotone lever check)
df["_eqp_decile"] = pd.qcut(df["eqpdays"].rank(method="first"), 10, labels=False) + 1
eqp_churn = df.groupby("_eqp_decile")["churn"].mean()
plt.figure(figsize=(8, 5))
sns.barplot(x=eqp_churn.index, y=eqp_churn.values, color=PALETTE["churned"])
plt.axhline(churn_rate, ls="--", color="black", lw=1.2, label=f"overall {churn_rate:.0%}")
plt.xlabel("Equipment-age decile (1=newest, 10=oldest)")
plt.ylabel("Churn rate")
plt.title("Churn jumps for older-handset customers")
plt.legend()
savefig("04_churn_by_eqp_decile.png")
print("\nChurn by equipment-age decile:")
print(eqp_churn.round(3).to_string())

# 2e. Revenue distribution (value at stake)
plt.figure(figsize=(8, 5))
plt.hist(df["avgrev"].clip(upper=200), bins=40, color=PALETTE["stayed"])
plt.xlabel("Avg monthly revenue per customer ($)")
plt.ylabel("Customers")
plt.title(f"ARPU distribution (median ${df['avgrev'].median():.0f})")
savefig("05_arpu_dist.png")

df.drop(columns=["_eqp_decile"], inplace=True)

# ----------------------------------------------------------------------------
# 3. FEATURE ENGINEERING + PREPROCESSING
# ----------------------------------------------------------------------------
# Drop ID and columns with very heavy missingness (>40%) - little reliable signal
heavy_missing = (df.isna().mean() > 0.40)
drop_cols = ["Customer_ID"] + df.columns[heavy_missing].tolist()
print(f"\nDropping (ID + >40% missing): {drop_cols}")
data = df.drop(columns=drop_cols).copy()

# Derived features - ratios/deltas that no single raw column captures
eps = 1e-6
data["eqp_per_month"] = data["eqpdays"] / (data["months"] + eps)          # handset age relative to tenure
data["rev_per_min"]   = data["rev_Mean"] / (data["mou_Mean"] + eps)        # price intensity
data["overage_share"] = data["ovrrev_Mean"] / (data["rev_Mean"].abs() + eps)  # bill shock exposure
data["care_intensity"] = data["custcare_Mean"] / (data["mou_Mean"] + eps)  # support friction
data["usage_decline"] = (data["change_mou"] < 0).astype(int)               # recent usage drop flag
data["active_ratio"]  = data["actvsubs"] / (data["uniqsubs"] + eps)        # share of active lines

y = data["churn"].astype(int)
X = data.drop(columns=["churn"])

num_cols = X.select_dtypes(include=np.number).columns.tolist()
cat_cols = X.select_dtypes(exclude=np.number).columns.tolist()
print(f"Features: {X.shape[1]}  (numeric={len(num_cols)}, categorical={len(cat_cols)})")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y
)

# Preprocessing for linear / distance models: impute + scale + ordinal-encode
pre_linear = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("enc", OrdinalEncoder(handle_unknown="use_encoded_value",
                                             unknown_value=-1))]), cat_cols),
])
# Tree models: ordinal-encode categoricals, let trees handle NaN where supported
pre_tree = ColumnTransformer([
    ("num", "passthrough", num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("enc", OrdinalEncoder(handle_unknown="use_encoded_value",
                                             unknown_value=-1))]), cat_cols),
])

# ----------------------------------------------------------------------------
# 4. MODELS
# ----------------------------------------------------------------------------
models = {
    "Logistic Regression": Pipeline([
        ("pre", pre_linear),
        ("clf", LogisticRegression(max_iter=2000, C=0.5)),
    ]),
    "Random Forest": Pipeline([
        ("pre", pre_tree),
        ("imp", SimpleImputer(strategy="median")),
        ("clf", RandomForestClassifier(n_estimators=300, max_depth=14,
                                       n_jobs=-1, random_state=RANDOM_STATE)),
    ]),
    "XGBoost": Pipeline([
        ("pre", pre_tree),
        ("clf", XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=6,
                              subsample=0.9, colsample_bytree=0.9,
                              eval_metric="logloss", random_state=RANDOM_STATE)),
    ]),
}

results = []
proba = {}
for name, pipe in models.items():
    pipe.fit(X_train, y_train)
    p = pipe.predict_proba(X_test)[:, 1]
    pred = (p >= 0.5).astype(int)
    proba[name] = p
    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, pred),
        "ROC-AUC": roc_auc_score(y_test, p),
        "Precision": precision_score(y_test, pred),
        "Recall": recall_score(y_test, pred),
        "F1": f1_score(y_test, pred),
    })

res_df = pd.DataFrame(results).set_index("Model").round(4)
print("\n===== MODEL COMPARISON (held-out 30% test) =====")
print(res_df.to_string())

best_name = res_df["ROC-AUC"].idxmax()
best_proba = proba[best_name]
best_model = models[best_name]
print(f"\nBest model by ROC-AUC: {best_name}")

# 4a. Model comparison bar
plt.figure(figsize=(9, 5))
res_df[["Accuracy", "ROC-AUC", "F1"]].plot(kind="bar", ax=plt.gca())
plt.ylim(0.45, max(0.75, res_df["ROC-AUC"].max() + 0.05))
plt.axhline(0.5, ls="--", color="grey", lw=1, label="random baseline")
plt.title("Model comparison")
plt.ylabel("Score")
plt.xticks(rotation=15)
plt.legend(loc="lower right", fontsize=11)
savefig("06_model_comparison.png")

# 4b. ROC curves
plt.figure(figsize=(7, 6))
for name, p in proba.items():
    fpr, tpr, _ = roc_curve(y_test, p)
    plt.plot(fpr, tpr, label=f"{name} (AUC={roc_auc_score(y_test, p):.3f})")
plt.plot([0, 1], [0, 1], "--", color="grey")
plt.xlabel("False positive rate")
plt.ylabel("True positive rate")
plt.title("ROC curves")
plt.legend(fontsize=11)
savefig("07_roc.png")

# 4c. Confusion matrix (best model)
cm = confusion_matrix(y_test, (best_proba >= 0.5).astype(int))
plt.figure(figsize=(5.5, 4.5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["stay", "churn"], yticklabels=["stay", "churn"])
plt.title(f"Confusion matrix — {best_name}")
plt.xlabel("Predicted"); plt.ylabel("Actual")
savefig("08_confusion.png")

# 4d. Feature importance (XGBoost gain)
xgb_pipe = models["XGBoost"]
xgb = xgb_pipe.named_steps["clf"]
feat_names = num_cols + cat_cols
imp = pd.Series(xgb.feature_importances_, index=feat_names).sort_values(ascending=False).head(15)
plt.figure(figsize=(8, 7))
sns.barplot(x=imp.values, y=imp.index, color=PALETTE["stayed"])
plt.title("XGBoost feature importance (gain)")
plt.xlabel("Importance")
savefig("09_feature_importance.png")
print("\nTop 10 features (XGBoost gain):")
print(imp.head(10).round(4).to_string())

# ----------------------------------------------------------------------------
# 5. BUSINESS IMPACT — value-weighted top-decile retention campaign
# ----------------------------------------------------------------------------
test = X_test.copy()
test["churn"] = y_test.values
test["score"] = best_proba
test["avgrev"] = df.loc[X_test.index, "avgrev"].values

# Decile lift table (1 = highest risk)
test["risk_decile"] = pd.qcut(test["score"].rank(method="first"), 10, labels=False)
test["risk_decile"] = 10 - test["risk_decile"]  # 1=highest risk
lift = test.groupby("risk_decile").agg(
    customers=("churn", "size"),
    churn_rate=("churn", "mean"),
    avg_arpu=("avgrev", "mean"),
).round(3)
lift["lift_vs_base"] = (lift["churn_rate"] / churn_rate).round(2)
print("\n===== DECILE LIFT TABLE =====")
print(lift.to_string())

# Cumulative gains
order = test.sort_values("score", ascending=False)
order["cum_churn"] = order["churn"].cumsum()
total_churn = order["churn"].sum()
order["cum_pct_customers"] = np.arange(1, len(order) + 1) / len(order)
order["cum_pct_churn"] = order["cum_churn"] / total_churn
plt.figure(figsize=(7, 6))
plt.plot(order["cum_pct_customers"], order["cum_pct_churn"], color=PALETTE["churned"], lw=2.5, label="model")
plt.plot([0, 1], [0, 1], "--", color="grey", label="random")
plt.xlabel("Fraction of customers contacted (ranked by risk)")
plt.ylabel("Fraction of churners captured")
plt.title("Cumulative gains — targeting works")
plt.legend()
savefig("10_cumulative_gains.png")

# ---- Expected-value model (assumptions stated; tune/cite in slides) ----
TARGET_FRACTION = 0.20      # contact top 20% by risk
OFFER_COST      = 50.0      # $ per contacted customer (bill credit / handset subsidy)
SUCCESS_RATE    = 0.30      # fraction of true would-be churners actually retained
HORIZON_MONTHS  = 12        # value horizon for a saved customer
BASE_CUSTOMERS  = len(df)   # scale test economics to full book

n_target_test = int(len(test) * TARGET_FRACTION)
targeted = order.head(n_target_test)
true_churners_in_target = int(targeted["churn"].sum())
arpu_target = targeted.loc[targeted["churn"] == 1, "avgrev"].mean()

# scale to full customer base
scale = BASE_CUSTOMERS / len(test)
contacted_full = n_target_test * scale
churners_caught_full = true_churners_in_target * scale
saved = churners_caught_full * SUCCESS_RATE
revenue_retained = saved * arpu_target * HORIZON_MONTHS
campaign_cost = contacted_full * OFFER_COST
net_benefit = revenue_retained - campaign_cost
roi = net_benefit / campaign_cost

recall_at_target = true_churners_in_target / total_churn
precision_at_target = targeted["churn"].mean()

print("\n===== BUSINESS IMPACT (full 100k book, stated assumptions) =====")
print(f"Target: top {TARGET_FRACTION:.0%} by risk  -> contact ~{contacted_full:,.0f} customers")
print(f"Capture {recall_at_target:.0%} of all churners (precision in group {precision_at_target:.0%})")
print(f"Avg ARPU of targeted churners: ${arpu_target:,.1f}/mo")
print(f"Assumptions: offer ${OFFER_COST:.0f}/cust, success {SUCCESS_RATE:.0%}, horizon {HORIZON_MONTHS} mo")
print(f"Customers saved:        {saved:,.0f}")
print(f"Revenue retained:       ${revenue_retained:,.0f}")
print(f"Campaign cost:          ${campaign_cost:,.0f}")
print(f"NET BENEFIT:            ${net_benefit:,.0f}   (ROI {roi:.1f}x)")

# Sensitivity to success rate
plt.figure(figsize=(8, 5))
rates = np.linspace(0.1, 0.5, 9)
nets = [(churners_caught_full * r * arpu_target * HORIZON_MONTHS - campaign_cost) for r in rates]
plt.plot(rates, np.array(nets) / 1e6, marker="o", color=PALETTE["stayed"])
plt.axhline(0, ls="--", color="black", lw=1)
plt.xlabel("Offer success rate (assumption)")
plt.ylabel("Net benefit ($M)")
plt.title("Net benefit is robust across success-rate assumptions")
savefig("11_sensitivity.png")

print(f"\nAll figures saved to {FIG_DIR}")
print("DONE.")
