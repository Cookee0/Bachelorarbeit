# Runs SQL queries against one of the DBs (read-only).
# Usage:
#   python query.py "SELECT ..."              -> one query against extended
#   python query.py --db official "SELECT ..." -> one query against official
#   python query.py                            -> interactive mode, multi-line queries end with ";"
#                                                 or an empty line (empty line or "exit" quits)

import argparse
import sqlite3

import pandas as pd

from db import DBS, connect_readonly

pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


def run(con, sql):
    # Execute one query and print the result table.
    try:
        df = pd.read_sql_query(sql, con)
        print(df.to_string(index=False))
        print(f"({len(df)} rows)")
    except pd.errors.DatabaseError as e:
        print(f"Error: {e}")


parser = argparse.ArgumentParser()
parser.add_argument("--db", choices=DBS, default="extended")
parser.add_argument("sql", nargs="?")
args = parser.parse_args()

con = connect_readonly(DBS[args.db])
if args.sql:
    run(con, args.sql)
else:
    # Multi-line input: lines are collected until the statement ends with ";"
    # or an empty line follows. Empty line / "exit" on an empty prompt quits.
    print(
        f"Connected to {args.db} (read-only). End a query with ';' or an empty line. "
        "Empty line or 'exit' at 'sql>' quits."
    )
    buffer = []
    while True:
        line = input("sql> " if not buffer else "...> ")
        if not buffer and line.strip() in ("", "exit"):
            break
        if line.strip():
            buffer.append(line)
        sql = "\n".join(buffer)
        if not line.strip() or sqlite3.complete_statement(sql):
            run(con, sql)
            buffer = []
con.close()
