# -*- coding: utf-8 -*-
# Dynamics 1 — a new shelf, four numbered parts, built from the two textbook
# chapters Chris uploaded to Drive/Physics 8/Dynamics 1 on 2026-10-13:
#   06_Forces.pdf                     chapter 6 (6.1, 6.2, 6.3)
#   07_2D+Forces_Kinematics.pdf       chapter 7 (7.1, 7.2, 7.3)
#
# No objective sheet was in the folder (searched by parentId to the end of the
# listing, and by title across Drive for "Dynamics" and "Objectives"), so the
# scope is the chapters themselves.
#
# Chapter 7.2 (projectile motion) is NOT built here. Kinematics 2 · 2-2 was
# built from exactly that section in v181 (its srcName says "Chapter 7, Forces
# and Motion in Two Dimensions"), card for card: independence of motion,
# horizontal launch, launch at an angle, max height, range, flight time, frame
# of reference, air resistance. Re-asking it would be the v142 mistake.
#
# The numbered form (1-1 … 1-4) is structural, per v180/v181: "Circular Motion
# and Torque" would title-sort AHEAD of "Forces and Newton's Laws".
#
# Her sheet's notation throughout: F_net, F_N, F_fk, F_fs, μ_k, μ_s, v_i, v_f.
# Her sheet writes g = −9.8 m/s²; every weight here uses its SIZE, 9.8, with
# the direction said in words — a card says so outright.
#
# EVERY number is computed with sympy below and asserted before it reaches a
# question, including that no distractor is also correct. None of the
# textbook's worked-example or practice numbers is reused (168 N sign at
# 22.5°, 562 N trunk, 62 kg skier, 75 kg elevator, 50 kg bucket, 25 kg box,
# 13 g stopper, 0.18 kg softball, 8.8 m/s runner, 32 m/s car …).
#
# No free-body diagrams are drawn. renderGraph() draws an axed, gridded plot
# whose series are plain polylines with no arrowheads, so a "force arrow" would
# be a line on graph paper — the v142 motion-diagram call again. Forces are
# described in words and the parentNotes say so.
import sys, os, json, io
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

g = sp.Rational(49, 5)                         # |g| = 9.8 m/s², her sheet
def rnd(x, n=1):
    return float(sp.N(sp.Rational(round(float(x) * 10**n), 10**n)))
# rnd() hands back a raw float (5.94 can arrive as 5.9399999999999995), so
# round a second time at the same precision before comparing (v195).
def eq(x, n, want): return round(rnd(x, n), n) == want
def deg(x): return sp.deg(x)
def S(th): return sp.sin(sp.rad(th))
def Co(th): return sp.cos(sp.rad(th))
def T(th): return sp.tan(sp.rad(th))
def distinct(*xs):
    """Every option value differs from the answer (index 0) at the shown
    precision — so no distractor is quietly also correct."""
    a = xs[0]
    for x in xs[1:]:
        assert abs(float(x) - float(a)) > 1e-6, (a, x)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def add_sorts(path, uid, sorts):
    p = os.path.join(REPO, path)
    j = json.load(io.open(p, encoding='utf-8'))
    j['records'][uid]['sorts'] = sorts
    io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))

SRC6 = '06_Forces.pdf (Drive, Physics 8 › Dynamics 1)'
SRC7 = '07_2D+Forces_Kinematics.pdf (Drive, Physics 8 › Dynamics 1)'
NOFBD = ('No free-body diagrams are drawn in the app: its graph engine draws '
         'gridded plots with plain lines and no arrowheads, so an "arrow" would '
         'really be a line on graph paper and could mislead more than help. '
         'Every force is described in words instead, and the chapter asks her '
         'to draw these diagrams by hand, which is the better practice anyway.')

# =============================================================================
# 1-1 FORCES AND NEWTON'S LAWS  (chapter 6.1 and 6.3)
# =============================================================================
# --- numbers ----------------------------------------------------------------
assert 310 + 190 == 500 and 310 - 190 == 120
R_perp = sp.sqrt(120**2 + 160**2);           assert R_perp == 200
ang_perp = deg(sp.atan(sp.Rational(160, 120)))
assert eq(ang_perp, 1, 53.1) and eq(90 - ang_perp, 1, 36.9)
a_car = sp.Rational(3600 - 900, 1350);        assert a_car == 2
a_single = sp.Rational(3600, 1350);           assert eq(a_single, 2, 2.67)   # one force, not net
a_added = sp.Rational(3600 + 900, 1350);      assert eq(a_added, 2, 3.33)    # added the drag
a_flip = sp.Rational(1350, 2700);             assert a_flip == sp.Rational(1, 2)
distinct(a_car, a_single, a_added, a_flip)
mA = sp.Rational(24, 10) / sp.Rational(6, 10);   assert mA == 4
mB = sp.Rational(24, 10) / sp.Rational(18, 10);  assert eq(mB, 2, 1.33) and mB == mA / 3
distinct(mB, mA, 3 * mA, sp.Rational(18, 10) / sp.Rational(24, 10))
F_ball = sp.Rational(25, 100) * g;            assert eq(F_ball, 2, 2.45)
a_earth = F_ball / (6 * 10**24);              assert eq(a_earth * 10**25, 1, 4.1)
a_earth_flip = 6 * 10**24 / F_ball;           assert eq(a_earth_flip / 10**24, 1, 2.4)
ranks = [sp.Rational(18, 3), sp.Rational(30 - 10, 4), sp.Rational(24, 6), sp.Rational(40, 20)]
assert ranks == [6, 5, 4, 2] and sorted(ranks, reverse=True) == ranks
assert sp.Rational(30, 4) > ranks[0]          # the single-force trap would rank B FIRST
a2 = sp.Rational(2 * 6, 2 * 2);               assert a2 == 3      # 2F on 2m: unchanged

C, Q = [], []
card(C, 'Force',
     '**A force is a push or a pull exerted on an object.**\n'
     '• It has a size and a direction, so it is a vector.\n'
     '• It is measured in newtons (N).', frm='source')
card(C, 'System and environment',
     '**The system is the object you are studying; the environment is '
     'everything around it that can push or pull on it.**\n'
     '• Draw a circle round the system and look for every place the '
     'environment touches it. Contact forces act at exactly those places.')
card(C, 'Contact and long-range forces',
     '**A contact force acts only by touching; a long-range force acts '
     'without any contact at all.**\n'
     '• Contact: a hand, a rope, a floor, friction, air pushing on you.\n'
     '• Long-range: gravity (and magnets). In this unit gravity is the only '
     'long-range force in play.')
card(C, 'Every force has an agent',
     '**Every real force has a specific thing exerting it, called its '
     'agent — if you cannot name the agent, the force does not exist.**\n'
     '• Name forces as "agent on object": the rope on the bucket, Earth on '
     'the ball.\n'
     '• This one rule kills most invented forces, including "the force of the '
     'throw" after the ball has left the hand.',
     hint='No agent, no force. Ask "what is doing the pushing?"')
card(C, 'Free-body diagram',
     '**A free-body diagram replaces the object with a dot and draws every '
     'force on it as an arrow with its tail on the dot.**\n'
     '• Arrow length shows the size of the force; arrow direction shows its '
     'direction.\n'
     '• Only forces ON the object belong there — never forces the object '
     'exerts on something else.\n'
     '• Draw these by hand on paper; the app describes them in words.')
card(C, 'Net force',
     '**The net force is the vector sum of every force acting on the '
     'object.**\n'
     '• Same direction: add. Opposite directions: subtract, and the net '
     'points the way of the bigger one.\n'
     '• At right angles: combine with Pythagoras, then find the angle with '
     'tan⁻¹ — exactly as you did with vectors in Kinematics 2.')
card(C, 'Newton’s second law',
     '**The acceleration of an object is the net force on it divided by its '
     'mass, and it points the same way as the net force.**\n'
     '• Bigger net force, bigger acceleration. Bigger mass, smaller '
     'acceleration.\n'
     '• It is the NET force that goes in, never just one of the forces.',
     eq='F_net = ma     a = F_net / m')
card(C, 'The newton',
     '**One newton is the net force that gives a 1 kg mass an acceleration '
     'of 1 m/s².**\n'
     '• So 1 N = 1 kg·m/s².\n'
     '• For scale, a medium apple weighs about 1 N.')
card(C, 'Newton’s first law',
     '**An object at rest stays at rest, and a moving object keeps moving in '
     'a straight line at constant speed, if and only if the net force on it '
     'is zero.**\n'
     '• A net force does not keep things moving. It CHANGES how they are '
     'moving.')
card(C, 'Inertia',
     '**Inertia is an object’s tendency to resist a change in its '
     'velocity.**\n'
     '• The more mass, the more inertia.\n'
     '• Inertia is not a force. It is a property of the object, so it never '
     'appears as an arrow on a free-body diagram.')
card(C, 'Equilibrium',
     '**An object is in equilibrium when the net force on it is zero — which '
     'means it is either at rest OR moving at constant velocity.**\n'
     '• Being at rest is just the special case of constant velocity where the '
     'velocity happens to be zero.\n'
     '• Equilibrium does not mean "no forces". It means the forces cancel.')
card(C, 'Moving does not need a net force',
     '**A force is needed to CHANGE motion, not to keep it going.**\n'
     '• A crate pulled at constant speed has a pull exactly equal to the '
     'friction — not bigger. If the pull were bigger, the crate would be '
     'speeding up.\n'
     '• On a frictionless surface, a sliding object needs no forward force at '
     'all to keep sliding.',
     hint='Constant velocity always means balanced, however fast it is going.')
card(C, 'The throw does not travel with the ball',
     '**Once a thrown ball leaves the hand, the hand’s force is gone.**\n'
     '• A hand is a contact force, and contact has been broken.\n'
     '• Ignoring air, the only force left on the ball is gravity. It keeps '
     'moving forward because nothing is stopping it, not because something is '
     'pushing it.')
card(C, 'ma is not a force',
     '**ma is what the net force equals, not an extra force of its own.**\n'
     '• Experiments show the two sides of F_net = ma are equal; the equals '
     'sign does not create a new arrow.\n'
     '• Never draw an "ma" arrow on a free-body diagram.')
card(C, 'Newton’s third law',
     '**Forces come in pairs: if A pushes on B, then B pushes on A with a '
     'force of equal size in the opposite direction.**\n'
     '• The two forces act on DIFFERENT objects.\n'
     '• Neither one causes the other. They exist together or not at all.',
     eq='F_A on B = −F_B on A')
card(C, 'A third-law pair never cancels',
     '**The two forces in a third-law pair act on different objects, so they '
     'can never cancel each other out.**\n'
     '• Forces only cancel when they act on the SAME object.\n'
     '• A book on a table: the table’s push up and Earth’s pull down are '
     'equal and opposite, but both act on the book, so they are NOT a pair. '
     'The partner of Earth pulling the book is the book pulling Earth.',
     hint='Swap the names. The partner of "A on B" is always "B on A".')
card(C, 'What actually pushes a car forward',
     '**The road pushes the car forward.**\n'
     '• The tyres push backwards on the road; by the third law the road '
     'pushes forwards on the tyres with the same size of force.\n'
     '• That is why a car cannot accelerate on ice — no grip, no forward '
     'push from the road.')
card(C, 'Earth moves too, but not much',
     '**When a ball falls, it pulls up on Earth exactly as hard as Earth '
     'pulls down on it — but Earth’s enormous mass makes its acceleration '
     'unmeasurably small.**\n'
     '• Same force, wildly different masses, so wildly different '
     'accelerations: a = F_net / m on each.')
card(C, 'Tension in a rope',
     '**Tension is the pull a taut rope exerts, and in a light rope it is the '
     'same all the way along.**\n'
     '• In a tug-of-war where each team pulls with 400 N and nothing moves, '
     'the tension is 400 N — not 800 N.\n'
     '• Each end of the rope is just the other end’s third-law partner.')
card(C, 'The four fundamental forces',
     '**Physicists recognise four fundamental interactions: gravitational, '
     'electromagnetic, strong nuclear and weak nuclear.**\n'
     '• Every contact force — friction, the normal force, tension — is '
     'electromagnetic underneath.\n'
     '• The two nuclear forces act inside the nucleus of an atom.')

q(Q, 1, 'Which of these is a long-range force?',
  ['Gravity pulling on a falling apple', 'Friction from a carpet on a sliding box',
   'The tension in a rope lifting a bucket', 'The push of a table holding up a book'],
  0, 'Which one acts without anything touching?',
  ['A contact force needs the agent to touch the object.',
   'Friction, tension and a table’s push all need contact.',
   'Gravity acts across empty space between the apple and Earth.',
   'Gravity is the long-range force.'],
  '**Gravity is the only one here that acts without touching.** Friction, '
  'tension and a supporting surface all work through contact, which is why '
  'the circle-the-system step finds them at the touch points.',
  'Look for the touch points first; whatever is left over is long-range.')

q(Q, 1, 'What does it mean for an object to be in equilibrium?',
  ['The net force on it is zero, so it is at rest or at constant velocity',
   'No forces of any kind are acting on it at that moment',
   'It is at rest, and only being at rest counts as equilibrium',
   'Its speed is constant, though it may be changing direction'],
  0, 'Equilibrium is about the NET force.',
  ['Equilibrium is defined by the net force being zero.',
   'Zero net force means no acceleration.',
   'No acceleration means constant velocity, and rest is the special case of '
   'zero velocity.',
   'So it is at rest or moving at constant velocity.'],
  '**Zero net force — which allows rest or steady straight-line motion.** '
  'Plenty of forces can act, as long as they cancel. A steady speed while '
  'turning is NOT equilibrium, because a change of direction is an '
  'acceleration.',
  'Equilibrium means balanced, not empty.')

q(Q, 2, 'Two people push a stalled car in opposite directions along a level '
        'road: one with 310 N east, the other with 190 N west. What is the net '
        'force from the two of them?',
  ['120 N east', '500 N east', '120 N west', '500 N west'],
  0, 'Opposite directions subtract.',
  ['The forces point in opposite directions, so subtract the sizes.',
   '310 N − 190 N = 120 N.',
   'The net force points the way of the larger force, east.',
   'The net force is 120 N east.'],
  '**Opposite forces subtract: 310 − 190 = 120 N, pointing east because the '
  'east push is bigger.** 500 N is what you would get adding them, which '
  'only applies when both push the same way.',
  'A net force always has a direction. Say it.')

q(Q, 2, 'A sled is pulled with 120 N toward the north and 160 N toward the '
        'east at the same time. What is the net force on it?',
  ['200 N, 53.1° east of north', '280 N, 53.1° east of north',
   '200 N, 36.9° east of north', '40 N, 53.1° east of north'],
  0, 'The two pulls are at right angles.',
  ['Perpendicular forces combine with Pythagoras.',
   'F_net = √(120² + 160²) = √40 000 = 200 N.',
   'Measured from north, tan θ = 160 ÷ 120, so θ = 53.1° toward the east.',
   'The net force is 200 N, 53.1° east of north.'],
  '**√(120² + 160²) = 200 N, at tan⁻¹(160 ÷ 120) = 53.1° east of north.** '
  '280 N adds forces at right angles as if they were in a line, and 36.9° is '
  'the right angle measured from the wrong axis — it is 36.9° north of east, '
  'not east of north.',
  'Name the axis you measured from, or the angle means nothing.')

