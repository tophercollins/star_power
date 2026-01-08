# CLAUDE.md - Star Power Codebase Guide

**Last Updated**: 2026-01-08
**Project**: Star Power - A card-based strategy game
**Language**: Python 3.10+
**UI Framework**: DearPyGui

---

## Project Overview

Star Power is a turn-based card game where players compete by playing Star Cards, Power Cards, and collecting Fans through Event contests. The game features:

- 2 players (Human vs Computer)
- 4 stat types: Aura, Talent, Influence, Legacy
- 3 deck types: Main Deck (Stars + Powers), Event Deck (Stat Contests), Fan Deck (Victory Points)
- Win condition: First to 10 fans wins
- Card data sourced from Google Sheets for easy non-developer editing

---

## Architecture Philosophy

### Core Principles

1. **Separation of Concerns**: Game logic (engine) is completely separate from UI (game_client)
2. **Data-Driven Design**: Card definitions live in Google Sheets, not hardcoded
3. **Functional Rules**: Game mechanics are pure functions, not object methods
4. **Immutable Models**: Dataclasses represent state without behavior
5. **Command Pattern**: UI sends commands to engine via dispatch system

### MVC-Inspired Pattern

```
Model (engine/models/)           - Pure data structures (dataclasses)
Controller (engine/game_engine)  - Command dispatcher, state manager
View (ui/game_client)            - DearPyGui UI, rendering only
Rules (engine/rules/)            - Business logic functions
```

---

## Directory Structure

```
/home/user/star_power/
├── main.py                          # Entry point - initializes game
│
├── engine/                          # Core game logic (NEW architecture)
│   ├── game_engine.py              # GameEngine class - command dispatcher
│   ├── setup.py                    # Initialization: players, decks, starting hands
│   ├── serializers.py              # Convert models → JSON for UI
│   │
│   ├── models/                     # Data models (pure dataclasses, no logic)
│   │   ├── cards.py                # StarCard, PowerCard, FanCard, EventCard
│   │   ├── player.py               # Player model
│   │   └── deck.py                 # Deck model
│   │
│   └── rules/                      # Game mechanics (pure functions)
│       ├── common_ops.py           # Card play dispatcher
│       ├── deck_ops.py             # Deck manipulation (draw, shuffle, etc.)
│       ├── star_ops.py             # Star card play logic
│       └── power_ops.py            # Power card logic (INCOMPLETE - stub)
│
├── ui/                             # User interface
│   └── game_client.py              # DearPyGui client - 1025x900 window
│
├── utils/                          # External data integration
│   ├── card_loader.py              # Parse Google Sheets → card objects
│   ├── deck_builder.py             # Assemble decks from loaded cards
│   └── google_client.py            # Google Sheets API client
│
├── resources/                      # Configuration & credentials
│   ├── config.py                   # GAME_CONFIG dict, constants
│   └── google_service_account.json # Google API credentials (GITIGNORED)
│
├── classes/                        # LEGACY - old class-based architecture
├── classes legacy/                 # LEGACY - previous iteration (unused)
├── dearpyguitests/                 # UI prototypes & experiments
└── notes                           # Development notes
```

---

## Key Files Reference

### Entry Point
- **main.py** (20 lines): Orchestrates initialization
  - Build players → Build decks → Deal hands → Create engine → Launch UI

### Game Engine Core
- **engine/game_engine.py**: GameEngine class
  - `__init__`: Initialize with players and 3 decks
  - `dispatch(command)`: Process UI commands (PLAY_CARD, etc.)
  - `snapshot()`: Return full game state as JSON
  - `pending_card`: Tracks cards awaiting target selection

### Initialization
- **engine/setup.py**: Game setup functions
  - `build_players()`: Create 2 Player objects (Toph, Computer)
  - `build_decks()`: Load cards from Google Sheets, build 3 decks
  - `deal_starting_hands(players, deck)`: Deal 4 cards to each player

### Data Transformation
- **engine/serializers.py**: Model → JSON converters
  - `player_view(player)`: Serialize player state for UI
  - `star_card_view(card)`: Serialize star card with attachments
  - `deck_view(deck)`: Serialize deck contents and count

### Models (Pure Data)
- **engine/models/cards.py**: All card types
  - `StarCard`: Main playable cards (4 stats, tags, attachments)
  - `PowerCard`: Base class for modifier cards
  - `ModifyStatCard(PowerCard)`: Stat modification power cards
  - `LocationPowerCard(PowerCard)`: Location-based powers (stub)
  - `EventCard`: Base event card
  - `StatContestEvent(EventCard)`: Stat contest events
  - `FanCard`: Victory point cards (generic or tagged)

