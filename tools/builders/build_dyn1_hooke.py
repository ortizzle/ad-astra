# -*- coding: utf-8 -*-
# Dynamics 1 · 1-5 Hooke's Law and the Spring Lab — from the class's
# Hookes_Law_Lab_2026.pdf (Drive, Physics 8 › Dynamics 1, uploaded 2026-10-27)
# and entry 11 of her equation sheet, F = −kx.
#
# THE LAB HAS NO DATA YET. It asks her to hang masses on a vertical spring,
# record the STRETCH, turn each hanging mass (hanger included) into a weight in
# newtons, graph the two, and read a slope, a y-intercept and a percent error.
# Nothing here invents her readings — the v189 / Ramp Lab call. What this unit
# teaches is the reasoning every one of those steps depends on, plus the lab's
# own questions (the Moon, a mass for a given stretch, a force for a given
# stretch) answered with fresh numbers. The PhET part is done on her laptop.
#
# Two things the sheet leaves open, both taught carefully and both in the
# parentNote rather than decided quietly:
#   * Which quantity goes on which axis. The lab says "the relationship between
#     force and stretch"; the usual Hooke's-law graph puts force on the vertical
#     axis so the slope IS k. Every graded stem that needs the slope says which
#     axis is which, so no question depends on the class's choice.
#   * Percent error. Her sheet writes %Error = |b| / y_max · 100 and does not
#     define b or y_max (the home-written guide flags exactly this). In a lab
#     whose rubric asks for "slope, y-intercept, % error", b is almost certainly
#     the y-intercept of the best-fit line and y_max its largest force. Taught
#     that way, flagged `added`, and every stem says what b and y_max are.
#
# EVERY number is computed with sympy and asserted before it reaches a
# question, including that no distractor is also correct. None of the
# sources' numbers is reused in a graded stem: not the lab's 10 in or 30 cm,
# not the guide's 200 N/m, 0.15 m or 0.10 m, and not 1-2's 250 N/m / 0.12 m
# spring question.
import sys, os, json, io, re
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

g = sp.Rational(49, 5)                        # |g| = 9.8 m/s², her sheet's size
g_moon = sp.Rational(8, 5)                    # 1.6 m/s², as 1-2 uses
def rnd(x, n=1):
    return float(sp.N(sp.Rational(round(float(x) * 10**n), 10**n)))
def eq(x, n, want): return round(rnd(x, n), n) == want
def distinct(*xs):
    a = xs[0]
    for x in xs[1:]:
        assert abs(float(x) - float(a)) > 1e-6, (a, x)
R = sp.Rational

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = 'content/phys-dyn1-hooke.json'
UID = 'unit-phys-dyn1-hooke'
SRC = 'Hookes_Law_Lab_2026.pdf (Drive, Physics 8 › Dynamics 1)'