q(Q, 2, 'A 1350 kg car’s engine drives it forward with 3600 N while friction '
        'and air drag push back with 900 N in total. What is its '
        'acceleration?',
  ['2.0 m/s²', '2.7 m/s²', '3.3 m/s²', '0.50 m/s²'],
  0, 'Which force goes into F_net = ma?',
  ['Find the net force first: 3600 N forward − 900 N back = 2700 N forward.',
   'Then a = F_net / m.',
   'a = 2700 N ÷ 1350 kg.',
   'a = 2.0 m/s², forward.'],
  '**Acceleration comes from the NET force: (3600 − 900) ÷ 1350 = 2.0 m/s².** '
  '2.7 m/s² uses the engine force on its own, which is the commonest error in '
  'the topic; 3.3 m/s² adds the drag instead of subtracting it; 0.50 m/s² '
  'divides the mass by the force.',
  'Net force in, acceleration out. Never one force on its own.')

q(Q, 2, 'A 2.4 N net force gives cart A an acceleration of 0.60 m/s². The same '
        '2.4 N net force gives cart B an acceleration of 1.8 m/s². What is cart '
        'B’s mass?',
  ['1.3 kg', '4.0 kg', '12 kg', '0.75 kg'],
  0, 'Three times the acceleration from the same force — what does that say about mass?',
  ['Cart A: m = F_net / a = 2.4 ÷ 0.60 = 4.0 kg.',
   'Cart B: m = 2.4 ÷ 1.8 = 1.33 kg.',
   'B accelerates three times as much, so it has one third of A’s mass.',
   'Cart B’s mass is 1.3 kg.'],
  '**Same force, three times the acceleration, so one third of the mass: '
  '2.4 ÷ 1.8 = 1.3 kg.** 4.0 kg is cart A’s mass, 12 kg runs the ratio the '
  'wrong way, and 0.75 kg divides the acceleration by the force.',
  'For a fixed force, mass and acceleration go opposite ways.')

q(Q, 2, 'A rope pulls a crate across a rough floor at a constant 1.5 m/s with '
        'a horizontal force of 85 N. How big is the friction force on the '
        'crate?',
  ['85 N — at constant speed the forces balance',
   'Less than 85 N — the pull must win to keep it going',
   'More than 85 N — friction always beats a pull',
   'Zero — friction stops acting once a crate moves'],
  0, 'What does constant speed in a straight line tell you about the net force?',
  ['Constant velocity means zero acceleration.',
   'By the first law, zero acceleration means zero net force.',
   'The only horizontal forces are the 85 N pull and friction, so they must cancel.',
   'Friction is 85 N, opposite the pull.'],
  '**Constant velocity means zero net force, so friction exactly matches the '
  '85 N pull.** The idea that the pull must "win" to keep the crate moving is '
  'the misconception Newton’s first law exists to correct: if the pull won, '
  'the crate would be speeding up.',
  'Steady and straight means balanced, however fast it is going.')

q(Q, 2, 'A hockey puck glides across perfectly frictionless ice in a straight '
        'line at constant speed. Which horizontal forces act on it?',
  ['None — nothing is needed to keep it moving',
   'The stick’s push, still acting from the hit',
   'A forward force of inertia carrying it',
   'A small forward force that matches its speed'],
  0, 'Name the agent of each force offered.',
  ['On frictionless ice nothing touches the puck sideways.',
   'The stick lost contact after the hit, so its force is gone.',
   'Inertia is a property of the puck, not a force with an agent.',
   'So no horizontal force acts, and by the first law its velocity stays the same.'],
  '**No horizontal force acts, and none is needed: with zero net force a '
  'moving object keeps its velocity.** The stick’s force ended with contact, '
  'and inertia is not a force — it has no agent, so it cannot appear on a '
  'free-body diagram.',
  'If you cannot name the agent, the force is not there.')

q(Q, 3, 'A book rests on a table. The table pushes up on the book and Earth '
        'pulls down on the book, with forces of equal size. Are these two '
        'forces a Newton’s third-law pair?',
  ['No — both act on the book, so they are not a pair',
   'Yes — they are equal in size and opposite in direction',
   'Yes — one is the reaction caused by the other one',
   'No — third-law pairs only happen when things move'],
  0, 'A third-law pair is "A on B" and "B on A". Check the objects.',
  ['The table’s push is the table on the book.',
   'The gravity force is Earth on the book.',
   'Both act on the same object, the book, so they cannot be a pair.',
   'They balance because of the first law; the partner of Earth-on-book is '
   'book-on-Earth.'],
  '**Not a pair: a third-law pair acts on two DIFFERENT objects, and both of '
  'these act on the book.** They are equal because the book is in equilibrium, '
  'which is a first-law fact. The true partners are the book pulling up on '
  'Earth and the book pushing down on the table.',
  'Swap the two names: the partner of A-on-B is B-on-A.')

q(Q, 3, 'A horse pulls on a cart, and the cart pulls back on the horse with a '
        'force of exactly the same size. How can the cart ever start moving?',
  ['Only forces ON the cart decide its motion, and the pull can beat friction',
   'It cannot — the two equal pulls cancel, so neither one moves at all',
   'The horse must pull a little harder than the cart pulls back on it',
   'The horse’s pull happens first, before the cart has time to pull back'],
  0, 'Which object does each of the two forces act on?',
  ['The horse-on-cart pull acts on the cart; the cart-on-horse pull acts on the horse.',
   'Forces on different objects never cancel.',
   'To see whether the cart accelerates, add only the forces on the cart: the '
   'horse’s pull forward and friction back.',
   'If the pull is bigger than the friction, the cart accelerates.'],
  '**The pair acts on two different objects, so it never cancels.** The cart '
  'moves if the forces ON THE CART — the horse’s pull against the ground’s '
  'friction — are unbalanced. The horse itself moves forward because the '
  'ground pushes it forward harder than the cart pulls it back.',
  'Pick one object. Add only the forces on it.')

q(Q, 2, 'In a tug-of-war, each team pulls on its end of a rope with 450 N and '
        'the rope does not move. What is the tension in the rope?',
  ['450 N', '900 N', '0 N', '225 N'],
  0, 'Think of either end of the rope as the partner of the other.',
  ['Each team pulls on the rope with 450 N.',
   'The rope does not accelerate, so the forces on it balance.',
   'At any point the rope is pulled 450 N each way, which is what tension measures.',
   'The tension is 450 N.'],
  '**The tension equals the pull at each end: 450 N.** Adding the two teams '
  'to get 900 N is the classic mistake — one team is only the third-law '
  'partner of the other end of the rope. A rope tied to a tree and pulled with '
  '450 N has the same 450 N tension.',
  'Tension is the pull at one end, not both ends added.')

q(Q, 2, 'A 0.25 kg ball is dropped. Earth’s mass is 6.0 × 10²⁴ kg. How big is '
        'Earth’s acceleration toward the ball while it falls?',
  ['4.1 × 10⁻²⁵ m/s²', '9.8 m/s², the same as the ball',
   'Exactly zero — the ball pulls on nothing', '2.4 × 10²⁴ m/s²'],
  0, 'The ball pulls Earth as hard as Earth pulls the ball.',
  ['Earth pulls the ball with F = mg = 0.25 × 9.8 = 2.45 N.',
   'By the third law, the ball pulls Earth with 2.45 N.',
   'Earth’s acceleration is a = F_net / m = 2.45 ÷ (6.0 × 10²⁴).',
   'a = 4.1 × 10⁻²⁵ m/s², far too small to measure.'],
  '**The ball pulls on Earth with the same 2.45 N, but Earth’s huge mass '
  'makes the acceleration 4.1 × 10⁻²⁵ m/s².** It is not zero — the third law '
  'guarantees the force — just unmeasurable. 2.4 × 10²⁴ m/s² divides the mass '
  'by the force instead of the other way round.',
  'Equal forces do not mean equal accelerations. Divide by each mass.')

q(Q, 1, 'What is inertia?',
  ['An object’s tendency to resist any change in its velocity',
   'A force that keeps moving objects going forward',
   'The pull of gravity on an object, measured in newtons',
   'The steady speed a falling object settles at'],
  0, 'Is it something the object HAS, or something done TO it?',
  ['A force needs an agent outside the object.',
   'Inertia has no agent; it is a property of the object itself.',
   'It describes how hard it is to change the object’s velocity.',
   'Inertia is the tendency to resist a change in velocity.'],
  '**Inertia is a property, not a force: an object’s resistance to having its '
  'velocity changed.** The pull of gravity is weight, and the steady falling '
  'speed is terminal velocity — both real, both something else.',
  'Forces are done to objects. Inertia is something an object has.')

q(Q, 2, 'A pitcher throws a ball. Ignoring air, which forces act on the ball '
        'while it is in flight?',
  ['Only gravity, pulling straight down',
   'Gravity, plus the force of the throw carrying it on',
   'Only the force of the throw, until it runs out',
   'Gravity, plus a forward force from its inertia'],
  0, 'Name the agent of every force you include.',
  ['The hand pushed the ball only while touching it.',
   'In flight nothing touches the ball, so there are no contact forces.',
   'Gravity is long-range and keeps acting.',
   'The only force in flight is gravity, downward.'],
  '**Once contact ends, the hand’s force ends; gravity is the only force '
  'left.** The ball keeps moving forward because nothing pushes it backwards, '
  'which is the first law, not a leftover push. This is why projectiles have '
  'no horizontal acceleration.',
  'Contact broken, contact force gone.')

q(Q, 2, 'A car accelerates forward from a traffic light. Which force on the '
        'car actually pushes it forward?',
  ['The road’s friction on the tyres, pointing forward',
   'The tyres’ push on the road, pointing backward',
   'The engine’s push on the car, from inside it',
   'The car’s own momentum, building as it goes'],
  0, 'For the car to accelerate, a force must act ON the car, from outside it.',
  ['The tyres push backward on the road.',
   'That force acts on the road, so it cannot accelerate the car.',
   'By the third law, the road pushes forward on the tyres with the same size of force.',
   'That forward push from the road is what accelerates the car.'],
  '**The road pushes the car forward — the third-law partner of the tyres '
  'pushing the road back.** The tyres’ push acts on the road, so it is the '
  'wrong object as well as the wrong direction. Take the grip away, as on '
  'ice, and the engine can roar all it likes.',
  'Ask what is pushing ON the car from outside it.')

q(Q, 1, 'Which fundamental force is responsible for every everyday contact '
        'force, such as friction and the push of a floor?',
  ['The electromagnetic force', 'The gravitational force',
   'The strong nuclear force', 'The weak nuclear force'],
  0, 'Contact forces come from atoms pushing and pulling on atoms.',
  ['Contact forces happen where the atoms of two surfaces meet.',
   'Atoms and molecules are held together, and pushed apart, by electric forces.',
   'The two nuclear forces act only inside the nucleus.',
   'Contact forces are electromagnetic.'],
  '**Every contact force is electromagnetic underneath — the electrons of two '
  'surfaces repelling and attracting.** Gravity is the long-range force in '
  'this unit, and the strong and weak forces work only inside the nucleus.',
  'Touching is atoms meeting atoms, and that is electromagnetism.')

q(Q, 2, 'A lamp hangs at rest from a cord. Which forces belong on the lamp’s '
        'free-body diagram?',
  ['The cord pulling up and gravity pulling down, equal in size',
   'Gravity pulling down only, since the lamp is just hanging there',
   'The cord pulling up only, since nothing about the lamp is moving',
   'The cord up, gravity down, and the lamp pulling down on the cord'],
  0, 'Only forces acting ON the lamp go on its diagram.',
  ['Two agents act on the lamp: the cord touching it, and Earth.',
   'The cord pulls up; gravity pulls down.',
   'The lamp is at rest, so the net force is zero and the two are equal.',
   'The lamp pulling the cord is a force ON the cord, so it stays off.'],
  '**Tension up, gravity down, equal in size because the lamp is in '
  'equilibrium.** The lamp’s pull on the cord is a real force, but it acts on '
  'the cord, so it belongs on the cord’s diagram — never the lamp’s.',
  'One diagram, one object, only the forces on it.')

q(Q, 3, 'A cart accelerates at 3.0 m/s² under a certain net force. The net '
        'force is doubled AND the cart’s mass is doubled. What is its new '
        'acceleration?',
  ['3.0 m/s²', '6.0 m/s²', '1.5 m/s²', '12 m/s²'],
  0, 'a = F_net / m. What happens to a fraction when top and bottom both double?',
  ['Acceleration is F_net divided by m.',
   'Doubling F_net doubles the top of the fraction.',
   'Doubling m doubles the bottom, which cancels it.',
   'The acceleration stays 3.0 m/s².'],
  '**Doubling both the net force and the mass leaves a = F_net / m '
  'unchanged at 3.0 m/s².** 6.0 m/s² sees only the force, 1.5 m/s² only the '
  'mass, and 12 m/s² multiplies by both instead of dividing.',
  'Change two things at once? Write the fraction and watch both.')

q(Q, 3, 'Rank these carts from GREATEST to LEAST acceleration.',
  ['Cart A: 18 N forward on a 3.0 kg cart',
   'Cart B: 30 N forward and 10 N back on a 4.0 kg cart',
   'Cart C: 24 N forward on a 6.0 kg cart',
   'Cart D: 40 N forward on a 20 kg cart'],
  0, 'Find each net force before dividing by the mass.',
  ['A: 18 ÷ 3.0 = 6.0 m/s².',
   'B: the net force is 30 − 10 = 20 N, so 20 ÷ 4.0 = 5.0 m/s².',
   'C: 24 ÷ 6.0 = 4.0 m/s². D: 40 ÷ 20 = 2.0 m/s².',
   'So A, then B, then C, then D.'],
  '**A (6.0), B (5.0), C (4.0), D (2.0) m/s².** Cart B is the trap: using only '
  'its 30 N forward force gives 7.5 m/s² and puts it first. And cart D has the '
  'biggest force of all but the smallest acceleration, because its mass is '
  'biggest by more.',
  'Biggest force does not mean biggest acceleration. Divide.',
  kind='order')

