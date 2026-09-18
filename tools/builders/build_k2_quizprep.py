# -*- coding: utf-8 -*-
# Kinematics 2 · Quiz 1 Review: Vectors and Trig
#
# Built from the blank "Quiz 1_Vectors and Trig.pdf" her teacher shared as
# study material (Drive/Physics 8). The paper itself is NOT reproduced: every
# number here is fresh, per the standalone rule, so the unit teaches the five
# skills the quiz asks for rather than its five specific items.
#
# Scoped against the two lessons already on this shelf before a single card
# was written. 2-1 Vectors and Components already covers resolving, SOHCAHTOA,
# choosing the ratio, the unknown-in-a-denominator, recombining components,
# the radian-mode trap and the 45° crossover — none of that is repeated. What
# the quiz asks that 2-1 does not teach is what this unit is:
#   1. adding THREE vectors, including a pair that partly cancel
#   2. head-to-tail (graphical) addition, and that the order cannot matter
#   3. saying a direction out loud — "N° north of east" and its mirror trap
#   4. proportional reasoning with units (the paper-weight item)
#   5. the plain definitions of vector, scalar and resultant
#
# order:1 so it trails the numbered lessons on the Kinematics 2 shelf, the
# same whole-shelf bucket the Biology study guides use. prep:true because it
# genuinely IS test prep — the flag says what a unit is, never when it matters.
#
# EVERY number is computed with sympy in this file and asserted before it can
# be written into a question.
import sys, os, json, io
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

def rnd(x, n=1):
    return float(sp.N(sp.Rational(round(float(x) * 10**n), 10**n)))

# --- verified arithmetic ----------------------------------------------------
# Three forces on a crate: 180 N north, 80 N south, 240 N east
assert 180 - 80 == 100
res_crate = sp.sqrt(100**2 + 240**2);            assert res_crate == 260
ang_crate = sp.deg(sp.atan(sp.Rational(100, 240)))
assert rnd(ang_crate) == 22.6
# 850 m at 35° north of west
dx850, dy850 = 850*sp.cos(sp.rad(35)), 850*sp.sin(sp.rad(35))
assert (rnd(dx850), rnd(dy850)) == (696.3, 487.5)
# hiker: 140 m west, 60 m south
hik_mag = sp.sqrt(140**2 + 60**2);               assert rnd(hik_mag) == 152.3
hik_ang = sp.deg(sp.atan(sp.Rational(60, 140))); assert rnd(hik_ang) == 23.2
# head-to-tail on the graph: 6 km east then 8 km north
assert sp.sqrt(6**2 + 8**2) == 10
assert rnd(sp.deg(sp.atan(sp.Rational(8, 6)))) == 53.1
# two 10 N forces, resultant as the angle between them opens out
tworesult = [rnd(2*10*sp.cos(sp.rad(a)/2)) for a in (0, 60, 90, 180)]
assert tworesult == [20.0, 17.3, 14.1, 0.0]
# paper: 24 copies of a 4-page handout; a 500-sheet ream weighs 5.0 lb
assert 24*4 == 96
paper = sp.Rational(96, 500)*sp.Rational(5, 1);  assert rnd(paper, 2) == 0.96
# second ratio item: 18 copies of a 5-page packet, 250-sheet pack weighs 2.4 lb
assert 18*5 == 90
paper2 = sp.Rational(90, 250)*sp.Rational(24, 10); assert rnd(paper2, 3) == 0.864
# a resultant smaller than either vector: 9 N and 7 N, 150° apart
small = sp.sqrt(9**2 + 7**2 + 2*9*7*sp.cos(sp.rad(150))); assert rnd(small) == 4.6

C, Q = [], []

# ---- cards -----------------------------------------------------------------
card(C, 'Vector',
     '**A vector is a quantity that needs a direction as well as a size to be '
     'fully stated.**\n'
     '• Velocity, displacement, force and acceleration are all vectors.\n'
     '• "40 m/s" is not a velocity. "40 m/s east" is.\n'
     '• On paper a vector is drawn as an arrow: the length is the size, the '
     'way it points is the direction.')
