# Sedona's English Test 1, parts 5, 6 and 7 — Figurative Language, Symbolism
# and Motifs, and the To Kill a Mockingbird background.
#
# Same source and same discipline as the other two builders in this set: her
# own handwritten unit notes, read by RENDERING the pages with pypdfium2.
#
# Every graded question uses a FRESH example. Her notes' own examples live on
# the CARDS, where they are the reference she is revising from.
#
# Part 7 was scoped against content/tkam-1.json BEFORE anything was written.
# That unit is the reading companion for chapters 1-5 — plot, characters and
# the Boo Radley material — and covers none of the author's biography, the
# publication date, or the dating of the setting. There is no overlap here.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

SRC = 'English Test 1 notes (Drive, 2026-09-23)'


# ───────────────────────────────────────────────────────── 5 · Figurative Language
def figurative():
    C, Q = [], []

    card(C, 'Simile',
         "**Directly compares two things using “like” or “as.”**"
         "\n• The word doing the comparing is right there on the page."
         "\n• That is the whole difference between a simile and a metaphor.",
         hint='Like or as — say it out loud and you will hear it.')
    card(C, 'Standard metaphor',
         "**Implies a comparison between two unlike things, stated outright.**"
         "\n• Example: “This place is a zoo.”"
         "\n• It says one thing IS another, with no “like” anywhere.",
         hint='It claims the two things are the same thing.')
    card(C, 'Implied metaphor',
         "**Compares two things without directly stating the comparison.**"
         "\n• Example: “Not knowing anyone, he felt awkward at the party, so he started orbiting "
         "around the snack table.”"
         "\n• Nobody is called a planet — “orbiting” does all the work.",
         hint='The comparison is smuggled in by a verb.')
    card(C, 'Extended metaphor',
         "**Carried through multiple sentences, paragraphs, or whole works.**"
         "\n• One comparison, kept running."
         "\n• Length is the test — a single striking line is not extended.",
         hint='It keeps going after you notice it.')
    card(C, 'Which metaphor is which?',
         "**Stated outright is standard; hidden inside the wording is implied; kept running is extended.**"
         "\n• All three are metaphors, so “metaphor” alone never settles the question."
         "\n• Ask: is it said, is it hinted, or does it continue?",
         hint='Said, hinted, or sustained.')
    card(C, 'Personification',
         "**Giving human qualities to an animal, an object or an abstract idea.**"
         "\n• Example: “the city that never sleeps.”"
         "\n• The thing being given the quality cannot actually have it.",
         hint='Only people can do it, but something else is doing it.')
    card(C, 'Imagery',
         "**Used to appeal to one of the five senses.**"
         "\n• It is also one of the four routes to an author's tone."
         "\n• Naming a feeling is not imagery; making you sense something is.",
         hint='It reaches you through a sense, not through a statement.')
    card(C, 'The five kinds of imagery',
         "**Visual is sight, auditory is hearing, olfactory is smell, tactile is touch, gustatory "
         "is taste.**"
         "\n• Olfactory and gustatory are the two most often swapped."
         "\n• Olfactory shares its root with “olfactory nerve” — the nose.",
         hint='Gustatory shares a root with “gusto,” which is about eating.')
    card(C, 'Hyperbole',
         "**An exaggerated statement used to emphasize an idea or make a point.**"
         "\n• Nobody is meant to believe it literally."
         "\n• It is the opposite move from understatement.",
         hint='Too big on purpose.')
    card(C, 'Understatement',
         "**Describing something as having less of a quality than it actually has.**"
         "\n• The gap between what is said and what is true is the point."
         "\n• Too small on purpose — the mirror image of hyperbole.",
         hint='Too small on purpose.')
    card(C, 'Litotes',
         "**Phrases that express an affirmative by denying its opposite, through understatement.**"
         "\n• Example: “That wasn't half bad.”"
         "\n• Litotes is a KIND of understatement with a particular shape: a negative of the opposite.",
         hint='Not un-good. Look for the double negative.')
    card(C, 'Understatement or litotes?',
         "**All litotes is understatement; not all understatement is litotes.**"
         "\n• Litotes needs the denial — “not unkind,” “no small feat,” “wasn't half bad.”"
         "\n• Plain understatement just shrinks the truth without any denying.",
         hint='If there is no “not,” it is plain understatement.')
    card(C, 'Euphemism',
         "**A softer, more inoffensive word or phrase used as a substitute for a harsh comment.**"
         "\n• Example: “Robert was let go from his job.”"
         "\n• It protects the listener, or the speaker, from the blunt version.",
         hint='The polite word standing in for the hard one.')
    card(C, 'Synecdoche',
         "**A figure of speech in which a part is used to represent a whole, and vice versa.**"
         "\n• “All hands on deck” means all people, not all hands."
         "\n• It can run the other way too — “Washington decided” means a few officials there.",
         hint='A piece standing in for the whole thing.')
    card(C, 'Oxymoron',
         "**Combines contradictory words with opposing meanings.**"
         "\n• Example: “The end of the movie was bittersweet.”"
         "\n• The contradiction sits inside one short phrase, side by side.",
         hint='Two words that should not be able to share a phrase.')
    card(C, 'Pun',
         "**A play on words, usually on words that sound the same but mean different things.**"
         "\n• The joke lives in the sound, or in a word carrying two meanings at once."
         "\n• Both kinds count as a pun.",
         hint='One sound, two meanings, on purpose.')
    card(C, 'Allusion',
         "**A reference a writer makes to deepen the reader's understanding of their work.**"
         "\n• It borrows everything the reader already knows about the thing referred to."
         "\n• It only works when the reader recognises it, which is a real risk.",
         hint='It points outside the book to bring something in.')
    card(C, 'Alliteration',
         "**Repetition of the same sound at the beginning of adjacent or closely connected words.**"
         "\n• It is about SOUND, not spelling — “kind cat” alliterates."
         "\n• Close together is part of the definition; scattered repeats do not count.",
         hint='Same opening sound, words side by side.')
    card(C, 'Anaphora',
         "**Repetition of a word or phrase at the beginning of successive clauses.**"
         "\n• It is a favorite of speeches, where the build is the whole effect."
         "\n• What repeats is a word or phrase, not a sound.",
         hint='Each new clause starts the same way.')
    card(C, 'Alliteration or anaphora?',
         "**Alliteration repeats a SOUND across nearby words; anaphora repeats a WORD OR PHRASE "
         "across clauses.**"
         "\n• One works at the scale of a few syllables, the other at the scale of sentences."
         "\n• Ask what is repeating, and how far apart.",
         hint='A sound in a line, or a phrase across lines.')
    card(C, 'Idioms',
         "**An expression with a figurative or metaphorical meaning.**"
         "\n• Example: “Stop beating around the bush.”"
         "\n• The literal reading is nonsense, which is how you know it is an idiom.",
         hint='It means something the words do not say.')
    card(C, 'Reading any of these',
         "**Name the device, then say what it is DOING in that sentence.**"
         "\n• A test question rarely stops at the label."
         "\n• Every one of these is a choice, and every choice has an effect on tone or mood.",
         hint='The label is half an answer.')

    q(Q, 1, 'Which device directly compares two things using “like” or “as”?',
      ['Simile', 'Standard metaphor', 'Personification', 'Allusion'], 0,
      'One of these announces the comparison with a word you can point to.',
      ['A standard metaphor claims one thing IS another, with no comparing word.',
       'Personification gives a human quality to something that cannot have it.',
       'An allusion points outside the work entirely.',
       'Only one device uses “like” or “as” to compare directly.'],
      '**A simile directly compares two things using “like” or “as.”** That comparing word is the '
      'one reliable difference between a simile and a metaphor.',
      'If you can delete "like" and the sentence becomes a metaphor, it was a simile.')

    q(Q, 1, 'Which device gives human qualities to an animal, an object or an abstract idea?',
      ['Personification', 'Implied metaphor', 'Standard metaphor', 'Understatement'], 0,
      'Two of these are genuine near-misses. Ask what KIND of quality is being borrowed.',
      ['An implied metaphor compares without stating, but the quality borrowed need not be human.',
       'A standard metaphor says one thing IS another, outright.',
       'Understatement shrinks a quality rather than lending one.',
       'Only one device specifically hands a HUMAN quality to something that is not a person.'],
      '**Personification gives human qualities to an animal, an object or an abstract idea.** '
      'Abstract ideas count — "justice demanded an answer" is personification too.',
      'Implied metaphor is the near-miss: it also hides its comparison, but the quality it lends need not be human.')

    q(Q, 1, 'Which term names the repetition of a word or phrase at the beginning of successive clauses?',
      ['Anaphora', 'Alliteration', 'Litotes', 'Synecdoche'], 0,
      'One of these works at the scale of whole clauses.',
      ['Alliteration repeats a sound across nearby words, not a phrase across clauses.',
       'Litotes denies an opposite to state something positively.',
       'Synecdoche swaps a part for a whole.',
       'Repetition at the start of successive clauses is anaphora.'],
      '**Anaphora repeats a word or phrase at the beginning of successive clauses.** It is the '
      'device behind almost every famous speech, because the build IS the effect.',
      'Alliteration is its nearest neighbour and repeats a sound rather than a phrase.')

    q(Q, 1, 'Which sense does olfactory imagery appeal to?',
      ['Smell', 'Taste', 'Touch', 'Hearing'], 0,
      'Think of the olfactory nerve.',
      ['Tactile is touch and auditory is hearing.',
       'Gustatory is taste.',
       'That leaves one sense unaccounted for.',
       'Olfactory imagery appeals to smell.'],
      '**Olfactory is smell.** It shares a root with the olfactory nerve, which is the one that '
      'carries smell to the brain.',
      'Olfactory and gustatory are the pair most often swapped — smell and taste.')

    q(Q, 1, 'Which sense does gustatory imagery appeal to?',
      ['Taste', 'Smell', 'Touch', 'Sight'], 0,
      'Think of eating something with gusto.',
      ['Olfactory is smell and tactile is touch.',
       'Visual is sight.',
       'One sense is left over.',
       'Gustatory imagery appeals to taste.'],
      '**Gustatory is taste**, and it shares a root with "gusto" — enthusiasm, originally for food.',
      'Visual, auditory, olfactory, tactile, gustatory: sight, hearing, smell, touch, taste.')

    q(Q, 1, 'Which term names a figure of speech in which a part is used to represent a whole?',
      ['Synecdoche', 'Euphemism', 'Litotes', 'Idiom'], 0,
      'One of these is about scale — a piece standing in for the thing it belongs to.',
      ['A euphemism softens a harsh word.',
       'Litotes states something positively by denying its opposite.',
       'An idiom means something its words do not literally say.',
       'A part standing for a whole is synecdoche.'],
      '**Synecdoche uses a part to represent a whole, and can also run the other way.** "All hands '
      'on deck" means people; "Washington announced" means a few officials there.',
      'It is worth learning to say as well as spell: suh-NEK-duh-kee.')

    q(Q, 1, 'Which term names an expression whose meaning is figurative rather than literal?',
      ['Idiom', 'Allusion', 'Anaphora', 'Oxymoron'], 0,
      'Try reading each candidate device literally and see which one stops making sense.',
      ['An allusion is a reference to something outside the work.',
       'Anaphora is repetition at the start of clauses.',
       'An oxymoron joins two contradictory words.',
       'An expression with a figurative or metaphorical meaning is an idiom.'],
      '**An idiom means something its own words do not say.** "Beating around the bush" describes no '
      'bush and no beating, which is exactly the tell.',
      'Idioms rarely survive translation, which is another way of noticing they are not literal.')

    q(Q, 2, 'Which device is at work? “Her handwriting looked like a fence after a storm.”',
      ['Simile', 'Standard metaphor', 'Personification', 'Hyperbole'], 0,
      'Look for a comparing word.',
      ['Two unlike things are being compared — handwriting and a fence.',
       'The comparison is made out loud rather than implied.',
       'The word “like” is doing the comparing.',
       'A direct comparison using “like” or “as” is a simile.'],
      '**Simile.** The metaphor version would read "her handwriting was a fence after a storm" — '
      'same comparison, one word’s difference, different device.',
      'Similes are easier to spot than any other device on this list, which makes them free marks.')

    q(Q, 2, 'Which device is at work? “By seven o’clock the kitchen was a battlefield.”',
      ['Standard metaphor', 'Simile', 'Implied metaphor', 'Idiom'], 0,
      'The comparison is being made, but how?',
      ['A kitchen and a battlefield are genuinely unlike things.',
       'There is no “like” or “as” anywhere, so it is not a simile.',
       'The comparison is stated outright rather than hinted at.',
       'An outright claim that one thing IS another is a standard metaphor.'],
      '**Standard metaphor.** It implies a comparison between two unlike things and says it plainly — '
      'the kitchen is not called battlefield-ish, it is called a battlefield.',
      'The implied version would never use the word "battlefield" at all.')

    q(Q, 2, 'Which device is at work? “He bristled at the question, and nobody at the table risked a '
            'second one.”',
      ['Implied metaphor', 'Standard metaphor', 'Personification', 'Oxymoron'], 0,
      'Which word is describing him as something he is not?',
      ['“Bristled” is what an animal does when its hair stands up.',
       'He is never actually called an animal anywhere in the sentence.',
       'So a comparison is being made without being stated.',
       'A comparison made without directly stating it is an implied metaphor.'],
      '**Implied metaphor.** The whole comparison is carried by one verb, which is what makes implied '
      'metaphors easy to read past without noticing them.',
      'Personification runs the other way — that would be giving a HUMAN quality to something non-human.')

    q(Q, 2, 'Which device is at work? “The old radiator complained all night and finally gave up '
            'around four.”',
      ['Personification', 'Implied metaphor', 'Standard metaphor', 'Extended metaphor'], 0,
      'Complaining and giving up are things only one kind of thing can do.',
      ['A radiator cannot complain, and it cannot give up either.',
       'Both are human behaviours being handed to an object.',
       'No comparison to a second thing is ever made, so no metaphor is involved.',
       'Giving human qualities to an object is personification.'],
      '**Personification.** Notice it also does real work: two human verbs make the radiator sound '
      'tired and old, which no plain description would have done as fast.',
      'The three metaphors are all wrong here for one reason: nothing is being compared to anything else.')

    q(Q, 2, 'Which device is at work? “I have told you a thousand times to shut the gate.”',
      ['Hyperbole', 'Understatement', 'Litotes', 'Euphemism'], 0,
      'Is the number meant to be believed?',
      ['Nobody has literally said this a thousand times.',
       'The exaggeration is deliberate, not a mistake.',
       'It is there to emphasize how often the speaker has asked.',
       'An exaggerated statement used to make a point is hyperbole.'],
      '**Hyperbole.** It is an exaggerated statement used to emphasize an idea — and the exaggeration '
      'is the emphasis, which is why "several times" would land differently.',
      'Understatement is the mirror image, and the two are worth learning as a pair.')

    q(Q, 2, 'Which device is at work? A company announces that forty employees are now “between '
            'opportunities.”',
      ['Euphemism', 'Litotes', 'Idiom', 'Allusion'], 0,
      'What is the blunt version of the sentence?',
      ['The blunt version is that forty people lost their jobs.',
       'The phrase chosen is gentler than the blunt version.',
       'It is standing in as a substitute for the harsh comment.',
       'A softer word substituted for a harsh one is a euphemism.'],
      '**Euphemism.** The point of one is to protect somebody — sometimes the listener, and quite '
      'often the speaker.',
      'Euphemism is worth watching for in real writing, because noticing one usually tells you what is really being said.')

    q(Q, 2, 'Which device is at work? “The room filled with a deafening silence.”',
      ['Oxymoron', 'Pun', 'Synecdoche', 'Anaphora'], 0,
      'Read the two key words next to each other and ask whether they can both be true.',
      ['Silence is the absence of sound.',
       'Deafening describes an overwhelming amount of sound.',
       'The two words contradict each other and sit side by side.',
       'Contradictory words with opposing meanings in one phrase is an oxymoron.'],
      '**Oxymoron.** The contradiction is the meaning — it describes a silence so total it is as hard '
      'to ignore as a noise would be.',
      'Bittersweet, jumbo shrimp and deafening silence are the three you will meet most often.')

    q(Q, 2, 'Which device is at work? “The baker finally quit, because he kneaded the dough far more '
            'than he needed the dough.”',
      ['Pun', 'Idiom', 'Oxymoron', 'Anaphora'], 0,
      'Say the sentence out loud.',
      ['“Kneaded” and “needed” sound identical.',
       'They mean two completely different things.',
       'The sentence uses both on purpose, in one breath.',
       'Words that sound the same carrying different meanings is a pun.'],
      '**Pun.** The joke lives in the sound — which is why a pun almost always has to be heard rather '
      'than only read.',
      'A pun can also work on one word carrying two meanings at once, without any sound trick at all.')

    q(Q, 2, 'Which kind of imagery is at work? “The hallway smelled of wet wool and burnt coffee.”',
      ['Olfactory', 'Gustatory', 'Tactile', 'Auditory'], 0,
      'Which sense is the sentence reaching for?',
      ['Nothing here is being heard or touched.',
       'Nothing is being eaten or tasted either.',
       'The whole sentence is built on what the hallway smelled of.',
       'Imagery appealing to smell is olfactory.'],
      '**Olfactory.** Smell is the sense writers reach for least and the one that carries memory '
      'hardest, which is why a line like this does so much work.',
      'Gustatory would be the near-miss: coffee can be tasted, but here it is only being smelled.')

    q(Q, 3, 'After a kitchen fire destroyed half a house, the owner says, “We had a little trouble '
            'with the stove.” Which device is that?',
      ['Understatement, with no denial', 'Litotes, built on a denial',
       'Euphemism, a softer substitute', 'Hyperbole, an exaggeration'], 0,
      'Is anything being denied, or softened, or exaggerated?',
      ['Nothing is being exaggerated, so it is not hyperbole.',
       'No opposite is being denied — there is no “not” anywhere — so it is not litotes.',
       'No harsh word has been replaced with a gentler one, so it is not a euphemism.',
       'Describing something as having less of a quality than it has is understatement.'],
      '**Understatement.** Litotes is the tempting wrong answer, but litotes needs the denial of an '
      'opposite — "that was no small fire" would have been litotes.',
      'All litotes is understatement; not all understatement is litotes. That is the only bit worth memorising.')

    q(Q, 3, 'What makes litotes a particular kind of understatement rather than understatement in general?',
      ['It states the affirmative by denying its opposite',
       'It exaggerates the quality it is describing',
       'It replaces a harsh word with a softer word',
       'It repeats a sound at the start of two words'], 0,
      'Two of these describe completely different devices.',
      ['Exaggeration is hyperbole, which is understatement’s opposite.',
       'Replacing a harsh word is euphemism.',
       'Repeating an opening sound is alliteration.',
       'Litotes has a specific shape: it affirms by denying the opposite.'],
      '**Litotes expresses an affirmative by denying its opposite, through understatement.** "Not '
      'unfamiliar," "no small feat," "wasn’t half bad" — the denial is what makes it litotes.',
      'Look for a "not," a "no," or an "un-" doing the work.')

    q(Q, 3, 'A speech opens three sentences in a row with the words “We will.” Which device is that?',
      ['Anaphora', 'Alliteration', 'Hyperbole', 'Allusion'], 0,
      'What exactly is repeating — a sound, or a phrase?',
      ['A whole phrase is repeating, not a single opening sound.',
       'The repeats are at the start of successive clauses.',
       'Alliteration would mean nearby words sharing an opening sound.',
       'Repetition of a phrase at the start of successive clauses is anaphora.'],
      '**Anaphora.** The reason speeches use it is that each repetition makes the next one land '
      'harder — the effect is cumulative and disappears if you use it once.',
      'Alliteration is the near-miss: a sound in a line, against a phrase across lines.')

    q(Q, 3, 'Which device is at work in this passage?',
      ['Extended metaphor', 'Standard metaphor', 'Simile', 'Personification'], 0,
      'Count how far the comparison runs.',
      ['The project is called a ship in the first sentence.',
       'The next sentence keeps going with water and bailing.',
       'The one after that adds a course and lifeboats.',
       'One comparison carried through multiple sentences is an extended metaphor.'],
      '**Extended metaphor.** A standard metaphor would have stopped after "the project was a ship"; '
      'what makes this extended is that every following sentence stays inside it.',
      'Extended metaphors can run for a whole chapter, or a whole book.')
    Q[-1]['passage'] = ('The project was a ship. For two months it took on water faster than anyone '
                        'could bail, and by October the crew had stopped arguing about the course '
                        'and started arguing about the lifeboats.')

    q(Q, 3, 'A captain calls for “all hands on deck.” What is that phrase doing?',
      ['Naming a part to stand for whole people',
       'Naming a whole to stand for one small part',
       'Replacing a harsh phrase with a gentler one',
       'Exaggerating how many people are needed'], 0,
      'Hands are not what the captain actually wants on the deck.',
      ['The captain needs whole sailors, not detached hands.',
       'A hand is a part of a person.',
       'The part is being used to mean the entire person.',
       'A part standing for a whole is synecdoche.'],
      '**Synecdoche, running from part to whole.** It can also run the other way — "Washington '
      'decided" uses a whole city to mean a handful of officials in it.',
      'Hands for workers is the oldest example there is, and it survives in "farmhand" and "ranch hand."')

    q(Q, 3, 'A writer describes a character’s cluttered attic as “her own Pandora’s box.” What is '
            'that reference doing?',
      ['Deepening understanding by pointing outside the work',
       'Comparing two things directly using “like” or “as”',
       'Giving a human quality to something inanimate',
       'Repeating an opening sound across nearby words'], 0,
      'The phrase borrows something the reader is assumed to already know.',
      ['There is no “like” or “as,” so it is not a simile.',
       'The attic is not given any human quality.',
       'No sound is being repeated.',
       'A reference that borrows outside knowledge to deepen understanding is an allusion.'],
      '**Allusion.** It imports a whole story in three words — a box that should not be opened, and '
      'everything that escaped when it was.',
      'It only works if the reader knows the reference, which is the risk every allusion takes.')

    build('ad-astra', C, Q, 'unit-eng-t1-fig',
          'Test 1 · 5 Figurative Language', 'english',
          'Seventeen devices: simile, the three metaphors, personification, imagery and its five '
          'senses, hyperbole, understatement, litotes, euphemism, synecdoche, oxymoron, pun, '
          'allusion, alliteration, anaphora and idiom.',
          'This is the longest list on the test and the one most likely to be examined by handing you '
          'a sentence and asking what is happening in it — which is a different skill from reciting '
          'the definitions.',
          [('Name all seventeen devices from the lesson', 'source'),
           ('Tell standard, implied and extended metaphor apart', 'added'),
           ('Name all five kinds of imagery and the sense each one uses', 'source'),
           ('Separate understatement from litotes, and alliteration from anaphora', 'added'),
           ('Read a fresh sentence and name the device at work in it', 'added')],
          'Built from Sedona’s own handwritten notes. One thing worth a word: her pun line reads '
          '"words that sound the same but have different meanings", which describes one kind of pun '
          'rather than all of them — a pun can also turn on a single word carrying two meanings at '
          'once, with no sound trick. The card here teaches both and the question uses the '
          'sound-alike kind, so nothing on the test can catch her out either way. Everything else on '
          'both pages checks out, including litotes, which is the term most often written down wrong. '
          'Every example in the questions is fresh, so none of them can be answered from memory of her '
          'page.',
          ('Seventeen devices is a lot to hold at once. The two pairs that actually cost marks are understatement against litotes, and alliteration against anaphora.', 18),
          'content/eng-t1-fig.json', SRC,
          'Test 1 notes · Figurative Language (student’s own notes)',
          prep_=True, libv_=1)


