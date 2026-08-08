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
| `unit` | Study content: `{classId, title, cards[], questions[], status}`. `status:'draft'` means it is waiting for a grown-up and is hidden from her; absent or `'approved'` means live. |
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
  questions:[ {id, lv:1|2|3, q, opts:[4], ans:0-3, hint, steps:[…],
               ex:{main, tip, mnemonic?}} ]
}
```

**`steps` (v26, both apps): every question carries 3–6 strings that walk from
the question to the answer, one concrete move each, last step states the
answer.** After a wrong answer the quiz offers "Walk me through it" and reveals
them one per tap — free, because it is remediation, not part of the hint
economy, and only after answering so it teaches rather than leaks. Misses copy
`steps` onto the miss record so review-ladder rounds keep the walkthrough.
`UNIT_SCHEMA` requires it on generated units; hand-written units should include
it too.

Mergeable content files live in `content/` — each is a `{v, records}` JSON.
List every shipped file in `CONTENT_LIBRARY`; the parent view's "Check the
library" button fetches them from the app's own origin (no account, no
backend), merges through `Sync.merge`, and reports what arrived. Tombstones
beat library copies, so a discarded unit never resurrects — to re-ship one
deliberately, bump its `updatedAt` past the discard. Restore still works for
the same files as a manual fallback. Units shipped either way are
`status:'draft'`, so they land in the review queue, not in her app.

**Stamp `updatedAt` in the PAST — hours back, minimum.** A future-stamped
record wins every merge against real edits until the clock catches up, so the
parent's approvals silently revert to draft. This bit on 2026-08-08 (two files
shipped ~18h ahead). `migrate()` now clamps any record more than an hour in
the future on every ingest, so gists self-heal — but the clamp is a backstop,
not permission.

**Reading-companion additions (v32, both apps):** questions may carry
`passage` (a short quoted excerpt, under ~40 words and quoted exactly,
rendered as a styled quotation) and `kind:'order'` (put-in-order: `opts`
lists exactly 4 events in the CORRECT sequence with `ans:0`; she sees them
shuffled and taps them into order; inside `answer()`, −2 is the
wrong-sequence sentinel and −1 stays out-of-time). Misses carry `kind` and
`passage`, so review-ladder rounds re-ask faithfully. Book units set
`book:true`, which hides Beat the clock — a literature quiz is not a race.
Book units are split by chapter range, spoiler-bounded, and released through
the draft queue as she reads; ungraded "ponder" cards are a content
convention, not a mechanic.

- 15–30 cards; 18–24 questions (6–8 each at level 1 recall / 2 apply / 3 analyze).
  Quizzes run in **rounds of 5** (`QUIZ_ROUND`), least-practised questions first —
  don't tune question counts around "one sitting"; rounds handle that.
- `opts` must be exactly 4 with no duplicates, and `ans` must index into it.
  `generateUnit()` filters malformed questions before storing — keep that guard.
- `hint` on a card is a memory hook, never a restatement of the definition.
- `ex.main` explains *why* the answer is right, not just what it is.
- `classId:'__all__'` makes a unit appear under every class.

### Content rules (Chris-approved, 2026-08 — apply to EVERY unit, both apps)

- **Standalone always.** Never reference "the worksheet", "your practice sheet",
  or a numbered problem from the source material. A question restates all the
  context it needs. Fresh scenarios beat reworded worksheet problems — the sheets
  are her homework; this app is *extra*.
- **Bold answer first.** A card `def` LEADS with the straightforward answer
  wrapped in `**bold**` (one short sentence that works alone as the study
  answer), then at most 2–3 supporting `\n• ` bullet lines. `richify()` renders
  the bold; never use innerHTML for content.
- **Bullets are real.** Multi-item definitions/explanations use `\n• ` lines —
  the CSS preserves newlines.
- **Graphs where graphs teach.** Attach a `graph` spec (see `renderGraph()`:
  window `w`, typed `series` — line / vertex-form parabola / abs / pts — plus
  marked `pts`, `xl`/`yl` labels) to any card or question about reading a graph,
  and say "the graph shown". Verify the plotted function actually has the
  features the text claims. Math/physics units should use them liberally.
- **Formulas go in `eq`** fields — they render in textbook serif italics.
- **Verify provided answers.** When source material includes answer keys, re-derive
  every answer independently and flag misprints to Chris (they happen — the
  Lesson 1-1 vocab key had two).
- **Video-based material:** transcripts are usually unfetchable; build from the
  sheets and say so in `parentNote` — never invent video specifics.
- **Encouragement, not scorekeeping.** Answer feedback comes from `CHEER_RIGHT` /
  `CHEER_WRONG` — varied, warm, growth-mindset, no exclamation-mark cheerleading.
- Every unit ships as `status:'draft'` for the review queue. No exceptions.

### Retired: the orientation unit

"First Week: Rooms & Teachers" was removed in v22 (schema v4 tombstones
`unit-orientation` on migrate). Don't reintroduce boot-generated units.

---

## Visual language

Aquamarine is the *app's* colour (chrome, buttons, accents, and whatever she picks
in Personalize). **Each subject owns its own colour and texture** so the app never
reads as one flat wash of teal — that was direct feedback and it matters.

Since v22 this goes further: **any screen with a subject context (unit, cards,
quiz, focus, brief) overrides `--ac` on `#screen`** with the class palette's
`g1`, so buttons, progress bars, and eyebrows all wear the subject's colour while
she studies it. The derived tints (`--ac-8/14/25`, `--ac-fg`) are re-mixed on
`#screen` in CSS — if you add a new derived accent var, re-mix it there too or
subject screens won't pick it up.

