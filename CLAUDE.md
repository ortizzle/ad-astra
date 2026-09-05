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
- **Standalone from its SIBLINGS too, which is the half that got missed.**
  `pickRound()` serves 5 questions from the unit and shuffles them, so the
  question next door is usually absent. A stem may not open "The same student…",
  "For that same data…", "Using the same fit…", and an OPTION may not name a
  thing only a neighbouring question introduced. This shipped for real on
  2026-08-16: Science Quiz 1 asked about "the same student" as question 4 of 5,
  with one option mentioning a sidewalk that lived in a question the round never
  served. Everything a question needs is its own stem, its own `passage`, its own
  `graph`, and the unit title in the eyebrow — that is the entire context she
  gets. `check_content.py` now errors on a back-referencing stem and on "the
  graph shown" with no graph attached; it cannot catch a stem that leans on a
  scenario more loosely, so read new questions as if each were the only one.
- **A question may never contain its own answer.** In a vocabulary question
  this is the commonest way to ship an item that tests nothing: glossing the
  word in the stem — "Which word means the OPPOSITE of accustom (to get used
  to something)?" — hands over the very fact being tested, and asking for a
  SYNONYM while glossing is worse still, because the gloss usually *is* the
  answer ("concept (a general idea)" → `idea`). Chris caught this on
  2026-09-01. The rule generalises past vocabulary: a stem states the
  situation, never the knowledge. Where a word has two senses, disambiguate
  with a part-of-speech tag ("As an ADJECTIVE…") or a usage sentence
  ("Grandma retired at nine and slept soundly") — **context, never a
  definition.** Definitions belong on the card, in `steps`, and in `ex.main`,
  all of which she meets only after answering.
- **Distractors are the other half of the same bug.** Stripping the gloss
  achieves nothing if the wrong options are unrelated filler drawn at random
  from the word list — she still answers by eliminating on part of speech.
  Every option should be the same part of speech as the answer, and each
  should hold a *different* real relationship to the stem word. The strongest
  distractor in a synonym/antonym item is the word's own opposite number: put
  a synonym in an antonym question and she has to actually read which was
  asked. Check each one does not accidentally also work.
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

### Quiz variety (v64 / Wayfinder v52, both apps)

Two changes to how a round is chosen and shown, both from watching a real
session (Chris, 2026-08): a question she had already missed — and which was
therefore already sitting in the Growth Zone — came back around in an ordinary
quiz a few rounds later.

**Growth-Zone questions sort last in `pickRound()`.** A missed question is
already ON the review ladder, which has scheduled when it returns. Letting it
also compete for an ordinary quiz slot asks it twice and crowds out questions
she has never seen. It sorts behind everything else (`x.g-y.g` before the
attempts comparison) rather than being excluded, because a short unit — or one
where she has missed everything — still needs questions to serve. Measured: a
laddered question went from ~10/40 rounds to 0/40 while due, and back to 16/40
once the ladder cleared it.

**Multiple-choice options are shuffled per question.** They used to render in
fixed order with a fixed `ans` index, so the answer could be learned by
position, which is not knowing the answer. The permutation lives on
`quizState.optArr`, keyed by `optFor` = question id, so revealing a hint
(which re-renders) does not reshuffle the options underneath her mid-question.
`answer()` still receives the **original** index, so `q.ans`, the miss record
and every explanation downstream are untouched.

> ⚠️ **Content must never refer to an option by position.** No "the first two
> options", no "all of the above". Two existing questions did and were
> rewritten. `kind:'order'` and `kind:'spell'` are unaffected — order already
> shuffles its own display, and spell has one option.

The underlying cycle is unchanged and is working as designed: with 20 questions
and rounds of 5, rounds 1–4 cover the unit with no repeats and round 5 wraps.
Repetition after a full pass is correct; repeating a laddered question was not.

### Analogy questions (v73 / Wayfinder v58, both apps)

`kind:'analogy'` renders a standardized-test analogy — the stem on its own
plate (`analogyStem()`, `.analogy`), reading `WORD : WORD :: ? : ?`, above
ordinary multiple choice. Built at Chris's request for Wordly Wise, whose own
exercises use the format; the engine travels to both apps.

- **`q` holds ONLY the stem pair**, uppercase, exactly two words around one
  colon and nothing else. Options are lowercase `word : word` pairs.
  `analogyStem()` falls back to plain text if the stem does not parse, so a
  malformed stem degrades rather than rendering something misleading.
- **Underneath it is plain MC**, so option shuffling, the miss ladder,
  qstats and "see it again tomorrow" all work untouched. Nothing new is
  stored.
- **The relationship is the content, not the answer.** Every `ex.main` NAMES
  it — degree, antonym, synonym, type-to-category, person-to-action, or
  "lacks" — because naming it is the transferable skill. Wrong options must
  each hold a DIFFERENT nameable relationship, never a near-miss of the
  right one.
- **Every analogy must have one cleanly correct answer.** An item where the
  best option is merely the closest structural match is a weak item — one
  shipped in Book 9 Lesson 5 (VENERATE : RESPECT) and was replaced rather
  than excused. Chris writes these rather than lifting the book's, so the
  bar is higher than the book's, not equal to it.
- **Four per vocabulary lesson, four different relationships**, with wrong
  options drawn from relationships already named elsewhere in that lesson —
  so eliminating requires naming rather than feel.
- In `UNIT_SCHEMA` and the generation prompt, so generated vocab units can
  use it too — drafts still gate everything.

### The Algebra topic shelf (v85)

**A topic is the book, and everything belonging to that topic is a part of
it** — not just the homework lessons. Chris's call, 2026-08: Topic 1's four
lessons are homework-derived, but the Test 1 Study Guide is Topic 1 material
too and belongs on the same shelf, not on a shelf of its own.

The convention, and it applies to every topic from here on:

| Part | Title | `order` |
|---|---|---|
| Lesson | `Topic N · N-L Title` | *(none)* |
| Class study guide | `Topic N · Test N Study Guide` | 1 |
| Rescue Round (fresh variants on what she missed) | `Topic N · Test N Rescue Round` | 2 |
| Topic Review | `Topic N · Topic Review` | 3 |

- `unit-sgt1` was **retitled onto the Topic 1 shelf keeping its id**, so the
  progress and Growth Zone misses already attached to it stayed attached.
  Retitle, never re-mint, when moving a unit into a series — the same rule
  Wayfinder's `unit-m11` established.
- Editing a shipped content file means bumping its `updatedAt`, which
  re-drafts the unit on synced devices, so the grown-up re-approves once. It
  is tagged `wasApproved` and the queue labels it as an update, not new
  content.
- River's math shelves (Wayfinder) already follow the same shape and carry no
  `order` — their Topic Reviews sort last on title alone. Leave them; adding
  `order` would re-draft them for no visible gain.

### Topic 2 — Quadratic Functions and Equations (v132)

All 7 lessons (`aga_24_a2_0201..0207_se.pdf` in her Drive folder, uploaded
2026-08-25) shipped as `alg-topic2-01.json` … `-07.json`: vertex form,
standard form, factored form, complex numbers, completing the square, the
Quadratic Formula, linear-quadratic systems. 9–15 cards and 20 questions
each, shelving onto `Topic 2` the same way Topic 1 does — no `order` set, so
they sort 2-1 through 2-7 on title alone.

- **Every numeric answer was independently computed with `sympy` before
  being written into a question** — vertex/intercept arithmetic, factoring,
  the discriminant, complex-number operations, linear-quadratic
  intersections — never worked by hand and never copied from the textbook's
  own numbers. This caught one real error before it shipped: a completing-
  the-square rounding question (2-5 · q19) was first drafted with `x ≈ 0.37`
  from mental estimation; the actual root is `0.3753`, which rounds to
  `0.38`. Every fresh scenario in these 7 lessons uses numbers not printed in
  the source PDF, per the standalone-questions rule — the textbook's own
  worked examples and "Try It!" numbers were used only to calibrate style
  and difficulty, never copied into a question.
- **Graphs render liberally**, per the math/physics rule — vertex-form
  parabolas on the concept cards, with the vertex point labeled, using the
  same `renderGraph` `parabola` series type Topic 1 and the physics units
  already use.
- `tools/test_alg_topic2.js` walks all 7 flashcard decks and a full quiz
  round end to end, and structurally re-validates every question (4 unique
  options, `ans` in range) against the live schema, not just at authoring
  time.

> ⚠️ **`ExamView - Alg 2 Study Guide Test 2.pdf`, in the same Drive folder,
> is NOT Topic 2 material.** Its actual content is piecewise-defined
> functions and arithmetic sequences/series — Topic 1 Lessons 1-3 and 1-4,
> already shipped as `alg-topic1-03.json` / `-04.json`. It was not built
> into a "Topic 2 Test 2 Study Guide" unit; building it under that title
> would have shipped a study guide that quizzes the wrong material right
> before a real test. Flagged to Chris rather than guessed at — find out
> what Test 2 actually covers before shipping a study guide for it.

### Topic 1 · Test 2 Study Guide (v133)

Chris confirmed it: the ExamView PDF really is titled "Test 2" for her
class, and its content — piecewise-defined functions and arithmetic
sequences/series — is genuinely Topic 1 material (Lessons 1-3 and 1-4), not
Topic 2. `unit-sgt2` ships **built exactly like `unit-sgt1`**, per Chris's
own instruction: same `guide:true` paper-study-guide pattern, shelved onto
**Topic 1** (`order:1`, right alongside the four Topic 1 lessons and the
Test 1 Study Guide) because the shelf sorts by content, not by the label on
the paper the school handed out — the Topic-1-vs-Topic-2 folder mismatch
that shipped Topic 2's seven lessons does not repeat here.

- **The PDF was read directly, not through Drive's native extraction.**
  The first pass (`search_files`/`read_file_content`) came back with
  multi-column OCR reflow errors — one question's stem had merged with the
  next question's answer options. Downloading the file via
  `download_file_content`, decoding it locally, and reading the actual PDF
  gave a clean, page-by-page extraction (including the two questions built
  from a graph). Trust the rendered PDF over Drive's OCR snippet on any
  multi-column source.
- **All 30 answers were independently re-derived and matched the printed
  key with zero discrepancies** — a change from Test 1's guide, which
  caught two real misprints in the book's own key. Verified with the same
  discipline regardless: nothing here was assumed correct because the guide
  before it needed correcting.
- **Five questions were adapted from a graph or free-response original into
  an equivalent, independently verified multiple-choice question** (Q1
  evaluate-from-a-piecewise-graph, Q2 boundary inclusion, Q4 domain/range/
  min/max from a table, Q16 a sit-ups sequence term, Q22 a beads-in-a-
  necklace series total) — same "(adapted — …)" convention Test 1's guide
  established, so the entry grid still works with a single letter tap even
  where the paper wanted a graph or written response.
- Every one of the 30 questions carries a hand-authored, independently
  verified `variant` for the Rescue Round, same as Test 1's guide.
  `tools/test_sg2.js` exercises the whole loop end to end: paper entry with
  a realistic mixed pass, `gradeGuide()`'s tally/misses/qstats, the
  walkthrough, the rescue round drawing only from what was missed, and the
  shelf carrying all six Topic 1 parts (four lessons, two study guides).

### Growth Zone cleanup — a grown-up-only correction tool (v134, THIS APP ONLY)

Chris asked for a way to remove a question from the Growth Zone. Misses
landing there is automatic and stays automatic — this is the other
direction, for when the QUESTION was the problem: a misprint since fixed in
a content edit, a duplicate, or one that no longer applies. It is not a
shortcut for her. `SCREENS.growthedit`, reached from a "Manage the Growth
Zone" card in the parent view (only rendered when at least one `miss`
exists), lists every miss grouped by subject — same box bar, same "due
now"/"back in N days" line as her own screen — with a "Remove from the
Growth Zone" button on each.

- **Deliberately unreachable from her side.** Her own `SCREENS.growth` gains
  no button and no new code path. The Growth Zone's founding rule —
  "information, not a verdict" — depends on it not being a list she can
  quietly edit down herself; a self-serve delete button would turn a review
  ladder into a mechanic for avoiding review.
- **`softDelete(m.id)`, not a hard delete.** The miss record tombstones like
  every other delete in the app, so it can never resurrect from a stale
  device's sync, and Sync.merge handles it exactly like discarding any other
  record. Nothing else is touched — not the unit, not her `qstat` tally, not
  her XP. If she goes on to miss the live question again later, it lands
  back on the ladder as a brand new miss, same as always.
- **No confirmation modal.** One question, one tap, immediately reversible
  in effect (missing it again just re-adds it) — the same weight as
  dismissing a suggested assessment, which already ships with a bare ✕ and
  no modal. A bulk "clear everything" action would need one; a single row
  does not.
- `tools/test_growthedit.js` covers the whole loop: the entry card only
  appears in the parent view, every miss renders with a working Remove
  button, removing one drops the count by exactly one and re-renders in
  place, the record is a tombstone rather than erased, and — the rule that
  matters most — her own Growth Zone screen never shows the control.

### Grades, tabulated by subject (v135 / Wayfinder v113, both apps)

Chris asked whether grade data could be "calculated and tabulated based on
subject" as it's entered, with subjects that have nothing recorded still
visible rather than dropped. `gradesBySubject(date)` does exactly that:
derived at render time from `assess` records, same discipline as XP/level/
streak elsewhere — nothing new is stored, so there is no per-subject average
field that could drift out of sync with the underlying grades. A new "By
subject" card sits at the top of the parent view's Tests & quizzes section,
above the existing flat list (which stays, unchanged, for adding/editing
individual entries).

- **Scoped to the current quarter.** `currentQuarter(date)` already exists
  for the header's own "Quarter N" line; grades don't carry a `quarter`
  field of their own, so scoping filters by `a.date` against the quarter's
  `start`/`end`. A dragged-along average from a finished quarter would
  misrepresent how the current one is going, and "nothing recorded" needs a
  time window to mean anything actionable.
- **Every `STUDY_CLASSES` subject renders, even at zero — this is the
  point.** The existing activity "By subject" card (further down the same
  screen) deliberately SKIPS a subject with no sessions and no goal; this
  card does the opposite on purpose. A subject with nothing entered this
  quarter shows "No grades entered yet" rather than disappearing, because a
  silent gap is exactly what a parent scanning this can't act on.
- **Graded vs. pending are counted separately.** An assessment can exist
  with `score:null` (added, not marked yet) — `gradesBySubject` reports
  `graded`/`pending` as distinct counts, so "1 grade · 1 not marked yet"
  reads as two different facts, not one blurred number.
