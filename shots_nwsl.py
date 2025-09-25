import nwslpy

stats = nwslpy.load_player_match_stats("portland-thorns-fc-vs-kansas-city-current-2022-10-29")
players = nwslpy.load_players()

# Select the columns of interest
stats = stats[["shots_total"]]
# Join with information about the players
stats = stats.join(players)[["shots_total", "player_match_name"]]
# Find the players with the most shots
stats = stats.sort_values("shots_total", ascending=False)

print(stats.head(10))

