# Build a study companion for one kid

**A starter brief.** Everything here is a rule; none of it is our family's.

Drop this file into an empty repository as `CLAUDE.md`, open Claude Code, and
describe your own child — their year, their subjects, what they're finding
hard. Then build it.

Every rule below is either a bug that already happened or a decision made on
purpose. Where it says *never*, something already went wrong.

---

## Start here: the decision everything else follows from

**It is built for one child.** Not a class, not a product. No accounts, no
sign-up, no multi-tenancy, no roles.

That single constraint is what makes everything below affordable. There is no
auth to write, no backend to run, no settings screen for options nobody has.
When a second child needs one, fork the repo and replace the content — do not
add a profile picker. Two apps means two themes and two home-screen icons,
which is better for the kids and only marginally worse for you.

---

## Part one — the shape

### Four files, no build step

`index.html` (the entire app — inline CSS and JS), `manifest.json`, `icon.svg`,
`sw.js`. No npm, no bundler, no framework.

- Deploying is a `git push` to GitHub Pages.
- The whole app is readable in one file, which matters more than it sounds like
  it should when you come back to it in four months.
- When `index.html` approaches ~4,000 lines, split it into separate `.js` files
  loaded with `<script src>` — still no build step.

### The service worker will lie to you

Bump a cache-version constant on **every** deploy, in step with an app version
you show somewhere in the UI. Mobile Chrome caches aggressively, and a stale
worker will serve the old app indefinitely — you will debug a fix that shipped
perfectly.

- **Don't `skipWaiting()` on install.** A new worker taking over mid-session
  mixes old code with new caches. Let it wait, show a dismissible "a new version
  is ready" bar, and take over when they tap Refresh or on the next cold start.
- **Bound every network fetch in the worker.** A hung request for a stylesheet
  blocks every `<script>` after it, and the app simply never finishes loading —
  on a captive-portal wifi this is the whole experience.
- **Self-host your fonts.** Same reason. A typographic identity that arrives
  from a CDN on every cold start isn't yours.

---

## Part two — the data model

### One flat record store

Everything is one object keyed by id. Every record carries `id`, `type` and
`updatedAt`. That is the entire schema.

Typical types: `unit` (study content), `log` (one completed session), `miss` (a
missed question on the review ladder), `cleared`, `qstat` (per-question tally),
`mood`, `assess` (a test or quiz), `badge`, `prefs` (a single record, not a
localStorage key, so preferences follow the child to any device).

### Never store what you can derive

XP, level, streak, accuracy — all computed from the logs at render time.

A derived value cannot drift between two devices, so there is no counter to
reconcile during a merge. The moment you store one, you own a reconciliation
bug forever. Recompute instead.

### Deletes are tombstones

`softDelete(id)` writes `{deleted: true, updatedAt}`. It never removes the key.

Without this, deleting something on one device and syncing from another
resurrects it. Purge tombstones older than ~60 days during the merge.

### Merge per record, newest wins

Fetch the remote copy, merge, then write. Never a blind overwrite. If you change
a record's shape, bump a schema version and add a migration step so older
devices upgrade in place.

### Secrets are not records

API keys, sync tokens, the parent passcode hash: `localStorage` only. Never in
the record store, never in source. Assume the repository is public, because
mine are.

### Sync

One private GitHub Gist (or equivalent), with the id and a narrowly-scoped token
entered once per device. Content a parent writes on a laptop appears on the
child's phone; their progress appears on the parent's.

**The app must be completely usable with sync off.** The load path swallows
network errors by design. Offline-first is not a feature here, it's the default
state.

---

## Part three — time

This gets its own section because it caused the worst bug in the project.

- **Route every date operation through one helper, for one fixed timezone.**
- **Never derive "today" from `toISOString()`.** It rolls over mid-afternoon.
- **Date arithmetic must be pure calendar math** — build the date in UTC and
  slice the ISO string — not a local-midnight `Date` formatted into another
  zone. That version is correct on your own machine and one day short on any
  device further east, which silently compressed *every* spaced-repetition
  interval. It was invisible for weeks.
