# -*- coding: utf-8 -*-
# Dynamics 2 · 2-1 Applying Newton's Second Law, 2-2 Friction and the
# Coefficient, and 2-3 The Newton's Second Law Lab. Built from the three files
# in Drive › Physics 8 › Dynamics 2:
#   N2L_Worksheet.pdf                  10 MC + 5 free-response problems
#   Friction_and_the_Coefficient.pdf   5 free-response problems
#   Newtons_Law_Lab.pdf                the cart-and-hanging-mass lab
#
# The sheets were read for WHAT THEY ASK (ideas, traps, problem shapes), never
# for marks. None of their numbers is reused in a graded stem or option:
# fresh() below is asserted against every question.
#
# Dynamics 1 already teaches the second law and tension in words (1-1),
# apparent weight, μ, static and kinetic friction (1-2), and slopes, angled
# pulls and components (1-3). Dynamics 2 is the APPLIED layer: multi-step
# problems that chain those ideas — a system acceleration and then a tension,
# a scale reading and then the acceleration back out of it, a normal force and
# then the friction it sets, a stop up a rough slope and the slide back down.
#
# The lab has no data yet, so 2-3 teaches the reasoning only (the Ramp Lab and
# Hooke's-lab call): why the hanging mass counts, getting a from Δx and t, the
# linearization a against 1/M, the percent comparison, the Moon, and one error
# with its direction.
#
# g = 9.8 m/s² throughout, as in Dynamics 1. EVERY number is computed with
# sympy below and rounded half-up with Decimal; every wrong option is a named
# slip computed the same way, and named() asserts that no distractor rounds to
# the answer.
import sys, os, json, io, re
from decimal import Decimal, ROUND_HALF_UP
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
g = sp.Rational(98, 10)
def R(x): return sp.Rational(str(x))
def sin(d): return sp.sin(sp.Rational(d) * sp.pi / 180)
def cos(d): return sp.cos(sp.Rational(d) * sp.pi / 180)
def f(x, n):
    """x rounded half-up to n decimals, as text (minus sign as −)."""
    d = Decimal(str(sp.N(x, 40))).quantize(Decimal(1).scaleb(-n), ROUND_HALF_UP)
    return str(d).replace('-', '−')
def chk(x, n, want):
    got = f(x, n); assert got == want, (got, want); return want
def named(ans, *dists):
    """The answer and its slips, all as displayed text: none may coincide."""
    vals = [ans] + list(dists)
    assert len(set(vals)) == len(vals), vals
    nums = [float(v.replace('−', '-')) for v in vals]
    for v in nums[1:]: assert abs(v - nums[0]) > 1e-9, vals

def patch(path, uid, **fields):
    p = os.path.join(REPO, path)
    j = json.load(io.open(p, encoding='utf-8'))
    j['records'][uid].update(fields)
    io.open(p, 'w', encoding='utf-8').write(json.dumps(j, ensure_ascii=False, indent=1))

SRC_N2L = 'N2L_Worksheet.pdf (Drive, Physics 8 › Dynamics 2)'
SRC_FR = 'Friction_and_the_Coefficient.pdf (Drive, Physics 8 › Dynamics 2)'
SRC_LAB = 'Newtons_Law_Lab.pdf (Drive, Physics 8 › Dynamics 2)'

# Numbers the sheets use. None may appear in a graded stem or option.
FORBID = re.compile(
    r'(?<![\d.])(12(\.0)? kg|60(\.0)? N\b|52 N\b|30°|35°|3\.2 m/s²|50(\.0)? N\b|'
    r'4(\.0)? kg|6(\.0)? kg|65(\.0)? kg|520 N\b|2\.0 m/s²|1\.5 m/s²|3(\.0)? m/s\b(?!²)|'
    r'3 m/s²|0\.48|1\.02|1\.49|2\.03|2\.48|7\.0 N\b|140 N\b|60 kg|30 N\b|0\.30\b|'
    r'0\.20\b|37°|0\.45\b|10 m/s\b(?!²)|5(\.0)? m/s\b(?!²)|2\.5 m(?![/\w²]))')
def fresh(Q):
    for x in Q:
        texts = [x['q']] + x['opts']
        for t in texts:
            m = FORBID.search(t)
            assert not m, (x['id'], m.group(0), t)

# =============================================================================
# 2-1 APPLYING NEWTON'S SECOND LAW
# =============================================================================
# A. Two blocks on a frictionless floor, joined by a taut string.
mA, mB, P = R('3.0'), R('5.0'), 40
aAB = P / (mA + mB)
a_ok = chk(aAB, 1, '5.0'); a_one = chk(P / mB, 1, '8.0')
a_other = chk(P / mA, 0, '13'); a_sub = chk(P / (mB - mA), 0, '20')
named(a_ok, a_one, a_other, a_sub)
T_ok = chk(mA * aAB, 0, '15'); T_pull = '40'; T_big = chk(mB * aAB, 0, '25')
T_half = chk(R(P) / 2, 0, '20')
named(T_ok, T_pull, T_big, T_half)
T_sw = chk(mB * aAB, 0, '25')                       # pull the 3.0 kg block instead
assert f(P / mA, 0) == '13'

# B. Elevator speeding up on the way up.
mB_, aB_ = 56, R('1.2')
N_up = chk(mB_ * (g + aB_), 0, '616'); N_flip = chk(mB_ * (g - aB_), 0, '482')
N_ign = chk(mB_ * g, 0, '549'); N_ma = chk(mB_ * aB_, 0, '67')
named(N_up, N_flip, N_ign, N_ma)
# C. Moving up but slowing: acceleration DOWN.
mC, aC = 70, R('2.5')
N_sl = chk(mC * (g - aC), 0, '511'); N_sl_flip = chk(mC * (g + aC), 0, '861')
N_sl_ign = chk(mC * g, 0, '686'); N_sl_ma = chk(mC * aC, 0, '175')
named(N_sl, N_sl_flip, N_sl_ign, N_sl_ma)
# D. Constant velocity.
mD, vD = 58, R('4.0')
N_cv = chk(mD * g, 0, '568'); N_cv_sp = chk(mD * (g + vD), 0, '800')
N_cv_sub = chk(mD * (g - vD), 0, '336'); N_cv_m = '58'
named(N_cv, N_cv_sp, N_cv_sub, N_cv_m)
# E. From a reading back to the acceleration.
mE, NE = 45, 504
aE = R(NE) / mE - g
aE_ok = chk(aE, 1, '1.4'); aE_nog = chk(R(NE) / mE, 1, '11.2'); aE_add = chk(R(NE) / mE + g, 1, '21.0')
named(aE_ok, aE_nog, aE_add)
# G/H. An angled pull on a level floor.
mG, FG, thG, fG = 15, 80, 25, 40
NG = mG * g - FG * sin(thG)
NG_ok = chk(NG, 0, '113'); NG_no = chk(mG * g, 0, '147')
NG_add = chk(mG * g + FG * sin(thG), 0, '181'); NG_swap = chk(mG * g - FG * cos(thG), 0, '74')
named(NG_ok, NG_no, NG_add, NG_swap)
aG = (FG * cos(thG) - fG) / mG
aG_ok = chk(aG, 1, '2.2'); aG_whole = chk(R(FG - fG) / mG, 1, '2.7')
aG_add = chk((FG * cos(thG) + fG) / mG, 1, '7.5'); aG_nof = chk(FG * cos(thG) / mG, 1, '4.8')
named(aG_ok, aG_whole, aG_add, aG_nof)
# frictionless floor: a = F cosθ / m falls as θ rises
assert FG * cos(40) / mG < FG * cos(thG) / mG
# J. Working back to the friction on a slope.
mJ, thJ, aJ = R('4.5'), 40, R('4.1')
fJ = mJ * g * sin(thJ) - mJ * aJ
fJ_ok = chk(fJ, 1, '9.9'); fJ_add = chk(mJ * g * sin(thJ) + mJ * aJ, 0, '47')
fJ_swap = chk(mJ * g * cos(thJ) - mJ * aJ, 0, '15'); fJ_noa = chk(mJ * g * sin(thJ), 0, '28')
named(fJ_ok, fJ_add, fJ_swap, fJ_noa)
# K/L. A force–acceleration line for a cart of constant mass.
KF = [R('0.5'), R('1.0'), R('1.5'), R('2.0')]
Ka = [R('0.40'), R('0.80'), R('1.20'), R('1.60')]
slopeK = (Ka[-1] - Ka[0]) / (KF[-1] - KF[0])
assert slopeK == R('0.8') and all(a / F == slopeK for F, a in zip(KF, Ka))
mK = 1 / slopeK
mK_ok = chk(mK, 2, '1.25'); named(mK_ok, '0.80', '2.0', '1.6')
pred = slopeK * R('3.5')
pr_ok = chk(pred, 1, '2.8'); pr_div = chk(R('3.5') / slopeK, 1, '4.4')
named(pr_ok, pr_div, '3.5', '1.6')
GRAPH_K = {'w': [0, 2.5, 0, 2], 'gx': 0.5, 'gy': 0.4,
           'series': [{'type': 'pts', 'pts': [[0, 0]] + [[float(F), float(a)] for F, a in zip(KF, Ka)]}],
           'pts': [{'x': float(F), 'y': float(a)} for F, a in zip(KF, Ka)],
           'xl': 'net force F (N)', 'yl': 'a (m/s²)'}

C, Q = [], []
card(C, 'Solving a second-law problem',
     '**Draw the forces, pick a positive direction, add the forces along it, '
     'and set the total equal to ma.**\n'
     '• One free-body diagram per object, with every force on THAT object.\n'
     '• Forces along your positive direction are +, against it are −.\n'
     '• Only then put numbers in. Most wrong answers start as a missing or '
     'backwards arrow.', eq='ΣF = ma', frm='added')
card(C, 'Your sheet’s g',
     '**This unit uses g = 9.8 m/s² as a size, and says “down” in words.**\n'
     '• Your sheets may write g = −9.8 m/s², or round it to 10. The minus is '
     'only the direction: down.\n'
     '• A weight is mg using the size of g. If your class uses 10, your '
     'answers will be about 2 percent bigger than these, and both are right for '
     'their g.', hint='The minus sign on g means “down”, nothing more.', frm='added')
card(C, 'Connected objects share one acceleration',
     '**Two objects joined by a taut string move together, so they have the '
     'same acceleration.**\n'
     '• If one sped up more, the string would go slack or snap.\n'
     '• So treat them as ONE system first: the outside force over the total '
     'mass.', eq='a = F_net / (m₁ + m₂)')
card(C, 'The string is internal to the system',
     '**When both blocks are one system, the string’s pulls cancel and drop '
     'out.**\n'
     '• The string pulls the front block back and the back block forward by '
     'the same amount.\n'
     '• That is why the system equation has no T in it — and why you need a '
     'second step to find T.')
card(C, 'Then the tension from one block',
     '**To find the tension, write ΣF = ma for ONE block, using only the forces '
     'on it.**\n'
     '• The easiest block is the one the string pulls and nothing else does: '
     'T = m_that block × a.\n'
     '• You already know a from the system step.', eq='T = m_back × a')
