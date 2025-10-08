# SQL Database Creation Script
import sqlite3

conn = sqlite3.connect('data/nwsl_fantasy.db')
cursor = conn.cursor()

# Player Table (Player ID, Name, Team ID, Position, etc.)
player_table_sql = """
CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    name TEXT,
    team_id TEXT,
    position TEXT
);
"""

# Team Table (Team ID, Team Name, etc.)
team_table_sql = """
CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    team_name TEXT
);
"""

# Player - Team Association Table
player_team_table_sql = """
CREATE TABLE IF NOT EXISTS player_team (
    player_id TEXT,
    team_id TEXT,
    PRIMARY KEY (player_id, team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
"""

# Match Table (Match ID, Date, Home Team, Away Team, Score)
match_table_sql = """
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    match_date TEXT,
    home_team_id TEXT, 
    away_team_id TEXT,
    home_score INTEGER,
    away_score INTEGER,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
);  
"""

# Player Match Stats Table (Match ID, Player ID, stats..., match points)
player_match_stats_table_sql = """
CREATE TABLE IF NOT EXISTS player_match_stats (
    match_id TEXT,
    player_id TEXT,
    minutes INTEGER,
    goals INTEGER,
    assists INTEGER,
    shots INTEGER,
    shots_on_target INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    fouls_committed INTEGER,
    fouls_suffered INTEGER,
    saves INTEGER,
    clean_sheet INTEGER,
    match_points INTEGER,
    PRIMARY KEY (match_id, player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);  
"""

# User Table (User ID, Username, Password Hash)
user_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
"""

# Fantasy Team Table (User ID, Player IDs, Total Points)
fantasy_team_table_sql = """
CREATE TABLE IF NOT EXISTS fantasy_teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    FW1 TEXT,
    FW2 TEXT,
    FW3 TEXT,
    MF1 TEXT,
    MF2 TEXT,
    MF3 TEXT,
    MF4 TEXT,
    MF5 TEXT,
    DF1 TEXT,
    DF2 TEXT,
    DF3 TEXT,
    DF4 TEXT,
    DF5 TEXT,
    GK1 TEXT,
    GK2 TEXT,
    total_points INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (FW1) REFERENCES players(player_id),
    FOREIGN KEY (FW2) REFERENCES players(player_id),
    FOREIGN KEY (FW3) REFERENCES players(player_id),
    FOREIGN KEY (MF1) REFERENCES players(player_id),
    FOREIGN KEY (MF2) REFERENCES players(player_id),
    FOREIGN KEY (MF3) REFERENCES players(player_id),
    FOREIGN KEY (MF4) REFERENCES players(player_id),
    FOREIGN KEY (MF5) REFERENCES players(player_id),
    FOREIGN KEY (DF1) REFERENCES players(player_id),
    FOREIGN KEY (DF2) REFERENCES players(player_id),
    FOREIGN KEY (DF3) REFERENCES players(player_id),
    FOREIGN KEY (DF4) REFERENCES players(player_id),
    FOREIGN KEY (DF5) REFERENCES players(player_id),
    FOREIGN KEY (GK1) REFERENCES players(player_id),
    FOREIGN KEY (GK2) REFERENCES players(player_id)
);
"""

# Execute table creation statements
cursor.execute(player_table_sql)
cursor.execute(team_table_sql)
cursor.execute(player_team_table_sql)
cursor.execute(match_table_sql)
cursor.execute(player_match_stats_table_sql)
cursor.execute(user_table_sql)
cursor.execute(fantasy_team_table_sql)