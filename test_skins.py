"""
Test script to verify skins calculation
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
        
        player_names = [name.strip() for name in rows[1][2:]]
        
        for row in rows[2:]:
            if not row or not row[0]:
                continue
                
            date_str = row[0].strip()
            hole_num = int(row[1].strip())
            scores = [int(score.strip()) if score.strip() else config.DEFAULT_SCORE 
                     for score in row[2:]]
            
            if hole_num == 1:
                if current_round:
                    rounds.append(current_round)
                current_round = {
                    'holes': [],
                    'start_date': None,
                    'end_date': None
                }
            
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
        
        if current_round and current_round['holes']:
            rounds.append(current_round)
    
    return rounds, player_names


def calculate_skins(round_data, player_names):
    """Calculate skins for a round"""
    skins = {player: 0 for player in player_names}
    points_pool = 0
    
    print(f"\n  Hole-by-hole breakdown:")
    print(f"  {'Hole':<6} {'Date':<10} {'Scores':<50} {'Winner':<15} {'Points'}")
    print(f"  {'-'*100}")
    
    for hole in round_data['holes']:
        scores = hole['scores']
        points_pool += 1
        
        min_score = min(scores.values())
        winners = [player for player, score in scores.items() if score == min_score]
        
        # Format scores for display
        scores_str = ', '.join([f"{p[:3]}:{s}" for p, s in scores.items()])
        
        if len(winners) == 1:
            winner = winners[0]
            skins[winner] += points_pool
            print(f"  {hole['hole_num']:<6} {hole['date']:<10} {scores_str:<50} {winner:<15} +{points_pool}")
            points_pool = 0
        else:
            winners_str = ', '.join([w[:3] for w in winners])
            print(f"  {hole['hole_num']:<6} {hole['date']:<10} {scores_str:<50} Tie ({winners_str})  Carry")
    
    if points_pool > 0:
        print(f"\n  Note: {points_pool} point(s) carried over (round ended before being won)")
    
    return skins


if __name__ == '__main__':
    print("\n" + "="*100)
    print("SKINS COMPETITION - DETAILED CALCULATION")
    print("="*100)
    
    rounds, player_names = load_scores()
    
    for i, round_data in enumerate(rounds, 1):
        print(f"\n{'='*100}")
        print(f"Round {i}: {round_data['start_date']} to {round_data['end_date']}")
        print(f"{'='*100}")
        
        skins_results = calculate_skins(round_data, player_names)
        
        print(f"\n  Final Skins Count:")
        for player in player_names:
            print(f"    {player:<10}: {skins_results[player]} skins")
        
        max_skins = max(skins_results.values())
        if max_skins > 0:
            winners = [p for p in player_names if skins_results[p] == max_skins]
            print(f"\n  Round Winner(s): {', '.join(winners)} with {max_skins} skins")
    
    print("\n" + "="*100 + "\n")

# Made with Bob
