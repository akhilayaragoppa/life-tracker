# Deployment Guide - Life Tracker

Deploy your Life Tracker system for free and access it from anywhere. Updates are automatic via git push.

## Prerequisites

1. **GitHub Account** - For code hosting and auto-deployment
2. **Supabase Account** - Already have this (your database)
3. **Vercel Account** - Free, for frontend hosting
4. **Render Account** - Free, for backend hosting

---

## Step 1: Push Code to GitHub

```bash
cd /Users/akhila.yaragoppa/Documents/Misc/life_tracker

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Life Tracker system"

# Create a new repo on GitHub (github.com/new), then:
git remote add origin https://github.com/YOUR_USERNAME/life-tracker.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (Free)

### 2a. Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (easiest)

### 2b. Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect your `life-tracker` repository
3. Configure:
   - **Name:** `life-tracker-backend`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** **Free**

### 2c. Add Environment Variables
In Render dashboard, go to your service → Environment:

```
LLM_PROVIDER=google
GOOGLE_API_KEY=your_google_api_key_here
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here
```

Get these from:
- Google API Key: https://aistudio.google.com/apikey
- Supabase: Your dashboard → Settings → API

Click **"Save Changes"** - it will auto-deploy!

### 2d. Get Your Backend URL
After deployment completes (2-3 minutes), you'll get a URL like:
```
https://life-tracker-backend.onrender.com
```

**Important:** Free tier sleeps after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

---

## Step 3: Deploy Frontend to Vercel (Free)

### 3a. Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub

### 3b. Deploy Frontend
1. Click **"Add New Project"**
2. Import your `life-tracker` repository
3. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `frontend`
   - **Build Command:** (leave empty)
   - **Output Directory:** `.` (current directory)
4. Click **"Deploy"**

### 3c. Update Frontend API URLs
After deployment, you'll get a URL like:
```
https://life-tracker.vercel.app
```

Now update your frontend to use the deployed backend:

**Edit these files in your repo:**

`frontend/index.html` - Line 127:
```javascript
const API_BASE = 'https://life-tracker-backend.onrender.com';
```

`frontend/views.js` - Line 1:
```javascript
const API_BASE = 'https://life-tracker-backend.onrender.com';
```

Commit and push:
```bash
git add frontend/index.html frontend/views.js
git commit -m "Update API URLs for production"
git push
```

Vercel will **auto-deploy** in ~30 seconds! 🎉

---

## Step 4: Mobile Setup (PWA)

### iPhone/iPad:
1. Open `https://life-tracker.vercel.app` in Safari
2. Tap Share → **"Add to Home Screen"**
3. Name it "Life Tracker"
4. Tap Add

### Android:
1. Open `https://life-tracker.vercel.app` in Chrome
2. Tap menu (⋮) → **"Add to Home Screen"**
3. Tap Add

Now you have a native-feeling app icon!

---

## Future Updates - Super Simple

Just commit and push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Added new feature"
git push

# Both Vercel and Render auto-deploy within 1-2 minutes!
```

**No manual deployment needed** - it's all automatic from git push.

---

## Alternative Free Options

### Backend Alternatives:
1. **Railway** - Similar to Render, $5 free credit/month
2. **Fly.io** - Free tier, good for always-on apps
3. **Google Cloud Run** - Free tier, scales to zero
4. **Heroku** - No longer free 😢

### Frontend Alternatives:
1. **Netlify** - Same as Vercel, equally good
2. **Cloudflare Pages** - Fast global CDN
3. **GitHub Pages** - Free but requires build step

---

## Costs

**Current setup: $0/month**

- Frontend (Vercel): Free forever for personal projects
- Backend (Render): Free tier
  - 750 hours/month (enough for one service 24/7)
  - Sleeps after 15 min inactivity (wakes on request)
- Database (Supabase): Free tier
  - 500 MB database
  - 50,000 monthly active users
  - Unlimited API requests
- LLM (Google Gemini): Free tier
  - 1500 requests/day
  - More than enough for personal use

**If you need always-on backend (no sleep):**
- Render paid: $7/month
- Railway: $5/month
- Fly.io: ~$2-5/month

---

## Monitoring & Debugging

### Backend Logs (Render):
1. Go to Render dashboard
2. Click your service
3. **"Logs"** tab shows real-time output

### Frontend Errors:
Open browser DevTools (F12) → Console tab

### Backend Health Check:
Visit: `https://life-tracker-backend.onrender.com/`
Should return: `{"message": "Life Tracker API", "status": "running"}`

---

## Security Considerations

### Current Setup:
- ✅ Environment variables stored securely in Render
- ✅ HTTPS everywhere (Vercel + Render both auto-provision SSL)
- ✅ API keys never exposed to frontend
- ⚠️ No authentication yet (anyone with URL can use it)

### Adding Authentication (Optional):
1. Add a simple API key to backend
2. Store it in frontend environment variable
3. Or: Integrate Supabase Auth for user accounts

For personal use, security through obscurity (long random URL) is usually enough.

---

## Troubleshooting

**"Backend not responding"**
- Free tier sleeps after 15min inactivity
- First request wakes it (takes ~30 seconds)
- Solution: Use paid tier ($7/month) or accept the wait

**"CORS error"**
- Check backend CORS settings in `main.py`
- Should have `allow_origins=["*"]` for development
- For production, set to your Vercel URL

**"Supabase connection failed"**
- Double-check environment variables in Render
- Make sure URL is correct (no postgres. prefix)
- Check Supabase dashboard for connection limits

---

## Next Steps

1. **Deploy** following steps above
2. **Bookmark** your Vercel URL
3. **Add to home screen** on phone
4. **Start using!**

Your Life Tracker is now accessible from anywhere, updates automatically, and costs $0/month. 🚀
