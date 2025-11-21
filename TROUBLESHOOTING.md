# Troubleshooting Guide

## 403 Forbidden Error

If you get a 403 error when accessing http://localhost:5000, try these solutions:

### Solution 1: Use 127.0.0.1 instead of localhost
```
http://127.0.0.1:5000
```

### Solution 2: Check if the server is running
Look for this message in the terminal:
```
* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
```

### Solution 3: Try a different port
If port 5000 is blocked or in use, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```
Then access: http://localhost:8080

### Solution 4: Check firewall settings
On macOS, you may need to allow Python to accept incoming connections:
- Go to System Preferences → Security & Privacy → Firewall
- Click "Firewall Options"
- Ensure Python is allowed

### Solution 5: Restart the application
1. Stop the server (Ctrl+C)
2. Restart with: `./run.sh` or `python app.py`

## Other Common Issues

### "Module not found" errors
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### CSV file not found
Check that `config.py` has the correct path:
```python
SPREADSHEET_PATH = "sourceData/Wordler Skins Sandbox - Scores.csv"
```

### Port already in use
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process (replace PID with actual process ID)
kill -9 PID
```

## Testing Without Browser

You can test if the server is working using curl:
```bash
curl http://localhost:5000
```

If this works but the browser doesn't, it's likely a browser-specific issue.

## Getting Help

If none of these solutions work, check:
1. Terminal output for error messages
2. Browser console (F12) for JavaScript errors
3. Try a different browser