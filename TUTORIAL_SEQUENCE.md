# Star Power - Tutorial Learning Sequence

**Purpose**: Progressive feature introduction to onboard new players from simple to complex gameplay.

---

## Phase 1: Core Mechanics (IMPLEMENTED)
**Goal**: Learn basic gameplay loop and win condition

### Features Active:
- ✅ Star Cards with 4 stats (Aura, Talent, Influence, Legacy)
- ✅ Power Cards that boost star stats permanently
- ✅ Simple single-stat event contests (highest stat wins)
- ✅ Fan cards as victory points
- ✅ First to 5 fans wins
- ✅ Turn-based play (1 star, 1 power per turn)
- ✅ Turn order rotation (different player starts each turn)
- ✅ Event visible before playing cards (strategic planning)

### Tutorial Steps:
1. **Card Types**: Show hand with Star and Power cards
2. **Playing Cards**: Play a Star to your board
3. **Boosting Stars**: Play a Power card on your Star
4. **Events**: Event card appears - select your Star to compete
5. **Winning Fans**: Win contest, get fan attached to Star
6. **Victory**: First to 5 fans wins!

### What Players Learn:
- Star stats determine event outcomes
- Power cards make stars stronger
- Event selection is part of your turn
- Fans accumulate on individual stars
- Basic strategic decision: which star to buff vs which to compete with

**Estimated Play Time**: 5-10 minutes per game

---

## Phase 2: Resource Management (IMPLEMENTED)
**Goal**: Prevent "spam one star" optimal strategy

### New Feature Added:
- ✅ **Star Exhaustion**: Stars that compete in an event become exhausted
  - Exhausted stars skip the NEXT event (one full cycle)
  - Forces players to maintain multiple viable stars
  - Visual indicator: grayed out with 😴 badge

### Tutorial Steps:
1. Recap Phase 1 basics
2. **Exhaustion Intro**: Win an event → Star becomes exhausted
3. **Waiting Period**: Show exhausted star can't compete next event
4. **Recovery**: After missing one event, star refreshes
5. **Strategic Depth**: Build multiple stars to always have options

### What Players Learn:
- Can't rely on one star all game
- Need to spread power cards across stars
- Timing decisions: when to use your best star
- Board presence matters (need multiple stars)

**New Strategic Considerations**:
- Do I buff one star heavily or spread buffs?
- When do I commit my strongest star to an event?
- How many stars should I maintain on the board?

**Estimated Play Time**: 8-12 minutes per game

---

## Phase 3: [PLANNED - NOT YET IMPLEMENTED]
**Goal**: TBD - Add another layer of strategy

### Potential Features to Add:
- **Board Limits**: Max 3 stars on board (forces tough choices)
- **Debuff/Negative Power Cards**: Can target opponent's stars
- **Tag-Based Bonuses**: Matching fan tags to star tags for bonus points
- **Event Preview**: See next 2 events (planning ahead)
- **Multi-Star Events**: Some events require 2 stars to participate
- **Risk/Reward Events**: Higher stakes - winner gets +2 fans, loser gets -1

### Tutorial Steps:
[To be designed based on which feature is chosen]

### What Players Learn:
[To be designed]

---

## Phase 4: [PLANNED - NOT YET IMPLEMENTED]
**Goal**: TBD

### Features:
[To be designed]

---

## Design Principles for Tutorial Progression

1. **Incremental Complexity**: Each phase adds ONE major mechanic
2. **Build on Previous**: New mechanics modify/extend existing ones, not replace
3. **Interactive Learning**: Tutorial via actual gameplay, not text walls
4. **Quick Wins**: Phase 1 should be completable in <10 minutes
5. **Strategic Depth**: Each phase should introduce new decision points
6. **No Overwhelming**: Maximum 3 new concepts per phase

---

## Implementation Checklist

When adding a new tutorial phase:

- [ ] Design the mechanic
- [ ] Implement backend logic
- [ ] Update frontend UI
- [ ] Create tutorial overlay/prompts for new feature
- [ ] Add visual indicators for new mechanic state
- [ ] Playtest with new players
- [ ] Update this document with actual tutorial steps
- [ ] Consider "skip tutorial" option for returning players

---

## Current Status

**Completed Phases**:
- Phase 1: Core Mechanics ✅
- Phase 2: Resource Management (Star Exhaustion) ✅

**Next Phase**: To be decided

**Player Feedback Needed**:
- Is 5 fans the right win condition?
- Is exhaustion penalty (miss one event) too harsh/lenient?
- What mechanics cause confusion?
- What strategic depth is missing?

---

## Version History

- **2026-01-20**: Created tutorial sequence doc
  - Documented Phase 1 (Core Mechanics) - implemented
  - Documented Phase 2 (Star Exhaustion) - implemented
  - Outlined potential Phase 3 features