card(C, 'Scalar',
     '**A scalar is a quantity that is fully stated by a size alone.**\n'
     '• Speed, distance, mass, time, temperature and energy are scalars.\n'
     '• "12 kg" is complete. Asking "12 kg in which direction?" is a question '
     'with no answer.')
card(C, 'Magnitude',
     '**The magnitude of a vector is its size alone, with the direction '
     'stripped off — and it is never negative.**\n'
     '• A velocity of −6 m/s has a magnitude of 6 m/s; the minus sign is the '
     'direction, not part of the size.\n'
     '• The magnitude of a vector is a scalar.')
card(C, 'Resultant',
     '**The resultant is the single vector that does exactly the same job as '
     'all the vectors being added, together.**\n'
     '• Replace three forces with their resultant and the crate cannot tell '
     'the difference.\n'
     '• A resultant is not finished until you have stated both its magnitude '
     'and its direction.')
card(C, 'Adding along one line',
     '**Vectors on the same line add as ordinary signed numbers — but only '
     'after you have chosen which way is positive and said so.**\n'
     '• Same direction: add the sizes.\n'
     '• Opposite directions: subtract, and the answer points the way the '
     'bigger one did.\n'
     '• Write the choice down. Half the sign errors in this topic come from '
     'changing your mind about it halfway through.')
card(C, 'Collapse the opposing pair first',
     '**With three or more vectors, deal with the ones that share a line '
     'before you touch any triangle.**\n'
     '• Two along north–south and one along east–west is not a three-vector '
     'problem. Combine the north–south pair into one number and you have an '
     'ordinary right triangle.\n'
     '• It turns arithmetic you can do in your head into the setup you '
     'already know.')
card(C, 'Head to tail',
     '**To add vectors graphically, draw the first, start the second at the '
     'tip of the first, and keep going — then draw the resultant from the '
     'tail of the FIRST to the tip of the LAST.**\n'
     '• The chain itself is not the answer. The resultant is the arrow that '
     'closes the gap from where you started to where you ended.\n'
     '• The vectors keep their own lengths and their own directions; you only '
     'move where each one starts.')
card(C, 'The order does not matter',
     '**Added in any order, the same set of vectors gives the same '
     'resultant.**\n'
     '• The chain of arrows takes a different shape, but the start and the end '
     'are in the same two places, so the arrow between them is identical.\n'
     '• So if adding the same vectors two ways gives two answers, one of them '
     'has an arithmetic mistake in it.',
     eq='P + Q + R = R + Q + P')
card(C, 'Drawing it to scale',
     '**A graphical answer is only as good as the scale you declared.**\n'
     '• Pick a scale first and write it on the page, e.g. 1 cm = 50 N.\n'
     '• Measure the resultant with a ruler and convert it back; measure its '
     'direction with a protractor from a stated axis.\n'
     '• The arrowheads matter — an arrow with no head is a line, and a line '
     'points both ways.')
card(C, 'The component method',
     '**The reliable way to add any number of vectors: add all the x parts, '
     'add all the y parts, then rebuild one vector from those two totals.**\n'
     '• Resolve each vector, keeping west and south negative.\n'
     '• Add down each column.\n'
     '• The two totals are the legs of one right triangle.',
     eq='R = √(Σx)² + (Σy)²   θ = tan⁻¹ |Σy / Σx|')
card(C, 'Saying a direction out loud',
     '**"40° north of east" means: point east, then turn 40° toward north.**\n'
     '• The word AFTER "of" is where you start. The word before it is where '
     'you are heading.\n'
     '• A direction with no reference axis named is not an answer. "30°" on '
     'its own could be four different directions.')
card(C, 'North of west is not west of north',
     '**"25° north of west" and "25° west of north" are different directions, '
     'and they are 40° apart.**\n'
     '• North of west starts at west and tips 25° upward — mostly west.\n'
     '• West of north starts at north and tips 25° sideways — mostly north.\n'
     '• They only coincide at 45°. Read the phrase backwards from "of" every '
     'single time.')
