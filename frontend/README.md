# Star Power - Test Web UI

Quick and ready test interface for the Star Power card game backend.

## Live Demo

**Backend API**: https://starpower-production.up.railway.app

## Local Testing

### Option 1: Direct File Open
```bash
open index.html
# Or on Linux:
xdg-open index.html
```

### Option 2: Local Server (Recommended)
```bash
python3 -m http.server 8000
# Visit: http://localhost:8000
```

## Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? [your account]
# - Link to existing project? No
# - Project name? star-power-frontend
# - In which directory is your code located? ./
```

## Features

✅ Create new games
✅ Display player hands and boards
✅ Play Star Cards from hand
✅ View opponent's board
✅ Debug console for API calls

## Not Yet Implemented

❌ Power card functionality
❌ Event system
❌ Turn progression
❌ Fan cards and victory
❌ AI opponent moves

## Architecture

- **Single HTML file**: Vanilla JavaScript, no build process
- **API**: Calls Railway backend at `starpower-production.up.railway.app`
- **Styling**: Modern CSS with gradient backgrounds
- **State**: Fetched from backend on each action

## API Endpoints Used

- `POST /api/game/create` - Create new game
- `GET /api/game/{id}/state` - Get current game state
- `POST /api/game/{id}/play_card` - Play a card from hand

## Troubleshooting

**Cards not displaying?**
- Check browser console for errors
- Verify backend is running: https://starpower-production.up.railway.app/health

**Can't play cards?**
- Only Star Cards work currently (backend limitation)
- Power Cards will show "not implemented" in logs

**CORS errors?**
- Use local server (Option 2) instead of file:// protocol
