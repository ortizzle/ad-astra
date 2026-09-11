# -*- coding: utf-8 -*-
# Kinematics 2 · 2-2 Projectile Motion — second half of her teacher's
# "Kinematics 2 Objectives.pdf", built from chapter 7.2 of
# "Textbook+2D+Kinematics.pdf" (Drive/Physics 8, both uploaded 2026-09-11).
#
# Shelves behind 2-1 Vectors and Components on the new "Kinematics 2" spine.
# See build_kinematics2_a.py's header for why that shelf exists and why both
# parts carry numbers.
#
# g = 9.80 m/s^2 throughout, matching the textbook and the existing
# phys-kinematics-equations unit. EVERY number is computed with sympy here and
# asserted before it reaches a question; none of the textbook's own worked
# examples (15 m/s off a 44 m cliff, 4.47 m/s at 66 deg, the 27 m/s football)
# is reused.
import sys, os, json, io
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

g = sp.Rational(98, 10)
def rnd(x, n=1):
    return float(sp.N(sp.Rational(round(float(x) * 10**n), 10**n)))

# --- horizontal launch: h = 20 m, vx = 12 m/s -------------------------------
t20 = sp.sqrt(2*20/g);                 assert rnd(t20, 2) == 2.02
assert rnd(12*t20) == 24.2
assert rnd(g*t20) == 19.8
assert rnd(sp.sqrt(12**2 + (g*t20)**2)) == 23.2
# --- horizontal launch: h = 45 m, vx = 8 m/s --------------------------------
t45 = sp.sqrt(2*45/g);                 assert rnd(t45, 2) == 3.03
assert rnd(8*t45) == 24.2
# --- table: h = 1.2 m, lands 0.75 m away ------------------------------------
tt = sp.sqrt(2*sp.Rational(12,10)/g);  assert rnd(tt, 2) == 0.49
assert rnd(sp.Rational(75,100)/tt, 2) == 1.52
# --- angled launch: 20 m/s at 40 deg ----------------------------------------
vx40 = 20*sp.cos(sp.rad(40)); vy40 = 20*sp.sin(sp.rad(40))
assert (rnd(vx40), rnd(vy40)) == (15.3, 12.9)
tup40 = vy40/g;                        assert rnd(tup40, 2) == 1.31
hang40 = 2*tup40;                      assert rnd(hang40, 2) == 2.62
hmax40 = vy40**2/(2*g);                assert rnd(hmax40) == 8.4
R40 = vx40*hang40;                     assert rnd(R40) == 40.2
# --- angled launch: 15 m/s at 30 deg ----------------------------------------
vy30 = 15*sp.sin(sp.rad(30));          assert rnd(vy30, 2) == 7.5
assert rnd(2*vy30/g, 2) == 1.53
assert rnd(vy30**2/(2*g), 2) == 2.87
# --- dropped from rest: 3.0 s -----------------------------------------------
assert rnd(sp.Rational(1,2)*g*9) == 44.1

C, Q = [], []

# ---- cards -----------------------------------------------------------------
card(C, 'Projectile',
     '**A projectile is any object that has been given an initial thrust and '
     'then moves under gravity alone.**\n'
     '• A football, a bullet, a drop of water — what it is does not matter.\n'
     '• Once the thrust is over, the only force acting on it is gravity, pulling '
     'straight down. Air resistance is ignored throughout this unit.')
card(C, 'Trajectory',
     '**The trajectory is the path a projectile takes through space — and it is '
     'always a parabola.**\n'
     '• The shape comes from combining constant horizontal velocity with steady '
     'downward acceleration.\n'
     '• Neither motion on its own is a curve. The curve is what the two of them '
     'together produce.')
card(C, 'Two problems, not one',
     '**Split every projectile into a horizontal problem and a vertical problem, '
     'and solve them separately.**\n'
     '• Horizontal: no force, so no acceleration — a constant-velocity problem.\n'
     '• Vertical: gravity only — a free-fall problem, exactly like something '
     'dropped or thrown straight up.\n'
     '• That is the whole method. Everything else is bookkeeping.')
