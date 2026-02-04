# IMPLEMENTATION_PLAN.md

Step-by-step build sequence. Each step is small, specific, and references the relevant doc. The more steps, the less AI guesses.

---

## Build Phases

| Phase | Name | Goal |
|-------|------|------|
| 1 | Project Setup | Flutter project, dependencies, folder structure |
| 2 | Theme & Navigation | App shell, theming, routing |
| 3 | Database | SQLite schema, models, data access layer |
| 4 | Campaign Management | Create, view, edit campaigns |
| 5 | Player & Character Management | Add players/characters to campaigns |
| 6 | Audio Recording | Record, stop, save audio files |
| 7 | Local Transcription | Whisper integration, transcript storage |
| 8 | AI Processing | LLM pipeline, entity extraction, summaries |
| 9 | Session Review | Display processed session, 4-section drill-down |
| 10 | Editing & Resync | Inline editing, cascade resync |
| 11 | World Database | Browse all entities across campaign |
| 12 | Processing Queue | Offline queue, auto-process when online |
| 13 | Notifications | Email notification on processing complete |
| 14 | Onboarding | First-time user guided walkthrough |
| 15 | Polish & Testing | Bug fixes, performance, edge cases |

---

## Phase 1: Project Setup

**Reference:** TECH_STACK.md

### 1.1 Initialize Flutter project
- Run `flutter create ttrpg_session_tracker`
- Verify it builds and runs on desktop (Windows/Mac/Linux)

### 1.2 Configure pubspec.yaml
- Add dependencies per TECH_STACK.md:
  - `sqflite: ^2.3.0`
  - `sqflite_common_ffi: ^2.3.0`
  - `path_provider: ^2.1.0`
  - `record: ^5.0.0`
  - `supabase_flutter: ^2.0.0`
  - `flutter_riverpod: ^2.5.0`
  - `uuid: ^4.0.0`
  - `flutter_secure_storage: ^9.0.0`
- Run `flutter pub get`
- Verify build succeeds

### 1.3 Create folder structure
- Per FRONTEND_GUIDELINES.md file structure:
```
lib/
  main.dart
  app.dart
  ui/
    screens/
    widgets/
    theme/
  data/
    database/
    models/
    repositories/
  services/
    audio/
    transcription/
    processing/
    notifications/
  providers/
  utils/
```

### 1.4 Configure .gitignore
- Add Flutter defaults
- Add `.env` and API key files
- Add audio files directory (optional, large files)

### 1.5 Set up environment config
- Create env loading for API keys (Gemini, Supabase)
- Use `flutter_secure_storage` for local key storage
- Never hardcode keys

---

## Phase 2: Theme & Navigation

**Reference:** FRONTEND_GUIDELINES.md, APP_FLOW.md

### 2.1 Define color constants
- Create `lib/ui/theme/colors.dart`
- Define light mode palette per FRONTEND_GUIDELINES.md
- Define dark mode palette per FRONTEND_GUIDELINES.md
- Define status colors (recording, processing, complete, queued)

### 2.2 Define spacing constants
- Create `lib/ui/theme/spacing.dart`
- Define spacing scale: xxs (2px) through 3xl (64px)

### 2.3 Define typography
- Create `lib/ui/theme/typography.dart`
- Define text styles: xs, sm, base, lg, xl, 2xl
- System fonts only (no custom font loading)

### 2.4 Build app theme
- Create `lib/ui/theme/app_theme.dart`
- Build `ThemeData` for light mode
- Build `ThemeData` for dark mode
- Set `themeMode: ThemeMode.system`

### 2.5 Set up routing
- Define routes per APP_FLOW.md screen inventory
- Use Flutter's `GoRouter` or Navigator 2.0
- Routes:
  - `/` → Home
  - `/onboarding` → Onboarding
  - `/campaigns` → Campaigns List
  - `/campaigns/new` → New Campaign
  - `/campaigns/:id` → Campaign Home
  - `/campaigns/:id/sessions/new` → Session Setup
  - `/campaigns/:id/sessions/:sessionId/record` → Recording
  - `/campaigns/:id/sessions/:sessionId/complete` → Post-Session
  - `/campaigns/:id/sessions/:sessionId` → Session Detail
  - `/campaigns/:id/sessions/:sessionId/summary` → Session Summary
  - `/campaigns/:id/sessions/:sessionId/entities` → Extracted Items
  - `/campaigns/:id/sessions/:sessionId/actions` → What's Next
  - `/campaigns/:id/sessions/:sessionId/players` → Player Moments
  - `/campaigns/:id/world` → World Database
  - `/campaigns/:id/players` → Players/Characters

