# Are High-Paid Running Backs Worth It? A NFL Cap Analysis (2011 - 2025)

![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# Overview
- This project answers a highly debated question within the NFL analytics community. 
- In the modern NFL, salary cap management is the most important factor in a team's success, can make or break a NFL teams roster being contenders or failures. Since the cap space is obviously not unlimited, every single contract offered can take away the opportunity to upgrade needed positions. Since premium running backs can be offered gigantic contract offers that can eat up salary cap, it has created a debate if offering a running back a massive deal is worth it or could that money be spent elsewhere.
- This is a project designed to analyze the value of high paying running backs to a NFL team and if this investment results in playoff success.

# Motivation
- There has been a movement in the NFL community that has grown in recent years of an anti-running back movement. Essentially this is the idea that if you have the chance to save money by getting similar production from a top tier running back using a running back committee you go for it and use the money elsewhere to upgrade on other positions on the team.

- This data-driven approach adds value to the debate since nowadays sports teams and moves within the world of sports is being decided by analytics.

# Data sources
- Spotrac (https://www.spotrac.com/): the largest online sports database that provides detailed, up-to-date information on professional sports contracts, team payrolls, and salary caps
- Pro Football Reference (https://www.pro-football-reference.com/): a comprehensive online database for American football statistics, covering NFL, AFL, and historical data.
 
- All the data used in this project was manually collected.

## Why 2011-2025?
The 2011 CBA introduced the current rookie wage scale and standardized NFL contract structures, making salary data consistent and comparable across all seasons. This makes 2011 the most logical starting point for this type of analysis. Spotrac's reliable historical salary data also begins around this period.
 
# Project Structure
- `csv_files/` — raw data files used to populate the database
- `database/` — SQLite database and all Python scripts for setup, loading, and querying data
- `charts/` — generated chart images from the analysis
- `visuals/` — script used to generate the charts
- `rb_analysis.ipynb` — Jupyter notebook containing the full analysis and findings
- `requirements.txt` — list of dependencies needed to run the project

# How to run

```markdown
## How to Run
1. Clone the repository
2. Create and activate a virtual environment:
```
python -m venv venv
```
Windows:
```
venv\Scripts\activate
```
Mac/Linux:
```
source venv/bin/activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Create the database:
```
python database/create_db.py
```
5. Load the data:
```
python database/load_data.py
```
6. Generate charts:
```
python visuals/visuals.py
```
7. Open the notebook:
```
jupyter lab
```
Then open `rb_analysis.ipynb` and run **Kernel → Restart & Run All**
```

# Key Findings
- 63.81% missed playoffs.
- Teams that missed the playoffs had a higher average RB cap hit than teams that made the Super Bowl.
- Since 2011, the 2024 Eagles are the only team in this dataset to have won the Super Bowl ( 0.95%).
-  Super Bowl winning teams paid their RB an average of $3,256,230 (2.43% of cap); nearly half of what top paid RB teams committed.

# Tools Used
- Python — data analysis and visualization
- Pandas — data manipulation and querying
- SQLite — relational database storage
- Matplotlib / Seaborn — data visualization
- Jupyter Lab — interactive notebook presentation
