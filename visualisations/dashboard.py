import matplotlib.pyplot as plt
import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from dashboard_data import get_stadium_data, get_group_stats, get_team_data, get_player_data, get_goalscorers
from adjustText import adjust_text

# Load data
stadium_data = get_stadium_data()
group_stats_df = get_group_stats()
team_data_df = get_team_data()

# Safely load player data
players_list_df = get_player_data()
if players_list_df is None:
    players_list_df = pd.DataFrame()

# Safely load goalscorer data
goalscorers_df = get_goalscorers()
if goalscorers_df is None:
    goalscorers_df = pd.DataFrame()

# Set up subplots
fig = plt.figure(figsize=(18, 22))

# 1. Stadium Map with Labels
ax1 = fig.add_subplot(4, 2, 1, projection=ccrs.PlateCarree())
ax1.stock_img()
ax1.coastlines()
ax1.add_feature(cfeature.BORDERS)
ax1.set_extent([50.75, 52.0, 24.8, 26.1], crs=ccrs.PlateCarree())
texts = []
for idx, row in stadium_data.iterrows():
    ax1.plot(row['Lon'], row['Lat'], marker='o', color='red', transform=ccrs.PlateCarree())
    texts.append(ax1.text(row['Lon'] + 0.02, row['Lat'] + 0.02, row['Stadium'], fontsize=8, transform=ccrs.PlateCarree()))
adjust_text(texts, ax=ax1, arrowprops=dict(arrowstyle='-', color='gray'))
ax1.set_title("World Cup Stadiums - Qatar")

# 2. Goals vs Expected Goals
ax2 = fig.add_subplot(4, 2, 2)
x = group_stats_df.get("expected_goal_scored", pd.Series())
y = group_stats_df.get("goals_scored", pd.Series())
if not x.empty and not y.empty:
    ax2.scatter(x, y)
    ax2.plot([x.min(), x.max()], [x.min(), x.max()], 'r--')
    for i, team in enumerate(group_stats_df.get("team", [])):
        ax2.text(x.iloc[i], y.iloc[i], team, fontsize=7)
ax2.set_xlabel("Expected Goals")
ax2.set_ylabel("Actual Goals")
ax2.set_title("Goals vs Expected Goals")

# 3. Heatmap: xG Difference per Group
ax3 = fig.add_subplot(4, 2, 3)
pivot = group_stats_df.pivot(index='team', columns='group', values='exp_goal_difference')
sns.heatmap(pivot, annot=True, cmap='coolwarm', center=0, ax=ax3)
ax3.set_title("xG Difference by Group")

# 4. Age Distribution by Position
ax4 = fig.add_subplot(4, 2, 4)
if not players_list_df.empty and 'Pos' in players_list_df.columns:
    sns.boxplot(x='Pos', y='Age', data=players_list_df, ax=ax4)
else:
    ax4.text(0.5, 0.5, "Player data not available", ha='center', va='center')
ax4.set_title("Player Age by Position")

# 5. Vertical Bar Chart for Goalscorers with Country Hue
ax5 = fig.add_subplot(4, 2, 5)
if not goalscorers_df.empty and 'Player' in goalscorers_df.columns:
    goalscorers_sorted = goalscorers_df.sort_values("Goals", ascending=True)
    if 'Country' in goalscorers_sorted.columns:
        sns.barplot(data=goalscorers_sorted, y="Player", x="Goals", hue="Country", dodge=False, ax=ax5)
    else:
        sns.barplot(data=goalscorers_sorted, y="Player", x="Goals", ax=ax5)
    ax5.set_xlabel("Goals")
else:
    ax5.text(0.5, 0.5, "Goalscorer data not available", ha='center', va='center')
ax5.set_title("Top Goal Scorers by Country")

plt.tight_layout()
plt.show()