### 2.6 Build app shell
- Create `lib/app.dart` with `MaterialApp.router`
- Sidebar navigation for desktop (collapsible)
- Breadcrumb component for sub-pages
- Back button on all drill-down pages

### 2.7 Create placeholder screens
- Create empty screen widget for every route
- Each displays its name and route for verification
- Verify all navigation paths work

---

## Phase 3: Database

**Reference:** BACKEND_STRUCTURE.md

### 3.1 Set up SQLite database helper
- Create `lib/data/database/database_helper.dart`
- Initialize SQLite with `sqflite_common_ffi` for desktop
- Handle database creation, versioning, migrations

### 3.2 Create all tables
- Implement `onCreate` with all tables from BACKEND_STRUCTURE.md:
  - `users`
  - `worlds`
  - `campaigns`
  - `players`
  - `campaign_players`
  - `characters`
  - `sessions`
  - `session_attendees`
  - `session_audio`
  - `session_transcripts`
  - `transcript_segments`
  - `session_summaries`
  - `scenes`
  - `npcs`
  - `locations`
  - `items`
  - `entity_appearances`
  - `npc_relationships`
  - `npc_quotes`
  - `action_items`
  - `player_moments`
  - `processing_queue`
  - `campaign_imports`

### 3.3 Create indexes
- Add all indexes from BACKEND_STRUCTURE.md
- Verify query performance on key lookups

### 3.4 Create Dart model classes
- Create `lib/data/models/` with one file per entity:
  - `user.dart`
  - `world.dart`
  - `campaign.dart`
  - `player.dart`
  - `character.dart`
  - `session.dart`
  - `session_audio.dart`
  - `session_transcript.dart`
  - `transcript_segment.dart`
  - `session_summary.dart`
  - `scene.dart`
  - `npc.dart`
  - `location.dart`
  - `item.dart`
  - `entity_appearance.dart`
  - `action_item.dart`
  - `player_moment.dart`
- Each model has: `fromMap()`, `toMap()`, fields matching schema

### 3.5 Create repository layer
- Create `lib/data/repositories/` with one repo per domain:
  - `campaign_repository.dart` (campaigns + worlds)
  - `player_repository.dart` (players + characters)
  - `session_repository.dart` (sessions + audio + transcripts)
  - `entity_repository.dart` (NPCs, locations, items)
  - `action_item_repository.dart`
  - `player_moment_repository.dart`
- Each repo handles CRUD operations for its domain
- All database access goes through repositories (never direct SQL in UI)

### 3.6 Seed default user
- Create hardcoded MVP user on first launch
- Insert into `users` table
- Store user_id for all subsequent operations

### 3.7 Create Riverpod providers for repositories
- Create `lib/providers/` with providers for each repository
- UI accesses data through providers only

---

## Phase 4: Campaign Management

**Reference:** APP_FLOW.md Flow 2, Flow 3

### 4.1 Build Home screen
- Three options: Continue Campaign, New Campaign, Review/Stats/Edit
- Simple layout per FRONTEND_GUIDELINES.md

### 4.2 Build Campaigns List screen
- Fetch all campaigns from `campaign_repository`
- Display as list with: name, game system, status, session count
- Tap → navigate to Campaign Home

### 4.3 Build New Campaign form
- Fields: name (required), game system, description
- Import/paste text area (optional)
- Auto-create World with same name on save
- Save → navigate to Campaign Home

### 4.4 Build Campaign Home screen
- Display campaign name, game system, description
- Sections/links to: Sessions, World Database, Players/Characters
- Layout TBD (start with simple vertical sections, iterate)
- "New Session" / "Record" button prominent