build('ad-astra', C, Q, 'unit-phys-dyn1-newton',
      'Dynamics 1 · 1-1 Forces and Newton’s Laws', 'physics',
      'What a force is and where forces come from: systems and their '
      'environment, contact and long-range forces, naming the agent of every '
      'force, free-body diagrams, adding forces to get the net force, and '
      'Newton’s three laws — the second as F_net = ma, the first as the law '
      'of inertia and equilibrium, and the third as forces that always come '
      'in pairs on two different objects. Tension in ropes and the four '
      'fundamental forces round it off.',
      'Kinematics described motion without asking what caused it. This is the '
      'cause. Every problem in the rest of the course — slopes, circles, '
      'energy, collisions — starts with the same move: find every force on '
      'one object, add them, and let the net force set the acceleration.',
      [('Define a force and differentiate between contact forces and '
        'long-range forces.', 'source'),
       ('Recognise the significance of Newton’s second law of motion and use '
        'it to solve motion problems.', 'source'),
       ('Explain the meaning of Newton’s first law and describe an object in '
        'equilibrium.', 'source'),
       ('Explain the meaning of interaction pairs of forces and how they are '
        'related by Newton’s third law.', 'source'),
       ('List the four fundamental forces.', 'source'),
       ('Explain the tension in ropes and strings in terms of Newton’s third '
        'law.', 'source')],
      'The first part of the new Dynamics 1 shelf, from chapter 6.1 (Force and '
      'Motion) and 6.3 (Interaction Forces) of the textbook pages in the '
      'Dynamics 1 folder. No objective sheet was in the folder, so the '
      'objectives above are the chapter’s own. Every number was computed with '
      'sympy in the builder and checked before it was written, and none of '
      'the chapter’s worked-example numbers is reused. Four misconceptions '
      'get deliberate airtime because the chapter names them and they cost '
      'marks quietly: that a moving object needs a net force to keep moving '
      '(it needs one only to CHANGE its motion — the constant-speed crate '
      'question offers "the pull must win" as a wrong answer); that the '
      'thrower’s force travels with the ball; that a third-law pair can cancel '
      '(it acts on two different objects, so it never can — the book-on-a-table '
      'question is the classic test of this); and that any single force, '
      'rather than the net force, sets the acceleration. The tug-of-war tension '
      'trap (450 N, not 900 N) is in too. ' + NOFBD,
      ('Read the cards on the three laws until you can say each one without '
       'looking, then take the quiz. For every question, name each force by '
       'its agent before you calculate anything.', 25),
      'content/phys-dyn1-newton.json',
      'Chapter 6, Forces (6.1 Force and Motion, 6.3 Interaction Forces)',
      SRC6, offset_hours=3, libv_=1)

add_sorts('content/phys-dyn1-newton.json', 'unit-phys-dyn1-newton', [{
  'id': 's-bal', 'title': 'Balanced or unbalanced?',
  'a': 'Balanced', 'b': 'Unbalanced',
  'items': [
    {'t': 'A lamp hanging still from the ceiling', 'k': 'a',
     'why': 'At rest, so zero acceleration and zero net force: the cord’s pull matches gravity.'},
    {'t': 'A car on cruise control at a steady 100 km/h on a straight, level road', 'k': 'a',
     'why': 'Constant speed in a straight line is constant velocity, so the net force is zero. Fast is not the same as accelerating.'},
    {'t': 'A sky diver falling at a constant terminal speed', 'k': 'a',
     'why': 'At terminal velocity the air’s drag has grown to equal her weight.'},
    {'t': 'A book lying on a desk', 'k': 'a',
     'why': 'The desk pushes up exactly as hard as gravity pulls down.'},
    {'t': 'An elevator rising at a steady 2 m/s', 'k': 'a',
     'why': 'Moving up, but not speeding up or slowing down — constant velocity, zero net force.'},
    {'t': 'A puck gliding straight at constant speed on frictionless ice', 'k': 'a',
     'why': 'Nothing acts sideways at all, and nothing needs to: the first law keeps it going.'},
    {'t': 'A car pulling away from a red light', 'k': 'b',
     'why': 'Speeding up is accelerating, so the net force points forward.'},
    {'t': 'A bike braking to a stop', 'k': 'b',
     'why': 'Slowing down is accelerating too, with the net force pointing backward.'},
    {'t': 'A ball at the very top of its throw, momentarily still', 'k': 'b',
     'why': 'Still for an instant, but gravity is the only force on it — the velocity is about to change.'},
    {'t': 'A car going round a bend at a steady 40 km/h', 'k': 'b',
     'why': 'Steady speed, but the direction is changing, and a change of direction is an acceleration.'},
    {'t': 'An apple just after it leaves the branch', 'k': 'b',
     'why': 'Only gravity acts, so it speeds up as it falls.'},
    {'t': 'A rocket lifting off and gaining speed', 'k': 'b',
     'why': 'The thrust beats its weight, so the net force points up and it accelerates.'},
  ]}])

# =============================================================================
# 1-2 WEIGHT, FRICTION AND APPARENT WEIGHT  (chapter 6.2)
# =============================================================================
m_ast = 54
assert m_ast * sp.Rational(16, 10) == sp.Rational(864, 10)            # 86.4 N on the Moon
assert m_ast * g == sp.Rational(2646, 5) and eq(m_ast * g, 1, 529.2)   # on Earth
distinct(sp.Rational(864, 10), m_ast * g, 54, 9)
W_bag = sp.Rational(75, 10) * g;          assert eq(W_bag, 1, 73.5)
assert eq(sp.Rational(75, 10) / g, 2, 0.77) and eq(sp.Rational(75, 10) + g, 1, 17.3)
m_sc = sp.Rational(637) / g;              assert m_sc == 65
assert eq(637 * g, 0, 6243)
F_up = 48 * (g + sp.Rational(3, 2));      assert eq(F_up, 0, 542)
assert eq(48 * g, 0, 470) and eq(48 * (g - sp.Rational(3, 2)), 0, 398) and 48 * sp.Rational(3, 2) == 72
distinct(F_up, 48 * g, 48 * (g - sp.Rational(3, 2)), 72)
fs_max = sp.Rational(45, 100) * 18 * g;   assert eq(fs_max, 1, 79.4)
assert 60 < fs_max < 90                   # 60 N holds still, 90 N slides
fk = sp.Rational(25, 100) * 32 * g;       assert eq(fk, 1, 78.4)
assert eq(32 * g, 1, 313.6) and sp.Rational(25, 100) * 32 == 8
a_fr = (150 - fk) / 32;                   assert eq(a_fr, 2, 2.24)
assert eq(sp.Rational(150, 32), 2, 4.69) and eq((150 + fk) / 32, 2, 7.14)
distinct(a_fr, sp.Rational(150, 32), (150 + fk) / 32, (150 - 32 * g) / 32)
assert eq((150 - 32 * g) / 32, 2, -5.11)
mu_sled = sp.Rational(11, 44);            assert mu_sled == sp.Rational(1, 4)
FN_push = 12 * g + 30;                    assert eq(FN_push, 1, 147.6)
assert eq(12 * g, 1, 117.6) and eq(12 * g - 30, 1, 87.6)
k_spr = 250; x_spr = sp.Rational(12, 100)
assert k_spr * x_spr == 30 and eq(k_spr / x_spr, 0, 2083)
T_p = 2 * sp.pi * sp.sqrt(sp.Rational(2) / g);  assert eq(T_p, 2, 2.84)
assert sp.simplify(2 * sp.pi * sp.sqrt(4 * sp.Rational(2) / g) / T_p) == 2   # 4× length → 2× period
assert eq(2 * sp.pi * sp.sqrt(sp.Rational(8) / g), 2, 5.68)

C, Q = [], []
card(C, 'Mass',
     '**Mass is the amount of matter in an object, measured in kilograms, '
     'and it is the same everywhere.**\n'
     '• It is also a measure of inertia: more mass, harder to speed up or '
     'slow down.\n'
     '• It has no direction — mass is a scalar.')
card(C, 'Weight',
     '**Weight is the force of gravity on an object, F_g = mg, measured in '
     'newtons and pointing toward the centre of Earth.**\n'
     '• It changes from planet to planet because g does; the mass does not.\n'
     '• On the Moon, where g is about 1.6 m/s², you weigh about a sixth of '
     'your Earth weight.',
     eq='F_g = mg')
card(C, 'Weight uses the SIZE of g',
     '**Your sheet writes g = −9.8 m/s²; the minus sign is the direction '
     '(down), so the size of a weight is m × 9.8.**\n'
     '• A 50 kg student weighs 50 × 9.8 = 490 N, pointing down.\n'
     '• In a force problem, give the size from 9.8 and say "down" in words, or '
     'keep the minus all the way through with up as positive — just never '
     'mix the two in one problem.', frm='added')
card(C, 'Everything falls with the same acceleration',
     '**Ignoring air, a heavy object and a light one fall with the same '
     'acceleration, g.**\n'
     '• The heavy one does feel a bigger pull — but it also has more mass to '
     'move, and the two cancel exactly in a = F_net / m.\n'
     '• A feather really does fall slower in air. That is air drag, not '
     'gravity.')
card(C, 'What a scale measures',
     '**A bathroom scale measures the force it pushes up on you, not your '
     'mass.**\n'
     '• Standing still, that push equals your weight, so the scale reads your '
     'weight.\n'
     '• Take the same scale to the Moon and it reads less, though your mass '
     'has not changed.')
card(C, 'Normal force',
     '**The normal force is the push a surface exerts on an object, '
     'perpendicular to the surface and away from it.**\n'
     '• It is as big as it needs to be to stop the object sinking in — no more.\n'
     '• It is NOT automatically equal to the weight.',
     hint='"Normal" here means perpendicular, as in geometry.')
card(C, 'Normal force with an extra push',
     '**Press down on a box and the floor must push up harder; lift up on it '
     'and the floor pushes up less.**\n'
     '• Push down with P: F_N = mg + P.\n'
     '• Lift up with P: F_N = mg − P.\n'
     '• And on a slope it is less than mg again — that is in 1-3.')
card(C, 'Apparent weight',
     '**Your apparent weight is the force a scale or floor actually exerts on '
     'you, and it changes when you accelerate up or down.**\n'
     '• Accelerating upward: the floor must push harder, F = m(g + a). You '
     'feel heavier.\n'
     '• Accelerating downward: F = m(g − a). You feel lighter.',
     eq='F_scale = m(g + a)  (a positive upward)')
card(C, 'It is the acceleration, not the direction of travel',
     '**An elevator moving at constant speed — up or down — reads your true '
     'weight.**\n'
     '• Speeding up while going up, or slowing down while going down, both '
     'mean an UPWARD acceleration, so both read heavy.\n'
     '• Slowing down while going up reads light.',
     hint='Ask which way the velocity is CHANGING, not which way it points.')
card(C, 'Weightlessness',
     '**Weightlessness means your apparent weight is zero, not that your '
     'weight is zero.**\n'
     '• In free fall, you and the scale fall together, so the scale has '
     'nothing to push on and reads zero.\n'
     '• Gravity is still pulling you with your full weight the whole time.')
card(C, 'Friction',
     '**Friction is the contact force that opposes sliding between two '
     'surfaces, acting parallel to the surface.**\n'
     '• It points opposite to the sliding, or opposite to the way the object '
     'would slide.\n'
     '• It comes from the microscopic bumps of the two surfaces briefly '
     'bonding.')
card(C, 'Static friction',
     '**Static friction holds a still object in place, and it grows to match '
     'whatever push it is resisting — up to a limit.**\n'
     '• Push with 20 N and it pushes back 20 N; push with 30 N and it gives '
     '30 N.\n'
     '• The most it can give is μ_s F_N. Push harder than that and the object '
     'starts to slide.',
     eq='F_fs ≤ μ_s F_N')
card(C, 'Kinetic friction',
     '**Once an object is sliding, kinetic friction acts on it with a fixed '
     'size, μ_k F_N.**\n'
     '• μ_k is usually smaller than μ_s, which is why it is harder to start a '
     'heavy box moving than to keep it moving.',
     eq='F_fk = μ_k F_N')
card(C, 'The coefficient of friction',
     '**μ is a number with no units that says how grippy two surfaces are '
     'together.**\n'
     '• It depends on BOTH surfaces: rubber on dry concrete grips far better '
     'than steel on oiled steel.\n'
     '• It is usually below 1, but it does not have to be — drag-racing '
     'tyres reach about 5.')
card(C, 'Friction ignores area and speed',
     '**In the model you use, friction depends on the surfaces and the normal '
     'force — not on how much area is touching, and not on how fast it '
     'slides.**\n'
     '• A brick slid on its wide face or its narrow edge feels the same '
     'friction.')
card(C, 'Air drag and terminal velocity',
     '**Air drag grows as an object speeds up, until it equals the weight; '
     'then the net force is zero and the speed stops changing.**\n'
     '• That steady speed is the terminal velocity.\n'
     '• A sky diver changes hers by changing shape: spread out is slower, '
     'tucked in is faster, and a parachute makes it slow enough to land.')
card(C, 'Simple harmonic motion',
     '**When the force pulling an object back to its resting position grows '
     'in proportion to how far it is pulled away, it moves back and forth in '
     'simple harmonic motion.**\n'
     '• Period: the time for one complete cycle. Amplitude: the biggest '
     'distance from rest.\n'
     '• A spring is the classic case: F = −kx, where the minus means the pull '
     'is always back toward rest.',
     eq='F = −kx')
card(C, 'A pendulum’s period',
     '**For small swings, a pendulum’s period depends only on its length and '
     'on g — not on the mass of the bob, and not on how far it swings.**\n'
     '• Longer string, longer period. Four times the length, twice the '
     'period.\n'
     '• This formula is from the textbook; it is not on your sheet.',
     eq='T = 2π √(l / g)')
card(C, 'Resonance',
     '**Small pushes timed to match an object’s own period build up a large '
     'swing — that is mechanical resonance.**\n'
     '• Pumping a playground swing, rocking a stuck car free, bouncing on a '
     'diving board.\n'
     '• It can also do damage: a crowd jumping in time with a balcony’s '
     'natural period can shake it apart.')

q(Q, 1, 'An astronaut has a mass of 54 kg on Earth. What is her mass on the '
        'Moon, where g is about 1.6 m/s²?',
  ['54 kg', '9.0 kg', '86 kg', '0 kg'],
  0, 'Does the amount of matter in her change on the trip?',
  ['Mass is the amount of matter in an object.',
   'Travelling to the Moon does not add or remove any matter.',
   'Only weight depends on g; mass does not.',
   'Her mass is still 54 kg.'],
  '**Mass does not change from place to place: still 54 kg.** 9.0 kg divides '
  'by six, which is what happens to her WEIGHT, and 86 kg confuses the '
  'kilograms with her Moon weight in newtons.',
  'Mass is how much of you there is. Weight is how hard a planet pulls.')

q(Q, 2, 'An astronaut has a mass of 54 kg. What is her weight on the Moon, '
        'where g is about 1.6 m/s²?',
  ['86 N', '529 N', '54 N', '9.0 N'],
  0, 'Weight is F_g = mg — with which g?',
  ['Weight is F_g = mg.',
   'On the Moon, use the Moon’s g, 1.6 m/s².',
   'F_g = 54 × 1.6 = 86.4 N.',
   'Her Moon weight is 86 N.'],
  '**F_g = mg = 54 × 1.6 = 86 N.** 529 N is her Earth weight, 54 N writes '
  'her mass with the wrong unit, and 9.0 N divides her mass by six instead '
  'of multiplying by the Moon’s g.',
  'Kilograms and newtons measure different things. The unit tells you which.')

q(Q, 2, 'What is the weight of a 7.5 kg bag of rice near Earth’s surface?',
  ['73.5 N', '7.5 N', '0.77 N', '17.3 N'],
  0, 'F_g = mg, using the size of g.',
  ['Weight is F_g = mg.',
   'Use the size of g, 9.8 m/s².',
   'F_g = 7.5 × 9.8 = 73.5 N.',
   'The bag weighs 73.5 N, pointing down.'],
  '**F_g = mg = 7.5 × 9.8 = 73.5 N.** 7.5 N treats the mass as if it were a '
  'weight, 0.77 N divides instead of multiplying, and 17.3 N adds the two.',
  'Kilograms times 9.8 gives newtons.')