# =============================================================================
# numbers
# =============================================================================
# weight of a 350 g mass
w350 = R(350, 1000) * g;                      assert eq(w350, 2, 3.43)
distinct(w350, 350, R(35, 100), 350 * g)       # grams as N, kg as N, grams × g
# stretch, not length: relaxed 12.0 cm, loaded 19.0 cm, 0.150 kg in all
F_len = R(150, 1000) * g;                     assert eq(F_len, 2, 1.47)
k_len = F_len / R(7, 100);                    assert k_len == 21
k_len_L = F_len / R(19, 100);                 assert eq(k_len_L, 1, 7.7)      # used the length
k_len_cm = F_len / 7;                         assert eq(k_len_cm, 2, 0.21)    # cm as m
k_len_g = 150 / R(7, 100);                    assert eq(k_len_g, -1, 2140)    # grams as N
distinct(k_len, k_len_L, k_len_cm, k_len_g)
# the hanger: 50 g hanger + 150 g slotted masses, stretch 8.0 cm
k_hang = R(200, 1000) * g / R(8, 100);        assert eq(k_hang, 1, 24.5)
k_nohang = R(150, 1000) * g / R(8, 100);      assert eq(k_nohang, 1, 18.4)    # forgot the hanger
k_hang_cm = R(200, 1000) * g / 8;             assert eq(k_hang_cm, 3, 0.245)
k_hang_g = 200 / R(8, 100);                   assert k_hang_g == 2500
distinct(k_hang, k_nohang, k_hang_cm, k_hang_g)
# k from a graph: line through (0.25 m, 4.0 N)
k_gr = R(4) / R(1, 4);                        assert k_gr == 16
distinct(k_gr, 4, R(1, 4) / 4, R(4) / 25)      # read a force, inverted, stretch in cm
assert eq(R(1, 4) / 4, 3, 0.063) or eq(R(1, 4) / 4, 4, 0.0625)
# force at a stretch: k = 36 N/m, 18 cm
F18 = 36 * R(18, 100);                        assert eq(F18, 2, 6.48)
distinct(F18, 36 * 18, 36 / R(18, 100), R(18, 100) / 36)
assert 36 * 18 == 648 and 36 / R(18, 100) == 200 and eq(R(18, 100) / 36, 4, 0.005)
# mass for a stretch, with inches: k = 42 N/m, 6.0 in
x_in = 6 * R(254, 10000);                     assert x_in == R(1524, 10000)
F_in = 42 * x_in;                             assert eq(F_in, 4, 6.4008)
m_in = F_in / g;                              assert eq(m_in, 2, 0.65)
m_in_inch = 42 * 6 / g;                       assert eq(m_in_inch, 1, 25.7)   # inches as metres
m_in_cm = 42 * R(1524, 100) / g;              assert eq(m_in_cm, 1, 65.3)     # cm as metres
distinct(m_in, m_in_inch, m_in_cm, F_in)                                       # newtons as kg
assert eq(F_in, 1, 6.4)
# proportional: 2.0 N → 3.0 cm, so 5.0 N → 7.5 cm
x5 = R(3) * R(5) / R(2);                      assert x5 == R(15, 2)
distinct(x5, R(3) * R(2) / R(5), 3 * 5, 3 + (5 - 2))
assert R(6, 5) == R(3) * R(2) / R(5)
# Moon numeric: 0.30 kg on a k = 8.0 N/m spring
x_moon = R(30, 100) * g_moon / 8;             assert x_moon == R(6, 100)     # 6.0 cm
x_earth = R(30, 100) * g / 8;                 assert eq(x_earth * 100, 1, 36.8)
x_massF = R(30, 100) / 8;                     assert eq(x_massF * 100, 1, 3.8)
distinct(x_moon * 100, x_earth * 100, x_massF * 100, x_moon)                   # metres labelled cm
# Moon: the slope is k, which never involves g
kk, xx, mm, gg = sp.symbols('k x m g', positive=True)
slope = sp.diff(kk * xx, xx);                 assert slope == kk and gg not in slope.free_symbols
# intercept: a 50 g hanger left out of every weight shifts every force down
b_hang = -R(50, 1000) * g;                    assert eq(b_hang, 2, -0.49)
# percent error on her sheet: |b| / y_max × 100, b = −0.18 N, y_max = 6.0 N
pe = abs(R(-18, 100)) / 6 * 100;              assert pe == 3
distinct(pe, pe / 100, R(6) / R(18, 100) * 100, -pe)
assert eq(R(6) / R(18, 100) * 100, 0, 3333)
# order: rank springs by k, stiffest first
springs = {'B': R(4) / R(5, 100), 'A': R(42, 10) / R(7, 100),
           'C': R(75, 10) / R(25, 100), 'D': R(2) / R(20, 100)}
assert [springs[s] for s in 'BACD'] == [80, 60, 30, 10]
assert max(R(4), R(42, 10), R(75, 10), R(2)) == R(75, 10)   # C pulls hardest yet ranks third

C, Q = [], []
# =============================================================================
# cards
# =============================================================================
card(C, 'Hooke’s law',
     '**The force a spring exerts is proportional to how far it is stretched '
     'or compressed.**\n'
     '• Twice the stretch, twice the force — as long as the spring is not '
     'overstretched.\n'
     '• It is entry 11 on your sheet.',
     eq='F = −kx', hint='Pull twice as far, it pulls back twice as hard.')
card(C, 'What the minus sign means',
     '**The minus sign says the spring’s force points the opposite way to its '
     'stretch or squash: always back toward its relaxed length.**\n'
     '• Pull it down and it pulls up. Squash it and it pushes out.\n'
     '• That is why it is called a restoring force. For the SIZE of the force, '
     'use kx and say the direction in words.',
     frm='added', hint='Stretch one way, force the other.')
card(C, 'Stretch, not length',
     '**x is the stretch — how much LONGER the spring got — not how long the '
     'spring is.**\n'
     '• Stretch = loaded length − relaxed length.\n'
     '• Measure the relaxed length first, with nothing hanging, then '
     'subtract it from every loaded reading.\n'
     '• Your lab sheet puts this in capitals for a reason: using the length '
     'is the commonest way to ruin the whole graph.',
     eq='stretch = loaded length − relaxed length',
     hint='The meter stick reads a length. You record a difference.')
card(C, 'Weight in newtons, hanger included',
     '**The force on the spring is the weight of EVERYTHING hanging from it, '
     'F_g = mg, in newtons.**\n'
     '• That includes the mass hanger itself, not just the slotted masses on '
     'it.\n'
     '• Use 9.8 m/s² for the size of g; the force points down.',
     eq='F_g = mg', hint='The hanger is hanging too.')
card(C, 'Grams to kilograms first',
     '**Divide grams by 1000 before multiplying by g — a 250 g mass is 0.250 kg '
     'and weighs 2.45 N.**\n'
     '• Multiplying grams straight by 9.8 makes every force a thousand times '
     'too big.\n'
     '• A mass in grams is never a force in newtons, however tidy the number '
     'looks.', frm='added')
card(C, 'The spring constant, k',
     '**k says how stiff a spring is: the force needed for each metre of '
     'stretch, in newtons per metre (N/m).**\n'
     '• Bigger k, stiffer spring: more force for the same stretch.\n'
     '• k belongs to the spring. It does not change with the masses you hang '
     'or the planet you are on.',
     eq='k = F / x', hint='Newtons per metre: force per stretch.')