- **engine/models/player.py**: Player dataclass
  - Fields: `name`, `hand`, `star_cards`, `locations`

- **engine/models/deck.py**: Deck dataclass
  - Fields: `cards` (list)

### Game Rules (Functions)
- **engine/rules/star_ops.py**: Star card operations
  - `play_star_from_hand(player, hand_index)`: Move star from hand to board

- **engine/rules/deck_ops.py**: Deck operations
  - `draw_card(player, deck)`: Draw 1 card from deck to hand
  - `shuffle_deck(deck)`: Randomize deck order
  - `add_card(deck, card)`: Add card to deck
  - `peek_cards(deck, count)`: View top N cards without drawing

- **engine/rules/common_ops.py**: Card play dispatcher
  - `play_card_from_hand(player, hand_index)`: Route to correct play function

- **engine/rules/power_ops.py**: Power card operations (STUB - NOT IMPLEMENTED)

### UI
- **ui/game_client.py**: DearPyGui interface
  - `GameClient.__init__(engine)`: Create viewport, setup UI, render initial state
  - `setup_ui()`: Create window layout with 3 zones
  - `refresh_zones()`: Re-render all UI based on current game state
  - `display_card(card, parent)`: Render individual card widget
  - **UI Zones**:
    - `deck_zone`: Shows 3 deck card counts
    - `board_zone`: Opponent stars (top) + Player stars (bottom)
    - `hand_zone`: Player's hand with play buttons

### Utilities
- **utils/card_loader.py**: Google Sheets → Card objects
  - `load_star_cards(sheet)`: Parse StarCard rows
  - `load_power_cards(sheet)`: Parse PowerCard rows
  - `load_event_cards(sheet)`: Parse EventCard rows
  - `load_fan_cards(sheet)`: Parse FanCard rows

- **utils/deck_builder.py**: Card lists → Deck objects
  - `build_main_deck_from_sheet()`: Create main deck (stars + powers)
  - `build_event_deck_from_sheet()`: Create event deck
  - `build_fan_deck_from_sheet()`: Create fan deck

- **utils/google_client.py**: Google API setup
  - `init_google_sheets_client()`: Authenticate and return gspread client

### Configuration
- **resources/config.py**: Game constants
  - `GAME_CONFIG`: Dict with all game rules
    - `starting_hand_size`: 4
    - `cards_drawn_per_turn`: 1
    - `star_cards_per_turn_limit`: 1
    - `power_cards_per_turn_limit`: 2
    - `fans_to_win`: 10
    - Deck composition ratios
  - `GOOGLE_SPREADSHEET_ID`: Sheet ID for card data

---

## Development Conventions

### Naming Conventions
- **Modules**: `snake_case` (game_engine.py, card_loader.py)
- **Classes**: `PascalCase` (GameEngine, StarCard, Player)
- **Functions**: `snake_case` (play_star_from_hand, draw_card)
- **Constants**: `UPPER_SNAKE_CASE` (GAME_CONFIG, GOOGLE_SPREADSHEET_ID)
- **Private/Internal**: Leading underscore `_helper_function`

### Code Organization Patterns

#### Dataclass Models (models/)
- **Pure data structures** - no methods except `__init__` (auto-generated)
- Use `@dataclass` decorator
- Type hints required for all fields
- Use `field(default_factory=list)` for mutable defaults
- Import from `__future__ import annotations` for forward references

Example:
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class StarCard:
    id: str
    name: str
    aura: int
    tags: List[str] = field(default_factory=list)
```

#### Rule Functions (rules/)
- **Pure functions** that take state, return nothing (mutate in place)
- Always accept player/deck objects as parameters
- Use logging for debugging: `logger.info(f"{player.name} played {card.name}")`
- Validate inputs before mutations
- Keep functions focused - one responsibility

Example:
```python
import logging
logger = logging.getLogger(__name__)

def play_star_from_hand(player, hand_index: int):
    card = player.hand[hand_index]
    if not isinstance(card, StarCard):
        logger.info(f"Cannot play non-star card: {card.name}")
        return

    player.hand.pop(hand_index)
    player.star_cards.append(card)
    logger.info(f"{player.name} played {card.name}")
