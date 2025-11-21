# Quick Deployment Guide - Get Your App Online in 10 Minutes!

## Easiest Method: Render.com (Recommended)

### Step 1: Prepare Your Code (2 minutes)

1. **Initialize Git** (if not already done):
   ```bash
   cd /Users/joc/Education/WordleWithBob
   git init
   git add .
   git commit -m "Initial commit - Wordle Competitions App"
   ```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Name it: `wordle-competitions`
   - Don't initialize with README (we already have files)
   - Click "Create repository"

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/wordle-competitions.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Render (5 minutes)

1. **Sign up at Render.com**:
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (easiest)

2. **Create New Web Service**:
   - Click "New +" button
   - Select "Web Service"
   - Click "Connect" next to your `wordle-competitions` repository
   - If you don't see it, click "Configure account" to grant access

3. **Configure the Service**:
   - **Name**: `wordle-competitions` (or any name you like)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

4. **Click "Create Web Service"**

5. **Wait for Deployment** (2-3 minutes):
   - Watch the logs as it builds
   - When you see "Your service is live 🎉", it's ready!

6. **Access Your App**:
   - Click the URL at the top (looks like: `https://wordle-competitions-xxxx.onrender.com`)
   - Share this URL with your friends!

### Step 3: Update Your App Later

Whenever you want to update the app:

```bash
# Make your changes to the code
git add .
git commit -m "Description of changes"
git push
```

Render will automatically detect the changes and redeploy! ✨

---

## Important Notes

### Free Tier Limitations:
- **Sleeps after 15 minutes** of inactivity
- Takes ~30 seconds to wake up on first visit
- Perfect for your use case (checking scores occasionally)

### Custom Domain (Optional):
- Free tier gives you: `your-app.onrender.com`
- Custom domain (like `wordle.yourname.com`) requires paid plan ($7/month)

### Keeping It Awake (Optional):
If you want to prevent sleeping, you can:
1. Use a service like UptimeRobot (free) to ping your app every 14 minutes
2. Or upgrade to paid plan ($7/month) for always-on

---

## Alternative: PythonAnywhere (No Sleep!)

If you don't want the sleep issue:

1. **Sign up**: https://www.pythonanywhere.com/registration/register/beginner/
2. **Upload files**: Use the Files tab
3. **Create Web App**: Web tab → Add new web app → Flask
4. **Configure**: Point to your app.py file
5. **Done!** Your app is at: `https://YOUR_USERNAME.pythonanywhere.com`

**Pros**: Always on, no sleep
**Cons**: Manual file uploads for updates (or use git)

---

## Troubleshooting

### "Build failed" on Render:
- Check that `requirements.txt` and `Procfile` exist
- Look at the build logs for specific errors

### "Application Error" after deployment:
- Check the logs in Render dashboard
- Ensure `config.py` and CSV file are in the repository

### Can't access the URL:
- Wait 2-3 minutes after deployment
- Check if build completed successfully
- Try accessing in incognito/private browser window

---

## Need Help?

Check the full `DEPLOYMENT.md` file for more hosting options and detailed instructions.

Your app will be accessible 24/7 from anywhere in the world! 🌍