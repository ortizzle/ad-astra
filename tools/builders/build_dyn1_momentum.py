# -*- coding: utf-8 -*-
# Dynamics 1 · 1-6 Impulse and Momentum, and 1-7 Conservation of Momentum.
# Built from the files uploaded to Drive › Physics 8 › Dynamics 1 on
# 2026-10-27:
#   09_Momentum.pdf                     textbook chapter 9 (9.1, 9.2)
#   Conservation+of+Momentum+HW.pdf     40 multiple-choice items (Parts I–III)
#   Conservation_of_Momentum_Lab.pdf    the spring-cart "explosion" lab
# plus entries 19–23 of Equation_Sheet_Student_Guide.pdf for her sheet's
# notation (J = Ft = Δp, p = mv, m₂Δv₂ = −m₁Δv₁, m₁v₁_i + m₂v₂_i = …).
#
# The homework and the lab were read for WHAT THEY ASK (ideas, traps, shapes),
# never for marks. None of their numbers or scenarios is reused in a graded
# stem, and none of the textbook's worked-example or practice numbers either:
# FORBID below is asserted against every stem and option.
#
# The lab has no data yet, so it is taught as reasoning (the Ramp Lab and
# Kinematics 2 · 2-3 call): why m₁/m₂ should equal Δx₂/Δx₁, why the spring is
# internal, and why kinetic energy was not conserved.
#
# 1-5 is reserved for the Hooke's Law unit and is not built here.
#
# EVERY number is computed with sympy below and asserted before it reaches a
# question, including that no distractor is also correct. Positive direction
# is named in every stem that needs a sign. g is never needed.
import sys, os, json, io, re
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

def R(a, b=None): return sp.Rational(a, b) if b is not None else sp.Rational(str(a))
def rnd(x, n=1):
    return float(sp.N(sp.Rational(round(float(x) * 10**n), 10**n)))
def eq(x, n, want): return round(rnd(x, n), n) == want
def distinct(*xs):
    a = xs[0]
    for x in xs[1:]:
        assert abs(float(x) - float(a)) > 1e-6, (a, x)
def KE(m, v): return R(1)/2 * m * v**2

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def patch(path, uid, **fields):
    p = os.path.join(REPO, path)
    j = json.load(io.open(p, encoding='utf-8'))
    j['records'][uid].update(fields)
    io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))

SRC9 = '09_Momentum.pdf (Drive, Physics 8 › Dynamics 1)'
SRCHW = 'Conservation+of+Momentum+HW.pdf (Drive, Physics 8 › Dynamics 1)'
SRCLAB = 'Conservation_of_Momentum_Lab.pdf (Drive, Physics 8 › Dynamics 1)'

# Numbers that must never appear in a graded stem or option: the textbook's
# worked examples and practice problems, and the homework's (mass, speed)
# pairings. A pairing is a mass followed, in the same sentence, by a speed.
FORBID = re.compile(
    r'(?<![\d.])(2200 kg|725 kg|0\.144 kg|240(\.0)? kg|0\.060 kg|2275 kg|875 kg|'
    r'0\.105 kg|35(\.0)? g\b|0\.355 kg|0\.710 kg|84 kg|875 m/s|4\.00 kg|625 m/s|'
    r'225 kg|35\.6 kg|0\.115 kg|845 kg|72 000|2575 kg|825 kg|0\.265 kg|92 kg|'
    r'7\.0 kg|1\.4 N·s|38(\.0)? m/s|0\.150 kg|0\.17 kg|0\.200 kg|5\.00 g)')
HW_PAIRS = [('2.0', '5.0'), ('3.0', '4.0'), ('2.0', '6.0'), ('1.0', '8.0'),
            ('0.20', '15'), ('0.50', '10'), ('1.5', '4.0'), ('4.0', '3.0'),
            ('3.0', '10'), ('0.10', '20'), ('1.0', '6.0'), ('2.0', '4.0'),
            ('0.40', '5.0'), ('2.0', '3.0'), ('1.0', '12'), ('0.20', '10'),
            ('0.50', '8.0'), ('60', '10'), ('0.50', '6.0')]
def fresh(Q):
    for x in Q:
        if x.get('kind') == 'order':
            texts = [x['q']] + x['opts']          # each option is its own scene
        else:
            texts = [' '.join([x['q']] + x['opts'])]
        for t in texts:
            assert not FORBID.search(t), (x['id'], FORBID.search(t).group(0))
            for s in re.split(r'(?<=[.?;:])\s', t):
                for m, v in HW_PAIRS:
                    pat = r'(?<![\d.])%s kg\b[^.?;]*?(?<![\d.])%s m/s' % (re.escape(m), re.escape(v))
                    assert not re.search(pat, s), (x['id'], m, v, s)

# =============================================================================
# 1-6 IMPULSE AND MOMENTUM  (chapter 9.1)
# =============================================================================
# --- numbers ----------------------------------------------------------------
p_ball = R('0.45') * R(-14);              assert p_ball == R('-6.3')
p_div = R(14) / R('0.45');                assert eq(p_div, 0, 31)
p_sq = R('0.45') * 14**2;                 assert eq(p_sq, 0, 88)
distinct(p_ball, -p_ball, -p_div, -p_sq)

p_car = 1600 * R('4.5');                  assert p_car == 7200
v_bike = p_car / 180;                     assert v_bike == 40
v_inv = R('4.5') * 180 / 1600;            assert eq(v_inv, 2, 0.51)
v_ke = R('4.5') * sp.sqrt(R(1600) / 180); assert eq(v_ke, 0, 13)
distinct(v_bike, v_inv, R('4.5'), v_ke)

J_puck = 48 * R('0.025');                 assert J_puck == R('1.2')
distinct(J_puck, R(48) / R('0.025'), J_puck / 2, 48)
assert R(48) / R('0.025') == 1920

v_kick = R('5.4') / R('0.36');            assert v_kick == 15
distinct(v_kick, R('5.4') * R('0.36'), R('0.36') / R('5.4'), R('5.4'))
assert eq(R('5.4') * R('0.36'), 1, 1.9) and eq(R('0.36') / R('5.4'), 3, 0.067)

dp_catch = R('0.14') * (0 - 25);          assert dp_catch == R('-3.5')
F_catch = abs(dp_catch) / R('0.010');     assert F_catch == 350
distinct(F_catch, R('3.5'), R('3.5') * R('0.010'), R(25) / R('0.010'))

dp_reb = R('0.40') * (R(-5) - R('7.5'));  assert dp_reb == -5
dp_slip = R('0.40') * (R(-5) + R('7.5')); assert dp_slip == 1            # subtracted speeds
dp_final = R('0.40') * R(-5);             assert dp_final == -2          # final only
distinct(dp_reb, -dp_slip, -dp_reb, dp_final)

J_land = 55 * 8;                          assert J_land == 440
F_mat = R(J_land) / R('0.040');           assert F_mat == 11000
F_pad = R(J_land) / R('0.50');            assert F_pad == 880
assert F_mat / F_pad == R('12.5')

J_tri = R(1, 2) * R('0.006') * 900;       assert J_tri == R('2.7')
distinct(J_tri, 2 * J_tri, R(1, 2) * 6 * 900, R(900) / 6)
assert R(1, 2) * 6 * 900 == 2700 and R(900) / 6 == 150

p_i = R('2.5') * 3;                       assert p_i == R('7.5')
J16 = R(-5) * 2;                          assert J16 == -10
v_f16 = (p_i + J16) / R('2.5');           assert v_f16 == -1
v_wrong_add = (p_i - J16) / R('2.5');     assert v_wrong_add == 7
v_rest16 = J16 / R('2.5');                assert v_rest16 == -4
distinct(v_f16, v_wrong_add, -v_f16, v_rest16)

ordA = R('2.5') * (R('2.4') + R('2.4'));  assert ordA == 12              # bounces back
ordB = 3 * 3;                             assert ordB == 9               # stops
ordC = R('0.75') * (8 + 2);               assert ordC == R('7.5')        # bounces back slower
ordD = 4 * (R('3.5') - 2);                assert ordD == 6               # speeds up
assert [ordA, ordB, ordC, ordD] == sorted([ordA, ordB, ordC, ordD], reverse=True)
assert R('2.5') * 0 == 0 and R('0.75') * (8 - 2) < ordD                  # ignoring the rebound reorders

t_tug = R(36000) / 1500;                  assert t_tug == 24
distinct(t_tug, R(1500) / 36000, R(36000) * 1500, R('2.4'))

J_graph = 6 * 2 + (-4) * 1;               assert J_graph == 8
distinct(J_graph, 6 * 2 + 4 * 1, 6 * 2, 6 - 4)

C, Q = [], []
card(C, 'Momentum',
     '**Momentum is an object’s mass multiplied by its velocity.**\n'
     '• Its unit is kg·m/s.\n'
     '• Newton called it the “quantity of motion”: how hard a moving thing is '
     'to stop depends on both how heavy and how fast it is.',
     eq='p = mv')
card(C, 'Momentum has a direction',
     '**Momentum is a vector: it points the same way as the velocity.**\n'
     '• Pick a positive direction first. Anything moving the other way has a '
     'negative velocity, so a negative momentum.\n'
     '• A car going north and the same car going south at the same speed have '
     'momenta of the same size and opposite signs, so they are different '
     'momenta.',
     hint='A minus sign is a direction, never “less”.')
card(C, 'Heavy and slow, or light and fast',
     '**A light, fast object can have exactly the same momentum as a heavy, '
     'slow one.**\n'
     '• A bullet and a slowly rolling truck can carry equal momentum: the '
     'bullet’s speed makes up for its tiny mass.\n'
     '• To compare momenta, multiply; never compare masses or speeds alone.')
