# Latin I · Vocabulary Quiz 1 (v202) — from "quiz - Oct 2.pdf" (Latin folder,
# Drive, uploaded 2026-10-02): a one-page typed list of fifteen dictionary
# entries, with two handwritten notes beside it (amica, and "big" for magnus).
# The list is the source; every derivative hook and every grammar call that
# the list does not print is flagged 'added'.
#
# `sp` respellings follow the pronunciation unit's own convention (CAPS for
# stress, v = w, c and g always hard) and were worked syllable by syllable:
# agricola stresses -GRI- because its next-to-last syllable is short and open;
# audio and video stress their first syllable for the same reason.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

C, Q = [], []
def W(term, sp, d, hint, frm='source'):
    card(C, term, d, hint, frm=frm)
    C[-1]['sp'] = sp

W('agricola', 'ah-GREE-koh-lah',
  '**farmer** — *agricola, agricolae*, m.\n• First declension like *puella*, but MASCULINE, because a farmer in Rome was a man.\n• So an adjective with it takes the masculine form: *agricola magnus*.',
  'agri- is a field, as in AGRIculture.')
W('amicus', 'ah-MEE-koos',
  '**friend** — *amicus, amici*, m.\n• Second declension.\n• A female friend is *amica, amicae*, f.',
  'An AMICable person is friendly.')
W('amo', 'AH-moh',
  '**to love** — *amo, amare, amavi, amatus*\n• *amo* on its own means I love; *amare* is to love.\n• First conjugation: the infinitive ends in -are.',
  'An AMATeur does it for love, not for pay.')
W('audio', 'OW-dee-oh',
  '**to hear** — *audio, audire, audivi, auditus*\n• Fourth conjugation: the infinitive ends in -ire.\n• *audis* you hear · *audit* he or she hears.',
  'AUDIO is what you hear; an AUDIence listens.')
W('deus', 'DAY-oos',
  '**god** — *deus, dei*, m.\n• Second declension.',
  'A DEIty is a god.')
W('donum', 'DOH-noom',
  '**gift** — *donum, doni*, n.\n• Second declension, NEUTER: that is what the n. means.\n• Plural *dona*, gifts.',
  'When you DONate, you give a gift.')
W('do', 'doh',
  '**to give** — *do, dare, dedi, datus*\n• *do* is I give; *dare* is to give.\n• The third part, *dedi* (I gave), does not follow the pattern, so it has to be learned.',
  'DATA are things that are "given".')
W('magnus', 'MAHG-noos',
  '**great, big** — *magnus, magna, magnum*\n• An adjective: the three forms are masculine, feminine and neuter.\n• *magnum donum* — a big gift.',
  'MAGNIFY makes something look bigger.')
W('multus', 'MOOL-toos',
  '**many** — *multus, multa, multum*\n• Many in the plural: *multi pueri*, many boys. In the singular it means much.\n• *multa dona* — many gifts.',
  'MULTIply makes many of something.')
W('-ne (question suffix)', 'nay',
  '**A suffix added to the first word of a sentence that turns it into a yes/no question.**\n• *Videt.* He sees. → *Videtne?* Does he see?\n• It is not a separate word, so it has no meaning of its own.',
  'Think of it as a spoken question mark, attached to the front.')
W('sed', 'sed',
  '**but**\n• *Puella videt, sed non audit.* The girl sees, but she does not hear.',
  'It joins two ideas that pull in different directions.')
W('puella', 'poo-EL-lah',
  '**girl** — *puella, puellae*, f.\n• First declension, the model word for it.',
  'Two l-sounds in the middle, both said.')
W('puer', 'POO-er',
  '**boy** — *puer, pueri*, m.\n• Second declension. The e stays in every form: *pueri*, not *puri*.',
  'Watch for puer next to puella: boy and girl.')
W('non', 'nohn',
  '**not**\n• It goes just before the word it makes negative, usually the verb: *Puer non audit.* The boy does not hear.',
  'NON-fiction is NOT made up.')
