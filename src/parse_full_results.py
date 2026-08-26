from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from team_mapping import OPENFOOTBALL_TEAM_MAP

DATE_RE = re.compile(
    r"^\s{2}(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$"
)
STAGE_RE = re.compile(r"^▪\s+(.+)$")
MATCH_RE = re.compile(r"^\s{4}(?:(\d{2}:\d{2})\s+)?(.+?)\s+v\s+(.+?)\s{2,}(.+?)\s*$")


def normalize_stage(heading: str) -> tuple[str, int | None]:
    if heading.startswith("League, Matchday"):
        return "League Phase", int(re.search(r"(\d+)$", heading).group(1))
    if heading.startswith("Playoffs, Matchday"):
        return "Knockout Play-offs", int(re.search(r"(\d+)$", heading).group(1))
    mapping = {
        "Finals, Round of 16": "Round of 16",
        "Finals, Quarterfinals": "Quarter-finals",
        "Finals, Semifinals": "Semi-finals",
        "Finals, Final": "Final",
    }
    return mapping.get(heading, heading), None


def parse_score(score_text: str) -> dict:
    extra_time = "a.e.t." in score_text
    penalty_shootout = "pen." in score_text
    penalty_home = penalty_away = None

    if penalty_shootout:
        match = re.match(
            r"(\d+)-(\d+)\s+pen\.\s+(\d+)-(\d+)\s+a\.e\.t\.", score_text
        )
        if not match:
            raise ValueError(f"Unrecognized penalty score: {score_text}")
        penalty_home, penalty_away, home_goals, away_goals = map(int, match.groups())
    else:
        match = re.match(r"(\d+)-(\d+)", score_text)
        if not match:
            raise ValueError(f"Unrecognized score: {score_text}")
        home_goals, away_goals = map(int, match.groups())

    parenthetical = re.search(r"\((.*?)\)", score_text)
    score_pairs = re.findall(r"(\d+)-(\d+)", parenthetical.group(1)) if parenthetical else []

    if len(score_pairs) == 1:
        half_time_home, half_time_away = map(int, score_pairs[0])
        regulation_home, regulation_away = home_goals, away_goals
    elif len(score_pairs) >= 2:
        regulation_home, regulation_away = map(int, score_pairs[0])
        half_time_home, half_time_away = map(int, score_pairs[-1])
    else:
        half_time_home = half_time_away = None
        regulation_home, regulation_away = home_goals, away_goals

    if home_goals > away_goals:
        match_outcome = "H"
    elif home_goals < away_goals:
        match_outcome = "A"
    else:
        match_outcome = "D"

    return {
        "home_goals": home_goals,
        "away_goals": away_goals,
        "regulation_home_goals": regulation_home,
        "regulation_away_goals": regulation_away,
        "half_time_home_goals": half_time_home,
        "half_time_away_goals": half_time_away,
        "extra_time": int(extra_time),
        "penalty_shootout": int(penalty_shootout),
        "penalty_home": penalty_home,
        "penalty_away": penalty_away,
        "match_outcome": match_outcome,
    }


def parse_results(source: Path) -> pd.DataFrame:
    lines = source.read_text(encoding="utf-8").splitlines()

    current_stage = None
    current_matchday = None
    current_date = None
    current_year = 2025
    current_time = None
    records: list[dict] = []

    for line in lines:
        stage_match = STAGE_RE.match(line)
        if stage_match:
            current_stage, current_matchday = normalize_stage(stage_match.group(1))
            current_time = None
            continue

        date_match = DATE_RE.match(line)
        if date_match:
            _, month, day, explicit_year = date_match.groups()
            if explicit_year:
                current_year = int(explicit_year)
            current_date = datetime.strptime(
                f"{current_year} {month} {day}", "%Y %b %d"
            ).date()
            current_time = None
            continue

        match = MATCH_RE.match(line)
        if not match or current_date is None:
            continue

        kickoff_time, home_raw, away_raw, score_text = match.groups()
        home_raw = home_raw.strip()
        away_raw = away_raw.strip()
        score_text = score_text.strip()

        if kickoff_time:
            current_time = kickoff_time

        if home_raw not in OPENFOOTBALL_TEAM_MAP or away_raw not in OPENFOOTBALL_TEAM_MAP:
            raise KeyError(f"Missing team mapping: {home_raw!r} or {away_raw!r}")

        home_team = OPENFOOTBALL_TEAM_MAP[home_raw][0]
        away_team = OPENFOOTBALL_TEAM_MAP[away_raw][0]
        score = parse_score(score_text)

        if score["home_goals"] > score["away_goals"]:
            winner = home_team
        elif score["home_goals"] < score["away_goals"]:
            winner = away_team
        elif score["penalty_shootout"]:
            winner = home_team if score["penalty_home"] > score["penalty_away"] else away_team
        else:
            winner = "Draw"

        records.append(
            {
                "date": current_date.isoformat(),
                "kickoff_time": current_time,
                "stage": current_stage,
                "matchday": current_matchday,
                "home_team": home_team,
                "away_team": away_team,
                **score,
                "winner": winner,
                "source_score": score_text,
            }
        )

    matches = pd.DataFrame(records)
    if len(matches) != 189:
        raise ValueError(f"Expected 189 matches, parsed {len(matches)}")

    return matches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/cl.txt"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/matches.csv"))
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    matches = parse_results(args.input)
    matches.insert(0, "match_id", range(1, len(matches) + 1))
    matches.to_csv(args.output, index=False)
    print(f"Parsed {len(matches)} matches -> {args.output}")


if __name__ == "__main__":
    main()
