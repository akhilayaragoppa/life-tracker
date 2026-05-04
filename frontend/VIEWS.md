# Life Tracker Views - The Visibility Layer

This is the most critical part of your system: **clean, focused visualization** that keeps you on track without overwhelming you.

## The Four Views

### 1. **Today View** 🔥
**Purpose:** Maximum focus on what matters RIGHT NOW

**Design:**
- **Limited to 3-5 tasks** - System enforces this to prevent overwhelm
- Big, clear task cards
- One-click complete
- Yellow banner reminds you to choose wisely

**Philosophy:** If you can't do it in one good day, you shouldn't put it here.

---

### 2. **Week View** 📅
**Purpose:** See everything on your plate, organized by urgency

**Sections:**
- 🔥 **Today** - Urgent, do now
- 📅 **This Week** - Important, but not today
- 📆 **This Month** - On the horizon
- 🗂️ **Someday** - Eventually

**Features:**
- Tasks grouped by urgency bucket
- See deadlines at a glance
- Complete tasks directly
- Count badges show workload per section

**Use this to:** Plan your week, see what's coming, prioritize.

---

### 3. **Goals View** 🎯
**Purpose:** Track larger ambitions and the progress toward them

**Goal Cards show:**
- **Progress bar** - Auto-calculated from linked tasks
- **Category** - Quick visual grouping
- **Next 2-3 tasks** - What to work on next
- **Description** - Why this matters

**The magic:** When you complete tasks linked to a goal, the progress bar automatically updates. This keeps you motivated and shows you're making real progress on big things.

**Use this to:** Remember why you're doing small tasks, see the bigger picture, stay motivated.

---

### 4. **Bucket View** 📦
**Purpose:** Your idea dump - everything unscheduled

**Features:**
- **Category filters** - Browse by chore, wish, health, work, etc.
- **Promote buttons** - One tap to move to "This Week" or "Today"
- **Grid layout** - Scan quickly

**Philosophy:** This is where ideas go to wait. Nothing clutters your Today or Week view until you're ready.

**Use this to:** Review unscheduled items, promote what's ready, clean out stale ideas.

---

## Key Design Principles

### 1. **Clean by Design, Not Discipline**
You don't need to manually organize or clean up. The system enforces:
- Only 3-5 tasks in Today view
- Clear separation of timeframes
- Auto-categorization from capture

### 2. **No Clutter**
- Bucket is hidden from main views
- Completed tasks disappear immediately
- Goals show only next 2-3 tasks, not everything

### 3. **Easy to Act**
Every view has action buttons:
- ✓ Complete (one click)
- → Promote to This Week
- 🔥 Promote to Today

### 4. **Always Current**
- Auto-refreshes every 30 seconds
- Real-time progress updates
- No stale data

---

## How to Use the System

### Daily Workflow
1. **Morning:** Open Today view, see your 3-5 focus tasks
2. **During day:** Complete tasks as you finish them
3. **End of day:** Check Week view, promote tomorrow's priorities

### Weekly Planning
1. **Sunday evening or Monday morning**
2. Open Week view
3. See what's coming up
4. Promote 3-5 items to Today for Monday
5. Review Bucket, promote anything ready

### Goal Check-ins
1. **Once a week or when feeling unmotivated**
2. Open Goals view
3. See your progress bars
4. Feel good about what you've accomplished
5. Pick next tasks to work on

### Bucket Review
1. **When you have time or need inspiration**
2. Open Bucket view
3. Filter by category
4. Promote what's ready
5. Delete what's stale

---

## Technical Details

**Files:**
- `views.html` - The dashboard UI
- `views.js` - Data loading and view logic

**Navigation:**
- Top tabs switch between views
- "+ Capture" button always visible
- Mobile-responsive (tabs collapse on phone)

**Data Flow:**
- Fetches from backend API every 30 seconds
- Updates immediately on actions (complete, promote)
- Shows loading states while fetching

**Keyboard Shortcuts (future):**
- `1` - Today view
- `2` - Week view  
- `3` - Goals view
- `4` - Bucket view
- `c` - Capture (goes to index.html)

---

## Running the Views

Same as the capture interface:

```bash
cd frontend
python3 -m http.server 3000
```

Then open http://localhost:3000/views.html

**Make sure backend is running:**
```bash
cd backend
python main.py
```

---

## What Makes This Different

Most todo apps fail because:
1. **Too flexible** - You can add unlimited tasks to "today" until it's meaningless
2. **No hierarchy** - Tasks and goals treated the same
3. **Manual organization** - You spend more time organizing than doing

This system fixes that:
1. **Today is limited** - Forces prioritization
2. **Goals and tasks are separate** - Goals track progress via linked tasks
3. **Auto-organized** - LLM classifies, you just promote when ready

The result: **You always know what to focus on, and you can see your progress on bigger things.**
