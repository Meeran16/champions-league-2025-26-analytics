# Interview Explanation Notes

## 30-second explanation

I built a SQL and Python analysis of the 2025/26 UEFA Champions League. I combined a complete 189-match results source with a richer 144-match league-phase statistics dataset. The two sources used different team names and data formats, so I standardized club names, parsed scores and percentage fields, validated all league-phase matches across both sources, and loaded the clean data into a relational SQLite database. I then used SQL for team rankings, home-versus-away analysis, rolling form and attacking efficiency, and Python for visual summaries.

## Why two sources?

The complete source covers the entire tournament but mainly provides fixtures and scores. The second source has richer match statistics but only covers the 144-match league phase. Keeping those scopes separate avoids pretending that possession or shot data exists for knockout matches.

## Data-cleaning examples

- Removed seven empty separator rows from the detailed CSV.
- Converted possession values such as `63%` into numeric values.
- Parsed strings such as `3 of 10` into shots on target = 3 and total shots = 10.
- Standardized names such as `FC Bayern München` and `Bayern Munich` to one canonical value.
- Matched all 144 detailed rows to the complete results source with no score mismatches.
- Modelled extra time and penalty shootouts separately.

## SQL examples to discuss

- `JOIN` to connect matches, teams and detailed statistics.
- `CASE` to convert scores into 3/1/0 league points.
- `UNION ALL` to transform home and away records into a team-centric match table.
- CTEs to make multi-step analysis readable.
- `RANK()` for efficiency rankings.
- `ROW_NUMBER()` and rolling `SUM() OVER (...)` for five-match form.
- Conditional aggregation for home-versus-away comparisons.

## Important limitation

The detailed statistics cover only the league phase. Knockout analysis therefore uses scores/results unless a new validated detailed-stat source is added later.

## Good interview principle

Do not claim that possession, shots or another metric *causes* winning from this project. The analysis is descriptive. It can show associations and patterns, but causal conclusions would require a different design.
