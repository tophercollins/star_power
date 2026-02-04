# FRONTEND_GUIDELINES.md

Design system for TTRPG Session Tracker. Clean, minimal, Notion/Obsidian-inspired. Speed and efficiency first. Nothing gets in the GM's way.

---

## Design Philosophy

- **Clean and minimal** - Notion/Obsidian level simplicity
- **Speed over style** - every interaction should feel instant
- **Dark mode + light mode** - user's choice, system default respected
- **Pleasant workspace** - a place to write and connect ideas
- **No fantasy theming** - substance over gimmicks
- **Accessibility** - readable, high contrast, keyboard navigable

---

## Typography

Use Flutter's default system fonts. No custom font loading for MVP.

| Use | Font | Details |
|-----|------|---------|
| UI (headings, buttons, labels) | System default (Roboto on Android, SF Pro on iOS/Mac, Segoe UI on Windows) | Clean, readable, zero setup |
| Body text / editable areas | System default | Consistent with platform |
| Monospace (code, raw transcript) | System monospace | For transcript display |

**Scale:**

| Token | Size | Use |
|-------|------|-----|
| `xs` | 12sp | Captions, timestamps, metadata |
| `sm` | 14sp | Secondary text, labels |
| `base` | 16sp | Body text, default |
| `lg` | 18sp | Section headers |
| `xl` | 22sp | Page titles |
| `2xl` | 28sp | Screen titles |

**Rules:**
- Max line width: 72 characters for reading comfort
- Line height: 1.5 for body, 1.2 for headings
- Font weight: Regular (400) for body, Semi-bold (600) for headings

---

## Color Palette

Use Material 3 color system. Minimal custom colors.

### Light Mode

| Token | Hex | Use |
|-------|-----|-----|
| `background` | `#FFFFFF` | Page background |
| `surface` | `#F7F7F7` | Cards, panels |
| `surfaceVariant` | `#EEEEEE` | Hover states, secondary surfaces |
| `onBackground` | `#1A1A1A` | Primary text |
| `onSurface` | `#333333` | Secondary text |
| `onSurfaceVariant` | `#666666` | Tertiary text, placeholders |
| `primary` | `#2563EB` | Buttons, links, active states |
| `onPrimary` | `#FFFFFF` | Text on primary |
| `outline` | `#D1D5DB` | Borders, dividers |
| `error` | `#DC2626` | Error states |
| `success` | `#16A34A` | Success states |

### Dark Mode

| Token | Hex | Use |
|-------|-----|-----|
| `background` | `#1A1A1A` | Page background |
| `surface` | `#252525` | Cards, panels |
| `surfaceVariant` | `#333333` | Hover states, secondary surfaces |
| `onBackground` | `#E5E5E5` | Primary text |
| `onSurface` | `#CCCCCC` | Secondary text |
| `onSurfaceVariant` | `#999999` | Tertiary text, placeholders |
| `primary` | `#3B82F6` | Buttons, links, active states |
| `onPrimary` | `#FFFFFF` | Text on primary |
| `outline` | `#404040` | Borders, dividers |
| `error` | `#EF4444` | Error states |
| `success` | `#22C55E` | Success states |

### Status Colors (Both Modes)

| Status | Light | Dark | Use |
|--------|-------|------|-----|
| Recording | `#DC2626` | `#EF4444` | Active recording indicator |
| Processing | `#F59E0B` | `#FBBF24` | Transcribing/processing |
| Complete | `#16A34A` | `#22C55E` | Ready to review |
| Queued | `#6B7280` | `#9CA3AF` | Waiting for connection |

---

## Spacing Scale

Consistent 4px base unit.

| Token | Value | Use |
|-------|-------|-----|
| `xxs` | 2px | Tight gaps |
| `xs` | 4px | Icon padding, tight spacing |
| `sm` | 8px | Compact element spacing |
| `md` | 16px | Default padding/margin |
| `lg` | 24px | Section spacing |
| `xl` | 32px | Large section gaps |
| `2xl` | 48px | Page-level spacing |
| `3xl` | 64px | Major section breaks |

---

## Layout Rules

### General
- Max content width: 800px (centered, like Notion/Obsidian)
- Side padding: 16px (mobile), 24px (tablet), 32px (desktop)
- Use Flutter's `SafeArea` everywhere

### Cards
- Border radius: 8px
- Padding: 16px
- Elevation: 0 (flat, use borders instead of shadows)
- Border: 1px solid `outline` color

### Lists
- Item padding: 12px vertical, 16px horizontal
- Divider between items: 1px `outline`
- No alternating row colors

