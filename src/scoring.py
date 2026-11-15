# Execution-based scoring: runs SQL and compares result sets.
import datetime as dt, time
from collections import Counter
from decimal import Decimal
from db import DBS, connect_readonly

def run_sql(db_path, sql, timeout_s=30):
    # Run read-only and abort the query after timeout_s seconds.
    con = connect_readonly(db_path)
    deadline = time.monotonic() + timeout_s
    con.set_progress_handler(lambda: time.monotonic() > deadline, 10_000)   # True aborts the query
    try:
        return con.execute(sql).fetchall()
    finally:
        con.close()

def _norm(v):
    # Normalize one cell to a comparable (type, text) pair.
    if v is None:
        return ("null", "")
    if isinstance(v, bool):
        return ("b", str(v))
    if isinstance(v, (int, float, Decimal)):
        return ("n", f"{round(float(v), 4):.4f}")
    if isinstance(v, (dt.date, dt.datetime)):
        return ("s", v.isoformat())
    if isinstance(v, bytes):
        return ("s", v.hex())
    return ("s", str(v).strip())

def result_key(rows):
    """Multiset of rows; ignores row order, column order and column names."""
    return Counter(tuple(sorted(_norm(v) for v in row)) for row in rows)

def same_result(rows_a, rows_b):
    return result_key(rows_a) == result_key(rows_b)