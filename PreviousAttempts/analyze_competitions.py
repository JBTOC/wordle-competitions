"""
Script to analyze Wordle competitions and identify start/end dates
"""

import csv
from datetime import datetime
import config

def parse_date(date_str):
    """Parse date string in format 'May-15' or 'Jul-08' to a datetime object"""
    # Assuming current year or most recent year for the month
    current_year = 2024  # Adjust as needed
    try:
        date_obj = datetime.strptime(f"{date_str}-{current_year}", "%b-%d-%Y")
        return date_obj
    except ValueError:
        return None

def analyze_competitions():
    """Analyze the CSV file to identify all competitions with their start and end dates"""
    
    competitions = []
    current_competition = None
    
    with open(config.CSV_FILE_PATH, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        # Skip header rows and start from data
        for i in range(config.DATA_START_ROW, len(rows)):
            row = rows[i]
            
            if len(row) < 2:
                continue
                
            date_str = row[config.DATE_COLUMN]
            hole_str = row[config.HOLE_COLUMN]
            
            try:
                hole_num = int(hole_str)
            except (ValueError, IndexError):
                continue
            
            # When we encounter hole 1, it's the start of a new competition
            if hole_num == 1:
                # If there's a current competition, close it with the previous row's date
                if current_competition is not None:
                    # End date is the previous row
                    if i > config.DATA_START_ROW:
                        prev_row = rows[i - 1]
                        current_competition['end_date'] = prev_row[config.DATE_COLUMN]
                        current_competition['end_hole'] = int(prev_row[config.HOLE_COLUMN])
                    competitions.append(current_competition)
                
                # Start a new competition
                current_competition = {
                    'competition_num': len(competitions) + 1,
                    'start_date': date_str,
                    'start_hole': hole_num,
                    'end_date': None,
                    'end_hole': None
                }
            
            # Update the current competition's end date as we go
            if current_competition is not None:
                current_competition['end_date'] = date_str
                current_competition['end_hole'] = hole_num
        
        # Don't forget to add the last competition
        if current_competition is not None:
            competitions.append(current_competition)
    
    return competitions

def main():
    """Main function to display competition information"""
    print("=" * 80)
    print("WORDLE COMPETITIONS ANALYSIS")
    print("=" * 80)
    print(f"\nAnalyzing file: {config.CSV_FILE_PATH}")
    print(f"Expected holes per competition: {config.HOLES_PER_COMPETITION}")
    print(f"\nTeams: {', '.join(config.TEAMS.keys())}")
    print(f"Players: {', '.join(config.PLAYERS.keys())}")
    print("\n" + "=" * 80)
    
    competitions = analyze_competitions()
    
    print(f"\nFound {len(competitions)} competition(s):\n")
    
    for comp in competitions:
        holes_played = comp['end_hole'] - comp['start_hole'] + 1
        status = "✓ Complete" if holes_played == config.HOLES_PER_COMPETITION else f"⚠ Incomplete ({holes_played} holes)"
        
        print(f"Competition {comp['competition_num']}:")
        print(f"  Start Date: {comp['start_date']} (Hole {comp['start_hole']})")
        print(f"  End Date:   {comp['end_date']} (Hole {comp['end_hole']})")
        print(f"  Holes:      {holes_played} {status}")
        print()
    
    print("=" * 80)

if __name__ == "__main__":
    main()

# Made with Bob
