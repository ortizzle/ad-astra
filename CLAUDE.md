# Claude Guide — Ad Astra

> **This repo is public.** Names, schools, teachers and Drive folder IDs are
> deliberately absent here — they live in the `roster` record (entered in the
> grown-up settings, carried by the private Gist) and in Claude's private
> project memory. Do not paste them back into any tracked file.

## What this is

A school-year learning PWA for one **8th-grade** student, SY 2026–27.
Successor to the Summer Science Lab, rebuilt from scratch around three things the
old app didn't have: her **real class schedule and academic calendar**, a **shared
data layer** so a parent sees the same content and progress from their own device, and
an **automated content pipeline** so study material comes from Drive documents
instead of being hand-written into the source.

The same engine is forked for a younger sibling in **Wayfinder** — see the
sibling-app note below.

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
| `miss` | A Growth Zone entry — one missed question, plus its `box`/`due` on the review ladder |
| `cleared` | A question that survived all five review intervals |
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
the same Gist ID and a token with only the `gist` scope. Content a parent generates
on a laptop appears on the student's phone; her progress appears on theirs.

The Gist ID and token live in `localStorage` only. **Never hardcode either into
the HTML — this repo is public.** Same for the Anthropic API key.

The app is fully usable with sync off. `Sync.load()` swallows network errors by
design: offline-first, local always works.

---

## School data

`CLASSES` and `CAL` are derived from the school's published `.ics` timetable and
academic-calendar PDF. **This** schedule is identical Monday–Friday, which is why
`CLASSES` is a flat array; Wayfinder's rotates by weekday and is structured
differently.

`CAL.closed` holds no-school date ranges; `CAL.quarters` drives the quarter
countdown; `CAL.milestones` drives "on the horizon" (Pre-Comp exams 12/15–12/16,
Comp exams 5/11–5/13, etc. — the grades 6–8 testing calendar).

All date logic uses **Arizona time** via the `AZ` helper. Arizona has no DST.
Never derive "today" from `toISOString()` — it rolls over at 5pm local.

---

## Adding study content

Three routes, in order of preference:

1. **From Drive (best).** Pull the class materials from the student's Drive folder,
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
facts — only real rooms, times, and (once entered in `roster`) teachers.

---

## Visual language

Aquamarine is the *app's* colour (chrome, buttons, accents, and whatever she picks
in Personalize). **Each subject owns its own colour and texture** so the app never
reads as one flat wash of teal — that was direct feedback and it matters.

`CLASSES` carries `color`, `g1`, `g2` per subject; `paint(node, cls)` adds
`.subj .pat-<id>` and sets the CSS custom properties. Textures are pure CSS:
graph paper (Algebra), ruled paper with a red margin (English), cell dots
(Biology), orbit arcs (Physics), columns (History), a Greek key (Latin), curtain
stripes (Theatre). Applied to subject tiles, flashcard faces, and the current
period row.

> ⚠️ **The pattern layers live in `background-image`, so any later rule using the
> `background` shorthand silently wipes them.** This bit twice. `.face` and
> `.face.back` are therefore written as `:not(.subj)`. If you add a component
> that can be painted, use `background-color`, or scope the plain background with
> `:not(.subj)`.

**the student chose "Studio"** from `prototype.html` (which also holds Field Notes and
Aurora, rendered as real UI). That decision is made — don't re-litigate it. The
prototype file stays as a reference; it is a dev artifact, not cached by the
service worker and not linked from the app.

**She picks each subject's colour** in Settings → Subject colours, from the
twelve options in `SUBJECT_PALETTE`. `CLASSES[].pal` is only the default;
`palOf(cls)` resolves her override from `prefs().subjectColors` first. Never read
a hardcoded colour off a class — go through `palOf()` or `classColor()`.

Every palette entry is a mid-tone → deep pair, and `.subj::after` lays a
**bottom scrim** under the text. That combination is what keeps labels readable
on any hue. If you add a palette option, keep it in that tonal range and check
white text over it — bold is fine, unreadable is not.

## Backups

The in-app "Back up" button uses the **Web Share API** (`navigator.share` with a
file), which on her Pixel opens the Android share sheet so Drive is one tap away.
Desktop falls back to a plain download. There is deliberately **no Google OAuth**
— writing to Drive directly would need a client ID and a backend, which breaks
the no-backend rule for a once-a-week action.

The Drive folder is **Ad Astra Backups**, inside her 8th Grade folder:
`<in the private notes>`. The Setup screen links straight to it.

