from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DB = Path("data/processed/champions_league.db")
FIGURES = Path("reports/figures")
REPORT = Path("reports/analysis_summary.md")


def query(conn, sql):
    return pd.read_sql_query(sql, conn)


def save_bar(df, x, y, title, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df[x], df[y])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    if not DB.exists():
        raise SystemExit("Database not found. Run python src/run_pipeline.py first.")

    FIGURES.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB) as conn:
        overview = query(conn, """
            SELECT
                COUNT(*) AS matches,
                SUM(home_goals + away_goals) AS goals,
                ROUND(1.0 * SUM(home_goals + away_goals) / COUNT(*), 2) AS goals_per_match
            FROM matches
        """).iloc[0]

        stage = query(conn, """
            SELECT stage, COUNT(*) AS matches, SUM(home_goals + away_goals) AS goals
            FROM matches
            GROUP BY stage
            ORDER BY CASE stage
                WHEN 'League Phase' THEN 1
                WHEN 'Knockout Play-offs' THEN 2
                WHEN 'Round of 16' THEN 3
                WHEN 'Quarter-finals' THEN 4
                WHEN 'Semi-finals' THEN 5
                WHEN 'Final' THEN 6
            END
        """)

        standings = query(conn, """
            WITH team_matches AS (
                SELECT t.team_name,
                       m.home_goals AS gf,
                       m.away_goals AS ga,
                       CASE WHEN m.home_goals > m.away_goals THEN 3
                            WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END AS pts
                FROM matches m JOIN teams t ON t.team_id=m.home_team_id
                WHERE m.stage='League Phase'
                UNION ALL
                SELECT t.team_name,
                       m.away_goals,
                       m.home_goals,
                       CASE WHEN m.away_goals > m.home_goals THEN 3
                            WHEN m.away_goals = m.home_goals THEN 1 ELSE 0 END
                FROM matches m JOIN teams t ON t.team_id=m.away_team_id
                WHERE m.stage='League Phase'
            )
            SELECT team_name,
                   COUNT(*) AS played,
                   SUM(pts) AS points,
                   SUM(gf) AS goals_for,
                   SUM(ga) AS goals_against,
                   SUM(gf)-SUM(ga) AS goal_difference
            FROM team_matches
            GROUP BY team_name
            ORDER BY points DESC, goal_difference DESC, goals_for DESC
        """)

        outcomes = query(conn, """
            SELECT CASE match_outcome WHEN 'H' THEN 'Home Win' WHEN 'D' THEN 'Draw' ELSE 'Away Win' END AS outcome,
                   COUNT(*) AS matches
            FROM matches
            WHERE stage='League Phase'
            GROUP BY match_outcome
            ORDER BY matches DESC
        """)

        efficiency = query(conn, """
            WITH team_stats AS (
                SELECT ht.team_name, m.home_goals goals, s.home_shots_total shots,
                       s.home_shots_on_target_count sot, s.home_possession possession
                FROM league_phase_stats s
                JOIN matches m ON m.match_id=s.match_id
                JOIN teams ht ON ht.team_id=m.home_team_id
                UNION ALL
                SELECT at.team_name, m.away_goals, s.away_shots_total,
                       s.away_shots_on_target_count, s.away_possession
                FROM league_phase_stats s
                JOIN matches m ON m.match_id=s.match_id
                JOIN teams at ON at.team_id=m.away_team_id
            )
            SELECT team_name,
                   SUM(goals) goals,
                   SUM(shots) shots,
                   SUM(sot) shots_on_target,
                   ROUND(100.0*SUM(goals)/NULLIF(SUM(shots),0),1) goal_conversion_pct,
                   ROUND(100.0*SUM(sot)/NULLIF(SUM(shots),0),1) shot_accuracy_pct,
                   ROUND(AVG(possession),1) avg_possession
            FROM team_stats
            GROUP BY team_name
            ORDER BY goal_conversion_pct DESC, goals DESC
        """)

        more_possession = query(conn, """
            WITH team_view AS (
                SELECT
                    CASE
                        WHEN s.home_possession > s.away_possession THEN 'Home'
                        WHEN s.away_possession > s.home_possession THEN 'Away'
                        ELSE 'Equal'
                    END AS more_possession_side,
                    m.match_outcome
                FROM league_phase_stats s
                JOIN matches m ON m.match_id=s.match_id
            )
            SELECT
                SUM(CASE WHEN more_possession_side='Home' AND match_outcome='H' THEN 1
                         WHEN more_possession_side='Away' AND match_outcome='A' THEN 1 ELSE 0 END) AS more_possession_wins,
                SUM(CASE WHEN more_possession_side IN ('Home','Away') THEN 1 ELSE 0 END) AS unequal_possession_matches
            FROM team_view
        """).iloc[0]

        final_row = query(conn, """
            SELECT ht.team_name home_team, at.team_name away_team,
                   m.home_goals, m.away_goals, m.penalty_home, m.penalty_away, m.winner
            FROM matches m
            JOIN teams ht ON ht.team_id=m.home_team_id
            JOIN teams at ON at.team_id=m.away_team_id
            WHERE stage='Final'
        """).iloc[0]

    save_bar(
        standings.head(12), "team_name", "points",
        "2025/26 Champions League League Phase — Top 12 by Points",
        "Points", "league_phase_top12_points.png"
    )
    save_bar(
        outcomes, "outcome", "matches",
        "League Phase Match Outcomes",
        "Matches", "league_phase_outcomes.png"
    )
    save_bar(
        efficiency.head(12), "team_name", "goal_conversion_pct",
        "League Phase — Top 12 Goal Conversion Rates",
        "Goal conversion (%)", "goal_conversion_top12.png"
    )

    possession_win_rate = 100.0 * more_possession["more_possession_wins"] / more_possession["unequal_possession_matches"]

    lines = [
        "# Initial Analysis Summary",
        "",
        "This report is generated from the locally built SQLite database. It is intended as a concise portfolio summary rather than a complete football-performance model.",
        "",
        "## Competition overview",
        "",
        f"- Full competition matches: **{int(overview['matches'])}**",
        f"- Goals scored: **{int(overview['goals'])}**",
        f"- Goals per match: **{overview['goals_per_match']:.2f}**",
        f"- Final: **{final_row['home_team']} {int(final_row['home_goals'])}-{int(final_row['away_goals'])} {final_row['away_team']} after extra time; {final_row['winner']} won the penalty shootout {int(final_row['penalty_home'])}-{int(final_row['penalty_away'])}.**",
        "",
        "## Stage counts",
        "",
        stage.to_markdown(index=False),
        "",
        "## League-phase leaders",
        "",
        standings.head(10).to_markdown(index=False),
        "",
        "## League-phase outcomes",
        "",
        outcomes.to_markdown(index=False),
        "",
        "## Detailed-stat observation",
        "",
        f"Across league-phase matches where one side had strictly more possession, that side won **{possession_win_rate:.1f}%** of those matches. This is descriptive only; it does not establish that possession causes winning.",
        "",
        "## Highest goal-conversion rates",
        "",
        efficiency.head(10).to_markdown(index=False),
        "",
        "## Figures",
        "",
        "- `figures/league_phase_top12_points.png`",
        "- `figures/league_phase_outcomes.png`",
        "- `figures/goal_conversion_top12.png`",
        "",
        "## Interpretation note",
        "",
        "The detailed CSV covers the 144-match league phase only. Knockout-stage conclusions in this project therefore use match results, not possession or shooting statistics, unless another source is explicitly added later.",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated report -> {REPORT}")


if __name__ == "__main__":
    main()
