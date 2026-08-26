# Data Dictionary

## `teams`

| Column | Meaning |
|---|---|
| `team_id` | Surrogate integer key |
| `team_name` | Canonical team name used across sources |
| `country_code` | Country code supplied in the OpenFootball source |

## `matches`

Contains all 189 competition matches.

| Column | Meaning |
|---|---|
| `match_id` | Unique match key |
| `date` | Match date |
| `kickoff_time` | Kick-off time from the source |
| `stage` | League Phase, Knockout Play-offs, Round of 16, Quarter-finals, Semi-finals or Final |
| `matchday` | League/play-off matchday where applicable |
| `home_team_id` / `away_team_id` | Foreign keys to `teams` |
| `home_goals` / `away_goals` | Final football score excluding penalty-shootout kicks |
| `regulation_home_goals` / `regulation_away_goals` | Score after normal time where extra time occurred; otherwise final match score |
| `half_time_home_goals` / `half_time_away_goals` | Half-time score |
| `extra_time` | 1 when extra time was played |
| `penalty_shootout` | 1 when decided by penalties |
| `penalty_home` / `penalty_away` | Penalty shootout score, separate from the match score |
| `match_outcome` | `H`, `D` or `A` based on the football match score excluding penalties |
| `winner` | Match winner; for a penalty shootout this records the shootout winner |
| `source_score` | Original score representation retained for traceability |

## `league_phase_stats`

Contains detailed statistics for the 144 league-phase matches only.

| Column | Meaning |
|---|---|
| `match_id` | Foreign key to `matches` |
| `venue` | Stadium/venue |
| `referee` | Match referee |
| `home_possession` / `away_possession` | Possession percentage with `%` removed |
| `home_shots_total` / `away_shots_total` | Total shots parsed from the source's `x of y` field |
| `home_shots_on_target_count` / `away_shots_on_target_count` | Shots on target |
| `home_saves_count` / `away_saves_count` | Goalkeeper saves |
| `home_shots_on_target_pct` / `away_shots_on_target_pct` | Source shooting-on-target percentage |
| `home_saves_pct` / `away_saves_pct` | Source save percentage |

## Data-quality notes

- The detailed CSV originally contains 151 rows, of which 7 are empty separators. They are removed during cleaning.
- All 144 retained league-phase matches join one-to-one to the complete match source by date, home team and away team.
- All 144 scores agree across the two sources after cleaning.
- Possession totals equal 100% for 132 matches and 101% for 12 matches because the source percentages are rounded.
- The raw sources use different club-name conventions. `src/team_mapping.py` provides the canonical mapping used for joins.
- The final is stored as a 1–1 match after extra time with a separate 4–3 penalty-shootout score rather than incorrectly treating 4–3 as the football score.