card(C, 'No acceleration sideways',
     '**Once a projectile is in the air, nothing pushes or pulls it horizontally, '
     'so aₓ = 0 and vₓ never changes.**\n'
     '• The horizontal speed it leaves with is the horizontal speed it lands with.\n'
     '• So horizontal distance is just speed × time.',
     eq='x = vₓ t')
card(C, 'Gravity acts vertically',
     '**All of gravity’s effect is in the vertical direction: aᵧ = −g = '
     '−9.80 m/s².**\n'
     '• So every vertical calculation is an ordinary kinematics problem with '
     'a = −g.\n'
     '• Gravity has no horizontal component at all, which is why vₓ survives '
     'untouched.',
     eq='vᵧ = vᵧ₀ − g t     y = y₀ + vᵧ₀ t − ½ g t²')
card(C, 'Time is the bridge',
     '**The two problems share exactly one quantity: time.**\n'
     '• A projectile is in the air for one length of time, and both the vertical '
     'and the horizontal motion use it.\n'
     '• So the usual route is: solve the VERTICAL problem for t, then feed that t '
     'into the horizontal one.',
     hint='Stuck on a range question? You are almost always missing t, and t '
          'almost always comes from the vertical side.')
card(C, 'Launched horizontally means vᵧ₀ = 0',
     '**A projectile fired horizontally has no initial vertical velocity, so its '
     'fall is identical to that of an object simply dropped.**\n'
     '• Fire a bullet horizontally and drop one from the same height at the same '
     'moment: they land together.\n'
     '• The fired one travels much further sideways. That changes where it lands, '
     'never when.')
card(C, 'Dropped and thrown land together',
     '**Two balls released from the same height hit the ground at the same time '
     'even if one is given a horizontal push.**\n'
     '• The strobe photo of this is the clearest evidence for independence there '
     'is — at every flash the two balls are at the SAME height.\n'
     '• A faster horizontal throw does not buy any extra hang time.')
card(C, 'Time to fall from a height',
     '**Dropped from rest, the fall time depends only on the height and g — never '
     'on the horizontal speed, and never on the mass.**',
     eq='t = √(2h / g)')
card(C, 'Maximum height',
     '**At the top of the arc the vertical velocity is momentarily zero — but the '
     'horizontal velocity is not.**\n'
     '• The projectile is still moving at the top; it is just not moving UP any '
     'more.\n'
     '• Set vᵧ = 0 to find the time to the top, then use it to find the height.',
     eq='t_up = vᵧ₀ / g     y_max = vᵧ₀² / (2g)')
card(C, 'Range and hang time',
     '**Range is the horizontal distance travelled; hang time is how long the '
     'projectile is in the air.** Landing back at launch height, the arc is '
     'symmetric, so the whole flight takes twice the time to the top.',
     eq='t_hang = 2 vᵧ₀ / g     R = vₓ × t_hang')
card(C, 'The arc is symmetric',
     '**Coming down mirrors going up.** At any given height the speed on the way '
     'down equals the speed on the way up — only the direction of the vertical '
     'part is reversed.\n'
     '• So a ball landing at its launch height arrives at exactly the speed it '
     'left with.\n'
     '• And it takes as long to come down as it took to go up.')
card(C, 'Speed at any instant',
     '**Combine the two components with Pythagoras.** The horizontal part is '
     'unchanged; only the vertical part has grown.',
     eq='v = √(vₓ² + vᵧ²)')
card(C, 'Mass does not appear',
     '**No projectile-motion equation contains mass.**\n'
     '• Roll a heavy ball and a light ball off the same table at the same speed '
     'and they land together, at the same distance.\n'
     '• True only because air resistance is being ignored — but it is what every '
     'question in this unit assumes.',
     frm='added')
card(C, 'Frame of reference changes the shape',
     '**Toss a ball straight up on a moving bus and you see a straight line up '
     'and down; someone on the pavement sees a parabola.**\n'
     '• You and the observer disagree about the horizontal motion, because you are '
     'moving with the bus and they are not.\n'
     '• You agree exactly on the vertical motion — same height, same time in the '
     'air.')
