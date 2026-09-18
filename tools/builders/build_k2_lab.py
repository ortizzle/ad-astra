# -*- coding: utf-8 -*-
# Kinematics 2 · 2-3 Horizontal Projectile Motion Lab
#
# From "Horizontal Projectile Motion Lab.pdf" (Drive, Physics 8) — the Nerf-gun
# muzzle-velocity measurement plus the PhET cannonball height-vs-range
# investigation.
#
# Same call the Ramp Lab unit (Kinematics 1) made, and for the same reason:
# the lab asks her to COLLECT data that does not exist yet, so inventing a
# table of results would be inventing her experiment. This unit teaches the
# REASONING the lab runs on instead — why a height-vs-range graph is curved,
# what to plot to straighten it, what the slope of the straightened line
# physically is, how to get the launch speed back out of it, and what the Moon
# and a doubled launch speed each do to it.
#
# Its own numbered part of the Kinematics 2 shelf, sorting after 2-2 on title
# alone. No prep flag: a lab is not test prep, and prep:true says what a unit
# IS (v139), not what happens to be near it on the calendar.
#
# g = 9.80 m/s² throughout, matching 2-1, 2-2 and the textbook. EVERY number is
# computed with sympy here and asserted before it can be written.
import sys, os, json, io
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

G = sp.Rational(98, 10)
GMOON = sp.Rational(162, 100)

def rnd(x, n=2):
    return float(sp.N(sp.Rational(round(float(x) * 10**n), 10**n)))
def tfall(y, g=G):
    return sp.sqrt(2*sp.Rational(y).limit_denominator()/g)
def rng(v, y, g=G):
    return v*tfall(y, g)
def slope(v, g=G):
    return v*sp.sqrt(2/g)

# --- verified arithmetic ----------------------------------------------------
# Nerf gun: fired level from 1.25 m, dart lands 6.40 m away
t_nerf = tfall(sp.Rational(125, 100));         assert rnd(t_nerf, 3) == 0.505
v_nerf = sp.Rational(640, 100)/t_nerf;         assert rnd(v_nerf, 1) == 12.7
# the linearized slope for that same launch speed
m_earth = slope(v_nerf);                       assert rnd(m_earth, 2) == 5.72
# reading a launch speed back off a measured slope of 5.72
v_back = sp.Rational(572, 100)*sp.sqrt(G/2);   assert rnd(v_back, 1) == 12.7
assert rnd(sp.sqrt(G/2), 4) == 2.2136
assert rnd(sp.sqrt(2/G), 4) == 0.4518
# the Moon steepens the line by √(g_earth / g_moon)
m_moon = slope(v_nerf, GMOON)
assert rnd(m_moon/m_earth, 3) == rnd(sp.sqrt(G/GMOON), 3) == 2.46
# percent error against an accepted 13.5 m/s
# the question states the measured value as 12.7 m/s, so the error is computed
# from that stated figure, not from the unrounded 12.6714 behind it
pct = abs(sp.Rational(127, 10) - sp.Rational(135, 10))/sp.Rational(135, 10)*100
assert rnd(pct, 1) == 5.9
assert rnd(sp.Rational(8, 10)/sp.Rational(127, 10)*100, 1) == 6.3  # the wrong denominator
# quadrupling the drop height doubles the range
assert rnd(rng(4, 2)/rng(4, sp.Rational(1, 2)), 4) == 2.0
# ball thrown level at 12 m/s from 1.90 m, wall 4.50 m away
t_wall = sp.Rational(450, 100)/12;             assert rnd(t_wall, 4) == 0.375
drop_wall = G*t_wall**2/2;                     assert rnd(drop_wall, 3) == 0.689
h_wall = sp.Rational(190, 100) - drop_wall;    assert rnd(h_wall, 2) == 1.21
# a 4.0 m/s launch, for the two graphs
assert rnd(rng(4, 2), 2) == 2.56
assert rnd(slope(4), 3) == 1.807
# the ranking question: four different launch speeds and heights
setups = {'A': (6, sp.Rational(45, 100)), 'B': (3, 2),
          'C': (4, sp.Rational(125, 100)), 'D': (8, sp.Rational(20, 100))}