W('video', 'WEE-deh-oh',
  '**to see** — *video, videre, vidi, visus*\n• Second conjugation: the infinitive ends in -ere, with a long e.\n• *videt* he or she sees.',
  'A VIDEO is something you see; VISion comes from visus.')

V = ['to hear', 'to see', 'to give', 'to love']
# ---------------- level 1: recall
q(Q, 1, 'What does *audio* mean?', V, 0,
  'Think of something you put in your ears.',
  ['*audio* is a verb, so the answer is a verb.', 'English kept the word: an audio track is something you listen to.', 'So *audio* means to hear.'],
  '***audio* means to hear.** It is a fourth-conjugation verb: *audio, audire, audivi, auditus*.',
  'audio, audience, audible — all about hearing.')
q(Q, 1, 'What does *donum* mean?', ['gift', 'god', 'friend', 'farmer'], 0,
  'What do you hand over when you donate?',
  ['*donum* is a noun, so look for a thing or person.', 'The English word donate keeps its root.', 'A donation is a gift, so *donum* means gift.'],
  '***donum* means gift.** It is neuter: *donum, doni*, n.',
  'Do not mix it up with *deus*, god — both start with d.')
q(Q, 1, 'What does *puer* mean?', ['boy', 'girl', 'friend', 'god'], 0,
  'It is the masculine partner of *puella*.',
  ['*puella* is the girl.', '*puer* is the word that sits beside it on the list.', 'So *puer* means boy.'],
  '***puer* means boy.** *puer, pueri*, m. — second declension.',
  'puer and puella: boy and girl.')
q(Q, 1, 'What does *sed* mean?', ['but', 'not', 'and', 'or'], 0,
  'It sits between two ideas that pull in different directions.',
  ['*non* is the word for not, so *sed* is not that.', 'In *Videt, sed non audit*, the two halves disagree.', 'The word that links disagreeing ideas is but.'],
  '***sed* means but.** It joins two clauses that contrast.',
  'non = not; sed = but. Two short words, two different jobs.')
q(Q, 1, 'Which Latin word means "many"?', ['multus', 'magnus', 'amicus', 'deus'], 0,
  'Which one starts like multiply?',
  ['Two of the options are adjectives: *multus* and *magnus*.', '*magnus* is big; MAGNIfy makes things bigger.', '*multus* is many; MULTIply makes many.'],
  '***multus* means many.** *magnus* is the trap: it means great or big.',
  'multi- = many; magni- = big.')
q(Q, 1, 'Which Latin word means "god"?', ['deus', 'donum', 'do', 'audio'], 0,
  'Which one starts like deity?',
  ['*donum* is a gift and *do* is to give.', '*audio* is to hear.', '*deus* is the one left, and deity comes from it.'],
  '***deus* means god.** *deus, dei*, m.',
  'deus and donum both start with d — the deity is the god.')
q(Q, 1, 'Which Latin word means "I love"?', ['amo', 'amicus', 'audio', 'do'], 0,
  'One of these looks like it shares a root with it, but is a noun.',
  ['*amicus* comes from the same root but is a noun: friend.', '*audio* and *do* are verbs, but they mean hear and give.', '*amo* is the verb, and on its own it means I love.'],
  '***amo* means I love.** The first dictionary form of a verb is the I form.',
  'A friend (amicus) is someone you love (amo).')
for en, la in (('farmer', 'agricola'), ('girl', 'puella'), ('gift', 'donum'), ('boy', 'puer')):
    q(Q, 1, 'Type the Latin word for "%s" (its dictionary form).' % en, [la], 0,
      'Say it out loud first, then spell each sound.',
      ['Find the English word on your list.', 'The first form in the dictionary entry is the one to type.', 'Spell it: %s.' % la],
      '**%s means %s.**' % (la, en),
      'Spelling counts on a vocabulary quiz, so type it the way the list prints it.', kind='spell')

