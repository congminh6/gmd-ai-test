import pandas as pd

def run(tables, report):
    df = tables["rt001"]
    psu_num = pd.to_numeric(df["psu"], errors="coerce")
    df["__derived.psu_int__"] = psu_num.round().astype("Int64")
