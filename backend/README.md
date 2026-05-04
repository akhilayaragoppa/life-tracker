# Life Tracker Backend

Zero-friction capture system with LLM classification and Supabase storage.

## Setup

1. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up Supabase**
   - Go to [supabase.com](https://supabase.com) and create a new project
   - In the SQL Editor, run the contents of `supabase_schema.sql`
   - Get your project URL and anon key from Settings > API

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your keys:
   # - LLM_PROVIDER: "anthropic" or "google"
   # - ANTHROPIC_API_KEY (if using Anthropic - get from https://console.anthropic.com)
   # - GOOGLE_API_KEY (if using Google - get from https://aistudio.google.com/apikey)
   # - SUPABASE_URL
   # - SUPABASE_KEY
   ```

4. **Run the server**
   ```bash
   python main.py
   # Or with uvicorn:
   uvicorn main:app --reload
   ```

   Server runs at http://localhost:8000
   API docs at http://localhost:8000/docs

## API Endpoints

### POST /capture
Zero-friction capture endpoint. Send natural language text, get back classified item.

```bash
curl -X POST http://localhost:8000/capture \
  -H "Content-Type: application/json" \
  -d '{"text": "call the dentist sometime this week"}'
```

Response includes LLM classification (goal/task, category, timeline, etc.) and adds to inbox.

### GET /inbox
Get inbox items awaiting processing.

```bash
# Get unprocessed items
curl http://localhost:8000/inbox?processed=false

# Get all inbox items
curl http://localhost:8000/inbox
```

### POST /inbox/{id}/process
Convert inbox item to task/goal or dismiss.

```bash
# Accept and create task/goal
curl -X POST http://localhost:8000/inbox/{id}/process?action=accept

# Dismiss
curl -X POST http://localhost:8000/inbox/{id}/process?action=dismiss
```

### GET /tasks
Get tasks with optional filters.

```bash
# Get today's tasks
curl http://localhost:8000/tasks?urgency_bucket=today&completed=false

# Get all incomplete tasks
curl http://localhost:8000/tasks?completed=false
```

### PATCH /tasks/{id}/complete
Mark task as completed. Auto-updates linked goal progress.

### GET /goals
Get all goals with progress percentages.

## How It Works

1. **Capture** - User sends natural language text to `/capture`
2. **Classify** - Claude Haiku analyzes and extracts:
   - Type (goal vs task)
   - Category (chore, wish, health, etc.)
   - Timeline (today, this week, bucket, etc.)
   - Clear title and optional deadline
   - For goals: suggests 2-3 starter tasks
3. **Inbox** - Classified item goes to inbox for review
4. **Process** - Accept to create task/goal, or dismiss
5. **Track** - Tasks link to goals, progress auto-calculates

## LLM Provider Options

The system supports two LLM providers for classification:

**Anthropic (Claude Haiku 4.0)**
- Cost: ~$0.0002 per call
- Very reliable JSON output
- Excellent classification accuracy
- Set `LLM_PROVIDER=anthropic` in .env

**Google (Gemini 2.0 Flash)**
- Cost: Free tier available (1500 requests/day), then ~$0.00001 per call
- Fast and cost-effective
- Good classification quality
- Set `LLM_PROVIDER=google` in .env

Switch providers by changing `LLM_PROVIDER` in your .env file. Normal usage: <₹50/month with either provider.
