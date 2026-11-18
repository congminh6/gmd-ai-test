import pandas as pd

def run(tables, report):
    df = tables["SRB__EU-SILC_v01_M_v02_A_UDB-C_R"]
    age = pd.to_numeric(df["rx010"], errors="coerce")
    df["__derived.childyr__"] = age.where((age >= 0) & (age < 5))
