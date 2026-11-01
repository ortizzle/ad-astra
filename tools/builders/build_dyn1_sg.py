# -*- coding: utf-8 -*-
# Dynamics 1 · Test Study Guide: Newton’s Laws and Momentum.
# Built from three files uploaded to Drive › Physics 8 › Dynamics 1 on
# 2026-11-01:
#   N1L_N3L_COM+Study+Guide.pdf     the teacher's list of mandatory objectives
#                                   for the test (N1L, N3L, conservation of
#                                   momentum). This is the unit's SOURCE.
#   Newtons_First_Third_Laws_30_Question_Quiz.pdf
#                                   a 30-item multiple-choice "assessment" with
#                                   no key. Read ONLY to calibrate style and
#                                   difficulty. Not transcribed: it may be a
#                                   quiz she has not sat yet.
#   0631_001.pdf                    a 40-item Conservation of Momentum practice
#                                   with a key and handwritten working. Read for
#                                   what it ASKS only; no mark, letter or
#                                   working of hers is recorded anywhere.
#
# Scope was settled against the seven shipped Dynamics 1 parts first (1-1 to
# 1-7). This unit is the TEST REVIEW: one card per objective cluster on the
# guide, and fresh questions across every cluster. It re-teaches nothing in
# the same way: no incline, no friction coefficient, no impulse graph, no
# elastic/inelastic kinetic energy (the guide lists none of them).
#
# EVERY number is computed below and asserted before it reaches a question,
# including that no distractor is also correct. g = 9.8 m/s², as her quiz
# says (the momentum practice says 10; the cards name both).
# FORBID and QUIZ_PAIRS / HW_PAIRS keep the quiz's and the practice's own
# numbers out of every stem and option.
import sys, os, json, io, re, math
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

G = Fr(98, 10)
def F(x): return Fr(str(x))
def r(x, n=1): return round(float(x), n)
def distinct(*xs):
    a = xs[0]
    for x in xs[1:]:
        assert abs(float(x) - float(a)) > 1e-6, (a, x)
def S(d): return math.sin(math.radians(d))
def Co(d): return math.cos(math.radians(d))

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = 'content/phys-dyn1-sg.json'
UID = 'unit-phys-dyn1-sg'
SRC_SG = 'N1L_N3L_COM+Study+Guide.pdf (Drive, Physics 8 › Dynamics 1)'
SRC_QZ = 'Newtons_First_Third_Laws_30_Question_Quiz.pdf'
SRC_HW = '0631_001.pdf (Conservation of Momentum practice)'

# --- the sources' own numbers, kept out of every graded stem and option -----
# The quiz's distinctive figures (anchored so 0.75 kg never matches 75 kg).
FORBID = re.compile(
    r'(?<![\d.])(12 kg|45 N(?![/·])|75 kg|20 kg|60 N(?![/·])|5\.0 kg|70 kg|140 N|'
    r'15 kg|25 kg|80 N(?![/·])|50 kg|100 N(?![/·])|120 N(?![/·])|10 kg|35 N(?![/·])|'
    r'40 kg|60 kg|30 kg|6\.0 kg|12 N(?![/·])|1000 kg|2000 kg|6000 N|0\.25(?! kg)|'
    r'25°|30°|73\.5|117\.6|735|588|266|156\.8|39\.2|86\.6)')
# The practice's (mass, speed) pairings, the same list 1-7's builder guards.
HW_PAIRS = [('2.0', '5.0'), ('3.0', '4.0'), ('2.0', '6.0'), ('1.0', '8.0'),
            ('0.20', '15'), ('0.50', '10'), ('1.5', '4.0'), ('4.0', '3.0'),
            ('3.0', '10'), ('0.10', '20'), ('1.0', '6.0'), ('2.0', '4.0'),
            ('0.40', '5.0'), ('2.0', '3.0'), ('1.0', '12'), ('0.20', '10'),
            ('0.50', '8.0'), ('60', '10'), ('0.50', '6.0')]
def fresh(Q):
    for x in Q:
        texts = ([x['q']] + x['opts']) if x.get('kind') == 'order' else [' '.join([x['q']] + x['opts'])]
        for t in texts:
            assert not FORBID.search(t), (x['id'], FORBID.search(t).group(0))
            for s in re.split(r'(?<=[.?;:])\s', t):
                for m, v in HW_PAIRS:
                    pat = r'(?<![\d.])%s kg\b[^.?;]*?(?<![\d.])%s m/s' % (re.escape(m), re.escape(v))
                    assert not re.search(pat, s), (x['id'], m, v, s)

# =============================================================================
# NUMBERS
# =============================================================================
# Hooke: k = 160 N/m, stretched 4.5 cm
hk = 160 * F('0.045');                 assert hk == F('7.2')
hk_cm = 160 * F('4.5');                assert hk_cm == 720              # cm left in
hk_div = F(160) / F('0.045');          assert r(hk_div, 0) == 3556      # k ÷ x
hk_divcm = F(160) / F('4.5');          assert r(hk_divcm, 0) == 36      # k ÷ x in cm
distinct(hk, hk_cm, hk_div, hk_divcm)

# k from a graph: force (N) against extension in CENTIMETRES, point (16 cm, 5.6 N)
gk = F('5.6') / F('0.16');             assert gk == 35
gk_cm = F('5.6') / 16;                 assert gk_cm == F('0.35')        # cm left in
gk_inv = F('0.16') / F('5.6');         assert r(gk_inv, 3) == 0.029     # run over rise
gk_invcm = F(16) / F('5.6');           assert r(gk_invcm, 1) == 2.9
distinct(gk, gk_cm, gk_inv, gk_invcm)
assert F('0.35') * 20 == 7                                               # line stays in the window

# Mars rover: weight 1110 N where g = 3.7 m/s² → mass, which is the same on Earth
m_rov = F(1110) / F('3.7');            assert m_rov == 300
m_rov_e = F(1110) / G;                 assert r(m_rov_e, 0) == 113      # divided by Earth's g
m_rov_x = F(1110) * F('3.7');          assert r(m_rov_x, 0) == 4107
distinct(m_rov, m_rov_e, m_rov_x, 1110)

# Normal force: 36 kg trunk, pulled straight up with 150 N, stays on the floor
W_tr = 36 * G;                         assert W_tr == F('352.8')
N_tr = W_tr - 150;                     assert r(N_tr, 0) == 203
N_add = W_tr + 150;                    assert r(N_add, 0) == 503
distinct(N_tr, W_tr, N_add, 150)
assert N_tr > 0                                                          # it really does stay down

# Tension, parallel forces: 3.5 kg pot on cord A, 2.5 kg pot hanging below it on cord B
T_A = (F('3.5') + F('2.5')) * G;       assert T_A == F('58.8')
T_top = F('3.5') * G;                  assert T_top == F('34.3')
T_B = F('2.5') * G;                    assert T_B == F('24.5')
distinct(T_A, T_top, T_B, 6)

# Tension at an angle: 210 N banner, two ropes each 40° above the horizontal
T_ban = 210 / (2 * S(40));             assert r(T_ban, 0) == 163
T_cos = 210 / (2 * Co(40));            assert r(T_cos, 0) == 137
distinct(T_ban, T_cos, 105, 210)
assert abs(2 * T_ban * S(40) - 210) < 1e-9                              # verticals hold the weight
assert abs(T_ban * Co(40) - T_ban * Co(40)) < 1e-12                     # horizontals cancel by symmetry