card(C, 'The tension is less than the pull',
     '**The pull speeds up both blocks; the string only has to speed up the '
     'one behind it, so the tension is smaller than the pull.**\n'
     '• Setting the tension equal to the applied force is the commonest slip.\n'
     '• The tension is the pull’s share for the trailing block: '
     'T = F × m_back / (m₁ + m₂).',
     hint='The string only drags what is behind it.')
card(C, 'Pull the other block instead',
     '**Pull the other block with the same force and the acceleration stays '
     'the same, but the tension changes.**\n'
     '• The total mass is unchanged, so a is unchanged.\n'
     '• Now the string drags the OTHER block, so T = that block’s mass × a. '
     'Pulling the lighter block gives the bigger tension.')
card(C, 'Scale reading: speeding up going up',
     '**When the acceleration points up, the scale reads more than your '
     'weight: N = m(g + a).**\n'
     '• The floor has to hold you up AND push you faster.\n'
     '• Speeding up on the way up and slowing down on the way down both have '
     'an upward acceleration.', eq='N = m(g + a)')
card(C, 'Scale reading: acceleration down',
     '**When the acceleration points down, the scale reads less: '
     'N = m(g − a).**\n'
     '• Slowing down on the way UP is an acceleration down — the reading '
     'drops even though you are rising.\n'
     '• Flipping the sign of a is the slip to watch for: decide the direction '
     'of the acceleration, not the direction of travel.', eq='N = m(g − a)')
card(C, 'Scale reading at constant velocity',
     '**At constant velocity the scale reads exactly your weight, however fast '
     'the elevator moves.**\n'
     '• Constant velocity means a = 0, so N = mg.\n'
     '• A speed is not an acceleration: 4 m/s up adds nothing to the reading.')
card(C, 'From a scale reading back to the acceleration',
     '**Divide the reading by the mass and subtract g; what is left is the '
     'acceleration.**\n'
     '• A positive answer points up, a negative one points down.\n'
     '• Forgetting to subtract g gives an absurd acceleration — a quick check '
     'that something went wrong.', eq='a = N / m − g')
card(C, 'An angled pull lifts as well as drags',
     '**The vertical part of an upward pull, F sin θ, takes some of the weight, '
     'so the normal force shrinks.**\n'
     '• N = mg − F sin θ on a level floor.\n'
     '• Only the horizontal part, F cos θ, speeds the object along the floor.\n'
     '• Less normal force means less friction, which is the next unit’s '
     'story.', eq='N = mg − F sin θ')
card(C, 'Tilting the pull up further',
     '**On a frictionless floor, a steeper pull always gives a smaller '
     'acceleration, because cos θ shrinks.**\n'
     '• On a rough floor it is a trade: less horizontal drive, but less '
     'friction too. Tilting a little can help; tilting a lot never does.',
     frm='added')
card(C, 'Working back to friction on a slope',
     '**If you measure how fast something slides down a slope, the shortfall '
     'from g sin θ is friction’s doing.**\n'
     '• Down the slope: mg sin θ − f = ma, so f = mg sin θ − ma.\n'
     '• On a frictionless slope a would be g sin θ; anything less is '
     'friction.', eq='f = mg sin θ − ma')
card(C, 'Acceleration against force: a straight line',
     '**For one cart of fixed mass, acceleration is proportional to the net '
     'force, so a graph of a against F is a straight line through the '
     'origin.**\n'
     '• Double the force, double the acceleration.')
C[-1]['graph'] = GRAPH_K
card(C, 'The slope is 1 / mass',
     '**The slope of a against F is 1 ÷ the mass, in (m/s²) per newton, which '
     'is 1/kg.**\n'
     '• a = (1/m) F has the same shape as y = mx.\n'
     '• So the mass is 1 ÷ slope: a steeper line means a lighter cart.',
     eq='slope = Δa / ΔF = 1 / m')
card(C, 'Which variable goes on which axis',
     '**The one you choose goes across the bottom; the one you measure goes up '
     'the side.**\n'
     '• Choosing the force and measuring the acceleration makes force the '
     'independent variable and acceleration the dependent one.')
card(C, 'Acceleration follows the net force, not the motion',
     '**The acceleration always points the way the net force points — even '
     'when the object is moving the other way.**\n'
     '• A box sliding left while slowing down has a net force to the right.\n'
     '• Velocity tells you where it is going; acceleration tells you how that '
     'is changing.')

q(Q, 1, 'Two blocks on a frictionless table are joined by a taut string, and '
        'one block is pulled so both speed up. How do their accelerations compare?',
  ['They are equal, because the taut string makes them move together',
   'The pulled block’s is bigger, because the force acts on it directly',
   'The heavier block’s is smaller, because it has more inertia to overcome',
   'The block behind has none until the string stretches tight enough'],
  0, 'What would happen to the string if one went faster?',
  ['The string is taut and does not stretch.',
   'If one block sped up more, the gap would change and the string would go slack.',
   'So they keep the same velocity at every moment.',
   'Same velocity at every moment means the same acceleration.'],
  '**A taut string forces the two blocks to share one acceleration.** The '
  'pulled block feels a bigger net force, but it is not ahead: the string '
  'holds the gap fixed. That is what makes the one-system step work.',
  'Joined and taut means one acceleration.')

q(Q, 2, 'A 3.0 kg block and a 5.0 kg block sit on a frictionless table, joined '
        'by a light string. A 40 N horizontal pull acts on the 5.0 kg block. '
        'What is the acceleration of the blocks?',
  [a_ok + ' m/s²', a_one + ' m/s²', a_other + ' m/s²', a_sub + ' m/s²'],
  0, 'Both blocks move, so both masses count.',
  ['The string makes the blocks one system.',
   'Total mass: 3.0 kg + 5.0 kg = 8.0 kg.',
   'a = F / m = 40 N ÷ 8.0 kg.',
   'a = 5.0 m/s².'],
  '**a = 40 N ÷ (3.0 + 5.0) kg = 5.0 m/s².** 8.0 m/s² uses only the pulled '
  'block’s mass, 13 m/s² only the other block’s, and 20 m/s² subtracts the '
  'masses — but the pull has to speed up everything joined to it.',
  'System first: outside force over total mass.')

q(Q, 2, 'A 3.0 kg block and a 5.0 kg block sit on a frictionless table, joined '
        'by a light string. A 40 N horizontal pull acts on the 5.0 kg block, so '
        'both accelerate at 5.0 m/s². What is the tension in the string?',
  [T_ok + ' N', T_pull + ' N', T_big + ' N', T_half + ' N'],
  0, 'Which block does the string pull, and nothing else?',
  ['The string is the only horizontal force on the 3.0 kg block.',
   'For that block: T = ma.',
   'T = 3.0 kg × 5.0 m/s².',
   'T = 15 N.'],
  '**T = 3.0 kg × 5.0 m/s² = 15 N.** 40 N sets the tension equal to the pull; '
  '25 N uses the pulled block’s mass, which the string does not drag; 20 N '
  'splits the pull evenly, as if the blocks had equal masses.',
  'Find T from the block the string drags.')

q(Q, 3, 'A 3.0 kg block and a 5.0 kg block sit on a frictionless table, joined '
        'by a light string. A 40 N horizontal pull now acts on the 3.0 kg block '
        'instead, pulling the other way. What are the acceleration and the '
        'tension?',
  [a_ok + ' m/s² and ' + T_sw + ' N', a_ok + ' m/s² and ' + T_ok + ' N',
   a_ok + ' m/s² and ' + T_pull + ' N', a_other + ' m/s² and ' + T_sw + ' N'],
  0, 'The total mass has not changed. The block being dragged has.',
  ['The system is still 8.0 kg, so a = 40 N ÷ 8.0 kg = 5.0 m/s².',
   'Now the string drags the 5.0 kg block.',
   'T = 5.0 kg × 5.0 m/s² = 25 N.',
   'The answer is 5.0 m/s² and 25 N.'],
  '**Same acceleration, 5.0 m/s², but the tension rises to 25 N.** The string '
  'now drags the heavier block. Carrying 15 N over ignores which block is '
  'behind; 40 N sets the tension equal to the pull; 13 m/s² counts only the '
  'pulled block’s mass.',
  'Pull the lighter block and the string works harder.')

q(Q, 2, 'Two crates joined by a rope are pulled across smooth ice by a second '
        'rope on the front crate. Why is the tension in the joining rope less '
        'than the pull on the front rope?',
  ['The joining rope only speeds up the back crate; the pull speeds up both',
   'Some of the pull is used up stretching the joining rope as they move',
   'Tension always shrinks along a rope, so the far end pulls less hard',
   'The back crate pushes forward on the front crate and cancels some pull'],
  0, 'How much mass does each rope have to accelerate?',
  ['Both crates share the same acceleration.',
   'The front rope must give that acceleration to both crates.',
   'The joining rope must give it only to the back crate.',
   'Less mass at the same acceleration needs less force, so the tension is smaller.'],
  '**The front rope accelerates both crates; the joining rope accelerates only '
  'the back one**, so it needs less force. A light rope passes its tension '
  'along unchanged, and the back crate pulls back on the front one rather than '
  'pushing it forward.',
  'Tension = the share of the pull for whatever is behind.')

q(Q, 2, 'A 56 kg student stands on a scale in an elevator that is speeding up '
        'as it rises, at 1.2 m/s². What does the scale read?',
  [N_up + ' N', N_flip + ' N', N_ign + ' N', N_ma + ' N'],
  0, 'The acceleration points up, so the floor pushes harder than her weight.',
  ['Upward is positive: N − mg = ma.',
   'N = m(g + a) = 56 kg × (9.8 + 1.2) m/s².',
   'N = 56 × 11.0 = 616 N.',
   'The scale reads 616 N.'],
  '**N = 56 × (9.8 + 1.2) = 616 N.** 482 N flips the sign of a; 549 N is her '
  'weight, ignoring the acceleration; 67 N is only ma, forgetting that the '
  'floor holds her up as well.',
  'Upward acceleration: g + a.')

q(Q, 2, 'A 70 kg passenger stands on a scale in an elevator that is moving UP '
        'but slowing down at 2.5 m/s². What does the scale read?',
  [N_sl + ' N', N_sl_flip + ' N', N_sl_ign + ' N', N_sl_ma + ' N'],
  0, 'Slowing while rising: which way does the acceleration point?',
  ['Moving up and slowing down means the acceleration points down.',
   'With up as positive, a = −2.5 m/s², so N = m(g − 2.5).',
   'N = 70 × 7.3 = 511 N.',
   'The scale reads 511 N.'],
  '**The acceleration points down, so N = 70 × (9.8 − 2.5) = 511 N.** 861 N '
  'uses g + a because the elevator is rising — the slip of reading the '
  'direction of travel instead of the acceleration. 686 N ignores the '
  'acceleration; 175 N is only ma.',
  'Slowing on the way up feels light.')

q(Q, 1, 'A 58 kg student stands on a scale in an elevator rising at a steady '
        '4.0 m/s. What does the scale read?',
  [N_cv + ' N', N_cv_sp + ' N', N_cv_sub + ' N', N_cv_m + ' N'],
  0, 'What is the acceleration at a steady speed?',
  ['A steady speed in a straight line means a = 0.',
   'So N = mg.',
   'N = 58 × 9.8 = 568 N.',
   'The scale reads 568 N.'],
  '**Constant velocity means no acceleration, so N = mg = 568 N.** 800 N and '
  '336 N treat the speed 4.0 m/s as if it were an acceleration; 58 N uses the '
  'mass as if it were a weight.',
  'A speed is not an acceleration.')