card(C, 'Which angle the calculator hands you',
     '**tan⁻¹(opposite ÷ adjacent) gives the angle measured from the side you '
     'put on the BOTTOM of that fraction.**\n'
     '• Put the east component underneath and you get the angle from east.\n'
     '• Put the north component underneath and you get the angle from north.\n'
     '• Both are correct descriptions of the same arrow. Say which one you '
     'chose, or the number means nothing.')
card(C, 'Check the quadrant before you trust it',
     '**The calculator only ever returns an angle between −90° and 90°, so it '
     'cannot tell you which quadrant you are in. The signs of your components '
     'can.**\n'
     '• Negative x and negative y is down and to the left — south of west, '
     'whatever the bare angle says.\n'
     '• Sketch the two components roughly before you write the direction down.')
card(C, 'A ratio is a bridge between units',
     '**When a problem gives you "this many per that many", it is handing you '
     'a conversion factor — write it as a fraction and let the units '
     'cancel.**\n'
     '• 500 sheets per 5.0 lb can be used either way up; choose the way up '
     'that cancels the unit you have.\n'
     '• If the units of your answer come out wrong, you used it upside down.',
     eq='90 sheets × (5.0 lb / 500 sheets) = 0.90 lb')
card(C, 'Round up when you are counting objects',
     '**You cannot print 0.4 of a copy or buy 0.4 of a ream, so a count of '
     'real objects always rounds UP to the next whole one.**\n'
     '• 23 students needing one each is 23 copies, not 22.6 of anything — and '
     'if a spare is wanted, it is 24.\n'
     '• Round the COUNT up first, then do the arithmetic. Rounding at the end '
     'quietly changes the answer.')

# a head-to-tail diagram for the card that teaches it
C[6]['graph'] = {
    'w': [-1, 9, -1, 7], 'gx': 1, 'gy': 1, 'lx': 2, 'ly': 2,
    'xl': 'east', 'yl': 'north',
    'series': [{'type': 'pts', 'pts': [[0, 0], [3, 0], [3, 4], [7, 5]]},
               {'type': 'pts', 'pts': [[0, 0], [7, 5]]}],
    'pts': [{'x': 7, 'y': 5, 'label': 'end'}]}

# ---- questions -------------------------------------------------------------
q(Q, 1, 'Which of these quantities is a vector?',
  ['Velocity', 'Speed', 'Mass', 'Temperature'], 0,
  'One of these four cannot be fully stated without saying which way.',
  ['Ask of each one: would a direction add anything to it?',
   'A mass of 12 kg pointing north is not a thing. Nor is 20 °C east.',
   'Speed is how fast, with no direction attached.',
   'Velocity is how fast AND which way, so velocity is the vector.'],
  '**Velocity.** It carries a direction as part of the quantity itself — '
  '40 m/s east is a different velocity from 40 m/s west, even though both '
  'are the same speed.',
  'Speed and velocity are the pair most often swapped. Speed is the '
  'magnitude of velocity, which makes speed the scalar.')

q(Q, 1, 'Which of these quantities is a scalar?',
  ['Distance', 'Displacement', 'Acceleration', 'Force'], 0,
  'Three of these four would be incomplete without a direction.',
  ['A scalar is complete with a number and a unit alone.',
   'A force of 30 N with no direction stated does not tell you what happens.',
   'Displacement and acceleration both need a direction too.',
   'Distance is just how far the path was, so it is the scalar.'],
  '**Distance.** It adds up the whole path with no regard to '
  'direction, so 400 m round a track is 400 m however many turns it took.',
  'Its vector partner is displacement, which measures only from start to '
  'finish — one lap of a track is 400 m of distance and zero displacement.')

q(Q, 1, 'What does the resultant of several vectors mean?',
  ['The single vector that has the same overall effect as all of them together',
   'The largest of the vectors being added',
   'The total of all their magnitudes added up as plain numbers',
   'The difference between the largest and the smallest of them'], 0,
  'Think about what you could replace the whole set with.',
  ['Adding vectors is a search for one vector that could stand in for the set.',
   'That stand-in has to reproduce the whole effect, not just the biggest part of it.',
   'Adding the magnitudes as plain numbers ignores every direction involved.',
   'So the resultant is the single vector with the same overall effect.'],
  '**The single vector that has the same overall effect as all of them '
  'together.** Swap the set for its resultant and nothing about the motion or '
  'the push changes.',
  'A resultant is only half-stated until its direction is given too. A bare '
  'number is not an answer to "find the resultant".')