### Forms
- Label above field
- Field height: 48px
- Field border radius: 6px
- Field border: 1px solid `outline`
- Focus border: 2px solid `primary`
- Spacing between fields: 16px

---

## Component Styles

### Buttons

| Type | Style | Use |
|------|-------|-----|
| Primary | Filled `primary` color, white text, 8px radius | Main actions (Start Recording, Save) |
| Secondary | Outlined, `primary` border and text, transparent fill | Secondary actions (Cancel, Back) |
| Text | No border, `primary` text only | Tertiary actions (Skip, Learn more) |
| Danger | Filled `error` color, white text | Destructive actions (Delete) |

- Button height: 44px (touch-friendly)
- Button padding: 16px horizontal
- Disabled: 40% opacity

### Navigation

- Sidebar on desktop (collapsible)
- Bottom nav on mobile (future)
- Breadcrumbs for drill-down pages
- Back button always visible on sub-pages

### Edit Button

- Small icon button (pencil icon)
- Positioned top-right of editable content
- On tap: content becomes editable inline
- Save/Cancel buttons appear below edited content

### Recording Indicator

- Red dot + timer text
- Fixed position (always visible during recording)
- Pulsing animation on the dot

### Status Badges

- Small pill shape
- Background: status color at 15% opacity
- Text: status color at 100%
- Border radius: 12px
- Padding: 4px 8px

---

## Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 600px | Single column, bottom nav |
| Tablet | 600px - 1024px | Single column, wider content |
| Desktop | > 1024px | Sidebar + content area |

**MVP focuses on desktop (> 1024px).** Mobile/tablet layouts are future.

---

## Icons

- Use **Material Icons** (built into Flutter)
- Size: 24px default, 20px for compact, 28px for emphasis
- Color: inherit from text context

---

## Animations

- Keep minimal. Speed over flair.
- Page transitions: 200ms fade
- Button press: subtle scale (0.98)
- Loading states: simple circular progress indicator
- Recording dot: pulsing (1s cycle)
- No bouncing, no sliding panels, no parallax

---

## Editable Content Areas

Since the app is a workspace (like Obsidian):

- Editable areas should feel like writing, not form-filling
- Generous padding around text areas
- Subtle border that only shows on hover/focus
- Auto-expanding height (no fixed text areas)
- Markdown support for summaries and notes (future)

---

## Empty States

When a list or section has no data:

- Brief, friendly message ("No sessions yet")
- Clear call to action ("Record your first session")
- No sad face illustrations or complex graphics
- Keep it simple and actionable

---

## Loading States

- Skeleton screens for content loading (gray blocks where content will appear)
- Circular progress for actions (saving, processing)
- Never block the whole screen unless absolutely necessary

---

## Accessibility

- Minimum contrast ratio: 4.5:1 for text
- All interactive elements: minimum 44x44px touch target
- Keyboard navigation support
- Screen reader labels on all buttons and inputs
- Focus indicators visible in both themes

---

## Flutter-Specific Conventions

### Theme Setup
```dart
// Use MaterialApp with ThemeData
MaterialApp(
  theme: lightTheme,
  darkTheme: darkTheme,
  themeMode: ThemeMode.system, // Respect OS setting
)
```

### Widget Guidelines
- Use `const` constructors where possible
- Prefer `Column`/`Row` with `Expanded` over complex layouts
- Use `ListView.builder` for long lists (not `Column` with `children`)
- Extract reusable widgets into separate files
- Name widgets descriptively: `SessionCard`, `EntityListTile`, `RecordingTimer`

### File Structure (UI)
```
lib/
  ui/
    screens/          # Full-page screens
      home_screen.dart
      campaign_home_screen.dart
      session_detail_screen.dart
      recording_screen.dart
    widgets/          # Reusable components
      session_card.dart
      entity_list_tile.dart
      edit_button.dart
      status_badge.dart
    theme/
      app_theme.dart  # Light + dark theme definitions
      colors.dart     # Color constants
      spacing.dart    # Spacing constants
      typography.dart # Text style definitions
```

---

## Design Decisions to Revisit

- **Campaign Home layout:** Needs mockups (tabs vs cards vs sidebar)
- **Entity organization in Extracted Items:** Tabs, filters, or mixed list
- **Markdown editor choice:** For note/summary editing
- **Fantasy theming (optional):** Could add subtle theme as paid feature later, but MVP stays clean
- **Custom fonts:** Could add Inter or similar later if system fonts feel too generic

---

## Document References

- PRD.md - Feature requirements
- APP_FLOW.md - User navigation
- TECH_STACK.md - Dependencies (Flutter, Material 3)
- BACKEND_STRUCTURE.md - Data models that inform UI
- IMPLEMENTATION_PLAN.md - Build sequence
