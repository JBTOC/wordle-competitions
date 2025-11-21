#!/bin/bash
# Startup script for Wordle Competitions Web App

echo "Starting Wordle Competitions Web Application..."
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠ No virtual environment found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install requirements if Flask is not installed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

echo ""
echo "Starting web server..."
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

# Made with Bob
