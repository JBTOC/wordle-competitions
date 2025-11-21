"""
Wordle Competition Configuration File
This file contains all the configuration settings for the Wordle competition scoring system.
"""

# Path to the CSV file containing the scores
CSV_FILE_PATH = "sourceData/Wordler Skins Sandbox - Scores.csv"

# Team definitions
TEAMS = {
    "Dub": {
        "name": "Dub",
        "players": ["Lorcan", "Keith", "Gerry", "Johnny"]
    },
    "Mucker": {
        "name": "Mucker",
        "players": ["Paul", "Raffe", "JOCO", "Giller"]
    }
}

# Player definitions with team assignments
PLAYERS = {
    "Lorcan": {
        "name": "Lorcan",
        "team": "Dub",
        "column_index": 2  # Column in CSV (0-based)
    },
    "Keith": {
        "name": "Keith",
        "team": "Dub",
        "column_index": 3
    },
    "Gerry": {
        "name": "Gerry",
        "team": "Dub",
        "column_index": 4
    },
    "Johnny": {
        "name": "Johnny",
        "team": "Dub",
        "column_index": 5
    },
    "Paul": {
        "name": "Paul",
        "team": "Mucker",
        "column_index": 6
    },
    "Raffe": {
        "name": "Raffe",
        "team": "Mucker",
        "column_index": 7
    },
    "JOCO": {
        "name": "JOCO",
        "team": "Mucker",
        "column_index": 8
    },
    "Giller": {
        "name": "Giller",
        "team": "Mucker",
        "column_index": 9
    }
}

# Competition settings
HOLES_PER_COMPETITION = 18

# CSV structure settings
HEADER_ROW_TEAMS = 0  # Row index for team names (0-based)
HEADER_ROW_PLAYERS = 1  # Row index for player names (0-based)
DATA_START_ROW = 2  # Row index where score data starts (0-based)
DATE_COLUMN = 0  # Column index for date
HOLE_COLUMN = 1  # Column index for hole number

# Made with Bob
