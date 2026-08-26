-- Advanced SQL examples: rolling form, ranking, and efficiency.

-- Five-match rolling points during the league phase.
WITH team_matches AS (
    SELECT
        m.match_id,
        m.date,
        t.team_name,
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
        m.match_id,
        m.date,
        t.team_name,
        CASE
            WHEN m.away_goals > m.home_goals THEN 3
            WHEN m.away_goals = m.home_goals THEN 1
            ELSE 0
        END AS points
    FROM matches m
    JOIN teams t ON t.team_id = m.away_team_id
    WHERE m.stage = 'League Phase'
),
ordered AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY team_name ORDER BY date, match_id) AS match_number
    FROM team_matches
)
SELECT
    team_name,
    date,
    match_number,
    points,
    SUM(points) OVER (
        PARTITION BY team_name
        ORDER BY date, match_id
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS rolling_5_match_points
FROM ordered
ORDER BY team_name, date, match_id;

-- League-phase attacking efficiency using the detailed 144-match dataset.
WITH team_stats AS (
    SELECT
        ht.team_name,
        m.home_goals AS goals,
        s.home_shots_total AS shots,
        s.home_shots_on_target_count AS shots_on_target,
        s.home_possession AS possession
    FROM league_phase_stats s
    JOIN matches m ON m.match_id = s.match_id
    JOIN teams ht ON ht.team_id = m.home_team_id

    UNION ALL

    SELECT
        at.team_name,
        m.away_goals,
        s.away_shots_total,
        s.away_shots_on_target_count,
        s.away_possession
    FROM league_phase_stats s
    JOIN matches m ON m.match_id = s.match_id
    JOIN teams at ON at.team_id = m.away_team_id
)
SELECT
    team_name,
    COUNT(*) AS matches,
    SUM(goals) AS goals,
    SUM(shots) AS shots,
    SUM(shots_on_target) AS shots_on_target,
    ROUND(100.0 * SUM(goals) / NULLIF(SUM(shots), 0), 1) AS goal_conversion_pct,
    ROUND(100.0 * SUM(shots_on_target) / NULLIF(SUM(shots), 0), 1) AS shot_accuracy_pct,
    ROUND(AVG(possession), 1) AS avg_possession,
    RANK() OVER (ORDER BY 1.0 * SUM(goals) / NULLIF(SUM(shots), 0) DESC) AS conversion_rank
FROM team_stats
GROUP BY team_name
ORDER BY conversion_rank, goals DESC;

-- Does the team with more possession win more often?
WITH possession_result AS (
    SELECT
        CASE
            WHEN s.home_possession > s.away_possession THEN 'Home had more possession'
            WHEN s.home_possession < s.away_possession THEN 'Away had more possession'
            ELSE 'Equal possession'
        END AS possession_side,
        m.match_outcome
    FROM league_phase_stats s
    JOIN matches m ON m.match_id = s.match_id
)
SELECT
    possession_side,
    match_outcome,
    COUNT(*) AS matches
FROM possession_result
GROUP BY possession_side, match_outcome
ORDER BY possession_side, match_outcome;
