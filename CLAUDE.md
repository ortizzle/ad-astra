# Claude Guide — Ad Astra

## What this is

A school-year learning PWA for **Sedona (8th grade, BASIS Chandler, SY 2026–27)**.
Successor to the Summer Science Lab, rebuilt from scratch around three things the
old app didn't have: her **real class schedule and academic calendar**, a **shared
data layer** so Chris sees the same content and progress from his own device, and
an **automated content pipeline** so study material comes from Drive documents
instead of being hand-written into the source.

The same engine is intended to be forked for **River (4th grade, BASIS Chandler
Primary South)** — see "Phase 2" below.

---

## Architecture

Four files. No build step, no backend, no npm.

| File | Purpose |
|---|---|
| `index.html` | The entire app — inline CSS and JS |
| `manifest.json` | PWA install metadata |
| `icon.svg` | App icon (constellation mark) |
| `sw.js` | Service worker. **Bump `CACHE_VERSION` on every deploy.** |

Keep it this way. If `index.html` approaches ~4,000 lines, raise splitting into
`index.html` + separate `.js` files loaded with `<script src>` (still no build
step) rather than doing it unilaterally.

---

## The data model — read this before changing storage

Everything is one flat **record store**, `DATA.records`, keyed by id. Every record
has `id`, `type`, and `updatedAt`. This is what makes Gist sync safe.

| `type` | What it is |
|---|---|
| `unit` | Study content: `{classId, title, cards[], questions[]}` |
| `log` | One completed study session: `{mode, classId, unitId, date, correct, total, seconds, xp, hints}` |
| `focus` | One completed Pomodoro block: `{classId, minutes, date, xp}` |
| `miss` | A Growth Zone entry — one missed question |
| `cleared` | A Growth Zone item resolved on a retake |
| `qstat` | Per-question tally `{qid, attempts, correct}` — powers strong/weak topics |
| `mood` | An emotion check: `{when:'pre'|'post', logId, readiness, feeling}` |
| `assess` | A test/quiz/project: `{classId, kind, title, date, score}` |
| `badge` | An earned badge |
| `prefs` | Her personalization (accent, avatar, nickname, motto, goals) — **one singleton record with `id:'prefs'`** |

**XP, level, streak, and accuracy are never stored.** They are derived from `log`
and `focus` records by `stats()`. This is deliberate: derived values cannot drift
between two devices, so there is no counter to reconcile during a merge. Do not
add a stored `xp` field — recompute instead.

`prefs` is a record rather than a localStorage key on purpose, so her theme and
goals follow her to any device she signs the Gist into. Secrets (API key, Gist
token, parent passcode hash) stay in localStorage and are deliberately **not**
records — they must never enter the shared Gist.

**Deletes are tombstones.** `softDelete(id)` writes `{deleted:true, updatedAt}`;
it never removes the key. Without this, deleting a unit on one device and syncing
from another resurrects it. Tombstones older than 60 days are purged during merge.

**Merging** is per-record, newest `updatedAt` wins (`Sync.merge`). Saving always
fetches remote first, merges, then writes — never a blind overwrite.

If you change a record's shape, bump `SCHEMA_VERSION` and add a step to
`migrate()` so older devices upgrade in place.

---

## Sync

Progress *and* content flow through one private GitHub Gist. Both devices enter
the same Gist ID and a token with only the `gist` scope, in Setup. Content Chris
generates on his laptop appears on Sedona's phone; her progress appears on his.

The Gist ID and token live in `localStorage` only. **Never hardcode either into
the HTML — this repo is public.** Same for the Anthropic API key.

The app is fully usable with sync off. `Sync.load()` swallows network errors by
design: offline-first, local always works.

---

## School data

Both `CLASSES` and `CAL` come from files in Sedona's Drive folder (the
`.ics` class schedule and the BASIS Chandler SY26-27 academic calendar PDF).
Sedona's schedule is **identical Monday–Friday**, which is why `CLASSES` is a flat
array. River's rotates by weekday — see Phase 2.

`CAL.closed` holds no-school date ranges; `CAL.quarters` drives the quarter
countdown; `CAL.milestones` drives "on the horizon" (Pre-Comp exams 12/15–12/16,
Comp exams 5/11–5/13, etc. — the grades 6–8 testing calendar).

