import pandas as pd
import numpy as np


def run(tables, report):
    df = tables["rt001"]

    # Candidate date string fields observed in the household file
    cands = ["s09a1_40", "s09b1w1_", "s09b1w2_"]

    def to_dt(series):
        # Robust parse with day-first (common in D/M/Y); coerce bad parses to NaT
        s = series.astype(str).str.strip()
        s = s.replace({"": np.nan, "nan": np.nan, "NaN": np.nan})
        return pd.to_datetime(s, errors="coerce", dayfirst=True)

    dt = None
    present = []
    for c in cands:
        if c in df.columns:
            present.append(c)
            cur = to_dt(df[c])
            dt = cur if dt is None else dt.fillna(cur)

    if dt is None:
        df["__derived.intmonth__"] = np.nan
        df["__derived.intyear__"] = np.nan
        report.add("MOD-IDN-intdate_parse", "warning", "No candidate date columns found in rt001", columns=cands)
        return

    df["__derived.intmonth__"] = dt.dt.month
    df["__derived.intyear__"] = dt.dt.year

    bad_month = df["__derived.intmonth__"].notna() & ~df["__derived.intmonth__"].between(1, 12)
    if bad_month.any():
        report.add(
            "MOD-IDN-intdate_parse",
            "warning",
            "Some derived interview months are outside 1..12",
            n_bad=int(bad_month.sum()),
            present_columns=present,
        )
