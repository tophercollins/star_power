# Legacy Desktop Application

This directory contains the original DearPyGui desktop version of Star Power.

## Original Desktop App

The desktop application was the initial implementation of Star Power:
- **UI**: DearPyGui (Python GUI framework)
- **Platform**: Desktop only (Windows, macOS, Linux)
- **Mode**: Single machine, local play

### Running the Legacy App

```bash
cd legacy
pip install dearpygui gspread google-auth
python main.py
```

## Why It Was Moved

The project has evolved into a multiplayer cross-platform game:
- **New backend**: FastAPI REST API (in `/backend`)
- **Future frontend**: React Native / PWA for mobile and web
- **Multiplayer**: Play against others online

The legacy desktop app is preserved for:
- Reference implementation
- Testing game logic
- Educational purposes

## Reusing Components

The core game engine is shared between legacy and new implementations:
- `/engine` - Game logic (shared)
- `/utils` - Card loaders (shared)
- `/resources` - Configuration (shared)

Only the UI layer (`/legacy/ui`) is desktop-specific.
