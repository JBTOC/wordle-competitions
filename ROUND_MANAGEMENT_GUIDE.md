# Round Management System - User Guide

## Overview

The Round Management System allows you to create, manage, and track multiple competition rounds with customizable competitors, teams, and competitions.

## Features

### 1. Start New Round
- Create a new round with a specific start date
- Customize competitors and team assignments
- Select which competitions to include
- All settings are persisted in round-specific configuration files

### 2. View All Rounds
- See all active and completed rounds
- Quick access to round details
- Filter by status (active/completed)

### 3. Round Details
- View complete round configuration
- See all competitors and their teams
- Access competitions for that round
- Edit or close the round

### 4. Edit Round
- Modify competitors during the round
- Add or remove competitors
- Change team assignments
- Add new competitions to ongoing rounds

## How to Use

### Starting a New Round

1. **Click "Start New Round"** on the home page
2. **Enter the round date** in format YYMMDD (e.g., 251205 for Dec 5, 2025)
3. **Configure competitors:**
   - Default competitors from config.py are pre-filled
   - Add new competitors with the "+ Add Competitor" button
   - Remove competitors with the "Remove" button
   - Assign each competitor to a team
4. **Select competitions:**
   - Check which competitions to include (default: Skins)
   - More competitions will be added in future updates
5. **Click "Start Round"**

### Viewing Rounds

1. **Click "View All Rounds"** on the home page
2. You'll see:
   - **Active Rounds** section (rounds in progress)
   - **All Rounds** section (complete history)
3. **Click on any round** to see details

### Managing a Round

From the round details page, you can:

- **View competitors** and their team assignments
- **Access competitions** by clicking on competition cards
- **Edit configuration** with the "Edit Round Configuration" button
- **Close the round** when it's complete (changes status to "completed")

### Editing a Round

1. Go to the round details page
2. Click "Edit Round Configuration"
3. Make your changes:
   - Add/remove competitors
   - Change team assignments
   - Add/remove competitions
4. Click "Save Changes"

## Data Storage

### Round Configuration Files

Each round is stored in its own directory under `rounds/`:

```
rounds/
├── 251205/                    # Round started Dec 5, 2025
│   ├── config.py             # Python configuration file
│   └── config.json           # JSON configuration (for easy reading)
├── 251212/                    # Round started Dec 12, 2025
│   ├── config.py
│   └── config.json
└── ...
```

### Configuration Contents

Each round configuration includes:
- **Round date** (YYMMDD format)
- **Start date** (ISO format)
- **Status** (active/completed)
- **Competitors** (list with names and teams)
- **Teams** (list of team names)
- **Competitions** (list of competition types)
- **Default score** (inherited from main config)

### Example Round Config (config.py)

```python
# Round Configuration - Started December 05, 2025
# Created: 2025-12-05T10:30:00

ROUND_DATE = '251205'
START_DATE = '2025-12-05T00:00:00'
STATUS = 'active'

COMPETITORS = [
    {'name': 'Lorcan', 'team': 'Dub'},
    {'name': 'Keith', 'team': 'Dub'},
    {'name': 'Gerry', 'team': 'Dub'},
    {'name': 'Johnny', 'team': 'Dub'},
    {'name': 'Paul', 'team': 'Mucker'},
    {'name': 'Raffe', 'team': 'Mucker'},
    {'name': 'JOCO', 'team': 'Mucker'},
    {'name': 'Giller', 'team': 'Mucker'},
]

TEAMS = ['Dub', 'Mucker']

COMPETITIONS = ['skins']

# Default score when a player doesn't have an entry
DEFAULT_SCORE = 8
```

## Multiple Rounds

- You can have **multiple active rounds** at the same time
- Each round is completely independent
- Round configurations don't affect each other
- The main `config.py` provides defaults for new rounds

## Date Format

**Important:** Round dates use YYMMDD format:
- `251205` = December 5, 2025
- `260115` = January 15, 2026
- `251231` = December 31, 2025

This format:
- ✅ Sorts chronologically
- ✅ Creates unique directory names
- ✅ Is compact and readable
- ✅ Works well for file systems

## API Endpoints

For programmatic access:

- `GET /api/rounds` - Get all rounds as JSON
- `GET /api/round/<round_date>` - Get specific round as JSON

Example:
```bash
curl http://localhost:8080/api/rounds
curl http://localhost:8080/api/round/251205
```

## Tips

1. **Start dates carefully** - The round date becomes the directory name
2. **Keep competitors consistent** - Use the same names across rounds for easier tracking
3. **Close completed rounds** - Mark rounds as completed when done
4. **Backup round data** - The `rounds/` directory contains all your data
5. **Edit anytime** - You can modify round configuration at any point

## Future Enhancements

Coming soon:
- More competition types (not just Skins)
- Round statistics and summaries
- Export round data
- Round templates
- Bulk competitor management
- Team-based competitions

## Troubleshooting

### "Round not found" error
- Check the round date format (YYMMDD)
- Verify the round exists in the `rounds/` directory

### Can't edit round
- Make sure you're accessing the correct round date
- Check file permissions on the `rounds/` directory

### Changes not saving
- Ensure the `rounds/` directory is writable
- Check for error messages in the browser console

## Technical Details

### Architecture

The round management system is built as a separate module:

- **`round_manager.py`** - Core round management logic
- **`round_routes.py`** - Flask blueprint for web routes
- **`templates/`** - HTML templates for UI
- **`rounds/`** - Data storage directory

### Integration

The system integrates with the existing app through:
- Flask blueprints (no modification to existing routes)
- Separate templates (existing templates unchanged)
- Independent data storage (doesn't affect existing CSV data)

This modular design means:
- ✅ Existing functionality remains unchanged
- ✅ Easy to extend with new features
- ✅ Can be disabled without breaking the app
- ✅ Clean separation of concerns