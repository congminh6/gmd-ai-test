import pandas as pd


def run(tables, report):
    # agecat is the survey's own age category for a delivery that releases no age in years. The decision is the
    # delivery's, never a row's: the column is filled for every person or for none. A delivery where any row has
    # an age (RX010) has ages, and carries no class. A delivery with none carries the year of birth as released
    # (RB080: a 5-year class under Eurostat's disclosure rules) - and only when every row has it. The answer is
    # written as a column that holds the same value in every row, for the binding of agecat to read.
    r = tables["PRT__EU-SILC_v01_M_v01_A_UDB-C_R"]
    age = pd.to_numeric(r["rx010"], errors="coerce")
    born = r["rb080"]
    applies = bool(not age.notna().any() and born.notna().all())
    r["__derived.agecat_applies__"] = int(applies)
    tables["PRT__EU-SILC_v01_M_v01_A_UDB-C_R"] = r
    report.add("DEM-agecat", "prelude", "R: whether this delivery carries the year-of-birth class as agecat",
               rows=len(r), rows_with_age=int(age.notna().sum()), rows_with_birth_class=int(born.notna().sum()),
               applies=applies)
