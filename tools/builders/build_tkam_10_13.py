# To Kill a Mockingbird — chapter quizzes for chapters 10, 11, 12 and 13.
# One unit per chapter, written through tkam_common.chapter(), which builds,
# balances, marks the unit book:true, attaches passages and refuses to write
# a file that mentions anything from a LATER chapter (later_tells).
#
# Spoiler rule: each quiz may look back, never forward. Nothing about the
# trial's events, Tom Robinson's fate, Bob Ewell's later actions or Boo's
# later role. The racial slur the novel uses is written "a racial slur".
# Passages are only lines quoted exactly; everything else is paraphrase.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tkam_common import card, q, chapter

# The checker warns when the right answer outruns the longest wrong one by
# more than 10%. Check it here so a draft never reaches the checker with one.
def _lengths(ch, Q):
    bad = []
    for x in Q:
        if x['kind'] != 'mc': continue
        L = [len(o) for o in x['opts']]
        rival = max(L[:x['ans']] + L[x['ans'] + 1:])
        if L[x['ans']] > rival * 1.10: bad.append((ch, x['id'], L))
    assert not bad, bad

# Tells that would only appear if a quiz reached past chapter 13.
LATE = ['trial', 'verdict', 'guilty', 'lynch', 'the mob', 'jailhouse',
        'mayella', 'missionary', 'dill runs away', 'under the bed',
        'under her bed', 'testif', 'bob ewell spit', 'courtroom', 'jury']

# ─────────────────────────────── Chapter 10 ───────────────────────────────
C, Q = [], []
card(C, 'Atticus, as his children see him',
     "**To Scout and Jem he seems feeble: nearly fifty, in glasses, and he never does anything.**\n"
     "• He works in an office. He doesn't hunt, fish, play poker, drink or smoke.\n"
     "• Asked to play in the town's football game, he says he is too old for that.",
     "Keep their list of complaints in mind. The chapter answers every one of them.")
card(C, 'A sin to kill a mockingbird',
     "**A mockingbird does no harm and only makes music, so killing one is a sin.**\n"
     "• Atticus gives the children air rifles but won't teach them to shoot; he says shoot all the bluejays they want, if they can hit them.\n"
     "• It is the only time Scout hears him call anything a sin. Miss Maudie explains: mockingbirds don't eat gardens or nest in corncribs, they just sing.",
     "This is the book's title. Start a quiet list of people in Maycomb who seem to fit the rule.")
card(C, 'Tim Johnson',
     "**A liver-colored bird dog, the pet of Maycomb, who comes down the street sick with rabies.**\n"
     "• \"Mad\" here means rabid, not angry: a bite could spread a deadly disease.\n"
     "• Jem spots him moving slowly and strangely and fetches Calpurnia.",
     "A mad dog in a quiet street: the whole neighborhood goes indoors and watches.")
card(C, 'Calpurnia in an emergency',
     "**She phones the warning to Atticus and the neighbors, then runs to the Radleys' front door herself.**\n"
     "• She asks the telephone operator to spread the word along the street.\n"
     "• Nobody in Maycomb uses the Radleys' front door. She pounds on it anyway.",
     "Notice whose house she makes sure to warn in person.")
card(C, 'The one shot',
     "**Sheriff Heck Tate hands Atticus the rifle, and Atticus drops the dog with a single shot.**\n"
     "• Heck says he can't shoot that well, and a miss would go straight into the Radley house.\n"
     "• Atticus pushes his glasses up, they fall into the street, and he fires anyway.",
     "The man with the badge hands the gun to the man in the office. That says everything.")
card(C, 'Ol\' One-Shot',
     "**Miss Maudie tells the children that Atticus was the deadest shot in Maycomb County.**\n"
     "• He put his gun down because the gift gave him an unfair advantage over most living things.\n"
     "• Her rule on bragging: people in their right minds never take pride in their talents.",
     "He didn't lose the skill. He chose not to use it.")
card(C, 'feeble',
     "**Weak and without much strength — Scout's word for her father as the chapter opens.**\n"
     "• She means too old and too quiet to do anything worth boasting about.\n"
     "• The rest of the chapter proves the word wrong.",
     "The chapter opens on this word and spends every page taking it back.")
card(C, 'Strength you don\'t show off',
     "**Atticus's ability was there all along; he simply never paraded it.**\n"
     "• Jem won't let Scout brag at school. Atticus is a gentleman, he says, just like him.\n"
     "• The children measured their father by what he displayed. The chapter measures him by what he holds back.",
     "Ask of any character: what can they do that they never mention?", frm='added')
card(C, 'Ponder: why didn\'t he ever tell them?',
     "**Atticus never once mentioned that he could shoot.**\n"
     "• Was that modesty, or did he think the skill was nothing to be proud of?\n"
     "• If you had a talent like that, would you have told your children? Worth a minute at dinner.",
     "There is no wrong answer. Be ready to say why.", frm='added')

q(Q, 1, "At the start of chapter 10, why do Scout and Jem think their father is feeble?",
  ["He's nearly fifty and never does anything exciting",
   "He is often sick and has to stay home from work",
   "He loses every argument he has with Miss Maudie",
   "He won't let them play outside after it gets dark"], 0,
  "Count his years, then list what other fathers in town do that he doesn't.",
  ["Go to Scout's complaints at the very start of the chapter.",
   "Atticus is nearly fifty, wears glasses and works in an office.",
   "He doesn't hunt, fish, play poker or join the town football game.",
   "So to them he seems feeble: he's nearly fifty and never does anything exciting."],
  "**He's nearly fifty and never does anything exciting.** Scout measures her father against the other fathers in town, the ones who hunt and play football, and he loses on every count she can see. The chapter exists to show her what she couldn't see.",
  "When a chapter opens on a list of complaints, expect its ending to test them.")
q(Q, 2, "Atticus tells Jem this about the air rifles. Why is a mockingbird different from a bluejay, according to Miss Maudie?",
  ["It does no harm and only makes music for people",
   "It is rare in Alabama and protected by the law",
   "It is too small and quick for a child to hit",
   "It eats the insects that ruin people's gardens"], 0,
  "Ask Miss Maudie's question: what does a mockingbird take from anyone?",
  ["Atticus sets the rule; Miss Maudie gives the reason when Scout asks her.",
   "Mockingbirds don't eat up people's gardens or nest in corncribs.",
   "All they do is sing their hearts out for people.",
   "So a mockingbird is different because it does no harm and only makes music."],
  "**It does no harm and only makes music.** Bluejays are pests; a mockingbird takes nothing and gives song. Killing one hurts something that never hurt anyone, which is why Atticus, who almost never calls anything a sin, calls this one.",
  "When a book's title turns up in a character's mouth, slow down. The author is handing you a key.")
