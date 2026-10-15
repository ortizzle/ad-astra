# To Kill a Mockingbird, chapter quizzes for chapters 6, 7, 8 and 9.
#
# One unit per chapter, written by tkam_common.chapter(), which builds through
# unit_common.build() (validation + _balance) and then adds book:true, the
# passages and a spoiler sweep. Each chapter passes the tells of LATER
# chapters; a hit anywhere in the shipped record fails the build.
#
# Rules this file holds itself to, beyond the shared checker:
# - Spoiler-bounded. Chapter 9 may look back; nothing looks forward.
# - The novel's racial slur is never printed (chapter 9). The rape charge is
#   not named in these chapters (it is first named in chapter 12).
# - Passages are used only where the wording is certain. Anything less
#   certain is paraphrased in the stem instead.
# - The correct option is never the giveaway by length: _len_ok() below runs
#   the checker's own length rule before anything is written.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q
from tkam_common import chapter


def _len_ok(Q, ch):
    """The checker's length tell, run at build time: the correct option may not
    outrun the longest wrong one by more than 10%."""
    bad = []
    for x in Q:
        if x.get('kind') == 'order': continue
        lens = [len(o) for o in x['opts']]
        right = lens[x['ans']]
        rival = max(lens[:x['ans']] + lens[x['ans'] + 1:])
        if right > rival * 1.10: bad.append((ch, x['id'], right, rival))
    assert not bad, bad


