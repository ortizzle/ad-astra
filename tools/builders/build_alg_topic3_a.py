# Algebra & Geometry II — Topic 3: Polynomial Functions, lessons 3-1 and 3-2.
#
# Sources (her Drive "Topic 3" folder, uploaded 2026-09-17):
#   aga_24_a2_0301_se.pdf / 0302_se.pdf   — the student-edition lessons
#   3-1_ / 3-2_ Mathematical Literacy and Vocabulary (PDF)
#   polynomial-practice.pdf               — her teacher's own 3.1-3.2 practice sheet
#
# EVERY algebraic result below is expanded and compared with sympy before it can
# reach a question (see ck/deg/end). Nothing is worked by hand, and none of the
# sources' own numbers are reused — the practice sheet and the textbook examples
# were read to calibrate difficulty and style only, per the standalone rule.
import sympy as sp
from unit_common import card, q, build

x, y, z, a, b, c, d = sp.symbols('x y z a b c d')

def ck(got, want):
    """Assert two expressions are equal as polynomials, and hand back the string
    form actually used in the question so the file can never drift from the maths."""
    g, w = sp.expand(sp.sympify(got)), sp.expand(sp.sympify(want))
    assert sp.simplify(g - w) == 0, 'MISMATCH: %s  !=  %s' % (g, w)
    return w

def deg(e, v=x):
    return sp.degree(sp.expand(sp.sympify(e)), v)

def lead(e, v=x):
    return sp.LC(sp.Poly(sp.expand(sp.sympify(e)), v))

def end(e, v=x):
    """End behaviour as (left, right) in {'up','down'} — computed, never asserted by eye."""
    p = sp.expand(sp.sympify(e))
    L = sp.limit(p, v, -sp.oo); R = sp.limit(p, v, sp.oo)
    f = lambda t: 'up' if t == sp.oo else 'down'
    return f(L), f(R)

# ---------------------------------------------------------------- 3-1
C, Q = [], []

card(C, 'Polynomial function',
     "**A function built from terms of the form axⁿ, where every exponent on the variable is a whole number.**"
     "\n• No variable in a denominator, under a radical, or with a negative or fractional exponent."
     "\n• f(x) = 4x³ − x + 7 is one; f(x) = 4x⁻³ + 7 and f(x) = √x are not.",
     hint='Whole-number exponents only — that single test rules every impostor out.')

card(C, 'Standard form',
     "**The terms written in order from the greatest exponent down to the least.**"
     "\n• 3x² − 1 + 5x⁴ − x becomes 5x⁴ + 3x² − x − 1."
     "\n• Put it in standard form FIRST — degree and leading coefficient are both read off the front, and reading them off an unsorted polynomial is the commonest slip in this lesson.",
     hint='Sort before you read anything off it.')

card(C, 'Degree',
     "**The greatest exponent on the variable once the polynomial is simplified.**"
     "\n• The degree tells you the SHAPE: how the ends behave and how many turns are possible."
     "\n• 7x³ − 9x⁵ + 2 has degree 5, not 3 — the greatest exponent, not the first one written.",
     hint='Greatest exponent, not the leading one as written.')

card(C, 'Leading coefficient',
     "**The number multiplying the highest-degree term.**"
     "\n• In standard form it is simply the first coefficient."
     "\n• Its SIGN decides which way the right-hand end of the graph goes.",
     hint='It rides on the highest power, wherever that term happens to be written.')

card(C, 'Term',
     "**One part of a polynomial — a coefficient times a power of the variable.**"
     "\n• Terms are separated by + and − signs."
     "\n• 5x⁴ + 3x² − x − 1 has four terms.",
     hint='Count the pieces the plus and minus signs cut it into.')

card(C, 'End behaviour',
     "**What the function values do as x runs far out to the left and far out to the right.**"
     "\n• Written as: as x → ∞, f(x) → ∞ (and separately for x → −∞)."
     "\n• It depends on exactly two things — the degree's parity and the leading coefficient's sign. Nothing else in the polynomial matters.",
     hint='Only the highest-degree term survives far from the origin; everything else is dwarfed.')

card(C, 'The four end-behaviour cases',
     "**Even degree: both ends agree. Odd degree: the ends disagree.**"
     "\n• Even degree, positive lead — both ends up. Even degree, negative lead — both ends down."
     "\n• Odd degree, positive lead — down on the left, up on the right. Odd degree, negative lead — up on the left, down on the right."
     "\n• Sanity check: y = x² is both ends up, y = x³ falls left and rises right. Every case is one of those two pictures, possibly flipped.",
     hint='Parity says whether the ends MATCH; the sign says which way the right end points.')

card(C, 'Turning point',
     "**A point where the graph changes direction — from rising to falling, or falling to rising.**"
     "\n• Each one is either a relative maximum or a relative minimum."
     "\n• A polynomial of degree n has AT MOST n − 1 turning points, and may have fewer.",
     hint='At most n − 1 — an upper limit, never a promise.')

card(C, 'Relative maximum',
     "**A point higher than every point immediately around it — where the graph stops rising and starts falling.**"
     "\n• \"Relative\" because it only beats its own neighbourhood; the graph may climb higher somewhere else entirely."
     "\n• On an odd-degree polynomial there is never a highest point overall, since one end runs off to +∞.",
     hint='A local hilltop, not necessarily the highest hill on the map.')

card(C, 'Relative minimum',
     "**A point lower than every point immediately around it — where the graph stops falling and starts rising.**"
     "\n• The mirror image of a relative maximum."
     "\n• Reading these off a graph is how you describe where a quantity bottoms out.",
     hint='A local valley floor.')

card(C, 'Why at most n − 1 turns',
     "**A degree-n polynomial changes direction at most n − 1 times, so counting turns puts a FLOOR under the degree.**"
     "\n• Three visible turning points means the degree is at least 4 — it could be higher."
     "\n• This is the usual way a question gives you a graph and asks for the smallest degree that could produce it.",
     hint='Turns seen + 1 = the least degree that could do it.')

card(C, 'Increasing and decreasing intervals',
     "**Intervals of x on which the graph is going up, or going down, read left to right.**"
     "\n• Always described in terms of x-values, never y-values."
     "\n• They are separated exactly by the turning points.",
     hint='Read left to right, and name the x-interval.')

card(C, 'A cubic, read off its graph',
     "**f(x) = x³ − 4x has odd degree and a positive leading coefficient, so it falls on the left and rises on the right.**"
     "\n• Two turning points — the most a degree-3 polynomial can have."
     "\n• It crosses at x = −2, 0 and 2.",
     eq='f(x) = x³ − 4x',
     hint='Odd degree: the two ends point opposite ways.', frm='added')
C[-1]['graph'] = {'w': [-3.2, 3.2, -6, 6], 'gx': 1, 'gy': 2,
                  'series': [{'type': 'poly', 'c': [1, 0, -4, 0]}],
                  'pts': [{'x': -2, 'y': 0, 'label': '−2'}, {'x': 2, 'y': 0, 'label': '2'}],
                  'xl': 'x', 'yl': 'f(x)'}

