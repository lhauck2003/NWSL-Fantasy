def calculate_fantasy_points(player_stats: dict, position: str) -> int:
    """
    Example scoring function
    """
    points = 0
    points += int(player_stats.get("goals_summary", 0)) * 5
    points += int(player_stats.get("assists_summary", 0)) * 3
    points += int(player_stats.get("minutes_summary", 0)) // 30
    if position == "GK":
        points += int(player_stats.get("saves_summary", 0))
    return points