# ─────────────────────────────────────────────────────────────── Chapter 6
def ch6():
    C, Q = [], []
    card(C, "Dill's last night",
         "**Dill's last night in Maycomb before he goes home, and he wants one more try at the Radley Place.**"
         "\n• Jem and Dill plan to peek in a Radley window through a loose shutter."
         "\n• Scout objects, gets told she is turning into a girl, and goes along anyway.",
         hint='A last night is when a summer of dares runs out of time and gets bold.')
    card(C, 'The raid on the back porch',
         "**The three creep through the back of the Radley lot and up onto the back porch to look inside.**"
         "\n• It is the furthest any of them has ever gone onto the Radley Place."
         "\n• In chapter 1, touching the side of the house was the whole dare.",
         hint='Measure the raid against chapter 1: a touch on the wall, then the porch itself.')
    card(C, 'The shadow in the hat',
         "**A man's shadow, wearing a hat, crosses the porch toward Jem — then turns and goes back the way it came.**"
         "\n• Nobody sees a face; the children see only the shadow."
         "\n• It does nothing to them. They run anyway.",
         hint='Note what the shadow DOES, not what the children fear it will do.')
    card(C, 'The shotgun and the lost pants',
         "**As they run, a shotgun goes off, and Jem's pants catch on the wire fence, so he wriggles out and leaves them.**"
         "\n• They reach the street with Jem in his shorts."
         "\n• The pants are evidence, hanging on the Radley fence.",
         hint='The pants are the loose end the whole rest of the chapter has to deal with.')
    card(C, 'Mr. Nathan Radley',
         "**Boo's older brother, who now runs the Radley house — he tells the neighbors he fired at an intruder in his collard patch.**"
         "\n• Neighbors gather in the street; Miss Stephanie Crawford spreads the story fast."
         "\n• His version is the one the town hears.",
         hint='Two stories of one night: what happened, and what Mr. Nathan says happened.')
    card(C, "Dill's cover story",
         "**Dill explains Jem's missing pants by saying he won them from Jem in a game of strip poker.**"
         "\n• Strip poker: a card game where the loser of a hand takes off a piece of clothing."
         "\n• It shocks the grown-ups, but it keeps the Radley yard out of the conversation.",
         hint='Dill would rather they be in trouble for cards than for the Radley Place.')
    card(C, 'Collard patch',
         "**A garden bed of collard greens — a leafy vegetable common in Southern kitchens.**"
         "\n• Mr. Nathan's story puts the intruder there, at the back of the lot."
         "\n• That small detail is what makes the shooting sound like protecting a garden.",
         hint='Collards are greens; a patch is a bed of them.')
    card(C, 'Theme: what Jem will risk',
         "**Jem goes back alone, in the middle of the night, for his pants — because keeping Atticus's trust matters more to him than being afraid.**"
         "\n• Atticus has never whipped him, and Jem wants to keep it that way."
         "\n• Scout begs him not to go; for the first time, she cannot follow his reasons.",
         hint="Jem's fear of the Radley Place loses to his fear of letting Atticus down.")
    card(C, 'Ponder: brave or foolish?',
         "**Was Jem brave or foolish to go back for his pants — and can it be both?**"
         "\n• Think about what he was really protecting."
         "\n• There is no single right answer to this one.",
         hint='A dinner-table question: argue it from both sides.')

    q(Q, 1, 'Why do Jem and Dill choose this particular night to try the Radley Place again?',
      ['It is Dill\'s last night in Maycomb before going home',
       'Atticus is away from home until late that evening',
       'The Radleys have gone out of town for the weekend',
       'Miss Stephanie dared them to do it over supper'],
      0, 'Whose summer is about to end?',
      ['Look at the opening of the chapter: what is special about this evening?',
       'Dill only stays in Maycomb for the summer.',
       'He goes home the next day, so this is the last chance.',
       "It is Dill's last night in Maycomb."],
      "**It is Dill's last night.** The summer of dares is out of time, which is why this attempt is the boldest yet.",
      'When characters take a bigger risk than usual, look for a deadline in the setup.')

    q(Q, 1, 'What do the children see when they reach the Radley back porch?',
      ['The shadow of a man in a hat crossing the porch',
       "Boo Radley's face pressed against the window glass",
       'A lamp being carried from room to room inside',
       'Mr. Nathan Radley sitting alone on the back steps'],
      0, 'They never see a face.',
      ['Recall what Scout describes from the porch.',
       'She sees a shape, not a person she can identify.',
       'The shape is a shadow, and it is wearing a hat.',
       'They see the shadow of a man in a hat crossing the porch.'],
      "**The shadow of a man in a hat.** No face, no name — the children fill in the rest themselves, which is how the Boo legend always works.",
      'Separate what a narrator saw from what she assumed about it.')

    q(Q, 1, 'What does Mr. Nathan Radley tell the gathered neighbors about the gunshot?',
      ['He fired at an intruder in his collard patch',
       'He scared off a stray dog digging in his yard',
       'He shot at a snake under the back porch',
       'He heard thieves trying the front door lock'],
      0, 'Where does his story place the trouble?',
      ['The neighbors gather in the street after the shot.',
       'Mr. Nathan explains it in terms of his garden.',
       'He says someone was in his collard patch and he fired at them.',
       'His story: he fired at an intruder in his collard patch.'],
      "**He fired at an intruder in his collard patch.** It is the version the town hears, and the children know it is not the whole story.",
      "Every public explanation in this book is worth checking against what the reader saw happen.")

    q(Q, 2, 'Jem turns up among the neighbors in his shorts. Why does Dill say he won Jem\'s pants playing strip poker?',
      ['It gives the grown-ups a story with no Radleys in it',
       'He wants Jem punished for being the one who ran',
       'He truly believes the game is what everyone was doing',
       'He hopes the shock will make Miss Rachel laugh'],
      0, 'Which trouble is smaller: cards, or the Radley yard?',
      ['The missing pants need an explanation on the spot.',
       'The true one — they were caught on the Radley fence — would connect the children to the gunshot.',
       'A card game is bad, but it happened nowhere near the Radley Place.',
       'So Dill offers strip poker: a story with no Radleys in it.'],
      "**It gives the grown-ups a story with no Radleys in it.** Dill trades a scolding about cards for the far bigger trouble of the truth.",
      'When a character lies, ask what the lie is protecting, not just what it says.')

    q(Q, 2, 'Put these chapter 6 events in the order they happen.',
      ["Jem and Dill plan to peek in a Radley window on Dill's last night",
       'A shadow in a hat crosses the back porch toward Jem',
       "Dill tells the neighbors he won Jem's pants at strip poker",
       'Jem slips out in the middle of the night to get his pants back'],
      0, 'Plan, porch, cover story, then the night trip.',
      ['The plan comes first, at the start of the evening.',
       'On the back porch, the shadow appears and the children run.',
       "Out in the street, Dill covers for the missing pants.",
       'Only later that night does Jem go back alone.'],
      "**Plan → shadow → cover story → Jem goes back.** The chapter closes on the riskiest move of all, made alone.",
      'In an order question, look for cause and effect: each event creates the problem the next one solves.', kind='order')

    q(Q, 2, 'Scout begs Jem not to go back to the Radley fence that night. What reason does he give for going anyway?',
      ['Atticus has never whipped him, and he means to keep it so',
       'He wants one more chance to see Boo up close at night',
       'Dill made him promise to finish the raid before he left',
       'He wants to prove to Scout that he is not afraid at all'],
      0, 'Who would find out if the pants stayed on the fence?',
      ['Left on the fence, the pants would be found in the morning.',
       'That would tell Atticus where the children really were.',
       'Jem says Atticus has never whipped him, and he means to keep it that way.',
       "So he goes back for Atticus's sake, not for Boo's."],
      "**Atticus has never whipped him, and he wants to keep it that way.** It is less about punishment than about not losing his father's trust.",
      'A character\'s stated reason is a clue to what he values most.')

    q(Q, 2, 'Mr. Nathan Radley says he fired at someone in his collard patch. What is a collard patch?',
      ['A garden bed of leafy collard greens',
       'A fenced pen where chickens are kept',
       'A strip of grass along the back fence',
       'A woodpile stacked behind the house'],
      0, 'Collards are something you would cook.',
      ['"Patch" usually means a small planted area, like a pumpkin patch.',
       'Collards are a leafy green vegetable common in the South.',
       'So a collard patch is a garden bed of collard greens.'],
      "**A garden bed of collard greens.** Placing the intruder in the garden makes the shot sound like a man protecting his vegetables.",
      'For an unfamiliar compound word, define each half and then put them back together.')

    q(Q, 3, 'The children know they were on the back porch. Mr. Nathan tells the town about an intruder in his collard patch. What does that gap show?',
      ["What Maycomb hears about the Radleys isn't the whole truth",
       'Mr. Nathan never actually heard anyone on his property',
       'The children have mixed up which house they were at',
       'Miss Stephanie invented the gunshot to spread gossip'],
      0, 'Two versions of one night — who knows both?',
      ['The reader and the children know where they really were.',
       'The neighbors only get Mr. Nathan\'s account, retold by Miss Stephanie.',
       'His version may be honest about the shot but leaves the real story out.',
       'So the public version of the Radleys keeps drifting from what really happens.'],
      "**What Maycomb hears isn't the whole truth.** It is the same pattern as the Boo legend: a confident public story, built without the facts.",
      'When the reader knows more than the town, the book is usually teaching you to distrust the town\'s version.')

    q(Q, 3, 'Earlier in the book Jem acts mostly on dares and Dill\'s ideas. What does going back alone for his pants show about him?',
      ['He now weighs his father\'s trust above his own fear',
       'He has stopped believing Boo Radley is real at all',
       'He wants to take over the Radley games from Dill',
       'He no longer cares what Scout thinks of his choices'],
      0, 'Whose opinion is he protecting?',
      ['Before, Jem took risks to impress Dill or win a dare.',
       'This time nobody is watching, and there is nothing to win.',
       "The risk is to keep Atticus's trust intact.",
       "So Jem is putting his father's opinion of him ahead of his fear."],
      "**He now weighs his father's trust above his own fear.** A dare is for an audience; this risk is taken alone, for a reason of his own.",
      'Track whether a character acts for an audience or for himself. The change is often the point.')

    q(Q, 3, 'The Maycomb legend says Boo Radley is a dangerous monster. On the porch, the shadow comes toward Jem, then turns and goes back. What is a careful reading?',
      ['It did nothing — once again the evidence does not fit the monster story',
       'The shadow proves the legend right — Boo really does hunt at night',
       'The shadow means Jem imagined the whole thing out of pure fright',
       'The shadow shows that Mr. Nathan is the real danger in that house'],
      0, 'Stick to what the shadow actually did.',
      ['The legend predicts a monster who attacks.',
       'The shadow approaches, then withdraws without touching anyone.',
       'Nothing in the scene proves who it was, or that it meant harm.',
       'So, once again, the evidence does not fit the monster story.'],
      "**The shadow did nothing.** It is the same gap the book keeps showing you: frightening rumor on one side, a quiet and harmless fact on the other.",
      'In a mystery, judge characters by what they do on the page, not by what others say they would do.')

    _len_ok(Q, 6)
    chapter(6, 'The Raid on the Radley Place', C, Q,
            "Chapter 6 of To Kill a Mockingbird: on Dill's last night in Maycomb, Jem, Dill and Scout creep onto the Radley back porch to peek in a window. A man's shadow crosses the porch, a shotgun goes off as they run, and Jem loses his pants on the fence. Mr. Nathan Radley tells the neighbors he fired at an intruder in his collard patch, Dill covers with a strip-poker story, and Jem goes back alone in the night for his pants.",
            "This is the boldest raid yet, and the first time Jem's choices are his own rather than a dare. The gap between what happened and what the town is told is the book's favorite pattern.",
            [("Retell the raid and its aftermath in order, from the plan to Jem's night trip.", 'source'),
             ("Explain why Dill invents the strip-poker story and what it protects.", 'source'),
             ("Explain why Jem goes back for his pants, and what that shows about how he is changing.", 'added'),
             ("Compare what the children know about the night with the version the town hears.", 'added')],
            "This quiz covers chapter 6 only and stops at the end of that chapter, with Jem back from the fence. There is a gunshot, though nobody is hurt, and a strip-poker cover story that the grown-ups find shocking; neither is graphic. The thing most likely to trip her up is keeping the town's version of the night (an intruder in the collard patch) separate from what the reader saw. The ponder card about Jem going back is worth a minute at dinner.",
            ("Finish chapter 6, then run the cards and the quiz.", 10),
            passages={},
            later_tells=['cement', 'soap', 'blanket', 'mended', 'sewed', 'sewn', 'pocket watch',
                         'medal', 'snowman', 'azalea', 'tom robinson', 'mad dog', 'dubose',
                         'aunt alexandra', 'cecil', 'christmas', 'uncle jack', 'twine'])