card(C, 'A quartic, read off its graph',
     "**g(x) = −x⁴ + 5x² − 4 has even degree and a negative leading coefficient, so BOTH ends go down.**"
     "\n• Three turning points — the most a degree-4 polynomial can have."
     "\n• Because both ends fall, this one does have a highest point overall.",
     eq='g(x) = −x⁴ + 5x² − 4',
     hint='Even degree: both ends agree, and the negative lead sends both of them down.', frm='added')
C[-1]['graph'] = {'w': [-3, 3, -8, 4], 'gx': 1, 'gy': 2,
                  'series': [{'type': 'poly', 'c': [-1, 0, 5, 0, -4]}],
                  'xl': 'x', 'yl': 'g(x)'}

# --- verify every claim the two graph cards make, rather than trusting the picture
assert end('x**3 - 4*x') == ('down', 'up') and deg('x**3 - 4*x') == 3
assert sorted(sp.solve(sp.Eq(x**3 - 4*x, 0), x)) == [-2, 0, 2]
assert end('-x**4 + 5*x**2 - 4') == ('down', 'down') and deg('-x**4 + 5*x**2 - 4') == 4
# turning points = real roots of the derivative
assert len([r for r in sp.solve(sp.diff(x**3 - 4*x, x), x) if r.is_real]) == 2
assert len([r for r in sp.solve(sp.diff(-x**4 + 5*x**2 - 4, x), x) if r.is_real]) == 3

# ---- questions -------------------------------------------------------------
q(Q, 1, 'Which one of these is a polynomial function?',
  ['h(x) = 6x⁴ − 2x + 9', 'h(x) = 6x⁻⁴ − 2x + 9', 'h(x) = 6√x − 2x + 9', 'h(x) = 6⁄x⁴ − 2x + 9'], 0,
  'Check every exponent on the variable.',
  ['A polynomial allows only whole-number exponents on the variable.',
   'A negative exponent (x⁻⁴) is disqualifying.',
   'A radical is a ½ power, and a variable in a denominator is a negative power — both disqualifying.',
   'Only 6x⁴ − 2x + 9 has whole-number exponents throughout.'],
  '**h(x) = 6x⁴ − 2x + 9.** Every exponent on x is a whole number. The other three each break that in a different way: a negative exponent, a radical (which is really the ½ power), and a variable in a denominator (which is really a negative power).',
  'The three impostors are the same disqualification wearing three costumes.')

_p1 = '2*x**2 - 7*x**5 + x - 4'
assert deg(_p1) == 5 and lead(_p1) == -7
q(Q, 1, 'What is the degree of 2x² − 7x⁵ + x − 4?',
  ['5', '2', '4', '−7'], 0,
  'Degree is about the greatest exponent, not the term written first.',
  ['Scan every term for its exponent on x: 2, 5, 1, 0.',
   'The greatest of those is 5.',
   'It does not matter that the 5 is not the first term written.',
   'The degree is 5.'],
  '**5.** Degree is the GREATEST exponent once you look at every term — not the exponent on whichever term happens to be written first. Writing it in standard form (−7x⁵ + 2x² + x − 4) makes it obvious, which is exactly why standard form comes first.',
  'Sorting into standard form before reading anything off costs a second and prevents this.')

q(Q, 1, 'What is the leading coefficient of 2x² − 7x⁵ + x − 4?',
  ['−7', '2', '5', '−4'], 0,
  'The leading coefficient rides on the highest-degree term.',
  ['Find the highest-degree term first: −7x⁵.',
   'The leading coefficient is the number multiplying it.',
   'The sign travels with it — it is −7, not 7.',
   'The leading coefficient is −7.'],
  '**−7.** The leading coefficient belongs to the highest-degree term wherever that term is written, and the minus sign is part of it. Answering 2 means reading the first term written rather than the highest-degree one.',
  'Negative leading coefficients matter enormously here — the sign flips the end behaviour.')

_p2 = '4*x**3 - 9 + x**6 - 2*x'
ck(_p2, 'x**6 + 4*x**3 - 2*x - 9')
q(Q, 1, 'Write 4x³ − 9 + x⁶ − 2x in standard form.',
  ['x⁶ + 4x³ − 2x − 9', '−9 − 2x + 4x³ + x⁶', '4x³ + x⁶ − 2x − 9', 'x⁶ + 4x³ − 9 − 2x'], 0,
  'Greatest exponent first, then down.',
  ['List each term with its exponent: 4x³ (3), −9 (0), x⁶ (6), −2x (1).',
   'Order them from greatest exponent to least: 6, 3, 1, 0.',
   'That gives x⁶ + 4x³ − 2x − 9.',
   'Each term keeps the sign it already had.'],
  '**x⁶ + 4x³ − 2x − 9.** Standard form runs from the greatest exponent down to the constant, and every term keeps its own sign on the way. Ascending order is a real ordering, just not this one.',
  'The constant is the x⁰ term, so it always lands last.')

q(Q, 1, 'A polynomial function has degree 6. What is the greatest number of turning points its graph can have?',
  ['5', '6', '7', '3'], 0,
  'The rule is one less than the degree.',
  ['A degree-n polynomial has at most n − 1 turning points.',
   'Here n = 6.',
   'So at most 6 − 1 = 5 turning points.',
   'It may well have fewer — 5 is a ceiling, not a promise.'],
  '**5.** The bound is n − 1, so a degree-6 polynomial turns at most 5 times. Note the direction of the rule: it caps the turns, it does not guarantee them — y = x⁶ is degree 6 and turns exactly once.',
  'Read it as a ceiling. The same rule run backwards gives a FLOOR on the degree from a graph.')

q(Q, 1, 'What does the end behaviour of a polynomial function describe?',
  ['What the function values do as x runs far out in both directions',
   'Where the graph crosses the x-axis and the y-axis',
   'The highest and lowest points the graph ever reaches',
   'The intervals on which the graph is increasing or decreasing'], 0,
  'The word "end" is about the far ends of the x-axis.',
  ['End behaviour looks at x → ∞ and x → −∞.',
   'It reports what f(x) does out there — rising without bound, or falling without bound.',
   'Crossings, peaks and intervals are all features near the middle of the graph.',
   'End behaviour is about the far left and far right.'],
  '**What the function values do as x runs far out in both directions.** Far from the origin the highest-degree term dwarfs everything else, which is why only the degree and the leading coefficient decide end behaviour — the rest of the polynomial stops mattering out there.',
  'That is also why you can state the end behaviour without doing any arithmetic at all.')

q(Q, 1, 'On a graph, a relative minimum is the point where the function changes from',
  ['decreasing to increasing', 'increasing to decreasing', 'positive to negative', 'negative to positive'], 0,
  'Picture the bottom of a valley and walk through it left to right.',
  ['Walking left to right, you come DOWN into a valley — the function is decreasing.',
   'At the bottom it stops falling.',
   'Then you climb out — the function is increasing.',
   'So a relative minimum is decreasing changing to increasing.'],
  '**Decreasing to increasing.** Increasing-to-decreasing is the other one, a relative maximum. Positive-to-negative describes crossing the x-axis, which is a different feature entirely — a valley floor can sit well above or well below the axis.',
  'Sign changes are about the x-axis; turning points are about direction.')

