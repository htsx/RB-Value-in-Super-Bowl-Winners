# sb_rosters_to_sqlite.py
import os
import requests
from bs4 import BeautifulSoup
import sqlite3

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

# Absolute path to avoid issues
db_path = os.path.join("database", "sb_teams.db")

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop old sb_rosters table if it exists
cursor.execute("DROP TABLE IF EXISTS sb_rosters;")
conn.commit()

# Create sb_rosters table
cursor.execute("""
CREATE TABLE sb_rosters (
    No INTEGER,
    Team TEXT,
    Player TEXT,
    FOREIGN KEY (No) REFERENCES sb_winners(No)
)
""")
conn.commit()

# Scrape the roster page
url = "http://www.allcompetitions.com/nfl_sbros.php"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to fetch page, status code:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Find all roster cells
roster_cells = soup.find_all("td", class_="roster")

insert_count = 0

for cell in roster_cells:
    # Year and team
    span = cell.find("span", class_="roswin")
    if not span:
        continue

    year_team_text = span.get_text().strip()  # e.g., "2026 SEATTLE SEAHAWKS: "
    if year_team_text.endswith(":"):
        year_team_text = year_team_text[:-1]

    parts = year_team_text.split(" ", 1)
    if len(parts) < 2:
        continue

    try:
        year = int(parts[0])
    except ValueError:
        continue
    team = parts[1].strip()

    # Convert year to Super Bowl number
    sb_no = year - 1966

    # Player names (all text in the cell, remove span)
    player_text = cell.get_text().replace(span.get_text(), "").strip()
    # Remove Head Coach portion
    player_text = player_text.split("(Head Coach")[0].strip()

    # Split players by comma
    players = [p.strip() for p in player_text.split(",") if p.strip()]

    for player in players:
        cursor.execute("""
        INSERT INTO sb_rosters (No, Team, Player)
        VALUES (?, ?, ?)
        """, (sb_no, team, player))
        insert_count += 1

conn.commit()
conn.close()

print(f"Super Bowl winning rosters inserted successfully! Total players: {insert_count}")