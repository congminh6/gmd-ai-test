import pandas as pd
import numpy as np

def run(tables, report):
    df = tables["silc24_pr"]
    age = pd.to_numeric(df["fk070"], errors="coerce")
    mob = pd.to_numeric(df["fk075"], errors="coerce")

    # completed months at 31 Dec 2023 using month of birth and completed years at that date
    m = age * 12 + (12 - mob)

    # restrict to under-5 and plausible inputs
    m = m.where((age >= 0) & (age < 5) & (mob >= 1) & (mob <= 12))

    df["__derived.childmth__"] = m