card(C, 'What you choose and what you measure',
     '**In this lab you choose the force (by choosing the masses), so force is '
     'the independent variable and stretch is the dependent one.**\n'
     '• The spring decides the stretch; you read it off the meter stick.\n'
     '• The spring constant is not a variable here at all — it is what the '
     'graph lets you find.', frm='added')
card(C, 'The force–stretch graph: its slope is k',
     '**With force on the vertical axis and stretch (in metres) on the '
     'horizontal, the slope of the best-fit line is the spring constant.**\n'
     '• Slope = rise ÷ run = force ÷ stretch = k, in N/m.\n'
     '• If your class puts stretch on the vertical axis instead, the slope is '
     '1/k, in m/N — check which way your teacher wants it.\n'
     '• The line on this card has a slope of 20 N/m.')
C[-1]['graph'] = {'w': [0, 0.3, 0, 6], 'gx': 0.05, 'gy': 1,
                  'series': [{'type': 'line', 'm': 20, 'b': 0}],
                  'xl': 'Stretch (m)', 'yl': 'Force (N)'}
card(C, 'Why the line should go through the origin',
     '**No weight hung, no stretch: an unloaded spring sits at its relaxed '
     'length, so the line should pass through (0, 0).**\n'
     '• That is also why Hooke’s law has no "+ b" in it.', frm='added')
card(C, 'An intercept that is not zero',
     '**A best-fit line that clearly misses the origin points to a slip made '
     'the same way in every reading.**\n'
     '• Leaving the hanger out of every weight drops every force by the '
     'hanger’s weight, so the line crosses the force axis BELOW zero.\n'
     '• Recording lengths instead of stretches shifts every reading by the '
     'relaxed length.\n'
     '• A small intercept is just scatter. A big one is a clue.', frm='added')
card(C, 'Percent error on your sheet',
     '**Your sheet’s percent error is |b| ÷ y_max × 100 — in this lab, most '
     'likely the size of the y-intercept compared with the largest force you '
     'plotted.**\n'
     '• It measures how far your line misses the origin, as a percentage.\n'
     '• The sheet does not say what b and y_max are, so ask your teacher; '
     'this is the reading that fits a lab that asks for slope, y-intercept and '
     '% error together.',
     eq='%Error = |b| / y_max · 100', frm='added')
card(C, 'Stiffer spring, steeper line',
     '**On a force–stretch graph, the stiffer spring has the steeper line.**\n'
     '• Steeper means more force for each centimetre of stretch.\n'
     '• On this card, spring A (40 N/m) is four times as stiff as spring B '
     '(10 N/m).', frm='added')
C[-1]['graph'] = {'w': [0, 0.3, 0, 12], 'gx': 0.05, 'gy': 2,
                  'series': [{'type': 'line', 'm': 40, 'b': 0},
                             {'type': 'line', 'm': 10, 'b': 0}],
                  'pts': [{'x': 0.25, 'y': 10, 'label': 'A'},
                          {'x': 0.25, 'y': 2.5, 'label': 'B'}],
                  'xl': 'Stretch (m)', 'yl': 'Force (N)'}
card(C, 'Your mathematical expression',
     '**Your mathematical expression is the line’s equation with your own '
     'numbers in it: F = (your k) × x.**\n'
     '• Use it forwards: put in a stretch, get a force.\n'
     '• Use it backwards: put in a force, get a stretch.\n'
     '• Keep the units on the slope, N/m, so the expression says what it '
     'means.')
card(C, 'Working backward to a mass',
     '**To find the mass that gives a certain stretch: F = kx for the force, '
     'then m = F ÷ g for the mass.**\n'
     '• Two steps, and the second one is the one people forget: a force in '
     'newtons is not a mass in kilograms.\n'
     '• This is also how the PhET simulation’s unknown masses are found.',
     eq='m = kx / g')
card(C, 'Inches to metres',
     '**1 inch is 2.54 cm, which is 0.0254 m — convert to metres before using '
     'k in N/m.**\n'
     '• N/m only works with metres. A stretch in inches or centimetres has to '
     'be converted first, or the answer comes out tens or hundreds of times '
     'too big.',
     eq='1 in = 2.54 cm = 0.0254 m', frm='added')
card(C, 'The lab on the Moon',
     '**Same masses on the Moon: smaller weights, so smaller stretches — but '
     'the same slope, because k belongs to the spring.**\n'
     '• Independent values (the weights): smaller, about one-sixth, since g is '
     'about 1.6 m/s² there.\n'
     '• Dependent values (the stretches): smaller by the same factor.\n'
     '• Slope (k): unchanged. Every point slides down the SAME line toward the '
     'origin.',
     hint='The spring does not know which planet it is on.')
card(C, 'The elastic limit',
     '**Hooke’s law only holds up to the spring’s elastic limit; stretched '
     'past it, the line bends and the spring stays longer for good.**\n'
     '• On the graph, the points stop following the straight line.\n'
     '• A damaged spring never returns to its relaxed length, so its readings '
     'no longer count.', frm='added')
