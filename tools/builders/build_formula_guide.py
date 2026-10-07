# The physics formula guide (v203) — from "Equation_Sheet_Student_Guide.pdf",
# added to the Physics 8 Drive folder on 2026-10-06. It was written at home to
# go with the teacher's own equation sheet: one entry per formula, in the
# sheet's own order, each saying what the formula calculates, what every
# symbol means and is measured in, when to use it, a worked example with
# every substitution shown, the common mistakes, and (where the sheet is
# unclear) a note on what to ask the teacher.
#
# It is transcribed nearly as written. Every worked example is re-checked
# below before anything is written; a guide that shows a wrong number on
# her phone is worse than no guide.
#
# Writes FORMULA_GUIDE into index.html between its BEGIN/END markers, so a
# rerun replaces the block rather than appending a second copy.
#
# `v` is the finder's variable sets: a formula FITS when one of its sets
# holds the quantity she wants and everything else in that set is something
# she already knows. g, G and c are on the sheet, so they never appear in a
# set: they always count as known. A formula with no `v` (the quadratic, the
# percent error, the Δp line, the three constants) is not offered by the
# finder at all, because it answers no "I know these, I want that" question.
import json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import REPO

def near(x, want, tol=0.051):
    assert abs(x - want) <= tol, (x, want)

# ---- every worked example, recomputed
r = [(20 + math.sqrt(400 - 4*5*15)) / 10, (20 - math.sqrt(400 - 4*5*15)) / 10]
assert r == [3.0, 1.0]
near(abs(-3.0) / 50.0 * 100, 6.0)
near((17.0 - 5.0) / 4.0, 3.0)
near(2.0*5.0 + 0.5*5.0*(10.0 - 2.0), 30.0)
near((4.0 + 12.0) / 2 * 3.0, 24.0)
near(3.0*4.0 + 0.5*2.0*4.0**2, 28.0)
near((0 - 20.0**2) / (2*-5.0), 40.0)
near(1500*2.0, 3000); near(1000*10**2/50, 2000)
near(5.0*9.8, 49); near(0.30*49, 14.7)
near(0.50*49, 24.5); assert 20 <= 24.5 < 30
near(-200*0.15, -30)
FG = 6.67e-11*70*5.97e24/(6.37e6)**2
near(FG, 687, 0.6); near(6.67e-11*70*5.97e24, 2.787e16, 0.001e16); near((6.37e6)**2, 4.058e13, 0.001e13)
near(40*5.0*math.cos(math.radians(30)), 173.2)
near(0.5*2.0*3.0**2, 9.0)
near(3.0*9.8*4.0, 117.6)
near(600/12, 50); near(20*3.0, 60)
near(0.5*200*0.10**2, 1.0)
near(math.sqrt(10*3.0*math.cos(0) / 1.0), 5.477); near(round(math.sqrt(30), 1), 5.5)
near(20*0.10, 2.0); near(2.0/0.50, 4.0)
near(1200*15, 18000)
near(-(2.0*6.0)/3.0, -4.0)
near((1.0*4.0 + 3.0*0) / (1.0 + 3.0), 1.0)
near(0 + -9.8*2.0, -19.6)
near(1.5e11/3e8, 500); near(500/60, 8.33, 0.01)
near(math.degrees(math.asin(0.60)), 36.9); near(10*math.sin(math.radians(30)), 5.0)
near(math.degrees(math.acos(0.80)), 36.9); near(10*math.cos(math.radians(30)), 8.66, 0.006)
near(6.67e-11*1.0*1.0/1.0**2, 6.67e-11, 1e-15)

G = []
def f(n, sec, nm, eq, does, sym, when, ex, watch, note=None, v=None):
    assert len(G) + 1 == n
    e = {'n': n, 'sec': sec, 'nm': nm, 'eq': eq, 'does': does, 'sym': sym,
         'when': when, 'ex': ex, 'watch': watch}
    if note: e['note'] = note
    if v: e['v'] = v
    G.append(e)

GEN, KIN, NEW, WE, IM, PC = 'General', 'Kinematics', "Newton's Laws", 'Work and Energy', 'Impulse and Momentum', 'Physical Constants'

