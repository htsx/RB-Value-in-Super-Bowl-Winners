import pandas as pd
import sqlite3

conn = sqlite3.connect('database/rb_analysis.db')

# -----------------------------------------------
# QUERY 1: Join both tables to see RB salary vs team outcome
# -----------------------------------------------
print("=== RB SALARY VS TEAM OUTCOME ===")
query1 = '''
    SELECT 
        r.player_name,
        r.team,
        r.season,
        r.contract_average,
        r.cap_hit,
        r.cap_percentage,
        t.wins,
        t.losses,
        t.made_playoffs,
        t.playoff_result
    FROM rb_top_5 r
    JOIN team_data t ON r.team = t.team AND r.season = t.season
    ORDER BY r.season DESC
'''
df = pd.read_sql(query1, conn)
print(df.to_string())

# -----------------------------------------------
# QUERY 2: Playoff outcome distribution for top paid RB teams
# -----------------------------------------------
print("\n=== PLAYOFF OUTCOME DISTRIBUTION ===")
query2 = '''
    SELECT 
        COALESCE(t.playoff_result, 'Missed Playoffs') as outcome,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM team_data), 2) as percentage
    FROM team_data t
    GROUP BY outcome
    ORDER BY count DESC
'''
print(pd.read_sql(query2, conn).to_string())

# -----------------------------------------------
# QUERY 3: Average wins by playoff result
# -----------------------------------------------
print("\n=== AVERAGE WINS BY PLAYOFF RESULT ===")
query3 = '''
    SELECT 
        COALESCE(playoff_result, 'Missed Playoffs') as outcome,
        ROUND(AVG(wins), 1) as avg_wins,
        COUNT(*) as count
    FROM team_data
    GROUP BY outcome
    ORDER BY avg_wins DESC
'''
print(pd.read_sql(query3, conn).to_string())

# -----------------------------------------------
# QUERY 4: How often did top paid RB teams win the Super Bowl?
# -----------------------------------------------
print("\n=== SUPER BOWL WINS BY TOP PAID RB TEAMS ===")
query4 = '''
    SELECT 
        COUNT(*) as total_team_seasons,
        SUM(CASE WHEN playoff_result = 'Super Bowl Win' THEN 1 ELSE 0 END) as super_bowl_wins,
        ROUND(SUM(CASE WHEN playoff_result = 'Super Bowl Win' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_percentage
    FROM team_data
'''
print(pd.read_sql(query4, conn).to_string())

# -----------------------------------------------
# QUERY 5: Average cap hit by playoff result
# -----------------------------------------------
print("\n=== AVERAGE CAP HIT BY PLAYOFF RESULT ===")
query5 = '''
    SELECT 
        COALESCE(t.playoff_result, 'Missed Playoffs') as outcome,
        ROUND(AVG(r.cap_hit), 2) as avg_cap_hit,
        ROUND(AVG(r.cap_percentage), 2) as avg_cap_percentage
    FROM rb_top_5 r
    JOIN team_data t ON r.team = t.team AND r.season = t.season
    GROUP BY outcome
    ORDER BY avg_cap_hit DESC
'''
print(pd.read_sql(query5, conn).to_string())

conn.close()