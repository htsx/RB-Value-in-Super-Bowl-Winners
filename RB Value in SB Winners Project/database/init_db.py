# init_db.py
import sqlite3
import os

DB_FILE = "sb_teams.db"

# Delete existing database file if it exists
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Deleted existing database {DB_FILE}")

# Connect to (or create) the database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 1️⃣ Table for Super Bowl winners
cursor.execute("""
CREATE TABLE sb_winners (
    No INTEGER,
    Date TEXT,
    Site TEXT,
    Winner TEXT,
    Loser TEXT,
    Winner_Score INTEGER,
    Loser_Score INTEGER
)
""")

# 2️⃣ Table for SB-winning rosters
cursor.execute("""
CREATE TABLE sb_rosters (
    SB_Season INTEGER,
    Team TEXT,
    Player TEXT
)
""")

# 3️⃣ Table for player salaries
cursor.execute("""
CREATE TABLE player_salaries (
    Player TEXT,
    Team TEXT,
    Season INTEGER,
    Salary REAL
)
""")

conn.commit()
conn.close()

print(f"Created new database {DB_FILE} with tables: sb_winners, sb_rosters, player_salaries")