# Free-body diagram: weight 260 N, normal 260 N, pull 95 N east, friction 70 N west
fb_net = 95 - 70;                      assert fb_net == 25
fb_add = 95 + 70;                      assert fb_add == 165
distinct(fb_net, fb_add, 0)

# Net force on one axis: 130 N east, 85 N west, 30 N west
nf = 130 - 85 - 30;                    assert nf == 15
nf_all = 130 + 85 + 30;                assert nf_all == 245
nf_one = 130 - 85 + 30;                assert nf_one == 75
distinct(nf, nf_all, nf_one, -nf)

# Inertia: 1500 kg car, 6000 kg truck
inr = F(6000) / 1500;                  assert inr == 4

# Third law: bus 3000 kg, bug 0.0020 kg, 1.5 N
a_bug = F('1.5') / F('0.0020');        assert a_bug == 750
a_bus = F('1.5') / 3000;               assert a_bus == F('0.0005')

# 2-D equilibrium: 36 N east, 15 N north, 39 N at 22.6° south of west
ang3 = math.degrees(math.atan2(15, 36)); assert r(ang3, 1) == 22.6
assert abs(39 * Co(ang3) - 36) < 1e-9 and abs(39 * S(ang3) - 15) < 1e-9
assert 36 + 15 != 39                                                     # magnitudes do not add

# Components: 160 N at 35° above the horizontal
cx = 160 * Co(35);                     assert r(cx, 0) == 131
cy = 160 * S(35);                      assert r(cy, 0) == 92
cdiv = 160 / Co(35);                   assert r(cdiv, 0) == 195
distinct(cx, cy, cdiv, 160)

# Resultant: 20 N east, 21 N north
res = math.hypot(20, 21);              assert res == 29
distinct(res, 41, 1, 841)

# Angle: 16 N east, 30 N north
res2 = math.hypot(16, 30);             assert res2 == 34
th = math.degrees(math.atan2(30, 16)); assert r(th, 1) == 61.9
th_flip = math.degrees(math.atan2(16, 30)); assert r(th_flip, 1) == 28.1
th_rad = math.atan(30 / 16);           assert r(th_rad, 1) == 1.1        # radian mode
assert r(th + th_flip, 6) == 90

# Total momentum: 0.35 kg east 2.4 m/s, 0.50 kg west 1.2 m/s (east +)
pt = F('0.35') * F('2.4') + F('0.50') * F('-1.2'); assert pt == F('0.24')
pt_abs = F('0.35') * F('2.4') + F('0.50') * F('1.2'); assert pt_abs == F('1.44')
distinct(pt, -pt, pt_abs, 0)

# Δp: 1.8 kg cart east at 4.5 → east at 1.5 (east +)
dp = F('1.8') * (F('1.5') - F('4.5')); assert dp == F('-5.4')
dp_add = -F('1.8') * (F('1.5') + F('4.5')); assert dp_add == F('-10.8')
dp_f = F('1.8') * F('1.5');             assert dp_f == F('2.7')
distinct(dp, -dp, dp_add, dp_f)

# Conservation: 2.5 kg east 2.0 hits 1.5 kg at rest; after, 2.5 kg east 0.50
v2 = (F('2.5') * 2 - F('2.5') * F('0.50')) / F('1.5'); assert v2 == F('2.5')
v2_ign = F('2.5') * 2 / F('1.5');       assert r(v2_ign, 1) == 3.3
v2_add = (F('2.5') * 2 + F('2.5') * F('0.50')) / F('1.5'); assert r(v2_add, 1) == 4.2
v2_wm = (F('2.5') * 2 - F('2.5') * F('0.50')) / F('2.5'); assert v2_wm == F('1.5')
distinct(v2, v2_ign, v2_add, v2_wm)
assert F('2.5') * 2 == F('2.5') * F('0.50') + F('1.5') * v2              # momentum balances

# Recoil: 480 kg cannon at rest fires a 4.0 kg ball east at 150 m/s
vc = -(F('4.0') * 150) / 480;           assert vc == F('-1.25')
vc_inv = F(480) * 150 / F('4.0');       assert vc_inv == 18000
distinct(abs(vc), 150, vc_inv)

# Predict: 1.2 kg east 1.5 and 0.90 kg west 2.0 stick → total zero, they stop
pz = F('1.2') * F('1.5') + F('0.90') * F(-2); assert pz == 0

# Transfer: a cart loses 3.0 kg·m/s; the other gains exactly that, forward.

# Order: momentum magnitudes, greatest to least
ORD_P = [('A 900 kg car rolling at 3.0 m/s', 900 * 3),
         ('An 85 kg cyclist and bike at 12 m/s', 85 * 12),
         ('A 32 kg child running at 6.5 m/s', F(32) * F('6.5')),
         ('A 0.010 kg bullet at 400 m/s', F('0.010') * 400)]
vals = [v for _, v in ORD_P]
assert vals == sorted(vals, reverse=True) and vals == [2700, 1020, 208, 4]
assert sorted([400, 12, F('6.5'), 3], reverse=True)[0] == 400            # by speed the bullet would lead

# =============================================================================
# CARDS
# =============================================================================
C, Q = [], []
card(C, 'Fundamental and derived SI units',
     '**A fundamental (base) SI unit stands on its own; a derived unit is built '
     'by multiplying and dividing base units.**\n'
     '• The base units you meet in physics: the metre (m), kilogram (kg), second '
     '(s), ampere (A) and kelvin (K). The mole and the candela complete the seven.\n'
     '• Derived: the newton, N = kg·m/s²; the joule, J = kg·m²/s²; speed in m/s; '
     'a spring constant in N/m; momentum in kg·m/s.\n'
     '• Test: if you can write it using only other units, it is derived.',
     hint='Mass, length and time come first. Everything mechanical is built from those three.',
     frm='added')
card(C, 'Hooke’s law',
     '**A spring pulls or pushes with a force proportional to how far it is '
     'stretched or squeezed, in the direction opposite to that displacement.**\n'
     '• Double the stretch and the spring force doubles.\n'
     '• The minus sign is the direction: stretch it right and it pulls left; '
     'squeeze it left and it pushes right.\n'
     '• x is the change from the relaxed length, never the length itself.',
     eq='F = −kx')
card(C, 'The spring constant from a graph',
     '**On a graph of force (vertical) against extension (horizontal), the '
     'slope of the straight line is the spring constant k.**\n'
     '• Read a point ON the line, far from the origin, and divide its force by '
     'its extension.\n'
     '• Put the extension into metres before you divide, so k comes out in N/m.\n'
     '• A steeper line is a stiffer spring.',
     eq='k = rise ÷ run = F ÷ x')
card(C, 'Four contact forces',
     '**Normal force, tension, friction and spring force are all pushes or pulls '
     'from something touching the object.**\n'
     '• Normal: a surface pushing straight out of itself, at right angles to it.\n'
     '• Tension: a rope, string or cable pulling along its own length, away from '
     'the object.\n'
     '• Friction: a surface resisting sliding, along the surface, against the '
     'slide.\n'
     '• Spring force: a stretched or squeezed spring, back toward its relaxed length.',
     hint='Name what is touching the object, and you have named the force.')
