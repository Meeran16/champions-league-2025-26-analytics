<div align="center">

# UEFA Champions League 2025/26 Analytics

**SQL + Python analysis of the complete 2025/26 Champions League season**

Python · SQL · SQLite · Pandas · Matplotlib · Jupyter

</div>

---

## Project Overview

This project analyzes the **2025/26 UEFA Champions League** using complementary match datasets and a reproducible player-leaderboard layer:

- a complete competition-results source containing **189 matches** across the league phase and knockout stages;
- a richer match-statistics source containing **144 league-phase matches** with possession, shots, saves, venue and referee information;
- local player-statistic snapshots derived from published UEFA leaderboards and a StatBunker goalkeeper clean-sheet table.

The project focuses on a practical analytics workflow: source inspection, data cleaning, cross-source validation, relational modelling, SQL analysis, Python visualization and explainable position-specific player scoring.

The source scopes are deliberately kept separate. Detailed possession and shooting analysis is performed only for the league phase because the richer match dataset does not contain the knockout rounds. The player layer is also explicitly bounded: it is a **Leaderboard Performance Index (LPI)** built from published leaderboard candidates, not a full event-data model of every player action.

---

## Analytical Questions

The project is designed to answer questions such as:

- Which teams performed best during the league phase?
- How large was home advantage?
- Which clubs combined scoring output with shooting efficiency?
- How did home and away performance differ by team?
- What did five-match rolling form look like?
- How often did the side with more possession actually win?
- Which teams scored and conceded the most across the complete competition?
- How did match characteristics change across tournament stages?
- How should extra-time and penalty-shootout matches be represented correctly in an analytical database?
- Which published statistical leaders score most strongly within a transparent, position-specific player index?

---

## Data Sources

| Source | Coverage | Main fields used |
|---|---:|---|
| OpenFootball Champions League 2025/26 | 189 matches | dates, stages, teams, scores, half-time scores, extra time, penalties |
| Champions League Matches 2025–2026 dataset | 144 league-phase matches | venue, referee, possession, shots, shots on target, saves |
| UEFA Champions League 2025/26 published player leaderboards | selected top-six player leaderboards | goals, assists, attempts on target, tackles, balls recovered, saves |
| StatBunker goalkeeper snapshot | goalkeeper clean-sheet table | clean sheets, appearances, clean-sheet percentage |

Match-source details are documented in [`data/raw/README.md`](data/raw/README.md). Player-source details and reproducibility notes are documented in [`data/raw/player_sources.md`](data/raw/player_sources.md).

The original match datasets are intentionally excluded from Git tracking. The repository stores the processing logic, generated analysis outputs and the small player-source snapshots required to reproduce the LPI.

---

## Data Engineering Workflow

```text
Complete results source                 Detailed league-phase source
       189 matches                               144 matches
            │                                         │
            ▼                                         ▼
   Parse stages/scores                       Clean percentages
   Extra time/penalties                      Parse "x of y" fields
            │                                         │
            └───────────────┬─────────────────────────┘
                            ▼
                   Standardize team names
                            ▼
                   Cross-source validation
                            ▼
                      SQLite database
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
          SQL analysis              Python analysis
              │                           │
              └─────────────┬─────────────┘
                            ▼
                    Findings + figures
```

The player layer is intentionally independent of live web access:

```text
UEFA leaderboard snapshot      StatBunker goalkeeper snapshot
            │                              │
            └──────────────┬───────────────┘
                           ▼
                  Position-specific LPI
                           ▼
                  Player ranking tables
                           ▼
                Markdown report + charts
                           ▼
                     SQLite tables
```

---

## Data Quality and Cleaning

Several realistic cleaning problems are handled explicitly:

