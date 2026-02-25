import pandas as pd
from datetime import datetime

# Load the raw CSV
df = pd.read_csv("data/sb_winners.csv")

# Drop rows with missing critical data
df = df.dropna(subset=["Date", "Winner", "Loser"])

# Convert Date to Year
def extract_year(date_str):
    try:
        return datetime.strptime(date_str, "%b. %d, %Y").year
    except Exception:
        try:
            # fallback if month abbreviation has no dot
            return datetime.strptime(date_str, "%b %d, %Y").year
        except Exception:
            return None

df["Year"] = df["Date"].apply(extract_year)

# Drop rows where Year couldn't be parsed
df = df.dropna(subset=["Year"])
df["Year"] = df["Year"].astype(int)

# Convert scores to numeric
df["Winner Score"] = pd.to_numeric(df["Winner Score"], errors="coerce")
df["Loser Score"] = pd.to_numeric(df["Loser Score"], errors="coerce")

# Drop rows with missing scores
df = df.dropna(subset=["Winner Score", "Loser Score"])

# Reset index
df = df.reset_index(drop=True)

# Optional: reorder columns nicely
df = df[["No.", "Date", "Year", "Site", "Winner", "Loser", "Winner Score", "Loser Score"]]

# Save cleaned CSV
df.to_csv("data/sb_winners_cleaned.csv", index=False)

print("Saved cleaned sb_winners_cleaned.csv!")