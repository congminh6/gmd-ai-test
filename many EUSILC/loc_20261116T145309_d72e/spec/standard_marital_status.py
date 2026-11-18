import pandas as pd


def run(tables, report):
    # PB190 is the de jure marital status (1 never married, 2 married, 3 separated, 4 widowed, 5 divorced).
    # PB200 says whether the person lives in a consensual union, both partners in the household (1 yes, on a
    # legal basis; 2 yes, without a legal basis; 3 no). The status the binding places is PB190's code, and
    # 6 "in a consensual union without a legal basis" where PB200 is 2 and the person is not legally married:
    # a legal marriage stands, whatever PB200 says. PB200 missing leaves PB190's code as it is.
    p = tables["LUX__EU-SILC_v01_M_v01_A_UDB-C_P"]
    status = pd.to_numeric(p["pb190"], errors="coerce")
    status = status.where(status.between(1, 5))
    union = pd.to_numeric(p["pb200"], errors="coerce")
    de_facto = (union == 2) & (status != 2)
    p["__derived.marital_status__"] = status.mask(de_facto, 6)
    tables["LUX__EU-SILC_v01_M_v01_A_UDB-C_P"] = p
    report.add("marital_status", "prelude", "P: PB190, and 6 where PB200 is a union without a legal basis",
               rows=int(p["__derived.marital_status__"].notna().sum()), in_union=int(de_facto.sum()),
               in_union_never_married=int((de_facto & (status == 1)).sum()),
               in_union_status_missing=int((de_facto & status.isna()).sum()),
               married_kept=int(((union == 2) & (status == 2)).sum()))
