# Sedona's English Test 1, parts 3 and 4 — Diction, and Tone and Mood.
#
# Same source and same discipline as build_eng_t1_plot_context.py: her own
# handwritten unit notes, read by RENDERING the pages with pypdfium2 rather
# than trusting Drive's OCR. That mattered again here — the OCR filed
# "Style & voice" under "Tone is NOT", where it would have taught the exact
# opposite of what the page says. It belongs to "why use tone".
#
# Every graded question uses a FRESH example. Her notes' own examples live on
# the CARDS, where they are the reference she is revising from.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

SRC = 'English Test 1 notes (Drive, 2026-09-23)'


# ──────────────────────────────────────────────────────────────────── 3 · Diction
def diction():
    C, Q = [], []

    card(C, 'Diction',
         "**The linguistic choices a writer makes to convey an idea, a point of view or a story.**"
         "\n• The words the author uses to establish style and tone."
         "\n• Everything else in this lesson is a KIND of diction.",
         hint='Diction is which words. Syntax is what order.')
    card(C, 'Formal diction',
         "**Sophisticated language, without contractions or colloquialisms.**"
         "\n• Example: “I will get to this issue right away.”"
         "\n• Used where distance and correctness matter.",
         hint='No contractions, no slang, no shortcuts.')
    card(C, 'Informal diction',
         "**More conversational, and often used in narrative literature.**"
         "\n• Example: “I've got this.”"
         "\n• A contraction is usually the fastest tell.",
         hint='It sounds like a person talking.')
    card(C, 'Pedantic diction',
         "**Highly detailed or academic in writing.**"
         "\n• Example: “In examination of your stance, I have identified some critical errors "
         "that I will now expound on…”"
         "\n• Formal carried further than the occasion asked for.",
         hint='Academic, and a little pleased with itself.')
    card(C, 'Formal or pedantic?',
         "**Formal fits the occasion; pedantic goes further than the occasion needs.**"
         "\n• Both avoid contractions, so that tell settles nothing here."
         "\n• Ask whether the extra vocabulary is doing work or performing.",
         hint='Correct, or showing off?')
    card(C, 'Colloquial diction',
         "**Words or expressions that are informal in nature and generally represent a certain "
         "region or time.**"
         "\n• It adds color and realism to writing."
         "\n• Example: most of the US says “soda”; the North and Midwest say “pop.”",
         hint='It tells you WHERE, or WHEN.')
    card(C, 'Slang diction',
         "**Originated within a specific culture or subgroup, but gained traction.**"
         "\n• Example: “Red is looking pretty sus.”"
         "\n• It tells you which group, not which place.",
         hint='It tells you WHO.')
    card(C, 'Colloquial or slang?',
         "**Colloquial marks a region or an era; slang marks a subgroup and then spreads out of it.**"
         "\n• Both are informal, so “informal” never decides between them."
         "\n• Ask what the word marks: where you are from, or who you run with.",
         hint='A place and a time, or a crowd.')
    card(C, 'Abstract diction',
         "**Uses words to express something intangible, like an idea or an emotion.**"
         "\n• Example: “Hank's love for science does not impair his spiritual beliefs.”"
         "\n• Nothing in it could be photographed.",
         hint='You cannot point at it.')
    card(C, 'Concrete diction',
         "**Uses words for their literal meanings, and refers to things that appeal to the senses.**"
         "\n• Example: “I ate an apple.”"
         "\n• If you could photograph it, taste it or hear it, it is concrete.",
         hint='You could put it in a photograph.')
    card(C, 'Poetic diction',
         "**Driven by lyrical words that relate to a specific theme reflected in a poem, a sound, "
         "and so on.**"
         "\n• Example: “What a foolish and ignorant thing you just said. Hear my rebuttal and your "
         "cheeks will burn red.”"
         "\n• Sound and rhythm are doing work the plain version would not.",
         hint='It would survive being read aloud.')
    card(C, 'Why diction is on the tone list',
         "**Diction is the first of the four routes to an author's tone.**"
         "\n• Change the words and the attitude they carry changes with them."
         "\n• Which is why a diction question and a tone question are often one question.",
         hint='Words carry an attitude whether you meant them to or not.')

    q(Q, 1, 'What does the term diction name?',
      ['The linguistic choices a writer makes',
       'The order words are arranged in a sentence',
       'The emotion a reader is left holding at the end',
       'The attitude an author takes toward a subject'], 0,
      'Three of these have their own names elsewhere in this unit.',
      ['Diction is about WHICH words get chosen.',
       'Word order has its own name — syntax.',
       'The emotion a reader feels is mood; the attitude an author holds is tone.',
       'That leaves the writer’s linguistic choices.'],
      '**Diction is which words a writer picks to convey an idea, a point of view or a story.**'
      ' Syntax, mood and tone are three different things that sit right next to it.',
      'Worth learning the neighbours too — the wrong ones here are the three terms most often swapped for diction.')

    q(Q, 1, 'Which kind of diction avoids contractions and colloquialisms?',
      ['Formal diction', 'Informal diction', 'Slang diction', 'Concrete diction'], 0,
      'Think about which one you would use writing to somebody you have never met.',
      ['Contractions are a mark of conversation.',
       'Colloquialisms are regional expressions.',
       'Stripping both out leaves language that keeps its distance.',
       'That is formal diction.'],
      '**Formal diction uses sophisticated language without contractions or colloquialisms.**'
      ' It is the register of an essay, an application, or a letter to a stranger.',
      'Informal and slang both keep contractions; concrete is about senses, not register.')

    q(Q, 1, 'Which kind of diction is tied to a particular region or era?',
      ['Colloquial diction', 'Slang diction', 'Pedantic diction', 'Poetic diction'], 0,
      'One of these tells you where somebody grew up.',
      ['Slang belongs to a subgroup rather than a place.',
       'Pedantic is about how academic the writing is.',
       'Poetic is about lyrical sound and theme.',
       'Only one is defined by region and time.'],
      '**Colloquial diction is informal language that represents a certain region or time**, and it '
      'adds color and realism to writing.',
      'Slang is its closest neighbour and the commonest wrong answer — slang marks a group, not a map.')

    q(Q, 1, 'Which pair names two kinds of diction that sit at opposite ends of one scale?',
      ['Abstract and concrete', 'Formal and pedantic', 'Slang and informal', 'Poetic and lyrical'], 0,
      'One pair genuinely opposes; the others overlap or repeat.',
      ['Pedantic is formal taken further, so they sit on the same end.',
       'Slang is a kind of informal language, not its opposite.',
       '“Lyrical” is part of the definition of poetic, so that pair says one thing twice.',
       'Abstract is the intangible; concrete is the literal and the sensory.'],
      '**Abstract and concrete are genuine opposites** — one reaches for ideas and emotions, the '
      'other for things you could photograph.',
      'Watching for pairs that merely overlap is a useful habit on any matching question.')

    q(Q, 2, 'Which kind of diction is at work? “The committee will review the proposal at its '
            'earliest convenience.”',
      ['Formal diction', 'Informal diction', 'Slang diction', 'Poetic diction'], 0,
      'Count the contractions.',
      ['There are no contractions anywhere in the sentence.',
       'There is no regional expression and no subculture vocabulary.',
       'Nothing here is lyrical or built for sound.',
       'Sophisticated language with no contractions is formal diction.'],
      '**Formal.** “At its earliest convenience” is the giveaway — it is a phrase that exists to keep '
      'a polite distance, and the sentence refuses every shortcut available to it.',
      'Ask yourself what the informal version would be: “we’ll look at it soon.”')

    q(Q, 2, 'Which kind of diction is at work? “Don’t worry about it — we’ll sort it out '
            'tomorrow.”',
      ['Informal diction', 'Formal diction', 'Pedantic diction', 'Abstract diction'], 0,
      'Two contractions in one short sentence.',
      ['“Don’t” and “we’ll” are both contractions.',
       'The sentence is doing the work of speech, not of a document.',
       'Nothing here is academic or especially detailed.',
       'Conversational language like this is informal diction.'],
      '**Informal.** It is more conversational, which is why it turns up constantly in narrative '
      'literature — dialogue that sounded formal would not sound like people.',
      'Contractions are the quickest tell, though not the only one.')

    q(Q, 2, 'Which kind of diction is at work? “Upon a rigorous parsing of your hypothesis, I have '
            'isolated three methodological deficiencies.”',
      ['Pedantic diction', 'Formal diction', 'Colloquial diction', 'Concrete diction'], 0,
      'Formal is the near-miss here. Ask whether the vocabulary is earning its keep.',
      ['There are no contractions, so it is certainly not informal.',
       'Formal would be the answer if the vocabulary fit the occasion.',
       '“Rigorous parsing” and “methodological deficiencies” are heavier than the point needs.',
       'Highly detailed and academic in writing is pedantic diction.'],
      '**Pedantic.** Every one of these words could be swapped for a plainer one without losing '
      'meaning, which is what separates pedantic from merely formal.',
      'A plain version — “I found three problems with your method” — says the same thing.')

    q(Q, 2, 'Which kind of diction is at work? In Pittsburgh a group of people is “yinz”; in Texas '
            'it is “y’all.”',
      ['Colloquial diction', 'Slang diction', 'Pedantic diction', 'Abstract diction'], 0,
      'What do these two words tell you about a speaker?',
      ['Both words mean exactly the same thing.',
       'The difference between them is geography, not meaning.',
       'Neither word originated inside a subculture and spread outward.',
       'Language that represents a certain region is colloquial diction.'],
      '**Colloquial.** These are regional expressions, and a writer who uses one is placing a '
      'character on a map — which is the “color and realism” colloquial diction adds.',
      'A novel set in one place and written in another place’s expressions reads wrong, even when nobody can say why.')

    q(Q, 2, 'Which kind of diction is at work? A group of students calls a disappointing movie “mid,” '
            'a word that began inside online gaming communities.',
      ['Slang diction', 'Colloquial diction', 'Formal diction', 'Concrete diction'], 0,
      'The sentence tells you where the word came from.',
      ['The word did not come from a region — it came from a community.',
       'It began inside a specific subgroup.',
       'It then spread outward to people who were never part of that subgroup.',
       'Originating in a subculture and gaining traction is slang diction.'],
      '**Slang.** The definition is precise about this: it originates within a specific culture or '
      'subgroup and then gains traction more widely.',
      'Slang also dates fast, which is why a novel that leans on it can age badly.')

    q(Q, 2, 'Which kind of diction is at work? “Her ambition outlasted her patience, and her pride '
            'outlasted both.”',
      ['Abstract diction', 'Concrete diction', 'Colloquial diction', 'Informal diction'], 0,
      'Try to draw this sentence.',
      ['Ambition, patience and pride are the three nouns doing the work.',
       'Not one of them can be seen, heard, touched or photographed.',
       'A sentence built entirely out of intangibles is not appealing to the senses.',
       'Expressing something intangible is abstract diction.'],
      '**Abstract.** Every noun in it is an idea rather than a thing, which is what abstract diction '
      'means — words used to express something intangible.',
      'Abstract writing is not weaker writing; it is just doing a different job.')

    q(Q, 2, 'Which kind of diction is at work? “She set the chipped blue mug on the windowsill and '
            'wiped her hands on her jeans.”',
      ['Concrete diction', 'Abstract diction', 'Pedantic diction', 'Poetic diction'], 0,
      'How many of these details could a camera catch?',
      ['A chipped blue mug is something you could see and hold.',
       'A windowsill and a pair of jeans are the same.',
       'Every word is being used for its literal meaning.',
       'Words for their literal meanings that appeal to the senses are concrete diction.'],
      '**Concrete.** “Chipped” and “blue” are the tell — the sentence is not just naming a mug, it is '
      'giving you enough to see one.',
      'The abstract version says “she was tired.” The concrete version shows you.')

    q(Q, 2, 'Which kind of diction is at work? “The harbor held its breath beneath a bruised and '
            'lowering sky.”',
      ['Poetic diction', 'Pedantic diction', 'Colloquial diction', 'Informal diction'], 0,
      'Read it aloud and listen to what the words are doing besides describing.',
      ['A harbor cannot hold its breath and a sky cannot bruise.',
       'The words are chosen for their sound and their weight as much as their meaning.',
       'Nothing here is academic, regional or conversational.',
       'Lyrical words serving a theme are poetic diction.'],
      '**Poetic.** It is driven by lyrical word choice, and the theme it serves — something '
      'ominous coming — is carried by sound as much as by statement.',
      'A poetic line usually survives being read aloud better than it survives being paraphrased.')

    q(Q, 2, 'A writer uses a run of very short sentences to make a scene feel fast. Which choice is '
            'she making?',
      ['Syntax, which is word order', 'Diction, which is word choice',
       'Imagery, which appeals to senses', 'Details, which are what is kept'], 0,
      'Is she changing which words, or how they are arranged?',
      ['She has not said anything about which words she chose.',
       'What changed is how those words are arranged and broken up.',
       'Arrangement affects the pacing of a story.',
       'Arrangement of words is syntax, not diction.'],
      '**Syntax.** Diction and syntax sit next to each other on the tone list and get swapped '
      'constantly — diction is WHICH words, syntax is what ORDER and what shape.',
      'Both change a reader’s experience; only one of them changes the vocabulary.')

    q(Q, 3, 'Two sentences both avoid contractions and both use long words. What separates pedantic '
            'diction from merely formal diction?',
      ['Pedantic goes further than the occasion needs',
       'Pedantic always appears in dialogue, not narration',
       'Pedantic uses contractions where formal does not',
       'Pedantic is spoken aloud where formal is written'], 0,
      'The tell you would normally use has been taken away. What is left?',
      ['Contractions cannot decide it — the question says neither has any.',
       'Long words cannot decide it either, for the same reason.',
       'What is left is whether the difficulty is earning anything.',
       'Formal fits the occasion; pedantic overshoots it.'],
      '**Pedantic diction is highly detailed or academic beyond what the moment asks for.** Formal '
      'and pedantic overlap almost entirely on the page — the difference is the fit, not the feature.',
      'A useful test: rewrite the line plainly. If nothing is lost, the original was pedantic.')

    q(Q, 3, 'A writer wants to check whether a line is concrete rather than abstract. Which test '
            'actually settles it?',
      ['Ask whether it could be photographed or tasted',
       'Ask whether the sentence runs longer than a clause',
       'Ask whether the writer used any adjectives at all',
       'Ask whether the line appears early in a paragraph'], 0,
      'Concrete diction is defined by what it appeals to.',
      ['Length has nothing to do with it — “I ate an apple” is short and concrete.',
       'Adjectives appear in abstract writing just as often.',
       'Position in the paragraph is irrelevant to word choice.',
       'Concrete diction refers to things that appeal to the senses.'],
      '**If a camera, a hand or an ear could catch it, it is concrete.** Abstract diction expresses '
      'something intangible — an idea or an emotion — and no sense can reach it.',
      'Most real writing mixes the two; the question is which one a given line is doing.')

    q(Q, 3, 'A student writes “The data was bad.” Her teacher asks for formal diction instead. Which '
            'revision does that?',
      ['The data proved unreliable under repeated testing',
       'The data was, like, completely useless if we’re honest',
       'The data stunk to high heaven, plain and simple',
       'The data betrayed us, cold and indifferent as stone'], 0,
      'Three of these change the register in some direction. Only one raises it.',
      ['One revision adds filler words that belong to speech.',
       'One reaches for a regional expression instead.',
       'One goes lyrical, which is a different choice entirely.',
       'Only one uses sophisticated language with no contractions and no colloquialisms.'],
      '**Formal diction raises the register without reaching for extra difficulty.** “Proved '
      'unreliable under repeated testing” also says more than “bad” did, which is usually what the '
      'request is really after.',
      'The other three are informal, colloquial and poetic — all real choices, just not the one asked for.')

    q(Q, 3, 'A novel set in rural Alabama in the 1930s gives a character “reckon” where another book '
            'would use “suppose.” What is that choice doing?',
      ['Placing the character in a region and a period',
       'Marking the character as part of a subculture',
       'Expressing an idea that has no physical form',
       'Slowing the pacing of the scene through syntax'], 0,
      'Ask what the word would tell a reader who knew nothing else about the speaker.',
      ['“Reckon” is not a subculture word that spread outward — it is a regional one.',
       '“Suppose” is not intangible; both words name the same ordinary act.',
       'Swapping one word for another of the same length changes no pacing.',
       'A word that represents a certain region and time is colloquial diction at work.'],
      '**Colloquial diction is how a book puts a character somewhere.** It is the "color and realism" '
      'half of the definition doing its job — the word carries a place and an era with it.',
      'This is also why changing one character’s vocabulary can quietly relocate a whole scene.')

    q(Q, 3, 'Why is a question about an author’s diction so often also a question about tone?',
      ['Word choice carries an attitude with it',
       'Tone is decided before any words are chosen',
       'Diction is the only route a reader can check',
       'Every tone word is also a diction term'], 0,
      'Diction is the first of the four routes to tone. Why would that be?',
      ['Tone is the attitude an author conveys to an audience.',
       'An audience can only meet that attitude through the words on the page.',
       'Swap the words and the attitude they carry changes with them.',
       'So diction is not merely one clue to tone — it is the main one.'],
      '**Diction is the first of the four things used to determine tone**, alongside imagery, details '
      'and syntax. Words are how an attitude reaches a reader at all.',
      'The reverse holds too: deciding on a tone is largely deciding which words are allowed.')

    build('ad-astra', C, Q, 'unit-eng-t1-diction',
          'Test 1 · 3 Diction', 'english',
          'The eight kinds of diction — formal, informal, pedantic, colloquial, slang, abstract, '
          'concrete and poetic — with what each one is for, and the two pairs that get confused: '
          'formal against pedantic, and colloquial against slang.',
          'Diction is the first of the four routes to tone, so this lesson is doing double duty: '
          'naming a register on its own, and setting up every tone question that follows.',
          [('Define diction and tell it apart from syntax, tone and mood', 'source'),
           ('Name all eight kinds of diction and what each one is for', 'source'),
           ('Read a sentence and say which kind of diction is at work', 'added'),
           ('Separate formal from pedantic, and colloquial from slang', 'added'),
           ('Say why word choice shapes an author’s tone', 'added')],
          'Built from Sedona’s own handwritten notes. One thing to check with her: her concrete-diction '
          'line reads "refer to things that appeal to the specific", and the sentence trails off. The '
          'standard definition — and the one this lesson teaches — is that concrete diction appeals to '
          'the SENSES. Her example ("I ate an apple") fits the sensory reading exactly, so this is '
          'almost certainly a dropped word rather than a different definition, but it is worth a glance '
          'at her page. Everything else on both diction pages checks out. The questions all use fresh '
          'sentences, so none of them can be answered from memory of the examples on her page.',
          ('Eight kinds, and two pairs that blur. Get formal-against-pedantic straight first — that is where the marks go.', 14),
          'content/eng-t1-diction.json', SRC,
          'Test 1 notes · Diction (student’s own notes)',
          prep_=True, libv_=1)


