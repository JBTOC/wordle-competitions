# Fix Git Remote Error

## Problem
You added the wrong remote URL and now get "error: remote origin already exists"

## Solution

### Step 1: Remove the incorrect remote
```bash
git remote remove origin
```

### Step 2: Add the correct remote (with YOUR actual username)
```bash
git remote add origin https://github.com/YOUR_ACTUAL_USERNAME/wordle-competitions.git
```

### Step 3: Verify it's correct
```bash
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_ACTUAL_USERNAME/wordle-competitions.git (fetch)
origin  https://github.com/YOUR_ACTUAL_USERNAME/wordle-competitions.git (push)
```

### Step 4: Push to GitHub
```bash
git push -u origin main
```

---

## Alternative: Update the existing remote

Instead of removing and re-adding, you can just update the URL:

```bash
git remote set-url origin https://github.com/YOUR_ACTUAL_USERNAME/wordle-competitions.git
```

Then verify:
```bash
git remote -v
```

And push:
```bash
git push -u origin main
```

---

## Complete Command Sequence

Here's the full sequence with the fix:

```bash
# Navigate to your project
cd /Users/joc/Education/WordleWithBob

# Remove the incorrect remote
git remote remove origin

# Add the correct remote (REPLACE YOUR_ACTUAL_USERNAME!)
git remote add origin https://github.com/YOUR_ACTUAL_USERNAME/wordle-competitions.git

# Verify it's correct
git remote -v

# Push to GitHub
git push -u origin main
```

---

## If You Get Authentication Errors

If you get asked for username/password and it fails:

### Option 1: Use Personal Access Token (Recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with 'repo' scope
3. Use the token as your password when prompted

### Option 2: Use SSH instead
```bash
# Remove HTTPS remote
git remote remove origin

# Add SSH remote (REPLACE YOUR_ACTUAL_USERNAME!)
git remote add origin git@github.com:YOUR_ACTUAL_USERNAME/wordle-competitions.git

# Push
git push -u origin main
```

---

## Quick Check Commands

```bash
# See current remotes
git remote -v

# See git status
git status

# See commit history
git log --oneline