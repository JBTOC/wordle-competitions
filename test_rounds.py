"""
Test script to analyze rounds in the data
"""

import csv
from datetime import datetime
import config


def parse_date(date_str):
    """Convert date string like 'May-15' to a datetime object (assuming 2024)"""
    try:
        return datetime.strptime(f"{date_str}-2024", "%b-%d-%Y")
    except ValueError:
        return None


def load_scores():
    """Load scores from CSV file and organize by rounds"""
    rounds = []
    current_round = None
    
    with open(config.SPREADSHEET_PATH, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Skip first two rows (teams and player names)
        player_names = [name.strip() for name in rows[1][2:]]
        
        for row in rows[2:]:
            if not row or not row[0]:
                continue
                
            date_str = row[0].strip()
            hole_num = int(row[1].strip())
            scores = [int(score.strip()) if score.strip() else config.DEFAULT_SCORE 
                     for score in row[2:]]
            
            # If hole is 1, start a new round
            if hole_num == 1:
                if current_round:
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
                
                if current_round['start_date'] is None:
                    current_round['start_date'] = date_str
                current_round['end_date'] = date_str
        
        # Don't forget the last round
        if current_round and current_round['holes']:
            rounds.append(current_round)
    
    return rounds, player_names


if __name__ == '__main__':
    print("\n" + "="*60)
    print("WORDLE COMPETITIONS - ROUNDS ANALYSIS")
    print("="*60 + "\n")
    
    rounds, player_names = load_scores()
    
    print(f"Players: {', '.join(player_names)}")
    print(f"Total Rounds Found: {len(rounds)}\n")
    print("-"*60 + "\n")
    
    for i, round_data in enumerate(rounds, 1):
        print(f"Round {i}:")
        print(f"  Start Date: {round_data['start_date']}")
        print(f"  End Date:   {round_data['end_date']}")
        print(f"  Holes:      {len(round_data['holes'])}")
        
        # Show first and last hole numbers
        first_hole = round_data['holes'][0]['hole_num']
        last_hole = round_data['holes'][-1]['hole_num']
        print(f"  Hole Range: {first_hole} to {last_hole}")
        print()
    
    print("="*60)

# Made with Bob