C[-1]['graph'] = {'w': [0, 0.4, 0, 7], 'gx': 0.05, 'gy': 1,
                  'series': [{'type': 'pts', 'pts': [[0, 0], [0.1, 2], [0.2, 4],
                              [0.25, 5], [0.3, 5.6], [0.35, 5.9], [0.4, 6.1]]}],
                  'xl': 'Stretch (m)', 'yl': 'Force (N)'}
card(C, 'Why one trial is enough here',
     '**A hanging mass that has stopped moving gives the same stretch every '
     'time, so this lab needs one careful reading per mass, not several '
     'trials.**\n'
     '• Wait for the bouncing to stop before you read the meter stick.\n'
     '• Read the scale at eye level, at the same point on the spring each '
     'time.')

# =============================================================================
# questions
# =============================================================================
q(Q, 1, 'In your sheet’s Hooke’s law, F = −kx, what does the minus sign tell you?',
  ['The spring’s force points opposite to its stretch or squash',
   'The spring constant is negative whenever a spring is stretched',
   'The force gets weaker the further the spring is pulled out',
   'The spring’s force is always smaller than the weight it holds'],
  0, 'Pull a spring down. Which way does it pull?',
  ['Stretch a spring downward and it pulls back up.',
   'Squash it and it pushes back out.',
   'Either way, its force is opposite to its displacement x.',
   'The minus sign records exactly that: the force is a restoring force.'],
  '**The minus sign shows the spring always pulls or pushes back toward its '
  'relaxed length — opposite to x.** k itself is always positive, and the '
  'size of the force, kx, grows with the stretch rather than shrinking.',
  'For the size use kx; for the direction say "back toward relaxed".', frm='added')

q(Q, 1, 'A spring hangs from a clamp. A hand pulls its lower end 6 cm below '
        'its relaxed position and holds it there. Which way does the spring '
        'pull on the hand?',
  ['Up, back toward its relaxed length',
   'Down, the same way it was stretched',
   'Sideways, at right angles to the stretch',
   'Neither way, until the hand lets go'],
  0, 'It is a restoring force.',
  ['The spring has been stretched downward.',
   'A spring’s force is opposite to its stretch.',
   'So it pulls upward on whatever is holding its end.',
   'It pulls up, toward its relaxed length.'],
  '**Stretched down, the spring pulls up — that is the minus sign in F = −kx.** '
  'It pulls the whole time it is stretched, not only once it is released; the '
  'hand can feel it.', 'Stretch down, pull up.', frm='added')

q(Q, 1, 'What are the units of a spring constant?',
  ['N/m', 'N·m', 'm/N', 'kg/m'],
  0, 'k = F ÷ x.',
  ['k is force divided by stretch.',
   'Force is in newtons and stretch is in metres.',
   'So k is newtons divided by metres.',
   'The unit is N/m.'],
  '**k = F ÷ x, so its unit is newtons per metre, N/m.** m/N is the ratio '
  'upside down, which is what the slope would be with stretch on the vertical '
  'axis; N·m multiplies instead of dividing; and kg/m mixes up mass and force.',
  'Force per stretch: N/m.', frm='added')

q(Q, 1, 'In a spring lab where you hang chosen masses and measure how far the '
        'spring stretches, what is the independent variable?',
  ['The weight hung, set by the masses you choose',
   'The stretch you read off the meter stick',
   'The spring constant of the spring itself',
   'The length of the spring before loading'],
  0, 'Which one do YOU decide?',
  ['The independent variable is the one you choose and change.',
   'You decide which masses to hang, so you set the weight.',
   'The spring then decides the stretch, which you measure.',
   'So the weight is independent and the stretch is dependent.'],
  '**You choose the masses, so the weight (the force) is the independent '
  'variable; the stretch is what you measure.** The spring constant is what '
  'the experiment finds, and the relaxed length is a starting point you '
  'subtract, not a variable.', 'Chosen = independent. Measured = dependent.')

q(Q, 1, 'Why should a spring’s force-against-stretch line pass through the '
        'origin?',
  ['With no weight hung, the spring sits at its relaxed length',
   'Every straight line drawn on a graph has to start at zero',
   'The meter stick starts at zero, so the readings must too',
   'The spring constant stays at zero until a mass is hung'],
  0, 'What is the stretch when the force is zero?',
  ['With nothing pulling on it, a spring is at its relaxed length.',
   'Its stretch is then zero.',
   'Zero force and zero stretch is the point (0, 0).',
   'So the line should pass through the origin.'],
  '**Zero force means zero stretch, so (0, 0) is a real data point.** Plenty of '
  'straight lines miss the origin; this one should not, which is why a big '
  'intercept on your graph is worth explaining.',
  'No pull, no stretch.', frm='added')

