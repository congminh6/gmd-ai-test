import pandas as pd


def run(tables, report):
    # PE041 is the ISCED-2011 3-digit attainment code (0, 100, 200, 340, 344, 350, 353, 354, 450, 500, 600, 700,
    # 800): its hundreds digit is the ISCED level the canon's anchor places (0..8). Missing stays missing.
    # A delivery that releases the level alone (one digit, 0..8: IRL 2025 in the UDB) carries the level itself.
    p = tables["SRB__EU-SILC_v01_M_v01_A_UDB-C_P"]
    code = pd.to_numeric(p["pe041"], errors="coerce")
    level = (code // 100).where(code >= 100, code.where(code <= 8))
    p["__derived.isced_level__"] = level.where(code.notna())
    tables["SRB__EU-SILC_v01_M_v01_A_UDB-C_P"] = p
    report.add("isced_level", "prelude", "P: ISCED level = PE041 // 100",
               rows=int(code.notna().sum()), levels=sorted(int(x) for x in level.dropna().unique()),
               one_digit=int(((code > 0) & (code <= 8)).sum()))
