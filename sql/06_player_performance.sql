-- Offline, reproducible player-ranking analysis.
-- Rankings are a project-created Leaderboard Performance Index (LPI), not an official UEFA award.

SELECT
    position_group,
    COUNT(*) AS candidate_players,
    ROUND(MAX(performance_score), 2) AS highest_score,
    ROUND(AVG(performance_score), 2) AS average_score
FROM player_rankings
GROUP BY position_group
ORDER BY position_group;

SELECT
    rank,
    player,
    squad,
    performance_score
FROM player_rankings
WHERE position_group = 'Forward'
ORDER BY rank
LIMIT 10;