- **The average is a plain mean of each assessment's stored percentage** —
  no weighting by points or kind. The schema already normalizes points/outOf
  down to `score` (v84's grades-as-points work); tabulating averages it the
  same way a report card would, without inventing precision the school
  itself doesn't establish.
- **The value column stays short, on purpose.** `.row .v` is
  `white-space:nowrap` (the same trap `guidewalk`'s steps hit once already —
  see the learning-pass section above); "No grades entered yet" reads as the
  `.k small` subtext under the subject name, never as the `.v` value, which
  only ever holds a percentage or an em dash.
- `tools/test_gradesbysubj.js` seeds a graded subject (verifies the average
  and confirms a grade from a prior quarter is excluded), a pending-only
  subject, and a subject with nothing at all — and checks the card text
  directly, including the quarter label.

### Kinematics 1 · Equations of Motion, the Ramp Lab, and Biology Quiz 1 Review (v136)

Chris uploaded new material into both girls' Drive folders; these three
ship for Sedona.

- **`phys-kinematics-equations.json`** (`unit-phys-eqs`) — from HW05
  ("Kinematic Equations 1 and 2") and HW06 ("Kinematic Equations 3 and 4"),
  combined into one unit since all four SUVAT equations are one coherent
  skill (picking the equation missing exactly the one quantity a problem
  never mentions). 18 questions, every numeric answer independently
  verified with sympy — this caught a real arithmetic slip mid-build (a
  thrown-down-ball velocity written as 43.2 m/s where 3 + 9.8×4 actually
  works out to 42.2). g is taken as 9.8 m/s² throughout, matching how the
  source worksheet's own dynamite-blast problem is set up.
- **`phys-ramp-lab.json`** (`unit-phys-ramp`) — from the Ramp Lab handout.
  The lab itself asks her to collect real data, which doesn't exist yet, so
  this covers the REASONING behind it instead: why a position-time graph
  under acceleration is curved and has to be linearized (plot against t²,
  not t), what a steeper ramp or a push at the start does to the measured
  acceleration, the Moon-gravity scaling, and percent error. The one numeric
  question on the sheet (a multi-leg average-speed word problem) turns out
  to be impossible as printed — the time budget is already spent before the
  last leg starts — so it's echoed with fresh numbers plus a second version
  that lands on a real, if extreme, answer (120 km/h), so she isn't
  blindsided expecting every version to resolve to an ordinary number.
- **`bio-quiz1-review.json`** (`unit-bio-q1`) — the actual returned
  "8th Grade Biology Scientific Method Quiz," shipped `guide:true` exactly
  like the Algebra study guides: paper-entry grid, instant grading, a
  walkthrough of misses, hand-verified variants for the rescue round. Two
  versions of the real quiz exist (V1/V2, same 23 items in a different
  option order — ordinary test security, not different content); V1's order
  is used as the canonical transcription. **Only 18 of the 23 items are
  scored here** — five (a three-part free-response exercise-variable
  question, and two "describe what's wrong with this graph" prompts) were
  never multiple choice on the real paper, so they don't fit an A/B/C/D
  grid without misrepresenting what she actually circled (the same principle
  that keeps guide-unit option order fixed to begin with). Two of those
  ideas (a graph needs a title; a non-zero y-axis exaggerates differences)
  land as recap cards instead, and the y-axis one is already a full lesson
  in `bio-unit-1`. The two graphs behind the scored questions (a three-line
  vegetable-consumption trend, a depth-vs-bubble-rate data table) were read
  from the PDF's actual images via `download_file_content` + a direct
  `Read`, not the OCR text extraction, which cannot see graphs at all.
  Confirmed with Chris before building, since an untitled "Quiz" PDF with
  two versions and no visible answer key could just as easily have been an
  upcoming test — building study content from a live, not-yet-administered
  quiz would be studying the test itself, not the material it covers.
- `tools/test_newcontent.js` walks all three: a full quiz round and
  flashcard deck on each physics unit (including the `kind:'order'`
  ramp-ranking question), and the Biology guide's full paper-entry →
  grading → rescue-round loop.

> ⚠️ **`bio-quiz1-review.json` and, on first draft, `bio-unit-3-enzymes.json`
> both shipped with `classId:'biology'` — the real id is `'bio'`** (matching
> `bio-unit-1.json`/`bio-unit-1b.json`/`bio-unit-2.json`). A unit under a
> classId `CLASS_BY_ID` doesn't recognize is effectively orphaned: it never
> shelves with the rest of Biology, never appears on the subject screen, and
> the mistake produces no error anywhere — nothing crashes, it just silently
> doesn't show up. Caught only because `test_enzymes.js` navigated to the
> real subject screen and checked for the spine; `test_newcontent.js`'s
> guide-flow test for the same unit called `gradeGuide()`/`buildRescueUnit()`
> directly and never touched `CLASS_BY_ID`, so it passed the whole time this
> was broken. `bio-quiz1-review.json` had already shipped with the bad id —
> fixed in place with `libv` bumped (2), the same "immune to the approval
> race" mechanism documented above. **Always verify a new content file's
> `classId` against an existing shipped file for the same subject** before
> trusting it, and prefer a test that actually navigates to the subject
> screen over one that only calls the unit's own functions directly.

### Biology 8 · Unit 3: Enzymes (v137)

Built from four photographed pages of her completed "Enzyme Review" packet
(not from Drive — Chris photographed the physical binder). Covers enzyme
specificity (shape/active-site matching), the substrate-plus-"-ase" naming
pattern, digestive enzymes vs. synthesizing enzymes (DNA polymerase, ATP
synthase), reading a pH-vs-activity or temperature-vs-activity graph, and
what denaturation actually changes at the molecular level. 12 cards, 18
questions, every scenario fresh — none reuse the packet's own molecule-shape
diagrams or pepsin's/trypsin's exact pH values (those appear only inside
explanations, as real-world reference facts, never as the graded question).

- **Two of her own written answers turned out to be worth flagging in
  `parentNote`, independent of the unit itself.** Question 13 asked what two
  internal body conditions could replace "Z" on a generic rise-then-fall
  enzyme-activity graph; she wrote "Substrate" and "active site," but the
  very next question on the same page correctly names the real answer as pH
  and temperature — and a graph shaped like that (up, peak, down) is the
  textbook curve for pH or temperature, not substrate concentration (which
  typically rises then flattens, not falls) or "active site" (a fixed
  structural feature, not a condition that varies). Question 14 asked what
  KIND of organic molecule an enzyme is; she wrote "catalyst," which is the
  right word for what an enzyme DOES, not what it IS (a protein) — the same
  mix-up the unit's own cards (`c1`/`c2`) separate on purpose. Every other
  answer on the packet was correct; this isn't a pattern of struggling, just
  two specific, nameable mix-ups worth a word from Chris.
- **The below-optimum/above-optimum asymmetry gets its own cards and
  questions** (`c7`/`c8`, `q9`/`q10`): below an enzyme's optimal temperature
  it's merely slow and fully reversible; well above it, denaturation is
  permanent. The packet's own questions (21–23) touch this but don't state
  the reversibility distinction outright, so it's called out explicitly
  here — a common exam trap is treating "too cold" and "too hot" as
  symmetric outcomes when they aren't.
- `tools/test_enzymes.js` seeds all four Biology units together, confirms
  the new one shelves correctly under the real "Biology 8" spine (the check
  that caught the classId bug above), and walks a full flashcard deck and
  quiz round.

### Test prep, in gold (v139 / Wayfinder v116, both apps) + Biology Test 1 Study Guide

Chris: test prep has to STAND OUT, "anytime it's test prep." Two pieces:

**The treatment (engine, both apps).** A unit flagged **`prep:true`** — or
any `guide:true` unit, since a paper guide is test prep by definition —
wears an opaque gold "✍️ TEST PREP" band above its title and a 2px gold
card edge (`prepcard`/`prepband`), and its stop on the topic map wears a
gold pip ring (`.stop.prep`). Rules that are the point:

- **`prep:true` is an explicit content flag, never inferred** — same rule as
  `book`/`guide`/`bee`/`capstone`. Deriving it from upcoming `assess`
  records was considered and rejected: a unit would silently gain and lose
  the band as tests came and went, and the runway already owns time-based
  urgency. The flag says what a unit IS, not when it matters.
- **Guides get the treatment for free** (`u.guide || u.prep`), so the three
  shipped guide units (both algebra study guides, the Biology quiz review)
  did not need editing, re-shipping, or re-approval.
- **The gold is the done-pip/crest gold** (#f2ca63 with #2a1c00 ink — the
  already-measured ≈11:1 pair `.pip.done` ships), opaque per the badge
  rule, and identical in both themes on purpose: like the note-from-home
  post-it, it reads as a physical object, not theme chrome. A DONE prep
  stop keeps the full gold done pip — done outranks prep.

**The content (`bio-sg-test1.json`, `unit-bio-sgt1`, THIS APP ONLY).** Built
from the teacher's own "Test 1 (Monday 8/31) Study Guide" PDF — Units 1 and
2 in one test. The real test is FILL-IN-THE-BLANK, so the unit is built
recall-first: 27 cards covering every blank on the guide (the nextUp copy
tells her to say each answer out loud before flipping — production practice,
not recognition), then 24 fresh-scenario questions including a
`kind:'order'` pH ranking and two Chargaff calculations with different
numbers than the guide's own 37%. `prep:true`, `book:true`, `order:1`,
shelving onto Biology 8 beside the Quiz Review.

- **Her own filled-in answer on the guide's FIRST blank is wrong** — she
  wrote "dependent variable" for "a proposed explanation linking what is
  changed to a predicted outcome" (answer: hypothesis). Flagged prominently
  in `parentNote` because she'd otherwise rehearse the error from her own
  paper all weekend; the unit's first card and first question both target
  exactly that distinction. Her other filled blank (quantitative) was right.
- **Two content calls made honestly rather than confidently**: "which
  biomolecules are polar" teaches carbs + nucleic acids (lipids nonpolar,
  proteins mixed/amphipathic) with a note to confirm what her class marked;
  and "breaking bonds ___ energy" teaches the chemically correct direction
  (breaking ABSORBS, forming RELEASES) with a card explaining why the "ATP's
  broken bond releases energy" shorthand is about the whole reaction. Both
  are in `parentNote`.
- `tools/test_biosg1.js` covers the unit end to end plus the treatment:
  both prep stops gold-ringed on the shelf, the band on the opened card, an
  ordinary lesson NOT getting it, and no Beat-the-clock door (`book:true`).

### Tutoring on Today (v140 / Wayfinder v118, both apps)

Chris granted a one-time read of both girls' Google Calendar (2026-08-30) to
check for scheduled tutoring, with the explicit ask that it "show up in the
daily briefing." A new **`TUTORING`** constant (weekday + times, no other
fields) renders a quiet card on Today, the same visual weight as Student
hours but a separate card, because it is a different fact: Student hours are
optional extra time with a teacher; tutoring is a standing appointment.

- **Read once, not synced live.** The app has no Google OAuth and gains none
  here — this is the same boundary the Drive pipeline and the "no write path
  to Drive" rule already draw. Her calendar was read by Claude directly (a
  connector already available in the session, distinct from Drive), and the
  result was hand-transcribed into `TUTORING`, exactly like `STUDENT_HOURS`
  is hand-transcribed from the newsletter. If the schedule changes on the
  calendar, it will not show here until this is refreshed by hand.
- **Times only, same privacy rule as everywhere else in this file.** The
  tutor's name and email are deliberately not in `TUTORING` or anywhere else
  in this public repo.
- **Not gated on a school day.** `STUDENT_HOURS` only makes sense when school
  is in session; tutoring is an outside commitment and keeps running on a
  weekend or a school holiday (Sedona's runs Sundays; a Labor-Day-Monday
  tutoring session for a sibling app's equivalent case is exactly what
  `tools/test_tutoring.js` checks for). It is keyed on the real weekday
  (`wd`, i.e. `AZ.weekday(AZ.today())`), never a shown/future day.
- Sedona's real slots as read from the calendar: **Sundays, 1:00–3:00 pm**
  and **Wednesdays, 3:00–5:30 pm**, weekly, via video call. A one-off Sunday
  session on 8/23 at a different time and a physical address did not fit the
  weekly pattern and was treated as a makeup, not a third recurring slot.
- `tools/test_tutoring.js` checks both weekly slots render with the right
  time, a non-tutoring day renders nothing, and (documented above) that it
  is not accidentally school-day-gated.

### What the completed guide got wrong (v141, THIS APP ONLY)

Chris uploaded Sedona's **completed** Test 1 study guide the day before the
test ("Biology Study Guide - Test 1 - ANSWERS.pdf", Drive, 2026-08-30) and
asked for the material to be reviewed against it. Read the same way the
first pass was — `download_file_content`, decode, render the pages with
`pypdfium2` and read the images — since the answers are handwritten and no
text extraction can see them at all.

**Confirmed with Chris before changing anything: these were her own answers,
not checked against a teacher's key.** That single fact decided every edit
below, and it is the reason to ask rather than infer — had they been the
teacher's, the correct response would have been the opposite in two of the
three cases (match the key, note the real chemistry in the explanation). A
graded question that trains her against what the test marks correct is worse
than no question.

Most of the guide is right — all of Unit 1's vocabulary, the CHON(PS) chart,
all four levels of protein organisation, saturated vs. unsaturated, and the
Chargaff calculation (37% C → 37% G → 13% A, 13% T). **The first blank now
reads "hypothesis", so the v139 flag is resolved** — she fixed it herself.
Three answers were wrong, and all three had already been flagged as open
questions in v139's `parentNote`, so this closes them:

- **"Breaking bonds ___ energy" — she wrote "releases" (and "making bonds
  uses").** It is the reverse, and this is not a convention difference:
  pulling two bonded atoms apart always costs energy. The misconception comes
  straight from the "breaking ATP's phosphate bond releases energy"
  shorthand, which describes the whole reaction — the new bonds formed
  afterwards release more than the break cost. `c26` now leads with the
  magnet analogy and `q23`'s explanation names the ATP shorthand outright.
  **The shipped answer was already correct and did not move.**
- **Bond strength order — she wrote "ionic, covalent, metallic, hydrogen".**
  Genuinely ambiguous between courses: general chemistry ranks ionic first
  (lattice energy), biology ranks covalent first, because the question is
  about bonds inside a watery cell where water pulls ionic bonds apart. This
  is a biology class, so `c9`/`q7` keep covalent-first — but both now NAME
  the other convention rather than treating her answer as simply wrong, and
  note that the blank asks for three types, not the four she listed.
- **"Which biomolecules are polar" — she wrote carbohydrates and proteins.**
  The shipped card was *also* incomplete, in the other direction (it said
  carbohydrates and nucleic acids, calling proteins "the mixed case"). The
  defensible teaching is the odd one out: **lipids are nonpolar; the other
  three all carry polar groups**, nucleic acids most of all with their
  charged phosphate backbone. `c11` rewritten, and a new **`q25`** added —
  the guide has a blank for this and nothing graded covered it. Its four
  options are identical but for the biomolecule name, so the length-bias
  check stays clean.

`parentNote` was rewritten around what is now known rather than what was
open, and adds the one thing the multiple-choice app cannot practise: **the
real test is fill-in-the-blank, and five of her right answers are
misspelled** — experemental, controled, inferance, deoxiribose, matallic.

`libv` bumped to 2 with `updatedAt` stamped in the past, per the
approval-race rule — so the fix lands even though the unit was shipped
before Chris approved it. `tools/test_biosg1.js` gained nine assertions
covering all three corrections by their *teaching*, not merely their
presence.

### The equations on the sheet, and the textbook's definitions (v142)

Chris: the physics teacher shared equations and textbook pages — put the
equations somewhere they pull up during physics, and make study material
from the textbook.

**The equations went into `SHEETS.physics`**, which already existed as the
Unusual Conversion Factors sheet and already renders a button on the subject
screen AND inside every physics quiz. Nothing new was built: the entry gained
sections and was renamed `Formulas & conversions`. It now leads with Table
5–2's four constant-acceleration equations, then the definitions of average
velocity/acceleration, free fall, what each motion graph's slope and area
mean, and a notation row. Conversion factors keep their sections underneath.

- **The four equations are labelled by what they LEAVE OUT** — missing
  position, missing final velocity, missing time, missing acceleration —
  because that is how `phys-kinematics-equations.json` already teaches
  choosing between them. Same names on the sheet and in the unit.
- **A notation row earns its place**: her worksheets write `Δx`, the textbook
  writes `d − d₀`, and they are the same quantity. Both notations reach her,
  so the sheet says so rather than letting her guess.
- `.frow` is `flex-direction:column` and wraps, so long equations are safe
  there — this is NOT the `.row .v` nowrap trap.

> ⚠️ **Superseded by v143 — the teacher's own sheet DOES exist.** v142
> shipped the textbook's Table 5–2 transcription and said in this file that
> no separate handout was in Drive. That was wrong: `Equations.docx` was
> sitting in the Physics 8 folder and my `parentId` search simply didn't
> return it. Chris pointed at it ("I resaved the equation sheet in physics
> folder") and it replaced the transcription. **A search that comes back
> empty is not evidence a file is absent** — say "I didn't find it", not
> "it isn't there", and ask.

**The unit is `phys-ch3-describing-motion.json`** (`unit-phys-ch3`), from
chapter 3, shelving onto the existing `Kinematics 1` spine. It is
deliberately the VOCABULARY chapter — motion diagrams, the particle model,
coordinate systems and origins, position vectors, scalar vs. vector,
displacement, distance, time interval, and the operational definitions of
average velocity, average speed, instantaneous velocity and average
acceleration.

- **Chapter 5 was deliberately NOT built as a unit.** Its graphs are already
  `phys-kinematics-graphs.json` (20 cards, slope/area/best-fit) and its
  equations already `phys-kinematics-equations.json`. A chapter-5 unit would
  have re-asked what she has met. Checked the existing card lists before
  building rather than after.
- The three ideas the unit targets hardest are the ones that actually cost
  marks: distance (scalar) vs. displacement (vector), average speed vs.
  average velocity (a full lap = large speed, zero displacement), and a
  negative acceleration meaning "velocity is shrinking", never "moving
  backwards".
- No graphs, on purpose. Chapter 3 is pre-graph — its visual is the motion
  diagram, a row of dots — and `renderGraph` draws an axed, gridded plot,
  which would misrepresent one. "Graphs where graphs teach" is not "graphs
  everywhere".

**Ad Astra's `tools/builders/unit_common.py` was behind Wayfinder's** and
gained two things from it, both additive and backwards-compatible: a `kind`
parameter on `q()` (default `'mc'`, so every existing builder is unaffected)
and `_balance()`, which rotates correct answers across the four positions.
Ad Astra content had been drifting to `ans:0` for want of it. `build()`'s
option validation is now kind-aware to match.

`tools/test_phys_ch3.js` covers both halves: the sheet opens with all four
equations and still carries its conversion factors, g and the notation note
render, the unit shelves with the other Kinematics 1 parts, the Sheet tool
is reachable from inside a physics quiz, and answers are spread across all
four positions.

### Practice, then the test (v150 / Wayfinder v131, both apps)

Chris reviewed both apps with Kat and sent nine notes, to be read "as a UX
and UI expert who builds kid learning apps". All nine shipped together,
engine, identical in both apps; every one is a rule, not a preference.

**Status on the doors.** A door says where she is with it, or it is just a
picture. `cardsProgress(u)` is the best single run through the deck
("4 of 13 seen" → "✓ deck done"); `quizProgress(u)` is the quiz in
ROUNDS, because the round is the unit she experiences — 16 questions in
rounds of 5 is four quizzes, and the door reads "Quiz · round 2 of 4 · 7 of
16 questions met · 3 rounds to go" with a bar. Rounds done is floored from
questions met; `pickRound` serves least-practised first, so k clean rounds
meet k×size questions and the count is exact until the lesson is done. A
round she leaves early counts its questions, never itself.

- **`seen` and `deck` ride on cards logs from v150.** Earlier logs kept only
  xp (seen×5, capped at 150), so a run under the cap is recovered exactly
  and one at the cap counts as 30 — a floor, never an invention.
- **"Met" means met in the QUIZ.** Kat's rule, and the biggest change:
  Beat the clock is practice, and a question she has only raced no longer
  moves the map, the shelf count, the gilt spine or the crest. `qstat.plain`
  counts untimed sightings (`answer()` adds one when `!quizState.timed`;
  `gradeGuide()` always adds one) and `unitAttempted()` reads it through
  `qstatPlain()`, which treats a tally written before the field existed as
  all-plain — so nothing already finished un-does, and only clock-only
  attempts made from here on stop counting.

**Practice, then the test.** The unit card has two labelled sections
(`.seclab`): **Practice** — Flashcards and Beat the clock as tiles, then
Match, Sort, Star sky, the Bee — and **Test yourself** — the quiz as one wide
door (`quizDoor()`, `.qdoor`, the `.door` layout with the quiz drawing),
last on the card. The order on the card is the order of the work, and the
quiz is deliberately not a third tile: the thing that finishes a lesson
should not look like one more way to practise it. A finished lesson's door
says "finished ✓" and stays open — another round is review, never a lock.

**The details fold behind the title.** Counts, the time estimate and the
source are grown-up facts; they sat between her and the doors on every
card. The title is now a 44px button (`.ttl`, `aria-expanded`) that opens
`.dtl`. **"What this covers" is gone from her side** (Chris: the kids will
not read it); `SCREENS.brief` stays for the review queue.

**The lesson opens under its own stop.** `topicMap()` takes an `openNode`
and appends it directly after the matching `.stop`, so what was tapped and
what opened are never a screen apart — `SCREENS.shelf` builds the card
first and passes it in. `.tmap>.card` is positioned so it paints over the
spine line. `#shelfopen` and the scroll-into-view from v138 are unchanged.

**After a round, back to the lesson.** `lessonHome(unitId, classId)` opens
a book lesson on its shelf with its own stop open, else the subject screen.
`finishQuiz` lands there (the results modal opens over the next round's
door) and `SCREENS.postmood`'s `leave()` returns there while rounds remain
— **even with a miss**. The Growth Zone is the destination only once the
lesson is finished and something was missed; review rounds and the daily
three keep their own `back`. The results say "Round 1 of 3 · 2 more to
finish the lesson" so the next round is named before she leaves.

**A test prompt is a door to the Growth Zone for its subject.**
`goGrowthFor(cid)` sets `gzFilter` to the subject when it has anything on
the ladder (an empty filter would be a chip for nothing) and opens Growth.
Wired on: Coming up test rows (and exam events carrying a `classId`), the
subject screen's upcoming-tests rows, the brief's ledger test rows
(single-test days carry `cid`), and the runway's head (`.rwhead`, a button
around the eyebrow and heading).

**Today, streamlined; the timetable lives on Study.** Chris: "getting
crowded visually and the monochromatic scheme isn't helping… okay to
remove things with little to no value", and "move the schedule line up in
Today to Study — it looks better and does the same thing".

- **The day's line-up IS the subject list.** Study's tile grid is gone;
  `.period.tap` rows in the day's order (each a button to its subject, the
  live one painted with NOW, the old tile's units/accuracy/goal line as
  `.dt`, the start time as `.tm`) replace it. A subject with no period on
  the shown day — a club here, an off-rotation class in Wayfinder — follows
  the line-up with its days (`daysFor`) or "Club" where the time goes, so
  nothing she studies is ever missing. A day off shows the weekday order
  (Wayfinder: the next school day's) with nothing painted. Registered clubs
  went with it. Breaks and bookends are not subjects and stay off.
- **Today keeps what is about today.** The day card wears the live (or
  about-to-start) class's subject hue (`subj-a`, direction A carried to
  the top of the tab); events are pinned directly under it, and an event
  pinned there is dropped from Coming up rather than said twice. **Early
  release moved onto the day card** (`.erline`, warm) because the pick-up
  row that carried it left with the timetable — never the usual time, "not
  published yet" until the school says. Student hours and tutoring share
  one quiet "Extra help today" card (both keyed on the real weekday; hours
  only on a school day). **"On the horizon" is gone**: the next milestone is
  one quiet Coming up row when within three weeks, and the quarter
  countdown row is not printed at all — the header names the quarter, and
  a number that only counts down is scorekeeping.

Measured (`tools/contrast_ux2.js`, accent × theme): section labels 6.44:1
worst, the door's status line 4.83:1, the done tile's status 5.71:1, the
day card's text and early-release line on the subject wash 6.60:1 and
7.55:1. One trap: `.erline` was first written as a bare class and lost to
`.card p` on specificity — it rendered muted, not warm, and only the probe
noticing the two ratios were identical caught it. It is `.card p.erline`.

`tools/test_ux2.js` (same file, both apps) seeds its own three-lesson
series and walks all of it: the card inside the map under its stop, the
section order, the folded details, a full deck run marking the tile done
(and a pre-v150 log read back from xp), a timed round leaving "0 of 12 met",
a legacy qstat still counting, round 1 → "round 2 of 3" on the door and the
stop, the check-in returning to the lesson despite a miss, the finished
lesson going to Growth, and all three test prompts landing on Growth with
the subject filter set. `test_foldtt.js` now tests the Study line-up;
`test_horizon.js` the folded row; `test_tutoring.js`, `test_clubs.js` and
`test_asl.js` were moved to the new surfaces.

> Stale before this work and left alone: `test_guide.js`'s resume check
> (it reads `order[0]` from a round the v117 resume path restores whole)
> and `test_polish.js` (the retired hero). `test_alg_topic2.js` and
> `test_newcontent.js` were failing since v149 on slider questions (one
> option by contract; no `.opt` to tap) and were fixed here.

### The number line (v149 / Wayfinder v130, both apps)

The fourth game, and the first new QUESTION KIND since analogies. `kind:'slider'`
draws a number line and she drags a marker to where the number belongs;
right means within `line.tol` of `line.ans`. Placing numbers on a line is the
best-evidenced activity there is for number sense, and the same widget does
estimation for physics: guess first, then compute.

**The contract mirrors `spell` everywhere else**, which is what made it
cheap: `opts:[<answer as text>]`, `ans:0`, and a `line` object the engine
reads — `{lo, hi, ans, tol, step?, ticks?, labels?, unit?}`. So misses, qstats,
the day view's `items`, the review queue and the Growth Zone all read the
answer as they read any other question, and a missed slider comes back live
(`missAsQuestion` falls through to the unit for anything with fewer than
four options) with its line intact. `-4` is the off-the-mark sentinel; her
value lives on `quizState.sliderVal` so a hint re-render never moves the
marker; **never served in a timed round** (dragging against a countdown
tests dragging) — the same filter as `spell`.

- **The control is a native range input over a hand-drawn track.** Chrome
  moves a 28px thumb's centre from 14px to width−14px, so every tick,
  label and marker is placed with one `calc()` and the thumb sits exactly on
  the value it reads. Touch-friendly, keyboard-accessible, no library.
- **Place it stays disabled until she has moved the marker.** Starting at
  `lo` and allowing an immediate tap would let a wrong answer happen by
  accident.
- **The answered view shows both markers**, hers and the answer, and says
  "You put it at 0.77 · it belongs at 0.65" — the gap is the lesson, so it
  is drawn rather than described.
- **Tolerance is a content decision and the checker polices it**: `0 < tol <
  a quarter of the line`, and `step` never coarser than twice `tol`. River's
  hundredths questions zoom the line (0.3 to 0.4) so a thumb-width on a
  phone is never the difference between right and wrong.
- `check_content.py` validates the line; `unit_common.slider()` authors one
  with opts derived from the line and its step's decimals.

**Content, this app**: four estimation questions on `Kinematics 1 · Equations
of Motion` (fallen distance after 2 s, braking distance from 20 m/s, height
of a 15 m/s throw, a sled's speed after 5 s — every answer computed in the
builder, never typed) and three on `Topic 2 · 2-1 Vertex Form` (where the
vertex sits; the sign of h is the whole trap, and placing −3 instead of 3
is visible on a line in a way a wrong option is not). Both files re-draft
once (`libv` bumped). River's twelve-decimal unit is in wayfinder/CLAUDE.md.

> The physics file's ids ran `q1…q18`, not `q0…`, and the first append
> minted a duplicate `q18` — the checker caught it. New ids are minted from
> `max(existing)+1`, never from `len()`.

`tools/test_numberline.js` (same file, both apps) seeds its own three-slider
unit so it never depends on which app's content carries sliders: the timed
filter, the rendered control's bounds and ticks, dragging enabling Place it,
a re-render keeping the marker, the −4 sentinel with her value in the miss
and the day-view item, a within-tolerance hit writing no miss, and the miss
coming back in the Growth Zone as a slider.

**Spot-the-flaw is the last of the cheap tier.** Content-heavy; still on the list.

### `kind:'dress'` (v148 / Wayfinder v127, engine in both apps)

A day she dresses differently for — Picture Day, a Spirit Week theme — is
an event `kind` of its own: it pins on Today with a `Dress` label, never
quiet, and lists in Coming up. Built for River's Cub Hub (see
wayfinder/CLAUDE.md, same section); this app carries the kind with no
content yet. When the upper-school newsletter lists one, it goes in
`CAL.events` like any other event.

### Swipe sort (v146 / Wayfinder v125, both apps)

The third cheap game, and the first that needed authored content. Two
buckets, one card at a time, swipe left or right (or tap a side). The
material is the category judgement itself — observation or inference,
scalar or vector, changed-on-purpose or measured — which is what the tests
actually ask and what a four-option quiz reaches only sideways.

**Sets ride on the unit**: `u.sorts = [{id, title, a, b, items:[{t, k:'a'|'b',
why}]}]`, left is always `a`. So a set drafts, approves and shelves with its
unit, `unitDelta` treats `sorts` as a meta change (re-approval shows only
the changed sets), and `SCREENS.reviewunit` lists every item with its
bucket — nothing reaches her unread. Adding a set to a shipped file bumps
`libv`, so the five units below re-draft once. Rules that are the point:

- **A wrong swipe is information, not a fault.** The card turns, says which
  bucket it belonged in and why, waits for a tap, and goes to the back of the
  pile — the round ends only when every card is in its place. Nothing
  breaks. No buzz on a miss; the right-answer buzz on a hit.
- **Speed is hers.** An elapsed clock, never a countdown.
- **One log** (`mode:'sort'`) updated in place as cards land, so leaving
  keeps what she earned; `correct` is right-first-time, XP flat per
  first-time-right (`SORT_XP` 3), no speed bonus.
- **Never on the review ladder.** A sort item is not a question record and
  never becomes a miss. The quiz owns the ladder.
- **Date-seeded with `mixHash`**, same pile all day, fresh tomorrow;
  "Again" re-salts.
- **An item may not name its own bucket.** `check_content.py` errors on it
  (first word of either label, five letters or more, inside the item
  text) — the sort-set form of the glossed-stem rule. It also requires 6+
  items, 2+ per bucket, unique text, and a `why` on each.
- Bucket plates use `--text` on the accent wash, the pair the chip fix
  settled on; a hit or miss borrows `--good` / `--bad`.

**The first five sets**, each 10–12 fresh items, none lifted from the
unit's own questions:

| App | Unit | Set |
|---|---|---|
| Wayfinder | Quiz 1: Thinking Like a Scientist | Observation or inference? |
| Wayfinder | Quiz 1 Part 2: Measurement | Quantitative or qualitative? |
| Wayfinder | Quiz 1 Part 3: Variables | Changed on purpose, or measured at the end |
| Ad Astra | Kinematics 1 · Describing Motion | Scalar or vector? |
| Ad Astra | Kinematics 1 · Motion Graphs | Which graph is it true of? (position–time / velocity–time) |

The variables set names the experiment inside every item ("Testing whether
salt changes how fast ice melts: the amount of salt…") because the pile
shuffles and a returned card can arrive far from its partner — the
standalone rule, applied to a game. The scalar/vector set mixes named
quantities (velocity, acceleration) with described ones (“she ended up
3 km east of home”) so it tests the concept, not the glossary.

`tools/test_sort.js` (same file, both apps): the door on the card and on
the shelf, the deal, a right tap counting and logging in place, a wrong
tap's verdict/why/Got-it and the card returning to the back, pointer
swipes (a short drag snaps back, a long one sorts), the finish tally at
(n−1)×3 XP with the returned card named, Again reordering, the review
queue showing the set, and `unitDelta` flagging a sorts change.

**Next**: the number line (`kind:'slider'`) needs engine plus content;
spot-the-flaw is content-heavy. Both are still on the list.

### Match, and the daily three (v145 / Wayfinder v124, both apps)

Chris asked for learning games and picked the low-hanging fruit first. Two
shipped together, both engine, both zero-content: they run on the decks and
questions the girls already have. Swipe sort and the number line come next
and need authored content; spot-the-flaw after that.

**Match** (`SCREENS.match`, `matchCards`, `matchDeal`, `matchLog`): terms
and definitions face down in a 3-across grid, find the pairs. A secondary
button under the three mode tiles on any deck with 4+ matchable cards —
Star sky's door, same weight, never a fourth tile (the row is measured for
three). Rules that are the point:

- **One log, updated in place** (`mode:'match'`, `logId` on `matchState`),
  written on every pair found, so leaving early keeps her minutes and XP.
  Star sky's rule. `flips` rides on the log as a number for the day view,
  never as a verdict on screen.
- **A wrong flip is nothing, and it stays up until her next tap.** The first
  build turned a wrong pair back after 750ms; Chris caught it live — the
  second tile "flips over too fast to read it". A timer cannot know how long
  a definition takes to read, so there is none: the pair stays face-up, the
  header says "tap any tile to carry on", and her next tap turns the pair
  back and (if it landed on a fresh tile) brings that tile up in the same
  tap. No penalty, no count of misses, the right-answer buzz `[12,40,12]` on
  a match and silence on a miss — the phone never scolds.
- **Flat XP per pair** (`MATCH_XP` 4, so 24 for a full six), the order of a
  flashcard run, and no speed bonus: racing a memory game teaches nothing.
