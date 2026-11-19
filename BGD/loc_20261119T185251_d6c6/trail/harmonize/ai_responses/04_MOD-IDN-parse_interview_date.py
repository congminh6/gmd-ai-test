import pandas as pd
import numpy as np
import re


def _parse_best(series: pd.Series) -> pd.Series:
    """Parse dates from strings with a simple dayfirst heuristic."""
    s = series.astype("string").str.strip()
    s = s.replace({"": pd.NA, "NA": pd.NA, "N/A": pd.NA, "nan": pd.NA})

    # Special-case YYYYMMDD
    yyyymmdd = s.str.fullmatch(r"\d{8}")

    dt1 = pd.to_datetime(s.where(~yyyymmdd, pd.NA), errors="coerce", dayfirst=False)
    dt2 = pd.to_datetime(s.where(~yyyymmdd, pd.NA), errors="coerce", dayfirst=True)
    dt_ymd = pd.to_datetime(s.where(yyyymmdd, pd.NA), format="%Y%m%d", errors="coerce")

    # Choose the parse (dayfirst false/true) with more successes
    ok1 = int(dt1.notna().sum())
    ok2 = int(dt2.notna().sum())
    dt = dt1 if ok1 >= ok2 else dt2

    # Fill any missing from the YYYYMMDD parse
    dt = dt.fillna(dt_ymd)
    return dt


def run(tables, report):
    df = tables["rt001"]
    if "s09b1w1_" not in df.columns:
        raise KeyError("rt001.s09b1w1_ not found")

    dt = _parse_best(df["s09b1w1_"])

    df["__derived.intyear__"] = dt.dt.year
    df["__derived.intmonth__"] = dt.dt.month

    report.add(
        "parse_interview_date",
        kind="info",
        detail="Parsed rt001.s09b1w1_ into __derived.intyear__/__derived.intmonth__",
        parsed=int(dt.notna().sum()),
        total=int(len(dt)),
    )