# ──────────────────────────────────────────────────────── 6 · Symbolism and Motifs
def symbolism():
    C, Q = [], []

    card(C, 'Symbol',
         "**Something used to represent an idea.**"
         "\n• The object stays itself and also stands for something larger."
         "\n• A symbol can appear once and still be a symbol.",
         hint='A thing, plus an idea riding on it.')
    card(C, 'Intangible symbols: numbers',
         "**Zero is mystery or emptiness, thirteen is evil and misfortune, three signifies "
         "fulfillment.**"
         "\n• These are traditional associations, carried by centuries of use."
         "\n• A writer can lean on them without explaining them.",
         hint='Three is the number that completes something.')
    card(C, 'Nature symbols',
         "**Dawn is new beginnings, light is knowledge, truth and safety, darkness is evil and "
         "ignorance, flowers are beauty and youth.**"
         "\n• Seasons carry meaning too — spring for beginnings, winter for endings."
         "\n• Light and darkness are the oldest paired opposites in literature.",
         hint='Dawn is where the day begins, so it is where things begin.')
    card(C, 'Weather symbols',
         "**Fog and mist are isolation, rain is sadness or despair, wind and storms are violence, "
         "lightning is power and strength.**"
         "\n• Weather is the easiest symbol for a writer to put on a page unnoticed."
         "\n• Which is exactly why it is worth noticing.",
         hint='Fog cuts you off from everything. That is isolation.')
    card(C, 'Symbols in life',
         "**Signs and flags are symbols you already read fluently every day.**"
         "\n• A red octagon means stop before you have read the word."
         "\n• Nobody thinks a flag is a country, and nobody is confused by that.",
         hint='You have been reading symbols since long before English class.')
    card(C, 'Symbols in literature',
         "**In Flipped the eggs symbolize friendship; in the Narrative of the Life of Frederick "
         "Douglass the white-sailed ships represent freedom.**"
         "\n• A Midsummer Night's Dream uses the love potion for how arbitrary love can be."
         "\n• Three books, three ordinary objects, three large ideas.",
         hint='An egg, a sail and a potion.')
    card(C, 'Why use symbols',
         "**They help a reader visualize complex ideas and track the story's progress.**"
         "\n• An idea is hard to hold; an object is easy."
         "\n• Watching an object change across a book is one way of watching the story move.",
         hint='It gives an abstract idea something to sit on.')
    card(C, 'Motif',
         "**A concrete object or idea that repeats throughout the text.**"
         "\n• Motifs have deeper meanings that lead back to the theme."
         "\n• Repetition is the definition, not a bonus feature.",
         hint='If it only happens once, it is not a motif.')
    card(C, 'Motif examples',
         "**In To Kill a Mockingbird the mockingbird stands for innocent people; in A Midsummer "
         "Night's Dream the forest stands for chaos and confusion.**"
         "\n• Both return again and again rather than appearing once."
         "\n• Both point at what their book is actually about.",
         hint='A bird and a wood, each turning up over and over.')
    card(C, 'Why use motifs',
         "**They help the author and the reader organize the themes of the work.**"
         "\n• They weave the parts of a text together."
         "\n• They remind a reader of the theme through vivid and memorable imagery.",
         hint='A thread running through, holding the parts together.')
    card(C, 'Symbol or motif?',
         "**A symbol can appear once; a motif has to repeat.**"
         "\n• Every motif is doing symbolic work, so “symbol” is never the wrong word for one."
         "\n• But only repetition earns the word motif.",
         hint='Count the appearances. That settles it.')
    card(C, 'Motif or theme?',
         "**A motif is concrete and repeats; the theme is the idea it leads back to.**"
         "\n• The mockingbird is the motif; what a book says about harming the innocent is the theme."
         "\n• You can point at a motif. You can only state a theme.",
         hint='One you can draw. One you can only say.')
    card(C, 'The list is a starting point',
         "**Traditional meanings tell you what to check, never what to conclude.**"
         "\n• Rain is despair in one book and relief after a drought in another."
         "\n• The book you are actually reading always outranks the list.",
         hint='Check the list, then check the book.')
    card(C, 'Reading a symbol well',
         "**Say what the object is, what idea it carries, and how you know.**"
         "\n• The “how you know” is the evidence, and it is where the marks are."
         "\n• Without it, an interpretation is a guess with a confident voice.",
         hint='Object, idea, evidence.')

    q(Q, 1, 'What does a symbol do?',
      ['Represents an idea', 'Repeats through a whole text',
       'Compares two unlike things', 'States the author’s attitude'], 0,
      'One of the wrong answers is the definition of a motif.',
      ['Repeating through a text is what makes something a motif.',
       'Comparing two unlike things is a metaphor.',
       'Stating the author’s attitude is tone.',
       'A symbol is something used to represent an idea.'],
      '**A symbol is something used to represent an idea.** It stays itself and carries something '
      'larger at the same time.',
      'Motif is the closest neighbour, and repetition is the whole difference.')

    q(Q, 1, 'Traditionally, what does dawn symbolize?',
      ['New beginnings', 'Evil and ignorance', 'Sadness or despair', 'Beauty and youth'], 0,
      'Think about what part of the day it is.',
      ['Evil and ignorance are carried by darkness.',
       'Sadness or despair is carried by rain.',
       'Beauty and youth are carried by flowers.',
       'Dawn is where a day begins, and it symbolizes new beginnings.'],
      '**Dawn symbolizes new beginnings.** It sits on the nature list beside light, darkness, flowers '
      'and the seasons.',
      'Ending a chapter at sunrise is a choice, and this is usually what the choice is doing.')

    q(Q, 1, 'Traditionally, what do fog and mist symbolize?',
      ['Isolation', 'Fulfillment', 'Power', 'Beauty'], 0,
      'What does fog actually do to somebody standing in it?',
      ['Fulfillment is carried by the number three.',
       'Power and strength are carried by lightning.',
       'Beauty and youth are carried by flowers.',
       'Fog cuts a person off from everything around them, which is isolation.'],
      '**Fog and mist symbolize isolation.** The physical effect and the symbolic meaning are the '
      'same thing, which is why it is easy to remember.',
      'Weather is the easiest symbol to slip onto a page unnoticed, so it is worth noticing.')

    q(Q, 1, 'Traditionally, what does the number thirteen symbolize?',
      ['Evil and misfortune', 'Mystery or emptiness',
       'Peace and fulfillment', 'Knowledge and truth'], 0,
      'Think about which floor some buildings skip.',
      ['Mystery or emptiness belongs to zero.',
       'Fulfillment belongs to three.',
       'Knowledge and truth belong to light.',
       'Thirteen symbolizes evil and misfortune.'],
      '**Thirteen symbolizes evil and misfortune** — an association strong enough that real buildings '
      'still skip the floor.',
      'Zero, thirteen and three are the three numbers on her list, and each carries a different idea.')

    q(Q, 1, 'What makes something a motif rather than only a symbol?',
      ['It repeats throughout the text', 'It appears in the opening chapter',
       'It is named in the book’s own title', 'It is described in great detail'], 0,
      'One word in the definition of a motif is doing all the work.',
      ['Where it first appears does not matter.',
       'Plenty of motifs are never in a title.',
       'A single vivid description is still a single appearance.',
       'A motif is a concrete object or idea that repeats throughout the text.'],
      '**Repetition is what earns the word motif.** A symbol can do its job in one appearance; a '
      'motif is defined by coming back.',
      'Which is why counting appearances settles almost every symbol-or-motif question.')

    q(Q, 1, 'Traditionally, what does lightning symbolize?',
      ['Power and strength', 'Sadness and despair',
       'Beauty and youth', 'Truth and safety'], 0,
      'Think about what lightning is, physically.',
      ['Sadness and despair belong to rain.',
       'Beauty and youth belong to flowers.',
       'Truth and safety belong to light.',
       'Lightning symbolizes power and strength.'],
      '**Lightning symbolizes power and strength.** It sits on the weather list with fog, rain, and '
      'wind and storms.',
      'Wind and storms carry violence, which is close but not the same idea.')

    q(Q, 2, 'A novel opens on a grey morning with mist across the fields, and its main character has '
            'just moved to a town where she knows nobody. What is the mist most likely doing?',
      ['Signalling how isolated she is', 'Promising her a new beginning',
       'Warning of violence to come', 'Marking her growing power'], 0,
      'Match the weather to what the sentence already tells you about her.',
      ['She has just arrived somewhere she knows nobody.',
       'That is a description of being cut off from other people.',
       'Fog and mist traditionally symbolize isolation.',
       'The weather and her situation are saying the same thing.'],
      '**Isolation.** The test is not whether the traditional meaning exists but whether it fits what '
      'is actually happening — and here the two line up exactly.',
      'When the weather and the situation agree, the symbol is doing its job quietly and well.')

    q(Q, 2, 'A story ends at sunrise, with a character walking out of a house she has decided to '
            'leave for good. What does the timing most likely symbolize?',
      ['A new beginning for her', 'An approaching danger',
       'A loss of knowledge', 'A return to childhood'], 0,
      'The author could have set this at any hour and chose one.',
      ['She has just made a decision to leave something behind.',
       'Leaving one life behind means starting another.',
       'Dawn traditionally symbolizes new beginnings.',
       'Setting the scene at sunrise reinforces what the plot already did.'],
      '**A new beginning.** This is symbolism at its most ordinary and most effective — the time of '
      'day agreeing with the decision, without a word of explanation.',
      'Ask of any scene: why THIS time of day, this weather, this season? Usually there is an answer.')

    q(Q, 2, 'A play returns to a pair of broken spectacles in its first act, its fourth act and its '
            'closing line. What is that?',
      ['A motif', 'A setting', 'A theme', 'A narrator'], 0,
      'The question tells you how many times the object appears.',
      ['A setting is where a scene happens, not an object in it.',
       'A theme is an idea, and spectacles are an object.',
       'A narrator is a voice, not a prop.',
       'A concrete object repeating throughout a text is a motif.'],
      '**A motif.** Three appearances spread across the whole play is exactly the repetition the '
      'definition asks for.',
      'The next question a test would ask is what the spectacles MEAN — motifs have deeper meanings that lead back to the theme.')

    q(Q, 2, 'Why do authors use symbols?',
      ['To help a reader visualize complex ideas',
       'To keep a plot from needing a real climax',
       'To make every chapter the same length',
       'To tell a reader exactly what to feel'], 0,
      'Symbols are doing a job an abstract idea cannot do by itself.',
      ['Ideas like freedom or grief are hard to hold in your head.',
       'An object is easy to hold in your head.',
       'A symbol gives the idea something concrete to sit on.',
       'Symbols help a reader visualize complex ideas and track the story’s progress.'],
      '**Symbols make an abstract idea visible, and let a reader track a story’s progress.** '
      'Watching an object change across a book is one way of watching the story itself move.',
      'They also work without being explained, which a direct statement of the idea never does.')

    q(Q, 2, 'Why do motifs help a reader hold on to a theme?',
      ['Vivid repeated imagery is memorable',
       'Themes are always stated in chapter one',
       'A motif can replace the need for a plot',
       'Repetition makes a book shorter to read'], 0,
      'Think about what repetition does to a reader’s memory.',
      ['A theme is an idea, and ideas are easy to lose across three hundred pages.',
       'A motif is concrete and turns up again and again.',
       'Each reappearance reminds a reader of the idea it carries.',
       'Motifs remind a reader of the theme through vivid and memorable imagery.'],
      '**Motifs weave the parts of a text together and keep the theme in front of a reader.** That is '
      'the work they do for the author as well — organising the themes while writing.',
      'It is also why a motif you notice early makes the rest of the book easier to read.')

    q(Q, 2, 'In To Kill a Mockingbird a mockingbird turns up again and again and stands for innocent '
            'people. Which term covers that?',
      ['Motif', 'Allusion', 'Euphemism', 'Setting'], 0,
      'Two facts are given: it repeats, and it stands for something.',
      ['An allusion points outside the work to something else.',
       'A euphemism softens a harsh word.',
       'A setting is where the story happens.',
       'A concrete object that repeats and carries a deeper meaning is a motif.'],
      '**A motif.** It is also fair to call it a symbol — every motif does symbolic work — but the '
      'repetition is what makes motif the more precise word.',
      'And its deeper meaning leads straight back to the theme, which is what motifs are for.')

    q(Q, 3, 'One novel uses rain for grief; another uses rain for relief after a long drought. What '
            'does that tell you about the traditional meanings?',
      ['They are starting points, not fixed rules',
       'One of the two authors has used it wrongly',
       'Rain cannot be a symbol in either novel',
       'A symbol means whatever a reader decides'], 0,
      'Both books are using rain deliberately, and they disagree.',
      ['Neither author is making a mistake — both choices are deliberate.',
       'Rain is clearly working as a symbol in both.',
       'But it is not working as the same symbol.',
       'So the traditional meaning is something to check against the book, not a key to it.'],
      '**The list tells you what to check; the book tells you what to conclude.** Rain means sadness '
      'or despair by tradition, and a farmer watching a drought break would tell you otherwise.',
      'The last wrong answer goes too far the other way — a reading still has to be supported by the text.')

    q(Q, 3, 'A character carries the same chipped pocket watch in every chapter, and each time it '
            'appears somebody is running out of time. What is the watch, and what does it lead to?',
      ['A motif, leading back to the theme',
       'A theme, leading back to the plot',
       'A setting, leading back to the mood',
       'An allusion, leading back to history'], 0,
      'Two things have to be named: what the watch IS, and where it points.',
      ['It is a concrete object appearing in every chapter, so it is a motif.',
       'A theme is an idea rather than an object, so the watch cannot be one.',
       'Motifs have deeper meanings that lead back to the theme.',
       'So the watch is the motif and the theme is what it keeps pointing at.'],
      '**A motif, leading back to the theme.** The watch is what you can point at; what the book is '
      'saying about time running out is what you can only state.',
      'A good answer on a test names both halves — the object and the idea it carries.')

    q(Q, 3, 'What separates a motif from the theme it points at?',
      ['A motif is concrete; a theme is an idea',
       'A motif is always shorter than a theme',
       'A motif appears in poetry but not prose',
       'A motif is stated while a theme is hidden'], 0,
      'One of these you could photograph.',
      ['A motif is a concrete object or idea that repeats.',
       'A theme is what the book is saying, which has no physical form.',
       'Motifs appear in every kind of writing, not only poetry.',
       'And a theme is usually the thing NOT stated outright.'],
      '**You can point at a motif; you can only state a theme.** The motif is the concrete thing '
      'that keeps returning, and the theme is the idea all that returning adds up to.',
      'This is why "the mockingbird" is not a theme — it is the motif that leads to one.')

    q(Q, 3, 'A writer wants a reader to feel a character’s hope growing, without ever using the '
            'word. Which choice does that work?',
      ['Letting the light grow across the chapters',
       'Naming the feeling in every single chapter',
       'Repeating the number thirteen throughout',
       'Setting each new scene in heavier fog'], 0,
      'Two of the wrong answers use symbols that carry the opposite idea.',
      ['Naming the feeling is exactly what the writer said she would not do.',
       'Thirteen traditionally carries misfortune, not hope.',
       'Fog carries isolation, which would work against hope.',
       'Light traditionally carries knowledge, truth and safety, and growing light carries growing hope.'],
      '**Light, growing across the book.** This is a motif doing what motifs do — repeating, changing '
      'a little each time, and letting a reader track the story’s progress without narration.',
      'Notice both wrong symbols were real symbols, just ones carrying the wrong idea.')

    q(Q, 3, 'A flag and a wedding ring do the same job in real life that a symbol does in a novel. '
            'What job is that?',
      ['Standing for an idea bigger than itself',
       'Repeating until a reader has to notice it',
       'Replacing a harsh word with a gentler one',
       'Exaggerating something to emphasize a point'], 0,
      'Nobody confuses a ring with a marriage, and nobody needs it explained.',
      ['A ring is a small circle of metal that stands for a promise.',
       'A flag is a piece of cloth that stands for a country.',
       'In both cases the object is ordinary and the idea is large.',
       'Something used to represent an idea is a symbol.'],
      '**Standing for an idea larger than itself.** Signs and flags are the everyday version, and '
      'nobody finds them confusing — which is worth remembering when a symbol in a novel feels hard.',
      'Repetition, euphemism and exaggeration are three other devices, each doing a different job.')

    build('ad-astra', C, Q, 'unit-eng-t1-sym',
          'Test 1 · 6 Symbolism and Motifs', 'english',
          'What a symbol is, the traditional meanings of numbers, nature and weather, symbols in life '
          'and in three books her class has read, what a motif is and how it differs from a symbol '
          'and from a theme, and why writers use both.',
          'Symbol and motif are the two terms an essay question is most likely to ask her to USE '
          'rather than define, and the difference between them is one word: repetition.',
          [('Define a symbol and a motif and tell them apart', 'source'),
           ('Recall the traditional meanings for numbers, nature and weather', 'source'),
           ('Say why writers use symbols and motifs', 'source'),
           ('Read a scene and say what an object is carrying', 'added'),
           ('Separate a motif from the theme it leads back to', 'added')],
          'Built from Sedona’s own handwritten notes, and the pages check out throughout. One '
          'teaching choice worth naming: her notes give the traditional meanings as a list, and this '
          'unit adds a card and a question saying outright that the list is a starting point rather '
          'than a key — rain means despair by tradition and relief to a farmer in a drought. That is '
          'not a correction to anything on her page; it is the step between memorising the list and '
          'being able to use it on a book, which is what an essay question will actually ask for. Her '
          'class’s three literature examples (Flipped, the Frederick Douglass narrative, A Midsummer '
          'Night’s Dream) are on the cards exactly as she has them.',
          ('The traditional meanings are quick to learn. Spend the time instead on symbol against motif, and motif against theme.', 15),
          'content/eng-t1-sym.json', SRC,
          'Test 1 notes · Symbolism and Motifs (student’s own notes)',
          prep_=True, libv_=1)


