import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('database/rb_analysis.db')
cursor = conn.cursor()

# Create players table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        team TEXT NOT NULL,
        year INTEGER NOT NULL,
        cap_hit REAL,
        contract_average REAL,
        cap_percentage REAL
    )
''')

# Create team_outcomes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS team_outcomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team TEXT NOT NULL,
        year INTEGER NOT NULL,
        wins INTEGER,
        losses INTEGER,
        made_playoffs INTEGER,  -- 1 for yes, 0 for no
        playoff_result TEXT     -- 'missed', 'wild card loss', 'divisional loss', 
                                -- 'conference loss', 'super bowl loss', 'super bowl win'
    )
''')

conn.commit()
conn.close()

print("Tables created successfully!")