q(Q, 1, "Who is Tim Johnson?",
  ["A liver-colored dog who is sick with rabies",
   "A bird dog Atticus used to hunt with as a boy",
   "A neighbor's hound who has been chasing cars",
   "A guard dog the Radleys keep in their yard"], 0,
  "Jem sees him first, at the far end of the street.",
  ["Find the moment Jem notices a dog at the end of the street.",
   "The dog is the pet of Maycomb, but today he moves slowly and strangely.",
   "Calpurnia looks and knows what it means: a mad dog.",
   "So Tim Johnson is a liver-colored dog who is sick with rabies."],
  "**A liver-colored dog who is sick with rabies.** \"Mad\" in Maycomb's mouth means rabid. Everyone's pet has become the most dangerous thing on the street, which is why the whole neighborhood shuts its doors.",
  "Old-fashioned words often mean something sharper than they do today. Check the context before you trust the modern meaning.")
q(Q, 2, "When the mad dog comes down the street, Calpurnia phones a warning and then runs to the Radley house to pound on the front door. What does that run show about her?",
  ["She warns everyone, even the family nobody visits",
   "She hopes to see Boo Radley up close at last",
   "She believes the dog came out of the Radley yard",
   "She wants Mr. Radley to come and shoot the dog"], 0,
  "Which house in Maycomb does everyone else avoid?",
  ["Calpurnia's first move is the telephone: Atticus, then the neighbors.",
   "Then she runs out into the street, toward the danger.",
   "She goes to the Radley Place, the one house the whole town keeps away from, and uses the front door nobody uses.",
   "So the run shows she warns everyone, even the family nobody visits."],
  "**She warns everyone, even the family nobody visits.** The children have spent years treating the Radley house as a haunted place. Calpurnia treats it as a home with people inside who need to be told.",
  "Watch what characters do in an emergency. Panic strips away manners and shows what they really believe.")
q(Q, 2, "Sheriff Heck Tate arrives with a rifle but hands it to Atticus instead of shooting the mad dog himself. What reason does Heck give?",
  ["He can't shoot well enough to risk a miss",
   "His own rifle had jammed on the way over",
   "The dog is on Atticus's side of the street",
   "He thinks Atticus should guard his own house"], 0,
  "Look at where the dog is standing when the shot has to be taken.",
  ["The dog is in the street in front of the Radley Place.",
   "A missed shot there would go straight into the Radley house.",
   "Heck says outright that he can't shoot that well.",
   "So he hands the rifle over: he can't shoot well enough to risk a miss."],
  "**He can't shoot well enough to risk a miss.** The sheriff, the man with the badge, defers to the father the children call feeble. It is the first hint, before Miss Maudie says a word, that they have Atticus wrong.",
  "When one character hands a job to another, ask what the first one knows that the reader doesn't yet.")
q(Q, 2, "Put these chapter 10 events in the order they happen.",
  ["Atticus gives the children air rifles but won't teach them to shoot",
   "Jem notices Tim Johnson moving strangely at the end of the street",
   "Atticus drops the dog with a single shot",
   "Miss Maudie tells the children Atticus was the deadest shot in the county"], 0,
  "The rifles come before the dog; the explanation comes after the shot.",
  ["The air rifles and the mockingbird rule come early in the chapter.",
   "Then, one February day, Jem spots Tim Johnson coming down the street.",
   "Heck Tate arrives, hands Atticus the rifle, and one shot drops the dog.",
   "Only afterwards does Miss Maudie explain what the children just saw: he was the deadest shot in Maycomb County."],
  "**Air rifles → Tim Johnson → the shot → Miss Maudie's explanation.** The chapter sets up a father who won't teach them to shoot, then shows why.",
  "In an order question, look for the setup and the payoff. The setup always comes first.", kind='order')
q(Q, 3, "Miss Maudie says Atticus gave up shooting because he felt it gave him an unfair advantage over most living things. What does that choice say about him?",
  ["He thinks a gift should be held back, not shown off",
   "He had lost his nerve after a bad hunting accident",
   "He wanted his children to become the better shots",
   "He believed hunting was against the law in Maycomb"], 0,
  "He still has the skill. The shot proves it. So what did he give up?",
  ["Start from Miss Maudie's explanation: the skill gave him an unfair advantage.",
   "He didn't lose it; the mad dog proves he still has it.",
   "He chose not to use it unless he had to, and he never bragged about it.",
   "So the choice says he thinks a gift should be held back, not shown off."],
  "**He thinks a gift should be held back, not shown off.** Atticus treats his talent as something that calls for restraint. He uses it once, because the street needs him, then hands the gun back. Miss Maudie puts it as a rule: people in their right minds never take pride in their talents.",
  "A character's refusals tell you as much as their actions. Ask what they could do and choose not to.")
q(Q, 3, "Scout wants to tell everyone at school that her father is the best shot in the county. Jem tells her not to say a word. Why?",
  ["If Atticus were proud of it, he'd have told them",
   "Nobody at school would ever believe a word of it",
   "Atticus made them promise to keep it a secret",
   "He doesn't want Scout to get credit for finding out"], 0,
  "Atticus kept this quiet for years. What does that tell Jem?",
  ["Jem has just watched his father do something nobody expected.",
   "He reasons: Atticus never mentioned it, so he isn't proud of it.",
   "Bragging would do exactly what Atticus chose not to do.",
   "So Jem keeps quiet: if Atticus were proud of it, he'd have told them."],
  "**If Atticus were proud of it, he'd have told them.** Jem copies his father's restraint on purpose. Atticus is a gentleman, he says, just like him. The boy who was embarrassed by a feeble father ends the chapter trying to be that father.",
  "When a character starts quoting or copying another, the book is showing you who they are becoming.")
q(Q, 1, "Scout says her father was feeble. In that sentence, what does feeble mean?",
  ["Weak and without much strength",
   "Strict and quick to punish",
   "Quiet and hard to understand",
   "Busy and away from home a lot"], 0,
  "She is comparing him to fathers who hunt and play football.",
  ["Look at what Scout lists next: his age, his glasses, the things he doesn't do.",
   "All of them are about strength and ability, not about strictness or time.",
   "Feeble is the word for someone without much strength.",
   "So feeble means weak and without much strength."],
  "**Weak and without much strength.** Scout means Atticus is too old and too quiet to impress anyone. The chapter is built to take the word back.",
  "Use the sentences around an unfamiliar word. Here, the list that follows is the definition.")
q(Q, 3, "By the end of chapter 10, which statement best describes how Scout and Jem's view of Atticus has changed?",
  ["His strength was there all along; he just never showed it off",
   "He is braver than they thought, but too old to be any use",
   "He is a fine shot, which makes him the best father in town",
   "He was hiding his past because he was ashamed of it"], 0,
  "Compare their list at the start with what Miss Maudie says at the end.",
  ["At the start they list what he can't do: hunt, play football, show off.",
   "The mad dog shows a skill nobody suspected, and even the sheriff defers to him.",
   "Miss Maudie explains he gave it up on purpose, not out of weakness.",
   "So the change is this: his strength was there all along; he just never showed it off."],
  "**His strength was there all along; he just never showed it off.** The chapter doesn't make Atticus a different man. It makes his children see the man who was always there.",
  "When a character seems to change, ask whether the character changed or the narrator's view of them did.")