```

#### Serializers (serializers.py)
- Convert internal objects → JSON dicts for UI
- Use descriptive key names
- Include all data needed for rendering
- Return dicts, not JSON strings

Example:
```python
def star_card_view(card: StarCard) -> dict:
    return {
        "id": card.id,
        "name": card.name,
        "stats": {
            "aura": card.aura,
            "talent": card.talent,
            "influence": card.influence,
            "legacy": card.legacy
        },
        "attached_fans": [fan_view(f) for f in card.attached_fans]
    }
```

### Type Hints
- **Required** for all function parameters and return types
- Use `typing` module: `List`, `Dict`, `Tuple`, `Optional`, `Any`
- Model types: Import actual classes (e.g., `from engine.models.cards import StarCard`)

```python
from typing import List, Dict, Any, Optional
from engine.models.player import Player
from engine.models.deck import Deck

def deal_starting_hands(players: List[Player], deck: Deck) -> None:
    ...
```

### Logging
- Use Python's `logging` module (not print statements)
- Format: `"%(asctime)s - %(levelname)s - %(message)s"`
- Create module-level logger: `logger = logging.getLogger(__name__)`
- Log key events: initialization, card plays, errors
- Use f-strings for log messages

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Initializing GameEngine")
logger.info(f"Dispatch: {action} {payload}")
```

### Error Handling
- Validate inputs early (type checks, index bounds)
- Log invalid operations instead of raising exceptions (game continues)
- Use `isinstance()` for type checks
- Check list bounds before accessing: `if 0 <= index < len(list)`

---

## Data Flow

### Initialization Flow
```
main.py
  → build_players() [setup.py]
      → Creates 2 Player objects

  → build_decks() [setup.py]
      → init_google_sheets_client() [google_client.py]
      → load_star_cards() [card_loader.py]
      → load_power_cards() [card_loader.py]
      → load_event_cards() [card_loader.py]
      → load_fan_cards() [card_loader.py]
      → build_main_deck_from_sheet() [deck_builder.py]
      → build_event_deck_from_sheet() [deck_builder.py]
      → build_fan_deck_from_sheet() [deck_builder.py]

  → deal_starting_hands() [setup.py]
      → draw_card() x4 per player [deck_ops.py]

  → GameEngine(players, decks)

  → GameClient(engine)
      → setup_ui()
      → refresh_zones() (initial render)
```

### Game Loop Flow
```
User clicks "Play" button in UI
  ↓
GameClient sends command to engine.dispatch()
  {
    "type": "PLAY_CARD",
    "payload": {"player": 0, "hand_index": 2}
  }
  ↓
GameEngine.dispatch() routes to appropriate rule function
  → play_card_from_hand() [common_ops.py]
      → play_star_from_hand() [star_ops.py]
          OR
      → play_power_from_hand() [power_ops.py] (STUB)
  ↓
Rule function mutates Player/Deck objects
  (e.g., move card from hand to star_cards)
  ↓
GameEngine.snapshot() serializes game state
  → player_view() [serializers.py]
  → deck_view() [serializers.py]
  Returns: {"players": [...], "decks": {...}, "turn": 1}
  ↓
GameClient receives snapshot
  ↓
GameClient.refresh_zones() re-renders UI
  → Clears old widgets
  → Calls display_card() for each card
  → Shows updated state
```

---

## Google Sheets Integration

### Card Data Source
- **Spreadsheet ID**: `1CuN3CzMUi3YkNAEWqDReA2UoiKqvNBYu5WA_HzlAOHQ`
- **Authentication**: Service account JSON (gitignored)
- **Sheets Expected**:
  - "Star Cards" - Columns: Name, Aura, Talent, Influence, Legacy, Tags
  - "Power Cards" - Columns: Name, Description, Stat Modifiers
  - "Event Cards" - Columns: Name, Description, Stat Options
  - "Fan Cards" - Columns: Name, Bonus, Tag

### Card Loading Process
1. Initialize gspread client with service account
2. Open spreadsheet by ID
3. For each card type:
   - Get worksheet by name
   - Read all rows (skip header)
   - Parse into card objects with UUIDs
   - Validate required fields
4. Return lists of card objects

---

## Common Workflows

### Adding a New Card Type

1. **Define model** in `engine/models/cards.py`:
   ```python
   @dataclass
   class NewCardType:
       id: str
       name: str
       # ... other fields
   ```

2. **Create loader** in `utils/card_loader.py`:
   ```python
   def load_new_cards(sheet) -> List[NewCardType]:
       worksheet = sheet.worksheet("New Cards")
       rows = worksheet.get_all_values()[1:]  # Skip header
       return [NewCardType(id=str(uuid.uuid4()), ...) for row in rows]
   ```

