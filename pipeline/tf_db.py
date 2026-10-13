"""Load teamfight data into an in-memory DuckDB database and run the SQL in pipeline/sql/.

As a library:
    con = build(mi, teamfights)      # parsed MATCH INFO rows + read_teamfights() output
    problems = run_checks(con)       # rows returned by sql/checks_teamfights.sql

From the command line (the workbook must have been saved by Excel):
    python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx                      # run checks
    python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx "SELECT * FROM comp_stats ORDER BY freq DESC LIMIT 5"
    python3 pipeline/tf_db.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx --save teamfights.duckdb   # file for the duckdb CLI
"""
import os
import re
import sys

import duckdb
import openpyxl

sys.path.insert(0, os.path.dirname(__file__))
from export_site_data import HERO_ROLES, read_teamfights, rows  # noqa: E402

SQL_DIR = os.path.join(os.path.dirname(__file__), "sql")
ROLE_RANK = {"T": 1, "D": 2, "S": 3}


def build(mi, teamfights, path=":memory:"):
    con = duckdb.connect(path)
    con.execute("""
        CREATE OR REPLACE TABLE hero_roles (hero VARCHAR PRIMARY KEY, role VARCHAR, role_rank INTEGER);
        CREATE OR REPLACE TABLE match_info (match_id VARCHAR PRIMARY KEY, week INTEGER, day INTEGER, match_no INTEGER,
            set_no INTEGER, team1 VARCHAR, team2 VARCHAR, map VARCHAR, map_type VARCHAR, map_winner VARCHAR);
        CREATE OR REPLACE TABLE teamfights (tf_id INTEGER PRIMARY KEY, match_id VARCHAR, ord INTEGER,
            team1 VARCHAR, team2 VARCHAR, winner VARCHAR);
        CREATE OR REPLACE TABLE tf_hero (tf_id INTEGER, side INTEGER, hero VARCHAR);
    """)
    con.executemany("INSERT INTO hero_roles VALUES (?, ?, ?)",
                    [(h, r, ROLE_RANK[r]) for h, r in HERO_ROLES.items()])
    con.executemany("INSERT INTO match_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [(m["MATCH_ID"], m["WEEK"], m["DAY"], m["MATCH"], m["Set #"], m["TEAM 1"], m["TEAM 2"],
                      m["MAP"], m["MAP TYPE"], m["WINNER"]) for m in mi.values()])
    con.executemany("INSERT INTO teamfights VALUES (?, ?, ?, ?, ?, ?)",
                    [(i, t["MATCH_ID"], t["Order"], t["TEAM 1"], t["TEAM 2"], t["WINNER"])
                     for i, t in enumerate(teamfights, 1)])
    con.executemany("INSERT INTO tf_hero VALUES (?, ?, ?)",
                    [(i, side, h) for i, t in enumerate(teamfights, 1)
                     for side, key in ((1, "TEAM 1 COMP"), (2, "TEAM 2 COMP")) for h in t[key] if h])
    with open(os.path.join(SQL_DIR, "teamfights.sql"), encoding="utf-8") as f:
        con.execute(f.read())
    return con


def run_checks(con):
    """Run every check in sql/checks_teamfights.sql; return one message per offending row."""
    with open(os.path.join(SQL_DIR, "checks_teamfights.sql"), encoding="utf-8") as f:
        blocks = re.split(r"^-- check:", f.read(), flags=re.M)[1:]
    problems = []
    for block in blocks:
        name, query = block.split("\n", 1)
        cur = con.execute(query)
        cols = [d[0] for d in cur.description]
        problems += [f"{name.strip()}: " + ", ".join(f"{c}={v}" for c, v in zip(cols, r)) for r in cur.fetchall()]
    return problems


def load(path, db_path=":memory:"):
    """Parse a workbook (Excel-saved) and return (con, problems)."""
    wb = openpyxl.load_workbook(path, data_only=True)
    mi = {r["MATCH_ID"]: r for r in rows(wb["MATCH INFO"]) if r["MAP"] and r["MATCH_ID"]}
    teamfights, problems = read_teamfights(wb, mi)
    con = build(mi, teamfights, db_path)
    return con, problems + run_checks(con)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    db_path = argv[argv.index("--save") + 1] if "--save" in argv else ":memory:"
    if db_path != ":memory:" and os.path.exists(db_path):
        os.remove(db_path)
    con, problems = load(argv[0], db_path)
    query = next((a for a in argv[1:] if a != "--save" and a != db_path), None)
    if query:
        print(con.sql(query))
    print("checks: OK" if not problems else "PROBLEMS:\n  " + "\n  ".join(problems))
    if db_path != ":memory:":
        print(f"saved {db_path}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