# ---------------- level 2: apply
q(Q, 2, 'Which phrase means "the great farmer"?',
  ['agricola magnus', 'agricola magna', 'agricola magnum', 'agricolus magnus'], 0,
  'Check the gender of farmer in the dictionary entry, not its ending.',
  ['The entry is *agricola, -ae*, m.', 'm. means masculine, even though the word ends in -a.', 'An adjective matches the GENDER of its noun.', 'The masculine form of the adjective is *magnus*.'],
  '***agricola magnus*.** Agricola looks feminine, but it is masculine, so the adjective is masculine too.',
  'Agreement is about gender, not about matching endings.', frm='added')
q(Q, 2, 'A dictionary prints *donum, -i, n.* What does the n. tell you?',
  ['The noun is neuter', 'The word is a noun', 'The word is plural', 'The word is said with an n-sound'], 0,
  'Dictionary entries list a gender letter after the genitive.',
  ['*agricola* has m. and *puella* has f.', 'Those letters are genders: masculine and feminine.', 'The third gender is neuter, marked n.'],
  '**The noun is neuter.** m., f. and n. are the three genders.',
  'Neuter means neither masculine nor feminine.')
q(Q, 2, '*amicus* is a male friend. Which word names a female friend?',
  ['amica', 'amici', 'amicae', 'amicum'], 0,
  'Swap the masculine ending for the first-declension one.',
  ['*amicus* is second declension, masculine.', 'The feminine version moves to the first declension, like *puella*.', 'The first-declension nominative ends in -a.', 'So a female friend is *amica*.'],
  '***amica*** — a female friend. *amici* is friends (plural) and *amicae* is female friends (plural).',
  'amicus / amica, just like the -us / -a of an adjective.')
q(Q, 2, 'Which sentence asks "Does the girl see the farmer?"',
  ['Videtne puella agricolam?', 'Puella agricolam videt.', 'Puella agricolam non videt.', 'Videtne agricola puellam?'], 0,
  'Look for the question marker, then check who is the subject.',
  ['A yes/no question needs -ne on the first word.', 'Two options have it: *Videtne puella agricolam?* and *Videtne agricola puellam?*', 'The girl is doing the seeing, so she must be the subject: *puella*.', 'The farmer is being seen, so he is *agricolam*.'],
  '***Videtne puella agricolam?*** -ne makes it a question, and *puella* is the subject.',
  'Check both: the question marker AND who is doing what.')
q(Q, 2, 'Translate: *Puer non audit.*',
  ['The boy does not hear.', 'The boy hears.', 'The boy does not see.', 'The girl does not hear.'], 0,
  'Find the subject, the verb, and the little word in front of the verb.',
  ['*puer* is boy.', '*audit* is he hears.', '*non* in front of the verb makes it negative.', 'The boy does not hear.'],
  '**The boy does not hear.** *non* sits just before the verb it negates.',
  'non = not, placed right before the verb.')
q(Q, 2, 'Translate: *Puella videt, sed non audit.*',
  ['The girl sees, but she does not hear.', 'The girl sees and hears.', 'The girl does not see, but she hears.', 'The girl hears, but she does not see.'], 0,
  'Two verbs, one *sed*, one *non*. Which verb does the *non* touch?',
  ['*videt* is she sees.', '*sed* is but.', '*non audit* is she does not hear.', 'Put it together: the girl sees, but she does not hear.'],
  '**The girl sees, but she does not hear.** *non* belongs to *audit*, the verb right after it.',
  'non only reaches the word it sits in front of.')
q(Q, 2, 'In *do, dare, dedi, datus*, which form means "to give"?',
  ['dare', 'do', 'dedi', 'datus'], 0,
  'The second dictionary form is always the infinitive.',
  ['*do* is I give.', '*dare* is the infinitive, the to- form.', '*dedi* is I gave.', 'So to give is *dare*.'],
  '***dare* means to give.** The second principal part of a verb is its infinitive.',
  'amo / amare, video / videre, do / dare: the second form is the "to" form.', frm='added')
