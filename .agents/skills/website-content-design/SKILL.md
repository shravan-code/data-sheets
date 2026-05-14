# Website Content Design Skill

## Design Reference

The canonical design reference is in the **`data-cake-design/`** folder at the project root. It is a React + Vite + Tailwind v4 implementation of the exact dark IDE-themed design system. Use its components and pages as the visual specification for how every page should look.

---

### Color System (`src/index.css`)

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-surface` | `#0b141c` | Page background |
| `--color-surface-container` | `#182028` | Card / container backgrounds |
| `--color-surface-container-high` | `#222b33` | Code block header, table header |
| `--color-surface-container-highest` | `#2d363e` | Scrollbar thumb |
| `--color-primary-container` | `#0d1117` | Active nav item background |
| `--color-on-surface` | `#dae3ee` | Primary text (headings, body) |
| `--color-on-surface-variant` | `#c6c6cb` | Secondary text (metadata, descriptions) |
| `--color-outline` | `#8f9095` | Subtle outlines |
| `--color-outline-variant` | `#45474b` | Primary borders |
| `--color-secondary-fixed` | `#5bffa1` | Accent (green) — active links, highlights, icons |
| `--color-secondary-container` | `#27ff97` | Button hover / brighter accent |
| `--color-on-secondary` | `#00391d` | Text on accent backgrounds |

---

### Typography

| Usage | Font |
|-------|------|
| Everything (body + headings + labels) | `JetBrains Mono`, monospace |
| Monospace (fallback) | `ui-monospace`, `SFMono-Regular`, `monospace` |

All text uses `JetBrains Mono`. No font switching between headings and body — it is monospace throughout. Use uppercase + wide tracking (`tracking-wider`, `tracking-widest`, `uppercase`) for labels, section headers, and metadata.

---

### Layout Structure (every non-home page)

```
Navbar (sticky top, bg-surface, border-bottom)
Logo (left): Code2 icon + "Data Cake" text, both in secondary-fixed
Nav links (center/left): uppercase, hover:text-secondary-fixed
Icons (right): Terminal, UserCircle2

Page content area: max-w-[1200px] mx-auto px-4 md:px-10 py-8
[Mobile] Hamburger menu with spring animation overlay
Sidebar (left, hidden on mobile):
  Collapsible category buttons (uppercase, small font)
  Sub-items with border-left, active state has border-left-2 + bg-primary-container
  Portfolio link at bottom with ExternalLink icon
Main content (flex-1, min-w-0):
  Back link (ArrowLeft + "Back to ...", font-mono, hover:text-secondary-fixed)
  Page header (section ID badge, h1, description)
  Sections with border-left accent + colored indicator bar
  Code blocks: dark container, header with language name + Copy button
  Info cards (bg-surface-container, border, flex with icon)
  Tables (bordered, alternating row backgrounds)
  Bottom navigation cards
TOC Sidebar (right, hidden on mobile):
  "On This Page" heading (uppercase, tracking-widest)
  Links with left border, active item has bg-secondary-fixed indicator

Footer (bg-surface, border-top, mt-auto)
Logo + copyright (left)
Link list (right, hover:text-secondary-fixed)
```

---

### Component Designs (from `data-cake-design/src/`)

#### Navbar (`src/components/Navbar.tsx`)
- Sticky top, `z-50`, `bg-surface`, `border-b border-outline-variant`
- Height: `h-16`, inner `max-w-[1200px] mx-auto`
- Logo: `Code2` icon (w-6 h-6, `text-secondary-fixed`, `fill-secondary-fixed/20`) + "Data Cake" text (bold, uppercase, tracking-wider, `text-secondary-fixed`)
- Desktop links: hidden on mobile (`hidden md:flex`), active link has `border-b-2 border-secondary-fixed`
- Right icons: Terminal + UserCircle2, `hover:text-secondary-fixed`
- Mobile: hamburger Menu/X icon, full-screen slide-in overlay with spring animation

#### Sidebar (`src/components/Sidebar.tsx`)
- Desktop: `hidden lg:block w-64 pr-8 border-r border-outline-variant sticky top-24 h-[calc(100vh-6rem)]`
- Category buttons: full width, flex with icon + label + chevron, `bg-surface-container`, border, hover effect
- Nav links: sub-items with `border-l border-outline-variant pl-4`, active item has `-ml-[17px] border-l-2 border-secondary-fixed bg-primary-container`
- Portfolio: `mt-auto pt-8 border-t`, icon + label + `ExternalLink`

#### Footer (`src/components/Footer.tsx`)
- `bg-surface border-t border-outline-variant w-full mt-auto`
- Flex row (column on mobile), `max-w-[1200px] mx-auto`, `py-8`
- Links: text-xs, underline, `hover:text-secondary-fixed`

#### Home Page (`src/pages/Home.tsx`)
- Hero section: `py-24 md:py-32`, `border-b border-outline-variant`, IDE grid overlay background
- Terminal prompt: in secondary-fixed
- h1: Large, bold, `text-on-surface`
- Description: `border-l-2 border-outline-variant pl-6`
- CTA buttons: solid secondary-fixed + outlined variant
- Featured paths section: 3-column grid, PathCards with hover underline effect

#### Curriculum/Module Page (`src/pages/Curriculum.tsx`)
- Hero badge: pill with Award icon + "EXPERT DOCUMENTATION" label
- Centered h1 with secondary-fixed accent word
- Section headers: numbered badge (border, square) + h2
- LessonCard: `bg-surface-container`, border, hover effect, icon + title + tag + read time
- Timeline section: circular numbered badge with vertical line, dashed locked modules

#### Lesson Page (`src/pages/Lesson.tsx`)
- Three-column layout: Sidebar | Main | TOC
- Section headers: `border-l border-outline-variant pl-4 md:pl-8 ml-0.5` with colored indicator bar (`w-[5px] h-6 bg-secondary-fixed` for active, `bg-outline-variant` for regular)
- Inline code: `font-mono bg-surface-container-high px-1.5 py-0.5 rounded border border-outline-variant`
- Code blocks:
  - Container: `bg-primary-container border border-outline-variant rounded`
  - Header: `bg-surface-container-high border-b`, shows language + Copy button
  - Pre/code: light-on-dark, comments after `#` in dimmer color
- Pro Tip cards: `bg-surface-container`, border, flex with Lightbulb icon in secondary-fixed
- Tables: `border border-outline-variant rounded overflow-hidden`, alternating row backgrounds (`bg-surface` / `bg-primary-container`)
- TOC: `w-56 shrink-0 sticky top-24 h-[calc(100vh-6rem)]`, left border + active indicator

---

### Mobile Behavior

- Sidebar: Slide-in from left with spring animation, full-screen backdrop blur overlay
- TOC: Expandable accordion below mobile nav bar (hidden on desktop)
- Mobile nav bar: sticky with hamburger, "NAV" + "CONTENT" toggle buttons, breadcrumb trail
- Navbar: full-screen mobile menu overlay with spring slide from right

---

### Home Page Exception

`index.html` is exempt from these rules. It can have its own unique design, hero section, animations, and layout. The only shared element is the navbar.