f(1, GEN, 'Quadratic formula', 't = (−b ± √(b² − 4ac)) / 2a',
  'It solves a quadratic equation (one with a squared term, a plain term and a constant) for the unknown. The ± means there are usually two answers: one using +, one using −.',
  [['t', 'The unknown being solved for (seconds, if it is a time)', 's'],
   ['a', 'Coefficient of t² (not acceleration here)', 'varies'],
   ['b', 'Coefficient of t', 'varies'],
   ['c', 'The constant term, the number with no t', 'varies'],
   ['±', 'Do the calculation twice, once with +, once with −', ''],
   ['√', 'Square root of everything under the bar, b² − 4ac', '']],
  'When the unknown appears both squared and unsquared. Rearrange so one side is zero, then read off a, b and c. You need all three, and a ≠ 0.',
  {'q': 'A ball is thrown straight up at 20 m/s. When is it 15 m above its starting point? Take up as positive and g ≈ −10 m/s². Formula 6 gives 15 = 20t − 5t², so 5t² − 20t + 15 = 0: a = 5, b = −20, c = 15.',
   'lines': [['t = (−(−20) ± √((−20)² − 4(5)(15))) / 2(5)', 'substitute'],
             ['= (20 ± √(400 − 300)) / 10', 'simplify'],
             ['= (20 ± 10) / 10', '√100 = 10'],
             ['t = 3 s or t = 1 s', 'one with +, one with −']],
   'end': 'Both make sense: the ball passes 15 m at 1 s on the way up and at 3 s on the way down.'},
  ['−b means the opposite of b. Here b = −20, so −b = +20.',
   'The whole top line is divided by 2a, not just the square root.',
   'The equation must equal zero before you read off a, b and c.',
   'If b² − 4ac is negative there is no real solution. Reject answers (like a negative time) that do not fit.'],
  'The sheet does not say which equation this solves or what a, b and c are. a and b are used elsewhere on the sheet for other things, so here they are read as the coefficients of a quadratic.')

f(2, GEN, 'Percent error', '%Error = (|b| / y_max) · 100',
  'It divides the size of b by y_max and multiplies by 100, to express the ratio as a percent.',
  [['%Error', 'The result: the name of the quantity, not % times Error', '%'],
   ['|b|', 'The size of b, with any minus sign dropped (|−3| = 3)', 'same as y_max'],
   ['y_max', 'The value |b| is compared against', 'same as b'],
   ['· 100', 'Turns a fraction into a percent', '']],
  'To say how large one quantity is compared with another, as a percent. b and y_max must be in the same units, so they cancel.',
  {'q': 'The numbers only show the arithmetic: b = −3.0 cm and y_max = 50.0 cm.',
   'lines': [['%Error = (|−3.0| / 50.0) · 100', 'substitute'],
             ['= (3.0 / 50.0) · 100', '|−3.0| = 3.0'],
             ['= 0.060 · 100', 'divide'],
             ['= 6.0 %', 'multiply']], 'end': ''},
  ['Forgetting the · 100 leaves 0.060 instead of 6.0 %.',
   'Keep |b| positive: the bars remove the sign.',
   'b and y_max in the same units (do not mix mm and m).',
   'Divide by y_max, not the other way round.'],
  'The sheet does not say what b or y_max are in an experiment. Ask exactly what to use for each in your lab.')

f(3, KIN, 'Acceleration from a change in velocity', 'a = (v_f − v_i) / t',
  'Acceleration: how quickly velocity changes. The change in velocity divided by the time the change takes.',
  [['a', 'Acceleration (constant, or the average over the interval)', 'm/s²'],
   ['v_f', 'Final velocity, at the end of the interval', 'm/s'],
   ['v_i', 'Initial velocity, at the start of the interval', 'm/s'],
   ['t', 'Time between the initial and final moments', 's']],
  'When you know the starting velocity, the ending velocity and how long it took, and you want the acceleration. In a straight line, give velocities a sign.',
  {'q': 'A car speeds up from 5.0 m/s to 17.0 m/s in 4.0 s. Find its acceleration.',
   'lines': [['a = (17.0 − 5.0) / 4.0', 'substitute'],
             ['= 12.0 / 4.0', 'subtract'],
             ['= 3.0 m/s²', 'divide']],
   'end': 'Each second the car gains 3.0 m/s.'},
  ['Subtract in the right order: final minus initial.',
   'It gives the average acceleration; that equals the constant acceleration only if it does not change.',
   'A negative a does not always mean slowing down: it means the acceleration points the negative way.',
   't is the elapsed time, not a clock reading.'],
  v=[['a', 'vf', 'vi', 't']])

f(4, KIN, 'Displacement from v_i, v_f and t', 'Δx = v_i t + ½t(v_f − v_i)',
  'The displacement (change in position) over a time interval, when you know the starting velocity, the ending velocity and the time.',
  [['Δx', 'Displacement: change in position, with direction', 'm'],
   ['v_i', 'Initial velocity', 'm/s'], ['v_f', 'Final velocity', 'm/s'],
   ['t', 'Elapsed time', 's']],
  'When you know v_i, v_f and t and need Δx. Straight-line motion with constant acceleration — the acceleration itself is not needed.',
  {'q': 'A cyclist speeds up steadily from 2.0 m/s to 10.0 m/s in 5.0 s. How far does she travel?',
   'lines': [['Δx = (2.0)(5.0) + ½(5.0)(10.0 − 2.0)', 'substitute'],
             ['= 10.0 + ½(5.0)(8.0)', 'parentheses first'],
             ['= 10.0 + 20.0', '½(5.0)(8.0) = 20.0'],
             ['= 30.0 m', 'add']], 'end': ''},
  ['Work out (v_f − v_i) first, then multiply by ½t.',
   'Only valid when acceleration is constant.',
   'Use consistent units: convert km/h to m/s first.',
   'The result is displacement, which can differ from distance if the object turns round.'],
  v=[['dx', 'vi', 'vf', 't']])

