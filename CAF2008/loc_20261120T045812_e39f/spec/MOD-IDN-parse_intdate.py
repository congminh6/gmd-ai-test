import pandas as pd
import numpy as np


def run(tables, report):
    df = tables["hhdata"]

    s = pd.to_numeric(df["a4"], errors="coerce")
    s_int = s.astype("Int64")

    def _parse_one(x):
        if pd.isna(x):
            return (np.nan, np.nan)
        try:
            xi = int(x)
        except Exception:
            return (np.nan, np.nan)
        if xi < 0:
            return (np.nan, np.nan)

        ss = str(xi)
        if len(ss) == 5:
            ss = "0" + ss
        # Expect ddmmyy after padding
        if len(ss) != 6:
            return (np.nan, np.nan)

        mm = int(ss[2:4])
        yy = int(ss[4:6])

        # Guard invalid month
        if mm < 1 or mm > 12:
            return (np.nan, np.nan)

        # Expand 2-digit year (assume 19xx for 80-99, else 20xx)
        year = (1900 + yy) if yy >= 80 else (2000 + yy)

        # Guard implausible year (keep conservative bounds)
        if year < 1980 or year > 2100:
            return (np.nan, np.nan)

        return (mm, year)

    parsed = s_int.map(_parse_one)
    df["__derived.intmonth__"] = parsed.map(lambda t: t[0]).astype("Float64")
    df["__derived.intyear__"] = parsed.map(lambda t: t[1]).astype("Float64")
