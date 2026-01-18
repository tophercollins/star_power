# ⭐ Star Power

A competitive multiplayer card game where you build your celebrity empire!

## 🎮 What is Star Power?

Star Power is a turn-based strategy card game where two players compete by:
- Playing **Star Cards** (celebrities/influencers) with 4 stats: Aura, Talent, Influence, Legacy
- Enhancing stars with **Power Cards** (stat modifiers)
- Competing in **Events** (stat contests)
- Collecting **Fans** (victory points)
- First to 10 fans wins!

## 🏗️ Project Structure

```
star_power/
├── backend/              # FastAPI REST API
│   ├── main.py          # API entry point
│   ├── api/             # Endpoints
│   ├── services/        # Business logic
│   └── database/        # Models & DB
│
├── engine/              # Core game logic (shared)
│   ├── game_engine.py  # Command dispatcher
│   ├── rules/          # Game mechanics
│   ├── models/         # Data models
│   └── serializers.py  # State serialization
│
├── utils/               # Utilities (shared)
│   ├── card_loader.py  # Load cards from Google Sheets
│   └── deck_builder.py # Build game decks
│
├── resources/           # Configuration
│   └── config.py       # Game constants
│
├── legacy/              # Original desktop app
│   ├── main.py         # DearPyGui version
│   └── ui/             # Desktop UI
│
└── CLAUDE.md           # Complete codebase documentation
```

## 🚀 Quick Start

### Backend API (Development)

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the server
python main.py

# Visit http://localhost:8000/docs for API documentation
```

### Test the API

```bash
# Create a game
curl -X POST http://localhost:8000/api/game/create \
  -H "Content-Type: application/json" \
  -d '{"player1_name": "Toph", "player2_name": "Computer"}'

# You'll get back a game_id - use it to play:
curl -X POST http://localhost:8000/api/game/{game_id}/play_card \
  -H "Content-Type: application/json" \
  -d '{"player_index": 0, "hand_index": 0}'
```

## 📦 Tech Stack

**Backend:**
- Python 3.10+
- FastAPI (REST API)
- SQLAlchemy (ORM, future)
- PostgreSQL/Supabase (database, future)

**Game Engine:**
- Pure Python dataclasses
- Functional rule system
- Command-driven architecture

**Data Source:**
- Google Sheets API (card definitions)

**Deployment:**
- Railway (backend hosting)
- Supabase (database)

## 🎯 Current Status

**✅ Completed:**
- Core game engine
- Star card play mechanics
- FastAPI backend with REST endpoints
- In-memory game state management
- Google Sheets card data loading

**🚧 In Progress:**
- Database persistence
- User authentication
- Multiplayer matchmaking

**📋 Planned:**
- Power card implementation
- Event system
- Fan collection
- Win conditions
- Mobile app (React Native)
- Web app (PWA)

## 📖 Documentation

See [CLAUDE.md](./CLAUDE.md) for comprehensive documentation including:
- Complete game mechanics
- Technical architecture
- Code organization
- Development workflows
- API reference

## 🔧 Development

### Setting Up

```bash
# Clone the repository
git clone https://github.com/tophercollins/star_power.git
cd star_power

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes, commit
git add .
git commit -m "Add your feature"

# Push to GitHub
git push origin feature/your-feature

# Merge to main (triggers Railway auto-deploy)
git checkout main
git merge feature/your-feature
git push origin main
```

## 🌐 API Endpoints

### Game Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/game/create` | Create a new game |
| GET | `/api/game/{id}/state` | Get current game state |
| POST | `/api/game/{id}/play_card` | Play a card from hand |
| DELETE | `/api/game/{id}` | Delete a game |
| GET | `/api/games/active` | List active games |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health status |
| GET | `/` | API information |

Full API documentation at `/docs` when running locally.

## 🎲 Game Rules

### The Four Stats

Every Star Card has four stats (1-10):

- **Aura**: Presence, charisma, mystique
- **Talent**: Skill, artistic ability
- **Influence**: Reach, connections, impact
- **Legacy**: Longevity, cultural impact

### Card Types

1. **Star Cards**: Celebrities/influencers (main playable cards)
2. **Power Cards**: Stat modifiers and enhancements
3. **Event Cards**: Trigger stat contests between players
4. **Fan Cards**: Victory points (first to 10 wins)

See [CLAUDE.md](./CLAUDE.md) for complete rules and mechanics.

## 🤝 Contributing

This is currently a solo project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

[Add your license here]

## 🙏 Acknowledgments

- Card data sourced from Google Sheets
- Built with FastAPI, Python, and passion for card games!

---

**Built by [Topher Collins](https://github.com/tophercollins)**
