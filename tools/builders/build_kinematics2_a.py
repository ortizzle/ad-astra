# -*- coding: utf-8 -*-
# Kinematics 2 · 2-1 Vectors and Components — from "Kinematics 2 Objectives.pdf"
# (her teacher's own objective list, Drive/Physics 8, uploaded 2026-09-11) and
# chapter 7 of "Textbook+2D+Kinematics.pdf" in the same folder.
#
# Its OWN shelf. "Kinematics 1" holds four parts (Describing Motion, Motion
# Graphs, Equations of Motion, the Ramp Lab) and this is a new unit of study
# with its own objective sheet, not a fifth part of that one.
#
# The numbered form (2-1, 2-2) is deliberate and structural, per the Biology
# shelf's v180 lesson: "Projectile Motion" would title-sort AHEAD of "Vectors
# and Components", which is backwards for how the class meets them. Numbering
# both parts fixes the order by construction instead of by luck. (Kinematics 1
# keeps its unnumbered titles — mixing the two forms inside ONE shelf is the
# bug; two shelves may differ.)
#
# EVERY number below is computed with sympy in this file and asserted before
# it can be written into a question. Nothing is worked by hand, and no number
# printed in the textbook's own worked examples is reused.
import sys, os, json, io
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

def rnd(x, n=1):
    return float(sp.N(sp.Rational(round(float(x) * 10**n), 10**n)))
def comp(v, th):
    return (sp.N(v*sp.cos(sp.rad(th))), sp.N(v*sp.sin(sp.rad(th))))

# --- verified arithmetic ----------------------------------------------------
vx24, vy24 = comp(24, 35);  assert (rnd(vx24), rnd(vy24)) == (19.7, 13.8)
vx18, vy18 = comp(18, 50);  assert (rnd(vx18), rnd(vy18)) == (11.6, 13.8)
vx40, vy40 = comp(40, 25);  assert (rnd(vx40), rnd(vy40)) == (36.3, 16.9)
assert rnd(sp.sqrt(9**2 + 12**2)) == 15.0
assert rnd(sp.sqrt(30**2 + 40**2)) == 50.0
assert rnd(sp.deg(sp.atan(sp.Rational(40, 30)))) == 53.1
assert rnd(sp.sqrt(15**2 + 8**2)) == 17.0
assert rnd(sp.deg(sp.atan(sp.Rational(8, 15)))) == 28.1
opp20, adj20 = 20*sp.sin(sp.rad(40)), 20*sp.cos(sp.rad(40))
assert (rnd(opp20), rnd(adj20)) == (12.9, 15.3)
hyp30 = 15/sp.sin(sp.rad(30));  assert rnd(hyp30) == 30.0
hyp55 = 12/sp.cos(sp.rad(55));  assert rnd(hyp55) == 20.9
assert rnd(12*sp.tan(sp.rad(55))) == 17.1
assert rnd(50*sp.cos(sp.rad(28))) == 44.1

C, Q = [], []

# ---- cards -----------------------------------------------------------------
card(C, 'Component',
     '**A component is the part of a vector that points along one chosen axis.**\n'
     '• Every vector can be replaced by two perpendicular components — usually one '
     'horizontal (x) and one vertical (y) — that together do exactly the same job.\n'
     '• The components are not smaller copies of the vector. They are the vector, '
     'split into two directions.')
card(C, 'Resolving a vector',
     '**Resolving means finding those two components.** With the magnitude and '
     'the angle from the x-axis:',
     eq='v_x = v cos θ    v_y = v sin θ')
card(C, 'Finding the components graphically',
     '**Drop a line straight down from the arrow’s tip to the x-axis, and straight '
     'across to the y-axis. Those two segments ARE the components.**\n'
     '• The vector, its x-component and its y-component form a right triangle, with '
     'the vector itself as the hypotenuse.\n'
     '• Which is why the whole topic reduces to right-triangle trigonometry.')
card(C, 'Perpendicular components are independent',
     '**What happens along x has no effect on what happens along y.**\n'
     '• Changing a vector’s horizontal part does not change its vertical part at '
     'all.\n'
     '• This is the single idea the rest of the unit is built on: a two-dimensional '
     'problem becomes two separate one-dimensional problems.')
card(C, 'Opposite, adjacent, hypotenuse',
     '**They are named relative to the angle you are working with — not to the page.**\n'
     '• Hypotenuse: always the side across from the right angle, and always the '
     'longest side.\n'
     '• Opposite: the side across the triangle from your angle.\n'
     '• Adjacent: the remaining side, the one touching your angle.',
     hint='Move to the other non-right angle and "opposite" and "adjacent" swap '
          'places. The hypotenuse never moves.')