card(C, 'Impulse',
     '**Impulse is a force multiplied by the time it acts.**\n'
     '• Its unit is the newton-second, N·s, which is the same as kg·m/s.\n'
     '• It is a vector pointing the way the force points.\n'
     '• t is only the time the force actually acts — the contact time.',
     eq='J = Ft')
card(C, 'The impulse–momentum theorem',
     '**The impulse on an object equals its change in momentum.**\n'
     '• It comes straight from F = ma with a = Δv / t: multiply both sides by '
     't and Ft = mΔv.\n'
     '• So a final momentum is the starting momentum plus the impulse.',
     eq='J = Ft = Δp     Δp = p_f − p_i')
card(C, 'Change means final minus initial',
     '**Δp is the final momentum minus the initial momentum, signs '
     'included.**\n'
     '• Write each momentum with its sign before you subtract.\n'
     '• Getting the subtraction backwards gives the right size and the wrong '
     'direction.')
card(C, 'A bounce changes momentum more than a stop',
     '**An object that bounces back has a bigger change in momentum than one '
     'that simply stops.**\n'
     '• Stopping takes the momentum to zero. Bouncing takes it to zero and then '
     'out the other way.\n'
     '• A ball that bounces back at the speed it arrived has Δp of twice its '
     'momentum — so the wall gives it twice the impulse.\n'
     '• The speed being the same does NOT make Δp zero: the direction changed.',
     hint='Same speed back is not “no change”. It is double.')
card(C, 'Longer time, smaller force',
     '**The same change in momentum can come from a big force for a short time '
     'or a small force for a long time.**\n'
     '• Ft is fixed by the change in momentum, so stretching t shrinks F.\n'
     '• Bending your knees when you land, padded dashboards, crumple zones and '
     'bumpers that push in all work this way.')
card(C, 'How an air bag helps',
     '**An air bag makes the driver’s stop take longer, so the force on the '
     'driver is smaller.**\n'
     '• The driver’s change in momentum is the same with or without it: the '
     'same mass goes from the same speed to zero.\n'
     '• Only the time changes, and a longer time means a smaller average '
     'force.',
     hint='The air bag changes t, not Δp.')
card(C, 'Catching with soft hands',
     '**To catch something with less sting, let your hands move back with '
     'it.**\n'
     '• Moving with the ball stretches the time it takes to stop, so the same '
     'impulse needs less force.\n'
     '• Meeting it with stiff, still hands stops it fast, with a big force.')
card(C, 'Follow-through',
     '**Following through keeps the bat, racket or foot in contact longer, so '
     'the ball gets a bigger impulse and leaves with more momentum.**\n'
     '• With the same force, a longer contact time means a bigger Ft.\n'
     '• This is the other side of the air bag: there the change was fixed and '
     'time shrank the force; here the force is fixed and time grows the '
     'change.', frm='added')
card(C, 'Impulse is the area under a force–time graph',
     '**The impulse is the area between a force–time graph and the time '
     'axis.**\n'
     '• A constant force gives a rectangle: force × time.\n'
     '• A force that rises and falls gives another shape, such as a triangle '
     '(½ × base × height).\n'
     '• Read the time axis’s unit: milliseconds must become seconds.')
C[-1]['graph'] = {'w': [0, 3, 0, 50], 'gx': 0.5, 'gy': 10,
                  'series': [{'type': 'pts', 'pts': [[0, 40], [2, 40], [2, 0], [3, 0]]}],
                  'xl': 't (s)', 'yl': 'F (N)'}
card(C, 'Area below the axis counts as negative',
     '**Force below the time axis is pushing the negative way, so its area is '
     'subtracted.**\n'
     '• Add the area above the axis, subtract the area below: that total is '
     'the impulse.\n'
     '• A push forward followed by a push back can leave a small net '
     'impulse, or none at all.')
card(C, 'Average force',
     '**When the force changes during a hit, use the average force: the change '
     'in momentum divided by the time.**\n'
     '• Real collisions start small, peak and fall away. The impulse is the '
     'same as a steady average force acting for the whole time.',
     eq='F = Δp / t')
card(C, 'Momentum is not kinetic energy',
     '**Momentum is mv; kinetic energy is ½mv². They are different '
     'quantities.**\n'
     '• Momentum has a direction; kinetic energy never does.\n'
     '• Double the speed and the momentum doubles, but the kinetic energy '
     'becomes four times as big.',
     hint='Squared speed means energy. Plain speed means momentum.',
     eq='p = mv     KE = ½mv²', frm='added')
card(C, 'Newton’s second law, in momentum form',
     '**The net force on an object equals the rate its momentum changes.**\n'
     '• F = Δp / t is the same law as F = ma, written the way Newton first '
     'wrote it.\n'
     '• No net force means no change in momentum.')
card(C, 'Your sheet’s notation',
     '**Your sheet writes impulse as J = Ft = Δp, and uses i and f for before '
     'and after.**\n'
     '• The textbook writes the same thing with 1 and 2: Ft = p₂ − p₁.\n'
     '• Both mean final minus initial.', frm='added')

q(Q, 1, 'What is an object’s momentum?',
  ['Its mass times its velocity, pointing the way it moves',
   'Half its mass times its speed squared, with no direction',
   'The force on it times the time that force acts',
   'Its mass times its acceleration, pointing the way it speeds up'],
  0, 'Which quantity depends on mass and plain velocity?',
  ['Momentum is defined as p = mv.',
   'Velocity has a direction, so momentum does too.',
   '½mv² is kinetic energy, Ft is impulse and ma is the net force.',
   'Momentum is mass times velocity.'],
  '**Momentum is p = mv, a vector in the direction of the velocity.** The '
  'other three are real quantities with other names: kinetic energy, impulse '
  'and the net force.',
  'p = mv — no squares, no time.')

q(Q, 1, 'Which unit measures impulse?',
  ['N·s, which is the same as kg·m/s', 'N·m, which is the same as a joule',
   'N/s, which is the same as kg·m/s³', 'kg·m/s², which is the same as a newton'],
  0, 'Impulse is force multiplied by time.',
  ['Impulse is J = Ft.',
   'So its unit is a newton times a second, N·s.',
   'A newton is kg·m/s², and multiplying by s gives kg·m/s — the unit of momentum.',
   'The unit is N·s, which equals kg·m/s.'],
  '**Force × time gives newton-seconds, and N·s = kg·m/s**, the same unit as '
  'momentum — which is exactly why impulse can equal a change in momentum. '
  'N·m is the unit of work and energy; kg·m/s² is a force.',
  'Matching units is a quick check that J = Δp makes sense.')

q(Q, 1, 'By the impulse–momentum theorem, the impulse on an object is equal to…',
  ['its change in momentum', 'its final momentum',
   'its change in kinetic energy', 'the force needed to keep it moving'],
  0, 'Ft = mΔv.',
  ['Start from F = ma and write a as Δv / t.',
   'Multiply both sides by t: Ft = mΔv.',
   'mΔv is the change in momentum.',
   'Impulse equals the change in momentum.'],
  '**Impulse equals the CHANGE in momentum, Ft = Δp.** It equals the final '
  'momentum only when the object starts at rest. Changing energy is the job of '
  'work, and no force is needed just to keep something moving.',
  'Impulse changes momentum. It does not set it from nothing.')

q(Q, 1, 'A car drives north at 20 m/s. Later, the same car drives south at 20 m/s. '
        'Are its two momenta the same?',
  ['No: they are the same size but point in opposite directions',
   'Yes: the same mass at the same speed gives the same momentum',
   'No: going south it has less momentum, because south is negative',
   'Yes: momentum has a size but no direction, like speed'],
  0, 'Is momentum a vector?',
  ['Momentum is mass times velocity, and velocity has a direction.',
   'North and south are opposite directions.',
   'So the two momenta have equal sizes and opposite directions.',
   'They are different momenta.'],
  '**Same size, opposite directions — so not the same momentum.** A negative '
  'sign only says which way; it is not “less” momentum. And momentum is a '
  'vector, unlike speed.',
  'Two vectors are equal only if size AND direction match.')

q(Q, 2, 'A 0.45 kg ball rolls west at 14 m/s. Taking east as positive, what is '
        'its momentum?',
  ['−6.3 kg·m/s', '+6.3 kg·m/s', '−31 kg·m/s', '−88 kg·m/s'],
  0, 'p = mv, and the velocity carries a sign.',
  ['East is positive, so a westward velocity is −14 m/s.',
   'p = mv = (0.45 kg)(−14 m/s).',
   'p = −6.3 kg·m/s.',
   'The momentum is −6.3 kg·m/s, that is 6.3 kg·m/s west.'],
  '**p = (0.45)(−14) = −6.3 kg·m/s.** +6.3 drops the sign that says it is '
  'moving west; −31 divides the speed by the mass; −88 squares the speed, '
  'which mixes momentum up with kinetic energy.',
  'Write the sign into the velocity before you multiply.')

q(Q, 2, 'A 1600 kg car rolls at 4.5 m/s. How fast would a 180 kg motorbike and '
        'rider have to go to have the same momentum?',
  ['40 m/s', '0.51 m/s', '4.5 m/s', '13 m/s'],
  0, 'Find the car’s momentum, then divide by the bike’s mass.',
  ['The car’s momentum: p = (1600)(4.5) = 7200 kg·m/s.',
   'The bike needs the same p, so v = p / m.',
   'v = 7200 ÷ 180 = 40 m/s.',
   'The bike would need 40 m/s.'],
  '**p = 1600 × 4.5 = 7200 kg·m/s, and 7200 ÷ 180 = 40 m/s.** 0.51 m/s puts '
  'the masses the wrong way up; 4.5 m/s forgets that a lighter object needs '
  'more speed; 13 m/s is the speed for equal kinetic energy, not equal momentum.',
  'A lighter object needs more speed — by exactly the mass ratio.')

