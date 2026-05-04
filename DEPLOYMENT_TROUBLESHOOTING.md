# Deployment Troubleshooting

## Common Issues & Solutions

### Vercel Frontend Issues

#### Issue: "No Output Directory named 'frontend' found"
**Solution:**
1. In Vercel dashboard → Your project → Settings → General
2. **Root Directory:** Leave blank (or set to `.`)
3. **Build Command:** `echo "No build needed"`
4. **Output Directory:** `frontend`
5. Click "Save"
6. Redeploy: Deployments tab → Click ⋯ → "Redeploy"

**Alternative:** If above doesn't work, try:
- Root Directory: `frontend`
- Output Directory: `.` (current directory)

#### Issue: 404 on all routes except index
**Fix:** Already handled in `vercel.json` with routes configuration.

---

### Render Backend Issues

#### Issue: Pydantic compilation fails (Rust/Cargo errors)
**Root cause:** Render's free tier has Python 3.14 which causes pydantic-core compilation issues.

**Solutions tried:**
1. ✅ Downgraded pydantic to 2.8.2 (has pre-built wheels)
2. ✅ Set Python to 3.11.9 in `runtime.txt`
3. ✅ Added `--no-cache-dir` to avoid cached broken builds

**If still failing:**
Try these in Render dashboard → Environment:
```
PYTHON_VERSION=3.11.9
PIP_NO_BINARY=:none:
```

Or modify `render.yaml` build command to:
```yaml
buildCommand: "pip install --only-binary=:all: -r requirements.txt"
```

#### Issue: "Read-only file system" during build
This happens when Cargo tries to write to `/usr/local/cargo`. The fix is to avoid compiling from source by using pre-built wheels (already done in requirements.txt).

#### Issue: Build succeeds but app crashes on start
**Check logs:** Render dashboard → Logs tab

Common causes:
1. **Missing environment variables** - Verify all are set:
   - `LLM_PROVIDER=google`
   - `GOOGLE_API_KEY=your_key`
   - `SUPABASE_URL=your_url`
   - `SUPABASE_KEY=your_key`

2. **Port binding** - Already fixed: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Import errors** - Check logs for missing dependencies

---

### Alternative Deployment Options

If Render continues to fail, try these free alternatives:

#### Option 1: Railway.app (Easiest)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
cd backend
railway init
railway up
```

- $5 free credit/month
- Better build environment than Render free tier
- No sleep (always on)

#### Option 2: Fly.io
```bash
# Install flyctl
brew install flyctl

# Login and launch
flyctl auth login
cd backend
flyctl launch
```

Create `Dockerfile` in backend/:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Option 3: Google Cloud Run (Free tier)
```bash
gcloud run deploy life-tracker-backend \
  --source backend/ \
  --region us-central1 \
  --allow-unauthenticated
```

Requires `Dockerfile` (same as above).

---

### CORS Issues

If frontend can't reach backend:

#### Symptom: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Fix in `backend/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    # allow_origins=["https://your-vercel-app.vercel.app"],  # For production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, replace `["*"]` with your actual Vercel URL.

---

### Supabase Connection Issues

#### Issue: "Connection refused" or "SSL required"
**Check:**
1. Supabase URL is correct (should be `https://PROJECT_ID.supabase.co`)
2. Using **anon public** key, not service_role key
3. RLS policies are set correctly (we set to allow all in schema)

**Test connection manually:**
```bash
curl https://YOUR_PROJECT.supabase.co/rest/v1/inbox \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

---

### LLM/Google API Issues

#### Issue: "API key invalid" or "quota exceeded"
**Solutions:**
1. **Generate new key:** https://aistudio.google.com/apikey
2. **Check quota:** https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
3. Free tier: 1500 requests/day (plenty for personal use)

#### Issue: Response too slow
Google Gemini Flash is very fast (<1s typically). If slow:
- Check Render logs for other issues
- Try Anthropic Claude Haiku instead:
  ```
  LLM_PROVIDER=anthropic
  ANTHROPIC_API_KEY=sk-ant-...
  ```

---

### Debugging Checklist

When something breaks:

**Frontend (Vercel):**
1. ✅ Check Vercel deployment logs
2. ✅ Open browser DevTools → Console for errors
3. ✅ Verify API_BASE URL in `index.html` and `views.js`
4. ✅ Test backend URL directly in browser

**Backend (Render):**
1. ✅ Check Render build logs
2. ✅ Check Render runtime logs
3. ✅ Test health endpoint: `https://your-backend.onrender.com/`
4. ✅ Verify all environment variables are set
5. ✅ Check Supabase connection from logs

**Both:**
1. ✅ Clear browser cache
2. ✅ Try incognito/private window
3. ✅ Check if services are awake (Render free tier sleeps)

---

## Quick Test Commands

### Test Backend Locally
```bash
cd backend
python main.py
# Visit http://localhost:8000
```

### Test Frontend Locally
```bash
cd frontend
python3 -m http.server 3000
# Visit http://localhost:3000
```

### Test Backend on Render
```bash
curl https://your-backend.onrender.com/
# Should return: {"message": "Life Tracker API", "status": "running"}
```

### Test Full Flow
```bash
# Capture test
curl -X POST https://your-backend.onrender.com/capture \
  -H "Content-Type: application/json" \
  -d '{"text": "test task for tomorrow"}'
```

---

## Getting Help

If still stuck:

1. **Check Render status:** https://status.render.com
2. **Check Vercel status:** https://www.vercel-status.com
3. **Render support:** https://render.com/docs
4. **Vercel support:** https://vercel.com/docs

**Share these when asking for help:**
- Full error message from logs
- Your `render.yaml` or `vercel.json` config
- Python/dependency versions
- What you've already tried

---

## Success Verification

Once deployed successfully, you should be able to:

1. ✅ Visit frontend: `https://life-tracker.vercel.app`
2. ✅ Type a task and hit Capture
3. ✅ See "✓ Captured successfully!"
4. ✅ See the task appear in Recent Captures
5. ✅ Visit `/views.html` and see your task in a view
6. ✅ Complete the task and see it disappear

**Backend wake-up:** First request after 15min idle takes ~30s (Render free tier). Subsequent requests are fast.