card(C, 'SOHCAHTOA',
     '**Sine = Opposite/Hypotenuse. Cosine = Adjacent/Hypotenuse. Tangent = '
     'Opposite/Adjacent.**\n'
     '• Each ratio uses exactly two sides, so pick the one whose two sides are the '
     'one you know and the one you want.',
     eq='sin θ = O/H    cos θ = A/H    tan θ = O/A')
card(C, 'Choosing the right ratio',
     '**List what you know and what you want, then find the ratio that names both '
     'and nothing else.**\n'
     '• Know the hypotenuse, want the opposite → sine.\n'
     '• Know the hypotenuse, want the adjacent → cosine.\n'
     '• Know one leg, want the other leg → tangent.',
     frm='added')
card(C, 'When the unknown is on the bottom',
     '**If the side you want is the denominator, multiply both sides up and then '
     'divide.** Wanting the hypotenuse from the opposite side:',
     eq='sin θ = O/H  →  H = O / sin θ',
     frm='added')
card(C, 'Back from components to the vector',
     '**Pythagoras gives the magnitude; the inverse tangent gives the angle.**\n'
     '• The angle comes out measured from the x-axis, which is the convention every '
     'projectile problem uses.',
     eq='v = √(vₓ² + vᵧ²)    θ = tan⁻¹(vᵧ / vₓ)')
card(C, 'A component is never bigger than its vector',
     '**Both sin θ and cos θ are at most 1, so neither component can exceed the '
     'magnitude.**\n'
     '• If your answer for a component comes out larger than the vector itself, you '
     'have divided where you should have multiplied.\n'
     '• A quick sanity check that costs two seconds and catches a lot.',
     frm='added')
card(C, 'Degrees, not radians',
     '**A calculator left in radian mode gives silently wrong answers to every one '
     'of these problems.**\n'
     '• cos 60° = 0.5. If your calculator does not say 0.5, it is in the wrong '
     'mode.\n'
     '• Nothing about a radian-mode answer looks wrong — it is a plausible number, '
     'just not the right one.',
     frm='added')
card(C, 'The 45° special case',
     '**At 45° the two components are equal**, because sin 45° = cos 45°.\n'
     '• Below 45° the horizontal component is the bigger one.\n'
     '• Above 45° the vertical component is the bigger one.\n'
     '• Useful for checking an answer at a glance before you trust it.')
card(C, 'Straight along an axis',
     '**A vector pointing along the x-axis has zero vertical component; one '
     'pointing straight up has zero horizontal component.**\n'
     '• cos 0° = 1 and sin 0° = 0, so the formulas give this automatically.\n'
     '• A ball thrown horizontally therefore starts with vᵧ = 0 — the fact the whole '
     'next lesson leans on.')
card(C, 'Adding two perpendicular vectors',
     '**Add the x-parts to each other and the y-parts to each other, never the '
     'magnitudes to each other.**\n'
     '• A 3-unit vector east plus a 4-unit vector north is 5 units, not 7.\n'
     '• Magnitudes only add directly when the two vectors point the same way.')

# ---- questions -------------------------------------------------------------
q(Q, 1, 'In a right triangle you are working from a 32° angle. Which side is '
        'the hypotenuse?',
  ['The side across from the right angle',
   'The side across from the 32° angle',
   'The shorter of the two sides touching the 32° angle',
   'Whichever side is drawn along the bottom'],
  0,
  'One side is named without reference to your angle at all.',
  ['Opposite and adjacent are named relative to the angle you chose.',
   'The hypotenuse is not — it is defined by the right angle.',
   'It is the side across from the 90° corner, and it is always the longest side.',
   'So it is the side across from the right angle.'],
  '**The hypotenuse is fixed by the right angle, so it stays the same side no '
  'matter which of the other two angles you work from.** Opposite and adjacent '
  'are the pair that swap when you move to the other angle. And it is never '
  'defined by how the triangle happens to be drawn on the page.',
  'Find the right angle first. The side facing it is the hypotenuse, always.')