q(Q, 2, 'A hockey stick pushes a puck with an average force of 48 N for '
        '0.025 s. What impulse does the stick give the puck?',
  ['1.2 N·s', '1920 N·s', '0.60 N·s', '48 N·s'],
  0, 'J = Ft.',
  ['Impulse is force times the time it acts.',
   'J = (48 N)(0.025 s).',
   'J = 1.2 N·s.',
   'The impulse is 1.2 N·s, in the direction of the push.'],
  '**J = Ft = 48 × 0.025 = 1.2 N·s.** 1920 divides the force by the time; '
  '0.60 halves it for no reason (a ½ belongs to a triangle on a graph, not to '
  'an average force); 48 leaves out the time altogether.',
  'Impulse multiplies. Force divided by time is not anything useful.')

q(Q, 2, 'A 0.36 kg ball at rest is kicked, receiving an impulse of 5.4 N·s '
        'toward the east. What is its velocity just after the kick?',
  ['15 m/s east', '1.9 m/s east', '0.067 m/s east', '5.4 m/s east'],
  0, 'The impulse equals its change in momentum, and it started with none.',
  ['It starts at rest, so its starting momentum is 0.',
   'Δp = J, so its final momentum is 5.4 kg·m/s east.',
   'v = p / m = 5.4 ÷ 0.36 = 15 m/s.',
   'The ball leaves at 15 m/s east.'],
  '**From rest, p_f = J = 5.4 kg·m/s, so v = 5.4 ÷ 0.36 = 15 m/s east.** '
  '1.9 multiplies by the mass instead of dividing; 0.067 divides the wrong '
  'way round; 5.4 treats an impulse as if it were a speed.',
  'Impulse gives momentum. Divide by mass to get velocity.')

q(Q, 2, 'A 0.14 kg ball moving at 25 m/s is caught and brought to rest in '
        '0.010 s. What is the size of the average force on the ball?',
  ['350 N', '3.5 N', '0.035 N', '2500 N'],
  0, 'Find the change in momentum, then divide by the time.',
  ['Change in momentum: 0.14 × (0 − 25) = −3.5 kg·m/s.',
   'F = Δp / t = 3.5 ÷ 0.010 in size.',
   'F = 350 N.',
   'The average force is 350 N, against the ball’s motion.'],
  '**Δp = 3.5 kg·m/s in size, and 3.5 ÷ 0.010 = 350 N.** 3.5 N is the impulse '
  'passed off as a force; 0.035 N multiplies by the time; 2500 N leaves out '
  'the mass.',
  'Units guard this one: kg·m/s ÷ s = N.')

q(Q, 2, 'Taking east as positive: a 0.40 kg ball moving east at 7.5 m/s hits a '
        'wall and bounces back west at 5.0 m/s. What is its change in momentum?',
  ['−5.0 kg·m/s', '−1.0 kg·m/s', '+5.0 kg·m/s', '−2.0 kg·m/s'],
  0, 'Final minus initial, with both signs written in.',
  ['Initial momentum: 0.40 × (+7.5) = +3.0 kg·m/s.',
   'Final momentum: 0.40 × (−5.0) = −2.0 kg·m/s.',
   'Δp = p_f − p_i = −2.0 − (+3.0) = −5.0 kg·m/s.',
   'The change is −5.0 kg·m/s, that is 5.0 kg·m/s toward the west.'],
  '**Δp = (−2.0) − (+3.0) = −5.0 kg·m/s.** −1.0 subtracts the speeds as if '
  'the ball had only slowed down — it reversed, so the two parts ADD. +5.0 '
  'subtracts the wrong way round; −2.0 is just the final momentum.',
  'A bounce: the sizes add, because the direction flipped.')

q(Q, 2, 'A tennis ball hits the floor moving down at 6 m/s and leaves moving '
        'up at 6 m/s. What is true about its change in momentum?',
  ['It is not zero: it points up and is twice its momentum just before landing',
   'It is zero, because the ball’s speed is the same before and after',
   'It is not zero: it points down, the way the ball was moving at first',
   'It is not zero: it points up and equals its momentum just before landing'],
  0, 'Same speed is not the same velocity.',
  ['Take up as positive. Just before landing, p = −6m.',
   'Just after, p = +6m.',
   'Δp = (+6m) − (−6m) = +12m.',
   'So Δp points up and is twice the landing momentum.'],
  '**Δp = (+6m) − (−6m) = +12m: upward, and twice the size of either '
  'momentum.** The floor had to stop the ball AND send it back up. The change '
  'points the way the floor pushes, up.',
  'Speed unchanged, direction reversed: Δp doubled.')

q(Q, 3, 'Two balls of equal mass hit a hanging board at the same speed. One is '
        'made of clay and sticks; the other is rubber and bounces straight '
        'back. Which gives the board the bigger impulse?',
  ['The rubber ball: its momentum is reversed, not just stopped',
   'The clay ball: it hands over all its momentum and keeps none',
   'Neither: equal masses at equal speeds give equal impulses',
   'The clay ball: it stays touching the board, so it pushes longer'],
  0, 'The board’s impulse on each ball equals that ball’s change in momentum.',
  ['The clay ball goes from p to 0: a change of size p.',
   'The rubber ball goes from p to −p: a change of size 2p.',
   'By the third law, the board gets an equal and opposite impulse to each.',
   'The rubber ball gives the bigger impulse.'],
  '**The rubber ball’s momentum changes by 2p, the clay’s by p — and the board '
  'receives the same size of impulse it gives.** Equal start conditions do not '
  'mean equal changes. Keeping its momentum is exactly what the bouncing ball '
  'does NOT do: it leaves with momentum the other way.',
  'Bouncing beats sticking for knocking a target back.')

q(Q, 2, 'Why does an air bag reduce injuries in a crash?',
  ['It makes the stop take longer, so the same change in momentum needs less force',
   'It makes the driver’s change in momentum smaller, so the impulse is smaller',
   'It makes the stop take less time, so the driver stops before hitting anything',
   'It pushes the driver back with a force larger than the force of the crash'],
  0, 'What does the air bag change: Δp, or t?',
  ['The driver goes from the car’s speed to zero either way.',
   'So the change in momentum, and the impulse, are the same.',
   'The air bag stretches out the time of the stop.',
   'With Ft fixed, a longer t means a smaller average F.'],
  '**The change in momentum is fixed by the crash; the air bag only makes the '
  'time longer, so the average force is smaller.** “A smaller change in '
  'momentum” is the tempting answer, but nothing about the bag changes the driver’s mass or how '
  'fast the driver was going.',
  'Air bags, bent knees and crumple zones all change t, never Δp.')

q(Q, 3, 'A 55 kg stunt performer lands at 8.0 m/s. On a thin mat she stops in '
        '0.040 s; on a thick crash pad she stops in 0.50 s. How do the two stops '
        'compare?',
  ['Same impulse; the pad’s average force is 12.5 times smaller',
   'The pad’s average force and impulse are both 12.5 times smaller',
   'Same average force; the pad only spreads it across a larger area',
   'Same impulse; the pad’s average force is 12.5 times larger'],
  0, 'Her change in momentum is the same on both.',
  ['Her change in momentum is 55 × 8.0 = 440 kg·m/s either way, so the impulse is the same.',
   'On the mat: F = 440 ÷ 0.040 = 11 000 N.',
   'On the pad: F = 440 ÷ 0.50 = 880 N.',
   '11 000 ÷ 880 = 12.5, so the pad’s force is 12.5 times smaller.'],
  '**The impulse is 440 N·s both times; dividing by 0.50 s instead of 0.040 s '
  'makes the force 12.5 times smaller.** The impulse cannot shrink, because she '
  'still goes from 8.0 m/s to rest. A longer time means a SMALLER force, '
  'never a larger one.',
  'Same Δp, ratio of times = ratio of forces, upside down.')

q(Q, 2, 'To catch a fast ball barehanded with the least sting, you should…',
  ['let your hands move back with the ball as it arrives',
   'hold your hands perfectly still so the ball stops at once',
   'push your hands forward to meet the ball early',
   'close your hands quickly so the ball stops sooner'],
  0, 'Which choice makes the stop take the longest?',
  ['The ball’s change in momentum is the same however you catch it.',
   'Moving your hands back with it makes the stop take longer.',
   'A longer stopping time means a smaller average force.',
   'So let your hands move back with the ball.'],
  '**Giving with the ball stretches the stopping time, so the same impulse '
  'needs a smaller force on your hands.** Stiff hands, meeting it early or '
  'snapping shut all make the stop quicker — and quicker means harder.',
  'Soft hands are long t.')

q(Q, 2, 'A batter learns to follow through, keeping the bat on the ball longer '
        'with the same average force. What changes?',
  ['The impulse grows, so the ball leaves with more momentum',
   'Nothing: the impulse stays the same, so the ball’s speed does too',
   'The force on the ball grows, while the impulse stays the same',
   'The ball leaves slower, because the force is spread out in time'],
  0, 'Impulse is Ft. Which part changed?',
  ['The average force stays the same.',
   'The contact time gets longer.',
   'So Ft, the impulse, gets bigger.',
   'A bigger impulse means a bigger change in momentum: the ball leaves faster.'],
  '**Same force, longer time: a bigger Ft, so more momentum for the ball.** '
  'This is the air bag run in reverse. There the change in momentum was fixed '
  'and a longer time shrank the force; here the force is fixed and a longer '
  'time grows the change.',
  'Ask which of F, t and Δp is fixed, then read off the other two.', frm='added')