q(Q, 3, 'A 45 kg student stands on a scale in a moving elevator, and the scale '
        'reads 504 N. What is the elevator’s acceleration?',
  [aE_ok + ' m/s² upward', aE_ok + ' m/s² downward',
   aE_nog + ' m/s² upward', aE_add + ' m/s² upward'],
  0, 'Divide by the mass, then take g away.',
  ['Upward is positive: N − mg = ma, so a = N / m − g.',
   'N / m = 504 ÷ 45 = 11.2 m/s².',
   'a = 11.2 − 9.8 = +1.4 m/s².',
   'The acceleration is 1.4 m/s² upward.'],
  '**a = 504 ÷ 45 − 9.8 = +1.4 m/s², upward** — the reading is above her '
  'weight (441 N), so the floor pushes her up harder than gravity pulls down. '
  '“Downward” flips the sign; 11.2 forgets to subtract g; 21.0 adds it.',
  'Reading above the weight means acceleration up.')

q(Q, 2, 'A scale in an elevator reads LESS than the weight of the person '
        'standing on it. Which could the elevator be doing?',
  ['Moving up and slowing down', 'Moving up at a steady speed',
   'Moving up and speeding up', 'Moving down and slowing down'],
  0, 'A low reading needs a downward acceleration.',
  ['N < mg means the net force on the person points down.',
   'So the acceleration points down.',
   'Rising while slowing is an acceleration down; so is falling while speeding up.',
   'Of the choices, only moving up and slowing down fits.'],
  '**A low reading means the acceleration points down, and rising-but-slowing '
  'is exactly that.** A steady speed reads the weight; speeding up on the way '
  'up and slowing down on the way down both read MORE than the weight.',
  'Ask which way the speed is changing, not which way it moves.')

q(Q, 2, 'A 15 kg crate on a level floor is pulled with 80 N by a rope angled '
        '25° above the horizontal. What is the normal force from the floor?',
  [NG_ok + ' N', NG_no + ' N', NG_add + ' N', NG_swap + ' N'],
  0, 'The rope lifts a little as well as dragging.',
  ['Weight: 15 × 9.8 = 147 N, down.',
   'The rope’s vertical part: 80 sin 25° = 33.8 N, up.',
   'Vertically nothing accelerates: N + 33.8 = 147.',
   'N = 147 − 33.8 ≈ 113 N.'],
  '**N = mg − F sin θ = 147 − 33.8 ≈ 113 N.** 147 N leaves the rope’s lift '
  'out; 181 N adds it as if the rope pressed down; 74 N subtracts '
  'F cos θ — sine and cosine swapped.',
  'Vertical part: sine, when the angle is from the horizontal.')

q(Q, 3, 'A 15 kg crate on a level floor is pulled with 80 N by a rope angled '
        '25° above the horizontal, and kinetic friction on it is 40 N. What is '
        'its acceleration along the floor?',
  [aG_ok + ' m/s²', aG_whole + ' m/s²', aG_add + ' m/s²', aG_nof + ' m/s²'],
  0, 'Only the horizontal part of the pull drives it along.',
  ['Horizontal part of the pull: 80 cos 25° = 72.5 N.',
   'Friction points backward: net force = 72.5 − 40 = 32.5 N.',
   'a = 32.5 N ÷ 15 kg.',
   'a ≈ 2.2 m/s².'],
  '**a = (80 cos 25° − 40) ÷ 15 ≈ 2.2 m/s².** 2.7 uses the whole 80 N as if '
  'the rope were level; 7.5 adds friction instead of subtracting it; 4.8 '
  'leaves friction out.',
  'Horizontal part forward, friction back.')

q(Q, 2, 'A cart on a frictionless floor is pulled by a rope with a force of '
        'fixed size. If the rope is tilted further above the horizontal, what '
        'happens to the cart’s acceleration?',
  ['It decreases, because the horizontal part F cos θ gets smaller',
   'It increases, because the normal force gets smaller',
   'It stays the same, because the size of the pull has not changed',
   'It increases, because the rope now lifts part of the cart’s weight'],
  0, 'With no friction, only one part of the pull matters.',
  ['Only the horizontal part, F cos θ, accelerates the cart along the floor.',
   'As θ grows, cos θ shrinks.',
   'There is no friction for a smaller normal force to reduce.',
   'So the acceleration decreases.'],
  '**On a frictionless floor the acceleration falls as the rope tilts up**, '
  'because F cos θ shrinks. A smaller normal force only helps when there is '
  'friction to reduce; here there is none.',
  'No friction: steeper pull, less acceleration.')

q(Q, 3, 'A 4.5 kg block slides down a 40° ramp, and its acceleration is '
        'measured as 4.1 m/s². How big is the friction on it?',
  [fJ_ok + ' N', fJ_add + ' N', fJ_swap + ' N', fJ_noa + ' N'],
  0, 'Gravity’s part down the slope, minus what the acceleration needs.',
  ['Down the slope: mg sin θ − f = ma.',
   'mg sin 40° = 4.5 × 9.8 × 0.643 ≈ 28.3 N.',
   'ma = 4.5 × 4.1 = 18.45 N.',
   'f = 28.3 − 18.45 ≈ 9.9 N.'],
  '**f = mg sin θ − ma ≈ 28.3 − 18.5 = 9.9 N.** 47 N adds ma instead of '
  'subtracting it; 15 N uses cos 40° for the down-slope part, swapping sine '
  'and cosine; 28 N is gravity’s part alone, ignoring the acceleration.',
  'Friction is the shortfall from g sin θ.')

q(Q, 1, 'The graph shown plots a cart’s acceleration against the net force on '
        'it, with the cart’s mass kept the same. What does the slope of the '
        'line stand for?',
  ['1 ÷ the cart’s mass', 'The cart’s mass', 'The cart’s weight',
   'The net force on the cart'],
  0, 'Compare a = (1/m)F with y = mx.',
  ['The line has the form a = (something) × F.',
   'Newton’s second law gives a = F / m = (1/m) F.',
   'So the slope is the number multiplying F.',
   'The slope is 1 ÷ the mass.'],
  '**The slope of a against F is 1/m.** Plotting F against a instead would make '
  'the slope the mass — which axis holds which quantity decides it.',
  'Rise over run: (m/s²) per N is 1/kg.')
Q[-1]['graph'] = GRAPH_K

q(Q, 2, 'The graph shown plots a cart’s acceleration against the net force on '
        'it, with the cart’s mass kept the same. What is the cart’s mass?',
  [mK_ok + ' kg', '0.80 kg', '2.0 kg', '1.6 kg'],
  0, 'Find the slope, then turn it upside down.',
  ['Slope = Δa / ΔF = (1.60 − 0.40) ÷ (2.0 − 0.5) = 0.80 (m/s²)/N.',
   'The slope is 1/m.',
   'm = 1 ÷ 0.80 = 1.25 kg.',
   'The cart’s mass is 1.25 kg.'],
  '**Slope 0.80 = 1/m, so m = 1.25 kg.** 0.80 kg reads the slope itself as '
  'the mass; 2.0 kg and 1.6 kg are just the largest force and the largest '
  'acceleration on the graph.',
  'Steeper line, lighter cart.')
Q[-1]['graph'] = GRAPH_K

q(Q, 2, 'A cart of fixed mass speeds up at 0.80 m/s² for every newton of net '
        'force, along a straight line through the origin. What acceleration '
        'would a 3.5 N net force give it?',
  [pr_ok + ' m/s²', pr_div + ' m/s²', '3.5 m/s²', '1.6 m/s²'],
  0, 'Multiply the force by the slope.',
  ['a = slope × F.',
   'a = 0.80 (m/s²)/N × 3.5 N.',
   'a = 2.8 m/s².',
   'It would accelerate at 2.8 m/s².'],
  '**a = 0.80 × 3.5 = 2.8 m/s².** 4.4 divides by the slope instead of '
  'multiplying; 3.5 assumes a equals F; 1.6 assumes the line stops rising '
  'once the data run out.',
  'A straight line through the origin keeps going.')

q(Q, 1, 'In an experiment, you choose the net force on a cart and measure the '
        'acceleration it gets. Which is the independent variable?',
  ['The net force', 'The acceleration', 'The cart’s mass', 'The time taken'],
  0, 'Which one do you set yourself?',
  ['The independent variable is the one you choose and change.',
   'The dependent variable is the one you measure.',
   'Here you choose the force and measure the acceleration.',
   'The net force is independent.'],
  '**You set the net force, so it is the independent variable**, and it goes '
  'across the horizontal axis. The acceleration is what you measure; the mass '
  'is held constant, a controlled variable.',
  'Choose it: independent. Measure it: dependent.')

q(Q, 2, 'A box slides to the left across a floor and is slowing down. Which '
        'way does the net force on it point?',
  ['To the right', 'To the left', 'Straight down', 'There is none'],
  0, 'Slowing down means the acceleration opposes the velocity.',
  ['It moves left.',
   'It is slowing, so its acceleration points opposite to its velocity: right.',
   'The net force points the same way as the acceleration.',
   'The net force points right.'],
  '**Right — the net force points along the acceleration, not along the '
  'motion.** Something moving left with a leftward net force would be '
  'speeding up, and zero net force would keep its speed constant.',
  'Net force follows the acceleration.')

q(Q, 2, 'Put the steps for finding the tension between two connected blocks in '
        'order.',
  ['Draw a free-body diagram for each block and pick a positive direction',
   'Treat both blocks as one system and find a = F_net ÷ (m₁ + m₂)',
   'Choose one block and write ΣF = ma using only the forces on it',
   'Solve that one block’s equation for the tension T'],
  0, 'You need the acceleration before the tension.',
  ['Start with the forces: one diagram per block.',
   'The system step gives a, because T cancels inside the system.',
   'Then one block’s own equation contains T.',
   'Solve it for T.'],
  '**Diagrams, then the system’s acceleration, then one block’s equation, '
  'then T.** Trying to find T first fails: each block’s equation has two '
  'unknowns, T and a, until the system step supplies a.',
  'System for a, one block for T.', kind='order')

fresh(Q)
NOTE_N2L = (
    'From N2L_Worksheet.pdf in the new Dynamics 2 folder. The sheet was read '
    'for what it asks — connected blocks and tension, elevator scale readings, '
    'an angled pull with friction, a block on a ramp, and a force–acceleration '
    'data table — and nothing of hers was marked or recorded. Dynamics 1 '
    'already teaches the second law, tension, apparent weight and slopes in '
    'words, so this unit is the multi-step layer: the system’s acceleration '
    'first, then the tension from one block; a scale reading forward and '
    'backward; the normal force before anything that depends on it. Every '
    'number was computed with sympy and checked, every wrong option is a named '
    'slip (one block’s mass only, tension equal to the pull, the sign of a '
    'flipped, a speed used as an acceleration, sine and cosine swapped, '
    'friction added), and none of the sheet’s numbers is reused. This unit '
    'uses g = 9.8 m/s²; her sheets may write it as −9.8 or 10, and a card '
    'says so. One thing on the sheet: free-response problem 3 skips part (d), '
    'going straight from (c) to (e).')
