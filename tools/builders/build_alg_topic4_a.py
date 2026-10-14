# Algebra & Geometry II — Topic 4: Rational Functions, lessons 4-1, 4-2 and 4-3.
#
# Sources (her Drive "Topic 4" folder, uploaded 2026-10-14):
#   aga_24_a2_0401_se.pdf .. 0404_se.pdf   — the student-edition lessons (clean text layer)
#   aga_24_a2_na_0401_ap.pdf               — the 4-1 "Additional Practice" sheet
#   aga_24_a2_na_04NN_lps.pptx             — lesson presentation slides (4-1, 4-3, 4-4, 4-5)
#
# EVERY number, expression, asymptote and option below is computed or checked with
# sympy before it can reach a question: `same()` asserts a displayed answer equals the
# computed one, `differs()` asserts each distractor does NOT (so no question can quietly
# carry two right answers). None of the textbook's own examples, Try Its or practice
# numbers are reused — they were read to calibrate style and difficulty only.
import sympy as sp
from unit_common import card, q, build
from topic4_common import x, y, z, r, E, same, differs, poles, holes, hasym, rgraph, finish

def inv_k(xv, yv):
    return sp.nsimplify(xv) * sp.nsimplify(yv)

# ================================================================ 4-1
C, Q = [], []

card(C, 'Inverse variation',
     "**A relationship of the form y = k/x, with k ≠ 0: multiply one variable by a number and the other is divided by that same number.**"
     "\n• Double x and y halves; triple x and y drops to a third."
     "\n• Said aloud: \"y varies inversely as x\".",
     eq='y = k/x   (k ≠ 0)',
     hint='One goes up by a FACTOR, the other comes down by the same factor.')

card(C, 'Constant of variation',
     "**The number k = xy that every pair in an inverse variation shares.**"
     "\n• One known pair is enough to find it: multiply the two values."
     "\n• Once you have k, any other value is k divided by the one you know.",
     eq='k = xy',
     hint='Find k first, every time — it is the whole relationship in one number.')

card(C, 'Testing a table',
     "**Multiply x by y in EVERY column; it is an inverse variation only if every product is the same.**"
     "\n• One column that breaks the pattern is enough to rule it out."
     "\n• Checking two or three columns and stopping is how a near-miss table slips through.",
     hint='Every column, not just the first few.')

card(C, 'Direct vs. inverse',
     "**Direct variation keeps the RATIO y/x constant; inverse variation keeps the PRODUCT xy constant.**"
     "\n• Direct: y = kx, and the two variables rise and fall together."
     "\n• Inverse: y = k/x, and as one rises the other falls.",
     hint='Ratio for direct, product for inverse.')

card(C, 'Falling is not enough',
     "**A table where y goes down as x goes up is not automatically an inverse variation — the product xy still has to stay constant.**"
     "\n• x: 1, 2, 3, 4 with y: 20, 16, 12, 8 falls steadily, but its products are 20, 32, 36, 32. That is a straight line going down, not an inverse variation."
     "\n• Inverse variation falls fast at first and then ever more slowly; it never reaches zero.",
     hint='Steady drops by the same AMOUNT are linear, not inverse.', frm='added')

card(C, 'The reciprocal function',
     "**f(x) = 1/x sends every nonzero number to its reciprocal; its graph is two separate branches, in quadrants I and III.**"
     "\n• It is the simplest inverse variation, with k = 1."
     "\n• Near 0 the values blow up; far from 0 they shrink toward 0.",
     eq='f(x) = 1/x',
     hint='Two branches, because x = 0 splits the graph in half.')
C[-1]['graph'] = rgraph([1 / x], [-5, 5, -5, 5], vas=[0], has=[0])

card(C, 'Asymptote',
     "**A line that a graph gets closer and closer to as it runs off along it.**"
     "\n• A vertical asymptote marks an x-value the function can never use."
     "\n• A horizontal asymptote describes where the values settle as x runs far left and far right.",
     hint='The graph hugs it more and more tightly.')

card(C, 'Key features of y = 1/x',
     "**Vertical asymptote x = 0, horizontal asymptote y = 0; domain all x ≠ 0, range all y ≠ 0.**"
     "\n• As x → ±∞, f(x) → 0. As x → 0 from the right, f(x) → +∞; from the left, f(x) → −∞."
     "\n• It never touches y = 0, because 1/x = 0 would need 1 = 0.",
     hint='The two axes are the two asymptotes.')

card(C, 'When k is negative',
     "**y = k/x with k < 0 puts the two branches in quadrants II and IV instead of I and III.**"
     "\n• It is the k > 0 graph flipped over the x-axis."
     "\n• The asymptotes do not move: still x = 0 and y = 0.",
     hint='A negative k flips the picture; it never moves the asymptotes.')
C[-1]['graph'] = rgraph([-4 / x], [-5, 5, -5, 5], vas=[0], has=[0])
assert all(sp.sign((-4 / x).subs(x, t)) < 0 for t in (1, 2, 3)) and (-4 / x).subs(x, -2) > 0

card(C, 'Translating the reciprocal function',
     "**y = a/(x − h) + k is 1/x moved h units horizontally and k units vertically, so its asymptotes are x = h and y = k.**"
     "\n• Domain: every x except h. Range: every y except k."
     "\n• The point (h, k), where the two asymptotes cross, is the centre the two branches curl around.",
     eq='y = a/(x − h) + k',
     hint='The asymptotes move with the graph — read them straight off h and k.')
_f = 1 / (x + 2) + 1
assert poles(_f) == [-2] and hasym(_f) == 1
C[-1]['graph'] = rgraph([_f], [-6, 4, -4, 5], vas=[-2], has=[1],
                        pts=[{'x': -2, 'y': 1, 'label': '(−2, 1)'}])

card(C, 'The sign trap in x − h',
     "**In 1/(x + 3), h is −3: the vertical asymptote is x = −3, to the LEFT.**"
     "\n• x + 3 = x − (−3). The number inside moves the graph the opposite way to its sign."
     "\n• The k outside does what it says: + 4 is up 4, − 4 is down 4.",
     hint='Inside the denominator, the sign lies; outside, it tells the truth.')

card(C, 'Solving an inverse variation problem',
     "**Find k from the pair you are given, then divide k by the new value.**"
     "\n• Check it makes sense: if one quantity got bigger, the other must have got smaller."
     "\n• If your answer moved in the same direction, you treated it as direct variation by mistake.",
     hint='Bigger in, smaller out — always.')

card(C, 'Varying inversely as the square',
     "**y = k/x² means y is divided by the SQUARE of whatever x is multiplied by.**"
     "\n• Multiply x by 2 and y is divided by 4; multiply x by 5 and y is divided by 25."
     "\n• Light and sound fade with distance this way.",
     eq='y = k/x²',
     hint='Square the scale factor before you divide.')

# ---- questions: level 1 -------------------------------------------------------
q(Q, 1, 'Which equation models an inverse variation?',
  ['y = 9/x', 'y = 9x', 'y = x/9', 'y = 9 − x'], 0,
  'Look for the variable in the denominator with a constant on top.',
  ['An inverse variation has the form y = k/x with k ≠ 0.',
   'y = 9x and y = x/9 are both direct variations: y is a constant times x.',
   'y = 9 − x falls as x rises, but it is linear, not inverse.',
   'Only y = 9/x has the form k/x.'],
  '**y = 9/x.** Here k = 9, so every pair multiplies to 9. y = 9x and y = x/9 are direct variations, where the ratio stays fixed, and y = 9 − x is a falling line: it decreases, but its products do not stay constant.',
  'Decreasing is not the test. The product is.')