q(Q, 2, 'A bathroom scale on Earth reads 637 N when a student stands still on '
        'it. What is the student’s mass?',
  ['65 kg', '637 kg', '6243 kg', '6.5 kg'],
  0, 'Run F_g = mg backwards.',
  ['Standing still, the scale reads the student’s weight, 637 N.',
   'm = F_g ÷ g.',
   'm = 637 ÷ 9.8 = 65 kg.',
   'The student’s mass is 65 kg.'],
  '**m = F_g ÷ g = 637 ÷ 9.8 = 65 kg.** 637 kg reads the newtons as '
  'kilograms, and 6243 kg multiplies by g instead of dividing.',
  'Newtons divided by 9.8 gives kilograms.')

q(Q, 3, 'A 48 kg student stands on a scale in an elevator that is speeding up '
        'as it rises, accelerating at 1.5 m/s². What does the scale read?',
  ['542 N', '470 N', '398 N', '72 N'],
  0, 'The net force must point the same way as the acceleration.',
  ['Up is positive. The forces are the scale’s push up and her weight down.',
   'F_net = F_scale − mg = ma, so F_scale = m(g + a).',
   'F_scale = 48 × (9.8 + 1.5) = 48 × 11.3.',
   'The scale reads 542 N.'],
  '**Accelerating upward, the scale must push up MORE than her weight: '
  'm(g + a) = 542 N.** 470 N is her true weight, 398 N uses g − a (the '
  'reading for a DOWNWARD acceleration), and 72 N is only the net force, '
  'ma.',
  'Feel heavier when the acceleration points up.')

q(Q, 2, 'A 48 kg student stands on a scale in an elevator moving DOWN at a '
        'constant 3 m/s. What does the scale read?',
  ['470 N, the student’s true weight', 'Less than 470 N, since it is going down',
   'More than 470 N, to slow the drop', 'Zero, because the student is moving down'],
  0, 'Is the elevator accelerating?',
  ['Constant speed in a straight line means zero acceleration.',
   'Zero acceleration means zero net force.',
   'So the scale’s push exactly equals the weight, 48 × 9.8.',
   'The scale reads 470 N.'],
  '**Constant velocity, so zero net force, so the scale reads the true '
  'weight, 470 N — whichever way the elevator is moving.** The reading only '
  'changes while the elevator speeds up or slows down.',
  'Direction of travel does not matter. Acceleration does.')

q(Q, 3, 'A student rides an elevator standing on a scale. Rank these moments '
        'from the HIGHEST scale reading to the LOWEST.',
  ['Speeding up while going up', 'Moving up at a constant speed',
   'Slowing down while going up', 'Falling freely after the cable snaps'],
  0, 'For each moment, which way does the ACCELERATION point?',
  ['Speeding up while rising: acceleration up, so the reading is m(g + a), '
   'above the true weight.',
   'Constant speed: no acceleration, so the reading is the true weight.',
   'Slowing while rising: acceleration down, so m(g − a), below the true weight.',
   'Free fall: a = g downward, so m(g − g) = 0. The scale reads nothing.'],
  '**Highest when accelerating upward, then true weight at constant speed, '
  'then light when accelerating downward, and zero in free fall.** The trap is '
  'slowing down while going up: the elevator is still rising, but its '
  'acceleration points down, so it reads light.',
  'Apparent weight follows the acceleration, never the velocity.',
  kind='order')

q(Q, 2, 'An astronaut floating in an orbiting space station is called '
        '"weightless". What is actually true?',
  ['Her apparent weight is zero, but gravity still pulls on her',
   'She has no weight at all, because there is no gravity up there',
   'Her mass has dropped to zero, so gravity has nothing to pull',
   'Gravity and her inertia are cancelling, so the net force is zero'],
  0, 'Weightless describes what a scale would read.',
  ['She and the station are both falling freely around Earth together.',
   'Nothing pushes up on her, so a scale under her would read zero.',
   'Gravity is still pulling her — it is what keeps the station in orbit.',
   'So her apparent weight is zero; her real weight is not.'],
  '**Weightlessness is zero APPARENT weight: nothing pushes up on her because '
  'she is in free fall.** Gravity at the station’s height is still about '
  'nine-tenths of its strength at the ground. Her mass is unchanged, and '
  'inertia is not a force, so it cannot cancel anything.',
  'Weightless means "no scale can feel you", not "no gravity".')

q(Q, 2, 'An 18 kg box sits on a floor with μ_s = 0.45. You push it '
        'horizontally with 60 N and it does not move. What is the static '
        'friction force?',
  ['60 N', '79.4 N', '0 N', '19.4 N'],
  0, 'Static friction is an "up to" force, not a fixed one.',
  ['The most static friction could give is μ_s F_N = 0.45 × 18 × 9.8 = 79.4 N.',
   'Your 60 N push is less than that, so the box stays put.',
   'The box is not accelerating, so friction must exactly balance your push.',
   'Static friction is 60 N.'],
  '**Static friction matches the push, 60 N — it only reaches its maximum, '
  '79.4 N, at the moment the box is about to slide.** Reading the ≤ on your '
  'sheet as = is the error here; 19.4 N is the leftover capacity, not a force '
  'acting.',
  'F_fs ≤ μ_s F_N. The "≤" is the whole point.')

q(Q, 2, 'An 18 kg box sits on a floor with μ_s = 0.45. Will it start to slide '
        'if you push it horizontally with 90 N?',
  ['Yes — 90 N is more than the 79.4 N limit',
   'No — friction always grows to match a push',
   'No — 90 N is less than its 176 N weight',
   'Yes — any push at all moves a box on a floor'],
  0, 'Compare the push with the most static friction can give.',
  ['F_N = mg = 18 × 9.8 = 176.4 N on a level floor with no extra push.',
   'Maximum static friction = μ_s F_N = 0.45 × 176.4 = 79.4 N.',
   '90 N is more than 79.4 N.',
   'Friction cannot hold it, so it slides.'],
  '**Static friction can only grow to μ_s F_N = 79.4 N, and 90 N beats it, so '
  'the box slides.** Comparing the push with the WEIGHT mixes a horizontal '
  'force with a vertical one; the weight matters only through the normal '
  'force.',
  'Find the limit first, then compare.')

q(Q, 2, 'A 32 kg crate slides across a floor at constant speed. μ_k = 0.25. '
        'How hard must it be pushed horizontally?',
  ['78.4 N', '313.6 N', '8.0 N', '0 N'],
  0, 'Constant speed means the push balances the friction.',
  ['On a level floor with no extra push, F_N = mg = 32 × 9.8 = 313.6 N.',
   'F_fk = μ_k F_N = 0.25 × 313.6 = 78.4 N.',
   'Constant speed means zero net force, so the push equals the friction.',
   'The push is 78.4 N.'],
  '**At constant speed the push equals kinetic friction, μ_k F_N = 78.4 N.** '
  '313.6 N is the weight, 8.0 N forgets to multiply by g, and 0 N is the '
  '"moving things need no force" idea applied where there IS friction to '
  'balance.',
  'Constant speed with friction means the push equals the friction.')

q(Q, 3, 'A 32 kg crate on a floor with μ_k = 0.25 is pushed horizontally with '
        '150 N while it slides. What is its acceleration?',
  ['2.24 m/s²', '4.69 m/s²', '7.14 m/s²', '−5.11 m/s²'],
  0, 'Find the net force first.',
  ['F_fk = μ_k mg = 0.25 × 32 × 9.8 = 78.4 N, opposing the push.',
   'F_net = 150 − 78.4 = 71.6 N.',
   'a = F_net ÷ m = 71.6 ÷ 32.',
   'a = 2.24 m/s², in the direction of the push.'],
  '**a = (150 − 78.4) ÷ 32 = 2.24 m/s².** 4.69 m/s² ignores friction — the '
  'single-force trap again — 7.14 m/s² adds friction as if it helped, and '
  '−5.11 m/s² subtracts the whole weight instead of the friction.',
  'Friction joins the net force. It does not replace it.')

q(Q, 2, 'A sled with a weight of 44 N is pulled across packed snow at constant '
        'speed by a horizontal force of 11 N. What is the coefficient of '
        'kinetic friction?',
  ['0.25', '4.0', '11', '0.20'],
  0, 'At constant speed, the pull IS the friction.',
  ['Constant speed means the 11 N pull equals the friction.',
   'On level snow with no extra push, F_N equals the weight, 44 N.',
   'μ_k = F_fk ÷ F_N = 11 ÷ 44.',
   'μ_k = 0.25.'],
  '**μ_k = F_fk ÷ F_N = 11 ÷ 44 = 0.25.** 4.0 divides the wrong way round — a '
  'coefficient bigger than 1 is possible but would be very grippy snow — and '
  '11 is the friction force itself, which has units.',
  'μ has no units. If your answer has newtons, you have not divided.')

q(Q, 2, 'A 12 kg box sits on a level floor and you press straight down on its '
        'lid with 30 N. What is the normal force from the floor?',
  ['147.6 N', '117.6 N', '87.6 N', '30 N'],
  0, 'The floor must hold up everything pressing down on it.',
  ['Two forces push the box down: its weight, 12 × 9.8 = 117.6 N, and your 30 N.',
   'The box is not accelerating, so the floor’s push up must balance both.',
   'F_N = 117.6 + 30.',
   'The normal force is 147.6 N.'],
  '**The floor pushes up with the weight PLUS your push: 147.6 N.** Assuming '
  'the normal force always equals mg (117.6 N) is the trap — the floor '
  'pushes back with whatever it takes. 87.6 N is what it would be if you '
  'LIFTED with 30 N.',
  'The normal force is whatever it needs to be. Add up what it is fighting.')

q(Q, 3, 'A brick slides across a floor, first on its wide face and then on its '
        'narrow edge. How does the kinetic friction compare?',
  ['It is the same, since area does not enter F_fk = μ_k F_N',
   'It is bigger on the wide face, where more of it is touching',
   'It is bigger on the narrow edge, where the weight is concentrated',
   'It depends on which way up it was moving the fastest'],
  0, 'Look for area in your sheet’s friction formula.',
  ['Kinetic friction is F_fk = μ_k F_N.',
   'The surfaces are the same, so μ_k is the same.',
   'The weight is the same, so F_N is the same.',
   'Contact area appears nowhere, so the friction is the same.'],
  '**Friction depends on the surfaces and the normal force, and neither '
  'changes when the brick is turned over.** More area touching spreads the '
  'same weight more thinly, and the two effects cancel in this model. Speed '
  'does not enter either.',
  'If a quantity is not in the formula, it cannot change the answer.')

q(Q, 3, 'A sky diver reaches terminal velocity. What is the net force on her '
        'at that point?',
  ['Zero — air drag has grown to equal her weight',
   'Downward, equal to her full weight',
   'Upward, because the air is slowing her',
   'Zero, because gravity stops at high speed'],
  0, 'Terminal velocity is a CONSTANT velocity.',
  ['At terminal velocity her speed is no longer changing.',
   'No acceleration means zero net force.',
   'Gravity has not changed, so the drag must have grown to match it.',
   'The net force is zero.'],
  '**Constant velocity, so zero net force: drag up exactly equals weight '
  'down.** Gravity never switches off. If the net force pointed up she would '
  'be slowing down, which only happens for a moment after the parachute '
  'opens.',
  'Steady speed always means balanced forces, falling or not.')

q(Q, 2, 'Which change would make a pendulum’s period longer?',
  ['Making the string longer', 'Using a heavier bob on it',
   'Pulling it back slightly further', 'Giving it a push instead of letting go'],
  0, 'Look at what appears in T = 2π √(l / g).',
  ['The period depends only on the length l and on g.',
   'The mass of the bob is not in the formula.',
   'For small swings, the amplitude is not in it either.',
   'So only a longer string gives a longer period.'],
  '**Only length and g set a pendulum’s period; a longer string swings more '
  'slowly.** A heavier bob, a slightly bigger swing or a starting push all '
  'change how big the swing is, not how long each one takes.',
  'Length and g. Nothing else.')

q(Q, 3, 'A pendulum’s string is made four times as long. What happens to its '
        'period?',
  ['It doubles', 'It becomes four times as long',
   'It stays exactly the same', 'It halves'],
  0, 'The length is under a square root.',
  ['T = 2π √(l / g).',
   'Multiplying l by 4 multiplies √l by √4 = 2.',
   'Nothing else in the formula changes.',
   'The period doubles.'],
  '**The length sits under a square root, so four times the length gives '
  '√4 = 2 times the period.** A 2.0 m pendulum, for instance, has a period '
  'of 2.84 s; an 8.0 m one, 5.68 s. Four times is what you get if you forget '
  'the root.',
  'Square root: four times in, two times out.')

q(Q, 2, 'A spring with k = 250 N/m is stretched 0.12 m from its resting '
        'length. What force does it exert on whatever is stretching it?',
  ['30 N, back toward its resting length', '30 N, further in the stretch direction',
   '2083 N, back toward its resting length', '0.00048 N, back toward its resting length'],
  0, 'F = −kx. What does the minus sign tell you?',
  ['The size is kx = 250 × 0.12.',
   'That is 30 N.',
   'The minus sign in F = −kx means the force is opposite to the stretch.',
   'So 30 N, pulling back toward the resting length.'],
  '**kx = 250 × 0.12 = 30 N, and the minus sign makes it a restoring force, '
  'back toward rest.** That restoring direction is what makes a mass on a '
  'spring bounce in simple harmonic motion. 2083 N divides k by x.',
  'A spring always pulls or pushes back toward where it rests.')

q(Q, 1, 'Ignoring air, a 5 kg ball and a 1 kg ball are dropped together from '
        'the same height. Which lands first?',
  ['They land at the same time', 'The 5 kg ball, being heavier',
   'The 1 kg ball, being easier to move', 'It depends on how high they start'],
  0, 'The heavier ball is pulled harder — but what else is bigger?',
  ['The 5 kg ball has five times the weight.',
   'It also has five times the mass to accelerate.',
   'a = F_net / m = 5mg ÷ 5m = g, the same for both.',
   'Same acceleration from the same height, so they land together.'],
  '**Ignoring air, every object falls with the same acceleration, g, so they '
  'land together.** The bigger pull on the heavier ball is exactly cancelled '
  'by its bigger mass. In real air, a very light or spread-out object does '
  'fall behind — that is drag, not gravity.',
  'More weight, more mass, same g.')