build('ad-astra', C, Q, 'unit-phys-dyn2-n2l',
      'Dynamics 2 · 2-1 Applying Newton’s Second Law', 'physics',
      'Newton’s second law put to work on problems with more than one step: '
      'two blocks joined by a string (the system’s acceleration first, then the '
      'tension from one block), scale readings in an elevator and working back '
      'from a reading, a pull at an angle, friction worked out from a measured '
      'slide down a ramp, and reading a force–acceleration graph whose slope '
      'is 1 ÷ the mass.',
      'Real problems rarely hand you the net force. Breaking one into a system '
      'step and an object step, or into a vertical and a horizontal step, is '
      'the move every later unit — friction, circular motion, energy — builds '
      'on.',
      [('Use a free-body diagram and ΣF = ma to find an acceleration.', 'source'),
       ('Find the acceleration of connected objects and the tension between them.', 'source'),
       ('Find a scale reading in an accelerating elevator, and the acceleration from a reading.', 'source'),
       ('Find the normal force and acceleration for a pull at an angle.', 'source'),
       ('Interpret the slope of an acceleration–force graph as 1 ÷ mass.', 'source'),
       ('Follow a fixed order of steps for multi-object problems.', 'added')],
      NOTE_N2L,
      ('Read the cards, then take the quiz. Before every calculation, draw the '
       'arrows and say which way is positive.', 30),
      'content/phys-dyn2-n2l.json', 'Newton’s Second Law (worksheet)', SRC_N2L,
      offset_hours=3, libv_=1)
patch('content/phys-dyn2-n2l.json', 'unit-phys-dyn2-n2l', quarter=2)

# =============================================================================
# 2-2 FRICTION AND THE COEFFICIENT
# =============================================================================
# a. Constant velocity on a level floor.
Fa, ma_ = 85, 40
mu_a = R(Fa) / (ma_ * g)
mu_ok = chk(mu_a, 2, '0.22'); mu_m = chk(R(Fa) / ma_, 1, '2.1'); mu_inv = chk(ma_ * g / Fa, 1, '4.6')
named(mu_ok, mu_m, mu_inv, '0.00')
# b–d. Two blocks on a rough floor.
m1, m2, Pb, mub = R('2.0'), R('3.0'), 45, R('0.35')
f1, f2 = mub * m1 * g, mub * m2 * g
fb_ok = chk(f2, 0, '10'); fb_tot = chk(f1 + f2, 0, '17'); fb_m = chk(mub * m2, 2, '1.05'); fb_oth = chk(f1, 1, '6.9')
named(fb_ok, fb_tot, fb_m, fb_oth)
ab = (Pb - f1 - f2) / (m1 + m2)
ab_ok = chk(ab, 1, '5.6'); ab_nof = chk(R(Pb) / (m1 + m2), 1, '9.0')
ab_add = chk((Pb + f1 + f2) / (m1 + m2), 0, '12'); ab_one = chk((Pb - f2) / (m1 + m2), 1, '6.9')
named(ab_ok, ab_nof, ab_add, ab_one)
Tb = m1 * ab + f1
assert sp.simplify(Tb - Pb * m1 / (m1 + m2)) == 0
Tb_ok = chk(Tb, 0, '18'); Tb_pull = '45'; Tb_big = chk(m2 * ab + f2, 0, '27'); Tb_nof = chk(m1 * ab, 0, '11')
named(Tb_ok, Tb_pull, Tb_big, Tb_nof)
# the tension does not depend on μ, while both still slide
for mu in (R('0.10'), R('0.50')):
    a_ = (Pb - mu * (m1 + m2) * g) / (m1 + m2); assert a_ > 0
    assert sp.simplify(m1 * (a_ + mu * g) - Tb) == 0
# e/f. A block in an accelerating elevator.
me, aye, mue, Fe = R('2.5'), R('1.8'), R('0.40'), 18
Ne = me * (g + aye)
Ne_ok = chk(Ne, 0, '29'); Ne_g = chk(me * g, 0, '25'); Ne_m = chk(me * (g - aye), 0, '20'); Ne_ma = chk(me * aye, 1, '4.5')
named(Ne_ok, Ne_g, Ne_m, Ne_ma)
axe = (Fe - mue * Ne) / me
ax_ok = chk(axe, 1, '2.6'); ax_g = chk((Fe - mue * me * g) / me, 1, '3.3')
ax_m = chk((Fe - mue * me * (g - aye)) / me, 1, '4.0'); ax_nof = chk(R(Fe) / me, 1, '7.2')
named(ax_ok, ax_g, ax_m, ax_nof)
# h/i. An angled pull on a rough floor.
mh, Fh, thh, muh = 18, 95, 20, R('0.40')
Nh = mh * g - Fh * sin(thh); fh = muh * Nh
fh_ok = chk(fh, 0, '58'); fh_no = chk(muh * mh * g, 0, '71')
fh_add = chk(muh * (mh * g + Fh * sin(thh)), 0, '84'); fh_swap = chk(muh * (mh * g - Fh * cos(thh)), 0, '35')
named(fh_ok, fh_no, fh_add, fh_swap)
ah = (Fh * cos(thh) - fh) / mh
ah_ok = chk(ah, 1, '1.8'); ah_no = chk((Fh * cos(thh) - muh * mh * g) / mh, 2, '1.04')
ah_whole = chk((Fh - fh) / mh, 1, '2.1'); ah_add = chk((Fh * cos(thh) + fh) / mh, 1, '8.2')
named(ah_ok, ah_no, ah_whole, ah_add)
# j–m. Up a rough slope and back down.
thj, v0j, muj = 25, R('6.0'), R('0.15')
a_up = g * (sin(thj) + muj * cos(thj))
a_dn = g * (sin(thj) - muj * cos(thj))
up_ok = chk(a_up, 1, '5.5'); up_fup = chk(a_dn, 1, '2.8')
up_swap = chk(g * (cos(thj) + muj * sin(thj)), 1, '9.5'); up_nof = chk(g * sin(thj), 1, '4.1')
named(up_ok, up_fup, up_swap, up_nof)
dj = v0j**2 / (2 * a_up)          # from v² = v₀² + 2aΔx with v = 0, a = −a_up
assert sp.simplify(0 - (v0j**2 - 2 * a_up * dj)) == 0
dj_ok = chk(dj, 1, '3.3'); dj_fup = chk(v0j**2 / (2 * a_dn), 1, '6.4')
dj_no2 = chk(v0j**2 / a_up, 1, '6.6'); dj_nosq = chk(v0j / (2 * a_up), 2, '0.55')
named(dj_ok, dj_fup, dj_no2, dj_nosq)
dn_ok = chk(a_dn, 1, '2.8'); dn_down = up_ok; dn_nof = up_nof
dn_swap = chk(g * (cos(thj) - muj * sin(thj)), 1, '8.3')
named(dn_ok, dn_down, dn_nof, dn_swap)
assert sp.tan(sp.Rational(thj) * sp.pi / 180).evalf() > muj      # it does slide back
vb = sp.sqrt(2 * a_dn * dj)
vb_ok = chk(vb, 1, '4.3'); vb_same = '6.0'; vb_nosq = chk(2 * a_dn * dj, 0, '18')
vb_nof = chk(sp.sqrt(2 * g * sin(thj) * dj), 1, '5.2')
named(vb_ok, vb_same, vb_nosq, vb_nof)
assert sp.N(sp.sqrt(2 * a_up * dj)) == sp.N(v0j)              # using a_up just returns 6.0
# n. A puck stopped by friction on an elevator floor.
vn, ayn, dn_ = R('3.5'), R('1.2'), R('1.75')
decel = vn**2 / (2 * dn_); assert decel == R('3.5')
mun = decel / (g + ayn)
mun_ok = chk(mun, 2, '0.32'); mun_g = chk(decel / g, 2, '0.36')
mun_m = chk(decel / (g - ayn), 2, '0.41'); mun_no2 = chk(vn**2 / dn_ / (g + ayn), 2, '0.64')
named(mun_ok, mun_g, mun_m, mun_no2)

C, Q = [], []
card(C, 'The coefficient of friction',
     '**μ is the friction force divided by the normal force. It has no '
     'units.**\n'
     '• Both are forces in newtons, so the units cancel.\n'
     '• It describes the two surfaces, not the object’s size or weight.',
     eq='μ = f / N')
card(C, 'Find N first',
     '**Friction depends on the normal force, so find N before you find '
     'friction.**\n'
     '• N equals mg only on a level surface, at rest or at constant velocity, '
     'with nothing else pushing up or down.\n'
     '• An angled pull, a slope, a push from above or an accelerating '
     'elevator all change N.', hint='No N, no friction.', frm='added')
card(C, 'Constant velocity gives μ directly',
     '**Pulled level at constant velocity, the friction exactly balances the '
     'pull, so μ = pull ÷ mg.**\n'
     '• Constant velocity means zero net force — not zero friction.\n'
     '• This is how a coefficient is measured in a lab.', eq='μ_k = F_pull / mg')
card(C, 'Kinetic friction',
     '**Once a surface slides, kinetic friction is μ_k N and points against the '
     'sliding.**\n'
     '• It does not change with speed.\n'
     '• It always opposes the motion relative to the surface — never “the '
     'direction it is pulled from”.', eq='f_k = μ_k N')
card(C, 'Two blocks: each has its own friction',
     '**On a rough floor every block has its own friction, μ × its own normal '
     'force.**\n'
     '• The heavier block has the bigger friction.\n'
     '• The system’s total friction is the sum of the two.')
card(C, 'Two blocks: the system acceleration',
     '**Subtract BOTH blocks’ friction from the pull, then divide by the total '
     'mass.**\n'
     '• a = (F − f₁ − f₂) ÷ (m₁ + m₂).\n'
     '• Adding friction instead of subtracting it is the slip to watch for.',
     eq='a = (F − f₁ − f₂) / (m₁ + m₂)')
card(C, 'Two blocks: the tension',
     '**For the block behind, the string pulls forward and friction pulls '
     'back: T − f = m a.**\n'
     '• So T = m(a + μg) for that block.\n'
     '• Leaving friction out of that block’s equation makes the tension too '
     'small.')
card(C, 'A surprise in the tension',
     '**When both blocks have the same μ, the tension is the same share of the '
     'pull it would be with no friction at all: T = F × m_back / (m₁ + m₂).**\n'
     '• Friction slows both blocks in proportion to their masses, so the '
     'string has no extra work to do.\n'
     '• This only holds while both blocks are sliding.', frm='added')
card(C, 'Friction in an accelerating elevator',
     '**In an elevator accelerating up, the floor pushes harder, N = m(g + a), '
     'so friction grows too.**\n'
     '• Accelerating down, N = m(g − a) and friction shrinks.\n'
     '• In free fall the normal force — and the friction — would be zero.',
     eq='f = μ m(g + a)')
card(C, 'An angled pull and friction',
     '**Pulling up at an angle lowers the normal force, so it lowers the '
     'friction as well.**\n'
     '• N = mg − F sin θ, then f = μN.\n'
     '• The same pull held level presses nothing off the floor, so it meets '
     'more friction.')
card(C, 'Sliding UP a rough slope',
     '**On the way up, gravity’s down-slope part and friction BOTH point down '
     'the slope.**\n'
     '• Friction opposes the sliding, which is up the slope.\n'
     '• So the deceleration is g(sin θ + μ cos θ).',
     eq='a = −g(sin θ + μ cos θ)', hint='Going up, both arrows point down.')
