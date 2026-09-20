---
name: Civic Horizon
colors:
  surface: '#f8f9ff'
  surface-dim: '#ccdbf1'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eef4ff'
  surface-container: '#e4efff'
  surface-container-high: '#dae9ff'
  surface-container-highest: '#d4e4fa'
  on-surface: '#0d1d2c'
  on-surface-variant: '#43474e'
  inverse-surface: '#233242'
  inverse-on-surface: '#e9f1ff'
  outline: '#73777f'
  outline-variant: '#c3c6cf'
  surface-tint: '#406186'
  primary: '#00213e'
  on-primary: '#ffffff'
  primary-container: '#11375a'
  on-primary-container: '#80a1c9'
  inverse-primary: '#a8c9f4'
  secondary: '#885200'
  on-secondary: '#ffffff'
  secondary-container: '#fd9e15'
  on-secondary-container: '#663c00'
  tertiary: '#00213f'
  on-tertiary: '#ffffff'
  tertiary-container: '#003763'
  on-tertiary-container: '#5da2ee'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d1e4ff'
  primary-fixed-dim: '#a8c9f4'
  on-primary-fixed: '#001d36'
  on-primary-fixed-variant: '#26496d'
  secondary-fixed: '#ffdcbb'
  secondary-fixed-dim: '#ffb869'
  on-secondary-fixed: '#2c1700'
  on-secondary-fixed-variant: '#683d00'
  tertiary-fixed: '#d2e4ff'
  tertiary-fixed-dim: '#a1c9ff'
  on-tertiary-fixed: '#001c37'
  on-tertiary-fixed-variant: '#00487f'
  background: '#f8f9ff'
  on-background: '#0d1d2c'
  surface-variant: '#d4e4fa'
  election-gold: '#FFCC4D'
  selection-yellow: '#FFD500'
  selection-border: '#D8B200'
  surface-base: '#F4F7FA'
  surface-card: '#FFFFFF'
  border-subtle: '#DCE3EA'
  border-strong: '#CBD5E1'
  status-open: '#1F8A4C'
  status-open-surface: '#EBF7EE'
  status-closed: '#C0392B'
  status-closed-surface: '#FDEDEC'
  text-primary: '#112233'
  text-secondary: '#4B5B6D'
  admin-sidebar-bg: '#0D2B47'
typography:
  display-lg:
    fontFamily: Open Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Open Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Open Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Open Sans
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 28px
  headline-md:
    fontFamily: Open Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Open Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  title-lg:
    fontFamily: Open Sans
    fontSize: 16px
    fontWeight: '700'
    lineHeight: 22px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes a unified civic-democratic interface bridging institutional authority and student-friendly accessibility. It synthesizes two previously distinct contexts—the vibrant voter engagement surfaces and the analytical election administrator dashboard—into a cohesive, trustworthy digital experience.

### Brand Personality & Emotional Impact
- **Institutional Legitimacy & Trust:** Grounded in deep civic navy hues, evoking constitutional seriousness, accuracy, and ballot integrity.
- **Empowering & Engaging:** Energetic gold accents and warm amber feedback loops convey optimism, participation, and celebratory school leadership.
- **Unambiguous Clarity:** High-contrast legibility and definitive interaction states eliminate cognitive strain, ensuring zero student error during mobile voting.

### Visual Style: Institutional Modernism with Tactile Accents
The design language adopts **Corporate / Modern** principles elevated by crisp structural cards, hairline borders, and warm tactile feedback:
- Structured card surfaces with balanced neutral backgrounds (`#F4F7FA`).
- Targeted civic gold accents for selections, active states, and callout indicators rather than overwhelming saturated floods.
- Subtle depth layering using crisp borders paired with multi-tier ambient shadows instead of heavy ungrounded blur effects.

## Colors

The palette establishes a harmonious bridge between executive civic dignity and engaging voter dynamics.

### Key Roles
- **Primary (`#11375A`):** Deep Sovereign Navy. Anchors top navigation hierarchies, modal headers, primary interactive surfaces, and statistical leaders.
- **Secondary (`#FD9E16`):** Vibrant Amber. Used for administrative highlights, analytic progress bars, key action buttons, and active dashboard indicators.
- **Tertiary (`#1D6FB8`):** Civic Cobalt. Handles interactive hyperlinking, intermediate actions, information notices, and active tabs.
- **Neutral (`#6B7A8D`):** Slate Gray. Provides calibrated contrast for secondary copy, form helper text, and subtle grid dividers.

### Functional States & Ballot Affirmation
- **Candidate Selection (`#FFD500` / `#D8B200`):** Provides instant, high-contrast feedback on voter ballots. When a candidate card is selected, it fills with luminous election gold and an authoritative deep gold border, ensuring voters have zero ambiguity about their choices.
- **Civic Status Badging:** High-visibility pairing for live voting indicators. Open elections use `#1F8A4C` over `#EBF7EE`; closed states rely on `#C0392B` over `#FDEDEC`.

## Typography

The type system blends the authoritative, open humanist cadence of **Open Sans** for headlines and banners with the systematic, engineered precision of **Inter** for forms, analytical tables, and ballot body copy.

### Hierarchy Guidelines
- **Civic Headers:** Top-level election names and modal titles employ `display-lg` and `headline-lg` in `Open Sans` 700 to ground the page with administrative certainty.
- **Ballot & Candidate Labels:** Candidate names use `headline-sm` or `title-lg` to guarantee legibility across varied photo backgrounds and card scales.
- **Badges & Status Metrics:** Status indicators (OPEN/CLOSED) and table headers leverage `label-sm` or `label-md` in uppercase with subtle letter-spacing for rapid visual scanning on both mobile devices and wide admin monitors.