### 4.5 Campaign import processing
- If import text provided during creation:
  - Store in `campaign_imports` table (immutable)
  - Add to `processing_queue`
  - Process when online (Phase 8)

---

## Phase 5: Player & Character Management

**Reference:** APP_FLOW.md Flow 4

### 5.1 Build Players/Characters screen
- List all players in campaign with their characters
- "Add Player" and "Add Character" buttons

### 5.2 Build Add Player form
- Field: name
- Save to `players` table + `campaign_players` link

### 5.3 Build Add Character form
- Select player (dropdown)
- Fields: character name, class (optional), race (optional), level (optional)
- Backstory text area (optional)
- Save to `characters` table

### 5.4 Player/Character editing
- Tap player/character → view detail
- Edit button → inline editing
- Save updates to database

---

## Phase 6: Audio Recording

**Reference:** PRD.md Session Recording, APP_FLOW.md Flow 5

### 6.1 Build Session Setup screen
- Display all players/characters in campaign
- Checkboxes to select who's present
- "Start Recording" button
- Create `sessions` row on start (status: recording)
- Create `session_attendees` rows for selected players/characters

### 6.2 Build Recording screen
- Elapsed timer (HH:MM:SS)
- Stop button
- Recording indicator (red pulsing dot)
- Initialize `record` package for audio capture
- Save to local file: `{app_data}/audio/{session_id}.wav`

### 6.3 Handle long recordings
- Test with extended recordings (simulate 10 hours)
- Implement chunked writing if needed (avoid memory issues)
- Periodic file flush to prevent data loss

### 6.4 Build Post-Session screen
- On stop: save `session_audio` record
- Display: session duration, date/time
- Update session status to `transcribing`
- Show status indicator

### 6.5 Handle recording errors
- Catch audio permission errors
- Catch disk full errors
- Log errors, show user-friendly message

---

## Phase 7: Local Transcription

**Reference:** TECH_STACK.md Transcription section

### 7.1 Integrate whisper.cpp
- Evaluate `whisper_flutter_new` package
- If insufficient: build custom FFI bindings to whisper.cpp
- Bundle base model (~150MB) with app or download on first use