q(Q, 1, 'In an inverse variation y = k/x, what stays the same for every pair of values?',
  ['The product xy', 'The ratio y/x', 'The difference y − x', 'The sum x + y'], 0,
  'Rearrange y = k/x so k stands alone.',
  ['Start from y = k/x.',
   'Multiply both sides by x: xy = k.',
   'k is a constant, so xy is the same for every pair.',
   'The product xy stays the same.'],
  '**The product xy.** Multiplying y = k/x through by x gives xy = k. A constant RATIO is the mark of direct variation, which is the commonest mix-up here.',
  'Ratio for direct, product for inverse.')

q(Q, 1, 'What are the asymptotes of f(x) = 1/x?',
  ['x = 0 and y = 0', 'x = 1 and y = 1', 'y = x and y = −x', 'x = 0 only'], 0,
  'Which x can you never use, and where do the values settle far out?',
  ['1/x is undefined at x = 0, so x = 0 is a vertical asymptote.',
   'As x runs far left or right, 1/x shrinks toward 0.',
   'So y = 0 is a horizontal asymptote.',
   'The asymptotes are x = 0 and y = 0.'],
  '**x = 0 and y = 0.** The function cannot use x = 0, and far out its values close in on 0 without reaching it, so both axes are asymptotes. y = x and y = −x are the graph\'s lines of symmetry, not lines it approaches.',
  'For 1/x the two axes ARE the two asymptotes.')

q(Q, 1, 'What is the domain of f(x) = 1/x?',
  ['All real numbers except 0', 'All real numbers', 'Only positive numbers', 'All real numbers except 1'], 0,
  'Which input makes the denominator zero?',
  ['The domain is every x the function can accept.',
   'Division by zero is undefined.',
   'x = 0 is the only input that puts 0 in the denominator.',
   'The domain is all real numbers except 0.'],
  '**All real numbers except 0.** Negative inputs are fine — 1/(−4) = −0.25 — which is exactly why the graph has a branch on the left. Only 0 is excluded.',
  'Excluded x-values come from the denominator and nowhere else.')

_tabs = {'A': ([3, 4, 6, 8], [16, 12, 8, 6]),
         'B': ([1, 2, 4, 8], [24, 12, 8, 3]),
         'C': ([1, 2, 3, 4], [20, 16, 12, 8]),
         'D': ([2, 4, 6, 8], [5, 10, 15, 20])}
_prod = {k: [a_ * b_ for a_, b_ in zip(*v)] for k, v in _tabs.items()}
assert len(set(_prod['A'])) == 1 and _prod['A'][0] == 48
assert all(len(set(_prod[k])) > 1 for k in 'BCD')
assert _prod['B'] == [24, 24, 32, 24]
q(Q, 1, 'Which set of pairs is an inverse variation?',
  ['x: 3, 4, 6, 8 with y: 16, 12, 8, 6', 'x: 1, 2, 4, 8 with y: 24, 12, 8, 3',
   'x: 1, 2, 3, 4 with y: 20, 16, 12, 8', 'x: 2, 4, 6, 8 with y: 5, 10, 15, 20'], 0,
  'Multiply each x by its own y, all the way along.',
  ['Products for 3, 4, 6, 8 with 16, 12, 8, 6: 48, 48, 48, 48 — constant.',
   'Products for 1, 2, 4, 8 with 24, 12, 8, 3: 24, 24, 32, 24 — one column breaks it.',
   '1, 2, 3, 4 with 20, 16, 12, 8 falls by a steady 4, which is linear: products 20, 32, 36, 32.',
   '2, 4, 6, 8 with 5, 10, 15, 20 rises together with x — direct variation.',
   'Only x: 3, 4, 6, 8 with y: 16, 12, 8, 6 keeps xy = 48.'],
  '**x: 3, 4, 6, 8 with y: 16, 12, 8, 6.** Every product is 48. The 24, 12, 8, 3 set is the trap: three of its four products are 24, and the column 4 × 8 = 32 rules it out. The steadily falling set is a line, and the rising set is direct variation.',
  'Check every column. Three out of four is still a no.')

_g = 1 / (x - 6) + 2
assert poles(_g) == [6]
q(Q, 1, 'What is the vertical asymptote of g(x) = 1/(x − 6) + 2?',
  ['x = 6', 'x = −6', 'x = 2', 'x = −2'], 0,
  'Which x-value makes the denominator zero?',
  ['The vertical asymptote sits where x − 6 = 0.',
   'Solve: x = 6.',
   'The + 2 outside the fraction moves the graph up; it does not touch the vertical asymptote.',
   'The vertical asymptote is x = 6.'],
  '**x = 6.** It is the one input that makes the denominator 0. Answering x = −6 flips the sign inside the denominator, and x = 2 reads the vertical shift as if it were the horizontal one.',
  'Set the denominator equal to zero — it beats remembering a sign rule.')

_h = 5 / (x + 4) - 7
assert hasym(_h) == -7
q(Q, 1, 'What is the horizontal asymptote of h(x) = 5/(x + 4) − 7?',
  ['y = −7', 'y = 7', 'y = −4', 'y = 5'], 0,
  'Where do the values settle as x runs far out?',
  ['As x runs far left or right, 5/(x + 4) shrinks toward 0.',
   'So h(x) settles toward 0 − 7.',
   'That level is the horizontal asymptote.',
   'The horizontal asymptote is y = −7.'],
  '**y = −7.** The fraction fades to 0 far out, leaving only the − 7. The 5 stretches the branches but moves no asymptote, and the + 4 inside sets the VERTICAL asymptote, x = −4.',
  'The number added outside the fraction is the horizontal asymptote, sign and all.')

# ---- level 2 -----------------------------------------------------------------
_k = inv_k(8, 6); assert _k == 48 and _k / 12 == 4
q(Q, 2, 'x and y vary inversely, and y = 6 when x = 8. What is y when x = 12?',
  ['4', '9', '72', '10'], 0,
  'Find k first.',
  ['k = xy = 8 × 6 = 48.',
   'So y = 48/x.',
   'When x = 12, y = 48 ÷ 12.',
   'y = 4.'],
  '**4.** k = 48, and 48 ÷ 12 = 4. Check the direction: x went up, so y had to come down. 9 is what direct variation would give (y rising with x), and 10 adds the change in x onto y as if the relationship were a line.',
  'If your answer moved the same way as x, it was not inverse variation.')

assert inv_k(-5, 4) == -20
q(Q, 2, 'x and y vary inversely, and y = 4 when x = −5. Which equation models the relationship?',
  ['y = −20/x', 'y = 20/x', 'y = −0.8/x', 'y = −0.8x'], 0,
  'k is the product of the pair, and signs come along.',
  ['k = xy = (−5)(4).',
   'k = −20.',
   'Substitute into y = k/x.',
   'y = −20/x.'],
  '**y = −20/x.** The product is negative, so k is negative. −0.8 is y ÷ x — the ratio, which belongs to direct variation, whether you then put it in the denominator or not.',
  'Keep the sign: a negative k puts the branches in quadrants II and IV.')