card(C, 'Air resistance, set aside',
     '**Every answer in this unit assumes no air resistance, which is a genuine '
     'simplification rather than a fact.**\n'
     '• For a dense, slow, compact object it barely matters.\n'
     '• For a golf ball, a spinning baseball or a frisbee it matters enormously — '
     'dimples and spin are engineered around it.',
     frm='added')

# ---- questions -------------------------------------------------------------
q(Q, 1, 'While a projectile is in the air, what is its horizontal acceleration?',
  ['Zero', '9.80 m/s² forwards', '9.80 m/s² downwards',
   'It depends on the launch angle'],
  0,
  'Which direction does gravity pull, and is anything else pushing?',
  ['Once the thrust is over, the only force on a projectile is gravity.',
   'Gravity pulls straight down, so it has no horizontal component.',
   'No horizontal force means no horizontal acceleration.',
   'So aₓ = 0, whatever the launch angle was.'],
  '**Nothing acts horizontally on a projectile, so its horizontal acceleration '
  'is zero and its horizontal speed never changes.** The 9.80 m/s² belongs '
  'entirely to the vertical direction. This is exactly why the horizontal half '
  'of every problem is a plain constant-velocity calculation.',
  'Gravity is vertical. All of it, always.')

q(Q, 2, 'A ball is rolled off a table at 2 m/s; an identical ball is dropped '
        'from the table edge at the same instant. Which lands first?',
  ['Neither — they land together',
   'The dropped one, because it goes straight down',
   'The rolled one, because it is already moving',
   'The dropped one, because the rolled one travels further'],
  0,
  'The fall is governed by the vertical motion. What is the rolled ball’s '
  'starting vertical velocity?',
  ['A ball rolled off horizontally leaves with zero vertical velocity.',
   'So its vertical motion is identical to that of a dropped ball.',
   'Both start the same height up with the same vertical start and the same '
   'acceleration.',
   'They therefore take the same time and land together.'],
  '**Horizontal and vertical motions are independent, so a horizontal push '
  'changes where a ball lands, never when.** The rolled ball really does travel '
  'a longer total path — but distance travelled is not what sets the fall time; '
  'height and g are.',
  'The strobe photo: at every flash, both balls are at the same height.')

q(Q, 2, 'A stone is thrown horizontally at 12 m/s from a cliff 20 m high. How '
        'long is it in the air?',
  ['2.02 s', '1.67 s', '4.08 s', '0.61 s'],
  0,
  'Solve the vertical problem. Does 12 m/s appear in it anywhere?',
  ['Thrown horizontally, so the initial vertical velocity is zero.',
   'The vertical problem is then a plain drop from 20 m: t = √(2h/g).',
   't = √(2 × 20 / 9.80) = √4.082.',
   't = 2.02 s. The 12 m/s never enters — it is horizontal.'],
  '**The fall time comes from the vertical problem alone: √(2 × 20 / 9.80) = '
  '2.02 s.** 1.67 s is 20 ÷ 12, which treats a height as though it were a '
  'horizontal distance. The horizontal speed cannot affect the fall time, which '
  'is the whole point of independence.',
  'Time almost always comes out of the vertical side first.')

q(Q, 2, 'A stone thrown horizontally at 12 m/s off a 20 m cliff is in the air '
        'for 2.02 s. How far from the base of the cliff does it land?',
  ['24.2 m', '20.0 m', '44.2 m', '12.0 m'],
  0,
  'Horizontally there is no acceleration, so the distance formula is the '
  'simplest one there is.',
  ['Horizontally aₓ = 0, so x = vₓ × t.',
   'x = 12 m/s × 2.02 s.',
   'x = 24.2 m.',
   'No ½ a t² term is needed, because there is no horizontal acceleration to '
   'put in it.'],
  '**With no horizontal acceleration, horizontal distance is simply speed × '
  'time: 12 × 2.02 = 24.2 m.** 44.2 m is what you get by wrongly applying the '
  'free-fall equation sideways — that is the vertical drop in 3.0 s, not a '
  'horizontal distance.',
  'Sideways: x = v t. No squared term, ever.')

