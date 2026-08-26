from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd


def load_player_data(rankings_path: Path, db_path: Path) -> None:
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}. Run 'python src/run_pipeline.py' first.")
    rankings = pd.read_csv(rankings_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS player_rankings")
        rankings.to_sql("player_rankings", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_player_rankings_position_rank ON player_rankings(position_group, rank)")
        conn.commit()
    print(f"Loaded player rankings into -> {db_path}")
