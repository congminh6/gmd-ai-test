import pandas as pd
import numpy as np


def run(tables, report):
    hh = tables["silc24_h"]
    pr = tables["silc24_pr"]

    # Count persons per household from the full person register (all ages)
    hsize = (
        pr.groupby("hh_id")["pers_id"].nunique(dropna=True)
        .rename("__derived.hsize__")
        .reset_index()
    )

    base = hh[["hh_id", "hg110"]].copy()
    out = base.merge(hsize, on="hh_id", how="left")

    denom = out["__derived.hsize__"].replace({0: np.nan}).astype(float)
    out["__derived.welfare_pc__"] = out["hg110"].astype(float) / denom

    tables["wlf_hh"] = out[["hh_id", "__derived.hsize__", "__derived.welfare_pc__"]]
