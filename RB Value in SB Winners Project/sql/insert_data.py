import sqlite3

conn = sqlite3.connect('rb_analysis.db')
cursor = conn.cursor()

# -----------------------------------------------
# INSERT PLAYERS
# Format: (player_name, team, year, cap_hit, contract_average, cap_percentage)
# -----------------------------------------------
players_data = [
    ('Saquon Barkley', 'PHI', 2024, 12800000, 12800000, 7.2),
    ('Derrick Henry', 'BAL', 2024, 11000000, 11000000, 6.1),
    # Add more rows here as you collect data...
]

cursor.executemany('''
    INSERT INTO players (player_name, team, year, cap_hit, contract_average, cap_percentage)
    VALUES (?, ?, ?, ?, ?, ?)
''', players_data)

# -----------------------------------------------
# INSERT TEAM OUTCOMES
# Format: (team, year, wins, losses, made_playoffs, playoff_result)
# made_playoffs: 1 = yes, 0 = no
# playoff_result options: 'missed', 'wild card loss', 'divisional loss', 
#                         'conference loss', 'super bowl loss', 'super bowl win'
# -----------------------------------------------
outcomes_data = [
    ('PHI', 2024, 14, 3, 1, 'super bowl win'),
    ('BAL', 2024, 12, 5, 1, 'divisional loss'),
    # Add more rows here as you collect data...
]

cursor.executemany('''
    INSERT INTO team_outcomes (team, year, wins, losses, made_playoffs, playoff_result)
    VALUES (?, ?, ?, ?, ?, ?)
''', outcomes_data)

conn.commit()
conn.close()

print("Data inserted successfully!")