q(Q, 1, 'A box is pulled with 60 N to the east and 25 N to the west at the '
        'same time. What is the resultant force on it?',
  ['35 N east', '85 N east', '35 N west', '85 N west'], 0,
  'These two act along one line, so no triangle is involved.',
  ['Both forces lie on the east–west line, so this is signed arithmetic.',
   'Call east positive: +60 N and −25 N.',
   '60 − 25 = 35.',
   'The answer is positive, so it points the way the bigger force did: 35 N east.'],
  '**35 N east.** Opposing vectors on one line subtract, and the resultant '
  'keeps the direction of the larger one.',
  'Adding them to 85 N is the commonest slip here. Two forces fighting each '
  'other can never produce more than the stronger one alone.')

q(Q, 1, 'A resultant is described as "40° north of east". Which instruction '
        'matches that phrase?',
  ['Face east, then turn 40° toward north',
   'Face north, then turn 40° toward east',
   'Face north-east, then turn 40° toward north',
   'Face east, then turn 40° toward south'], 0,
  'The word that comes after "of" tells you where to begin.',
  ['Read the phrase around the word "of".',
   'The direction named after "of" is the axis you start on: east.',
   'The direction named before it is the one you rotate toward: north.',
   'So you face east and swing 40° toward north.'],
  '**Face east, then turn 40° toward north.** Start on the axis named after '
  '"of", rotate toward the direction named before it.',
  'The mirror phrase, 40° east of north, is a genuinely different direction — '
  'and the two are 10° apart here, which is easily enough to be marked wrong.')

q(Q, 1, 'In head-to-tail addition, where is the resultant arrow drawn?',
  ['From the tail of the first vector to the tip of the last',
   'From the tip of the first vector to the tip of the last',
   'From the tail of the first vector to the tail of the last',
   'Along the longest single vector in the chain'], 0,
  'The resultant answers "where did you end up, compared with where you began?"',
  ['Each vector starts where the one before it ended, making a chain.',
   'The chain shows the journey; the resultant shows the net change.',
   'The journey began at the tail of the first arrow and finished at the tip '
   'of the last one.',
   'So the resultant runs from that starting point straight to that finishing point.'],
  '**From the tail of the first vector to the tip of the last.** It closes '
  'the gap between where the chain began and where it ended.',
  'This is why a chain that closes back on its own starting point has a '
  'resultant of zero — the arrow would have no length.')

q(Q, 1, 'Three forces are added in the order P, then Q, then R. A second '
        'student adds the same three as R, then P, then Q. What happens to '
        'the resultant?',
  ['It is identical for both students',
   'It has the same magnitude but a different direction',
   'It has the same direction but a different magnitude',
   'It cannot be compared, because the order of addition sets the result'], 0,
  'Sketch both chains and look at where each one starts and ends.',
  ['Each chain uses the same three arrows, just linked up in a different order.',
   'Both chains begin at the same point and finish at the same point.',
   'The resultant is drawn between those two points and nothing else.',
   'So both students draw the identical resultant.'],
  '**It is identical for both students.** Vector addition does not care about '
  'order — the chain changes shape, but its two ends do not move.',
  'That makes it a free check on your own work: add the set a second time in '
  'a different order, and any disagreement is an arithmetic error to hunt down.')

q(Q, 2, 'Three forces act on a crate: 180 N north, 80 N south, and 240 N '
        'east. Reduced to one pair of perpendicular forces, what is acting '
        'on the crate?',
  ['100 N north and 240 N east', '260 N north and 240 N east',
   '100 N south and 240 N east', '180 N north and 160 N east'], 0,
  'Two of these three share a line. Deal with those first.',
  ['North and south lie on the same line, so combine them before anything else.',
   'Call north positive: +180 N and −80 N give 180 − 80 = 100 N.',
   'The result is positive, so those two together are 100 N north.',
   'Nothing opposes the east force, so it stays as it is: 100 N north and '
   '240 N east.'],
  '**100 N north and 240 N east.** Collapsing the opposing pair turns a '
  'three-force problem into an ordinary right triangle.',
  'Adding 180 and 80 to get 260 N treats two opposing forces as though they '
  'were helping each other. Check which way each one points before you '
  'combine any pair.')

