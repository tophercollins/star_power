# PRD.md - Product Requirements Document

## Product Overview

**Product Name:** TTRPG Session Tracker

**One-liner:** A desktop app that records TTRPG session audio, transcribes it, and uses AI to generate summaries, extract entities, and track campaign details—helping GMs maintain consistency and never lose important details.

**Target User:** Game Masters (GMs) who run tabletop RPGs and want to:
- Keep a searchable record of all sessions
- Track NPCs, locations, items, and plot threads automatically
- Understand their players better over time
- Improve GM quality and consistency

---

## MVP Scope

### What MVP Does

1. **Campaign Management**
   - Create multiple campaigns
   - Each campaign has its own isolated database of entities
   - Campaigns have a name and game system (D&D 5e, Pathfinder, etc.)
   - System-agnostic core (D&D first, but flexible)

2. **Player & Character Management**
   - Add players (real people) to a campaign
   - Add characters linked to players
   - Pre-select which players/characters are present before each session
   - Track player preferences and play style over time

3. **Session Recording**
   - Manual start/stop recording
   - Works fully offline
   - Supports long sessions (up to 10 hours)
   - Handles variable audio environments (6-7 people in room, or online via Zoom/Discord)

4. **Transcription**
   - Local transcription using Whisper (free, offline)
   - Runs after session ends
   - Timestamps preserved for audio linking
   - Target: 99% accuracy

5. **AI Processing**
   - Queues automatically, processes when online
   - Completes within 1 minute of coming online
   - Generates:
     - Overall session summary
     - Scene-by-scene breakdowns with timestamps
     - Extracted NPCs (new and returning)
     - Extracted locations
     - Extracted items
     - Action items and plot threads
     - Player/character moments and quotes

6. **Entity Database**
   - NPCs, locations, items stored per campaign
   - Entities link to sessions where they appeared
   - All data editable

7. **Editing & Sync**
   - All outputs editable (summaries, entities, everything)
   - Changes can cascade (edit summary → entities update, edit entity → summaries adjust)
   - Auto-sync as optional toggle
   - Manual "resync" button for MVP

8. **Data Storage**
   - Raw audio files preserved (never auto-deleted)
   - Raw transcripts preserved
   - Timestamps linking transcript to audio
   - Relational data structure for future search capabilities

---

## Entity Definitions

### NPC
- Name
- Description/appearance
- Role (ally, enemy, merchant, quest giver, etc.)
- Location where first met
- Relationship to players/party
- Status (alive, dead, unknown)
- Key quotes
- Sessions appeared in

### Location
- Name
- Description
- Type (city, dungeon, tavern, wilderness, etc.)
- Notable NPCs present
- Connected locations
- Items/loot found there
- Events that happened there
- Sessions appeared in

### Item
- Name
- Description
- Type (weapon, armor, consumable, quest item, treasure, etc.)
- Current owner (player, NPC, location)
- Magical/special properties
- Where it was found
- Session it appeared in

### Player (Real Person)
- Name
- Play style and preferences
- What they enjoy
- Wrapped-style stats over time
- Characters they've played

### Character (Fictional)
- Name
- Player who plays them
- Class, race, level (flexible per system)
- Backstory summary
- Goals and motivations
- Key moments across sessions
- Memorable quotes
- Relationships with NPCs
- Character arc progression
- Wrapped-style stats

---

## User Stories

### Campaign Setup
- As a GM, I want to create a new campaign with a name and game system so I can organize my games separately.
- As a GM, I want to add players and their characters to a campaign so the app knows who's involved.

### Session Recording
- As a GM, I want to select which players/characters are present before starting a session so the AI can better attribute quotes and actions.
- As a GM, I want to hit a record button and have it capture audio for my entire session (up to 10 hours).
- As a GM, I want recording to work offline so I don't need internet at the table.
- As a GM, I want to stop recording and have transcription start automatically.

### Processing
- As a GM, I want the app to automatically process my session when I'm back online so I don't have to remember to trigger it.
- As a GM, I want processing to complete quickly (under 1 minute) so I can review outputs soon after a session.