_lengths(10, Q)
chapter(10, 'Mockingbirds and a Mad Dog', C, Q,
        "Chapter 10 of To Kill a Mockingbird: Scout and Jem decide their father is feeble, Atticus gives them air rifles with one rule about mockingbirds, and a mad dog named Tim Johnson comes down the street. Sheriff Heck Tate hands Atticus the rifle, and the children learn that their quiet father was once the deadest shot in Maycomb County.",
        "This is the chapter that gives the book its title, and it sets up the novel's idea of strength: the kind you hold back. What the children think a father should be, and what Atticus actually is, will matter for the rest of the book.",
        [("Explain why it is a sin to kill a mockingbird, in Atticus's and Miss Maudie's words.", 'source'),
         ("Describe how the mad dog changes Scout and Jem's view of their father.", 'source'),
         ("Explain why Atticus gave up shooting and why Jem won't let Scout brag.", 'source'),
         ("Start tracking which characters seem to fit the mockingbird rule.", 'added')],
        "This covers chapter 10 only and stops at the end of it: the air rifles, the mockingbird rule, the mad dog and Miss Maudie's reveal. Nothing here reaches past the chapter. A sick dog is shot in the street; it is handled briefly and without detail. The thing most likely to trip her up is reading the mockingbird line as a rule about birds only. The theme card nudges her to keep a list of who else fits it, without naming anyone. The ponder card is a good one for dinner.",
        ("Finish chapter 10, then run the cards and the quiz.", 10),
        passages={
            'q1': "“Shoot all the bluejays you want, if you can hit 'em, but remember it's a sin to kill a mockingbird.”",
            'q6': "“People in their right minds never take pride in their talents.”",
        },
        later_tells=LATE + ['dubose', 'camellia', 'morphine', 'alexandra', 'first purchase',
                            'mister jem', 'legislature', 'helen robinson', 'reverend sykes',
                            'lula', 'licked', 'beholden', 'heredity'])

# ─────────────────────────────── Chapter 11 ───────────────────────────────
C, Q = [], []
card(C, 'Mrs. Henry Lafayette Dubose',
     "**An old, sick, sharp-tongued neighbor who insults the children every time they pass.**\n"
     "• She lives two doors up the street, with a servant, Jessie, close at hand.\n"
     "• Atticus greets her with courtesy anyway, every single time.",
     "Watch how Atticus treats her, then watch how Jem does.")
card(C, 'The camellias',
     "**On Jem's twelfth birthday, after Mrs. Dubose insults Atticus, Jem cuts the tops off her camellia bushes.**\n"
     "• He uses the baton he bought Scout with his birthday money, then snaps it.\n"
     "• The insult used a racial slur and called Atticus no better than the people he works for.",
     "The calmest boy on the street finally loses his temper. Note what does it.")
card(C, 'The punishment',
     "**Atticus sends Jem back, and Mrs. Dubose asks him to read aloud to her every afternoon for a month.**\n"
     "• Scout goes with him every day.\n"
     "• An alarm clock ends each reading, and each day it rings a little later.",
     "Atticus could have punished Jem himself. He sends him to the person he wronged.")
card(C, 'Atticus and his conscience',
     "**Most of the town thinks Atticus is wrong to defend Tom Robinson; he says conscience doesn't follow majority rule.**\n"
     "• Before he can live with other folks, he has to live with himself.\n"
     "• He tells Scout the name Mrs. Dubose called him is meant as an insult, but it only shows how poor the person using it is.",
     "Majority rule works for votes. Atticus says it doesn't work for right and wrong.")
card(C, 'Morphine',
     "**Mrs. Dubose had taken morphine for her pain for years, and she broke herself of it before she died.**\n"
     "• Her frightening fits during the readings were her body fighting the drug.\n"
     "• Her mind was fixed on the alarm clock; Atticus says the reading may have been some distraction.",
     "Reread the fits once you know what they were. Nothing about them changes except what they mean.")
card(C, 'The white camellia',
     "**After she dies, Mrs. Dubose leaves Jem a candy box with one perfect white camellia inside.**\n"
     "• It is a Snow-on-the-Mountain, the kind he cut down.\n"
     "• Jem is furious, then sits turning the flower over long after Scout goes to bed.",
     "A gift from the very bushes he wrecked. Is it a jab, or a pardon?")
card(C, 'Real courage',
     "**Courage is knowing you're beaten before you start, starting anyway, and seeing it through.**\n"
     "• Atticus wanted Jem to see it, instead of thinking courage is a man with a gun in his hand.\n"
     "• By her own measure Mrs. Dubose won. Atticus calls her the bravest person he ever knew.",
     "Set this beside the mad dog in chapter 10: two kinds of brave, one chapter apart.", frm='source')
card(C, 'beholden',
     "**Owing something to someone; in their debt.**\n"
     "• Mrs. Dubose meant to leave the world beholden to nothing and nobody, not even a drug.\n"
     "• Atticus admires that, even though her views were very different from his.",
     "Be-HOLD-en: something still has a hold on you.")
card(C, 'Ponder: cruel and brave at once?',
     "**Mrs. Dubose insulted the Finches for months, and Atticus calls her the bravest person he ever knew.**\n"
     "• Does one cancel the other, or can both be true of one person?\n"
     "• Can you think of anyone you'd describe that way?",
     "There is no wrong answer. Be ready to say why.", frm='added')

q(Q, 1, "On Jem's twelfth birthday, Mrs. Dubose insults Atticus. What does Jem do next?",
  ["Cuts the tops off her camellia bushes",
   "Throws rocks at the windows of her house",
   "Shouts the insult back at her from the street",
   "Tears the screen door off her front porch"], 0,
  "He is carrying the baton he just bought for Scout.",
  ["It's Jem's twelfth birthday, and he has bought Scout a baton.",
   "Mrs. Dubose says Atticus is no better than the people he works for, using a racial slur.",
   "Jem snaps: he takes the baton into her yard.",
   "He cuts the tops off her camellia bushes."],
  "**He cuts the tops off her camellia bushes.** Jem has taken months of her insults about himself. It is the insult to Atticus that breaks him, which tells you whose dignity he cares about most.",
  "Notice which insult finally makes a patient character act. That is what they care about most.")
q(Q, 1, "What is Jem's punishment for wrecking Mrs. Dubose's camellias?",
  ["Reading aloud to her every afternoon for a month",
   "Working in her yard every Saturday until spring",
   "Paying for new bushes out of his birthday money",
   "Writing her a letter of apology every week"], 0,
  "Atticus sends him back to her, and she names the price.",
  ["Atticus doesn't punish Jem himself; he sends him to talk to Mrs. Dubose.",
   "She asks for something that costs Jem his afternoons.",
   "He must come every afternoon after school, and Scout goes with him.",
   "So the punishment is reading aloud to her every afternoon for a month."],
  "**Reading aloud to her every afternoon for a month.** It looks like a simple punishment. By the end of the chapter it turns out to have been part of something much bigger in her life.",
  "When a punishment seems oddly specific, keep it in mind. The book may explain it later.")