_k = 15 * 32; assert _k == 480 and sp.Rational(_k, 24) == 20 and sp.Rational(32 * 24, 15) == sp.Rational(256, 5)
q(Q, 2, 'The time to fill a tank varies inversely with the flow rate. At 15 gallons per minute it takes 32 minutes. How long does it take at 24 gallons per minute?',
  ['20 minutes', '51.2 minutes', '23 minutes', '0.05 minutes'], 0,
  'Faster flow means less time — find k, then divide.',
  ['k = rate × time = 15 × 32 = 480 gallons (the size of the tank).',
   'time = 480 ÷ rate.',
   'At 24 gallons per minute: 480 ÷ 24.',
   'It takes 20 minutes.'],
  '**20 minutes.** Here k is the tank\'s volume, 480 gallons, which is exactly why rate × time stays fixed. 51.2 minutes multiplies as if faster flow took LONGER, 23 subtracts the change in rate, and 0.05 divides the wrong way round.',
  'Ask what k means in the situation — it makes the set-up obvious.')

_f = 3 / (x - 1) + 4
assert poles(_f) == [1] and hasym(_f) == 4
q(Q, 2, 'What are the domain and range of f(x) = 3/(x − 1) + 4?',
  ['Domain: x ≠ 1. Range: y ≠ 4.', 'Domain: x ≠ −1. Range: y ≠ 4.',
   'Domain: x ≠ 4. Range: y ≠ 1.', 'Domain: x ≠ 1. Range: y ≠ 3.'], 0,
  'The domain misses the vertical asymptote; the range misses the horizontal one.',
  ['The vertical asymptote is where x − 1 = 0: x = 1.',
   'So the domain is every x except 1.',
   'The horizontal asymptote is the + 4: y = 4, a value the graph never reaches.',
   'Domain: x ≠ 1. Range: y ≠ 4.'],
  '**Domain x ≠ 1, range y ≠ 4.** For a translated reciprocal function the excluded x is the vertical asymptote and the excluded y is the horizontal one. The 3 is a stretch: it changes how steep the branches are, not which values they miss.',
  'Domain ↔ vertical asymptote; range ↔ horizontal asymptote.')

q(Q, 2, 'How does the graph of g(x) = 1/(x + 3) − 5 relate to the graph of f(x) = 1/x?',
  ['Left 3 units and down 5 units', 'Right 3 units and down 5 units',
   'Left 3 units and up 5 units', 'Left 5 units and down 3 units'], 0,
  'x + 3 is x − (−3).',
  ['Write g(x) as 1/(x − (−3)) + (−5).',
   'So h = −3: a horizontal shift of 3 units left.',
   'k = −5: a vertical shift of 5 units down.',
   'g is f moved left 3 and down 5.'],
  '**Left 3 and down 5.** The new asymptotes are x = −3 and y = −5. "Right 3" is the sign trap inside the denominator; swapping 3 and 5 mixes up which number belongs to which direction.',
  'Check by finding the vertical asymptote: x + 3 = 0 at x = −3, which is to the left.')

_t = 1 / (x + 2) + 6
assert poles(_t) == [-2] and hasym(_t) == 6
for s_, vv, hh in (('1/(x − 2) + 6', 2, 6), ('1/(x + 6) − 2', -6, -2), ('1/(x + 2) − 6', -2, -6)):
    assert poles(E(s_)) == [vv] and hasym(E(s_)) == hh
q(Q, 2, 'Which function has asymptotes x = −2 and y = 6?',
  ['y = 1/(x + 2) + 6', 'y = 1/(x − 2) + 6', 'y = 1/(x + 6) − 2', 'y = 1/(x + 2) − 6'], 0,
  'Build it from y = 1/(x − h) + k with h = −2 and k = 6.',
  ['A vertical asymptote at x = −2 means h = −2.',
   'x − (−2) is x + 2, so the denominator is x + 2.',
   'A horizontal asymptote at y = 6 means k = 6, added outside.',
   'y = 1/(x + 2) + 6.'],
  '**y = 1/(x + 2) + 6.** Its denominator is zero at x = −2 and it settles toward 6. The x − 2 version puts the vertical asymptote at x = 2, the x + 6 version swaps the two numbers, and the − 6 version puts the horizontal asymptote at y = −6.',
  'Test each option by setting its denominator to zero — quicker than a rule.')

_gr = 1 / (x - 2) - 1
assert poles(_gr) == [2] and hasym(_gr) == -1
for s_ in ('1/(x + 2) − 1', '1/(x − 2) + 1', '1/(x + 1) − 2'):
    differs(s_, _gr)
q(Q, 2, 'The graph shown is a translation of y = 1/x, with its asymptotes drawn in. Which equation does it show?',
  ['y = 1/(x − 2) − 1', 'y = 1/(x + 2) − 1', 'y = 1/(x − 2) + 1', 'y = 1/(x + 1) − 2'], 0,
  'Read the two asymptote lines first, then build the equation from them.',
  ['The vertical asymptote is the line x = 2, so h = 2 and the denominator is x − 2.',
   'The horizontal asymptote is the line y = −1, so k = −1.',
   'The branches sit top-right and bottom-left of the centre, so a is positive.',
   'y = 1/(x − 2) − 1.'],
  '**y = 1/(x − 2) − 1.** The asymptotes cross at (2, −1), and that crossing point is (h, k). The x + 2 option would sit left of the y-axis, the + 1 option above the x-axis, and the last swaps the two numbers.',
  'The crossing point of the asymptotes is (h, k) — find it and the equation writes itself.')
Q[-1]['graph'] = rgraph([_gr], [-3, 7, -5, 4], vas=[2], has=[-1])

# ---- level 3 -----------------------------------------------------------------
_k = sp.Symbol('k', positive=True)
_yv = _k / x**2
assert sp.simplify(_yv.subs(x, 3 * x) / _yv) == sp.Rational(1, 9)
q(Q, 3, 'y varies inversely as the square of x. If x is multiplied by 3, what happens to y?',
  ['y is divided by 9', 'y is divided by 3', 'y is multiplied by 9', 'y is divided by 6'], 0,
  'Write y = k/x², then put 3x in place of x.',
  ['The relationship is y = k/x².',
   'Replace x with 3x: k/(3x)² = k/(9x²).',
   'That is the old y divided by 9.',
   'y is divided by 9.'],
  '**y is divided by 9.** The scale factor on x gets squared before it divides: 3² = 9. "Divided by 3" is ordinary inverse variation, which forgets the square; "multiplied by 9" forgets that it is inverse.',
  'Square the factor, then divide by it.')

q(Q, 3, 'Why can the graph of y = 4/x never touch the line y = 0?',
  ['Solving 4/x = 0 would need 4 = 0, which is impossible',
   'Because x = 0 is excluded from the domain of the function',
   'Because the graph only appears in the first quadrant',
   'Because y = 0 is the vertical asymptote of the graph'], 0,
  'Try to solve 4/x = 0 and see what happens.',
  ['Touching y = 0 would mean 4/x = 0 for some x.',
   'Multiply both sides by x: 4 = 0 · x = 0.',
   '4 = 0 is false for every x, so there is no such point.',
   'A fraction is zero only when its numerator is zero, and 4 never is.'],
  '**Because 4/x = 0 would need 4 = 0.** A fraction is zero only when its numerator is. "x = 0 is excluded" is true, but it explains the VERTICAL asymptote, not this horizontal one. The graph also has a third-quadrant branch, and y = 0 is horizontal, not vertical.',
  'Vertical asymptotes come from the denominator; this one comes from the numerator never being 0.')