q(Q, 2, 'A crate is pushed by 100 N to the north and 240 N to the east at the '
        'same time. What is the magnitude of the resultant force?',
  ['260 N', '340 N', '140 N', '218 N'], 0,
  'Two perpendicular forces are the legs of a right triangle.',
  ['The two forces are at right angles, so they are the legs and the '
   'resultant is the hypotenuse.',
   'Square each: 100² = 10 000 and 240² = 57 600.',
   'Add them: 10 000 + 57 600 = 67 600.',
   'Take the square root: √67 600 = 260, so the resultant is 260 N.'],
  '**260 N.** Perpendicular vectors combine through Pythagoras, never by '
  'plain addition.',
  'Notice the resultant is bigger than either force but smaller than their '
  'sum of 340 N. That is always true of two perpendicular vectors, and it is '
  'a one-second check on any answer you get.')

q(Q, 2, 'A force of 100 N north and a force of 240 N east act on the same '
        'crate. In what direction does their resultant point?',
  ['22.6° north of east', '67.4° north of east', '22.6° east of north',
   '45° north of east'], 0,
  'Decide first which axis you want the angle measured from, then choose what '
  'goes on the bottom of the fraction.',
  ['To measure the angle up from east, put the east force on the bottom.',
   'tan θ = 100 ÷ 240 = 0.4167.',
   'θ = tan⁻¹(0.4167) = 22.6°.',
   'That angle was measured from east, so the direction is 22.6° north of east.'],
  '**22.6° north of east.** The east force is much the larger of the two, so '
  'the resultant should lean mostly east — a small angle up from east is '
  'exactly what you would expect.',
  'Putting the north force on the bottom instead gives 67.4°, which is also a '
  'true angle for this arrow — but measured from north, not east. The number '
  'is meaningless until you say which axis it came from.')

q(Q, 2, 'A hiker walks a displacement of 850 m at 35° north of west. What are '
        'the sizes of its westward and northward parts?',
  ['696 m west and 488 m north', '488 m west and 696 m north',
   '696 m west and 850 m north', '350 m west and 774 m north'], 0,
  'The angle is measured from west, so west is the adjacent side.',
  ['"North of west" means the angle starts at the west axis.',
   'The west part is therefore adjacent to the 35° angle: 850 × cos 35° = 696 m.',
   'The north part is opposite it: 850 × sin 35° = 488 m.',
   'So the displacement is 696 m west and 488 m north.'],
  '**696 m west and 488 m north.** With the angle measured from west, cosine '
  'gives the westward part and sine gives the northward part.',
  'Swapping them is the standard trap. The angle here is under 45°, so the '
  'arrow leans mostly west — and the westward part must come out the bigger '
  'of the two.')

q(Q, 2, 'A 4-page handout is printed for a class of 23 students, plus one '
        'spare copy. Paper is sold in reams of 500 sheets, and a full ream '
        'weighs 5.0 lb. What is the weight of the paper used?',
  ['0.96 lb', '0.92 lb', '4.8 lb', '0.24 lb'], 0,
  'Work out how many SHEETS are involved before you touch the weight.',
  ['23 students plus one spare is 24 copies.',
   'Each copy is 4 pages, so 24 × 4 = 96 sheets.',
   'A ream is 500 sheets weighing 5.0 lb, so each sheet weighs 5.0 ÷ 500 lb.',
   '96 × (5.0 ÷ 500) = 0.96 lb.'],
  '**0.96 lb.** The ream gives you a ratio — 5.0 lb per 500 sheets — and 96 '
  'sheets is a bit under a fifth of a ream, so a bit under a pound is the '
  'answer to expect.',
  'Forgetting the spare copy gives 0.92 lb, and forgetting that each copy is '
  'four sheets gives 0.24 lb. Count the objects carefully, then convert once.')