_q8 = '3*x**4 - x**2 + 5'
assert end(_q8) == ('up', 'up')
q(Q, 2, 'Describe the end behaviour of f(x) = 3x⁴ − x² + 5.',
  ['As x → −∞, f(x) → ∞ and as x → ∞, f(x) → ∞',
   'As x → −∞, f(x) → −∞ and as x → ∞, f(x) → ∞',
   'As x → −∞, f(x) → ∞ and as x → ∞, f(x) → −∞',
   'As x → −∞, f(x) → −∞ and as x → ∞, f(x) → −∞'], 0,
  'Two questions only: is the degree even or odd, and is the lead positive or negative?',
  ['The degree is 4, which is even, so both ends agree.',
   'The leading coefficient is 3, which is positive, so the right end rises.',
   'Both ends agree and the right one rises, so both rise.',
   'As x → −∞, f(x) → ∞ and as x → ∞, f(x) → ∞.'],
  '**Both ends rise.** Even degree makes the ends agree; a positive leading coefficient sends the right end up; agreeing means the left goes up too. The −x² and the +5 have no say — far from the origin 3x⁴ dwarfs both.',
  'Think of y = x² and stretch it: same picture, higher degree.')

_q9 = '-2*x**5 + 40*x**2'
assert end(_q9) == ('up', 'down')
q(Q, 2, 'Describe the end behaviour of g(x) = −2x⁵ + 40x².',
  ['As x → −∞, g(x) → ∞ and as x → ∞, g(x) → −∞',
   'As x → −∞, g(x) → −∞ and as x → ∞, g(x) → ∞',
   'As x → −∞, g(x) → ∞ and as x → ∞, g(x) → ∞',
   'As x → −∞, g(x) → −∞ and as x → ∞, g(x) → −∞'], 0,
  'Odd degree means the two ends disagree — then let the sign place them.',
  ['The degree is 5, which is odd, so the ends point opposite ways.',
   'The leading coefficient is −2, which is negative, so the right end falls.',
   'The ends disagree, so the left end must rise.',
   'As x → −∞, g(x) → ∞ and as x → ∞, g(x) → −∞.'],
  '**Up on the left, down on the right.** Odd degree makes the ends disagree, and the negative lead pulls the right-hand end down. The +40x² is a big-looking coefficient, and it genuinely shapes the middle of the graph — but far out, x⁵ beats x² no matter what sits in front of them.',
  'A large coefficient on a low-degree term never changes end behaviour. Degree wins every time.')

q(Q, 2, 'A polynomial graph has exactly 3 turning points. What is the LEAST degree it could have?',
  ['4', '3', '5', '6'], 0,
  'Run the turning-point rule backwards.',
  ['A degree-n polynomial has at most n − 1 turning points.',
   'To allow 3 turns you need n − 1 ≥ 3.',
   'So n ≥ 4.',
   'The least possible degree is 4.'],
  '**4.** Turns + 1 gives the least degree that could produce the graph. It really is only a floor: a degree-6 polynomial can also show exactly 3 turns, so a graph can never pin the degree down exactly — it can only rule degrees out from below.',
  'Answering 3 uses n turns instead of n − 1 — off by one in the direction that makes the polynomial too simple.')

q(Q, 2, 'The graph shown has how many turning points, and what does that say about its degree?',
  ['2 turning points, so the degree is at least 3',
   '3 turning points, so the degree is at least 4',
   '2 turning points, so the degree is exactly 2',
   '3 turning points, so the degree is exactly 3'], 0,
  'Count the direction changes, then add one.',
  ['Walk the curve left to right and count where it changes direction.',
   'It falls, turns up, rises, turns down — no, here it rises to a peak then falls to a valley then rises: 2 turns.',
   'Two turns means n − 1 ≥ 2, so n ≥ 3.',
   '2 turning points, so the degree is at least 3.'],
  '**2 turning points, so the degree is at least 3.** Counting turns gives a floor on the degree, never an exact value — "exactly 3" claims more than a picture can tell you. And a degree-2 graph (a parabola) turns only once, so 2 turns rules degree 2 out completely.',
  'A graph bounds the degree from below. Only the equation pins it down.')
Q[-1]['graph'] = {'w': [-3.2, 3.2, -6, 6], 'gx': 1, 'gy': 2,
                  'series': [{'type': 'poly', 'c': [1, 0, -4, 0]}],
                  'xl': 'x', 'yl': 'f(x)'}

q(Q, 2, 'A function is decreasing on (−∞, −1), increasing on (−1, 2), and decreasing on (2, ∞). Where are its turning points?',
  ['At x = −1 and x = 2', 'At x = 0 only', 'At x = −1, 0 and 2', 'There are no turning points'], 0,
  'A turning point sits exactly where the description switches direction.',
  ['The description changes from decreasing to increasing at x = −1.',
   'That switch is a turning point — a relative minimum.',
   'It changes from increasing to decreasing at x = 2, another turning point — a relative maximum.',
   'The turning points are at x = −1 and x = 2.'],
  '**At x = −1 and x = 2.** Turning points are exactly the boundaries between the increasing and decreasing intervals, so you can read them straight off a description like this without ever seeing the graph. Two turns also tells you the degree is at least 3.',
  'The intervals and the turning points are two ways of saying the same thing.')

_q13 = '(x - 1)*(x + 3)*(x - 4)'
assert deg(_q13) == 3 and end(_q13) == ('down', 'up')
ck(_q13, 'x**3 - 2*x**2 - 11*x + 12')
q(Q, 2, 'Without multiplying it out, what are the degree and end behaviour of f(x) = (x − 1)(x + 3)(x − 4)?',
  ['Degree 3; falls on the left, rises on the right',
   'Degree 3; rises on the left, falls on the right',
   'Degree 1; falls on the left, rises on the right',
   'Degree 3; both ends rise'], 0,
  'Degrees add when factors multiply, and each x here carries a coefficient of 1.',
  ['Each factor contributes one power of x, so the degree is 1 + 1 + 1 = 3.',
   'Multiplying the leading terms gives x · x · x = x³, so the leading coefficient is +1.',
   'Odd degree means the ends disagree; a positive lead sends the right end up.',
   'Degree 3, falling on the left and rising on the right.'],
  '**Degree 3; falls left, rises right.** You never have to expand it: the degree is the number of linear factors, and the leading coefficient is the product of the factors’ leading coefficients. Answering degree 1 counts the factors’ individual degrees instead of adding them.',
  'Factored form hands you the degree and the end behaviour faster than standard form does.')

q(Q, 2, 'Which statement about a polynomial of EVEN degree with a NEGATIVE leading coefficient is true?',
  ['It has a highest point overall, but no lowest point overall',
   'It has a lowest point overall, but no highest point overall',
   'It has both a highest and a lowest point overall',
   'It has neither a highest nor a lowest point overall'], 0,
  'Sketch the ends first, then ask what the middle must do.',
  ['Even degree means both ends agree; a negative lead sends the right end down.',
   'So both ends run down to −∞.',
   'Running down forever in both directions means there is no lowest point — the values go below any number you name.',
   'But the graph must top out somewhere in the middle, so there IS a highest point overall.'],
  '**A highest point overall, but no lowest.** Both ends dive to −∞, so no value is the smallest — you can always go further out and get lower. In between, the curve has to reach a maximum. This is the upside-down version of y = x², which has a lowest point and no highest.',
  'Odd-degree polynomials have neither, since one end goes each way.')