card(C, 'How far up before it stops',
     '**Use v² = v₀² + 2aΔx with v = 0: the distance is v₀² ÷ 2|a|.**\n'
     '• Square the starting speed; keep the 2.\n'
     '• The bigger the deceleration, the shorter the slide.',
     eq='v² = v₀² + 2aΔx')
card(C, 'Coming back down',
     '**On the way down, friction flips to point UP the slope, so the '
     'acceleration is smaller: g(sin θ − μ cos θ).**\n'
     '• It only slides back if the slope is steep enough to beat static '
     'friction.\n'
     '• Friction always opposes the sliding, so it reverses when the motion '
     'does.', eq='a = g(sin θ − μ cos θ)')
card(C, 'Slower at the bottom',
     '**A block that slides up a rough slope and back comes down slower than it '
     'went up.**\n'
     '• Friction took energy on the way up AND on the way down.\n'
     '• Only on a frictionless slope would it return at its starting speed.')
card(C, 'Stopping on an elevator floor',
     '**A puck sliding to a stop on an accelerating elevator floor decelerates '
     'at μ(g + a), because the floor presses harder.**\n'
     '• Find the deceleration from v₀² ÷ 2Δx, then divide by (g + a) to get μ.\n'
     '• Using g alone overestimates μ.', eq='μ = v₀² / [2Δx (g + a)]')
card(C, 'Your sheet’s g',
     '**This unit uses g = 9.8 m/s² as a size and says “down” in words.**\n'
     '• Your sheets may write −9.8 or 10; the minus is only the direction.\n'
     '• With g = 10 your answers come out a little different, and both are '
     'right for their g.', frm='added')

q(Q, 1, 'What does the coefficient of friction μ compare?',
  ['The friction force with the normal force pressing the surfaces together',
   'The friction force with the object’s mass in kilograms',
   'The pulling force with the object’s weight when it speeds up',
   'The friction force with the speed the object slides at'],
  0, 'μ = f / N.',
  ['μ is defined as friction divided by normal force.',
   'Both are forces, so μ has no units.',
   'It describes how grippy the two surfaces are.',
   'It compares friction with the normal force.'],
  '**μ = f ÷ N, two forces, so it has no units.** Dividing by a mass would '
  'give units of m/s², and kinetic friction does not depend on speed.',
  'Friction per newton of squeeze.')

q(Q, 2, 'An 85 N horizontal force pulls a 40 kg box across a level floor at '
        'constant velocity. What is the coefficient of kinetic friction?',
  [mu_ok, mu_m, mu_inv, '0.00'],
  0, 'At constant velocity, friction equals the pull.',
  ['Constant velocity: net force zero, so friction = 85 N.',
   'Level floor, level pull: N = mg = 40 × 9.8 = 392 N.',
   'μ = f / N = 85 ÷ 392.',
   'μ ≈ 0.22.'],
  '**μ = 85 ÷ 392 ≈ 0.22.** 2.1 divides by the mass instead of the weight; '
  '4.6 divides the wrong way up; 0.00 mistakes “zero net force” for “zero '
  'friction”.',
  'Constant velocity: friction = pull.')

q(Q, 2, 'A 2.0 kg block and a 3.0 kg block, joined by a string, slide across a '
        'rough floor. μ_k = 0.35 between each block and the floor. How big is '
        'the friction on the 3.0 kg block?',
  [fb_ok + ' N', fb_tot + ' N', fb_m + ' N', fb_oth + ' N'],
  0, 'Each block has its own normal force.',
  ['On a level floor, the 3.0 kg block’s N = 3.0 × 9.8 = 29.4 N.',
   'f = μN = 0.35 × 29.4.',
   'f = 10.3 N.',
   'About 10 N.'],
  '**f = 0.35 × 3.0 × 9.8 ≈ 10 N.** 17 N is the friction on both blocks '
  'together; 1.05 N uses the mass as if it were a weight; 6.9 N is the 2.0 kg '
  'block’s friction.',
  'Each block: μ × its own N.')

q(Q, 3, 'A 2.0 kg block and a 3.0 kg block, joined by a string, are pulled '
        'across a rough floor by a 45 N horizontal force on the 3.0 kg block. '
        'μ_k = 0.35 between each block and the floor. What is their acceleration?',
  [ab_ok + ' m/s²', ab_nof + ' m/s²', ab_add + ' m/s²', ab_one + ' m/s²'],
  0, 'Subtract both frictions, divide by both masses.',
  ['Frictions: 0.35 × 2.0 × 9.8 = 6.86 N and 0.35 × 3.0 × 9.8 = 10.29 N.',
   'Net force on the system: 45 − 6.86 − 10.29 = 27.85 N.',
   'a = 27.85 ÷ 5.0 kg.',
   'a ≈ 5.6 m/s².'],
  '**a = (45 − 17.15) ÷ 5.0 ≈ 5.6 m/s².** 9.0 leaves friction out; 12 adds '
  'friction instead of subtracting it; 6.9 subtracts only the pulled block’s '
  'friction.',
  'Every sliding block brings its own friction.')

q(Q, 3, 'A 2.0 kg block and a 3.0 kg block, joined by a string, are pulled '
        'across a rough floor by a 45 N horizontal force on the 3.0 kg block, '
        'so both accelerate at about 5.57 m/s². μ_k = 0.35 between each block '
        'and the floor. What is the tension in the string?',
  [Tb_ok + ' N', Tb_pull + ' N', Tb_big + ' N', Tb_nof + ' N'],
  0, 'Use the 2.0 kg block: the string pulls it forward, friction pulls it back.',
  ['For the 2.0 kg block: T − f = ma.',
   'f = 0.35 × 2.0 × 9.8 = 6.86 N; ma = 2.0 × 5.57 = 11.14 N.',
   'T = 11.14 + 6.86 = 18.0 N.',
   'The tension is 18 N.'],
  '**T = ma + f = 11.1 + 6.9 = 18 N** — exactly 45 × 2.0 ÷ 5.0, the same share '
  'as with no friction. 45 N sets the tension equal to the pull; 27 N works '
  'from the pulled block as if the string dragged it; 11 N leaves friction out '
  'of the back block’s equation.',
  'The back block needs force for its acceleration AND its friction.')

q(Q, 3, 'Two blocks joined by a string are pulled across a rough floor by a '
        'steady horizontal force, and the same μ_k applies to both. If the '
        'floor were made rougher for both blocks, with both still sliding, what '
        'would happen to the tension in the string?',
  ['It would stay the same',
   'It would grow, because the back block has more friction to overcome',
   'It would shrink, because the blocks accelerate less',
   'It would become equal to the pull, because nothing accelerates'],
  0, 'T = m_back(a + μg), and a = F/M − μg.',
  ['System: a = F / (m₁ + m₂) − μg.',
   'Back block: T = m_back(a + μg).',
   'Substituting, the μg terms cancel: T = F × m_back / (m₁ + m₂).',
   'μ is gone, so the tension stays the same.'],
  '**It stays the same.** More friction does take away acceleration, but it '
  'also adds the same μg per kilogram to what the string must supply, and the '
  'two cancel exactly. It holds while both blocks still slide.',
  'Equal μ: friction drops out of the tension.', frm='added')

q(Q, 2, 'A 2.5 kg block rests on a table inside an elevator that is '
        'accelerating upward at 1.8 m/s². What is the normal force on the block?',
  [Ne_ok + ' N', Ne_g + ' N', Ne_m + ' N', Ne_ma + ' N'],
  0, 'The table must also push it faster.',
  ['Upward positive: N − mg = ma.',
   'N = m(g + a) = 2.5 × (9.8 + 1.8).',
   'N = 2.5 × 11.6 = 29 N.',
   'The normal force is 29 N.'],
  '**N = 2.5 × 11.6 = 29 N.** 25 N ignores the elevator; 20 N flips the sign '
  'of a; 4.5 N is only ma.',
  'Elevator up: g + a.')

q(Q, 3, 'A 2.5 kg block on a table inside an elevator accelerating upward at '
        '1.8 m/s² is pushed sideways with 18 N. μ_k = 0.40 between block and '
        'table. What is its horizontal acceleration?',
  [ax_ok + ' m/s²', ax_g + ' m/s²', ax_m + ' m/s²', ax_nof + ' m/s²'],
  0, 'The normal force is m(g + a), not mg.',
  ['N = 2.5 × (9.8 + 1.8) = 29 N.',
   'f = 0.40 × 29 = 11.6 N.',
   'Horizontally: a = (18 − 11.6) ÷ 2.5.',
   'a ≈ 2.6 m/s².'],
  '**a = (18 − 0.40 × 29) ÷ 2.5 ≈ 2.6 m/s².** 3.3 uses N = mg, ignoring the '
  'elevator; 4.0 flips the sign to g − a; 7.2 leaves friction out.',
  'Elevator going up: more friction.')

q(Q, 2, 'A box slides across the floor of an elevator that is accelerating '
        'DOWNWARD. Compared with the same slide in an elevator at rest, the '
        'friction on the box is…',
  ['smaller, because the floor presses up on the box less hard',
   'larger, because the box presses down harder while it falls',
   'the same, because μ only depends on the two surfaces',
   'zero, because the box is falling with the elevator'],
  0, 'f = μN. What happens to N?',
  ['Accelerating down: N = m(g − a).',
   'That is less than mg.',
   'Friction is μN, so it is smaller too.',
   'Friction is smaller.'],
  '**N = m(g − a) is smaller, so friction is smaller.** μ is unchanged — it is '
  'N that changes. Friction would only vanish in free fall, where a = g.',
  'Friction rides on the normal force.')

q(Q, 2, 'An 18 kg box is pulled across a level floor by a rope at 20° above the '
        'horizontal with a 95 N force. μ_k = 0.40. How big is the friction?',
  [fh_ok + ' N', fh_no + ' N', fh_add + ' N', fh_swap + ' N'],
  0, 'Find N first: the rope lifts a little.',
  ['Weight: 18 × 9.8 = 176.4 N.',
   'Rope’s vertical part: 95 sin 20° = 32.5 N, so N = 176.4 − 32.5 = 143.9 N.',
   'f = 0.40 × 143.9.',
   'f ≈ 58 N.'],
  '**f = 0.40 × (176.4 − 32.5) ≈ 58 N.** 71 N forgets to subtract the rope’s '
  'lift; 84 N adds it; 35 N subtracts 95 cos 20°, sine and cosine swapped.',
  'Normal force first, then friction.')

q(Q, 3, 'An 18 kg box is pulled across a level floor by a rope at 20° above the '
        'horizontal with a 95 N force. μ_k = 0.40, and the friction on it is '
        'about 58 N. What is its acceleration?',
  [ah_ok + ' m/s²', ah_no + ' m/s²', ah_whole + ' m/s²', ah_add + ' m/s²'],
  0, 'Horizontal part of the pull, minus friction, over the mass.',
  ['Horizontal part: 95 cos 20° = 89.3 N.',
   'Net force: 89.3 − 57.6 = 31.7 N.',
   'a = 31.7 ÷ 18.',
   'a ≈ 1.8 m/s².'],
  '**a = (89.3 − 57.6) ÷ 18 ≈ 1.8 m/s².** 1.04 uses the friction you would get '
  'with N = mg; 2.1 uses the whole 95 N as if the rope were level; 8.2 adds '
  'friction.',
  'Forward part minus friction.')

