-- Overall home/draw/away outcome distribution during the league phase.
SELECT
    CASE match_outcome
        WHEN 'H' THEN 'Home Win'
        WHEN 'D' THEN 'Draw'
        WHEN 'A' THEN 'Away Win'
    END AS outcome,
    COUNT(*) AS matches,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS share_pct
FROM matches
WHERE stage = 'League Phase'
GROUP BY match_outcome
ORDER BY matches DESC;

-- Team-level home versus away points per game.
WITH team_matches AS (
    SELECT
        t.team_name,
        'Home' AS venue_role,
        CASE
            WHEN m.home_goals > m.away_goals THEN 3
            WHEN m.home_goals = m.away_goals THEN 1
            ELSE 0
        END AS points
    FROM matches m
    JOIN teams t ON t.team_id = m.home_team_id
    WHERE m.stage = 'League Phase'

    UNION ALL

    SELECT
        t.team_name,
        'Away',
        CASE
            WHEN m.away_goals > m.home_goals THEN 3
            WHEN m.away_goals = m.home_goals THEN 1
            ELSE 0
        END
    FROM matches m
    JOIN teams t ON t.team_id = m.away_team_id
    WHERE m.stage = 'League Phase'
)
SELECT
    team_name,
    ROUND(AVG(CASE WHEN venue_role = 'Home' THEN points END), 2) AS home_ppg,
    ROUND(AVG(CASE WHEN venue_role = 'Away' THEN points END), 2) AS away_ppg,
    ROUND(
        AVG(CASE WHEN venue_role = 'Home' THEN points END)
        - AVG(CASE WHEN venue_role = 'Away' THEN points END),
        2
    ) AS home_advantage_ppg
FROM team_matches
GROUP BY team_name
ORDER BY home_advantage_ppg DESC;