f(5, KIN, 'Displacement from average velocity', 'Δx = ((v_i + v_f) / 2) t',
  'Displacement equals the average of the initial and final velocities, multiplied by the time.',
  [['Δx', 'Displacement', 'm'], ['v_i, v_f', 'Initial and final velocity', 'm/s'],
   ['(v_i + v_f) / 2', 'The average of the two velocities', 'm/s'], ['t', 'Elapsed time', 's']],
  'When you know both velocities and the time, and the acceleration is constant. Often the quickest way to Δx.',
  {'q': 'A train goes from 4.0 m/s to 12.0 m/s in 3.0 s at constant acceleration. Find Δx.',
   'lines': [['Δx = ((4.0 + 12.0) / 2)(3.0)', 'substitute'],
             ['= (16.0 / 2)(3.0)', 'add'],
             ['= (8.0)(3.0)', 'divide'],
             ['= 24.0 m', 'multiply']], 'end': ''},
  ['Averaging the two velocities only gives the true average velocity when acceleration is constant.',
   'Add first, then divide by 2, then multiply by t.',
   'Do not forget the t at the end.'],
  v=[['dx', 'vi', 'vf', 't']])

f(6, KIN, 'Displacement from v_i, a and t', 'Δx = v_i t + ½at²',
  'Displacement when you know the starting velocity, the constant acceleration and the time, but not the final velocity.',
  [['Δx', 'Displacement', 'm'], ['v_i', 'Initial velocity', 'm/s'],
   ['a', 'Constant acceleration', 'm/s²'], ['t', 'Elapsed time — only t is squared', 's']],
  'When you know v_i, a and t. Constant acceleration in a straight line.',
  {'q': 'A skater moving at 3.0 m/s accelerates at 2.0 m/s² for 4.0 s. How far does she go?',
   'lines': [['Δx = (3.0)(4.0) + ½(2.0)(4.0)²', 'substitute'],
             ['= 12.0 + ½(2.0)(16.0)', '4.0² = 16.0'],
             ['= 12.0 + 16.0', '½(2.0)(16.0) = 16.0'],
             ['= 28.0 m', 'add']], 'end': ''},
  ['at² means a · (t²), not (at)².', 'Do not forget the ½.',
   'Keep the sign of a: slowing down in the positive direction means a < 0.',
   'Constant acceleration only.'],
  v=[['dx', 'vi', 'a', 't']])

f(7, KIN, 'Displacement without time', 'Δx = (v_f² − v_i²) / 2a',
  'Displacement when you know the starting and ending velocities and the acceleration, but not the time.',
  [['Δx', 'Displacement', 'm'], ['v_f²', 'The final velocity, squared', 'm²/s²'],
   ['v_i²', 'The initial velocity, squared', 'm²/s²'],
   ['a', 'Constant acceleration (must not be zero)', 'm/s²']],
  'When time is neither given nor asked for. You need v_i, v_f and a.',
  {'q': 'A car moving at 20.0 m/s brakes uniformly at −5.0 m/s² until it stops (v_f = 0). How far does it travel?',
   'lines': [['Δx = ((0)² − (20.0)²) / 2(−5.0)', 'substitute'],
             ['= (0 − 400) / −10.0', 'square, multiply'],
             ['= 40 m', 'negative ÷ negative']], 'end': ''},
  ['Square each velocity first, then subtract: v_f² − v_i² is not (v_f − v_i)².',
   'The bottom is 2a, twice the acceleration.',
   'Keep the sign of a; two negatives give a positive Δx here.',
   'a cannot be 0. If a = 0, use formula 5.'],
  v=[['dx', 'vf', 'vi', 'a']])

f(8, NEW, 'Net force and circular motion', 'F_net = ma = mv² / r',
  'The net force on an object. F_net = ma is Newton\'s second law. The second part, ma = mv²/r, gives the same net force for an object moving at constant speed on a circle.',
  [['F_net', 'Net force: the vector sum of all forces on the object', 'N'],
   ['m', 'Mass of the object', 'kg'], ['a', 'Acceleration of the object', 'm/s²'],
   ['v', 'Speed of the object', 'm/s'], ['r', 'Radius of the circular path', 'm']],
  'F_net = ma any time you know two of net force, mass and acceleration. mv²/r when the object goes round a circle at constant speed and you know m, v and r.',
  {'q': '(a) A 1500 kg car accelerates at 2.0 m/s². (b) A 1000 kg car goes round a curve of radius 50 m at 10 m/s.',
   'lines': [['(a) F_net = (1500)(2.0) = 3000 N', 'straight line'],
             ['(b) F_net = (1000)(10)² / 50', 'substitute'],
             ['= (1000)(100) / 50', 'v² = 100'],
             ['= 2000 N, toward the centre', 'divide']], 'end': ''},
  ['F_net is the total force, not any single force. Add forces as vectors.',
   'Square only v in mv²/r, and divide by r (the radius, not the diameter).',
   'Mass in kilograms.',
   'ma = mv²/r holds only for motion in a circle at constant speed.'],
  'The sheet puts both on one line without saying the second (= mv²/r) applies only to circular motion at constant speed. The first is general; the second is a special case.',
  v=[['F', 'm', 'a'], ['F', 'm', 'v', 'r']])