q(Q, 2, 'The graph shown is the force of a racket on a ball during one hit: it '
        'rises from 0 to 900 N at 3 ms and falls back to 0 at 6 ms. What '
        'impulse does the racket give the ball?',
  ['2.7 N·s', '5.4 N·s', '2700 N·s', '150 N·s'],
  0, 'The impulse is the area of the triangle. Watch the time unit.',
  ['The area under the graph is a triangle with base 6 ms and height 900 N.',
   '6 ms = 0.006 s.',
   'Area = ½ × 0.006 × 900 = 2.7.',
   'The impulse is 2.7 N·s.'],
  '**Impulse = area = ½ × 0.006 s × 900 N = 2.7 N·s.** 5.4 forgets the ½ of a '
  'triangle; 2700 leaves the time in milliseconds; 150 divides the force by the '
  'time.',
  'Triangle: ½ × base × height, with the base in seconds.')
Q[-1]['graph'] = {'w': [0, 8, 0, 1000], 'gx': 1, 'gy': 100, 'ly': 200,
                  'series': [{'type': 'pts', 'pts': [[0, 0], [3, 900], [6, 0], [8, 0]]}],
                  'pts': [{'x': 3, 'y': 900, 'label': '900 N'}],
                  'xl': 't (ms)', 'yl': 'F (N)'}

q(Q, 3, 'The graph shown is the force on a cart: +6 N for the first 2 s, then '
        '−4 N for the next 1 s. What is the total impulse on the cart?',
  ['8 N·s', '16 N·s', '12 N·s', '2 N·s'],
  0, 'Area above the axis counts plus; area below counts minus.',
  ['First part: 6 N × 2 s = +12 N·s.',
   'Second part: −4 N × 1 s = −4 N·s.',
   'Total = 12 − 4 = 8 N·s.',
   'The total impulse is 8 N·s in the positive direction.'],
  '**(+6)(2) + (−4)(1) = 12 − 4 = 8 N·s.** 16 counts the backward push as if '
  'it were forward; 12 ignores it altogether; 2 subtracts the forces and '
  'forgets the times.',
  'Below the axis is a push the other way: subtract it.')
Q[-1]['graph'] = {'w': [0, 4, -6, 8], 'gx': 0.5, 'gy': 2, 'lx': 1,
                  'series': [{'type': 'pts', 'pts': [[0, 6], [2, 6], [2, -4], [3, -4], [3, 0], [4, 0]]}],
                  'xl': 't (s)', 'yl': 'F (N)'}

q(Q, 3, 'Taking east as positive: a 2.5 kg cart moves east at 3.0 m/s. A '
        'constant 5.0 N force pointing WEST acts on it for 2.0 s. What is its '
        'velocity afterward?',
  ['1.0 m/s west', '7.0 m/s east', '1.0 m/s east', '4.0 m/s west'],
  0, 'Final momentum = starting momentum + impulse, with signs.',
  ['Starting momentum: 2.5 × (+3.0) = +7.5 kg·m/s.',
   'Impulse: (−5.0 N)(2.0 s) = −10 N·s.',
   'Final momentum: 7.5 + (−10) = −2.5 kg·m/s.',
   'v = −2.5 ÷ 2.5 = −1.0 m/s, so 1.0 m/s west.'],
  '**p_f = 7.5 − 10 = −2.5 kg·m/s, so v = −1.0 m/s: 1.0 m/s west.** The '
  'westward push first stopped the cart, then started it the other way. '
  '7.0 m/s east adds the impulse with the wrong sign; 1.0 m/s east loses the '
  'sign of the answer; 4.0 m/s west forgets the cart was already moving.',
  'Start with what it had, then add the impulse.')

q(Q, 2, 'A tugboat must change a barge’s momentum by 36 000 kg·m/s. Its engine '
        'pushes with an average force of 1500 N. How long must it push?',
  ['24 s', '0.042 s', '5.4 × 10⁷ s', '2.4 s'],
  0, 'Ft = Δp, so t = Δp / F.',
  ['Impulse needed: 36 000 N·s.',
   't = Δp / F = 36 000 ÷ 1500.',
   't = 24 s.',
   'It must push for 24 s.'],
  '**t = 36 000 ÷ 1500 = 24 s.** 0.042 s divides the wrong way round; '
  '5.4 × 10⁷ s multiplies; 2.4 s slips a decimal place.',
  'A small force can do the same job given enough time.')

q(Q, 2, 'Doubling a car’s speed does what to its momentum and its kinetic energy?',
  ['Its momentum doubles; its kinetic energy becomes four times as big',
   'Its momentum doubles; its kinetic energy doubles too',
   'Its momentum becomes four times as big; its kinetic energy doubles',
   'Its momentum becomes four times as big; so does its kinetic energy'],
  0, 'p = mv but KE = ½mv².',
  ['Momentum is proportional to v, so doubling v doubles p.',
   'Kinetic energy is proportional to v².',
   '2² = 4, so the kinetic energy is four times as big.',
   'Momentum ×2, kinetic energy ×4.'],
  '**p = mv grows with v; KE = ½mv² grows with v².** So twice the speed is '
  'twice the momentum but four times the kinetic energy — which is why the two '
  'can never be swapped for each other.',
  'Squared speed belongs to energy.', frm='added')

q(Q, 3, 'Rank these carts from GREATEST to LEAST change in momentum (size only).',
  ['A: 2.5 kg cart hits a wall at 2.4 m/s and bounces back at 2.4 m/s',
   'B: 3.0 kg cart at 3.0 m/s stops dead against a wall',
   'C: 0.75 kg cart hits a wall at 8.0 m/s and bounces back at 2.0 m/s',
   'D: 4.0 kg cart speeds up in a straight line from 2.0 m/s to 3.5 m/s'],
  0, 'For a bounce, the speeds add.',
  ['A: 2.5 × (2.4 + 2.4) = 12 kg·m/s.',
   'B: 3.0 × 3.0 = 9 kg·m/s.',
   'C: 0.75 × (8.0 + 2.0) = 7.5 kg·m/s.',
   'D: 4.0 × (3.5 − 2.0) = 6 kg·m/s. So A, B, C, D.'],
  '**A (12), B (9), C (7.5), D (6) kg·m/s.** Cart A is the trap: it bounces '
  'back at the same speed, and calling that “no change” puts it last instead '
  'of first. Cart C’s reversal adds its two speeds too.',
  'Reversing direction always adds the two sizes.',
  kind='order')

fresh(Q)
build('ad-astra', C, Q, 'unit-phys-dyn1-impulse',
      'Dynamics 1 · 1-6 Impulse and Momentum', 'physics',
      'Momentum as mass times velocity — a vector with a sign — and impulse as '
      'force times the time it acts. The impulse–momentum theorem ties them '
      'together: the impulse on an object equals its change in momentum. From '
      'there: why a bounce changes momentum more than a stop, why a longer '
      'stopping time means a smaller force (air bags, bent knees, soft '
      'hands), how follow-through adds momentum, and how to read an impulse '
      'off a force–time graph as an area.',
      'Forces in a crash, a kick or a catch change too fast to follow with '
      'F = ma moment by moment. Impulse skips the moment-by-moment detail and '
      'compares before with after — and it is the step that leads straight '
      'into conservation of momentum in 1-7.',
      [('Define the momentum of an object.', 'source'),
       ('Determine the impulse given to an object.', 'source'),
       ('Recognize that impulse equals the change in momentum of an object.', 'source'),
       ('Compare the system before and after an event in momentum problems.', 'source'),
       ('Explain how stretching the stopping time reduces the force, using air '
        'bags and catching as examples.', 'added'),
       ('Find an impulse as the area under a force–time graph.', 'source')],
      'From chapter 9.1 (Impulse and Momentum) of 09_Momentum.pdf in the '
      'Dynamics 1 folder, with the momentum homework and the explosion lab '
      'read for what they ask; nothing of hers was marked or recorded. Every '
      'number was computed with sympy in the builder and checked before it '
      'was written, and none of the textbook’s or the homework’s own numbers '
      'is reused in a graded question. The traps with deliberate airtime: the '
      'sign that says which way (dropped signs are offered as wrong answers), '
      'a bounce counting as “no change” because the speed is the same (it is '
      'double the momentum, and the rebound question offers the subtracted '
      'speeds), an impulse passed off as a force (forgetting to divide by the '
      'time), milliseconds left unconverted on a force–time graph, area below '
      'the axis being subtracted, and the air bag “making the change in '
      'momentum smaller” (it changes only the time). Two notation points are '
      'worth knowing: her sheet writes J = Ft = Δp with i and f for before '
      'and after, while the textbook writes Ft = p₂ − p₁ — the same thing; '
      'and two cards are flagged as study suggestions rather than class '
      'material (follow-through, and momentum versus kinetic energy, which '
      'the sheet’s own guide warns about).',
      ('Read the cards on impulse and the bounce until you can explain why a '
       'bounce doubles the change, then take the quiz. On every question, '
       'write the positive direction down before you touch a number.', 25),
      'content/phys-dyn1-impulse.json',
      'Chapter 9, Momentum and Its Conservation (9.1 Impulse and Momentum)',
      SRC9 + '; questions shaped by ' + SRCHW, offset_hours=3, libv_=1)
patch('content/phys-dyn1-impulse.json', 'unit-phys-dyn1-impulse', quarter=2)

# =============================================================================
# 1-7 CONSERVATION OF MOMENTUM  (chapter 9.2, the homework, the lab)
# =============================================================================
v3 = (R('1.2') * 5) / (R('1.2') + R('1.8'));        assert v3 == 2
distinct(v3, R('1.2') * 5 / R('1.8'), 5, R('2.5'))
assert eq(R('1.2') * 5 / R('1.8'), 1, 3.3)

p4 = R('0.90') * 6 + R('1.5') * (-2);               assert p4 == R('2.4')
v4 = p4 / (R('0.90') + R('1.5'));                   assert v4 == 1
v4_nosign = (R('0.90') * 6 + R('1.5') * 2) / R('2.4'); assert v4_nosign == R('3.5')
v4_avg = R(6 - 2, 2);                                assert v4_avg == 2
distinct(v4, v4_nosign, -v4, v4_avg)

