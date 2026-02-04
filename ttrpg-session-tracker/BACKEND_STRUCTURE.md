# BACKEND_STRUCTURE.md

Database schema with every table, column, type, and relationship defined. All data is relational. Raw transcripts are immutable. Processed outputs are stored separately and can be regenerated at any time.

---

## Schema Overview

```
User (future multi-user)
  └── World
        ├── NPC
        ├── Location
        ├── Item
        └── Campaign
              ├── Player ←→ Campaign (many-to-many)
              ├── Character (belongs to Player + Campaign)
              └── Session
                    ├── SessionAudio (immutable)
                    ├── SessionTranscript (immutable)
                    ├── SessionSummary (editable, separate from transcript)
                    ├── Scene
                    ├── ActionItem
                    ├── PlayerMoment
                    └── EntityAppearance (links to NPC/Location/Item)
```

---

## Entity Relationship Diagram

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│   User   │────<│    World     │────<│   Campaign   │
└──────────┘     └──────────────┘     └──────────────┘
                        │                     │
                   ┌────┼────┐                │
                   │    │    │                │
                ┌──┴┐ ┌┴──┐ ┌┴──┐    ┌───────┴───────┐
                │NPC│ │Loc│ │Itm│    │    Session     │
                └───┘ └───┘ └───┘    └───────┬───────┘
                   │    │    │        ┌──┬──┬─┼──┬──┐
                   │    │    │        │  │  │ │  │  │
                   └────┼────┘        │  │  │ │  │  │
                        │             │  │  │ │  │  │
                 ┌──────┴──────┐      │  │  │ │  │  │
                 │  Entity     │<─────┘  │  │ │  │  │
                 │ Appearance  │         │  │ │  │  │
                 └─────────────┘         │  │ │  │  │
                                         │  │ │  │  │
              ┌──────────────────────────┘  │ │  │  │
              │  ┌─────────────────────────┘ │  │  │
              │  │  ┌────────────────────────┘  │  │
              │  │  │  ┌────────────────────────┘  │
              │  │  │  │  ┌────────────────────────┘
              ▼  ▼  ▼  ▼  ▼
           Audio Transcript Summary Scenes ActionItems PlayerMoments

