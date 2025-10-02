import sqlite3
from contextlib import contextmanager
from .schemas import RAW_DDL, LOC_DDL, DW_DDL

@contextmanager
def connect(db_path: str, readonly: bool = False):
    uri = f"file:{db_path}?mode=ro" if readonly else db_path
    conn = sqlite3.connect(uri, uri=readonly)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_raw(db_path: str):
    with connect(db_path) as conn:
        conn.execute(RAW_DDL)

def init_loc(db_path: str):
    with connect(db_path) as conn:
        conn.execute(LOC_DDL)

def init_dw(db_path: str):
    with connect(db_path) as conn:
        for stmt in DW_DDL.strip().split(';'):
            if stmt.strip():
                conn.execute(stmt + ';')