v5 = (R('2.4') * 4 - R('2.4') * 1) / R('1.6');      assert v5 == R('4.5')
assert KE(R('2.4'), 1) + KE(R('1.6'), v5) <= KE(R('2.4'), 4)   # physical: KE does not grow
distinct(v5, 3, R('2.4') * 4 / R('1.6'), (R('2.4') * 4 + R('2.4') * 1) / R('1.6'))
assert R('2.4') * 4 / R('1.6') == 6 and (R('2.4') * 4 + R('2.4')) / R('1.6') == R('7.5')

v6 = -(R('2.4') * 12) / 48;                          assert v6 == R('-0.60')
distinct(v6, -v6, -12, -(48 * R(12)) / R('2.4'))
assert 48 * R(12) / R('2.4') == 240

v7 = -(R('0.60') * 9) / R('0.90');                   assert v7 == -6
distinct(v7, -9, -(R('0.90') * 9) / R('0.60'), -v7)
assert R('0.90') * 9 / R('0.60') == R('13.5')

v8 = (3 * 2 - 1 * 9) / R(2);                         assert v8 == R('-1.5')
distinct(v8, -v8, R(-9, 2), (3 * 2 + 9) / R(2))
assert (3 * 2 + 9) / R(2) == R('7.5')

lost11 = KE(R('0.80'), 6) - KE(R('2.4'), R('0.80') * 6 / R('2.4'))
assert R('0.80') * 6 / R('2.4') == 2 and KE(R('0.80'), 6) == R('14.4')
assert KE(R('2.4'), 2) == R('4.8') and lost11 == R('9.6')
distinct(lost11, 0, R('14.4'), R('4.8'))

ratio15 = R(54) / 36;                                 assert ratio15 == R('1.5')
ke_ratio16 = R(1, 3)                                  # KE = p²/2m with m_X = 3 m_Y
assert (R(1) / (2 * 3)) / (R(1) / 2) == ke_ratio16

dx2 = R('0.40') * R('0.75') / R('0.50');             assert dx2 == R('0.60')
dx2_inv = R('0.40') * R('0.50') / R('0.75');         assert eq(dx2_inv, 2, 0.27)
dx2_ke = R('0.40') * (R('0.75') / R('0.50'))**2;     assert dx2_ke == R('0.90')
distinct(dx2, dx2_inv, R('0.40'), dx2_ke)

px, py = R('1.2') * 5, R('1.6') * 5;                     assert (px, py) == (6, 8)
v22 = sp.sqrt(px**2 + py**2) / R('2.8');             assert eq(v22, 1, 3.6)
distinct(v22, (px + py) / R('2.8'), (py - px) / R('2.8'), sp.sqrt(px**2 + py**2))
assert (px + py) / R('2.8') == 5 and eq((py - px) / R('2.8'), 2, 0.71)

oA = R(1) * 9 / 3;                                    assert oA == 3
oB = R(3) * 5 / 6;                                    assert oB == R('2.5')
oC = (R('2.5') * 6 - R('2.5') * 2) / 5;              assert oC == 2
oD = R(4) * 2 / 5;                                    assert oD == R('1.6')
assert [oA, oB, oC, oD] == sorted([oA, oB, oC, oD], reverse=True)
assert (R('2.5') * 6 + R('2.5') * 2) / 5 == 4 > oA                 # the sign slip puts C first

v9 = R('0.80')                                         # identical gliders, elastic: they swap
assert KE(1, v9) == KE(1, 0) + KE(1, v9)

C, Q = [], []
card(C, 'A system',
     '**A system is the set of objects you choose to study together.**\n'
     '• The momentum of the system is the sum of the momenta of everything in '
     'it, signs included.\n'
     '• Choosing the system is the first step of every momentum problem.')
card(C, 'Closed system',
     '**A closed system neither gains nor loses mass.**\n'
     '• No objects join it and none leave it during the event.')
card(C, 'Internal and external forces',
     '**An internal force acts between two objects inside the system; an '
     'external force comes from something outside it.**\n'
     '• Two carts pushing on each other: internal.\n'
     '• Friction from the track, or a hand pushing one cart: external.')
card(C, 'Isolated system',
     '**An isolated system is a closed system with no net external force on '
     'it.**\n'
     '• Nothing on Earth is perfectly isolated, but small outside forces can '
     'often be ignored.')
card(C, 'The law of conservation of momentum',
     '**The total momentum of a closed, isolated system does not change.**\n'
     '• Total momentum before = total momentum after.\n'
     '• The objects’ momenta can each change; their total cannot.',
     eq='m₁v₁_i + m₂v₂_i = m₁v₁_f + m₂v₂_f')
card(C, 'Why: Newton’s third law',
     '**Colliding objects push on each other with equal and opposite forces '
     'for the same time, so they get equal and opposite impulses.**\n'
     '• So whatever momentum one gains, the other loses: Δp₁ = −Δp₂.\n'
     '• Your sheet prints this as Δp = −Δp; the two Δp’s belong to the two '
     'different objects.',
     eq='m₂Δv₂ = −m₁Δv₁')
card(C, 'Choosing the system decides what is conserved',
     '**Momentum is conserved only for a system that includes every object '
     'pushing on every other.**\n'
     '• A falling ball alone gains momentum, because Earth pulls it from '
     'outside.\n'
     '• Ball and Earth together form an isolated system: the ball’s downward '
     'momentum is matched by Earth’s tiny upward momentum.')
card(C, 'Short collisions',
     '**In a very short collision, outside forces such as friction or gravity '
     'have too little time to give much impulse, so momentum is very nearly '
     'conserved.**\n'
     '• The collision forces are huge but brief; the outside forces are small, '
     'and Ft for them is tiny.\n'
     '• That is why a crash on an ordinary road can be treated as isolated '
     'for the instant of the crash.')
card(C, 'Stick together: perfectly inelastic',
     '**When colliding objects stick together, the collision is perfectly '
     'inelastic, and they share one final velocity.**\n'
     '• Total momentum before = (m₁ + m₂) × v_f.\n'
     '• So v_f = total momentum ÷ total mass.',
     eq='m₁v₁_i + m₂v₂_i = (m₁ + m₂)v_f')
card(C, 'Elastic collisions',
     '**In a perfectly elastic collision, both the total momentum AND the total '
     'kinetic energy are conserved.**\n'
     '• Objects bounce apart with no energy lost to heat, sound or denting.\n'
     '• When a moving ball hits an identical ball at rest head-on and '
     'elastically, the first stops and the second moves off at the first '
     'one’s speed.')
card(C, 'Inelastic collisions lose kinetic energy',
     '**In an inelastic collision, momentum is still conserved but some '
     'kinetic energy is not.**\n'
     '• The lost kinetic energy becomes internal energy (heating), the '
     'energy of bending and denting, and sound.\n'
     '• It is not destroyed, and it never becomes extra momentum.')
card(C, 'Momentum always, kinetic energy sometimes',
     '**Total momentum is conserved in every collision of an isolated system; '
     'total kinetic energy only in an elastic one.**\n'
     '• So never solve a sticky collision by assuming kinetic energy stays '
     'the same.\n'
     '• To decide whether a collision was elastic, compare the total ½mv² '
     'before and after.',
     hint='Momentum: always. Kinetic energy: only if nothing dents.')
card(C, 'Explosions and recoil from rest',
     '**When a system at rest pushes itself apart, its total momentum stays '
     'zero, so the pieces leave with equal and opposite momenta.**\n'
     '• The backward motion is called recoil.\n'
     '• The lighter piece moves faster, by exactly the ratio of the masses.',
     eq='m_A v_A = −m_B v_B')
card(C, 'Rockets',
     '**A rocket moves forward because the gas it throws backward carries '
     'momentum backward.**\n'
     '• Rocket and gas form an isolated system with a fixed total, so the '
     'rocket gains forward momentum.\n'
     '• It does not push on the air or on space: it works best in a vacuum.')
card(C, 'Equal momenta, different masses',
     '**Two objects with momenta of the same size have speeds in the opposite '
     'ratio to their masses — and the lighter one has more kinetic '
     'energy.**\n'
     '• Twice the mass means half the speed.\n'
     '• Kinetic energy can be written p² ÷ 2m, so for the same p the smaller '
     'mass has the larger KE.', eq='KE = p² / 2m', frm='added')
card(C, 'Two dimensions',
     '**In two dimensions, momentum is conserved separately along each '
     'direction.**\n'
     '• Add the x-momenta, add the y-momenta, then combine them with '
     'Pythagoras.\n'
     '• Never add momenta at right angles as if they were in a line.')
card(C, 'The explosion lab: why the ratios should match',
     '**The total momentum starts at zero, so m₁v₁ = m₂v₂ in size, which makes '
     'm₁ ÷ m₂ = v₂ ÷ v₁.**\n'
     '• The carts reach the ends at the same time, so the distance each covers '
     'is in proportion to its speed.\n'
     '• So the speed ratio can be replaced by the distance ratio: '
     'm₁ ÷ m₂ = Δx₂ ÷ Δx₁. The heavier cart covers the shorter distance.',
     eq='m₁ / m₂ = Δx₂ / Δx₁', frm='added')
card(C, 'Why the times have to be equal',
     '**Only when both carts travel for the same time is distance a fair '
     'stand-in for speed.**\n'
     '• That is why the lab has you move the start point until the carts hit '
     'the ends together.\n'
     '• Friction slows both carts a little, so expect the two ratios to agree '
     'closely, not perfectly.', frm='added')
card(C, 'The spring is an internal force',
     '**The spring is part of the cart system: it pushes on both carts at '
     'once, equally and in opposite directions.**\n'
     '• Internal forces cannot change the total momentum.\n'
     '• That is exactly why the carts’ momenta come out equal and opposite.',
     frm='added')