- **Date-seeded**: the same six all day, a fresh six tomorrow, nothing
  stored. "Play again" re-salts within the day, and the button says which it
  can do — "a fresh six" on a deck of more than six, "same pairs, new places"
  on a deck of exactly six.
- **Ponder cards and picture-only cards are skipped** (a prompt is not a
  definition; the ASL alphabet cannot be matched to text), and the def tile
  shows the def's `**bold lead**` only — term ↔ meaning, not term ↔ paragraph.

> ⚠️ **Seed with `mixHash` (FNV-1a), never `hashStr`.** `hashStr` is a
> polynomial roll: changing the salt in front of a card id adds the same
> constant to every key, so the relative order never changes. The first
> build dealt the identical six for every salt — consecutive ids, at that —
> and `test_games.js` caught it. `mixHash` xor-multiplies, so the salt
> reaches every later character. The daily three's tie-break uses it too.

**The daily three** (`dailyPicks`, `buildDailyUnit`, `dailyDone`,
`dailySquares`, `dailyShareButton`): one tiny fixed ritual on Today, under
the parked-round door and above everything else, because a habit needs a
door that is always in the same place. Three questions, one per subject
where she has approved units, subjects rotating with the date and the
least-practised question winning inside each. Served as an ordinary round
with the synthetic id `__daily__` — so it skips the check-in like a shuffle
round, misses land in the Growth Zone on their REAL unit, qstats credit the
real unit, `realUnit()` keeps it out of save/resume, and `finishQuiz`'s
existing `_srcUnit` pairing settles any laddered question it re-asks.

- **Done is done.** The door becomes a quiet card — "The daily three ·
  done ✦✦✦" — and stops asking. No streak, nothing gated, never more than
  three. A partial round leaves the door up.
- **The completion bonus scales with its length** (3 of 5 → 30, so 60 XP
  for a clean run). Unscaled, a one-minute ritual paid 80 against a full
  quiz round's 65 at 4 of 5, which would quietly cheapen the quiz. Only
  `__daily__` scales; nothing else moved.
- **The share is one plain line** through the Web Share API (the backup
  already uses it), else the clipboard, else a toast: `✦✦✦ Ad Astra · The
  daily three · Sep 2 · done`. It says done, never a score — what goes to
  the family thread is the ritual, not the marks. The results modal shows
  the three squares and the share button above the companion; the
  constellation above already shows which stars lit.
- The quiz's Back and the results/mood return path go to Today for the
  daily, not to a `__all__` unit screen.

`tools/test_games.js` (same file, both apps): the Match door on a rich deck
and its absence on a thin one, 12 face-down 44px tiles, a wrong pair turning
back with nothing logged, a right pair logging in place, a full game keeping
ONE log at 24 XP, Play again dealing a genuinely different six; then the
daily door, three questions from three subjects identical all day and
different tomorrow, the round skipping the check-in, a deliberate miss
landing on its real unit and subject, 20 XP at 2 of 3, three squares and a
share button in the modal, the done card back on Today, and a share line
with no score in it.

> `tools/test_polish.js` fails two checks in BOTH apps on the state before
> this work ("thread hero present", "check-in starts itself") — the hero it
> looks for was retired in v125 / Wayfinder v108. Stale test, not a
> regression; left for a separate pass.

### The Growth Zone, focused (v144 / Wayfinder v123, both apps)

Chris: the Growth Zone had grown large and unappealing, and in test week
there was no way to pick "just maths, and just the recent material that
will be on the test" — which is the smart use of the time. Three changes
to `SCREENS.growth`, engine, identical in both apps.

**Chips scope the WHOLE ladder, not the due card.** They used to live
inside the due card, appear only when due questions spanned more than one
subject, and cover only what was due. Now a row above the card — an
"Everything · N" reset, then subjects ranked by nearest unscored test —
filters both lists and both review doors. Inside a subject a second row
lists its units, ranked **most recently missed first**, which is the honest
proxy for "the recent material". One subject on the ladder needs no chooser
and is implicitly chosen, so its unit chips still appear. The filter is
session-scoped (`gzFilter`), never stored: she picks Algebra, reviews,
comes back and it is still Algebra.

> ⚠️ **Rank units by `on`, never by `updatedAt`.** `put()` re-stamps
> `updatedAt` on every write, so a review round would bounce a weeks-old
> unit back to the top of "recent". `on` is set when the miss is born and
> survives every reschedule (`answer()` keeps `was.on` on a re-miss). The
> first build used `updatedAt` and the test caught the inversion.

**A second door: "Review all N · ahead of time."** Everything in the
filter, due or not — the test-week door. `buildReviewUnit(opt)` gained
`unitId` and `all`; with `all`, due questions still come first, then lowest
box. No new ladder rule was needed: `finishQuiz` already promotes a laddered
question on ANY correct sighting in an ordinary round and resets it on a
miss, so an early review settles through the same code. Verified: two box-3
misses reviewed six days early both cleared. The door renders as the
primary button only when nothing is due, so the daily habit is never
upstaged. The old "📄 Study guide" chip is gone; a guide unit is just a unit
chip wearing 📄.

**Rows fold.** A row is the question (clamped to two lines) and its ladder
bar; a tap on the head (`.mhead`, 44px, `aria-expanded`) opens the answer,
what she chose, the explanation and any graph. Measured on the seeded
screen: folded is under 70% of the fully open height. Inside one subject
the group header is dropped — it would only repeat the chip. Explanations
now go through `richify()`, so a `**bold**` run renders as bold; the old
screen printed the asterisks.

- **The selected chip's text is `--text`, not `--ac-fg`.** The nav's
  `--ac-fg`-on-`--ac-8` pill is fine on the nav; the same pair over the
  light paper measured **4.41:1** with the aqua accent — the wash trap
  `.felt` hit in v84. Wash + accent border carry the selection.
  `tools/contrast_gzchip.js` sweeps accent × sky × theme for the selected
  and unselected chip: worst **12.4:1** here, 13.4:1 in Wayfinder.
- `tools/test_batch6.js`'s Growth section was rewritten to the new
  contract (a chip filters; the primary button then starts the scoped
  round), and its first-action threshold moved from 320px to 380px: the
  chip row above the card is itself a row of actions.
- `tools/test_gzfilter.js` (same file, both apps): seeds two subjects and
  three units with mixed due dates and first-missed dates, and walks the
  reset chip, subject chip, unit ranking, the ahead-of-time door becoming
  primary when nothing is due, the scoped round, the ladder clearing early
  reviews, the filter surviving navigation, the fold ratio, and 44px on
  every chip and row head.

> A probe I wrote first for the chip reported 15:1 and passed. Chrome had
> returned `color(srgb 0.15 0.41 0.37)` and my regex read the floats as
> 0–255. `tools/README.md` already says this; `contrast_batch6.js` already
> parses it. Reuse the parser, do not write a new one.

### Her teacher's sheet, all of it (v143)

`Equations.docx` — the real handout, found in the Physics 8 Drive folder
after v142 shipped the textbook's version. It replaces that transcription
outright, per the `SHEETS` rule that a sheet is *the teacher's own reference
sheet, transcribed*.

**Getting the equations out took parsing, not extraction.** Drive's
`read_file_content` returned only the eight section headings — General /
Kinematics / Newton's Laws / Work and Energy / Impulse and Momentum / Waves
and Light / Electric Circuits / Physical Constants — and nothing between
them, because every equation is an **OMML** expression (`<m:oMath>`), which
Drive's text extractor drops silently. A `.docx` is a zip: downloading it,
unzipping `word/document.xml` and walking the `m:` namespace recovered all
56 expressions exactly (fractions, sub/superscripts, radicals, the `|b|`
delimiter pair), with zero images to render. **If a Word document comes back
as headings with nothing under them, look for OMML before assuming the file
is empty or scanned.**

- **It is the WHOLE YEAR, not kinematics** — Newton's Laws, energy, momentum,
  waves and optics, circuits, constants. All of it ships now rather than
  being held back until her class reaches each unit: it is a reference sheet,
  she has the paper copy already, and gating it would be the app deciding
  what she is allowed to look up.
- **Her notation, not the book's.** The sheet writes `Δx`, `v_i`, `v_f`; the
  textbook writes `d − d₀`, `v₀`, `v`. The transcription keeps hers, and the
  `Notation` block (ours, kept from v142 and now earning its place three
  times over) says the two are the same quantities.
