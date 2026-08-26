from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from player_metrics import build_rankings

POSITIONS = ["Forward", "Midfielder", "Defender", "Goalkeeper"]


def make_chart(top5: pd.DataFrame, position: str, output: Path) -> None:
    plot = top5.sort_values("performance_score", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(plot["player"], plot["performance_score"])
    ax.set_xlabel("Leaderboard Performance Index (0–100)")
    ax.set_title(f"Top 5 {position}s — UEFA Champions League 2025/26")
    ax.set_xlim(0, 100)
    for y, value in enumerate(plot["performance_score"]):
        ax.text(min(value + 1, 98), y, f"{value:.1f}", va="center")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)


def build_report(rankings: pd.DataFrame, report_path: Path) -> None:
    lines = [
        "# Player Performance Rankings — UEFA Champions League 2025/26",
        "",
        "These are project rankings produced by a **Leaderboard Performance Index (LPI)**. They are not official UEFA awards.",
        "",
        "The model uses a local, versioned snapshot of UEFA's published 2025/26 leaderboards so the project is reproducible and does not depend on fragile live scraping. Goalkeepers additionally use StatBunker clean-sheet totals/rates.",
        "",
        "A player receives leaderboard points only when appearing in a published top-six category. This is deliberate: a missing leaderboard value means *outside the published top six*, not zero real-world performance.",
        "",
    ]
    for position in POSITIONS:
        top5 = rankings[rankings["position_group"] == position].nsmallest(5, "rank")
        lines += [f"## Top 5 {position}s", ""]
        lines += [top5[["rank", "player", "squad", "performance_score"]].to_markdown(index=False), ""]
    lines += [
        "## Interpretation",
        "",
        "The LPI is intentionally explainable rather than predictive. It combines placement in relevant official leaderboards with position-specific weights. It should be described as an analytical index, not as an objective statement of the best footballers in the world.",
        "",
        "## Position rule",
        "",
        "Primary position follows UEFA squad categorisation where available. Tactical placement in a Team of the Season formation is not used to reclassify a player's primary squad position.",
        "",
        "## Why a snapshot?",
        "",
        "The earlier live-scraping approach was removed because public sites can return 403 errors or time out. Keeping a cited source snapshot makes the pipeline deterministic and interview-friendly.",
        "",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    leaderboards = Path("data/raw/uefa_player_leaderboards.csv")
    clean_sheets = Path("data/raw/goalkeeper_clean_sheets.csv")
    rankings_path = Path("data/processed/player_rankings.csv")
    report_path = Path("reports/player_rankings.md")
    figures = Path("reports/figures")

    rankings = build_rankings(leaderboards, clean_sheets)
    rankings_path.parent.mkdir(parents=True, exist_ok=True)
    rankings.to_csv(rankings_path, index=False)
    build_report(rankings, report_path)

    for position in POSITIONS:
        top5 = rankings[rankings["position_group"] == position].nsmallest(5, "rank")
        make_chart(top5, position, figures / f"top5_{position.lower()}s.png")

    print(f"Saved rankings -> {rankings_path}")
    print(f"Saved report -> {report_path}")
    for position in POSITIONS:
        print(f"\nTop 5 {position}s")
        print(rankings[rankings["position_group"] == position].nsmallest(5, "rank")[["rank", "player", "squad", "performance_score"]].to_string(index=False))


if __name__ == "__main__":
    main()
