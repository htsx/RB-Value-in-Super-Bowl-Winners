import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.5993.90 Safari/537.36"
}

def get_season_year(date_string):
    """Extract NFL season year from Super Bowl date."""
    year = int(re.search(r"\d{4}", date_string).group())
    return year - 1  # Super Bowl played the next calendar year

def build_wiki_url(season_year, team_name):
    """Build Wikipedia season URL from year and team name."""
    mapping = {
        "Green Bay": "Green Bay Packers",
        "New England": "New England Patriots",
        "San Francisco": "San Francisco 49ers",
        "Dallas": "Dallas Cowboys",
        "Miami": "Miami Dolphins",
        "Denver": "Denver Broncos",
        "Washington": "Washington Commanders",
        "Pittsburgh": "Pittsburgh Steelers",
        "Kansas City": "Kansas City Chiefs",
        "New York Giants": "New York Giants",
        "New York Jets": "New York Jets",
        "Los Angeles Rams": "Los Angeles Rams",
        "St. Louis Rams": "St. Louis Rams",
        "Baltimore": "Baltimore Ravens",
        "Oakland": "Oakland Raiders",
        "Los Angeles Raiders": "Oakland Raiders",
        "Tampa Bay": "Tampa Bay Buccaneers",
        "Philadelphia": "Philadelphia Eagles",
        "Seattle": "Seattle Seahawks",
        "Indianapolis": "Indianapolis Colts"
    }
    team_name = mapping.get(team_name, team_name)
    team_slug = team_name.replace(" ", "_")
    return f"https://en.wikipedia.org/wiki/{season_year}_{team_slug}_season"

def scrape_table_roster(html_text):
    """Try to extract roster from HTML tables."""
    try:
        tables = pd.read_html(html_text)
        for table in tables:
            if "Pos" in table.columns or "Position" in table.columns:
                return table
    except ValueError:
        pass
    return None

def scrape_list_roster(soup):
    """Extract roster from bullet lists if no table exists."""
    roster = []
    # Find h2/h3 headers containing 'Roster'
    headers = soup.find_all(['h2', 'h3'])
    for header in headers:
        if 'Roster' in header.text:
            # The roster list is often in the next <ul>
            ul = header.find_next('ul')
            if ul:
                for li in ul.find_all('li'):
                    roster.append({'Player': li.text.strip()})
                return pd.DataFrame(roster)
    return None

def scrape_roster(url):
    """Fetch roster from Wikipedia, table or list format."""
    print(f"Fetching {url}")
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
    except requests.HTTPError as e:
        print(f"HTTP error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    df = scrape_table_roster(r.text)
    if df is not None:
        return df

    # fallback to list-based roster
    df = scrape_list_roster(soup)
    if df is not None:
        return df

    print("No roster found")
    return None

def scrape_sb_rosters(csv_path, output_path="data/sb_winner_rosters.csv"):
    """Scrape all SB-winning rosters and save to CSV."""
    sb_df = pd.read_csv(csv_path)
    all_rosters = []

    for _, row in sb_df.iterrows():
        winner = row["Winner"].strip()
        season_year = get_season_year(row["Date"])
        url = build_wiki_url(season_year, winner)

        roster = scrape_roster(url)
        if roster is not None:
            roster["SB_Season"] = season_year
            roster["Team"] = winner
            all_rosters.append(roster)
        else:
            print(f"Skipped {winner} {season_year}: roster not found")

        time.sleep(1)  # polite delay

    if all_rosters:
        final = pd.concat(all_rosters, ignore_index=True)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final.to_csv(output_path, index=False)
        print(f"Saved {output_path}")
    else:
        print("No rosters scraped.")

# Run the scraper
scrape_sb_rosters("data/sb_winners_cleaned.csv")