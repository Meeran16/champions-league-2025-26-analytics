from pathlib import Path

from build_database import build_database
from clean_league_stats import clean_stats
from parse_full_results import parse_results


def main() -> None:
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    matches = parse_results(raw_dir / "cl.txt")
    matches.insert(0, "match_id", range(1, len(matches) + 1))
    matches_path = processed_dir / "matches.csv"
    matches.to_csv(matches_path, index=False)

    stats = clean_stats(raw_dir / "champions_league_matches.csv", matches_path)
    stats_path = processed_dir / "league_phase_stats.csv"
    stats.to_csv(stats_path, index=False)

    build_database(matches_path, stats_path, processed_dir / "champions_league.db")

    print("Pipeline complete.")
    print(f"  Full competition matches: {len(matches)}")
    print(f"  Detailed league-phase matches: {len(stats)}")


if __name__ == "__main__":
    main()