card(C, 'Weight: Fg = mg',
     '**An object’s weight is the force of gravity on it: its mass times the '
     'gravitational field strength g.**\n'
     '• Near Earth’s surface, g = 9.8 m/s² (your quiz uses 9.8; the momentum '
     'practice says 10 — use whatever the test states).\n'
     '• Weight is a force, so it is in newtons and points down.\n'
     '• Work backward with m = Fg ÷ g, using the g of the planet you are on.',
     eq='Fg = mg')
card(C, 'Mass and weight are different things',
     '**Mass is how much matter an object has, measured in kilograms; weight is '
     'the pull of gravity on it, measured in newtons.**\n'
     '• Mass does two jobs: it measures how hard the object is to speed up, slow '
     'down or turn (its inertia), AND it sets how strongly gravity pulls it.\n'
     '• Mass does not depend on gravity: it is the same on Earth, on the Moon and '
     'floating in deep space. Weight changes from planet to planet.',
     hint='Weightless is not massless. A floating crate is still just as hard to shove.')
card(C, 'Normal force on a level surface',
     '**For an object at rest on a level surface with only gravity and the '
     'surface acting up and down, the normal force equals the weight, mg.**\n'
     '• It is equilibrium in the vertical direction: up forces = down forces.\n'
     '• An extra push down on the object makes the normal force bigger; an '
     'upward pull that does not lift it makes it smaller.',
     eq='N = mg   (level, at rest, nothing else vertical)')
card(C, 'Tension with parallel forces',
     '**When a hanging object is at rest, the upward tensions add up to '
     'everything hanging below them.**\n'
     '• A rope holding a stack of objects holds the weight of every object below it.\n'
     '• Two identical vertical ropes sharing a load equally each hold half of it.',
     eq='ΣT_up = total weight below')
card(C, 'Tension at an angle',
     '**A rope at an angle pulls sideways as well as up, so only its vertical '
     'part holds the weight.**\n'
     '• For two matching ropes each at θ above the horizontal: 2T sin θ = weight, '
     'and the sideways parts cancel each other.\n'
     '• So each rope carries MORE than half the weight, and the flatter the '
     'ropes, the bigger the tension.',
     eq='2T sin θ = Fg')
card(C, 'Forces on it, forces it exerts',
     '**Choose one object (the system) first; only forces acting ON it count '
     'toward its motion.**\n'
     '• A force the object exerts on something else belongs to that other '
     'object’s diagram.\n'
     '• Name every force as “A on B”. If B is not your object, leave it off.',
     hint='Your object must be the second name: “… on the cart”.')
card(C, 'Drawing a free-body diagram',
     '**A free-body diagram is the object drawn as a dot, with one arrow for '
     'every force acting on it.**\n'
     '• Each arrow starts at the dot, points the way the force acts, and is '
     'labelled with its agent (“rope on crate”).\n'
     '• Draw longer arrows for bigger forces.\n'
     '• Then add the arrows along each axis: what is left over is the net force.',
     frm='added')
card(C, 'Net force: the vector sum',
     '**The net force is the vector sum of all the forces acting on one object.**\n'
     '• Along one line: choose a positive direction and add the forces with signs.\n'
     '• At right angles: add each axis separately, then combine (Pythagoras).\n'
     '• Only the net force decides the acceleration: F_net = ma.',
     eq='F_net = ΣF')
card(C, 'Inertia and Newton’s first law',
     '**An object keeps its velocity — staying at rest, or moving in a straight '
     'line at constant speed — unless a nonzero net force acts on it.**\n'
     '• Inertia is that resistance to a change in motion, and mass measures it.\n'
     '• Twice the mass means twice the inertia: a 4 kg block is twice as hard to '
     'speed up as a 2 kg block.\n'
     '• Nothing “runs out”: a moving thing slows only because a force (often '
     'friction) acts on it.',
     hint='Inertia is not a force. It is the reason a force is needed.')
card(C, 'Balanced or unbalanced: read the motion',
     '**Balanced forces (net force zero) mean no change in velocity; unbalanced '
     'forces (a nonzero net force) mean the velocity is changing.**\n'
     '• Constant speed in a straight line: net force zero, even though it is moving.\n'
     '• Speeding up, slowing down OR changing direction: there is a net force.\n'
     '• The net force points the way the velocity is changing, not necessarily '
     'the way it is moving.',
     hint='A change in motion needs a net force. Motion itself does not.')
card(C, 'Newton’s third law',
     '**When object A exerts a force on object B, B exerts a force on A of equal '
     'size in the opposite direction.**\n'
     '• To find a partner, swap the names: the partner of “foot on ball” is '
     '“ball on foot”.\n'
     '• Equal forces do not mean equal effects: the lighter object accelerates '
     'more (a = F ÷ m).',
     eq='F_A on B = −F_B on A')
card(C, 'The four marks of a third-law pair',
     '**A third-law pair is equal in size, opposite in direction, simultaneous, '
     'and acts on two DIFFERENT objects.**\n'
     '• Simultaneous: neither comes first; they start and stop together.\n'
     '• Different objects: that is why a pair can never cancel.\n'
     '• The two forces are always the same type: two contact forces, or two '
     'gravitational pulls.')
card(C, 'The pair that is not a pair: weight and normal force',
     '**A book’s weight and the table’s normal force on it are NOT a third-law '
     'pair, even when they are equal and opposite.**\n'
     '• Both act on the same object, the book — a pair must act on two.\n'
     '• They are different types: one is gravity, one is a contact push.\n'
     '• The real partners: Earth pulls the book ↔ the book pulls Earth; the '
     'table pushes the book ↔ the book pushes the table.',
     hint='Equal and opposite on the SAME object is balance, not a third-law pair.',
     frm='added')
card(C, 'Static and dynamic equilibrium',
     '**An object is in equilibrium whenever the net force on it is zero: static '
     'if it is at rest, dynamic if it moves at constant velocity.**\n'
     '• A lamp hanging still: static. A crate pushed across a floor at a steady '
     '2 m/s: dynamic.\n'
     '• Both have balanced forces, and nothing about the forces tells you which '
     'one you have — only the motion does.',
     frm='added')
card(C, 'Splitting an angled force',
     '**A force F at angle θ above the horizontal has a horizontal part F cos θ '
     'and a vertical part F sin θ.**\n'
     '• Cos goes with the side NEXT TO the angle, sin with the side opposite it.\n'
     '• Check the extremes: at 0° the whole force is horizontal (cos 0° = 1).\n'
     '• If the angle is measured from the vertical, the two swap.',
     eq='Fx = F cos θ     Fy = F sin θ')
card(C, 'Combining two perpendicular forces',
     '**Two forces at right angles combine into a resultant whose size comes '
     'from Pythagoras and whose angle comes from the inverse tangent.**\n'
     '• R = √(Fx² + Fy²): square, add, then take the root.\n'
     '• θ = tan⁻¹(opposite ÷ adjacent) is measured from the axis of the force '
     'on the bottom of the fraction — so say which axis, e.g. “62° north of east”.\n'
     '• Calculator in degree mode.',
     eq='R = √(Fx² + Fy²)     θ = tan⁻¹(Fy ÷ Fx)')
