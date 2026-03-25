import pandas as pd
import sqlite3

# Load CSV files
rb_df = pd.read_csv('csv_files/rb_top_5.csv')
team_df = pd.read_csv('csv_files/team_data.csv')

# Connect to SQLite database
conn = sqlite3.connect('database/rb_analysis.db')

# Load data into tables
rb_df.to_sql('rb_top_5', conn, if_exists='replace', index=False)
team_df.to_sql('team_data', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("Data loaded successfully into rb_analysis.db!")