q(Q, 3, "Scout tells Atticus that most folks seem to think he's wrong to defend Tom Robinson. What is Atticus's answer, in plain words?",
  ["What the town thinks can't settle what he knows is right",
   "The town will change its mind once it hears the facts",
   "He would drop the case if his own family asked him to",
   "Most of the town is right, but he must finish the job"], 0,
  "He says conscience is the one thing that doesn't do something.",
  ["Scout's argument is a vote: most folks think he's wrong.",
   "Atticus grants that people are entitled to their opinions.",
   "But before he can live with other folks, he has to live with himself.",
   "Conscience doesn't follow majority rule, so the town's view can't settle what he knows is right."],
  "**What the town thinks can't settle what he knows is right.** Atticus respects the town's right to disagree, but he won't let a head count decide his conscience. That is the whole argument in a line.",
  "When a character answers an argument, check whether they dispute the facts or the method. Atticus disputes the method.")
q(Q, 2, "During the readings, an alarm clock ends each afternoon, and it rings a little later every day. Why?",
  ["She was holding out longer between doses of morphine",
   "She was falling asleep later in the afternoon",
   "She wanted to punish Jem a little more each day",
   "Jessie kept forgetting to wind the clock on time"], 0,
  "Atticus explains the clock after she dies.",
  ["Atticus tells the children Mrs. Dubose was a morphine addict.",
   "She had decided to break herself of the drug before she died.",
   "Her mind was fixed on the clock: each day she lasted a little longer.",
   "So the clock rang later because she was holding out longer between doses of morphine."],
  "**She was holding out longer between doses of morphine.** The readings that felt like a punishment to Jem were happening alongside a much harder fight. Atticus says the reading may have been some distraction for her.",
  "When a detail repeats with a small change each time, the change is the clue.")
q(Q, 2, "Put these chapter 11 events in the order they happen.",
  ["Mrs. Dubose insults Atticus on Jem's twelfth birthday",
   "Jem cuts the tops off her camellias",
   "Jem reads aloud to her every afternoon",
   "A candy box with a white camellia arrives for Jem"], 0,
  "Insult, damage, punishment, and then a gift.",
  ["The insult comes first, on Jem's twelfth birthday.",
   "Jem's temper breaks, and the camellias come down.",
   "Atticus sends him back, and the month of readings begins.",
   "After she dies, Jessie brings Jem the candy box with one white camellia."],
  "**Insult → camellias → readings → the white camellia.** The chapter ends where it started: with a camellia, now given rather than destroyed.",
  "Look for objects that come back at the end of a chapter. The repeat is usually the point.", kind='order')
q(Q, 2, "Atticus says Mrs. Dubose could have stayed on morphine and died with less pain. Why didn't she?",
  ["She meant to die owing nothing to anyone or anything",
   "Her doctor refused to give her any more of the drug",
   "She could no longer afford to pay for the medicine",
   "She wanted the children to stop coming to visit her"], 0,
  "The chapter's vocabulary word is the answer's key.",
  ["Atticus says she took morphine as a pain-killer for years.",
   "He says she could have stayed on it.",
   "But she said she would leave this world beholden to nothing and nobody.",
   "So she quit because she meant to die owing nothing to anyone or anything."],
  "**She meant to die owing nothing to anyone or anything.** Atticus says it would have been all right for someone that sick to take anything that made it easier, but it wasn't all right for her. The choice was hers, and she saw it through.",
  "A character's stated reason is worth more than a guessed one. Find the line where they say it.")
q(Q, 3, "Atticus describes real courage this way. Which situation fits his definition?",
  ["Starting a fight you expect to lose, and finishing it",
   "Winning a fight because you were the better shot",
   "Refusing a fight because you can't be sure to win",
   "Starting a fight only once you know you will win"], 0,
  "His definition has three parts. Find the option that has all three.",
  ["Break the line into three parts: you know you're licked, you begin anyway, you see it through.",
   "Being the better shot isn't it: Atticus says courage is not a man with a gun in his hand.",
   "Waiting for a sure win, or refusing to start, drops the part about beginning anyway.",
   "Only starting a fight you expect to lose, and finishing it, fits all three parts."],
  "**Starting a fight you expect to lose, and finishing it.** Atticus wants Jem to stop thinking of courage as the mad dog in the street. Mrs. Dubose was licked before she began, began anyway, and saw it through.",
  "When a definition has several parts, test each option against every part. Most wrong answers match only one.")
q(Q, 3, "Mrs. Dubose leaves Jem a candy box holding a single white camellia. What makes the gift hard to read?",
  ["It could be a last jab, or a sign of respect",
   "It shows she had forgotten all about the bushes",
   "It proves she had forgiven him from the very start",
   "It means she wanted Jem to plant her a new garden"], 0,
  "It comes from the very bushes he cut down.",
  ["The flower is a Snow-on-the-Mountain, the kind Jem wrecked.",
   "That could be a reminder of what he did.",
   "But she chose a perfect one and chose to send it to him at all.",
   "So it is hard to read: it could be a last jab, or a sign of respect."],
  "**It could be a last jab, or a sign of respect.** Jem is furious at first, then sits turning the flower over. The book gives you both readings and lets you weigh them, which is exactly what Jem is doing.",
  "When a gift could mean two things, the book often wants you to hold both.")
q(Q, 1, "Mrs. Dubose wanted to leave the world 'beholden to nothing and nobody.' What does beholden mean?",
  ["In debt to someone or something",
   "Afraid of someone or something",
   "Forgotten by someone or something",
   "Angry at someone or something"], 0,
  "What did she refuse to keep depending on?",
  ["Find what she was giving up: the morphine she had taken for years.",
   "She did not want to leave the world still depending on it.",
   "Depending on something means you owe it something.",
   "So beholden means in debt to someone or something."],
  "**In debt to someone or something.** She refused to owe her last days to a drug. The word explains the whole fight Jem and Scout were watching without knowing it.",
  "If a word is new, find what the character is trying to get free of. The word often names it.")
q(Q, 2, "Atticus keeps greeting Mrs. Dubose politely even though she insults his family. What is he showing the children?",
  ["You can stay courteous to someone who isn't",
   "Old people should be obeyed whatever they say",
   "Insults stop if you pretend not to hear them",
   "Neighbors must agree with each other in public"], 0,
  "Her manners don't change his.",
  ["Mrs. Dubose is rude to the whole family, every time.",
   "Atticus answers with courtesy, every time.",
   "He isn't agreeing with her or obeying her; he is choosing how he behaves.",
   "So he is showing that you can stay courteous to someone who isn't."],
  "**You can stay courteous to someone who isn't.** Atticus never lets someone else's rudeness decide his own manners. Jem, who loses his temper this chapter, is learning it the hard way.",
  "Compare how two characters react to the same person. The difference is usually the lesson.")