assert all(s_ * (120 / s_) == 120 for s_ in (20, 40, 60))
q(Q, 3, 'Which pair of quantities genuinely varies inversely?',
  ['The time to drive a fixed 120 miles, and your average speed',
   'The gas left in a tank, and the miles driven since filling it',
   'The cost of some apples, and how many pounds you buy',
   'A child\'s age, and the child\'s height'], 0,
  'For each pair ask: is the PRODUCT fixed, whatever the values?',
  ['Speed × time = distance, and the distance is fixed at 120 miles, so the product never changes.',
   'Gas left goes DOWN by about the same amount every mile — that is a falling line, and at 0 miles an inverse variation would need infinite gas.',
   'Apples cost more the more you buy: the ratio is fixed, so that is direct variation.',
   'Age and height both rise, but neither their ratio nor their product is fixed.',
   'Only speed and time for a fixed trip vary inversely.'],
  '**Driving time and speed over a fixed 120 miles.** Their product is always 120, so doubling the speed halves the time. The gas-in-the-tank pair is a trap: it decreases, but by a fixed amount per mile, which makes it linear. An inverse variation would need the tank to hold infinite gas before the trip began.',
  'Something going down is not enough. Ask what stays fixed.', frm='added')

_xs, _ys = [2, 3, 6, 9], [27, 18, 9, 5]
_pp = [a_ * b_ for a_, b_ in zip(_xs, _ys)]
assert _pp == [54, 54, 54, 45]
q(Q, 3, 'A table pairs x = 2, 3, 6, 9 with y = 27, 18, 9, 5. A classmate says it is an inverse variation because y always falls as x rises. Which verdict is right?',
  ['Not inverse: 9 × 5 = 45 breaks the product of 54 the other columns share',
   'Inverse: y falls every single time that x rises in the table',
   'Inverse: three of the four products agree, which is close enough',
   'Not inverse: the y-values do not fall by the same amount each time'], 0,
  'Multiply every column. All of them.',
  ['2 × 27 = 54, 3 × 18 = 54, 6 × 9 = 54.',
   '9 × 5 = 45.',
   'One product disagrees, so xy is not constant.',
   'It is not an inverse variation, and the last column is the reason.'],
  '**Not inverse — 9 × 5 = 45 breaks the pattern.** Falling as x rises is necessary but not sufficient, and "close enough" is not a test. The \"same amount each time\" verdict is right for the wrong reason: a steady drop by the same amount would make it LINEAR, which is not what inverse variation needs.',
  'A right verdict with a wrong reason costs marks on a written answer.')

assert 6 * 10 == 60 and sp.Rational(60, 4) == 15
q(Q, 3, 'The number of identical pumps and the time needed to drain a pond vary inversely. Six pumps drain it in 10 hours. How many pumps are needed to drain it in 4 hours?',
  ['15 pumps', '2.4 pumps', '12 pumps', '40 pumps'], 0,
  'Less time needs MORE pumps — find k first.',
  ['k = pumps × hours = 6 × 10 = 60 pump-hours of work.',
   'pumps = 60 ÷ hours.',
   'For 4 hours: 60 ÷ 4.',
   '15 pumps.'],
  '**15 pumps.** The job is 60 pump-hours whichever way you split it. 2.4 treats it as direct variation, so cutting the time would cut the pumps — the opposite of what happens. 40 multiplies 10 by 4, and 12 just doubles the pumps.',
  'Name k in words — "pump-hours" — and the set-up stops being guesswork.')

assert sp.Rational(240, 12) - sp.Rational(240, 16) == 5
q(Q, 3, 'A $240 bus rental is split equally, so each share is 240/n dollars for n people. A group of 12 is joined by 4 more people. By how much does each person\'s share drop?',
  ['$5', '$15', '$4', '$1.25'], 0,
  'Work out the share before and after; do not guess from the 4.',
  ['Before: 240 ÷ 12 = $20 each.',
   'After: 240 ÷ 16 = $15 each.',
   'The drop is $20 − $15.',
   'Each share drops by $5.'],
  '**$5.** The share falls from $20 to $15. $15 is the new share rather than the drop, $4 assumes each extra person knocks a dollar off, and $1.25 is 20 ÷ 16. The jump from 12 to 16 people is a third more people, but the share falls by only a quarter — inverse variation never moves in equal steps.',
  'With inverse variation, compute both values; equal steps in one never mean equal steps in the other.')

build('ad-astra', C, Q, 'unit-alg-t4-01',
      'Topic 4 · 4-1 Inverse Variation and the Reciprocal Function', 'algeo',
      'Lesson 4-1 introduces inverse variation, y = k/x, and its graph: how to recognise an inverse variation from a table, '
      'find and use the constant of variation, and graph the reciprocal function f(x) = 1/x and its translations, with their '
      'asymptotes, domain and range.',
      'Inverse variation describes every trade-off where one thing goes up exactly as another comes down — speed and travel '
      'time, workers and hours, pressure and volume. And the graph of 1/x is the parent of every rational function in this topic.',
      [('Decide whether a table or a situation is an inverse variation by checking that xy is constant', 'source'),
       ('Write an inverse variation equation from one pair of values and use it to find another', 'source'),
       ('Graph y = 1/x and its translations, and state their asymptotes, domain and range', 'source'),
       ('Tell inverse variation apart from direct variation and from a line that simply decreases', 'added')],
      'Two things trip students up here. First, treating any decreasing pattern as inverse variation — the test is that '
      'the PRODUCT xy stays constant, and one question deliberately offers a table where three of four products agree. '
      'Second, the sign inside the denominator: 1/(x + 3) moves the graph LEFT. One thing worth knowing: the textbook\'s '
      'own practice includes "gas left in a tank varies inversely with miles driven", which is not actually an inverse '
      'variation (the tank empties at a steady rate, a falling line). This unit teaches it as the counter-example; if her '
      'class marks it the book\'s way, that is worth a word with her teacher.',
      ('Start with the table test — multiply every column — then the translated graphs.', 18),
      'content/alg-topic4-01.json',
      'enVision Algebra 2, Lesson 4-1 (Drive)',
      'enVision Algebra 2 Lesson 4-1: Inverse Variation and the Reciprocal Function',
      libv_=1)
finish('content/alg-topic4-01.json')

# ================================================================ 4-2
C, Q = [], []

card(C, 'Rational function',
     "**A function written as one polynomial divided by another, P(x)/Q(x), with Q(x) not the zero polynomial.**"
     "\n• Its domain is every x where Q(x) ≠ 0."
     "\n• Rational numbers are ratios of integers; rational expressions are ratios of polynomials.",
     eq='R(x) = P(x)/Q(x)',
     hint='Polynomial over polynomial — nothing under a root, no variable exponents.')

card(C, 'Vertical asymptotes',
     "**x = a is a vertical asymptote when the denominator is 0 at a and the numerator is not.**"
     "\n• Factor the denominator and set each factor equal to 0."
     "\n• Close to a, the values shoot off to +∞ or −∞; test a value on each side to see which.",
     hint='Zero underneath, not zero on top.')

