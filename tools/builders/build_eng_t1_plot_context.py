# Sedona's English Test 1, parts 1 and 2 — built from her own handwritten unit
# notes ("English - Test 1.pdf", Drive, 2026-09-23).
#
# The pages were read by RENDERING them with pypdfium2, not through Drive's
# OCR. Drive does produce a text layer for this file, and most of it is right,
# but it mis-assigned list items in two places that matter: it filed "Style &
# voice" under "Tone is NOT" (it belongs to "why use tone"), and it scrambled
# the five context-clue steps out of order. The rendered page is the source of
# truth for anything in a list.
#
# Every graded question uses a FRESH example. Her notes' own examples live on
# the CARDS, where they are the reference she is revising from — the standalone
# rule (the notes are her homework; this app is extra).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

SRC = 'English Test 1 notes (Drive, 2026-09-23)'


# ─────────────────────────────────────────────────────────────── 1 · Plot Diagram
def plot():
    C, Q = [], []

    card(C, 'Plot diagram',
         "**A graphic organizer that splits a story into five separate parts.**"
         "\n• Exposition, rising action, climax, falling action, resolution."
         "\n• Drawn as a mountain — the climax is the peak.",
         hint='Five parts, one peak.')
    card(C, 'Exposition',
         "**The foundation the story is built on.**"
         "\n• Includes characters, setting and world-building."
         "\n• This is the “before” — the trouble has not taken hold yet.",
         hint='Ex-position = the position everything starts from.')
    card(C, 'Show, don’t tell',
         "**Instead of SAYING a character is brave, SHOW them being brave.**"
         "\n• A named trait is a claim; an action is evidence."
         "\n• An exposition technique.",
         hint='A claim tells. A scene shows.')
    card(C, 'Integrate details',
         "**Reveal information through dialogue, action or description.**"
         "\n• The opposite is stopping the story to explain."
         "\n• This is about HOW the information arrives.",
         hint='Woven in, not pasted on.')
    card(C, 'Pace yourself',
         "**Don’t explain everything at once — introduce details as they become necessary.**"
         "\n• This is about WHEN the information arrives."
         "\n• Everything at once is a briefing, not a beginning.",
         hint='As needed, not all at once.')
    card(C, 'Rising action',
         "**Sets the stage and is where the story begins to move forward.**"
         "\n• Everything between the setup and the turning point.",
         hint='The long climb up to the peak.')
    card(C, 'Rising action · builds tension',
         "**Raises the stakes, starting from a small problem and growing it into a big one.**"
         "\n• Small → large is the test: if the trouble never grows, it is not rising.",
         hint='Small problem, bigger problem, biggest problem.')
    card(C, 'Rising action · develops character',
         "**True nature is revealed by what a character DOES.**"
         "\n• Not by what the narrator calls them.",
         hint='Actions, not labels.')
    card(C, 'Rising action · justifies the climax',
         "**Without compelling rising action, the climax feels unreal.**"
         "\n• The turning point has to be EARNED by what came before it.",
         hint='An unearned peak reads as unreal.')
    card(C, 'Climax',
         "**The most intense or crucial part of the story — the turning point.**"
         "\n• Only ONE moment turns the story; every other tense beat is rising action."
         "\n• Tense is not the test. Turning is the test.",
         hint='The one beat the story cannot go back from.')
    card(C, 'Falling action',
         "**When the intense tension begins to dissipate and the story wraps up.**"
         "\n• Starts the moment the turning point is behind you.",
         hint='Coming down the far side of the mountain.')
    card(C, 'The two purposes of falling action',
         "**It lets the audience process the climax, and it transitions the story smoothly toward the conclusion.**"
         "\n• Cut it and the ending arrives before the reader has caught up.",
         hint='Process, then transition.')
    card(C, 'What falling action shows',
         "**The immediate consequences of what happened.**"
         "\n• Does the setting change?"
         "\n• How are the other characters reacting?"
         "\n• It sets up the new normal.",
         hint='Consequences, reactions, new normal.')
    card(C, 'Resolution',
         "**Ties up the significant threads.**"
         "\n• Significant ones — not every thread in the book.",
         hint='The knots that mattered get tied.')

    # ── questions ──
    q(Q, 1,
      'Put these four moments from one story in the order a plot diagram would place them.',
      ['Nadia is the only eighth grader on a robotics team that has never won a match',
       'The team’s sensor fails at three straight practices and nobody will say whose code broke it',
       'At the regional final Nadia tells the judges the bug was hers',
       'The team keeps her on as lead programmer for next season'],
      0, 'Which one could you read first and still understand nothing has gone wrong yet?',
      ['The setup comes first: who she is and where she is, before any trouble.',
       'Then the trouble grows — a fault nobody will own is a problem getting bigger.',
       'The turning point is the moment she does the thing that changes everything.',
       'What the team decides afterwards is the new normal, so it lands last.'],
      '**Exposition, rising action, climax, resolution.** A plot diagram is a shape, and the shape '
      'is the order: set it up, wind it up, turn it, settle it.',
      'When you are unsure which beat is the climax, ask which one the story could not undo.',
      kind='order')

    q(Q, 1,
      'Which part of a plot diagram introduces the characters, the setting and the world, before the trouble has taken hold?',
      ['Exposition', 'Rising action', 'Falling action', 'Resolution'], 0,
      'It is the part the rest is built on top of.',
      ['Ask what job the part does, not where it sits.',
       'Characters, setting and world-building are all setup, not movement.',
       'Setup is the foundation the story is built on.',
       'That is the exposition.'],
      '**Exposition.** It is named the foundation for a reason — it carries the weight of everything '
      'after it, and it is the only part where nothing has gone wrong yet.',
      'Rising action can still introduce a character, but its job is to move the story, not to set it up.')

    q(Q, 2,
      'A novel has four scenes so tense you hold your breath. Only one of them changes the direction of the story for good. On a plot diagram, what are the other three?',
      ['Rising action', 'Climax', 'Falling action', 'Exposition'], 0,
      'How many turning points does one story get?',
      ['A story has exactly one climax.',
       'So three of those four tense scenes are not it.',
       'Everything tense before the turning point is the climb toward it.',
       'That climb is the rising action.'],
      '**Rising action.** Being tense is not what makes a beat the climax — TURNING the story is. '
      'Three tense scenes that leave the story pointing the same way are the climb, not the peak.',
      'This is the single commonest mix-up in the whole topic: intensity feels like a climax, but only one beat is one.')

    q(Q, 2,
      'A writer wants the reader to understand that Marcus is anxious. Which sentence SHOWS it rather than telling it?',
      ['Marcus checked the lock, walked to the car, then came back and checked it again',
       'Marcus was the most anxious person in his entire family',
       'Marcus felt a familiar and quite overwhelming anxiety about the front door',
       'Marcus had been an anxious child and was now an even more anxious adult'], 0,
      'One of these would still work with the word “anxious” deleted from the language.',
      ['Telling names the trait outright.',
       'Showing gives you an action and lets you draw the conclusion.',
       'Three of these hand you the word “anxious” and ask you to believe it.',
       'Only the double-check at the lock makes you work it out — that is showing.'],
      '**Checking the lock twice.** The reader concludes “anxious” for themselves, which is what '
      'makes it stick. A named trait is a claim; an action is evidence.',
      'A quick test: cross out the trait word. If the sentence dies, it was telling.')

    q(Q, 2,
      'A writer needs the reader to learn that the narrator’s mother is a nurse. Which handling follows “integrate details”?',
      ['Her mother came in still wearing scrubs and asked who wanted the last orange',
       'Her mother was a nurse at the county hospital and had been for eleven years',
       'It is important to know that her mother worked in medicine',
       'Chapter Two: The Nurse'], 0,
      'Integrating means the fact arrives while something else is happening.',
      ['Integrating details means the information rides along on dialogue, action or description.',
       'A sentence that stops to state a fact is the opposite of integrating it.',
       'So is a narrator announcing what the reader should notice, or a chapter title doing the work.',
       'The scrubs arrive inside a scene that was happening anyway.'],
      '**The scrubs and the orange.** The fact is carried by an action the story wanted regardless, so '
      'nothing pauses to deliver it.',
      'Integrate is about HOW a fact arrives. Pace yourself is about WHEN. Keep those two apart.')

    q(Q, 2,
      'Two writers each need the reader to learn the same ten facts about a town. Which choice follows “pace yourself”?',
      ['Release each fact at the point the story first needs it',
       'Put all ten in the opening chapter so nothing is confusing later',
       'Hold all ten back for the final chapter as a surprise',
       'Restate all ten at the start of every chapter'], 0,
      'The rule is about timing, and its test is necessity.',
      ['Pacing means introducing details as they become NECESSARY.',
       'All ten up front is exactly the “everything at once” the rule warns against.',
       'All ten at the end withholds what the story needed earlier, which is the same error reversed.',
       'Releasing each fact where the story first needs it is the rule itself.'],
      '**Release each fact where the story first needs it.** A reader remembers a detail they were '
      'given a reason to care about, and forgets one handed over before it mattered.',
      'Front-loading feels thorough while you are writing it and reads as a lecture afterwards.')

    q(Q, 2,
      'In the middle of a novel, a disagreement over a borrowed bike grows until two families have stopped speaking. Which job of the rising action is that?',
      ['Building tension', 'Developing character', 'Justifying the climax', 'Tying up threads'], 0,
      'Look at the size of the problem at the start and at the end.',
      ['Name what actually changed across the passage.',
       'The problem itself got bigger: one bike, then two households.',
       'Growing a small problem into a big one is the definition of building tension.',
       'So this is tension-building.'],
      '**Building tension.** The test is escalation — the stakes are higher at the end of the passage '
      'than at the start. A problem that stays the same size is not rising.',
      'The three jobs do overlap in real stories. Ask which one the passage is MOSTLY doing.')

    q(Q, 3,
      'A reader finishes a novel and says the final confrontation felt like it came out of nowhere. Which job did the rising action most likely fail at?',
      ['Justifying the climax — the turning point was never built up to',
       'Tying up the significant threads at the end of the book',
       'Introducing the setting and the world in the first chapter',
       'Letting the reader process the confrontation afterwards'], 0,
      'The complaint is about what was missing BEFORE the big moment.',
      ['Locate the complaint in time: the reader is objecting to the climax feeling unearned.',
       'Tying up threads and letting the reader process both happen after the climax, so neither is the cause.',
       'Introducing the setting is exposition’s job, not the rising action’s.',
       'That leaves the job of justifying the climax — building enough that the turn feels real.'],
      '**Justifying the climax.** Your notes put it exactly: without compelling rising action, the climax '
      'feels unreal. “Out of nowhere” is a reader describing a peak that was never climbed to.',
      'A climax is only as believable as the middle of the book makes it.')

    q(Q, 2,
      'The morning after the warehouse fire, neighbours stand in the road working out who will take which family in. Which part of the plot diagram is this?',
      ['Falling action', 'Climax', 'Rising action', 'Exposition'], 0,
      'The big event is over — this is the world reacting to it.',
      ['Ask whether the intense moment is ahead or behind.',
       'The fire has already happened, so the peak is behind us.',
       'Working out who sleeps where shows the immediate consequences and starts a new normal.',
       'Showing consequences and settling into a new normal is falling action.'],
      '**Falling action.** It shows the immediate consequences, how other characters are reacting, and '
      'the shape of the new normal — all three of the things falling action is for.',
      'Falling action is not filler. Without it the ending arrives before the reader has caught up.')

    q(Q, 1,
      'Which part of a plot diagram ties up the significant threads?',
      ['Resolution', 'Falling action', 'Climax', 'Rising action'], 0,
      'It is the last of the five.',
      ['Work from the end backwards.',
       'The final part of the diagram is where the story finishes its business.',
       'Finishing that business is tying up the threads that mattered.',
       'That is the resolution.'],
      '**Resolution.** Note the word SIGNIFICANT — a resolution ties up the threads that mattered, not '
      'every thread the book ever started.',
      'Falling action lowers the tension; the resolution closes the story out.')

    q(Q, 3,
      'Falling action has two primary purposes. Which pair names them?',
      ['Let the audience process the climax, and transition the story smoothly toward the conclusion',
       'Introduce the remaining characters, and establish the rules of the world',
       'Raise the stakes steadily, and reveal each character’s true nature through what they do',
       'State the theme outright, and tell the reader what to feel about it'], 0,
      'Both purposes are about the reader, just after the biggest moment.',
      ['Falling action sits between the peak and the ending, so its purposes face both ways.',
       'Looking back: the reader needs a moment to take in what just happened.',
       'Looking forward: the story has to get to its conclusion without lurching.',
       'Processing and transitioning are the two.'],
      '**Processing and transitioning.** Introducing the world is exposition and raising the stakes is '
      'rising action — both belong on the far side of the climax from this one.',
      'If a film ends two seconds after the explosion, this is the part it skipped.')

    q(Q, 2,
      'Which detail belongs in the exposition of a story rather than anywhere else?',
      ['The narrator lives above her aunt’s laundrette and has done since she was six',
       'The narrator finally tells her aunt what she overheard',
       'The laundrette’s takings have gone missing three weeks running',
       'The narrator and her aunt reopen the shop together in the spring'], 0,
      'Only one of these is true before anything goes wrong.',
      ['Exposition is the setup: who, where, and the ordinary state of things.',
       'A confrontation is a turning point and missing takings are trouble growing.',
       'Reopening in the spring is a new normal, which comes after everything.',
       'Living above the laundrette is the ordinary state of things.'],
      '**Living above the laundrette.** It is a standing fact about her world, true before the story’s '
      'trouble starts — which is exactly what exposition carries.',
      'Ask of any detail: could this be true on page one with nothing wrong yet?')

    q(Q, 3,
      'Why does the plot diagram call the exposition the “foundation” rather than just the beginning?',
      ['Because everything later stands on it — stakes only matter if you know what is at risk',
       'Because it is always the longest section, and length is what makes it matter',
       'Because it is the only part of the diagram allowed to contain description',
       'Because a reader who skips it can still follow the plot perfectly well'], 0,
      'Think about what breaks later if the setup is thin.',
      ['A foundation is about load, not order — it is what the rest rests on.',
       'Length is not the point; plenty of stories open in a page.',
       'Description turns up everywhere, so that cannot be it.',
       'What makes it load-bearing is that stakes need something established to threaten.'],
      '**Everything later stands on it.** You cannot raise the stakes for a reader who does not yet know '
      'what there is to lose — which is why a thin setup shows up as a flat middle.',
      'Weak exposition rarely feels like an exposition problem. It feels like a boring rising action.')

    q(Q, 2,
      'A character everybody in the book describes as dependable is shown, over several chapters, quietly breaking three promises. Which job of the rising action is the writer leaning on hardest?',
      ['Developing character — true nature is revealed by what they DO',
       'Building tension — growing a small problem into a large one',
       'Justifying the climax — earning the turning point in advance',
       'Setting the scene — naming the time and place'], 0,
      'Notice the gap between what people SAY about him and what he DOES.',
      ['The passage sets a label against a pattern of actions.',
       'Your notes are explicit: true nature is revealed by what a character does.',
       'The actions here are contradicting the label everyone uses.',
       'That is character development doing its job.'],
      '**Developing character.** The writer has put a stated trait and a demonstrated one side by side, '
      'and the demonstrated one wins. That gap IS the characterisation.',
      'When a label and an action disagree in a novel, believe the action.')

    q(Q, 1,
      'On the plot diagram drawn as a mountain, which part is the peak?',
      ['The climax', 'The exposition', 'The falling action', 'The resolution'], 0,
      'The shape is doing the explaining.',
      ['The diagram climbs, peaks and descends.',
       'The climb is the rising action and the descent is the falling action.',
       'So the point where the climb becomes the descent is the peak.',
       'That point is the climax.'],
      '**The climax.** The picture is the definition: everything before it goes up, everything after it '
      'comes down, and the turn happens exactly once.',
      'If you can draw the mountain you can usually reconstruct the five parts from it.')

    q(Q, 3,
      'A story shows, right after its turning point, that the corner shop has reopened under a new name and the neighbours now cross the road to avoid each other. What is that doing?',
      ['Showing the immediate consequences — the setting and the relationships both changed',
       'Building tension by growing one small problem into a much larger one',
       'Introducing the world and its people before any of the trouble starts',
       'Tying up every single thread the story has left open anywhere'], 0,
      'Two things have changed, and the change is the point.',
      ['Locate it: right after the turning point puts us in the falling action.',
       'Falling action shows what the climax cost — has the setting changed, how are people reacting?',
       'A renamed shop is a changed setting; crossing the road is a changed relationship.',
       'So it is showing the immediate consequences.'],
      '**Showing the immediate consequences.** Your notes list exactly these two questions — does the '
      'setting change, and how are other characters reacting — as what falling action puts on the page.',
      'Consequences are how a reader learns the climax actually mattered.')

    build('ad-astra', C, Q, 'unit-eng-t1-plot',
          'Test 1 · 1 Plot Diagram', 'english',
          'The five parts of a plot diagram and the craft techniques that go with them, from your '
          'Test 1 notes: exposition (show don’t tell, integrate details, pace yourself), rising action '
          'and its three jobs, the climax, falling action and its two purposes, and the resolution.',
          'Almost every question about a story’s structure reduces to naming which of five parts a '
          'moment belongs to. The one that actually costs marks is telling a tense rising-action beat '
          'from the climax, so that distinction gets the most room here.',
          [('Name all five parts of a plot diagram in order', 'source'),
           ('Place a moment from an unfamiliar story into the right part', 'added'),
           ('Tell the climax from a merely tense rising-action beat', 'added'),
           ('Say what show-don’t-tell, integrate details and pace yourself each ask for', 'source'),
           ('State the three jobs of rising action and the two purposes of falling action', 'source')],
          'Built from Sedona’s own handwritten notes, so the definitions are her class’s, not ours. '
          'Two things worth knowing. Her notes’ examples stayed on the flashcards and every graded '
          'question uses a fresh story instead, so she cannot answer from memory of the page. And the '
          'distinction the questions push hardest — a tense beat is not automatically the climax, only '
          'the beat that TURNS the story is — is not stated that bluntly in the notes; it is the reliable '
          'way to answer the identification questions a test asks.',
          ('Say the five parts out loud in order before you flip a single card.', 14),
          'content/eng-t1-plot.json', SRC,
          'Test 1 notes · Plot Diagram (student’s own notes)',
          prep_=True, libv_=1)


