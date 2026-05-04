# Life Tracker Frontend

Zero-friction capture interface for your life tracker system.

## Features

- **Single text field** - Just type naturally, no forms or dropdowns
- **Instant capture** - Hit Cmd/Ctrl+Enter or click Capture
- **Recent items view** - See your last 5 captures with classification
- **Mobile-friendly** - Responsive design, works on any device
- **PWA-ready** - Can be installed as an app on your phone

## Running Locally

The frontend is a simple static HTML file. You can run it with any static file server:

### Option 1: Python (simplest)
```bash
cd frontend
python3 -m http.server 3000
```

Then open http://localhost:3000

### Option 2: Node.js
```bash
cd frontend
npx serve -p 3000
```

### Option 3: Just open the file
```bash
open index.html
```
(CORS may require backend configuration)

## Mobile Setup (PWA)

### On iPhone/iPad:
1. Open http://your-ip:3000 in Safari
2. Tap the Share button
3. Tap "Add to Home Screen"
4. Now you have a quick-capture app!

### On Android:
1. Open http://your-ip:3000 in Chrome
2. Tap the menu (three dots)
3. Tap "Add to Home Screen"
4. Launch from your home screen

## Usage

**Just type naturally:**
- "call the dentist sometime this week"
- "build self confidence"
- "grocery shopping tomorrow"

The system automatically:
- Classifies as goal or task
- Assigns category (chore, health, work, etc.)
- Extracts timeline (today, this week, bucket)
- Extracts deadlines if mentioned
- Suggests starter tasks for goals

## Keyboard Shortcuts

- **Cmd/Ctrl + Enter** - Capture and clear
- **Tab** - Focus capture button
- **Esc** - Clear input (when focused)

## API Configuration

The frontend connects to `http://localhost:8000` by default. To change this, edit the `API_BASE` constant in `index.html`:

```javascript
const API_BASE = 'http://your-server:8000';
```

## Next Steps

Future enhancements:
- Inbox management page (view, accept, dismiss)
- Today/Week/Goals views
- Offline support with service worker
- Voice input via Web Speech API
- Dark mode toggle
