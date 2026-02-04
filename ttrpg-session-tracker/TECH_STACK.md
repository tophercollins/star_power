# TECH_STACK.md

Every package, dependency, API, and tool locked to specific versions. This eliminates ambiguity and ensures consistent builds.

---

## Core Framework

| Technology | Version | Purpose |
|------------|---------|---------|
| **Flutter** | 3.38.x (stable) | Cross-platform UI framework |
| **Dart** | 3.10.x | Programming language |

**Why Flutter:**
- Single codebase: iOS, Android, Windows, Mac, Linux, Web
- Native performance (compiles to ARM)
- Offline-first capable
- Growing desktop adoption
- Long-term Google backing

---

## Local Database

| Package | Version | Purpose |
|---------|---------|---------|
| **sqflite** | ^2.3.x | SQLite plugin for Flutter |
| **sqflite_common_ffi** | ^2.3.x | Desktop SQLite support |
| **path_provider** | ^2.1.x | Local file paths |

**Why SQLite:**
- Relational data (campaigns → sessions → entities)
- Complex queries supported
- Battle-tested, portable
- Works offline

---

## Audio Recording

| Package | Version | Purpose |
|---------|---------|---------|
| **record** | ^5.x | Cross-platform audio recording |

**Why record:**
- Simple API
- Desktop + mobile support
- Handles long recordings
- Multiple audio formats (WAV, AAC, etc.)

---

## Transcription

### MVP: Local Whisper

| Component | Details |
|-----------|---------|
| **whisper.cpp** | C++ port of OpenAI Whisper |
| **Model** | base (~150MB) or small (~500MB) |
| **Integration** | FFI bindings or bundled binary |

**Packages to evaluate:**
- `whisper_flutter_new` - Flutter bindings for whisper.cpp
- Custom FFI implementation if needed

**Why local for MVP:**
- Offline capability
- No per-transcription cost
- User privacy

### V2+: Cloud Transcription

| Service | Cost | Purpose |
|---------|------|---------|
| **OpenAI Whisper API** | $0.006/min | High-quality cloud transcription |

**Why cloud for V2:**
- Smaller app size
- Best accuracy
- Simpler maintenance
- Cost baked into subscription

---

## LLM Processing

| Service | Model | Cost (per 1M tokens) |
|---------|-------|---------------------|
| **Google AI** | Gemini 1.5 Flash | $0.075 in / $0.30 out |

**Why Gemini Flash:**
- Cheapest quality option
- 1M token context (handles long transcripts)
- Forces good prompt engineering discipline
- Easy to swap to GPT-4o or Claude later

**Abstraction:** Build a provider interface so LLM can be swapped without code changes.

---

## Backend (Sync & Auth)

| Service | Purpose |
|---------|---------|
| **Supabase** | Postgres database, Auth, Storage, Realtime |

**Why Supabase:**
- Postgres-based (industry standard, portable)
- Open source (can self-host later)
- Built-in auth
- Low lock-in risk
- Generous free tier for MVP

| Package | Version | Purpose |
|---------|---------|---------|
| **supabase_flutter** | ^2.x | Flutter client for Supabase |

---

## Email Notifications

| Service | Purpose |
|---------|---------|
| **Resend** | Transactional email |

**Why Resend:**
- Modern API
- Cheap
- Easy to swap to SendGrid/Postmark/SMTP later

---

## File Storage

### Local (MVP)
- Audio files stored locally via `path_provider`
- SQLite for structured data
- Raw transcripts as text files or in DB

### Cloud (V2+)
- **Supabase Storage** for audio backup/sync
- Or **Cloudflare R2** (cheaper for large files)

---

## State Management (Flutter)

| Package | Version | Purpose |
|---------|---------|---------|
| **riverpod** | ^2.5.x | State management |

**Why Riverpod:**
- Type-safe
- Testable
- Good for complex apps
- Active development

**Alternative:** `bloc` if team prefers it. Decision can be made at implementation.

---

## Development Tools

| Tool | Purpose |
|------|---------|
| **VS Code** or **Android Studio** | IDE |
| **Flutter DevTools** | Debugging, performance |
| **Git** | Version control |
| **GitHub Actions** | CI/CD |

---

## Platform-Specific Notes

### Desktop (Windows, Mac, Linux)
- Full offline support
- Local Whisper transcription
- SQLite for storage
- ~150-500MB app size (with Whisper model)

### Mobile (iOS, Android) - Future
- Cloud transcription default (smaller app)
- Optional model download for offline
- Push notifications via Firebase Cloud Messaging

### Web - Future (Low Priority)
- Limited audio recording support
- Cloud-only processing
- Supabase for storage

---

## Version Locking Strategy

```yaml
# pubspec.yaml approach
dependencies:
  flutter:
    sdk: flutter
  sqflite: ^2.3.0
  path_provider: ^2.1.0
  record: ^5.0.0
  supabase_flutter: ^2.0.0
  riverpod: ^2.5.0
  # etc.
```

- Use caret (^) for minor version flexibility
- Lock major versions
- Run `flutter pub upgrade --major-versions` periodically
- Test thoroughly before major upgrades

---

## API Keys & Secrets

| Service | Secret Type | Storage |
|---------|-------------|---------|
| Google AI (Gemini) | API Key | Environment variable / secure storage |
| Supabase | Anon Key + URL | Environment variable |
| Resend | API Key | Server-side only |

**Never commit API keys to git.**

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Flutter App                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │     UI      │  │   State     │  │   Services  │     │
│  │  (Widgets)  │  │ (Riverpod)  │  │             │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│  ┌───────────────────────┼───────────────────────────┐ │
│  │                 Local Layer                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │ │
│  │  │  SQLite  │  │  Audio   │  │   Whisper    │    │ │
│  │  │    DB    │  │  Files   │  │  (Local)     │    │ │
│  │  └──────────┘  └──────────┘  └──────────────┘    │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                           │
                           │ (When Online)
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Cloud Services                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Supabase │  │  Gemini  │  │  Resend  │  │Whisper │ │
│  │  (Auth,  │  │  Flash   │  │ (Email)  │  │  API   │ │
│  │  Sync)   │  │  (LLM)   │  │          │  │ (V2+)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Decision Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | Flutter | Single codebase, native performance, all platforms |
| Language | Dart | Comes with Flutter, easy to learn |
| Database | SQLite | Relational, offline, portable |
| Audio | record package | Simple, cross-platform |
| Transcription (MVP) | Local Whisper | Offline, free |
| Transcription (V2) | Whisper API | Better UX, cost in subscription |
| LLM | Gemini Flash | Cheapest, easy to swap later |
| Backend | Supabase | Postgres, low lock-in, can self-host |
| Email | Resend | Modern, cheap, swappable |
| State | Riverpod | Type-safe, testable |

---

## Document References

- PRD.md - Feature requirements
- APP_FLOW.md - User navigation
- FRONTEND_GUIDELINES.md - Design system
- BACKEND_STRUCTURE.md - Database schema
- IMPLEMENTATION_PLAN.md - Build sequence