f(9, NEW, 'Kinetic friction', 'F_fk = μ_k F_N',
  'The friction force on an object that is sliding across a surface.',
  [['F_fk', 'Friction force; k marks it as kinetic (sliding)', 'N'],
   ['μ_k', 'Coefficient of kinetic friction: how grippy the surfaces are when sliding', 'none'],
   ['F_N', 'Normal force: the surface pushing back, perpendicular to it', 'N']],
  'When an object is sliding. You need μ_k for the two surfaces and the normal force.',
  {'q': 'A 5.0 kg box slides on a level floor with μ_k = 0.30. On a level floor with nothing else pushing up or down, the normal force equals the weight. Use |g| = 9.8 m/s².',
   'lines': [['F_N = mg = (5.0)(9.8) = 49 N', 'normal force'],
             ['F_fk = (0.30)(49 N)', 'substitute'],
             ['= 14.7 N ≈ 15 N', 'opposite to the motion']], 'end': ''},
  ['F_N is not always mg: on a slope, or with an extra push up or down, find it from the forces perpendicular to the surface.',
   'Do not mix up μ_k (sliding) and μ_s (not yet sliding, formula 10).',
   'Kinetic friction does not depend on speed or contact area.',
   'It points opposite to the sliding.'],
  v=[['Ff', 'mu', 'FN']])

f(10, NEW, 'Static friction (the most it can be)', 'F_fs ≤ μ_s F_N',
  'The largest friction force that can hold an object still. The ≤ says the actual static friction can be anything up to μ_s F_N.',
  [['F_fs', 'Static friction; s means static (not sliding)', 'N'], ['≤', 'Less than or equal to', ''],
   ['μ_s', 'Coefficient of static friction', 'none'], ['F_N', 'Normal force', 'N']],
  'To find out whether something will start to slide: compare the push with the most static friction can give, μ_s F_N.',
  {'q': 'The same 5.0 kg box sits still with μ_s = 0.50 and F_N = 49 N. Will it slide if pushed with 20 N? With 30 N?',
   'lines': [['max F_fs = (0.50)(49 N) = 24.5 N', 'substitute, multiply'],
             ['20 N ≤ 24.5 N', 'friction matches the push; it stays put'],
             ['30 N > 24.5 N', 'friction cannot hold it; it slides']],
   'end': 'Once it slides, kinetic friction (formula 9) takes over.'},
  ['Do not treat ≤ as =: static friction only equals μ_s F_N at the point of sliding.',
   'Use it only for objects that are not sliding.',
   'Usually μ_s is larger than μ_k for the same surfaces.'],
  v=[['Ff', 'mu', 'FN']])

f(11, NEW, 'Spring force (Hooke\'s law)', 'F = −kx',
  'The force a spring exerts when stretched or squashed. The minus sign shows it always pulls or pushes back toward its relaxed length.',
  [['F', 'Force exerted by the spring', 'N'], ['k', 'Spring constant: how stiff the spring is', 'N/m'],
   ['x', 'Stretch or squash from the relaxed length', 'm'], ['−', 'The force is opposite to x', '']],
  'When you know how stiff a spring is and how far it is stretched or squashed, and want the force.',
  {'q': 'A spring with k = 200 N/m is stretched 0.15 m in the positive direction.',
   'lines': [['F = −(200)(0.15)', 'substitute'],
             ['= −30 N', 'multiply']],
   'end': 'The spring pulls back with 30 N, the negative way.'},
  ['x is the stretch or squash, not the spring\'s total length.', 'Convert centimeters to meters.',
   'Keep the minus sign: it carries the direction.', 'Only for a spring not stretched too far.'],
  v=[['F', 'k', 'x']])

f(12, NEW, 'Gravitation between two masses', 'F_G = −G m₁m₂ / r²',
  'The gravitational pull between two objects. It grows with both masses and weakens with the square of the distance between them.',
  [['F_G', 'Gravitational force between the two objects', 'N'],
   ['G', 'Gravitational constant (formula 28)', 'N·m²/kg²'],
   ['m₁, m₂', 'The two masses', 'kg'], ['r', 'Distance between their centres', 'm']],
  'To find the pull between two masses — a planet and a person, two spacecraft. You need both masses and r.',
  {'q': 'A 70 kg person on Earth\'s surface: Earth\'s mass is 5.97 × 10²⁴ kg and r = 6.37 × 10⁶ m.',
   'lines': [['F_G = −(6.67 × 10⁻¹¹)(70)(5.97 × 10²⁴) / (6.37 × 10⁶)²', 'substitute'],
             ['= −(2.787 × 10¹⁶) / (4.058 × 10¹³)', 'top, then r²'],
             ['= −687 N', 'divide']],
   'end': 'About 687 N — almost exactly the person\'s weight, (70)(9.8) = 686 N.'},
  ['r is centre to centre, and it is squared.', 'Convert kilometers to meters.',
   'Big G (formula 28) is not little g (formula 24).',
   'The pull is mutual: each object pulls the other just as hard.'],
  'The sheet has a minus sign in front but does not say which direction is positive. The size of the force is G m₁m₂ / r². Ask whether the minus sign is expected in your answers.',
  v=[['F', 'm', 'r']])