# ─────────────────────────────────────────── 2 · Context Clues and Inferences
def context():
    C, Q = [], []

    card(C, 'Context clues',
         "**Hints inside a sentence or paragraph that help you work out an unfamiliar word.**"
         "\n• The sentence does the defining — you do not need the dictionary.",
         hint='The neighbours of a word tell you about it.')
    card(C, 'Synonym / restatement clue',
         "**The author provides a similar word or phrase that means the same thing.**"
         "\n• Often arrives after a comma, a dash, or the word “or”.",
         hint='Said twice, second time easier.')
    card(C, 'Antonym / contrast clue',
         "**The author uses a word or phrase with the OPPOSITE meaning.**"
         "\n• Signposted by but, unlike, however, instead, while."
         "\n• You learn the word by learning what it is NOT.",
         hint='The clue is the opposite, so flip it.')
    card(C, 'Cause and effect clue',
         "**The author explains the reason FOR the word, or the RESULT of it.**"
         "\n• Signposted by because, so, therefore, as a result, which meant.",
         hint='Why it happened, or what it caused.')
    card(C, 'The five steps, in order',
         "**Read the sentence → look for clues → make an educated guess → substitute and check → confirm.**"
         "\n• Reading the whole sentence first is a step, not a warm-up.",
         hint='Read, look, guess, substitute, confirm.')
    card(C, 'Substitute and check',
         "**Put your guess in place of the word and re-read the sentence.**"
         "\n• If it stops making sense, the guess was wrong — and you have found that out for free."
         "\n• This is the step people skip, and it is the one that catches mistakes.",
         hint='Swap it in and listen.')
    card(C, 'Inference',
         "**Using textual evidence AND your background knowledge to understand something the author "
         "doesn’t state.**"
         "\n• Both halves are required — evidence alone is quoting, knowledge alone is guessing.",
         hint='What the page shows plus what you already know.')
    card(C, 'Making an inference, in order',
         "**Find evidence → activate prior knowledge → put it together → articulate your thinking.**",
         hint='Evidence, knowledge, combine, explain.')
    card(C, 'Find evidence',
         "**Point at the actual words on the page.**"
         "\n• If you cannot quote anything, you are not inferring yet.",
         hint='Put your finger on the line.')
    card(C, 'Activate prior knowledge',
         "**Bring in what you already know about how the world works.**"
         "\n• This is the half that lets you get past what is literally printed.",
         hint='What you brought with you.')
    card(C, 'Articulate your thinking',
         "**Say HOW you got there, not just what you concluded.**"
         "\n• An inference you cannot explain is a guess wearing a better coat.",
         hint='Show the working.')
    card(C, 'Context clue vs. inference',
         "**A context clue works out a WORD. An inference works out an unstated IDEA.**"
         "\n• Both start from evidence in the text; they aim at different targets."
         "\n• Only an inference brings in what you already know from outside the book.",
         hint='One decodes a word, one decodes a meaning.',
         frm='added')

    # ── questions ──
    q(Q, 2,
      'Read the sentence. “Most of the cast was gregarious, but Dev preferred to eat lunch alone in the '
      'costume room.” Which kind of context clue is at work?',
      ['Antonym and contrast', 'Synonym and restatement', 'Cause and effect',
       'No clue is present in the sentence'], 0,
      'One small word in the middle is doing all the work.',
      ['Find the signpost word: “but”.',
       '“But” sets what follows AGAINST what came before.',
       'So eating alone is the opposite of gregarious, not a restatement of it.',
       'A clue built on an opposite is an antonym and contrast clue.'],
      '**Antonym and contrast.** The sentence never says what gregarious means — it shows you its '
      'opposite and lets you flip it. Gregarious turns out to mean sociable, fond of company.',
      'But, unlike, however, instead, while — each of those is a contrast clue announcing itself.')

    q(Q, 2,
      'Read the sentence. “Because the iron bridge had corroded through forty wet winters, the county '
      'closed it to lorries.” Which kind of context clue is at work?',
      ['Cause and effect', 'Antonym and contrast', 'Synonym and restatement',
       'No clue is present in the sentence'], 0,
      'The sentence tells you what the word LED TO.',
      ['Find the signpost: the sentence opens with “because”.',
       'That sets up a reason and a result.',
       'Corroding is the reason; closing the bridge to lorries is the result.',
       'A clue built from a reason or a result is a cause and effect clue.'],
      '**Cause and effect.** You learn what corroded means from its consequence: whatever happened to '
      'that iron over forty wet winters made it unsafe to drive on. It means eaten away by rust.',
      'Because, so, therefore, as a result, which meant — all of them announce a cause-and-effect clue.')

    q(Q, 2,
      'Read the sentence. “The coach was adamant — completely unwilling to be talked round — that nobody '
      'would skip the warm-up.” Which kind of context clue is at work?',
      ['Synonym and restatement', 'Cause and effect', 'Antonym and contrast',
       'No clue is present in the sentence'], 0,
      'Look at what sits between the two dashes.',
      ['The dashes hold a phrase that interrupts the sentence.',
       'That phrase says the same thing again in easier words.',
       'Saying it again in different words is restating it, not contrasting or explaining a result.',
       'So this is a synonym and restatement clue.'],
      '**Synonym and restatement.** The author defines adamant in place, inside a pair of dashes — it '
      'means immovable, refusing to change your mind.',
      'A comma, a pair of dashes, or the word “or” often carries a restatement clue right behind it.')

    q(Q, 2,
      'In the sentence “The negotiator remained impassive while both sides shouted across the table,” '
      'what does IMPASSIVE most likely mean?',
      ['Showing no emotion', 'Extremely loud', 'Easily offended', 'Unable to attend'], 0,
      'Set the word against what everyone else in the sentence is doing.',
      ['Read the whole sentence before deciding anything.',
       'The clue is the contrast: both sides are shouting, and the negotiator REMAINED something.',
       'Remaining, while others shout, points at staying outwardly unmoved.',
       'Substitute it in: the negotiator remained showing no emotion while both sides shouted. It holds.'],
      '**Showing no emotion.** “While” sets the negotiator against the shouting, so the word has to '
      'mean something opposite to it — and substituting the guess back in keeps the sentence sensible.',
      'Every option here is a real word about people, so you cannot eliminate on shape. You have to use the clue.')

    q(Q, 1,
      'In the five steps for using context clues, which step comes immediately AFTER making an educated guess?',
      ['Substitute and check', 'Read the sentence', 'Look for clues', 'Confirm'], 0,
      'A guess is not the end of the process.',
      ['The five steps run: read the sentence, look for clues, make an educated guess, then two more.',
       'Reading and looking both come before the guess, so neither can follow it.',
       'Confirming is the last step, so something sits between.',
       'That something is substituting the guess in and checking it.'],
      '**Substitute and check.** It is the step that turns a guess into an answer — and it is the one '
      'most often skipped, which is exactly why it catches so many wrong guesses.',
      'Guess, swap it in, re-read. If the sentence goes strange, you have saved yourself a wrong answer.')

    q(Q, 3,
      'Why is “substitute and check” worth doing even when you feel confident about your guess?',
      ['It tests the guess against the whole sentence, which is where a wrong guess falls apart',
       'It is the only step in the list that requires you to read the sentence at all',
       'It replaces the need to look for any clues in the sentence in the first place',
       'It guarantees the word has only one possible meaning'], 0,
      'Think about what a wrong guess does to the sentence around it.',
      ['A guess is formed from a clue, which is usually part of the sentence.',
       'Substituting puts that guess back against ALL of the sentence.',
       'A guess that fits the clue but breaks the rest of the sentence is exposed by that.',
       'So the step is a check on the guess, using the sentence as the judge.'],
      '**It tests the guess against the whole sentence.** Confidence is not evidence. A wrong guess '
      'usually sounds fine on its own and only goes strange once it is back in place.',
      'The step costs about four seconds and is the cheapest way to catch yourself being wrong.')

    q(Q, 1,
      'Put the four steps of making an inference in order.',
      ['Find evidence', 'Activate prior knowledge', 'Put it together', 'Articulate your thinking'], 0,
      'You cannot combine two things before you have both of them.',
      ['An inference needs evidence from the page, so that is collected first.',
       'Then you bring in what you already know from outside the book.',
       'Only once you hold both can you put them together.',
       'Explaining how you got there comes last — it is the step that proves it was not a guess.'],
      '**Evidence, prior knowledge, put it together, articulate.** The order matters: the last step is '
      'what separates an inference from a hunch, and it only exists because the first three did.',
      'If you ever cannot do step four, go back and check whether you really did step one.',
      kind='order')

    q(Q, 2,
      'Read the passage, then answer.',
      ['She has been waiting a long time and is trying not to show it',
       'She is waiting for a train that has not been announced yet',
       'She dislikes the person she has arranged to meet here',
       'The café is about to close and she has been asked to leave'], 0,
      'Count the cups, then think about what three of them means.',
      ['Find the evidence: three empty cups, a phone face-down, a folded and refolded receipt.',
       'Activate what you know: one person does not drink three coffees in five minutes.',
       'Fiddling with a receipt over and over is what people do to occupy themselves while waiting.',
       'Put it together: a long wait, being managed quietly.'],
      '**She has been waiting a long time and is trying not to show it.** Nothing in the passage says '
      '“waiting” or “impatient” — the three cups measure the time and the refolded receipt shows '
      'the effort of sitting still.',
      'A good inference can always be traced back to specific words. Point at the three cups.')
    Q[-1]['passage'] = ('Three empty cups stood at her elbow. Her phone lay face-down beside them. '
                        'She folded the receipt in half, then in half again, and smoothed it flat.')

    q(Q, 3,
      'A classmate says: “I think the narrator’s family is short of money.” Which response shows they '
      'have actually made an INFERENCE rather than a guess?',
      ['“The coat is his brother’s and nobody buys anything new — hand-me-downs usually mean money is tight”',
       '“It just feels like that sort of book, and I am usually right about these things”',
       '“The back cover of the book says outright that the family is poor”',
       '“My own family was short of money once, so I recognise it when I see it”'], 0,
      'Look for BOTH halves: something quoted, and something known.',
      ['An inference needs textual evidence plus background knowledge.',
       'A feeling about the sort of book has neither.',
       'The back cover is not the text doing the work, it is being told outright.',
       'Personal experience alone is prior knowledge with no evidence attached.',
       'Only the coat answer points at the page AND brings in what hand-me-downs usually mean.'],
      '**The coat answer.** It quotes the page and names the outside knowledge it is using, which is the '
      'whole definition. The others have one half, or neither.',
      'The giveaway is the word “because”, spoken or implied. An inference can always finish that sentence.')

    q(Q, 3,
      'What is the difference between using a context clue and making an inference?',
      ['A context clue works out an unfamiliar WORD; an inference works out an unstated idea',
       'A context clue uses the text and an inference does not use the text at all',
       'A context clue is only ever a guess, while an inference is a certainty',
       'They are two different names for exactly the same reading process'], 0,
      'Ask what each one is aimed AT.',
      ['Both start from evidence in the text, so that cannot be the difference.',
       'Neither is a certainty and neither is a pure guess, so that is not it either.',
       'They are not the same process, or the notes would not separate them.',
       'What differs is the target: one decodes a word, the other decodes an unstated idea.'],
      '**One decodes a word, one decodes an unstated idea.** They share a method — start from what is on '
      'the page — but an inference also brings in what you already know from outside the book.',
      'If the answer could go in a dictionary, it was a context clue. If it could not, it was an inference.')

    q(Q, 2,
      'Read the sentence. “The soup was so insipid that three people at the table reached for the salt '
      'without saying anything.” What does INSIPID mean, and which clue tells you?',
      ['Lacking flavour — a cause and effect clue', 'Extremely spicy — a contrast clue',
       'Served cold — a restatement clue', 'Very expensive — a cause and effect clue'], 0,
      'What did the soup CAUSE three people to do?',
      ['The sentence gives a result: everyone reaches for the salt.',
       'Reaching for salt is what people do when food needs seasoning.',
       'So insipid describes food that needs it — flavourless.',
       'Because the meaning came from a RESULT, the clue is cause and effect.'],
      '**Lacking flavour, from a cause and effect clue.** The word is never restated and never contrasted '
      '— you get it entirely from what it made three people do.',
      'When a sentence shows you a consequence, read backwards from the consequence to the word.')

    q(Q, 1,
      'Which pair of things does an inference require?',
      ['Textual evidence and your background knowledge', 'A dictionary and a highlighter',
       'The author’s own explanation and a summary', 'Two different translations of the same passage'], 0,
      'Your notes name both halves in a single sentence.',
      ['An inference reaches something the author never states outright.',
       'Evidence from the page alone only gets you what IS stated.',
       'Knowledge alone, with nothing quoted, is not reading at all.',
       'So it takes both together.'],
      '**Textual evidence and background knowledge.** Drop the evidence and you are guessing; drop the '
      'knowledge and you are only repeating what is printed.',
      'This is the definition most likely to appear as a fill-in-the-blank. Learn both halves.')

    q(Q, 2,
      'Which sentence contains NO usable context clue for the unfamiliar word?',
      ['The room was redolent, and everyone agreed about it afterwards',
       'The room was redolent — thick with the smell of bay and burnt sugar',
       'The room was redolent, unlike the odourless corridor outside it',
       'The room was so redolent that she could tell what had been cooked before she opened the door'], 0,
      'Three of these give you something to work from. One only reports that people agreed.',
      ['Check each sentence for a restatement, a contrast, or a cause and effect.',
       'One restates redolent as thick with smell; one contrasts it with odourless; one gives a result.',
       'The remaining sentence says only that everyone agreed, which tells you nothing about the word.',
       'Agreement is not a clue — it does not point at a meaning.'],
      '**“Everyone agreed about it afterwards.”** It sounds like it is telling you something, but you '
      'could swap almost any adjective into that sentence and it would read exactly the same.',
      'A clue has to narrow the meaning. If the sentence works with the opposite word too, it is not a clue.')

    q(Q, 3,
      'Read the passage, then answer.',
      ['The dog has been in this house a long time and knows its routines',
       'The dog is unwell and has been waiting to be carried out',
       'Somebody is about to arrive and the dog has heard them coming',
       'The dog has only recently been adopted into this house'], 0,
      'The dog moves before the kettle does anything.',
      ['Find the evidence: the dog leaves the hall BEFORE the kettle clicks.',
       'Activate what you know: an animal only anticipates a sound it has heard many times.',
       'A newly arrived dog would have nothing to anticipate yet.',
       'Put it together: this dog has learned the routine of the house, which takes time.'],
      '**The dog has been there a long time and knows the routines.** The order of events is the whole '
      'inference — moving first means predicting, and predicting means having learned.',
      'When a passage is careful about the ORDER things happen in, the order is usually the evidence.')
    Q[-1]['passage'] = ('The kettle had not clicked yet when the old dog got up, stretched, and padded '
                        'out of the hall towards the kitchen.')

    q(Q, 2,
      'You meet an unfamiliar word in the middle of a long sentence. According to the five steps, what do you do FIRST?',
      ['Read the whole sentence', 'Look for clues around the word',
       'Make an educated guess at the meaning', 'Substitute a likely word and check it'], 0,
      'The first step is the one that is easy to skip because it feels like not-yet-working.',
      ['All four of these are real steps, so the question is only about order.',
       'You cannot look for clues without having read the sentence they are in.',
       'Guessing and substituting both come later still.',
       'So reading the whole sentence is first.'],
      '**Read the whole sentence.** It counts as a step because the clue is often AFTER the word — stop '
      'at the hard word and you have skipped the part that explains it.',
      'Most missed context clues are sitting in the second half of a sentence somebody abandoned halfway.')

    q(Q, 3,
      'The last step of making an inference is to articulate your thinking. Why does that step exist?',
      ['Because an inference you cannot explain cannot be told apart from a guess',
       'Because teachers require every answer to be written in full sentences',
       'Because saying it aloud makes it easier to memorise',
       'Because it is the step where you finally decide what you think'], 0,
      'Think about what the step lets somebody ELSE check.',
      ['The first three steps happen inside your head.',
       'Nobody else — including you, later — can see whether they actually happened.',
       'Articulating exposes the evidence and the reasoning to inspection.',
       'That is what distinguishes an inference from a hunch that happened to be right.'],
      '**An inference you cannot explain is indistinguishable from a guess.** Explaining is not a '
      'formality tacked on the end; it is the proof that the first three steps really happened.',
      'This is also why a right answer with no reasoning often earns partial credit at best.')

    build('ad-astra', C, Q, 'unit-eng-t1-context',
          'Test 1 · 2 Context Clues and Inferences', 'english',
          'The three kinds of context clue (synonym and restatement, antonym and contrast, cause and '
          'effect), the five steps for using them, and what an inference is — evidence from the page '
          'plus background knowledge — with its own four steps.',
          'These two are the reading skills every other English question quietly sits on top of. A '
          'passage question you cannot answer is very often a word you decided to skip.',
          [('Name the three kinds of context clue and spot each one in a sentence', 'source'),
           ('Work out an unfamiliar word from the sentence around it', 'added'),
           ('Give the five steps for using context clues in order', 'source'),
           ('Say what an inference requires, and give its four steps in order', 'source'),
           ('Tell a real inference from a guess', 'added')],
          'Built from Sedona’s own handwritten notes. One thing to flag: Drive’s scan of her '
          'handwriting returned the five context-clue steps in the WRONG order, and the pages had to be '
          'rendered and read as images to get them right. The order taught here — read the sentence, '
          'look for clues, make an educated guess, substitute and check, confirm — is what her page '
          'actually says. If her memory of the order disagrees, her page wins. The questions use fresh '
          'sentences throughout, so none of this can be answered from memory of the notes.',
          ('Two short passages in here ask you to infer something nobody says outright. Take those slowly.', 15),
          'content/eng-t1-context.json', SRC,
          'Test 1 notes · Context Clues and Inferences (student’s own notes)',
          prep_=True, libv_=1)


if __name__ == '__main__':
    plot()
    context()