rs = {k: rnd(rng(v, y), 2) for k, (v, y) in setups.items()}
assert rs == {'A': 1.82, 'B': 1.92, 'C': 2.02, 'D': 1.62}, rs
assert sorted(rs, key=lambda k: -rs[k]) == ['C', 'B', 'A', 'D']

C, Q = [], []

# ---- cards -----------------------------------------------------------------
card(C, 'What the lab measures',
     '**A projectile launched horizontally is timed by its FALL, and carried by '
     'its launch speed — so the height it starts from and the distance it lands '
     'away are enough to work out how fast it left.**\n'
     '• Nothing about the launcher itself has to be known.\n'
     '• Two measurements with a tape measure replace a speed sensor.')
card(C, 'Two equations, one unknown in common',
     '**The vertical drop gives the time; the horizontal distance uses it.**\n'
     '• Launched level, the starting vertical velocity is zero, so the drop is '
     'purely free fall.\n'
     '• There is no horizontal acceleration, so the sideways trip is at a '
     'steady speed.',
     eq='Δy = ½gt²        Δx = v t')
card(C, 'Merging them into one',
     '**Solve the vertical equation for t, substitute it into the horizontal '
     'one, and the time disappears — leaving one equation in the two things you '
     'actually measured.**\n'
     '• t = √(2Δy ÷ g) from the drop.\n'
     '• Put that in place of t in Δx = v t.\n'
     '• Nothing was assumed doing this; it is the same two equations rearranged.',
     eq='Δx = v √(2Δy / g)')
card(C, 'Why the raw graph curves',
     '**Range does not grow in step with height — it grows with the SQUARE ROOT '
     'of height, so a plot of range against height bends over.**\n'
     '• Doubling the height does not double the range.\n'
     '• A curve cannot be given a meaningful slope, which is why the lab asks '
     'for a second, straightened graph.')
card(C, 'Linearizing it',
     '**Plot range against the SQUARE ROOT of the drop height and the curve '
     'becomes a straight line through the origin.**\n'
     '• The equation is already in the shape y = mx once √Δy is treated as the '
     'x variable.\n'
     '• Straightening a curve by plotting against a function of the variable is '
     'the standard move — the Ramp Lab does the same thing with t².',
     eq='Δx = [ v √(2/g) ] · √Δy')
card(C, 'What the slope physically is',
     '**The slope of the straightened line is the launch speed multiplied by '
     '√(2 ÷ g) — so it is not the speed itself, and it is not dimensionless.**\n'
     '• With g = 9.80 m/s², √(2/g) works out at 0.4518 s/√m.\n'
     '• A faster launch tilts the line up; nothing else on the graph changes.',
     eq='slope = v √(2/g)')
card(C, 'Getting the speed back out',
     '**Multiply the measured slope by √(g ÷ 2) to recover the launch '
     'speed.**\n'
     '• √(9.80 ÷ 2) = 2.2136, so a slope of 5.72 means a launch speed of about '
     '12.7 m/s.\n'
     '• Dividing by √(2/g) is the same move written the other way up.',
     eq='v = slope × √(g/2)')
card(C, 'The intercept should be zero',
     '**A launcher fired level from a height of zero would land at a distance '
     'of zero, so the straightened line is expected to pass through the '
     'origin.**\n'
     '• A noticeably non-zero intercept points at a systematic error — the '
     'height measured from the wrong reference point, or a launcher that is not '
     'quite level.\n'
     '• Report it rather than forcing the line through the origin to hide it.')
card(C, 'A line of best fit, not dot to dot',
     '**Draw one straight line that balances the scatter, and take the slope '
     'from two points ON THE LINE — never from two data points.**\n'
     '• Joining the dots turns random scatter into fake structure.\n'
     '• Use two widely separated points on the line so a small reading error in '
     'either matters less.')
