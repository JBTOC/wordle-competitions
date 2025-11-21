# Deployment Guide - Free Hosting Options

This guide shows how to deploy your Wordle Competitions app to free hosting platforms so it's accessible 24/7 without running a local server.

## Option 1: Render.com (Recommended - Easiest)

Render offers free hosting for web apps with automatic deployments from GitHub.

### Steps:

1. **Create a GitHub repository** (if you haven't already)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/wordle-competitions.git
   git push -u origin main
   ```

2. **Sign up at [Render.com](https://render.com)** (free account)

3. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: wordle-competitions
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Plan**: Free

4. **Deploy** - Render will automatically deploy your app!

Your app will be available at: `https://wordle-competitions.onrender.com`

**Note**: Free tier sleeps after 15 minutes of inactivity, takes ~30 seconds to wake up.

---

## Option 2: PythonAnywhere (Good Alternative)

Free tier includes 1 web app with custom subdomain.

### Steps:

1. **Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)** (free account)

2. **Upload your files**
   - Use the Files tab to upload all project files
   - Or clone from GitHub

3. **Create a Web App**
   - Go to Web tab → "Add a new web app"
   - Choose Flask
   - Python 3.10

4. **Configure WSGI file** (edit the auto-generated file):
   ```python
   import sys
   path = '/home/YOUR_USERNAME/WordleWithBob'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Install requirements**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

6. **Reload** the web app

Your app will be at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Option 3: Railway.app (Modern & Fast)

Similar to Render, with generous free tier.

### Steps:

1. **Sign up at [Railway.app](https://railway.app)** with GitHub

2. **Create New Project** → "Deploy from GitHub repo"

3. **Select your repository**

4. **Railway auto-detects** Python and deploys automatically

Your app will be at: `https://YOUR_APP.up.railway.app`

---

## Option 4: Fly.io (Advanced)

Good for more control, requires Docker knowledge.

### Steps:

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Launch app**
   ```bash
   fly launch
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

---

## Required Files for Deployment

I've created these files for you:

### 1. `requirements.txt` ✓ (Already exists)
Lists Python dependencies

### 2. `Procfile` (for Render/Railway)
Tells the platform how to run your app

### 3. `runtime.txt` (optional)
Specifies Python version

### 4. `.gitignore`
Prevents uploading unnecessary files

---

## Updating Your Deployed App

After initial deployment, to update:

1. **Make changes locally**
2. **Commit and push to GitHub**
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. **Auto-deploys** on Render/Railway/Fly
4. **Manual reload** on PythonAnywhere

---

## Cost Comparison

| Platform | Free Tier | Custom Domain | Sleep/Limits |
|----------|-----------|---------------|--------------|
| **Render** | ✓ | ✓ (paid) | Sleeps after 15min |
| **PythonAnywhere** | ✓ | ✗ | Always on, limited CPU |
| **Railway** | ✓ ($5 credit/mo) | ✓ | 500 hours/month |
| **Fly.io** | ✓ | ✓ | 3 VMs free |

---

## Recommendation

**For your use case (Wordle competitions):**

1. **Best choice**: **Render.com** - Easiest setup, auto-deploys from GitHub
2. **Alternative**: **PythonAnywhere** - Always on, no sleep time
3. **If you know Docker**: **Fly.io** - Most flexible

All options are completely free for your app's needs!