card(C, 'Kinetic energy in the explosion',
     '**Kinetic energy was NOT conserved in the explosion lab: it was zero '
     'before the release and more than zero after.**\n'
     '• It came from the elastic potential energy stored in the compressed '
     'spring (PE = ½kx² on your sheet).\n'
     '• Kinetic energy has no direction, so the two carts’ amounts add — they '
     'cannot cancel the way momenta do.', frm='added')

q(Q, 1, 'What does the law of conservation of momentum say?',
  ['In a closed, isolated system, the total momentum stays the same',
   'In any collision, each object keeps the momentum it started with',
   'In any collision, the total kinetic energy stays the same',
   'Total momentum stays the same whatever outside forces act'],
  0, 'Is it about each object, or about the total?',
  ['The law is about a closed, isolated system.',
   'Inside it, objects can trade momentum with each other.',
   'What cannot change is the total.',
   'Total momentum before equals total momentum after.'],
  '**The TOTAL momentum of a closed, isolated system is constant.** Each '
  'object’s own momentum can change completely — that is the collision. '
  'Kinetic energy is conserved only in elastic collisions, and an outside '
  'force can change the total.',
  'Conserved means the total, not each piece.')

q(Q, 1, 'Which describes an isolated system?',
  ['No mass enters or leaves it, and the net external force on it is zero',
   'No forces of any kind act between the objects that are inside it',
   'All of its objects start at rest and stay at rest throughout',
   'It is far enough from Earth that gravity cannot reach any of it'],
  0, 'Closed, plus one more condition.',
  ['A closed system gains and loses no mass.',
   'An isolated system is closed AND has no net external force.',
   'Forces inside the system are allowed — that is what a collision is.',
   'So: no mass in or out, and zero net external force.'],
  '**Closed (no mass in or out) and no net external force.** Internal forces '
  'can be as big as you like; it is outside forces that would change the total '
  'momentum.',
  'Inside forces are fine. Outside forces are the problem.')

q(Q, 1, 'In a perfectly elastic collision of an isolated system, what is '
        'conserved?',
  ['Both the total momentum and the total kinetic energy',
   'The total momentum, but not the total kinetic energy',
   'The total kinetic energy, but not the total momentum',
   'The velocity of each object, before and after'],
  0, '“Elastic” adds something to what is always conserved.',
  ['Total momentum is conserved in every collision of an isolated system.',
   'An elastic collision also loses no kinetic energy.',
   'Each object’s velocity still changes.',
   'Both total momentum and total kinetic energy are conserved.'],
  '**Momentum is conserved in every collision; elastic means kinetic energy is '
  'conserved too.** Momentum without kinetic energy describes an inelastic '
  'collision. Kinetic energy without momentum never happens in an isolated '
  'system.',
  'Elastic = momentum AND kinetic energy.')

q(Q, 2, 'Taking east as positive: a 1.2 kg cart moving east at 5.0 m/s hits a '
        '1.8 kg cart at rest, and they stick together. What is their velocity '
        'afterward?',
  ['2.0 m/s east', '3.3 m/s east', '5.0 m/s east', '2.5 m/s east'],
  0, 'Total momentum before = (total mass) × shared velocity.',
  ['Momentum before: 1.2 × 5.0 + 1.8 × 0 = 6.0 kg·m/s.',
   'After, the carts move together with mass 1.2 + 1.8 = 3.0 kg.',
   'v_f = 6.0 ÷ 3.0 = 2.0 m/s.',
   'They move off at 2.0 m/s east.'],
  '**6.0 kg·m/s shared by 3.0 kg gives 2.0 m/s east.** 3.3 m/s divides by the '
  'second cart’s mass alone; 5.0 m/s forgets the extra mass has to be carried; '
  '2.5 m/s averages the two velocities, which only works for equal masses.',
  'Stuck together: divide by BOTH masses.')

q(Q, 2, 'Taking east as positive: a 0.90 kg cart moving east at 6.0 m/s meets '
        'a 1.5 kg cart moving west at 2.0 m/s head-on, and they stick. What is '
        'their velocity afterward?',
  ['1.0 m/s east', '3.5 m/s east', '1.0 m/s west', '2.0 m/s east'],
  0, 'The westward cart’s momentum is negative.',
  ['East cart: 0.90 × (+6.0) = +5.4 kg·m/s.',
   'West cart: 1.5 × (−2.0) = −3.0 kg·m/s.',
   'Total: +2.4 kg·m/s, shared by 0.90 + 1.5 = 2.4 kg.',
   'v_f = 2.4 ÷ 2.4 = +1.0 m/s, so 1.0 m/s east.'],
  '**(+5.4) + (−3.0) = +2.4 kg·m/s over 2.4 kg: 1.0 m/s east.** 3.5 m/s adds '
  'the two momenta as if both carts were going east — the sign that marks '
  'head-on was dropped. 2.0 m/s averages the velocities; west has the wrong '
  'direction for a positive total.',
  'Head-on means opposite signs. Write them before adding.')

q(Q, 2, 'Taking east as positive: a 2.4 kg cart moving east at 4.0 m/s hits a '
        '1.6 kg cart at rest. Afterward the 2.4 kg cart moves east at 1.0 m/s. '
        'What is the 1.6 kg cart’s velocity?',
  ['4.5 m/s east', '3.0 m/s east', '6.0 m/s east', '7.5 m/s east'],
  0, 'Total momentum before = total momentum after, with both carts moving after.',
  ['Before: 2.4 × 4.0 + 1.6 × 0 = 9.6 kg·m/s.',
   'After: 2.4 × 1.0 + 1.6 v = 2.4 + 1.6 v.',
   '9.6 = 2.4 + 1.6 v, so 1.6 v = 7.2.',
   'v = 4.5 m/s east.'],
  '**9.6 = 2.4 + 1.6v gives v = 4.5 m/s east.** 3.0 m/s passes the first '
  'cart’s lost SPEED across, ignoring the different masses; 6.0 m/s forgets '
  'the first cart still has momentum; 7.5 m/s adds that momentum instead of '
  'taking it away.',
  'Momentum moves between objects; speed does not.')

q(Q, 2, 'Taking east as positive: a 48 kg skater stands still on smooth ice and '
        'throws a 2.4 kg ball east at 12 m/s. What is the skater’s velocity '
        'just afterward?',
  ['0.60 m/s west', '0.60 m/s east', '12 m/s west', '240 m/s west'],
  0, 'They start at rest, so the total momentum stays zero.',
  ['Total momentum before: 0.',
   'Ball after: 2.4 × (+12) = +28.8 kg·m/s.',
   'The skater must carry −28.8 kg·m/s, so v = −28.8 ÷ 48.',
   'v = −0.60 m/s, so 0.60 m/s west.'],
  '**The skater’s momentum must cancel the ball’s: −28.8 ÷ 48 = −0.60 m/s, '
  '0.60 m/s west.** East is the ball’s direction, not the recoil’s; 12 m/s '
  'gives the skater the ball’s speed instead of its momentum; 240 m/s puts the '
  'masses upside down.',
  'From rest: equal and opposite momenta, never equal speeds.')

q(Q, 2, 'Taking east as positive: a 1.5 kg object at rest bursts into two '
        'pieces. The 0.60 kg piece flies east at 9.0 m/s. What is the 0.90 kg '
        'piece’s velocity?',
  ['6.0 m/s west', '9.0 m/s west', '13.5 m/s west', '6.0 m/s east'],
  0, 'From rest, the two momenta must add to zero.',
  ['Total before: 0.',
   'Light piece: 0.60 × (+9.0) = +5.4 kg·m/s.',
   'Heavy piece needs −5.4 kg·m/s: v = −5.4 ÷ 0.90.',
   'v = −6.0 m/s, so 6.0 m/s west.'],
  '**0.60 × 9.0 = 5.4 kg·m/s, so the 0.90 kg piece carries 5.4 west: '
  '6.0 m/s west.** 9.0 m/s gives both pieces the same speed; 13.5 m/s inverts '
  'the mass ratio, making the heavier piece faster; east ignores the cancelling.',
  'The heavier piece is the slower one. Check your answer obeys that.')

q(Q, 3, 'Taking east as positive: a 3.0 kg object moving east at 2.0 m/s splits '
        'into two pieces. The 1.0 kg piece flies east at 9.0 m/s. What is the '
        '2.0 kg piece’s velocity?',
  ['1.5 m/s west', '1.5 m/s east', '4.5 m/s west', '7.5 m/s east'],
  0, 'The total is not zero this time: it started moving.',
  ['Total before: 3.0 × (+2.0) = +6.0 kg·m/s.',
   'After: 1.0 × 9.0 + 2.0 v = 9.0 + 2.0 v.',
   '6.0 = 9.0 + 2.0 v, so 2.0 v = −3.0.',
   'v = −1.5 m/s, so 1.5 m/s west.'],
  '**6.0 = 9.0 + 2.0v gives v = −1.5 m/s: 1.5 m/s west.** The fast piece '
  'carries more momentum than the whole object had, so the other piece must '
  'go backward. 4.5 m/s west treats it as if it started at rest; 7.5 m/s east '
  'adds the fast piece’s momentum instead of subtracting it.',
  'Before an explosion is not always zero. Check what it started with.')

q(Q, 2, 'Two identical gliders sit on a frictionless air track. One moves at '
        '0.80 m/s into the other, which is at rest, in a head-on, perfectly '
        'elastic collision. The first glider stops. How fast does the second '
        'move off?',
  ['0.80 m/s', '0.40 m/s', '1.6 m/s', '0 m/s'],
  0, 'Equal masses, one stops: where did its momentum go?',
  ['Before, the total momentum is m × 0.80.',
   'After, the first glider has none, so the second has all of it.',
   'Same mass, same momentum: same speed.',
   'The second glider moves at 0.80 m/s.'],
  '**All of the momentum passes to an identical glider, so it leaves at '
  '0.80 m/s** — and its kinetic energy matches too, as an elastic collision '
  'needs. 0.40 m/s is what they would share if they stuck together; 1.6 m/s '
  'creates momentum; 0 m/s destroys it.',
  'Identical, elastic, head-on: they swap velocities.')

