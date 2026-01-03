"""
Round Management Module
Handles creation, persistence, and retrieval of competition rounds
"""

import os
import json
from datetime import datetime
from pathlib import Path
import config

# Directory to store round configurations
ROUNDS_DIR = "rounds"

def ensure_rounds_directory():
    """Create rounds directory if it doesn't exist"""
    Path(ROUNDS_DIR).mkdir(exist_ok=True)

def parse_round_date(date_str):
    """
    Parse date in format YYMMDD (e.g., 251205 for Dec 5, 2025)
    Returns datetime object
    """
    try:
        return datetime.strptime(date_str, "%y%m%d")
    except ValueError:
        raise ValueError("Date must be in format YYMMDD (e.g., 251205 for Dec 5, 2025)")

def format_round_date(dt):
    """Format datetime as YYMMDD"""
    return dt.strftime("%y%m%d")

def get_round_config_path(round_date_str):
    """Get path to round configuration file"""
    ensure_rounds_directory()
    return os.path.join(ROUNDS_DIR, round_date_str, "config.py")

def get_round_data_path(round_date_str):
    """Get path to round data directory"""
    ensure_rounds_directory()
    return os.path.join(ROUNDS_DIR, round_date_str)

def create_new_round(round_date_str, competitors=None, teams=None, competitions=None):
    """
    Create a new round with specified configuration
    
    Args:
        round_date_str: Date in YYMMDD format
        competitors: List of dicts with 'name' and 'team' keys (defaults to config.PLAYERS)
        teams: List of team names (defaults to config.TEAMS)
        competitions: List of competition names (defaults to ['skins'])
    
    Returns:
        dict: Round configuration
    """
    # Validate date format
    round_date = parse_round_date(round_date_str)
    
    # Use defaults if not provided
    if competitors is None:
        competitors = config.PLAYERS.copy()
    if teams is None:
        teams = config.TEAMS.copy()
    if competitions is None:
        competitions = ['skins']
    
    # Create round directory
    round_dir = get_round_data_path(round_date_str)
    Path(round_dir).mkdir(parents=True, exist_ok=True)
    
    # Create round configuration
    round_config = {
        'round_date': round_date_str,
        'round_date_formatted': round_date.strftime("%B %d, %Y"),
        'start_date': round_date.isoformat(),
        'competitors': competitors,
        'teams': teams,
        'competitions': competitions,
        'created_at': datetime.now().isoformat(),
        'status': 'active'
    }
    
    # Save configuration as Python file
    config_path = get_round_config_path(round_date_str)
    with open(config_path, 'w') as f:
        f.write(f"# Round Configuration - Started {round_config['round_date_formatted']}\n")
        f.write(f"# Created: {round_config['created_at']}\n\n")
        f.write(f"ROUND_DATE = '{round_date_str}'\n")
        f.write(f"START_DATE = '{round_config['start_date']}'\n")
        f.write(f"STATUS = '{round_config['status']}'\n\n")
        f.write(f"COMPETITORS = {repr(competitors)}\n\n")
        f.write(f"TEAMS = {repr(teams)}\n\n")
        f.write(f"COMPETITIONS = {repr(competitions)}\n\n")
        f.write(f"# Default score when a player doesn't have an entry\n")
        f.write(f"DEFAULT_SCORE = {config.DEFAULT_SCORE}\n")
    
    # Also save as JSON for easy reading
    json_path = os.path.join(round_dir, "config.json")
    with open(json_path, 'w') as f:
        json.dump(round_config, f, indent=2)
    
    return round_config

def get_all_rounds():
    """
    Get list of all rounds
    
    Returns:
        list: List of round configurations sorted by date (newest first)
    """
    ensure_rounds_directory()
    rounds = []
    
    if not os.path.exists(ROUNDS_DIR):
        return rounds
    
    for round_dir in os.listdir(ROUNDS_DIR):
        round_path = os.path.join(ROUNDS_DIR, round_dir)
        if os.path.isdir(round_path):
            json_path = os.path.join(round_path, "config.json")
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    round_config = json.load(f)
                    rounds.append(round_config)
    
    # Sort by date (newest first)
    rounds.sort(key=lambda x: x['round_date'], reverse=True)
    return rounds

def get_round_config(round_date_str):
    """
    Get configuration for a specific round
    
    Args:
        round_date_str: Date in YYMMDD format
    
    Returns:
        dict: Round configuration or None if not found
    """
    json_path = os.path.join(ROUNDS_DIR, round_date_str, "config.json")
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    return None

def get_active_rounds():
    """Get list of active rounds"""
    all_rounds = get_all_rounds()
    return [r for r in all_rounds if r.get('status') == 'active']

def update_round_config(round_date_str, **updates):
    """
    Update round configuration
    
    Args:
        round_date_str: Date in YYMMDD format
        **updates: Fields to update (competitors, teams, competitions, status)
    """
    round_config = get_round_config(round_date_str)
    if not round_config:
        raise ValueError(f"Round {round_date_str} not found")
    
    # Update fields
    for key, value in updates.items():
        if key in ['competitors', 'teams', 'competitions', 'status']:
            round_config[key] = value
    
    round_config['updated_at'] = datetime.now().isoformat()
    
    # Save updated configuration
    round_dir = get_round_data_path(round_date_str)
    
    # Update Python config file
    config_path = get_round_config_path(round_date_str)
    with open(config_path, 'w') as f:
        f.write(f"# Round Configuration - Started {round_config['round_date_formatted']}\n")
        f.write(f"# Updated: {round_config['updated_at']}\n\n")
        f.write(f"ROUND_DATE = '{round_date_str}'\n")
        f.write(f"START_DATE = '{round_config['start_date']}'\n")
        f.write(f"STATUS = '{round_config['status']}'\n\n")
        f.write(f"COMPETITORS = {repr(round_config['competitors'])}\n\n")
        f.write(f"TEAMS = {repr(round_config['teams'])}\n\n")
        f.write(f"COMPETITIONS = {repr(round_config['competitions'])}\n\n")
        f.write(f"# Default score when a player doesn't have an entry\n")
        f.write(f"DEFAULT_SCORE = {config.DEFAULT_SCORE}\n")
    
    # Update JSON file
    json_path = os.path.join(round_dir, "config.json")
    with open(json_path, 'w') as f:
        json.dump(round_config, f, indent=2)
    
    return round_config

# Made with Bob
