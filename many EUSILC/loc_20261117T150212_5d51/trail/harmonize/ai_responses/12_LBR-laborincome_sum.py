import numpy as np
import pandas as pd

def run(tables, report):
    df = tables["silc24_p"]
    cols = ["fg010", "fg020", "fg030", "fg040"]
    present = df[cols].notna().any(axis=1)
    total = df[cols].fillna(0).sum(axis=1)
    df["__derived.laborincome__"] = np.where(present, total, np.nan)