- **The sign of g genuinely conflicts between her two sources, and the sheet
  says so.** Her teacher's sheet builds the minus in — `g = −9.8 m/s² ≈ −10
  m/s²`; the textbook writes `g = +9.80` and puts the minus in the equation.
  Neither is wrong, and a student who mixes them loses marks quietly, so the
  Notation block names both and tells her to use her class's convention.
- **The missing-quantity labels are ours; every equation is hers.** Her five
  kinematics equations map onto missing Δx / missing a (twice — two forms of
  the same relation) / missing `v_f` / missing t, which is exactly how
  `phys-kinematics-equations.json` already teaches choosing between them.
  Labelling is not editing.
- **Two things on the sheet were transcribed as printed rather than
  "corrected".** `Δp = −Δp` is literally what she has on paper — shorthand
  for one object's momentum change being minus the other's, with the
  subscripted `m₂Δv₂ = −m₁Δv₁` on the next line — so the label carries the
  meaning and the equation stays as issued. And `tan θ` is absent from her
  Physical Constants block; it was not added, because a sheet with extras on
  it is no longer the sheet she is holding.
- **Unicode subscripts where they exist, `_x` where they do not** — the
  convention `algeo`'s `A_B`/`P_B` already set. `F_net`, `v_i`, `d_o` and
  `m₁v₁_i` all read cleanly at 390px; verified nothing overflows (`.frow` is
  `flex-direction:column` and wraps).
- Two blocks kept from v142 sit under the teacher's sections and are
  **labelled as the textbook's** in their own headings, so provenance is
  visible on screen rather than only in this file.

`tools/test_phys_ch3.js` now asserts all eight of her section headings, all
five kinematics equations verbatim, a sample from each later unit, the
negative g (and that the textbook's +9.80 is gone), the notation block naming
the g conflict, and that the textbook blocks say they are the textbook's.

### The lesson you meant (v138 / Wayfinder v115, both apps)

Chris asked for a UX review; its top finding was his own report made
precise: picking a lesson on the topic map could open the WRONG one without
anyone noticing, because three screens in a row hid the lesson's identity.
Tapping a map stop gave nearly no feedback at the tap point (`.stop.here`
was a 4px ring of 8%-alpha accent around the pip); the opened card rendered
below the entire map — off-screen on any topic with 5+ lessons, since
`onPick` re-rendered without scrolling; and the check-in screen never named
the unit, so the last screen before the round said nothing about which
lesson was about to be quizzed. Three fixes, all engine, shipped to both
apps together:

- **The opened card scrolls into view on pick.** The card carries
  `id:'shelfopen'`; `onPick` scrolls it into view after the re-render,
  `behavior:'smooth'` gated on `prefers-reduced-motion` like every other
  motion in the app, with a small `scrollMarginTop` so it doesn't kiss the
  viewport edge.
- **The selected map row is unmistakable**: full-row `--ac-8` wash, title in
  `--ac-fg`, and the sub-label steps up from `--faint` to `--muted` — the
  same tint trap `.felt` documented in v84 (`--faint` over `--ac-8` fails
  4.5:1). Measured across all 12 subject palettes × both themes in both
  apps: worst `.t` 6.63:1, worst `.s` 4.95:1 — and the `--muted` step-up was
  load-bearing, not precautionary.
- **The check-in names the unit** — an eyebrow above "Before you start"
  reading `📖 <unit title>`, plus ` · Beat the clock` when timed. The
  screen already carries the subject accent, so it colours itself. Review
  and shuffle rounds still skip the check-in entirely, so this adds no
  friction to the daily habit loop.

`tools/test_shelfpick.js` (same file, both apps) covers all three: a
7-lesson shelf, tapping lesson 5, asserting the row visibly selects (real
computed background, not a pip ring), the page actually scrolled, the opened
card is the tapped lesson's, and the check-in names the unit — with Beat the
clock named only in timed mode.

### Flag this question (v136 / Wayfinder v112, both apps)

Chris asked for a way for the girls to flag a question they think might be
wrong, so he can remove it from the material or explain it to them. Every
answered question (right or wrong, in an ordinary round, a Growth Zone
review, or a shuffle round) gets a quiet "🚩 Something wrong with this
question?" ghost button under its explanation. Tapping it opens a modal with
an optional textarea — say what seems off, or just flag it — and writes one
`flag` record (`{unitId, classId, qid, q, note, date}`). The button then
relabels itself "🚩 Flagged for a grown-up" and disables, so she can't
double-flag the same question, and gets no other feedback: no XP, no
Growth Zone entry, nothing gamified.

- **This is not the Growth Zone.** The Growth Zone is about what SHE knows;
  a flag is about whether the QUESTION ITSELF is right — a typo'd answer key,
  a confusing scenario, a graph that doesn't match its own text. The two
  systems don't touch: flagging changes nothing about her tally, her ladder,
  or her XP.
- **Nothing happens automatically.** A flag only ever surfaces to a
  grown-up; it never edits, hides, or skips the question by itself. The
  parent view gets an accent card ("N questions were flagged") above the
  wellbeing section, leading to `SCREENS.flagged` — same subject-grouped
  layout as the Growth Zone cleanup tool, with the question, her optional
  note in quotes, and two actions: **Remove the question** (filters it out
  of the live unit's `questions[]` for good, and — the one bit of cleanup
  this needs that Growth Zone cleanup didn't — tombstones any existing
  `miss` record for that unit/qid too, so a question pulled for being wrong
  can't keep resurfacing in the Growth Zone from an old snapshotted miss)
  or **Dismiss — it checked out** (just softDeletes the flag, question
  untouched, for when Chris looks and it's actually fine).
- **`_srcUnit`/`_srcClass`/`_srcQid` are used exactly like the "see it again
  tomorrow" 🌱 button already does**, so a flag raised mid-review-round or
  mid-shuffle-round correctly attributes to the real unit and question, not
  a synthetic round id.
- **Excluded on a rescue-round variant** (`q._rescue`) — a variant is a
  sub-field of another question (`q.variant`), not a top-level array entry,
  so there's no clean "remove this" target. If a variant itself is wrong,
  flagging the original question it came from is the door.
- **Not in `PROGRESS_TYPES`.** A flag is a content-correctness signal, not
  her activity — Fresh start leaves it alone, same as units, assessments,
  prefs and roster.
- `tools/test_flag.js` covers the whole loop both ways: flagging a right
  answer and a wrong one, the note saving, the no-double-flag guard, the
  parent card appearing, removing (unit shrinks by exactly one question, the
  matching miss is tombstoned, the flag clears) and dismissing (flag clears,
  question and unit untouched).

### The round, drawn (v89 / Wayfinder v71, both apps)

River asked for something game-like in the quizzes; Chris wanted nothing too
gamey. Two additions came out of a prototype she played first
(`wayfinder/prototype.html`), and both sit on the intrinsic side of the line:
they make effort legible, they never price it.

**The round bar is a constellation.** `roundBand()` replaces the row of `✦`
glyphs with an SVG band: every question is a star, answering lights it and
draws the line to the one before, so a finished round is a shape. Positions
come from `roundPoints()`, seeded by a stable hash of the unit id — a unit
always draws the same shape and different units differ, but nothing is stored
and nothing is collected.

- **A missed question still lights its star**, just dimmer, and its segment
  still draws. Nothing breaks and nothing is taken away — the Sky Map rule.
- **Deliberately UNNAMED.** The Sky Map names constellations and one there
  means a week she showed up five days of seven. A round happens several times
  a day; naming those too would spend the Sky Map's currency.

**The topic map** replaces the shelf's contents list — `topicMap()`, one stop
per part on a left rail, coverage on each, the tapped lesson opening as a full
`unitCard()` **below** the map so the path stays whole while she reads. One
spine, not a path above a duplicate list.

**The crest** (`crestEl()`, `.tcrest`) marks a topic that is genuinely over.

- **`capstone:true` is a content flag, never inferred.** A series with a
  capstone has a defined end — River's maths topics finish on a Topic Review.
  A vocabulary book that gains a lesson a week has no honest "finished", so it
  gets no crest rather than one that could later un-earn itself.
- **Earned by finishing the capstone itself**, so a lesson shipped afterwards
  can never take it back. Verified.
- Not currency: it cannot be spent, traded or bought, and nothing is gated.

**The round, redrawn (v91 / Wayfinder v73, both apps).** Two changes to the
screen she uses most, prototyped in `wayfinder/prototype2.html` before either
was built.

- **One slim tool row, not four stacked buttons.** Hint, Calculator, Sheet and
  Leave were four full-width `.btn-ghost`s under every question — measured at
  ~250px of furniture between her and the next question, now **72px**
  (`.tools`/`.tool`). They share the WIDTH, not the height: every tool still
  renders at 48px, four of them at 83px wide on a 390px screen, nothing
  clipped. The answers are now the only big targets on the screen.
  - **The hint keeps its price on the button** — "Hint −5". She must never buy
    one without being told what it costs.
  - **The sheet reads just "Sheet"** in the row; "DBQ essay rubric" does not
    fit a quarter of the width, and the subject screen still names it in full.
- **The round ends on the shape it drew.** The results modal opened on
  `${pct}%` in 28px Fraunces; it now opens on the finished constellation
  (`roundBand(u,{state,tall:true})`, 104px) with the score as one quiet
  `.tally` line — `4 of 5 · +65 XP · 2 sec`. **The fraction is said once**,
  not in a headline and a message and a box; the percentage is not printed at
  all (the parent view keeps it). The headline names COMPLETION, not the
  score, so it reads the same at 40% as at 100% — Sky Map rules.
  - `roundBand` gained an `opt.state`, so the band can be drawn from a state
    array after `quizState` is gone; `roundState(u)` is the live read. Same
    seed, so it is the shape she watched being drawn.
  - **A missed question still lights its star**, dim, and its segment still
    draws.

Measured across accent × sky × theme after the change: worst `.tool` label
**4.54:1** (Ad Astra) / 5.75:1 (Wayfinder), worst `.tally` 4.94 / 6.19 — all
clear. One trap on the way: `.tool` transitions its `color`, so a probe reading
`getComputedStyle` immediately after flipping the theme gets the INTERPOLATED
value and reports a failure the app does not have (it claimed 3.11:1).
`contrast_tools.js` now disables transitions first and asserts `--muted`
actually tracked the theme.

Three bugs the screenshots caught, all mine: the map's alternating zigzag left
~165px a side at 390px and River's lesson titles wrapped to four lines into the
spine (now a left rail); `.t`/`.s` were spans and ran together on one line
(now `display:block`); and **`.crest` was already the subject-header crest
ring** defined later in the sheet, which forced the block to 52×52 — renamed to
`.tcrest` rather than fought.

### The batch of six (v92 / Wayfinder v74)

Six improvements shipped together; all engine except where marked.

**Growth re-quiz + prioritization.** `buildReviewUnit(opt)` takes an optional
filter — `{classId}` for one subject, `{guide:true}` for questions that came
off a paper study guide. The Growth due card grows chips for both, but only
when the due list spans more than one subject (a one-subject list needs no
chooser), and the guide chip only when guide misses are a strict subset.
Subjects are ranked by **days to the nearest unscored test** (then count);
the same ranking orders the Due/Settling groups, whose headers say "· test in
N days" inside 14. The id stays `__review__` whichever door she uses, so the
ladder settles identically. "Learned for good" moved below the lists — state,
not action. The start button sits directly under the count now (the audit
measured 397px of preamble before the first action).

**Re-approvals show only the difference.** `unitDelta(old, new)` runs inside
`fetchLibrary()` — the ONE moment both copies exist — and its result rides the
re-drafted record as `chg` (ids for kept items, display text for removed ones,
since a removed item has no record left to read). `SCREENS.reviewunit` in chg
mode renders just the changed/new items (expanded), a summary sentence, the
removed list, and a "Show the whole unit" escape; the unit-level blocks
(parent note, summary, objectives) are hidden because they are exactly what
was already read. Approving deletes `chg` with `wasApproved`. In the ordinary
full view, **question rows now collapse to question + correct answer** — the
two things a read-through actually verifies — with options/explanation/
provenance one tap away per item. Cards stay full; they are the substance.

**The update bar.** The service workers **no longer `skipWaiting()` at
install** — a new worker used to take over mid-session the moment it
installed. It now waits; the page shows a dismissible "A new version is
ready" bar (`.swbar`, `offerUpdate()`), and the takeover happens when she
taps Refresh (a `'skip'` message → `skipWaiting()`) or on the next cold
start. The `controllerchange` reload is guarded by `swAccepted`, so nothing
ever yanks a mid-round quiz. Found while testing the swap: **a hung CDN fetch
(fonts) blocks every `<script>` after the stylesheet — the app simply never
finishes loading** on a captive-portal-style connection. The SW's CDN branch
is now bounded: cache, else network for 4s, else `Response.error()` and the
system font stack carries on. `tools/test_swflow.js` runs the whole flow for
real, bumping sw.js on disk and restoring it.

**The exam ramp.** A plan entry gains `ramp` when its subject has an unscored
assessment within 7 days AND 2+ units — inside test week the right work
changes *shape* (interleaved practice across all units; deciding which skill
a question wants is itself the tested skill), not just minutes. Study renders
a "Mixed round — all <subject> units" button under that plan card, and
`threadTarget()` hands the thread to the mixed round inside 3 days — **but
due reviews still outrank it**, always.

**How well you call it (THIS APP ONLY, deliberately).** A Stars card built
from `calibrationPairs()`: her last 10 readiness-vs-score pairs drawn as
hollow (felt) and filled (went) dots, one sentence naming the average gap's
direction. Rules that are the point: needs 4+ pairs so one odd day cannot
masquerade as a pattern; the direction is information about her gut, never a
verdict; second person throughout. Wayfinder keeps calibration parent-side —
9 is young to be handed a self-model chart; revisit if she asks.

**Audit fixes.** Clubs rows stop repeating the standard after-school time
(the audit counted "3:45" printed 25 times) — rows keep what DIFFERS, morning
clubs say so, the detail modal keeps everything. The Settings picker grids
(avatar / companion / celebration) collapse to `.pickrow` rows showing the
current choice — the screen rendered 52 buttons at once; nothing was removed,
only deferred behind one tap.

**tools/ is the pipeline's home now.** The Playwright harness (sweeps,
feature tests, contrast probes, the SW flow test, `serve.js`) and the content
builders + `check_content.py` live in each repo's `tools/`, not in session
scratch space that dies with the container. Never cached — the SW shell is a
fixed list. `tools/README.md` carries the hard-won probe rules (opaque-surface
compositing, transitions-off before reading colours, assert-the-knob-turned,
never wait on `load` across a SW swap).

Two Wayfinder parity gaps found and fixed on the way: its Growth list and its
review queue never rendered a miss's/question's `graph` (Ad Astra's did), and
its review queue didn't `richify()` explanations.

### The polish pass (v93 / Wayfinder v75, both apps)

Friction and look-and-feel, shipped together after the batch of six.

**The fonts live in the repo now** (`fonts/`, three woff2 latin subsets,
~176KB). They register under the SAME family names as before, so no other
CSS changed; they are in the SW SHELL and preloaded. The reason is not
aesthetics: the whole typographic identity used to arrive from Google's CDN
on every cold start, and on a captive-portal-style connection that meant
system fonts (or, before the v92 timeout, an app that never finished
loading). `tools/test_fonts.js` loads the app with EVERY non-localhost
request aborted and asserts all three faces render.

**Friction cuts, all measured behaviors (`tools/test_polish.js`):**
- *Pick up the thread* renders on Today as well as Study — the commonest
  intent of any open no longer costs a tab switch. Same `threadTarget()`,
  strip rules (a door, not a scoreboard).
- **A right answer's feedback card advances the round** (`.explain.go-on`
  clicks the Next button). Wrong answers deliberately do NOT — the
  explanation and walkthrough journey stays.
- **The check-in starts itself** once both taps land — after a 700ms beat
  (room to re-tap a mis-hit; readiness feeds calibration, so a polluted pair
  matters), armed once per visit, and **never on a low mood** — the care
  note and the real option to stop must get their moment. The button stays.
- The parent view says when it last synced — sync failures are swallowed by
  design (offline-first), which is right for her and wrong for a parent
  whose token died quietly.
- The live period row carries a progress line (`.pleft`) — how far through
  the period, white on the painted fill.
- The trusted-device gate skip already existed (a checkbox in the passcode
  modal) — checked before building it twice.

**Look and feel:**
- **The nav's active tab wears a tinted pill**, not just a colour —
  `.nav-btn.on` was the last place colour was the sole signal.
- **Light mode carries the identity now.** The washes were always
  accent-keyed; they sat on near-white paper. The paper itself is tinted per
  app (sea-glass here, blossom-warmed in Wayfinder), raised/line tokens
  follow, wash alphas up. Deeper paper needs deeper ink: `--muted`,
  `--faint`, `--ac-fg` (mix 40%→32%), `--warm`, `--good` were all deepened,
  and `tools/contrast_light.js` measures every reading token against the
  page, the card, the raised surface AND the wash-tinted worst case, per
  accent per sky — worst case after tuning 5.33:1 (here) / 5.49:1
  (Wayfinder). The first cut measured 4.07 and was rejected by the probe.
- **The type scale lost its half-point one-offs**: 9→9.5, 11→11.5, 12→12.5,
  13.5→13, 14.5→14 (31 declarations per app). Micro sizes only round UP;
  nothing a reader relies on shrank more than half a point. Overflow and
  tool-clipping tests re-run after.

**`wayfinder/prototype3.html` — borders → tonal hierarchy — is a PROPOSAL,
not shipped.** The rule it argues: a border means "you can press this";
static cards separate by tone and room instead. Do not apply it to either
app without Chris and the girls choosing it from the prototype, and if it
ships, it ships through the full accent × sky × theme sweep.

### The runway (v94 / Wayfinder v76, both apps)

Today's prime space held generic counters and, briefly, two copies of the same
door. It now answers two questions instead — **what is necessary, and what is
possible, before the next test.** `runway(date)` finds the next unscored
`assess` within 14 days and gathers, for THAT subject: review still due,
lessons still open, and the next student-hours window.

```
BEFORE YOUR MATH QUIZ
Friday · in 3 days
  12  review questions due in Accelerated Math      ›   → review round, that subject only
  14  lessons open · pick up 1-2 Place Value…       ›   → straight into that lesson
  🕐 Student hours Thursdays, 7:00–7:30 am — the last one before it.
