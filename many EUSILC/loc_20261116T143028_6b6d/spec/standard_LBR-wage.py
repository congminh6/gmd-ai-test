import pandas as pd


def run(tables, report):
    # The user database gives every income variable in EURO; HX010 is the conversion factor to the national
    # currency (1 in a euro country). The annual incomes from work of the income reference year, in the national
    # currency, as their own table keyed by the person id alone, like the personal file (so a gate can read the
    # person's labor status); the key correspondences PB030 -> RB030, PX030 -> RX030 and HB030 -> RX030 are
    # applied before preludes run.
    p, h = tables["SRB__EU-SILC_v01_M_v03_A_UDB-C_P"], tables["SRB__EU-SILC_v01_M_v03_A_UDB-C_H"]
    rate = pd.to_numeric(p["rx030"].map(h.drop_duplicates("rx030").set_index("rx030")["hx010"]), errors="coerce").fillna(1.0)
    wage = pd.to_numeric(p["py010g"], errors="coerce") * rate
    # employee cash income and the cash benefits or losses from self-employment: the income from every job
    work = p[["py010g", "py050g"]].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1) * rate
    tables["wage_lcu"] = pd.DataFrame({"rb030": p["rb030"], "__derived.wage_annual__": wage,
                                       "__derived.labor_income__": work})
    report.add("LBR-wage", "prelude", "wage_lcu: PY010G * HX010 and (PY010G + PY050G) * HX010 (annual, national currency)",
               rows=int(wage.notna().sum()), positive=int((wage > 0).sum()), labor_income_negative=int((work < 0).sum()))
