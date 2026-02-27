# sb_winners_to_sqlite.py
import requests
from bs4 import BeautifulSoup
import sqlite3

# Database setup
conn = sqlite3.connect("database/sb_teams.db")  # creates the DB if it doesn't exist
cursor = conn.cursor()

# Create table for SB winners
cursor.execute("""
CREATE TABLE IF NOT EXISTS sb_winners (
    No INTEGER,
    Date TEXT,
    Site TEXT,
    Winner TEXT,
    Loser TEXT,
    Winner_Score INTEGER,
    Loser_Score INTEGER
)
""")
conn.commit()

# Clear table every time script runs
cursor.execute("DELETE FROM sb_winners;")
conn.commit()

# Scrape ESPN Super Bowl winners
url = "https://www.espn.com/nfl/superbowl/history/winners"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
html = response.text

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")
rows = table.find_all("tr")

for row in rows[1:]:  # skip table header
    cols = [td.get_text(strip=True) for td in row.find_all("td")]

    if len(cols) >= 4:
        no, date, site, result = cols[:4]

        # Parse result ("TeamA 35, TeamB 10")
        try:
            parts = result.split(",")
            winner_part, loser_part = parts[0].strip(), parts[1].strip()
            loser_part = parts[1].strip()
            winner_team, winner_score = winner_part.rsplit(" ", 1)
            loser_team, loser_score = loser_part.rsplit(" ", 1)
            winner_score = int(winner_score)
            loser_score = int(loser_score)
        except Exception as e:
            winner_team = loser_team = ""
            winner_score = loser_score = None

        # Insert into database
        cursor.execute("""
        INSERT INTO sb_winners (No, Date, Site, Winner, Loser, Winner_Score, Loser_Score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (no, date, site, winner_team, loser_team, winner_score, loser_score))

conn.commit()
conn.close()
print("Super Bowl winners inserted into sb_teams.db!")