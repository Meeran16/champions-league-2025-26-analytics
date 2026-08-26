# Player Performance Rankings — UEFA Champions League 2025/26

These are project rankings produced by a **Leaderboard Performance Index (LPI)**. They are not official UEFA awards.

The model uses a local, versioned snapshot of UEFA's published 2025/26 leaderboards so the project is reproducible and does not depend on fragile live scraping. Goalkeepers additionally use StatBunker clean-sheet totals/rates.

A player receives leaderboard points only when appearing in a published top-six category. This is deliberate: a missing leaderboard value means *outside the published top six*, not zero real-world performance.

## Top 5 Forwards

|   rank | player                | squad               |   performance_score |
|-------:|:----------------------|:--------------------|--------------------:|
|      1 | Kylian Mbappe         | Real Madrid         |               80    |
|      2 | Harry Kane            | Bayern Munich       |               58.75 |
|      3 | Julian Alvarez        | Atletico Madrid     |               52    |
|      4 | Khvicha Kvaratskhelia | Paris Saint-Germain |               42.25 |
|      5 | Anthony Gordon        | Newcastle United    |               29.25 |

## Top 5 Midfielders

|   rank | player              | squad         |   performance_score |
|-------:|:--------------------|:--------------|--------------------:|
|      1 | Moises Caicedo      | Chelsea       |               35    |
|      2 | Manuel Locatelli    | Juventus      |               35    |
|      3 | Michael Olise       | Bayern Munich |               27    |
|      4 | Aurelien Tchouameni | Real Madrid   |               22.75 |
|      5 | Lucas Torreira      | Galatasaray   |               17.5  |

## Top 5 Defenders

|   rank | player           | squad               |   performance_score |
|-------:|:-----------------|:--------------------|--------------------:|
|      1 | William Pacho    | Paris Saint-Germain |               50    |
|      2 | Nuno Mendes      | Paris Saint-Germain |               40    |
|      3 | Odin Bjortuft    | Bodo/Glimt          |               32.5  |
|      4 | Odilon Kossounou | Atalanta            |               17.5  |
|      5 | Achraf Hakimi    | Paris Saint-Germain |               16.25 |

## Top 5 Goalkeepers

|   rank | player            | squad             |   performance_score |
|-------:|:------------------|:------------------|--------------------:|
|      1 | Thibaut Courtois  | Real Madrid       |               79.38 |
|      2 | Nikita Haikin     | Bodo/Glimt        |               64.9  |
|      3 | David Raya        | Arsenal           |               61    |
|      4 | Ugurcan Cakir     | Galatasaray       |               59.24 |
|      5 | Guglielmo Vicario | Tottenham Hotspur |               38.31 |

## Interpretation

The LPI is intentionally explainable rather than predictive. It combines placement in relevant official leaderboards with position-specific weights. It should be described as an analytical index, not as an objective statement of the best footballers in the world.

## Position rule

Primary position follows UEFA squad categorisation where available. Tactical placement in a Team of the Season formation is not used to reclassify a player's primary squad position.

## Why a snapshot?

The earlier live-scraping approach was removed because public sites can return 403 errors or time out. Keeping a cited source snapshot makes the pipeline deterministic and interview-friendly.