Layout: flashcard **terms are centered, definitions left-aligned** (ruled-page
read); stacked buttons keep ≥10px between them (`.btn+.btn` rule) — don't crowd
tap targets to save vertical space.

**Versioning:** `APP_VERSION` in index.html ('vNN · one-to-three words') is shown
at the bottom of Settings and MUST be bumped together with `sw.js`
`CACHE_VERSION` on every deploy — same number, matching summary.

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

### Personalization (v27, both apps)

Everything here lives on `prefs` (synced, no new record types) and is **free
and flat** — nothing unlockable, ever. Cosmetics must never become rewards;
that would turn identity into a grind economy, the exact mechanic these apps
refuse. All of it holds the existing contrast bar.

- **Skies** (`prefs.sky`, `SKIES`, `[data-sky=…]` CSS): alternate canvas
  washes. Only `--wash-1/2` change — `--ink` and every text colour stay put,
  so the contrast measurements hold under every sky. Sky rosters are identity
  and differ per app.
- **Celebration styles** (`prefs.fx`, `FX_STYLES`, `celebrate()`): confetti,
  stars, petals, bubbles, quiet glow. Same triggers, same rules; "quiet"
  exists because confetti can turn cringe overnight at 13 and opting down
  should cost nothing.
- **Subject icons** (`prefs.subjectIcons`, `ICON_CHOICES`): picked in the
  subject-colour modal. `applyTheme()` writes the override onto the class
  objects themselves (`baseIcon` keeps the default recoverable), so every
  render site picks it up without knowing the feature exists.
- **Badge pins** (`prefs.pins`): up to three EARNED badges featured at the
  top of Stars. Curation of display only — no new mechanics.
- **Companion extras**: pool lines may carry `{name}` — rendered with the
  roster first name, dropped from the pool when no name is set. `prefs.mline`
  is one line of hers that joins the idle rotation; her words, so the
  curation rules (which bind only our copy) do not apply to it.

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

## The companion

A creature she picks and names in Settings (`prefs.companion = {sp, nm}`,
synced; `null`/"—" = off, the default). Landed here **at her request**
(2026-08) — it began as Wayfinder-only and the agreed bar for porting it was
her asking. The two apps' companions share rules but **not** roster or copy
(this one is night-sky and ocean, the lines are drier) — identity, not
engine, so do not sync them as parity.

It is a **messenger, not a second voice**: every line comes from the curated
`COMPANION_*` pools or is assembled from `studyPlan()`/`dueMisses()`, never
from the model. Deliberate rules, do not relax: never interrupts (Study perch
and quiz-results modal only), never sad or disappointed (under-80% gets the
`COMPANION_STEADY` pool — calm, dry, forward-looking), process praise only,
no care-and-feeding mechanics, no stored counters, owns no records.

**Species voices** (`COMPANION_VOICES`, v26): a species listed there overrides
the default pools; everyone else falls back. The dragon's voice is hers —
witty, dry, a shade dark, always landing on reassurance. Dark humor about the
QUESTIONS is fine; gloom about HER never is. Same hard rules as the defaults:
no exclamation marks, no trait praise, never sad.

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

### School events — the newsletter layer

`CAL.events` holds dated items lifted from the school newsletter. They live in
**code, not the record store**, on purpose: they are identical on every device,
so one deploy updates all four phones and nobody types anything. Per-class tests
stay as `assess` records — those are hers, and only she and a parent know them.

```js
{start:'2026-12-15', end:'2026-12-16', name:'Pre-Comp Exams', icon:'✍️',
 kind:'exam', note:'The dry run for Comps — same shape, lower stakes.'}
```

`end` is optional (a one-day event). Helpers: `eventsOn(date)`,
`upcomingEvents(from, days)`, `earlyReleaseOn(date)`, `whenLabel(from, ev)`.