f(13, WE, 'Work', 'W = FΔx cos θ',
  'The work done by a constant force: the energy it transfers by moving an object. Only the part of the force along the motion counts.',
  [['W', 'Work done by the force', 'J'], ['F', 'Size of the force', 'N'],
   ['Δx', 'Size of the displacement', 'm'],
   ['θ', 'Angle between the force and the motion', '°'], ['cos θ', 'Cosine of that angle', 'none']],
  'When a known constant force acts while the object moves. You need F, Δx and θ.',
  {'q': 'Someone pulls a suitcase with 40 N at 30° above the horizontal while it moves 5.0 m along the floor.',
   'lines': [['W = (40)(5.0) cos 30°', 'substitute'],
             ['= (200)(0.866)', 'cos 30° = 0.866'],
             ['= 173 J', 'multiply']], 'end': ''},
  ['θ is between the force and the displacement, not from the vertical.',
   'Calculator in degrees mode.',
   'A force at 90° to the motion does no work: cos 90° = 0.',
   'A force against the motion (180°) does negative work: cos 180° = −1.'],
  v=[['W', 'F', 'dx', 'th']])

f(14, WE, 'Kinetic energy', 'KE = ½mv²',
  'The energy an object has because it is moving.',
  [['KE', 'Kinetic energy', 'J'], ['m', 'Mass', 'kg'], ['v', 'Speed', 'm/s']],
  'When you know an object\'s mass and speed. It is what changes when net work is done on an object.',
  {'q': 'A 2.0 kg cart moves at 3.0 m/s.',
   'lines': [['KE = ½(2.0)(3.0)²', 'substitute'], ['= ½(2.0)(9.0)', '3.0² = 9.0'], ['= 9.0 J', 'multiply']], 'end': ''},
  ['Square only v, not mv: ½mv² is not ½(mv)².', 'Doubling the speed makes KE four times bigger.', 'KE is never negative.'],
  v=[['KE', 'm', 'v']])

f(15, WE, 'Gravitational potential energy', 'PE = mgh',
  'The energy stored because of an object\'s height.',
  [['PE', 'Gravitational potential energy', 'J'], ['m', 'Mass', 'kg'],
   ['g', 'Acceleration due to gravity (formula 24)', 'm/s²'],
   ['h', 'Height above the level you chose as zero', 'm']],
  'Near Earth\'s surface when something is raised or lowered. Choose your zero height first; only changes in PE matter.',
  {'q': 'A 3.0 kg box sits 4.0 m above the floor (the floor is zero). Use the size of g, 9.8 m/s².',
   'lines': [['PE = (3.0)(9.8)(4.0)', 'substitute'], ['= 117.6 J ≈ 118 J', 'multiply']], 'end': ''},
  ['h is measured from your chosen zero.', 'Stay consistent with the sign you give g.',
   'Not the same as a spring\'s PE (formula 17): same name, different formula.'],
  'The sheet lists g = −9.8 m/s². Put that into PE = mgh with a positive height and you get a negative PE, while PE above the zero level is normally positive. The example uses 9.8; ask how your class handles the sign here.',
  v=[['PE', 'm', 'h']])

f(16, WE, 'Power', 'P = W / t = Fv',
  'How fast work is done. The first form divides work by time; the second multiplies force by speed.',
  [['P', 'Power', 'W (watt)'], ['W (italic)', 'Work done', 'J'], ['t', 'Time taken', 's'],
   ['F', 'Force', 'N'], ['v', 'Speed', 'm/s']],
  'W / t when you know the work and how long it took. Fv when a force acts along the motion and you know the force and speed.',
  {'q': '(a) A motor does 600 J of work in 12 s. (b) A 20 N force moves an object at a steady 3.0 m/s along the force.',
   'lines': [['(a) P = 600 / 12 = 50 W', 'work ÷ time'],
             ['(b) P = (20)(3.0) = 60 W', 'force × speed']], 'end': ''},
  ['Italic W is work; upright W is the watt. Do not mix them up.', 'Convert minutes to seconds.',
   'Fv assumes the force points along the motion.'],
  v=[['P', 'W', 't'], ['P', 'F', 'v']])

