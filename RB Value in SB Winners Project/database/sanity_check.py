import pandas as pd
import sqlite3

conn = sqlite3.connect('database/rb_analysis.db')

#Check total rows in each table
print("=== ROW COUNTS ===")
print("rb_top_5 rows:", pd.read_sql("SELECT COUNT(*) as count FROM rb_top_5", conn)['count'][0])
print("team_data rows:", pd.read_sql("SELECT COUNT(*) as count FROM team_data", conn)['count'][0])

#Preview first 5 rows of each table
print("\n=== RB_TOP_5 SAMPLE ===")
print(pd.read_sql("SELECT * FROM rb_top_5 LIMIT 5", conn).to_string())

print("\n=== TEAM_DATA SAMPLE ===")
print(pd.read_sql("SELECT * FROM team_data LIMIT 5", conn).to_string())

#Check seasons range
print("\n=== SEASONS RANGE ===")
print(pd.read_sql("SELECT MIN(season) as first_season, MAX(season) as last_season FROM rb_top_5", conn).to_string())

#Check for missing values in rb_top_5
print("\n=== MISSING VALUES IN RB_TOP_5 ===")
rb_df = pd.read_sql("SELECT * FROM rb_top_5", conn)
print(rb_df.isnull().sum())

#Check for missing values in team_data
print("\n=== MISSING VALUES IN TEAM_DATA ===")
team_df = pd.read_sql("SELECT * FROM team_data", conn)
print(team_df.isnull().sum())

#Check distinct playoff results
print("\n=== DISTINCT PLAYOFF RESULTS ===")
print(pd.read_sql("SELECT DISTINCT playoff_result FROM team_data", conn).to_string())

#Check how many teams per season
print("\n=== TEAMS PER SEASON IN RB_TOP_5 ===")
print(pd.read_sql("SELECT season, COUNT(*) as count FROM rb_top_5 GROUP BY season ORDER BY season", conn).to_string())

conn.close()