All date logic uses **Arizona time** via the `AZ` helper. Arizona has no DST.
Never derive "today" from `toISOString()` — it rolls over at 5pm local.

---

## Adding study content

Three routes, in order of preference:

1. **From Drive (best).** Pull the class materials from Sedona's Drive folder,
   write a `unit` record, and add it to the store. Anchor every card and question
   to the actual source — do not invent facts. This is the intended workflow once
   teachers start posting notes.
2. **In-app AI generation.** Setup → Anthropic key, then Study → "Generate a unit
   from notes". Uses `claude-opus-5` with a JSON schema via `output_config.format`,
   so the response is guaranteed-valid JSON with no fence-stripping. Browser-direct
   (`anthropic-dangerous-direct-browser-access`), key from `localStorage`.
3. **Hand-written.** Only for small fixes.

### Unit shape

```js
{
  id, type:'unit', classId:'bio', title:'Unit 3: Cell Division',
  quarter:2, source:'Bio notes 10/14 (Drive)',
  cards:[ {id, term, def, hint, eq?} ],
  questions:[ {id, lv:1|2|3, q, opts:[4], ans:0-3, hint, ex:{main, tip, mnemonic?}} ]
}
```

- 15–30 cards; 18–24 questions (6–8 each at level 1 recall / 2 apply / 3 analyze).
- `opts` must be exactly 4 with no duplicates, and `ans` must index into it.
  `generateUnit()` filters malformed questions before storing — keep that guard.
- `hint` on a card is a memory hook, never a restatement of the definition.
- `ex.main` explains *why* the answer is right, not just what it is.
- `classId:'__all__'` makes a unit appear under every class (the orientation unit
  uses this).

### The orientation unit

`buildOrientationUnit()` generates "First Week: Rooms & Teachers" from the
schedule data at boot. It is regenerated on every load and should not be
hand-edited. It exists so the app is useful before any class content arrives, and
so the study engine is demonstrably working. It contains no invented academic
facts — only her real rooms, times, and teachers.

---

## Voice

Sedona is sharp and responds to wit and real stakes. Direct, never condescending,
never over-explaining. The Growth Zone is framed as information, not a verdict —
that framing is load-bearing, don't soften it into praise.

---

## Non-negotiables (these are past bugs, not preferences)

- All DOM via `createElement`/`appendChild`; all events via `addEventListener`.
  **Never** inline `onclick` or `innerHTML` with interpolated data.
- **Never** `alert()`, `confirm()`, or `prompt()` — use `showModal()`.
- Chrome on Android (Pixel) is the mobile target. 44px minimum tap targets,
  `viewport-fit=cover` with safe-area insets, no hover-dependent UI.
- Arizona time via `AZ` for every date operation.
- Fetch-merge-write for every sync; tombstones for every delete.
- Secrets in `localStorage` via the Setup UI, never in source.

---

## Phase 2 — River

River is **4th grade at BASIS Chandler Primary South**, same first/last day
(8/3/2026 – 5/21/2027) but a **different academic calendar PDF** and a schedule
that **rotates by weekday**:

- Fixed daily: Accelerated Math 4 (7:40), English 4 (9:30), Recess, Lunch,
  Science 4 (12:00), History 4 (1:50)
- Rotating 8:35 slot: Musical Theatre (M), Visual Arts (Tu), Computer Enrichment
  (W), PE Martial Arts (Th), Engineering & Technology (F)
- Rotating 11:05 and 12:55 slots vary similarly; Thursday has Study Hall

That means `CLASSES` must become **keyed by weekday** for River. The cleanest fork
is: copy this repo, replace `STUDENT` / `CLASSES` / `CAL`, change the theme, and
leave the record store, sync, badge engine, and study screens untouched.

Her Drive folder also has a 4th-grade supply list and the CPS academic calendar.

**Open question for Chris:** two separate apps (current plan) vs. one app with a
profile picker. Two apps means two themes and two home-screen icons — better for
the kids. One app means one deploy and one Gist — better for maintenance.

---

## Deploy

Not yet deployed. Repo lives under the `ortizzle` GitHub account; deploy is a
`git push` to the Pages branch via `gh`. After deploying, bump `CACHE_VERSION` in
`sw.js` and remember mobile Chrome caches hard — hard-refresh or append `?v=N`
when verifying.