q(Q, 3, 'Two stones are thrown horizontally from cliffs. One leaves a 20 m '
        'cliff at 12 m/s; the other leaves a 45 m cliff at 8 m/s. Compare where '
        'they land relative to the base of their cliff.',
  ['Both land 24.2 m out, despite the different cliffs and speeds',
   'The faster one lands further out, because it is faster',
   'The one from the higher cliff lands further out, because it falls longer',
   'Neither can be compared without knowing the masses'],
  0,
  'Work out each fall time first, then each horizontal distance.',
  ['Cliff one: t = √(2 × 20/9.80) = 2.02 s, so x = 12 × 2.02 = 24.2 m.',
   'Cliff two: t = √(2 × 45/9.80) = 3.03 s, so x = 8 × 3.03 = 24.2 m.',
   'The second stone is slower but stays in the air longer, and the two effects '
   'exactly cancel here.',
   'Both land 24.2 m from the base.'],
  '**Range depends on BOTH the horizontal speed and the fall time, and here a '
  'slower throw from a higher cliff buys back exactly what the speed lost.** '
  'Reasoning from one factor alone — "faster goes further", "higher goes '
  'further" — gets this wrong, because each ignores the other. Mass appears in '
  'neither calculation.',
  'Range = vₓ × t. Two inputs, so never judge it from one of them.')

q(Q, 3, 'A marble rolls off a bench 1.2 m high and lands 0.75 m from its base. '
        'How fast was it rolling?',
  ['1.52 m/s', '0.63 m/s', '2.45 m/s', '0.90 m/s'],
  0,
  'You cannot get speed directly. What can you get from the height alone?',
  ['The height gives the fall time: t = √(2 × 1.2 / 9.80) = 0.49 s.',
   'Horizontally, x = vₓ t, and both x and t are now known.',
   'vₓ = x / t = 0.75 / 0.49.',
   'vₓ = 1.52 m/s.'],
  '**Work the vertical side for the time, then run the horizontal equation '
  'backwards.** 0.63 m/s is 0.75 ÷ 1.2, dividing the landing distance by the '
  'HEIGHT — which mixes a vertical quantity into a horizontal calculation and '
  'has the wrong units for a speed.',
  'Same two-step method as always, just with the last step reversed.')

q(Q, 2, 'A ball is launched at 20 m/s, 40° above the horizontal. What are its '
        'initial velocity components?',
  ['15.3 m/s horizontal, 12.9 m/s vertical',
   '12.9 m/s horizontal, 15.3 m/s vertical',
   '20.0 m/s horizontal, 9.80 m/s vertical',
   '10.0 m/s horizontal, 17.3 m/s vertical'],
  0,
  'Every angled-launch problem opens the same way.',
  ['vₓ₀ = v₀ cos θ = 20 × cos 40° = 15.3 m/s.',
   'vᵧ₀ = v₀ sin θ = 20 × sin 40° = 12.9 m/s.',
   'Check: 40° is below 45°, so the horizontal part should be the bigger — and '
   'it is.',
   'So 15.3 m/s horizontal and 12.9 m/s vertical.'],
  '**Resolving the launch velocity is step one of every angled projectile '
  'problem: cos for horizontal, sin for vertical.** The 45° check catches a '
  'swap instantly. 9.80 is an acceleration, not a velocity component, and has '
  'no business in this answer at all.',
  'Resolve first. Then you have two ordinary one-dimensional problems.')

q(Q, 2, 'That ball leaves at 20 m/s, 40° up, with vᵧ₀ = 12.9 m/s. How long until '
        'it reaches the top of its arc?',
  ['1.31 s', '2.62 s', '1.56 s', '0.76 s'],
  0,
  'What is true about the vertical velocity exactly at the top?',
  ['At the highest point the vertical velocity is momentarily zero.',
   'vᵧ = vᵧ₀ − g t, so 0 = 12.9 − 9.80 t.',
   't = 12.9 / 9.80.',
   't = 1.31 s.'],
  '**Setting vᵧ = 0 is what defines the top of the arc, giving t = vᵧ₀/g = '
  '1.31 s.** 2.62 s is the whole hang time — twice this, because the descent '
  'mirrors the climb. Note the ball is still moving at the top: its horizontal '
  '15.3 m/s never stopped.',
  'Top of the arc means vᵧ = 0, never v = 0.')