q(Q, 2, 'A 350 g mass hangs from a spring. What force does it pull down with, '
        'in newtons?',
  ['3.43 N', '350 N', '0.35 N', '3430 N'],
  0, 'Grams to kilograms first, then F_g = mg.',
  ['350 g = 0.350 kg.',
   'F_g = mg = 0.350 × 9.8.',
   'F_g = 3.43 N.',
   'The mass pulls down on the spring with 3.43 N.'],
  '**350 g = 0.350 kg, and 0.350 × 9.8 = 3.43 N.** 350 N treats grams as '
  'newtons, 0.35 N treats kilograms as newtons, and 3430 N multiplies the '
  'grams by 9.8 without converting.', 'Divide by 1000, then multiply by 9.8.')

q(Q, 2, 'A spring is 12.0 cm long with nothing on it. With 0.150 kg hanging '
        'from it (hanger included) it is 19.0 cm long. What is its spring '
        'constant?',
  ['21 N/m', '7.7 N/m', '0.21 N/m', '2140 N/m'],
  0, 'x is the stretch, not the length.',
  ['Weight: 0.150 × 9.8 = 1.47 N.',
   'Stretch: 19.0 cm − 12.0 cm = 7.0 cm = 0.070 m.',
   'k = F ÷ x = 1.47 ÷ 0.070.',
   'k = 21 N/m.'],
  '**k = 1.47 N ÷ 0.070 m = 21 N/m.** 7.7 N/m divides by the whole 19.0 cm '
  'length instead of the 7.0 cm stretch — the mistake the lab sheet warns '
  'about in capitals. 0.21 N/m leaves the stretch in centimetres, and '
  '2140 N/m uses the 150 grams as if they were newtons.',
  'Subtract the relaxed length first. Always.')

q(Q, 2, 'A 50 g mass hanger carrying 150 g of slotted masses stretches a spring '
        '8.0 cm. What is the spring constant?',
  ['24.5 N/m', '18.4 N/m', '0.245 N/m', '2500 N/m'],
  0, 'Everything hanging from the spring pulls on it.',
  ['Total mass hanging: 50 g + 150 g = 200 g = 0.200 kg.',
   'Weight: 0.200 × 9.8 = 1.96 N.',
   'Stretch: 8.0 cm = 0.080 m.',
   'k = 1.96 ÷ 0.080 = 24.5 N/m.'],
  '**The hanger counts: 0.200 kg weighs 1.96 N, and 1.96 ÷ 0.080 = 24.5 N/m.** '
  '18.4 N/m leaves the hanger out, 0.245 N/m keeps the stretch in centimetres, '
  'and 2500 N/m uses the 200 grams as newtons.',
  'Hanger + masses, in kilograms, times 9.8.')

q(Q, 2, 'The graph shown plots the force on a spring in newtons (vertical axis) '
        'against its stretch in metres (horizontal axis). What is the spring '
        'constant?',
  ['16 N/m', '4.0 N/m', '0.063 N/m', '0.16 N/m'],
  0, 'The slope is rise over run.',
  ['Pick a point on the line far from the origin: (0.25 m, 4.0 N).',
   'The line starts at (0, 0), so the rise is 4.0 N and the run is 0.25 m.',
   'Slope = 4.0 ÷ 0.25.',
   'k = 16 N/m.'],
  '**The slope is 4.0 N ÷ 0.25 m = 16 N/m.** 4.0 N/m reads one force off the '
  'graph and calls it k; 0.063 N/m divides the stretch by the force; and '
  '0.16 N/m treats the 0.25 m as 25.',
  'Slope of force against stretch = k.')
Q[-1]['graph'] = {'w': [0, 0.3, 0, 5], 'gx': 0.05, 'gy': 1,
                  'series': [{'type': 'line', 'm': 16, 'b': 0}],
                  'pts': [{'x': 0.25, 'y': 4, 'label': '(0.25, 4.0)'}],
                  'xl': 'Stretch (m)', 'yl': 'Force (N)'}

q(Q, 2, 'The graph shown plots force against stretch for two springs, A and B. '
        'Which statement is true?',
  ['A is stiffer: it needs more force per metre of stretch',
   'B is stiffer: it stretches further for the same force',
   'A is stiffer: it stretches further for the same force',
   'They are equally stiff: both lines start from zero'],
  0, 'Steeper line, more force per metre.',
  ['The slope of each line is its spring constant k.',
   'A’s line is steeper: 30 N/m against B’s 12 N/m.',
   'A bigger k means more force for each metre of stretch.',
   'So A is the stiffer spring, and it stretches LESS for the same force.'],
  '**A’s steeper line means a bigger k, so A is stiffer and stretches less for '
  'any given force.** Stretching further for the same force is what makes B '
  'the softer one. Starting at zero says nothing about stiffness: every ideal '
  'spring’s line does.', 'Stiffer = steeper.', frm='added')
Q[-1]['graph'] = {'w': [0, 0.3, 0, 9], 'gx': 0.05, 'gy': 1,
                  'series': [{'type': 'line', 'm': 30, 'b': 0},
                             {'type': 'line', 'm': 12, 'b': 0}],
                  'pts': [{'x': 0.25, 'y': 7.5, 'label': 'A'},
                          {'x': 0.25, 'y': 3, 'label': 'B'}],
                  'xl': 'Stretch (m)', 'yl': 'Force (N)'}

