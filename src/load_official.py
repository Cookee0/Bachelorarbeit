# Reads the official DDL and CSVs and writes them to a SQLite database.
# This is the database for the benchmark.

import csv, pathlib, re, sqlite3

BENCH = pathlib.Path("G:/Programmieren/__Projekte/Bachelorarbeit/benchmark/Bachelorarbeit")
CSV_DIR = BENCH / "data"
DDL = (BENCH / "DDL/ACME_small.ddl").read_text(encoding="utf-8")
DB_PATH = pathlib.Path("G:/Programmieren/__Projekte/Bachelorarbeit/data/official.sqlite")

# The DDL is T-SQL style and has no ';' between statements, which SQLite requires.
# Everything else (ASC in PRIMARY KEY, foreign keys to tables outside this extract) SQLite accepts as is.
DDL = re.sub(r"\)\s*(?=CREATE\s+TABLE)", ");\n", DDL, flags=re.I).strip() + ";"
# The official sample data violates the DDL's NOT NULL constraints (e.g. empty Coverage_Identifier in
# Policy_Coverage_Detail.csv), so those are relaxed on load; primary keys and declared types are kept.
DDL = re.sub(r"\bNOT\s+NULL\b", "NULL", DDL, flags=re.I)

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DB_PATH.unlink(missing_ok=True)  # always rebuild from scratch
con = sqlite3.connect(DB_PATH)
con.executescript(DDL)

# Table names come straight from the database the DDL just created
tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")]
print(len(tables), "tables in DDL:", tables)

for t in tables:
    path = CSV_DIR / f"{t}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No CSV for table {t}: {path}")
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        db_cols = [r[1] for r in con.execute(f'PRAGMA table_info("{t}")')]
        unknown = [c for c in header if c not in db_cols]
        if unknown:
            raise ValueError(f"CSV columns not in table {t}: {unknown}")
        sql = f'INSERT INTO "{t}" ({", ".join(chr(34) + c + chr(34) for c in header)}) VALUES ({", ".join("?" * len(header))})'
        # empty CSV fields are NULL, not empty strings
        con.executemany(sql, ([v if v != "" else None for v in row] for row in reader))
    con.commit()
    print(t, con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0], "rows")
con.close()