# ───────────────────────────────────────────── 7 · To Kill a Mockingbird background
def tkam():
    C, Q = [], []

    card(C, 'Harper Lee',
         "**The author of To Kill a Mockingbird.**"
         "\n• She published it in 1960."
         "\n• Almost everything in the novel's world comes from somewhere in her own.",
         hint='One book, one name, one enormous reputation.')
    card(C, 'A small town of her own',
         "**She grew up in a small town, and Maycomb is based on it.**"
         "\n• Maycomb itself is invented; the kind of place it is, is not."
         "\n• Knowing a town that well is why the novel's background detail is so exact.",
         hint='She did not have to research the setting.')
    card(C, 'Her father the lawyer',
         "**Her father was a lawyer, and she studied law herself before dropping out to write.**"
         "\n• A small-town lawyer sits at the center of the novel."
         "\n• She knew the world of a county courthouse from the inside.",
         hint='She left the law, and then wrote about it.')
    card(C, 'Published in 1960',
         "**To Kill a Mockingbird was published in 1960.**"
         "\n• It was her first novel."
         "\n• It won the Pulitzer Prize the following year.",
         hint='1960 — a quarter century after the events in it.')
    card(C, 'The airline clerk years',
         "**She worked as an airline clerk while trying to get the book written.**"
         "\n• Friends eventually gave her money so she could write full time."
         "\n• The novel exists partly because somebody funded a year of her life.",
         hint='A day job, and then a gift that ended it.')
    card(C, 'Maycomb, Alabama, 1933–1935',
         "**The novel is set in the invented town of Maycomb, Alabama, between 1933 and 1935.**"
         "\n• Two years, one town, one county courthouse."
         "\n• Every one of the three conditions below is true of that place in those years.",
         hint='Alabama, the mid-1930s, two years.')
    card(C, 'The 1930s: the Great Depression',
         "**The novel is set during the Great Depression.**"
         "\n• Almost nobody in Maycomb has money, and the novel says so constantly."
         "\n• Poverty is the pressure under every conflict in the book.",
         hint='Nobody in the town has anything to spare.')
    card(C, 'The 1930s: prejudice and legal segregation',
         "**Segregation in the 1930s South was not merely a custom — it was written into law.**"
         "\n• That is what the word “legal” is doing on your page."
         "\n• The courthouse in the novel is operating inside that system, not outside it.",
         hint='Not just how people behaved — how the law was written.')
    card(C, 'The 1930s: ignorance',
         "**Ignorance is named as the third condition of the setting.**"
         "\n• Schooling was limited, and reliable information was scarce."
         "\n• Prejudice and ignorance hold each other up, which is why both are on the list.",
         hint='The third leg, holding the other two up.')
    card(C, 'Why the setting matters',
         "**Depression, legal segregation and ignorance are the pressure the plot runs on.**"
         "\n• Move the same story to another decade and most of it stops working."
         "\n• A setting question on a test is usually really a question about that pressure.",
         hint='The setting is not scenery here. It is the engine.')
    card(C, 'Set in the 1930s, written in the 1950s',
         "**The events are 1933–1935; the book was published in 1960.**"
         "\n• So it is a book looking BACK at that decade, not a report from inside it."
         "\n• Twenty-five years, and the beginning of the civil rights movement, sit in that gap.",
         hint='A quarter of a century between the story and the telling.')

    q(Q, 1, 'Who wrote To Kill a Mockingbird?',
      ['Harper Lee', 'Flannery O’Connor', 'Eudora Welty', 'Carson McCullers'], 0,
      'All four are Southern writers. Only one wrote this novel.',
      ['Flannery O’Connor wrote short stories set in Georgia.',
       'Eudora Welty wrote about Mississippi.',
       'Carson McCullers wrote The Heart Is a Lonely Hunter.',
       'To Kill a Mockingbird is Harper Lee’s.'],
      '**Harper Lee.** The other three are real Southern writers of roughly the same era, which is '
      'worth knowing on its own — this was not a lone voice in an empty room.',
      'It was her first novel, and for most of her life it was her only published one.')

    q(Q, 1, 'In what year was To Kill a Mockingbird published?',
      ['1960', '1935', '1947', '1972'], 0,
      'It was published well after the years it describes.',
      ['The novel is set between 1933 and 1935.',
       'It was not published anywhere near those years.',
       'Nor was it published as late as the 1970s.',
       'It was published in 1960.'],
      '**1960**, which is a quarter of a century after the events it describes. That gap is worth '
      'holding on to — the book looks back at the 1930s rather than reporting from inside it.',
      'It won the Pulitzer Prize the year after publication.')

    q(Q, 1, 'Where and when is the novel set?',
      ['Maycomb, Alabama, 1933 to 1935', 'Mobile, Alabama, 1919 to 1921',
       'Maycomb, Georgia, 1947 to 1949', 'Monroeville, Tennessee, 1955'], 0,
      'Three of the four get either the place or the years wrong.',
      ['The state is Alabama.',
       'The town is Maycomb, which is invented.',
       'The years are the middle of the 1930s.',
       'Maycomb, Alabama, 1933 to 1935.'],
      '**Maycomb, Alabama, 1933 to 1935.** Two years in one small town, and the county courthouse is '
      'at the center of them.',
      'Maycomb is invented, but it is built out of a real small town the author knew.')

    q(Q, 1, 'What was Harper Lee’s father’s profession?',
      ['Lawyer', 'Doctor', 'Minister', 'Teacher'], 0,
      'Think about the profession at the center of the novel.',
      ['The novel puts a small-town lawyer at its center.',
       'The author studied law herself before leaving to write.',
       'That interest did not come from nowhere.',
       'Her father was a lawyer.'],
      '**Her father was a lawyer**, and she studied law herself before dropping out to become a '
      'writer — which is why the novel’s courthouse feels observed rather than researched.',
      'Writing what you know is a cliché, but it is a fair description of what happened here.')

    q(Q, 2, 'Harper Lee studied law and left before finishing. How does that show up in the novel?',
      ['It centers on a small-town lawyer',
       'It is narrated entirely by a judge',
       'It quotes a statute in every chapter',
       'It was written inside a real courtroom'], 0,
      'Ask what the novel actually does with the law, not what it could have done.',
      ['The novel is not narrated by a judge.',
       'It does not quote statutes at a reader.',
       'What it does is put a lawyer, and a trial, at its heart.',
       'A small-town lawyer is the center of the book.'],
      '**The novel centers on a small-town lawyer**, which is both her father’s profession and the '
      'career she started and left.',
      'Knowing a world from the inside shows up as confidence in the background detail, not as legal jargon.')

    q(Q, 2, 'Before the novel was published, how did Harper Lee support herself?',
      ['By working as an airline clerk', 'By practicing law in Alabama',
       'By teaching at a local school', 'By writing for a newspaper'], 0,
      'She was not making a living from writing yet.',
      ['She never finished her law degree, so she was not practicing.',
       'She was not teaching or reporting either.',
       'She had an ordinary job that had nothing to do with books.',
       'She worked as an airline clerk.'],
      '**She worked as an airline clerk** while trying to get the book written — a detail worth '
      'keeping, because it says something true about how long books take.',
      'The job ended when friends gave her money to write full time.')

    q(Q, 2, 'What let Harper Lee stop working and write full time?',
      ['A gift of money from friends', 'The success of an earlier novel',
       'A university research grant', 'A contract to write a screenplay'], 0,
      'It was not the book that paid for the book.',
      ['This was her first novel, so no earlier one had made money.',
       'No university or studio was involved.',
       'The money came from people who knew her.',
       'Friends gave her money so she could write full time.'],
      '**Friends funded a year of her life so she could finish it.** The novel exists partly because '
      'somebody decided it was worth paying for before anyone had read a word.',
      'Worth remembering next time a book seems to have appeared out of nowhere.')

    q(Q, 2, 'Which set names the three conditions of the 1930s that shape the novel?',
      ['Depression, segregation, ignorance', 'War, rationing, and migration',
       'Industry, immigration, and growth', 'Prohibition, radio, and drought'], 0,
      'All four sets describe real features of some part of American history.',
      ['Rationing and mass migration belong to the 1940s.',
       'Industry and immigration describe a different era and a different region.',
       'Prohibition had ended by 1933.',
       'The three named conditions are the Great Depression, prejudice with legal segregation, and ignorance.'],
      '**The Great Depression, prejudice and legal segregation, and ignorance.** These three are not '
      'background colour — they are the pressure the whole plot runs on.',
      'Move the same story to a wealthier decade and most of it stops working.')

    q(Q, 3, 'Maycomb is invented, but it is built out of something real. What?',
      ['The small town the author grew up in',
       'A town she read about in a court record',
       'A city she moved to as a grown adult',
       'A town invented for an earlier novel'], 0,
      'She did not need to research what a small Alabama town was like.',
      ['This was her first novel, so there is no earlier one to borrow from.',
       'She did not build it from documents or from a city.',
       'She grew up in a small Southern town herself.',
       'Maycomb is based on the town she grew up in.'],
      '**Maycomb is invented, and the kind of place it is is not.** That is why its background detail '
      '— who knows whom, who owes whom, what everybody has always said — reads as observed.',
      'Inventing the name gave her freedom; knowing the real place gave her the detail.')

    q(Q, 3, 'The novel describes 1933 to 1935 but was published in 1960. Why does that gap matter?',
      ['It looks back on the 1930s from later',
       'It was written while those events happened',
       'It means the dates inside it are unreliable',
       'It shows the author never visited Alabama'], 0,
      'Twenty-five years is long enough for the country to have changed.',
      ['A book published in 1960 was not written during 1933.',
       'The dates inside the novel are perfectly clear.',
       'The author grew up in Alabama, so she certainly visited.',
       'The novel is looking back across twenty-five years at a decade that was already over.'],
      '**It is a book about the past, written later, for readers living in a changed country.** The '
      'beginning of the civil rights movement sits inside that twenty-five-year gap.',
      'A novel written from inside the 1930s would have been a different book entirely.')

    q(Q, 3, 'Why does the Great Depression matter to a story about one small Alabama town?',
      ['Poverty sharpens every conflict in it',
       'It explains why the town has no school',
       'It is the reason the novel has a narrator',
       'It places the story outside the South'], 0,
      'Think about what having no money does to a disagreement between neighbours.',
      ['The town does have a school; that is not what the Depression explains.',
       'Every novel has a narrator, Depression or not.',
       'The Depression does not move the story anywhere.',
       'What it does is put every person in the town under financial pressure.'],
      '**Poverty is the pressure under every conflict in the book.** When nobody has anything to '
      'spare, ordinary disagreements get harder and pride gets more expensive.',
      'The setting here is not scenery — it is closer to being the engine.')

    q(Q, 3, 'Segregation in the 1930s South is described as LEGAL. What does that word add?',
      ['The unfairness was written into the law',
       'It only applied inside actual courtrooms',
       'It was enforced by one county judge alone',
       'It had already ended by the mid-1930s'], 0,
      'Compare a rule people follow out of habit with a rule a court will enforce.',
      ['It had not ended — it lasted decades longer.',
       'It was not the decision of any single judge.',
       'It reached far beyond courtrooms into schools, buses and shops.',
       'Legal means the system itself required it, rather than merely tolerating it.'],
      '**Legal segregation means the unfairness was the law, not a departure from it.** That is why a '
      'trial in this novel is happening inside the system rather than against it.',
      'It is the difference between breaking the rules and the rules themselves being the problem.')

    build('ad-astra', C, Q, 'unit-eng-t1-tkam',
          'Test 1 · 7 To Kill a Mockingbird: Background', 'english',
          'Harper Lee, the small town behind Maycomb, her father’s profession and her own abandoned '
          'law degree, the 1960 publication, how the book got written, and the setting: Maycomb, '
          'Alabama, 1933 to 1935, under the Depression, legal segregation and ignorance.',
          'This is the short, factual part of the test — the kind where every mark is available if you '
          'have the dates and the three conditions of the setting straight.',
          [('Name the author, the publication year, and the setting in place and time', 'source'),
           ('Say how Harper Lee’s own life reaches into the novel', 'source'),
           ('Name the three conditions of the 1930s that shape the book', 'source'),
           ('Explain why each of those three matters to the plot', 'added'),
           ('Say what the gap between the setting and the publication changes', 'added')],
          'Built from Sedona’s own handwritten notes, and every factual claim on her page was checked '
          'independently — the author, the 1960 publication, the father’s profession, the abandoned '
          'law degree, the airline job, the friends who funded the writing year, and the 1933 to 1935 '
          'dating all hold up. Scoped deliberately against the reading companion she already has for '
          'chapters 1 to 5: that unit covers plot, characters and the Boo Radley material and contains '
          'none of this, so there is nothing repeated between them. Nothing here reaches past chapter '
          'five of the novel, so it is safe to approve whatever she has read so far.',
          ('Short and mostly factual. Get the year, the place and the three conditions of the 1930s solid and this part is free marks.', 10),
          'content/eng-t1-tkam.json', SRC,
          'Test 1 notes · To Kill a Mockingbird background (student’s own notes)',
          prep_=True, libv_=1)


if __name__ == '__main__':
    figurative()
    symbolism()
    tkam()