q(Q, 2, 'Two equal boxes are dragged across the same rough floor with pulls of '
        'equal size: one pulled level, one pulled upward at an angle. Which '
        'box meets less friction?',
  ['The one pulled upward, because its normal force is smaller',
   'The one pulled level, because all of its pull is horizontal',
   'Neither, because both boxes have the same weight',
   'Neither, because both pulls are the same size'],
  0, 'Friction = μN. Which normal force is smaller?',
  ['The angled pull has an upward part, F sin θ.',
   'That takes some weight off the floor: N = mg − F sin θ.',
   'Smaller N means smaller μN.',
   'The box pulled upward meets less friction.'],
  '**The angled pull lifts a little, so N and friction both shrink.** Same '
  'weight is not the same normal force once something else pushes up.',
  'Lift a little, drag less.')

q(Q, 2, 'A block slides UP a 25° ramp, starting at 6.0 m/s. μ_k = 0.15. What '
        'is its acceleration while it slides up?',
  [up_ok + ' m/s² down the slope', up_fup + ' m/s² down the slope',
   up_swap + ' m/s² down the slope', up_nof + ' m/s² down the slope'],
  0, 'Going up, which way do gravity’s part and friction point?',
  ['Friction opposes the sliding, so it points DOWN the slope.',
   'Gravity’s part also points down the slope.',
   'a = g(sin 25° + 0.15 cos 25°) = 9.8 × (0.423 + 0.136).',
   'a ≈ 5.5 m/s² down the slope.'],
  '**a = g(sin θ + μ cos θ) ≈ 5.5 m/s² down the slope.** 2.8 leaves friction '
  'pointing up the slope, as if it were coming down; 9.5 swaps sine and '
  'cosine; 4.1 forgets friction.',
  'Up the slope: both arrows point down.')

q(Q, 3, 'A block slides UP a 25° ramp, starting at 6.0 m/s. μ_k = 0.15. How far '
        'up the ramp does it slide before it stops?',
  [dj_ok + ' m', dj_fup + ' m', dj_no2 + ' m', dj_nosq + ' m'],
  0, 'Find the deceleration, then use v² = v₀² + 2aΔx with v = 0.',
  ['Deceleration: g(sin 25° + 0.15 cos 25°) ≈ 5.47 m/s².',
   '0 = 6.0² − 2 × 5.47 × Δx.',
   'Δx = 36 ÷ 10.95.',
   'Δx ≈ 3.3 m.'],
  '**Δx = 6.0² ÷ (2 × 5.47) ≈ 3.3 m.** 6.4 m uses friction pointing up the '
  'slope; 6.6 m drops the 2; 0.55 m forgets to square the speed.',
  'Square the speed, keep the 2.')

q(Q, 2, 'A block that slid up a 25° ramp stops and then slides back down. '
        'μ_k = 0.15. What is its acceleration on the way down?',
  [dn_ok + ' m/s² down the slope', dn_down + ' m/s² down the slope',
   dn_nof + ' m/s² down the slope', dn_swap + ' m/s² down the slope'],
  0, 'Friction opposes the sliding — which way is that now?',
  ['It now slides down, so friction points UP the slope.',
   'Gravity’s part still points down.',
   'a = g(sin 25° − 0.15 cos 25°) = 9.8 × (0.423 − 0.136).',
   'a ≈ 2.8 m/s² down the slope.'],
  '**a = g(sin θ − μ cos θ) ≈ 2.8 m/s²** — smaller than on the way up, '
  'because friction flipped. 5.5 leaves friction pointing down the slope; 4.1 '
  'forgets friction; 8.3 swaps sine and cosine.',
  'Friction turns round when the motion does.')

q(Q, 3, 'A block slides UP a 25° ramp starting at 6.0 m/s, stops about 3.3 m up, '
        'and slides back down. μ_k = 0.15. How fast is it moving when it '
        'reaches the bottom?',
  [vb_ok + ' m/s', vb_same + ' m/s', vb_nosq + ' m/s', vb_nof + ' m/s'],
  0, 'Use the down-slope acceleration over the same distance.',
  ['On the way down, a = g(sin 25° − 0.15 cos 25°) ≈ 2.81 m/s².',
   'It slides Δx ≈ 3.29 m from rest.',
   'v² = 2 × 2.81 × 3.29 ≈ 18.5.',
   'v ≈ 4.3 m/s.'],
  '**v = √(2 × 2.81 × 3.29) ≈ 4.3 m/s**, slower than the 6.0 m/s it started '
  'with, because friction took energy both ways. 6.0 m/s is what a '
  'frictionless ramp would give; 18 forgets the square root; 5.2 forgets '
  'friction on the way down.',
  'Rough slope: it comes back slower.')

q(Q, 3, 'A puck slides across the floor of an elevator that is accelerating '
        'upward at 1.2 m/s². It starts at 3.5 m/s and stops in 1.75 m. What is '
        'the coefficient of kinetic friction?',
  [mun_ok, mun_g, mun_m, mun_no2],
  0, 'Deceleration from the stop; then μ = deceleration ÷ (g + a).',
  ['Deceleration: v₀² ÷ 2Δx = 3.5² ÷ (2 × 1.75) = 3.5 m/s².',
   'Friction supplies it: μ m(g + a) = m × 3.5.',
   'μ = 3.5 ÷ (9.8 + 1.2) = 3.5 ÷ 11.0.',
   'μ ≈ 0.32.'],
  '**μ = 3.5 ÷ 11.0 ≈ 0.32.** 0.36 ignores the elevator; 0.41 flips its sign '
  'to g − a; 0.64 drops the 2 in v² = 2aΔx.',
  'The elevator presses the puck harder.')

q(Q, 1, 'A box sits on a level floor with nothing else pushing or pulling it '
        'up or down. When is its normal force equal to mg?',
  ['In an elevator moving up at a steady speed',
   'In an elevator speeding up on the way up',
   'When it is pulled by a rope angled upward',
   'When someone presses down on its lid'],
  0, 'N = mg needs zero vertical acceleration and no other vertical force.',
  ['A steady speed means no vertical acceleration.',
   'Speeding up adds ma to N.',
   'An upward rope or a push from above changes N too.',
   'Only the steady elevator gives N = mg.'],
  '**At a steady speed there is no acceleration, so N = mg.** Speeding up '
  'gives m(g + a); an upward rope takes F sin θ off; a press from above adds '
  'to it.', 'Check every vertical force before writing N = mg.')

q(Q, 2, 'Put the steps for finding how far a block slides UP a rough ramp in '
        'order.',
  ['Draw the forces: gravity’s part and friction both down the slope',
   'Find the normal force, N = mg cos θ, and then friction, f = μN',
   'Find the deceleration, a = (mg sin θ + f) ÷ m',
   'Use v² = v₀² + 2aΔx with v = 0 to solve for Δx'],
  0, 'Forces, then N, then a, then distance.',
  ['Start with the free-body diagram.',
   'Friction needs the normal force.',
   'The net force gives the deceleration.',
   'The kinematic equation gives the distance.'],
  '**Diagram, normal force and friction, deceleration, then distance.** Each '
  'step needs the one before: friction needs N, the deceleration needs '
  'friction, and the distance needs the deceleration.',
  'Forces before motion.', kind='order')

fresh(Q)
NOTE_FR = (
    'From Friction_and_the_Coefficient.pdf in the Dynamics 2 folder. The sheet '
    'was read for what it asks — μ from a constant-velocity pull, two blocks '
    'with friction on each, friction in an accelerating elevator, a block '
    'sliding up a rough ramp and back, and a puck stopped on an elevator floor '
    '— and nothing of hers was marked or recorded. Dynamics 1 · 1-2 already '
    'teaches μ, static and kinetic friction, so this unit is the applied '
    'layer: the normal force first (it is not always mg), then friction, then '
    'the motion. Every number was computed with sympy and checked; every wrong '
    'option is a named slip (mass used as weight, the angled pull’s lift not '
    'subtracted, friction added, friction left pointing up the slope on the '
    'way up, g + a flipped, the 2 or the square dropped in v² = 2aΔx), and '
    'none of the sheet’s numbers is reused. One card notes that with equal μ '
    'the tension between two blocks does not depend on friction; it is ours, '
    'flagged as a study suggestion. Things on the sheet worth knowing: '
    'problem 2 says the blocks are “as shown to the right”, and that picture '
    'was not seen, so their masses are unknown here; problem 4(f), the speed '
    'back at the bottom, is extra credit. This unit uses g = 9.8 m/s²; her '
    'sheets may write −9.8 or 10.')
build('ad-astra', C, Q, 'unit-phys-dyn2-friction',
      'Dynamics 2 · 2-2 Friction and the Coefficient', 'physics',
      'Friction problems with more than one step: μ from a constant-velocity '
      'pull, two connected blocks each with its own friction, friction in an '
      'accelerating elevator where the floor presses harder, an angled pull '
      'that lifts some weight off the floor, and a block sliding up a rough '
      'ramp — how far it goes, and how it comes back down slower.',
      'Friction is where the normal force stops being “just mg”. Getting N '
      'right first is what makes every one of these problems come out.',
      [('Find the coefficient of friction from a constant-velocity pull.', 'source'),
       ('Find the friction on each of two connected blocks, their acceleration and the tension.', 'source'),
       ('Find the normal force and friction in an accelerating elevator.', 'source'),
       ('Find the acceleration and stopping distance of a block sliding up a rough ramp.', 'source'),
       ('Explain why a block comes back down a rough ramp slower than it went up.', 'source'),
       ('Find the normal force before finding any friction.', 'added')],
      NOTE_FR,
      ('Read the cards, then take the quiz. For every problem, find the normal '
       'force before you touch μ.', 30),
      'content/phys-dyn2-friction.json', 'Friction and the Coefficient (worksheet)', SRC_FR,
      offset_hours=3, libv_=1)
patch('content/phys-dyn2-friction.json', 'unit-phys-dyn2-friction', quarter=2)