```

Rules that are the point:

- **`assess` records only.** School-wide events are not subject-specific, so
  "what is still open in that subject" would be a lie — and benchmark testing
  (Fast Bridge) explicitly has nothing to revise for, so turning it into a
  countdown would provoke exactly the cramming the calendar layer refuses.
- **Name ONE lesson, never a pile.** "14 lessons still open" is the whole book
  restated as a debt. The count stays (it is true) but the words point at the
  next actionable thing — the lesson she was last in, else the first unstarted.
- **`nextHoursBefore()` says when it is the LAST window** before the test.
  Stated, never nagged. Today only counts while its afternoon slot is still
  ahead (`AZ.nowMinutes() < 900`). Gated by `HOURS_START` where the app defines
  one — the `typeof` check covers Ad Astra, which has no gate.
- **Nothing outstanding says so**, rather than rendering empty rows.

**Two redundancies removed at the same time**, both introduced by the v93 hero:

- `threadTarget(date, opt)` now returns a **`kind`** (`due`/`ramp`/`lesson`/
  `plan`) plus `classId`/`unitId`, and takes `opt.skipDue` so a caller that
  already shows the Growth door can ask for the next-best thread. Today renders
  the hero only when it is not repeating the strip tile or the runway's lesson.
  Measured before the fix: the strip said "10 · to review · Growth Zone" and
  the hero directly beneath said "10 questions are back" — same number, same
  destination; with nothing due it was "15m suggested · Theatre" above
  "Start: Theatrical Design", same subject, same destination.
- **The strip's Growth tile yields to the runway's review row** — two review
  counts one screen apart read as a contradiction, not as extra information.
  Growth keeps its nav count badge, so the door never disappears.

**"Before the bell" only fires when a bell is within 45 minutes.** It used to
fire at 4am pointing at a drop-off three hours away — accurate and useless.
Outside that window the card gives the shape of the day ("7 classes today ·
First up: Accelerated Math at 7:40 AM"). Live-class and after-school states are
unchanged. The card is now `.daycard`, because it drops its accent wash when a
runway card is present — two accent-washed cards stacked is two focal points,
and a probe looking for `.card.ac` would otherwise find the wrong one (mine
did).

### Stars, rebuilt (v95 / Wayfinder v77, both apps)

Stars counted **activity** and never said what she **knows**. Measured before:
the streak was printed three times on one screen (header pill, glance tile,
stats row), the level three times, the Growth count twice; and seven of its
rows — Days studied, Study sessions, Questions answered, Focus minutes — were
counters that only go up, cannot be acted on, and read identically after a
great month and a mechanical one.

**"What you have locked in" replaces all of it.** `lockedIn()` groups
`cleared` records by subject. A `cleared` record means a question she once
missed came back five times over three weeks and she got every one — the only
signal in either app that **cannot be farmed by showing up**, which is why it
now leads the tab. Each subject is a chip carrying that subject's colour and
opening it. The empty state explains the bar rather than showing a zero.

**Trophies come home.** `trophies()` collects topic crests already won on a
shelf (`crestWon`) and books already finished in the reading log
(`mode:'readfin'`). Both were earned elsewhere and appeared nowhere on the tab
that is supposed to hold achievements. No new mechanic, nothing storable,
nothing that can be un-won.

**`movement(date)`** prints at most one line: a subject whose accuracy over
the last three weeks beats the three before it by 8+ points, with 15+ answers
on **both** sides so a couple of lucky rounds cannot manufacture a trend. It
names the direction and stops — change, never a grade. Same rule as the
calibration card.

**Badges: earned first, the rest behind one tap.** A grid where more than half
the tiles are greyed "not yet" is the nearest thing to a nag mechanic in
either app, and neither runs a prize economy. Nothing is removed — the button
says how many remain and shows them all.

Net: **1.9 screens → 1.4**, and no number is printed twice. The sky map is
untouched; it was already doing exactly this.

Two traps, both mine, both caught by rendering rather than reading:
`shelvesFor()` returns `{shelves, loose}` and I called `.forEach` on it — the
whole tab threw. And two of my own assertions were wrong before the code was:
`ctx.view` is not the current screen (the global `view` is), and an unscoped
`/bad/i` "grade word" check matches **Bad**ges.

### Vertical rhythm (v97 / Wayfinder v79, both apps)

Chris flagged Today as feeling tight. Measuring it found **seven** different
gaps between sibling blocks, grown one feature at a time: 0, 2, 8, 9, 10, 12,
14, 26. The 2px was the visible one — `.statstrip`'s margin was `14px 0 2px`,
so the strip was glued to the hero card beneath it — and two pairs sat flush
at 0px, including the badge grid against its own "N more to find" button.

**Three tokens now, and every gap on every tab is one of them:**

| token | value | between |
|---|---|---|
| `--gap-row` | 10px | rows of a list — periods, misses, plan rows, options, events |
| `--gap` | 14px | sibling blocks — cards, card buttons, the strip |
| `--gap-sec` | 26px | the air before a section divider |

10px is not arbitrary: it is what the existing `.btn+.btn` rule already
required ("don't crowd tap targets to save vertical space"), so the row scale
settles on the documented floor rather than under it.

`tools/test_rhythm.js` walks Today, Study, Growth and Stars and asserts the
whole screen uses only that scale, so a future one-off gap fails a test rather
than accumulating.

Two things the same screenshot showed, both fixed:

- **The weekday was printed twice on a weekend.** The eyebrow says "Saturday,
  August 15" and the heading said "Saturday" again 40px below. It now says
  **"No school today · Back on Monday"** — the thing a weekend actually wants
  to know.
- **`.opt` had diverged**: 12px in this app, 9px in Wayfinder. The same element
  spaced two different ways. Both now use `--gap-row`.

**The timetable folds on a day off** (v98, THIS APP ONLY). The schedule is
identical every weekday, so on a Saturday it was eleven rows of hypothetical —
measured at 1703px, against 957px folded, so **746px** of the screen was a
schedule that did not apply. It now sits behind "Show the weekday timetable";
`ctx._showTT` opens it, nothing is removed, and a school day is never folded.
**Events still render when it is folded** — a performance or a community
evening on a day off is the opposite of hypothetical.

Deliberately not ported: Wayfinder's schedule ROTATES, so on an off-day it
already shows the next school day's real line-up rather than a generic
timetable. That is news, and folding it would hide something true.

### Direction A — the subject owns the colour (v116 / Wayfinder v94, both apps)

Chris, 2026-08: *"The main pages look too monochromatic... It would be nice for
the right things to be the center of attention."* Three directions were built as
real UI in `ad-astra/prototype-focus.html` and he chose **A**.

The diagnosis: one hue was doing every job — important, interactive, active,
decorative — so it signalled none of them. Under A the accent keeps **one** job,
*the thing you can tap*, and anything that belongs to a subject wears that
subject's own hue instead. Three render sites opt in by adding `subj-a` and
setting `--pc` from `classColor()`: the runway card (always — it is about one
subject's test), the week card (only when `wk.focusCid` resolves), and a Coming
up row (only when the item has a `classId`).

Rules that are the point:

- **A subject hue only ever appears where that subject is the topic.** It is
  never decoration. The three strip tiles (Growth / Reading / Level) deliberately
  keep the accent: they are not subject-bound, and colouring them would be
  exactly the "hue everywhere" problem this replaces.
- **`--pc-fg` is the subject colour as TEXT, exactly as `--ac-fg` is for the
  accent, and for the same reason.** The palette's `g1` values are FILLS,
  designed to sit behind white labels on a subject tile. Used as text they
  measured 4.37:1 for orchid in dark and failed on **all twelve** in light,
  worst 1.60:1. `--pc-fg` lifts 10% toward white in dark and deepens to 42%
  over ink in light: worst case **4.90:1** (orchid, dark) and **5.76:1** (lime,
  light) across every palette in both themes.
- **The 3px rules use `--pc-fg`, never raw `--pc`** — the same call `.row.now`
  already made for `--ac-fg`. Raw `--pc` as a rule measured **1.65:1** in light:
  a hue, not a mark. With `--pc-fg`, 5.98:1. The same upgrade was applied to the
  four pre-existing raw-`--pc` rules (`.rw.lead`, `.lk`, `.tile`, `.plan`);
  painted `.subj` tiles are unaffected — they hide their border by design
  because the fill IS the subject colour.
- **`--pc-fg` must be DECLARED on every element that can carry its own `--pc`.**
  An unregistered custom property resolves its `var()` references on the element
  where it is declared, so a week-card row that overrides `--pc` still inherits
  the CARD's already-computed `--pc-fg` — the lead rows wore the focus subject's
  colour no matter whose door they were. The declaration selector list therefore
  names `.rw.lead`, `.lk`, `.tile` and `.plan` alongside the `subj-a` classes.
- **The week card's doors are not all one subject.** A lesson door can point at
  another class, so the row rule lives on `.rw.lead` (which carries its own
  `--pc`), and the card-wide `.rw` rule is scoped to the runway — whose rows
  really are all the card's subject.
- **`.row.now` still wins over `.row.subj-a`** (later in the sheet, equal
  specificity), and that is correct: accent means "this lands today", subject
  hue means "this subject". Today is a different axis from topic.

Two cascade traps, both real, both caught by rendering rather than reading:

> ⚠️ **`.card.ac` sets the same `background-image` at equal specificity and
> later in the sheet.** The subject gradient written with the other `subj-a`
> rules was silently replaced by the accent one — the eyebrow and rules went
> subject-coloured while the card itself stayed accent. The wash therefore
> lives *after* `.card.ac` and is written `.card.subj-a,.card.ac.subj-a`.

> ⚠️ **That rule must NOT set `background-color`.** `.card.ac.week` and
> `.card.ac.daycard` carry the glass mix that lets the comet through, at the
> same specificity and earlier in the sheet — setting it would quietly make the
> two top cards opaque again.

**Directions B (depth, not hue) and C (one loud thing) were not chosen.**
`prototype-focus.html` stays as the reference; it is a dev artifact, not cached
by the service worker and not linked from the app.

### The batch of four (v118 / Wayfinder v96, both apps)

Four small improvements from the v117 review's idea list, shipped together.

**The resume door on Today.** A round parked earlier today renders as a hero
card — "Pick your round back up · <unit> · N of M answered" — straight back
into the quiz. Rules that are the point:

- **It outranks every suggestion, and the generic hero yields to it** (`pkLive`
  joins the dupe conditions): a half-finished round is not advice, it is her
  own work made findable.
- **Same validity rules as `loadRound`, WITHOUT consuming the save** — today
  only, a real approved unit, matching question fingerprint. The quiz screen
  still owns the actual pickup.
- **The save fires before Next advances**, so an answered question still sits
  at `pk.i` — the door's "questions left" check steps past it the way the
  quiz's own resume does, or it shows for a finished round and tapping it
  starts a fresh one (caught live: "3 of 3 answered" with nothing to resume).
- `saveRound` now stores `classId` (it lived only in nav ctx), so the door can
  route without guessing at `__all__` units.

**The star sky gate is content-shaped, and Latin joined it.** The old gate was
`/wordly wise/i` on the title; now it also needs **≥6 single-word cards**
(`skyCards` filters multi-word terms — 'First declension' or 'C — vacca' are
cards, not words you can say into a microphone), and Latin units qualify.
Measured on the real shelf: Unit 1's eight case names get the game; the
Pronunciation & Greetings unit (3 single-word cards after filtering) rightly
does not. Deliberately NOT opened to science units with single-word terms —
the allowlist stays vocabulary. Belt and braces: the clue line is now run
through `skyBlank` too, so a future def that uses its own word cannot hand
the answer over.

**A right answer buzzes back** — `[12, 40, 12]`, the star sky's win pattern
scaled down. **A miss deliberately gets nothing: the phone never scolds.**

**Growth Zone group headers wear their subject's rule** (`.subjline`,
direction A carried to the screen where she acts on it). Same grammar as a
Coming up row: this colour = this subject, wherever she meets it.

### Signed up, and the club on the day (v99, THIS APP ONLY)

Starring a club and being registered for it were the **same flag**, which is
why Sedona's ASL Club came off the list when she tidied her wishlist — she had
actually signed up for it. They are different facts and now have different
states.

`clubState(id)` reads the one `clubpicks` map that already existed and returns
`'reg'` / `'want'` / `null`. **A stored `true` predates this and reads as
`'want'`** — exactly what it meant when it was written, so nothing migrates.
`setClubState()` writes it; the detail modal gains "✓ I am signed up for this"
below the star, and the clubs screen splits into *You are signed up for* and
*Starred — hoping to join*. The cost total stays on the starred block, where
"if you got all of these" is the question being asked.

**A registered club joins the day it meets**, as an `.evt.club` row after the
last period. Rules that are the point:

- **Only when the day, the time AND the cadence are all genuinely derivable.**
  `weekly*` → every matching weekday from `first`; `bi-weekly` → every 14 days
  from the first matching weekday (which is not always `first` itself);
  **everything else is not placed**. Of 34 clubs, 6 list no time and 3 say
  only "monthly" — a monthly club gives no week, and putting it on a guessed
  one would be the app inventing her afternoon. The signed-up card SAYS how
  many of hers are placed rather than leaving the omission to be noticed.
- **Starred clubs never appear on a day.** A star is a wish; a schedule is a
  claim about what is happening.
- It takes the **quiet plate with an accent left rule** (`.evt.club`), not the
  full accent wash a pinned school event gets — two accent-washed rows on one
  day is two focal points — so the day reads as one of hers among the school's.
- **Folded away with the timetable on a day off**, because a club does not meet
  when there is no school.
- `.st.reg` (green tick) and `.st.want` (accent star) replaced a single
  `.st.done`; the glyph already separates them and the colour only reinforces.

`tools/test_clubs.js` covers the states, the cadence arithmetic over a whole
year, and that nothing vague is ever placed; `tools/contrast_clubs.js` sweeps
the new surfaces across accent × sky × theme (288 samples, worst 6.44:1).

**Real dates beat inferred cadence (v131).** A club may carry **`dates`** —
an explicit array of ISO meeting dates — and when present `clubMeetsOn()`
uses it directly instead of computing from `freq`/`first`. Built for ASL
Club: the teacher's actual remaining-year schedule (ParentSquare, 2026-08)
turned out to be genuinely irregular — a 7-day gap around Veterans Day, a
five-week winter-break gap, and Feb 15 named outright as "NO MEETING"
(which is also Presidents Day on `CAL.closed` — the two independent sources
agree). A pure every-14-days rule from the original `first:'Aug 17'` would
have placed both of those wrong, so the real list wins outright rather than
being reconciled against the cadence math. A date the club is explicitly
**not** meeting is simply left out of the array — never encoded as a rule of
its own. `freq`/`first` stay on the record for the "N of yours are placed"
count and the row's caption text; only placement itself defers to `dates`.

> ⚠️ **`go(screen)` resets `ctx` to `{}`.** Setting `ctx._showTT = true`
> *before* `go('today')` in a test does nothing — the flag has to be set
> *after* the navigation, followed by a plain `render()` (not another `go()`,
> which would reset it again). Caught because the club-row assertion in
> `tools/test_clubs.js` failed even though `clubsOn(date)` was already
> returning the right club — the row itself was folded away with the rest of
> the period list, which has been folded by default since v106.

**"On the horizon" said the same thing twice** (v99 / Wayfinder v80, both
apps), caught in a screenshot of the club work. The card printed the next
milestone and then "Quarter N ends" beneath it — and since every milestone in
both calendars **is** a quarter boundary, those were the same fact and the
same number on **242 of ~290 school days**. The quarter row now renders only
when `ms.date !== q.end`.

> The first version of `tools/test_horizon.js` passed against the unfixed app.
> It regexed `/(\d+) days/` over the card's concatenated text, where "End of
> Quarter 1" + "3 days" reads as "…Quarter 13 days" — so it compared "13 days"
> against "3 days" and saw no duplicate. It reads the `.v` cells now. Reverting
> the fix and watching the test fail is what exposed it; a green test on a bug
> you can see in a screenshot means the test is wrong.

### Paper study guides — two doors (v87 / Wayfinder v69, both apps)

A unit flagged **`guide:true`** mirrors a printout the class handed out, and
gets two doors on its card instead of the usual mode tiles. Built for Sedona's
Test 1 Study Guide (Chris, 2026-08); it is engine, so both apps carry it.

**Door 1 — "I did it on paper."** `SCREENS.guideentry` is a grid of A/B/C/D,
one row per question. Thirty taps instead of thirty quiz screens, because she
has already done the thinking on paper. `gradeGuide()` then writes everything
an ordinary round writes — qstats, misses, one `log` (tagged `paper:true`) —
and hands off to `SCREENS.guidewalk`: what she got wrong, what she put, the
right answer, and the `steps` revealed on demand.

**Door 2 — "Work it here."** The ordinary quiz screen with `guideMode:'work'`:
every question in the authored order, and her place saved after each answer.

**The rescue round** (`__rescue__`, `buildRescueUnit()`): for each missed
question that carries a hand-written **`variant`**, it asks the variant — same
skill, fresh numbers. Synthetic like `__review__`; never stored, never synced.

Rules that are the point:

- **Option order is FIXED on a guide unit.** Everywhere else options shuffle so
  the answer cannot be learned by position (v64). Here they must not: she is
  entering the letter she wrote, and if the app's C is not the paper's C the
  whole mode is a lie. Scoped to `u.guide`; the rescue round shuffles normally,
  because that is practice, not transcription.
- **A blank is a blank, never a wrong answer.** Skipping a question on paper is
  not the same as missing it, and scoring it wrong would put a question she
  never attempted onto the review ladder. The button says how many it will mark.
- **The rescue round never moves the ladder, in either direction.** Answering a
  fresh variant moments after reading the walkthrough is massed practice, not
  spaced retrieval; promoting the box would credit a durability she has not
  shown. `finishQuiz` excludes `__rescue__`, and `answer()` writes no new miss
  for a `_rescue` question. Attempts still count, so the work is visible.
- **`guidepass` is one record per unit** (`guide_<unitId>`), holding
  `{answers:{qid:idx}, submitted}`. In `PROGRESS_TYPES`, so Fresh start clears
  it. The deterministic id means it can never duplicate across devices.
- **Variants are hand-authored and verified**, never generated — a confidently
  wrong rescue question is worse than none. All 30 for Test 1 were re-derived
  independently in the builder's assertions. `check_content.py` enforces that a
  guide unit has a variant on every question, and that each variant is not a
  copy of its original.

Incidental, caught by screenshot: the walkthrough steps were first built out of
`.row`/`.k`/`.v`, which is a label-and-value layout — `.row .v` is
`white-space:nowrap`, so a sentence-long step ran off the side of the screen.
They now use the same `.step` markup the quiz's own walkthrough uses, and
`test_overflow.js` opens every walkthrough at once to keep it that way.

### The Wordly Wise Book 9 shelf (v73)

Sedona's vocabulary lessons ship as `Wordly Wise Book 9 · Lesson N`, so they
shelve as one book. 15 cards (every card carries hand-checked `sp`) and 18
questions each, 3–4 of them analogies. All seven lessons are built.

**Lesson 2's PDF is a pure scan with no text layer** — every text extraction
(Drive's included) returns empty on it. It was read by rendering the pages to
images with `pypdfium2` and reading those. If a source file comes back empty,
render it rather than assuming the file is broken; and never guess a word list
from the lesson numbering.

### Per-unit sitting size (v69 / Wayfinder v57, both apps)

A unit may carry **`round`** — how many questions `pickRound()` serves per
sitting (default `QUIZ_ROUND` = 5). The unit pill reads "one sitting" when
`round >= questions.length`. Built for River's math program (a lesson-a-day
unit serves all ~10 questions in one quiz; a topic review holds a 24-question
pool served 12 at a time), but it is engine, so both apps carry it. Content
knob only — selection order (least-practised, Growth-Zone-last, recency) is
untouched. This app ships the engine with no `round` content yet.

### The learning pass (v65 / Wayfinder v53, both apps)

A code-review-plus-educator sweep. Four engine changes, all rules-compliant:

- **`AZ.shift()` timezone fix.** It built a LOCAL-midnight `Date` and formatted
  it in Arizona time — identical on a Phoenix phone, one day short on any
  device east of Arizona, which silently compressed every review-ladder
  interval. Now pure calendar arithmetic (`Date.UTC` in, ISO slice out).
  Verified across month end, year end, leap day and negative shifts.
- **Recency-aware `pickRound()`.** `qstat.updatedAt` is stamped on every answer,
  so it doubles as last-seen for free. Among equal attempt counts the question
  met longest ago comes back first — spaced retrieval for material she got
  RIGHT, not only for misses (successive relearning, not just error repair).
- **"See it again tomorrow"** (`🌱`, quiz explain block, correct answers only).
  A right answer she is not sure of is hidden shakiness no tally can see. One
  tap writes an ordinary box-0 miss — her call, no XP change, no penalty.
  Hidden in review rounds and when the question is already laddered. This is
  self-flagged fragile knowledge: metacognition plus autonomy, and it must
  never gain a cost or a guilt mechanic.
- **"Depth of understanding"** (parent view). Accuracy split by question level
  (recall / apply / analyze), rendered only with ≥4 attempts on ≥2 levels, with
  one interpretive line when the spread is ≥15 points. Levels are looked up
  from the unit at render time — nothing new is stored.

Plus the pipeline now enforces the shuffle invariant: the generation prompt
forbids positional references outright, and `generateUnit()` drops any question
whose text matches the positional/"of the above" pattern — belt and braces.

**Editing a shipped content file requires bumping its `updatedAt`** or the fix
never propagates: an approval re-stamps the record newer, and merge keeps the
newer copy. Bumping re-drafts the unit on synced devices (approval is part of
the record), so the grown-up re-approves once — say so when you do it.
Since v67/Wayfinder v55, `fetchLibrary()` tags such re-drafts `wasApproved`,
the queue labels them "update to a unit you approved", the toast counts them
separately from genuinely new units, and approving clears the flag. The gate
itself is deliberate and stays: a fix is new content, and nothing reaches her
unread — the marker only makes the second read cheap.

**`libv` — a content version, because timestamps alone were not enough
(v88 / Wayfinder v70).** Bumping `updatedAt` is necessary but NOT sufficient:
approving a unit re-stamps it to the moment of approval, so a fix shipped even
minutes earlier LOSES the merge and vanishes. The toast then says "library
already in sync", which is a lie — the file differs. This bit for real on
2026-08-13: the Test 1 Study Guide's guide flag and 30 variants were shipped,
Chris approved the previous version afterwards, and his approval silently ate
the update.

A shipped unit may now carry **`libv`**, an integer the author bumps whenever
the file's content changes. In `fetchLibrary()`, an incoming unit whose `libv`
beats the local copy's has its stamp lifted just past the local record, so the
ordinary merge does the right thing regardless of when anything was approved.

- **Bump `libv` on every edit to a shipped file**, alongside `updatedAt`. The
  timestamp still matters for ordinary sync; `libv` is what makes a content fix
  immune to the approval race.
- **Tombstones still win.** A discarded unit is skipped outright, so a newer
  `libv` cannot resurrect it; re-shipping one deliberately still means bumping
  `updatedAt` past the discard. Both are covered by `test_tomb_lib.js`.
- Stamp `updatedAt` at **just before now** — newer than anything already
  written, never in the future. The older "hours back, minimum" advice was an
  over-correction from the 18-hours-in-the-FUTURE incident; hours-back is
  actively wrong when the grown-up approved an hour ago.

**Spoken-as coverage:** every Wordly Wise unit now carries `sp` on all cards —
Lessons 2–5 from the book's own pronunciation guides, Lesson 1 hand-authored
(its source is a photo transcription with no guides). Future vocab units
should ship with `sp` from day one.

### How questions should make her think (v63, both apps)

Derived from her actual Physics lab, which Chris supplied **as style context
rather than as material to build** — the point was to calibrate the questions,
not to make a unit out of it. That lab asks: predict forward from your
expression, solve backwards for the other variable, state the *physical
significance* of a slope, say how you knew, reason counterfactually ("if the
car were faster…"), and rank several slopes with ties allowed.

Those moves are now in the generation system prompt in both apps, and
hand-written units should use them too:

- **Interpret, don't just compute.** What does the slope/intercept/rate *mean*
  here, not only what does it equal.
- **Both directions.** If one question predicts an output from an input,
  another solves backwards for the input.
- **Counterfactual.** Change one variable, ask what follows and why.
- **Rank, don't just pick.** Use `kind:'order'` for a strict ranking. It
  **cannot express a tie**, so a genuine tie must be asked as multiple choice
  over candidate rankings.
- **Make her say how she knew.** Prefer options that state a *reason* over
  options that state only an answer.
- **Carry the units.** A rate per second asked about in minutes — the
  conversion is part of the work, not friction to smooth away.

If a teacher's own assignment shows a distinctive question style, that is worth
capturing here the same way. The transferable thing is the *shape of the
thinking*, and it costs nothing to match it.

### The day (v76 / Wayfinder v59, both apps)

`SCREENS.day` — the parent-side answer to "what did she actually do today",
which the weekly aggregates never gave. Reached from a **Today** card at the
top of the parent view; steps back through history a day at a time.

- **`dayReport(date)`** derives everything from existing `log` and `focus`
  records at render time — no new record types, no counters, backfills over
  all history.
- Shows the day's sessions **in order** (each labelled by `modeLabel()`:
  Quiz, Beat the clock, Growth Zone review, Shuffle round, Flashcards,
  Reading, Focus timer), each with its score where it has one, then the same
  day **broken down by subject**, each subject expandable to its own
  sessions.
- **Quizzes carry a score; nothing else does.** A flashcard run has no
  score and inventing one for visual symmetry would be a lie.
- **No clock times, deliberately.** `at` orders the day's sessions and does
  nothing else — when she studied is surveillance flavour, not actionable
  signal (same call as the activity card).
- Mission Control gained a **Today** line, so one parent screen shows both
  girls' current day.

**Redesigned as a dashboard (v78 / Wayfinder v61).** Four stat tiles
(minutes, quizzes, accuracy with a meter, Growth due) → subjects with
accuracy meters → every session → **inside a quiz session, every question
with what she picked**. Each layer is one tap deeper.

- Quiz logs now carry **`items`**: `{c, qt, ch, ca}` per question — right
  flag, question text, what she chose, and the correct answer *only when she
  got it wrong* (when right, the two are the same). Stored as short **text,
  not option indexes**: options shuffle per question and a unit can be edited
  later, so an index would quietly point at the wrong option months on.
  Capped at `QUIZ_ITEM_MAX` (40) so one long round cannot bloat the gist.
- Purely additive — logs written before this keep their scores, render fine,
  and the screen says so rather than pretending the detail is missing.
- **"Open the day" sits directly under the Sandbox row** at the top of the
  grown-up area: it is the screen a parent opens most, so it does not belong
  buried mid-page.
- **The emotion check, per session** (v80 / Wayfinder v63): each quiz's
  readiness and before/after mood, matched to its session by `logId` rather
  than by time, with a compact emoji chip on the session's meta line. The
  card states the **calibration** outright — "Felt ready for 100% · scored
  50%" plus one interpretive line — because the GAP is the whole point of
  the readiness rating, not the number. A pre-quiz mood of 1–2 adds the same
  gentle-check-in note the all-time card uses. Sessions with no check-in
  (she skipped it, or it was flashcards) simply do not appear.
- **Growth Zone due, per subject**, renders on the day screen — but only on
  TODAY. "Due" is a current state, not something that was true on a past
  date; showing it under an old day would be a plain lie.

**One day, one list (v84 / Wayfinder v66).** A UX pass measured the screen
rather than reading it: an ordinary evening rendered **18 cards over 3.7
screens**, with `67%` printed six times and the same interpretive sentence
printed twice, word for word. It had grown into three complete inventories of
the same sessions — By subject, Session by session, How she felt — sorted three
ways, leaving a parent to assemble the meaning. Now **7 cards over 2.0
screens**, and no duplicated sentence.

- **One spine.** Sessions live in a single card as rows, each opening to
  *everything* about that session — its questions and its emotion check
  together. "How she felt" is gone as a section; it was naming the quiz a
  second time in order to exist.
- **`ctx.dayView`** toggles that one list between `order` and `subject`
  (chips, default `order`). Subject mode groups the SAME session objects under
  `daySubjectHead()` — so the drill-down stays one tap from either view, and
  `rep.sessions.indexOf(s)` keeps the open session open across the toggle.
- **`daySignals(rep)` → "Worth a word"**, the layer that was missing: at most
  **two** things a parent might actually raise, each linking to its session.
  Ranked wellbeing-first (low mood → stopped early → big negative calibration
  gap → weak subject → beat-her-own-expectation). The rules are the point and
  do not relax: it describes a SESSION, never her; no verdict language; good
  news is eligible; capped at two so it can never become a list of faults;
  and when nothing stands out it SAYS so, because an ordinary evening is
  information too.
- **The interpretive line prints only when `|gap| > 15`.** Printing it under
  every quiz is what turned it into wallpaper.
- **Rows with nothing underneath are not buttons.** They used to render as
  disabled buttons identical to live ones — half the boxes were inert. Dead
  buttons went 2 → 0.
- **Misses first, and by default misses only** (`ctx.allQ`). An open
  18-question quiz showed 18 rows; what a parent acts on is the handful she
  got wrong, and the confirmations buried them. It now shows 6, captioned
  "6 missed of 18" with "Show all 18" beside it. The count is ALWAYS stated,
  so nothing is hidden silently, and a perfect round says "All 4 right"
  rather than rendering four rows of agreement. `allQ` rides the
  order/subject chips but is deliberately dropped when a DIFFERENT session is
  opened, so every session starts at misses-first.
- `.felt` lays `--ac-8` over the card, which is the tint trap: `--faint`
  measured **4.30:1** there in dark and now uses `--muted` (worst case 4.69:1
  across all accents, both themes). The probe that caught it had to be
  hardened first — routing the accent through `prefs()` silently did nothing,
  so it reported one ratio twelve times and called it a pass.
- Incidental, found by the smoke test: `.back-chip` was `min-height:40px`
  against the stated 44px minimum, on a control that appears on nearly every
  screen.

**Tap targets (v86 / Wayfinder v68).** A sweep of every screen in both apps —
seeded and on a fresh install — found `.btn-sm` at `min-height:40px`, the last
control class under the stated minimum. It carries *Show the answer* (tutor),
*Reset to defaults* (setup), and in the parent view *Turn on*, *Add score*, the
score button itself and *Show what she was told*. Now `var(--tap)`. Together
with the `.back-chip` fix, **no button in either app renders under 44px on any
screen.** The one remaining disabled button — *Start the quiz* on the check-in
— is correct: it enables once both taps are made, which was verified rather
than assumed.

### Leaving a quiz part-way (v77 / Wayfinder v60, both apps)

A round she abandons is logged as **the questions she actually answered** —
never as the full round with the rest counted wrong. `finishQuiz(u, partial)`
takes the flag; `go()` calls it when navigating away from the quiz view with
at least one answer on `quizState.seen`.

- **It never counted unanswered questions wrong** — before this, quitting
  wrote no log at all. The bug was the other way round: her answers already
  updated `qstat` and the Growth Zone as they happened, but with no `log` the
  session left no minutes, no XP, no streak or sky-map day, and nothing in
  the day view. Real work vanished.
- `total` = `quizState.seen.length` on a partial round, so accuracy is over
  what she answered.
- **No completion or speed bonus** on a short round — per-question XP only.
  Finishing is what those bonuses are for.
- `quizState.logged` makes a round loggable exactly once; `quizState` is
  cleared afterwards so returning starts a fresh round rather than resuming
  a logged one.
- **The "Exit quiz" button had to be fixed too** (v78): it nulled `quizState`
  before navigating, so the `go()` hook never saw the round and the most
  common way of leaving was the one that still lost the work. It now logs
  the partial round first, then clears.
- Everything else in `finishQuiz` already judged only `askedThisRound`, so
  the miss ladder, qstats and badges settle correctly on a short round.
- The day view labels it "Quiz · stopped early". That is parent-side
  information, not a mark against her — her own screens say nothing.
- **A resumed round's clock excludes the parked gap (v117 / Wayfinder v95).**
  `seconds` is `now − quizState.start`, and the saved round carried `start`
  verbatim — so a round parked at 8am and resumed at 6pm logged ten hours of
  "study" into the day view and the parent's weekly minutes. `saveRound` now
  stores `elapsed` and the resume path rebases `start = now − elapsed`. A save
  from an older client has no `elapsed` and restarts the clock at zero —
  undercounting is the safe direction.
- **Closing or backgrounding the app mid-round (v83 / Wayfinder v65).** The
  navigation hooks above only fire on in-app navigation or the Exit button.
  On a phone the commonest way a quiz ends is none of those — she switches
  apps, locks the screen, or the PWA is killed. `persistRound()` now runs on
  `visibilitychange` (hidden) and `pagehide` and writes the round's log at
  that moment. `put()` writes through to localStorage synchronously, which is
  what makes it survive; sync happens on next launch.
  - It deliberately does **not** settle the ladder or clear `quizState` — a
    quick app-switch must not cost her the round she is in.
  - `quizState.logId` keeps it to ONE record: coming back and finishing
    updates that same log in place rather than adding a second.
  - `quizState.settled` (not `logged`) now guards the ladder, so the two
    concerns are separate: the log may be written many times, the ladder
    exactly once.
  - `beforeunload` is deliberately unused — mobile browsers fire it
    unreliably.

### Teach it back, the weekly aim, and the activity view (v66 / Wayfinder v54, both apps)

Three additions from the educator review, approved by Chris 2026-08-09.

**Teach it back** (`teach` records, postmood screen). After a quiz of 80%+ on
4+ questions, the check-in screen offers one optional textarea: explain the
trickiest idea in your own words. Saved verbatim (keyed `teach_<logId>` so a
log can only ever produce one), surfaced in the parent view under "In her own
words", quoted exactly. Rules that are the point: never required, never
graded, and deliberately **no XP** — explaining is its own payoff and pricing
it would cheapen it (the app says so in its own copy). In `PROGRESS_TYPES`.

**The weekly aim** (`prefs.intent = {text, week, done}`). One small self-set
goal, entered on Study, keyed to `AZ.weekStart()` so it dissolves every
Monday. Tracked by nothing except her own tap on Done. It appears in exactly
two places: her Study tab, and one quiet line in the parent activity card
("marked done by her"). Self-set proximal goals beat assigned ones for
commitment — and the moment this gains a consequence it stops working, so it
must never gain one.

**Activity, last 7 days** (parent view). This week against last, per mode:
active days, minutes, quiz rounds, flashcard runs, focus minutes, reading
minutes — each with "(was N)" — plus "Where the week went" (top subjects by
minutes). All derived from existing `log`/`focus` records at render time;
nothing new is stored. Time-of-day patterns were considered and deliberately
left out: that is surveillance flavour, not actionable signal.

### Retired: the orientation unit

"First Week: Rooms & Teachers" was removed in v22 (schema v4 tombstones
`unit-orientation` on migrate). Don't reintroduce boot-generated units.

### An extracurricular subject — ASL (v129, THIS APP ONLY)

Sedona takes American Sign Language through school as an extracurricular
club. She wanted it to get the same study space as a real class — flashcards,
a quiz, its own colour — but it is not a period on her `.ics` timetable, and
it never will be.

**`EXTRACURRICULARS` is a second array, deliberately not folded into
`CLASSES`.** Every raw read of `CLASSES` (the weekday timetable, "before the
bell", "tomorrow starts with…") assumes every entry has a real `start`/`end`
minute and a room, because it is rendering an actual schedule. An
extracurricular has neither. Adding it to `CLASSES` would have put it on the
timetable as a period with a garbage time (`fmtTime(undefined)`), or forced a
fake time onto a club that doesn't meet during the school day — the app
inventing her afternoon, which the clubs feature already refuses to do
elsewhere. Instead `CLASS_BY_ID` and `STUDY_CLASSES` are built from
`CLASSES.concat(EXTRACURRICULARS)`, so ASL exists everywhere a *subject*
needs to exist — Study tiles, the study plan, the tutor, Subject colours, the
Growth Zone, the review queue, focus timer, unit generation — and nowhere a
*period* needs to exist. If you add another extracurricular, it goes in
`EXTRACURRICULARS`, never `CLASSES`.

- **One render site assumed every subject has a period and had to be
  taught otherwise.** `SCREENS.unit`'s eyebrow read
  `` `${fmtTime(c.start)} · ${whereLine(c)}` `` unconditionally — the one
  place a raw `CLASSES`-shaped read leaked into a `STUDY_CLASSES`-only
  screen. It now checks `c.extracurricular` first and prints "Extracurricular"
  instead of a NaN time and an undefined room.
- **`applyTheme()`'s icon-override loop was `CLASSES`-only too**, which
  would have silently ignored her picking a different icon for ASL in
  Subject colours. Now `CLASSES.concat(EXTRACURRICULARS)`.
- Palette: **coral** — the one `SUBJECT_PALETTE` entry no class had claimed.
  Texture: `.pat-asl`, paired dots on the diagonal (two points of contact),
  distinct from Biology's single dot grid.

**ASL is learned by watching a sign, not by reading about one — so the
content never tries to describe a handshape or a movement in words.** A
confidently wrong text description of a physical sign is worse than none,
the same principle that keeps `sp` (spoken-as) hand-authored-only. Instead a
card may carry **`watchUrl`**, rendered as a real button on the back face
(`.watchb`, 44px, opens in a new tab) reading "▶ Watch the sign · \<host\>" —
the hostname is parsed from the URL and printed on the button itself, so
leaving the app is never a surprise. `stopPropagation` keeps the tap from
also flipping the card. Every `watchUrl` in `content/asl-1.json` was found
and verified by search against Signing Savvy (a real ASL video dictionary),
never guessed or pattern-matched from the word.

- **The card's own `def` covers only what the sign MEANS and when you'd use
  it** — never the handshape or motion. The orientation card (`c0`) says
  this rule outright, so it doesn't need re-explaining on every card.
- `unit-asl1` is titled `ASL Club · Class 1`, on purpose — the ` · ` shelves
  it the moment a second class's vocabulary ships, the same convention as
  the Wordly Wise and Algebra shelves.
- Quiz questions test vocabulary — meaning, category, opposite pairs, which
  phrase fits a scenario — never handshape recognition, since there is no
  way to test that without the video itself. All eleven words from Class 1
  are covered, `round:11` (one sitting, matching how the class actually
  runs).
- Ships `status:'draft'` and through `CONTENT_LIBRARY` like everything else
  — nothing about a club exempts it from the review queue.

`tools/test_asl.js` covers the split: ASL renders as a Study tile and a
working subject page, quiz and flashcards (with a working, correctly-hosted
Watch button that doesn't flip the card) — and never appears on the weekday
timetable, with no NaN leaking into the schedule render.

**The review queue didn't show the video either (v129 follow-up).** Chris
caught this live: the parent review screen listed each card's term and
definition — including the sentence "watch the linked video" — with nothing
actually clickable. `watchNode(card, linkClass)` is now the one function
both render sites (the flashcard face, the parent review row) call for a
card's video affordance, so a fix to one can never again miss the other.

**Inline embeds, ready for verified video ids (v130).** YouTube itself is
unreachable from this environment's tooling (WebFetch and even a raw
`curl` both get network-policy-blocked for `youtube.com`), so a real
per-word video could not be sourced and verified the way the Signing Savvy
links were — never guess a video id or trust a search-result title alone
for her app. `watchNode()` now branches: a card carrying **`embedId`** (a
YouTube video id, hand-verified before it ships — same bar as `watchUrl`)
embeds inline via `youtube-nocookie.com` in a responsive `.vidwrap`, no new
tab; a card with only `watchUrl` keeps the external link. The capability
shipped ahead of the content on purpose, so wiring in real ids later is a
one-line change per card, not an engine change.

### The manual alphabet (v130, THIS APP ONLY)

Fingerspelling is the one part of ASL a STATIC IMAGE can teach honestly —
unlike a moving sign, there is no motion to misrepresent, so unlike
`watchUrl`/`embedId` this needed no video and no click-through. `unit-asl-alpha`
("ASL Club · Alphabet") ships 27 cards (one orientation card + all 26
letters), each showing its handshape via a new card field, **`imgUrl`**,
rendered inline by `signImgNode()` — the same shared-function pattern
`watchNode()` set: both the flashcard face and the parent review row call it,
so the review screen shows the actual picture rather than describing one.

- **The images are Wikimedia Commons' `Sign_language_<LETTER>.svg` series**
  — the same public-domain illustrations used in Wikipedia's "American
  manual alphabet" article across many language editions — addressed via
  the stable `Special:FilePath/<filename>` redirect, so no hash-path needed
  guessing. Existence and the public-domain tag were confirmed for all 26
  letters by search before any of them shipped; I did not invent or
  pattern-guess a single filename.
- **Unlike Signing Savvy, hotlinking Commons media is the intended use** —
  the whole point of the license. This is why the alphabet embeds directly
  and the vocabulary signs still only link out: one is a freely-licensed
  static reference, the other is a commercial video dictionary's paid
  content, and those two things get different treatment on purpose.
- **`def` never describes a handshape in words**, same rule as the
  vocabulary cards — the image is the entire answer. J and Z each say
  outright that they trace a small motion the image can't show, rather than
  silently presenting a static picture as the whole story.
- **A unit with zero questions is a real, general case now, not an
  `own`-deck special case.** `unitCard()` used to render a Quiz and Beat-the-
  clock tile unconditionally — harmless before because the only
  zero-question units were `own:true` decks, which bypass `unitCard()`
  entirely through `ownCardsCard()`. The alphabet is an ordinary draft unit
  with `questions:[]`, and would have gotten a Quiz tile that opened onto
  nothing. Both tiles are now gated on `u.questions.length`, and the pill
  reads "reference only" instead of "0 questions · one sitting".
- **`finishCards()`'s no-quiz message now says the right thing for the right
  reason.** It used to say "You wrote these" unconditionally when a deck had
  no questions — true for her own cards, false for a reference deck she
  didn't write. Now checks `u.own` and picks the honest sentence.
- Shelves onto the same "ASL Club" spine as Class 1, via the ordinary
  ` · ` title convention — no new mechanism.

`tools/test_asl.js` covers all of it: the image renders and points at the
real Commons URL, the deck offers Flashcards only, the pill says "reference
only", and finishing the deck neither claims she wrote the cards nor offers
a quiz that isn't there.

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
| **Today** | The school day: what class is now/next, the full schedule, upcoming tests, on the horizon — plus the three-tile strip (see below). Still **not a dashboard**: no affirmation, no streak, and the strip's numbers exist to be tapped, not admired. |
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

**Today gets marked (v79 / Wayfinder v62).** In "Coming up", a row whose item
LANDS today wears `.row.now` — an `--ac-8` tint and a 3px `--ac-fg` rule.
Deliberate boundaries:

- **Only what lands today**: a test dated today, a one-day event today, or a
  multi-day event on its FIRST day. An event already running ("Day 7 of 10")
  stays plain — it is ongoing, not today's business, and if half the list
  lights up the highlight stops meaning anything.
- Day 1 of a multi-day event now reads **"Starts today"** rather than
  "Day 1 of 5", so the highlighted row explains itself.
- The tint and rule only ever REINFORCE a label the row already carries in
  words. Colour is never the sole signal.
- The rule uses `--ac-fg`, not `--ac`: raw accent measured 1.49:1 against the
  tinted row on the light canvas — a hue, not a mark. `--ac-fg` gives 5.06:1
  light and 8.07:1 dark.

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

### Reference sheets (v54 / Wayfinder v44, both apps)

`SHEETS` maps a `classId` to the teacher's own reference sheet, transcribed —
`{nm, ic, note, sections:[{h, rows:[[label, value]]}]}`. Any subject listed
gets a button on its subject screen AND inside its quizzes, alongside the
calculator (`openSheet(classId)`). This app carries two: the math department's
formula sheet (`algeo`) and the Kinematics Unusual Conversion Factors table
(`physics`). Wayfinder ships the same engine with an empty registry until a
teacher issues River one.

They are **reference, not answers**: they restate facts the class hands out on
paper anyway, so the skill under test (method, setup) is untouched. Don't put
worked examples or solution steps in a sheet.

### Spoken-as cards (v58 / Wayfinder v48, both apps)

A card may carry **`sp`** — a hand-checked respelling of its term. Where it is
present the 🔊 button speaks `sp` instead of `term`, and the respelling also
renders under the term as `.saidas`. Built for Latin, but it earns its keep on
anything where reading a word is not the same as saying it.

- **Shown as well as spoken, always.** A recording alone is a black box she
  cannot check; the printed line is what lets her compare the voice to the page
  and catch it being wrong. Never add `sp` without letting it render.
- **Lowercased on the way to the voice.** CAPS mark stress for the eye, but
  Android TTS reads an all-caps run as an acronym and spells "OO" out loud.
- **`.saidas` carries its own dark plate on a painted face.** The `::after`
  scrim only guards the bottom of the card; the respelling sits mid-face, where
  it measured 2.45:1 over the lighter palettes. With the plate: 6.92:1 worst
  case across all twelve, both themes.
- **Hand-authored only.** `sp` is not in `UNIT_SCHEMA` and the model must not
  invent one — a confidently wrong pronunciation is worse than none. Write it,
  verify it, then ship it.
- **Say what the voice cannot do.** The browser voice has no trill, so the
  Latin R card says so outright rather than teaching her a flat r. If a sound
  is beyond the synthesiser, the content admits it.

### Rubric self-check (v63 / Wayfinder v51, both apps)

A `SHEETS` entry may carry a structured **`rubric`** — `{total, rows:[{k, nm,
max, bands:[{nm, lo, hi, d}]}]}`. Where one is present the sheet modal is
**rendered from it**, so the rubric she reads and the rubric she rates herself
against cannot drift apart, and the subject screen gains a second button:
*Check my work against it* (`SCREENS.selfcheck`).

She rates her own draft band by band, sees a predicted range (sum of the band
lows to the sum of the band highs — the rubric's own arithmetic, not ours), and
saves a `selfcheck` record. A grown-up adds the real score later; the parent
view lists prediction against actual and reports whether she reads her own work
accurately, over-rates it, or is harder on herself than the marker.

Rules that are the point, not the decoration:

- **The app never evaluates her writing.** It has no opinion about her essay and
  must not acquire one. She does the judging; the rubric is the only authority.
  This is what keeps the feature on the right side of doing her homework.
- **"What would move this up" quotes the next band verbatim**, in the teacher's
  words. It never proposes sentences — that would be writing the essay for her.
- **No model call, no API key, offline.** Nothing is sent anywhere.
- **It is the readiness check, applied to essays.** Same metacognitive payload
  as `calibrationPairs()`: the gap between predicted and actual is the product,
  not either number alone. Keep the copy pointed at the gap.
- `selfcheck` is in `PROGRESS_TYPES`, so Fresh start clears it.

Wayfinder ships the whole engine with an empty `SHEETS`, so the button appears
only once a teacher issues River a rubric.

### The Today strip (v51 / Wayfinder v43, both apps)

Three tiles under the day header, each a live number that is really a **door**:
Growth (count due → Growth Zone; when nothing is due, the study plan's top
subject and its minutes → that subject), Reading (minutes this calendar month
→ the reading log), Level (level + XP → Stars).

This bends the old "Today is not a dashboard" rule deliberately, and the
distinction is load-bearing: **stats as navigation, not as scorekeeping.**
Every tile must lead somewhere she can act. If a tile is ever added that only
displays a number, it belongs on Stars instead. The affirmation and streak
stay off Today.

Events in "Coming up" may carry `classId` (Mini-Comps do) or `screen` (the
club registration does); either makes the row tappable. Tests are tappable via
their own `classId`.

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
- **A unit may carry `order`** (v85 / Wayfinder v67) — absent means 0, so
  numbered lessons keep sorting by title (`numeric:true`, so 1-10 lands after
  1-9) and anything tagged falls in behind them. It exists because
  end-of-topic material does not alphabetise into the order the work is done:
  a *Rescue Round* would sort ahead of the *Study Guide* it responds to, and a
  *Topic Review* ahead of both. Content-only knob; every derived thing on the
  shelf is untouched, and a book with no `order` anywhere sorts exactly as it
  did before.
- Spines are a **solid colour** — the series' `SUBJECT_PALETTE` deep (`g2`)
  darkened 15% in `spineEl()`, picked by a stable hash of the series name.
  White labels measure ≥5.3:1 across all twelve. Subject texture on spines
  was tried and rejected as visual noise (Chris, 2026-08) — don't reapply
  `paint()` to them.
- `SCREENS.shelf` is the book's table of contents: one row per lesson, the
  bookmarked (or tapped) lesson expanded as the full `unitCard()`. Rows show
  coverage ("7/15 seen"), never accuracy.

### Mode tiles (v68 / Wayfinder v56, both apps)

The three doors into a unit — Flashcards, Quiz, Beat the clock — are drawn
rather than labelled: a fanned card stack, a marked answer sheet, and a
stopwatch whose hand actually sweeps (`.mhand`, `no-preference` only). Inline
SVG via `createElementNS` (`modeSVG`/`modeTile`), coloured through
`currentColor` = `--ac-fg`, so every subject tints its own set. Two rules:
`background-color` only (shorthand wipes pattern layers), and **text colour is
inherited, never `var(--ink)`** — `--ink` is the page canvas in these apps,
and painting text with it renders invisible labels in light mode (caught by
screenshot, 2026-08-09). Book units still get no clock tile.

### The batch of nine (v39 / Wayfinder v34, both apps)

- **Pick up the thread** (`threadTarget()`): the one-tap resume card at the top
  of Study — due reviews always win, else the most recently touched unfinished
  lesson (straight into a quiz), else the top of the study plan.
- **Home-screen shortcuts**: `manifest.json` `shortcuts` land with a hash
  (`#thread`/`#growth`/`#focus`) consumed once at boot.