### Reviewing Outputs
- As a GM, I want to see an overall session summary so I can quickly remember what happened.
- As a GM, I want to see scene-by-scene breakdowns so I can find specific moments.
- As a GM, I want to see extracted NPCs, locations, and items so my campaign database grows automatically.
- As a GM, I want to see action items and plot threads so I don't forget to follow up.
- As a GM, I want to see player moments and quotes so I can reward good roleplay and understand my players.

### Editing
- As a GM, I want to edit any output (summaries, entities) so I can correct mistakes.
- As a GM, I want my edits to propagate to related content so everything stays consistent.

### Viewing History
- As a GM, I want to view past sessions for a campaign so I can review what happened.
- As a GM, I want to view all NPCs/locations/items for a campaign so I can reference my world.

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Transcription accuracy | 99% |
| Processing time (once online) | < 1 minute |
| Session recording reliability | Works offline, handles 10+ hour sessions |
| Data persistence | Raw audio and transcripts never lost |

---

## Out of Scope for MVP

The following are explicitly **not** in MVP but documented for future development:

- Multiple users / accounts
- Sharing campaigns with other GMs
- Player-facing features (players viewing their character)
- Mobile app (desktop first)
- Real-time transcription during session
- Voice/speaker identification (who said what)
- VTT integrations (Roll20, Foundry, etc.)
- AI GM suggestions ("Based on last session, consider...")
- Search functionality (full-text, entity, natural language)
- Wrapped-style stats and analytics

---

## Future Features (Documented Ideas)

- **Search:** Full-text across transcripts, by entity, by session, natural language queries
- **Speaker identification:** Attribute quotes to specific players automatically
- **Real-time transcription:** See transcript as session happens
- **Mobile app:** Record from phone, sync to desktop
- **Multi-user:** Accounts, authentication, data isolation
- **Sharing:** Share campaigns or sessions with other GMs
- **Player features:** Players can view their character, add notes
- **VTT integration:** Pull data from Roll20, Foundry, etc.
- **AI suggestions:** "Last session you mentioned the thieves' guild, consider following up"
- **Wrapped stats:** Per-player and per-character statistics over time
- **Export:** Export campaign data, summaries, or full transcripts

---

## Business Model

**Approach:** SaaS subscription with API costs baked into pricing.

- **Transcription:** Free (local Whisper) - no per-session cost
- **AI Processing:** Paid API (e.g., OpenAI GPT-4o) - ~$1-2 per long session, ~$0.30-0.50 per short session
- **Pricing tiers absorb API costs** with healthy margin

| Plan | Price | Sessions/month | Est. API Cost | Margin |
|------|-------|----------------|---------------|--------|
| Hobby | $10/mo | 4 | ~$2-4 | $6-8 |
| Pro | $25/mo | 12 | ~$6-12 | $13-19 |
| Unlimited | $50/mo | 30 | ~$15-30 | $20-35 |

**Future consideration:** Self-hosted LLMs at scale to improve margins.

---

## Constraints

- **Offline-first:** Recording and transcription must work without internet
- **AI processing online:** Requires internet for LLM API calls (queues when offline)
- **Long sessions:** Must handle up to 10-hour recordings
- **Variable audio:** Must handle 6-7 people in a room or online (Zoom/Discord)

---

## Technical Constraints

- **Platform:** Desktop app first (Windows, Mac, Linux)
- **Data model:** Include user_id field now for future multi-user support
- **Storage:** Keep raw audio, raw transcript, and processed outputs
- **Relationships:** Store entity-session links with timestamps for future search
- **Schema flexibility:** Entities have flexible fields for system-agnostic support

---

## Non-Goals

- This is **not** a note-taking app (audio is the source of truth)
- This is **not** a VTT or game-running tool
- This is **not** a player-facing app (GM only for MVP)
- This is **not** a real-time tool (post-session processing)

---

## Open Questions

- Online session recording: Capture via app or use platform exports (Zoom/Discord)?
- Audio chunking strategy for 10-hour sessions?

---

## Document References

- APP_FLOW.md - User navigation and screen flows
- TECH_STACK.md - Dependencies and versions
- FRONTEND_GUIDELINES.md - Design system
- BACKEND_STRUCTURE.md - Database schema and API
- IMPLEMENTATION_PLAN.md - Build sequence