# =============================================================================
# 2-3 THE NEWTON'S SECOND LAW LAB
# =============================================================================
mh_g = R('0.120')
w_ok = chk(mh_g * g, 1, '1.2'); w_g = chk(120 * g, 0, '1176'); w_m = '0.12'
w_div = chk(mh_g / g, 3, '0.012')
named(w_ok, w_g, w_m, w_div)
M_ok = chk(R('0.50') + R('0.25') + R('0.050'), 2, '0.80')
M_noh = chk(R('0.50') + R('0.25'), 2, '0.75'); M_nocart = chk(R('0.50') + R('0.050'), 2, '0.55')
M_noC = chk(R('0.50') + R('0.25') - R('0.050'), 2, '0.70')
named(M_ok, M_noh, M_nocart, M_noC)
dx, tt = R('0.72'), R('1.2')
al_ok = chk(2 * dx / tt**2, 1, '1.0'); al_no2 = chk(dx / tt**2, 2, '0.50')
al_v = chk(dx / tt, 2, '0.60'); al_nosq = chk(2 * dx / tt, 1, '1.2')
named(al_ok, al_no2, al_v, al_nosq)
p1, p2 = (R('0.80'), R('0.64')), (R('2.0'), R('1.6'))
sl = (p2[1] - p1[1]) / (p2[0] - p1[0]); assert sl == R('0.8')
assert p1[1] / p1[0] == sl and p2[1] / p2[0] == sl      # through the origin
sl_ok = chk(sl, 2, '0.80'); sl_inv = chk(1 / sl, 2, '1.25')
sl_div = chk(sl / g, 3, '0.082'); sl_mul = chk(sl * g, 1, '7.8')
named(sl_ok, sl_inv, sl_div, sl_mul)
runs = [(R('0.50'), R('1.86')), (R('0.75'), R('1.28')), (R('1.00'), R('0.99'))]
Fs = [m * a for m, a in runs]
avg_ok = chk(sum(Fs) / 3, 2, '0.96'); avg_sum = chk(sum(Fs), 1, '2.9')
avg_a = chk(sum(a for _, a in runs) / 3, 1, '1.4'); avg_div = chk(sum(a / m for m, a in runs) / 3, 1, '2.1')
named(avg_ok, avg_sum, avg_a, avg_div)
ex, ac = R('0.90'), R('0.98')
pe_ok = chk(abs(ex - ac) / ac * 100, 1, '8.2'); pe_exp = chk(abs(ex - ac) / ex * 100, 1, '8.9')
pe_no100 = chk(abs(ex - ac) / ac, 3, '0.082'); pe_ratio = chk(ex / ac * 100, 0, '92')
named(pe_ok, pe_exp, pe_no100, pe_ratio)
pd = abs(ex - ac) / ((ex + ac) / 2) * 100; assert f(pd, 1) == '8.5'     # % difference, for the card
# Moon: weight of the hanging mass is 1/6, total mass unchanged → a is 1/6.
for M in (R('0.5'), R('1.0')):
    assert sp.simplify((mh_g * g / 6 / M) / (mh_g * g / M) - R(1) / 6) == 0
GRAPH_M = {'w': [0, 1.6, 0, 2.4], 'gx': 0.2, 'gy': 0.4,
           'series': [{'type': 'pts', 'pts': [[float(m), round(0.96 / float(m), 3)]
                                              for m in [0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.4, 1.6]]}],
           'xl': 'total mass M (kg)', 'yl': 'a (m/s²)'}
GRAPH_L = {'w': [0, 2.5, 0, 2.4], 'gx': 0.5, 'gy': 0.4,
           'series': [{'type': 'line', 'm': 0.96, 'b': 0}],
           'xl': '1 / M (1/kg)', 'yl': 'a (m/s²)'}

C, Q = [], []
card(C, 'What the lab is testing',
     '**How the acceleration of a system depends on its total mass, when the '
     'pulling force stays the same.**\n'
     '• The force is held constant; the total mass is changed run by run.\n'
     '• Newton’s second law predicts a = F / M.')
card(C, 'The pulling force is the hanging weight',
     '**The force that speeds the system up is the weight of the hanging mass: '
     'F = m_hanging × g.**\n'
     '• Convert grams to kilograms before multiplying by 9.8.\n'
     '• A mass in kilograms is not a weight in newtons.', eq='F = m_h g')
card(C, 'Total system mass',
     '**Everything that moves counts: the cart, the mass on the cart and the '
     'hanging mass.**\n'
     '• Your sheet writes it as Total System Mass = Mass on Cart + Mass of '
     'Cart + Mass Hanging.', eq='M = m_on cart + m_cart + m_hanging')
card(C, 'Why the hanging mass counts',
     '**The hanging mass speeds up too, so its weight has to accelerate it as '
     'well as the cart.**\n'
     '• The string makes the cart and the hanging mass one system with one '
     'acceleration.\n'
     '• Leaving it out makes M too small, so the force you work out from Ma '
     'comes out too small.', hint='If it moves, it is in M.')
card(C, 'Keep the force fixed',
     '**Change only the mass ON the cart, so the hanging weight — the force — '
     'stays the same every run.**\n'
     '• Changing the hanging mass would change the force and the total mass at '
     'once, and you could not tell which caused what.', frm='added')
card(C, 'Acceleration from distance and time',
     '**The cart starts from rest, so Δx = ½at², which rearranges to '
     'a = 2Δx / t².**\n'
     '• Starting from rest is what removes the v₀t term.\n'
     '• Square the time; keep the 2. Δx / t is an average speed, not an '
     'acceleration.', eq='a = 2Δx / t²')
card(C, 'Do not graph distance against time',
     '**Your sheet says not to graph distance and time: each run gives ONE '
     'acceleration, and the graph is acceleration against mass.**\n'
     '• The distance and time are only the route to each run’s a.')
card(C, 'Acceleration against mass is a curve',
     '**Plotted against the total mass, the acceleration falls along a curve, '
     'not a straight line.**\n'
     '• Double the mass and a halves; it never quite reaches zero.\n'
     '• That inverse shape is hard to read a constant from.')
C[-1]['graph'] = GRAPH_M
card(C, 'Linearize: plot a against 1/M',
     '**Plot acceleration against 1 ÷ total mass and the points fall on a '
     'straight line through the origin.**\n'
     '• a = F × (1/M) has the shape y = mx.\n'
     '• Make a second data table with a 1/M column before you graph.',
     eq='a = F (1 / M)')
C[-1]['graph'] = GRAPH_L
card(C, 'The slope is the force',
     '**The slope of a against 1/M is the pulling force — the hanging weight — '
     'in newtons.**\n'
     '• Units: (m/s²) ÷ (1/kg) = kg·m/s² = N.\n'
     '• Divide the slope by g to get the hanging mass back.',
     eq='slope = F = m_h g')
card(C, 'The average force',
     '**Multiply each run’s total mass by its acceleration to get a force, then '
     'average those forces.**\n'
     '• If the law holds, every run gives about the same F.\n'
     '• The average should come close to the hanging weight.', eq='F = Ma')
card(C, 'Percent error and percent difference',
     '**Percent error compares a measurement with an accepted value; percent '
     'difference compares two measurements with each other.**\n'
     '• Percent error: |experimental − actual| ÷ actual × 100.\n'
     '• Percent difference: |A − B| ÷ the average of A and B × 100.\n'
     '• The hanging weight is the accepted value here, so the formula your '
     'sheet prints is the percent-error one.', frm='added')
card(C, 'On the Moon',
     '**On the Moon the hanging weight is one-sixth as big, so every '
     'acceleration is one-sixth as big — the masses do not change.**\n'
     '• The line on the a-against-1/M graph is one-sixth as steep.\n'
     '• Saying “nothing changes because mass is the same everywhere” misses '
     'that the FORCE is a weight.')
card(C, 'Friction as a source of error',
     '**Friction in the wheels and pulley makes the measured acceleration too '
     'low, so the force worked out from Ma comes out lower than the hanging '
     'weight.**\n'
     '• Lessen it: a smooth track, free-spinning wheels and pulley, or tilt '
     'the track just enough that the cart rolls at a steady speed with no '
     'hanging mass.', frm='added')

q(Q, 1, 'What relationship does a cart-and-hanging-mass lab investigate when '
        'the mass on the cart is changed run by run?',
  ['How the system’s acceleration depends on its total mass, with the force kept the same',
   'How the hanging weight depends on the speed the cart reaches at the edge',
   'How the distance the cart travels depends on the length of the table',
   'How the friction on the cart depends on the size of the hanging weight'],
  0, 'What is changed, and what is kept the same?',
  ['The hanging mass stays the same, so the pulling force stays the same.',
   'The mass on the cart changes, so the total mass changes.',
   'Each run measures the acceleration.',
   'So the lab tests how acceleration depends on total mass.'],
  '**Fixed force, changing total mass, measured acceleration.** The law it '
  'tests is a = F / M.', 'Fixed F, change M, measure a.')

q(Q, 1, 'A 120 g mass hangs from the string over the edge of the table. What '
        'force does it pull with?',
  [w_ok + ' N', w_g + ' N', w_m + ' N', w_div + ' N'],
  0, 'Weight = mass in kilograms × g.',
  ['120 g = 0.120 kg.',
   'F = mg = 0.120 × 9.8.',
   'F = 1.176 N.',
   'About 1.2 N.'],
  '**F = 0.120 kg × 9.8 ≈ 1.2 N.** 1176 N leaves the mass in grams; 0.12 N uses '
  'the mass as if it were a weight; 0.012 N divides by g.',
  'Grams to kilograms, then × 9.8.')

q(Q, 2, 'A 0.50 kg cart carries 0.25 kg of extra mass and is pulled by a 0.050 kg '
        'hanging mass. What total mass is being accelerated?',
  [M_ok + ' kg', M_noh + ' kg', M_nocart + ' kg', M_noC + ' kg'],
  0, 'Count everything that moves.',
  ['The cart moves: 0.50 kg.',
   'The mass on the cart moves with it: 0.25 kg.',
   'The hanging mass moves too: 0.050 kg.',
   'M = 0.50 + 0.25 + 0.050 = 0.80 kg.'],
  '**M = 0.80 kg.** 0.75 kg leaves out the hanging mass, which accelerates '
  'with the cart; 0.55 kg forgets the mass on the cart; 0.70 kg subtracts the '
  'hanging mass as if it pulled against the system.',
  'If it moves, it is in M.')

q(Q, 2, 'Starting from rest, a cart travels 0.72 m in 1.2 s at a steady '
        'acceleration. What is its acceleration?',
  [al_ok + ' m/s²', al_no2 + ' m/s²', al_v + ' m/s²', al_nosq + ' m/s²'],
  0, 'From rest: Δx = ½at².',
  ['From rest, Δx = ½at², so a = 2Δx / t².',
   'a = 2 × 0.72 ÷ 1.2².',
   'a = 1.44 ÷ 1.44.',
   'a = 1.0 m/s².'],
  '**a = 2 × 0.72 ÷ 1.44 = 1.0 m/s².** 0.50 drops the 2; 0.60 is Δx / t, an '
  'average speed; 1.2 forgets to square the time.',
  'Square the time, keep the 2.')

q(Q, 1, 'A cart starts from rest and you measure the distance Δx it travels in '
        'a time t. Which equation gives its acceleration?',
  ['a = 2Δx ÷ t²', 'a = Δx ÷ t²', 'a = Δx ÷ t', 'a = 2Δx ÷ t'],
  0, 'Start from Δx = v₀t + ½at² with v₀ = 0.',
  ['Δx = v₀t + ½at².',
   'From rest, v₀ = 0, so Δx = ½at².',
   'Multiply by 2 and divide by t².',
   'a = 2Δx / t².'],
  '**From rest, Δx = ½at², so a = 2Δx / t².** Δx ÷ t is an average speed, '
  'and dropping the 2 halves every acceleration.',
  'From rest, the ½ becomes a 2.')

q(Q, 2, 'Why must the hanging mass be included in the total mass of the system?',
  ['It accelerates along with the cart, so the force has to speed it up too',
   'Its weight pushes the cart down onto the table and adds to the friction',
   'It is the force, and forces are always added to the mass in this lab',
   'It hangs below the table, so it is the heaviest part of the system'],
  0, 'Does the hanging mass speed up?',
  ['The string joins the cart and the hanging mass.',
   'They move together with one acceleration.',
   'The hanging weight must accelerate everything that moves.',
   'So the hanging mass belongs in the total mass.'],
  '**The hanging mass speeds up with the cart, so it is part of what the '
  'force must accelerate.** It does not press on the cart, and a force is '
  'never added to a mass.', 'If it moves, it is in M.')