### 7.2 Build transcription service
- Create `lib/services/transcription/transcription_service.dart`
- Accept audio file path, return transcript with timestamps
- Run in isolate (background thread, don't block UI)

### 7.3 Implement audio chunking
- Split long audio into processable chunks (e.g., 30-minute segments)
- Transcribe chunks sequentially
- Merge results with correct timestamp offsets

### 7.4 Store transcript
- Save to `session_transcripts` table (version 1)
- Save segments to `transcript_segments` with timestamps
- Update session status to `queued` (waiting for AI processing)
- Mark as immutable (no further edits to this record)

### 7.5 Test transcription accuracy
- Record sample sessions
- Compare transcription output to actual speech
- Tune model size (base vs small) based on quality/speed tradeoff

---

## Phase 8: AI Processing

**Reference:** PRD.md AI Processing, BACKEND_STRUCTURE.md

### 8.1 Build LLM service
- Create `lib/services/processing/llm_service.dart`
- Implement Gemini Flash API client
- Build provider interface (abstract class) so LLM can be swapped later
- Handle API key from secure storage

### 8.2 Design prompt templates
- Session summary prompt
- Scene identification prompt
- Entity extraction prompt (NPCs, locations, items)
- Action items / plot threads prompt
- Player moments prompt
- Include session attendees list in context for better attribution

### 8.3 Build processing pipeline
- Create `lib/services/processing/session_processor.dart`
- Pipeline steps:
  1. Load transcript from DB
  2. Load existing campaign entities (for matching returning NPCs)
  3. Load session attendees
  4. Call LLM: generate overall summary → `session_summaries`
  5. Call LLM: identify scenes → `scenes`
  6. Call LLM: extract entities → `npcs`, `locations`, `items` + `entity_appearances`
  7. Call LLM: extract action items → `action_items`
  8. Call LLM: extract player moments → `player_moments`
  9. Update session status to `complete`

### 8.4 Handle entity matching
- When LLM extracts an NPC, check if name matches existing NPC in world
- If match: create `entity_appearance` linking to existing entity, update entity if new info
- If new: create new entity record
- Same logic for locations and items
- Respect `is_edited` flag (don't overwrite GM edits)

### 8.5 Handle transcript chunking for LLM
- Long transcripts may exceed context window
- Split into chunks with overlap
- Process chunks sequentially, merge results
- Deduplicate entities across chunks

### 8.6 Handle campaign imports
- Same processing pipeline but for pasted text instead of transcript
- Extract entities from imported text
- Store in world database

### 8.7 Test with sample transcripts
- Create sample TTRPG transcripts
- Run through pipeline
- Verify entity extraction accuracy
- Iterate on prompts

---

## Phase 9: Session Review

**Reference:** APP_FLOW.md Flow 7

### 9.1 Build Session Detail screen
- Four sections with preview info:
  - Session Summary (snippet)
  - Extracted Items (NPC/location/item counts)
  - What's Next (action items snippet)
  - Player Moments (highlights snippet)
- Each section: preview content + "View more" to drill down

### 9.2 Build Session Summary drill-down
- New page: full overall summary
- Scene-by-scene breakdowns with timestamps
- Edit button on each section
- Back to Session Detail

### 9.3 Build Extracted Items drill-down
- New page: lists of NPCs, locations, items
- Each entity shows key info (name, description, role/type)
- Edit button on each entity
- Back to Session Detail

### 9.4 Build What's Next drill-down
- New page: action items and plot threads
- Each item shows: title, description, type, status
- Edit button on each
- Back to Session Detail

### 9.5 Build Player Moments drill-down
- New page: per-player breakdown
- Quotes, highlights, memorable moments
- Edit button on each
- Back to Session Detail

### 9.6 Build Past Sessions list
- From Campaign Home → Sessions
- List all sessions: number, date, summary snippet, status badge
- Tap → Session Detail

---

## Phase 10: Editing & Resync

**Reference:** PRD.md Editing & Sync, BACKEND_STRUCTURE.md Edit Cascade Logic

### 10.1 Build inline editing
- Edit button (pencil icon) on all editable content
- Tap → content becomes editable text field
- Save/Cancel buttons appear
- Save → update database, set `is_edited = 1`

### 10.2 Build Resync functionality
- "Resync" button on session detail pages
- On press:
  1. Collect all edited content for this session
  2. Send to LLM with context: "These edits were made, update related content"
  3. Update summaries that reference edited entities
  4. Update entities mentioned in edited summaries
  5. Preserve `is_edited` fields (don't overwrite user changes)

### 10.3 Test edit cascade
- Edit an NPC name → resync → verify summaries update
- Edit a summary → resync → verify entities update
- Verify `is_edited` protection works

---

## Phase 11: World Database

**Reference:** APP_FLOW.md Flow 8

### 11.1 Build World Database screen
- From Campaign Home → World Database
- Display all entities for world:
  - NPCs section
  - Locations section
  - Items section
- Each entity: name, key info, session count

### 11.2 Build entity detail view
- Tap entity → full detail page
- All fields from BACKEND_STRUCTURE.md entity tables
- Sessions appeared in (with links)
- Related entities (NPCs at location, items owned by NPC, etc.)
- Edit button → inline editing

### 11.3 Build NPC relationships view
- Show NPC → character relationships
- Show quotes
- Show appearance history across sessions

---

## Phase 12: Processing Queue

**Reference:** BACKEND_STRUCTURE.md processing_queue

### 12.1 Build queue manager
- Create `lib/services/processing/queue_manager.dart`
- Monitor `processing_queue` table
- Check network connectivity
- When online: process pending items sequentially

### 12.2 Implement connectivity monitoring
- Listen for network state changes
- On reconnect: trigger queue processing
- Show connectivity status in UI (subtle indicator)

### 12.3 Handle processing errors
- Log errors to `processing_queue.error_message`
- Increment `attempts`
- Retry with backoff (max 3 attempts)
- Show error status in session list

### 12.4 Background processing
- Processing runs in isolate (background)
- UI remains responsive
- Progress indicator on session card

---

## Phase 13: Notifications

**Reference:** APP_FLOW.md Flow 6

### 13.1 Set up Resend integration
- Create `lib/services/notifications/email_service.dart`
- Configure Resend API (server-side or direct API call)
- Email template: "Your session has been processed"
- Include link to session detail (deep link for future)

### 13.2 Trigger email on processing complete
- After successful processing pipeline
- Send email with session summary preview
- Handle email failures gracefully (log, don't block)

### 13.3 In-app status updates
- Session card shows current status badge
- Status updates in real-time as processing progresses
- "Ready to review" state clearly visible

---

## Phase 14: Onboarding

**Reference:** APP_FLOW.md Flow 1

### 14.1 Detect first launch
- Check local storage for `has_completed_onboarding` flag
- If false → show onboarding
- If true → show Home screen

### 14.2 Build onboarding flow
- Welcome screen: brief intro to app
- Feature highlights: record → transcribe → insights (3 steps)
- Call to action: "Create your first campaign" or "Skip"
- Apply engagement science: quick to value, not overwhelming

### 14.3 Connect onboarding to campaign creation
- "Create campaign" from onboarding → New Campaign form
- On complete → Campaign Home
- Set `has_completed_onboarding = true`

---

## Phase 15: Polish & Testing

### 15.1 Performance testing
- Test with 10-hour audio files
- Test with large campaign (50+ sessions, 100+ entities)
- Profile memory usage during recording
- Profile database query performance

### 15.2 Error handling pass
- Review all user-facing operations
- Add error messages for common failures
- Ensure no unhandled exceptions crash the app

### 15.3 UI polish
- Verify dark mode and light mode look correct on all screens
- Check spacing and typography consistency
- Verify all edit buttons work
- Test all navigation paths from APP_FLOW.md

### 15.4 Data integrity
- Verify immutable records can't be modified
- Verify `is_edited` flags work correctly
- Verify entity matching (returning NPCs) works
- Verify world-level entity sharing across campaigns

### 15.5 Desktop platform testing
- Test on Windows
- Test on macOS
- Test on Linux
- Fix platform-specific issues

### 15.6 Delete functionality
- Implement delete for campaigns, sessions, entities
- Confirmation dialogs
- Hard delete for privacy compliance

---

## Build Order Dependencies

```
Phase 1 (Setup)
  ↓
Phase 2 (Theme & Navigation)
  ↓
Phase 3 (Database)
  ↓
Phase 4 (Campaigns) ←→ Phase 5 (Players) [can parallel]
  ↓
Phase 6 (Recording)
  ↓
Phase 7 (Transcription)
  ↓
Phase 8 (AI Processing)
  ↓
Phase 9 (Session Review)
  ↓
Phase 10 (Editing & Resync)
  ↓
Phase 11 (World Database) [can parallel with Phase 10]
  ↓
Phase 12 (Processing Queue)
  ↓
Phase 13 (Notifications)
  ↓
Phase 14 (Onboarding) [can be done anytime after Phase 4]
  ↓
Phase 15 (Polish & Testing)
```

---

## MVP Completion Checklist

- [ ] Can create a campaign with name and game system
- [ ] Can add players and characters to campaign
- [ ] Can select attendees and start recording
- [ ] Recording works offline for 10+ hours
- [ ] Transcription runs locally after recording stops
- [ ] AI processes transcript when online (< 1 minute)
- [ ] Session detail shows: summary, scenes, entities, actions, player moments
- [ ] All outputs are editable inline
- [ ] Resync propagates edits to related content
- [ ] Entities stored at world level, viewable in World Database
- [ ] Processing queue handles offline → online transition
- [ ] Email notification sent when processing complete
- [ ] Onboarding guides first-time user
- [ ] Dark mode and light mode work
- [ ] Works on Windows, Mac, and Linux

---

## Document References

- PRD.md - What to build and success criteria
- APP_FLOW.md - How users navigate (screen inventory, flows)
- TECH_STACK.md - What to build with (exact packages and versions)
- FRONTEND_GUIDELINES.md - How it looks (colors, spacing, components)
- BACKEND_STRUCTURE.md - How data works (schema, relationships, rules)
