-- Top five players by primary position according to the project LPI.
SELECT
    position_group,
    rank,
    player,
    squad,
    ROUND(performance_score, 2) AS performance_score
FROM player_rankings
WHERE rank <= 5
ORDER BY
    CASE position_group
        WHEN 'Forward' THEN 1
        WHEN 'Midfielder' THEN 2
        WHEN 'Defender' THEN 3
        WHEN 'Goalkeeper' THEN 4
        ELSE 5
    END,
    rank;