q(Q, 2, 'With the hanging mass kept the same, a graph of acceleration against '
        'total system mass would look like…',
  ['a curve that falls more and more slowly as the mass grows',
   'a straight line rising from the origin as the mass grows',
   'a straight line falling steadily until it reaches zero',
   'a flat line, because the pulling force never changes'],
  0, 'a = F / M with F fixed.',
  ['F is fixed, so a = F / M.',
   'Doubling M halves a; tripling M thirds it.',
   'That is an inverse relationship.',
   'It is a falling curve that never reaches zero.'],
  '**a = F / M is an inverse relationship: a falling curve, not a line.** It '
  'never reaches zero, and a fixed force does not mean a fixed acceleration.',
  'Inverse: a curve, not a line.')

q(Q, 2, 'To turn the lab’s data into a straight-line graph, what should you '
        'plot?',
  ['Acceleration against 1 ÷ total mass',
   'Acceleration against total mass squared',
   'Distance against time for each run',
   'Total mass against the hanging weight'],
  0, 'Make a = F / M look like y = mx.',
  ['a = F / M = F × (1/M).',
   'With y = a and x = 1/M, that is y = mx.',
   'So a against 1/M is a straight line through the origin.',
   'Plot acceleration against 1 ÷ total mass.'],
  '**a against 1/M is a straight line**, because a = F × (1/M). Distance '
  'against time is what your sheet tells you NOT to graph.',
  'Linearize by flipping the mass.')

q(Q, 3, 'In the lab, acceleration is plotted against 1 ÷ total mass and the '
        'points fall on a straight line. What does the slope of that line '
        'stand for?',
  ['The hanging weight — the force pulling the system',
   'The total mass of the cart and everything on it',
   'The acceleration of the cart on every run',
   'One divided by the hanging weight'],
  0, 'a = F × (1/M). What multiplies 1/M?',
  ['The line is a = (slope) × (1/M).',
   'Newton’s second law gives a = F × (1/M).',
   'So the slope is F.',
   'F is the hanging weight.'],
  '**The slope is the pulling force — the hanging weight — in newtons.** '
  'Units: (m/s²) ÷ (1/kg) = N. It is a force, not a mass or an acceleration.',
  'Slope of a against 1/M = F.')

q(Q, 2, 'A line of acceleration against 1 ÷ total mass passes through the '
        'origin, (0.80 kg⁻¹, 0.64 m/s²) and (2.0 kg⁻¹, 1.6 m/s²). What force '
        'pulled the system?',
  [sl_ok + ' N', sl_inv + ' N', sl_div + ' N', sl_mul + ' N'],
  0, 'The slope is the force.',
  ['Slope = rise ÷ run.',
   '= (1.6 − 0.64) ÷ (2.0 − 0.80) = 0.96 ÷ 1.2.',
   '= 0.80 N.',
   'The force is 0.80 N.'],
  '**Slope = 0.96 ÷ 1.2 = 0.80 N.** 1.25 N is run over rise, upside down; '
  '0.082 N divides by g (that is the hanging mass, in kg); 7.8 N multiplies '
  'by g, which was already inside the weight.',
  'Rise over run, then read it as newtons.')

q(Q, 2, 'Three lab runs gave a total mass of 0.50 kg at 1.86 m/s², 0.75 kg at '
        '1.28 m/s², and 1.00 kg at 0.99 m/s². What is the average force?',
  [avg_ok + ' N', avg_sum + ' N', avg_a + ' N', avg_div + ' N'],
  0, 'F = Ma for each run, then average.',
  ['Run forces: 0.50 × 1.86 = 0.93 N, 0.75 × 1.28 = 0.96 N, 1.00 × 0.99 = 0.99 N.',
   'Add them: 2.88 N.',
   'Divide by 3.',
   'The average force is 0.96 N.'],
  '**(0.93 + 0.96 + 0.99) ÷ 3 = 0.96 N.** 2.9 N adds without dividing; 1.4 N '
  'averages the accelerations and leaves the masses out; 2.1 N divides a by '
  'M instead of multiplying.',
  'One force per run, then the mean.')

q(Q, 3, 'A lab’s average force is 0.90 N and the hanging weight is 0.98 N. '
        'Using |experimental − actual| ÷ actual × 100, what is the result, in '
        'percent?',
  [pe_ok, pe_exp, pe_no100, pe_ratio],
  0, 'The hanging weight is the actual value.',
  ['|0.90 − 0.98| = 0.08 N.',
   'Divide by the actual value: 0.08 ÷ 0.98 = 0.0816.',
   'Multiply by 100.',
   'About 8.2.'],
  '**0.08 ÷ 0.98 × 100 ≈ 8.2 percent.** 8.9 divides by the experimental '
  'value; 0.082 forgets the × 100; 92 is the ratio of the two, not their '
  'difference.',
  'Divide by the accepted value.')

q(Q, 2, 'Which comparison calls for a percent DIFFERENCE rather than a percent '
        'error?',
  ['Two measured values, with no accepted value to compare against',
   'A measured value against a value printed in the textbook',
   'A measured acceleration against the accepted value of g',
   'A measured force against a weight worked out from a known mass'],
  0, 'Percent error needs an accepted value.',
  ['Percent error compares a measurement with an accepted value.',
   'Percent difference compares two measurements with each other.',
   'Every other choice has an accepted value to compare with.',
   'Two measured values call for a percent difference.'],
  '**Percent difference is for two measurements with no accepted value.** A '
  'textbook value, g, or a weight from a known mass is an accepted value — '
  'that is a percent error.',
  'Accepted value: error. Two measurements: difference.')

q(Q, 2, 'If the cart-and-hanging-mass lab were done on the Moon, where g is '
        'one-sixth of Earth’s, how would the measured accelerations change?',
  ['Each would be one-sixth as big, because the hanging weight is one-sixth as big',
   'Nothing would change, because the masses are the same on the Moon',
   'Each would be six times as big, because the cart weighs less on the Moon',
   'The cart would not move, because the hanging mass would weigh nothing'],
  0, 'What is the force, and what is the mass?',
  ['The force is the hanging WEIGHT, m_h g, which is one-sixth as big.',
   'The total mass is unchanged.',
   'a = F / M, so every a is one-sixth as big.',
   'The accelerations are each one-sixth as big.'],
  '**The pulling force is a weight, so it drops to one-sixth, and so does '
  'every acceleration.** The masses do not change — which is exactly why the '
  'answer is not “nothing changes”. Weight on the Moon is smaller, not zero.',
  'The force is a weight; weights shrink on the Moon.')

q(Q, 3, 'Friction in the cart’s wheels and the pulley is not accounted for in '
        'the lab. How does it affect the force worked out from Ma?',
  ['It makes the force come out lower than the hanging weight',
   'It makes the force come out higher than the hanging weight',
   'It has no effect, because friction acts on the cart only',
   'It has no effect, because it cancels out over several runs'],
  0, 'Friction slows the cart. What does that do to a?',
  ['Friction opposes the motion, so the measured acceleration is lower.',
   'F = Ma uses that lower acceleration.',
   'So the worked-out force is lower than the true pull.',
   'The force comes out low.'],
  '**Friction lowers the measured a, so Ma comes out below the hanging '
  'weight.** It acts on every run in the same direction, so averaging does not '
  'cancel it. A smoother track or a slightly tilted one reduces it.',
  'Name the error AND its direction.', frm='added')

q(Q, 2, 'A cart lab keeps its hanging weight fixed and doubles the total system '
        'mass. What happens to the acceleration?',
  ['It halves', 'It doubles', 'It stays the same', 'It falls to a quarter'],
  0, 'a = F / M.',
  ['F stays the same.',
   'M doubles.',
   'a = F / M, so a is divided by 2.',
   'The acceleration halves.'],
  '**a = F / M: double M and a halves.** It would fall to a quarter only if '
  'a depended on M squared, which it does not.', 'Inverse: double one, halve the other.')

q(Q, 2, 'Put the steps of the Newton’s second law lab in order.',
  ['Find the weight of the hanging mass in newtons',
   'Release the cart from rest and time it over a measured distance',
   'Work out each run’s acceleration with a = 2Δx ÷ t²',
   'Plot acceleration against 1 ÷ total mass and find the slope'],
  0, 'You need the data before the graph.',
  ['First, know the pulling force.',
   'Then collect a distance and a time for each run.',
   'Turn each into an acceleration.',
   'Then graph and find the slope.'],
  '**Force, runs, accelerations, then the linearized graph.** The slope is '
  'then compared with the hanging weight from the first step.',
  'Measure, compute, then graph.', kind='order')

fresh(Q)
NOTE_LAB = (
    'From Newtons_Law_Lab.pdf in the Dynamics 2 folder: a cart on a table '
    'pulled by a hanging mass over the edge, with the total system mass '
    'changed run by run. The sheet was read for what it asks; the setup '
    'picture on it was not seen. The lab has no data yet, so this unit '
    'teaches the reasoning only — why the hanging mass counts in the total, '
    'getting a from Δx and t with a = 2Δx / t², the linearization (a against '
    '1/M, slope = the hanging weight), the average force, the Moon question '
    '(every acceleration one-sixth, not “nothing changes”), and one source of '
    'error with its direction (friction makes a low, so the force comes out '
    'low). None of her results are invented, and none of the numbers in the '
    'questions are hers. Worth knowing: the sheet asks for a percent '
    'DIFFERENCE but prints the percent-error formula, |experimental − actual| '
    '÷ actual × 100 (the formula text came through garbled when the PDF was '
    'read, so this is our reading of it). Since the hanging weight is an '
    'accepted value, percent error is the right comparison; a card explains '
    'both, and the quiz uses the printed formula. The sheet also says not to '
    'graph distance against time, which the cards repeat.')
build('ad-astra', C, Q, 'unit-phys-dyn2-lab',
      'Dynamics 2 · 2-3 The Newton’s Second Law Lab: Mass and Acceleration', 'physics',
      'The reasoning behind the cart-and-hanging-mass lab: the hanging weight is '
      'the force, the total mass includes everything that moves (the hanging '
      'mass too), each run’s acceleration comes from a = 2Δx / t², and plotting '
      'a against 1 ÷ total mass gives a straight line whose slope is the '
      'force. Then comparing that force with the hanging weight, the Moon, and '
      'which way friction pushes the result.',
      'A lab is only as good as the reasoning around it. Knowing what the slope '
      'should be before you measure it is what lets you tell a good run from '
      'a bad one.',
      [('Determine the weight of the hanging mass.', 'source'),
       ('Find the total system mass, including the hanging mass.', 'source'),
       ('Use a kinematic equation to find each run’s acceleration from distance and time.', 'source'),
       ('Linearize the data and interpret the slope.', 'source'),
       ('Compare the average force with the hanging weight as a percent.', 'source'),
       ('Predict how the data would change on the Moon.', 'source'),
       ('Name one source of error and the direction it pushes the result.', 'source')],
      NOTE_LAB,
      ('Read the cards before lab day, then take the quiz. Say out loud what '
       'the slope of your graph should be before you draw it.', 25),
      'content/phys-dyn2-lab.json', 'Newton’s Second Law Lab', SRC_LAB,
      offset_hours=3, libv_=1)
patch('content/phys-dyn2-lab.json', 'unit-phys-dyn2-lab', quarter=2)
