# 🚀 Getting Started with Star Power Backend

Quick guide to get the Star Power API running locally and deployed to Railway.

## Prerequisites

- Python 3.10+
- Git
- Google Sheets API credentials (for card data)
- Railway account (for deployment)

## Local Setup (5 minutes)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
# Copy example file
cp ../.env.example .env

# Edit .env (optional for local testing)
# The app works with default values
```

### 3. Run the Server

```bash
python main.py
```

Server starts at: **http://localhost:8000**

API docs at: **http://localhost:8000/docs**

### 4. Test the API

**Option A: Use the interactive docs**
- Go to http://localhost:8000/docs
- Try the "Create Game" endpoint
- Click "Try it out" → "Execute"

**Option B: Use cURL**

```bash
# Create a game
curl -X POST http://localhost:8000/api/game/create \
  -H "Content-Type: application/json" \
  -d '{"player1_name": "Toph", "player2_name": "Computer"}'

# Response includes game_id - copy it
# Example: "game_id": "123e4567-e89b-12d3-a456-426614174000"

# Get game state
curl http://localhost:8000/api/game/{game_id}/state

# Play a card (player 0, card at index 0)
curl -X POST http://localhost:8000/api/game/{game_id}/play_card \
  -H "Content-Type: application/json" \
  -d '{"player_index": 0, "hand_index": 0}'
```

## Deploy to Railway (10 minutes)

### 1. Prepare Your Code

```bash
# Make sure all changes are committed
git add .
git commit -m "Add FastAPI backend"
git push origin main
```

### 2. Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `tophercollins/star_power`
6. Railway will auto-detect and deploy!

### 3. Configure Environment Variables (Optional)

In Railway dashboard:
1. Click your service
2. Go to "Variables" tab
3. Add variables (if needed):
   - `GOOGLE_CREDENTIALS` (for Google Sheets)
   - `DATABASE_URL` (when you add Supabase)

### 4. Get Your Live URL

Railway assigns a URL like:
```
https://star-power-production.up.railway.app
```

Test it:
```bash
curl https://your-app.railway.app/health
```

### 5. Set Up Auto-Deploy

In Railway:
1. Settings → Environment
2. Select branch: `main`
3. Enable "Auto Deploy" ✅

Now every push to `main` auto-deploys!

## Next Steps

### Add Database (Supabase)

1. Go to [supabase.com](https://supabase.com)
2. Create project: "star-power"
3. Copy connection string from Settings → Database
4. Add to Railway: Variable `DATABASE_URL`

### Add Authentication

1. Uncomment database code in `backend/main.py`
2. Run migrations (future)
3. Implement user registration/login

### Build Frontend

1. Create React Native app
2. Connect to Railway API
3. Deploy mobile app

## Troubleshooting

### Google Sheets Error

**Problem**: Can't load cards from Google Sheets

**Solution**:
```bash
# Add service account JSON to Railway
# In Railway Variables:
GOOGLE_CREDENTIALS={"type":"service_account",...}
```

### Import Error

**Problem**: `ModuleNotFoundError: No module named 'engine'`

**Solution**:
```bash
# Make sure you're running from backend/ directory
cd backend
python main.py
```

### Port Already in Use

**Problem**: `Address already in use`

**Solution**:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
PORT=8001 python main.py
```

## Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-endpoint

# 2. Make changes
# Edit backend/api/routes.py

# 3. Test locally
cd backend && python main.py
# Visit http://localhost:8000/docs

# 4. Commit
git add .
git commit -m "Add new endpoint"

# 5. Push
git push origin feature/new-endpoint

# 6. Merge to main
git checkout main
git merge feature/new-endpoint
git push origin main

# 7. Railway auto-deploys!
```

## Useful Commands

```bash
# Run server
python backend/main.py

# Run in development mode (auto-reload)
cd backend && uvicorn main:app --reload

# Check API docs
open http://localhost:8000/docs

# Test health endpoint
curl http://localhost:8000/health

# View Railway logs
railway logs

# Deploy manually
railway up
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Railway Docs](https://docs.railway.app/)
- [Supabase Docs](https://supabase.com/docs)
- [CLAUDE.md](./CLAUDE.md) - Full codebase documentation

## Need Help?

Check the full documentation in `CLAUDE.md` for:
- Complete API reference
- Architecture details
- Code organization
- Development patterns
