from pathlib import Path
import pandas as pd

EXPECTED_TOP = {
    "Forward": "Kylian Mbappe",
    "Defender": "William Pacho",
}


def main() -> None:
    path = Path("data/processed/player_rankings.csv")
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}; run player upgrade first.")
    df = pd.read_csv(path)
    expected_positions = {"Forward", "Midfielder", "Defender", "Goalkeeper"}
    assert expected_positions.issubset(set(df["position_group"])), "Position groups missing"
    assert df["performance_score"].between(0, 100).all(), "Score outside 0–100"
    assert df.groupby("position_group")["rank"].min().eq(1).all(), "Rank 1 missing"
    assert df.groupby("position_group").size().ge(5).all(), "Fewer than five candidates for a position"
    for position, expected in EXPECTED_TOP.items():
        actual = df[(df["position_group"] == position) & (df["rank"] == 1)].iloc[0]["player"]
        assert actual == expected, f"Unexpected {position} leader: {actual}"
    print("Player validation passed:")
    for position in ["Forward", "Midfielder", "Defender", "Goalkeeper"]:
        g = df[df["position_group"] == position]
        leader = g.nsmallest(1, "rank").iloc[0]
        print(f"  {position}: {len(g)} candidates, leader = {leader['player']} ({leader['performance_score']:.2f})")
    print("  score bounds: passed")
    print("  source mode: offline snapshots")


if __name__ == "__main__":
    main()