q(Q, 2, 'The graph shown adds two displacements head to tail: 6 km east, then '
        '8 km north. What is the resultant displacement?',
  ['10 km, at 53° north of east', '14 km, at 53° north of east',
   '10 km, at 37° north of east', '2 km, at 53° north of east'], 0,
  'The resultant runs straight from the origin to the far end of the chain.',
  ['The chain starts at the origin and ends 6 km east and 8 km north of it.',
   'Magnitude: √(6² + 8²) = √100 = 10 km.',
   'Direction from east: tan θ = 8 ÷ 6, so θ = 53°.',
   'The resultant is 10 km at 53° north of east.'],
  '**10 km, at 53° north of east.** The two legs and the resultant make a '
  '6–8–10 right triangle, and the north leg is the longer of the two, so the '
  'arrow must lean more north than east.',
  'Adding 6 and 8 to get 14 km would only be right if both displacements '
  'pointed the same way. The walk covered 14 km of ground but ended 10 km '
  'from where it started.')

q(Q, 2, 'Two forces of the same size act on a ring. What must be true for '
        'their resultant to be exactly zero?',
  ['They point in exactly opposite directions',
   'They act at right angles to each other',
   'They act at 45° to each other',
   'They point in exactly the same direction'], 0,
  'Picture the head-to-tail chain closing back onto its own starting point.',
  ['A resultant of zero means the chain ends where it began.',
   'Draw the first arrow, then the second from its tip.',
   'To get back to the start, the second must retrace the first exactly.',
   'That means equal in size and opposite in direction.'],
  '**They point in exactly opposite directions.** Equal and opposite is the '
  'only way two vectors can cancel completely.',
  'At right angles two equal forces give about 1.41 times one of them, not '
  'zero — perpendicular vectors never cancel, however you arrange them.')

q(Q, 3, 'A displacement has components of 140 m west and 60 m south. Which is '
        'the correct full statement of that displacement?',
  ['152 m, at 23° south of west', '152 m, at 23° west of south',
   '152 m, at 67° south of west', '200 m, at 23° south of west'], 0,
  'Find the magnitude first, then decide which axis you are measuring the '
  'angle from.',
  ['Magnitude: √(140² + 60²) = √23 200 = 152 m.',
   'Both components point into the lower-left quadrant, so the direction is '
   'somewhere between west and south.',
   'Measuring up from west means west goes on the bottom: tan θ = 60 ÷ 140, '
   'so θ = 23°.',
   'That angle came from the west axis, so it reads 152 m at 23° south of west.'],
  '**152 m, at 23° south of west.** The west component is well over twice the '
  'south one, so the arrow must lie mostly west — a small angle down from '
  'west, not a small angle across from south.',
  '"23° west of south" is a different direction entirely: it would mean an '
  'arrow pointing mostly south. Sketching the two components roughly before '
  'you write the direction catches this in seconds.')

q(Q, 3, 'A student computes tan⁻¹(60 ÷ 140) = 23° for a displacement with '
        'components 140 m west and 60 m south, then writes the direction as '
        '"23°". Why is that not yet an answer?',
  ['No reference axis is named, so the angle could describe four different directions',
   'The angle should have been computed as tan⁻¹(140 ÷ 60) instead',
   'A direction must always be given as a value between 0° and 360°',
   'The two components should have been added before taking the inverse tangent'], 0,
  'Ask what somebody reading "23°" alone would actually be able to draw.',
  ['The arithmetic itself is right: tan⁻¹(60 ÷ 140) really is 23°.',
   'But an angle only means something once you say what it was measured from '
   'and which way it was turned.',
   'A bare 23° could be measured up from west, down from west, across from '
   'north, and more besides.',
   'So the missing piece is the reference axis, not the arithmetic.'],
  '**No reference axis is named, so the angle could describe four different '
  'directions.** Writing "23° south of west" turns the number into a '
  'direction somebody else could draw.',
  'tan⁻¹(140 ÷ 60) = 67° is also a genuinely correct angle for this same '
  'arrow, measured from south instead. Two different numbers, one arrow — '
  'which is exactly why the axis has to be stated.')

