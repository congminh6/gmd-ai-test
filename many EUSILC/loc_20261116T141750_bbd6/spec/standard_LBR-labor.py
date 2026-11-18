import pandas as pd

# NACE Rev. 2 sections as the user database groups them, on the canon's four categories: agriculture; industry
# (mining to water supply, construction); services (trade to public administration); other (education, health,
# arts and other services) - the grouping the GMD's ten-category classification gives its "other services".
NACE4 = {"a": 1, "b - e": 2, "f": 2, "g": 3, "h": 3, "i": 3, "j": 3, "k": 3, "l - n": 3, "o": 3,
         "p": 4, "q": 4, "r - u": 4}


def run(tables, report):
    p = tables["SVN__EU-SILC_v01_M_v01_A_UDB-C_P"]
    section = p["pl111a"].astype("string").str.strip().str.lower()
    p["__derived.industrycat4__"] = pd.to_numeric(section.map(NACE4), errors="coerce")
    # PL051A is ISCO-08: two digits in most deliveries (the major group is the first digit, 0 for the armed
    # forces: 01-03), one digit in a few (the major group itself).
    code = pd.to_numeric(p["pl051a"], errors="coerce")
    two_digit = bool(code.max() > 9)
    major = (code // 10) if two_digit else code
    p["__derived.isco_major__"] = major.where(code.notna() & major.between(0, 9))
    # the calendar of the income reference year gives each month one main activity, so the four work columns
    # (full-time / part-time, employee / self-employed) never overlap and sum to at most 12
    work = p[["pl073", "pl074", "pl075", "pl076"]].apply(pd.to_numeric, errors="coerce")
    p["__derived.wmonths__"] = work.sum(axis=1, min_count=1).clip(upper=12)
    tables["SVN__EU-SILC_v01_M_v01_A_UDB-C_P"] = p
    report.add("LBR-labor", "prelude", "P: industrycat4 from PL111A, ISCO major group from PL051A, months worked",
               sections_not_placed=int((section.notna() & (section != "") & ~section.isin(list(NACE4))).sum()),
               occupation_digits=2 if two_digit else 1, months_over_12=int((work.sum(axis=1) > 12).sum()))
