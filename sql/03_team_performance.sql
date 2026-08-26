-- League-phase team performance table.
-- Each match is converted into one row per team, then aggregated.

WITH team_matches AS (
    SELECT
        m.match_id,
        m.date,
        t.team_name,
        'Home' AS venue_role,
        m.home_goals AS goals_for,
        m.away_goals AS goals_against,
        CASE
            WHEN m.home_goals > m.away_goals THEN 3
            WHEN m.home_goals = m.away_goals THEN 1
            ELSE 0
        END AS points,
        CASE WHEN m.home_goals > m.away_goals THEN 1 ELSE 0 END AS win,
        CASE WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END AS draw,
        CASE WHEN m.home_goals < m.away_goals THEN 1 ELSE 0 END AS loss
    FROM matches m
    JOIN teams t ON t.team_id = m.home_team_id
    WHERE m.stage = 'League Phase'

    UNION ALL

    SELECT
        m.match_id,
        m.date,
        t.team_name,
        'Away' AS venue_role,
        m.away_goals AS goals_for,
        m.home_goals AS goals_against,
        CASE
            WHEN m.away_goals > m.home_goals THEN 3
            WHEN m.away_goals = m.home_goals THEN 1
            ELSE 0
        END AS points,
        CASE WHEN m.away_goals > m.home_goals THEN 1 ELSE 0 END AS win,
        CASE WHEN m.away_goals = m.home_goals THEN 1 ELSE 0 END AS draw,
        CASE WHEN m.away_goals < m.home_goals THEN 1 ELSE 0 END AS loss
    FROM matches m
    JOIN teams t ON t.team_id = m.away_team_id
    WHERE m.stage = 'League Phase'
)
SELECT
    team_name,
    COUNT(*) AS played,
    SUM(win) AS wins,
    SUM(draw) AS draws,
    SUM(loss) AS losses,
    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against,
    SUM(goals_for) - SUM(goals_against) AS goal_difference,
    SUM(points) AS points,
    ROUND(1.0 * SUM(points) / COUNT(*), 2) AS points_per_match
FROM team_matches
GROUP BY team_name
ORDER BY points DESC, goal_difference DESC, goals_for DESC;

-- Full-competition goal production by team.
WITH team_goals AS (
    SELECT t.team_name, m.home_goals AS goals_for, m.away_goals AS goals_against
    FROM matches m
    JOIN teams t ON t.team_id = m.home_team_id

    UNION ALL

    SELECT t.team_name, m.away_goals, m.home_goals
    FROM matches m
    JOIN teams t ON t.team_id = m.away_team_id
)
SELECT
    team_name,
    COUNT(*) AS matches_played,
    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against,
    SUM(goals_for) - SUM(goals_against) AS goal_difference,
    ROUND(1.0 * SUM(goals_for) / COUNT(*), 2) AS goals_per_match
FROM team_goals
GROUP BY team_name
ORDER BY goals_for DESC, goal_difference DESC;
