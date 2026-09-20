# Election Room — UI Description

**Product:** School (JHS) prefect-election voting system for the **Westland Electoral Commission**. Students authenticate with a student ID, vote once, and (after the election closes) results are published. Staff get a live admin dashboard. Mobile-first usage is expected (students on phones; admins likely on desktop).

**Brand feel:** School institutional + civic election authority. Two visual systems coexist and could be unified:
- **Public site** (students/voters): bright, warm, yellow + navy + light blue, soft glassmorphism.
- **Staff dashboard** (admin): professional infographic style, navy + orange, Open Sans.

---

## 1. Global

### Color palette
| Role | Public | Dashboard |
|---|---|---|
| Primary blue | `#1d6fb8` (dark `#155892`) | Navy `#11375a`, `#194264` |
| Accent orange | — | `#fd9e16` / `#f08c00` / `#fece61` |
| Header yellow | `#ffcc4d` | — |
| Selected w/ yellow | `#ffd500` (checked card) | — |
| Background | body `#f4f7fa` | `#e7ebee` |
| Card/white | `#ffffff` | `#ffffff` |
| Text / muted | `#2c3e50` / `#6b7a8d` | `#2b3440` / `#7a8794` |
| Border | `#dce3ea` | `#d8dee5` |
| Success / Danger | `#1f8a4c` / `#c0392b` | `#1f8a4c` / `#c0392b` |

### Typography
- Public: `Segoe UI`, `Roboto`, system sans.
- Dashboard: `Open Sans` (Google Fonts), weights 400/600/700, system fallback.

### Radius / shadow
- Public: 8px radius, subtle `0 8px 32px rgba(17,55,90,.12)` on frosted cards.
- Dashboard: 12px radius, `0 2px 6px rgba(17,55,90,.10)`.

### Layout
- Public pages: centered container, **max-width 760px** (vote ballot widens to **1100px**).
- Dashboard: **max-width 1400px**, full-width shell, two-column grid (**232px sidebar + content**).

### Global components
- **Navbar (public):** solid **yellow** bar (`#ffcc4d`), navy text; left = brand **"WESTLAND ELECTORAL COMMISSION"**, right = links **Vote · Results · Dashboard** (staff only) · **Admin**.
- **Message toasts:** stacked under navbar in container — error = pale red bg/red text, success = pale green bg/green text.
- **Footer:** none rendered (commented out) on public pages.

---

## 2. Home (`/`)
- Centered hero card (white, 1px border): big **election name** heading + status line — **"The election is currently OPEN"** (green) or **"CLOSED"** (red), or "No election has been set up yet".
- Two-column card grid (stacked on mobile):
  - **Cast Your Vote** → navigation card (blue heading, muted description).
  - **View Results** → navigation card.

---

## 3. Voting flow (`/vote/`) — the core screen
Background: soft 3-stop gradient `#fdf2dd → #eef4fb → #e7edf5` with two large blurred orbs (orange top-left, navy bottom-right). Everything glassy: `backdrop-filter: blur(14px)` white `rgba(255,255,255,.55)` cards with white borders.

**Step A — Student ID entry (no session):**
- Centered narrow column (max 480px): heading **"Cast Your Vote"**, helper "Enter your student ID to begin voting."
- Single text input + **Continue** button (blue).
- Error state: red alert box ("No student was found with that ID…", "election is currently closed", "You have already voted", inactive account).

**Step B — Ballot (after ID accepted):**
- Greeting: **"Hi, {Full Name}"**.
- Instruction: "Select **one** candidate for each position. You will review your choices before submitting."
- One **fieldset per position** — a rounded card with the position name as `legend` (navy/blue, bold).
- Inside: **candidate gallery** — hidden radio inputs driving cards:
  - Card: portrait photo (**300px tall**, `object-fit: cover`, rounded 12px, light gray placeholder bg) + candidate full name (bold, ~1.2rem) under it.
  - Default: white card, 2px border; hover border turns blue.
  - **Selected: card turns yellow `#ffd500`** with dark border `#e6c200` and near-black text — the selection is unmistakable.
  - Grid: **3 columns** desktop → **2** (≤1000px) → **1** (≤480px).
- Footer button: **"Review My Choices"** (blue).
- Field errors appear as red text under the fieldset.