3. **Update deck builder** if needed in `utils/deck_builder.py`

4. **Add play logic** in `engine/rules/new_card_ops.py`:
   ```python
   def play_new_card(player, hand_index: int):
       # Implementation
       logger.info(f"{player.name} played new card")
   ```

5. **Update dispatcher** in `engine/rules/common_ops.py`

6. **Add serializer** in `engine/serializers.py`:
   ```python
   def new_card_view(card: NewCardType) -> dict:
       return {"id": card.id, "name": card.name, ...}
   ```

7. **Update UI rendering** in `ui/game_client.py`

### Adding a New Game Rule

1. Create function in appropriate `engine/rules/*_ops.py` file
2. Accept player/deck objects as parameters
3. Mutate state in place
4. Add logging for debugging
5. Update dispatcher in `engine/game_engine.py` if new command type
6. Test with logging output

### Modifying Game Constants

1. Edit `resources/config.py`
2. Update `GAME_CONFIG` dict
3. No code changes needed - config is imported everywhere
4. Restart game to see changes

### Debugging UI Issues

1. Check logs for dispatch commands
2. Verify serializers return expected JSON structure
3. Use DearPyGui debug window (if available)
4. Check `refresh_zones()` is called after state changes
5. Verify card IDs match between engine and UI

---

## Important Notes for AI Assistants

### Current State of Development

**COMPLETE**:
- Core game engine architecture
- Player and deck models
- Star card play functionality
- UI rendering with DearPyGui
- Google Sheets integration
- Deck building and initialization
- Basic command dispatch system

**INCOMPLETE/STUB**:
- **Power card play logic** (`engine/rules/power_ops.py` is empty)
- **Event card system** (models exist, no game flow)
- **Fan card distribution** (cards loaded, not awarded)
- **AI player logic** (Computer player exists, no decision making)
- **Win condition checking** (10 fans, not implemented)
- **Turn system** (turn counter exists, no end-turn logic)