card(C, 'Equilibrium in two dimensions',
     '**An object is in equilibrium in two dimensions only when the forces '
     'balance along BOTH axes at once.**\n'
     '• Split every angled force into components.\n'
     '• Then check ΣFx = 0 and ΣFy = 0 separately.\n'
     '• Adding the sizes of the forces never tells you: 12 N east and 5 N north '
     'are balanced by a single 13 N force, not a 17 N one.',
     eq='ΣFx = 0 and ΣFy = 0')
card(C, 'Momentum',
     '**Momentum is mass times velocity: a vector with the direction of the '
     'velocity, measured in kg·m/s (the same as N·s).**\n'
     '• More mass or more speed means more momentum, in proportion: double either '
     'and p doubles.\n'
     '• To compare two objects, multiply mass by speed for each — a light, fast '
     'object can beat a heavy, slow one.',
     eq='p = mv')
card(C, 'Total momentum of a two-object system',
     '**A system is a group of interacting objects studied together, and its '
     'momentum is the sum of its members’ momenta, with signs.**\n'
     '• Pick a positive direction; anything moving the other way is negative.\n'
     '• The sign of the total says which way the system’s momentum points.\n'
     '• Opposite motions subtract; they cancel exactly only if the momenta match.',
     eq='p_total = m₁v₁ + m₂v₂')
card(C, 'Change in momentum',
     '**The change in momentum is the final momentum minus the initial momentum, '
     'signs included.**\n'
     '• An object that slows down while still moving east has a Δp pointing west.\n'
     '• Reversing the subtraction gives the right size and the wrong direction.',
     eq='Δp = p_f − p_i')
card(C, 'Conservation of momentum in a closed system',
     '**In a closed system — one with no net external force — the total momentum '
     'before an interaction equals the total momentum after it.**\n'
     '• Forces between the objects are internal; they move momentum around inside '
     'the system but cannot change the total.\n'
     '• Set it up as m₁v₁ᵢ + m₂v₂ᵢ = m₁v₁f + m₂v₂f and solve for the one unknown.',
     eq='p_before = p_after')
card(C, 'Collisions move momentum around',
     '**In a collision, whatever momentum one object loses, the other gains — in '
     'the same direction.**\n'
     '• That is the third law at work: equal and opposite forces for the same time.\n'
     '• To predict the motion afterward, find the total before; the objects must '
     'share exactly that total afterward. A total of zero means they cannot both '
     'move the same way.',
     hint='Lost by one = gained by the other.')

# =============================================================================
# QUESTIONS
# =============================================================================
q(Q, 1, 'Which of these is a derived SI unit rather than a fundamental one?',
  ['The newton', 'The kilogram', 'The metre', 'The second'],
  0, 'Can the unit be written using other units?',
  ['A fundamental unit cannot be broken into other units.',
   'The kilogram, metre and second are three of the base units.',
   'The newton is kg·m/s², built from all three.',
   'So the newton is derived.'],
  '**The newton is derived: 1 N = 1 kg·m/s².** The kilogram, metre and second '
  'are base units — they are what the newton is built from.',
  'If it has a definition made of other units, it is derived.')

q(Q, 1, 'A cart rolls into a spring fixed to a wall and squeezes it 4 cm toward '
        'the wall. Which way does the spring push on the cart?',
  ['Away from the wall, opposite to the squeeze',
   'Toward the wall, the way it was squeezed',
   'Straight down, into the track',
   'It does not push until the cart has stopped'],
  0, 'The spring always pushes back toward its relaxed length.',
  ['The cart moved the spring’s end toward the wall: that is the displacement.',
   'Hooke’s law, F = −kx: the force is opposite to the displacement.',
   'Opposite to “toward the wall” is away from it.',
   'The spring pushes the cart away from the wall.'],
  '**Away from the wall.** The minus in F = −kx says the spring force always '
  'opposes the displacement — squeezed toward the wall, it pushes back out. It '
  'pushes the whole time it is squeezed, not only once the cart stops.',
  'Squeeze it, it pushes out. Stretch it, it pulls in.')

q(Q, 2, 'A spring with a spring constant of 160 N/m is stretched 4.5 cm from its '
        'relaxed length. What size of force does it exert?',
  ['7.2 N', '720 N', '3560 N', '36 N'],
  0, 'Put the stretch into metres first.',
  ['4.5 cm = 0.045 m.',
   'F = kx = (160 N/m)(0.045 m).',
   'F = 7.2 N.',
   'The spring exerts 7.2 N.'],
  '**F = kx = 160 × 0.045 = 7.2 N.** 720 N leaves the stretch in centimetres; '
  '3560 N and 36 N divide k by the stretch instead of multiplying (in metres and '
  'in centimetres).',
  'N/m times m gives N. Check the units cancel.')

q(Q, 2, 'The graph shown plots the force on a spring in newtons (vertical axis) '
        'against its extension in CENTIMETRES (horizontal axis). The marked point '
        'is (16 cm, 5.6 N). What is the spring constant?',
  ['35 N/m', '0.35 N/m', '0.029 N/m', '2.9 N/m'],
  0, 'Slope = force ÷ extension, with the extension in metres.',
  ['The line passes through the origin, so k = F ÷ x for any point on it.',
   'Use the marked point: F = 5.6 N, x = 16 cm = 0.16 m.',
   'k = 5.6 ÷ 0.16 = 35 N/m.',
   'The spring constant is 35 N/m.'],
  '**k = 5.6 N ÷ 0.16 m = 35 N/m.** 0.35 N/m divides by 16 without converting '
  'centimetres, which really gives N/cm; 0.029 and 2.9 turn the slope upside '
  'down (extension ÷ force).',
  'Force is up the side, so force goes on top.')
Q[-1]['graph'] = {'w': [0, 20, 0, 8], 'gx': 5, 'gy': 2,
                  'series': [{'type': 'line', 'm': 0.35, 'b': 0}],
                  'pts': [{'x': 16, 'y': 5.6, 'label': '(16, 5.6)'}],
                  'xl': 'Extension (cm)', 'yl': 'Force (N)'}

q(Q, 1, 'A climber hangs still from a rope. What is the force the rope exerts '
        'on her called?',
  ['Tension', 'Normal force', 'Friction', 'Spring force'],
  0, 'Ropes and cables pull along their length.',
  ['The rope is what touches her, so the force comes from the rope.',
   'A rope pulls along its own length.',
   'That pull is called tension.',
   'The rope exerts tension.'],
  '**Tension.** A normal force comes from a surface pushing out of itself; '
  'friction resists sliding along a surface; a spring force comes from a '
  'stretched or squeezed spring.',
  'Name what touches the object: rope → tension.')

q(Q, 2, 'A rover’s weight on Mars, where g is about 3.7 m/s², is 1110 N. What is '
        'its mass back on Earth?',
  ['300 kg', '113 kg', '4107 kg', '1110 kg'],
  0, 'Find the mass where you know g, then ask whether mass depends on the planet.',
  ['On Mars, m = Fg ÷ g = 1110 ÷ 3.7.',
   'm = 300 kg.',
   'Mass does not depend on gravity, so it is the same on Earth.',
   'Its mass on Earth is 300 kg.'],
  '**m = 1110 ÷ 3.7 = 300 kg, and mass does not change from planet to planet.** '
  '113 kg divides a Mars weight by Earth’s 9.8; 4107 kg multiplies instead of '
  'dividing; 1110 kg treats a weight in newtons as a mass.',
  'Its WEIGHT on Earth would change. Its mass will not.')

