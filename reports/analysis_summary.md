# Initial Analysis Summary

This report is generated from the locally built SQLite database. It is intended as a concise portfolio summary rather than a complete football-performance model.

## Competition overview

- Full competition matches: **189**
- Goals scored: **655**
- Goals per match: **3.47**
- Final: **Paris Saint-Germain 1-1 Arsenal after extra time; Paris Saint-Germain won the penalty shootout 4-3.**

## Stage counts

| stage              |   matches |   goals |
|:-------------------|----------:|--------:|
| League Phase       |       144 |     487 |
| Knockout Play-offs |        16 |      64 |
| Round of 16        |        16 |      68 |
| Quarter-finals     |         8 |      20 |
| Semi-finals        |         4 |      14 |
| Final              |         1 |       2 |

## League-phase leaders

| team_name         |   played |   points |   goals_for |   goals_against |   goal_difference |
|:------------------|---------:|---------:|------------:|----------------:|------------------:|
| Arsenal           |        8 |       24 |          23 |               4 |                19 |
| Bayern Munich     |        8 |       21 |          22 |               8 |                14 |
| Liverpool         |        8 |       18 |          20 |               8 |                12 |
| Tottenham Hotspur |        8 |       17 |          17 |               7 |                10 |
| Barcelona         |        8 |       16 |          22 |              14 |                 8 |
| Chelsea           |        8 |       16 |          17 |              10 |                 7 |
| Sporting CP       |        8 |       16 |          17 |              11 |                 6 |
| Manchester City   |        8 |       16 |          15 |               9 |                 6 |
| Real Madrid       |        8 |       15 |          21 |              12 |                 9 |
| Inter             |        8 |       15 |          15 |               7 |                 8 |

## League-phase outcomes

| outcome   |   matches |
|:----------|----------:|
| Home Win  |        71 |
| Away Win  |        48 |
| Draw      |        25 |

## Detailed-stat observation

Across league-phase matches where one side had strictly more possession, that side won **51.1%** of those matches. This is descriptive only; it does not establish that possession causes winning.

## Highest goal-conversion rates

| team_name           |   goals |   shots |   shots_on_target |   goal_conversion_pct |   shot_accuracy_pct |   avg_possession |
|:--------------------|--------:|--------:|------------------:|----------------------:|--------------------:|-----------------:|
| Dortmund            |      19 |      94 |                41 |                  20.2 |                43.6 |             54.5 |
| Sporting CP         |      17 |      89 |                39 |                  19.1 |                43.8 |             48.6 |
| PSV                 |      16 |      86 |                31 |                  18.6 |                36   |             51.8 |
| Eintracht Frankfurt |      10 |      55 |                24 |                  18.2 |                43.6 |             39.4 |
| Arsenal             |      23 |     134 |                63 |                  17.2 |                47   |             54.6 |
| Tottenham Hotspur   |      17 |     100 |                38 |                  17   |                38   |             50.8 |
| Newcastle United    |      17 |     104 |                48 |                  16.3 |                46.2 |             47.8 |
| Qarabağ             |      13 |      82 |                33 |                  15.9 |                40.2 |             46.1 |
| Bayern Munich       |      22 |     139 |                61 |                  15.8 |                43.9 |             58.8 |
| Barcelona           |      22 |     140 |                55 |                  15.7 |                39.3 |             64.8 |

## Figures

- `figures/league_phase_top12_points.png`
- `figures/league_phase_outcomes.png`
- `figures/goal_conversion_top12.png`

## Interpretation note

The detailed CSV covers the 144-match league phase only. Knockout-stage conclusions in this project therefore use match results, not possession or shooting statistics, unless another source is explicitly added later.