# APP_FLOW.md

Every page and every user navigation path documented. Step-by-step sequences, decision points, and screen inventory.

---

## Screen Inventory

| Screen | Route | Description |
|--------|-------|-------------|
| Onboarding | `/onboarding` | First-time user guided walkthrough |
| Home | `/` | Main landing - continue, new, review |
| Campaigns List | `/campaigns` | All campaigns |
| Campaign Home | `/campaigns/:id` | Campaign dashboard - sessions, world, players |
| New Campaign | `/campaigns/new` | Create campaign form |
| Session Setup | `/campaigns/:id/sessions/new` | Select attendees before recording |
| Recording | `/campaigns/:id/sessions/:sessionId/record` | Active recording screen |
| Post-Session | `/campaigns/:id/sessions/:sessionId/complete` | Session complete summary |
| Session Detail | `/campaigns/:id/sessions/:sessionId` | Processed session with 4 sections |
| Session Summary | `/campaigns/:id/sessions/:sessionId/summary` | Full summary + scenes (drill-down) |
| Extracted Items | `/campaigns/:id/sessions/:sessionId/entities` | NPCs, locations, items (drill-down) |
| What's Next | `/campaigns/:id/sessions/:sessionId/actions` | Action items, plot threads (drill-down) |
| Player Moments | `/campaigns/:id/sessions/:sessionId/players` | Player highlights (drill-down) |
| World Database | `/campaigns/:id/world` | All campaign entities |
| Players/Characters | `/campaigns/:id/players` | Campaign roster |
| Add Player | `/campaigns/:id/players/new` | Add player form |
| Add Character | `/campaigns/:id/characters/new` | Add character form |

---

## Navigation Structure

```
Home
├── Continue Campaign → Campaigns List → Campaign Home
├── New Campaign → New Campaign Form → Campaign Home
└── Review/Stats/Edit → Campaigns List

Campaign Home (layout TBD - needs visual mockups)
├── Sessions (list of past sessions, start new)
├── World Database (NPCs, locations, items)
└── Players/Characters (campaign roster)
```

---

## Flow 1: First-Time User (Onboarding)

**Trigger:** User opens app for the first time

**Steps:**
1. App detects first launch
2. Display onboarding welcome screen
3. Guided walkthrough begins:
   - Brief intro to app purpose
   - Show key features (record → transcribe → insights)
   - Prompt to create first campaign (or skip)
4. If user creates campaign: → New Campaign flow
5. If user skips: → Home screen