q(Q, 2, 'What does *multi pueri* mean?',
  ['many boys', 'great boys', 'the boy\'s friends', 'big boy'], 0,
  'multi is the plural of multus.',
  ['*pueri* here is plural: boys.', '*multi* is the matching plural of *multus*.', 'In the plural, *multus* means many.', 'So: many boys.'],
  '**many boys.** *multus* means many in the plural.',
  'magnus would make it great boys, not many boys.')
q(Q, 2, 'Which English word comes from *magnus*?',
  ['magnify', 'multiply', 'amicable', 'donate'], 0,
  'Find the word that is about making something bigger.',
  ['*magnus* means great or big.', 'multiply comes from *multus*, amicable from *amicus*, donate from *donum*.', 'To magnify is to make something look bigger.'],
  '**magnify** — to make bigger, from *magnus*.',
  'Matching a derivative to its root is a fast way to remember a meaning.', frm='added')
q(Q, 2, 'An audience is named for what it does. Which Latin verb is inside the word?',
  ['audio', 'video', 'amo', 'do'], 0,
  'What does an audience do during a concert?',
  ['An audience listens.', 'Listening is hearing.', 'The verb for to hear is *audio*.'],
  '***audio***, to hear. An audience is a group of hearers.',
  'audio, audible, auditorium — all hearing words.', frm='added')
q(Q, 2, 'The English word "data" comes from *datus*. Which verb is *datus* a form of?',
  ['do — to give', 'video — to see', 'audio — to hear', 'amo — to love'], 0,
  'Look for the dictionary entry that ends in *datus*.',
  ['Each verb on the list has four forms.', '*do, dare, dedi, datus* ends in *datus*.', 'So data are literally things given.'],
  '***do*, to give.** *datus* is its fourth principal part, and data are facts "given".',
  'Four principal parts: memorize all four, not just the first.', frm='added')
q(Q, 2, '*Videt* means "he sees". Which verb on your list is it a form of?',
  ['video', 'audio', 'do', 'amo'], 0,
  'Strip the ending and compare the stem with each dictionary entry.',
  ['*videt* = the stem *vid-* + the ending -t, he or she.', 'The entry with the stem *vid-* is *video, videre, vidi, visus*.', 'That verb means to see, which matches.'],
  '***video***, to see. *videt* is its he-or-she form.',
  'The ending names the subject; the stem names the verb.')
q(Q, 2, 'What does *Audisne?* ask?',
  ['Do you hear?', 'You hear.', 'You do not hear.', 'Who hears?'], 0,
  'Split off the suffix first, then read what is left.',
  ['*Audisne* is *audis* + -ne.', '*audis* means you hear.', '-ne turns a statement into a yes/no question.', 'So it asks: Do you hear?'],
  '**Do you hear?** -ne turns *audis*, you hear, into a yes/no question.',
  'A yes/no question asks for yes or no; "Who hears?" asks for a name.')

# ---------------- level 3: analyze
q(Q, 3, '*agricola* ends in -a like *puella*. What makes it different?',
  ['It is masculine, even though it is first declension', 'It is second declension, so it takes -us adjectives', 'It is neuter, so it is neither masculine nor feminine', 'It is plural, so on its own it means farmers'], 0,
  'Compare the genitive and the gender letter in both entries.',
  ['*puella, -ae*, f. and *agricola, -ae*, m.', 'Both have -ae, so both are first declension.', 'The difference is the gender letter: f. against m.', '*agricola* is masculine.'],
  '**It is masculine, even though it is first declension.** Ending and gender do not always line up.',
  'Always read the gender letter, never guess it from the ending.')