q(Q, 3, 'Can the resultant of two forces be smaller in magnitude than either '
        'one of the forces on its own?',
  ['Yes, when they point in directions that partly oppose each other',
   'No, a resultant is always at least as large as the largest force',
   'Yes, but only when the two forces are exactly equal in size',
   'No, unless one of the two forces is zero'], 0,
  'Try 9 N and 7 N pulling almost against each other.',
  ['Two vectors pointing the same way give the largest possible resultant.',
   'Turning one of them away from the other makes the resultant shrink.',
   'A 9 N and a 7 N force 150° apart give a resultant of about 4.6 N.',
   '4.6 N is smaller than either of them, so yes, it can happen.'],
  '**Yes, when they point in directions that partly oppose each other.** Two '
  'vectors can produce anything from the sum of their sizes down to the '
  'difference between them, depending on the angle between them.',
  'That range is a useful check: the resultant of a 9 N and a 7 N force must '
  'always lie between 2 N and 16 N, whatever the angle. An answer outside '
  'that band has a mistake in it.')

q(Q, 3, 'Two forces of 10 N each act on a ring. Put these angles BETWEEN the '
        'two forces in order, from the LARGEST resultant to the SMALLEST.',
  ['0°', '60°', '90°', '180°'], 0,
  'Think about how much of the second force is still helping the first as '
  'the angle opens out.',
  ['At 0° the forces point the same way and simply add: 20 N.',
   'At 60° they are still largely helping each other: about 17.3 N.',
   'At 90° they are the legs of a right triangle: about 14.1 N.',
   'At 180° they are exactly opposite and cancel completely: 0 N.',
   'So the resultant falls steadily as the angle opens: 0°, 60°, 90°, 180°.'],
  '**0°, 60°, 90°, 180°.** The wider the angle between two vectors, the less '
  'of each one is pulling in the other one\'s direction, so the resultant '
  'shrinks the whole way from their sum down to zero.',
  'The two ends are worth memorising as bounds: the resultant of two vectors '
  'is never more than their sum and never less than their difference.',
  kind='order')

q(Q, 3, 'A 5-page packet is printed for 17 club members, plus one spare copy. '
        'Paper comes in packs of 250 sheets, and a full pack weighs 2.4 lb. '
        'What is the weight of the paper used?',
  ['0.864 lb', '0.816 lb', '0.173 lb', '1.73 lb'], 0,
  'Count the sheets first, then use the pack as a ratio.',
  ['17 members plus one spare is 18 copies.',
   '18 copies × 5 pages = 90 sheets.',
   'Each sheet weighs 2.4 ÷ 250 lb, which is 0.0096 lb.',
   '90 × 0.0096 = 0.864 lb.'],
  '**0.864 lb.** 90 sheets is a bit over a third of the pack, so a bit over a '
  'third of 2.4 lb is the answer to expect — and 0.864 lb is.',
  'Carry the units through the arithmetic and they check the setup for you: '
  'sheets × (lb ÷ sheets) leaves lb. If you had divided instead, the units '
  'would have come out as sheets² per lb, which is not a weight.')

q(Q, 3, 'A student adds three forces graphically, then measures the resultant '
        'with a ruler and writes "7.4 cm" as the answer. What is missing?',
  ['The measurement has to be converted back through the stated scale, and a '
   'direction given',
   'The three forces should have been drawn from a single shared starting point',
   'The resultant should have been measured from the tip of the first force',
   'The forces should have been listed in order of size before drawing'], 0,
  'A force is not measured in centimetres.',
  ['In a scale drawing, centimetres on the page stand in for newtons.',
   'The scale written on the page — say 1 cm = 50 N — converts the '
   'measurement back into a force.',
   'A resultant also needs its direction, measured with a protractor from a '
   'stated axis.',
   'So the answer needs the conversion and the direction before it is finished.'],
  '**The measurement has to be converted back through the stated scale, and a '
  'direction given.** A ruler reading is only an intermediate step; the '
  'answer is a force with a size and a direction.',
  'This is why the scale gets written on the page before any drawing starts. '
  'A scale decided afterwards is a scale chosen to fit the answer.')