q(Q, 3, 'A 0.80 kg cart moving at 6.0 m/s hits a 1.6 kg cart at rest, and they '
        'stick together. How much kinetic energy is lost in the collision?',
  ['9.6 J', '0 J', '14.4 J', '4.8 J'],
  0, 'Use momentum to find the speed after, then compare ½mv² before and after.',
  ['Momentum: 0.80 × 6.0 = 4.8 kg·m/s, so v_f = 4.8 ÷ 2.4 = 2.0 m/s.',
   'KE before: ½ × 0.80 × 6.0² = 14.4 J.',
   'KE after: ½ × 2.4 × 2.0² = 4.8 J.',
   'Lost: 14.4 − 4.8 = 9.6 J.'],
  '**14.4 J before, 4.8 J after: 9.6 J lost.** 0 J assumes kinetic energy is '
  'conserved, which never happens when objects stick. 14.4 J says all of it '
  'went, but the carts are still moving; 4.8 J is what is LEFT, not what was '
  'lost.',
  'Momentum gives you v_f. Kinetic energy is a separate check.')

q(Q, 2, 'A lump of putty hits a cart and sticks to it. Momentum is conserved, '
        'but some kinetic energy disappears. Where does it go?',
  ['Into heating, the putty’s squashing, and the sound of the hit',
   'Into extra momentum that the putty and the cart carry away',
   'Nowhere: it is destroyed at the very instant the two touch',
   'Into gravitational potential energy stored up in the cart'],
  0, 'Energy is never destroyed. What happens to the putty?',
  ['Energy is never destroyed, only changed into other forms.',
   'The putty deforms and warms up, and the hit makes a sound.',
   'Momentum and energy are different quantities: one cannot become the other.',
   'The lost kinetic energy becomes internal energy, deformation and sound.'],
  '**It becomes internal (thermal) energy, the energy of squashing the putty, '
  'and sound.** Energy cannot turn into momentum — they are different '
  'quantities, measured in different units — and nothing about a level cart '
  'stores gravitational energy.',
  'Lost kinetic energy is changed, not destroyed.')

q(Q, 2, 'A rocket in deep space, far from any planet, fires its engine and '
        'speeds up. What explains its forward motion?',
  ['The exhaust gas carries momentum backward, so the rocket gains it forward',
   'The exhaust gas pushes against the empty space behind the rocket',
   'The engine creates new momentum, since nothing is out there to push on',
   'Newton’s third law does not apply in space, so the engine just pushes'],
  0, 'Rocket and gas together are an isolated system.',
  ['Treat the rocket and its fuel as one isolated system.',
   'The engine pushes gas backward; the gas pushes the rocket forward.',
   'The total momentum stays the same.',
   'So the gas’s backward momentum is matched by the rocket’s forward gain.'],
  '**The gas and the rocket push on each other: backward momentum for the gas, '
  'forward momentum for the rocket, total unchanged.** There is nothing in '
  'space to push against, and nothing needs to be. Momentum is never created, '
  'and the third law holds everywhere.',
  'A rocket pushes on its own exhaust, not on anything outside.')

q(Q, 2, 'Two cars collide on a dry road, where friction acts on their tires. '
        'Why can conservation of momentum still be used for the instant of '
        'the crash?',
  ['The crash is so brief that friction’s impulse is tiny next to the crash’s',
   'Friction stops acting on the tires during the instant of a crash',
   'Internal forces are always bigger than every external force there is',
   'Momentum is conserved in every system, whatever acts on it from outside'],
  0, 'Impulse is force times time. How much time does friction get?',
  ['Friction is an external force, so it does change the total momentum.',
   'But impulse is Ft, and the crash lasts only a fraction of a second.',
   'The crash forces are enormous; friction is small and gets very little time.',
   'So friction’s impulse is negligible during the crash itself.'],
  '**Friction is still there, but in so short a time its impulse is tiny '
  'beside the huge crash forces**, so momentum is very nearly conserved just '
  'before and just after. Over a longer time — the skid afterward — friction '
  'does bring the wreck to a stop.',
  'Short collision: outside impulses are negligible, not absent.')

q(Q, 3, 'A 36 kg skater and a 54 kg skater stand still on smooth ice and push '
        'off from each other. Which is true just afterward?',
  ['Their momenta are equal in size; the 36 kg skater is 1.5 times as fast',
   'They move apart at equal speeds, heading in opposite directions',
   'The 54 kg skater has more momentum, because it has the more mass',
   'The 36 kg skater pushed harder, so it is the one moving faster'],
  0, 'Total momentum before the push was zero.',
  ['The total starts at zero, so it stays zero.',
   'So their momenta are equal in size and opposite in direction.',
   'Equal mv with masses 36 and 54 means speeds in the ratio 54 ÷ 36.',
   '54 ÷ 36 = 1.5: the lighter skater is 1.5 times as fast.'],
  '**Equal and opposite momenta, so the 36 kg skater moves 54 ÷ 36 = 1.5 times '
  'as fast.** By the third law each pushed the other equally hard; the lighter '
  'one is faster only because the same momentum needs more speed on less mass.',
  'Same momentum: speeds go the opposite way to masses.')

q(Q, 3, 'Object X has three times the mass of object Y, and their momenta are '
        'the same size. How do their kinetic energies compare?',
  ['X has one-third the kinetic energy of Y', 'X has three times the kinetic energy of Y',
   'X and Y have the same kinetic energy', 'X has nine times the kinetic energy of Y'],
  0, 'Same momentum, three times the mass: what is X’s speed?',
  ['Same momentum with three times the mass means X has one-third the speed.',
   'KE = ½mv²: X has 3 times the mass but (⅓)² = ⅑ of the v².',
   '3 × ⅑ = ⅓.',
   'X has one-third the kinetic energy of Y.'],
  '**X: 3 × the mass, ⅓ of the speed, so 3 × ⅑ = ⅓ of the kinetic energy.** '
  'Writing KE = p² ÷ 2m shows it directly: the same p over three times the '
  'mass. Equal momenta do not mean equal energies.',
  'For the same momentum, the lighter object carries more energy.', frm='added')

q(Q, 3, 'Taking east and north as positive: a 1.2 kg puck slides east at '
        '5.0 m/s and a 1.6 kg puck slides north at 5.0 m/s. They collide and '
        'stick. How fast is the pair moving afterward?',
  ['3.6 m/s', '5.0 m/s', '0.71 m/s', '10 m/s'],
  0, 'Keep the east and north momenta separate, then combine.',
  ['East momentum: 1.2 × 5.0 = 6.0 kg·m/s. North momentum: 1.6 × 5.0 = 8.0 kg·m/s.',
   'Total momentum: √(6.0² + 8.0²) = 10 kg·m/s.',
   'Shared by 1.2 + 1.6 = 2.8 kg.',
   'v = 10 ÷ 2.8 ≈ 3.6 m/s.'],
  '**√(6.0² + 8.0²) = 10 kg·m/s, shared by 2.8 kg: about 3.6 m/s.** 5.0 m/s '
  'adds momenta at right angles as if they were in a line; 0.71 m/s subtracts '
  'them; 10 m/s forgets to divide the momentum by the mass.',
  'Right angles: Pythagoras on the momenta, then divide by the mass.')

q(Q, 2, 'In a spring-cart explosion lab, two carts at rest are pushed apart by '
        'a spring and reach the two ends of the track at the same moment. Why '
        'should m₁ ÷ m₂ equal Δx₂ ÷ Δx₁?',
  ['Total momentum stays zero, so m₁v₁ = m₂v₂; equal times make distance track speed',
   'The spring pushes the heavier cart harder, so it covers the longer distance',
   'Kinetic energy is conserved, so the two carts must leave at equal speeds',
   'The spring gives both carts the same speed, so their distances match'],
  0, 'What starts at zero, and how are distance and speed linked here?',
  ['Before release, the total momentum is zero, so it stays zero.',
   'So the two momenta are equal in size: m₁v₁ = m₂v₂, giving m₁ ÷ m₂ = v₂ ÷ v₁.',
   'Both carts travel for the same time, so each distance is in proportion to its speed.',
   'So m₁ ÷ m₂ = Δx₂ ÷ Δx₁.'],
  '**Zero total momentum makes m₁v₁ = m₂v₂, and equal travel times let '
  'distance stand in for speed.** The spring pushes both carts equally hard (third '
  'law), kinetic energy is NOT conserved here, and equal speeds would only '
  'happen with equal masses.',
  'This is why the lab makes you adjust the start until the carts arrive together.',
  frm='added')

q(Q, 2, 'In a spring-cart explosion, a 0.75 kg cart and a 0.50 kg cart start at '
        'rest and reach the track’s ends at the same moment. The 0.75 kg cart '
        'travels 0.40 m. How far does the 0.50 kg cart travel?',
  ['0.60 m', '0.27 m', '0.40 m', '0.90 m'],
  0, 'm₁ ÷ m₂ = Δx₂ ÷ Δx₁. The lighter cart goes farther.',
  ['m₁ ÷ m₂ = 0.75 ÷ 0.50 = 1.5.',
   'So Δx₂ ÷ Δx₁ = 1.5.',
   'Δx₂ = 1.5 × 0.40 m = 0.60 m.',
   'The 0.50 kg cart travels 0.60 m.'],
  '**The mass ratio 1.5 becomes the distance ratio: 1.5 × 0.40 = 0.60 m.** '
  '0.27 m inverts the ratio, sending the lighter cart a shorter way; 0.40 m '
  'assumes equal speeds; 0.90 m squares the ratio, which is what equal kinetic '
  'energies would give.',
  'Lighter cart, longer trip — by the mass ratio, not its square.', frm='added')