f(17, WE, 'Elastic potential energy of a spring', 'PE = ½kx²',
  'The energy stored in a stretched or squashed spring.',
  [['PE', 'Energy stored in the spring', 'J'], ['k', 'Spring constant', 'N/m'],
   ['x', 'Stretch or squash from the relaxed length', 'm']],
  'When you know the spring constant and how far it is stretched or squashed. Same k and x as formula 11.',
  {'q': 'A spring with k = 200 N/m is squashed 0.10 m.',
   'lines': [['PE = ½(200)(0.10)²', 'substitute'], ['= ½(200)(0.010)', '0.10² = 0.010'], ['= 1.0 J', 'multiply']], 'end': ''},
  ['Square only x: 0.10² = 0.010, not 0.20.',
   'Stretching and squashing by the same amount store the same energy.',
   'Formula 15 uses the same symbol PE for gravity.'],
  v=[['PE', 'k', 'x']])

f(18, WE, 'Work and the change in energy', 'FΔx cos θ = [KE_f + PE_f] − [KE_o + PE_o]',
  'The work done by a force equals the change in the object\'s total energy (kinetic plus potential): the end minus the start.',
  [['FΔx cos θ', 'Work done by the force (formula 13)', 'J'],
   ['KE_f, PE_f', 'Kinetic and potential energy at the end', 'J'],
   ['KE_o, PE_o', 'Kinetic and potential energy at the start', 'J'],
   ['[ ]', 'Add each total before subtracting', '']],
  'When a push, a pull or friction does work and you want how the speed or height changed. Use formulas 14, 15 and 17 for each KE and PE.',
  {'q': 'A 2.0 kg block at rest on a frictionless, level floor is pushed with 10 N (θ = 0°) for 3.0 m. Find its final speed. The floor is level, so PE is 0 at the start and end.',
   'lines': [['Left: (10)(3.0) cos 0° = 30 J', 'work'],
             ['Right: [½(2.0)v_f² + 0] − [0 + 0] = 1.0 v_f²', 'energy change'],
             ['30 = 1.0 v_f²', 'set them equal'],
             ['v_f = √30 ≈ 5.5 m/s', 'square root']], 'end': ''},
  ['Always final minus initial on the right.',
   'Do not count the same effect twice: if gravity is already in a PE term, do not also count its work on the left.',
   'Friction opposes the motion (θ = 180°), so its work is negative.'],
  'The sheet uses o for the starting values here but i everywhere else, and does not define o. It most likely means original. It also does not say which forces F means.',
  v=[['F', 'dx', 'th', 'KE', 'PE']])

f(19, IM, 'Impulse', 'J = Ft = Δp',
  'Impulse: the effect of a force acting over a time. It equals force times time, and also the change in momentum.',
  [['J', 'Impulse', 'N·s'], ['F', 'Force (or the average force)', 'N'],
   ['t', 'How long the force acts', 's'], ['Δp', 'Change in momentum, final minus initial', 'kg·m/s']],
  'Collisions, kicks and impacts — whenever a force acts for a short time and you want the change in momentum, or the reverse. You need two of F, t and Δp.',
  {'q': 'A 20 N force acts on a 0.50 kg ball, at rest, for 0.10 s. Find the impulse and the final speed.',
   'lines': [['J = (20)(0.10) = 2.0 N·s', 'force × time'],
             ['Δp = J = 2.0 kg·m/s', 'it started at rest'],
             ['2.0 = (0.50)v, so v = 4.0 m/s', 'p = mv (formula 21)']], 'end': ''},
  ['t is only the time the force actually acts (the contact time).', 'If the force changes, use the average force.',
   'Δp has a direction (a sign).', 'Convert milliseconds to seconds.'],
  v=[['J', 'F', 't'], ['J', 'dp'], ['dp', 'F', 't']])

f(20, IM, 'Change in momentum', 'Δp = −Δp',
  'Read literally, it says a change in momentum equals its own negative. No other quantity appears in it.',
  [['Δp', 'Change in momentum', 'kg·m/s'], ['−', 'The opposite of what follows', '']],
  'As written there is nothing to calculate. Formulas 22 and 23, which follow it, are the ones you solve problems with.',
  {'q': 'What it says, taken literally:',
   'lines': [['Δp = −Δp', ''], ['2Δp = 0', 'add Δp to both sides'], ['Δp = 0', 'divide by 2']],
   'end': 'So as written it is only true when Δp = 0.'},
  ['Do not put two different numbers into the two Δp symbols unless your class labels them (say, as two objects).',
   'Do not use it to find an unknown: it has no other variable.'],
  'Both symbols are identical with no labels, so as written it means Δp = 0. It is probably meant to say that when two objects interact, one\'s change in momentum is minus the other\'s — which would need labels 1 and 2. Ask what it is meant to say.')

f(21, IM, 'Momentum', 'p = mv',
  'Momentum: how hard a moving object is to stop, depending on both how heavy and how fast it is.',
  [['p', 'Momentum (it has a direction)', 'kg·m/s'], ['m', 'Mass', 'kg'], ['v', 'Velocity, with its sign', 'm/s']],
  'To compare moving objects, to find momentum before and after a collision, or to switch between momentum and velocity.',
  {'q': 'A 1200 kg car travels at 15 m/s east (east is positive).',
   'lines': [['p = (1200)(15)', 'substitute'], ['= 18 000 kg·m/s east', 'multiply']], 'end': ''},
  ['Momentum is mv, not mv² (that is mixing it up with kinetic energy).',
   'Motion the negative way gives negative momentum.',
   'Add momenta with their signs, not just their sizes.'],
  v=[['p', 'm', 'v']])

