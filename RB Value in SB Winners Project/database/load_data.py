import pandas as pd
import sqlite3
 
#Load Excel sheets
rb_df = pd.read_excel('rb_analysis.xlsx', sheet_name='rb_top_5')
team_df = pd.read_excel('rb_analysis.xlsx', sheet_name='team_data')
 
#Convert made_playoffs from yes/no to 1/0
team_df['made_playoffs'] = team_df['made_playoffs'].str.lower().map({'yes': 1, 'no': 0})
 
#Connect to SQLite database
conn = sqlite3.connect('rb_analysis.db')
 
#Load data into tables
rb_df.to_sql('rb_top_5', conn, if_exists='replace', index=False)
team_df.to_sql('team_data', conn, if_exists='replace', index=False)
 
conn.commit()
conn.close()
 
print("Data loaded successfully into rb_analysis.db!")