q(Q, 3, 'Why does the dictionary entry say *puer, pueri* instead of just *puer*?',
  ['The second form is the genitive, which tells you the declension',
   'The second form is the feminine, used when the child is a girl',
   'The second form is the plural, used only when there are two boys',
   'The second form shows how to say the word aloud, syllable by syllable'], 0,
  'What does the second form tell you on every noun entry?',
  ['On every noun entry, the second form is the genitive singular.', '*pueri* ends in -i, which marks the second declension.', 'It also shows the e stays: *pueri*, not *puri*.'],
  '**The second form is the genitive, which tells you the declension.** -i means second declension.',
  'The girl is *puella*, a different word, not a form of *puer*.', frm='added')
q(Q, 3, 'Translate: *Agricola puellae donum dat.*',
  ['The farmer gives a gift to the girl.', 'The girl gives a gift to the farmer.', 'The farmer sees a gift and a girl.', 'The farmer loves the girl\'s gift.'], 0,
  'Find the verb first, then decide who is giving and who is receiving.',
  ['*dat* is from *do*: he gives.', '*agricola* is the subject: the farmer gives.', '*donum* is what is given: a gift.', '*puellae* is the one receiving it: to the girl.'],
  '**The farmer gives a gift to the girl.** *puellae* is the dative, the receiver.',
  'Verb first, then subject, then object.')
q(Q, 3, '*Puerum puella videt.* Who sees whom?',
  ['The girl sees the boy.', 'The boy sees the girl.', 'The boy and the girl see.', 'The girl sees the boys.'], 0,
  'Word order does not decide it; the endings do.',
  ['*puerum* ends in -um: the accusative, the one being seen.', '*puella* ends in -a: the nominative, the one seeing.', '*videt* means sees.', 'The girl sees the boy.'],
  '**The girl sees the boy.** In Latin, the endings show who does what, not the word order.',
  'Coming first in the sentence does not make a word the subject.', frm='added')
q(Q, 3, 'How do *magnum donum* and *multa dona* differ?',
  ['One big gift, then many gifts', 'Many gifts, then one big gift', 'A god\'s gift, then a friend\'s gift', 'Both mean many gifts'], 0,
  'One phrase is singular and one is plural. Which adjective is which?',
  ['*donum* is one gift; *dona* is gifts.', '*magnum* means big.', '*multa* means many.', 'So: a big gift, then many gifts.'],
  '**One big gift, then many gifts.** *magnus* is about size, *multus* about number.',
  'magnus: how big. multus: how many.')

build('ad-astra', C, Q, 'unit-latin-vocab1', 'Latin I · Vocabulary Quiz 1', 'latin',
  'The fifteen-word vocabulary list for the Latin quiz on Friday, October 2: four nouns, four verbs with their principal parts, two adjectives, and the small words *sed*, *non* and the question suffix -ne.',
  'A vocabulary list is where the language becomes usable: these fifteen words are enough to build real sentences, and every one of them returns in later units. Learning each dictionary entry whole, with its genitive and gender, saves you from guessing later.',
  [('Give the English meaning of each word on the list', 'source'),
   ('Give the Latin word for each English meaning, spelled correctly', 'source'),
   ('Read a dictionary entry: genitive, gender and principal parts', 'added'),
   ('Use -ne, non and sed in a short sentence', 'added')],
  'Built from the Latin vocabulary list uploaded on 10/2 ("quiz - Oct 2"), read for what it asks only. Its two handwritten notes, amica beside amicus and "big" beside magnus, are on the cards. The quiz itself is dated today, so this unit is mostly for keeping the words fresh; all fifteen will come back in later units. Two things to know: agricola is masculine even though it ends in -a, which is the most common trap with this list, and the derivative hooks (agriculture, magnify, data and so on) are study aids we added, not part of the list. Every respelling follows the pronunciation unit\'s conventions.',
  ('Say each word out loud before you flip the card, then try a round.', 12),
  'content/latin-vocab-1.json', 'quiz - Oct 2 (Latin vocabulary list, Drive)', 'Latin I vocabulary list (Drive folder)',
  offset_hours=3, prep_=True, libv_=1)