card(C, 'Axes, labels, units',
     '**Every axis needs the quantity, its unit, and a scale that uses most of '
     'the page.**\n'
     '• The linearized x-axis is √Δy in √m, not Δy in m — labelling it wrong '
     'makes the slope meaningless.\n'
     '• A scale that crams the data into one corner throws away precision you '
     'already paid for.')
card(C, 'On the Moon',
     '**Lower gravity means a longer fall, so the same launcher shoots farther '
     'and the line gets steeper — the slope grows by √(g_earth ÷ g_moon), about '
     '2.46 times.**\n'
     '• Nothing about the launcher changed. Only the clock did.\n'
     '• Gravity sits under a square root, so a sixth of the gravity is not six '
     'times the range.')
card(C, 'Doubling the launch speed',
     '**The slope doubles, exactly.**\n'
     '• v multiplies the whole slope expression, so the relationship between '
     'them is straight proportion.\n'
     '• Gravity and the drop height are untouched, so the shape of the graph is '
     'the same line, tilted up.')
card(C, 'Percent error',
     '**Compare what you measured with the accepted value, as a fraction of the '
     'accepted value.**\n'
     '• The accepted value goes on the bottom; using your own measurement there '
     'is the usual slip.\n'
     '• It is always a positive number — take the size of the difference.',
     eq='% error = |measured − accepted| ÷ accepted × 100')
card(C, 'Why a simulation needs no repeats',
     '**Repeat trials exist to average away random measurement error, and a '
     'simulation has none — the same settings give the same answer every '
     'time.**\n'
     '• The real Nerf launch does need repeats: the trigger, the dart and the '
     'tape measure all vary.\n'
     '• A simulation can still be systematically wrong, but running it three '
     'times will never reveal it.')
card(C, 'What the model leaves out',
     '**Air resistance is ignored, which is a decent approximation for a dense '
     'compact object over a short flight and a poor one for a foam dart.**\n'
     '• A real dart falls slightly short, so a speed worked out this way tends '
     'to read a little low.\n'
     '• Naming the assumption is part of the write-up, not an excuse added '
     'afterwards.')

# graphs: the raw curve, and the same launch straightened
C[3]['graph'] = {
    'w': [0, 2, 0, 3], 'gx': 0.5, 'gy': 0.5,
    'xl': 'drop height Δy (m)', 'yl': 'range Δx (m)',
    'series': [{'type': 'pts', 'pts': [[rnd(sp.Rational(i, 20), 3),
                                        rnd(rng(4, sp.Rational(i, 20)), 3)]
                                       for i in range(0, 41)]}]}
C[4]['graph'] = {
    'w': [0, 1.5, 0, 3], 'gx': 0.5, 'gy': 0.5,
    'xl': '√Δy (√m)', 'yl': 'range Δx (m)',
    'series': [{'type': 'line', 'm': rnd(slope(4), 3), 'b': 0}]}

# ---- questions -------------------------------------------------------------
q(Q, 1, 'A ball rolls off the end of a level bench. What is its vertical '
        'velocity at the instant it leaves?',
  ['Zero', 'Equal to its rolling speed', 'Equal to g', 'Half its rolling speed'], 0,
  'It was travelling sideways along the bench the whole way to the edge.',
  ['Along the bench the ball moves horizontally and only horizontally.',
   'Leaving the edge does not give it any sudden downward push.',
   'So at that instant it has no vertical velocity at all.',
   'Its vertical velocity starts at zero and grows from there.'],
  '**Zero.** That is exactly what makes the vertical half of the problem '
  'ordinary free fall from rest, so the drop is ½gt² with no extra term.',
  'This is the one fact that lets the two equations be merged in the first '
  'place. A launch at an angle would carry a starting vertical velocity and '
  'the whole method would need another term.')

