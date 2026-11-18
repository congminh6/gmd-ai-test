import pandas as pd


def run(tables, report):
    # The UDB form: income variables are in EURO; HX010 is the conversion factor euro -> national currency (missing
    # when the national currency is the euro). Disposable household income (HY020) in the national currency per
    # household member (HB120, the 2021+ household size). The aggregate is Eurostat's; the currency conversion and
    # the per-capita division are this prelude's.
    h = tables["AUT__EU-SILC_v01_M_v01_A_UDB-C_H"]
    income = pd.to_numeric(h["hy020"], errors="coerce")
    rate = pd.to_numeric(h["hx010"], errors="coerce").fillna(1.0)
    size = pd.to_numeric(h["hb120"], errors="coerce")
    # HY020 may be negative (losses from self-employment outweigh the rest; the standard's range is signed); the
    # canon's welfare is non-negative, so a negative disposable income is left missing here — an open question for
    # the GMD team (SOURCES.md), counted in the report.
    h["__derived.welfare_pc__"] = (income * rate / size).where((size > 0) & (income >= 0))
    tables["AUT__EU-SILC_v01_M_v01_A_UDB-C_H"] = h
    report.add("welfare_pc", "prelude", "H (UDB): welfare_pc = HY020 * HX010 / HB120; negative HY020 left missing",
               rows=int(((size > 0) & (income >= 0)).sum()),
               euro_country=bool(pd.to_numeric(h["hx010"], errors="coerce").isna().all()), negative=int((income < 0).sum()))