build('ad-astra', C, Q, 'unit-phys-dyn1-weight',
      'Dynamics 1 · 1-2 Weight, Friction and Apparent Weight', 'physics',
      'Newton’s laws put to work on the forces you meet every day: mass and '
      'weight and how F_g = mg connects them, what a scale really measures and '
      'why you feel heavier or lighter in an elevator, the normal force, '
      'static and kinetic friction with your sheet’s F_fs ≤ μ_s F_N and '
      'F_fk = μ_k F_N, air drag and terminal velocity, and the back-and-forth '
      'of springs and pendulums.',
      'Friction and the normal force are in nearly every force problem from '
      'here on, and the difference between mass and weight is the single '
      'idea most often mixed up on a physics test. Getting them straight now '
      'makes slopes and circles in 1-3 and 1-4 a matter of geometry.',
      [('Describe how the weight and the mass of an object are related.', 'source'),
       ('Differentiate between the gravitational force weight and what is '
        'experienced as apparent weight.', 'source'),
       ('Define the friction force and distinguish between static and '
        'kinetic friction.', 'source'),
       ('Describe simple harmonic motion and explain how the acceleration due '
        'to gravity influences such motion.', 'source')],
      'From chapter 6.2 (Using Newton’s Laws). Every number was computed with '
      'sympy and checked before it was written; none of the chapter’s own '
      'numbers is reused. Weights use the SIZE of g, 9.8 m/s², with the '
      'direction given in words — her sheet writes g = −9.8 m/s², and one card '
      'says outright that the minus is the direction, so the two never fight. '
      'The traps that get deliberate airtime: mass versus weight (a sort set '
      'drills it twelve ways, and the Moon questions offer the kilogram-for-'
      'newton swap as a wrong answer); the normal force is NOT automatically '
      'the weight (pressing down on a box raises it); apparent weight follows '
      'the acceleration, not the direction of travel (the elevator ranking '
      'puts "slowing down while going up" below the true weight); and the ≤ '
      'in F_fs ≤ μ_s F_N, which students read as = and then answer that '
      'static friction is always at its maximum. The pendulum-period formula '
      'is from the textbook and is not on her sheet; the card says so. ' + NOFBD,
      ('Do the mass-or-weight sort first — it takes two minutes and every later '
       'question leans on it. Then the quiz, writing F_N down before you touch '
       'friction every time.', 25),
      'content/phys-dyn1-weight.json',
      'Chapter 6, Forces (6.2 Using Newton’s Laws)',
      SRC6, offset_hours=3, libv_=1)

add_sorts('content/phys-dyn1-weight.json', 'unit-phys-dyn1-weight', [{
  'id': 's-mw', 'title': 'Mass or weight?',
  'a': 'Mass', 'b': 'Weight',
  'items': [
    {'t': 'Measured in kilograms', 'k': 'a',
     'why': 'The kilogram is the unit of mass. Forces are measured in newtons.'},
    {'t': 'Exactly the same on the Moon as on Earth', 'k': 'a',
     'why': 'The amount of matter does not change with location.'},
    {'t': 'Has no direction at all', 'k': 'a',
     'why': 'Mass is a scalar. A force always points somewhere.'},
    {'t': 'Why a loaded shopping cart is harder to get rolling than an empty one', 'k': 'a',
     'why': 'Resisting a change in velocity is inertia, and mass is the measure of inertia.'},
    {'t': 'How much matter an object contains', 'k': 'a',
     'why': 'That is the definition of mass.'},
    {'t': 'Would be unchanged for a rock floating far out in deep space', 'k': 'a',
     'why': 'Far from any planet the pull of gravity is tiny, but the rock’s matter is all still there.'},
    {'t': 'Measured in newtons', 'k': 'b',
     'why': 'The pull of gravity is a force, and forces are measured in newtons.'},
    {'t': 'Drops to about a sixth on the Moon', 'k': 'b',
     'why': 'F_g = mg, and the Moon’s g is about a sixth of Earth’s.'},
    {'t': 'Points straight down toward the centre of Earth', 'k': 'b',
     'why': 'It is a force, so it has a direction.'},
    {'t': 'What the spring in a bathroom scale is pushed by when you stand still', 'k': 'b',
     'why': 'A spring scale responds to force, so standing still it reads the pull of gravity on you.'},
    {'t': 'Found by multiplying by 9.8 near Earth’s surface', 'k': 'b',
     'why': 'F_g = mg turns kilograms into newtons.'},
    {'t': 'The pull Earth exerts on you', 'k': 'b',
     'why': 'That pull is the force of gravity on you, which is what the word means.'},
  ]}])

# =============================================================================
# 1-3 EQUILIBRIUM AND INCLINED PLANES  (chapter 7.1)
# =============================================================================
assert sp.sqrt(30**2 + 40**2) == 50
eq_ang = deg(sp.atan(sp.Rational(40, 30)))
assert eq(eq_ang, 1, 53.1) and eq(90 - eq_ang, 1, 36.9)
T_sign = 240 / (2 * S(30));               assert sp.simplify(T_sign - 240) == 0
assert eq(240 / (2 * Co(30)), 1, 138.6)
assert all(240 / (2 * S(a)) > 240 / (2 * S(b)) for a, b in [(10, 30), (20, 45), (5, 60)])
par = 400 * S(25); perp = 400 * Co(25)
assert eq(par, 0, 169) and eq(perp, 0, 363) and eq(400 * T(25), 0, 187)
distinct(par, perp, 400, 400 * T(25))
a_fl = g * S(20);                         assert eq(a_fl, 2, 3.35)
assert eq(g * Co(20), 2, 9.21) and eq(g * T(20), 2, 3.57)
distinct(a_fl, g * Co(20), g, g * T(20))
a_sl = g * (S(35) - sp.Rational(1, 10) * Co(35));   assert eq(a_sl, 2, 4.82)
assert eq(g * S(35), 2, 5.62) and eq(g * (S(35) + sp.Rational(1, 10) * Co(35)), 2, 6.42)
assert eq(g * (S(35) - sp.Rational(1, 10) * S(35)), 2, 5.06)
distinct(a_sl, g * S(35), g * (S(35) + sp.Rational(1, 10) * Co(35)), g * (S(35) - sp.Rational(1, 10) * S(35)))
v_sl = sp.Rational(482, 100) * 3;         assert eq(v_sl, 1, 14.5)
assert eq(sp.Rational(1, 2) * sp.Rational(482, 100) * 9, 1, 21.7)      # distance, not speed
mu_c = T(16);                             assert eq(mu_c, 2, 0.29)
assert eq(Co(16), 2, 0.96) and eq(1 / T(16), 2, 3.49)
distinct(mu_c, Co(16), 1 / T(16), 0)
assert eq(T(22), 2, 0.40) and T(22) < sp.Rational(45, 100)        # stays put
assert eq(S(22), 2, 0.37)
FNs = [Co(a) for a in (0, 20, 40, 60)]
assert all(FNs[i] > FNs[i + 1] for i in range(3))

C, Q = [], []
card(C, 'Forces at an angle: split them',
     '**Resolve every force into x and y components and solve the two '
     'directions separately.**\n'
     '• F_net,x = ma_x and F_net,y = ma_y are two separate equations.\n'
     '• This is the component method from Kinematics 2, used on forces '
     'instead of velocities.')
card(C, 'Equilibrium with several forces',
     '**An object is in equilibrium when the forces on it add to zero — '
     'drawn head to tail, the arrows close into a loop that ends where it '
     'began.**\n'
     '• In components: the x-parts add to zero AND the y-parts add to zero.\n'
     '• Three, four or ten forces: the rule is the same.')
card(C, 'Resultant',
     '**The resultant is the single force that has the same effect as all the '
     'forces on an object put together.**\n'
     '• It is the vector sum — the net force.')
card(C, 'Equilibrant',
     '**The equilibrant is the one extra force that would put an object in '
     'equilibrium: the same size as the resultant, pointing the opposite '
     'way.**\n'
     '• Find the resultant of the forces you have, then turn it round by 180°.\n'
     '• The resultant and the equilibrant together add to zero.',
     hint='Same size, opposite direction. Equal-and-opposite to the resultant.')
card(C, 'Two ropes holding a sign',
     '**When two ropes hold a weight, only their vertical components hold it '
     'up.**\n'
     '• For two ropes at the same angle θ above the horizontal: 2T sin θ = F_g.\n'
     '• The horizontal components pull against each other and cancel.',
     eq='2T sin θ = F_g')
card(C, 'Why shallow ropes snap',
     '**The flatter a rope is, the bigger the tension it needs to hold the '
     'same weight.**\n'
     '• A nearly horizontal rope has a tiny vertical component, so the tension '
     'must be huge to make up the weight.\n'
     '• That is why a picture should hang from steep wires, and why pushing '
     'sideways on the middle of a taut rope tied to a stuck car pulls the car '
     'with a big force.')
card(C, 'Tilt the axes on a slope',
     '**On a slope, put the x-axis along the slope and the y-axis '
     'perpendicular to it.**\n'
     '• The motion, the friction and the normal force then all lie along an '
     'axis.\n'
     '• Only the weight is at an angle — so it is the one force you have to '
     'resolve.')
card(C, 'Weight’s two parts on a slope',
     '**On a slope at angle θ, weight splits into F_g sin θ pulling down the '
     'slope and F_g cos θ pressing into the slope.**\n'
     '• The down-slope part is what makes things slide.\n'
     '• The into-slope part is what the normal force has to balance.',
     eq='down the slope: F_g sin θ     into the slope: F_g cos θ')
card(C, 'Which one is sine? Check the extremes',
     '**Test the formula at 0° and 90° and the sine and cosine can never swap '
     'by accident.**\n'
     '• At 0°, flat ground, nothing pulls an object along: sin 0° = 0. ✓\n'
     '• At 90°, a vertical wall, all the weight pulls along it: sin 90° = 1. ✓',
     frm='added', hint='Flat ground has no slope pull. That rules out cosine.')
card(C, 'The normal force on a slope is LESS than the weight',
     '**On a slope, F_N = F_g cos θ, which is smaller than the weight.**\n'
     '• The surface only has to balance the part of the weight pressing into '
     'it.\n'
     '• Steeper slope, smaller normal force, and so less friction too.',
     eq='F_N = F_g cos θ')
card(C, 'Sliding down a frictionless slope',
     '**With no friction, the acceleration down a slope is g sin θ — and the '
     'mass cancels.**\n'
     '• A heavy crate and a light box slide down the same smooth ramp with the '
     'same acceleration.',
     eq='a = g sin θ')
card(C, 'Sliding down with friction',
     '**Friction acts up the slope against a sliding object, so the '
     'acceleration is g(sin θ − μ_k cos θ).**\n'
     '• The friction uses the normal force, F_g cos θ — never the full weight.\n'
     '• The mass still cancels.',
     eq='a = g(sin θ − μ_k cos θ)')
card(C, 'Sliding at constant velocity',
     '**An object slides down a slope at constant velocity when μ_k = tan θ.**\n'
     '• Then friction exactly balances the down-slope pull, and the net force '
     'is zero.\n'
     '• Constant velocity does not mean "no friction" — it means friction is '
     'exactly big enough.')
card(C, 'Will it stay put?',
     '**An object rests on a slope without slipping as long as tan θ is no '
     'bigger than μ_s.**\n'
     '• Tilt a board slowly: the object starts to slide at the angle where '
     'tan θ = μ_s.')
card(C, 'Which way friction points on a slope',
     '**Friction always opposes the sliding: up the slope when the object '
     'slides down, and down the slope when it slides up.**\n'
     '• A skier coasting UP a slope has friction and the weight’s down-slope '
     'part both pulling back, so she slows quickly.')

# --- v2 (2026-10-27): the N1L assignment's two ideas the shelf lacked ------
# "Forces in N1L and N3L" (Drive, Dynamics 1) asks for a pull at an angle on a
# level floor (its normal force and its friction) with the angle given from the
# VERTICAL, and for two forces 30° apart added into a resultant and an
# equilibrant. Nothing on the shelf taught either: 1-2's only normal-force
# change is a straight-down press, and every resultant here was at 90°.
# Appended at the END of both lists so every existing id keeps its meaning.
# Fresh numbers throughout (never 7900 N / 1100 kg, 15 kg / 53° / 35 N,
# 400 N and 200 N at 30°, 70 kg / 650 N, 10 N / 8 N).
FN_ang = 20 * g - 80 * S(30);             assert FN_ang == 156
assert eq(20 * g - 80 * Co(30), 0, 127) and 20 * g + 80 * S(30) == 236
distinct(FN_ang, 20 * g, 20 * g + 80 * S(30), 20 * g - 80 * Co(30))
mu_p, m_p = sp.Rational(1, 5), 28
F_p = mu_p * m_p * g / (Co(35) + mu_p * S(35))
assert eq(F_p, 1, 58.8)
assert sp.simplify(F_p * Co(35) - mu_p * (m_p * g - F_p * S(35))) == 0   # constant velocity
assert eq(mu_p * m_p * g, 1, 54.9)                                        # pull as if horizontal
assert eq(mu_p * m_p * g / Co(35), 1, 67.0)                               # full weight as F_N
assert eq(mu_p * m_p * g / (Co(35) - mu_p * S(35)), 1, 77.9)              # lift counted as a press
distinct(F_p, mu_p * m_p * g, mu_p * m_p * g / Co(35), mu_p * m_p * g / (Co(35) - mu_p * S(35)))
hx_v = 60 * S(40);                        assert eq(hx_v, 1, 38.6)
assert eq(60 * Co(40), 1, 46.0) and eq(60 * T(40), 1, 50.3)
distinct(hx_v, 60 * Co(40), 60, 60 * T(40))
F_v = 24 / S(60);                         assert eq(F_v, 1, 27.7)
assert 24 / Co(60) == 48 and eq(24 * S(60), 1, 20.8)
distinct(F_v, 48, 24, 24 * S(60))
Rx2 = 300 + 150 * Co(40); Ry2 = 150 * S(40)
R2 = sp.sqrt(Rx2**2 + Ry2**2);            assert eq(R2, 0, 426)
assert sp.simplify(R2**2 - (300**2 + 150**2 + 2 * 300 * 150 * Co(40))) == 0
assert eq(deg(sp.atan(Ry2 / Rx2)), 1, 13.1)
assert eq(sp.sqrt(300**2 + 150**2), 0, 335)                               # as if at 90°
distinct(R2, 450, sp.sqrt(300**2 + 150**2), 150)
assert R2 < 450 and R2 > 300                                              # between max and sum

card(C, 'A pull at an angle lifts as well as drags',
     '**Pull a box along a level floor with the rope angled upward, and the '
     'rope’s upward part takes some of the weight, so the normal force — and '
     'the friction — get smaller.**\n'
     '• Angle θ above the horizontal: F_N = mg − F sin θ.\n'
     '• At constant velocity the forward part of the pull equals the '
     'friction: F cos θ = μ_k F_N.\n'
     '• Pushing DOWN at an angle does the opposite and adds to the normal '
     'force.',
     eq='F_N = mg − F sin θ   (θ above the horizontal)',
     hint='An upward pull lightens the load on the floor.')
card(C, 'Read where the angle is measured from',
     '**An angle measured from the VERTICAL swaps sine and cosine: the '
     'horizontal part becomes F sin θ and the vertical part F cos θ.**\n'
     '• From the horizontal: horizontal F cos θ, vertical F sin θ.\n'
     '• From the vertical: horizontal F sin θ, vertical F cos θ.\n'
     '• Check it at 0°: a pull at 0° to the vertical goes straight up, so its '
     'horizontal part must be zero — and sin 0° = 0.',
     frm='added', hint='Cosine sits next to the angle; the angle sits next to its reference line.')
