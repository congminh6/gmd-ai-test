import pandas as pd
import numpy as np

def run(tables, report):
    df = tables["silc24_h"]
    s = pd.to_numeric(df["hh060"], errors="coerce")
    # hh060=10 represents '10 or more' in labels; keep as 10 (lower bound)
    df["__derived.rooms_num__"] = s.where(s.notna(), np.nan)
