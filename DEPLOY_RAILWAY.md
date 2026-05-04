# Deploy Backend to Railway (Easier Alternative to Render)

Railway is more reliable than Render free tier and respects Python version settings.

## Why Railway?

- ✅ Respects `runtime.txt` Python version
- ✅ $5 free credit/month (enough for small projects)
- ✅ No sleep (always on, unlike Render free tier)
- ✅ Better build environment
- ✅ Faster deployments

## Deploy Steps

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login
```bash
railway login
```
This opens browser - login with GitHub.

### 3. Deploy from Backend Directory
```bash
cd /Users/akhila.yaragoppa/Documents/Misc/life_tracker/backend

# Initialize Railway project
railway init

# When prompted:
# - Project name: life-tracker-backend
# - Link to GitHub: Yes (optional but recommended)

# Deploy
railway up
```

### 4. Add Environment Variables
```bash
# Add your API keys
railway variables set LLM_PROVIDER=google
railway variables set GOOGLE_API_KEY=your_key_here
railway variables set SUPABASE_URL=your_url_here
railway variables set SUPABASE_KEY=your_key_here
```

### 5. Expose Public URL
```bash
railway domain
```

This generates a public URL like: `https://life-tracker-backend.up.railway.app`

### 6. Update Frontend
Update `frontend/index.html` and `frontend/views.js`:
```javascript
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://life-tracker-backend.up.railway.app'; // Your Railway URL
```

Commit and push to update Vercel.

---

## Railway Dashboard

View logs and manage: https://railway.app/dashboard

---

## Cost

- **Free credit:** $5/month
- **Usage:** ~$2-3/month for small app (always on)
- **No credit card** required initially

---

## Auto-Deploy from GitHub

If you linked to GitHub during setup:

1. Every `git push` auto-deploys
2. Monitor in Railway dashboard
3. Rollback via UI if needed

---

## Why This is Better Than Render Free Tier

| Feature | Railway | Render Free |
|---------|---------|-------------|
| Python version control | ✅ Yes | ❌ No (forced 3.14) |
| Always on | ✅ Yes | ❌ Sleeps after 15min |
| Build environment | ✅ Better | ❌ Limited |
| Deployment speed | ✅ Fast (~1-2min) | ⚠️ Slow (3-5min) |
| Cost | $5 credit/month | Free but limited |

---

## Quick Commands

```bash
# View logs
railway logs

# Open in browser
railway open

# Check status
railway status

# Link to GitHub (if not done during init)
railway link

# Deploy new changes
cd backend && railway up
```

---

## Troubleshooting

**If deployment fails:**
```bash
# Check logs
railway logs --follow

# Verify environment variables
railway variables
```

**To redeploy:**
```bash
railway up --detach
```

**To delete and start over:**
```bash
railway down
railway init
```

---

## Alternative: Deploy Directly from Root

If Railway doesn't pick up the `backend/` directory properly:

```bash
# From root directory
cd /Users/akhila.yaragoppa/Documents/Misc/life_tracker

railway init

# Railway will auto-detect the backend/ directory
# Or manually set in railway.toml
```

Create `railway.toml` in root:
```toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r backend/requirements.txt"

[deploy]
startCommand = "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

This way Railway builds from root but runs from backend directory.