_lengths(11, Q)
chapter(11, 'Mrs. Dubose', C, Q,
        "Chapter 11 of To Kill a Mockingbird: Mrs. Dubose's insults, Jem's twelfth birthday and the wrecked camellias, a month of afternoons reading aloud to her, Atticus on conscience and majority rule, and what Atticus tells the children after she dies: about the morphine, the white camellia she left Jem, and what real courage is.",
        "Chapter 10 showed one kind of bravery, a man with a gun. Chapter 11 sets out the book's other kind, and Atticus says outright that it is the real one. His line about conscience and majority rule is the clearest statement of why he does what he does.",
        [("Explain Jem's punishment and what the alarm clock turned out to measure.", 'source'),
         ("Put Atticus's definition of courage into your own words and test it on an example.", 'source'),
         ("Explain what Atticus means when he says conscience doesn't follow majority rule.", 'source'),
         ("Weigh two readings of the white camellia and say which you find stronger.", 'added')],
        "This covers chapter 11 only and stops at the end of it, with the white camellia and Atticus's talk about courage. Nothing here reaches past the chapter. Two things to know: Mrs. Dubose insults the family with a racial slur, and the app always writes 'a racial slur' and never prints it; and morphine addiction and withdrawal are explained plainly, the way Atticus explains them to the children. The thing most likely to trip her up is the courage line. It is easy to admire as a sentence and harder to apply, so one question asks her to test it against examples. The ponder card is a good dinner question.",
        ("Finish chapter 11, then run the cards and the quiz.", 10),
        passages={
            'q2': "“… before I can live with other folks I've got to live with myself. The one thing that doesn't abide by majority rule is a person's conscience.”",
            'q6': "“It's when you know you're licked before you begin but you begin anyway and you see it through no matter what.”",
        },
        later_tells=LATE + ['alexandra', 'first purchase', 'mister jem', 'legislature',
                            'helen robinson', 'reverend sykes', 'lula', 'zeebo', 'heredity',
                            'gentle breeding'])

# ─────────────────────────────── Chapter 12 ───────────────────────────────
C, Q = [], []
card(C, 'Jem at twelve',
     "**Jem is moody and distant, and he tells Scout to stop pestering him.**\n"
     "• Calpurnia starts calling him Mister Jem.\n"
     "• Scout feels him growing up and away from her, and she can't follow yet.",
     "\"Mister Jem\": Calpurnia notices the change before Scout accepts it.")
card(C, 'No Dill this summer',
     "**Dill writes that he isn't coming to Maycomb this summer.**\n"
     "• He has a new father, and the two of them are building a fishing boat in Meridian.\n"
     "• Scout takes it hard. For her, summer was Dill.",
     "The summer without Dill is the summer Scout has to find new company.")
card(C, 'Atticus away',
     "**Atticus is called away for two weeks to an emergency session of the state legislature.**\n"
     "• That leaves Calpurnia in charge of the children.\n"
     "• It is how Scout and Jem end up at Calpurnia's church on Sunday.",
     "With Atticus gone, Calpurnia's world opens up to them.")
card(C, 'First Purchase African M.E. Church',
     "**Calpurnia's church, paid for with the first earnings of freed slaves.**\n"
     "• Black families worship there on Sundays; on weekdays white men gamble in it.\n"
     "• It has no hymnbooks, and few in the congregation can read.",
     "The name tells you its history. Freedom paid for this building.")
card(C, 'Lula and Zeebo',
     "**Lula objects to Calpurnia bringing white children to a Black church; the rest of the congregation makes them welcome.**\n"
     "• Zeebo, Calpurnia's son and Maycomb's garbage collector, greets them.\n"
     "• For one Sunday morning, Scout and Jem are the outsiders.",
     "One person turns them away; a whole room takes them in. Notice which the book lingers on.")
card(C, 'lining a hymn',
     "**Reading out a line of a hymn so the congregation can sing it back.**\n"
     "• Zeebo does it at First Purchase, because there are no hymnbooks and few people can read.\n"
     "• The song moves one line at a time: spoken, then sung.",
     "A hymn passed along a line at a time, like a rope hand over hand.")
card(C, 'The collection for Helen Robinson',
     "**Reverend Sykes keeps the church doors shut until the collection for Helen Robinson reaches ten dollars.**\n"
     "• Helen is the wife of Tom Robinson, who has been accused of raping Bob Ewell's daughter.\n"
     "• Since then, people won't give Helen work, so the congregation gives what little it has.",
     "Ten dollars, from people who have very little: count it as a measure of the room.")
card(C, 'Calpurnia\'s two ways of talking',
     "**At church Calpurnia talks the way her congregation talks; at the Finches' she talks the way the Finches do.**\n"
     "• Talking the other way at church would look like putting on airs.\n"
     "• She says folks don't like having somebody around who knows more than they do.\n"
     "• Scout is amazed. Calpurnia has a whole life Scout never thought about.",
     "Think of how you talk to friends and how you talk to a teacher. Calpurnia is doing the same.")
card(C, 'Ponder: being the outsider',
     "**For one Sunday, Scout and Jem are the ones who don't belong, and most of the room makes space for them anyway.**\n"
     "• Why might Lula have felt the way she did?\n"
     "• Where in Maycomb are those roles reversed every day of the week?",
     "There is no wrong answer. Be ready to say why.", frm='added')

q(Q, 1, "Why isn't Dill coming to Maycomb this summer?",
  ["He has a new father and is staying in Meridian",
   "He is sick and has to stay in bed all summer",
   "His aunt Rachel has moved away from Maycomb",
   "He has been sent to a summer school for boys"], 0,
  "His letter is about a boat.",
  ["Scout gets a letter from Dill.",
   "He writes that he has a new father.",
   "The two of them are building a fishing boat in Meridian.",
   "So he isn't coming because he has a new father and is staying in Meridian."],
  "**He has a new father and is staying in Meridian.** After years of Dill's stories about fathers, this one seems real. Scout's summer, though, loses its center.",
  "When a regular character drops out, ask whose story the space opens up for.")
q(Q, 1, "Who looks after Scout and Jem while Atticus is away at the legislature?",
  ["Calpurnia", "Miss Maudie", "Aunt Alexandra", "Miss Stephanie"], 0,
  "She takes them to her own church on Sunday.",
  ["Atticus is called away for two weeks.",
   "The person already running the household stays in charge.",
   "She is the one who takes them to church that Sunday.",
   "So it is Calpurnia."],
  "**Calpurnia.** With Atticus gone, the children spend a Sunday in her world instead of theirs, and they see a side of her they never knew.",
  "When a parent leaves a story for a while, watch who steps forward. The book is about to show you that character up close.")
q(Q, 2, "Lula meets Calpurnia at the church and objects to the children. What is her complaint?",
  ["White children don't belong in a Black church",
   "The children arrived too late for the service",
   "Calpurnia didn't ask Reverend Sykes first",
   "The children were dressed too plainly for it"], 0,
  "Lula says the white people have their church and this one is theirs.",
  ["Lula steps up as Calpurnia and the children arrive.",
   "She says Calpurnia has no business bringing white children there.",
   "Her point: the white people have their own church, and this one is theirs.",
   "So her complaint is that white children don't belong in a Black church."],
  "**White children don't belong in a Black church.** Lula turns Maycomb's usual rule around for one morning. The rest of the congregation answers her by making room.",
  "When a minor character objects, ask what rule they are pointing to. It is often the town's rule seen from the other side.")
