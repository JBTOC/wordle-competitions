# Wordle Competitions Web Application

A Python web application to track and display Wordle competition results, starting with the Skins competition.

## 🌐 Deploy Online (Free!)

Want to share this with your friends? Deploy it for free in 10 minutes!

**👉 See [DEPLOY_QUICK_START.md](DEPLOY_QUICK_START.md) for step-by-step instructions**

Your app will be accessible 24/7 from anywhere at a URL like: `https://wordle-competitions.onrender.com`

## Features

- **Skins Competition**: Golf-style skins game where players compete for accumulated points
- **Round-based Tracking**: Automatically identifies rounds (typically 18 holes each)
- **Configurable**: Easy-to-manage configuration file for players, teams, and data source
- **Web-based**: Access from any device with a browser
- **Free Hosting**: Deploy to Render, PythonAnywhere, or other free platforms

## Setup

1. **Quick Start (Recommended)**
   ```bash
   ./run.sh
   ```
   This script will automatically:
   - Activate/create virtual environment
   - Install dependencies
   - Start the web server

2. **Manual Setup**
   ```bash
   # Create and activate virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configuration**
   Edit `config.py` to customize:
   - Player names and team assignments
   - Path to the CSV data file
   - Default scores and round settings

## Running the Application

### Option 1: Using the startup script (Easiest)
```bash
./run.sh
```

### Option 2: Manual start
```bash
source .venv/bin/activate
python app.py
```

When you run the app, it will:
1. Print all rounds found in the data with their start and end dates
2. Start the web server on port 5000

**Access the web interface:** Open your browser and go to `http://localhost:5000`

## Testing

Run the test scripts to verify functionality:

```bash
# View rounds analysis
python test_rounds.py

# View detailed skins calculation
python test_skins.py
```

## Data Format

The CSV file should have:
- **Row 1**: Team names for each player
- **Row 2**: Headers (Date, Hole, Player names...)
- **Row 3+**: Daily scores (Date, Hole number, scores for each player)

### Round Identification
- A new round starts when Hole number is 1
- The previous round ends on the row before the next Hole 1
- Typically 18 holes per round

## Skins Competition Rules

1. Each hole is worth 1 point initially
2. If one player alone gets the lowest score, they win the "skin" and collect all accumulated points
3. If there's a tie for lowest score, no one wins and points carry over to the next hole
4. Missing scores default to 8
5. Points reset to 1 after each skin is won

## Configuration File (config.py)

The configuration file contains:
- `SPREADSHEET_PATH`: Path to your CSV file
- `PLAYERS`: List of player dictionaries with name and team
- `TEAMS`: List of team names
- `DEFAULT_SCORE`: Score assigned when a player has no entry (default: 8)
- `HOLES_PER_ROUND`: Typical number of holes per round (default: 18)

## Project Structure

```
WordleWithBob/
├── app.py                 # Main Flask application
├── config.py              # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   └── skins.html        # Skins competition results
└── sourceData/           # Data directory
    └── Wordler Skins Sandbox - Scores.csv
```

## Future Enhancements

- Additional competition types
- Team-based competitions
- Historical statistics
- Player performance charts