q(Q, 1, 'Which quantity does the vertical drop of a horizontally launched '
        'object give you?',
  ['The time it spends in the air', 'The horizontal distance it covers',
   'Its launch speed', 'Its landing angle'], 0,
  'Ask which of these could be found without knowing how fast it left.',
  ['The drop is pure free fall from rest, so Δy = ½gt².',
   'That equation contains only the drop height, g, and the time.',
   'Rearranged, it gives the time in the air.',
   'The launch speed never appears in it, so time is what falls out.'],
  '**The time it spends in the air.** The vertical half of the problem knows '
  'nothing about the launch speed, which is why the fall works as a clock.',
  'This is why a dropped ball and a ball rolled off the same table at any '
  'speed land at the same moment — they share the identical fall.')

q(Q, 1, 'In a graph of range against drop height for a horizontally launched '
        'projectile, what shape does the data take?',
  ['A curve that rises steeply then flattens', 'A straight line through the origin',
   'A straight line with a positive intercept', 'A curve that rises ever more steeply'], 0,
  'Range depends on the square root of the height, not on the height itself.',
  ['Range is the launch speed times the fall time.',
   'The fall time goes as the square root of the height.',
   'So range goes as √Δy, and a square-root curve climbs fast at first.',
   'It then flattens off, rather than staying straight or steepening.'],
  '**A curve that rises steeply then flattens.** Each extra centimetre of '
  'height buys less range than the one before it, which is exactly what a '
  'square root does.',
  'A curve has a different slope at every point, so no single number can be '
  'read off it. That is why the lab asks for a second graph rather than more '
  'data.')

q(Q, 1, 'To straighten the height-versus-range graph, what belongs on the '
        'horizontal axis?',
  ['The square root of the drop height', 'The drop height itself',
   'The square of the drop height', 'The fall time squared'], 0,
  'Look at the merged equation and ask what would make it read y = mx.',
  ['The merged equation is Δx = v √(2Δy / g).',
   'Pull the constants together: Δx = [v √(2/g)] × √Δy.',
   'That is y = mx with √Δy playing the part of x.',
   'So plotting range against √Δy gives a straight line through the origin.'],
  '**The square root of the drop height.** Once √Δy is treated as the '
  'variable, the equation is already in straight-line form and nothing else '
  'needs rearranging.',
  'Squaring the height would bend the graph further the wrong way. The Ramp '
  'Lab straightens its own curve the mirror-image way, by plotting against t² '
  'rather than t.')

q(Q, 1, 'What would a clearly non-zero vertical intercept on the straightened '
        'graph suggest?',
  ['A systematic error, such as measuring the height from the wrong point',
   'That the launcher was fired harder on some trials than others',
   'That gravity was stronger than 9.80 m/s² during the experiment',
   'That the data simply needs more trials averaged into it'], 0,
  'Ask what range the equation predicts for a drop height of zero.',
  ['At a drop height of zero the merged equation gives a range of zero.',
   'So the line is expected to pass through the origin.',
   'An offset means every reading is shifted the same way, not scattered.',
   'A consistent shift like that is a systematic error, not random noise.'],
  '**A systematic error, such as measuring the height from the wrong point.** '
  'Random scatter moves points both ways around the line; a systematic error '
  'moves them all the same way and lifts the whole line.',
  'Report the intercept you actually got. Forcing the line through the origin '
  'to make it look right hides the one thing the intercept was there to tell '
  'you.')

q(Q, 1, 'Why does the simulation half of this lab not need the trial repeated '
        'two more times?',
  ['A simulation has no random measurement error to average away',
   'A simulation is guaranteed to be more accurate than a real launcher',
   'Repeats are only needed when the graph turns out to be curved',
   'A simulation already averages several runs before showing a result'], 0,
  'Ask what repeating a trial is actually FOR.',
  ['Repeats exist to average out random error — a slightly misread tape, a '
   'slightly different trigger pull.',
   'The same settings in a simulation give an identical answer every time.',
   'Averaging identical numbers changes nothing.',
   'So the repeats have nothing left to do.'],
  '**A simulation has no random measurement error to average away.** The real '
  'Nerf launch does, which is why that half of the lab still needs repeats.',
  'It does not follow that a simulation is right. A simulation can be '
  'systematically wrong, and running it three times will never show that — '
  'only comparing it with something real will.')

