"""
Build the 15-slide business-proposal deck -> LavudyaAkhil31.pdf
Self-contained: renders each slide with matplotlib and writes a single PDF.
Run:  python make_slides.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.image as mpimg

plt.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["text.parse_math"] = False    # treat '$' as a literal dollar sign

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "reports" / "figures"
W, H = 13.333, 7.5            # 16:9 inches

# palette
ACCENT  = "#0E6655"          # deep teal
ACCENT2 = "#16A085"
DARK    = "#1C2833"
GRAY    = "#5D6D7E"
LIGHT   = "#EAF2EF"
RED     = "#C0392B"

AUTHOR = "Lavudya Akhil  ·  GCI World 2026 Spring — Final Assignment"

pdf = PdfPages(ROOT / "reports" / "Slides.pdf")
_page = {"n": 0}


def new_slide(footer=True, page_num=True):
    fig = plt.figure(figsize=(W, H), dpi=200)
    fig.patch.set_facecolor("white")
    bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, 1); bg.set_ylim(0, 1); bg.axis("off")
    bg.add_patch(Rectangle((0, 0), 0.013, 1, color=ACCENT, zorder=5))      # left brand bar
    _page["n"] += 1
    if footer:
        bg.add_line(plt.Line2D([0.055, 0.945], [0.075, 0.075], color="#D5DBDB", lw=1))
        bg.text(0.055, 0.045, AUTHOR, fontsize=9, color=GRAY, va="center")
    if page_num:
        bg.text(0.945, 0.045, f"{_page['n']}/15", fontsize=9, color=GRAY,
                va="center", ha="right")
    return fig, bg


def header(bg, title, kicker=None):
    y = 0.90
    if kicker:
        bg.text(0.055, 0.935, kicker.upper(), fontsize=11, color=ACCENT2,
                fontweight="bold", va="center")
    bg.text(0.055, y, title, fontsize=27, color=DARK, fontweight="bold", va="top")
    bg.add_line(plt.Line2D([0.057, 0.30], [0.845, 0.845], color=ACCENT, lw=3.5))


def bullets(bg, items, x=0.07, y0=0.74, dy=0.083, size=15, color=DARK, bold_lead=False):
    y = y0
    for it in items:
        bg.text(x, y, "▪", fontsize=12, color=ACCENT, va="top")
        if bold_lead and "—" in it:
            lead, rest = it.split("—", 1)
            bg.text(x + 0.022, y, lead.strip(), fontsize=size, color=DARK,
                    fontweight="bold", va="top")
            bg.text(x + 0.022 + 0.012 * len(lead), y, "— " + rest.strip(),
                    fontsize=size, color=GRAY, va="top")
        else:
            bg.text(x + 0.022, y, it, fontsize=size, color=color, va="top", wrap=True)
        y -= dy


def place_image(fig, path, box):
    """Place image preserving aspect ratio, centered in box=[x,y,w,h] (fig fraction)."""
    img = mpimg.imread(str(path))
    ih, iw = img.shape[0], img.shape[1]
    bx, by, bw, bh = box
    box_ar = (bw * W) / (bh * H)
    img_ar = iw / ih
    if img_ar > box_ar:           # image wider -> fit width
        nw = bw; nh = bw * (W / H) / img_ar
    else:                         # fit height
        nh = bh; nw = bh * (H / W) * img_ar
    nx = bx + (bw - nw) / 2; ny = by + (bh - nh) / 2
    ax = fig.add_axes([nx, ny, nw, nh]); ax.imshow(img); ax.axis("off")


def metric_card(bg, x, y, w, h, big, label, color=ACCENT):
    bg.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.02",
                                fc=LIGHT, ec=color, lw=1.6, zorder=2))
    bg.text(x + w / 2, y + h * 0.62, big, fontsize=26, color=color,
            fontweight="bold", ha="center", va="center")
    bg.text(x + w / 2, y + h * 0.24, label, fontsize=11, color=GRAY,
            ha="center", va="center")


def source(bg, text):
    bg.text(0.055, 0.105, text, fontsize=8.5, color=GRAY, style="italic", va="center")


# ============================================================ SLIDE 1 — TITLE
fig, bg = new_slide(footer=False, page_num=False)
bg.add_patch(Rectangle((0, 0), 1, 1, color="white"))
bg.add_patch(Rectangle((0, 0), 0.013, 1, color=ACCENT))
bg.add_patch(Rectangle((0, 0.0), 1, 0.16, color=ACCENT, alpha=0.10))
bg.text(0.06, 0.70, "Turning Churn Risk into Retained Revenue", fontsize=31,
        color=DARK, fontweight="bold", va="center")
bg.text(0.06, 0.60, "A value-weighted retention proposal for Company A (Telecom)",
        fontsize=19, color=ACCENT, va="center")
bg.add_line(plt.Line2D([0.062, 0.45], [0.535, 0.535], color=ACCENT, lw=3))
bg.text(0.06, 0.45, "Proof-of-Concept · Data-driven business proposal backed by a machine-learning model",
        fontsize=13, color=GRAY, va="center")
bg.text(0.06, 0.20, "Lavudya Akhil", fontsize=16, color=DARK, fontweight="bold", va="center")
bg.text(0.06, 0.155, "Omnicampus: LavudyaAkhil31   ·   GCI World 2026 Spring   ·   June 2026",
        fontsize=12, color=GRAY, va="center")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 2 — EXEC SUMMARY
fig, bg = new_slide()
header(bg, "Executive summary", "the one-slide takeaway")
bg.text(0.055, 0.80,
        "Company A can grow margin fastest by keeping the customers it already has.\n"
        "I built a model that ranks every customer by churn risk and revenue at stake, so the\n"
        "retention team spends its budget only where it pays back.",
        fontsize=15, color=DARK, va="top", linespacing=1.5)
metric_card(bg, 0.055, 0.30, 0.20, 0.20, "0.70", "Model ROC-AUC (XGBoost)")
metric_card(bg, 0.285, 0.30, 0.20, 0.20, "79.5%", "churn in the top-risk decile")
metric_card(bg, 0.515, 0.30, 0.20, 0.20, "$2.07M", "net benefit / year", color=RED)
metric_card(bg, 0.745, 0.30, 0.20, 0.20, "2.1×", "return on campaign spend", color=RED)
bg.text(0.055, 0.20,
        "Recommendation: target the top 20% highest-risk, high-value customers with a handset-upgrade /\n"
        "bill-credit offer. This captures ~30% of all churners and is net-positive even under conservative assumptions.",
        fontsize=12.5, color=GRAY, va="top", linespacing=1.5)
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 3 — MARKET
fig, bg = new_slide()
header(bg, "Why retention is the right lever", "market context")
bullets(bg, [
    "Mobile markets like India are saturated — net new connections are scarce, so operators "
    "grow by lifting revenue-per-user and cutting churn, not by adding subscribers.",
    "Winning back a lost subscriber costs several times more than keeping an existing one — "
    "retention is the cheaper, higher-margin growth lever.",
    "Churn is not random: usage decline, ageing handsets and support friction show up months "
    "before a customer leaves — so churn is predictable, and therefore preventable.",
    "Implication for Company A: a model that flags at-risk, high-value customers early turns a "
    "reactive cost into a proactive, measurable revenue play.",
], y0=0.76, dy=0.135, size=14.5)
source(bg, "Sources: Harvard Business Review (2014) [1]; TRAI Performance Indicators [2]; GSMA, The Mobile Economy [3]. See References.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 4 — CLIENT & DATA
fig, bg = new_slide()
header(bg, "The client and the data", "starting point")
bullets(bg, [
    "Company A — a wireless operator with ~100,000 customers and no in-house ML capability.",
    "Two linked tables joined 1:1 on Customer_ID into a single 100,000 × 100 analysis table.",
], y0=0.78, dy=0.085, size=15)
# two table cards
bg.add_patch(FancyBboxPatch((0.055, 0.30), 0.41, 0.28,
             boxstyle="round,pad=0.008,rounding_size=0.02", fc=LIGHT, ec=ACCENT, lw=1.6))
bg.text(0.075, 0.545, "Client.csv", fontsize=16, color=ACCENT, fontweight="bold", va="top")
bg.text(0.075, 0.49, "One row per customer:\n• tenure, plan, credit class\n• demographics\n• equipment (handset age, price)",
        fontsize=12.5, color=DARK, va="top", linespacing=1.5)
bg.add_patch(FancyBboxPatch((0.53, 0.30), 0.41, 0.28,
             boxstyle="round,pad=0.008,rounding_size=0.02", fc=LIGHT, ec=ACCENT, lw=1.6))
bg.text(0.55, 0.545, "Record.csv", fontsize=16, color=ACCENT, fontweight="bold", va="top")
bg.text(0.55, 0.49, "One row per customer:\n• monthly usage & minutes\n• billing & overage\n• call quality + churn target",
        fontsize=12.5, color=DARK, va="top", linespacing=1.5)
bg.text(0.055, 0.21, "Target variable: churn = 1 if the customer left within 31–60 days of the observation date.",
        fontsize=13, color=GRAY, va="center")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 5 — EDA DATA QUALITY
fig, bg = new_slide()
header(bg, "What the data is — and isn't — good for", "exploratory analysis (1/2)")
place_image(fig, FIG / "01_churn_balance.png", [0.055, 0.16, 0.40, 0.62])
place_image(fig, FIG / "02_missingness.png",  [0.50, 0.14, 0.45, 0.64])
bg.text(0.055, 0.135, "Churn is ~50/50 — accuracy is meaningful, but I rank by probability (ROC-AUC) for targeting.",
        fontsize=11.5, color=DARK, va="center")
source(bg, "Demographic columns are 30–50% missing (third-party append) and are dropped; operator-owned usage/billing data is near-complete and actionable.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 6 — EDA THE LEVER
fig, bg = new_slide()
header(bg, "The lever: ageing handsets drive churn", "exploratory analysis (2/2)")
place_image(fig, FIG / "04_churn_by_eqp_decile.png", [0.05, 0.17, 0.44, 0.60])
place_image(fig, FIG / "05_arpu_dist.png",           [0.52, 0.17, 0.44, 0.60])
bg.text(0.055, 0.135,
        "Newer-handset customers churn ~37–43%; older-handset customers ~53–60% — a clear, intervenable threshold.\n"
        "Revenue is right-skewed, so a few high-ARPU customers carry outsized value.",
        fontsize=11, color=DARK, va="center", linespacing=1.4)
source(bg, "Handset age is one of the few churn drivers the business can actually change (upgrade / subsidy) — unlike tenure or demographics.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 7 — PROBLEM DEFINITION
fig, bg = new_slide()
header(bg, "Problem definition", "from data to a question")
rows = [
    ("Business question", "Which customers should we spend retention budget on, and what is the return?"),
    ("Target variable", "churn (binary) — justified by EDA: balanced, and tied to an actionable lever."),
    ("ML task", "Classification used as a ranking model — score every customer by churn probability."),
    ("Primary metric", "ROC-AUC (threshold-free, suits ranking); Accuracy / F1 reported as support."),
    ("Who acts on it", "Retention / CRM team — sends a targeted offer to the highest-risk, high-value list."),
]
y = 0.76
for k, v in rows:
    bg.text(0.06, y, k, fontsize=14.5, color=ACCENT, fontweight="bold", va="top")
    bg.text(0.30, y, v, fontsize=13.5, color=DARK, va="top")
    y -= 0.125
source(bg, "The model is evidence for a decision, not the deliverable itself — every choice above serves the retention recommendation.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 8 — APPROACH
fig, bg = new_slide()
header(bg, "Approach: features and models", "method")
bg.text(0.055, 0.79, "Feature engineering — encode business intuition no single column captures:",
        fontsize=15, color=DARK, fontweight="bold", va="top")
bullets(bg, [
    "handset age relative to tenure · price-per-minute · overage (bill-shock) share",
    "support-call intensity · recent usage-decline flag · share of active lines",
], y0=0.71, dy=0.07, size=13.5)
bg.text(0.055, 0.50, "Models compared (weakest → strongest, so the choice is justified):",
        fontsize=15, color=DARK, fontweight="bold", va="top")
bullets(bg, [
    "Logistic Regression — interpretable linear baseline.",
    "Random Forest — captures non-linear interactions.",
    "XGBoost — gradient-boosted trees: strong on tabular data, handles missing values, explainable.",
], y0=0.42, dy=0.072, size=13.5, bold_lead=True)
source(bg, "All models share the same stratified 70/30 train/test split and random_state = 42 for a fair, reproducible comparison.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 9 — MODEL RESULTS
fig, bg = new_slide()
header(bg, "Model results — XGBoost wins", "evaluation")
place_image(fig, FIG / "06_model_comparison.png", [0.05, 0.30, 0.44, 0.48])
place_image(fig, FIG / "07_roc.png",              [0.52, 0.20, 0.42, 0.60])
# scores table (left, below chart)
bg.text(0.055, 0.285, "Held-out test scores", fontsize=12.5, color=ACCENT, fontweight="bold", va="top")
tbl = [("Model", "Acc", "AUC", "F1"),
       ("Logistic Reg.", "0.59", "0.626", "0.58"),
       ("Random Forest", "0.62", "0.679", "0.63"),
       ("XGBoost", "0.64", "0.696", "0.64")]
x0 = 0.055; ys = 0.245; cw = [0.16, 0.07, 0.085, 0.07]
for r, row in enumerate(tbl):
    xx = x0
    for c, cell in enumerate(row):
        bold = (r == 0) or (r == 3)
        col = ACCENT if r == 3 else (DARK if r == 0 else GRAY)
        bg.text(xx, ys - r * 0.033, cell, fontsize=11.5, color=col,
                fontweight="bold" if bold else "normal", va="top")
        xx += cw[c]
bg.text(0.52, 0.155, "Selected model: XGBoost — ROC-AUC 0.70 vs 0.50 random baseline.",
        fontsize=12, color=DARK, va="center", fontweight="bold")
source(bg, "Model: XGBoost · Metric: ROC-AUC = 0.696 (Accuracy 0.64, F1 0.64) on a 30% held-out test set.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 10 — DRIVERS
fig, bg = new_slide()
header(bg, "What the model says drives churn", "interpretation")
place_image(fig, FIG / "09_feature_importance.png", [0.05, 0.16, 0.52, 0.64])
bullets(bg, [
    "Equipment age (eqpdays, age-vs-tenure) is the strongest signal.",
    "Billing & usage level and price-per-minute follow.",
    "Support-call intensity flags service friction.",
], x=0.60, y0=0.70, dy=0.085, size=13.5)
bg.text(0.60, 0.40, "Importance + intervenability:", fontsize=13.5, color=ACCENT,
        fontweight="bold", va="top")
bg.text(0.60, 0.355, "Tenure and demographics rank high but cannot\nbe changed. Handset age can — so it becomes\nthe lever the proposal pulls.",
        fontsize=12.5, color=DARK, va="top", linespacing=1.5)
source(bg, "Feature importance = XGBoost 'gain' (how much each feature improves the model when used).")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 11 — TARGETING WORKS
fig, bg = new_slide()
header(bg, "Targeting by risk works", "from scores to a target list")
place_image(fig, FIG / "10_cumulative_gains.png", [0.52, 0.18, 0.43, 0.60])
bg.text(0.055, 0.78, "Rank by risk, act on the top slice:",
        fontsize=14.5, color=DARK, fontweight="bold", va="top")
# decile mini table
mini = [("Risk decile", "Churn rate", "Lift"),
        ("1 (highest)", "79.5%", "1.60×"),
        ("2", "67.8%", "1.37×"),
        ("3", "61.4%", "1.24×"),
        ("10 (lowest)", "19.3%", "0.39×")]
ys = 0.66; x0 = 0.06; cw = [0.16, 0.13, 0.09]
for r, row in enumerate(mini):
    xx = x0
    for c, cell in enumerate(row):
        bold = (r == 0) or (r == 1)
        col = ACCENT if r == 1 else (DARK if r == 0 else GRAY)
        bg.text(xx, ys - r * 0.05, cell, fontsize=13, color=col,
                fontweight="bold" if bold else "normal", va="top")
        xx += cw[c]
bg.text(0.055, 0.30, "The cumulative-gains curve shows the top 20% of\ncustomers by risk contain ~30% of all churners —\nfar more than the 20% a random campaign would hit.",
        fontsize=12.5, color=DARK, va="top", linespacing=1.5)
source(bg, "Lift = decile churn rate ÷ overall churn rate. A perfectly random target would have lift = 1.0 in every decile.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 12 — BUSINESS IMPACT
fig, bg = new_slide()
header(bg, "Quantified business impact", "the proposal in dollars")
bg.text(0.055, 0.81, "Campaign: contact the top 20% by risk on the full 100,000-customer book.",
        fontsize=14.5, color=DARK, fontweight="bold", va="top")
metric_card(bg, 0.055, 0.50, 0.205, 0.20, "20,000", "customers contacted")
metric_card(bg, 0.275, 0.50, 0.205, 0.20, "~4,400", "churners actually saved")
metric_card(bg, 0.495, 0.50, 0.205, 0.20, "$3.07M", "revenue retained", color=ACCENT)
metric_card(bg, 0.715, 0.50, 0.205, 0.20, "$2.07M", "NET benefit", color=RED)
bg.text(0.055, 0.40, "Assumptions (stated transparently, stress-tested next slide):",
        fontsize=13, color=ACCENT, fontweight="bold", va="top")
bullets(bg, [
    "Offer cost $50 / contacted customer   ·   Offer success rate 30%   ·   Value horizon 12 months",
    "Avg revenue of targeted churners ≈ $58 / month   ·   Campaign cost $1.0M → 2.1× ROI",
], y0=0.34, dy=0.07, size=12.5)
source(bg, "Net benefit = (saved customers × monthly ARPU × 12) − campaign cost. Targeting fraction is model-derived; cost & success rate are planning assumptions.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 13 — ROBUSTNESS
fig, bg = new_slide()
header(bg, "Is the case robust?", "sensitivity analysis")
place_image(fig, FIG / "11_sensitivity.png", [0.05, 0.17, 0.50, 0.62])
bullets(bg, [
    "The biggest unknown is the offer success rate.",
    "The campaign stays net-positive across the full plausible range (10–50%).",
    "Even at a pessimistic 10% success, the program does not lose money.",
    "So the recommendation is robust — not knife-edge on one assumption.",
], x=0.58, y0=0.70, dy=0.10, size=13.5)
source(bg, "A real A/B pilot (Next Steps) would replace the assumed success rate with a measured one before full roll-out.")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 14 — RECOMMENDATION
fig, bg = new_slide()
header(bg, "Recommendation & roadmap", "what to do next")
bg.text(0.055, 0.80, "Recommendation", fontsize=15, color=ACCENT, fontweight="bold", va="top")
bg.text(0.055, 0.755, "Score the customer book monthly; target the top-risk, high-ARPU segment with a handset-upgrade or\n"
        "bill-credit offer, prioritising customers also showing usage decline or support friction.",
        fontsize=13.5, color=DARK, va="top", linespacing=1.5)
bg.text(0.055, 0.58, "Roadmap", fontsize=15, color=ACCENT, fontweight="bold", va="top")
bullets(bg, [
    "Pilot — run a small A/B test to measure the true offer success rate.",
    "Scale — roll out monthly scoring; tune offer cost by ARPU tier.",
    "Explain — add SHAP per-customer reasons for the CRM team.",
    "Sustain — monitor for drift and re-train quarterly.",
], y0=0.52, dy=0.078, size=13.5, bold_lead=True)
bg.text(0.055, 0.165, "Risks: model shows correlation not causation; offer cannibalisation and seasonality are out of scope for the PoC.",
        fontsize=11.5, color=GRAY, va="center")
pdf.savefig(fig); plt.close(fig)

# ============================================================ SLIDE 15 — REFERENCES
fig, bg = new_slide()
header(bg, "References", "sources & methods")
refs = [
    "[1]  A. Gallo, “The Value of Keeping the Right Customers,” Harvard Business Review, 2014.\n       https://hbr.org/2014/10/the-value-of-keeping-the-right-customers",
    "[2]  Telecom Regulatory Authority of India (TRAI), “Indian Telecom Services Performance Indicators.”\n       https://www.trai.gov.in/release-publication/reports",
    "[3]  GSMA, “The Mobile Economy” (annual report series).  https://www.gsma.com/mobileeconomy/",
    "[4]  T. Chen & C. Guestrin, “XGBoost: A Scalable Tree Boosting System,” KDD ’16, 2016.\n       https://doi.org/10.1145/2939672.2939785",
    "[5]  F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” JMLR 12, 2011.\n       https://jmlr.org/papers/v12/pedregosa11a.html",
]
y = 0.77
for r in refs:
    bg.text(0.055, y, r, fontsize=12.5, color=DARK, va="top", linespacing=1.45)
    y -= 0.135
bg.text(0.055, 0.10, "Dataset: Company A telecom dataset provided with the GCI World 2026 final assignment.",
        fontsize=11, color=GRAY, style="italic", va="center")
pdf.savefig(fig); plt.close(fig)

pdf.close()
print(f"Wrote reports/slides.pdf with {_page['n']} slides")
