import csv, sqlite3
from db import ROOT, DBS, tables, columns

BENCH = ROOT / "benchmark/Bachelorarbeit"
CSV_DIR = BENCH / "data"
DDL = (BENCH / "DDL/ACME_small.ddl").read_text(encoding="utf-8")

# The DDL is T-SQL style. It contains no ';' between statements. This is required by SQLite.
# Split on "CREATE TABLE" and terminate each statement with ';'.
DDL = ";\n".join("CREATE TABLE " + s.strip() for s in DDL.split("CREATE TABLE") if s.strip()) + ";"

# The official sample data violates the NOT NULL constraints (e.g. empty Coverage_Identifier in
# Policy_Coverage_Detail.csv), so they are relaxed on load; primary keys and declared types are kept.
DDL = DDL.replace("NOT NULL", "NULL")

db = DBS["official"]
db.unlink(missing_ok=True)  # always rebuild from scratch
con = sqlite3.connect(db)
con.executescript(DDL)
ts = tables(con)
print(len(ts), "tables:", ts)
assert len(ts) == 13, "expected the 13 tables of ACME_small.ddl"

for t in ts:
    cols = columns(con, t)
    path = CSV_DIR / f"{t}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No CSV for table {t}: {path}")
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = {h.strip().lower(): h for h in reader.fieldnames}  # CSV header case may differ
        missing = [c for c in cols if c.lower() not in header]
        if missing:
            raise ValueError(f"{t}: CSV lacks columns {missing}")
        extra = set(header) - {c.lower() for c in cols}
        if extra:
            print(f"  {t}: CSV columns not in DDL, ignored: {sorted(extra)}")
        rows = [[r[header[c.lower()]] if r[header[c.lower()]] != "" else None for c in cols]   # '' -> NULL
                for r in reader]
    col_list = ", ".join(f'"{c}"' for c in cols)
    marks = ", ".join("?" for _ in cols)
    con.executemany(f'INSERT INTO "{t}" ({col_list}) VALUES ({marks})', rows)
    print(t, len(rows), "rows")

con.commit()
con.close()