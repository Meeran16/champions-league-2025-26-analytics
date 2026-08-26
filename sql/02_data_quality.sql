-- Basic dataset checks used before analysis.

-- Expected: 36 teams.
SELECT COUNT(*) AS team_count FROM teams;

-- Expected: 189 matches.
SELECT COUNT(*) AS match_count FROM matches;

-- Expected stage distribution: 144, 16, 16, 8, 4, 1.
SELECT stage, COUNT(*) AS matches
FROM matches
GROUP BY stage
ORDER BY CASE stage
    WHEN 'League Phase' THEN 1
    WHEN 'Knockout Play-offs' THEN 2
    WHEN 'Round of 16' THEN 3
    WHEN 'Quarter-finals' THEN 4
    WHEN 'Semi-finals' THEN 5
    WHEN 'Final' THEN 6
END;

-- Expected: 144 detailed league-phase rows.
SELECT COUNT(*) AS detailed_match_count
FROM league_phase_stats;

-- Every detailed row should link to a league-phase match.
SELECT COUNT(*) AS invalid_detail_links
FROM league_phase_stats s
JOIN matches m ON m.match_id = s.match_id
WHERE m.stage <> 'League Phase';

-- Possession is rounded in the source. Some rows sum to 101 rather than 100.
SELECT
    ROUND(home_possession + away_possession, 1) AS possession_total,
    COUNT(*) AS matches
FROM league_phase_stats
GROUP BY ROUND(home_possession + away_possession, 1)
ORDER BY possession_total;

-- The saves denominator is expected to equal the opponent's shots on target.
SELECT COUNT(*) AS impossible_save_counts
FROM league_phase_stats
WHERE home_saves_count > away_shots_on_target_count
   OR away_saves_count > home_shots_on_target_count;
