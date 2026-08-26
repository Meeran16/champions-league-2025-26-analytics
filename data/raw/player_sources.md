# Player source snapshots

The local CSV files in this directory are intentionally small source snapshots used to make the player-ranking pipeline reproducible.

## UEFA official statistics

Season: UEFA Champions League 2025/26

Source page:
`https://www.uefa.com/uefachampionsleague/history/seasons/2026/statistics/`

Snapshot categories:
- Goals
- Assists
- Attempts on target
- Tackles
- Balls recovered
- Saves

## StatBunker goalkeeper clean sheets

Source page:
`https://www.statbunker.com/competitions/Top10KeepersCleanSheets?comp_id=783`

Snapshot fields:
- player
- club
- clean sheets
- matches played
- clean-sheet percentage

## Reproducibility note

The application does not scrape either website at runtime. If the source statistics are updated or corrected, update these snapshots intentionally and commit that change so the analysis remains auditable.
