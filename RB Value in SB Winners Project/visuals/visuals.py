import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('database/rb_analysis.db')

# Set style
sns.set_theme(style="darkgrid")

#Chart 1: Playoff Outcome Distribution (Bar Chart)
query1 = '''
    SELECT 
        COALESCE(playoff_result, 'Missed Playoffs') as outcome,
        COUNT(*) as count
    FROM team_data
    GROUP BY outcome
    ORDER BY count DESC
'''
df1 = pd.read_sql(query1, conn)

plt.figure(figsize=(10, 6))
colors = ['#d9534f' if x == 'Missed Playoffs' else '#5bc0de' if x == 'Super Bowl Win' else '#f0ad4e' for x in df1['outcome']]
bars = plt.bar(df1['outcome'], df1['count'], color=colors)
plt.title('Playoff Outcomes for Teams with a Top-Paid RB (2011-2025)', fontsize=14, fontweight='bold')
plt.xlabel('Outcome')
plt.ylabel('Number of Teams')
plt.xticks(rotation=15)
for bar, count in zip(bars, df1['count']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, str(count), ha='center', fontsize=11)
plt.tight_layout()
plt.savefig('charts/chart1_outcome_distribution.png', dpi=150)
plt.close()
print("Chart 1 saved")

#Chart 2: Average Wins by Playoff Result (Horizontal Bar)
query2 = '''
    SELECT 
        COALESCE(playoff_result, 'Missed Playoffs') as outcome,
        ROUND(AVG(wins), 1) as avg_wins
    FROM team_data
    GROUP BY outcome
    ORDER BY avg_wins ASC
'''
df2 = pd.read_sql(query2, conn)

plt.figure(figsize=(10, 6))
bars = plt.barh(df2['outcome'], df2['avg_wins'], color='#5b9bd5')
plt.title('Average Wins by Playoff Outcome (Top-Paid RB Teams)', fontsize=14, fontweight='bold')
plt.xlabel('Average Wins')
for bar, val in zip(bars, df2['avg_wins']):
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, str(val), va='center', fontsize=11)
plt.tight_layout()
plt.savefig('charts/chart2_avg_wins.png', dpi=150)
plt.close()
print("Chart 2 saved")

#Chart 3: Cap Hit vs Wins (Scatter Plot)
query3 = '''
    SELECT 
        r.cap_hit,
        r.cap_percentage,
        t.wins,
        COALESCE(t.playoff_result, 'Missed Playoffs') as outcome
    FROM rb_top_5 r
    JOIN team_data t ON r.team = t.team AND r.season = t.season
    WHERE r.cap_hit IS NOT NULL
'''
df3 = pd.read_sql(query3, conn)

plt.figure(figsize=(10, 6))
outcome_colors = {
    'Missed Playoffs': '#d9534f',
    'Wild Card': '#f0ad4e',
    'Divisional': '#f7c04a',
    'Conference Championship': '#5bc0de',
    'Super Bowl Loss': '#5b9bd5',
    'Super Bowl Win': '#27ae60'
}
for outcome, group in df3.groupby('outcome'):
    plt.scatter(group['cap_hit'], group['wins'], label=outcome, color=outcome_colors.get(outcome, 'gray'), alpha=0.7, s=80)
plt.title('RB Cap Hit vs Team Wins (2011-2025)', fontsize=14, fontweight='bold')
plt.xlabel('RB Cap Hit ($)')
plt.ylabel('Team Wins')
plt.legend(title='Outcome', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('charts/chart3_caphit_vs_wins.png', dpi=150)
plt.close()
print("Chart 3 saved")

#Chart 4: Pie Chart - Overall Outcome Breakdown
plt.figure(figsize=(8, 8))
colors_pie = ['#d9534f', '#f0ad4e', '#f7c04a', '#5bc0de', '#5b9bd5', '#27ae60']
wedges, texts, autotexts = plt.pie(
    df1['count'],
    labels=df1['outcome'],
    autopct='%1.1f%%',
    colors=colors_pie,
    startangle=140
)
plt.title('Outcome Breakdown for Teams with a Top-Paid RB (2011-2025)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/chart4_pie_outcomes.png', dpi=150)
plt.close()
print("Chart 4 saved")

#Chart 5: Average Cap Percentage by Season (Line Chart)
query5 = '''
    SELECT 
        r.season,
        ROUND(AVG(r.cap_percentage), 2) as avg_cap_percentage,
        ROUND(AVG(t.wins), 1) as avg_wins
    FROM rb_top_5 r
    JOIN team_data t ON r.team = t.team AND r.season = t.season
    WHERE r.cap_percentage IS NOT NULL
    GROUP BY r.season
    ORDER BY r.season ASC
'''
df5 = pd.read_sql(query5, conn)

fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = '#5b9bd5'
ax1.set_xlabel('Season')
ax1.set_ylabel('Avg Cap Percentage (%)', color=color1)
ax1.plot(df5['season'], df5['avg_cap_percentage'], color=color1, marker='o', linewidth=2, label='Avg Cap %')
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = '#d9534f'
ax2.set_ylabel('Avg Wins', color=color2)
ax2.plot(df5['season'], df5['avg_wins'], color=color2, marker='s', linewidth=2, linestyle='--', label='Avg Wins')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('Avg RB Cap % vs Avg Team Wins Over Time (2011-2025)', fontsize=14, fontweight='bold')
fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
plt.xticks(df5['season'], rotation=45)
plt.tight_layout()
plt.savefig('charts/chart5_cap_pct_over_time.png', dpi=150)
plt.close()
print("Chart 5 saved")

#Chart 6: Super Bowl Winners vs Top Paid RB Teams Cap Hit Comparison
categories = ['Super Bowl Winners', 'Top Paid RB Teams']
avg_cap_hits = [3256230.60, 6868709.22]
colors = ['#27ae60', '#d9534f']

plt.figure(figsize=(8, 6))
bars = plt.bar(categories, avg_cap_hits, color=colors, width=0.4)
plt.title('Average RB Cap Hit: Super Bowl Winners vs Top Paid RB Teams (2011-2025)', fontsize=13, fontweight='bold')
plt.ylabel('Average Cap Hit ($)')
plt.ylim(0, 9000000)
for bar, val in zip(bars, avg_cap_hits):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100000, '${:,.0f}'.format(val), ha='center', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/chart6_sb_vs_toppaid.png', dpi=150)
plt.close()
print("Chart 6 saved")

conn.close()
print("\nAll charts saved to charts/ folder!")