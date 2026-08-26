# Player Ranking Methodology

## Purpose

This project adds an explainable player-ranking layer to the UEFA Champions League 2025/26 analytics repository.

The output is a **Leaderboard Performance Index (LPI)**. It is a portfolio analytics model and **not an official UEFA award**.

## Why local snapshots are used

The first implementation attempted live scraping. FBref returned HTTP 403 and StatBunker later timed out. Live scraping therefore made the project non-deterministic.

The final implementation stores small, cited source snapshots in `data/raw/` and performs all ranking calculations locally. This improves reproducibility and makes the project safe to demonstrate in an interview without relying on third-party website availability.

## Source signals

UEFA 2025/26 published top-six leaderboards:

- Goals
- Assists
- Attempts on target
- Tackles
- Balls recovered
- Saves

StatBunker snapshot:

- Goalkeeper clean sheets
- Goalkeeper matches played
- Clean-sheet percentage

## Leaderboard points

Published rank is converted to a transparent signal:

| Rank | Points |
|---:|---:|
| 1 | 100 |
| 2 | 80 |
| 3 | 65 |
| 4 | 50 |
| 5 | 35 |
| 6 | 20 |

If a player is absent from a published top-six list, the model gives zero *leaderboard points* for that category. This does **not** mean the player's actual statistic was zero.

## Position weights

### Forward
- Goals: 45%
- Attempts on target: 35%
- Assists: 20%

### Midfielder
- Tackles: 35%
- Balls recovered: 30%
- Assists: 25%
- Attempts on target: 10%

### Defender
- Balls recovered: 50%
- Tackles: 25%
- Assists: 25%

### Goalkeeper
- UEFA saves leaderboard: 60%
- Clean-sheet signal: 40%

The clean-sheet signal combines clean-sheet count and clean-sheet percentage among goalkeepers with at least six appearances.

## Position classification

Primary position follows UEFA squad categorisation where available. A tactical role in a Team of the Season formation does not automatically replace the player's primary squad category.

## Limitation

This model ranks players from published leaderboard candidates; it is not a full event-data model covering every action by every player. The dashboard should label the result clearly as `Leaderboard Performance Index` or `Project Performance Index`, not as an official UEFA ranking.
