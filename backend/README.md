# Star Power Backend API

FastAPI backend for the Star Power celebrity card game.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Server starts at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp ../.env.example .env
# Edit .env with your values
```

## API Endpoints

### Health Check
```
GET /health
```

### Game Management

**Create a new game:**
```
POST /api/game/create
{
  "player1_name": "Toph",
  "player2_name": "Computer"
}
```

**Get game state:**
```
GET /api/game/{game_id}/state
```

**Play a card:**
```
POST /api/game/{game_id}/play_card
{
  "player_index": 0,
  "hand_index": 2
}
```

**Delete a game:**
```
DELETE /api/game/{game_id}
```

**List active games:**
```
GET /api/games/active
```

## Testing with cURL

```bash
# Create a game
curl -X POST http://localhost:8000/api/game/create \
  -H "Content-Type: application/json" \
  -d '{"player1_name": "Toph", "player2_name": "Computer"}'

# Get game state (replace {game_id})
curl http://localhost:8000/api/game/{game_id}/state

# Play a card
curl -X POST http://localhost:8000/api/game/{game_id}/play_card \
  -H "Content-Type: application/json" \
  -d '{"player_index": 0, "hand_index": 0}'
```

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── api/
│   ├── routes.py        # API endpoint definitions
│   └── __init__.py
├── services/
│   ├── game_service.py  # Business logic layer
│   └── __init__.py
├── database/
│   ├── models.py        # SQLAlchemy models (future)
│   ├── connection.py    # Database connection (future)
│   └── __init__.py
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Deployment

### Railway

1. Push to GitHub
2. Connect Railway to your repo
3. Railway auto-deploys from `main` branch
4. Set environment variables in Railway dashboard

### Environment Variables for Railway

```
DATABASE_URL=postgresql://...  (from Supabase)
GOOGLE_CREDENTIALS={"type":"service_account",...}
GOOGLE_SPREADSHEET_ID=...
```

## Development Roadmap

- [x] Basic game creation and card playing
- [ ] Database persistence (Supabase)
- [ ] User authentication
- [ ] Real-time updates (WebSockets)
- [ ] Power card implementation
- [ ] Event system
- [ ] Fan collection and win conditions
- [ ] Matchmaking
- [ ] Game history and replay

## API Documentation

When running locally, visit:
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