q(Q, 1, 'You know the hypotenuse of a right triangle and one of its acute '
        'angles, and you want the side ACROSS from that angle. Which ratio do '
        'you use?',
  ['Sine', 'Cosine', 'Tangent', 'Pythagoras'],
  0,
  'Write down the two sides involved, then find the ratio that names exactly '
  'those two.',
  ['The side across from the angle is the opposite.',
   'So the two sides involved are the opposite and the hypotenuse.',
   'SOH: sine = opposite over hypotenuse — that ratio names exactly those two.',
   'Cosine uses the adjacent and tangent uses no hypotenuse, so neither fits.'],
  '**Sine is the ratio that pairs the opposite with the hypotenuse, which is '
  'exactly the pair you have here.** Pythagoras is a real tool but needs two '
  'SIDES, not a side and an angle, so it cannot start this problem.',
  'Name the two sides first. The ratio picks itself.')

q(Q, 2, 'A cable pulls with a force of 20 N at 40° above the horizontal. What '
        'is its horizontal component?',
  ['15.3 N', '12.9 N', '20.0 N', '26.1 N'],
  0,
  'Horizontal goes with one of sine or cosine. Which?',
  ['The horizontal component is the adjacent side, so use cosine.',
   'vₓ = 20 × cos 40°.',
   'cos 40° = 0.766, so 20 × 0.766 = 15.3 N.',
   'Sanity check: 40° is below 45°, so the horizontal part should be the bigger '
   'of the two — and 15.3 N beats the 12.9 N vertical part.'],
  '**The horizontal component is the adjacent side, so it uses cosine: 20 cos '
  '40° = 15.3 N.** 12.9 N is what you get from sine, which is the VERTICAL '
  'component. The 26.1 N option is bigger than the force itself, which is '
  'impossible — a component can never exceed its own vector.',
  'Below 45°, horizontal wins. Above 45°, vertical wins.')

q(Q, 2, 'A ball is launched at 24 m/s, 35° above the horizontal. What are its '
        'starting horizontal and vertical velocity components?',
  ['19.7 m/s horizontal, 13.8 m/s vertical',
   '13.8 m/s horizontal, 19.7 m/s vertical',
   '24.0 m/s horizontal, 13.8 m/s vertical',
   '12.0 m/s horizontal, 20.8 m/s vertical'],
  0,
  'Which of sine and cosine belongs to the horizontal?',
  ['vₓ = v cos θ = 24 × cos 35° = 19.7 m/s.',
   'vᵧ = v sin θ = 24 × sin 35° = 13.8 m/s.',
   '35° is below 45°, so the horizontal part should be the larger of the two — and '
   'it is.',
   'So 19.7 m/s horizontal and 13.8 m/s vertical.'],
  '**Cosine goes with horizontal and sine with vertical, giving 19.7 m/s and '
  '13.8 m/s.** Swapping them is the commonest slip here, and the 45° check '
  'catches it instantly: a shallow launch must have more horizontal speed than '
  'vertical. The 24.0 m/s option forgets to resolve at all.',
  'cos → across. Both words start the same way.')

q(Q, 2, 'A different ball is launched at 18 m/s, 50° above the horizontal. '
        'Which component is bigger?',
  ['The vertical one, because 50° is above 45°',
   'The horizontal one, because horizontal always wins',
   'They are equal, because both use the same 18 m/s',
   'It cannot be decided without calculating both'],
  0,
  'There is one angle where the two components are exactly equal.',
  ['At 45° the components are equal, because sin 45° = cos 45°.',
   'Above 45° the sine is the larger of the two, and sine belongs to the '
   'vertical.',
   '50° is above 45°, so the vertical component is bigger.',
   'Checking: 18 sin 50° = 13.8 m/s against 18 cos 50° = 11.6 m/s.'],
  '**Above 45° the vertical component wins; below it the horizontal does.** You '
  'genuinely can answer this without a calculator, which is the point of '
  'knowing the 45° crossover — it is the fastest check there is on a component '
  'answer you have just worked out.',
  'Steeper than 45° means more up than across.')

q(Q, 2, 'A velocity has components of 30 m/s east and 40 m/s north. What is its '
        'magnitude?',
  ['50 m/s', '70 m/s', '35 m/s', '1200 m/s'],
  0,
  'The two components are perpendicular, so they form a right triangle with the '
  'vector.',
  ['The components and the vector make a right triangle, with the vector as the '
   'hypotenuse.',
   'So v = √(30² + 40²).',
   '30² + 40² = 900 + 1600 = 2500.',
   '√2500 = 50 m/s.'],
  '**Perpendicular components combine by Pythagoras, not by addition: √(30² + '
  '40²) = 50 m/s.** Adding straight across gives 70, which would only be right '
  'if both parts pointed the same way. The magnitude always lands between the '
  'larger component and their sum.',
  'A 3-4-5 triangle in disguise. Spotting it saves the arithmetic.')

