import numpy as np
import pandas as pd


def run(tables, report):
    df = tables["silc24_pr"]

    # Age is recorded as age on 2023-12-31; -1 appears in the observed range and is treated as missing.
    age = pd.to_numeric(df["fk070"], errors="coerce")
    age = age.mask(age < 0)
    df["__derived.age__"] = age

    # Child ages for those under 5
    under5 = age.notna() & (age < 5)
    df["__derived.childyr__"] = np.where(under5, age, np.nan)

    # Month-of-birth is 1..12; reference month is December (12) because age is as of Dec 31.
    mob = pd.to_numeric(df["fk075"], errors="coerce")
    childmth = np.where(under5 & mob.notna(), age * 12 + (12 - mob), np.nan)
    # Keep only 0..59
    childmth = np.where((childmth >= 0) & (childmth <= 59), childmth, np.nan)
    df["__derived.childmth__"] = childmth

    tables["silc24_pr"] = df