# ────────────────────────────────────────────────────────────── 4 · Tone and Mood
def tone():
    C, Q = [], []

    card(C, 'Tone',
         "**The attitude the author is trying to convey to their audience.**"
         "\n• It belongs to the AUTHOR, not to anyone inside the story."
         "\n• Every tone word names an attitude somebody is holding.",
         hint='Tone is how the author feels about it.')
    card(C, 'Determining tone',
         "**Four things: diction, imagery, details and syntax.**"
         "\n• Diction is the choice of words; imagery is words that appeal to the senses."
         "\n• Details are the words the author chose to include; syntax impacts the pacing of a story.",
         hint='What words, what senses, what was kept, what shape.')
    card(C, 'Why use tone',
         "**Six reasons: it creates atmosphere, develops character, develops plot, expresses theme, "
         "engages the reader, and establishes style and voice.**"
         "\n• Style and voice belongs HERE — it is something tone DOES."
         "\n• It is not on the list of things tone is not.",
         hint='Six jobs, and style is one of them.')
    card(C, 'Tone is not: character',
         "**Tone belongs to the author, never to a person inside the story.**"
         "\n• A cruel character can appear in a compassionate book."
         "\n• The author's attitude toward that character is the tone.",
         hint='The villain has a mood. The book has a tone.')
    card(C, 'Tone is not: narrator',
         "**A narrator is a voice inside the telling; the author stands behind it.**"
         "\n• A cheerful narrator can sit inside a grim book — often on purpose."
         "\n• “Who is speaking” never answers “what does the author think.”",
         hint='The narrator is a costume the author is wearing.')
    card(C, 'Tone is not: mood',
         "**Tone is what the author feels; mood is what the reader is made to feel.**"
         "\n• They often match, which is exactly why they blur."
         "\n• They can also disagree, and a writer can do that deliberately.",
         hint='Whose feeling is it? That settles it every time.')
    card(C, 'Positive tone words',
         "**Admiring, calm, candid, benevolent, inspirational, modest, respectful.**"
         "\n• Every one of these describes an attitude somebody is holding."
         "\n• Candid is the useful one — it means honest, including about yourself.",
         hint='These are attitudes, not atmospheres.')
    card(C, 'Negative tone words',
         "**Apathetic, confused, cruel, diabolical, foreboding, grim, pretentious, naive.**"
         "\n• Apathetic means not caring, which is itself an attitude."
         "\n• Foreboding is an attitude that is warning you something is coming.",
         hint='Naive is negative here because it means not seeing clearly.')
    card(C, 'Mood',
         "**The emotion the author is trying to evoke from the reader.**"
         "\n• Mood is more than just a statement of feeling."
         "\n• A line that SAYS “she was sad” has stated a feeling, not built a mood.",
         hint='Mood is how the page makes YOU feel.')
    card(C, 'Determining mood',
         "**Four things: setting, figurative language, diction, and genre and plot.**"
         "\n• Diction appears on BOTH lists — it shapes tone and mood at once."
         "\n• Setting and genre are on the mood list only.",
         hint='Where it happens, how it is said, what kind of story it is.')
    card(C, 'Positive mood words',
         "**Cheerful, romantic, idyllic, whimsical, lighthearted, centered, sentimental.**"
         "\n• Idyllic means peaceful and perfect, usually somewhere rural."
         "\n• These describe the air in a room, not a person's opinion.",
         hint='These are atmospheres, not attitudes.')
    card(C, 'Negative mood words',
         "**Gloomy, ominous, tense, lonely, pessimistic, panicked, uneasy.**"
         "\n• Ominous is mood's near-twin for foreboding on the tone list."
         "\n• Uneasy is the quiet one — something is wrong and you cannot name it.",
         hint='Ominous is what foreboding writing produces.')
    card(C, 'Tone and mood, side by side',
         "**Ask whose feeling it is: the author's is tone, the reader's is mood.**"
         "\n• One question separates them every time, and it is always the same question."
         "\n• The two word banks barely overlap, which is a clue in itself.",
         hint='Author = tone. Audience = mood.')
    card(C, 'Mood is not a statement of feeling',
         "**Naming an emotion is not the same as producing one.**"
         "\n• “The room was scary” states a feeling; a dark corridor and a door that should be "
         "locked produces one."
         "\n• Which is why setting and figurative language are on the mood list.",
         hint='Stating is telling. Mood is built.')

    q(Q, 1, 'Whose attitude does tone describe?',
      ['The author’s', 'The narrator’s', 'The reader’s', 'The main character’s'], 0,
      'Three of these are explicitly named as things tone is NOT.',
      ['The reader’s feeling has its own name — mood.',
       'A character is inside the story; tone is not a character.',
       'A narrator is a voice inside the telling, and tone is not the narrator either.',
       'Tone is the attitude the author conveys to their audience.'],
      '**Tone is the author’s attitude toward the audience and the subject.** Character, narrator '
      'and mood are the three things it is specifically not.',
      'That short "tone is not" list is doing real work — those are the three answers people actually give.')

    q(Q, 1, 'Whose emotion does mood describe?',
      ['The reader’s', 'The author’s', 'The narrator’s', 'A minor character’s'], 0,
      'Mood is about what the writing does to somebody.',
      ['Mood refers to the emotion the author is trying to evoke.',
       'Evoke from whom? From the person reading.',
       'The author’s own attitude has a different name — tone.',
       'So mood lives on the reader’s side of the page.'],
      '**Mood is the emotion the author is trying to evoke from the reader.** Tone is what the author '
      'feels; mood is what you are made to feel.',
      'Whose feeling is it — that one question settles nearly every tone-or-mood item.')

    q(Q, 1, 'Which set of four is used to determine an author’s tone?',
      ['Diction, imagery, details, syntax', 'Setting, figurative language, diction, genre',
       'Exposition, rising action, climax, theme', 'Rhythm, rhyme, meter, stanza'], 0,
      'One of the wrong sets is the MOOD list, which shares exactly one item with the right answer.',
      ['One set belongs to plot structure, not to tone.',
       'One set belongs to poetry’s sound, not to tone.',
       'One set is the list for determining mood, and it shares diction with the tone list.',
       'The tone list is diction, imagery, details and syntax.'],
      '**Diction is the choice of words, imagery appeals to the senses, details are what the author '
      'chose to include, and syntax affects the pacing.** All four are routes to the same thing.',
      'Diction is on both lists — that overlap is the reason they get confused.')

    q(Q, 1, 'Which set of four is used to determine a piece’s mood?',
      ['Setting, figurative language, diction, genre', 'Diction, imagery, details, and syntax',
       'Exposition, climax, resolution, and theme', 'Grammar, spelling, punctuation, tense'], 0,
      'Two of the four routes to mood are about the world of the story rather than its words.',
      ['Mechanics like spelling do not build an emotion.',
       'Plot stages describe structure, not atmosphere.',
       'One wrong set is the tone list, which again shares diction.',
       'Mood comes from setting, figurative language, diction, and genre and plot.'],
      '**Setting and genre are on the mood list only** — where a scene happens and what kind of story '
      'it is do a great deal of the work of making you feel something.',
      'A dark corridor in a horror novel and the same corridor in a comedy do not produce the same feeling.')

    q(Q, 1, 'Which of these is a negative MOOD word?',
      ['Ominous', 'Admiring', 'Candid', 'Idyllic'], 0,
      'Three of these name somebody’s attitude, or an atmosphere that is pleasant.',
      ['Admiring and candid both name attitudes a person holds — those are tone words.',
       'Idyllic describes an atmosphere, so it is a mood word, but a positive one.',
       'That leaves one word describing an atmosphere that is unpleasant.',
       'Ominous is a negative mood word.'],
      '**Ominous means the air feels like something bad is coming.** It is an atmosphere rather than '
      'an opinion, which is what makes it mood rather than tone.',
      'Its tone counterpart is foreboding — an author writing foreboding prose produces an ominous mood.')

    q(Q, 1, 'Which of these is a positive TONE word?',
      ['Benevolent', 'Whimsical', 'Tense', 'Diabolical'], 0,
      'Two of these describe an atmosphere, not an attitude.',
      ['Whimsical and tense both describe how a scene feels to read — those are mood words.',
       'Diabolical does name an attitude, so it is a tone word, but not a positive one.',
       'That leaves a word naming a kindly attitude.',
       'Benevolent is a positive tone word.'],
      '**Benevolent means well-meaning toward somebody**, which is an attitude, so it belongs on the '
      'tone list rather than the mood list.',
      'Sorting a word by asking "is this an attitude or an atmosphere" works better than memorising both banks.')

    q(Q, 2, 'What tone is this author taking toward the subject?',
      ['Admiring', 'Apathetic', 'Diabolical', 'Pretentious'], 0,
      'The author chose which details to include. What do those choices add up to?',
      ['The details kept are effort, skill and modesty.',
       'Nothing is said outright about what the author thinks of her.',
       'But no author includes those three details by accident.',
       'The attitude they build is admiration.'],
      '**Admiring.** This is the "details" route to tone at work — the author never states an opinion, '
      'but chooses only the facts that build one.',
      'An apathetic author would have given the same events two flat lines and moved on.')
    Q[-1]['passage'] = ('Every morning before dawn she was already at the bench, sleeves rolled, '
                        'working on the engine nobody else had managed to fix. She never once '
                        'mentioned it to anyone.')

    q(Q, 2, 'What mood is this passage building?',
      ['Ominous', 'Idyllic', 'Whimsical', 'Sentimental'], 0,
      'Nothing bad has actually happened yet. What are you expecting anyway?',
      ['The setting is a dark corridor with failing lights.',
       'A door that should have been locked opens on its own.',
       'The passage then stops, giving you nothing to settle on.',
       'That combination evokes a feeling that something bad is coming.'],
      '**Ominous.** Notice how much of this comes from setting — one of the four routes to mood — '
      'rather than from any word naming an emotion.',
      'The passage never says "frightening." A mood that had to say so would not be much of a mood.')
    Q[-1]['passage'] = ('The corridor lights flickered twice and went out. Somewhere below, a door '
                        'that should have been locked swung slowly open, and then there was nothing '
                        'at all.')

    q(Q, 2, 'What tone is this writer taking?',
      ['Candid', 'Pretentious', 'Foreboding', 'Cruel'], 0,
      'The writer had the option of looking better than this. What did they do instead?',
      ['The report lists what failed alongside what worked.',
       'It also admits to what the writer still does not understand.',
       'No attempt is made to present the work as more finished than it is.',
       'Honesty about your own limits is a candid tone.'],
      '**Candid.** Candid is honest, including about yourself — which is exactly what a '
      'pretentious tone would have refused.',
      'Pretentious is the near-miss here, and it is the opposite choice about the same material.')
    Q[-1]['passage'] = ('The report lists what worked, what failed, and what the writer still does '
                        'not understand. It makes no attempt to look better than it is.')

    q(Q, 2, 'A narrator cheerfully describes a town where nobody locks a door, while a reader keeps '
            'noticing how many houses stand empty. Which term names the reader’s uneasy feeling?',
      ['Mood', 'Tone', 'Diction', 'Syntax'], 0,
      'Whose feeling is being described in the question?',
      ['The cheerfulness belongs to the narrator’s voice.',
       'The unease belongs to the person reading.',
       'A feeling evoked in the reader has one name.',
       'That name is mood.'],
      '**Mood, because it is the reader’s feeling.** This is also a clean example of tone and mood '
      'pulling apart on purpose — a cheerful surface producing an uneasy reader.',
      'Writers do this deliberately, and spotting the gap is usually the whole point of the question.')

    q(Q, 2, 'An author writes about a family’s ordinary Sunday in a way that quietly warns you '
            'something is coming. Which tone word names that?',
      ['Foreboding', 'Benevolent', 'Apathetic', 'Modest'], 0,
      'The author is holding an attitude about what is ahead, not about the family.',
      ['Benevolent and modest are both warm attitudes, and nothing here is warm.',
       'Apathetic would mean the author did not care, but this author is signalling hard.',
       'The attitude on the page is a warning.',
       'A tone that warns of something coming is foreboding.'],
      '**Foreboding.** It sits on the negative tone list, and it is the attitude that produces an '
      'ominous mood in a reader.',
      'Pairing foreboding with ominous is worth memorising — they are the tone and mood sides of one effect.')

    q(Q, 2, 'A student writes “The passage made me feel sad,” and her teacher says that states a '
            'feeling rather than describing mood. What is missing?',
      ['How the writing produces that feeling',
       'A quotation drawn from a later chapter',
       'The name of the book’s actual narrator',
       'A count of how many pages it covers'], 0,
      'Mood is described as being more than just a statement of feeling. More in what way?',
      ['Naming an emotion reports a result.',
       'It says nothing about what caused the result.',
       'Mood is built out of setting, figurative language, diction, and genre and plot.',
       'So a description of mood has to point at what did the building.'],
      '**Mood is more than just a statement of feeling.** "It made me sad" is a reaction; describing '
      'mood means showing which choices on the page produced it.',
      'The same rule is why "the tone is sad" alone rarely earns full marks either.')

    q(Q, 2, 'A writer breaks a chase scene into a run of very short sentences. Which route to tone is '
            'she using?',
      ['Syntax', 'Imagery', 'Details', 'Diction'], 0,
      'She has changed the shape of the sentences, not the words in them.',
      ['Diction would mean choosing different words.',
       'Imagery would mean words appealing to the senses.',
       'Details would mean changing what is included.',
       'Sentence shape and length affect the pacing, and that is syntax.'],
      '**Syntax impacts the pacing of a story**, which is why it earns a place on the tone list beside '
      'diction, imagery and details.',
      'Long, winding sentences do the opposite job — the same scene can be made to feel slow.')

    q(Q, 3, 'A boastful villain narrates a chapter, and the writing around him makes clear he is not '
            'to be admired. Where does the tone live?',
      ['In the author’s attitude toward the villain',
       'In the villain’s own attitude toward himself',
       'In the reader’s reaction to the whole chapter',
       'In the narrator’s choice of boastful vocabulary'], 0,
      'Two of the wrong answers are named outright as things tone is not.',
      ['Tone is not a character, so the villain’s self-regard is not it.',
       'Tone is not the narrator, so his vocabulary is not it either.',
       'Tone is not mood, so the reader’s reaction is a different thing.',
       'What is left is the author’s attitude, which is what tone means.'],
      '**Tone is the author’s attitude, which can sit in direct opposition to the narrator’s.** '
      'A book can let a character praise himself while the writing around him disagrees.',
      'This gap is how irony works, and it is why "tone is not the narrator" is on the list at all.')

    q(Q, 3, 'Diction appears on the tone list and on the mood list. What follows from that?',
      ['One word choice can shape both at once',
       'Tone and mood always turn out the same',
       'Mood cannot be judged without the tone',
       'Diction matters more than any other route'], 0,
      'Sharing one route is not the same as being the same thing.',
      ['Tone has three routes that mood does not: imagery, details and syntax.',
       'Mood has three routes that tone does not: setting, figurative language, and genre and plot.',
       'So they overlap in one place and separate everywhere else.',
       'A single word choice can move both, without making them identical.'],
      '**Diction is the one shared route, which is why it is the most efficient thing to change** — and '
      'why tone and mood so often agree without being the same thing.',
      'When they disagree, it is usually because the other six routes are pulling in different directions.')

    q(Q, 3, 'Two readers agree a chapter feels tense but disagree about whether the author sounds '
            'sympathetic. Which question would settle the disagreement?',
      ['What attitude do the author’s word choices carry?',
       'What emotion did the chapter leave each of you with?',
       'Which character does the most speaking in the scene?',
       'How many of the sentences run longer than a line?'], 0,
      'They already agree on one of the two things. Which one is still open?',
      ['"Feels tense" is a statement about mood, and they agree on it.',
       'What is disputed is whether the author sounds sympathetic, which is tone.',
       'Asking about the emotion again would only re-answer the settled half.',
       'Tone is reached through diction, imagery, details and syntax.'],
      '**The open question is about tone, so it has to be answered with tone’s own evidence.** '
      'Agreeing on mood tells you nothing about the author’s attitude.',
      'Noticing which of the two is actually being argued about is half the work on questions like this.')

    q(Q, 3, 'An author gives an ordinary farmhouse warm light, soft sounds and a slow pace. Which '
            'pairing describes what has been built?',
      ['An idyllic mood, from setting and diction',
       'A grim tone, built from syntax and details',
       'A naive tone, built from imagery and plot',
       'A panicked mood, from genre and setting'], 0,
      'Name the feeling first, then check which routes produced it.',
      ['Warm light and soft sounds describe a place, which is setting.',
       '"Warm" and "soft" are word choices, which is diction.',
       'The feeling those produce in a reader is peaceful and a little perfect.',
       'Idyllic is the mood word for that, and setting and diction are both on the mood list.'],
      '**Idyllic, built from setting and diction — both genuine routes to mood.** The wrong pairings '
      'each name a feeling the description does not support, or a route from the wrong list.',
      'Check both halves of an answer like this: the right feeling reached by the wrong route is still wrong.')

    q(Q, 3, 'Establishing style and voice is listed as one of the things tone DOES. What does that '
            'mean in practice?',
      ['A consistent attitude is part of how a writer sounds',
       'A writer has to keep one single tone in every book',
       'Style can stand in for describing a setting at all',
       'Voice is decided by the narrator rather than by the author'], 0,
      'Think about what makes two books by the same author recognisable as hers.',
      ['Tone is the attitude an author conveys.',
       'An author who takes similar attitudes across their work becomes recognisable for it.',
       'That recognisability is what "style and voice" names.',
       'So establishing style is something tone does, alongside atmosphere, character, plot, theme and engagement.'],
      '**Style and voice is one of the six reasons to use tone** — not something tone is not. An '
      'author’s habitual attitude is a large part of what makes their writing sound like theirs.',
      'It sits on the list beside creating atmosphere, developing character and plot, expressing theme, and engaging the reader.')

    build('ad-astra', C, Q, 'unit-eng-t1-tone',
          'Test 1 · 4 Tone and Mood', 'english',
          'Tone as the author’s attitude and mood as the reader’s emotion; the four routes to each; '
          'the three things tone is NOT (character, narrator, mood); the six things tone does; and '
          'both word banks.',
          'Tone and mood are the two terms most often swapped for each other on a test, and the fix is '
          'one question you can ask every time: whose feeling is this?',
          [('Define tone and mood and tell them apart reliably', 'source'),
           ('Name the four routes to tone and the four routes to mood', 'source'),
           ('Say what tone is NOT, and why each one is on that list', 'source'),
           ('Read a short passage and name its tone or its mood', 'added'),
           ('Choose a word from the right bank for the right job', 'added')],
          'Built from Sedona’s own handwritten notes, and the pages had to be rendered as images to '
          'get one detail right: Drive’s scan of her handwriting filed "style and voice" under "Tone '
          'is NOT", where it would have taught the exact opposite. Her page has it under "why use '
          'tone", which is correct, and a question here pins it. The three things tone is genuinely '
          'not — character, narrator, mood — are the whole difficulty of this lesson, and the last '
          'five questions are all built on them. Her word banks are reproduced exactly as she wrote '
          'them; every passage in the questions is original.',
          ('Three short passages in here. Name the feeling first, then work out which choices on the page built it.', 15),
          'content/eng-t1-tone.json', SRC,
          'Test 1 notes · Tone and Mood (student’s own notes)',
          prep_=True, libv_=1)


if __name__ == '__main__':
    diction()
    tone()