## Layout & Spacing

The layout model adapts seamlessly between focused civic voter actions and comprehensive administrative operations.

### Grid Architecture
- **Public Voting View:** A single-column centered container constrained to `760px` for authentication and instructions, widening smoothly to `1120px` for the multi-candidate ballot grid.
- **Candidate Ballot Grid:** Adapts dynamically:
  - **Desktop (>1024px):** 3-column card grid with `1.5rem` gutters.
  - **Tablet (640px - 1024px):** 2-column card grid with `1rem` gutters.
  - **Mobile (<640px):** 1-column layout maximizing photo presentation and single-tap accuracy.
- **Administrative Dashboard:** Full-width adaptive shell up to `1440px` with a persistent `240px` navigation column on desktop, converting into an inline utility navigation header on tablet and mobile viewports (`<860px`).
- **Metric Grids:** 4-column KPI distribution across desktop screens collapsing to 2-column at `1024px` and 1-column below `640px`.

## Elevation & Depth

Visual hierarchy uses a refined ambient shadow model combined with low-contrast structural boundaries rather than aggressive borders or heavy skeletal skeuomorphism.

### Depth Hierarchy
- **Level 0 (Flat/Base):** Canvas background (`#F4F7FA`). No elevation.
- **Level 1 (Structural Cards):** Content containers, candidate selection cards, and data tables. Layered with a 1px border of `#DCE3EA` and soft shadow: `0 1px 3px rgba(17, 55, 90, 0.06), 0 4px 12px rgba(17, 55, 90, 0.04)`.
- **Level 2 (Active/Hover/Dropdowns):** Hovered candidate cards, active stat cards, and contextual tooltips: `0 4px 16px rgba(17, 55, 90, 0.10)`.
- **Level 3 (Overlays & Verification Modals):** Confirmation dialogs and crucial ballot validation screens: `0 12px 32px rgba(17, 55, 90, 0.20)`. Backdrops use a soft tint of `rgba(17, 55, 90, 0.60)` with a subtle `backdrop-filter: blur(4px)`.

## Shapes

The design system maintains a balanced **Rounded (0.5rem / 8px)** curvature throughout core interactive modules.

### Shape Application
- **Standard Controls (Inputs, Buttons, Badges):** `rounded` (8px / `0.5rem`) for disciplined institutional clarity and touch target ergonomics.
- **Surfaces & Cards:** `rounded-lg` (16px / `1rem`) on candidate ballot cards, summary cards, and administrative metric containers.
- **Modal Dialogs & Confirmation Windows:** `rounded-xl` (24px / `1.5rem`) to frame decisive voting moments.
- **Status Pills & Chips:** Fully rounded (9999px pill) for live state flags, turnout badges, and category tags.
- **Candidate Imagery:** `12px` interior corner radius inside cards to create a unified framing border around portraits.

## Components

### Buttons
- **Primary (Civic Deep Navy):** Background `#11375A`, text `#FFFFFF`, hover `#194264`. Height 44px (48px on mobile for accessibility). Font weight 600.
- **Accent Action (Amber Gold):** Background `#FD9E16`, text `#112233`, hover `#F08C00`. Used for high-prominence dashboard operations and final confirmation triggers.
- **Secondary / Ghost:** Background transparent, border 1px `#DCE3EA`, text `#11375A`, hover background `#EEF4FB`.
- **Disabled State:** Background `#E2E8F0`, text `#94A3B8`, non-clickable cursor.

### Candidate Ballot Card
- **Structure:** White card (`#FFFFFF`) with 1.5px border (`#DCE3EA`). Contains portrait photo (`aspect-ratio: 4/5` or `300px` mobile-scaled height), candidate name (`headline-sm`), and a circular radio status indicator.
- **Hover State:** Border transitions to `#1D6FB8` with Level 2 elevation.
- **Selected State:** Card surface transforms immediately to `#FFD500` with a 2px `#D8B200` border. Text transforms to high-contrast `#112233`. Radio mark transforms into a solid deep navy checkmark badge.

### Status Indicators & Badges
- **Election OPEN Badge:** Pill shape, background `#EBF7EE`, text `#1F8A4C`, border 1px `#B8E5C4`. Includes a live animated pulsing green indicator dot.
- **Election CLOSED Badge:** Pill shape, background `#FDEDEC`, text `#C0392B`, border 1px `#F5C2BE`.
- **Standings Leader Badge:** Deep navy pill with small gold star icon (`★`) indicating leading candidates in live results.

### Inputs & Authentication Fields
- **Student ID Input:** 48px height, 1px border `#CBD5E1`, text `#112233`, background `#FFFFFF`. Focus state features a crisp 2px glow ring of `#1D6FB8` with zero horizontal layout shift.
- **Error Feedback:** Red alert container with subtle `#FDEDEC` surface and `#C0392B` typography, positioned directly inline below the input.

### Metric & Statistics Cards
- **Stat Surface:** Elevated Level 1 card featuring an accent line on top (3px height) in `#FD9E16` or `#11375A`.
- **KPI Metrics:** `display-lg` typography for voter tallies and percentage indicators.
- **Progress Trackers:** 8px rounded track background `#E2E8F0` with smooth horizontal fills using amber `#FD9E16` or civic blue `#1D6FB8`.

### Confirmation & Success Modals
- **Review Summary Modal:** Constrained to `600px` width. Two-column review table displaying position title against selected candidate thumbnail and full name. Fixed actions at footer: "Change Vote" (Ghost) and "Confirm & Cast Ballot" (Primary Navy).