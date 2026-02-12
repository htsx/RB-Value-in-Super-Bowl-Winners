import pandas as pd
import requests

url = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions#results"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

tables = pd.read_html(response.text)

# Find the table that contains the correct column
df = None
for table in tables:
    if "Winning team" in table.columns:
        df = table
        break

if df is not None:
    # Save to CSV
    df.to_csv("super_bowl_winners.csv", index=False)
    # Print the table
    print(df)
    print("Success!")
else:
    print("No table found with column 'Winning team'.")
