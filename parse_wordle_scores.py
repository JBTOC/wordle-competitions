#!/usr/bin/env python3
"""
Parse WhatsApp Wordle dump and generate CSV file with scores.
"""

import re
import csv
from datetime import datetime
from collections import OrderedDict

def parse_wordle_line(line):
    """
    Parse a line like: [03/04/2024, 11:17:40] Lorcan Kavanagh: Wordle 1,019 6/6
    Returns: (date, player_name, score) or None if not a valid Wordle line
    """
    # Pattern to match Wordle score lines
    pattern = r'\[(\d{2}/\d{2}/\d{4}), \d{2}:\d{2}:\d{2}\] ([^:]+): Wordle \d+[,\d]* ([X\d])/6'
    
    match = re.search(pattern, line)
    if match:
        date_str = match.group(1)  # DD/MM/YYYY
        player_name = match.group(2).strip()
        score = match.group(3)
        
        # Convert date to YYMMDD format
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        formatted_date = date_obj.strftime('%y%m%d')
        
        # Convert X to 7
        if score == 'X':
            score = '7'
        
        return (formatted_date, player_name, score)
    
    return None

def main():
    input_file = '/Users/joc/Education/WordleWithBob/sourceData/whatsappWordleDump.txt'
    output_file = '/Users/joc/Education/WordleWithBob/sourceData/Wordler Skins Parse Inputs - Scores.csv'
    
    # Dictionary to store scores: {date: {player: score}}
    scores_by_date = OrderedDict()
    
    # Set to track all unique players
    all_players = set()
    
    print("Parsing input file...")
    
    # Read and parse the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            result = parse_wordle_line(line)
            if result:
                date, player, score = result
                
                # Add player to set
                all_players.add(player)
                
                # Initialize date entry if not exists
                if date not in scores_by_date:
                    scores_by_date[date] = {}
                
                # Store score for this player on this date
                scores_by_date[date][player] = score
                
                print(f"Found: {date} - {player}: {score}")
    
    # Sort players alphabetically for consistent column order
    sorted_players = sorted(all_players)
    
    print(f"\nFound {len(scores_by_date)} dates and {len(sorted_players)} players")
    print(f"Players: {', '.join(sorted_players)}")
    
    # Create CSV file
    print(f"\nWriting to CSV: {output_file}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Row 1: Team names (placeholder for now - will be filled in later)
        # Row 2: Player names
        # Row 3+: Date, Hole, Scores
        
        writer = csv.writer(csvfile)
        
        # Row 1: Team names (empty for now - user will provide instructions later)
        team_row = ['Date', 'Hole'] + [''] * len(sorted_players)
        writer.writerow(team_row)
        
        # Row 2: Player names
        player_row = ['Date', 'Hole'] + sorted_players
        writer.writerow(player_row)
        
        # Rows 3+: Scores
        hole = 1
        for date in sorted(scores_by_date.keys()):
            row = [date, str(hole)]
            
            # Add score for each player (or empty if they didn't play)
            for player in sorted_players:
                score = scores_by_date[date].get(player, '')
                row.append(score)
            
            writer.writerow(row)
            
            # Increment hole number (reset to 1 after 18)
            hole = 1 if hole == 18 else hole + 1
    
    # Fill in missing scores with 8
    print("\nFilling missing scores with 8...")
    
    # Read the CSV back
    rows = []
    with open(output_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    # Update rows 3+ (index 2+) to fill empty scores with 8
    for i in range(2, len(rows)):
        for j in range(2, len(rows[i])):
            if rows[i][j] == '':
                rows[i][j] = '8'
    
    # Write back
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
    print(f"\nComplete! CSV file created with {len(rows) - 2} score rows")
    print(f"Output file: {output_file}")

if __name__ == '__main__':
    main()

# Made with Bob