q(Q, 2, 'A launcher is fired level from a height of 1.25 m and its dart lands '
        '6.40 m away. What was the launch speed?',
  ['12.7 m/s', '5.12 m/s', '25.3 m/s', '8.94 m/s'], 0,
  'Find how long the dart was in the air before you touch the 6.40 m.',
  ['The fall is free fall from rest: 1.25 = ½ × 9.80 × t².',
   't² = 2 × 1.25 ÷ 9.80 = 0.2551, so t = 0.505 s.',
   'Horizontally there is no acceleration, so v = Δx ÷ t.',
   'v = 6.40 ÷ 0.505 = 12.7 m/s.'],
  '**12.7 m/s.** The drop supplies the clock and the horizontal distance '
  'supplies the trip, so two tape-measure readings are enough to get a speed.',
  'Dividing 6.40 by 1.25 gives 5.12, which is the commonest wrong turn here — '
  'it divides a distance by a distance and calls the result a speed. Check '
  'the units of what you divided.')

q(Q, 2, 'The straightened graph of a level launch has a slope of 5.72. Taking '
        'g as 9.80 m/s², what was the launch speed?',
  ['12.7 m/s', '2.58 m/s', '5.72 m/s', '56.1 m/s'], 0,
  'The slope is the launch speed times a constant, so undo the constant.',
  ['The slope of this graph is v √(2/g).',
   '√(2 ÷ 9.80) = 0.4518, so slope = v × 0.4518.',
   'Divide to recover v: v = 5.72 ÷ 0.4518.',
   'That is 12.7 m/s.'],
  '**12.7 m/s.** Multiplying the slope by √(g/2) = 2.2136 is the same step '
  'written the other way up, and gives the same 12.7 m/s.',
  'Reading the slope straight off as the speed is the trap this graph is '
  'built to catch. The slope carries a √(2/g) inside it, so it is not a speed '
  'and its units are not m/s.')

q(Q, 2, 'A ball is launched horizontally at 4.0 m/s from a bench 0.50 m high. '
        'How does its range change if the same launch is repeated from 2.0 m?',
  ['It doubles', 'It quadruples', 'It grows by half',
   'It stays the same, since the launch speed did not change'], 0,
  'Range follows the square root of the height, not the height.',
  ['Range = v √(2Δy / g), so range is proportional to √Δy.',
   'The height went from 0.50 m to 2.0 m, a factor of four.',
   'The square root of four is two.',
   'So the range doubles.'],
  '**It doubles.** Quadrupling the height doubles the range — the square root '
  'is what turns a factor of four into a factor of two.',
  'This is the counterfactual worth remembering from the whole lab: because '
  'height sits under a square root, big changes in height produce modest '
  'changes in range.')

q(Q, 2, 'If this lab were repeated on the Moon, where gravity is much weaker, '
        'what would happen to the slope of the straightened graph?',
  ['It would get steeper', 'It would get shallower',
   'It would be unchanged, since the launcher is the same',
   'The graph would stop being a straight line'], 0,
  'Weaker gravity means a longer fall from the same height.',
  ['The slope is v √(2/g), and g is on the bottom inside the root.',
   'A smaller g therefore makes the whole slope bigger.',
   'Physically: the fall takes longer, so the same launch speed carries it '
   'farther sideways.',
   'So the line gets steeper.'],
  '**It would get steeper.** With g = 1.62 m/s² the slope grows by '
  '√(9.80 ÷ 1.62), which is about 2.46 times — noticeably steeper, but '
  'nothing like six times.',
  'Gravity is six times weaker and the slope changes by only about two and a '
  'half. That gap is the square root doing its work, and it is worth stating '
  'in the write-up rather than saying "six times farther".')

