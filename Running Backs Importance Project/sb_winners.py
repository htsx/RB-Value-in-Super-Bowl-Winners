import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.espn.com/nfl/superbowl/history/winners"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
html = response.text

soup = BeautifulSoup(html, "html.parser")

# Find the main table — ESPN uses a <table> for the content
table = soup.find("table")

# Collect rows
rows = table.find_all("tr")

# Prepare CSV
with open("data/sb_winners.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Write header
    writer.writerow(["No.", "Date", "Site", "Winner", "Loser", "Winner Score", "Loser Score"])

    for row in rows[1:]:  # skip header
        cols = [td.get_text(strip=True) for td in row.find_all("td")]

        if len(cols) >= 4:
            no, date, site, result = cols[:4]

            # Parse result ("TeamA 35, TeamB 10")
            try:
                parts = result.split(",")
                winner_part, loser_part = parts[0].strip(), parts[1].strip()

                winner_team, winner_score = winner_part.rsplit(" ", 1)
                loser_team, loser_score = loser_part.rsplit(" ", 1)
            except Exception as e:
                # Fallback if parse fails
                winner_team = loser_team = ""
                winner_score = loser_score = ""

            writer.writerow([
                no,
                date,
                site,
                winner_team,
                loser_team,
                winner_score,
                loser_score
            ])

print("Saved espn_superbowl_winners.csv!")