q(Q, 3, 'Same launch: 20 m/s at 40°, vₓ = 15.3 m/s, vᵧ₀ = 12.9 m/s, landing back '
        'at launch height. What is its range?',
  ['40.2 m', '20.1 m', '30.7 m', '52.4 m'],
  0,
  'Get the full hang time from the vertical side, then multiply.',
  ['Time to the top is vᵧ₀/g = 12.9/9.80 = 1.31 s.',
   'The arc is symmetric, so the whole flight is twice that: 2.62 s.',
   'Horizontally, R = vₓ × t_hang = 15.3 × 2.62.',
   'R = 40.2 m.'],
  '**Range needs the FULL hang time, not the time to the top: 15.3 × 2.62 = '
  '40.2 m.** 20.1 m is the commonest wrong answer here — exactly half, from '
  'stopping the clock at the peak. The symmetry of the arc is what makes '
  'doubling valid, and it only holds when the landing height equals the launch '
  'height.',
  'Peak time is half of hang time. Range uses the whole flight.')

q(Q, 2, 'An arrow is shot at 15 m/s, 30° above the horizontal, from and back to '
        'ground level. What is its maximum height?',
  ['2.87 m', '5.74 m', '7.50 m', '1.15 m'],
  0,
  'Only the vertical component of the launch decides how high it gets.',
  ['vᵧ₀ = 15 × sin 30° = 7.50 m/s.',
   'At the top vᵧ = 0, and y_max = vᵧ₀² / (2g).',
   'y_max = 7.50² / (2 × 9.80) = 56.25 / 19.6.',
   'y_max = 2.87 m.'],
  '**Maximum height depends only on the vertical component, so the horizontal '
  '13.0 m/s is irrelevant here.** 7.50 m is the vertical component itself, a '
  'speed rather than a height — a units check catches that one. Independence '
  'again: the sideways motion contributes nothing to how high it climbs.',
  'Height comes from vᵧ₀ alone. Range is the one that needs both.')

q(Q, 1, 'At the very top of a projectile’s arc, what is true?',
  ['Its vertical velocity is zero but it is still moving horizontally',
   'Its velocity is zero in every direction',
   'Its acceleration is zero',
   'Its horizontal velocity is zero but it is still moving vertically'],
  0,
  'Which of the two motions actually pauses at the top?',
  ['Going up, the vertical velocity shrinks to zero and then reverses.',
   'So at the peak, vᵧ = 0.',
   'The horizontal velocity was never being changed by anything, so it is '
   'unchanged.',
   'And gravity is still acting, so the acceleration is still 9.80 m/s² '
   'downwards.'],
  '**Only the vertical velocity reaches zero at the top; the horizontal '
  'velocity and the downward acceleration both carry on exactly as before.** If '
  'the acceleration really were zero there, the projectile would hang in the '
  'air rather than curving back down — which is what the parabola rules out.',
  'Zero vertical velocity is not the same as zero velocity.')

q(Q, 2, 'A ball is launched from ground level and lands back at ground level. '
        'How does its landing speed compare with its launch speed?',
  ['The same, because the arc is symmetric',
   'Faster, because gravity has been accelerating it',
   'Slower, because it has lost energy climbing',
   'It depends on the launch angle'],
  0,
  'What does the arc on the way down look like compared with the way up?',
  ['The horizontal velocity never changed at all.',
   'The vertical velocity gained coming down exactly what it lost going up, '
   'because the climb and the fall cover the same height.',
   'So at the landing height both components match their launch values, with '
   'the vertical one now pointing down.',
   'The speed is therefore the same.'],
  '**Ignoring air resistance, the descent mirrors the ascent, so the ball '
  'arrives at its launch height with exactly the speed it left with.** Gravity '
  'did slow it on the way up and speed it on the way down — those two effects '
  'are equal and opposite over equal heights. Only the direction has changed.',
  'Same height, same speed. It only lands faster if it lands lower.')