q(Q, 2, 'A spring has a spring constant of 36 N/m. How much force does it exert '
        'when it is stretched 18 cm?',
  ['6.48 N', '648 N', '200 N', '0.005 N'],
  0, 'Centimetres to metres, then F = kx.',
  ['18 cm = 0.18 m.',
   'F = kx = 36 × 0.18.',
   'F = 6.48 N.',
   'It pulls back toward its relaxed length with 6.48 N.'],
  '**F = kx = 36 N/m × 0.18 m = 6.48 N.** 648 N uses 18 as metres, 200 N '
  'divides k by the stretch, and 0.005 N divides the stretch by k.',
  'N/m needs metres.')

q(Q, 3, 'A spring has a spring constant of 42 N/m. What mass would you hang on '
        'it to stretch it 6.0 inches? (1 inch = 2.54 cm)',
  ['0.65 kg', '25.7 kg', '65.3 kg', '6.4 kg'],
  0, 'Inches to metres, F = kx, then m = F ÷ g.',
  ['6.0 in × 2.54 = 15.24 cm = 0.1524 m.',
   'F = kx = 42 × 0.1524 = 6.40 N.',
   'm = F ÷ g = 6.40 ÷ 9.8.',
   'm = 0.65 kg.'],
  '**6.0 in is 0.1524 m, so F = 42 × 0.1524 = 6.40 N and m = 6.40 ÷ 9.8 = '
  '0.65 kg.** 25.7 kg uses the 6.0 inches as if they were metres, 65.3 kg uses '
  'the 15.24 centimetres as metres, and 6.4 kg stops at the force and calls '
  'newtons kilograms.', 'Convert, multiply by k, divide by g.')

q(Q, 2, 'A 2.0 N weight stretches a spring 3.0 cm. Without passing the elastic '
        'limit, how far will a 5.0 N weight stretch it?',
  ['7.5 cm', '1.2 cm', '15 cm', '6.0 cm'],
  0, 'Stretch is proportional to force.',
  ['The force goes from 2.0 N to 5.0 N: 5.0 ÷ 2.0 = 2.5 times as much.',
   'Hooke’s law says the stretch grows by the same factor.',
   '3.0 cm × 2.5.',
   'The stretch is 7.5 cm.'],
  '**Two and a half times the force gives two and a half times the stretch: '
  '7.5 cm.** 1.2 cm flips the ratio, 15 cm multiplies by 5 instead of by 2.5, '
  'and 6.0 cm adds a centimetre per newton, which only happens for a spring '
  'with k = 100 N/m — not this one.', 'Same factor for force and stretch.',
  frm='added')

q(Q, 3, 'A spring lab is repeated on the Moon with the same masses. What happens '
        'to the weights hung (the independent values) and to the stretches '
        '(the dependent values)?',
  ['Both get smaller: lighter weights stretch it less',
   'The weights get smaller, but the stretches stay put',
   'The weights stay put, but the stretches get smaller',
   'Both stay the same, because the masses are the same'],
  0, 'Same mass, smaller g.',
  ['Weight is mg, and g on the Moon is about 1.6 m/s² instead of 9.8.',
   'So each mass weighs about one-sixth as much there.',
   'A smaller force stretches the same spring less, by the same factor.',
   'Both the weights and the stretches get smaller.'],
  '**The masses are the same, but each weighs about a sixth as much, so every '
  'stretch is about a sixth as big too.** "The masses are the same" is true and '
  'is exactly the trap: the spring responds to weight, not mass.',
  'Same masses, smaller weights, smaller stretches.')

q(Q, 3, 'A spring lab is repeated on the Moon with the same masses, and force '
        'is graphed on the vertical axis against stretch on the horizontal. '
        'What happens to the slope of the line?',
  ['It stays the same, because k belongs to the spring',
   'It drops to about a sixth, just as the weights do',
   'It rises, because the spring now stretches less',
   'It drops to zero, because the weights barely count'],
  0, 'What does the slope measure?',
  ['The slope of force against stretch is k.',
   'On the Moon the forces and the stretches both shrink by the same factor.',
   'Force ÷ stretch is therefore unchanged.',
   'The slope stays the same: every point slides down the same line.'],
  '**The slope is k, a property of the spring, so it does not change; the '
  'points just sit closer to the origin on the same line.** Weights shrink, '
  'stretches shrink with them, and their ratio holds steady. g never appears '
  'in k.', 'The spring does not know which planet it is on.')

