import pandas as pd
import numpy as np


def run(tables, report):
    df = tables["silc24_pr"]

    # Clean age: fk070 has an in-band -1 that is outside the valid range.
    age = pd.to_numeric(df["fk070"], errors="coerce")
    age = age.where(age >= 0)
    df["__derived.age__"] = age

    # Child age in years (under 5): same as cleaned age, but only for age < 5.
    df["__derived.childyr__"] = age.where(age < 5)

    # Child age in months at 31 Dec 2023 using year/month of birth.
    yob = pd.to_numeric(df["fk080"], errors="coerce")
    mob = pd.to_numeric(df["fk075"], errors="coerce")

    childmth = (2023 - yob) * 12 + (12 - mob)
    # Keep only plausible under-5 values.
    childmth = childmth.where((age < 5) & (childmth >= 0) & (childmth <= 59))
    df["__derived.childmth__"] = childmth