# ─────────────────────────────────────────────────────────────── Chapter 7
def ch7():
    C, Q = [], []
    card(C, 'The pants, waiting',
         "**When Jem went back that night, his pants were folded over the fence — and sewn up, crooked, like something he'd try to do himself.**"
         "\n• Jem keeps this to himself for about a week, moody and silent."
         "\n• Scout tries Atticus's advice and climbs into Jem's skin to understand him.",
         hint='Folded and mended: somebody knew he would come back.')
    card(C, 'The knothole gifts',
         "**More small presents turn up in the oak tree's knothole: gray twine, a whole pack of gum, a faded spelling medal, and a pocket watch on a chain with an aluminum knife.**"
         "\n• At first the children are not sure the twine is meant for them."
         "\n• By the watch, there is no doubt left: someone is giving them things.",
         hint='Each gift is a little more personal than the one before.')
    card(C, 'Two figures in soap',
         "**Someone carves two small soap figures, a boy and a girl, that look just like Jem and Scout.**"
         "\n• Jem recognises them at once: they are the two of them."
         "\n• To carve them, the giver must have watched the children closely.",
         hint='Gifts from a stranger are generous; portraits from a stranger mean he has been watching.')
    card(C, 'The thank-you note',
         "**Jem and Scout write a note to thank whoever has been leaving the gifts.**"
         "\n• It is the first time they try to reply."
         "\n• On the way to leave it, they find the knothole filled with cement.",
         hint='The conversation was about to go both ways.')
    card(C, 'Cement in the knothole',
         "**Mr. Nathan Radley says he filled the hole because the tree is dying — but Atticus says the tree looks perfectly healthy.**"
         "\n• Jem asks Mr. Nathan directly, and gets the dying-tree answer."
         "\n• That evening Atticus points to the green, full leaves.",
         hint="Two grown-ups, two answers. Only one of them is about the tree.")
    card(C, "Jem's tears",
         "**That night Jem stands alone on the porch, and Scout sees that he has been crying.**"
         "\n• He understands what the cement really means before she does."
         "\n• The narrator does not explain it; she lets you work it out.",
         hint='Ask what Jem has just lost.')
    card(C, 'Crude',
         "**Rough and simply made, without fine detail.**"
         "\n• One soap figure wears a crude dress: carved in a few rough strokes, not finely shaped."
         "\n• Crude can also mean rude, but here it describes how something was made.",
         hint='A crude carving is a sketch in soap, not a finished statue.')
    card(C, 'Theme: a conversation shut down',
         "**The knothole is the only way Boo and the children have of reaching each other, and the cement closes it.**"
         "\n• The gifts were one side of a friendship; the note would have been the other."
         "\n• Mr. Nathan, not Boo, is the one who seals it.",
         hint='A hole in a tree, a door between two worlds — then it is shut.')
    card(C, 'Ponder: who shut the door?',
         "**Why would Mr. Nathan fill the knothole and give a reason that isn't true?**"
         "\n• Think about what he might want to keep his brother away from."
         "\n• There is no single right answer to this one.",
         hint='A dinner-table question: there are several fair guesses.')

    q(Q, 1, 'When Jem went back for his pants, how did he find them?',
      ['Folded over the fence and sewn up crooked',
       'Torn to pieces and left in the collard patch',
       'Hanging on the fence exactly as he left them',
       'Folded neatly on the Radley front porch steps'],
      0, 'Someone had done something to them.',
      ['Recall what Jem finally tells Scout at the start of the chapter.',
       'The pants were not where he expected, or how he expected.',
       'They were folded over the fence and roughly mended.',
       'He found them folded over the fence and sewn up crooked.'],
      "**Folded over the fence and sewn up crooked.** Somebody mended them knowing he would come back, and did it the way a man, not a seamstress, would.",
      'A small physical detail in a novel is often a clue about who is behind it.')

    q(Q, 1, 'What do the two soap figures in the knothole look like?',
      ['A boy and a girl who look like Jem and Scout',
       'A man and a woman who look like Atticus and Calpurnia',
       'Two small dogs that look like the Finches\' neighbors\' pets',
       'A boy and a man who look like Jem and Atticus'],
      0, 'Jem knows who they are the moment he sees them.',
      ['There are two figures, carved in soap.',
       'One is a boy and one is a girl in a dress.',
       'Jem recognises them as the two of them.',
       'They look like Jem and Scout.'],
      "**A boy and a girl who look like Jem and Scout.** The giver has been watching them closely enough to carve them.",
      'Notice when a gift is personal; it tells you how well the giver knows the person receiving it.')

    q(Q, 1, 'Jem asks Mr. Nathan Radley why he filled the knothole with cement. What does he say?',
      ['The tree is dying, and sick trees get cement',
       'Children were stealing things out of the tree',
       'The hole had become a nest for wasps and bees',
       'He was told to by the people at the courthouse'],
      0, 'He gives a reason about the tree itself.',
      ['Jem asks Mr. Nathan directly.',
       'Mr. Nathan answers in terms of the tree\'s health.',
       'He says the tree is dying and you plug sick trees with cement.'],
      "**The tree is dying.** It is a plausible-sounding reason — until Atticus looks at the same tree.",
      'Keep a note of every explanation a character gives, so you can test it when another character weighs in.')

    q(Q, 2, 'The mended pants are sewn up crooked, "like somethin\' I\'d try to do," Jem says. What does that suggest?',
      ['Someone unskilled mended them knowing he would return',
       'Miss Maudie fixed them while the neighbors were outside',
       'Jem tore them worse than he first thought he had',
       'Atticus quietly repaired them after the children slept'],
      0, 'Who would sew the way Jem would?',
      ['A practised sewer would make neat stitches.',
       'These stitches are rough, like a beginner\'s.',
       'And the pants were folded, waiting, as if someone expected Jem back.',
       'So someone unskilled mended them, knowing he would return.'],
      "**Someone unskilled mended them, knowing he would return.** The repair is clumsy and kind at once, and it came from the Radley side of the fence.",
      'When a clue is described by how it was done, ask what kind of person would do it that way.')

    q(Q, 2, 'Put these chapter 7 events in the order they happen.',
      ['Jem tells Scout his pants were folded and mended on the fence',
       'Two soap figures that look like Jem and Scout appear in the knothole',
       'Jem and Scout write a note to thank whoever is leaving gifts',
       'Mr. Nathan Radley says he filled the hole because the tree is dying'],
      0, 'Secret, gifts, thanks, then the hole is shut.',
      ['The chapter opens with Jem finally telling Scout about the pants.',
       'The knothole gifts follow, including the soap figures.',
       'Eventually the children write a thank-you note.',
       'Then the hole is cemented, and Mr. Nathan explains why.'],
      "**Pants → soap figures → thank-you note → cement.** The chapter builds a friendship and then closes it off in its last pages.",
      'When a chapter builds something up slowly, expect the ending to change it.', kind='order')

    q(Q, 2, 'One soap figure wears a "crude dress." What does crude mean here?',
      ['Roughly made, without fine detail',
       'Rude and likely to offend people',
       'Old, faded and badly worn out',
       'Brightly painted in loud colors'],
      0, 'Think about carving a dress out of a bar of soap.',
      ['The figure is carved from soap.',
       'You cannot carve fine lace into soap with a knife.',
       'So the dress is shaped in a few rough strokes.',
       'Crude here means roughly made, without fine detail.'],
      "**Roughly made, without fine detail.** Crude can mean rude, but the sentence is about how the figure was carved, not about manners.",
      'When a word has two meanings, test both against what the sentence is describing.')

    q(Q, 2, 'Mr. Nathan says the tree is dying. What does Atticus say when Jem asks him about it?',
      ['The tree looks perfectly healthy to him',
       'The tree has been sick for years already',
       'Trees really should be filled with cement',
       'He has never looked at that tree closely'],
      0, 'Atticus points at the leaves.',
      ['Jem asks Atticus the same question that evening.',
       'Atticus looks at the tree\'s leaves: green and full.',
       'He sees no sign that it is sick.',
       'So Atticus says the tree looks perfectly healthy.'],
      "**The tree looks perfectly healthy.** That quietly tells Jem that Mr. Nathan's reason was not the real one.",
      'When two characters describe the same thing differently, one of them usually has a reason to.')

    q(Q, 3, 'Scout sees that Jem has been crying after he hears Atticus say the tree is healthy. What has Jem understood?',
      ['That the cement was put there to cut Boo off from them',
       'That Atticus is upset with him about the Radley raid',
       'That the gifts were left by Mr. Nathan all along',
       'That the tree will have to be cut down this winter'],
      0, 'If the tree is healthy, why is there cement?',
      ['Mr. Nathan said the tree was dying.',
       'Atticus says it is healthy, so that reason is false.',
       'The real effect of the cement is to close the knothole.',
       'The knothole was the only way Boo could reach the children.',
       'Jem understands the cement was meant to cut Boo off from them.'],
      "**The cement was there to cut Boo off from them.** Jem sees a friendship ended on purpose, and the narrator lets his tears say it.",
      'When a narrator shows an emotion without explaining it, work backward from what the character just learned.')

    q(Q, 3, 'The children were going to answer the gifts with a thank-you note. Why does it matter that the hole is sealed just then?',
      ['It stops the gift-giving just as it could become two-way',
       'It shows the children never really wanted the gifts',
       'It proves the gifts had been meant for someone else',
       'It means the note was too rude to send to anyone'],
      0, 'Until the note, who was doing all the giving?',
      ['So far, every gift has gone one way: from the tree to the children.',
       'The note would have been the first reply.',
       'The hole is sealed right before that answer arrives.',
       'So it stops the gift-giving just as it could become two-way.'],
      "**It stops the exchange just as it could become two-way.** The timing turns a run of small gifts into a real loss.",
      'Timing in a plot is rarely random; ask what an event prevents as well as what it causes.')

    q(Q, 3, 'Across chapters 4 to 7, the knothole holds gum, coins, twine, soap figures, a medal and a watch. What do the gifts suggest about the giver?',
      ['He is lonely and gentle, reaching out the only way he can',
       'He is playing a trick to lure the children onto his lot',
       'He is a thief, returning things he took from the town',
       'He wants payment and expects the children to give back'],
      0, 'Ask what kind of person gives small things in secret.',
      ['The gifts are small and kind, and they get more personal.',
       'The giver never asks for anything in return.',
       'He gives in secret, through a tree, instead of face to face.',
       'That fits someone lonely and gentle, reaching out the only way he can.'],
      "**He is lonely and gentle, reaching out the only way he can.** The gifts are the strongest evidence yet against the monster story.",
      'Judge a hidden character by the pattern of what he does, not by one single act.')

    _len_ok(Q, 7)
    chapter(7, 'The Knothole Closes', C, Q,
            "Chapter 7 of To Kill a Mockingbird: Jem tells Scout his pants were waiting for him, folded over the fence and sewn up crooked. The knothole in the oak tree keeps giving: gray twine, two soap figures that look like Jem and Scout, a pack of gum, a faded spelling medal, and a pocket watch with an aluminum knife. The children write a thank-you note, but the hole is filled with cement. Mr. Nathan Radley says the tree is dying; Atticus says it looks healthy, and Jem is left crying on the porch.",
            "This is the chapter where the Boo legend and the evidence part ways for good. Every gift points to a gentle, lonely giver, and the cement shows someone deliberately cutting him off.",
            [("List the knothole gifts and explain what they suggest about the giver.", 'source'),
             ("Explain what the mended pants tell Jem about who has been watching.", 'source'),
             ("Compare Mr. Nathan's reason for the cement with what Atticus says about the tree.", 'source'),
             ("Explain why Jem cries at the end of the chapter.", 'added')],
            "This quiz covers chapter 7 only and stops at the end of that chapter, with Jem on the porch after the knothole has been sealed. Nothing here is sensitive. The thing most likely to trip her up is Jem's tears: the book never says why he cries, and she has to work it out from the healthy tree and the cement. The ponder card about Mr. Nathan's motive is a good one for dinner.",
            ("Finish chapter 7, then run the cards and the quiz.", 10),
            passages={},
            later_tells=['blanket', 'snowman', 'azalea', 'burned', 'burning', 'tom robinson',
                         'cecil', 'christmas', 'uncle jack', 'mad dog', 'dubose',
                         'aunt alexandra', 'libel', 'unfathomable'])