- **Suggested tests** (`SUGGESTED_ASSESS`): newsletter-announced tests offered
  in the parent view as one-tap adds. Accepting writes a normal `assess` with
  id `assess_<sug id>`; dismissing tombstones the same id. The suggestion list
  lives in code; the records stay the family's.
- **Shuffle rounds** (`buildShuffleUnit()`, `__shuffle__`): one round of the
  least-practised questions across ALL of a subject's units — interleaving.
  Synthetic like `__review__`, never stored. Question ids are namespaced
  (`unit~q`); `_srcUnit/_srcClass/_srcQid` carry the real identity so qstats,
  misses and ladder promotion land on the original unit. Launches without the
  check-in (habit loop, like review) and is always untimed (`book:true`).
- **Read-aloud** (`say()`): browser SpeechSynthesis on flashcard terms —
  offline, tap-only, never automatic.
- **`kind:'spell'`** questions: type-the-word; the word is `opts[ans]`
  (usually `opts:[word], ans:0` — the 4-option rule is an MC rule). −3 is the
  wrong-spelling sentinel. Excluded from timed rounds. Hand-written content
  only; `generateUnit()`'s 4-option guard drops them from AI output by design.
- **Seasonal sky**: a sky-picker option that resolves to one of the app's real
  skies by the Arizona month (`seasonalSky()`), so it stays wash-only and every
  contrast measurement holds. Mappings are per-app identity.