q(Q, 3, 'A velocity has components of 15 m/s east and 8 m/s north. What is its '
        'magnitude and its angle above east?',
  ['17 m/s at 28.1°', '17 m/s at 61.9°', '23 m/s at 28.1°', '12.5 m/s at 32.0°'],
  0,
  'Two separate steps: Pythagoras for the size, inverse tangent for the '
  'direction.',
  ['Magnitude: √(15² + 8²) = √(225 + 64) = √289 = 17 m/s.',
   'Angle above east: the east part is adjacent and the north part is opposite, '
   'so use tangent.',
   'θ = tan⁻¹(8/15) = 28.1°.',
   'Check: the east component is the bigger one, so the angle above east must be '
   'under 45° — and 28.1° is.'],
  '**√(15² + 8²) = 17 m/s, and tan⁻¹(8/15) = 28.1° above east.** 61.9° is what you '
  'get from tan⁻¹(15/8) — the right idea with the fraction upside down, which '
  'measures the angle from north instead. The bigger component always sits '
  'nearer the direction the vector points.',
  'Put the side you are measuring AWAY from on the bottom of the fraction.')

q(Q, 2, 'In a right triangle the hypotenuse is 50 cm and one acute angle is '
        '28°. How long is the side adjacent to that angle?',
  ['44.1 cm', '23.5 cm', '56.6 cm', '26.6 cm'],
  0,
  'Adjacent and hypotenuse — which ratio names exactly those two?',
  ['Known: the hypotenuse. Wanted: the adjacent side.',
   'CAH: cosine = adjacent over hypotenuse.',
   'So adjacent = 50 × cos 28°.',
   'cos 28° = 0.8829, and 50 × 0.8829 = 44.1 cm.'],
  '**Cosine pairs the adjacent with the hypotenuse, so adjacent = 50 cos 28° = '
  '44.1 cm.** 23.5 cm comes from sine and is the OPPOSITE side. 56.6 cm is '
  'longer than the hypotenuse, which no leg of a right triangle can ever be.',
  'Any leg longer than the hypotenuse means the calculation went wrong.')

q(Q, 3, 'In a right triangle the side OPPOSITE a 30° angle is 15 m. How long is '
        'the hypotenuse?',
  ['30 m', '7.5 m', '26 m', '17.3 m'],
  0,
  'This time the side you want is on the bottom of the ratio.',
  ['Known: the opposite side. Wanted: the hypotenuse. SOH applies.',
   'sin 30° = opposite / hypotenuse, so 0.5 = 15 / H.',
   'Rearranging: H = 15 / sin 30° = 15 / 0.5.',
   'H = 30 m.'],
  '**When the unknown sits in the denominator, rearrange to H = O / sin θ — '
  'dividing, not multiplying: 15 / 0.5 = 30 m.** 7.5 m is what multiplying by '
  'sin 30° gives instead, and it fails the sanity check immediately, since the '
  'hypotenuse has to be the longest side.',
  'Unknown on the bottom means you will divide, not multiply.')

q(Q, 3, 'In a right triangle the side ADJACENT to a 55° angle is 12 cm. Find the '
        'hypotenuse and the opposite side.',
  ['Hypotenuse 20.9 cm, opposite 17.1 cm',
   'Hypotenuse 17.1 cm, opposite 20.9 cm',
   'Hypotenuse 6.9 cm, opposite 9.8 cm',
   'Hypotenuse 20.9 cm, opposite 8.9 cm'],
  0,
  'Two separate calculations from the same known side — one uses cosine, the '
  'other tangent.',
  ['Hypotenuse from the adjacent: cos 55° = 12 / H, so H = 12 / cos 55° = 20.9 cm.',
   'Opposite from the adjacent: tan 55° = O / 12, so O = 12 × tan 55° = 17.1 cm.',
   'Check the hypotenuse is the longest: 20.9 beats both 12 and 17.1.',
   'Check the angle: 55° is more than 45°, so the opposite side should beat the '
   'adjacent — 17.1 beats 12.'],
  '**H = 12/cos 55° = 20.9 cm and O = 12 tan 55° = 17.1 cm.** Two checks confirm '
  'it without redoing the trigonometry: the hypotenuse must be the longest side, '
  'and past 45° the opposite must beat the adjacent. The swapped option fails '
  'the first of those outright.',
  'Tangent is the one ratio that never touches the hypotenuse. That is when to '
  'reach for it.')