q(Q, 2, 'A 200 kg crate floats weightless inside a space station. Compared with '
        'shoving it along a smooth, frictionless floor on Earth, how hard is it to '
        'get moving?',
  ['Just as hard: its mass, and so its inertia, is unchanged',
   'Much easier: with no weight it has no inertia',
   'Impossible: with no gravity there is nothing to push against',
   'Harder: floating objects resist motion more'],
  0, 'Which property measures resistance to a change in motion?',
  ['Resistance to a change in motion is inertia.',
   'Inertia is measured by mass.',
   'The crate’s mass is still 200 kg in orbit; only its weight is missing.',
   'So it takes the same force to give it the same acceleration.'],
  '**Mass measures inertia, and the crate’s mass has not changed.** Weight is '
  'what went missing, and weight was never what made it hard to accelerate on '
  'a frictionless floor. a = F ÷ m is the same in orbit as on Earth.',
  'Weightless is not massless.')

q(Q, 2, 'A 36 kg trunk rests on a level floor. You pull straight UP on its handle '
        'with 150 N, but it stays on the floor. Using g = 9.8 m/s², what is the '
        'normal force from the floor?',
  ['203 N', '353 N', '503 N', '150 N'],
  0, 'Up forces = down forces, and your pull is an up force.',
  ['Weight: 36 × 9.8 = 352.8 N down.',
   'Up forces: the normal force plus your 150 N pull.',
   'N + 150 = 352.8, so N = 202.8 N.',
   'The normal force is about 203 N.'],
  '**N = 352.8 − 150 ≈ 203 N.** The floor only has to supply what your pull '
  'does not. 353 N ignores the pull; 503 N adds it as though you pushed down; '
  '150 N is your pull, not the floor’s push.',
  'An upward pull lightens the floor’s job.')

q(Q, 2, 'Two flower pots hang one below the other. A 3.5 kg pot hangs from a '
        'ceiling hook by cord A, and a 2.5 kg pot hangs from the bottom of the '
        'first pot by cord B. Both are still. Using g = 9.8 m/s², what is the '
        'tension in cord A?',
  ['58.8 N', '34.3 N', '24.5 N', '6.0 N'],
  0, 'What is cord A holding up?',
  ['Cord A holds the top pot AND everything hanging below it.',
   'Total mass below cord A: 3.5 + 2.5 = 6.0 kg.',
   'At rest, the tension equals that weight: 6.0 × 9.8 = 58.8 N.',
   'Cord A’s tension is 58.8 N.'],
  '**Cord A holds both pots: (3.5 + 2.5) × 9.8 = 58.8 N.** 34.3 N counts only '
  'the top pot; 24.5 N is cord B’s tension; 6.0 N is the mass, not the weight.',
  'A rope holds everything that hangs below it.')

q(Q, 3, 'A 210 N banner hangs still from two ropes, each making 40° with the '
        'horizontal. What is the tension in each rope?',
  ['163 N', '137 N', '105 N', '210 N'],
  0, 'Only each rope’s vertical part holds the banner.',
  ['The two vertical parts must add to the weight: 2T sin 40° = 210 N.',
   'sin 40° ≈ 0.643, so 2T × 0.643 = 210.',
   'T = 210 ÷ 1.286 ≈ 163 N.',
   'Each rope carries about 163 N.'],
  '**2T sin 40° = 210 N, so T ≈ 163 N.** 137 N uses cos, which is the sideways '
  'part for an angle above the horizontal; 105 N splits the weight as if the '
  'ropes were vertical; 210 N gives each rope the whole weight.',
  'Angled ropes carry more than half the weight each.')

q(Q, 1, 'A girl pushes a shopping cart along an aisle. You are drawing the '
        'free-body diagram of the CART. Which force belongs on it?',
  ['The girl’s push on the cart',
   'The cart’s push back on the girl',
   'The floor’s friction on the girl’s shoes',
   'The girl’s weight'],
  0, 'Keep only forces whose second name is “the cart”.',
  ['The system is the cart.',
   '“Girl on cart” acts on the cart: keep it.',
   '“Cart on girl”, “floor on shoes” and the girl’s weight all act on the girl.',
   'Only the girl’s push on the cart belongs.'],
  '**Only forces acting ON the cart count.** The cart’s push back on the girl is '
  'a force the cart EXERTS, so it belongs on the girl’s diagram, with her '
  'weight and the friction on her shoes.',
  'Write every force as “A on B”; B must be your object.')

q(Q, 2, 'A sled’s free-body diagram shows 260 N down (weight), 260 N up (normal '
        'force), 95 N east (a rope’s pull) and 70 N west (friction). What does the '
        'sled do?',
  ['Net force 25 N east: its velocity changes toward the east',
   'Net force 165 N east: it speeds up quickly',
   'Net force zero: it moves at constant velocity',
   'Net force 25 N east: it moves east at constant speed'],
  0, 'Add each axis separately, with signs.',
  ['Vertical: 260 up − 260 down = 0.',
   'Horizontal, east positive: 95 − 70 = +25 N.',
   'A nonzero net force means the velocity changes: it accelerates east.',
   'Net force 25 N east; the sled accelerates toward the east.'],
  '**The vertical forces balance; horizontally 95 − 70 = 25 N east, so it '
  'accelerates east.** 165 N adds forces that point opposite ways; “net zero” '
  'balances only the vertical pair; and “constant speed” forgets that a net '
  'force changes velocity.',
  'Net force means changing velocity — never steady motion.')

q(Q, 1, 'A 1500 kg car and a 6000 kg truck are both parked. How does the truck’s '
        'inertia compare with the car’s?',
  ['Four times as much',
   'The same: neither is moving',
   'A quarter as much',
   'Neither has inertia until it moves'],
  0, 'Inertia is measured by mass.',
  ['Inertia depends on mass, not on whether the object moves.',
   '6000 ÷ 1500 = 4.',
   'The truck has four times the mass.',
   'So it has four times the inertia.'],
  '**Inertia is set by mass, so the truck has 6000 ÷ 1500 = 4 times as much.** '
  'Objects at rest have inertia too — it is why starting them moving takes a '
  'force.',
  'More mass, more inertia, whether moving or not.')

q(Q, 2, 'A coin sits on a card laid across the top of a glass. The card is '
        'flicked sideways very quickly. What happens to the coin?',
  ['It drops into the glass',
   'It flies off sideways with the card',
   'It flies off in the opposite direction',
   'It stays in the air where it was'],
  0, 'For the instant of the flick, is there a sideways force on the coin?',
  ['The card slides out too fast for friction to drag the coin far.',
   'So almost no sideways net force acts on the coin.',
   'By the first law it stays where it was horizontally.',
   'Gravity is then unbalanced, so it falls into the glass.'],
  '**Its inertia keeps it where it was sideways, and gravity drops it into the '
  'glass.** It cannot fly with the card without a sideways force to change its '
  'motion, and nothing pushes it backward either. It cannot hover: once the '
  'card is gone, its weight is unbalanced.',
  'No net force, no change in motion — in that direction.')