card(C, 'Adding forces that are not at right angles',
     '**Split each force into components along one axis, add the x-parts and '
     'the y-parts, then recombine with Pythagoras.**\n'
     '• Lay the x-axis along one force: it is all x; the other has '
     'F cos θ along it and F sin θ across it.\n'
     '• The resultant is bigger than either force but smaller than their '
     'sum — the sum only happens when they point the same way.\n'
     '• The equilibrant (the ground holding a post still, say) is the same '
     'size as the resultant, pointing the opposite way.')

q(Q, 1, 'What is the equilibrant of a set of forces?',
  ['The single force that would cancel them: as big as their resultant, but opposite',
   'The single force with the same effect as all of them put together',
   'The biggest single force in the set, which the others must balance',
   'The force left over after the forces in the set cancel in pairs'],
  0, 'It is the force that PRODUCES equilibrium.',
  ['Add the forces to get their resultant.',
   'To make the total zero, the extra force must undo the resultant exactly.',
   'So it has the same size as the resultant and the opposite direction.',
   'That force is the equilibrant.'],
  '**The equilibrant is equal in size and opposite in direction to the '
  'resultant, so adding it makes the net force zero.** The single force with '
  'the same effect as all of them is the resultant itself — the equilibrant’s '
  'mirror image.',
  'Resultant: same effect. Equilibrant: cancels the effect.')

q(Q, 2, 'Two forces act on a ring: 30 N east and 40 N north. What third force '
        'would put the ring in equilibrium?',
  ['50 N, 53.1° south of west', '50 N, 53.1° north of east',
   '70 N, 53.1° south of west', '50 N, 36.9° south of west'],
  0, 'Find the resultant, then turn it round.',
  ['Resultant size: √(30² + 40²) = 50 N.',
   'Direction: tan⁻¹(40 ÷ 30) = 53.1° north of east.',
   'The equilibrant is the same size, pointing the opposite way.',
   'It is 50 N, 53.1° south of west.'],
  '**The resultant is 50 N at 53.1° north of east, so the equilibrant is '
  '50 N at 53.1° south of west.** 53.1° north of east is the resultant itself, '
  '70 N adds forces at right angles as if they were in a line, and 36.9° '
  'swaps which component is on the bottom of the ratio.',
  'Turn the resultant round 180°: north of east becomes south of west.')

q(Q, 1, 'Drawn head to tail, the forces on an object in equilibrium…',
  ['form a closed loop, ending exactly where they began',
   'form a straight line pointing the way the object moves',
   'form an open chain, with a gap the size of the weight',
   'form a loop that closes only if the object is at rest'],
  0, 'In equilibrium the forces add to zero.',
  ['Adding vectors head to tail, the sum runs from the first tail to the last head.',
   'In equilibrium the sum is zero.',
   'A sum of zero means the last head lands back on the first tail.',
   'So the arrows close into a loop.'],
  '**A zero sum means the chain of arrows closes up on itself.** That is just '
  'as true for an object moving at constant velocity as for one at rest — '
  'equilibrium is about the net force, not about standing still.',
  'Closed loop, zero net force.')

q(Q, 3, 'A 240 N sign hangs still from two ropes, each making 30° with the '
        'horizontal. What is the tension in each rope?',
  ['240 N', '120 N', '138.6 N', '480 N'],
  0, 'Only the vertical components hold the sign up.',
  ['The horizontal components cancel each other.',
   'The two vertical components hold up the weight: 2T sin 30° = 240 N.',
   'sin 30° = 0.5, so 2T × 0.5 = 240 N, which gives T = 240 N.',
   'Each rope has a tension of 240 N.'],
  '**2T sin 30° = 240 N, so each rope pulls with 240 N — as much as the whole '
  'sign weighs.** 120 N splits the weight in half as if the ropes were '
  'vertical; 138.6 N uses cosine, which is the horizontal component.',
  'Angled ropes always pull harder than half the weight.')

q(Q, 3, 'A painting hangs from two wires. If the wires are changed so they are '
        'closer to horizontal, what happens to the tension in them?',
  ['It increases, because each wire’s vertical part shrinks',
   'It decreases, because the wires now share the load better',
   'It stays the same, because the painting weighs the same',
   'It increases, because the painting gets heavier'],
  0, 'Which part of each wire’s pull is holding the painting up?',
  ['Only the vertical components hold up the weight: 2T sin θ = F_g.',
   'A flatter wire has a smaller angle θ, so a smaller sin θ.',
   'To make up the same weight, T must get bigger.',
   'The tension increases — which is why flat wires snap.'],
  '**T = F_g ÷ (2 sin θ), so a smaller angle means a bigger tension.** The '
  'weight is unchanged; it is the geometry that makes the wires work harder. '
  'Hang a painting from steep wires and they barely notice it.',
  'Flatter rope, bigger tension.')

q(Q, 2, 'A 400 N crate rests on a ramp inclined at 25°. What is the part of '
        'its weight that pulls it DOWN the ramp?',
  ['169 N', '363 N', '400 N', '187 N'],
  0, 'Down the slope is the sine part.',
  ['Down the slope: F_g sin θ.',
   'F_g sin 25° = 400 × 0.4226.',
   'That is 169 N.',
   'The down-slope part of the weight is 169 N.'],
  '**Down the slope is F_g sin θ = 400 sin 25° = 169 N.** 363 N is the cosine '
  'part, which presses INTO the ramp; 400 N is the whole weight; and 187 N '
  'uses tangent. Check it at 0°: flat ground has no down-slope pull, and '
  'sin 0° = 0.',
  'Sine runs down the slope. Test it at 0° if in doubt.')

q(Q, 2, 'A 400 N crate rests on a ramp inclined at 25°. What is the normal '
        'force from the ramp?',
  ['363 N', '400 N', '169 N', '437 N'],
  0, 'The ramp only has to balance the part of the weight pressing into it.',
  ['Perpendicular to the ramp, nothing accelerates.',
   'So the normal force balances the into-the-ramp part of the weight, F_g cos θ.',
   'F_N = 400 × cos 25° = 400 × 0.9063.',
   'The normal force is 363 N.'],
  '**On a slope F_N = F_g cos θ = 363 N — less than the full 400 N weight.** '
  'Writing F_N = mg out of habit is the trap: that is only true on level '
  'ground with nothing else pushing. 437 N would need something pressing the '
  'crate harder into the ramp.',
  'Normal force equals weight only on flat ground, with no extra push.')

q(Q, 3, 'A box slides down a frictionless ramp inclined at 20°. What is its '
        'acceleration?',
  ['3.35 m/s²', '9.21 m/s²', '9.8 m/s²', '3.57 m/s²'],
  0, 'Only the down-slope part of gravity accelerates it.',
  ['Along the ramp, the only force is F_g sin θ = mg sin θ.',
   'a = F_net ÷ m = g sin θ, and the mass cancels.',
   'a = 9.8 × sin 20° = 9.8 × 0.342.',
   'a = 3.35 m/s², down the ramp.'],
  '**a = g sin θ = 9.8 sin 20° = 3.35 m/s².** 9.21 m/s² uses cosine, 9.8 m/s² '
  'treats the ramp like a vertical drop, and 3.57 m/s² uses tangent.',
  'On a smooth slope, a = g sin θ — whatever the mass.')

q(Q, 3, 'A heavy crate and a light box slide down the same frictionless ramp. '
        'How do their accelerations compare?',
  ['They are equal, because the mass cancels',
   'The crate’s is bigger, because it is pulled harder',
   'The box’s is bigger, because it has less inertia',
   'The crate’s is bigger, because it presses harder'],
  0, 'Write out a = F_net ÷ m for each.',
  ['The down-slope force is mg sin θ.',
   'The acceleration is (mg sin θ) ÷ m.',
   'The m cancels, leaving g sin θ for both.',
   'The accelerations are equal.'],
  '**a = g sin θ has no mass in it: the bigger pull on the crate is exactly '
  'matched by its bigger inertia.** It is the slope version of a heavy and a '
  'light ball falling together — which is exactly what Galileo was using ramps '
  'to study.',
  'Bigger pull, bigger mass, same acceleration.')

q(Q, 3, 'A sled slides down a 35° snow slope with μ_k = 0.10. What is its '
        'acceleration?',
  ['4.82 m/s²', '5.62 m/s²', '6.42 m/s²', '5.06 m/s²'],
  0, 'Friction uses the NORMAL force, and it points up the slope.',
  ['Down the slope: g sin 35° = 5.62 m/s² worth of pull per kilogram.',
   'Friction per kilogram: μ_k g cos 35° = 0.10 × 9.8 × 0.819 = 0.80 m/s², up the slope.',
   'a = g(sin θ − μ_k cos θ) = 5.62 − 0.80.',
   'a = 4.82 m/s², down the slope.'],
  '**a = g(sin θ − μ_k cos θ) = 4.82 m/s².** 5.62 m/s² leaves friction out, '
  '6.42 m/s² adds it as if it helped, and 5.06 m/s² works out the friction '
  'from the sine part instead of the normal force.',
  'Friction always uses F_N, and on a slope F_N uses cosine.')

q(Q, 2, 'A sled starts from rest and accelerates down a slope at 4.82 m/s². '
        'How fast is it moving after 3.0 s?',
  ['14.5 m/s', '21.7 m/s', '1.6 m/s', '4.8 m/s'],
  0, 'Once you have a, the rest is kinematics.',
  ['Starting from rest, v_i = 0.',
   'v_f = v_i + at.',
   'v_f = 0 + 4.82 × 3.0.',
   'v_f = 14.5 m/s.'],
  '**v_f = v_i + at = 4.82 × 3.0 = 14.5 m/s.** 21.7 is ½at², which is the '
  'DISTANCE in metres, not a speed; 1.6 divides by the time; and 4.8 m/s is '
  'the acceleration with the wrong unit.',
  'Forces give you a. Kinematics does the rest.')

q(Q, 3, 'A box slides down a 16° ramp at a constant velocity. What is the '
        'coefficient of kinetic friction?',
  ['0.29', '0.96', '3.49', 'Zero — no friction is needed'],
  0, 'Constant velocity means the forces along the ramp balance.',
  ['Along the ramp, friction must equal the down-slope pull: μ_k mg cos θ = mg sin θ.',
   'Cancel mg: μ_k = sin θ ÷ cos θ = tan θ.',
   'μ_k = tan 16°.',
   'μ_k = 0.29.'],
  '**At constant velocity friction exactly balances the slope’s pull, so '
  'μ_k = tan θ = 0.29.** "Zero" is the moving-needs-a-force trap in reverse: '
  'without friction the box would speed up, not hold steady. 0.96 is cos 16° '
  'and 3.49 is the ratio upside down.',
  'Constant velocity on a slope: μ_k = tan θ.')

q(Q, 2, 'A block rests on a board tilted at 22°. The coefficient of static '
        'friction is 0.45. What happens?',
  ['It stays put: tan 22° = 0.40 is less than 0.45',
   'It slides: the angle is steeper than 0.45 radians',
   'It slides: any tilt at all makes a block slip',
   'It stays put only if the block is heavy enough'],
  0, 'Compare tan θ with μ_s.',
  ['The block slips once the down-slope pull beats the most static friction can give.',
   'mg sin θ ≤ μ_s mg cos θ cancels down to tan θ ≤ μ_s.',
   'tan 22° = 0.40, which is less than 0.45.',
   'So static friction can hold it, and it stays put.'],
  '**tan 22° = 0.40 is below μ_s = 0.45, so static friction is enough.** The '
  'mass cancels, so a heavier block slips at exactly the same angle — tilt the '
  'board to tan⁻¹ 0.45 = 24° and both go together.',
  'Holding still on a slope: tan θ ≤ μ_s. No mass in it.')

q(Q, 2, 'A skier finishes a run and coasts UP a short rise. Which way does '
        'friction on her point?',
  ['Down the slope, opposing her sliding up',
   'Up the slope, the way it always points on hills',
   'Straight down, the same as gravity',
   'Perpendicular to the slope, like the normal force'],
  0, 'Friction opposes the sliding, whatever the hill does.',
  ['Friction acts along the surface, against the direction of sliding.',
   'She is sliding up the slope.',
   'So friction points down the slope.',
   'Along with the down-slope part of her weight, it slows her quickly.'],
  '**Friction opposes the sliding, so for a skier sliding up it points down '
  'the slope.** It only points up the slope when she is sliding down. Here '
  'friction and gravity’s down-slope part both pull back, so she slows faster '
  'than she sped up.',
  'Find the sliding direction first. Friction is the other way.')

q(Q, 2, 'One box is placed on ramps of different steepness. Rank them '
        'from the LARGEST normal force to the SMALLEST.',
  ['On level ground', 'On a 20° ramp', 'On a 40° ramp', 'On a 60° ramp'],
  0, 'F_N = F_g cos θ. How does cos θ change as θ grows?',
  ['On a slope the normal force is F_g cos θ.',
   'cos 0° = 1, cos 20° = 0.94, cos 40° = 0.77, cos 60° = 0.50.',
   'cos θ gets smaller as the slope gets steeper.',
   'So level ground first, then 20°, 40° and 60°.'],
  '**F_N = F_g cos θ, which shrinks as the slope steepens — only on level '
  'ground does it equal the full weight.** At 60° the ramp holds up just half '
  'the box’s weight, which is also why friction is weaker on a steep slope.',
  'Steeper slope, smaller normal force.',
  kind='order')

q(Q, 3, 'A car is stuck in mud. A rope is tied tight between the car and a '
        'tree, and someone pushes sideways on the middle of the rope. Why can '
        'a modest push pull the car with a large force?',
  ['The rope is nearly straight, so a huge tension is needed to balance the push',
   'Pushing sideways adds the push to the rope’s tension along its length',
   'The tree pulls on the car as well, doubling whatever the person pushes',
   'Sideways pushes are always stronger than pulls made along a rope'],
  0, 'This is the shallow-rope sign problem turned on its side.',
  ['At the middle of the rope, the push is balanced by the two halves of the rope.',
   'The rope is almost straight, so each half has only a tiny component against the push.',
   'Tiny components must come from an enormous tension to balance the push.',
   'The enormous tension pulls along the rope, on the car.'],
  '**With the rope nearly straight, only a sliver of its tension opposes the '
  'push, so the tension has to be many times bigger than the push.** It is '
  'the two-rope sign in disguise: the flatter the rope, the bigger the '
  'tension.',
  'Nearly straight rope, enormous tension.')

q(Q, 2, 'A 20 kg crate is pulled across a level floor by a rope angled 30° '
        'above the horizontal, with a tension of 80 N. What is the normal force '
        'from the floor?',
  ['156 N', '196 N', '236 N', '127 N'],
  0, 'The rope’s upward part holds up some of the crate.',
  ['Weight: 20 × 9.8 = 196 N, down.',
   'The rope’s vertical part: 80 sin 30° = 40 N, up.',
   'Vertically nothing accelerates: F_N + 40 = 196.',
   'F_N = 156 N.'],
  '**The rope lifts with 80 sin 30° = 40 N, so the floor only has to supply '
  '196 − 40 = 156 N.** 196 N is the full weight, which is only right for a '
  'horizontal pull; 236 N adds the lift as if the rope pushed down; and 127 N '
  'uses cosine, which is the rope’s FORWARD part.',
  'Upward pull, smaller normal force.')