# ─────────────────────────────────────────────────────────────── Chapter 8
def ch8():
    C, Q = [], []
    card(C, 'Snow in Maycomb',
         "**A rare snow falls on Maycomb and school is closed for the day.**"
         "\n• Scout has never seen snow and first thinks the world is ending."
         "\n• Mr. Avery blames the change in the weather on children who misbehave.",
         hint="To a Southern town, snow is close to a miracle; to Mr. Avery, it is a punishment.")
    card(C, 'The snowman',
         "**There isn't enough snow for a real snowman, so Jem builds one from mud and covers it with snow — and it looks just like Mr. Avery.**"
         "\n• Jem is proud of his engineering."
         "\n• The likeness to a real neighbor is the problem.",
         hint='Mud underneath, snow on top: Jem solves the shortage like a builder.')
    card(C, 'Libel',
         "**A false or damaging portrayal of a real person that hurts his reputation.**"
         "\n• Atticus calls the snowman a near libel: it mocks Mr. Avery for all to see."
         "\n• He has Jem disguise it, and Jem adds Miss Maudie's sun hat and hedge clippers.",
         hint='Libel is damage done to a name, in words or pictures.')
    card(C, "Miss Maudie's fire",
         "**On the coldest night, Miss Maudie's house catches fire and burns down.**"
         "\n• The neighbors carry her furniture out into the street."
         "\n• Atticus sends Jem and Scout to stand by the Radley gate, out of the way.",
         hint='The whole street turns out for one neighbor.')
    card(C, 'The blanket',
         "**While Scout watches the fire, someone puts a blanket around her shoulders — and she never notices.**"
         "\n• Back home, Atticus asks where the blanket came from."
         "\n• He works out that it must have been Boo Radley.",
         hint='Scout was standing right in front of the Radley house.')
    card(C, "Jem's confession",
         "**Afraid Boo will get in trouble, Jem tells Atticus everything: the pants, the knothole gifts, the cement.**"
         "\n• It all comes out at once."
         "\n• Jem is now defending Boo, not hunting him.",
         hint='Jem stops keeping secrets from Atticus once Boo needs protecting.')
    card(C, 'Miss Maudie, the next day',
         "**Miss Maudie is cheerful: she always wanted a smaller house, and now she'll have more room for her azaleas.**"
         "\n• She has lost almost everything and refuses to mourn it."
         "\n• Her attitude surprises Scout more than the fire did.",
         hint='Ask what Miss Maudie cares about more than her house.')
    card(C, 'Unfathomable',
         "**Too deep or strange to understand.**"
         "\n• The chapter opens by calling the cold snap unfathomable, even to the town's most experienced weather prophets."
         "\n• A fathom is a measure of water depth, so unfathomable means too deep to measure.",
         hint='If you cannot measure how deep it goes, you cannot get to the bottom of it.')
    card(C, 'Ponder: being looked after',
         "**Would you want to know if someone had been quietly looking out for you without your noticing?**"
         "\n• Think about how Scout feels when she learns about the blanket."
         "\n• There is no single right answer to this one.",
         hint='A dinner-table question: gratitude, or a shiver, or both?')

    q(Q, 1, 'How does Jem build a snowman when there isn\'t enough snow?',
      ['He shapes a figure out of mud and covers it with snow',
       'He carves a figure out of ice from the town icehouse',
       'He waits two days for more snow to fall before building',
       'He makes a much smaller one with the snow there is'],
      0, 'He uses what Maycomb has plenty of.',
      ['There is not enough snow for a whole snowman.',
       'Jem has dirt and mud to work with instead.',
       'He builds the body from mud.',
       'Then he covers the mud figure with snow.'],
      "**He shapes it from mud and covers it with snow.** It is clever, and it is also why the snowman can be shaped so precisely into a real person.",
      'When a character solves a problem cleverly, look for the trouble the solution causes next.')

    q(Q, 1, 'Whose house burns down in chapter 8?',
      ["Miss Maudie Atkinson's", "Miss Stephanie Crawford's",
       "Miss Rachel Haverford's", "Mr. Avery's boarding house"],
      0, 'She loves her garden more than her house.',
      ['The fire breaks out on the coldest night of the winter.',
       'The neighbors carry furniture out of a house on the Finches\' street.',
       'It is the house of the neighbor the children like best.',
       "It is Miss Maudie Atkinson's house."],
      "**Miss Maudie Atkinson's.** The fire tests her, and the next morning shows what she is made of.",
      'Recall questions are easier when you tie each event to the character it changes.')

    q(Q, 1, 'Who does Atticus conclude put the blanket around Scout\'s shoulders?',
      ['Boo Radley', 'Mr. Nathan Radley', 'Mr. Avery', 'Miss Stephanie'],
      0, 'Where was Scout standing?',
      ['Scout was standing in front of the Radley house.',
       'She never saw who covered her.',
       'Everyone else Atticus could think of was busy with the fire.',
       'Atticus concludes it was Boo Radley.'],
      "**Boo Radley.** He came out among the whole town during the fire, and nobody saw him.",
      'Use where a character was standing as evidence; setting is often a clue.')

    q(Q, 2, 'Atticus calls Jem\'s snowman "a near libel" and has him disguise it. Why?',
      ['It mocks a real neighbor in a way anyone could recognise',
       'It is built on land that belongs to Miss Maudie',
       'It uses mud, which Atticus thinks is too messy',
       'It might frighten the younger children on the street'],
      0, 'Who does the snowman look like?',
      ['Libel means damaging a real person\'s reputation.',
       'The snowman is shaped to look like Mr. Avery.',
       'Anyone walking by would recognise who it mocks.',
       'So Atticus has Jem disguise it, to spare a real neighbor.'],
      "**It mocks a real neighbor in a way anyone could recognise.** Atticus treats even a joke about Mr. Avery as something that can hurt a person's name.",
      'When a character uses a legal word for an everyday situation, ask what serious principle he is pointing to.')

    q(Q, 2, 'Put these chapter 8 events in the order they happen.',
      ['Snow falls on Maycomb and school is closed',
       'Jem builds a snowman that looks like Mr. Avery',
       "Miss Maudie's house catches fire in the night",
       'Miss Maudie says she always wanted a smaller house'],
      0, 'Snow, snowman, fire, morning after.',
      ['The chapter opens with the cold and the snow.',
       'Jem builds the snowman during the snow day.',
       'The fire comes that night, the coldest of the winter.',
       "Miss Maudie's cheerful answer comes the next day."],
      "**Snow → snowman → fire → Miss Maudie's answer.** A strange, playful day turns into a frightening night, and ends on a lesson in resilience.",
      'Use time markers — day, night, next morning — to sort the events of a chapter.', kind='order')

    q(Q, 2, 'After the fire, Jem suddenly tells Atticus all about the pants and the knothole. What makes him do it?',
      ['He is afraid Boo will get in trouble for the blanket',
       'He wants Atticus to punish Mr. Nathan for the cement',
       'He thinks Atticus already knows everything anyway',
       'He wants to boast about how brave the raid had been'],
      0, 'Who does Jem want to protect now?',
      ['Atticus has just worked out that Boo put the blanket on Scout.',
       'Jem fears Boo could be blamed for coming out.',
       'To show Boo means no harm, he explains everything Boo has done.',
       'So he tells all because he is afraid Boo will get in trouble.'],
      "**He is afraid Boo will get in trouble.** Jem has moved from daring Boo to defending him.",
      'When a character changes sides, mark the moment; it is usually what the chapter is about.')

    q(Q, 2, 'The chapter calls the cold weather "unfathomable" to the town\'s weather prophets. What does unfathomable mean?',
      ['Too deep or strange to understand',
       'Easy to see coming from far away',
       'Dangerous to anyone left outside',
       'Expected at that time every year'],
      0, 'A fathom measures how deep water is.',
      ['A fathom is a unit for measuring water depth.',
       'Un- means not, and -able means can be.',
       'So unfathomable means something whose depth cannot be measured.',
       'In other words: too deep or strange to understand.'],
      "**Too deep or strange to understand.** Even the people who claim to predict the weather cannot explain this winter.",
      'Break a long word into prefix, root and suffix before guessing.')

    q(Q, 3, 'Boo walks among the whole town during the fire and puts a blanket on Scout, and nobody sees him. What does that suggest?',
      ["People see what they expect, and no one expects a kind Boo",
       'Boo has secretly been leaving his house every single night',
       'Scout was so cold that she fell asleep standing up',
       'The town has decided to stop gossiping about the Radleys'],
      0, 'Everyone is looking for a monster.',
      ['The whole street is out, and Boo walks right through it.',
       'He does something gentle and practical: he keeps a child warm.',
       'No one notices, because no one imagines Boo doing that.',
       "So people see what they expect, and nobody expects a kind Boo."],
      "**People see what they expect.** The town's legend is so strong that Boo can be kind in plain view without anyone noticing.",
      'When a character goes unseen in a crowd, ask what the crowd was looking for instead.')

    q(Q, 3, 'Miss Maudie loses her house and says she always wanted a smaller one, with more room for her azaleas. What does this show about her?',
      ['She values her garden and her spirit over her belongings',
       'She is hiding how angry she is at the fire department',
       'She never liked her neighbors and wants to move away',
       'She does not yet understand how much she has lost'],
      0, 'What does she still have?',
      ['Her house and most of her things are gone.',
       'She talks about her flowers and the space she has now.',
       'She chooses to look at what is left, not at what burned.',
       'She values her garden and her spirit over her belongings.'],
      "**She values her garden and her spirit over her belongings.** Her cheerfulness is a choice, and it teaches Scout more than any lecture could.",
      "When a character reacts to disaster in an unexpected way, the reaction is the clue to her character.")

    q(Q, 3, 'Mr. Avery blames the snow on children who misbehave. How does the chapter treat that idea?',
      ['As a superstition that the story gently pokes fun at',
       'As the real cause, since the snow follows the raid',
       "As Atticus's own belief, which he teaches the children",
       'As a warning that the children take very seriously'],
      0, 'Who in this book tends to be right about the world?',
      ['Mr. Avery claims children\'s bad behavior changes the seasons.',
       'The narrator reports it the way she reports other Maycomb superstitions.',
       'Atticus, the book\'s steady voice, never backs it.',
       'So the chapter treats it as a superstition to smile at.'],
      "**As a superstition the story gently pokes fun at.** It is another example of Maycomb explaining what it does not understand with a story that sounds certain.",
      'Notice whose explanations the narrator trusts; the others are often there to be questioned.')

    _len_ok(Q, 8)
    chapter(8, 'Snow, Fire and a Blanket', C, Q,
            "Chapter 8 of To Kill a Mockingbird: a rare snow closes school, and Mr. Avery blames it on badly behaved children. Jem builds a mud-and-snow snowman that looks like Mr. Avery until Atticus has him disguise it. That night Miss Maudie's house burns down. While the neighbors fight the fire, someone puts a blanket around Scout without her noticing; Atticus works out it was Boo Radley, and Jem tells him everything about the pants and the knothole. The next day Miss Maudie is cheerful about her loss.",
            "Boo steps out among the whole town and does something kind, and nobody sees him. That is the strongest evidence so far that the legend is wrong.",
            [("Retell the snow day, the snowman and the fire in order.", 'source'),
             ("Explain why Atticus calls the snowman a near libel.", 'source'),
             ("Explain what the blanket reveals about Boo, and why Jem tells Atticus everything.", 'source'),
             ("Describe how Miss Maudie responds to losing her house, and what that shows.", 'added')],
            "This quiz covers chapter 8 only and stops at the end of that chapter, the day after Miss Maudie's fire. There is a house fire, though nobody is hurt; it is not graphic. The thing most likely to trip her up is the blanket: she needs to see why Atticus concludes it was Boo, and why Jem suddenly tells him everything. The ponder card about being quietly looked after is a good one for dinner.",
            ("Finish chapter 8, then run the cards and the quiz.", 10),
            passages={'q6': "For reasons unfathomable to the most experienced prophets in Maycomb County, autumn turned to winter that year."},
            later_tells=['tom robinson', 'cecil', 'christmas', 'uncle jack', 'francis',
                         "finch's landing", 'mad dog', 'dubose', 'aunt alexandra',
                         'air rifle', 'legislature', 'usual disease'])


