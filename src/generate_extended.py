# Build data/extended.sqlite: the official DB plus generated rows.
# Rules (methods chapter):
# - Generic counts and distributions only, no question-specific rows.
# - No invented values: a column gets values only if the official DB has values in it.
#   Columns that are NULL throughout the official DB stay NULL (even where the DDL says NOT NULL,
#   exactly as in the official rows). Code/name columns use only values from the official DB.
#   IDs, dates, amounts and numbers follow the official format and vary by distribution.
# - Every FK between the 13 tables resolves; generated IDs start at ID0 (no collision).
# Deterministic: same SEED -> byte-identical DB.
import csv
import itertools
import random
import re
import shutil
import sqlite3
from datetime import date, timedelta

from db import DBS, ROOT, columns, tables

SEED = 20261114  # recorded seed: 2026-11-14
ID0 = 100_000  # first generated ID; official IDs are all below this
CUTOFF = date(
    2026, 11, 14
)  # no generated event lies after this day (fixed, not date.today())

random.seed(SEED)

N_PH, N_AG = (
    60,
    12,
)  # persons by role; only PH and AG occur in the official Agreement_Party_Role
N_POLICIES = 300
N_CATASTROPHES = 8
CLAIMS_PER_POLICY = ([0, 1, 2, 3], [40, 30, 18, 12])


# ---------------------------------------------------------------- helpers
def maybe(value, p):
    """value, or NULL with probability p (only for nullable columns)."""
    return None if random.random() < p else value


def iso(d):
    return d.isoformat() if d else None  # official format: 'YYYY-MM-DD' (date, no time)


def rand_date(a, b):
    return a + timedelta(days=random.randint(0, (b - a).days))


def add_years(d, n):
    return d.replace(year=d.year + n)


def ids():
    return itertools.count(ID0)


def insert(table, rows):
    """Rows give only the filled columns; every other column is NULL."""
    cols = columns(con, table)
    for r in rows:
        assert set(r) <= set(cols), f"{table}: unknown {set(r) - set(cols)}"
    col_list = ", ".join(f'"{c}"' for c in cols)
    marks = ", ".join("?" for _ in cols)
    con.executemany(
        f'INSERT INTO "{table}" ({col_list}) VALUES ({marks})',
        [[r.get(c) for c in cols] for r in rows],
    )
    print(f"  {table}: +{len(rows)}")


def distinct_values(table, col):
    return {
        v
        for (v,) in con.execute(
            f'SELECT DISTINCT "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL'
        )
    }


# ---------------------------------------------------------------- 1. copy official
shutil.copyfile(DBS["official"], DBS["extended"])
con = sqlite3.connect(DBS["extended"])
ts = tables(con)
assert len(ts) == 13, ts

# Generated-row key per table (used for the collision check and to select generated rows)
GEN_KEY = {
    "Catastrophe": "Catastrophe_Identifier",
    "Policy": "Policy_Identifier",
    "Agreement_Party_Role": "Agreement_Identifier",
    "Policy_Coverage_Detail": "Policy_Coverage_Detail_Identifier",
    "Policy_Amount": "Policy_Amount_Identifier",
    "Premium": "Policy_Amount_Identifier",
    "Claim": "Claim_Identifier",
    "Claim_Coverage": "Claim_Identifier",
    "Claim_Amount": "Claim_Amount_Identifier",
    "Loss_Reserve": "Claim_Amount_Identifier",
    "Expense_Reserve": "Claim_Amount_Identifier",
    "Loss_Payment": "Claim_Amount_Identifier",
    "Expense_Payment": "Claim_Amount_Identifier",
}
assert set(GEN_KEY) == set(ts)
for t, k in GEN_KEY.items():
    (mx,) = con.execute(f'SELECT MAX("{k}") FROM "{t}"').fetchone()
    assert mx is None or mx < ID0, f"official {t}.{k} reaches {mx} >= ID0"

# Profile of the official data, taken before anything is generated:
# which columns are always NULL, and the value sets of the code/name columns.
OFFICIAL_ALL_NULL = {
    (t, c) for t in ts for c in columns(con, t) if not distinct_values(t, c)
}
CODE_COLUMNS = [("Agreement_Party_Role", "Party_Role_Code"), ("Policy_Amount", "Amount_Type_Code"),
                ("Catastrophe", "Catastrophe_Name")]  # fmt: skip
