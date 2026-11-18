import pandas as pd


def run(tables, report):
    # Person-level table (output grain: pers_id)
    p = tables["silc24_p"].copy()
    h = tables["silc24_h"][["hh_id", "hb040"]].copy()

    # Merge household weight onto each person via hh_id
    merged = p[["pers_id", "hh_id"]].merge(h, on="hh_id", how="left", validate="m:1")

    merged = merged.rename(columns={"hb040": "__derived.hh_weight__"})

    # Keep only the output grain key + the derived value
    out = merged[["pers_id", "__derived.hh_weight__"]]

    tables["idn_weights"] = out