f(22, IM, 'Momentum changes of two interacting objects', 'm₂Δv₂ = −m₁Δv₁',
  'How the velocity changes of two objects that push on each other are related: object 2\'s change in momentum is the same size as object 1\'s and opposite in direction.',
  [['m₁, m₂', 'Masses of objects 1 and 2', 'kg'],
   ['Δv₁, Δv₂', 'Change in each one\'s velocity, final minus initial', 'm/s'],
   ['−', 'The changes point opposite ways', '']],
  'When two objects interact only with each other (a collision, an explosion, a push-off), you know both masses and one velocity change, and want the other. No outside force on the pair.',
  {'q': 'Two carts at rest push apart. Cart 1 (2.0 kg) ends up with Δv₁ = +6.0 m/s. Cart 2 is 3.0 kg. Find Δv₂.',
   'lines': [['(3.0)Δv₂ = −(2.0)(+6.0)', 'substitute'], ['(3.0)Δv₂ = −12.0', 'multiply'],
             ['Δv₂ = −4.0 m/s', 'divide by m₂']],
   'end': 'Cart 2 moves off at 4.0 m/s the other way.'},
  ['Keep the minus sign.', 'Δv is a change, not a final velocity.',
   'm₂ goes with Δv₂ — do not swap the subscripts.',
   'Only when no outside force acts (friction or an outside push breaks it).'],
  v=[['m', 'dv']])

f(23, IM, 'Conservation of momentum for two objects', 'm₁v₁_i + m₂v₂_i = m₁v₁_f + m₂v₂_f',
  'The total momentum of two objects before they interact equals their total momentum afterwards.',
  [['m₁, m₂', 'Masses of objects 1 and 2', 'kg'],
   ['v₁_i, v₂_i', 'Their velocities before', 'm/s'], ['v₁_f, v₂_f', 'Their velocities after', 'm/s']],
  'Collisions and explosions of two objects with no outside force. You need the masses and enough velocities to leave one unknown.',
  {'q': 'A 1.0 kg cart at 4.0 m/s hits a 3.0 kg cart at rest and they stick together. Find their common speed v.',
   'lines': [['(1.0)(4.0) + (3.0)(0) = (1.0)v + (3.0)v', 'substitute'],
             ['4.0 = 4.0v', 'simplify'], ['v = 1.0 m/s', 'divide']], 'end': ''},
  ['Give velocities signs: an object moving the other way has a negative velocity.',
   'Momentum is conserved with no outside force; kinetic energy is not always.',
   'An object at rest has v = 0, so its term is 0.'],
  v=[['m', 'vi', 'vf']])

f(24, PC, 'Acceleration due to gravity', 'g = −9.8 m/s² ≈ −10 m/s²',
  'The standard value of gravity\'s acceleration near Earth\'s surface — a precise value and a rounded one for quick estimates.',
  [['g', 'Acceleration due to gravity near Earth', 'm/s²'],
   ['−9.8', 'The minus sign means downward, with up positive', 'm/s²'],
   ['≈ −10', 'A rounded value for quick estimates', 'm/s²']],
  'Free fall, projectiles and weight near Earth, ignoring air resistance. Your teacher will say whether to use −9.8 or −10.',
  {'q': 'A ball is dropped from rest and falls for 2.0 s. From formula 3 with a = g: v_f = v_i + gt.',
   'lines': [['v_f = 0 + (−9.8)(2.0) = −19.6 m/s', 'using −9.8'], ['v_f ≈ 0 + (−10)(2.0) = −20 m/s', 'using −10']],
   'end': 'The two differ by only about 2%.'},
  ['With up positive, falling things have negative acceleration.', 'Use the same value all the way through one problem.',
   'Little g is not big G (formula 28).', 'See formula 15 about the sign of g in PE = mgh.'])

f(25, PC, 'Speed of light', 'c_v = 3 × 10⁸ m/s',
  'A constant of 3 × 10⁸ meters per second. The sheet writes it 3x10⁸, using the letter x as a times sign.',
  [['c_v', 'The constant (the sheet does not name it)', 'm/s'],
   ['3 × 10⁸', '300 000 000', '']],
  'Whenever a problem needs it — light travel times and the like.',
  {'q': 'How long does light take to travel the 1.5 × 10¹¹ m from the Sun to Earth? At constant speed, Δx = c_v t, so t = Δx / c_v.',
   'lines': [['t = (1.5 × 10¹¹) / (3 × 10⁸)', 'substitute'], ['= 500 s', 'divide'], ['≈ 8.3 minutes', '500 ÷ 60']], 'end': ''},
  ['3x10⁸ means 3 × 10⁸, not 3 times x times 10⁸.', 'Use meters, not kilometers.', 'It is rounded, so answers are approximate.'],
  'The sheet calls it c_v without saying what it is. Its value and units match the speed of light in a vacuum, usually written c. Ask what the v means.')

