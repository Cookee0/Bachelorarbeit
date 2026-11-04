# Initializes the DB connections and provides functions for querying the DB.
import pathlib, sqlite3

ROOT = pathlib.Path("G:/Programmieren/__Projekte/Bachelorarbeit")
DBS = {"official": ROOT / "data/official.sqlite",
       "extended": ROOT / "data/extended.sqlite"}

def connect_readonly(path):
    """Read-only connection. No query may change the DB."""
    return sqlite3.connect(pathlib.Path(path).as_uri() + "?mode=ro", uri=True)

def tables(con):
    return [t for (t,) in con.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]

def columns(con, table):
    return [row[1] for row in con.execute(f'PRAGMA table_info("{table}")')]