┌──────────┐     ┌──────────────┐
│  Player  │────<│  Character   │
│ (global) │     │ (per campaign)│
└──────────┘     └──────────────┘
```

---

## Tables

### users

Future multi-user support. Included now so schema doesn't need migration.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique user ID |
| name | TEXT | NOT NULL | Display name |
| email | TEXT | UNIQUE | Email address |
| created_at | TEXT (ISO 8601) | NOT NULL | Account creation timestamp |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update timestamp |

**MVP:** Single hardcoded user. Schema ready for multi-user.

---

### worlds

Auto-created when first campaign is made. Hidden in UI until user has multiple campaigns in one world.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique world ID |
| user_id | TEXT (UUID) | FK → users.id, NOT NULL | Owner |
| name | TEXT | NOT NULL | World name (defaults to first campaign name) |
| description | TEXT | | World description |
| game_system | TEXT | | Default game system (D&D 5e, etc.) |
| created_at | TEXT (ISO 8601) | NOT NULL | When the world idea was born |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### campaigns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique campaign ID |
| world_id | TEXT (UUID) | FK → worlds.id, NOT NULL | Parent world |
| name | TEXT | NOT NULL | Campaign name |
| description | TEXT | | Campaign description |
| game_system | TEXT | | Game system (inherits from world if blank) |
| status | TEXT | DEFAULT 'active' | active, paused, completed |
| start_date | TEXT (ISO 8601) | | First session date (backdatable) |
| created_at | TEXT (ISO 8601) | NOT NULL | Record creation timestamp |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### players

Global/user-level. Real people who can play across campaigns.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique player ID |
| user_id | TEXT (UUID) | FK → users.id, NOT NULL | Owner (the GM) |
| name | TEXT | NOT NULL | Player's real name |
| notes | TEXT | | GM notes about play style, preferences |
| created_at | TEXT (ISO 8601) | NOT NULL | Record creation |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### campaign_players

Many-to-many link between players and campaigns.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| campaign_id | TEXT (UUID) | FK → campaigns.id, NOT NULL | Campaign |
| player_id | TEXT (UUID) | FK → players.id, NOT NULL | Player |
| joined_at | TEXT (ISO 8601) | NOT NULL | When player joined campaign |

**Unique constraint:** (campaign_id, player_id)

---

### characters

Fictional characters. Belong to a player within a campaign.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique character ID |
| player_id | TEXT (UUID) | FK → players.id, NOT NULL | Who plays this character |
| campaign_id | TEXT (UUID) | FK → campaigns.id, NOT NULL | Which campaign |
| name | TEXT | NOT NULL | Character name |
| character_class | TEXT | | Class (Fighter, Wizard, etc.) |
| race | TEXT | | Race/species |
| level | INTEGER | | Current level |
| backstory | TEXT | | Backstory (pasted or AI-extracted) |
| goals | TEXT | | Character goals/motivations |
| notes | TEXT | | GM notes on arc, progression |
| status | TEXT | DEFAULT 'active' | active, retired, dead |
| created_at | TEXT (ISO 8601) | NOT NULL | Record creation |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### sessions

One per recording session.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique session ID |
| campaign_id | TEXT (UUID) | FK → campaigns.id, NOT NULL | Parent campaign |
| session_number | INTEGER | | Session sequence number |
| title | TEXT | | Optional session title |
| date | TEXT (ISO 8601) | NOT NULL | When session occurred |
| duration_seconds | INTEGER | | Recording duration |
| status | TEXT | DEFAULT 'recording' | recording, transcribing, queued, processing, complete, error |
| created_at | TEXT (ISO 8601) | NOT NULL | Record creation |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### session_attendees

Which players/characters were present at a session.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Session |
| player_id | TEXT (UUID) | FK → players.id, NOT NULL | Player present |
| character_id | TEXT (UUID) | FK → characters.id | Character played (nullable if GM-only) |

**Unique constraint:** (session_id, player_id)

---

### session_audio

Immutable. Raw audio file references. Never modified or deleted (unless user requests for privacy).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL, UNIQUE | One audio per session |
| file_path | TEXT | NOT NULL | Local file path to audio |
| file_size_bytes | INTEGER | | File size |
| format | TEXT | | Audio format (WAV, AAC, etc.) |
| duration_seconds | INTEGER | | Audio duration |
| checksum | TEXT | | File integrity hash |
| created_at | TEXT (ISO 8601) | NOT NULL | When recorded |

**Rule:** This record is IMMUTABLE after creation.

---

### session_transcripts

Immutable. Raw transcript output from Whisper. Never modified.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Parent session |
| version | INTEGER | DEFAULT 1 | Transcript version (reprocessing creates new version) |
| raw_text | TEXT | NOT NULL | Full transcript text |
| whisper_model | TEXT | | Model used (base, small, etc.) |
| language | TEXT | DEFAULT 'en' | Detected language |
| created_at | TEXT (ISO 8601) | NOT NULL | When transcribed |

**Rule:** This record is IMMUTABLE. Reprocessing creates a new row with incremented version.

---

### transcript_segments

Timestamped segments of the transcript. Enables linking to audio positions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| transcript_id | TEXT (UUID) | FK → session_transcripts.id, NOT NULL | Parent transcript |
| segment_index | INTEGER | NOT NULL | Order in transcript |
| start_time_ms | INTEGER | NOT NULL | Start timestamp (milliseconds) |
| end_time_ms | INTEGER | NOT NULL | End timestamp (milliseconds) |
| text | TEXT | NOT NULL | Segment text |

---

### session_summaries

Editable. AI-generated, GM-editable. Stored separately from transcript.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Parent session |
| transcript_id | TEXT (UUID) | FK → session_transcripts.id | Which transcript version generated this |
| overall_summary | TEXT | | Full session summary |
| is_edited | INTEGER | DEFAULT 0 | Whether GM has edited (0/1) |
| created_at | TEXT (ISO 8601) | NOT NULL | When generated |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last edit |

---

### scenes

AI-identified scenes within a session. Editable.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Parent session |
| scene_index | INTEGER | NOT NULL | Order in session |
| title | TEXT | | Scene title |
| summary | TEXT | | Scene description |
| start_time_ms | INTEGER | | Start timestamp |
| end_time_ms | INTEGER | | End timestamp |
| is_edited | INTEGER | DEFAULT 0 | Whether GM has edited |
| created_at | TEXT (ISO 8601) | NOT NULL | When generated |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last edit |

---

### npcs

World-level entities. Shared across campaigns in the same world.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique NPC ID |
| world_id | TEXT (UUID) | FK → worlds.id, NOT NULL | Parent world |
| copied_from_id | TEXT (UUID) | FK → npcs.id | If copied from another world |
| name | TEXT | NOT NULL | NPC name |
| description | TEXT | | Appearance/description |
| role | TEXT | | ally, enemy, merchant, quest_giver, neutral, etc. |
| status | TEXT | DEFAULT 'alive' | alive, dead, unknown, missing |
| notes | TEXT | | GM notes |
| is_edited | INTEGER | DEFAULT 0 | Whether GM has edited |
| created_at | TEXT (ISO 8601) | NOT NULL | When first extracted |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### locations

World-level entities.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique location ID |
| world_id | TEXT (UUID) | FK → worlds.id, NOT NULL | Parent world |
| copied_from_id | TEXT (UUID) | FK → locations.id | If copied from another world |
| name | TEXT | NOT NULL | Location name |
| description | TEXT | | Location description |
| location_type | TEXT | | city, dungeon, tavern, wilderness, etc. |
| parent_location_id | TEXT (UUID) | FK → locations.id | Connected/parent location |
| notes | TEXT | | GM notes |
| is_edited | INTEGER | DEFAULT 0 | Whether GM has edited |
| created_at | TEXT (ISO 8601) | NOT NULL | When first extracted |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### items

World-level entities.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique item ID |
| world_id | TEXT (UUID) | FK → worlds.id, NOT NULL | Parent world |
| copied_from_id | TEXT (UUID) | FK → items.id | If copied from another world |
| name | TEXT | NOT NULL | Item name |
| description | TEXT | | Item description |
| item_type | TEXT | | weapon, armor, consumable, quest_item, treasure, etc. |
| properties | TEXT | | Magical/special properties |
| current_owner_type | TEXT | | player_character, npc, location |
| current_owner_id | TEXT (UUID) | | FK to character, NPC, or location |
| notes | TEXT | | GM notes |
| is_edited | INTEGER | DEFAULT 0 | Whether GM has edited |
| created_at | TEXT (ISO 8601) | NOT NULL | When first extracted |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### entity_appearances

Links entities (NPCs, locations, items) to sessions where they appeared. Many-to-many with context.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Session appeared in |
| entity_type | TEXT | NOT NULL | npc, location, item |
| entity_id | TEXT (UUID) | NOT NULL | ID of the entity |
| context | TEXT | | Brief description of appearance/role in session |
| first_appearance | INTEGER | DEFAULT 0 | Was this the first time? (0/1) |
| timestamp_ms | INTEGER | | Approximate timestamp in session |
| created_at | TEXT (ISO 8601) | NOT NULL | When extracted |

**Index:** (session_id, entity_type, entity_id)

---

### npc_relationships

Relationships between NPCs and player characters.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| npc_id | TEXT (UUID) | FK → npcs.id, NOT NULL | NPC |
| character_id | TEXT (UUID) | FK → characters.id, NOT NULL | Player character |
| relationship | TEXT | | Description of relationship |
| sentiment | TEXT | | friendly, hostile, neutral, unknown |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### npc_quotes

Key quotes from NPCs extracted from sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| npc_id | TEXT (UUID) | FK → npcs.id, NOT NULL | NPC who said it |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Session it was said in |
| quote_text | TEXT | NOT NULL | The quote |
| context | TEXT | | Context around the quote |
| timestamp_ms | INTEGER | | When in the session |
| created_at | TEXT (ISO 8601) | NOT NULL | When extracted |

---

### action_items

Plot threads and action items. Can track status across sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Session extracted from |
| campaign_id | TEXT (UUID) | FK → campaigns.id, NOT NULL | Parent campaign |
| title | TEXT | NOT NULL | Brief description |
| description | TEXT | | Detailed description |
| action_type | TEXT | | plot_thread, action_item, follow_up, hook |
| status | TEXT | DEFAULT 'open' | open, in_progress, resolved, dropped |
| resolved_session_id | TEXT (UUID) | FK → sessions.id | Session where resolved |
| is_edited | INTEGER | DEFAULT 0 | Whether GM has edited |
| created_at | TEXT (ISO 8601) | NOT NULL | When extracted |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### player_moments

Player/character highlights per session.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Session it happened in |
| player_id | TEXT (UUID) | FK → players.id, NOT NULL | Player |
| character_id | TEXT (UUID) | FK → characters.id | Character (if applicable) |
| moment_type | TEXT | | quote, combat, roleplay, decision, funny, dramatic |
| description | TEXT | NOT NULL | What happened |
| quote_text | TEXT | | Direct quote if applicable |
| timestamp_ms | INTEGER | | When in the session |
| is_edited | INTEGER | DEFAULT 0 | Whether GM has edited |
| created_at | TEXT (ISO 8601) | NOT NULL | When extracted |
| updated_at | TEXT (ISO 8601) | NOT NULL | Last update |

---

### processing_queue

Tracks sessions waiting for AI processing. Enables offline-first queue.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| session_id | TEXT (UUID) | FK → sessions.id, NOT NULL | Session to process |
| status | TEXT | DEFAULT 'pending' | pending, processing, complete, error |
| error_message | TEXT | | Error details if failed |
| attempts | INTEGER | DEFAULT 0 | Number of processing attempts |
| created_at | TEXT (ISO 8601) | NOT NULL | When queued |
| started_at | TEXT (ISO 8601) | | When processing began |
| completed_at | TEXT (ISO 8601) | | When processing finished |

---

### campaign_imports

Tracks imported text that was processed for entity extraction (campaign creation imports).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique ID |
| campaign_id | TEXT (UUID) | FK → campaigns.id, NOT NULL | Campaign imported into |
| raw_text | TEXT | NOT NULL | Original imported text (immutable) |
| status | TEXT | DEFAULT 'pending' | pending, processing, complete, error |
| created_at | TEXT (ISO 8601) | NOT NULL | When imported |
| processed_at | TEXT (ISO 8601) | | When AI finished processing |

---

## Immutability Rules

| Table | Immutable? | Notes |
|-------|-----------|-------|
| session_audio | YES | Raw audio never modified. Delete only for privacy. |
| session_transcripts | YES | Reprocessing creates new version row. |
| transcript_segments | YES | Tied to transcript version. |
| campaign_imports | YES (raw_text) | Original import text never modified. |
| All other tables | NO | Editable by GM. `is_edited` flag tracks changes. |

---

## Data Storage Rules

### Audio Files
- Stored locally via `path_provider`
- Path: `{app_data}/audio/{session_id}.{format}`
- Never auto-deleted
- Future: backup to Supabase Storage / Cloudflare R2

### Transcripts
- Stored in SQLite (session_transcripts table)
- Versioned: reprocessing creates new row with incremented version
- Raw text preserved, never overwritten

### Processed Outputs
- All in SQLite relational tables
- Each has `is_edited` flag
- Each has `created_at` and `updated_at`
- Can be regenerated from transcript at any time

---

## Reprocessing Flow

When user triggers reprocess (or better LLM becomes available):

1. Take latest `session_transcripts` version (or create new version if retranscribing)
2. Run through LLM processing pipeline
3. Create new rows for: summary, scenes, entity appearances, action items, player moments
4. Mark old processed outputs as superseded (or replace, user choice)
5. Entities (NPCs, locations, items) are **updated**, not duplicated
6. GM edits on entities are preserved (AI won't overwrite `is_edited = 1` fields)

---

## Edit Cascade Logic (MVP)

When GM edits content:

1. **Edit entity (NPC/location/item)** → set `is_edited = 1`, update fields
2. **Press "Resync"** → LLM re-examines summaries referencing that entity, proposes updates
3. **Edit summary** → set `is_edited = 1`, update text
4. **Press "Resync"** → LLM re-examines entities mentioned in edited summary, proposes updates
5. **Auto-sync toggle (future)** → cascade happens automatically without Resync button

---

## Sync to Supabase (Future)

For multi-user / multi-device support:

| Local (SQLite) | Cloud (Supabase Postgres) |
|----------------|--------------------------|
| Primary data store | Backup + sync |
| Works offline | Requires internet |
| Source of truth | Eventually consistent |

**Sync strategy:** Last-write-wins with conflict detection. Detailed sync protocol TBD.

---

## API Key Storage

| Key | Storage Method |
|-----|---------------|
| Gemini API Key | Flutter secure storage (`flutter_secure_storage`) |
| Supabase Keys | Environment variables / secure storage |
| Resend Key | Server-side only (never on client) |

---

## Indexes

```sql
-- Performance indexes for common queries
CREATE INDEX idx_campaigns_world ON campaigns(world_id);
CREATE INDEX idx_sessions_campaign ON sessions(campaign_id);
CREATE INDEX idx_npcs_world ON npcs(world_id);
CREATE INDEX idx_locations_world ON locations(world_id);
CREATE INDEX idx_items_world ON items(world_id);
CREATE INDEX idx_entity_appearances_session ON entity_appearances(session_id);
CREATE INDEX idx_entity_appearances_entity ON entity_appearances(entity_type, entity_id);
CREATE INDEX idx_action_items_campaign ON action_items(campaign_id);
CREATE INDEX idx_action_items_status ON action_items(status);
CREATE INDEX idx_player_moments_session ON player_moments(session_id);
CREATE INDEX idx_player_moments_player ON player_moments(player_id);
CREATE INDEX idx_processing_queue_status ON processing_queue(status);
CREATE INDEX idx_transcript_segments_transcript ON transcript_segments(transcript_id);
```

---

## Document References

- PRD.md - Feature requirements and entity definitions
- APP_FLOW.md - User navigation and screen flows
- TECH_STACK.md - Dependencies and versions
- FRONTEND_GUIDELINES.md - Design system
- IMPLEMENTATION_PLAN.md - Build sequence
