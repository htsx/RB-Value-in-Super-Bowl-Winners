import pandas as pd
import sqlite3

conn = sqlite3.connect('database/rb_analysis.db')

#Q 1: Join both tables to see RB salary vs team outcome
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

#Q 2: Playoff outcome distribution for top paid RB teams
print("\n=== PLAYOFF OUTCOME DISTRIBUTION ===")
query2 = '''
    SELECT 
        playoff_result as outcome,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM team_data), 2) as percentage
    FROM team_data
    GROUP BY outcome
    ORDER BY count DESC
'''
print(pd.read_sql(query2, conn).to_string())

#Q 3: Average wins by playoff result
print("\n=== AVERAGE WINS BY PLAYOFF RESULT ===")
query3 = '''
    SELECT 
        playoff_result as outcome,
        ROUND(AVG(wins), 1) as avg_wins,
        COUNT(*) as count
    FROM team_data
    GROUP BY outcome
    ORDER BY avg_wins DESC
'''
print(pd.read_sql(query3, conn).to_string())

#Q 4: How often did top paid RB teams win the Super Bowl?
print("\n=== SUPER BOWL WINS BY TOP PAID RB TEAMS ===")
query4 = '''
    SELECT 
        COUNT(*) as total_team_seasons,
        SUM(CASE WHEN playoff_result = 'Super Bowl Win' THEN 1 ELSE 0 END) as super_bowl_wins,
        ROUND(SUM(CASE WHEN playoff_result = 'Super Bowl Win' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as win_percentage
    FROM team_data
'''
print(pd.read_sql(query4, conn).to_string())

#Q 5: Average cap hit by playoff result
print("\n=== AVERAGE CAP HIT BY PLAYOFF RESULT ===")
query5 = '''
    SELECT 
        t.playoff_result as outcome,
        ROUND(AVG(r.cap_hit), 2) as avg_cap_hit,
        ROUND(AVG(r.cap_percentage), 2) as avg_cap_percentage
    FROM rb_top_5 r
    JOIN team_data t ON r.team = t.team AND r.season = t.season
    GROUP BY outcome
    ORDER BY avg_cap_hit DESC
'''
print(pd.read_sql(query5, conn).to_string())

#Q 6: Average RB cap hit on Super Bowl winning teams
print("\n=== AVERAGE RB CAP HIT ON SUPER BOWL WINNING TEAMS ===")
query6 = '''
    SELECT 
        ROUND(AVG(cap_hit), 2) as avg_cap_hit,
        ROUND(AVG(cap_percentage), 2) as avg_cap_percentage
    FROM sb_winners_rb
'''
print(pd.read_sql(query6, conn).to_string())

#Q 7: SB winning teams RB cap % vs top paid RB teams cap %
print("\n=== SB WINNING TEAMS RB CAP % VS TOP PAID RB TEAMS CAP % ===")
query7 = '''
    SELECT 
        'Super Bowl Winners' as group_name,
        ROUND(AVG(cap_hit), 2) as avg_cap_hit,
        ROUND(AVG(cap_percentage), 2) as avg_cap_percentage
    FROM sb_winners_rb
    UNION ALL
    SELECT 
        'Top Paid RB Teams' as group_name,
        ROUND(AVG(cap_hit), 2) as avg_cap_hit,
        ROUND(AVG(cap_percentage), 2) as avg_cap_percentage
    FROM rb_top_5
'''
print(pd.read_sql(query7, conn).to_string())

conn.close()