OFFICIAL_CODES = {tc: distinct_values(*tc) for tc in CODE_COLUMNS}
CATASTROPHE_NAMES = sorted(
    OFFICIAL_CODES[("Catastrophe", "Catastrophe_Name")]
)  # sorted: deterministic
PREMIUM_CODE = "Year"  # official: premium rows 'Year', limit rows NULL
assert OFFICIAL_CODES[("Policy_Amount", "Amount_Type_Code")] == {PREMIUM_CODE}
assert OFFICIAL_CODES[("Agreement_Party_Role", "Party_Role_Code")] == {"PH", "AG"}

# IDs of parents outside the 13 tables (Party, Insurable_Object, Occurrence) are only referenced.
party_id, io_id, occ_id = ids(), ids(), ids()


# ---------------------------------------------------------------- 2. generators (parents first)
def gen_catastrophe(n=N_CATASTROPHES):
    """New catastrophe events; names only from the official names. Each event gets a year
    (not stored) so that claims are linked to events in the year of their loss."""
    rows, by_year = [], {}
    for cid in itertools.islice(ids(), n):
        rows.append(
            {
                "Catastrophe_Identifier": cid,
                "Catastrophe_Name": random.choice(CATASTROPHE_NAMES),
            }
        )
        by_year.setdefault(random.randint(2015, CUTOFF.year), []).append(cid)
    insert("Catastrophe", rows)
    return by_year


def gen_persons():
    """Persons exist only as Party_Identifier values (Party/Person are not among the 13 tables)."""
    return {
        "PH": [next(party_id) for _ in range(N_PH)],
        "AG": [next(party_id) for _ in range(N_AG)],
    }


def gen_policy(persons, n=N_POLICIES):
    # Skewed holder weights: a few holders own many policies, some own one or none.
    ph_weight = [random.expovariate(1.0) for _ in persons["PH"]]
    rows, pols = [], []
    for k, pid in enumerate(itertools.islice(ids(), n)):
        eff = date(random.randint(2015, 2025), random.randint(1, 12), 1)
        term = random.choices([1, 2, 3, 5], [60, 20, 10, 10])[0]
        exp = add_years(eff, term) - timedelta(days=1)
        rows.append({
            "Policy_Identifier": pid,
            "Effective_Date": iso(eff),
            "Expiration_Date": iso(exp),
            "Policy_Number": maybe(str(31003100000 + k), 0.05),  # 11 digits like the official numbers
        })  # fmt: skip
        pols.append({
            "id": pid, "eff": eff, "exp": exp, "term": term,
            "PH": random.choices(persons["PH"], ph_weight)[0],
            "AG": random.choice(persons["AG"]),
            "io": next(io_id),  # one insurable object per policy, as in the official data
        })  # fmt: skip
    insert("Policy", rows)
    return pols


def gen_agreement_party_role(pols):
    """One PH and one AG per policy, as official. Policy_Identifier is the Agreement_Identifier."""
    rows = [{"Agreement_Identifier": p["id"], "Party_Identifier": p[role], "Party_Role_Code": role}
            for p in pols for role in ("PH", "AG")]  # fmt: skip
    insert("Agreement_Party_Role", rows)


def gen_policy_coverage_detail(pols):
    """One detail per policy year, as in the official data (policy 1: 2015..2019)."""
    pcd_id, rows = ids(), []
    for p in pols:
        p["segs"] = []
        for y in range(p["term"]):
            seg = {"id": next(pcd_id), "eff": add_years(p["eff"], y),
                   "exp": add_years(p["eff"], y + 1) - timedelta(days=1)}  # fmt: skip
            p["segs"].append(seg)
            rows.append({
                "Effective_Date": iso(seg["eff"]),
                "Policy_Coverage_Detail_Identifier": seg["id"],
                "Insurable_Object_Identifier": p["io"],
                "Policy_Identifier": p["id"],
                "Expiration_Date": maybe(iso(seg["exp"]), 0.1),
            })  # fmt: skip
    insert("Policy_Coverage_Detail", rows)