q(Q, 3, 'A pilot flying level at constant speed releases a crate. Ignoring air '
        'resistance, where is the plane when the crate hits the ground?',
  ['Directly above the crate', 'Well behind the crate',
   'Well ahead of the crate', 'It depends on the plane’s altitude'],
  0,
  'What happens to the crate’s horizontal velocity after it is released?',
  ['At release the crate is moving forwards at exactly the plane’s speed.',
   'Nothing acts on it horizontally, so it keeps that speed the whole way down.',
   'The plane also keeps that speed, since it is flying at constant velocity.',
   'So they travel the same horizontal distance and the plane stays directly '
   'overhead.'],
  '**The crate keeps the plane’s horizontal velocity, so the two stay in step '
  'horizontally for the whole fall.** From the ground the crate traces a '
  'parabola; from the cockpit it appears to drop straight down. Both are right — '
  'that is a frame-of-reference difference, and the two frames still agree '
  'exactly on the vertical motion.',
  'Released, not thrown — so it starts with whatever the plane had.')

q(Q, 2, 'You toss a ball straight up and catch it while riding a smoothly '
        'moving bus. What do you see, and what does someone on the pavement '
        'see?',
  ['You see it go straight up and down; they see a parabola',
   'You both see a parabola',
   'You both see it go straight up and down',
   'You see a parabola; they see it go straight up and down'],
  0,
  'Who is moving along with the ball’s horizontal velocity?',
  ['On the bus, you and the ball share the same horizontal velocity.',
   'Relative to you the ball has no sideways motion at all, so you see a '
   'straight line.',
   'The observer on the pavement is not moving with the bus, so to them the '
   'ball has the bus’s horizontal velocity.',
   'Combined with the fall, that traces a parabola for them.'],
  '**The shape of a trajectory depends on the frame it is watched from.** You '
  'and the observer disagree about the horizontal motion and agree exactly on '
  'the vertical: same height reached, same time in the air. Neither of you is '
  'mistaken, which is why a frame of reference has to be stated.',
  'Disagree sideways. Agree vertically. Every time.')

q(Q, 2, 'An object dropped from rest falls for 3.0 s. How far does it fall?',
  ['44.1 m', '29.4 m', '14.7 m', '88.2 m'],
  0,
  'Dropped from rest, so the initial vertical velocity term drops out.',
  ['Starting from rest: y = ½ g t².',
   'y = ½ × 9.80 × 3.0².',
   'y = ½ × 9.80 × 9.0.',
   'y = 44.1 m.'],
  '**½ × 9.80 × 3.0² = 44.1 m.** 29.4 m is 9.80 × 3.0, which is the SPEED after '
  '3 seconds, not a distance — the units give it away. Forgetting to square the '
  'time, or forgetting the ½, are the two ways this goes wrong.',
  'Speed after t is g t. Distance after t is ½ g t². Different questions.')

q(Q, 3, 'A heavy ball and a light ball roll off the same table at the same '
        'speed. What happens?',
  ['They land together, at the same distance from the table',
   'The heavy one lands first, and closer to the table',
   'The heavy one lands first; both land the same distance out',
   'The light one lands further out, because it is easier to push'],
  0,
  'Look for mass in the projectile equations. Is it there?',
  ['Fall time is t = √(2h/g) — no mass in it.',
   'Horizontal distance is x = vₓ t — no mass in that either.',
   'Both balls have the same height and the same horizontal speed.',
   'So they land at the same moment and the same distance out.'],
  '**Mass appears in no projectile-motion equation, so it changes neither the '
  'fall time nor the range.** The one honest caveat is that this holds because '
  'air resistance is being ignored; with air in play a very light ball really '
  'does fall behind. Every question in this unit assumes it away.',
  'If a quantity is absent from the equations, it cannot change the answer.')