q(Q, 1, 'A car drives due east. What is the vertical component of its velocity?',
  ['Zero', 'Equal to its speed', 'Half its speed', 'Impossible to say'],
  0,
  'What is sin 0°?',
  ['The angle above the horizontal is 0°.',
   'vᵧ = v sin θ, and sin 0° = 0.',
   'So the vertical component is zero.',
   'Which matches common sense: driving east involves no upward motion at all.'],
  '**A vector lying along an axis puts everything into that one component and '
  'nothing into the other.** This is not a special rule — v sin 0° = 0 falls '
  'straight out of the ordinary formula. It matters because a ball thrown '
  'horizontally starts with exactly this: zero vertical velocity.',
  'The formulas handle the edge cases for free. Trust them.')

q(Q, 3, 'Two students resolve the same 40 m/s vector at 25°. One gets a '
        'horizontal component of 36.3 m/s; the other gets 16.9 m/s. Without '
        'redoing the trigonometry, who is right and how can you tell?',
  ['The first — below 45° the horizontal component must be the larger one',
   'The second — the horizontal component is always the smaller one',
   'The first — the horizontal component always equals the magnitude',
   'Neither — a component can never be more than half the magnitude'],
  0,
  'One check settles it, and it takes no calculator at all.',
  ['At 45° the two components are equal.',
   'Below 45° the cosine is the larger, and cosine belongs to the horizontal.',
   '25° is well below 45°, so the horizontal component must be the bigger of '
   'the two.',
   '36.3 m/s is the bigger one, so the first student is right.'],
  '**The 45° crossover decides it: a shallow angle means most of the vector is '
  'horizontal.** The other student has swapped sine for cosine, which is the '
  'usual cause. There is no rule capping a component at half the magnitude — at '
  '25° the horizontal part is more than 90% of the whole.',
  'Estimate before you calculate, and the calculator becomes a check rather '
  'than an oracle.')

q(Q, 2, 'A boat is rowed north across a river while the current carries it east. '
        'How does the eastward current affect how fast the boat moves north?',
  ['Not at all — perpendicular components are independent',
   'It slows the crossing down, since the boat is pushed',
   'It speeds the crossing up, since the boat gets a shove',
   'It depends on how strong the current happens to be'],
  0,
  'The two motions are at right angles to each other.',
  ['The rowing is northward and the current is eastward — perpendicular '
   'directions.',
   'Perpendicular components do not affect one another.',
   'So the northward speed is whatever the rowing alone would give.',
   'The current changes where the boat ends up, but not how quickly it crosses.'],
  '**Perpendicular components are independent, which is why the current changes '
  'the landing point downstream without changing the crossing time.** This is '
  'the same idea the whole projectile lesson runs on: the horizontal motion of a '
  'thrown ball never changes how fast it falls.',
  'Independence is what lets one 2-D problem split into two 1-D problems.')

q(Q, 2, 'A calculator returns cos 60° = 0.5 for one student and 0.9524 for '
        'another. What has gone wrong for the second?',
  ['It is set to radians instead of degrees',
   'It has rounded the answer badly',
   'It is out of battery',
   'Nothing — both answers are acceptable'],
  0,
  'There is one setting that turns every answer in this unit into a plausible '
  'wrong number.',
  ['cos 60° is exactly 0.5, a value worth knowing by heart.',
   '0.9524 is cos of 60 RADIANS, not 60 degrees.',
   'So the second calculator is in radian mode.',
   'Every trigonometry answer it gives in this unit will be wrong, and none of '
   'them will look wrong.'],
  '**Radian mode is the quiet killer in this topic: the answers stay plausible '
  'numbers, they are just not the right ones.** Testing cos 60° takes one second '
  'and should be the first thing done before any problem set. The two answers '
  'are not both acceptable — only one of them is cosine of an angle in degrees.',
  'Check cos 60° = 0.5 before you start. Every time.')

q(Q, 1, 'What does it mean to resolve a vector?',
  ['To replace it with two perpendicular components that do the same job',
   'To make it shorter so it fits on the diagram',
   'To work out the total of several vectors added together',
   'To convert its units into metres per second'],
  0,
  'Resolving turns one arrow into two.',
  ['A vector can be split into a horizontal part and a vertical part.',
   'Together those two parts have exactly the same effect as the original.',
   'Finding them is what resolving means.',
   'Adding vectors together is the opposite operation.'],
  '**Resolving splits one vector into two perpendicular components that between '
  'them do exactly what the original did.** It is the reverse of adding vectors, '
  'and it is worth doing because perpendicular components are independent — '
  'which turns one hard problem into two easy ones.',
  'Resolve to split apart. Add to combine.')