### Legacy Code
- **classes/** directory contains OLD architecture
- Do NOT modify files in `classes/` or `classes legacy/`
- These exist for reference only
- All new code should use `engine/` architecture

### Known Issues
- **game_engine.py:29-34**: Logic error - checks `isinstance(player, StarCard)` should check `isinstance(card, StarCard)`
- **Power card targeting**: `pending_card` system is partially implemented but unused
- **Type inconsistency**: Some functions use `Any` instead of specific model types

### Testing
- No automated tests currently exist
- Testing is manual via running `main.py`
- Check logs in console for debugging
- Visual verification through DearPyGui UI

### Dependencies (Inferred)
```
dearpygui>=1.0.0
gspread>=5.0.0
google-auth>=2.0.0
google-auth-oauthlib>=0.5.0
```
**Note**: No requirements.txt exists - dependencies must be installed manually

### Git Workflow
- Recent commits show iterative refactoring
- Commit messages are brief (e.g., "Latest", "Updates")
- No PR/issue workflow visible
- Direct commits to main branch

### When Modifying This Codebase

**DO**:
- Maintain separation between engine (logic) and UI (rendering)
- Use dataclasses for new models (no class methods)
- Write pure functions for game rules
- Add logging to new functions
- Follow existing naming conventions
- Update serializers when adding model fields
- Test via `main.py` after changes

**DON'T**:
- Mix UI code into engine modules
- Add methods to dataclass models (keep them pure data)
- Use print statements (use logging instead)
- Modify legacy `classes/` directory
- Hardcode card data (use Google Sheets)
- Raise exceptions for game logic errors (log and continue)
- Skip type hints

### File Modification Guidelines

**Safe to modify freely**:
- `engine/rules/*.py` - Add new rule functions
- `engine/serializers.py` - Add new view functions
- `resources/config.py` - Adjust game constants
- `ui/game_client.py` - UI improvements

**Modify with caution**:
- `engine/game_engine.py` - Core dispatcher (breaking changes affect everything)
- `engine/models/*.py` - Data models (changes ripple through serializers)
- `main.py` - Entry point (keep minimal)

**Do not modify**:
- `classes/**` - Legacy code
- `dearpyguitests/**` - UI experiments
- `.gitignore` - Already configured correctly
- `resources/google_service_account.json` - Credentials file

### UI Development

**DearPyGui Notes**:
- Window size: 1025x900
- Uses manual widget management (no automatic layouts in some areas)
- Cards displayed with text widgets for stats
- Buttons trigger engine.dispatch() calls
- UI refresh requires clearing old widgets and recreating

**Prototyping**:
- Use `dearpyguitests/` for UI experiments
- Test new layouts in isolation before integrating
- Reference numbered files (3.py, 4.py, etc.) for DearPyGui examples

### Google Sheets Access

**Setup Required**:
1. Google Cloud project with Sheets API enabled
2. Service account created
3. JSON key downloaded to `resources/google_service_account.json`
4. Spreadsheet shared with service account email

**Modifying Card Data**:
- Edit Google Sheets directly (no code changes needed)
- Restart `main.py` to reload cards
- Ensure column headers match loader expectations

---

## Architecture Decision Records

### Why Dataclasses Instead of Classes?

**Decision**: Use `@dataclass` for models instead of traditional classes with methods.

**Rationale**:
- Enforces separation of data (models) and behavior (rules)
- Reduces boilerplate (`__init__`, `__repr__` auto-generated)
- Type hints are mandatory, improving IDE support
- Immutability can be enforced with `frozen=True` if needed
- Easier to serialize/deserialize

### Why Functional Rules Instead of OOP Methods?

**Decision**: Game rules are pure functions in `engine/rules/`, not methods on card/player objects.

**Rationale**:
- Avoids circular dependencies (Player knows Card, Card knows Player)
- Easier to test (no complex object graphs needed)
- Game logic is centralized and discoverable
- Follows command pattern (dispatcher → functions)
- Easier to reason about state changes

### Why Google Sheets for Card Data?

**Decision**: Store card definitions in Google Sheets, not JSON/Python files.

**Rationale**:
- Non-developers (game designers) can edit cards
- No code changes needed to adjust balance
- Centralized data source (not duplicated across files)
- Easy to export/import for playtesting
- Version control via Google Sheets history

### Why DearPyGui?

**Decision**: Use DearPyGui for desktop UI instead of web frameworks or other GUI libraries.

**Rationale**:
- Immediate mode GUI (simple mental model)
- Pure Python (no HTML/CSS/JS needed)
- Fast rendering for card game needs
- Lightweight compared to Qt/Tkinter
- Good for prototyping game UIs

---

## Future Development Considerations

### Priority TODOs
1. **Implement power card play logic** (`engine/rules/power_ops.py`)
2. **Event system** - Trigger stat contests, award fans
3. **Fan distribution** - Award fans to contest winners
4. **Win condition** - Check for 10 fans, end game
5. **Turn management** - End turn, draw phase, event phase
6. **AI player** - Decision-making for Computer player

### Architectural Improvements
- Add automated tests (pytest)
- Create `requirements.txt` for dependencies
- Extract UI constants to config file
- Add error handling for Google Sheets failures
- Implement state history for undo/replay
- Add save/load game functionality

### Code Quality
- Fix type hints (`Any` → specific types)
- Add docstrings to functions
- Fix `game_engine.py` type checking bug
- Consistent error handling strategy
- Add input validation helpers

---

## Quick Reference

### Running the Game
```bash
cd /home/user/star_power
python main.py
```

### Key Imports
```python
# Models
from engine.models.cards import StarCard, PowerCard, FanCard, EventCard
from engine.models.player import Player
from engine.models.deck import Deck

# Rules
from engine.rules.star_ops import play_star_from_hand
from engine.rules.deck_ops import draw_card, shuffle_deck

# Serializers
from engine.serializers import player_view, star_card_view, deck_view

# Config
from resources.config import GAME_CONFIG
```

### Command Structure
```python
# Play a card
command = {
    "type": "PLAY_CARD",
    "payload": {
        "player": 0,      # Player index
        "hand_index": 2   # Card position in hand
    }
}
result = engine.dispatch(command)
```

### Logging Setup
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
```

---

## Contact & Resources

**Google Spreadsheet**: [Star Power Cards](https://docs.google.com/spreadsheets/d/1CuN3CzMUi3YkNAEWqDReA2UoiKqvNBYu5WA_HzlAOHQ)
**DearPyGui Docs**: [https://dearpygui.readthedocs.io/](https://dearpygui.readthedocs.io/)
**Python Dataclasses**: [https://docs.python.org/3/library/dataclasses.html](https://docs.python.org/3/library/dataclasses.html)

---

## Version History

- **2026-01-08**: Initial CLAUDE.md creation
  - Documented current architecture (engine/ui separation)
  - Identified incomplete features (power cards, events, AI)
  - Established coding conventions and workflows
