# Deployment Guide - Village Problem Portal

Deploy your portal live on **Render** (free) with automatic updates from GitHub.

## Prerequisites

✅ GitHub account (you have this)
✅ Render account (free signup)

## Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create new repository: `village-problem-portal` (or any name)
3. Choose **Public** or **Private**
4. Click **Create repository**

### Step 2: Initialize Git & Push Code

In your terminal:

```bash
cd /Users/abhishekupadhyay/my_python_project

# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Village Problem Portal"

# Add remote (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. **Sign up for Render:**
   - Go to [render.com](https://render.com)
   - Click "Get Started" → Sign up with GitHub
   - Authorize Render to access your repositories

2. **Create New Service:**
   - Dashboard → Click "+" or "New+"
   - Select **Web Service**
   - Connect your `village-problem-portal` repository
   - Click **Connect**

3. **Configure Service:**
   - **Name:** `village-portal` (or custom)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 2 -b 0.0.0.0:$PORT "app:create_app()"`
   - **Plan:** Free
   - Click **Create Web Service**

4. **Wait for Deployment:**
   - Render will build and deploy automatically
   - Takes 2-5 minutes
   - You'll get a public URL: `https://village-portal-xxxxx.onrender.com`

### Step 4: Add Custom Domain (Optional)

1. In Render dashboard → Your service → Settings
2. Scroll to **Custom Domains**
3. Enter your domain (e.g., `portal.myvillage.com`)
4. Follow DNS instructions to point your domain to Render

## Automatic Updates

After initial setup, every time you:
```bash
git push origin main
```

Render will **automatically redeploy** your app! 🚀

## How It Works

- **Procfile** - Tells Render how to run your app
- **render.yaml** - Deployment configuration
- **requirements.txt** - Python dependencies
- **gunicorn** - Production server (instead of Flask dev server)

## Troubleshooting

### Deployment Failed?
1. Check Render logs: Dashboard → Your service → Logs
2. Common issues:
   - Missing `requirements.txt`
   - Wrong start command
   - Missing Procfile

### App crashes on Render?
- View logs to see error
- Check that `main.py` uses `port` from environment:
  ```python
  port = int(os.environ.get('PORT', 8000))
  app.run(host='0.0.0.0', port=port)
  ```

### Database Issues?
- Render creates fresh database on each deploy
- Add persistent volume (paid feature) if you need data retention
- For MVP, it's fine to start fresh

## Getting Your Live URL

After deployment on Render:
```
🌐 Live Portal: https://village-portal-xxxxx.onrender.com
📊 Admin Dashboard: https://village-portal-xxxxx.onrender.com/admin
```

Share these links with villagers! ✅

## Free vs Paid

**Free Tier (includes):**
- 1 web service
- Auto-pauses after 15 minutes of inactivity
- Auto-wakes up on request (takes 30 seconds)
- HTTPS certificate
- Basic monitoring

**Paid Tier Benefits:**
- Always running (no auto-pause)
- Better performance
- More resources
- Custom domains

For MVP with villages, free tier is perfect! 🎉

---

Need help? Check Render docs: [render.com/docs](https://render.com/docs)