Three render sites:
- **Pinned above the day's periods** on the Today schedule — styled `.evt`, not
  as a tenth period, because it is not one.
- **"Coming up"**, merged with her own assessments and sorted by date. A
  Mini-Comp and a Friday maths quiz are the same thing to plan around, so
  splitting them into two lists would only hide one.
- **Pick-up row**, when `early:true` — see below.

**`kind` sets the tone, not just the icon.** `exam` gets the study nudge;
`benchmark` says explicitly that there is nothing to revise for, because a
diagnostic that reads like an exam gets crammed for, which is the wrong response;
`celebration` and `community` are things to look forward to; `note` and `early`
render quiet.

**Early release is a correctness issue, not decoration.** The pick-up row is what
a parent plans around, so on an `early:true` day it must never show the usual
time. It falls back to the event's `dismiss` string, or says the time is not
published — the school lists the days but not the times.

**In-progress events stay listed** until their last day (`evEnd(e) >= from`), so
a two-day exam does not vanish from "Coming up" halfway through, and shows
"Day 1 of 2".

`milestones` is now only structural — quarter boundaries, first and last day.
Anything dated and actionable belongs in `events`. Keep them disjoint or the same
item renders twice, once in each list.

### Content review — nothing reaches her unread

Generated units are written with `status:'draft'` and **`units()` filters drafts
out**, so a draft is invisible everywhere on the student side. A unit with no
`status` predates this gate and counts as approved.

- `drafts()` — the queue. Surfaced at the top of the parent view and as a count
  on the Study Material card.
- `SCREENS.review` — the queue list. `SCREENS.reviewunit` — every card and
  question in full, with the correct answer marked.
- Cuts are held in `ctx._cutC` / `ctx._cutQ` and only written on **Approve**, so
  backing out of a half-reviewed unit changes nothing.
- Generating from inside the parent area (`ctx.fromParent`) goes straight to the
  review screen. Generating from her side shows a plain explanation of why it is
  held — the framing is "catching what the model got wrong", never "checking on you".

### The source contract — what a unit owes the family

Every unit built from class material follows one framework, encoded in
`UNIT_SCHEMA` and the system prompt, not left to the model's discretion.

**The original is never altered.** Nothing is written back to Drive — the app has
no write path there and should not gain one. This is an engineering guarantee and
stays out of the UI: a student reading a recap does not need telling that a file
was left alone. Say it here, not on screen.

What the screen does show is the source, by name — `u.srcName`, entered on the
generate screen and rendered by `citeEl()` as a plain "From <file>". With no name
the line is omitted entirely rather than filled with a placeholder sentence.

**Every block declares its origin.** `from:'source'` means the substance is the
teacher's; `from:'added'` means it is our framing, advice or pacing. This is not
a tone convention — it is a schema field, rendered as a badge by `provTag()`:

| | `source` | `added` |
|---|---|---|
| Label | From class material | Study suggestion |
| Covers | facts, definitions, formulas, stated objectives, cards and questions traceable to the material | why-it-matters, study advice, time estimates, memory hooks, inferred objectives |

**Unmarked defaults to `added`, and this direction matters.** `generateUnit()`
coerces any missing or unrecognised flag to `'added'`. Defaulting the other way
would let a dropped field quietly borrow the school's authority, which is the
one failure the whole scheme exists to prevent. The prompt says the same thing:
*if you are unsure which a block is, it is "added"*.

**The blocks**, all required by the schema so a partial unit fails loudly rather
than silently shipping half a briefing:

- `summary` — what the material covers, in her language, naming the source. This
  block stands in for the teacher, so the prompt forbids editorialising in it.
- `why` — why it is worth knowing. Effectively always `added`.
- `objectives[]` — 3–5 "after this you should be able to…", each flagged
  individually: `source` when the material states it, `added` when inferred.
- `parentNote` — one paragraph for a parent who was not in the room, including
  the thing most likely to trip her up. Shown in the review queue and reachable
  later from the parent portal.
- `nextUp` — one line to her plus `minutes`, an honest estimate. The prompt
  explicitly forbids rounding to a comfortable number.

`SCREENS.brief` renders this for her; `SCREENS.reviewunit` renders the same plus
the parent note, with a legend explaining what green means. Units created before
this shipped have none of these fields and degrade to just the cards and quiz —
every render site guards, and no migration backfills them, because marking old
content `source` would be a lie.

### The Sky Map (v29, both apps)

The Stars tab's star chart, made literal: each school week is a named
constellation of seven stars, one per day, lit by any day with a `log` or
`focus` record. `SKY_GOAL` (5) of 7 completes the week and it joins the sky
map (`SCREENS.skymap`). Rules that are the point, not the decoration:

