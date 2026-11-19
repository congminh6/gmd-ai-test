import numpy as np
import pandas as pd


def run(tables, report):
    df = tables["rt002"]
    age = df["s01a_q04"]
    mth = df["s03b_q02"]

    # Default: not in universe (age>=5) -> NaN (binding routes to .c)
    out = pd.Series(np.nan, index=df.index, dtype="float64")

    under5 = age < 5
    valid = under5 & mth.notna() & (mth >= 0) & (mth <= 59)
    invalid = under5 & mth.notna() & (mth > 59)

    out.loc[valid] = mth.loc[valid].astype("float64")
    # sentinel for invalid values within universe
    out.loc[invalid] = -1.0

    df["__derived.childmth_clean__"] = out