q(Q, 3, 'A 28 kg sled is pulled at constant velocity across level snow by a '
        'rope angled 35° above the horizontal. μ_k = 0.20. What is the tension '
        'in the rope?',
  ['58.8 N', '54.9 N', '67.0 N', '77.9 N'],
  0, 'The normal force is NOT the weight: the rope lifts.',
  ['Constant velocity: forward part = friction, so T cos 35° = μ_k F_N.',
   'Vertically: F_N = mg − T sin 35° = 274.4 − T sin 35°.',
   'So T cos 35° = 0.20(274.4 − T sin 35°), which gives T(cos 35° + 0.20 sin 35°) = 54.88.',
   'T = 54.88 ÷ 0.934 = 58.8 N.'],
  '**T = μ_k mg ÷ (cos θ + μ_k sin θ) = 58.8 N.** 54.9 N treats the rope as '
  'horizontal, 67.0 N splits the pull correctly but keeps the full weight as '
  'the normal force, and 77.9 N counts the rope’s lift as a push down.',
  'Write both directions before solving: the lift changes the friction.')

q(Q, 2, 'A box is pulled with 60 N by a rope at 40° to the VERTICAL. What is '
        'the horizontal part of the pull?',
  ['38.6 N', '46.0 N', '60.0 N', '50.3 N'],
  0, 'From the vertical, the horizontal part is the sine part.',
  ['The angle is measured from the vertical.',
   'The side opposite that angle is the horizontal part.',
   'Horizontal part = 60 sin 40° = 60 × 0.643.',
   'It is 38.6 N.'],
  '**Measured from the vertical, the horizontal part is F sin θ = 60 sin 40° = '
  '38.6 N.** 46.0 N uses cosine, as if the 40° were above the horizontal; '
  '60.0 N is the whole pull; and 50.3 N uses tangent. Check at 0°: a rope at '
  '0° to the vertical pulls straight up and has no horizontal part.',
  'Find the reference line first, then pick sine or cosine.')

q(Q, 3, 'A box slides along a level floor at constant velocity, pulled by a '
        'force at 60° to the VERTICAL. Kinetic friction on the box is 24 N. '
        'How big is the pull?',
  ['27.7 N', '48.0 N', '24.0 N', '20.8 N'],
  0, 'Constant velocity: the horizontal part of the pull equals the friction.',
  ['Horizontally nothing accelerates, so the pull’s horizontal part = 24 N.',
   'From the vertical, the horizontal part is F sin 60°.',
   'F sin 60° = 24, so F = 24 ÷ 0.866.',
   'F = 27.7 N.'],
  '**F sin 60° = 24 N, so F = 27.7 N.** 48.0 N reads the angle from the '
  'horizontal and divides by cos 60°; 24.0 N forgets the pull is at an angle; '
  'and 20.8 N multiplies by sin 60° instead of dividing.',
  'From the vertical: horizontal = F sin θ.')

q(Q, 3, 'Two ropes tied to a fence post pull on it with 300 N and 150 N, with '
        '40° between the ropes. What is the size of the resultant force on '
        'the post?',
  ['426 N', '450 N', '335 N', '150 N'],
  0, 'Lay the x-axis along the 300 N rope and split the other one.',
  ['Along the 300 N rope: 300 + 150 cos 40° = 300 + 114.9 = 414.9 N.',
   'Across it: 150 sin 40° = 96.4 N.',
   'Resultant: √(414.9² + 96.4²).',
   'It is 426 N, 13.1° from the 300 N rope.'],
  '**By components, 414.9 N along and 96.4 N across combine to 426 N.** 450 N '
  'adds them as if they pulled the same way, 335 N uses Pythagoras as if they '
  'were at 90°, and 150 N subtracts them as if they pulled against each other. '
  'With 40° between them the answer has to lie between 300 N and 450 N.',
  'Not at 90°? Components first, then Pythagoras.')

q(Q, 2, 'Two ropes tied to a fence post pull on it with 300 N and 150 N, with '
        '40° between the ropes, and the post does not move. What force does the '
        'ground exert on the post?',
  ['426 N, opposite the ropes’ resultant',
   '426 N, along the ropes’ resultant',
   '450 N, opposite the ropes’ resultant',
   '335 N, opposite the ropes’ resultant'],
  0, 'The ground supplies the equilibrant.',
  ['The two ropes have a resultant of 426 N (by components).',
   'The post stays still, so the net force on it is zero.',
   'The ground must supply the equilibrant: equal and opposite to the resultant.',
   'It pushes with 426 N, opposite the ropes’ resultant.'],
  '**The ground’s force is the equilibrant: the same 426 N as the ropes’ '
  'resultant, pointing the opposite way.** A force along the resultant would '
  'double it instead of cancelling it, and 450 N and 335 N come from adding '
  'the ropes as if in a line or at right angles.',
  'Holding still: the ground cancels the resultant exactly.')

build('ad-astra', C, Q, 'unit-phys-dyn1-incline',
      'Dynamics 1 · 1-3 Equilibrium and Inclined Planes', 'physics',
      'Forces that act at angles other than 90°: finding the net force and the '
      'equilibrant when three or more forces act, the tension in two ropes '
      'holding a weight, and the inclined plane — tilting the axes, splitting '
      'the weight into a down-slope part and an into-slope part, and finding '
      'the acceleration with and without friction.',
      'Real forces rarely line up neatly. Ramps, ropes at angles and hanging '
      'signs all come down to one method — resolve, then apply Newton’s laws '
      'in each direction — and the slope is the case every physics test '
      'reaches for, because it uses everything in 1-1 and 1-2 at once.',
      [('Determine the force that produces equilibrium when three forces act '
        'on an object.', 'source'),
       ('Analyse the motion of an object on an inclined plane with and without '
        'friction.', 'source')],
      'From chapter 7.1 (Forces in Two Dimensions). Section 7.2, projectile '
      'motion, is deliberately not built here: Kinematics 2 · 2-2 already '
      'teaches it from the same chapter. Every number was computed with sympy '
      'and checked; none of the chapter’s own (the 168 N sign, the 562 N '
      'trunk, the 62 kg skier) is reused. The trap with the most airtime is '
      'that the normal force on a slope is F_g cos θ, NOT the weight — a card, '
      'a question offering the full weight as the wrong answer, and a ranking '
      'of the same box on four slopes. Others: which of sine and cosine runs '
      'down the slope (a card teaches checking at 0° and 90°, which catches a '
      'swap without a calculator); "constant velocity means no friction" '
      '(offered as a wrong answer — it means friction is exactly big enough); '
      'and friction always using the normal force, never the full weight. '
      'It has since gained the N1L assignment’s two ideas the shelf lacked — a pull '
      'angled up a level floor (with the angle read from the vertical as well as '
      'the horizontal) shrinking the normal force and friction, and two forces '
      'that are not at right angles added by components, with the ground’s '
      'equilibrant. '
      + NOFBD,
      ('Do 1-1 and 1-2 first if you have not. Here, for every slope problem, '
       'write F_g sin θ and F_g cos θ before anything else.', 25),
      'content/phys-dyn1-incline.json',
      'Chapter 7, Forces and Motion in Two Dimensions (7.1 Forces in Two Dimensions)',
      SRC7, offset_hours=3, libv_=2)

# =============================================================================
# 1-4 CIRCULAR MOTION AND TORQUE  (chapter 7.3)
# =============================================================================
a_cyc = sp.Rational(6**2, 18);            assert a_cyc == 2
distinct(a_cyc, sp.Rational(6, 18), 6**2 * 18, sp.Rational(18, 6))
F_cur = sp.Rational(950 * 15**2, 45);     assert F_cur == 4750
assert eq(sp.Rational(950 * 15, 45), 0, 317) and 950 * g == 9310
distinct(F_cur, sp.Rational(950 * 15, 45), 950 * g, 950 * 15**2)
v_st = 2 * sp.pi * sp.Rational(8, 10) / sp.Rational(9, 10)
a_st = v_st**2 / sp.Rational(8, 10)
assert sp.simplify(a_st - 4 * sp.pi**2 * sp.Rational(8, 10) / sp.Rational(81, 100)) == 0
F_st = sp.Rational(5, 100) * a_st
assert eq(v_st, 2, 5.59) and eq(a_st, 1, 39.0) and eq(F_st, 2, 1.95)
assert eq(sp.Rational(5, 100) * g, 2, 0.49) and eq(sp.Rational(5, 100) * v_st / sp.Rational(8, 10), 2, 0.35)
distinct(F_st, sp.Rational(5, 100) * g, sp.Rational(5, 100) * v_st / sp.Rational(8, 10), a_st)
mu_min = sp.Rational(12**2, 30) / g;      assert eq(mu_min, 2, 0.49)
assert sp.Rational(144, 30) == sp.Rational(24, 5) and eq(sp.Rational(12, 30) / g, 3, 0.041)
assert eq(30 * g / 144, 2, 2.04)
ac = [sp.Rational(10**2, 4), sp.Rational(14**2, 10), sp.Rational(6**2, 3), sp.Rational(20**2, 50)]
assert [float(x) for x in ac] == [25.0, 19.6, 12.0, 8.0]
assert all(ac[i] > ac[i + 1] for i in range(3))   # D is the FASTEST but least
d_see = sp.Rational(30 * 2, 45);          assert eq(d_see, 2, 1.33)
distinct(d_see, 3, 2, 1)
tau = sp.Rational(25, 100) * 80;          assert tau == 20 and 80 / sp.Rational(25, 100) == 320
assert sp.Rational(2)**2 == 4 and sp.Rational(1, 2) == sp.Rational(6**2, 2 * 18) / a_cyc   # ×2 r halves a

C, Q = [], []
card(C, 'Uniform circular motion',
     '**Uniform circular motion is movement around a circle of fixed radius '
     'at constant speed.**\n'
     '• A rider on a merry-go-round, a sock in a spinning drum, a car on a '
     'steady roundabout.\n'
     '• Constant speed — but not constant velocity.')
card(C, 'Constant speed, still accelerating',
     '**An object moving in a circle at constant speed IS accelerating, '
     'because its direction keeps changing.**\n'
     '• Velocity is a vector; change its direction and you have changed the '
     'velocity.\n'
     '• So circular motion is never equilibrium, and there must be a net '
     'force.')
card(C, 'Velocity points along the tangent',
     '**At every instant, the velocity of an object moving in a circle '
     'points along the tangent — at right angles to the radius.**\n'
     '• Its length (the speed) stays the same; its direction turns.')
card(C, 'Centripetal acceleration',
     '**The acceleration of an object in uniform circular motion always '
     'points toward the centre of the circle, and its size is v² ÷ r.**\n'
     '• "Centripetal" means centre-seeking.',
     eq='a_c = v² / r')
card(C, 'Using the period',
     '**The period T is the time for one full trip around the circle; the '
     'speed is the circumference divided by it.**\n'
     '• v = 2πr ÷ T, so a_c = 4π²r ÷ T².',
     eq='v = 2πr / T     a_c = 4π²r / T²')
card(C, 'A net force toward the centre',
     '**To move in a circle, an object needs a net force pointing toward the '
     'centre, of size mv² ÷ r.**\n'
     '• This is the "= mv² / r" end of your sheet’s F_net = ma = mv² / r.\n'
     '• That end applies only to motion in a circle at constant speed.',
     eq='F_net = mv² / r')
card(C, 'Name the agent of the inward force',
     '**Something real must supply the inward pull: tension, friction, '
     'gravity or a normal force.**\n'
     '• A stone whirled on a string: the string’s tension.\n'
     '• A car on a flat bend: the road’s friction on the tyres.\n'
     '• Earth around the Sun: the Sun’s gravity. Clothes in a spin cycle: the '
     'drum wall pushing inward.')
card(C, '"Centripetal force" is not an extra force',
     '**Centripetal force is the name for whichever real force points toward '
     'the centre — never an additional force to draw on the diagram.**\n'
     '• On a free-body diagram, draw tension, friction or gravity, labelled by '
     'its agent. Never a separate arrow called "centripetal".')
card(C, 'Let go and it flies off along the tangent',
     '**Release an object moving in a circle and it travels in a straight '
     'line along the tangent — the way it was moving at that instant.**\n'
     '• Not outward from the centre, and not on around the curve.\n'
     '• A hammer thrower releases at the moment the tangent points down the '
     'field.')
card(C, 'There is no centrifugal force',
     '**The outward "centrifugal force" you seem to feel on a turn does not '
     'exist.**\n'
     '• When a car turns left, you keep going straight, by the first law, '
     'until the door pushes you inward.\n'
     '• The force you actually feel is the door pushing you toward the centre '
     'of the turn.',
     hint='No agent, no force. Nothing out there is pushing you outward.')
card(C, 'Speed counts twice',
     '**The centripetal acceleration depends on the SQUARE of the speed: '
     'double the speed and it quadruples.**\n'
     '• That is why taking a bend at twice the speed needs four times the '
     'grip.')
card(C, 'A wider circle is gentler',
     '**At the same speed, a bigger radius means a smaller centripetal '
     'acceleration: double the radius and it halves.**\n'
     '• Tight bends are the dangerous ones.')
card(C, 'Rigid rotating objects',
     '**A rigid rotating object spins about its own axis — a door on its '
     'hinges, a merry-go-round, a wheel.**\n'
     '• What changes how it rotates is not just a force, but where and in '
     'which direction the force is applied.')
card(C, 'Lever arm',
     '**The lever arm is the perpendicular distance from the axis of rotation '
     'to the line along which a force acts.**\n'
     '• Push far from the hinge and at right angles to the door: long lever '
     'arm.\n'
     '• Push toward the hinge: the line of the force runs through the axis, '
     'so the lever arm is zero.')
card(C, 'Torque',
     '**Torque is force times lever arm, and it does for rotation what force '
     'does for straight-line motion.**\n'
     '• More torque, bigger change in rotation. Measured in N·m.\n'
     '• This formula is from the textbook; it is not on your sheet.',
     eq='τ = F × lever arm')
card(C, 'Balancing a seesaw',
     '**A seesaw balances when the two torques are equal: weight × distance '
     'on one side equals weight × distance on the other.**\n'
     '• The heavier person sits closer to the pivot.\n'
     '• A triple-beam balance works on exactly this idea.',
     eq='m_A g d_A = m_B g d_B')

q(Q, 1, 'An object moves around a circle at a steady speed. Which way does '
        'its acceleration point?',
  ['Toward the centre of the circle', 'Along the tangent, the way it moves',
   'Outward, away from the centre', 'Nowhere — a steady speed means no acceleration'],
  0, 'What is changing about its velocity?',
  ['The speed is not changing, but the direction is.',
   'The change in velocity between two nearby moments points toward the centre.',
   'Acceleration points the same way as the change in velocity.',
   'So the acceleration points toward the centre.'],
  '**Toward the centre — centripetal means centre-seeking.** A steady speed '
  'is not a steady velocity, because the direction is changing all the time. '
  'Along the tangent is the direction of the VELOCITY, and outward is the '
  'direction of a force that does not exist.',
  'Velocity along the tangent; acceleration toward the centre.')

