import pandas as pd
import numpy as np

def run(tables, report):
    df = tables["silc24_h"]
    # Codes: 1 Yes, 2 No cannot afford, 3 No other reason
    land_yes = df["hh150"].astype("float").eq(1)
    mob_yes = df["hh160"].astype("float").eq(1)
    out = pd.Series(np.where(land_yes | mob_yes, 1, 0), index=df.index)
    # preserve missingness if either source is missing
    out[df["hh150"].isna() & df["hh160"].isna()] = np.nan
    df["__derived.phone_any__"] = out