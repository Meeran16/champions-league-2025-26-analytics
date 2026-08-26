from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

from team_mapping import COUNTRY_BY_TEAM


def build_database(matches_path: Path, stats_path: Path, db_path: Path) -> None:
    matches = pd.read_csv(matches_path)
    stats = pd.read_csv(stats_path)

    teams = pd.DataFrame(
        [
            {"team_id": idx + 1, "team_name": team, "country_code": COUNTRY_BY_TEAM[team]}
            for idx, team in enumerate(sorted(COUNTRY_BY_TEAM))
        ]
    )
    team_ids = dict(zip(teams["team_name"], teams["team_id"]))

    match_db = matches.copy()
    match_db["home_team_id"] = match_db["home_team"].map(team_ids)
    match_db["away_team_id"] = match_db["away_team"].map(team_ids)
    match_db = match_db.drop(columns=["home_team", "away_team"])

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as conn:
        schema = Path("sql/01_schema.sql").read_text(encoding="utf-8")
        conn.executescript(schema)
        teams.to_sql("teams", conn, if_exists="append", index=False)
        match_db.to_sql("matches", conn, if_exists="append", index=False)
        stats.to_sql("league_phase_stats", conn, if_exists="append", index=False)

        conn.execute("CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_matches_stage ON matches(stage)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_matches_home_team ON matches(home_team_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_matches_away_team ON matches(away_team_id)")
        conn.commit()

    print(f"Built SQLite database -> {db_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", type=Path, default=Path("data/processed/matches.csv"))
    parser.add_argument("--stats", type=Path, default=Path("data/processed/league_phase_stats.csv"))
    parser.add_argument("--database", type=Path, default=Path("data/processed/champions_league.db"))
    args = parser.parse_args()
    build_database(args.matches, args.stats, args.database)


if __name__ == "__main__":
    main()