q(Q, 2, 'Which of these has a nonzero net force acting on it?',
  ['A car driving around a bend at a steady 15 m/s',
   'An elevator rising at a constant 3 m/s',
   'A book resting on a shelf',
   'A skydiver falling at her terminal velocity'],
  0, 'Look for a change in velocity — speed OR direction.',
  ['A net force is needed only when the velocity changes.',
   'The elevator, the book and the skydiver all have constant velocity.',
   'The car keeps its speed but its direction is changing.',
   'So only the car has a nonzero net force.'],
  '**The car: going round a bend changes its direction, so its velocity '
  'changes.** The other three are in equilibrium — rising, resting or falling '
  'at a steady velocity needs no net force.',
  'Turning counts as a change in motion.')

q(Q, 2, 'Three horizontal forces act on a crate: 130 N east, 85 N west and 30 N '
        'west. What is the net force?',
  ['15 N east', '245 N east', '75 N east', '15 N west'],
  0, 'Take east as positive and add with signs.',
  ['East positive: +130, −85, −30.',
   '130 − 85 − 30 = +15.',
   'Positive means east.',
   'The net force is 15 N east.'],
  '**+130 − 85 − 30 = +15 N, which is 15 N east.** 245 N adds every force as '
  'if all pointed one way; 75 N gives one westward force the wrong sign; '
  '15 N west gets the size right and the direction wrong.',
  'A vector sum keeps the signs.')

q(Q, 1, 'Which of these is NOT true of a Newton’s third-law force pair?',
  ['The two forces act on the same object',
   'The two forces are equal in size',
   'The two forces point in opposite directions',
   'The two forces start and stop at the same moment'],
  0, 'Recall the four marks of a third-law pair.',
  ['A third-law pair is equal in size.',
   'It is opposite in direction.',
   'It is simultaneous: neither comes first.',
   'It acts on two DIFFERENT objects — so “the same object” is the false one.'],
  '**A third-law pair always acts on two different objects.** Equal size, '
  'opposite directions and simultaneous are the other three marks — and acting '
  'on different objects is why the pair can never cancel.',
  'Equal, opposite, simultaneous, different objects.')

q(Q, 2, 'A dictionary rests on a desk. Earth pulls the dictionary down. What is '
        'the third-law partner of that force?',
  ['The dictionary pulls up on Earth',
   'The desk pushes up on the dictionary',
   'The dictionary pushes down on the desk',
   'Earth pulls down on the desk'],
  0, 'Swap the two names in “Earth on dictionary”.',
  ['The force is “Earth on dictionary”, a gravitational pull.',
   'Its partner is “dictionary on Earth”, also gravitational.',
   'Opposite direction: up, toward the dictionary.',
   'The dictionary pulls up on Earth.'],
  '**Swap the names: the dictionary pulls up on Earth, just as hard.** The '
  'desk’s push is the tempting one — equal and opposite — but it acts on the '
  'same object (the dictionary) and is a contact force, so it is a balancing '
  'force, not a partner.',
  'Partner of “A on B” is always “B on A”, same type of force.')

q(Q, 3, 'A 3000 kg bus hits a 0.0020 kg bug, and the bus pushes on the bug with '
        'a force of 1.5 N. Which statement is correct?',
  ['The bug pushes on the bus with 1.5 N; the bug’s acceleration is far larger',
   'The bug pushes on the bus with far less than 1.5 N, because it is so light',
   'The bug pushes on the bus with 1.5 N, so both accelerate equally',
   'The bug pushes on the bus with 1.5 N, and the bus accelerates more'],
  0, 'Same force on each — then a = F ÷ m.',
  ['Third law: the bug pushes back on the bus with 1.5 N.',
   'Bug: a = 1.5 ÷ 0.0020 = 750 m/s².',
   'Bus: a = 1.5 ÷ 3000 = 0.0005 m/s².',
   'Equal forces, wildly unequal accelerations.'],
  '**The forces are equal (1.5 N each way); the accelerations are not.** The '
  'bug’s tiny mass gives it 750 m/s², the bus barely 0.0005 m/s². Mass decides '
  'the effect of a force, never the size of its partner.',
  'Equal forces, unequal masses, unequal accelerations.')

q(Q, 2, 'An elevator rises at a steady 2 m/s. Which describes it?',
  ['Dynamic equilibrium: zero net force while moving at constant velocity',
   'Static equilibrium: zero net force while moving at constant velocity',
   'Not in equilibrium: it is moving',
   'Not in equilibrium: the cable must pull harder than gravity to lift it'],
  0, 'Constant velocity means zero net force. Is it at rest?',
  ['Steady speed in a straight line means the net force is zero.',
   'So it is in equilibrium.',
   'It is moving, so it is not static.',
   'It is in dynamic equilibrium.'],
  '**Zero net force with constant velocity is dynamic equilibrium.** Static '
  'equilibrium is the at-rest case. Moving does not need a net force, and the '
  'cable pulls exactly as hard as gravity — lifting at a steady speed takes '
  'no extra.',
  'At rest: static. Steady velocity: dynamic.')

q(Q, 3, 'Three forces act on a ring: 36 N east, 15 N north, and 39 N pointing '
        '22.6° south of west. Is the ring in equilibrium?',
  ['Yes: the east–west parts cancel and the north–south parts cancel',
   'No: 36 N + 15 N is 51 N, which is more than 39 N',
   'No: it would take four forces to balance in two dimensions',
   'Yes: any three forces at different angles will always balance'],
  0, 'Split the 39 N force and check each axis on its own.',
  ['West part of the 39 N: 39 cos 22.6° ≈ 36 N.',
   'South part: 39 sin 22.6° ≈ 15 N.',
   'East–west: 36 − 36 = 0. North–south: 15 − 15 = 0.',
   'Both axes balance, so the ring is in equilibrium.'],
  '**39 N at 22.6° south of west has components 36 N west and 15 N south, '
  'cancelling the other two exactly.** Adding magnitudes ignores direction; '
  'three forces can balance; and three random forces usually do not.',
  'Equilibrium in 2-D: ΣFx = 0 AND ΣFy = 0.')

q(Q, 2, 'A wagon is pulled by a handle with 160 N at 35° above the horizontal. '
        'What is the horizontal part of the pull?',
  ['131 N', '92 N', '160 N', '195 N'],
  0, 'The horizontal side is next to the angle.',
  ['The angle is from the horizontal, so the horizontal part uses cos.',
   'Fx = 160 cos 35°.',
   'cos 35° ≈ 0.819, so Fx ≈ 131 N.',
   'The horizontal part is about 131 N.'],
  '**Fx = 160 cos 35° ≈ 131 N.** 92 N is the vertical part (sin swapped in); '
  '160 N is the whole pull; 195 N divides by cos 35° instead of multiplying — '
  'a part can never be bigger than the whole.',
  'At 0° it is all horizontal: cos 0° = 1. That tells you which one is cos.')

q(Q, 2, 'Two ropes pull a post: 20 N east and 21 N north. What is the size of the '
        'resultant force?',
  ['29 N', '41 N', '1 N', '841 N'],
  0, 'They are at right angles: Pythagoras.',
  ['R² = 20² + 21² = 400 + 441 = 841.',
   'R = √841.',
   'R = 29 N.',
   'The resultant is 29 N.'],
  '**R = √(20² + 21²) = √841 = 29 N.** 41 N adds them as if in a line; 1 N '
  'subtracts them; 841 N forgets to take the square root.',
  'Perpendicular forces combine by Pythagoras, never by adding.')