q(Q, 2, "Zeebo 'lines' the hymns at First Purchase. Why does the church sing this way?",
  ["There are no hymnbooks, and few can read",
   "Reverend Sykes forbids musical instruments",
   "The congregation prefers to sing very slowly",
   "It is the oldest custom in the Methodist church"], 0,
  "Look at what the church doesn't have, and what most of the congregation can't do.",
  ["Scout notices there are no hymnbooks in the church.",
   "She also learns that few of the congregation can read.",
   "So Zeebo reads each line aloud and everyone sings it back.",
   "The church lines its hymns because there are no hymnbooks, and few can read."],
  "**There are no hymnbooks, and few can read.** The custom grows out of what the church has been denied. It also shows Scout that being able to read, which she takes for granted, is not something everyone gets.",
  "When a custom seems odd, look for the practical problem it solves.")
q(Q, 2, "Put these chapter 12 events in the order they happen.",
  ["Calpurnia takes Scout and Jem to First Purchase",
   "Lula objects to the children at the church",
   "Reverend Sykes collects ten dollars for Helen Robinson",
   "Aunt Alexandra is waiting on the Finches' porch"], 0,
  "Arrive, objection, service, home.",
  ["Calpurnia scrubs the children and walks them to her church.",
   "Lula objects as they arrive, and the congregation makes them welcome.",
   "During the service, Reverend Sykes keeps the doors shut until the collection reaches ten dollars.",
   "They walk home and find Aunt Alexandra sitting on the porch."],
  "**First Purchase → Lula → the collection → Aunt Alexandra.** The chapter opens a door into Calpurnia's world and closes on a new arrival in the Finches' own.",
  "Order questions often hinge on the chapter's last line. Find where the chapter ends and work back.", kind='order')
q(Q, 3, "Reverend Sykes keeps the church doors closed until the collection for Helen Robinson reaches ten dollars. What does that show about the congregation?",
  ["They give what little they have to help a neighbor",
   "They are mostly wealthy and can easily spare it",
   "They are angry that Helen has asked for charity",
   "They hope the money will impress their white guests"], 0,
  "Remember who sits in that church and what they can afford.",
  ["The congregation is poor: no hymnbooks, few who can read.",
   "Helen can't get work, so she can't feed her family.",
   "The church doesn't let anyone leave until ten dollars has been given.",
   "So the collection shows they give what little they have to help a neighbor."],
  "**They give what little they have to help a neighbor.** Ten dollars is a lot for that room. The church closes ranks around Helen when much of Maycomb has turned its back on her family.",
  "Weigh a gift against what the giver has, not against what it would cost you.")
q(Q, 2, "At church Calpurnia talks the way her congregation talks. What reason does she give for not talking the way she does at the Finches'?",
  ["Talking the other way would seem like putting on airs",
   "Her church friends asked her to speak more like them",
   "She doesn't want Atticus to hear about her church",
   "She is worried the children will copy her at home"], 0,
  "She asks Scout and Jem to imagine talking her way at home.",
  ["Calpurnia asks the children how it would sound if they talked her church's way at home.",
   "It would be out of place.",
   "The same is true for her at church: her neighbors would think she was showing off.",
   "So her reason is that talking the other way would seem like putting on airs."],
  "**Talking the other way would seem like putting on airs.** Calpurnia fits her speech to the people she is with. It isn't hiding; it's good manners in two worlds.",
  "When a character explains a habit, look for the comparison they use. Calpurnia makes the children imagine themselves in her place.")
q(Q, 3, "Calpurnia speaks one way at the Finches' and another at First Purchase, and Scout is amazed. What does Scout's surprise reveal?",
  ["She never imagined Calpurnia had a life apart from them",
   "She is upset that Calpurnia hid her church from them",
   "She thinks Calpurnia has been lying to the family",
   "She is jealous that Jem knew about it all along"], 0,
  "Ask what Scout had assumed about Calpurnia until that Sunday.",
  ["Scout has known Calpurnia her whole life, but only in the Finch house.",
   "At church she meets a Calpurnia with friends, a son and a way of speaking of her own.",
   "Scout had never thought about any of that before.",
   "So her surprise reveals she never imagined Calpurnia had a life apart from them."],
  "**She never imagined Calpurnia had a life apart from them.** It is the book's empathy lesson again, in a new setting: climbing into someone's skin starts with noticing they have a life you can't see from your own kitchen.",
  "A narrator's surprise often tells you what they had taken for granted.")
q(Q, 3, "Scout and Jem spend a Sunday as the only white people at First Purchase. What does the visit let them see that they couldn't see from home?",
  ["How Maycomb looks to the people it shuts out",
   "That Calpurnia's church is richer than their own",
   "That most of the church agrees with Lula's view",
   "That Calpurnia plans to stop working for Atticus"], 0,
  "Think about Lula, the hymnbooks and the collection together.",
  ["Lula's objection shows the town's color line from the other side.",
   "The missing hymnbooks and the readers who can't read show what the church has been denied.",
   "The collection shows a neighbor shut out of work being helped by those with little.",
   "Together they let the children see how Maycomb looks to the people it shuts out."],
  "**How Maycomb looks to the people it shuts out.** The children have lived in Maycomb all their lives. This chapter is the first time they stand on the other side of it.",
  "When characters visit somewhere new, ask what the visit lets them see about home.")
q(Q, 1, "Why is Calpurnia's church called First Purchase?",
  ["It was paid for with freed slaves' first earnings",
   "It was the first building bought in Maycomb County",
   "It was bought from the Finch family long ago",
   "It was the first church to buy its own hymnbooks"], 0,
  "The name is about who paid for it, and when.",
  ["The church's name comes from how it was paid for.",
   "The money came from people who had just been freed from slavery.",
   "It was among the first things they bought with their own earnings.",
   "So it is called First Purchase because it was paid for with freed slaves' first earnings."],
  "**It was paid for with freed slaves' first earnings.** The building is a record of what freedom first bought. That history sits under everything that happens there in this chapter.",
  "Names of places in this book often carry history. Stop and ask where a name came from.")