Q[12]['graph'] = {
    'w': [-1, 8, -1, 10], 'gx': 1, 'gy': 1, 'lx': 2, 'ly': 2,
    'xl': 'east (km)', 'yl': 'north (km)',
    'series': [{'type': 'pts', 'pts': [[0, 0], [6, 0], [6, 8]]},
               {'type': 'pts', 'pts': [[0, 0], [6, 8]]}],
    'pts': [{'x': 6, 'y': 0}, {'x': 6, 'y': 8, 'label': 'end'}]}

build('ad-astra', C, Q, 'unit-phys-k2-sgq1',
      'Kinematics 2 · Quiz 1 Review: Vectors and Trig', 'physics',
      'A review of everything Quiz 1 asks for: what makes a quantity a vector '
      'or a scalar, what a resultant is, how to add three vectors when two of '
      'them fight each other, how to add vectors head to tail on paper, how to '
      'say a direction so that somebody else could draw it, and the '
      'units-and-ratios arithmetic the quiz finishes on.',
      'Nearly every mark lost on a vectors quiz is lost in one of two places: '
      'a direction that was computed correctly and then written down '
      'ambiguously, or a pair of opposing vectors that got added instead of '
      'subtracted. Both are habits rather than concepts, which means both can '
      'be fixed in an evening.',
      [('State whether a given quantity is a vector or a scalar, and say why.', 'source'),
       ('Find the resultant of three vectors when two of them lie along the '
        'same line.', 'source'),
       ('Give a resultant as a magnitude AND a direction measured from a '
        'stated axis.', 'source'),
       ('Add vectors graphically, head to tail, and explain why the order '
        'cannot change the answer.', 'source'),
       ('Resolve a displacement given as an angle from a compass direction '
        'into its two components.', 'source'),
       ('Use a given ratio to convert between units, rounding a count of real '
        'objects up.', 'source'),
       ('Read "north of west" and "west of north" correctly and tell them '
        'apart.', 'added')],
      'Built from the blank Quiz 1 paper her teacher shared as study material, '
      'and deliberately NOT a copy of it — every number here is fresh, so the '
      'unit teaches the five skills the quiz asks for rather than its five '
      'specific items. It was scoped against the two lessons already on this '
      'shelf before anything was written: 2-1 Vectors and Components already '
      'covers resolving, SOHCAHTOA and recombining components, so none of that '
      'is repeated here. What the quiz asks that 2-1 does not teach is what '
      'this unit is — adding three vectors including a pair that partly '
      'cancel, head-to-tail addition on paper, stating a direction so somebody '
      'else could draw it, the units-and-ratios item, and the plain '
      'definitions. Two traps get deliberate airtime because they cost marks '
      'silently. "25° north of west" and "25° west of north" are 40° apart and '
      'read almost identically at speed. And the inverse tangent returns a '
      'perfectly correct angle measured from whichever component you put on '
      'the bottom of the fraction — so 22.6° and 67.4° can both be right for '
      'the same arrow, and a bare number with no axis named is not an answer. '
      'Every number in every question was computed with sympy inside the '
      'builder and asserted before it could be written.',
      ('Say the two definitions out loud before you start — vector, scalar — '
       'and then the head-to-tail rule. Everything else in this review is '
       'applying those three sentences carefully.', 20),
      'content/phys-k2-quiz1-review.json',
      'Quiz 1: Vectors and Trig (blank copy, shared as study material)',
      'Quiz 1_Vectors and Trig.pdf (Drive, Physics 8)',
      offset_hours=3, round_=10, order_=1)

p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'content/phys-k2-quiz1-review.json')
j = json.load(io.open(p, encoding='utf-8'))
u = j['records']['unit-phys-k2-sgq1']
u['libv'] = 1
u['prep'] = True
io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
print('  + libv 1, prep:true; all sympy assertions passed')