q(Q, 2, 'A launch speed is measured as 12.7 m/s where the accepted value is '
        '13.5 m/s. What is the percent error?',
  ['5.9%', '6.3%', '0.8%', '94.1%'], 0,
  'The accepted value belongs on the bottom of the fraction.',
  ['Take the size of the difference: |12.7 − 13.5| = 0.8 m/s.',
   'Divide by the ACCEPTED value: 0.8 ÷ 13.5 = 0.0593.',
   'Multiply by 100 to get a percentage.',
   'That is 5.9%.'],
  '**5.9%.** Percent error always measures the gap as a fraction of the value '
  'you were aiming at, not of the one you got.',
  'Dividing by 12.7 instead gives 6.3%, which is close enough to look right '
  'and is still the wrong calculation. And 0.8 on its own is the difference, '
  'not a percentage of anything.')

q(Q, 2, 'A ball is thrown horizontally at 12 m/s from a height of 1.90 m, '
        'toward a wall 4.50 m away. How far above the ground does it strike '
        'the wall?',
  ['1.21 m', '0.69 m', '1.90 m', '2.59 m'], 0,
  'Work out how long it takes to cover the 4.50 m, then see how far it fell '
  'in that time.',
  ['Horizontally there is no acceleration: t = 4.50 ÷ 12 = 0.375 s.',
   'Vertically it falls from rest: drop = ½ × 9.80 × 0.375² = 0.689 m.',
   'Subtract the drop from the height it started at.',
   '1.90 − 0.689 = 1.21 m above the ground.'],
  '**1.21 m.** The horizontal trip sets the clock and the vertical fall is '
  'read off that clock — the same two-step the whole lab runs on.',
  'Stopping at 0.689 m answers a different question: that is how far it FELL, '
  'not how high it ended up. Read the last line of the question again before '
  'writing the number down.')

q(Q, 3, 'Two students launch identical balls level from the same bench. One '
        'launches at 3.0 m/s, the other at 6.0 m/s. What do their two '
        'straightened graphs look like?',
  ['Both straight through the origin, the faster launch twice as steep',
   'Both straight through the origin, the faster launch four times as steep',
   'Both straight but the faster launch lifted to a higher intercept',
   'The faster launch straight, the slower one still curved'], 0,
  'The launch speed multiplies the whole slope expression.',
  ['The slope is v √(2/g), and only v differs between them.',
   'Doubling v doubles the slope exactly — there is no square involved.',
   'Neither line gains an intercept: a zero drop still means a zero range for '
   'both.',
   'So both pass through the origin and one is twice as steep.'],
  '**Both straight through the origin, the faster launch twice as steep.** '
  'The straightening works for any launch speed, so both graphs are lines; '
  'only the tilt carries the difference between them.',
  'Height sits under a square root and launch speed does not, which is why '
  'doubling the height and doubling the speed do such different things to '
  'this graph. Knowing which quantity is under the root is most of this '
  'topic.')

q(Q, 3, 'Four horizontal launches are set up. Put them in order from the '
        'LONGEST range to the SHORTEST. Take g as 9.80 m/s².',
  ['4.0 m/s from 1.25 m', '3.0 m/s from 2.00 m', '6.0 m/s from 0.45 m',
   '8.0 m/s from 0.20 m'], 0,
  'The fastest launch is not automatically the longest — the fall time matters '
  'just as much.',
  ['Range = v √(2Δy / g), so work each one out rather than judging on speed.',
   '4.0 m/s from 1.25 m: 4.0 × 0.505 = 2.02 m.',
   '3.0 m/s from 2.00 m: 3.0 × 0.639 = 1.92 m.',
   '6.0 m/s from 0.45 m: 6.0 × 0.303 = 1.82 m.',
   '8.0 m/s from 0.20 m: 8.0 × 0.202 = 1.62 m — the shortest, despite the '
   'fastest launch.'],
  '**4.0 m/s from 1.25 m, then 3.0 m/s from 2.00 m, then 6.0 m/s from 0.45 m, '
  'then 8.0 m/s from 0.20 m.** The slowest launch of the four is not last, and '
  'the fastest is — height buys time, and time is what the speed gets to act '
  'on.',
  'Ranking by launch speed alone puts the list in almost exactly the wrong '
  'order here. Both quantities have to be carried through before anything can '
  'be compared.',
  kind='order')

