import numpy as np
import pandas as pd


def run(tables, report):
    df = tables["rt002"]

    # Age: drop implausible ages outside canon range (0-120)
    age = df["s01a_q04"]
    df["__derived.age__"] = age.where((age >= 0) & (age <= 120))

    # Child age in months: keep only canon range (0-59)
    mth = df["s03b_q02"]
    df["__derived.childmth__"] = mth.where((mth >= 0) & (mth <= 59))

    # Literacy: 1 if can both read and write, 0 otherwise; treat 0/4 as not-asked/unknown -> missing
    can_read = df["s02a_q03"].replace({0: np.nan})
    can_write = df["s02a_q04"].replace({0: np.nan, 4: np.nan})

    lit = np.where((can_read == 1) & (can_write == 1), 1,
                   np.where(can_read.isna() | can_write.isna(), np.nan, 0))
    df["__derived.literacy__"] = lit

    # Ever attended school: infer from any non-zero response to where-last-study OR highest-class
    where_study = df["s02a_q06"]
    highest_class = df["s02a_q05"]
    ever = np.where((where_study > 0) | (highest_class > 0), 1,
                    np.where((where_study == 0) & (highest_class == 0), 0, np.nan))
    df["__derived.everattend__"] = ever
