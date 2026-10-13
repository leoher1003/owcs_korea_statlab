-- Data checks for TEAMFIGHT INFO. Every query must return zero rows; returned rows are the problems.
-- Each check starts with a "-- check: <name>" line (pipeline/tf_db.py splits on it).

-- check: teamfight map is not in MATCH INFO
SELECT t.tf_id, t.match_id FROM teamfights t ANTI JOIN match_info m USING (match_id);

-- check: winner is not one of the two teams
SELECT tf_id, match_id, team1, team2, winner FROM teamfights WHERE winner NOT IN (team1, team2);

-- check: a side does not have five distinct heroes
SELECT tf_id, side, count(*) AS heroes, count(DISTINCT hero) AS distinct_heroes
FROM tf_hero GROUP BY tf_id, side HAVING count(*) <> 5 OR count(DISTINCT hero) <> 5;

-- check: hero has no role (add it to HERO_ROLES in export_site_data.py)
SELECT DISTINCT hero FROM tf_hero ANTI JOIN hero_roles USING (hero);

-- check: a side is not 1 tank / 2 DPS / 2 support
SELECT tf_id, team, comp_key, roles FROM tf_side WHERE roles <> 'TDDSS';