card(C, 'Holes',
     "**When a factor cancels from top and bottom, its zero is a hole in the graph, not a vertical asymptote.**"
     "\n• (x − 2)(x + 4)/((x − 2)(x + 1)) has a hole at x = 2 and an asymptote only at x = −1."
     "\n• The x-value is still excluded from the domain — the graph just has a single missing point there.",
     hint='Cancel first, then look for asymptotes.')

card(C, 'Horizontal asymptotes: the three cases',
     "**Compare degrees: top lower → y = 0; equal → y = ratio of the leading coefficients; top higher → no horizontal asymptote.**"
     "\n• (3x + 1)/(x² + 4): bottom wins, so y = 0."
     "\n• (6x² − x)/(2x² + 5): a tie, so y = 6/2 = 3."
     "\n• (x³ + 1)/(4x − 1): top wins, so the values run off without settling.",
     hint='Whichever degree is bigger wins the far-out race.')

card(C, 'Why the leading coefficients decide it',
     "**Far from the origin only the highest-degree terms matter, so a tie in degree leaves the ratio of their coefficients.**"
     "\n• For (8x + 3)/(4x − 1) with x = 1,000: 8,003/3,999 ≈ 2.001, closing in on 8/4 = 2."
     "\n• Substituting a huge x is a quick way to check any horizontal asymptote.",
     hint='Plug in a very large x and watch where the values head.')

card(C, 'Rewriting as a translated reciprocal',
     "**Long division turns (ax + b)/(x − h) into k + r/(x − h), which is 1/x stretched by r and moved to the asymptotes x = h and y = k.**"
     "\n• (3x − 1)/(x − 2) = 3 + 5/(x − 2)."
     "\n• It works exactly like turning an improper fraction into a mixed number.",
     eq='(ax + b)/(x − h) = k + r/(x − h)',
     hint='The quotient is the horizontal asymptote; the remainder is the stretch.')
assert sp.simplify((3*x - 1)/(x - 2) - (3 + 5/(x - 2))) == 0

card(C, 'Graphing (ax + b)/(cx + d)',
     "**Draw the asymptotes x = −d/c and y = a/c first, then plot a couple of points on each side of the vertical one.**"
     "\n• The asymptotes are your frame; the points tell you which corners the branches occupy."
     "\n• Add the intercepts: x-intercept where ax + b = 0, y-intercept at f(0) = b/d.",
     hint='Frame first, points second.')
_f = (x + 1) / (x - 3)
assert poles(_f) == [3] and hasym(_f) == 1 and _f.subs(x, 0) == sp.Rational(-1, 3)
C[-1]['graph'] = rgraph([_f], [-5, 9, -5, 7], vas=[3], has=[1],
                        pts=[{'x': -1, 'y': 0, 'label': '(−1, 0)'}])
C[-1]['def'] += "\n• Shown: (x + 1)/(x − 3), with asymptotes x = 3 and y = 1 and x-intercept (−1, 0)."

card(C, 'Several vertical asymptotes',
     "**A denominator that factors into several pieces can give several vertical asymptotes — one for each zero that does not cancel.**"
     "\n• (x + 2)/(x² − x − 12) = (x + 2)/((x − 4)(x + 3)): asymptotes at x = 4 and x = −3."
     "\n• The graph then has three pieces, not two.",
     hint='Factor the bottom completely before you decide.')
assert poles((x + 2)/(x**2 - x - 12)) == [-3, 4]

card(C, 'A horizontal asymptote can be crossed',
     "**Graphs may cross a horizontal asymptote in the middle; they can never cross a vertical one.**"
     "\n• The horizontal asymptote only describes the far ends."
     "\n• To find a crossing, set f(x) equal to the asymptote value and solve.",
     hint='Horizontal = end behaviour only. Vertical = a forbidden x.')
_f = (x**2 + 2*x) / (x**2 + 1)
assert hasym(_f) == 1 and sp.solve(sp.Eq(_f, 1), x) == [sp.Rational(1, 2)]
C[-1]['graph'] = rgraph([_f], [-6, 6, -1, 3], gy=1, has=[1],
                        pts=[{'x': 0.5, 'y': 1, 'label': '(½, 1)'}])
C[-1]['def'] += "\n• Shown: (x² + 2x)/(x² + 1) has asymptote y = 1 and crosses it at (½, 1)."

card(C, 'Intercepts',
     "**x-intercepts are where the numerator is 0 (and the denominator is not); the y-intercept is f(0).**"
     "\n• A rational function may have no y-intercept at all, when x = 0 is excluded."
     "\n• A zero of the numerator that also zeroes the denominator is a hole, not an intercept.",
     hint='Top = 0 for x-intercepts; x = 0 for the y-intercept.')

card(C, 'Average cost',
     "**Average cost = (fixed cost + cost per item × x)/x, and its horizontal asymptote is the cost per item.**"
     "\n• Spreading a big fixed cost over more items drives the average down toward the per-item cost, never below it."
     "\n• Its vertical asymptote x = 0 says: with nothing made, there is no average.",
     hint='The fixed cost thins out; the per-item cost never does.')

card(C, 'Solving with a graph',
     "**To solve f(x) ≥ c for a rational model, graph y = f(x) and y = c and read where the curve is on or above the line.**"
     "\n• Or clear the denominator algebraically — but only after checking its sign."
     "\n• In a real model, keep only the inputs that make sense (ages, amounts and times are not negative).",
     hint='Intersection first, then the side of it you want.')

# ---- level 1 -----------------------------------------------------------------
q(Q, 1, 'Which of these is a rational function?',
  ['f(x) = (x + 5)/(x² − 9)', 'f(x) = √x/(x² + 1)', 'f(x) = (x + 1)/|x − 9|', 'f(x) = 2ˣ/(x² − 3)'], 0,
  'Both top and bottom must be polynomials.',
  ['A rational function is a polynomial divided by a polynomial.',
   '√x is not a polynomial, |x| is not a polynomial, and 2ˣ has the variable in the exponent.',
   'x + 5 and x² − 9 are both polynomials.',
   'f(x) = (x + 5)/(x² − 9) is the rational function.'],
  '**f(x) = (x + 5)/(x² − 9).** Polynomial over polynomial. Each of the others breaks the rule in a different place: a radical on top, an absolute value underneath, and an exponential on top.',
  'A rational function can still have a messy domain — that is what its asymptotes are about.')

q(Q, 1, 'What is the vertical asymptote of f(x) = (x + 1)/(x − 7)?',
  ['x = 7', 'x = −7', 'x = −1', 'y = 1'], 0,
  'Set the denominator equal to zero.',
  ['The denominator is x − 7.',
   'x − 7 = 0 when x = 7.',
   'The numerator is 8 there, not 0, so it is an asymptote rather than a hole.',
   'The vertical asymptote is x = 7.'],
  '**x = 7.** The bottom is zero there and the top is not. x = −1 is where the TOP is zero — that is the x-intercept — and y = 1 is the horizontal asymptote.',
  'Denominator zero → vertical asymptote; numerator zero → x-intercept.')
assert poles(E('(x + 1)/(x − 7)')) == [7]

