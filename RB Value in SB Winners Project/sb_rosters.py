import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
import time
import os

# -----------------------------
# Load winners CSV
# -----------------------------
df = pd.read_csv("data/sb_winners_cleaned.csv")

# -----------------------------
# Normalize team names from CSV
# -----------------------------
CSV_TO_FULL_TEAM = {
    "Green Bay": "Green Bay Packers",
    "New England": "New England Patriots",
    "Kansas City": "Kansas City Chiefs",
    "Baltimore": "Baltimore Ravens",
    "Dallas": "Dallas Cowboys",
    "Miami": "Miami Dolphins",
    "Pittsburgh": "Pittsburgh Steelers",
    "Oakland": "Oakland Raiders",
    "San Francisco": "San Francisco 49ers",
    "Washington": "Washington Redskins",
    "Los Angeles Raiders": "Oakland Raiders",
    "St. Louis": "St. Louis Rams",
    "Philadelphia": "Philadelphia Eagles",
    "Seattle": "Seattle Seahawks",
    "Tampa Bay": "Tampa Bay Buccaneers",
    "Indianapolis": "Indianapolis Colts",
    "New York Giants": "New York Giants",
    "New York Jets": "New York Jets",
    "Arizona": "Arizona Cardinals",
    "Atlanta": "Atlanta Falcons",
    "Buffalo": "Buffalo Bills",
    "Carolina": "Carolina Panthers",
    "Chicago": "Chicago Bears",
    "Cincinnati": "Cincinnati Bengals",
    "Cleveland": "Cleveland Browns",
    "Denver": "Denver Broncos",
    "Detroit": "Detroit Lions",
    "Houston": "Houston Texans",
    "Jacksonville": "Jacksonville Jaguars",
    "Los Angeles Rams": "Los Angeles Rams",
    "Minnesota": "Minnesota Vikings",
}

# -----------------------------
# Team abbreviations (PFR format)
# -----------------------------
TEAM_ABBR = {
    "Arizona Cardinals": "crd",
    "Atlanta Falcons": "atl",
    "Baltimore Ravens": "rav",
    "Buffalo Bills": "buf",
    "Carolina Panthers": "car",
    "Chicago Bears": "chi",
    "Cincinnati Bengals": "cin",
    "Cleveland Browns": "cle",
    "Dallas Cowboys": "dal",
    "Denver Broncos": "den",
    "Detroit Lions": "det",
    "Green Bay Packers": "gnb",
    "Houston Texans": "htx",
    "Indianapolis Colts": "clt",
    "Jacksonville Jaguars": "jax",
    "Kansas City Chiefs": "kan",
    "Oakland Raiders": "rai",
    "Las Vegas Raiders": "rai",
    "Los Angeles Chargers": "sdg",
    "Los Angeles Rams": "ram",
    "St. Louis Rams": "ram",
    "Miami Dolphins": "mia",
    "Minnesota Vikings": "min",
    "New England Patriots": "nwe",
    "New Orleans Saints": "nor",
    "New York Giants": "nyg",
    "New York Jets": "nyj",
    "Philadelphia Eagles": "phi",
    "Pittsburgh Steelers": "pit",
    "San Francisco 49ers": "sfo",
    "Seattle Seahawks": "sea",
    "Tampa Bay Buccaneers": "tam",
    "Tennessee Titans": "oti",
    "Washington Commanders": "was",
    "Washington Redskins": "was",
}

BASE_URL = "https://www.pro-football-reference.com/teams/{abbr}/{year}_roster.htm"

# -----------------------------
# Create Cloudscraper instance
# -----------------------------
scraper = cloudscraper.create_scraper()

all_rosters = []

for _, row in df.iterrows():
    year = int(row["Year"])
    csv_team = row["Winner"].strip()

    # Normalize name
    full_team = CSV_TO_FULL_TEAM.get(csv_team, csv_team)
    abbr = TEAM_ABBR.get(full_team)

    if not abbr:
        print(f"⚠️ No abbreviation for {csv_team} → {full_team}")
        continue

    url = BASE_URL.format(abbr=abbr, year=year)
    print(f"> Fetching {url}")

    try:
        r = scraper.get(url)

        if r.status_code != 200:
            print(f"❌ Failed ({r.status_code})")
            continue

        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("table", id="roster")
        if not table:
            print("❌ No roster table found")
            continue

        headers = [th.text.strip() for th in table.find("thead").find_all("th")]
        rows = table.find("tbody").find_all("tr")

        for tr in rows:
            cols = [td.text.strip() for td in tr.find_all("td")]
            if not cols:
                continue

            entry = dict(zip(headers[1:], cols))
            entry["Team"] = full_team
            entry["Year"] = year
            all_rosters.append(entry)

        time.sleep(3)  # be respectful

    except Exception as e:
        print(f"❌ Error: {e}")

# -----------------------------
# Save output
# -----------------------------
output = pd.DataFrame(all_rosters)
output.to_csv("sb_winner_rosters.csv", index=False)
print(r.text[:500])
print("✅ Done! Saved to sb_winner_rosters.csv")