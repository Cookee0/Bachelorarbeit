# Runs SQL queries against one of the DBs (read-only).
# Usage:
#   python query.py "SELECT ..."              -> one query against extended
#   python query.py --db official "SELECT ..." -> one query against official
#   python query.py                            -> interactive mode (empty line or "exit" quits)

import argparse

import pandas as pd

from db import DBS, connect_readonly

pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


def run(con, sql):
    try:
        df = pd.read_sql_query(sql, con)
        print(df.to_string(index=False))
        print(f"({len(df)} rows)")
    except Exception as e:
        print(f"Error: {e}")


parser = argparse.ArgumentParser()
parser.add_argument("--db", choices=DBS, default="extended")
parser.add_argument("sql", nargs="?")
args = parser.parse_args()

con = connect_readonly(DBS[args.db])
if args.sql:
    run(con, args.sql)
else:
    print(f"Connected to {args.db} (read-only). Empty line or 'exit' quits.")
    while (sql := input("sql> ").strip()) not in ("", "exit"):
        run(con, sql)
con.close()