## The psychology features — read before editing the copy

Three features are deliberately grounded in research rather than vibes. The exact
wording matters; do not "warm them up" into generic encouragement.

**Morning affirmations** (`AFFIRMATIONS`). Built on four findings: growth mindset
(Dweck — praise process and strategy, *never* fixed traits; "you're so smart"
measurably reduces persistence after failure), self-affirmation theory (Cohen &
Sherman — briefly connecting to your own values before an evaluative situation
buffers stress), self-compassion (Neff — permission to struggle predicts more
persistence than self-criticism), and self-determination theory (Deci & Ryan —
autonomy language beats pressure language). Rules that follow from that: no trait
praise, no "you'll ace it", no toxic positivity, no exclamation marks. Pools are
tagged `general` / `test` / `recover` and picked by context — a test within two
days, or recent accuracy under 65%. The pick is **deterministic by date** so it
does not reshuffle on every render.

**Emotion check** (`SCREENS.checkin`, `SCREENS.postmood`). Two taps before every
quiz, one after. The readiness rating is not decoration — it is compared to her
actual score in `calibrationPairs()`, which tells her whether her gut feeling
about being prepared is accurate. That gap ("you felt more ready than this turned
out") is the metacognitive payload of the whole feature. A low mood rating
surfaces a supportive note with an explicit permission to stop; keep that.

**Study-habit guidance** (`HABITS`, and the tutor system prompt). Retrieval
practice, spaced practice, interleaving, sleep, self-explanation. These are the
techniques with the strongest evidence base — do not swap them for study tips
that merely sound good.

## Voice

the student is sharp and responds to wit and real stakes. Direct, never condescending,
never over-explaining, dry rather than bubbly. The Growth Zone is framed as
information, not a verdict — that framing is load-bearing, don't soften it into
praise.

**Everything she sees is second person.** "Your school day", not "her school
day"; "your subjects", not "the student's subjects". The app talks *to* her, not
*about* her. Third person is correct in exactly two places: the parent view
(the parent reading about her) and the model system prompts. This was explicit
feedback — check any new copy against it.

## Screen layout — who owns what

| Tab | Holds |
|---|---|
| **Today** | The school day *only*: what class is now/next, the full schedule, upcoming tests, on the horizon. **No XP, level, streak or affirmation** — it is not a dashboard. |
| **Study** | The daily affirmation with its like/read buttons, "what to study today", subject tiles, and three whole-card buttons: Timer, Tutor, New study set. |
| **Growth** | The Growth Zone: what is due for review today, and everything still settling. Carries a count badge in the nav when anything is due. |
| **Stars** | All the gamification: level bar, streak/minutes/revisit strip, totals, badges. |
| **Settings** | Hers: appearance, accent, per-subject colours, avatar, nickname, motto, focus-timer default, and the door to the grown-up area. |
| **Parent** (passcoded) | Progress and effort, tests and scores, weekly goals, **what she is using** (tutor questions verbatim, timer/quiz/flashcard counts) — *plus* Gist sync, the Anthropic API key, and backup/restore. |

Focus does **not** get its own tab; it is reached from Study.

### Spaced repetition — the miss ladder

A missed question does not clear the moment she gets it right once. Each `miss`
carries a `box` (0–4) and a `due` date, stepped by `scheduleMiss()` along
`BOX_GAPS = [1, 2, 4, 8, 21]` days:

- **Miss it** → `box` resets to 0, back tomorrow. No partial credit for a near miss.
- **Get it right** → `box` moves up one, the gap widens.
- **Right at box 4** → a `cleared` record is written and the `miss` is tombstoned.
  It has survived every interval out to three weeks; that is the bar for "learned".

`dueMisses()` returns everything due today, easiest-forgotten first (lowest box).
`buildReviewUnit()` assembles those into a synthetic unit with `id:'__review__'`,
which the quiz screen loads through `unitFor()` instead of `DATA.records`.

Three things about the review unit are load-bearing:

- It is **never put into `DATA.records`** — it is a view, not content, and syncing
  it would mean syncing a snapshot of a moment.
- `missAsQuestion()` **rewrites each question's `id` to the miss id.** Questions
  are numbered per unit and restart at 1, so a mixed-subject round would collide.
- `answer()` credits the `qstat` tally to the question's **original** unit and
  class via `q._missId`, or the parent view would attribute the work to nothing.

The review round deliberately **skips the readiness check-in**. That question is
about one unit, and this runs most days — friction there would kill the habit.

Existing misses from before this shipped are stamped `box:0, due:today` by the
v3 migration, and `dueMisses()` also treats a missing `due` as due, so nothing
gets stranded.

**The brand block in the header is the way home** (`go('today')`). There are no
back buttons anywhere, so this is the only escape hatch — do not repurpose it.

## Light mode

`prefs.theme` is `auto` | `light` | `dark`. `applyTheme()` resolves `auto`
against `prefers-color-scheme` and always writes an explicit
`document.documentElement.dataset.theme`, so the CSS only ever handles two
states. A `matchMedia` listener re-applies when the system flips and the
preference is `auto`.

**`--ac` vs `--ac-fg`.** `--ac` is the raw accent, used for *fills* (buttons,
bars, borders) and is fine in both modes. `--ac-fg` is the accent as *text* —
identical to `--ac` in dark, deepened to `color-mix(… 40%, #04302a)` in light,
because raw aquamarine on white fails contrast. **Any new accent-coloured text
must use `--ac-fg`.** All six accents were measured at ≥5.2:1 in light and ≥7.3:1
in dark against their surface.

Subject cards keep their saturated fills in both modes by design — they are the
app's colour anchor, and the bottom scrim already guarantees the label contrast.

## Tutor

Ordered deliberately: **the ask box first**, then one or two techniques, then the
plan, then past questions.

- **She always gets an answer immediately.** With a key, Claude answers. Without
  one — or if the call fails — `localAnswer()` replies by reading her actual
  numbers and matching the question against keyword groups (forgetting, time,
  focus, tests, understanding), then names the technique that fits. It is not
  pretending to be the model, and the UI says which answered.
- **Every question is recorded either way**, with the answer and a `source` of
  `ai` or `app`, and surfaced verbatim in the parent view. Flagging that she is
  stuck is the point; the AI is an upgrade to the reply, not a precondition.
- `HABITS` entries each carry a `when(ctx)` returning *why it is relevant right
  now* or `null`; `relevantHabits()` shows at most two. Never render the whole
  list — a wall of eight tips is wallpaper.

## Parent view

Behind a passcode in You → Grown-ups. The passcode is a SHA-256 hash in
localStorage, set on first open — there is no default. **This deters a curious
12-year-old; it is not real security and should not be described as such.** It is
per-device by design (it is not a record, so it does not sync).

It shows effort (weekly minutes, 14-day chart, streak, focus time), accuracy by
subject, strong vs shaky questions from `qstat`, mood and calibration trends, real
test scores the parent enters, and weekly per-subject minute goals that feed the study
plan. Deliberately understated in tone so it does not read as surveillance.

## Study plan

`studyPlan(date)` is rule-based and always works without an API key. It scores
each subject on: days until the next unscored assessment, Growth Zone count,
accuracy under 70%, days since last studied, and progress against the weekly goal.
Top three surface on Today with a concrete minute recommendation. The AI tutor is
a layer *on top* of this, not a replacement — if the key is missing the app still
gives specific advice.

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

## Phase 2 — the student

the student is **4th grade at the primary school**, same first/last day
(8/3/2026 – 5/21/2027) but a **different academic calendar PDF** and a schedule
that **rotates by weekday**:

- Fixed daily: Accelerated Math 4 (7:40), English 4 (9:30), Recess, Lunch,
  Science 4 (12:00), History 4 (1:50)
- Rotating 8:35 slot: Musical Theatre (M), Visual Arts (Tu), Computer Enrichment
  (W), PE Martial Arts (Th), Engineering & Technology (F)
- Rotating 11:05 and 12:55 slots vary similarly; Thursday has Study Hall

That means `CLASSES` must become **keyed by weekday** for the student. The cleanest fork
is: copy this repo, replace `STUDENT` / `CLASSES` / `CAL`, change the theme, and
leave the record store, sync, badge engine, and study screens untouched.

Her Drive folder also has a 4th-grade supply list and the CPS academic calendar.

**Open question for the parent:** two separate apps (current plan) vs. one app with a
profile picker. Two apps means two themes and two home-screen icons — better for
the kids. One app means one deploy and one Gist — better for maintenance.

---

## Deploy

Live on GitHub Pages under the `ortizzle` account; deploy is a `git push` to the
Pages branch via `gh`. **Bump `CACHE_VERSION` in `sw.js` on every deploy** —
mobile Chrome caches hard, and a stale service worker will serve the old app
indefinitely. Hard-refresh or append `?v=N` when verifying.