_lengths(12, Q)
chapter(12, 'First Purchase', C, Q,
        "Chapter 12 of To Kill a Mockingbird: Jem turns twelve and pulls away from Scout, Dill writes that he isn't coming, and Atticus leaves for an emergency session of the legislature. Calpurnia takes the children to her church, First Purchase, where they meet Lula, Zeebo and Reverend Sykes, see the collection for Helen Robinson, and learn about Calpurnia's life away from the Finches. They come home to find Aunt Alexandra on the porch.",
        "This is the first time Scout and Jem see Maycomb from the other side of its color line, and the first time Scout sees Calpurnia as a person with a life of her own. It is the empathy lesson from chapter 3, put to work.",
        [("Explain why the children go to First Purchase and what Lula objects to.", 'source'),
         ("Describe what lining a hymn and the collection show about the congregation.", 'source'),
         ("Explain Calpurnia's reason for talking two different ways.", 'source'),
         ("Say what the visit lets Scout see about Maycomb and about Calpurnia.", 'added')],
        "This covers chapter 12 only and stops at the end of it, as the children find Aunt Alexandra on the porch. Nothing here reaches past the chapter. One thing to know: chapter 12 states the charge against Tom Robinson, that he is accused of raping Bob Ewell's daughter. The unit states it once, briefly, on one card, and asks nothing about it. The chapter also deals directly with segregation in Maycomb's churches, through Lula's objection. The thing most likely to trip her up is reading Calpurnia's two ways of talking as hiding or lying; her own reason is about manners, and a question asks for it.",
        ("Finish chapter 12, then run the cards and the quiz.", 10),
        passages={},
        later_tells=LATE + ['heredity', 'gentle breeding', 'feminine influence',
                            'fine folks', 'streak', 'front bedroom', 'what is rape'])

# ─────────────────────────────── Chapter 13 ───────────────────────────────
C, Q = [], []
card(C, 'Aunt Alexandra moves in',
     "**Atticus's sister comes to stay, saying the children need a feminine influence.**\n"
     "• Her first words are to have her bag put in the front bedroom.\n"
     "• Atticus says she is doing him a favor: he can't be home all day, and the summer will be a hot one.",
     "She arrives as if she had always lived there. That is the whole point of her.")
card(C, 'Aunt Alexandra and Maycomb',
     "**She fits into Maycomb at once, as if she had always lived there.**\n"
     "• The town's ladies call on her, and she serves them refreshments.\n"
     "• Maycomb's way of doing things is her way of doing things.",
     "Scout struggles with Maycomb's rules; her aunt was made for them.")
card(C, 'Streaks',
     "**Aunt Alexandra judges people by their families: to her, every Maycomb family has a streak.**\n"
     "• A drinking streak, a gambling streak, a mean streak, a funny streak.\n"
     "• Know someone's family, she believes, and you know what to expect of them.",
     "A streak is a family label pinned on a person before they have done anything.")
card(C, 'Fine Folks',
     "**Scout thought Fine Folks meant people who do the best they can with the sense they have; Aunt Alexandra means old families.**\n"
     "• To her, the longer a family has sat on one patch of land, the finer it is.\n"
     "• The two definitions measure completely different things: conduct, and ancestry.",
     "Hold the two definitions side by side. The chapter is an argument between them.")
card(C, 'Finch\'s Landing',
     "**The family homestead Simon Finch founded, and the root of Aunt Alexandra's pride.**\n"
     "• She lives there with her husband, Uncle Jimmy.\n"
     "• To her, the Landing is proof that the Finches are somebody.",
     "Simon Finch from chapter 1 is where her family pride begins.")
card(C, 'gentle breeding',
     "**Coming from a long line of well-born, well-mannered people.**\n"
     "• At Aunt Alexandra's urging, Atticus tells the children to live up to it.\n"
     "• \"Gentle\" here means well-born, as in gentleman, not soft or kind.",
     "Gentle, as in gentleman: it's about the family, not the temper.")
card(C, 'Atticus takes it back',
     "**When Scout cries, Atticus drops the speech and tells them to forget it.**\n"
     "• He had been saying his sister's words, not his own.\n"
     "• The children can hear the difference.",
     "When a character sounds unlike himself, ask whose words he is using.")
card(C, 'Family pride versus how you act',
     "**Aunt Alexandra values who your people were; Atticus values what you do.**\n"
     "• The chapter puts the two views under one roof.\n"
     "• Look back: everything Atticus has taught his children so far has been about conduct, not ancestry.",
     "Sort each lesson Atticus has given so far: is it about conduct, or about family?", frm='added')
card(C, 'Ponder: does family decide who you are?',
     "**Aunt Alexandra thinks a person's family tells you most of what you need to know about them.**\n"
     "• What would Atticus say? What would you?\n"
     "• Think of someone the book has already shown to be more than their family's reputation.",
     "There is no wrong answer. Be ready to say why.", frm='added')

q(Q, 1, "Why does Aunt Alexandra say she has come to live with the Finches?",
  ["The children need a feminine influence at home",
   "She has fallen out with Uncle Jimmy at the Landing",
   "Calpurnia is leaving to look after her own family",
   "Finch's Landing has become too lonely for her"], 0,
  "She thinks something is missing from the way Scout is being raised.",
  ["Aunt Alexandra arrives at the end of chapter 12 and settles in at the start of chapter 13.",
   "She and Atticus decided it would be best for the children.",
   "Her reason: Scout, especially, needs a woman's example at home.",
   "So she says the children need a feminine influence at home."],
  "**The children need a feminine influence at home.** Her reason is mostly about Scout, who still prefers overalls to dresses. Atticus adds a practical one: he can't be home all day in a hot summer.",
  "When a character gives a reason for arriving, ask who the reason is really aimed at.")
q(Q, 1, "How does Maycomb respond to Aunt Alexandra's arrival?",
  ["It takes her in at once, as if she had always been there",
   "It ignores her, since she comes from out at the Landing",
   "It keeps away from her because Atticus is so disliked",
   "It mocks her stiff, old-fashioned manners in secret"], 0,
  "Think about who comes to call, and how quickly.",
  ["The town's ladies start calling on her almost at once.",
   "She serves refreshments and joins in Maycomb's social life.",
   "Her ideas about family and manners are the town's ideas.",
   "So Maycomb takes her in at once, as if she had always been there."],
  "**It takes her in at once, as if she had always been there.** Scout spends the book chafing against Maycomb's rules. Her aunt fits them perfectly, which tells you how much of Maycomb she brings into the Finch house.",
  "When a newcomer fits in instantly, ask what that says about the place, not just the person.")
q(Q, 2, "Aunt Alexandra says every family in Maycomb has a 'streak' — a drinking streak, a gambling streak, a mean streak. What does this show about how she judges people?",
  ["She judges a person by the family behind them",
   "She judges a person by how much money they have",
   "She judges a person by how well they did in school",
   "She judges a person by how often they go to church"], 0,
  "A streak runs through a family, not through one person.",
  ["A streak is something a whole family supposedly shares.",
   "So the label lands on a person because of their relatives.",
   "It is decided before the person does anything at all.",
   "So she judges a person by the family behind them."],
  "**She judges a person by the family behind them.** It is the opposite of Atticus's method from chapter 3: climbing into someone's skin means looking at the one person in front of you, not their family label.",
  "Ask of any judgment in this book: is it about what someone did, or about where they came from?")