- The detailed source contains **151 raw rows**, including **7 empty separator rows**; the pipeline retains the **144 actual matches**.
- Possession values such as `63%` are converted to numeric percentages.
- Shooting values such as `3 of 10` are split into shots on target and total shots.
- The two match sources use different club-name conventions, so a canonical team mapping is maintained in [`src/team_mapping.py`](src/team_mapping.py).
- All **144 detailed matches** are joined one-to-one to the full competition source using date, home team and away team.
- All 144 linked scores are validated across both match sources.
- Possession totals are 100% for 132 matches and 101% for 12 matches because of source rounding.
- Extra time and penalty shootouts are modelled separately. The final, for example, is represented as a **1–1 match after extra time** with a separate **4–3 penalty shootout**, rather than being treated as a normal 4–3 match.
- Player ranking calculations use committed source snapshots rather than runtime scraping, so the analysis remains deterministic even when third-party sites block or time out.

A detailed match field-level description is available in [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## Database Design

The SQLite database starts with three core match tables:

```text
teams
  team_id (PK)
  team_name
  country_code

matches
  match_id (PK)
  date
  stage
  matchday
  home_team_id (FK)
  away_team_id (FK)
  goals
  half-time score
  extra-time flag
  penalty-shootout fields

league_phase_stats
  match_id (PK/FK)
  venue
  referee
  possession
  total shots
  shots on target
  saves
  shooting / save percentages
```

The player upgrade adds generated player-analysis tables to the same local database. This keeps full-season results, league-phase match statistics and the bounded player-ranking layer logically separate.

---

## SQL Skills Demonstrated

The SQL analysis includes:

`JOIN` · `GROUP BY` · `CASE` · CTEs · `UNION ALL` · conditional aggregation · `ROW_NUMBER()` · `RANK()` · rolling window calculations

Files:

- [`sql/02_data_quality.sql`](sql/02_data_quality.sql) — validation queries
- [`sql/03_team_performance.sql`](sql/03_team_performance.sql) — league table and full-competition team performance
- [`sql/04_home_away_analysis.sql`](sql/04_home_away_analysis.sql) — home/away performance
- [`sql/05_advanced_analysis.sql`](sql/05_advanced_analysis.sql) — rolling form and attacking-efficiency analysis
- [`sql/06_player_performance.sql`](sql/06_player_performance.sql) — player-performance exploration
- [`sql/07_position_rankings.sql`](sql/07_position_rankings.sql) — position-specific ranking queries

---

## Initial Findings

The generated analysis currently confirms:

- **36 teams** and **189 matches** are represented in the complete competition dataset.
- The tournament stages contain 144 league-phase matches, 16 knockout play-off matches, 16 Round-of-16 matches, 8 quarter-finals, 4 semi-finals and 1 final.
- Arsenal finished the league phase with **24 points from 8 matches** in the reconstructed league-phase table.
- The final finished **Paris Saint-Germain 1–1 Arsenal after extra time**, with Paris Saint-Germain winning the shootout **4–3**.

Additional generated findings are stored in [`reports/analysis_summary.md`](reports/analysis_summary.md).

### League-phase points

![League phase top teams](reports/figures/league_phase_top12_points.png)

### League-phase match outcomes

![League phase outcomes](reports/figures/league_phase_outcomes.png)

### Goal conversion

![Goal conversion](reports/figures/goal_conversion_top12.png)

---

## Player Performance Analysis

The repository includes a reproducible **Leaderboard Performance Index (LPI)** for four broad position groups:

- Forward
- Midfielder
- Defender
- Goalkeeper

The LPI is an explainable portfolio metric, **not an official UEFA player ranking**. It intentionally uses only statistics that can be preserved locally and traced back to published source tables.

For outfield players, published leaderboard rank is converted into a transparent point signal and then combined with position-specific weights:

| Position | Signals used |
|---|---|
| Forward | goals, attempts on target, assists |
| Midfielder | tackles, balls recovered, assists, attempts on target |
| Defender | balls recovered, tackles, assists |
| Goalkeeper | UEFA saves leaderboard plus StatBunker clean-sheet count/rate |

A player who is absent from a published top-six leaderboard receives zero **leaderboard points** for that category. This does not imply that the player's actual statistic was zero. For that reason, the LPI is explicitly described as a ranking of published leaderboard candidates rather than a complete all-player performance model.

The implementation uses **zero network requests at runtime**. Source snapshots are versioned in the repository, the ranking calculations are deterministic, and the resulting methodology can be reproduced during an interview or code review without depending on third-party website availability.

Detailed methodology: [`docs/player_ranking_methodology.md`](docs/player_ranking_methodology.md)

Generated report: [`reports/player_rankings.md`](reports/player_rankings.md)

Generated charts:

- [`reports/figures/top5_forwards.png`](reports/figures/top5_forwards.png)
- [`reports/figures/top5_midfielders.png`](reports/figures/top5_midfielders.png)
- [`reports/figures/top5_defenders.png`](reports/figures/top5_defenders.png)
- [`reports/figures/top5_goalkeepers.png`](reports/figures/top5_goalkeepers.png)

Run the player layer after the base pipeline:

```bash
python src/run_player_upgrade.py
python src/validate_player_data.py
```

The generated ranking data is loaded into the local SQLite database for subsequent SQL queries and dashboard work.

---

## Repository Structure

```text
champions-league-2025-26-analytics/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── README.md
│   │   └── player_sources.md
│   └── processed/              # generated locally, ignored by Git
│
├── src/
│   ├── team_mapping.py
│   ├── parse_full_results.py
│   ├── clean_league_stats.py
│   ├── build_database.py
│   ├── validate_data.py
│   ├── run_pipeline.py
│   ├── generate_report.py
│   ├── fetch_player_data.py
│   ├── player_metrics.py
│   ├── build_player_rankings.py
│   ├── load_player_data.py
│   ├── validate_player_data.py
│   └── run_player_upgrade.py
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_data_quality.sql
│   ├── 03_team_performance.sql
│   ├── 04_home_away_analysis.sql
│   ├── 05_advanced_analysis.sql
│   ├── 06_player_performance.sql
│   └── 07_position_rankings.sql
│
├── notebooks/
│   └── champions_league_analysis.ipynb
│
├── reports/
│   ├── analysis_summary.md
│   ├── player_rankings.md
│   └── figures/
│
└── docs/
    ├── data_dictionary.md
    ├── interview_notes.md
    └── player_ranking_methodology.md
```

---

## Run Locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the source datasets

Place the two raw match files in `data/raw/` as described in [`data/raw/README.md`](data/raw/README.md). The small player-source snapshots required by the LPI are already versioned with the project.

### 4. Run the complete match pipeline

```bash
python src/run_pipeline.py
```

### 5. Validate the match database

```bash
python src/validate_data.py
```

### 6. Generate the match report and figures

```bash
python src/generate_report.py
```

### 7. Run and validate the player layer

```bash
python src/run_player_upgrade.py
python src/validate_player_data.py
```

### 8. Open the notebook

```bash
jupyter notebook notebooks/champions_league_analysis.ipynb
```

---

## Interview-Friendly Summary

A concise explanation of the project is available in [`docs/interview_notes.md`](docs/interview_notes.md). It covers the project objective, why multiple sources were needed, the main cleaning decisions, SQL concepts used, the player-ranking design and the most important limitations.

---

## Current Scope and Limitations

The project contains two intentionally different analytical scopes:

1. **Team and match analytics** — complete results for all 189 matches, with richer possession/shooting analysis limited to the 144-match league phase.
2. **Player leaderboard analytics** — an explainable LPI based on preserved UEFA leaderboard snapshots and goalkeeper clean-sheet data.

The LPI should not be interpreted as a complete ranking of every eligible Champions League player because the source snapshots contain published leaderboard candidates rather than uniform event-level statistics for the whole player population. A future version could replace the LPI with a full per-90 model if a complete, redistributable and reproducible all-player dataset becomes available.

No knockout-stage possession or shooting values are inferred, and no missing player statistics are fabricated.