_q15a, _q15b = 'x**3 - 6*x', '-(x**3 - 6*x)'
assert end(_q15a) == ('down', 'up') and end(_q15b) == ('up', 'down')
q(Q, 3, 'f(x) = x³ − 6x falls on the left and rises on the right. What happens to the end behaviour of −f(x)?',
  ['It reverses: −f rises on the left and falls on the right',
   'It is unchanged, because the degree did not change',
   'Both ends of −f now rise',
   'Both ends of −f now fall'], 0,
  'Multiplying by −1 flips the sign of every output, including out at the ends.',
  ['Negating the whole function negates the leading coefficient: +1 becomes −1.',
   'The degree is still 3, so the ends still disagree.',
   'But the sign flip sends the right end the other way — down instead of up.',
   'So −f rises on the left and falls on the right: the end behaviour reverses.'],
  '**It reverses.** Negating a function reflects the whole graph across the x-axis, so every rise becomes a fall. The degree is untouched, which is why the ends still disagree — they have just swapped places. "Unchanged because the degree did not change" gets half the rule right and forgets the sign does the other half.',
  'Degree decides whether the ends match; the sign decides which way they point. Change one and only that half moves.')

q(Q, 3, 'Why can a polynomial of degree 4 never have 5 turning points?',
  ['Because a degree-n polynomial changes direction at most n − 1 times',
   'Because a degree-4 polynomial always has exactly 3 turning points',
   'Because turning points must come in pairs',
   'Because a degree-4 polynomial has at most 4 x-intercepts'], 0,
  'One of these states the actual rule; the others state true-sounding things that do not answer it.',
  ['The bound on turning points is n − 1.',
   'For n = 4 that is 3, so 5 is impossible.',
   '"Exactly 3" is false — y = x⁴ is degree 4 and turns once, so the rule has to be an upper bound.',
   'The reason is that a degree-n polynomial changes direction at most n − 1 times.'],
  '**Because a degree-n polynomial changes direction at most n − 1 times.** That is the rule itself. The x-intercept bound is a real and separate fact about a different feature, and "exactly 3" overstates a rule that is genuinely only a ceiling — y = x⁴ turns once.',
  'When a question asks WHY, the answer that states the governing rule beats one that states a true but unrelated fact.')

# a fresh applied scenario, deliberately not the source sheet's apple orchard
Vw = sp.expand((12 - 2*x)*(9 - 2*x)*x)
ck(Vw, '4*x**3 - 42*x**2 + 108*x')
assert deg(Vw) == 3
_crit = [r for r in sp.solve(sp.diff(Vw, x), x) if r.is_real and 0 < r < 4.5]
assert len(_crit) == 1
_xbest = sp.nsimplify(_crit[0])
# the maximising cut is 1.6972... cm — not used in any question text, only to
# confirm the box's single interior maximum really does sit between the
# intercepts, which is what the explanation claims. (My hand estimate said
# 1.696; the assert caught it.)
assert abs(float(_xbest) - 1.69722) < 0.001, float(_xbest)
assert 0 < float(_xbest) < 4.5
q(Q, 3, 'An open box is made from a 12 cm by 9 cm sheet by cutting a square of side x from each corner and folding the sides up. Its volume is V(x) = x(12 − 2x)(9 − 2x). What is the degree of V, and what do the x-intercepts mean here?',
  ['Degree 3; they are the cut sizes that give a box of zero volume',
   'Degree 3; they are the cut sizes that give the largest box',
   'Degree 2; they are the cut sizes that give a box of zero volume',
   'Degree 3; they are the possible heights of the box'], 0,
  'An intercept is where the OUTPUT is zero — so ask what a zero output means in this situation.',
  ['Three linear factors multiply to a degree-3 polynomial.',
   'An x-intercept is a value of x making V(x) = 0.',
   'V is the volume, so those are cut sizes producing no box at all — x = 0 (no sides folded up), x = 4.5 (the 9 cm side vanishes) and x = 6 (the 12 cm side vanishes).',
   'Degree 3, and the intercepts are the cut sizes giving zero volume.'],
  '**Degree 3, and they are the cut sizes giving zero volume.** Always translate an intercept back through the context: here the output is volume, so a zero means no box. The LARGEST box is at a turning point between the intercepts, not at one — a different feature answering a different question.',
  'Intercepts answer "when is the output nothing?"; turning points answer "when is it most?"')

q(Q, 3, 'Two polynomials both have degree 5. One has leading coefficient 100 and the other has leading coefficient 0.01, and both are positive. How do their end behaviours compare?',
  ['Identical — both fall on the left and rise on the right',
   'Opposite, because one coefficient is so much larger',
   'The one with lead 100 rises on both ends; the other does not',
   'Neither can be determined without the full polynomials'], 0,
  'Ask which two facts the rule actually uses.',
  ['End behaviour depends on the degree’s parity and the leading coefficient’s SIGN.',
   'Both have degree 5, which is odd, so both have ends that disagree.',
   'Both leading coefficients are positive, so both right ends rise.',
   'Their end behaviours are identical — the size of the coefficient never enters the rule.'],
  '**Identical.** The rule reads the SIGN of the leading coefficient and nothing else about it. The size changes how steeply the graph climbs and where its turns sit, so the two curves look very different near the origin — but "eventually rises" and "eventually falls" are the same for both.',
  'Size shapes the middle of the picture. Only the sign shapes the ends.')

q(Q, 3, 'Put these polynomials in order from LEAST degree to greatest degree.',
  ['7x − 4', '2x² − x³ + 1', 'x⁴ + 3x⁶ − x', '5x⁹ − x⁸'], 0,
  'Write each one in standard form first, then read the front.',
  ['7x − 4 has greatest exponent 1.',
   '2x² − x³ + 1 has greatest exponent 3 — not 2, which is only written first.',
   'x⁴ + 3x⁶ − x has greatest exponent 6, again not the one written first.',
   '5x⁹ − x⁸ has greatest exponent 9. So the order is 1, 3, 6, 9.'],
  '**Degrees 1, 3, 6 and 9.** Two of these deliberately do not lead with their highest-degree term, which is the whole trap — sorting into standard form first turns a fiddly comparison into reading four numbers off the front.',
  'The habit that prevents this is sorting before reading, every single time.',
  kind='order')

q(Q, 3, 'A graph falls on the left, rises to a peak, falls to a valley, and then rises on the right. What can you conclude about its degree and leading coefficient?',
  ['Odd degree, at least 3, with a positive leading coefficient',
   'Even degree, at least 4, with a positive leading coefficient',
   'Odd degree, exactly 3, with a negative leading coefficient',
   'Even degree, at least 4, with a negative leading coefficient'], 0,
  'Take the ends and the turns as two separate pieces of evidence, then combine them.',
  ['The ends disagree — down on the left, up on the right — so the degree is odd.',
   'The right end rises, so the leading coefficient is positive.',
   'There are 2 turning points, so the degree is at least 3.',
   'Odd, at least 3, positive lead.'],
  '**Odd degree, at least 3, positive lead.** Two independent readings: the ends give parity and sign, the turns give a floor on the degree. "Exactly 3" overreaches — a degree-5 polynomial can draw this same picture.',
  'Ends and turns answer different questions. Read both, and claim only what each supports.')

