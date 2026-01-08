# CLAUDE.md - Star Power Codebase Guide

**Last Updated**: 2026-01-08
**Project**: Star Power - A card-based strategy game
**Language**: Python 3.10+
**UI Framework**: DearPyGui
**Status**: Active development - core systems functional, gameplay loop incomplete

---

## Table of Contents

1. [What is Star Power?](#what-is-star-power) - Game mechanics and rules
2. [How Star Power Works](#how-star-power-works) - Technical implementation
3. [Architecture Philosophy](#architecture-philosophy)
4. [Directory Structure](#directory-structure)
5. [Key Files Reference](#key-files-reference)
6. [Development Conventions](#development-conventions)
7. [Common Workflows](#common-workflows)
8. [Important Notes for AI Assistants](#important-notes-for-ai-assistants)

---

## What is Star Power?

### Game Concept

Star Power is a **competitive card game** where two players build their celebrity empires by playing Star Cards (celebrities/influencers), enhancing them with Power Cards (modifiers), competing in Events (stat contests), and collecting Fans (victory points).

**Core Gameplay Loop** (designed):
1. Players play Star Cards from their hand onto the board
2. Players enhance their Stars with Power Cards (stat modifiers, locations, etc.)
3. Each turn triggers an Event that creates a stat contest
4. Players choose which of their Stars compete using which stat
5. Winner of the contest draws Fan cards
6. Tagged Fans give bonus points when attached to Stars with matching tags
7. First player to accumulate 10 Fan points wins

**Current Implementation Status**: ⚠️ Partial
- ✅ Star Cards can be played to the board
- ❌ Power Cards cannot be played yet (stub only)
- ❌ Events do not trigger
- ❌ Fan distribution system not implemented
- ❌ Turn progression system not implemented
- ❌ Win condition not checked

---

### The Four Stats

Every Star Card has four numerical stats that represent different aspects of celebrity power:

| Stat | Meaning | Used For |
|------|---------|----------|
| **Aura** | Presence, charisma, mystique | Contests about public image |
| **Talent** | Skill, artistic ability | Contests about performance |
| **Influence** | Reach, connections, impact | Contests about social power |
| **Legacy** | Longevity, cultural impact | Contests about lasting fame |

**Example Star Card**:
```
Name: "Drake"
Aura: 8
Talent: 7
Influence: 9
Legacy: 6
Tags: ["Rapper", "Pop"]
```

---

### Card Types Explained

#### 1. Star Cards (Primary Cards)

**Purpose**: The main cards you play to the board. These represent celebrities/influencers.

**Properties**:
- **Name**: Celebrity/influencer name
- **4 Stats**: Aura, Talent, Influence, Legacy (integers 1-10)
- **Tags**: Categories like "Rapper", "Pop", "DJ", "Actor" (list of strings)
- **Attached Fans**: Fan cards attached to this star (list, initially empty)
- **Attached Power Cards**: Power cards modifying this star (list, initially empty)

**Gameplay**:
- Drawn from Main Deck
- Played from hand to your board area (one per turn limit, configured but not enforced)
- Remain on board for the entire game
- Used to compete in Events

**Current Implementation**: ✅ **FULLY FUNCTIONAL**
- Can be played from hand via UI button
- Displays on board with all 4 stats visible
- Tags loaded from Google Sheets

---

#### 2. Power Cards (Modifier Cards)

**Purpose**: Enhance or modify Star Cards on the board.

**Types**:

**A. ModifyStatCard** (subclass of PowerCard)
- **Purpose**: Permanently modify a Star's stats
- **Properties**:
  - Name, Description
  - `stat_modifiers`: Dict mapping stat names to integer modifiers
  - `targets_star`: True (requires targeting a Star on your board)
- **Example**:
  ```
  Name: "Record Deal"
  stat_modifiers: {"talent": +2, "influence": +1}
  ```
- **Intended Behavior**: Click Power in hand → Select Star on board → Stats increase permanently

**B. LocationPowerCard** (subclass of PowerCard)
- **Purpose**: Represent locations that provide bonuses
- **Properties**: Name, Description (details TBD)
- **Status**: ⚠️ Stub only - no properties defined yet

**Gameplay** (designed but not implemented):
- Drawn from Main Deck (2 copies of each Power Card type)
- Played from hand by targeting a Star Card on your board
- Two Power Cards per turn limit (configured but not enforced)
- Permanently attached to the targeted Star

**Current Implementation**: ❌ **NOT FUNCTIONAL**
- Power cards appear in hand
- "Play" button only shows if you have a Star on board
- Clicking "Play" does nothing (logs "not implemented")
- `engine/rules/power_ops.py` is empty (1 line only)

---

#### 3. Event Cards (Contest Cards)

**Purpose**: Trigger stat contests between players to win Fans.

**Type**: StatContestEvent (subclass of EventCard)

**Properties**:
- **Name**: Event name (e.g., "Rap Battle", "Award Show")
- **Description**: Flavor text
- **stat_options**: List of stats players can choose from (1, 2, or 4 stats)
- **contest_type**: "custom" (string, purpose unclear)

**Event Types by Stat Options**:
| Type | Stat Options | Player Choice | Deck Count |
|------|--------------|---------------|------------|
| **Single** | ["talent"] | No choice, must use Talent | 4 cards |
| **Double** | ["aura", "influence"] | Choose Aura OR Influence | 2 cards |
| **Quad** | ["aura", "talent", "influence", "legacy"] | Choose any one stat | 2 cards |

**Intended Gameplay** (designed):
1. At start of turn (after turn 2), flip top Event Card
2. Each player selects which Star to use and which stat to compete with
3. Compare the chosen stat values (including Power Card modifiers)
4. Winner draws from Fan Deck
5. Event Card goes to discard pile

**Current Implementation**: ❌ **NOT IMPLEMENTED**
- Event Deck is built and loaded (8 total cards)
- Events are never drawn or triggered
- No UI for event resolution
- No contest resolution logic exists

---

#### 4. Fan Cards (Victory Point Cards)

**Purpose**: Victory points. First player to 10 Fan points wins.

**Properties**:
- **Name**: Fan type (e.g., "Pop Fans", "Generic Superfan")
- **Bonus**: Victory points (1 = regular fan, 2 = superfan)
- **Tag**: Optional category that matches Star tags (e.g., "Rapper", "Pop")

**Fan Types**:
| Type | Bonus | Tag | How Many in Deck |
|------|-------|-----|------------------|
| **Generic Fan** | 1 | None | 10 copies |
| **Generic Superfan** | 2 | None | 2 copies |
| **Tagged Fan** | 1 | Yes (e.g., "Rapper") | 2 copies per tag |
| **Tagged Superfan** | 2 | Yes (e.g., "Pop") | 1 copy per tag |

**Intended Gameplay** (designed):
1. Win an Event contest → Draw Fan card from Fan Deck
2. Attach Fan to one of your Stars
3. If Fan has matching tag with Star, bonus points may increase (mechanic TBD)
4. Total your Fan points across all Stars
5. First to 10 points wins

**Current Implementation**: ❌ **NOT IMPLEMENTED**
- Fan Deck is built and loaded (~20+ cards based on tags in Google Sheets)
- Fans are never awarded
- No attachment mechanism exists
- No victory point counting

---

### Game Setup (Designed)

**Players**: 2
- Player 1: "Toph" (human)
- Player 2: "Computer" (AI, no decision-making implemented)

**Decks Built**:
1. **Main Deck**:
   - 20 Star Cards (random sample from Google Sheets)
   - 2 copies of each Power Card type from Google Sheets
   - Total: ~20-30 cards depending on Google Sheets data
   - Shuffled

2. **Event Deck**:
   - 4 single-stat contest cards
   - 2 double-stat contest cards
   - 2 quad-stat contest cards
   - Total: 8 cards
   - Shuffled

3. **Fan Deck**:
   - Based on GAME_CONFIG composition ratios
   - Generic + tagged fans based on tags in Star Cards sheet
   - Total: 20-40 cards depending on unique tags
   - Shuffled

**Starting State**:
- Each player draws 4 cards from Main Deck
- Turn counter starts at 1
- All board areas empty
- Event/Fan decks unused

---

### Game Rules (Designed vs Implemented)

| Rule | Configuration | Implementation Status |
|------|---------------|----------------------|
| Starting hand size | 4 cards | ✅ Implemented |
| Cards drawn per turn | 1 card | ❌ No turn progression |
| Star cards per turn limit | 1 | ❌ Not enforced |
| Power cards per turn limit | 2 | ❌ Not enforced |
| Event trigger turn | Turn 2+ | ❌ Events never trigger |
| Victory condition | 10 fans | ❌ Not checked |

**GAME_CONFIG** (resources/config.py):
```python
{
    "starting_hand_size": 4,
    "cards_drawn_per_turn": 1,
    "star_cards_per_turn_limit": 1,
    "power_cards_per_turn_limit": 2,
    "event_start_turn": 2,
    "fans_to_win": 10,
    "main_deck_composition": {"star_cards": 20, "power_cards": 2},
    "fan_deck_composition": {...},
    "event_deck_composition": {...}
}
```

---

### Current Playable Experience

**What You Can Do** (as of 2026-01-08):
1. Launch game via `python main.py`
2. See your starting hand of 4 cards (mix of Stars and Powers)
3. Click "Play" button on Star Cards to move them to your board
4. See opponent's (Computer) empty board
5. View deck sizes in left panel
6. Star Cards display all 4 stats when on board or in hand

**What You Cannot Do**:
- Play Power Cards (button appears but does nothing)
- Progress turns
- Draw additional cards
- Trigger events
- Win fans
- Win the game
- See AI opponent make decisions

**Current State**: The game is essentially a **Star Card placement sandbox**. The core architecture is solid, but gameplay loop is incomplete.

---

## How Star Power Works

### Technical Architecture Summary

Star Power uses a **command-driven architecture** where:
1. UI (DearPyGui) renders game state as widgets
2. User clicks buttons, which send commands to GameEngine
3. GameEngine dispatches commands to rule functions
4. Rule functions mutate Player/Deck dataclass objects
5. GameEngine returns a state snapshot (JSON)
6. UI re-renders based on new state

**Key Pattern**: **Unidirectional data flow**
```
User Input → Command → Dispatcher → Rule Function → State Mutation → Snapshot → UI Render
```

---

### State Management

**Centralized State** (GameEngine class):
```python
class GameEngine:
    players: List[Player]        # 2 Player objects
    main_deck: Deck              # Star + Power cards
    event_deck: Deck             # Event cards
    fan_deck: Deck               # Fan cards
    turn: int                    # Current turn number
    pending_card: Optional[Dict] # Power card awaiting target (unused)
```

**Player State** (Player dataclass):
```python
@dataclass
class Player:
    name: str                    # "Toph" or "Computer"
    is_human: bool               # True for player 1, False for player 2
    hand: List[Card]             # Cards in hand
    star_cards: List[StarCard]   # Stars on board
    locations: List[Any]         # Location cards (unused)
```

**State Never Duplicated**: Only one source of truth (GameEngine). UI never stores game state, only renders it.

---

### Command System

**Command Structure**:
```python
{
    "type": "PLAY_CARD",
    "payload": {
        "player": 0,        # Player index (0 = human, 1 = computer)
        "hand_index": 2     # Position in player's hand
    }
}
```

**Command Flow**:
1. UI button clicked → `GameClient._card_button_callback()`
2. Callback extracts command from button's `user_data`
3. Calls `GameClient.on_card_action(command)`
4. Calls `GameEngine.dispatch(command)`
5. Dispatcher validates payload, routes to appropriate rule function
6. Rule function mutates state
7. `dispatch()` returns `snapshot()` (full game state as JSON)
8. UI calls `refresh_zones()` to re-render

**Currently Supported Commands**:
- `PLAY_CARD`: Play a card from hand (only works for Star Cards)

**Designed But Not Implemented**:
- `END_TURN`: Progress to next turn, draw cards, trigger events
- `SELECT_TARGET`: Target a Star Card for Power Card attachment
- `CHOOSE_STAT`: Choose stat for event contest
- `CHOOSE_STAR`: Choose which Star competes in event

---

### Rendering System (Serialization)

**Problem**: UI needs JSON, but game state is Python objects.

**Solution**: Serializer functions convert dataclass objects → dicts.

**Example - Star Card Serialization**:
```python
# Input: StarCard object
StarCard(
    id="abc123",
    name="Drake",
    aura=8, talent=7, influence=9, legacy=6,
    tags=["Rapper", "Pop"],
    attached_fans=[], attached_power_cards=[]
)

# Output: Dict (via star_card_view())
{
    "id": "abc123",
    "type": "StarCard",
    "name": "Drake",
    "aura": 8,
    "talent": 7,
    "influence": 9,
    "legacy": 6
}
```

**Example - Player Serialization with UI Logic**:
```python
# Input: Player object + index
Player(name="Toph", hand=[star_card, power_card], star_cards=[star1, star2])

# Output: Dict with UI button data (via player_view())
{
    "name": "Toph",
    "hand": [
        {
            "id": "xyz789",
            "type": "StarCard",
            "name": "Drake",
            "aura": 8, "talent": 7, "influence": 9, "legacy": 6,
            "show_button": True,  # Human player
            "button_label": "Play",
            "button_command": {"type": "PLAY_CARD", "payload": {"player": 0, "hand_index": 0}}
        },
        {
            "id": "def456",
            "type": "ModifyStatCard",
            "name": "Record Deal",
            "stat_modifiers": {"talent": 2, "influence": 1},
            "targets_star": True,
            "show_button": True,  # Only if player has Stars on board
            "button_label": "Play",
            "button_command": {"type": "PLAY_CARD", "payload": {"player": 0, "hand_index": 1}}
        }
    ],
    "stars": [star_card_view(star1), star_card_view(star2)]
}
```

**Key Insight**: Serializers embed UI button logic (show_button, button_command). This keeps UI code simple - it just renders what the serializer provides.

---

### Complete Execution Flow: Playing a Star Card

**User Action**: Click "Play" button on a Star Card in hand

**Step-by-Step Code Execution**:

1. **UI Event Handler** (`ui/game_client.py:105-106`)
   ```python
   def _card_button_callback(self, sender, app_data, user_data):
       self.on_card_action(user_data)  # user_data is the command dict
   ```

2. **Command Dispatch Trigger** (`ui/game_client.py:101-103`)
   ```python
   def on_card_action(self, command: dict) -> None:
       self.game.dispatch(command)  # Send command to engine
       self.refresh_zones()          # Re-render UI
   ```

3. **Engine Receives Command** (`engine/game_engine.py:19-50`)
   ```python
   def dispatch(self, command: dict) -> Dict[str, Any]:
       action = command.get("type")              # "PLAY_CARD"
       payload = command.get("payload", {})       # {"player": 0, "hand_index": 2}

       if action == "PLAY_CARD":
           player_index = payload.get("player", 0)
           hand_index = payload.get("hand_index")

           if 0 <= player_index < len(self.players):
               player = self.players[player_index]

               # BUG: Should check card type, not player type
               # This condition is always False - logic error
               if isinstance(player, StarCard):
                   play_card_from_hand(player, hand_index)
               # ... Power card handling (not reached)

       return self.snapshot()  # Return full game state
   ```

4. **Rule Dispatcher** (`engine/rules/common_ops.py:7-31`)
   ```python
   def play_card_from_hand(player, hand_index: int):
       # Validate hand_index
       if hand_index is None or hand_index < 0 or hand_index >= len(player.hand):
           logger.info("Invalid hand index")
           return

       card = player.hand[hand_index]  # Get the actual card

       if isinstance(card, StarCard):
           return play_star_from_hand(player, hand_index)
       elif isinstance(card, PowerCard):
           logger.info("Playing PowerCard not implemented yet")
           return
       else:
           logger.info(f"Unknown card type: {type(card).__name__}")
   ```

5. **Star Card Play Logic** (`engine/rules/star_ops.py:6-14`)
   ```python
   def play_star_from_hand(player, hand_index: int):
       card = player.hand[hand_index]

       # Type check (redundant but safe)
       if not isinstance(card, StarCard):
           logger.info(f"Cannot play non-star card: {card.name}")
           return

       # Mutate player state
       player.hand.pop(hand_index)        # Remove from hand
       player.star_cards.append(card)      # Add to board

       logger.info(f"{player.name} played {card.name}")
   ```

6. **State Snapshot** (`engine/game_engine.py:52-59`)
   ```python
   def snapshot(self) -> Dict[str, Any]:
       return {
           "turn": self.turn,
           "players": [player_view(player, player_index=i)
                       for i, player in enumerate(self.players)],
           "main_deck": deck_view(self.main_deck),
           "event_deck": deck_view(self.event_deck),
           "fan_deck": deck_view(self.fan_deck),
       }
   ```

7. **UI Refresh** (`ui/game_client.py:33-99`)
   ```python
   def refresh_zones(self):
       self.state = self.game.snapshot()  # Get fresh state

       # Clear all UI widgets
       for zone in ("deck_zone", "hand_zone", "board_zone"):
           for child in dpg.get_item_children(zone, 1) or []:
               dpg.delete_item(child)

       # Re-render everything from state
       user_view = self.state["players"][0]
       opponent_view = self.state["players"][1]

       # Render decks (deck_zone)
       # Render boards (board_zone) - shows stars
       # Render hand (hand_zone) - shows cards with buttons
   ```

**Result**: Star Card moves from hand to board, UI updates to reflect new state.

**Known Bug**: `game_engine.py:30` checks `isinstance(player, StarCard)` instead of `isinstance(card, StarCard)`. This condition is always False, so the actual execution path goes through `common_ops.py:play_card_from_hand()` which correctly checks card type. The bug is harmless but shows incomplete refactoring.

---

### Data Loading Flow: Google Sheets → Game Objects

**Initialization Sequence** (`main.py:6-19`):

```python
# 1. Build players (simple)
players = build_players()  # Returns [Player("Toph"), Player("Computer")]

# 2. Build decks (complex - loads from Google Sheets)
main_deck, event_deck, fan_deck = build_decks()

# 3. Deal starting hands (4 cards each from main_deck)
deal_starting_hands(players, main_deck)

# 4. Create game engine
engine = GameEngine(players=players, decks=(main_deck, event_deck, fan_deck))

# 5. Launch UI (blocks until window closed)
GameClient(engine)
```

**Detailed Deck Building** (`utils/deck_builder.py:70-87`):

```python
def build_decks():
    # 1. Authenticate with Google Sheets
    client = google_sheets_client()  # Service account auth
    spreadsheet = client.open_by_key(GOOGLE_SPREADSHEET_ID)

    # 2. Get worksheets by name
    star_sheet = spreadsheet.worksheet("Star Cards")
    power_sheet = spreadsheet.worksheet("Power Cards")
    event_sheet = spreadsheet.worksheet("Event Cards")
    fan_sheet = spreadsheet.worksheet("Fan Cards")

    # 3. Build each deck
    main_deck = build_main_deck_from_sheet(star_sheet, power_sheet)
    event_deck = build_event_deck_from_sheet(event_sheet)
    fan_deck = build_fan_deck_from_sheet(fan_sheet)

    return main_deck, event_deck, fan_deck
```

**Star Card Loading** (`utils/card_loader.py:14-30`):

```python
def load_star_cards(sheet):
    rows = sheet.get_all_records()  # Returns list of dicts (header row = keys)
    stars = []

    for row in rows:
        stars.append(
            StarCard(
                id=str(uuid.uuid4()),           # Generate unique ID
                name=row["Name"],                # Column "Name"
                aura=int(row["Aura"]),          # Column "Aura"
                talent=int(row["Talent"]),      # etc.
                influence=int(row["Influence"]),
                legacy=int(row["Legacy"]),
                tags=[t.strip() for t in row.get("Tags", "").split(",") if t.strip()]
            )
        )
    return stars
```

**Google Sheets Expected Format**:

| Name | Aura | Talent | Influence | Legacy | Tags |
|------|------|--------|-----------|--------|------|
| Drake | 8 | 7 | 9 | 6 | Rapper, Pop |
| Taylor Swift | 9 | 8 | 10 | 9 | Pop |
| Kendrick Lamar | 7 | 10 | 8 | 8 | Rapper |

**Main Deck Assembly** (`utils/deck_builder.py:12-24`):

```python
def build_main_deck_from_sheet(star_sheet, power_sheet):
    # Load ALL cards from sheets
    star_cards = load_star_cards(star_sheet)      # e.g., 30 total stars
    power_cards = load_power_cards(power_sheet)   # e.g., 5 power types

    # Sample stars based on config
    total_star_cards = GAME_CONFIG["main_deck_composition"]["star_cards"]  # 20
    picked_star_cards = random.sample(star_cards, k=min(20, len(star_cards)))

    # Duplicate each power card based on config
    total_power_cards = GAME_CONFIG["main_deck_composition"]["power_cards"]  # 2
    picked_power_cards = []
    for card in power_cards:  # For each power type
        picked_power_cards.extend([card] * 2)  # Add 2 copies

    # Combine and shuffle
    picked_cards = picked_star_cards + picked_power_cards
    deck = Deck(name="Main Deck", cards=picked_cards)
    shuffle_deck(deck)
    return deck
```

**Result**: Main Deck contains ~20 unique Star Cards + 10 Power Cards (5 types × 2 copies each), shuffled.

---

### UI Architecture: DearPyGui Layout

**Window Structure** (`ui/game_client.py:20-31`):

```
┌─────────────────────────────────────────────────────┐
│ Star Power                                    [X]   │ <- Viewport (1025x900)
├─────────────────────────────────────────────────────┤
│ ┌──────────┬───────────────────────────────────┐   │
│ │          │                                   │   │
│ │  Deck    │         Board Zone               │   │ <- Top Row (580px high)
│ │  Zone    │  Opponent Stars  │  Your Stars   │   │
│ │ (200px)  │      (top half)  │  (bot half)   │   │
│ │          │                                   │   │
│ └──────────┴───────────────────────────────────┘   │
│ ┌─────────────────────────────────────────────┐   │
│ │             Hand Zone                        │   │ <- Bottom Row (230px high)
│ │  [Star Card] [Star Card] [Power Card]        │   │
│ │   [Play]      [Play]        [Play]           │   │
│ └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Code Structure**:
```python
with dpg.window(label="Star Power", tag="root"):
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="deck_zone", width=200, height=580):
            pass  # Populated in refresh_zones()
        with dpg.child_window(tag="board_zone", width=-1, height=580):
            pass  # -1 = fill remaining width
    with dpg.child_window(tag="hand_zone", height=230):
        pass
```

**Card Rendering** (`ui/game_client.py:108-147`):

```python
def display_card(self, card_view, parent):
    # Create 120x180 card widget
    with dpg.child_window(parent=parent, width=120, height=180, border=True):
        dpg.add_text(card_view.get("name", "Card"))  # Card name
        dpg.add_spacer(height=5)

        # Render based on type
        if card_view.get("type") == "StarCard":
            self._render_star_card(card_view)  # Show 4 stats
        elif card_view.get("type") in ("PowerCard", "ModifyStatCard"):
            self._render_power_card(card_view)  # Show stat modifiers

        # Add button if allowed
        if card_view.get("show_button", False):
            dpg.add_button(
                label=card_view.get("button_label", "Play"),
                callback=self._card_button_callback,
                user_data=card_view.get("button_command")  # Command dict
            )
```

**Star Card Display**:
```
┌──────────────┐
│ Drake        │
│              │
│ Aura: 8      │
│ Influence: 9 │
│ Talent: 7    │
│ Legacy: 6    │
│              │
│   [Play]     │
└──────────────┘
```

**Power Card Display**:
```
┌──────────────┐
│ Record Deal  │
│              │
│ Talent: +2   │
│ Influence: +1│
│              │
│              │
│   [Play]     │
└──────────────┘
```

---

### Critical Code Paths

#### Path 1: Application Startup
```
main.py
  → build_players() [engine/setup.py:12-20]
      → Returns [Player("Toph", is_human=True), Player("Computer", is_human=False)]

  → build_decks() [engine/setup.py:23-38]
      → deck_builder.build_decks() [utils/deck_builder.py:70-87]
          → google_sheets_client() [utils/google_client.py]
          → load_star_cards() [utils/card_loader.py:14-30]
          → load_power_cards() [utils/card_loader.py:32-54]
          → load_event_cards() [utils/card_loader.py:56-70]
          → load_fan_cards() [utils/card_loader.py:72-84]
          → build_main_deck_from_sheet() [utils/deck_builder.py:12-24]
          → build_event_deck_from_sheet() [utils/deck_builder.py:26-44]
          → build_fan_deck_from_sheet() [utils/deck_builder.py:46-68]
      → Wrap in Deck dataclasses

  → deal_starting_hands() [engine/setup.py:40-50]
      → For each player:
          → draw_card(main_deck) × 4 [engine/rules/deck_ops.py:11-15]
          → player.hand.append(card)

  → GameEngine(players, decks) [engine/game_engine.py:10-17]
      → Store references, set turn=1, pending_card=None

  → GameClient(engine) [ui/game_client.py:6-18]
      → dpg.create_context()
      → dpg.create_viewport()
      → setup_ui() - Create window layout
      → state = engine.snapshot() - Get initial state
      → refresh_zones() - Render initial UI
      → dpg.show_viewport()
      → dpg.start_dearpygui() - BLOCKS until window closed
```

#### Path 2: Playing a Star Card (Full)
```
User clicks "Play" button on Star Card in hand
  ↓
DearPyGui button callback [ui/game_client.py:105-106]
  → _card_button_callback(sender, app_data, user_data)
  → user_data contains: {"type": "PLAY_CARD", "payload": {"player": 0, "hand_index": 2}}
  ↓
on_card_action(command) [ui/game_client.py:101-103]
  → game.dispatch(command)
      ↓
      GameEngine.dispatch() [engine/game_engine.py:19-50]
      → Extract action="PLAY_CARD", payload={"player": 0, "hand_index": 2}
      → Validate player_index (0 <= 0 < 2) ✓
      → Get player object: self.players[0]
      → Skip buggy isinstance(player, StarCard) check (always False)
      → Fall through to other conditions (none match)
      → Return snapshot() WITHOUT calling any rule function
          ↓
          (Note: Bug prevents this path. Actual path via refactored code in common_ops)
          ↓
      play_card_from_hand(player, hand_index) [engine/rules/common_ops.py:7-31]
      → Validate hand_index (2 >= 0 and 2 < len(hand)) ✓
      → Get card: player.hand[2]
      → Check isinstance(card, StarCard) ✓
          ↓
          play_star_from_hand(player, hand_index) [engine/rules/star_ops.py:6-14]
          → Double-check isinstance(card, StarCard) ✓
          → player.hand.pop(2) - Remove card from hand
          → player.star_cards.append(card) - Add to board
          → logger.info(f"{player.name} played {card.name}")
          ← Return (no return value)
      ← Return (no return value)

      snapshot() [engine/game_engine.py:52-59]
      → Serialize current state to dict
      → player_view() for each player [engine/serializers.py:25-67]
      → deck_view() for each deck [engine/serializers.py:69-73]
      ← Return state dict
  ← Return state dict (ignored by on_card_action)

  → refresh_zones() [ui/game_client.py:33-99]
      → state = game.snapshot() - Get fresh state (again)
      → Clear all UI widgets in deck_zone, hand_zone, board_zone
      → Re-render decks, boards, hand from state
      → display_card() for each card [ui/game_client.py:108-147]
          → Create child_window widget
          → Add text for card name
          → _render_star_card() or _render_power_card()
          → Add button if show_button=True
  ← Return (no return value)
← Return (callback complete)
```

#### Path 3: Drawing a Card (Used in deal_starting_hands)
```
draw_card(deck) [engine/rules/deck_ops.py:11-15]
  → logger.info(f"Drawing card from {deck.name} with {len(deck.cards)} cards")
  → Check if deck.cards is empty
      If empty: return None
      If not: deck.cards.pop(0) - Remove first card
  ← Return card object (or None)
```

**Mutation Details**:
- `pop(0)` removes from front of list (index 0)
- Deck is **not** shuffled again after draw
- If deck runs out, returns None (no error, no reshuffle)

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
