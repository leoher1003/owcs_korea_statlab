-- Teamfight / composition views. Base tables are loaded by pipeline/tf_db.py:
--   teamfights(tf_id, match_id, ord, team1, team2, winner)
--   tf_hero(tf_id, side, hero)            side = 1 or 2, five rows per side
--   hero_roles(hero, role, role_rank)     role T/D/S, role_rank 1/2/3
--   match_info(match_id, week, day, match_no, set_no, map, map_type, map_winner)

-- One row per teamfight per team, with an order-independent comp key (Tank, DPS, Support, then name).
CREATE OR REPLACE VIEW tf_side AS
SELECT t.tf_id, t.match_id, t.ord, s.side,
       CASE s.side WHEN 1 THEN t.team1 ELSE t.team2 END AS team,
       CASE s.side WHEN 1 THEN t.team2 ELSE t.team1 END AS opp_team,
       s.comp_key, s.roles,
       t.winner = CASE s.side WHEN 1 THEN t.team1 ELSE t.team2 END AS won
FROM teamfights t
JOIN (
    SELECT h.tf_id, h.side,
           string_agg(h.hero, ' / ' ORDER BY r.role_rank, h.hero) AS comp_key,
           string_agg(r.role, ''    ORDER BY r.role_rank, h.hero) AS roles
    FROM tf_hero h LEFT JOIN hero_roles r USING (hero)
    GROUP BY h.tf_id, h.side
) s ON s.tf_id = t.tf_id;

-- Each side paired with the opposing side's comp.
CREATE OR REPLACE VIEW tf_matchup AS
SELECT a.*, b.comp_key AS opp_comp, a.comp_key = b.comp_key AS is_mirror
FROM tf_side a JOIN tf_side b ON a.tf_id = b.tf_id AND a.side <> b.side;

-- Per-comp stats. Mirrors are excluded from W/L; fight_share = fights featuring the comp / all fights.
CREATE OR REPLACE VIEW comp_stats AS
WITH base AS (
    SELECT comp_key,
           count(*)                                         AS freq,
           count(*) FILTER (WHERE is_mirror) // 2           AS mirror,
           count(*) FILTER (WHERE NOT is_mirror AND won)     AS w,
           count(*) FILTER (WHERE NOT is_mirror AND NOT won) AS l,
           count(DISTINCT tf_id)                            AS fights
    FROM tf_matchup GROUP BY comp_key
), team_use AS (
    SELECT comp_key, team, count(*) AS uses,
           max(count(*)) OVER (PARTITION BY comp_key) AS top_uses
    FROM tf_side GROUP BY comp_key, team
), teams AS (
    SELECT comp_key,
           string_agg(team || ' (' || uses || ')', ', ' ORDER BY team) FILTER (WHERE uses = top_uses) AS favorite_team,
           string_agg(team || ' ' || uses, ', ' ORDER BY uses DESC, team)                            AS all_teams
    FROM team_use GROUP BY comp_key
)
SELECT b.comp_key,
       string_split(b.comp_key, ' / ')[1] AS tank,
       string_split(b.comp_key, ' / ')[2] AS dps1,
       string_split(b.comp_key, ' / ')[3] AS dps2,
       string_split(b.comp_key, ' / ')[4] AS support1,
       string_split(b.comp_key, ' / ')[5] AS support2,
       b.freq, b.mirror, b.w, b.l,
       CASE WHEN b.w + b.l > 0 THEN b.w / (b.w + b.l) END                AS win_rate,
       b.fights / (SELECT count(*) FROM teamfights)                       AS fight_share,
       t.favorite_team, t.all_teams
FROM base b JOIN teams t USING (comp_key);

-- Per-team teamfight record.
CREATE OR REPLACE VIEW team_tf_stats AS
SELECT team,
       count(*) FILTER (WHERE won)     AS w,
       count(*) FILTER (WHERE NOT won) AS l,
       count(*)                        AS n,
       avg(won::INT)                   AS win_rate,
       count(DISTINCT match_id)        AS maps,
       count(*) / count(DISTINCT match_id) AS fights_per_map
FROM tf_side GROUP BY team;