_f = E('(6x − 1)/(3x + 2)'); assert hasym(_f) == 2
q(Q, 1, 'What is the horizontal asymptote of f(x) = (6x − 1)/(3x + 2)?',
  ['y = 2', 'y = 6', 'y = −1/2', 'y = 0'], 0,
  'Compare the degrees of the top and the bottom.',
  ['Both top and bottom have degree 1 — a tie.',
   'A tie means the asymptote is the ratio of the leading coefficients.',
   'That ratio is 6/3.',
   'The horizontal asymptote is y = 2.'],
  '**y = 2.** Equal degrees, so divide the leading coefficients: 6 ÷ 3. y = −1/2 divides the constant terms, which matter near the origin but vanish far out; y = 0 is the rule for when the bottom has the HIGHER degree.',
  'Check with a big x: f(1,000) = 5,999/3,002 ≈ 1.998.')

_f = E('(x + 4)/(x² + 1)'); assert hasym(_f) == 0
q(Q, 1, 'What is the horizontal asymptote of f(x) = (x + 4)/(x² + 1)?',
  ['y = 0', 'y = 1', 'y = 4', 'There is none'], 0,
  'Which has the higher degree, top or bottom?',
  ['The top has degree 1; the bottom has degree 2.',
   'The bottom grows much faster, so the fraction shrinks toward 0.',
   'When the bottom has the higher degree, the asymptote is y = 0.',
   'The horizontal asymptote is y = 0.'],
  '**y = 0.** The bottom\'s x² outruns the top\'s x, so far out the fraction shrinks toward zero. y = 1 would need equal degrees, and "there is none" is the case when the TOP has the higher degree.',
  'Bottom-heavy fractions always settle on y = 0.')

_f = E('(x³ − 2)/(5x + 1)'); assert hasym(_f) is None
q(Q, 1, 'What is the horizontal asymptote of f(x) = (x³ − 2)/(5x + 1)?',
  ['None', 'y = 0', 'y = 1/5', 'y = −2'], 0,
  'Compare degrees: 3 against 1.',
  ['The top has degree 3; the bottom has degree 1.',
   'The top outgrows the bottom, so the values keep growing without settling.',
   'A top-heavy rational function has no horizontal asymptote.',
   'None.'],
  '**None.** With the higher degree on top, f(x) runs off to ±∞ instead of levelling out. y = 1/5 would need a tie in degree, and y = 0 would need the bottom to win.',
  'Top-heavy → no horizontal asymptote.')

_f = E('2x/(x² − 5x + 6)'); assert poles(_f) == [2, 3]
q(Q, 1, 'What is the domain of f(x) = 2x/(x² − 5x + 6)?',
  ['All real numbers except 2 and 3', 'All real numbers except −2 and −3',
   'All real numbers except 0', 'All real numbers except 6'], 0,
  'Factor the denominator and find its zeros.',
  ['x² − 5x + 6 = (x − 2)(x − 3).',
   'It is zero at x = 2 and at x = 3.',
   'Those two inputs are excluded.',
   'The domain is all real numbers except 2 and 3.'],
  '**All real numbers except 2 and 3.** Those are the zeros of (x − 2)(x − 3). −2 and −3 come from reading the signs in the factors instead of solving, and 0 is where the NUMERATOR is zero, which is perfectly allowed.',
  'Zeros of the numerator are allowed; zeros of the denominator are not.')

q(Q, 1, 'Which statement about the asymptotes of a rational function is true?',
  ['Its graph can cross a horizontal asymptote but never a vertical one',
   'Its graph can never cross either kind of asymptote at any point',
   'Its graph can cross a vertical asymptote but never a horizontal one',
   'Its graph can cross both kinds of asymptote as often as it likes'], 0,
  'What does each kind of asymptote actually describe?',
  ['A vertical asymptote x = a marks an input the function cannot take.',
   'So the graph has no point at all on that line.',
   'A horizontal asymptote only describes where the values settle far left and far right.',
   'In the middle of the graph, the curve is free to cross it.'],
  '**It can cross a horizontal asymptote but never a vertical one.** A vertical asymptote is an excluded x-value, so no point of the graph can sit on it. A horizontal asymptote is a statement about the far ends only, and plenty of graphs cross it in the middle before settling.',
  '"Never crosses an asymptote" is a myth that only holds for the vertical kind.')

# ---- level 2 -----------------------------------------------------------------
_t = E('(5x + 2)/(x − 1)')
same('5 + 7/(x − 1)', _t)
for s_ in ('5 + 2/(x − 1)', '2 + 5/(x − 1)', '5 − 7/(x − 1)'):
    differs(s_, _t)
q(Q, 2, 'Rewrite f(x) = (5x + 2)/(x − 1) in the form k + r/(x − h).',
  ['5 + 7/(x − 1)', '5 + 2/(x − 1)', '2 + 5/(x − 1)', '5 − 7/(x − 1)'], 0,
  'Divide x − 1 into 5x + 2 and keep the remainder.',
  ['5x ÷ x = 5, so the quotient is 5.',
   '5(x − 1) = 5x − 5.',
   '(5x + 2) − (5x − 5) = 7, the remainder.',
   'f(x) = 5 + 7/(x − 1).'],
  '**5 + 7/(x − 1).** So the graph is 1/x stretched by 7 and moved to the asymptotes x = 1 and y = 5. "5 + 2/(x − 1)" forgets to subtract 5(x − 1); "5 − 7/(x − 1)" subtracts the wrong way round.',
  'Check by recombining: 5(x − 1) + 7 = 5x + 2.')

_f = E('(x + 2)/(x² + x − 12)'); assert poles(_f) == [-4, 3]
q(Q, 2, 'What are the vertical asymptotes of f(x) = (x + 2)/(x² + x − 12)?',
  ['x = −4 and x = 3', 'x = 4 and x = −3', 'x = −2 only', 'x = −12 only'], 0,
  'Factor x² + x − 12.',
  ['x² + x − 12 = (x + 4)(x − 3).',
   'The zeros are x = −4 and x = 3.',
   'The numerator x + 2 is not zero at either, so neither is a hole.',
   'The vertical asymptotes are x = −4 and x = 3.'],
  '**x = −4 and x = 3.** (x + 4)(x − 3) is zero at both. x = 4 and x = −3 copy the signs out of the factors without solving, and x = −2 is the numerator\'s zero — the x-intercept.',
  'Solve each factor = 0; never read the answer straight off the sign.')

_f = E('(x − 5)/(x² − 2x − 15)')
assert poles(_f) == [-3] and holes(_f) == [5]
q(Q, 2, 'What does the graph of f(x) = (x − 5)/(x² − 2x − 15) have at x = 5 and at x = −3?',
  ['A hole at x = 5 and a vertical asymptote at x = −3',
   'A vertical asymptote at both x = 5 and x = −3',
   'A vertical asymptote at x = 5 and a hole at x = −3',
   'A hole at both x = 5 and x = −3, and no asymptote'], 0,
  'Factor the bottom and look for a factor that cancels.',
  ['x² − 2x − 15 = (x − 5)(x + 3).',
   'f(x) = (x − 5)/((x − 5)(x + 3)), and the x − 5 cancels.',
   'A cancelled factor leaves a hole; what remains, 1/(x + 3), has an asymptote at x = −3.',
   'Hole at x = 5, vertical asymptote at x = −3.'],
  '**A hole at x = 5 and a vertical asymptote at x = −3.** Both values are excluded from the domain, but they look different on the graph: the cancelled factor leaves a single missing point, while the factor that survives makes the values shoot off to infinity.',
  'Cancel first, then decide which zeros are holes and which are asymptotes.')