# ─────────────────────────────────────────────────────────────── Chapter 9
def ch9():
    C, Q = [], []
    card(C, 'Cecil Jacobs',
         "**A schoolmate who announces that Scout's father defends a Black man, using a racial slur to say it.**"
         "\n• She has to come home and ask Atticus what Cecil meant."
         "\n• Atticus had asked her not to fight, so she walks away — the first fight she has ever walked away from.",
         hint='For Scout, walking away takes more nerve than swinging.')
    card(C, 'Tom Robinson',
         "**The man Atticus is defending in court.**"
         "\n• The town is angry that Atticus means to defend him properly."
         "\n• In chapter 9 the details of the case are not explained.",
         hint='Watch how people talk about Atticus once they know he has taken the case.')
    card(C, 'Why Atticus takes the case',
         "**Atticus says that if he didn't, he couldn't hold up his head in town, couldn't represent the county in the legislature, and couldn't tell his children not to do something again.**"
         "\n• It is a matter of his own conscience."
         "\n• He also tells Scout he does not expect to win.",
         hint="Atticus's reason is about who he would become if he said no.")
    card(C, 'Licked before you start',
         "**Atticus says that being beaten long before you start is no reason not to try to win.**"
         "\n• He means a fight can be worth fighting even when the odds are hopeless."
         "\n• It reframes winning as doing the right thing, not getting the result.",
         hint='Courage is trying anyway.')
    card(C, 'Uncle Jack',
         "**Atticus's younger brother, a doctor, who visits the Finches every Christmas.**"
         "\n• Scout adores him."
         "\n• At Christmas he punishes her for a fight without hearing her side, then later admits he should have listened.",
         hint='Uncle Jack is kind, but new to children; he learns from Scout.')
    card(C, "Francis and Finch's Landing",
         "**At the family Christmas at Finch's Landing, cousin Francis calls Atticus an ugly name, and Scout fights him.**"
         "\n• Francis runs to the grown-ups, and Scout is punished before anyone asks why."
         "\n• Scout asks Uncle Jack not to tell Atticus what the fight was about.",
         hint='Scout broke her promise not to fight, and it was over Atticus.')
    card(C, "Maycomb's usual disease",
         "**Atticus's name for the town's prejudice: he hopes to get his children through what is coming without catching it.**"
         "\n• Scout overhears him say this to Uncle Jack."
         "\n• She later realises Atticus knew she was listening and wanted her to hear.",
         hint='A disease you can catch from the people around you.')
    card(C, 'A ray of sunshine',
         "**Aunt Alexandra tells Scout she should be a ray of sunshine in her father's lonely life — meaning a proper little lady in a dress.**"
         "\n• Scout says you could be a ray of sunshine in pants just as well."
         "\n• Atticus says there are already enough sunbeams in the family, and he doesn't mind her the way she is.",
         hint='Two grown-ups, one girl: one wants her changed, one does not.')
    card(C, 'Ponder: when not to fight',
         "**Scout walks away from Cecil but fights Francis. Was one choice right and the other wrong?**"
         "\n• Think about what each boy said, and what Atticus asked of her."
         "\n• There is no single right answer to this one.",
         hint='A dinner-table question: is walking away ever the harder thing?')

    q(Q, 1, 'What does Cecil Jacobs announce about Atticus in the schoolyard?',
      ['That her father is defending a Black man in court',
       'That her father is running for the state legislature',
       'That her father has been asked to leave his law office',
       'That her father is moving the family out of Maycomb'],
      0, 'It is about a case Atticus has taken.',
      ['Cecil says something about Atticus in front of the schoolyard.',
       'He uses a racial slur to say it.',
       'His news is that Atticus is defending a Black man.',
       'That is the news Scout brings home to Atticus.'],
      "**That her father is defending a Black man.** Cecil says it as an insult, which tells Scout how the town sees the case before she understands it.",
      'Notice how a character first learns key news; it often sets the tone for everything after.')

    q(Q, 1, 'What does Uncle Jack do for a living?',
      ['He is a doctor', 'He is a lawyer', 'He is a teacher', 'He is a judge'],
      0, 'He works with patients.',
      ['Uncle Jack is Atticus\'s younger brother.',
       'He visits every Christmas.',
       'He works in medicine.',
       'He is a doctor.'],
      "**He is a doctor.** He is good with patients, but he still has to learn how to listen to children.",
      'Tie each minor character to one concrete fact; it makes them easy to keep apart.')

    q(Q, 1, 'Where does the Finch family spend Christmas Day in chapter 9?',
      ["At Finch's Landing", 'At the courthouse',
       "At Miss Maudie's", 'At the Radley Place'],
      0, 'It is the family home, outside town.',
      ['The Finches leave town for Christmas Day.',
       'They visit the old family home.',
       "It is called Finch's Landing."],
      "**At Finch's Landing.** The old family place is where Scout meets the fight she cannot walk away from.",
      'Settings can be named after families; that usually means the family has deep roots there.')

    q(Q, 2, 'Why does Atticus say he must take Tom Robinson\'s case?',
      ['Without it he could not hold up his head or guide his children',
       'The judge offered him a large fee to take the case at all',
       'He is sure he can win it if he works hard enough',
       'Nobody else in Maycomb knows enough law to try it'],
      0, 'It is about his conscience, not money or odds.',
      ['Scout asks him why he is defending Tom.',
       'Atticus answers in terms of who he could be afterwards.',
       'If he refused, he could not hold up his head or tell his children what to do.',
       'So he takes it to keep his self-respect and his standing as their father.'],
      "**Without it he could not hold up his head or guide his children.** Atticus's reason is about integrity, not about winning.",
      'When a character explains a hard choice, sort his reasons into "what I gain" and "who I would be". Atticus\'s are all the second kind.')

    q(Q, 2, 'Put these chapter 9 events in the order they happen.',
      ['Cecil Jacobs taunts Scout about Atticus at school',
       'Uncle Jack arrives to spend Christmas with the Finches',
       "Scout fights her cousin Francis at Finch's Landing",
       'Scout overhears Atticus talking with Uncle Jack'],
      0, 'School, visitor, fight, overheard talk.',
      ['The chapter opens at school with Cecil.',
       'Then Christmas comes, and Uncle Jack arrives.',
       "On Christmas Day, Scout fights Francis at Finch's Landing.",
       'Afterwards, Scout overhears Atticus and Uncle Jack talking.'],
      "**Cecil → Uncle Jack → the fight with Francis → the overheard talk.** The chapter moves from one walked-away fight to one she could not walk away from.",
      'Holidays are useful anchors in an order question: the events before Christmas come first.', kind='order')

    q(Q, 2, 'Uncle Jack punishes Scout for fighting Francis. What does she later tell him he did wrong?',
      ['He never let her tell her side of the story',
       'He punished her harder than Francis deserved',
       'He told Atticus about the fight right away',
       'He took Francis\'s side because he is older'],
      0, 'What did he skip before he punished her?',
      ['Francis tells the grown-ups that Scout hit him.',
       'Uncle Jack punishes her straight away.',
       'He never asks why she did it.',
       'Scout tells him he never let her tell her side.'],
      "**He never let her tell her side.** Uncle Jack admits she is right, which tells you how seriously the Finches take fairness.",
      'Fairness in this book means hearing both sides; watch for who does and who does not.')

    q(Q, 2, 'Aunt Alexandra tells Scout she should be a ray of sunshine in her father\'s lonely life, which means wearing dresses and acting like a lady. What does Atticus say when Scout asks him about it?',
      ['There are enough sunbeams in the family; she can stay as she is',
       'Her aunt is right, and she should start wearing her dresses',
       'She should humor her aunt at Christmas and forget it after',
       'Ladies are made at school, so it is her teacher\'s job now'],
      0, 'Atticus rarely asks his children to be someone else.',
      ['Aunt Alexandra wants Scout to change how she dresses and behaves.',
       'Scout argues she could be a ray of sunshine in pants.',
       'Atticus answers with a joke about the family having enough sunbeams.',
       'He does not mind her the way she is.'],
      "**There are enough sunbeams in the family already.** Atticus turns the phrase into a joke, and underneath the joke he tells Scout she does not need fixing.",
      'When two adults give a child opposite messages, ask which one the narrator lets have the last word.')

    q(Q, 3, 'Atticus tells Scout he does not expect to win, then adds this. What is he teaching her?',
      ['A fight can be worth making even when you expect to lose',
       'Anyone who has lost before should simply stop trying',
       'Winning is the only reason to take on a difficult case',
       'History has already decided how the case must end'],
      0, "He has just said he won't win. So why fight?",
      ['Atticus admits he is not going to win the case.',
       'He says being beaten long before you start is no reason not to try.',
       'The worth of the fight does not depend on the result.',
       'So a fight can be worth making even when you expect to lose.'],
      "**A fight can be worth making even when you expect to lose.** For Atticus, doing the right thing is the point, not the scoreboard.",
      'When a character admits defeat and keeps going anyway, the book is defining courage.')

    q(Q, 3, 'Scout walks away from Cecil but fights Francis. Why is the second fight harder for her to avoid?',
      ['Francis is family, and he insults Atticus at a family Christmas',
       'Francis is much bigger, so walking away would look cowardly',
       'Cecil apologises to her before the fight can even start',
       'Atticus told her that fighting relatives does not count'],
      0, 'Think about who Francis is, and where they are.',
      ['With Cecil, Scout remembers Atticus\'s request and walks away.',
       'Francis is her own cousin, at a family Christmas.',
       'He insults Atticus personally, among the family.',
       'Coming from family, the insult is harder to walk away from.'],
      "**Francis is family, and he insults Atticus at a family Christmas.** An insult from a schoolmate stings; the same insult from inside the family feels like betrayal.",
      'Compare two similar scenes and ask what is different. The difference is usually the point.')

    q(Q, 3, 'Atticus tells Uncle Jack he hopes to get his children through this without catching "Maycomb\'s usual disease." Why does it matter that he knows Scout is listening?',
      ["He wants her to hear his reasons, not just the town's version",
       'He is testing whether she will admit to listening at doors',
       'He hopes she will repeat it to Cecil and Francis at school',
       'He wants her to feel guilty about her fight with Francis'],
      0, 'Whose explanation does Atticus want her to trust?',
      ['Atticus says he hopes his children will come to him for answers, not to the town.',
       'He calls the town\'s prejudice a disease they could catch.',
       'He knew Scout was listening the whole time.',
       "So he is making sure she hears his reasons, not just the town's version."],
      "**He wants her to hear his reasons, not just the town's version.** Talking where she can hear is Atticus's way of teaching her without a lecture.",
      'When a narrator says a character meant to be overheard, reread the speech as a message to her.')

    _len_ok(Q, 9)
    chapter(9, 'Licked a Hundred Years', C, Q,
            "Chapter 9 of To Kill a Mockingbird: Cecil Jacobs taunts Scout because Atticus is defending Tom Robinson, and she walks away from the fight. Atticus explains why he has to take the case, though he does not expect to win. At Christmas, Uncle Jack visits; at Finch's Landing, cousin Francis insults Atticus and Scout fights him. Uncle Jack punishes her without hearing her side and later admits he should have listened. Scout overhears Atticus hope that his children will get through what is coming without catching Maycomb's usual disease.",
            "This is where the trial enters the story and starts to change the children's lives. Atticus explains his conscience and his idea of courage, and Scout learns that the town's anger will reach her too.",
            [("Explain why Atticus takes the case and what he means about being licked before you start.", 'source'),
             ("Compare Scout's choice with Cecil to her fight with Francis.", 'added'),
             ("Explain what Uncle Jack learns from Scout about fairness.", 'source'),
             ("Explain what Atticus means by Maycomb's usual disease.", 'source')],
            "This quiz covers chapter 9 only and stops at the end of that chapter, after Christmas. Sensitive: Cecil and Francis both use a racial slur about Atticus and the man he is defending. The quiz never prints it; it says 'a racial slur' instead. The details of the case are not given in this chapter and do not appear here. The thing most likely to trip her up is why Atticus takes a case he expects to lose. The ponder card about when to fight is a good one for dinner.",
            ("Finish chapter 9, then run the cards and the quiz.", 10),
            passages={'q7': "“Simply because we were licked a hundred years before we started is no reason for us not to try to win.”"},
            later_tells=['mad dog', 'tim johnson', 'one-shot', 'dubose', 'camellia',
                         'first purchase', 'heck tate', ' rape', 'mayella', 'sin to kill',
                         'lula', 'nigger', 'n-word'])


if __name__ == '__main__':
    ch6(); ch7(); ch8(); ch9()
