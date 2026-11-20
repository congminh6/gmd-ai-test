import pandas as pd
import numpy as np


def run(tables, report):
    df = tables["ses54_user_rec02"]
    age = pd.to_numeric(df["HM04"], errors="coerce")
    df["__derived.childyr__"] = age.where(age < 5)