def gen_policy_amount(pols):
    """Per policy year a limit row (Amount_Type_Code NULL) and a premium row ('Year'), as official."""
    pa_id, rows, premium = ids(), [], []
    for p in pols:
        limit = random.choice([250_000, 500_000, 600_000, 1_000_000, 2_000_000])
        prem = round(limit * random.uniform(0.01, 0.025), -2)
        for seg in p["segs"]:
            common = {"Policy_Identifier": p["id"], "Effective_Date": iso(seg["eff"]),
                      "Policy_Coverage_Detail_Identifier": seg["id"]}  # fmt: skip
            rows.append(
                {
                    **common,
                    "Policy_Amount_Identifier": next(pa_id),
                    "Policy_Amount": limit,
                }
            )
            pid = next(pa_id)
            rows.append({**common, "Policy_Amount_Identifier": pid, "Amount_Type_Code": PREMIUM_CODE,
                         "Policy_Amount": int(prem)})  # fmt: skip
            premium.append({"Policy_Amount_Identifier": pid})
            prem = round(prem * random.uniform(1.0, 1.08), -2)  # renewals get dearer
    insert("Policy_Amount", rows)
    insert("Premium", premium)


def gen_claim(pols, cats_by_year):
    """Claims per policy with loss, open and close dates; each is linked to a coverage detail."""
    claim_id, rows, cover, claims = ids(), [], [], []
    for p in pols:
        k = random.choices(*CLAIMS_PER_POLICY)[0]
        last = min(p["exp"], CUTOFF - timedelta(days=30))
        if last < p["eff"]:
            continue
        for _ in range(k):
            loss = rand_date(p["eff"], last)
            seg = next(s for s in p["segs"] if s["eff"] <= loss <= s["exp"])
            opened = min(loss + timedelta(days=random.randint(0, 20)), CUTOFF)
            closed = None
            if random.random() < 0.75:
                closed = min(opened + timedelta(days=random.randint(5, 240)), CUTOFF)
            cats = cats_by_year.get(loss.year, [])
            cid = next(claim_id)
            rows.append({
                "Claim_Identifier": cid,
                "Catastrophe_Identifier": random.choice(cats) if cats and random.random() < 0.25 else None,
                "Company_Claim_Number": maybe(str(12400000 + cid - ID0), 0.05),  # 8 digits like official
                "Insurable_Object_Identifier": maybe(p["io"], 0.1),
                "Occurrence_Identifier": maybe(next(occ_id), 0.1),
                "Claim_Open_Date": iso(opened),
                "Claim_Close_Date": iso(closed),  # NULL = still open
            })  # fmt: skip
            cover.append({"Claim_Identifier": cid, "Effective_Date": iso(seg["eff"]),
                          "Policy_Coverage_Detail_Identifier": seg["id"]})  # fmt: skip
            claims.append({"id": cid, "closed": closed})
    insert("Claim", rows)
    insert("Claim_Coverage", cover)
    return claims


def gen_claim_amount(claims):
    """All four amount types (the subtype tables). Every claim gets a loss reserve; expense reserve,
    loss and expense payments vary. Only identifier, claim and amount are filled, as official."""
    ca_id, rows = ids(), []
    sub = {
        "Loss_Reserve": [],
        "Expense_Reserve": [],
        "Loss_Payment": [],
        "Expense_Payment": [],
    }

    def add(c, kind, amount):
        aid = next(ca_id)
        rows.append({"Claim_Amount_Identifier": aid, "Claim_Identifier": c["id"],
                     "Claim_Amount": max(100, int(round(amount, -2)))})  # whole numbers, as official  # fmt: skip
        sub[kind].append({"Claim_Amount_Identifier": aid})

    for c in claims:
        loss_res = random.lognormvariate(9.0, 1.0)  # median ~8,100
        add(c, "Loss_Reserve", loss_res)
        exp_res = (
            loss_res * random.uniform(0.1, 0.25) if random.random() < 0.7 else None
        )
        if exp_res:
            add(c, "Expense_Reserve", exp_res)
        n_pay = (
            random.choice([1, 2])
            if c["closed"]
            else (1 if random.random() < 0.4 else 0)
        )
        if n_pay:
            total = loss_res * random.uniform(0.5, 1.1)
            for share in [1.0] if n_pay == 1 else [0.4, 0.6]:
                add(c, "Loss_Payment", total * share)
            if random.random() < 0.7:
                base = exp_res or loss_res * random.uniform(0.05, 0.15)
                add(c, "Expense_Payment", base * random.uniform(0.5, 1.0))
    insert("Claim_Amount", rows)
    for kind, r in sub.items():
        insert(kind, r)