q(Q, 3, 'A student takes the slope of the straightened graph by drawing a '
        'line of best fit and then using the coordinates of the first and last '
        'DATA points. What is wrong with that?',
  ['The slope should come from two points on the LINE, not from the data',
   'The first and last points are too far apart to give a reliable slope',
   'The slope should be taken from the raw curve rather than the fitted line',
   'Data points cannot be used for a slope unless there are at least ten of them'], 0,
  'Ask what the line of best fit was drawn for in the first place.',
  ['The line of best fit averages out the scatter in the data.',
   'Using two data points throws that averaging away and takes whatever error '
   'those two happen to carry.',
   'Two widely separated points ON THE LINE keep the benefit of the fit.',
   'So the slope must be read off the line, not off the data.'],
  '**The slope should come from two points on the LINE, not from the data.** '
  'Drawing the fit and then ignoring it leaves you with the scatter you drew '
  'it to remove.',
  'Widely separated points are genuinely better, so that instinct was right — '
  'it is just that they need to be points on the fitted line.')

q(Q, 3, 'The lab ignores air resistance. For a foam dart measured this way, '
        'which way would that push the calculated launch speed?',
  ['It reads a little low, because the dart falls short of the ideal range',
   'It reads a little high, because the dart stays in the air longer',
   'It is unaffected, because air resistance acts vertically only',
   'It is unaffected, because both measurements are made with the same tape'], 0,
  'Air resistance shortens the horizontal trip; the calculation reads that '
  'shortfall as something else.',
  ['Air resistance drags on the dart, so it lands closer than the ideal model '
   'predicts.',
   'The calculation takes the measured range and divides by the fall time.',
   'A smaller measured range with the same fall time gives a smaller speed.',
   'So the answer comes out a little below the true launch speed.'],
  '**It reads a little low, because the dart falls short of the ideal '
  'range.** A foam dart is light and blunt, so this is not a negligible '
  'effect for it, even if it would be for a marble.',
  'Naming the direction an assumption pushes your answer is worth more in a '
  'write-up than naming the assumption alone. "Ignoring air resistance" says '
  'little; "so this is an underestimate" says something a reader can use.')

q(Q, 3, 'Why does the merged equation contain no reference to the mass of the '
        'object being launched?',
  ['Because the fall time and the horizontal motion are both mass-independent',
   'Because the masses used in this lab are all small enough to ignore',
   'Because the mass cancels between the two original equations',
   'Because mass only matters once air resistance is included in the model'], 0,
  'Look at where mass could have entered: the free fall, or the steady '
  'sideways trip.',
  ['The vertical half is free fall, and free fall accelerates every mass at g.',
   'The horizontal half is motion at a steady speed, which involves no mass '
   'either.',
   'So mass never enters either equation.',
   'It cannot appear in the merged one, because it was never in the originals.'],
  '**Because the fall time and the horizontal motion are both '
  'mass-independent.** Mass had no route into the equations to begin with, so '
  'nothing had to cancel it out.',
  'Air resistance is the real reason a feather and a marble behave '
  'differently, and it is exactly what this model sets aside — which is why '
  'an air-resistance answer is tempting here and still not the reason mass is '
  'absent from these two equations.')
