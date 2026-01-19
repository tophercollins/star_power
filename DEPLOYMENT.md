# Star Power - Deployment Guide

## Current Status ✅

**Backend**: Live at https://starpower-production.up.railway.app
**Frontend**: Ready to test locally or deploy to Vercel

## Testing the Complete Stack

### 1. Test the Backend API

```bash
# Health check
curl https://starpower-production.up.railway.app/health

# Create a game
curl -X POST https://starpower-production.up.railway.app/api/game/create \
  -H "Content-Type: application/json" \
  -d '{"player1_name": "Toph", "player2_name": "Computer"}'

# Interactive API docs
# Visit: https://starpower-production.up.railway.app/docs
```

### 2. Test the Frontend Locally

```bash
cd frontend
python3 -m http.server 8000
# Visit: http://localhost:8000
```

**What to test:**
- [ ] Enter your name
- [ ] Click "🎮 New Game" - should create a game and display 4 cards in your hand
- [ ] Click "Play" on a Star Card - should move it to "Your Stars"
- [ ] Click "Refresh" - should update the game state
- [ ] Toggle Debug - should show API call logs

### 3. Deploy Frontend to Vercel (Optional)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod

# You'll get a URL like: https://star-power-frontend.vercel.app
```

Or use the Vercel dashboard:
1. Go to https://vercel.com
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Deploy!

## Architecture Overview

```
┌─────────────┐         HTTPS          ┌──────────────────┐
│   Browser   │ ◄──────────────────► │  Railway Backend │
│             │    REST API calls      │  (FastAPI)       │
│ index.html  │                        │  Port: $PORT     │
└─────────────┘                        └──────────────────┘
      │                                         │
      │                                         │
      └─── Vanilla JS                          └─── Python 3.10
           (no build needed)                        In-memory state
                                                     Hardcoded cards
```

## Auto-Deployment Setup ⚙️

### Railway Backend (Already Configured)

**Trigger**: Push to `main` branch
**Files used**:
- `Procfile` - Tells Railway how to start the app
- `runtime.txt` - Specifies Python 3.10.13
- `backend/requirements.txt` - Python dependencies

**How it works**:
1. Push to main: `git push origin main`
2. Railway detects changes automatically
3. Builds using Python buildpack
4. Runs: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Live in ~2 minutes

### Vercel Frontend (When Ready)

**Trigger**: Push to `main` branch (after connecting GitHub)
**Files used**:
- `frontend/vercel.json` - Vercel configuration
- `frontend/index.html` - Static HTML file

**How it works**:
1. Connect GitHub repo to Vercel dashboard
2. Set root directory to `frontend`
3. Push to main → Auto-deploy
4. Live in ~30 seconds

## Environment Variables

### Backend (Railway)

Currently none required! Using hardcoded card data.

**Future (when adding database):**
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
```

Add in Railway dashboard: Settings → Variables

### Frontend (Vercel)

None required - API URL is hardcoded in `index.html`

**To change API endpoint:**
Edit line 8 in `frontend/index.html`:
```javascript
const API_URL = 'https://your-backend-url.railway.app';
```

## Monitoring & Logs

### Railway Logs

```bash
# View live logs (requires Railway CLI)
railway logs

# Or visit dashboard:
https://railway.app/project/[your-project]/deployments
```

### Vercel Logs

Visit dashboard: https://vercel.com/[your-project]/deployments

## Troubleshooting

### Backend not responding
- Check Railway dashboard for deployment status
- View logs in Railway dashboard
- Verify Procfile and runtime.txt are in repo root

### Frontend can't connect to backend
- Check CORS is enabled (already configured in `backend/main.py`)
- Verify API_URL in `index.html` matches Railway URL
- Open browser console (F12) for error messages

### Cards not displaying
- Toggle debug console in UI
- Check if game was created successfully
- Verify backend `/health` endpoint returns 200 OK

### Deployment failed
- Check Railway build logs for errors
- Verify all dependencies in `requirements.txt`
- Ensure Python version matches `runtime.txt`

## Next Steps

### Immediate (Testing)
- [ ] Test web UI locally
- [ ] Verify all Star Cards can be played
- [ ] Check deck counts update correctly
- [ ] Test with different player names

### Short Term (Features)
- [ ] Implement Power Card play logic
- [ ] Add end turn functionality
- [ ] Implement Event system
- [ ] Add Fan card distribution

### Medium Term (Infrastructure)
- [ ] Add Supabase database
- [ ] Implement user authentication
- [ ] Add game persistence
- [ ] Multiplayer matchmaking

### Long Term (Apps)
- [ ] React Native mobile app
- [ ] Progressive Web App (PWA)
- [ ] Real-time multiplayer (WebSockets)
- [ ] Leaderboards and statistics

## Useful Commands

```bash
# Backend development
cd backend
uvicorn main:app --reload --port 8000

# Frontend testing
cd frontend
python3 -m http.server 8000

# Git workflow
git checkout -b feature/my-feature
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
git checkout main
git merge feature/my-feature
git push origin main  # Triggers auto-deploy!

# Railway CLI
railway login
railway link
railway logs --tail
railway status

# Vercel CLI
vercel login
vercel --prod
vercel logs
```

## Support

- **Backend API Docs**: https://starpower-production.up.railway.app/docs
- **Codebase Documentation**: See `CLAUDE.md`
- **Game Rules**: See `README.md`
- **This Guide**: `DEPLOYMENT.md`

---

**Last Updated**: 2026-01-19
**Backend Status**: ✅ Live on Railway
**Frontend Status**: ⏳ Ready to deploy