# Generate parents before children so that every FK resolves.
print("Generating rows (seed", SEED, ")")
cats = gen_catastrophe()
persons = gen_persons()
pols = gen_policy(persons)
gen_agreement_party_role(pols)
gen_policy_coverage_detail(pols)
gen_policy_amount(pols)
claims = gen_claim(pols, cats)
gen_claim_amount(claims)
con.commit()


# ---------------------------------------------------------------- 3. checks
def check_fks():
    """One LEFT JOIN ... WHERE parent IS NULL per FK between existing tables."""
    with open(
        ROOT / "context/reference_relationships.csv", encoding="utf-8", newline=""
    ) as f:
        refs = [r for r in csv.DictReader(f) if r["table_exists"] == "1"]
    # Subtype tables point to Claim_Payment/Claim_Reserve (not in DB); their real parent is Claim_Amount.
    refs += [{"from_table": t, "from_columns": "Claim_Amount_Identifier", "to_table": "Claim_Amount",
              "to_columns": "Claim_Amount_Identifier"}
             for t in ("Loss_Reserve", "Expense_Reserve", "Loss_Payment", "Expense_Payment")]  # fmt: skip
    refs.append({"from_table": "Agreement_Party_Role", "from_columns": "Agreement_Identifier",
                 "to_table": "Policy", "to_columns": "Policy_Identifier"})  # fmt: skip
    bad = 0
    for r in refs:
        fc, tc = r["from_columns"].split(","), r["to_columns"].split(",")
        on = " AND ".join(f'c."{a}" = p."{b}"' for a, b in zip(fc, tc))
        notnull = " AND ".join(f'c."{a}" IS NOT NULL' for a in fc)
        sql = (f'SELECT COUNT(*) FROM "{r["from_table"]}" c LEFT JOIN "{r["to_table"]}" p ON {on} '
               f'WHERE {notnull} AND p."{tc[0]}" IS NULL')  # fmt: skip
        (n,) = con.execute(sql).fetchone()
        print(f"  {'OK ' if n == 0 else 'BAD'} {r['from_table']}({r['from_columns']}) -> "
              f"{r['to_table']}({r['to_columns']}): {n} orphans")  # fmt: skip
        bad += n
    return bad


def check_types():
    """Storage class per column must fit the declared DDL type; dates must be 'YYYY-MM-DD'."""
    allowed = {"int": {"integer"}, "bigint": {"integer"}, "decimal": {"integer", "real"},
               "datetime": {"text"}, "varchar": {"text"}, "char": {"text"}}  # fmt: skip
    bad = 0
    for t in ts:
        for _, col, decl, *_ in con.execute(f'PRAGMA table_info("{t}")'):
            base = decl.split("(")[0].lower()
            got = {
                s for (s,) in con.execute(f'SELECT DISTINCT typeof("{col}") FROM "{t}"')
            } - {"null"}
            if not got <= allowed[base]:
                print(f"  BAD type {t}.{col} ({decl}): {got}")
                bad += 1
            if base == "datetime":
                for v in distinct_values(t, col):
                    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                        print(f"  BAD date {t}.{col}: {v!r}")
                        bad += 1
    return bad


def check_no_invented_values():
    """Columns that are NULL throughout the official DB stay NULL; code/name columns only use official values."""
    bad = 0
    for t, c in sorted(OFFICIAL_ALL_NULL):
        (n,) = con.execute(
            f'SELECT COUNT(*) FROM "{t}" WHERE "{c}" IS NOT NULL'
        ).fetchone()
        if n:
            print(f"  BAD {t}.{c}: {n} values, official column is all NULL")
            bad += n
    for (t, c), official in OFFICIAL_CODES.items():
        extra = distinct_values(t, c) - official
        if extra:
            print(f"  BAD {t}.{c}: values not in official DB: {sorted(extra)}")
            bad += len(extra)
    print(
        f"  {len(OFFICIAL_ALL_NULL)} all-NULL columns and {len(OFFICIAL_CODES)} code columns checked"
    )
    return bad


print("FK check:")
problems = check_fks()
print("Type check:")
problems += check_types()
print("No invented values:")
problems += check_no_invented_values()
con.close()
assert problems == 0, f"{problems} problems"
print("All checks passed:", DBS["extended"])