q(Q, 3, 'Two forces act on a box: 16 N east and 30 N north. In what direction '
        'does their resultant point?',
  ['61.9° north of east', '28.1° north of east', '61.9° south of east',
   '1.1° north of east'],
  0, 'From the east axis, the north force is opposite the angle.',
  ['Measure from east: opposite = 30 N, adjacent = 16 N.',
   'θ = tan⁻¹(30 ÷ 16) = tan⁻¹(1.875).',
   'θ ≈ 61.9°, in degree mode.',
   'The resultant points 61.9° north of east.'],
  '**tan⁻¹(30 ÷ 16) ≈ 61.9°, measured from east toward north.** 28.1° flips '
  'the ratio (that angle is measured from north, not east); south of east puts '
  'it on the wrong side, since the force points north; 1.1 is the angle in '
  'radians, from a calculator in the wrong mode.',
  'Name the axis you measured from, and check the mode.')

q(Q, 1, 'Which pair of units BOTH measure momentum?',
  ['kg·m/s and N·s', 'kg·m/s² and N', 'kg·m²/s² and J', 'kg·m/s and N/s'],
  0, 'Momentum is mass times velocity.',
  ['p = mv, so its unit is kg × m/s = kg·m/s.',
   'A newton is kg·m/s², so N·s = kg·m/s² × s = kg·m/s.',
   'So kg·m/s and N·s are the same unit.',
   'Momentum is measured in kg·m/s or N·s.'],
  '**kg·m/s and N·s are the same unit, and both measure momentum.** kg·m/s² '
  'and N measure force; kg·m²/s² and J measure energy; N/s is a force per '
  'second, not a momentum.',
  'Multiply out the newton and the two units match.')

q(Q, 2, 'Taking east as positive: a 0.35 kg cart moves east at 2.4 m/s, and a '
        '0.50 kg cart moves west at 1.2 m/s. What is the total momentum of the '
        'two-cart system?',
  ['+0.24 kg·m/s', '−0.24 kg·m/s', '+1.44 kg·m/s', '0 kg·m/s'],
  0, 'Give the westward velocity a minus sign before multiplying.',
  ['East cart: 0.35 × 2.4 = +0.84 kg·m/s.',
   'West cart: 0.50 × (−1.2) = −0.60 kg·m/s.',
   'Total: 0.84 − 0.60 = +0.24 kg·m/s.',
   'The system’s momentum is 0.24 kg·m/s east.'],
  '**+0.84 + (−0.60) = +0.24 kg·m/s, pointing east.** −0.24 swaps the signs; '
  '+1.44 adds the sizes as if both moved east; 0 assumes opposite motions '
  'always cancel, which needs equal momenta, not just opposite directions.',
  'The sign of the total is the system’s direction.')

q(Q, 3, 'Taking east as positive: a 1.8 kg cart moving east at 4.5 m/s slows to '
        '1.5 m/s, still moving east. What is its change in momentum?',
  ['−5.4 kg·m/s', '+5.4 kg·m/s', '−10.8 kg·m/s', '+2.7 kg·m/s'],
  0, 'Δp = p_f − p_i, with both momenta positive here.',
  ['p_i = 1.8 × 4.5 = 8.1 kg·m/s.',
   'p_f = 1.8 × 1.5 = 2.7 kg·m/s.',
   'Δp = 2.7 − 8.1 = −5.4 kg·m/s.',
   'The change is 5.4 kg·m/s west, even though the cart still moves east.'],
  '**Δp = 2.7 − 8.1 = −5.4 kg·m/s.** Slowing down while moving east means the '
  'change points west. +5.4 subtracts the wrong way round; −10.8 adds the '
  'speeds as if it reversed; +2.7 is only the final momentum.',
  'Final minus initial — always in that order.')

q(Q, 1, 'What makes a system “closed” for conservation of momentum?',
  ['No net external force acts on it',
   'No forces of any kind act on any object in it',
   'None of its objects is moving',
   'Its objects stick together after they collide'],
  0, 'Which forces can change the TOTAL momentum?',
  ['Forces between the objects are internal and cannot change the total.',
   'Only an outside (external) force can change the total.',
   'So the condition is: no net external force.',
   'A closed system has no net external force.'],
  '**A closed system has no net external force.** The objects inside can push '
  'each other as hard as they like — those internal forces are what make a '
  'collision happen. Moving or sticking has nothing to do with it.',
  'Internal forces shuffle momentum; only external ones change the total.')

q(Q, 3, 'Taking east as positive: a 2.5 kg cart moving east at 2.0 m/s hits a '
        '1.5 kg cart at rest. Afterward the 2.5 kg cart moves east at 0.50 m/s. '
        'What is the 1.5 kg cart’s velocity?',
  ['2.5 m/s east', '3.3 m/s east', '4.2 m/s east', '1.5 m/s east'],
  0, 'Total before = total after; solve for the one unknown.',
  ['Before: 2.5 × 2.0 + 1.5 × 0 = 5.0 kg·m/s.',
   'After: 2.5 × 0.50 + 1.5v = 1.25 + 1.5v.',
   '5.0 = 1.25 + 1.5v, so 1.5v = 3.75.',
   'v = 2.5 m/s east.'],
  '**5.0 = 1.25 + 1.5v gives v = 2.5 m/s east.** 3.3 m/s forgets the first '
  'cart still has momentum afterward; 4.2 m/s adds its momentum instead of '
  'subtracting it; 1.5 m/s divides by the wrong cart’s mass.',
  'Write the full before = after equation, then solve.')

q(Q, 2, 'Taking east as positive: a 480 kg cannon at rest on frictionless wheels '
        'fires a 4.0 kg ball east at 150 m/s. What is the cannon’s recoil '
        'velocity?',
  ['1.25 m/s west', '1.25 m/s east', '150 m/s west', '18000 m/s west'],
  0, 'The total starts at zero and must stay zero.',
  ['Before: everything at rest, so the total momentum is 0.',
   'Ball: 4.0 × 150 = +600 kg·m/s.',
   'Cannon: 480v = −600, so v = −1.25 m/s.',
   'The cannon recoils at 1.25 m/s west.'],
  '**480v + 600 = 0, so v = −1.25 m/s: 1.25 m/s west.** East forgets the '
  'sign; 150 m/s gives the two equal speeds instead of equal momenta; '
  '18000 m/s turns the mass ratio upside down.',
  'Recoil: equal momenta, opposite directions — not equal speeds.')

q(Q, 2, 'A rolling cart bumps into a cart at rest, and in the collision the '
        'rolling cart loses 3.0 kg·m/s of momentum. What happens to the other cart, '
        'assuming no net external force?',
  ['It gains 3.0 kg·m/s, in the direction the first cart moved',
   'It gains less than 3.0 kg·m/s, because some is lost as sound',
   'It gains 3.0 kg·m/s in the opposite direction',
   'It gains more than 3.0 kg·m/s if it is lighter'],
  0, 'In a closed system, the total cannot change.',
  ['The total momentum before must equal the total after.',
   'If one cart loses 3.0 kg·m/s, the other must gain the same amount.',
   'It gains it in the same direction, so the total still points the same way.',
   'The resting cart gains 3.0 kg·m/s forward.'],
  '**A collision transfers momentum: what one loses, the other gains, same '
  'direction.** Sound and heat carry away kinetic ENERGY, not momentum. Gaining '
  'it backward would change the total; and a lighter cart gets the same '
  'momentum, just more speed.',
  'Lost by one = gained by the other.')