build('ad-astra', C, Q, 'unit-alg-t3-01',
      'Topic 3 · 3-1 Graphing Polynomial Functions', 'algeo',
      'Lesson 3-1 introduces polynomial functions and how to read their graphs: standard form, degree, '
      'leading coefficient and terms, then end behaviour, turning points, and relative maximums and minimums.',
      'Degree and leading coefficient are only two numbers, but between them they fix the whole shape of the '
      'graph before you plot a single point. Getting fluent at reading them costs seconds and saves whole questions.',
      [('Write a polynomial in standard form and identify its degree and leading coefficient', 'source'),
       ('State the end behaviour from the degree and the leading coefficient alone', 'source'),
       ('Use turning points to put a lower bound on the degree', 'source'),
       ('Read relative maximums, relative minimums and intervals of increase off a graph', 'source')],
      'The single most common slip in this lesson is reading the degree or the leading coefficient off the '
      'FIRST term written rather than the highest-degree one — several questions here are built to catch exactly '
      'that, and the fix is simply to write standard form first. The second is treating "at most n − 1 turning '
      'points" as a promise rather than a ceiling; a graph can only put a FLOOR under the degree, never pin it '
      'down. Her teacher’s own practice sheet (3.1–3.2) drills end behaviour hard, so it is worth the time.',
      ('Start with the four end-behaviour cases — they turn into free marks once they are automatic.', 18),
      'content/alg-topic3-01.json',
      'enVision Algebra 2, Lesson 3-1 (Drive)',
      'enVision Algebra 2 Lesson 3-1: Graphing Polynomial Functions')

# ---------------------------------------------------------------- 3-2
C, Q = [], []

card(C, 'Like terms',
     "**Terms with exactly the same variable raised to exactly the same power.**"
     "\n• 5x³ and −2x³ are like terms; 5x³ and 5x² are not."
     "\n• Only like terms can be combined, and combining them adds the coefficients while the power stays put.",
     hint='Same variable, same exponent — both, not either.')

card(C, 'Adding polynomials',
     "**Combine like terms; every unlike term just comes along unchanged.**"
     "\n• (3x² + x) + (x² − 4) = 4x² + x − 4."
     "\n• The exponents never change when you add — only the coefficients do.",
     hint='Add the coefficients, leave the powers alone.')

card(C, 'Subtracting polynomials',
     "**Distribute the minus sign to EVERY term in the second polynomial, then add.**"
     "\n• (5x² + 2x − 1) − (3x² − 7x + 4) = 5x² + 2x − 1 − 3x² + 7x − 4."
     "\n• Note −7x became +7x and +4 became −4. Missing the terms after the first is the single most common error in this lesson.",
     eq='(A) − (B) = A + (−1)·B',
     hint='The minus belongs to the whole bracket, not just its first term.')

card(C, 'Why the minus sign is the trap',
     "**Subtracting is multiplying the second polynomial by −1, so every single term flips sign — not just the one at the front.**"
     "\n• Writing the −1 in front of the bracket and distributing it deliberately is slower and much safer than doing it in your head."
     "\n• If you check one thing on a subtraction problem, check that the LAST term flipped.",
     hint='Check the last term — that is the one that gets forgotten.')

card(C, 'Closure',
     "**Add, subtract or multiply two polynomials and the result is always another polynomial.**"
     "\n• Polynomials are closed under addition, subtraction and multiplication."
     "\n• They are NOT closed under division — (x + 1) ÷ x is not a polynomial.",
     hint='Three of the four operations stay inside the club; division is the one that escapes.')

card(C, 'Multiplying a monomial by a polynomial',
     "**Distribute: multiply the monomial by every term.**"
     "\n• 3x²(2x³ − 5x + 1) = 6x⁵ − 15x³ + 3x²."
     "\n• Multiply the coefficients and ADD the exponents — x² · x³ = x⁵, never x⁶.",
     eq='x^m · x^n = x^(m+n)',
     hint='Coefficients multiply; exponents add.')

card(C, 'Multiplying two binomials',
     "**Every term in the first multiplies every term in the second.**"
     "\n• (2x + 3)(x − 5) = 2x² − 10x + 3x − 15 = 2x² − 7x − 15."
     "\n• Two terms times two terms gives four products before you combine.",
     hint='Count the products first: 2 × 2 = 4. If you have fewer, you missed one.')

card(C, 'Multiplying larger polynomials',
     "**Same rule — every term times every term — so an m-term by an n-term product has m × n products before combining.**"
     "\n• A binomial times a trinomial gives 2 × 3 = 6 products."
     "\n• Counting them first is the cheapest way to catch a missed one.",
     hint='m × n products. Count before you combine.')

card(C, 'Degree of a product',
     "**Multiply two polynomials and the degrees ADD.**"
     "\n• A degree-3 times a degree-4 gives a degree-7 polynomial."
     "\n• It follows from the highest-degree terms multiplying: x³ · x⁴ = x⁷."
     "\n• This lets you predict the degree of an answer before you expand — a fast check that you did not drop a term.",
     eq='deg(A·B) = deg A + deg B',
     hint='Degrees add on multiplication, the same way exponents do.')

card(C, 'Degree of a sum or difference',
     "**Usually the larger of the two degrees — but it can be LOWER if the leading terms cancel.**"
     "\n• (x³ + 2x) + (−x³ + 5) = 2x + 5, which is degree 1, not 3."
     "\n• So the rule for sums is genuinely different from the clean one for products.",
     hint='Products are predictable; sums can collapse.')

card(C, 'Example: a subtraction, worked',
     "**(4x³ − x² + 6) − (x³ + 5x² − 2) = 3x³ − 6x² + 8.**"
     "\n• Distribute: 4x³ − x² + 6 − x³ − 5x² + 2."
     "\n• Watch the last term: −2 became +2. Combine: (4 − 1)x³, (−1 − 5)x², (6 + 2).",
     hint='Every sign in the second bracket flipped — check the constant.', frm='added')

card(C, 'Example: a multiplication, worked',
     "**(x + 4)(2x² − 3x + 1) = 2x³ + 5x² − 11x + 4.**"
     "\n• Expect 1 × 3 + 1 × 3 = 6 products, and degree 1 + 2 = 3."
     "\n• x gives 2x³ − 3x² + x; 4 gives 8x² − 12x + 4; combining gives 2x³ + 5x² − 11x + 4.",
     hint='Predict the degree and the product count first, then check your answer against both.', frm='added')

ck('(4*x**3 - x**2 + 6) - (x**3 + 5*x**2 - 2)', '3*x**3 - 6*x**2 + 8')
ck('(x + 4)*(2*x**2 - 3*x + 1)', '2*x**3 + 5*x**2 - 11*x + 4')
ck('3*x**2*(2*x**3 - 5*x + 1)', '6*x**5 - 15*x**3 + 3*x**2')
ck('(2*x + 3)*(x - 5)', '2*x**2 - 7*x - 15')
ck('(3*x**2 + x) + (x**2 - 4)', '4*x**2 + x - 4')
ck('(5*x**2 + 2*x - 1) - (3*x**2 - 7*x + 4)', '2*x**2 + 9*x - 5')

