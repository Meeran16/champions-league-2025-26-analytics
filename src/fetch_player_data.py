"""Offline player source loader.

This module intentionally performs no network requests. The original live-scraping
implementation was removed because third-party sites returned 403 responses and
read timeouts. Source snapshots live in data/raw/ and are versioned for reproducibility.
"""
from pathlib import Path
import pandas as pd

LEADERBOARDS = Path("data/raw/uefa_player_leaderboards.csv")
CLEAN_SHEETS = Path("data/raw/goalkeeper_clean_sheets.csv")


def fetch_all(delay_seconds: float = 0.0) -> dict[str, pd.DataFrame]:
    del delay_seconds
    if not LEADERBOARDS.exists() or not CLEAN_SHEETS.exists():
        raise FileNotFoundError(
            "Local player source snapshots are missing. Expected: "
            f"{LEADERBOARDS} and {CLEAN_SHEETS}"
        )
    print("Loading local player source snapshots (no network requests).")
    return {
        "leaderboards": pd.read_csv(LEADERBOARDS),
        "clean_sheets": pd.read_csv(CLEAN_SHEETS),
    }


def clean_player_data(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
    # Backward-compatible helper for notebooks/scripts that import this name.
    leaderboards = raw["leaderboards"].copy()
    return leaderboards


if __name__ == "__main__":
    raw = fetch_all()
    print(f"UEFA leaderboard rows: {len(raw['leaderboards'])}")
    print(f"Goalkeeper clean-sheet rows: {len(raw['clean_sheets'])}")
