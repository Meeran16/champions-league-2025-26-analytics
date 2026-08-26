from __future__ import annotations

import sqlite3
from pathlib import Path


def scalar(conn, query):
    return conn.execute(query).fetchone()[0]


def main() -> None:
    db = Path("data/processed/champions_league.db")
    if not db.exists():
        raise SystemExit("Database not found. Run the build steps first.")

    with sqlite3.connect(db) as conn:
        checks = {
            "teams": scalar(conn, "SELECT COUNT(*) FROM teams"),
            "matches": scalar(conn, "SELECT COUNT(*) FROM matches"),
            "league_phase_matches": scalar(conn, "SELECT COUNT(*) FROM matches WHERE stage='League Phase'"),
            "league_phase_stats": scalar(conn, "SELECT COUNT(*) FROM league_phase_stats"),
            "penalty_shootouts": scalar(conn, "SELECT COUNT(*) FROM matches WHERE penalty_shootout=1"),
        }

        assert checks["teams"] == 36
        assert checks["matches"] == 189
        assert checks["league_phase_matches"] == 144
        assert checks["league_phase_stats"] == 144
        assert checks["penalty_shootouts"] == 1

        unmatched = scalar(
            conn,
            """
            SELECT COUNT(*)
            FROM league_phase_stats s
            LEFT JOIN matches m ON s.match_id = m.match_id
            WHERE m.match_id IS NULL
            """,
        )
        assert unmatched == 0

    print("Validation passed:")
    for key, value in checks.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