- **Gilt spines**: a finished book's spine title turns `#f8e7b4`. State, never
  currency.
- **Mission Control**: a parent-view card that fetches the sibling app's gist
  read-only (`SIB_FILE`, per-device `sib_gist` in localStorage, the Setup
  token) and summarizes week minutes, 7-day accuracy, Growth Zone due, drafts
  and the next test. Never merged, never written back — keep it that way.

### The visual pass + reading log (v40 / Wayfinder v35, both apps)

- **Living sky** (`.skyfx`): ambient twinkle plus a rare shooting star
  (Wayfinder) or aurora shimmer (Ad Astra). Dark mode only, hidden under
  `prefers-reduced-motion`, sits behind `#app` (z-index 0 vs 1).
- **Motion**: screens compose in with a 30ms stagger, presses compress 2%,
  bars glide. All inside a `no-preference` media query.
- **Hero moments**: thread card gets `.hero`; modal titles render in Fraunces.
- **Quiz constellation** (`.qstars`): the round bar is now one ✦ per question —
  gold right, dim-but-lit miss (showing up counts; Sky Map rules).
- **Crest rings** on subject headers; **✦ divider motif**; **illustrated empty
  states** (`emptyScene()`, static markup only).
- **Reading log** (`SCREENS.reading`): title + minutes stored as ordinary log
  records — `mode:'read'` (xp = minutes) and `mode:'readfin'` (+50, once per
  title). XP, streak, sky map and weekly minutes derive for free; Fresh start
  clears it. Books render as spines coloured by title hash; finished = gilt.
  **No prize economy on the student side, ever** — real-world celebrations live
  in Mission Control's family-week line (both girls ≥5 active days), parent
  view only, framed as a surprise, never a payout. Do not surface rewards to
  the girls.

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

### Grades as points, not percentages (v84 / Wayfinder v66, both apps)

An `assess` record now carries **`points`** and **`outOf`** alongside `score`.
Teachers award points — 42 out of 50, not 84% — and making a parent do that
division in their head to type one number threw away the form the grade
actually arrived in. The rubric self-check was already out of `rub.total`;
this brings test and quiz entry in line with it.

- **`score` stays, and stays the derived percentage** (`assessPct()`), so
  every existing reader — study plan, the horizon, the charts — is untouched
  and needs no migration. Purely additive: a record written before this has
  no `points`, and `assessLabel()` falls back to the percentage alone.
- **`outOf` defaults to 100**, so a parent who only knows "84%" enters it
  exactly as before.
- **The percentage is NOT clamped at 100.** Extra credit is real, and
  silently turning 52/50 into 100% would be the app editing the grade.
- `assessLabel()` prints `42/50 · 84%`, but just `84%` when the total is the
  default hundred — a fraction that says nothing the percentage doesn't is
  noise.
- The modal echoes the conversion live as you type, so it is visible rather
  than taken on trust.
- Fixed alongside: `studyPlan()` tested `!a.score` for "not marked yet", so a
  test she scored **zero** on kept driving the plan as though it were still
  upcoming. Now `a.score == null`.

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