q(Q, 3, 'In the straightened graph, the horizontal axis is labelled simply '
        '"height (m)" while the plotted values are square roots of the '
        'height. What does that cost?',
  ["The slope's units become wrong, so the speed it gives cannot be checked",
   'Nothing — the points are plotted correctly, so the line is correct',
   'The line stops passing through the origin, so the fit is unusable',
   'The plotted points land in the wrong places along the axis'], 0,
  'The points are where they should be. Ask what a reader of the graph would '
  'now believe.',
  ['The values plotted are right, so the line itself is unaffected.',
   'But the label tells a reader the x variable is Δy when it is really √Δy.',
   'The units of the slope are then wrong, and √(2/g) cannot be applied to it '
   'with any confidence.',
   'So the number survives and the meaning does not.'],
  "**The slope's units become wrong, so the speed it gives cannot be "
  'checked.** A slope is a ratio of two labelled quantities; mislabel one and '
  'the ratio stops meaning anything.',
  'This is why the rubric gives separate marks for labelling the axes with '
  'units. It is not tidiness — an unlabelled or wrongly labelled axis makes '
  'every calculation downstream unverifiable.')

build('ad-astra', C, Q, 'unit-phys-k2-lab',
      'Kinematics 2 · 2-3 Horizontal Projectile Motion Lab', 'physics',
      'The reasoning behind the Horizontal Projectile Motion Lab: merging the '
      'two projectile equations into one, why a height-against-range graph is '
      'curved and how to straighten it, what the slope of the straightened '
      'line physically is and how to get a launch speed back out of it, and '
      'what the Moon, a doubled launch speed and air resistance each do to the '
      'result.',
      'A lab mark is mostly not for collecting the data — it is for knowing '
      'what to plot, what the slope means, and which way your own assumptions '
      'pushed the answer. Those are the parts that transfer to every lab after '
      'this one, and they are the parts this lesson drills.',
      [('Combine the horizontal and vertical projectile equations into a '
        'single equation linking launch speed, drop height and range.', 'source'),
       ('Explain why range grows with the square root of drop height, and '
        'linearize the graph accordingly.', 'source'),
       ('State what the slope of the linearized graph represents, and use it '
        'to find the launch speed.', 'source'),
       ('Predict the effect of lower gravity and of a doubled launch speed on '
        'that slope.', 'source'),
       ('Find a launch speed from a single measured height and range.', 'source'),
       ('Compute a percent error, and say which way an ignored assumption '
        'pushed the result.', 'added')],
      'The lab asks her to collect real data — a Nerf launcher on a bench, then '
      'a PhET cannonball — and that data does not exist yet, so this unit '
      'deliberately does not invent a results table. It teaches the reasoning '
      'the lab runs on instead, which is the same call the Kinematics 1 Ramp '
      'Lab unit made. The heart of it is the merge the handout asks for in its '
      'own Question 1: solving the vertical equation for time and substituting '
      'it into the horizontal one gives Δx = v √(2Δy / g), which is already a '
      'straight line once range is plotted against the SQUARE ROOT of the drop '
      'height — and the slope of that line is v √(2/g), not the launch speed '
      'itself. Reading the slope straight off as a speed is the single mistake '
      'most likely to cost marks here, so it gets its own card and its own '
      'question. The Moon question is worth a word too: gravity there is about '
      'six times weaker, but the slope changes by only about 2.46 times, '
      'because g sits under a square root — "six times farther" is a very '
      'natural and quite wrong thing to write. Every number was computed with '
      'sympy inside the builder and asserted before it could be written, and '
      'none of the handout\'s own numbers is reused as a question.',
      ('Do the merge on paper before anything else — solve Δy = ½gt² for t and '
       'put it into Δx = v t. Once you have that one equation, every question '
       'in this lesson is a rearrangement of it.', 22),
      'content/phys-k2-lab.json',
      'Horizontal Projectile Motion Lab (Nerf launcher + PhET simulation)',
      'Horizontal Projectile Motion Lab.pdf (Drive, Physics 8)',
      offset_hours=3, round_=9)

p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'content/phys-k2-lab.json')
j = json.load(io.open(p, encoding='utf-8'))
j['records']['unit-phys-k2-lab']['libv'] = 1
io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
print('  + libv 1; all sympy assertions passed')
