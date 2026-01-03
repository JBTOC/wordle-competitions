"""
Round Management Routes
Separate module for handling round-related web routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import round_manager
import config

# Create blueprint
rounds_bp = Blueprint('rounds', __name__)

@rounds_bp.route('/start_round', methods=['GET', 'POST'])
def start_round():
    """Handle starting a new round"""
    if request.method == 'POST':
        try:
            # Get form data
            round_date = request.form.get('round_date')
            
            # Parse competitors from form
            competitors = []
            competitor_names = request.form.getlist('competitor_name[]')
            competitor_teams = request.form.getlist('competitor_team[]')
            
            for name, team in zip(competitor_names, competitor_teams):
                if name.strip():  # Only add non-empty names
                    competitors.append({
                        'name': name.strip(),
                        'team': team.strip()
                    })
            
            # Get selected competitions
            competitions = request.form.getlist('competitions[]')
            if not competitions:
                competitions = ['skins']  # Default
            
            # Get unique teams
            teams = list(set(comp['team'] for comp in competitors))
            
            # Create the round
            round_config = round_manager.create_new_round(
                round_date,
                competitors=competitors,
                teams=teams,
                competitions=competitions
            )
            
            flash(f"Round started successfully for {round_config['round_date_formatted']}!", 'success')
            return redirect(url_for('rounds.show_round', round_date=round_date))
            
        except ValueError as e:
            flash(f"Error: {str(e)}", 'error')
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", 'error')
    
    # GET request - show form
    # Get default values from config
    default_competitors = config.PLAYERS
    default_teams = config.TEAMS
    available_competitions = ['skins']  # Will expand in future
    
    return render_template('start_round.html',
                         default_competitors=default_competitors,
                         default_teams=default_teams,
                         available_competitions=available_competitions)

@rounds_bp.route('/rounds')
def list_rounds():
    """Show all rounds"""
    rounds = round_manager.get_all_rounds()
    active_rounds = round_manager.get_active_rounds()
    
    return render_template('rounds_list.html',
                         rounds=rounds,
                         active_rounds=active_rounds)

@rounds_bp.route('/round/<round_date>')
def show_round(round_date):
    """Show details for a specific round"""
    round_config = round_manager.get_round_config(round_date)
    
    if not round_config:
        flash(f"Round {round_date} not found", 'error')
        return redirect(url_for('rounds.list_rounds'))
    
    return render_template('show_round.html',
                         round_config=round_config)

@rounds_bp.route('/round/<round_date>/edit', methods=['GET', 'POST'])
def edit_round(round_date):
    """Edit round configuration"""
    round_config = round_manager.get_round_config(round_date)
    
    if not round_config:
        flash(f"Round {round_date} not found", 'error')
        return redirect(url_for('rounds.list_rounds'))
    
    if request.method == 'POST':
        try:
            # Parse updated competitors
            competitors = []
            competitor_names = request.form.getlist('competitor_name[]')
            competitor_teams = request.form.getlist('competitor_team[]')
            
            for name, team in zip(competitor_names, competitor_teams):
                if name.strip():
                    competitors.append({
                        'name': name.strip(),
                        'team': team.strip()
                    })
            
            # Get updated competitions
            competitions = request.form.getlist('competitions[]')
            if not competitions:
                competitions = ['skins']
            
            # Get unique teams
            teams = list(set(comp['team'] for comp in competitors))
            
            # Update the round
            round_manager.update_round_config(
                round_date,
                competitors=competitors,
                teams=teams,
                competitions=competitions
            )
            
            flash("Round updated successfully!", 'success')
            return redirect(url_for('rounds.show_round', round_date=round_date))
            
        except Exception as e:
            flash(f"Error updating round: {str(e)}", 'error')
    
    # GET request - show edit form
    available_competitions = ['skins']
    
    return render_template('edit_round.html',
                         round_config=round_config,
                         available_competitions=available_competitions)

@rounds_bp.route('/round/<round_date>/close', methods=['POST'])
def close_round(round_date):
    """Close/complete a round"""
    try:
        round_manager.update_round_config(round_date, status='completed')
        flash("Round closed successfully!", 'success')
    except Exception as e:
        flash(f"Error closing round: {str(e)}", 'error')
    
    return redirect(url_for('rounds.show_round', round_date=round_date))

@rounds_bp.route('/api/rounds')
def api_rounds():
    """API endpoint to get all rounds as JSON"""
    rounds = round_manager.get_all_rounds()
    return jsonify(rounds)

@rounds_bp.route('/api/round/<round_date>')
def api_round(round_date):
    """API endpoint to get specific round as JSON"""
    round_config = round_manager.get_round_config(round_date)
    if round_config:
        return jsonify(round_config)
    return jsonify({'error': 'Round not found'}), 404

# Made with Bob
