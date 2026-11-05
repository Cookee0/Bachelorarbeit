# Writes inputs.txt from schema and sample data of the official DB.

import pandas as pd

from db import BENCH, DBS, ROOT, columns, connect_readonly, tables

out = ["## Schema (DDL)\n" + (BENCH / "DDL/ACME_small.ddl").read_text(encoding="utf-8")]

con = connect_readonly(DBS["official"])
out.append("## Sample data")
for t in tables(con):
    sample = pd.read_sql_query(f'SELECT * FROM "{t}" LIMIT 3', con)
    out.append(f"### {t}\n{sample.to_string(index=False)}")
    for col in columns(con, t):
        n = con.execute(f'SELECT count(DISTINCT "{col}") FROM "{t}"').fetchone()[0]
        if n <= 20:
            vals = [
                v
                for (v,) in con.execute(
                    f'SELECT DISTINCT "{col}" FROM "{t}" ORDER BY 1'
                )
            ]
            out.append(f"{t}.{col} distinct values: {vals}")
con.close()

(ROOT / "context/inputs.txt").write_text("\n\n".join(out), encoding="utf-8")