# ---- questions -------------------------------------------------------------
q(Q, 1, 'Which pair are like terms?',
  ['−7x⁵ and 2x⁵', '−7x⁵ and 2x³', '−7x⁵ and 2y⁵', '−7x⁵ and −7x³'], 0,
  'Like terms need the same variable AND the same exponent.',
  ['Compare the variable: both must be x.',
   'Compare the exponent: both must be the same power.',
   '−7x⁵ and 2x⁵ match on both counts.',
   'The others differ in exponent, in variable, or in exponent again.'],
  '**−7x⁵ and 2x⁵.** Both conditions have to hold at once. Matching coefficients (the two −7s) counts for nothing — that is the one thing that is allowed to differ.',
  'Only like terms combine, and combining adds the coefficients while the power stays put.')

ck('(2*x**3 + 5*x - 1) + (4*x**3 - 3*x + 6)', '6*x**3 + 2*x + 5')
q(Q, 1, 'Simplify (2x³ + 5x − 1) + (4x³ − 3x + 6).',
  ['6x³ + 2x + 5', '6x³ + 8x + 5', '6x⁶ + 2x + 5', '6x³ + 2x − 7'], 0,
  'Group like terms, then add coefficients.',
  ['Cubes: 2x³ + 4x³ = 6x³.',
   'x terms: 5x + (−3x) = 2x.',
   'Constants: −1 + 6 = 5.',
   'The sum is 6x³ + 2x + 5.'],
  '**6x³ + 2x + 5.** Adding combines coefficients and leaves exponents alone — 6x⁶ comes from adding the exponents, which is the multiplication rule wandering into an addition problem.',
  'Exponents only add when you MULTIPLY. On a sum they never move.')

ck('(8*x**2 - 3*x + 5) - (2*x**2 + 6*x - 9)', '6*x**2 - 9*x + 14')
q(Q, 1, 'Simplify (8x² − 3x + 5) − (2x² + 6x − 9).',
  ['6x² − 9x + 14', '6x² + 3x − 4', '6x² − 9x − 4', '10x² + 3x − 4'], 0,
  'Distribute the minus across all three terms before combining anything.',
  ['Rewrite as 8x² − 3x + 5 − 2x² − 6x + 9 — all three signs flipped.',
   'Squares: 8x² − 2x² = 6x².',
   'x terms: −3x − 6x = −9x.',
   'Constants: 5 + 9 = 14. The result is 6x² − 9x + 14.'],
  '**6x² − 9x + 14.** The constant is where this is won or lost: −(−9) is +9, so 5 + 9 = 14. Getting −4 there means the minus sign reached the first term and then quietly stopped.',
  'On any subtraction, check the LAST term first. It is the one that gets forgotten.')

q(Q, 1, 'Polynomials are closed under which operations?',
  ['Addition, subtraction and multiplication', 'Addition and subtraction only',
   'All four, including division', 'Multiplication and division only'], 0,
  'Closed means the answer is always the same kind of thing you started with.',
  ['Add two polynomials and you always get a polynomial.',
   'Subtract two and you always get a polynomial.',
   'Multiply two and you always get a polynomial.',
   'Divide and you may not — (x + 1) ÷ x is not a polynomial. So it is the first three.'],
  '**Addition, subtraction and multiplication.** Division is the one that escapes: dividing can produce a variable in a denominator, which is a negative exponent, which a polynomial is not allowed. This is exactly like the integers — closed under the first three, not under division.',
  'The integers are the analogy: 3 ÷ 2 leaves the integers the same way (x + 1) ÷ x leaves the polynomials.')

ck('5*x**3*(3*x**2 - 4*x + 2)', '15*x**5 - 20*x**4 + 10*x**3')
q(Q, 1, 'Simplify 5x³(3x² − 4x + 2).',
  ['15x⁵ − 20x⁴ + 10x³', '15x⁶ − 20x³ + 10x³', '15x⁵ − 4x + 2', '8x⁵ − 20x⁴ + 10x³'], 0,
  'Multiply the coefficients, add the exponents, and reach every term.',
  ['5x³ · 3x² = 15x⁵ (coefficients multiply, exponents add).',
   '5x³ · (−4x) = −20x⁴.',
   '5x³ · 2 = 10x³.',
   'Together: 15x⁵ − 20x⁴ + 10x³.'],
  '**15x⁵ − 20x⁴ + 10x³.** Coefficients multiply and exponents ADD — x³ · x² = x⁵, not x⁶. And the monomial has to reach all three terms; stopping after the first leaves the rest of the bracket untouched.',
  'Adding the exponents on a multiplication is the mirror image of the mistake on the previous kind of question.')

q(Q, 1, 'A degree-4 polynomial is multiplied by a degree-5 polynomial. What is the degree of the product?',
  ['9', '20', '5', '1'], 0,
  'On a product, degrees behave the way exponents do.',
  ['The highest-degree terms multiply to give the highest-degree term of the product.',
   'x⁴ · x⁵ = x⁹.',
   'So the degrees add: 4 + 5 = 9.',
   'The product has degree 9.'],
  '**9.** Degrees add on multiplication because exponents do. Multiplying them (20) confuses the rule with the coefficients, which genuinely do multiply — but degrees are exponents, and exponents add.',
  'Predicting the degree before you expand catches a dropped term instantly.')

ck('(x + 7)*(x - 2)', 'x**2 + 5*x - 14')
q(Q, 2, 'Expand (x + 7)(x − 2).',
  ['x² + 5x − 14', 'x² − 5x − 14', 'x² + 5x + 14', 'x² − 14'], 0,
  'Expect four products before combining.',
  ['x · x = x².',
   'x · (−2) = −2x and 7 · x = 7x.',
   'Combine the middle: −2x + 7x = 5x.',
   '7 · (−2) = −14. So x² + 5x − 14.'],
  '**x² + 5x − 14.** The middle term comes from combining two separate products, which is why "x² − 14" is wrong — that answer multiplies only the first terms and only the last terms and skips the cross products entirely.',
  'Four products from two binomials. If you wrote fewer, one is missing.')

ck('(3*x - 4)*(2*x**2 + x - 5)', '6*x**3 - 5*x**2 - 19*x + 20')
q(Q, 2, 'Expand (3x − 4)(2x² + x − 5).',
  ['6x³ − 5x² − 19x + 20', '6x³ + 5x² − 19x − 20',
   '6x³ − 5x² − 11x + 20', '6x³ − 8x² − 19x + 20'], 0,
  'Two terms times three terms: expect six products, and degree 1 + 2 = 3.',
  ['3x across the trinomial: 6x³ + 3x² − 15x.',
   '−4 across the trinomial: −8x² − 4x + 20.',
   'Combine x²: 3x² − 8x² = −5x². Combine x: −15x − 4x = −19x.',
   'The product is 6x³ − 5x² − 19x + 20.'],
  '**6x³ − 5x² − 19x + 20.** The −4 must reach all three terms and carry its sign each time — including −4 · (−5) = +20. Checking the degree (3) and the product count (6) before combining catches a dropped term before it becomes a wrong answer.',
  'Distributing a NEGATIVE term across a trinomial is where this goes wrong. Write the sign every time.')