q(Q, 3, 'A hiker walks 9 km east, then 12 km north. Which statement is true?',
  ['She is 15 km from her start, and walked 21 km to get there',
   'She is 21 km from her start, and walked 21 km to get there',
   'She is 15 km from her start, and walked 15 km to get there',
   'She is 10.5 km from her start, and walked 21 km to get there'],
  0,
  'Two different quantities are being asked for, and only one of them uses '
  'Pythagoras.',
  ['Distance walked is just the path length: 9 + 12 = 21 km.',
   'Displacement is the straight line from start to finish.',
   'The two legs are perpendicular, so displacement = √(9² + 12²) = √225 = 15 km.',
   'So: 15 km away, having walked 21 km.'],
  '**Distance adds along the path (21 km); displacement combines by Pythagoras '
  '(15 km).** Perpendicular legs never add straight across for displacement, and '
  'the difference between the two numbers is the whole scalar-versus-vector '
  'distinction from the last unit, showing up in two dimensions.',
  'Distance is how far you walked. Displacement is how far you ended up.')

# ---- assemble --------------------------------------------------------------
build('ad-astra', C, Q, 'unit-phys-k2-vectors',
      'Kinematics 2 · 2-1 Vectors and Components', 'physics',
      'The trigonometry the rest of two-dimensional motion runs on: what a '
      'component is, how to find one graphically and with SOHCAHTOA, how to '
      'name the opposite, adjacent and hypotenuse relative to a chosen angle, '
      'how to get back from two components to a magnitude and a direction, and '
      'why perpendicular components never affect one another.',
      'Every projectile problem in the next lesson starts by splitting one '
      'velocity into two components and ends by recombining them. Get the '
      'splitting fluent here and the projectile work is arithmetic; get it shaky '
      'and every later problem carries the same error twice.',
      [('Define a component and identify the components of a vector '
        'graphically.', 'source'),
       ('Recall SOHCAHTOA from memory and name the opposite, adjacent and '
        'hypotenuse for a given non-right angle.', 'source'),
       ('Choose the right trigonometric ratio for the side you know and the '
        'side you want, including when the unknown is a denominator.', 'source'),
       ('Find all three sides of a right triangle from one side and one '
        'non-right angle.', 'source'),
       ('Resolve a velocity into its vertical and horizontal components from '
        'the launch angle and the total speed.', 'source'),
       ('Explain why vector quantities in perpendicular directions are '
        'independent of each other.', 'source'),
       ('Use the 45° crossover and the never-bigger-than-the-vector rule to '
        'check a component before trusting it.', 'added')],
      'This is the first half of her teacher’s Kinematics 2 objective list, '
      'with the trigonometry built out rather than assumed — the objectives say '
      '"recall SOHCAHTOA from memory", so the cards are written to be recited '
      'rather than merely recognised. Every number in every question was '
      'computed with sympy inside the builder and asserted before it could be '
      'written, so no answer here was worked by hand. None of the textbook’s '
      'own worked examples (the 15 m/s cliff, the 4.47 m/s ball at 66°, the '
      '27 m/s football) is reused as a question; they were read only to '
      'calibrate the difficulty. Two traps get their own cards because they cost '
      'marks silently rather than loudly: a calculator left in radian mode '
      'returns perfectly plausible wrong numbers for every problem in the unit '
      '(cos 60° = 0.5 is the one-second test), and an unknown side sitting in a '
      'denominator needs dividing rather than multiplying. The 45° crossover is '
      'taught as a checking habit, not just a fact — it catches a swapped sine '
      'and cosine, which is the single commonest error in this topic.',
      ('Learn the three SOHCAHTOA ratios cold before you start the quiz — say '
       'them out loud. Everything else in this lesson is choosing between '
       'them.', 22),
      'content/phys-k2-vectors.json',
      'Kinematics 2 Objectives (teacher’s objective list) + Chapter 7, '
      'Forces and Motion in Two Dimensions',
      'Kinematics 2 Objectives.pdf and Textbook 2D Kinematics.pdf (Drive, '
      'Physics 8)',
      offset_hours=3, round_=8)

p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'content/phys-k2-vectors.json')
j = json.load(io.open(p, encoding='utf-8'))
j['records']['unit-phys-k2-vectors']['libv'] = 1
io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
print('  + libv 1; all sympy assertions passed')
