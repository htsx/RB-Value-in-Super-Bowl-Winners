import sqlite3

#Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('database/rb_analysis.db')
cursor = conn.cursor()

#Create rb_top_5 table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rb_top_5 (
        player_name TEXT NOT NULL,
        team TEXT NOT NULL,
        season INTEGER NOT NULL,
        contract_average REAL,
        cap_hit REAL,
        cap_percentage REAL
    )
''')

#Create team_data table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS team_data (
        team TEXT NOT NULL,
        season INTEGER NOT NULL,
        wins INTEGER,
        losses INTEGER,
        tie INTEGER,
        made_playoffs INTEGER,
        playoff_result TEXT
    )
''')

conn.commit()
conn.close()

print("Tables created successfully!")