from pathlib import Path

from build_player_rankings import main as build_rankings_main
from load_player_data import load_player_data


def main() -> None:
    required = [
        Path("data/raw/uefa_player_leaderboards.csv"),
        Path("data/raw/goalkeeper_clean_sheets.csv"),
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing local source snapshot(s): {missing}")

    print("Using local source snapshots (no live web scraping).")
    build_rankings_main()
    rankings = Path("data/processed/player_rankings.csv")
    db = Path("data/processed/champions_league.db")
    load_player_data(rankings, db)
    print("\nPlayer-analysis upgrade complete.")
    print("  network requests: 0")
    print(f"  rankings: {rankings}")
    print("  report: reports/player_rankings.md")


if __name__ == "__main__":
    main()
