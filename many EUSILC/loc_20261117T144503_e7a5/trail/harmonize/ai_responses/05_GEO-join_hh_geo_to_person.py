import pandas as pd


def run(tables, report):
    p = tables["silc24_p"][["pers_id", "hh_id"]].copy()
    h = tables["silc24_h"][["hh_id", "hb031"]].copy()

    h = h.drop_duplicates(subset=["hh_id"], keep="first")

    merged = p.merge(h, on="hh_id", how="left", validate="m:1")

    out = merged[["pers_id"]].copy()
    out["__derived_hb031__"] = merged["hb031"]

    tables["geo_pers"] = out