- If your timezone observes daylight saving, decide how the helper handles it
  deliberately rather than discovering it in March.

---

## Part four — the learning engine

### Rounds, not quizzes

Serve five questions at a time, least-practised first, then longest-unseen. The
round is the unit the child actually experiences: sixteen questions in rounds of
five is four quizzes, and progress should be reported that way.

Don't tune content length around "one sitting" — rounds handle that.

### The review ladder

A missed question does not clear the moment they get it right once. Each miss
carries a box (0–4) and a due date, stepped along widening intervals:

```
box 0 ──1 day──▶ box 1 ──2 days──▶ box 2 ──4 days──▶ box 3 ──8 days──▶ box 4 ──21 days──▶ learned
```

- **Miss it** → box resets to 0, back tomorrow. No partial credit for a near miss.
- **Get it right** → up one box, the gap widens.
- **Right at the top box** → it has survived every interval out to three weeks.
  That is the bar for "learned": write a `cleared` record and tombstone the miss.

Three things about the review round are load-bearing:

- **It is a synthetic unit, assembled at render time and never stored.** It is a
  view, not content — syncing it would mean syncing a snapshot of a moment.
- **Rewrite each question's id to the miss id inside it.** Questions are numbered
  per unit and restart at 1, so a mixed-subject round collides otherwise.
- **Credit the tally to the original unit**, or the parent view attributes the
  work to nothing.

The review round should skip any pre-quiz ritual. It runs most days, and friction
there kills the habit.

### Shuffle the options

Fixed option order means the answer can be learned by position, which is not
knowing the answer.

- Shuffle per question, and key the permutation by question id so revealing a
  hint (which re-renders) doesn't reshuffle the options underneath them
  mid-question.
- Pass the **original** index to the answer handler, so the stored answer, the
  miss record and every explanation downstream are untouched.
- **Consequence for content:** no question may ever say "the first option" or
  "all of the above."
- **One exception:** a unit that transcribes a paper the child is physically
  holding must *not* shuffle. If your C isn't the paper's C, the whole mode is a
  lie.

### Questions already on the ladder sort last

A missed question is already scheduled to return. Letting it also compete for an
ordinary round asks it twice and crowds out questions they have never seen.

Sort it behind everything else rather than excluding it — a short unit, or one
where they've missed everything, still needs questions to serve.

### Timed practice is practice

If you add a beat-the-clock mode, count its sightings **separately**. A question
they have only raced shouldn't move the real progress markers. Give the timed
round its own fixed size rather than inheriting the content's sitting size —
racing twelve questions against a countdown is a different activity from
clearing a lesson.

### Leaving a round part-way

Log what they actually answered — never the full round with the remainder marked
wrong.