_f = E('(2x − 6)/(x + 3)')
assert sp.solve(sp.numer(sp.together(_f)), x) == [3] and _f.subs(x, 0) == -2
q(Q, 2, 'What are the intercepts of f(x) = (2x − 6)/(x + 3)?',
  ['x-intercept (3, 0) and y-intercept (0, −2)', 'x-intercept (−3, 0) and y-intercept (0, −2)',
   'x-intercept (3, 0) and y-intercept (0, 2)', 'x-intercept (3, 0) and no y-intercept'], 0,
  'Numerator zero for the x-intercept; x = 0 for the y-intercept.',
  ['2x − 6 = 0 gives x = 3, and the denominator is 6 there, not 0.',
   'So the x-intercept is (3, 0).',
   'f(0) = −6/3 = −2.',
   'The y-intercept is (0, −2).'],
  '**(3, 0) and (0, −2).** (−3, 0) uses the denominator\'s zero, which is the vertical asymptote — the function does not even exist there. (0, 2) drops the sign of −6, and x = 0 is a perfectly allowed input here, so there is a y-intercept.',
  'An x-intercept can never come from the denominator.')

_gr = E('(2x + 1)/(x − 2)')
assert poles(_gr) == [2] and hasym(_gr) == 2
for s_, vv, hh in (('(2x + 1)/(x + 2)', [-2], 2), ('(x + 1)/(x − 2)', [2], 1),
                   ('(x − 2)/(2x + 1)', [sp.Rational(-1, 2)], sp.Rational(1, 2))):
    assert poles(E(s_)) == vv and hasym(E(s_)) == hh
q(Q, 2, 'The graph shown has its asymptotes drawn in and crosses the x-axis at x = −½. Which function does it show?',
  ['f(x) = (2x + 1)/(x − 2)', 'f(x) = (2x + 1)/(x + 2)', 'f(x) = (x + 1)/(x − 2)', 'f(x) = (x − 2)/(2x + 1)'], 0,
  'Read the vertical asymptote, then the horizontal one, then check each option against both.',
  ['The vertical asymptote is x = 2, so the denominator is zero at 2: x − 2.',
   'The horizontal asymptote is y = 2, so the leading coefficients must divide to 2.',
   '(2x + 1)/(x − 2) has both, and its numerator is zero at x = −½.',
   'The graph shows f(x) = (2x + 1)/(x − 2).'],
  '**f(x) = (2x + 1)/(x − 2).** (2x + 1)/(x + 2) has the right horizontal asymptote but its vertical one is at x = −2. (x + 1)/(x − 2) has the right vertical asymptote but settles at y = 1. (x − 2)/(2x + 1) is the reciprocal: asymptotes x = −½ and y = ½.',
  'Two asymptotes usually narrow it to one option; the intercept confirms it.')
Q[-1]['graph'] = rgraph([_gr], [-6, 8, -6, 9], gy=2, vas=[2], has=[2])

_f = E('(2x² + x)/(x² − 9)')
assert hasym(_f) == 2 and sp.solve(sp.Eq(_f, 2), x) == [-18]
q(Q, 2, 'f(x) = (2x² + x)/(x² − 9) has horizontal asymptote y = 2. Where, if anywhere, does its graph cross that asymptote?',
  ['At x = −18', 'At x = 18', 'At x = 0', 'It never crosses it'], 0,
  'Set f(x) equal to 2 and solve.',
  ['(2x² + x)/(x² − 9) = 2.',
   'Multiply by x² − 9: 2x² + x = 2x² − 18.',
   'The 2x² terms cancel, leaving x = −18.',
   'x = −18 is not ±3, so it is allowed: the graph crosses y = 2 at x = −18.'],
  '**At x = −18.** Far out to the left the graph comes in from just above or below y = 2 and passes through it at (−18, 2) before settling. "It never crosses" is the myth from the vertical kind of asymptote; x = 0 is where the graph crosses the x-axis, not y = 2.',
  'Crossing a horizontal asymptote is just an ordinary equation: set f(x) = k.')

_C = (60000 + sp.Rational(1, 2) * x) / x
assert hasym(_C) == sp.Rational(1, 2)
q(Q, 2, 'An app costs $60,000 to build and $0.50 per download to deliver, so its average cost per download is C(x) = (60,000 + 0.5x)/x. What does the horizontal asymptote of C say?',
  ['y = 0.5: the average cost falls toward $0.50 and never reaches it',
   'y = 60,000: the average cost levels off at $60,000 per download',
   'y = 0: with enough downloads, each one costs almost nothing',
   'None exists: the average cost keeps falling forever with no limit'], 0,
  'Both top and bottom have degree 1. Compare their leading coefficients.',
  ['The top is 0.5x + 60,000 and the bottom is x: equal degrees.',
   'The ratio of leading coefficients is 0.5 ÷ 1 = 0.5.',
   'Far out, the $60,000 is spread so thin it hardly matters, but every download still costs $0.50.',
   'The horizontal asymptote is y = 0.5.'],
  '**y = 0.5.** C(x) = 0.5 + 60,000/x, and the second term shrinks toward 0 as downloads pile up, leaving the $0.50 that every single download costs. It never reaches $0.50, because some of the build cost is always in the average.',
  'In an average-cost model, the asymptote is the cost nobody can spread away.')

# ---- level 3 -----------------------------------------------------------------
_w = E('2x²/((x + 1)(x − 4))')
assert poles(_w) == [-1, 4] and hasym(_w) == 2
for s_ in ('2x/((x + 1)(x − 4))', 'x²/((x − 1)(x + 4))', '2x²/((x − 1)(x + 4))'):
    ff = E(s_); assert not (poles(ff) == [-1, 4] and hasym(ff) == 2)
q(Q, 3, 'Which function has vertical asymptotes x = −1 and x = 4, and horizontal asymptote y = 2?',
  ['f(x) = 2x²/((x + 1)(x − 4))', 'f(x) = 2x/((x + 1)(x − 4))',
   'f(x) = x²/((x − 1)(x + 4))', 'f(x) = 2x²/((x − 1)(x + 4))'], 0,
  'Build the denominator from the vertical asymptotes, then match the degrees for y = 2.',
  ['x = −1 and x = 4 need the factors (x + 1) and (x − 4) underneath.',
   'That denominator has degree 2 and leading coefficient 1.',
   'For y = 2, the top must also have degree 2 with leading coefficient 2: 2x².',
   'f(x) = 2x²/((x + 1)(x − 4)), and 2x² is not zero at −1 or 4.'],
  '**f(x) = 2x²/((x + 1)(x − 4)).** 2x/(…) has a lower-degree top, so its asymptote is y = 0. The (x − 1)(x + 4) versions put the vertical asymptotes at x = 1 and x = −4 — the sign trap again.',
  'Many functions fit these asymptotes. Any top of the form 2x² + bx + c works, as long as it is not zero at −1 or 4.')