f(26, PC, 'Sine (right triangle)', 'sin θ = opp / hyp',
  'The sine of an angle in a right triangle: the side opposite the angle divided by the hypotenuse.',
  [['θ', 'An angle of the triangle (not the right angle)', '°'], ['opp', 'Side opposite θ', 'any length'],
   ['hyp', 'Hypotenuse: the longest side, across from the right angle', 'same as opp']],
  'To find a side or an angle in a right triangle — like splitting a force or velocity into parts. You need two of θ, opp and hyp.',
  {'q': 'A ramp is 3.0 m high (opposite) and 5.0 m long (hypotenuse). Find the angle.',
   'lines': [['sin θ = 3.0 / 5.0 = 0.60', 'substitute'], ['θ = sin⁻¹(0.60) ≈ 36.9°', 'inverse sine key']],
   'end': 'The other way round: if θ = 30° and hyp = 10 m, opp = (10) sin 30° = 5.0 m.'},
  ['Right triangles only.', 'Opposite means across from θ — it changes if you pick the other angle.',
   'sin θ is never more than 1.', 'Calculator in degrees mode.'],
  v=[['th', 'opp', 'hyp']])

f(27, PC, 'Cosine (right triangle)', 'cos θ = adj / hyp',
  'The cosine of an angle in a right triangle: the side next to the angle divided by the hypotenuse.',
  [['θ', 'An angle of the triangle (not the right angle)', '°'],
   ['adj', 'Side next to θ (not the hypotenuse)', 'any length'], ['hyp', 'Hypotenuse', 'same as adj']],
  'To find a side or an angle in a right triangle, or the part of a vector along a direction. It is the cos θ in the work formula.',
  {'q': 'A right triangle has an adjacent side of 4.0 m and a hypotenuse of 5.0 m. Find θ.',
   'lines': [['cos θ = 4.0 / 5.0 = 0.80', 'substitute'], ['θ = cos⁻¹(0.80) ≈ 36.9°', 'inverse cosine']],
   'end': 'The other way round: if θ = 30° and hyp = 10 m, adj = (10) cos 30° = 8.66 m.'},
  ['Right triangles only.', 'Adjacent is the leg touching θ, not the hypotenuse.',
   'Do not swap sine and cosine: cosine uses the adjacent side.', 'Calculator in degrees mode.'],
  v=[['th', 'adj', 'hyp']])

f(28, PC, 'Gravitational constant', 'G = 6.67 × 10⁻¹¹ N·m² / kg²',
  'The value of the constant G in the law of gravitation (formula 12). It is the same everywhere in the universe.',
  [['G', 'Gravitational constant', 'N·m²/kg²'], ['6.67 × 10⁻¹¹', '0.0000000000667 — extremely small', '']],
  'Whenever you work out the pull between masses with formula 12.',
  {'q': 'The pull between two 1.0 kg masses 1.0 m apart, centre to centre.',
   'lines': [['|F_G| = (6.67 × 10⁻¹¹)(1.0)(1.0) / (1.0)²', 'substitute'], ['= 6.67 × 10⁻¹¹ N', 'bottom is 1.0']],
   'end': 'Tiny — which is why you never notice gravity between everyday objects.'},
  ['Big G is not little g (formula 24).', 'Keep the minus sign in the exponent.',
   'Use kilograms and meters so the answer comes out in newtons.'])

assert len(G) == 28
VARS = {'dx', 'vi', 'vf', 'v', 'a', 't', 'm', 'F', 'r', 'FN', 'mu', 'Ff', 'k', 'x', 'W', 'th',
        'KE', 'PE', 'h', 'P', 'p', 'dp', 'J', 'dv', 'opp', 'adj', 'hyp'}
for e in G:
    for s in e.get('v', []):
        assert set(s) <= VARS, (e['n'], s)
    assert e['does'] and e['when'] and e['watch'] and e['ex']['lines']
    blob = json.dumps(e, ensure_ascii=False)
    assert not re.search(r'Ortiz|Sedona|she (got|wrote)', blob)

js = 'const FORMULA_GUIDE = ' + json.dumps(G, ensure_ascii=False, indent=0).replace('\n', '') + ';'
path = os.path.join(REPO, 'index.html')
src = open(path, encoding='utf-8').read()
A, B = '/* FORMULA_GUIDE:BEGIN — generated by tools/builders/build_formula_guide.py */', '/* FORMULA_GUIDE:END */'
assert src.count(A) == 1 and src.count(B) == 1, 'markers missing'
i, j = src.index(A) + len(A), src.index(B)
src = src[:i] + '\n' + js + '\n' + src[j:]
open(path, 'w', encoding='utf-8').write(src)
print('FORMULA_GUIDE: %d entries, %d in the finder, %d with a note' % (
    len(G), sum(1 for e in G if e.get('v')), sum(1 for e in G if e.get('note'))))
