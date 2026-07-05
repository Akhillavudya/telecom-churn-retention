"""
Generate a small SYNTHETIC sample of the telecom dataset into data/sample/.

The real GCI CSVs (data/raw/) are licensing-restricted and git-ignored, so a person
who clones the public repo has no data to run on. This script reads the real files
LOCALLY and emits fake-but-realistic stand-ins: same columns, dtypes, missingness,
and value ranges, but every value is drawn from a fitted distribution -- no real
customer row survives. A mild, documented eqpdays/change_mou -> churn signal is baked
in so the pipeline still produces a non-degenerate lift curve on the sample.

Run (needs the real data present):  python src/make_sample_data.py
"""

import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "sample"
N = 3000
SEED = 42


def synth_column(s, rng):
    """Draw N synthetic values mimicking one real column's type, range, and missing rate."""
    miss = float(s.isna().mean())
    nonnull = s.dropna()
    if pd.api.types.is_numeric_dtype(s):
        mu, sd = float(nonnull.mean()), float(nonnull.std())
        lo, hi = float(nonnull.min()), float(nonnull.max())
        vals = np.clip(rng.normal(mu, sd if sd > 0 else 1.0, N), lo, hi)
        if pd.api.types.is_integer_dtype(s):
            vals = np.round(vals)                      # integer-valued, but float so NaN can live here
    else:
        freq = nonnull.astype(str).value_counts(normalize=True)
        vals = rng.choice(freq.index.to_numpy(), size=N, p=freq.to_numpy()).astype(object)
    out = pd.Series(vals)
    if miss > 0:
        out[rng.random(N) < miss] = np.nan            # reproduce the column's missingness
    return out


def synth_frame(real, rng, skip):
    """Build a synthetic DataFrame column-by-column, skipping columns handled specially."""
    return pd.DataFrame({c: synth_column(real[c], rng) for c in real.columns if c not in skip})


def make_churn(eqpdays, change_mou, rng):
    """Assign ~50/50 churn with a mild, honest eqpdays-up / change_mou-down signal."""
    def z(x):
        x = pd.to_numeric(x, errors="coerce").fillna(pd.to_numeric(x, errors="coerce").median())
        return (x - x.mean()) / (x.std() + 1e-9)
    logit = 0.7 * z(eqpdays) - 0.7 * z(change_mou) + rng.normal(0, 1.0, N)
    prob = 1 / (1 + np.exp(-(logit - logit.mean())))  # centre so the base rate lands near 50%
    return (rng.random(N) < prob).astype(int)


def main():
    """Read the real CSVs, synthesise both tables on a shared ID set, and write data/sample/."""
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    client = pd.read_csv(RAW / "Client.csv")
    record = pd.read_csv(RAW / "Record.csv")

    ids = np.arange(1, N + 1)
    client_syn = synth_frame(client, rng, skip={"Customer_ID"})
    record_syn = synth_frame(record, rng, skip={"Customer_ID", "churn"})
    client_syn["Customer_ID"] = ids
    record_syn["Customer_ID"] = ids
    record_syn["churn"] = make_churn(client_syn["eqpdays"], record_syn["change_mou"], rng)

    client_syn = client_syn[client.columns]           # keep the original column order
    record_syn = record_syn[record.columns]
    client_syn.to_csv(OUT / "Client.csv", index=False)
    record_syn.to_csv(OUT / "Record.csv", index=False)
    print(f"Wrote {N}-row synthetic sample -> {OUT}")
    print(f"  Client.csv {client_syn.shape} | Record.csv {record_syn.shape} | "
          f"churn rate {record_syn['churn'].mean():.3f}")


if __name__ == "__main__":
    main()
