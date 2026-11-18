import pandas as pd
import numpy as np


def run(tables, report):
    hh = tables["silc24_h"]
    p = tables["silc24_p"]

    # Count persons per household (regular members assumed to be the person roster rows)
    hsize = (
        p.groupby("hh_id")["pers_id"].nunique(dropna=True)
        .rename("__derived.hsize__")
        .reset_index()
    )

    base = hh[["hh_id", "hg110"]].copy()
    out = base.merge(hsize, on="hh_id", how="left")

    # Normalize to per-capita welfare; protect against division by zero
    out["__derived.welfare_pc__"] = out["hg110"].astype(float) / out["__derived.hsize__"].replace({0: np.nan}).astype(float)

    tables["wlf_hh"] = out[["hh_id", "__derived.hsize__", "__derived.welfare_pc__"]]