q(Q, 2, 'In a spring-cart explosion lab, why is the spring NOT counted as an '
        'external force?',
  ['It is part of the cart system, pushing both carts equally and oppositely',
   'It is too weak to count as a force compared with the carts’ weight',
   'It acts for too short a time to give either cart an impulse',
   'It pushes on only one of the carts, so it does not count'],
  0, 'External means from outside the system. Where is the spring?',
  ['The system is the two carts together, spring included.',
   'The spring pushes on both carts at the same time.',
   'By the third law, those pushes are equal and opposite.',
   'So it is an internal force and cannot change the total momentum.'],
  '**The spring is inside the system and pushes both carts at once, equally '
  'and oppositely — an internal force.** It is far from too weak: it is what '
  'sets the carts moving. It gives each cart a real impulse; the two impulses '
  'just cancel in the total.',
  'Internal forces move the pieces but never the total.', frm='added')

q(Q, 3, 'In a spring-cart explosion, momentum is conserved. Is kinetic energy '
        'conserved too?',
  ['No: it was zero before release and is not zero after; the spring supplied it',
   'Yes: momentum was conserved, so kinetic energy must be conserved as well',
   'Yes: the total is still zero, because the carts move in opposite directions',
   'No: some of it was lost to friction, so the total went down'],
  0, 'Can kinetic energy be negative?',
  ['Before release, neither cart moves, so the total kinetic energy is zero.',
   'After release, both carts move, and each ½mv² is positive.',
   'Kinetic energy has no direction, so the two amounts add rather than cancel.',
   'So it was not conserved: it came from the energy stored in the squeezed spring.'],
  '**Kinetic energy went from zero to something, so it was not conserved; it '
  'came from the spring’s stored elastic energy.** “The total is still zero” '
  'is the trap: momenta cancel because they have directions, but kinetic energy '
  'never does. Friction did take a little afterward, but the total went UP '
  'at release, not down.',
  'Momentum can cancel. Kinetic energy only ever adds.', frm='added')

q(Q, 3, 'Each collision ends with the two carts stuck together. Rank them from '
        'FASTEST to SLOWEST final speed.',
  ['A: 1.0 kg cart at 9.0 m/s hits a 2.0 kg cart at rest',
   'B: 3.0 kg cart at 5.0 m/s hits a 3.0 kg cart at rest',
   'C: 2.5 kg cart at 6.0 m/s hits a 2.5 kg cart coming toward it at 2.0 m/s',
   'D: 4.0 kg cart at 2.0 m/s hits a 1.0 kg cart at rest'],
  0, 'Total momentum ÷ total mass, with signs for the head-on one.',
  ['A: 9.0 ÷ 3.0 = 3.0 m/s.',
   'B: 15 ÷ 6.0 = 2.5 m/s.',
   'C: (15 − 5.0) ÷ 5.0 = 2.0 m/s, because the carts move toward each other.',
   'D: 8.0 ÷ 5.0 = 1.6 m/s. So A, B, C, D.'],
  '**A (3.0), B (2.5), C (2.0), D (1.6) m/s.** C is the trap: forgetting that '
  'the second cart is coming the other way gives (15 + 5.0) ÷ 5.0 = 4.0 m/s and '
  'puts it first.',
  'Head-on collisions subtract momenta.',
  kind='order')

fresh(Q)
build('ad-astra', C, Q, 'unit-phys-dyn1-momentum',
      'Dynamics 1 · 1-7 Conservation of Momentum', 'physics',
      'Why the total momentum of a closed, isolated system never changes — '
      'Newton’s third law gives colliding objects equal and opposite impulses '
      '— and how to use it: carts that stick together, carts that bounce apart, '
      'explosions and recoil from rest, rockets, and collisions at right '
      'angles. Elastic collisions keep kinetic energy as well; inelastic ones '
      'lose some of it to heating, denting and sound. It finishes with the '
      'reasoning behind the spring-cart explosion lab.',
      'Conservation of momentum lets you link before and after without knowing '
      'anything about the forces in between — which is why it works for car '
      'crashes, explosions and rockets, where those forces are far too fast '
      'and messy to measure.',
      [('Relate Newton’s third law of motion to conservation of momentum in '
        'collisions and explosions.', 'source'),
       ('Recognize the conditions under which the momentum of a system is '
        'conserved.', 'source'),
       ('Apply conservation of momentum to explain the propulsion of rockets.', 'source'),
       ('Distinguish momentum conservation from kinetic energy conservation in '
        'elastic and inelastic collisions.', 'source'),
       ('Solve conservation of momentum problems in two dimensions by using '
        'vector analysis.', 'source'),
       ('Explain why the mass ratio should equal the distance ratio in the '
        'spring-cart explosion lab, and why kinetic energy is not conserved '
        'there.', 'added')],
      'From chapter 9.2 (The Conservation of Momentum) of 09_Momentum.pdf, the '
      'Conservation of Momentum homework, and the explosion lab, all in the '
      'Dynamics 1 folder. The homework and the lab were read for what they '
      'ask; nothing of hers was marked or recorded. The lab has no data yet, '
      'so it is taught as reasoning only — why m₁/m₂ should equal Δx₂/Δx₁ '
      '(zero total momentum, plus equal travel times making distance stand in '
      'for speed), why the spring is an internal force, and why kinetic energy '
      'was not conserved (it came from the spring); none of her results are '
      'invented. The chapter does not cover elastic and inelastic collisions; '
      'those cards follow the homework’s own framing. Every number was '
      'computed with sympy and checked, and none of the textbook’s or the '
      'homework’s numbers is reused. Traps with deliberate airtime: dropping '
      'the sign in a head-on collision, dividing by only one mass when carts '
      'stick, giving recoiling objects equal speeds, assuming kinetic energy '
      'is conserved in a sticky collision, adding kinetic energies as if they '
      'could cancel, and adding momenta at right angles as if in a line. '
      'Things in the sources worth knowing: her sheet prints “Δp = −Δp” with '
      'no labels, which taken literally only says Δp = 0 — it means one '
      'object’s Δp is minus the other’s (m₂Δv₂ = −m₁Δv₁ on the next line). On '
      'the homework, item 32 works out to 0 J of kinetic energy lost and item '
      '33 to 8.0 m/s, and neither answer is among the four choices; items 26, '
      '30 and 33 also end with MORE kinetic energy than they started with, '
      'which an ordinary collision cannot do — the momentum arithmetic is '
      'fine, the situations are not physical. The homework says to use '
      'g = 10 m/s², though no item needs g. The lab compares distances, which '
      'only works because the carts travel for equal times, and friction '
      'slows them a little, so the two ratios should agree closely rather '
      'than exactly.',
      ('Read the cards up to the explosion lab, then take the quiz. Before '
       'every calculation, say which way is positive and add up the momentum '
       'before the event.', 30),
      'content/phys-dyn1-momentum.json',
      'Chapter 9, Momentum and Its Conservation (9.2 The Conservation of Momentum)',
      SRC9 + '; ' + SRCHW + '; ' + SRCLAB, offset_hours=3, libv_=1)
patch('content/phys-dyn1-momentum.json', 'unit-phys-dyn1-momentum', quarter=2,
      sorts=[{
  'id': 's-ke', 'title': 'Kinetic energy kept, or some lost?',
  'a': 'Elastic', 'b': 'Inelastic',
  'items': [
    {'t': 'Two steel ball bearings click together and bounce apart', 'k': 'a',
     'why': 'Hard steel barely dents, so almost no kinetic energy turns into heat or sound.'},
    {'t': 'Gas molecules bouncing off each other inside a sealed jar', 'k': 'a',
     'why': 'Molecule collisions lose no kinetic energy overall — the gas would cool down if they did.'},
    {'t': 'Two air-track gliders with magnets that repel before they touch', 'k': 'a',
     'why': 'The magnets push them apart without contact, so nothing deforms and the kinetic energy comes back.'},
    {'t': 'A moving billiard ball stops dead and the ball it hit rolls off at its speed', 'k': 'a',
     'why': 'Equal masses swapping velocities keeps both momentum and kinetic energy.'},
    {'t': 'Two gliders with springy bumpers bounce apart on an air track', 'k': 'a',
     'why': 'The bumpers squeeze and spring back, returning the energy.'},
    {'t': 'A superball dropped on a hard floor rebounds almost to the height it fell from', 'k': 'a',
     'why': 'Almost all of its kinetic energy comes back, so it is very nearly perfectly springy.'},
    {'t': 'A lump of clay hits a cart and sticks to it', 'k': 'b',
     'why': 'Objects that stick always lose kinetic energy, here to squashing the clay and heating it.'},
    {'t': 'Two carts with Velcro ends collide and move off together', 'k': 'b',
     'why': 'Sticking together is the perfectly inelastic case: the most kinetic energy that momentum allows is lost.'},
    {'t': 'A car crumples its bumper in a crash', 'k': 'b',
     'why': 'Bending metal and the bang of the crash take kinetic energy away.'},
    {'t': 'A dart thuds into a foam target and stays there', 'k': 'b',
     'why': 'It sticks, so it and the target share one velocity and kinetic energy is lost.'},
    {'t': 'A football player tackles another and they fall together', 'k': 'b',
     'why': 'They move off as one, so kinetic energy is lost to their bodies and the ground.'},
    {'t': 'An egg dropped on the floor splatters', 'k': 'b',
     'why': 'None of it bounces back; the kinetic energy goes into breaking and splashing.'},
  ]}])