- **Nothing breaks.** A short week stays dim and the next starts fresh — no
  streak-style loss, no negative copy anywhere on the map.
- **Everything is derived** from existing records (`studyDates()` →
  `skyWeek(i)`), so it backfills instantly, syncs for free, and stores no
  counters. Do not add a stored "constellation" record.
- **Stars light for showing up, never for scores**, and they are never
  currency — no redemption, in-app or implied.
- Rosters are identity: this app uses the real sky (`CONSTELLATIONS`, one
  honest line of astronomy each); Wayfinder invents playful ones. Keep the
  lore accurate here and keep the rosters divergent.

### The Bookshelf (v36 / Wayfinder v31, both apps)

Units that belong to a series render on the subject screen as **book spines on
a shelf** (`shelvesFor()`, `spineEl()`, `SCREENS.shelf`); standalone units stay
as ordinary cards below. Rules that are the point:

- **Membership is derived from the title convention `'Series · Part'`**
  (`seriesOf()`; an explicit `u.series` field overrides). Content shelves
  itself — no re-shipping, no migration. Keep the ` · ` separator in series
  unit titles; a title without it stays a loose card deliberately.
- **All state is derived, nothing stored**: a lesson is *done* when every
  question has ≥1 attempt (`unitDone()` via `qstat` coverage — coverage, not
  score); the ribbon marks the most recently touched shelf with unfinished
  lessons; the 🔖 bookmark inside holds the most recently studied unfinished
  lesson. No new record types, no counters.
- **Nothing is ever gated.** The shelf shows state; every lesson opens with a
  tap regardless of order or completion. Do not add locked-until-done.
- Spines are a **solid colour** — the series' `SUBJECT_PALETTE` deep (`g2`)
  darkened 15% in `spineEl()`, picked by a stable hash of the series name.
  White labels measure ≥5.3:1 across all twelve. Subject texture on spines
  was tried and rejected as visual noise (Chris, 2026-08) — don't reapply
  `paint()` to them.
- `SCREENS.shelf` is the book's table of contents: one row per lesson, the
  bookmarked (or tapped) lesson expanded as the full `unitCard()`. Rows show
  coverage ("7/15 seen"), never accuracy.

**Badge fills are opaque on purpose.** A badge lands on plain cards, accent-washed
cards and review rows; a translucent tint dropped the 10px label under 4.5:1 on
the lighter ones. Measured across all accents in both themes: worst case 4.54:1.

### Photo capture

`shotPicker()` gives two inputs: one with `capture="environment"` (straight to
the camera) and one without (the gallery). `readShot()` downscales to
**1400px on the long edge at JPEG q0.82** on the device before anything is sent —
a phone photo is otherwise mostly wasted tokens, and text stays legible well
below that. Up to `MAX_SHOTS` (6) per unit.

Photos go to Claude as `image` content blocks ahead of the text block, and are
**never stored** — `shotTray` is memory-only and cleared on success or on leaving
the screen. Only the unit they produce is saved, so nothing photographed ever
reaches the Gist.

Because adding a photo re-renders the screen, the form lives in `genForm`
(subject + notes) outside the render. Do not move it back inline.

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

**`--faint`, `--good`, `--warm` are read, not decoration.** They carry hints,
explanations, correct answers and warnings at 12–13px, so they are held to the
same 4.5:1 bar as body text against **both** the card (`#fff` in light) and the
page (`--ink`). The light values were deepened on 2026-08-02 for exactly this
reason — `--faint` was at 2.66:1. If you lighten any of them for aesthetics,
re-measure both surfaces first.

One trap when measuring: Chrome reports accent-tinted backgrounds as
`color(srgb … / 0.08)`, which naive contrast probes parse as opaque and report
wildly wrong ratios. Measure against the opaque surface underneath instead.

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

### Sandbox & Fresh start (v23, in BOTH apps)

Two grown-up escape hatches at the bottom of the parent view, added after a
parent's test sessions polluted real stats:

- **Sandbox** — a per-device localStorage flag (`sandbox` — never a record, so it
  never syncs). While on, `saveLocal()` is a no-op and `Sync.save`/`Sync.load`/
  `syncSoon` are blocked, so every write lives in memory only. Turning it off
  (or reloading) reloads clean data from localStorage and discards everything
  done in it. A dashed `--warm` banner rides on every screen while it is on, and
  Push / Pull / Back up / Restore refuse with a toast rather than act on
  discardable in-memory data.
- **Fresh start** — tombstones every record whose type is in `PROGRESS_TYPES`
  (`log, focus, miss, cleared, qstat, mood, ask, badge, affirm`) and pushes, so
  the wipe reaches every synced device and cannot be resurrected by a stale one.
  Units, assessments, prefs and roster are deliberately untouched.

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
