from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd


def percent_to_number(value):
    if pd.isna(value):
        return np.nan
    return float(str(value).strip().replace("%", ""))


def split_of(value):
    if pd.isna(value):
        return np.nan, np.nan
    match = re.match(r"\s*(\d+)\s+of\s+(\d+)\s*", str(value))
    if not match:
        raise ValueError(f"Unexpected 'x of y' value: {value}")
    return int(match.group(1)), int(match.group(2))


def parse_score(value):
    match = re.match(r"\s*(\d+)\s*[–-]\s*(\d+)\s*", str(value))
    if not match:
        raise ValueError(f"Unexpected score: {value}")
    return int(match.group(1)), int(match.group(2))


def clean_stats(source: Path, matches_path: Path) -> pd.DataFrame:
    raw = pd.read_csv(source)
    raw = raw.dropna(subset=["date", "home_team", "away_team", "score"]).copy()

    if len(raw) != 144:
        raise ValueError(f"Expected 144 detailed league-phase matches, found {len(raw)}")

    for column in ["home_possession", "away_possession"]:
        raw[column] = raw[column].map(percent_to_number)

    for side in ["home", "away"]:
        parsed_shots = raw[f"{side}_shots_on_target"].map(split_of)
        raw[f"{side}_shots_on_target_count"] = [x[0] for x in parsed_shots]
        raw[f"{side}_shots_total"] = [x[1] for x in parsed_shots]

        parsed_saves = raw[f"{side}_saves"].map(split_of)
        raw[f"{side}_saves_count"] = [x[0] for x in parsed_saves]
        raw[f"{side}_shots_on_target_faced"] = [x[1] for x in parsed_saves]

    scores = raw["score"].map(parse_score)
    raw["detail_home_goals"] = [x[0] for x in scores]
    raw["detail_away_goals"] = [x[1] for x in scores]

    matches = pd.read_csv(matches_path)
    league_matches = matches.loc[
        matches["stage"].eq("League Phase"),
        ["match_id", "date", "home_team", "away_team", "home_goals", "away_goals"],
    ].copy()

    merged = league_matches.merge(
        raw,
        on=["date", "home_team", "away_team"],
        how="left",
        validate="one_to_one",
        indicator=True,
    )

    if not merged["_merge"].eq("both").all():
        missing = merged.loc[merged["_merge"].ne("both"), ["date", "home_team", "away_team"]]
        raise ValueError(f"Unmatched detailed rows:\n{missing}")

    if not (
        merged["home_goals"].eq(merged["detail_home_goals"])
        & merged["away_goals"].eq(merged["detail_away_goals"])
    ).all():
        raise ValueError("Score mismatch between the two sources")

    if not merged["home_shots_on_target_faced"].eq(merged["away_shots_on_target_count"]).all():
        raise ValueError("Home saves denominator does not match away shots on target")
    if not merged["away_shots_on_target_faced"].eq(merged["home_shots_on_target_count"]).all():
        raise ValueError("Away saves denominator does not match home shots on target")

    keep = [
        "match_id", "venue", "referee", "home_possession", "away_possession",
        "home_shots_total", "away_shots_total",
        "home_shots_on_target_count", "away_shots_on_target_count",
        "home_saves_count", "away_saves_count",
        "home_shots_on_target_pct", "away_shots_on_target_pct",
        "home_saves_pct", "away_saves_pct",
    ]
    return merged[keep].copy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/champions_league_matches.csv"))
    parser.add_argument("--matches", type=Path, default=Path("data/processed/matches.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/league_phase_stats.csv"))
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cleaned = clean_stats(args.input, args.matches)
    cleaned.to_csv(args.output, index=False)
    print(f"Cleaned {len(cleaned)} detailed matches -> {args.output}")


if __name__ == "__main__":
    main()