**Step C — Confirmation modal** (full-screen overlay `rgba(17,55,90,.65)`):
- White modal card (max 640px, radius 16px, scrollable to 90vh), heading **"Confirm your choices"**.
- Line: "Voting as **{Name} ({ID})**. Once confirmed, your vote cannot be changed."
- Table: **Position | Your Choice** (choice = 30px mini portrait + name).
- Buttons: **Edit choices** (secondary/light) closes modal; **Submit vote** (primary blue).

**Step D — Success modal:**
- Green circular check mark on pale-green disc, heading **"Vote Submitted Successfully"**, "Thank you! Your vote has been recorded and cannot be changed."
- Buttons: **View results** (secondary) · **Done** (primary).

---

## 4. Results (`/results/`)
**While election is open:** single centered success-style box — **"Results are not available yet"** + "Voting is currently in progress…" + **Go to voting** button.

**After close:** one **results group card per position**:
- Group heading = **position name in uppercase** (navy/blue).
- Table: `Candidate | Votes`, uppercase gray headers, subtle row dividers.
  - Candidate cell: **40px circular photo** + full name.
  - Votes cell: **bold count**.
- Below table: "Total votes: N" (muted).
- **Winner line:** "Winner: **{Name}** (N votes)" — name in green. Ties handled: "Winner: **A** tied with **B**, **C** (N votes each)".

---

## 5. Staff Dashboard (`/dashboard/`) — admin infographic
Wide shell (`1400px`), gradient navy sidebar + light-gray content area.

**Sidebar (232px, navy gradient `#194264→#11375a`):**
- Brand: orange rounded square with **✓** + "Westland Elections Room".
- Nav: **Dashboard** (active = orange pill/navy text), **Live results**, **Admin panel**, **Public voting**, **Sign out**. Icons = simple UTF-8 glyphs (▨ ▥ ⚙ ✎). Hover = white tint.
- Bottom card: current admin name + "Election administrator · staff only".

**Topbar:**
- H1 **"Election dashboard"**, sub-line = election name + pill badge **OPENED** (green) / **CLOSED** (red).
- Actions: **Manage in admin** (white/ghost), **View live results** (orange).

**Stat cards (4-up grid → 2-up ≤1000px → 1-up ≤620px):**
Each = white card, orange gradient top edge, large navy number, small icon tile (orange tint), label, thin rounded progress bar (orange):
1. **Eligible voters** (bar 100%)
2. **Students who voted**
3. **Total votes cast**
4. **Voter turnout %**

**Bulk upload (superuser only):**
- Panel titled "Bulk upload students" with orange `CSV` chip; hint on column format (`student_id, full_name, gender, class_level`, optional header, duplicates skipped).
- Dashed-border form: file input + **Upload students** (navy) button.
- Result summary line + list of per-row errors/duplicates.

**Current standings:** per position — sub-heading (name + vote total); rows: mini circular photo + name | **horizontal bar** (orange gradient, width = share %) | bold count. **Leader row:** navy bar + name marked with a gold **★**.

**Recent votes:** table `Student | Position | Candidate | When` (latest 8), zebra striping, hover tint.

**Voting attendance:**
- Summary "**X** of **Y** students have voted".
- Filter pills: **All · Voted (X) · Not yet voted (Y)** — client-side toggle without page reload.
- Scrollable table (`max-height 400px`): `Student ID | Name | Status` — status = **Voted** (green chip + timestamp) or **Not voted** (red chip).

---

## 6. Responsive behavior
- Public: content stacks gracefully; ballot gallery 3→2→1 columns; navbar wraps.
- Dashboard: at ≤860px sidebar converts to a **horizontal top strip** (brand left, nav inline); stats collapse; tables stay scrollable horizontally.

---

## Notes / opportunities for the designer
- **Two distinct visual languages** (public glassy-yellow vs dashboard navy/orange) — a prime unification opportunity.
- Dashboard links to the Django Admin (currently the `unfold` theme build) — an "Admin panel" app view could replace that.
- No footer on public pages; the election-status UI exists on Home but could be surfaced more strongly.
- Data visualization is minimal (bars/pills) — room for charts (turnout over time, per-position vote share, donut for voter ratios).