- Persist on `visibilitychange` and `pagehide`. On a phone, the commonest way a
  round ends is the app being backgrounded, not a button being pressed.
  (`beforeunload` fires unreliably on mobile; don't rely on it.)
- Keep two guards, not one: the log may be written many times as they come and
  go, but the ladder must settle exactly once.
- **A resumed round has to rebase its clock.** Store elapsed time, not just the
  start, or a round parked at 8am and finished at 6pm logs ten hours of study
  into the week's minutes.

---

## Part five — content rules

These decide whether it teaches anything. Engine bugs are visible; content bugs
are silent, and a child will absorb a badly-built question without ever
mentioning it.

- **Standalone always.** Never reference "the worksheet" or a numbered problem
  from the source material. A question restates all the context it needs. Fresh
  scenarios beat reworded homework — the sheets are the homework; this is extra.

- **Standalone from its siblings, too.** This is the half that gets missed. A
  round serves five of twenty, shuffled, so the question next door is usually
  absent. A stem may not open "The same student…", and an option may not name a
  thing only a neighbouring question introduced.

- **A question may never contain its own answer.** Glossing the term in the stem
  — *"which word means the opposite of accustom (to get used to something)?"* —
  hands over the fact being tested. Asking for a synonym while glossing is worse:
  the gloss usually *is* the answer. Where a word has two senses, disambiguate
  with a part-of-speech tag or a usage sentence. Context, never a definition.

- **Distractors are the other half of that same bug.** Stripping the gloss
  achieves nothing if the wrong options are unrelated filler — they can still
  answer by eliminating on part of speech. Every option should be the same part
  of speech as the answer, and each should hold a *different* real relationship
  to the stem. The strongest distractor is the word's own opposite number: put a
  synonym in an antonym question and they have to read which was actually asked.

- **Lead with the answer, in bold.** A flashcard's definition opens with the
  straightforward answer — one short sentence that works alone — then at most
  two or three supporting bullets.

- **Explanations say why, not what.** "Because the slope is the rate" — not
  "the answer is B."

- **Every question carries its steps.** Three to six strings walking from the
  question to the answer, one concrete move each, the last one stating the
  answer. Offered after a wrong answer and free — it is remediation, not part of
  any hint economy — and only *after* answering, so it teaches rather than leaks.

- **Verify every answer key you're given.** Re-derive each answer independently.
  Real teacher keys contain real misprints; we have found several, and a
  confidently wrong question is worse than no question.

- **Balance the answer positions.** Authoring every correct answer into slot A is
  invisible to you and obvious to the child the first time something doesn't
  shuffle. Rotate deliberately, and write a checker that warns when one slot
  holds most of a unit's answers.

- **Nothing reaches them unread.** Everything ships as a draft for a grown-up to
  approve, and drafts are filtered out everywhere on the child's side. Frame it
  in the UI as catching what the model got wrong — never as checking on them.

- **Give content its own version integer, separate from the timestamp.**
  Approving a unit re-stamps it, so a fix you shipped an hour earlier loses the
  merge and vanishes — and the app cheerfully reports "already in sync," which
  is a lie. An explicit version the author bumps is what makes a content fix
  immune to that race.

---

## Part six — the psychology

These are grounded in research rather than vibes, and the exact wording matters.
Do not warm them up into generic encouragement.

- **Praise process and strategy, never fixed traits.** "You're so smart"
  measurably reduces persistence after failure. Every line of feedback names the
  approach or the showing-up.

- **Nothing breaks.** A short week stays dim and the next one starts fresh. No
  streak to lose, no negative copy anywhere, nothing that says they let something
  slip.

- **No prize economy. Ever.** Cosmetics — themes, avatars, companions — are free
  and flat, never unlockable. The moment identity becomes a reward it becomes a
  grind, which is the exact mechanic this kind of app should refuse. Real-world
  celebrations belong on the parent's side, framed as a surprise, never surfaced
  to the child as a payout.

- **The review list is information, not a verdict.** That framing is
  load-bearing. Don't soften it into praise, and don't let it become a list of
  faults. Correspondingly, don't give the child a self-serve button to delete
  entries from it — a review ladder they can quietly edit down is a mechanic for
  avoiding review. Put that tool on the parent's side, for when the *question*
  was wrong.

- **A self-set goal must stay consequence-free.** One small weekly aim they write
  and tick themselves, tracked by nothing else, dissolving each week. Self-set
  proximal goals beat assigned ones for commitment — and the moment it gains a
  consequence it stops working.

- **The phone never scolds.** A right answer can buzz back softly. A miss gets
  nothing: no buzz, no sound, no penalty.

- **Ask how ready they feel before, and how it went after.** The *gap* between
  what they predicted and what happened is the entire payload — not either number
  on its own. It is the one thing in the app that teaches them to read their own
  preparation. A low mood surfaces a supportive note with explicit permission to
  stop; keep that, and keep the line telling them to talk to someone they trust.

- **Second person everywhere they can see.** "Your school day", not "her school
  day". The app talks *to* them, not *about* them. Third person belongs in
  exactly two places: the parent view and the model prompts.

- **Pitch it up, not down.** Short sentences and ordinary words, but never baby
  talk, never exclamation marks, never "great job!" — a real explanation, said
  plainly. Kids read a condescending tone instantly.

---

## Part seven — the grown-up side

- Behind a passcode, per-device, and deliberately understated in tone so it
  doesn't read as surveillance.

- **No clock times.** *When* they studied is surveillance flavour, not actionable
  signal. Order the sessions; don't timestamp them.

- **At most two things worth a word.** Rank wellbeing first. It describes a
  *session*, never the child. No verdict language. Good news is eligible. Cap it,
  so it can never become a list of faults — and when nothing stands out, say so,
  because an ordinary evening is information too.

- **Show what they got wrong first.** An eighteen-question round rendered as
  eighteen rows buries the handful that matter. Show the misses, always state the
  full count so nothing is hidden silently, and put the rest one tap away.

- **A sandbox flag** — per-device, never a record — that blocks every write, so a
  parent poking around doesn't pollute real statistics. Add this earlier than you
  think you need to.

- **A "fresh start"** that tombstones progress records only, leaving content,
  grades and preferences alone.

---

## Part eight — non-negotiables

Each of these is a past bug, not a preference.

- All DOM via `createElement`/`appendChild`; all events via `addEventListener`.
  Never `innerHTML` with interpolated data, never inline `onclick`.
- Never `alert()`, `confirm()` or `prompt()`.
- 44px minimum tap targets, safe-area insets, no hover-dependent UI. Assume a
  phone in a pocket.
- Bump the cache version on every deploy.
- **Measure the computed style, not the stylesheet.** A rule you can read is not
  a rule that applied — specificity collisions are silent.
- **Every reading colour holds 4.5:1** against every surface it can land on: the
  card, the page, and the tinted wash. Sweep it across your whole palette in both
  themes with a real probe. Do not eyeball it.

---

## Part nine — traps that cost real time

> **The `background` shorthand silently wipes pattern layers** set via
> `background-image`. Use `background-color`, or scope the plain background with
> `:not()`. This one bit twice.

> **Seed shuffles with an avalanche hash (FNV-1a), not a polynomial roll.** A
> polynomial roll adds the same constant for a given salt, so the relative order
> never changes — "a fresh set every day" deals the identical set forever, and it
> looks plausible enough that only a test catches it.

> **An unregistered CSS custom property resolves where it is *declared*,** not
> where it is used. A child element that overrides `--x` still inherits the
> parent's already-computed `var(--y)`. Declare the derived token on every
> element that can carry its own base.

> **A block owns its own bottom margin.** Pairwise `.a + .b` rules only fix the
> adjacency you happened to think of; the third and fourth things that can follow
> it stay flush at zero. Ask what *else* can render there.

> **A test that passes against the bug it was written for is wrong.** Revert the
> fix, watch it fail, then keep it. We shipped a green test over a bug that was
> visible in a screenshot.

> **Trust the rendered PDF over any text extraction** on a multi-column source.
> Render the pages and read them as images; OCR reflow merges one question's stem
> with the next question's options, and you will not notice until it is content.

---

## Part ten — what you supply

None of this is portable, and all of it is the actual work:

- **Your child's timetable and academic calendar**, as constants in code rather
  than records — they're identical on every device, so one deploy updates every
  phone and nobody has to type anything.
- **Their real class material**, as content files. Anchor every card and question
  to the actual source; don't invent facts.
- **Your own theme, palette and voice.** Build it for the one kid who will use
  it, and let them choose the colours.

What you don't have to write is everything above — the record store, the ladder,
the round logic, the draft gate, the merge rules. That's what this file is for.

---

## Working with Claude on it

**Keep a `CLAUDE.md` and write down the *why*.** Every entry should be a bug that
happened or a decision made deliberately, with the reasoning and the date. That
file, not the code, is what makes the fortieth change as careful as the first —
and it is the only reason a brief like this one could be written at all.

**Measure before and after,** and put the number in the note: the gap in pixels,
the contrast ratio, how many times a value was printed on one screen. "It looks
tight" produces a different fix than "these two blocks are 0px apart."

**Keep a real browser-driven test harness in the repository**, not in a chat that
disappears when the session ends.