ck('(2*x + 5)**2', '4*x**2 + 20*x + 25')
q(Q, 2, 'Expand (2x + 5)².',
  ['4x² + 20x + 25', '4x² + 25', '2x² + 20x + 25', '4x² + 10x + 25'], 0,
  'Squaring means multiplying the binomial by itself — write it out twice.',
  ['(2x + 5)² means (2x + 5)(2x + 5).',
   'First terms: 2x · 2x = 4x².',
   'Cross terms: 2x · 5 = 10x, twice, giving 20x.',
   'Last: 5 · 5 = 25. So 4x² + 20x + 25.'],
  '**4x² + 20x + 25.** The middle term is the one that disappears if you square each piece separately — "4x² + 25" is what you get by squaring the terms and forgetting they multiply each other too. There are TWO cross products, which is why it is 20x and not 10x.',
  'Writing the bracket out twice rather than squaring in place prevents both wrong answers here.')

ck('(x**3 + 2*x) + (-x**3 + 5)', '2*x + 5')
q(Q, 2, 'What is the degree of (x³ + 2x) + (−x³ + 5)?',
  ['1', '3', '0', '6'], 0,
  'Simplify before you answer — something cancels.',
  ['Combine the cubes: x³ + (−x³) = 0.',
   'What is left is 2x + 5.',
   'The greatest exponent there is 1.',
   'The degree is 1.'],
  '**1.** The leading terms cancelled, so the sum has a LOWER degree than either polynomial it came from. That is the real difference between sums and products: a product’s degree is always the sum of the degrees, but a sum’s degree can collapse.',
  'Always simplify before reading a degree off. On sums, the answer can be smaller than you expect.')

ck('(x**2 + 3*x - 1) - (x**2 - 3*x + 1)', '6*x - 2')
q(Q, 2, 'Simplify (x² + 3x − 1) − (x² − 3x + 1).',
  ['6x − 2', '0', '2x² − 2', '6x'], 0,
  'Flip every sign in the second bracket, then see what survives.',
  ['Distribute: x² + 3x − 1 − x² + 3x − 1.',
   'Squares: x² − x² = 0.',
   'x terms: 3x + 3x = 6x.',
   'Constants: −1 − 1 = −2. The result is 6x − 2.'],
  '**6x − 2.** The two polynomials look nearly identical, which tempts you into answering 0 — but they differ in the signs of the last two terms, and subtracting flips those, so those terms DOUBLE rather than cancel. Only the x² terms cancel.',
  'Near-identical brackets are the classic setup for this. Distribute first, judge afterwards.')

_Aq = sp.expand((x + 6)*(x + 4) - x*(x + 4))
ck(_Aq, '6*x + 24')
q(Q, 2, 'A rectangular garden is x m by (x + 4) m. A path widens the longer pair of sides so the garden becomes (x + 6) m by (x + 4) m. How much area was added?',
  ['(6x + 24) m²', '(6x) m²', '(2x² + 10x + 24) m²', '(x² + 10x + 24) m²'], 0,
  'New area minus old area — and subtraction means distributing the minus.',
  ['New area: (x + 6)(x + 4) = x² + 10x + 24.',
   'Old area: x(x + 4) = x² + 4x.',
   'Subtract, distributing the minus: x² + 10x + 24 − x² − 4x.',
   'That leaves 6x + 24 square metres.'],
  '**(6x + 24) m².** Expand both areas, then subtract with the minus reaching every term. The x² terms cancel, which makes sense: the added strip is a rectangle, so its area should be degree 1 in x, not degree 2. Answering with an x² term means the subtraction never happened.',
  'A quick reality check: a strip added to one side should grow linearly, so an x² in the answer is a red flag.')

q(Q, 3, 'A student expands (3x − 2)(x² + 5x − 4) and gets 3x³ + 15x² − 12x − 2x² − 10x + 8, then writes the answer as 3x³ + 13x² − 2x + 8. What went wrong?',
  ['Nothing — both lines are correct',
   'The −2 was not distributed to every term',
   'The exponents were added incorrectly',
   'The x² terms were combined incorrectly'], 0,
  'Check the student’s work line by line instead of just redoing the problem.',
  ['3x across the trinomial gives 3x³ + 15x² − 12x. Correct.',
   '−2 across the trinomial gives −2x² − 10x + 8. Correct, including −2 · (−4) = +8.',
   'Combining: 15x² − 2x² = 13x², and −12x − 10x = −22x.',
   'The student wrote −2x where it should be −22x — an error in combining the x terms, not in the expansion.'],
  '**The expansion is right; the x terms were combined wrong.** Every product was distributed correctly, including −2 · (−4) = +8. The error is in the very last step: −12x − 10x is −22x, not −2x. A question asking "what went wrong" can have its error in the combining rather than the method, so check the final line as carefully as the first.',
  'Read a worked solution line by line. The mistake is often later than you expect.')
# Rebalanced so all four read as the same shape and length — two of them agree
# the expansion is right and differ only in WHICH terms were combined wrong, so
# eliminating takes the arithmetic rather than a ruler.
Q[-1]['opts'] = ['The expansion is right; the x terms were combined wrong',
                 'The expansion is right; the x² terms were combined wrong',
                 'The −2 was not distributed to every term of the trinomial',
                 'The exponents were added instead of being multiplied']
ck('(3*x - 2)*(x**2 + 5*x - 4)', '3*x**3 + 13*x**2 - 22*x + 8')

q(Q, 3, 'Is it possible for the product of two polynomials of degree 3 to have degree 5?',
  ['No — the degrees add, so the product must be degree 6',
   'Yes — if the leading terms cancel',
   'Yes — if one polynomial has a negative leading coefficient',
   'No — the product must be degree 9'], 0,
  'Ask what produces the highest-degree term of a product.',
  ['The highest-degree term of a product comes from multiplying the two leading terms.',
   'Two leading terms multiply to something of degree 3 + 3 = 6.',
   'Two non-zero numbers can never multiply to zero, so that term can never vanish.',
   'The product must have degree 6 — 5 is impossible.'],
  '**No — the degrees add, so it is always degree 6.** Cancellation is exactly what CAN happen on a sum and cannot happen on a product: adding can zero out a leading term, but multiplying two non-zero leading coefficients always gives a non-zero result. That asymmetry is the whole point.',
  'Sums can collapse in degree; products never can. Know which rule you are under.')

_wq = sp.expand((2*x + 1)*(2*x + 1)*(x + 3))
ck(_wq, '4*x**3 + 16*x**2 + 13*x + 3')
assert deg(_wq) == 3
q(Q, 3, 'A box has a square base of side (2x + 1) cm and height (x + 3) cm. Which expression gives its volume, and what degree is it?',
  ['4x³ + 16x² + 13x + 3, degree 3', '4x³ + 16x² + 13x + 3, degree 4',
   '2x³ + 7x² + 3x, degree 3', '4x² + 4x + 1, degree 2'], 0,
  'Volume is base area times height — and predict the degree before expanding.',
  ['Base area: (2x + 1)² = 4x² + 4x + 1.',
   'Predict the degree: 2 + 1 = 3, so the answer must be a cubic.',
   'Multiply by (x + 3): 4x³ + 4x² + x + 12x² + 12x + 3.',
   'Combine: 4x³ + 16x² + 13x + 3, degree 3.'],
  '**4x³ + 16x² + 13x + 3, degree 3.** Three linear factors multiply to a cubic, so the degree is settled before any expanding — a free check on the answer. The degree-2 option is the base area alone, with the height never used.',
  'Volume from three lengths is always degree 3. If your answer is not a cubic, you dropped a factor.')