q(Q, 2, "Scout thought 'Fine Folks' meant people who do the best they can with the sense they have. What does Aunt Alexandra mean by it?",
  ["Families who have lived on the same land the longest",
   "Families who give the most money to their church",
   "Families who have the best manners at the table",
   "Families who have sent their children to college"], 0,
  "She thinks time on one patch of land is what counts.",
  ["Scout's definition is about how people act.",
   "Aunt Alexandra's is about something a person can't choose.",
   "To her, the longer a family has stayed on one patch of land, the finer it is.",
   "So she means families who have lived on the same land the longest."],
  "**Families who have lived on the same land the longest.** Scout's definition rewards effort; her aunt's rewards staying put. Two people use the same phrase and mean opposite things.",
  "When two characters use the same phrase, check whether they mean the same thing by it.")
q(Q, 2, "Put these chapter 13 events in the order they happen.",
  ["Aunt Alexandra asks for her bag to go in the front bedroom",
   "Aunt Alexandra settles into Maycomb's social life",
   "Atticus tells the children to live up to their gentle breeding",
   "Atticus tells Scout to forget what he just said"], 0,
  "Arrival, settling in, a speech, and taking it back.",
  ["The chapter opens with Aunt Alexandra arriving and taking the front bedroom.",
   "Over the following weeks Maycomb's ladies call on her and she fits right in.",
   "At her urging, Atticus gives the children a speech about their family.",
   "Scout cries, and Atticus tells her to forget it."],
  "**Front bedroom → Maycomb's welcome → the speech → forget it.** The chapter builds Aunt Alexandra's influence step by step, then shows its limit: Atticus can't keep saying words that aren't his.",
  "Find the turn in a chapter: the moment the direction changes. Here it is Scout's tears.", kind='order')
q(Q, 1, "Scout cries after Atticus's speech about living up to their family name. What does Atticus do?",
  ["Tells them to forget everything he just said",
   "Sends Scout to her room until she calms down",
   "Asks Aunt Alexandra to explain it to her instead",
   "Promises to buy her a new dress for Sunday"], 0,
  "He takes the speech back.",
  ["Atticus gives the speech because his sister asked him to.",
   "Scout starts crying.",
   "Atticus drops the subject entirely.",
   "He tells them to forget everything he just said."],
  "**He tells them to forget everything he just said.** He can't keep up a speech he doesn't believe once he sees what it does to his daughter.",
  "Watch what a character does when their words hurt someone. That is often truer than the words.")
q(Q, 3, "Atticus gives the children a speech about their gentle breeding and then takes it back. What does that reveal?",
  ["The words were his sister's ideas, not his own",
   "He thinks the children are too young for manners",
   "He is afraid Aunt Alexandra will move back out",
   "He believes the Finches are better than other people"], 0,
  "Whose idea was the speech in the first place?",
  ["The speech was given at Aunt Alexandra's urging.",
   "It is about family and ancestry, which Atticus has never taught before.",
   "When it upsets Scout, he drops it at once.",
   "So it reveals the words were his sister's ideas, not his own."],
  "**The words were his sister's ideas, not his own.** Everything Atticus has taught so far is about how you treat people. The speech sounds wrong in his mouth because it is about who your people were.",
  "When a character sounds unlike himself, ask whose words he is borrowing.")
q(Q, 3, "Aunt Alexandra judges people by their families. Which earlier choice of Atticus's shows he judges people by what they do instead?",
  ["Calling Mrs. Dubose brave for how she faced her pain",
   "Telling the children to be proud of Finch's Landing",
   "Asking his sister to teach them their family's history",
   "Making the children call him Father instead of Atticus"], 0,
  "Look for a judgment that was about how someone acted.",
  ["Aunt Alexandra's measure is family and land.",
   "Look back for a time Atticus praised someone for an action.",
   "In chapter 11, he calls Mrs. Dubose the bravest person he ever knew for breaking her morphine habit.",
   "So the choice that shows his method is calling Mrs. Dubose brave for how she faced her pain."],
  "**Calling Mrs. Dubose brave for how she faced her pain.** He disagreed with nearly everything she said, but he judged her by what she did. That is the opposite of a family streak.",
  "To compare two characters' values, find a judgment each one makes and ask what it measures.")
q(Q, 2, "Atticus tells the children to live up to their 'gentle breeding.' In that phrase, what does gentle mean?",
  ["Well-born, from a respected old family",
   "Soft-spoken and kind to small animals",
   "Calm and slow to lose your temper",
   "Weak and easily hurt by others"], 0,
  "Think of the word gentleman.",
  ["Breeding here means your family line.",
   "Gentle goes with it in an older sense, the one in gentleman.",
   "That sense is about birth and rank, not temper.",
   "So gentle means well-born, from a respected old family."],
  "**Well-born, from a respected old family.** Aunt Alexandra means rank and ancestry. The everyday meaning of gentle, soft or kind, is a trap here.",
  "When an everyday word sits in an old-fashioned phrase, check for an older meaning.")
q(Q, 3, "Scout thought Fine Folks were people who do the best they can with the sense they have. Whose way of judging people is that definition closer to?",
  ["Atticus's, because it is about how people act",
   "Aunt Alexandra's, because it is about old families",
   "Calpurnia's, because it is about going to church",
   "Miss Stephanie's, because it is about town gossip"], 0,
  "Does Scout's definition measure conduct or ancestry?",
  ["Scout's definition is about effort: doing your best with what you have.",
   "That measures how a person acts, not who their family was.",
   "Atticus has judged people by their conduct all through the book.",
   "So Scout's definition is closer to Atticus's, because it is about how people act."],
  "**Atticus's, because it is about how people act.** Scout picked up her father's way of judging people without being told. Her aunt's arrival is the first time she hears the other way said out loud.",
  "When a child's idea matches a parent's, the book is often showing you what has been taught without words.")
_lengths(13, Q)
chapter(13, 'Aunt Alexandra', C, Q,
        "Chapter 13 of To Kill a Mockingbird: Aunt Alexandra moves in, saying the children need a feminine influence, and fits into Maycomb at once. Her ideas about family, heredity, streaks and Fine Folks fill the house, Finch's Landing and the family's history come up, and at her urging Atticus tells the children to live up to their gentle breeding, until Scout cries and he tells them to forget it.",
        "This chapter puts two ways of judging people under one roof: by family, or by conduct. Aunt Alexandra's arrival tests everything Atticus has taught so far, and his taking the speech back tells you which side he is on.",
        [("Explain why Aunt Alexandra comes and how Maycomb receives her.", 'source'),
         ("Compare Scout's and Aunt Alexandra's definitions of Fine Folks.", 'source'),
         ("Explain why Atticus takes back his speech about gentle breeding.", 'source'),
         ("Connect Aunt Alexandra's way of judging people to Atticus's earlier lessons.", 'added')],
        "This covers chapter 13 only and stops at the end of it, after Atticus tells the children to forget his speech about their family. Nothing here reaches past the chapter. There is nothing sensitive in this one. The thing most likely to trip her up is the word gentle in 'gentle breeding', which means well-born rather than kind; a card and a question cover it. The ponder card, about whether family decides who you are, is a good one for dinner.",
        ("Finish chapter 13, then run the cards and the quiz.", 10),
        passages={},
        later_tells=LATE + ['what is rape', 'carnal', 'calpurnia\'s house', 'runs away'])