q(Q, 3, 'Taking east as positive: a 1.2 kg cart moves east at 1.5 m/s and a '
        '0.90 kg cart moves west at 2.0 m/s. They collide and stick together. '
        'What happens next?',
  ['They stop dead',
   'They move east, because the 1.2 kg cart is heavier',
   'They move west, because the 0.90 kg cart is faster',
   'They bounce apart at the speeds they arrived with'],
  0, 'Find the total momentum before.',
  ['East cart: 1.2 × 1.5 = +1.8 kg·m/s.',
   'West cart: 0.90 × (−2.0) = −1.8 kg·m/s.',
   'Total: 0. Stuck together, they share one velocity, so 2.1v = 0.',
   'v = 0: they stop.'],
  '**The momenta are equal and opposite, so the total is zero and the stuck '
  'pair must be at rest.** Neither the heavier nor the faster cart “wins”: '
  'only mass times velocity counts. And carts that stick cannot bounce apart.',
  'Predict with the total, not with mass or speed alone.')

q(Q, 3, 'Rank these from GREATEST to LEAST momentum.',
  [t for t, _ in ORD_P],
  0, 'Multiply mass by speed for each one.',
  ['Car: 900 × 3.0 = 2700 kg·m/s.',
   'Cyclist: 85 × 12 = 1020 kg·m/s.',
   'Child: 32 × 6.5 = 208 kg·m/s.',
   'Bullet: 0.010 × 400 = 4.0 kg·m/s. So car, cyclist, child, bullet.'],
  '**Car (2700), cyclist (1020), child (208), bullet (4.0 kg·m/s).** The bullet '
  'is the trap: by far the fastest, but its mass is so small it comes last.',
  'Never rank momentum by speed alone.',
  kind='order')

q(Q, 1, 'Put the steps for drawing a free-body diagram in order.',
  ['Choose the one object you are studying',
   'Draw it as a dot',
   'Draw an arrow from the dot for each force acting ON it, labelled with its agent',
   'Add the forces along each axis to find the net force'],
  0, 'You cannot draw forces until you know whose forces they are.',
  ['First pick the object (the system).',
   'Represent it as a dot.',
   'Add every force acting on it, each labelled “agent on object”.',
   'Finally sum the arrows to get the net force.'],
  '**Object, dot, forces on it, net force.** Choosing the object comes first '
  'because it decides which forces belong; the net force comes last because it '
  'is built from all the arrows.',
  'Whose diagram is it? Answer that first.',
  frm='added', kind='order')

fresh(Q)
build('ad-astra', C, Q, UID,
      'Dynamics 1 · Test Study Guide: Newton’s Laws and Momentum', 'physics',
      'Every mandatory objective on the teacher’s study guide for the test on '
      'Newton’s first law, Newton’s third law and conservation of momentum: SI '
      'units, Hooke’s law and the spring constant from a graph, the contact '
      'forces, weight and mass, the normal force, tension straight and at '
      'angles, systems and free-body diagrams, inertia and the first law, net '
      'force, third-law pairs, equilibrium in one and two dimensions, vector '
      'components and resultants, and momentum: p = mv, system totals, Δp, '
      'conservation in a closed system, and predicting what happens after a '
      'collision.',
      'This is the test review: one card per objective on the guide, and '
      'fresh questions that make you choose which idea a problem wants, the '
      'way the test will.',
      [('Distinguish between fundamental and derived SI units.', 'source'),
       ('State Hooke’s law and find a spring constant from a force–extension graph.', 'source'),
       ('Define and identify normal, tension, friction and spring forces.', 'source'),
       ('Calculate weight or mass with Fg = mg, and compare mass and weight.', 'source'),
       ('Find the normal force and the tension on objects in equilibrium, '
        'including ropes at angles.', 'source'),
       ('Draw and analyze free-body diagrams for a chosen system.', 'source'),
       ('Apply Newton’s first and third laws, including the four marks of an '
        'action–reaction pair.', 'source'),
       ('Resolve forces into components, combine them, and decide whether an '
        'object is in equilibrium in one or two dimensions.', 'source'),
       ('Calculate momentum, total system momentum and change in momentum, and '
        'apply conservation of momentum to a 2-object closed system.', 'source')],
      'Built from the teacher’s N1L, N3L, COM study guide in the Dynamics 1 '
      'folder: one card for each cluster of its mandatory objectives, and '
      'fresh questions across all of them. Two other files that arrived with '
      'it were read for what they ask only and not transcribed: a 30-item '
      'multiple-choice “Newton’s First and Third Laws” assessment with no key, '
      'and a 40-item Conservation of Momentum practice with a key and '
      'handwritten working. None of their numbers or scenarios is reused, and '
      'nothing written on either paper is recorded anywhere. The 30-item quiz '
      'carries Name/Period/Date lines and may be a quiz she has not sat yet; '
      'if it is confirmed as practice, it could become a paper-entry study '
      'guide (letters entered from her paper, a walkthrough, and fresh rescue '
      'variants), the way the Algebra and Biology guides work. Every number '
      'here was computed in the builder and checked, including that no wrong '
      'option is also right, with g = 9.8 m/s² as her quiz states. Worth '
      'knowing: the momentum practice says to use g = 10 m/s² while the quiz '
      'says 9.8, so the first card on weight names both; the quiz also asks '
      'about friction coefficients and a ramp, and the practice about impulse '
      'and kinetic energy, none of which is on the guide’s list — those are '
      'covered in parts 1-2, 1-3, 1-6 and 1-7 rather than here. Three cards '
      'are flagged as study suggestions because the guide names the idea '
      'without explaining it: the list of base SI units, the free-body '
      'diagram steps, and static versus dynamic equilibrium (plus the '
      'weight-and-normal-force non-pair). The traps with deliberate airtime: '
      'mass used as weight, an upward pull added instead of subtracted, sin '
      'and cos swapped, a flipped tangent ratio and radian mode, centimetres '
      'left unconverted on a spring graph, a dropped sign in a momentum total, '
      'final-minus-initial reversed, recoil speeds made equal, and weight and '
      'normal force offered as a third-law pair.',
      ('Say each card’s bold answer aloud before flipping it, then take the '
       'quiz in rounds until every cluster feels routine. On every momentum '
       'question, write the positive direction down first.', 35),
      PATH,
      'N1L, N3L, COM Study Guide (mandatory objectives)',
      SRC_SG + '; question style calibrated against ' + SRC_QZ + ' and ' + SRC_HW,
      offset_hours=3, round_=12, order_=1, prep_=True, libv_=1)

# build() writes quarter 1; this is quarter-2 material, like the rest of Dynamics 1's
# later parts.
p = os.path.join(REPO, PATH)
j = json.load(io.open(p, encoding='utf-8'))
j['records'][UID]['quarter'] = 2
io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
print('  all assertions passed; quarter 2')