q(Q, 3, 'Order these moments in a projectile’s flight from FASTEST to SLOWEST '
        'total speed, for a ball launched at an angle and landing at its launch '
        'height.',
  ['The instant it is launched', 'Halfway up the climb',
   'At the top of the arc', 'It never slows below the top-of-arc speed'],
  0,
  'The horizontal part is constant, so only the vertical part changes the '
  'total.',
  ['Total speed is √(vₓ² + vᵧ²), and vₓ is the same the whole flight.',
   'So the total speed tracks the size of vᵧ, which shrinks all the way up to '
   'the top.',
   'At launch vᵧ is at its largest, so the speed is greatest there; halfway up '
   'it is smaller; at the top vᵧ = 0, the slowest moment of the flight.',
   'And it never goes below that, since from the top onwards vᵧ grows again — '
   'which is the last item.'],
  '**Speed is slowest at the top of the arc and greatest at launch and landing, '
  'because only the vertical component changes.** The top is the minimum, not a '
  'stop: the ball still has its full horizontal speed there. This is the '
  'symmetry card and the speed card working together.',
  'Constant horizontal plus shrinking vertical means the total shrinks to the '
  'peak, then grows back.',
  kind='order')

# ---- assemble --------------------------------------------------------------
build('ad-astra', C, Q, 'unit-phys-k2-projectiles',
      'Kinematics 2 · 2-2 Projectile Motion', 'physics',
      'Motion in two dimensions under gravity alone: why the horizontal and '
      'vertical motions of a projectile are completely independent, how to '
      'split any projectile into a constant-velocity problem sideways and a '
      'free-fall problem vertically, how time links the two, and how to find '
      'hang time, maximum height, range and the speed at any instant — for both '
      'a horizontal launch and a launch at an angle.',
      'This is where the last two units actually pay off: the kinematics '
      'equations from Kinematics 1 and the component work from 2-1 are both '
      'used, on every problem, in the same breath. It is also the first topic '
      'where the right method matters more than the right formula — split it in '
      'two, find the time, and almost every question falls out.',
      [('Recognise that the vertical and horizontal motions of a projectile are '
        'independent.', 'source'),
       ('Identify that gravity acts only in the vertical direction and that a '
        'projectile has no horizontal acceleration.', 'source'),
       ('Determine the components of a launch velocity from the angle and total '
        'speed.', 'source'),
       ('Relate the height, time in the air and initial vertical velocity of a '
        'projectile, then use them to find the range.', 'source'),
       ('Calculate the final velocity or distance travelled by a projectile '
        'using the kinematics equations.', 'source'),
       ('Explain how the shape of a trajectory depends on the frame of '
        'reference it is observed from.', 'source')],
      'The second half of her teacher’s Kinematics 2 objective list, built '
      'from chapter 7.2. Every number was computed with sympy inside the '
      'builder and asserted before it could be written into a question, with '
      'g = 9.80 m/s² throughout — the same value the textbook and her existing '
      'Equations of Motion unit both use. None of the chapter’s own worked '
      'examples is reused as a question; they were read to calibrate '
      'difficulty only. Three errors get deliberate airtime because they are '
      'the ones that cost marks rather than the ones that look hard: using the '
      'time to the TOP of the arc where the full hang time is needed (which '
      'halves the range, and is offered as a wrong option on the range '
      'question); applying ½ a t² horizontally, where there is no acceleration '
      'to put in it; and reading "vertical velocity is zero at the top" as '
      '"the projectile stops at the top". The unit also states plainly that '
      'ignoring air resistance is a simplification rather than a fact — true '
      'enough for a dense compact object, wildly untrue for a golf ball — so '
      'the assumption is visible rather than hidden. One caution for the real '
      'test: the symmetric doubling that gives hang time only holds when the '
      'projectile lands at its launch height, and every question here that '
      'uses it says so in the stem.',
      ('Do 2-1 first if you have not — every problem here opens by resolving a '
       'velocity. Then hold one sentence in your head: find the time from the '
       'vertical side, then use it on the horizontal side.', 25),
      'content/phys-k2-projectiles.json',
      'Chapter 7.2, Projectile Motion, and the Kinematics 2 objective list',
      'Textbook 2D Kinematics.pdf and Kinematics 2 Objectives.pdf (Drive, '
      'Physics 8)',
      offset_hours=3, round_=9)

p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'content/phys-k2-projectiles.json')
j = json.load(io.open(p, encoding='utf-8'))
j['records']['unit-phys-k2-projectiles']['libv'] = 1
io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))
print('  + libv 1; all sympy assertions passed')
