from __future__ import annotations

from pathlib import Path
import pandas as pd

RANK_POINTS = {1: 100.0, 2: 80.0, 3: 65.0, 4: 50.0, 5: 35.0, 6: 20.0}

WEIGHTS = {
    "Forward": {"Goals": 0.45, "Assists": 0.20, "ShotsOnTarget": 0.35},
    "Midfielder": {"Assists": 0.25, "ShotsOnTarget": 0.10, "Tackles": 0.35, "Recoveries": 0.30},
    "Defender": {"Recoveries": 0.50, "Tackles": 0.25, "Assists": 0.25},
}


def _leaderboard_matrix(leaderboards: pd.DataFrame) -> pd.DataFrame:
    df = leaderboards.copy()
    df["leaderboard_points"] = df["rank"].map(RANK_POINTS).fillna(0.0)
    base = (
        df[["player", "squad", "position_group"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    for category in sorted(df["category"].unique()):
        values = (
            df[df["category"] == category]
            .set_index(["player", "squad", "position_group"])["leaderboard_points"]
        )
        raw = (
            df[df["category"] == category]
            .set_index(["player", "squad", "position_group"])["value"]
        )
        key = pd.MultiIndex.from_frame(base[["player", "squad", "position_group"]])
        base[f"points_{category}"] = values.reindex(key).fillna(0).to_numpy()
        base[f"value_{category}"] = raw.reindex(key).fillna(0).to_numpy()
    return base


def score_outfield(leaderboards: pd.DataFrame) -> pd.DataFrame:
    matrix = _leaderboard_matrix(leaderboards)
    frames = []
    for position, weights in WEIGHTS.items():
        group = matrix[matrix["position_group"] == position].copy()
        if group.empty:
            continue
        score = pd.Series(0.0, index=group.index)
        for category, weight in weights.items():
            col = f"points_{category}"
            if col not in group:
                group[col] = 0.0
            score += group[col].fillna(0) * weight
        group["performance_score"] = score.round(2)
        group = group[group["performance_score"] > 0].copy()
        group["rank"] = group["performance_score"].rank(method="first", ascending=False).astype(int)
        frames.append(group)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def score_goalkeepers(leaderboards: pd.DataFrame, clean_sheets: pd.DataFrame) -> pd.DataFrame:
    save = leaderboards[leaderboards["category"] == "Saves"].copy()
    save["save_points"] = save["rank"].map(RANK_POINTS).fillna(0.0)
    keepers = clean_sheets.copy()
    keepers = keepers[keepers["matches_played"] >= 6].copy()
    keepers = keepers.merge(
        save[["player", "squad", "value", "save_points"]].rename(columns={"value": "saves"}),
        on=["player", "squad"], how="outer"
    )
    keepers["position_group"] = "Goalkeeper"
    for col in ["clean_sheets", "matches_played", "clean_sheet_pct", "saves", "save_points"]:
        keepers[col] = pd.to_numeric(keepers[col], errors="coerce").fillna(0)
    # Clean-sheet signal rewards both volume and rate. Percentile ranks are within
    # the goalkeeper population with at least six matches.
    keepers["cs_count_points"] = keepers["clean_sheets"].rank(pct=True, method="average") * 100
    keepers["cs_rate_points"] = keepers["clean_sheet_pct"].rank(pct=True, method="average") * 100
    keepers["clean_sheet_signal"] = 0.55 * keepers["cs_count_points"] + 0.45 * keepers["cs_rate_points"]
    keepers["performance_score"] = (0.60 * keepers["save_points"] + 0.40 * keepers["clean_sheet_signal"]).round(2)
    keepers = keepers[keepers["performance_score"] > 0].copy()
    keepers["rank"] = keepers["performance_score"].rank(method="first", ascending=False).astype(int)
    return keepers


def build_rankings(leaderboards_path: Path, clean_sheets_path: Path) -> pd.DataFrame:
    leaderboards = pd.read_csv(leaderboards_path)
    clean_sheets = pd.read_csv(clean_sheets_path)
    outfield = score_outfield(leaderboards)
    goalkeepers = score_goalkeepers(leaderboards, clean_sheets)
    common_cols = ["player", "squad", "position_group", "performance_score", "rank"]
    # Keep all source features too, which makes the ranking explainable in SQL/dashboard work.
    combined = pd.concat([outfield, goalkeepers], ignore_index=True, sort=False)
    return combined.sort_values(["position_group", "rank", "player"]).reset_index(drop=True)