q(Q, 3, 'Why does subtracting polynomials cause more errors than adding them?',
  ['Because the minus sign must be distributed to every term of the second polynomial',
   'Because subtraction changes the exponents as well as the coefficients',
   'Because the answer can have a different degree',
   'Because like terms cannot be combined under subtraction'], 0,
  'One of these names an actual extra step; the others describe things that do not happen.',
  ['Addition just combines like terms straight away.',
   'Subtraction inserts a step first: multiply the whole second polynomial by −1.',
   'That step touches EVERY term, and skipping the terms after the first is the usual slip.',
   'So it is the distribution of the minus sign that creates the extra risk.'],
  '**Because the minus sign must be distributed to every term.** Exponents never change under either operation, and like terms combine normally under both. A degree change from cancellation can happen on an addition just as easily, so it is not what makes subtraction harder — the extra distribution step is.',
  'Writing the −1 explicitly in front of the bracket turns the risky step into a visible one.')

ck('(x - 3)*(x + 3)', 'x**2 - 9')
q(Q, 2, 'Expand (x − 3)(x + 3).',
  ['x² − 9', 'x² + 9', 'x² − 6x − 9', 'x² − 6x + 9'], 0,
  'Work the four products and watch what happens to the middle two.',
  ['First terms: x · x = x².',
   'Cross terms: x · 3 = 3x and −3 · x = −3x.',
   'Those two cancel exactly, so there is no middle term.',
   'Last: −3 · 3 = −9. So x² − 9.'],
  '**x² − 9.** The cross terms cancel because the two constants are opposites — this is the difference-of-squares pattern, and Lesson 3-3 names it as an identity worth memorising. Getting −6x + 9 is the answer to (x − 3)², a different product entirely.',
  'A sum times its difference always loses the middle term. Spotting it saves real time later.')

ck('2*x*(x - 4) + 3*(x - 4)', '2*x**2 - 5*x - 12')
q(Q, 2, 'Simplify 2x(x − 4) + 3(x − 4).',
  ['2x² − 5x − 12', '2x² + 5x − 12', '2x² − 8x − 12', '2x² − 5x + 12'], 0,
  'Distribute both products first, then gather like terms.',
  ['2x(x − 4) = 2x² − 8x.',
   '3(x − 4) = 3x − 12.',
   'Add them: 2x² − 8x + 3x − 12.',
   'Combine the x terms: −8x + 3x = −5x, giving 2x² − 5x − 12.'],
  '**2x² − 5x − 12.** Both brackets have to be distributed before anything can be combined. Worth noticing: both terms share the factor (x − 4), so this is (2x + 3)(x − 4) — the same answer reached by factoring instead of expanding.',
  'A shared bracket is a factoring opportunity. Expanding and factoring should agree, which makes each a check on the other.')

ck('(x**2 + 2*x - 5) - (x**2 + 2*x - 5)', '0')
q(Q, 3, 'What is the degree of (4x⁵ + x² − 7) − (4x⁵ + x² − 7)?',
  # Every option is a phrase of comparable length: with '5'/'2'/'0' as bare
  # digits the 41-character answer was spottable without reading it at all
  # (check_content flagged 4000%, the worst in the library).
  ['No degree at all, because the result is 0',
   'Degree 5, the highest power written down',
   'Degree 2, from the x² terms',
   'Degree 0, the same as any constant'], 0,
  'Do the subtraction before you answer anything about degree.',
  ['Distribute the minus: 4x⁵ + x² − 7 − 4x⁵ − x² + 7.',
   'Every single term cancels with its partner.',
   'The result is the zero polynomial.',
   'The zero polynomial has no degree at all — it is the one polynomial with none.'],
  '**No degree at all, because the result is 0.** Subtracting a polynomial from itself leaves nothing, and the zero polynomial is the one case where "degree" is left undefined rather than being some number. Answering 0 confuses the zero polynomial with a constant like 7, which does have degree 0.',
  'A non-zero constant has degree 0. Zero itself is the exception, and it is the only one.')

_pr = sp.expand((x + 2)*(x - 5))
ck(_pr, 'x**2 - 3*x - 10')
q(Q, 3, 'Without expanding, how many terms will (x + 2)(x − 5) have after it is fully simplified, and why?',
  ['3, because two of the four products are like terms and combine',
   '4, because two terms times two terms gives four products',
   '2, because the cross terms always cancel',
   '3, because the degrees add to 2'], 0,
  'Count the products first, then ask which of them can combine.',
  ['Two terms times two terms gives 2 × 2 = 4 products.',
   'They are x², −5x, 2x and −10.',
   'The two middle products are both x terms, so they are like terms and combine into one.',
   'That leaves 3 terms: x² − 3x − 10.'],
  '**3, because two of the four products are like terms.** Four products go in and three terms come out, because the cross terms are both degree 1. They only vanish entirely when the constants are exact opposites, as in (x − 3)(x + 3) — here 2 and −5 are not, so they combine to −3x rather than cancelling.',
  'Count products, then check which are like terms. That predicts the shape of the answer before you do any of it.')

build('ad-astra', C, Q, 'unit-alg-t3-02',
      'Topic 3 · 3-2 Adding, Subtracting, and Multiplying Polynomials', 'algeo',
      'Lesson 3-2 covers the arithmetic of polynomials: combining like terms to add and subtract, distributing '
      'to multiply, and the fact that polynomials are closed under all three operations but not under division.',
      'Every later lesson in this topic — dividing, factoring, finding roots — assumes you can expand and combine '
      'without slips. This is the lesson where accuracy is worth more than speed.',
      [('Add and subtract polynomials by combining like terms', 'source'),
       ('Distribute the subtraction sign across every term of the second polynomial', 'source'),
       ('Multiply polynomials of any size, term by term', 'source'),
       ('Predict the degree of a sum or a product before expanding', 'added')],
      'The error to watch for is the subtraction sign: it has to reach EVERY term in the second bracket, and the '
      'term most often missed is the last one. Several questions here are built so that stopping halfway produces '
      'one of the wrong options rather than an obviously silly answer. The other pattern worth knowing is that '
      'exponents ADD on multiplication and never move on addition — mixing those two up accounts for most of the '
      'rest. Suggest she write the −1 in front of the bracket explicitly rather than distributing it mentally.',
      ('Do the subtraction questions slowly and check the last term of every bracket.', 16),
      'content/alg-topic3-02.json',
      'enVision Algebra 2, Lesson 3-2 (Drive)',
      'enVision Algebra 2 Lesson 3-2: Adding, Subtracting, and Multiplying Polynomials')

print('sympy verified every expansion above.')