q(Q, 3, 'On the Moon, where g is about 1.6 m/s², a 0.30 kg mass hangs from a '
        'spring with a spring constant of 8.0 N/m. How far does it stretch the '
        'spring?',
  ['6.0 cm', '36.8 cm', '3.8 cm', '0.060 cm'],
  0, 'Moon weight first, then x = F ÷ k.',
  ['Weight on the Moon: 0.30 × 1.6 = 0.48 N.',
   'x = F ÷ k = 0.48 ÷ 8.0 = 0.060 m.',
   '0.060 m is 6.0 cm.',
   'It stretches 6.0 cm.'],
  '**F = 0.30 × 1.6 = 0.48 N, and x = 0.48 ÷ 8.0 = 0.060 m = 6.0 cm.** '
  '36.8 cm uses Earth’s 9.8, 3.8 cm divides the mass by k as if kilograms were '
  'newtons, and 0.060 cm forgets to turn metres into centimetres.',
  'k stays 8.0 N/m on the Moon. Only the weight changes.')

q(Q, 3, 'A best-fit line of force against stretch crosses the force axis at '
        '−0.49 N instead of passing through zero. Which slip, made in every '
        'reading, would produce exactly that?',
  ['Leaving a 50 g hanger out of every weight',
   'Writing every stretch in cm instead of m',
   'Using 10 m/s² for g instead of 9.8 m/s²',
   'Running each reading three times, not once'],
  0, 'Which slip shifts every force by the same amount?',
  ['A slip that shifts every force down by the same amount moves the whole line down.',
   'A 50 g hanger weighs 0.050 × 9.8 = 0.49 N.',
   'Leaving it out makes every force 0.49 N too small.',
   'The line then crosses the force axis at −0.49 N.'],
  '**Forgetting the hanger lowers every force by its 0.49 N weight, which '
  'drops the whole line by 0.49 N.** Centimetres instead of metres changes '
  'the slope, not the intercept; using 10 for g scales every force a little, '
  'which also changes only the slope; and extra trials just average the same '
  'values.', 'Same shift in every reading = an intercept.', frm='added')

q(Q, 2, 'Your sheet gives percent error as |b| ÷ y_max × 100. A spring graph’s '
        'best-fit line has a y-intercept b of −0.18 N, and the largest force '
        'plotted, y_max, is 6.0 N. What is the percent error?',
  ['3.0%', '0.030%', '3333%', '−3.0%'],
  0, 'Drop the sign, divide, multiply by 100.',
  ['|b| = |−0.18| = 0.18 N.',
   '0.18 ÷ 6.0 = 0.030.',
   '0.030 × 100 = 3.0.',
   'The percent error is 3.0%.'],
  '**|−0.18| ÷ 6.0 × 100 = 3.0%.** 0.030% puts a % sign on the fraction '
  'without ever multiplying by 100, 3333% divides the wrong way round, and −3.0% '
  'keeps the sign the absolute-value bars remove.',
  'The bars make it positive; ×100 makes it a percent.', frm='added')

q(Q, 2, 'A student keeps adding masses to a spring. After a certain point each '
        'new 0.5 N of weight stretches it much further than before, and once '
        'the masses come off it stays longer than it started. What happened?',
  ['It went past its elastic limit and is now permanently stretched',
   'Its spring constant went up, so each weight stretches it further',
   'Hooke’s law still holds there; only the meter stick reading is off',
   'It ran out of stretch, and will snap back fully once it is unloaded'],
  0, 'Does it go back to its relaxed length?',
  ['Hooke’s law only holds up to the elastic limit.',
   'Past it, equal steps of force stop giving equal steps of stretch.',
   'A spring stretched that far does not return to its relaxed length.',
   'It has passed its elastic limit and been permanently deformed.'],
  '**The straight line ended at the elastic limit; past it the spring '
  'deformed for good.** A bigger k would mean LESS stretch per newton, not '
  'more, and a spring that stays longer has plainly not snapped back.',
  'Straight line only up to the elastic limit.', frm='added')

q(Q, 3, 'Rank these springs from STIFFEST to SOFTEST.',
  ['Spring B: 4.0 N stretches it 5.0 cm',
   'Spring A: 4.2 N stretches it 7.0 cm',
   'Spring C: 7.5 N stretches it 25 cm',
   'Spring D: 2.0 N stretches it 20 cm'],
  0, 'Work out k = F ÷ x for each, in N/m.',
  ['B: 4.0 ÷ 0.050 = 80 N/m.',
   'A: 4.2 ÷ 0.070 = 60 N/m.',
   'C: 7.5 ÷ 0.25 = 30 N/m.',
   'D: 2.0 ÷ 0.20 = 10 N/m, so B, A, C, D.'],
  '**Stiffness is force per stretch: B 80 N/m, A 60 N/m, C 30 N/m, D 10 N/m.** '
  'Spring C carries the biggest force, but it needed a long stretch to get '
  'there, so it is only third. The force alone never tells you how stiff a '
  'spring is.', 'Compare k, not the force.', frm='added', kind='order')

assert not any(re.search(r'(?<![\d.])(10 in\b|10 inch|30 cm|200 N/m|0\.15 m\b|0\.10 m\b|250 N/m|0\.12 m\b)',
                         ' '.join([x['q']] + x['opts'])) for x in Q), 'a source number reused'