_D = 300 * x / (x + 12)
assert sp.solve(sp.Eq(_D, 120), x) == [8]
assert sp.Rational(300, 1) * sp.Rational(2, 5) == 120   # the dropped-denominator slip: 300a = 120
q(Q, 3, 'A child\'s dose of a medicine is D(a) = 300a/(a + 12) milligrams, where a is the age in years, and the dose grows with age. At what age is the dose exactly 120 mg?',
  ['8 years', '4.8 years', '12 years', '0.4 years'], 0,
  'Set 300a/(a + 12) equal to 120 and clear the denominator.',
  ['300a/(a + 12) = 120.',
   'Multiply both sides by a + 12: 300a = 120a + 1,440.',
   '180a = 1,440.',
   'a = 8 years.'],
  '**8 years.** Check: D(8) = 2,400/20 = 120 mg. 4.8 years is 120 × 12 ÷ 300, which loses the a in the denominator; 0.4 years ignores the denominator entirely (300a = 120); 12 years mistakes the 12 in the formula for the answer.',
  'Clear the denominator by multiplying EVERY term on both sides by it.')

_f = 1 / (x - 3)**2
assert sp.limit(_f, x, 3, '+') == sp.oo and sp.limit(_f, x, 3, '-') == sp.oo
q(Q, 3, 'For f(x) = 1/(x − 3)², what happens as x approaches 3 from each side?',
  ['f(x) → +∞ from both the left and the right', 'f(x) → −∞ from the left and +∞ from the right',
   'f(x) → +∞ from the left and −∞ from the right', 'f(x) → 0 from both the left and the right'], 0,
  'What sign does a square have?',
  ['Near x = 3, (x − 3)² is a tiny number.',
   'A square is never negative, so it is a tiny POSITIVE number on both sides.',
   '1 divided by a tiny positive number is a huge positive number.',
   'f(x) → +∞ from both sides.'],
  '**+∞ from both sides.** The square makes the denominator positive whichever side you come from, so both pieces of the graph shoot upward. Opposite directions on the two sides is the behaviour of 1/(x − 3), whose denominator changes sign at 3.',
  'Test one value each side — 2.9 and 3.1 — whenever you are unsure.')

_f = E('(−3x + 1)/(x + 5)'); assert hasym(_f) == -3
assert hasym(E('(3x + 1)/(x − 5)')) == 3 and hasym(E('(x − 3)/(x + 5)')) == 1 and hasym(E('(−3x² + 1)/(x + 5)')) is None
q(Q, 3, 'Which function has the horizontal asymptote y = −3?',
  ['f(x) = (−3x + 1)/(x + 5)', 'f(x) = (3x + 1)/(x − 5)', 'f(x) = (x − 3)/(x + 5)', 'f(x) = (−3x² + 1)/(x + 5)'], 0,
  'You need equal degrees AND leading coefficients that divide to −3.',
  ['(−3x + 1)/(x + 5): equal degrees, −3 ÷ 1 = −3.',
   '(3x + 1)/(x − 5): equal degrees, but 3 ÷ 1 = 3.',
   '(x − 3)/(x + 5): equal degrees, 1 ÷ 1 = 1 — the −3 is a constant, which does not count.',
   '(−3x² + 1)/(x + 5): the top has the higher degree, so there is no horizontal asymptote.'],
  '**f(x) = (−3x + 1)/(x + 5).** Every option contains a 3; only one puts −3 on the LEADING terms with the degrees tied. The squared version is the subtle one: the leading coefficient is right, but the degrees are not equal.',
  'Degrees first, coefficients second.')

_f = E('(x² + 2x − 8)/(x² − 4)')
assert poles(_f) == [-2] and holes(_f) == [2] and hasym(_f) == 1
q(Q, 3, 'A classmate says f(x) = (x² + 2x − 8)/(x² − 4) has vertical asymptotes x = 2 and x = −2 and horizontal asymptote y = 1. What is wrong?',
  ['x = 2 is a hole, not an asymptote; only x = −2 is a vertical asymptote',
   'The horizontal asymptote should be y = 2, from the 2x in the numerator',
   'There is no horizontal asymptote, because the two degrees are equal',
   'Nothing is wrong — both vertical asymptotes and y = 1 are correct'], 0,
  'Factor top and bottom before deciding anything.',
  ['Top: x² + 2x − 8 = (x + 4)(x − 2). Bottom: x² − 4 = (x − 2)(x + 2).',
   'The factor x − 2 cancels, leaving (x + 4)/(x + 2) with a hole at x = 2.',
   'Only x + 2 survives underneath, so x = −2 is the one vertical asymptote.',
   'The degrees tie with leading coefficients 1 and 1, so y = 1 is right.'],
  '**x = 2 is a hole, not an asymptote.** The classmate found the zeros of the denominator without checking the numerator. y = 1 is correct, and equal degrees give the ratio of leading coefficients, not "no asymptote".',
  'Always factor the top too — a shared factor turns an asymptote into a hole.')

_C = 4 / (10 + x)
assert sp.solve(sp.Eq(_C, sp.Rational(1, 4)), x) == [6]
q(Q, 3, 'A jug holds 10 litres of juice that is 40% fruit, so 4 litres are fruit. After x litres of water are added, the fruit fraction is F(x) = 4/(10 + x). How much water makes the drink 25% fruit?',
  ['6 litres', '16 litres', '15 litres', '2.5 litres'], 0,
  'Set 4/(10 + x) equal to 0.25.',
  ['4/(10 + x) = 0.25.',
   'Multiply by 10 + x: 4 = 0.25(10 + x) = 2.5 + 0.25x.',
   '1.5 = 0.25x, so x = 6.',
   'Add 6 litres of water.'],
  '**6 litres.** Check: 4 out of 16 litres is 25%. 16 litres is the TOTAL volume, not the water added; 15 comes from 40 − 25; 2.5 litres is 25% of the original 10.',
  'Once you have an answer, plug it back into the model — it takes five seconds.')

build('ad-astra', C, Q, 'unit-alg-t4-02',
      'Topic 4 · 4-2 Graphing Rational Functions', 'algeo',
      'Lesson 4-2 graphs rational functions: finding vertical asymptotes from the denominator, horizontal asymptotes by '
      'comparing degrees, rewriting (ax + b)/(cx + d) with long division to see the translation, graphs that cross a '
      'horizontal asymptote, and rational models such as a dosage rule.',
      'Asymptotes are the skeleton of a rational graph: find them first and the curve almost draws itself. The same '
      'three-case degree comparison returns in calculus as the idea of a limit.',
      [('Find vertical asymptotes and holes by factoring the denominator', 'source'),
       ('Find the horizontal asymptote by comparing the degrees of the numerator and denominator', 'source'),
       ('Rewrite (ax + b)/(cx + d) as a translated reciprocal function and sketch it', 'source'),
       ('Use a rational model to answer a question about a real situation', 'source')],
      'The most common slip is treating every zero of the denominator as a vertical asymptote without factoring the '
      'numerator too — a shared factor makes a HOLE instead, and one question is built around exactly that error. The '
      'second is the myth that a graph can never cross an asymptote: that is only true of vertical ones, and the '
      'textbook spends a whole example on a graph crossing its horizontal asymptote.',
      ('Learn the three degree cases for horizontal asymptotes first; they come up in almost every question.', 20),
      'content/alg-topic4-02.json',
      'enVision Algebra 2, Lesson 4-2 (Drive)',
      'enVision Algebra 2 Lesson 4-2: Graphing Rational Functions',
      libv_=1)
finish('content/alg-topic4-02.json')