q(Q, 1, 'A rider goes round on a merry-go-round at a constant speed. Is she '
        'in equilibrium?',
  ['No — her direction is changing, so she is accelerating',
   'Yes — her speed is constant, so nothing is changing',
   'Yes — the forces on her balance out at every moment',
   'No — her speed rises and falls as she goes round'],
  0, 'Equilibrium needs constant VELOCITY.',
  ['Equilibrium means zero net force, which means constant velocity.',
   'Her speed is constant, but her direction keeps changing.',
   'A changing direction is a changing velocity, which is an acceleration.',
   'So she is not in equilibrium; a net force points to the centre.'],
  '**Not in equilibrium: constant speed in a circle is still an acceleration, '
  'so there must be a net force toward the centre.** Speed and velocity are '
  'different things, and circular motion is exactly where the difference '
  'matters.',
  'Turning counts as accelerating.')

q(Q, 2, 'A cyclist rides around a curve of radius 18 m at a steady 6.0 m/s. '
        'What is her centripetal acceleration?',
  ['2.0 m/s²', '0.33 m/s²', '648 m/s²', '3.0 m/s²'],
  0, 'a_c = v² / r.',
  ['a_c = v² ÷ r.',
   'v² = 6.0² = 36.',
   'a_c = 36 ÷ 18.',
   'a_c = 2.0 m/s², toward the centre of the curve.'],
  '**a_c = v² ÷ r = 36 ÷ 18 = 2.0 m/s².** 0.33 m/s² forgets to square the '
  'speed, 648 m/s² multiplies by the radius, and 3.0 m/s² divides the radius '
  'by the speed.',
  'Square the speed, then divide by the radius.')

q(Q, 2, 'A 950 kg car rounds a flat curve of radius 45 m at a steady 15 m/s. '
        'What size of net force acts on it?',
  ['4750 N', '317 N', '9310 N', '213 750 N'],
  0, 'Your sheet: F_net = mv² / r.',
  ['F_net = mv² ÷ r.',
   'F_net = 950 × 15² ÷ 45.',
   'F_net = 950 × 225 ÷ 45.',
   'F_net = 4750 N, toward the centre of the curve.'],
  '**F_net = mv² ÷ r = 950 × 225 ÷ 45 = 4750 N, pointing toward the '
  'centre.** 317 N forgets to square v, 9310 N is the car’s weight, and '
  '213 750 N forgets to divide by the radius.',
  'mv² over r. Square only the v.')

q(Q, 2, 'A car rounds a flat, unbanked curve at a steady speed. What supplies '
        'the force that keeps it on the curve?',
  ['Friction from the road on the tyres, pointing to the centre',
   'An outward centrifugal force balancing the turn',
   'The car’s weight, pulling it around the bend',
   'The engine, pushing the car into the turn'],
  0, 'Name a real force with an agent that points toward the centre.',
  ['The inward force must come from something touching the car or from gravity.',
   'Weight points straight down, not toward the centre of the curve.',
   'The road touches the tyres, and its sideways friction can point inward.',
   'So road friction supplies the inward force.'],
  '**The road’s friction on the tyres points toward the centre and keeps the '
  'car turning.** Weight is vertical, and centrifugal force has no agent, so '
  'it is not a real force. On ice there is no grip, and the car carries '
  'straight on.',
  'Name the agent. On a flat road it is friction.')

q(Q, 3, 'A 0.050 kg stopper on a 0.80 m string is whirled in a horizontal '
        'circle, making one revolution every 0.90 s. What is the tension in '
        'the string?',
  ['1.95 N', '0.49 N', '0.35 N', '39.0 N'],
  0, 'Find the speed from the period, then use F_net = mv² / r.',
  ['v = 2πr ÷ T = 2π × 0.80 ÷ 0.90 = 5.59 m/s.',
   'a_c = 4π²r ÷ T² = 4π² × 0.80 ÷ 0.90² = 39.0 m/s².',
   'The tension is the inward force: F_T = m a_c = 0.050 × 39.0.',
   'F_T = 1.95 N.'],
  '**v = 2πr ÷ T = 5.59 m/s, so F_T = mv² ÷ r = 1.95 N.** 0.49 N is the '
  'stopper’s weight, 0.35 N forgets to square the speed, and 39.0 is the '
  'acceleration, which still has to be multiplied by the mass.',
  'Period → speed → acceleration → force. One step at a time.')

q(Q, 3, 'A car rounds a curve, then rounds it again at twice the speed. How '
        'does the net force needed to keep it on the curve change?',
  ['It becomes four times as big', 'It becomes twice as big',
   'It stays the same', 'It becomes half as big'],
  0, 'How does v appear in mv² / r?',
  ['F_net = mv² ÷ r.',
   'Doubling v multiplies v² by 2² = 4.',
   'The mass and radius are unchanged.',
   'So the force needed is four times as big.'],
  '**Speed is squared in mv² ÷ r, so twice the speed needs four times the '
  'force.** That is why a bend you can take comfortably at 30 km/h can throw '
  'a car off the road at 60.',
  'Speed counts twice.')

q(Q, 3, 'A runner keeps the same speed but switches to a track with twice the '
        'radius. How does her centripetal acceleration change?',
  ['It halves', 'It doubles', 'It stays the same', 'It becomes a quarter'],
  0, 'Where is r in a_c = v² / r?',
  ['a_c = v² ÷ r.',
   'v is unchanged; r is doubled.',
   'Doubling the bottom of the fraction halves its value.',
   'The centripetal acceleration halves.'],
  '**r is on the bottom of v² ÷ r, so twice the radius halves the '
  'acceleration.** A quarter is what squaring would give, but the radius is '
  'not squared — only the speed is.',
  'Wider circle, gentler turn.')

q(Q, 2, 'A ball whirled on a string in a horizontal circle is suddenly '
        'released. Seen from above, in what direction does it fly off?',
  ['Straight along the tangent, the way it was moving',
   'Straight outward, away from the centre of the circle',
   'Along a curve that carries on around the circle',
   'Straight inward, toward the centre of the circle'],
  0, 'What force acts sideways on it once the string lets go?',
  ['Just before release, its velocity points along the tangent.',
   'Once released, the string’s inward pull is gone.',
   'With no sideways force, by the first law it keeps its velocity.',
   'So it moves straight along the tangent (while gravity pulls it down).'],
  '**Released, it keeps the velocity it had — along the tangent — and moves '
  'in a straight line.** It only curved because the string kept pulling it '
  'in. "Straight outward" is the centrifugal-force picture, and there is no '
  'force to cause it.',
  'Let go, and it goes the way it was already going.')

q(Q, 3, 'A car turns sharply to the left and you slide toward the right-hand '
        'door. What is really happening?',
  ['You keep moving straight while the car turns, until the door pushes you inward',
   'An outward centrifugal force throws you to the right as the car turns left',
   'The car’s friction pushes you to the right, away from the turn',
   'Your inertia is a force, and it pushes you outward on every turn'],
  0, 'Name the agent of each force offered.',
  ['Before the turn, you are moving straight ahead with the car.',
   'The car turns left; nothing has yet pushed you left, so you keep going '
   'straight, by the first law.',
   'Relative to the turning car, that looks like sliding right.',
   'When you reach the door, it pushes you left — toward the centre of the turn.'],
  '**Nothing pushes you outward: you keep going straight, and the car turns '
  'under you until the door pushes you inward.** Centrifugal force has no '
  'agent, and inertia is a property, not a force. The only real sideways force '
  'here points toward the centre.',
  'If you cannot name the agent, the force is not there.')

q(Q, 3, 'A car takes a flat curve of radius 30 m at 12 m/s. What is the '
        'smallest coefficient of static friction that keeps it from '
        'skidding?',
  ['0.49', '4.8', '0.041', '2.04'],
  0, 'Friction must supply mv² / r, and it can give at most μ_s mg.',
  ['The inward force needed is mv² ÷ r; friction must supply it.',
   'The most friction can give is μ_s F_N = μ_s mg on a flat road.',
   'μ_s mg = mv² ÷ r, so μ_s = v² ÷ (rg) = 144 ÷ (30 × 9.8).',
   'μ_s must be at least 0.49.'],
  '**Friction must supply mv² ÷ r, so μ_s ≥ v² ÷ (rg) = 0.49.** The mass '
  'cancels, so a truck and a car need the same grip on the same curve at the '
  'same speed. 4.8 is the acceleration, not the coefficient, and 0.041 forgets '
  'to square the speed.',
  'Grip needed = v² / (rg). No mass.')

q(Q, 3, 'Rank these objects in circular motion from the GREATEST centripetal '
        'acceleration to the LEAST.',
  ['A: 10 m/s around a 4.0 m radius', 'B: 14 m/s around a 10 m radius',
   'C: 6.0 m/s around a 3.0 m radius', 'D: 20 m/s around a 50 m radius'],
  0, 'Work out v² / r for each — the fastest is not automatically first.',
  ['A: 10² ÷ 4.0 = 25 m/s².',
   'B: 14² ÷ 10 = 19.6 m/s².',
   'C: 6.0² ÷ 3.0 = 12 m/s². D: 20² ÷ 50 = 8.0 m/s².',
   'So A, then B, then C, then D.'],
  '**A (25), B (19.6), C (12), D (8.0) m/s².** D is the fastest object here '
  'but has the smallest acceleration, because its circle is so wide. Speed '
  'alone does not decide it; v² and r both do.',
  'Compute v² / r. Never rank by speed alone.',
  kind='order')

q(Q, 1, 'What is torque?',
  ['A force multiplied by its lever arm about an axis',
   'The force that pulls an object toward the centre',
   'The speed at which an object spins about its axis',
   'A force that acts straight through the axis'],
  0, 'It is what changes rotation.',
  ['To turn something about an axis, both the force and where it acts matter.',
   'The lever arm is the perpendicular distance from the axis to the force’s line.',
   'Torque combines the two: force times lever arm.',
   'Torque is force × lever arm.'],
  '**Torque is force times lever arm, and it plays the role for rotation '
  'that force plays for straight-line motion.** A force through the axis has '
  'zero lever arm, so it produces no torque at all.',
  'Same force, longer lever arm, more torque.')

q(Q, 2, 'Why is a door handle put on the edge farthest from the hinges?',
  ['A longer lever arm gives more torque for the same push',
   'The door is lighter there, so it is easier to move',
   'Pushing near the hinges would bend the door',
   'The hinges only allow forces at the far edge'],
  0, 'Torque = force × lever arm.',
  ['The hinges are the axis of rotation.',
   'Pushing at the far edge gives the longest possible lever arm.',
   'Torque is force × lever arm, so the same push gives the most torque there.',
   'More torque means the door swings open more easily.'],
  '**The far edge gives the longest lever arm, so the same push gives the '
  'most torque.** Push right next to the hinges and even a hard shove barely '
  'turns the door; push toward the hinges and it does not turn at all.',
  'Push far from the axis, at right angles.')

q(Q, 2, 'A 0.25 m wrench is pushed with 80 N at right angles to the handle, '
        'at its end. What torque does it apply to the nut?',
  ['20 N·m', '320 N·m', '80 N·m', '0.0031 N·m'],
  0, 'Torque = force × lever arm.',
  ['The force is at right angles, so the lever arm is the full 0.25 m.',
   'τ = F × lever arm.',
   'τ = 80 × 0.25.',
   'τ = 20 N·m.'],
  '**τ = 80 N × 0.25 m = 20 N·m.** 320 N·m divides the force by the length, '
  '80 N·m forgets the lever arm altogether, and 0.0031 N·m divides the '
  'length by the force. A longer wrench, same push, more torque — which is '
  'why stuck nuts get a pipe slipped over the handle.',
  'Force times distance from the axis.')

q(Q, 3, 'A 30 kg child sits 2.0 m from the pivot of a seesaw. Where must a '
        '45 kg child sit, on the other side, to balance it?',
  ['1.3 m from the pivot', '3.0 m from the pivot',
   '2.0 m from the pivot', '1.0 m from the pivot'],
  0, 'Balanced means equal torques on each side.',
  ['Balance: m_A g d_A = m_B g d_B, and g cancels.',
   '30 × 2.0 = 45 × d.',
   'd = 60 ÷ 45.',
   'd = 1.3 m from the pivot.'],
  '**Equal torques: 30 × 2.0 = 45 × d, so d = 1.3 m — the heavier child sits '
  'closer in.** 3.0 m runs the ratio backwards, putting the heavier child '
  'farther out; 2.0 m assumes equal distances balance unequal weights.',
  'Heavier person, shorter lever arm.')

build('ad-astra', C, Q, 'unit-phys-dyn1-circle',
      'Dynamics 1 · 1-4 Circular Motion and Torque', 'physics',
      'Motion in a circle at constant speed: why it is still acceleration, '
      'why that acceleration points to the centre with size v² ÷ r, what '
      'real force supplies it in each situation, why there is no outward '
      '"centrifugal" force, and what happens when the inward force lets go. '
      'Then the first idea of rotation: lever arms, torque, and how a seesaw '
      'balances.',
      'Bends in roads, spinning rides, orbiting planets and thrown hammers are '
      'all the same problem, and it is the one place where constant speed and '
      'constant velocity part company for good. It is also on your sheet — '
      'the "= mv² / r" at the end of the Newton’s-laws row is this lesson.',
      [('Explain the acceleration of an object moving in a circle at constant '
        'speed.', 'source'),
       ('Describe how centripetal acceleration depends upon the object’s speed '
        'and the radius of the circle.', 'source'),
       ('Recognise the direction of the force that causes centripetal '
        'acceleration.', 'source'),
       ('Explain how the rate of circular motion is changed by exerting torque '
        'on it.', 'source')],
      'From chapter 7.3 (Circular Motion). Built because her own equation '
      'sheet carries F_net = ma = mv² / r, but with one caution: no objective '
      'list was in the Dynamics 1 folder, so whether her class covers 7.3 in '
      'this unit or a later one is not known — approve it, or hold it with a '
      'later release date, whichever fits. Every number was computed with '
      'sympy and checked; none of the chapter’s own (the 13 g stopper, the '
      '8.8 m/s runner, the 32 m/s car) is reused. The trap with the most '
      'airtime is centrifugal force: two cards and two questions say plainly '
      'that the outward push you feel on a turn has no agent and does not '
      'exist, and that a released object flies off along the tangent, not '
      'outward. Torque is a short final section, and its formula (like the '
      'seesaw balance) is from the textbook and is not on her sheet; the '
      'cards say so. ' + NOFBD,
      ('Learn the two directions first — velocity along the tangent, '
       'acceleration to the centre — then the quiz. For every question, name '
       'what is supplying the inward force.', 20),
      'content/phys-dyn1-circle.json',
      'Chapter 7, Forces and Motion in Two Dimensions (7.3 Circular Motion)',
      SRC7, offset_hours=3, libv_=1)

print('  all sympy assertions passed; sorts attached to 1-1 and 1-2')
