"""
Wordle Competitions Web Application
Calculates and displays Skins competition results
"""

from flask import Flask, render_template
import csv
from datetime import datetime
from collections import defaultdict
import config

app = Flask(__name__)
app.secret_key = 'wordle-competitions-secret-key-change-in-production'

# Import and register the rounds blueprint
from round_routes import rounds_bp
app.register_blueprint(rounds_bp)


def parse_date(date_str):
    """Convert date string like 'May-15' to a datetime object (assuming current year)"""
    # Add year 2024 for parsing (you can adjust this logic as needed)
    try:
        return datetime.strptime(f"{date_str}-2024", "%b-%d-%Y")
    except ValueError:
        # Handle different formats if needed
        return None


def load_scores():
    """Load scores from CSV file and organize by rounds"""
    rounds = []
    current_round = None
    
    with open(config.SPREADSHEET_PATH, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Skip first two rows (teams and player names)
        # Row 1: Teams
        # Row 2: Headers (Date, Hole, Player names...)
        player_names = [name.strip() for name in rows[1][2:]]  # Skip Date and Hole columns
        
        for row in rows[2:]:  # Start from row 3 (index 2)
            if not row or not row[0]:  # Skip empty rows
                continue
                
            date_str = row[0].strip()
            hole_num = int(row[1].strip())
            scores = [int(score.strip()) if score.strip() else config.DEFAULT_SCORE 
                     for score in row[2:]]
            
            # If hole is 1, start a new round
            if hole_num == 1:
                if current_round:  # Save previous round
                    rounds.append(current_round)
                current_round = {
                    'holes': [],
                    'start_date': None,
                    'end_date': None
                }
            
            # Add hole to current round
            if current_round is not None:
                hole_data = {
                    'date': date_str,
                    'date_obj': parse_date(date_str),
                    'hole_num': hole_num,
                    'scores': dict(zip(player_names, scores))
                }
                current_round['holes'].append(hole_data)
                
                # Update round dates
                if current_round['start_date'] is None:
                    current_round['start_date'] = date_str
                current_round['end_date'] = date_str
        
        # Don't forget the last round
        if current_round and current_round['holes']:
            rounds.append(current_round)
    
    return rounds, player_names


def calculate_skins(round_data, player_names):
    """
    Calculate skins for a round.
    Returns a dictionary with player names as keys and skin counts as values.
    """
    skins = {player: 0 for player in player_names}
    points_pool = 0  # Accumulated points when no one wins
    
    for hole in round_data['holes']:
        scores = hole['scores']
        points_pool += 1  # Each hole adds 1 point to the pool
        
        # Find the minimum score for this hole
        min_score = min(scores.values())
        
        # Find all players with the minimum score
        winners = [player for player, score in scores.items() if score == min_score]
        
        # If exactly one player has the lowest score, they win the skin
        if len(winners) == 1:
            winner = winners[0]
            skins[winner] += points_pool
            points_pool = 0  # Reset the pool after a skin is won
    
    return skins


@app.route('/')
def index():
    """Main page showing all competitions"""
    return render_template('index.html')


@app.route('/skins')
def skins():
    """Skins competition page"""
    rounds, player_names = load_scores()
    
    # Calculate skins for each round
    rounds_with_skins = []
    for i, round_data in enumerate(rounds, 1):
        skins_results = calculate_skins(round_data, player_names)
        rounds_with_skins.append({
            'round_num': i,
            'start_date': round_data['start_date'],
            'end_date': round_data['end_date'],
            'skins': skins_results,
            'total_holes': len(round_data['holes'])
        })
    
    return render_template('skins.html', 
                         rounds=rounds_with_skins, 
                         players=player_names)


if __name__ == '__main__':
    # First, let's print the rounds information
    print("\n=== ROUNDS ANALYSIS ===\n")
    rounds, player_names = load_scores()
    
    for i, round_data in enumerate(rounds, 1):
        print(f"Round {i}:")
        print(f"  Start Date: {round_data['start_date']}")
        print(f"  End Date: {round_data['end_date']}")
        print(f"  Number of Holes: {len(round_data['holes'])}")
        print()
    
    print(f"\nTotal Rounds Found: {len(rounds)}")
    print(f"Players: {', '.join(player_names)}")
    print("\n" + "="*50 + "\n")
    
    # Start the web server
    # host='0.0.0.0' allows access from any network interface
    # Using port 8080 instead of 5000
    app.run(debug=True, host='0.0.0.0', port=8080)

# Made with Bob
