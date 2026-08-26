PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    country_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    kickoff_time TEXT,
    stage TEXT NOT NULL,
    matchday INTEGER,
    home_goals INTEGER NOT NULL,
    away_goals INTEGER NOT NULL,
    regulation_home_goals INTEGER,
    regulation_away_goals INTEGER,
    half_time_home_goals INTEGER,
    half_time_away_goals INTEGER,
    extra_time INTEGER NOT NULL CHECK (extra_time IN (0, 1)),
    penalty_shootout INTEGER NOT NULL CHECK (penalty_shootout IN (0, 1)),
    penalty_home INTEGER,
    penalty_away INTEGER,
    match_outcome TEXT NOT NULL CHECK (match_outcome IN ('H', 'D', 'A')),
    winner TEXT NOT NULL,
    source_score TEXT NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS league_phase_stats (
    match_id INTEGER PRIMARY KEY,
    venue TEXT,
    referee TEXT,
    home_possession REAL,
    away_possession REAL,
    home_shots_total INTEGER,
    away_shots_total INTEGER,
    home_shots_on_target_count INTEGER,
    away_shots_on_target_count INTEGER,
    home_saves_count INTEGER,
    away_saves_count INTEGER,
    home_shots_on_target_pct REAL,
    away_shots_on_target_pct REAL,
    home_saves_pct REAL,
    away_saves_pct REAL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);