build('ad-astra', C, Q, UID,
      'Dynamics 1 · 1-5 Hooke’s Law and the Spring Lab', 'physics',
      'Hooke’s law, F = −kx, and the spring lab built on it: recording the '
      'stretch rather than the length, turning each hanging mass (hanger '
      'included) into a weight in newtons, reading the spring constant from '
      'the slope of a force–stretch graph, what the y-intercept and the '
      'percent error say about the data, and using the line to predict a '
      'force or a mass. Plus the lab’s own question: what changes on the Moon.',
      'Springs are the cleanest example of a force that depends on position, '
      'and the lab is the first time you build a law from your own data '
      'instead of reading it off the sheet. The graph skills — slope, '
      'intercept, what a line through the origin means — come back in every '
      'lab after this one.',
      [('Determine the relationship between force and stretch for a vertical '
        'spring.', 'source'),
       ('Find a spring constant from the slope of a force–stretch graph, with '
        'its units.', 'source'),
       ('Use F = kx to predict the force for a stretch and the mass needed for '
        'a stretch, converting units first.', 'source'),
       ('Explain why the spring constant does not change on the Moon even '
        'though the weights and stretches do.', 'source'),
       ('Recognise the elastic limit, beyond which Hooke’s law no longer '
        'holds.', 'added')],
      'From the class’s Hooke’s Law Lab sheet and entry 11 of her equation '
      'sheet (F = −kx). The lab has no data yet, so nothing here invents her '
      'readings: the unit teaches the reasoning behind each step and answers '
      'the lab’s own questions with fresh numbers (never the sheet’s 10 inches '
      'or 30 cm). The PhET part of the lab is done on her laptop and is not '
      'reproduced here. The traps with the most airtime: recording the length '
      'instead of the stretch, leaving the mass hanger out of the weight, '
      'grams or centimetres used without converting, a force in newtons '
      'treated as a mass, and the Moon — the weights and stretches shrink but '
      'the slope k does not. Three things on the sheets are worth a word with '
      'her teacher. The lab asks for a stretch of 10 inches while the class '
      'works in SI, so a card gives 1 in = 2.54 cm. The lab does not say which '
      'axis force goes on; the unit uses force on the vertical axis (slope = '
      'k) and says that the other way round gives 1/k, and every graded stem '
      'names its axes. And her sheet’s percent error, |b| ÷ y_max × 100, does '
      'not define b or y_max; in a lab that asks for slope, y-intercept and % '
      'error together it is taught as the intercept compared with the largest '
      'force, flagged as our reading. The elastic limit is added (the sheets '
      'only hint at it). The graphs here are real force–stretch plots, which '
      'the app draws properly, unlike free-body diagrams.',
      ('Before the lab, learn the stretch-not-length and hanger cards. After '
       'it, use the Moon and backward-to-a-mass questions to check your '
       'conclusion and questions.', 20),
      PATH, 'Hookes_Law_Lab_2026.pdf — Hooke’s Law Lab', SRC,
      offset_hours=3, libv_=1)

# Post-build: quarter 2 (build() writes 1), and a sort set.
p = os.path.join(REPO, PATH)
j = json.load(io.open(p, encoding='utf-8'))
u = j['records'][UID]
u['quarter'] = 2
u['sorts'] = [{
  'id': 's-moon', 'title': 'Move the spring lab to the Moon',
  'a': 'Different on the Moon', 'b': 'Same on the Moon',
  'items': [
    {'t': 'The weight of each hanging mass', 'k': 'a',
     'why': 'Weight is mg, and g is about a sixth as big there.'},
    {'t': 'The stretch each mass produces', 'k': 'a',
     'why': 'A smaller weight stretches the same spring less.'},
    {'t': 'The largest force on your graph', 'k': 'a',
     'why': 'The heaviest mass weighs less there, so the top force is smaller.'},
    {'t': 'The mass needed to stretch the spring 5 cm', 'k': 'a',
     'why': 'The same force needs about six times the mass when g is a sixth as big.'},
    {'t': 'How far the empty hanger stretches the spring', 'k': 'a',
     'why': 'The hanger weighs less there too.'},
    {'t': 'The meter stick reading for each mass', 'k': 'a',
     'why': 'Smaller stretches leave the end of the spring at a different mark.'},
    {'t': 'The masses themselves, in kilograms', 'k': 'b',
     'why': 'Mass is the amount of matter; it is the same everywhere.'},
    {'t': 'The spring constant k', 'k': 'b',
     'why': 'k belongs to the spring. g never appears in it.'},
    {'t': 'The slope of force against stretch', 'k': 'b',
     'why': 'The slope is k, and forces and stretches shrink together.'},
    {'t': 'The force needed to stretch the spring 5 cm', 'k': 'b',
     'why': 'F = kx, and neither k nor x has changed. Only the mass that supplies it would.'},
    {'t': 'The mass of the empty hanger, in grams', 'k': 'b',
     'why': 'A hanger is the same amount of metal wherever it is. Only its weight shrinks.'},
    {'t': 'The units of k, newtons per metre', 'k': 'b',
     'why': 'Units are units, on any planet.'},
  ]}]
io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
print('  all sympy assertions passed; quarter 2 and the Moon sort attached')