**Principles:**
- Apply engagement science
- Quick to value (don't overwhelm)
- Skip option always available

**Success:** User reaches Home or Campaign Home
**Error handling:** TBD

---

## Flow 2: Returning User - Home Screen

**Trigger:** User opens app (not first time)

**Screen:** Home

**Options:**
1. **Continue Campaign** → Campaigns List
2. **New Campaign** → New Campaign Form
3. **Review/Stats/Edit** → Campaigns List (browse mode)

---

## Flow 3: Create New Campaign

**Trigger:** User clicks "New Campaign" from Home

**Steps:**
1. Display New Campaign form
2. User enters:
   - Campaign name (required)
   - Game system (D&D 5e, Pathfinder, etc.)
   - Description (optional)
   - Import/paste existing info (optional) → AI will process and extract entities
3. User can add players/characters now or later
4. User clicks "Create"
5. If import text provided: AI processes in background
6. Navigate to Campaign Home

**Success:** Campaign created, user at Campaign Home
**Error handling:** TBD

---

## Flow 4: Add Players and Characters

**Trigger:** User wants to add participants to campaign

### Add Player
1. From Campaign Home → Players section → "Add Player"
2. Enter player name
3. Save

### Add Character
1. From Campaign Home → Players section → "Add Character"
2. Select which player this character belongs to
3. Enter character name
4. Optionally enter: class, race, level
5. Optionally paste backstory → AI extracts goals, relationships
6. Save

**Success:** Player/Character added to campaign
**Error handling:** TBD

---

## Flow 5: Start a Session (Recording)

**Trigger:** User wants to record a new session

**Steps:**
1. From Campaign Home → "New Session" or "Record"
2. **Session Setup screen:**
   - Display all players/characters in campaign
   - User selects who is present this session (checkboxes)
3. User clicks "Start Recording"
4. **Recording screen:**
   - Timer showing elapsed time
   - Stop button
   - (Future: "Catch me up" real-time summary button)
5. Recording runs (works offline)
6. User clicks "Stop" when session ends

**Success:** Recording saved, proceed to transcription
**Error handling:** TBD (checkpoint saves? recovery?)

---

## Flow 6: Post-Recording Processing

**Trigger:** User stops recording

**Steps:**
1. Recording stops
2. **Post-Session screen** displays:
   - Session duration
   - Date/time
   - Status: "Transcribing..." or "Queued for processing"
3. Transcription runs locally (Whisper) in background
4. When transcription complete + online:
   - AI processing begins automatically
5. User can:
   - Stay and wait
   - Navigate away (processing continues)
   - Close app entirely (processing queues)
6. When processing complete:
   - Email notification sent
   - (Future: Phone push notification)

**Success:** Session processed, ready for review
**Error handling:** TBD

---

## Flow 7: Review Processed Session

**Trigger:** User clicks email link OR navigates to session from Campaign Home

**Steps:**
1. **Session Detail screen** displays 4 sections with preview info:
   - **Session Summary** - overall summary snippet
   - **Extracted Items** - count of NPCs, locations, items found
   - **What's Next** - action items, plot threads snippet
   - **Player Moments** - highlights per player snippet
2. Each section has:
   - Preview content
   - "View more" to drill down
   - Edit button for inline editing

### Drill-down: Session Summary
- Navigate to Session Summary page
- Full overall summary
- Scene-by-scene breakdowns with timestamps
- Edit button on each section for inline editing
- Back to Session Detail

### Drill-down: Extracted Items
- Navigate to Extracted Items page
- Lists of NPCs, locations, items (sub-organization TBD)
- Each entity shows key info
- Edit button on each entity for inline editing
- Back to Session Detail

### Drill-down: What's Next
- Navigate to What's Next page
- Action items list
- Plot threads list
- Edit button on each for inline editing
- Back to Session Detail

### Drill-down: Player Moments
- Navigate to Player Moments page
- Per-player breakdown
- Quotes, highlights, memorable moments
- Edit button on each for inline editing
- Back to Session Detail

**Editing behavior:**
- Edit button → inline editing (no navigation)
- Save → triggers resync (MVP: manual "Resync" button)
- Changes cascade to related content

**Success:** User reviews and optionally edits session data
**Error handling:** TBD

---

## Flow 8: Browse World Database

**Trigger:** User wants to see all entities across campaign

**Steps:**
1. From Campaign Home → World Database
2. Display all entities for campaign:
   - NPCs (all sessions)
   - Locations (all sessions)
   - Items (all sessions)
3. Organization/filtering TBD (needs UI mockups)
4. Click entity → view full detail
5. Edit button → inline editing

**Success:** User browses/edits campaign entities
**Error handling:** TBD

---

## Flow 9: Browse Past Sessions

**Trigger:** User wants to review previous sessions

**Steps:**
1. From Campaign Home → Sessions list
2. Display all sessions for campaign:
   - Session number/date
   - Brief summary
   - Status (processed, pending, etc.)
3. Click session → Session Detail page

**Success:** User accesses past session
**Error handling:** TBD

---

## Flow 10: Delete Content

**Trigger:** User wants to delete campaign, session, or entity

**Availability:** Must be available for privacy reasons

**Details:** TBD

**Likely pattern:**
- Delete option in settings/menu for each item
- Confirmation dialog
- Hard delete (privacy requirement)

---

## Open Design Questions

- **Campaign Home layout:** Needs visual mockups and UI testing to determine best pattern (tabs, cards, sidebar, etc.)
- **Extracted Items organization:** How to display NPCs vs locations vs items (tabs, filters, mixed list?)
- **Error states:** All error handling TBD - focus on happy path for MVP
- **Settings/preferences:** Not MVP, but log user behavior to learn

---

## Future Flows (Not MVP)

- **Real-time "Catch me up"** during recording
- **Search** across transcripts and entities
- **Sharing** campaigns with other GMs
- **Player-facing views**
- **Mobile recording** with sync

---

## Document References

- PRD.md - Feature requirements and entity definitions
- TECH_STACK.md - Dependencies and versions
- FRONTEND_GUIDELINES.md - Design system
- BACKEND_STRUCTURE.md - Database schema and API
- IMPLEMENTATION_PLAN.md - Build sequence
