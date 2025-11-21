# Configuration file for Wordle Competitions

# Path to the CSV file containing scores
SPREADSHEET_PATH = "sourceData/Wordler Skins Sandbox - Scores.csv"

# Player configuration
# Each player has a name and team assignment
PLAYERS = [
    {"name": "Lorcan", "team": "Dub"},
    {"name": "Keith", "team": "Dub"},
    {"name": "Gerry", "team": "Dub"},
    {"name": "Johnny", "team": "Dub"},
    {"name": "Paul", "team": "Mucker"},
    {"name": "Raffe", "team": "Mucker"},
    {"name": "JOCO", "team": "Mucker"},
    {"name": "Giller", "team": "Mucker"},
]

# Teams configuration
TEAMS = ["Dub", "Mucker"]

# Default score when a player doesn't have an entry
DEFAULT_SCORE = 8

# Number of holes per round (typically)
HOLES_PER_ROUND = 18

# Made with Bob
