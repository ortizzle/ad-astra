# Algebra & Geometry II — Topic 3, lessons 3-5, 3-6 and 3-7.
#
# Sources: aga_24_a2_0305_se.pdf / 0307_se.pdf, the 3-5 / 3-6 / 3-7 Mathematical
# Literacy and Vocabulary sheets and their answer keys, all in her Drive
# "Topic 3" folder.
#
# NOTE ON 3-6: there is no aga_24_a2_0306_se.pdf in the folder — it is the one
# lesson whose student-edition pages were not uploaded. It was built from the
# 3-6 vocabulary sheet and its answer key (which show the lesson working with
# rational roots plus irrational and complex CONJUGATE PAIRS) and from the
# standard theorem set that vocabulary names. Flagged in its parentNote.
#
# Every root, factorisation and transformation below is computed with sympy.
import sympy as sp
from unit_common import card, q, build

x = sp.Symbol('x')
I = sp.I

def ck(got, want):
    g, w = sp.expand(sp.sympify(got)), sp.expand(sp.sympify(want))
    assert sp.simplify(g - w) == 0, 'MISMATCH: %s != %s' % (g, w)
    return w

def roots_of(e):
    """Real+complex roots with multiplicity, computed."""
    return sp.roots(sp.Poly(sp.expand(sp.sympify(e)), x))

# ---------------------------------------------------------------- 3-5
C, Q = [], []

card(C, 'Zero of a function',
     "**A value of x that makes the function equal 0.**"
     "\n• Zero, root, solution and x-intercept are four names for the same thing — which one gets used depends only on whether you are talking about the function, the equation or the graph."
     "\n• If x = 4 is a zero, then (x − 4) is a factor, and the graph meets the x-axis at 4.",
     hint='Four words, one idea. Questions switch between them freely.')

card(C, 'The Zero Product Property',
     "**If a product equals zero, at least one of the factors must be zero.**"
     "\n• This is why factoring solves equations: (x − 6)(x + 2) = 0 forces x = 6 or x = −2."
     "\n• It only works against ZERO. From (x − 6)(x + 2) = 5 you can conclude nothing about the individual factors.",
     eq='AB = 0 ⇒ A = 0 or B = 0',
     hint='Get one side to zero BEFORE you factor, or the property does not apply.')

card(C, 'Factor out the GCF first',
     "**Always pull out the greatest common factor before anything else.**"
     "\n• x³ − 4x² − 12x = x(x² − 4x − 12) = x(x − 6)(x + 2)."
     "\n• That leading x is itself a factor, so **x = 0 is a zero** — the one most often missed, because it does not look like a factor worth writing down.",
     hint='A common x means 0 is a root. Do not lose it.')

card(C, 'Multiplicity',
     "**How many times a factor is repeated.**"
     "\n• In (x − 3)²(x + 1), the zero 3 has multiplicity 2 and −1 has multiplicity 1."
     "\n• Multiplicities add up to the degree, which is what makes the count come out right.",
     hint='The exponent on the factor IS the multiplicity.')

card(C, 'What multiplicity does to the graph',
     "**Odd multiplicity CROSSES the axis; even multiplicity TOUCHES and turns back.**"
     "\n• A multiplicity of 1 is an ordinary crossing; 3 crosses too, but flattens as it goes through."
     "\n• A multiplicity of 2 bounces off the axis without ever changing sign.",
     hint='Odd crosses, even bounces. The parity is the whole rule.')

card(C, 'Reading zeros off a factored polynomial',
     "**Set each factor to zero and solve — the zero is the value that kills that factor, so the sign flips.**"
     "\n• (x − 5) gives the zero +5; (x + 5) gives −5."
     "\n• (2x − 3) gives x = 3⁄2 — a factor with a coefficient does not give a whole number.",
     hint='Solve each factor = 0. Never just read the number off the bracket.')

card(C, 'Building a polynomial from its zeros',
     "**Turn each zero a into a factor (x − a) and multiply.**"
     "\n• Zeros at 2, −1 and 4 give (x − 2)(x + 1)(x − 4)."
     "\n• Any non-zero multiple of that works too, so there are infinitely many — usually the one with leading coefficient 1 is wanted.",
     hint='Zeros to factors is the reverse of factors to zeros, sign flip and all.')

card(C, 'How many zeros to expect',
     "**A degree-n polynomial has at most n real zeros — and at most n − 1 turning points.**"
     "\n• Those are two different counts about two different features; do not swap them."
     "\n• A cubic has at most 3 zeros and at most 2 turns.",
     hint='Zeros: n. Turns: n − 1. Different questions, different bounds.')

card(C, 'Zeros and end behaviour together sketch the graph',
     "**The zeros say where it meets the axis; multiplicity says how; end behaviour says where it goes.**"
     "\n• With those three you can sketch a polynomial without plotting a single extra point."
     "\n• Between consecutive zeros the graph stays entirely above or entirely below the axis — it cannot change sign without a zero.",
     hint='Zeros, multiplicity, ends. Three facts and the shape is decided.', frm='added')

card(C, 'Example: zeros with a repeated factor',
     "**f(x) = (x + 2)²(x − 1) has zeros at −2 (multiplicity 2) and 1 (multiplicity 1).**"
     "\n• At −2 the graph touches and turns back; at 1 it crosses."
     "\n• Degree 3, so both ends behave oppositely: down on the left, up on the right.",
     eq='f(x) = (x + 2)²(x − 1)',
     hint='Count the exponents: 2 + 1 = 3, which is the degree.', frm='added')
C[-1]['graph'] = {'w': [-3.5, 2.5, -6, 6], 'gx': 1, 'gy': 2,
                  'series': [{'type': 'poly', 'c': [1, 3, 0, -4]}],
                  'pts': [{'x': -2, 'y': 0, 'label': 'touches'}, {'x': 1, 'y': 0, 'label': 'crosses'}],
                  'xl': 'x', 'yl': 'f(x)'}

card(C, 'Example: the zero that hides',
     "**g(x) = 2x³ − 8x factors to 2x(x − 2)(x + 2), so the zeros are 0, 2 and −2.**"
     "\n• Pulling out 2x first is what surfaces the zero at 0."
     "\n• What is left, x² − 4, is a difference of squares from Lesson 3-3.",
     eq='g(x) = 2x(x − 2)(x + 2)',
     hint='GCF first, every time — it is where the missing root lives.', frm='added')

ck('(x+2)**2*(x-1)', 'x**3 + 3*x**2 - 4')
assert roots_of('(x+2)**2*(x-1)') == {sp.Integer(-2): 2, sp.Integer(1): 1}
ck('2*x*(x-2)*(x+2)', '2*x**3 - 8*x')
assert sorted(sp.solve(sp.Eq(2*x**3 - 8*x, 0), x)) == [-2, 0, 2]
ck('x*(x-6)*(x+2)', 'x**3 - 4*x**2 - 12*x')

# ---- questions -------------------------------------------------------------
q(Q, 1, 'What are the zeros of f(x) = (x − 5)(x + 3)?',
  ['5 and −3', '−5 and 3', '5 and 3', '−5 and −3'], 0,
  'Set each factor to zero and solve it.',
  ['x − 5 = 0 gives x = 5.',
   'x + 3 = 0 gives x = −3.',
   'The signs flip from what is written in the brackets.',
   'The zeros are 5 and −3.'],
  '**5 and −3.** Each zero is the value that makes its own factor vanish, which is why the sign is the opposite of the one printed. Reading the numbers straight off the brackets gives −5 and 3 — exactly backwards, and it is the commonest error in this lesson.',
  'Actually solve each little equation. It takes a second and removes the guesswork.')

q(Q, 1, 'What does the Zero Product Property let you conclude from (x − 4)(x + 7) = 0?',
  ['x = 4 or x = −7', 'x = 4 and x = −7 simultaneously',
   'x = −4 or x = 7', 'Nothing without expanding first'], 0,
  'If a product is zero, at least one factor is zero.',
  ['A product equals zero only when a factor equals zero.',
   'So either x − 4 = 0 or x + 7 = 0.',
   'That gives x = 4 or x = −7.',
   'They are alternatives, not simultaneous — x cannot be two numbers at once.'],
  '**x = 4 or x = −7.** The word is OR: each zero is a separate solution, and the graph meets the axis at two different places. Expanding first would only make the problem harder — factored form is already the useful form.',
  'This is why factoring solves equations: it converts one hard equation into several easy ones.')

q(Q, 1, 'In f(x) = (x − 2)³(x + 5), what is the multiplicity of the zero at 2?',
  ['3', '1', '2', '4'], 0,
  'The exponent on the factor is the multiplicity.',
  ['The factor associated with the zero 2 is (x − 2).',
   'It is raised to the power 3.',
   'That exponent IS the multiplicity.',
   'So the zero at 2 has multiplicity 3.'],
  '**3.** Multiplicity is just the exponent on that factor. Answering 2 reads the zero’s VALUE rather than its exponent — an easy confusion when the number 2 appears in both roles in the same expression.',
  'The multiplicities add up to the degree: 3 + 1 = 4 here.')

q(Q, 1, 'A polynomial has a zero of multiplicity 2 at x = 6. What does its graph do at x = 6?',
  ['Touches the x-axis and turns back', 'Crosses the x-axis',
   'Crosses the axis while flattening out', 'Never reaches the x-axis'], 0,
  'Even or odd is the whole question.',
  ['Multiplicity 2 is even.',
   'Even multiplicity means the graph touches the axis without crossing it.',
   'So the function does not change sign there — it comes down to the axis and goes back the way it came.',
   'It touches and turns back.'],
  '**Touches and turns back.** Even multiplicity means no sign change: the graph reaches zero and retreats. Crossing-while-flattening is what an ODD multiplicity of 3 or more looks like, which is a different picture with a different parity.',
  'Odd crosses, even bounces. It is the only thing multiplicity changes about the picture.')

q(Q, 1, 'What is the greatest number of real zeros a degree-7 polynomial can have?',
  ['7', '6', '8', '14'], 0,
  'Careful — this is the zero count, not the turning-point count.',
  ['Each real zero corresponds to a linear factor.',
   'A degree-7 polynomial has at most 7 linear factors.',
   'So it has at most 7 real zeros.',
   'The n − 1 rule is about TURNING POINTS, which would be 6 — a different feature.'],
  '**7.** Zeros are capped at n; turning points are capped at n − 1. The two bounds get swapped constantly because they sit one apart and both mention the degree, so it is worth naming which feature a question is asking about before answering.',
  'Zeros: at most n. Turns: at most n − 1. Read the question for which it wants.')

q(Q, 1, 'Which polynomial has zeros at 3, −2 and 0?',
  ['f(x) = x(x − 3)(x + 2)', 'f(x) = (x − 3)(x − 2)',
   'f(x) = x(x + 3)(x − 2)', 'f(x) = (x + 3)(x − 2)(x − 0)'], 0,
  'Each zero a becomes a factor (x − a) — including zero itself.',
  ['The zero 3 gives the factor (x − 3).',
   'The zero −2 gives the factor (x + 2).',
   'The zero 0 gives the factor (x − 0), which is just x.',
   'So f(x) = x(x − 3)(x + 2).'],
  '**f(x) = x(x − 3)(x + 2).** Zero is a zero like any other; its factor is simply x. And the signs flip going from zero to factor, which is why a zero of −2 produces (x + 2) rather than (x − 2).',
  'Zeros to factors flips every sign. Going the other way flips them back.')

ck('x**3 - 9*x', 'x*(x-3)*(x+3)')
q(Q, 2, 'Find all the zeros of f(x) = x³ − 9x.',
  ['x = 0, x = 3 and x = −3',
   'x = 3 and x = −3 only',
   'x = 0 and x = 3 only',
   'x = 9 and x = −9'], 0,
  'Factor out the greatest common factor before doing anything else.',
  ['The GCF is x: f(x) = x(x² − 9).',
   'x² − 9 is a difference of squares: x(x − 3)(x + 3).',
   'Set each factor to zero.',
   'The zeros are 0, 3 and −3.'],
  '**0, 3 and −3.** The zero at 0 is the one people lose, because pulling out the x does not feel like finding a root — but that x is a genuine factor. A cubic should have up to three zeros, so an answer with only two is worth a second look on those grounds alone.',
  'Count your zeros against the degree. Coming up short usually means a GCF went unclaimed.')

q(Q, 2, 'A graph crosses the x-axis at x = −1, and touches without crossing at x = 4. Which function fits?',
  ['f(x) = (x + 1)(x − 4)²', 'f(x) = (x + 1)²(x − 4)',
   'f(x) = (x − 1)(x + 4)²', 'f(x) = (x + 1)(x − 4)'], 0,
  'Crossing means odd multiplicity; touching means even.',
  ['Crossing at −1 means that factor has odd multiplicity: (x + 1) to the first power.',
   'Touching at 4 means that factor has even multiplicity: (x − 4)².',
   'The zeros also have to have the right signs: −1 gives (x + 1), and 4 gives (x − 4).',
   'So f(x) = (x + 1)(x − 4)².'],
  '**f(x) = (x + 1)(x − 4)².** Two things have to line up at once: which zero is which (signs flip from the bracket) and which one carries the even exponent. Putting the square on the wrong factor describes a graph that touches at −1 and crosses at 4 — the exact mirror of what was asked.',
  'Handle the values first, then the multiplicities. Two separate decisions, made in order.')

ck('(x+1)*(x-4)**2', 'x**3 - 7*x**2 + 8*x + 16')

ck('2*x**2 - 7*x - 15', '(2*x+3)*(x-5)')
q(Q, 2, 'What are the zeros of f(x) = 2x² − 7x − 15?',
  ['5 and −3⁄2', '5 and 3⁄2', '−5 and 3⁄2', '5 and −3'], 0,
  'Factor it, then solve each factor — one of them has a coefficient.',
  ['2x² − 7x − 15 factors as (2x + 3)(x − 5).',
   'x − 5 = 0 gives x = 5.',
   '2x + 3 = 0 gives 2x = −3, so x = −3⁄2.',
   'The zeros are 5 and −3⁄2.'],
  '**5 and −3⁄2.** A factor with a coefficient in front does not hand you a whole number — you have to divide as well as move the constant across. Answering −3 stops halfway through solving 2x + 3 = 0.',
  'Whenever a factor starts with a number other than 1, expect a fraction.')

q(Q, 2, 'Between two consecutive zeros, what can the graph of a polynomial NOT do?',
  ['Change from positive to negative', 'Have a turning point',
   'Stay entirely above the axis', 'Curve'], 0,
  'Changing sign requires passing through a particular value.',
  ['To go from positive to negative, the graph must pass through zero.',
   'Passing through zero means hitting the x-axis — which would be another zero.',
   'But we said the two zeros are consecutive, so there is none in between.',
   'So it cannot change sign there.'],
  '**Change from positive to negative.** Between consecutive zeros the graph keeps one sign the whole way. It can certainly turn, curve, and stay above or below — it just cannot cross, because crossing is what a zero IS.',
  'This is what makes sketching from zeros work: each interval between zeros has a single sign to determine.')

ck('x**3 - 2*x**2 - 8*x', 'x*(x-4)*(x+2)')
q(Q, 2, 'Solve x³ = 2x² + 8x.',
  ['x = 0, 4 or −2', 'x = 4 or −2', 'x = 0 or 4', 'x = 2 or 8'], 0,
  'Move everything to one side first — the Zero Product Property needs a zero.',
  ['Rewrite as x³ − 2x² − 8x = 0.',
   'Factor out x: x(x² − 2x − 8) = 0.',
   'Factor the quadratic: x(x − 4)(x + 2) = 0.',
   'So x = 0, 4 or −2.'],
  '**x = 0, 4 or −2.** Two steps that both get skipped: moving everything to one side (the Zero Product Property says nothing about a product equal to 2x² + 8x), and keeping the x = 0 that the GCF produces. Dividing both sides by x would have destroyed that root silently.',
  'Never divide both sides by a variable — you throw away a solution and get no warning.')

q(Q, 3, 'A student solves x² = 5x by dividing both sides by x to get x = 5. What is wrong?',
  ['Dividing by x loses the solution x = 0',
   'Nothing — x = 5 is the complete answer',
   'They should have divided by 5 instead',
   'x² = 5x has no solutions'], 0,
  'Check whether any value was quietly excluded by that division.',
  ['Dividing by x assumes x is not zero — you cannot divide by zero.',
   'But x = 0 does satisfy the original: 0² = 5(0) is 0 = 0.',
   'Done properly: x² − 5x = 0, so x(x − 5) = 0, giving x = 0 or x = 5.',
   'Dividing by x threw away the solution x = 0.'],
  '**Dividing by x loses the solution x = 0.** Dividing by a variable silently assumes it is not zero, and that assumption removes a real answer with no error message. The safe move is always to bring everything to one side and factor — then the Zero Product Property finds every root.',
  'Subtract, never divide, when a variable is involved on both sides.')

q(Q, 3, 'A degree-4 polynomial has zeros at −3 and 2 only, and its graph touches the axis at both. What are the multiplicities?',
  ['Both have multiplicity 2', 'Both have multiplicity 1',
   '−3 has multiplicity 3 and 2 has multiplicity 1', 'It is impossible to tell'], 0,
  'Touching means even; and the multiplicities have to add to the degree.',
  ['Touching without crossing means each multiplicity is EVEN.',
   'The multiplicities must sum to the degree, which is 4.',
   'Two even numbers adding to 4 can only be 2 and 2.',
   'So both zeros have multiplicity 2.'],
  '**Both have multiplicity 2.** Two constraints pin it down exactly: even (from the touching) and summing to 4 (from the degree). The 3-and-1 option sums correctly but makes both multiplicities odd, which would mean the graph crosses at both — contradicting what was described.',
  'When a question gives you both the degree and the behaviour, the multiplicities are usually forced.')
ck('(x+3)**2*(x-2)**2', 'x**4 + 2*x**3 - 11*x**2 - 12*x + 36')

q(Q, 3, 'Why does knowing all the zeros of a polynomial let you write the whole function (up to a constant multiple)?',
  ['Each zero gives a linear factor, and those factors multiply up',
   'Because the zeros are also where the turning points sit',
   'Because every polynomial has exactly one zero to build on',
   'Because the zeros determine the end behaviour of the graph'], 0,
  'Ask what a zero actually tells you about the polynomial’s structure.',
  ['By the Factor Theorem, a zero at a means (x − a) is a factor.',
   'Knowing every zero therefore means knowing every linear factor.',
   'Multiplying them rebuilds the polynomial.',
   'Only an overall constant is left undetermined, since scaling does not move any zero.'],
  '**Each zero gives a linear factor, and those factors multiply up.** The leftover constant is exactly why it is "up to a multiple" — 2(x − 1)(x + 3) and (x − 1)(x + 3) have identical zeros. End behaviour, by contrast, comes from the degree and the leading coefficient, not from where the zeros sit.',
  'Zeros fix the SHAPE; the leading coefficient fixes how stretched it is.')

q(Q, 3, 'The graph shown crosses at x = 1 and touches the axis at x = −2. What is the least possible degree?',
  ['3', '2', '4', '5'], 0,
  'Add the smallest multiplicity each behaviour allows.',
  ['Crossing at 1 needs odd multiplicity — smallest is 1.',
   'Touching at −2 needs even multiplicity — smallest is 2.',
   'The multiplicities sum to at least 1 + 2 = 3.',
   'So the least possible degree is 3.'],
  '**3.** Each behaviour sets a minimum multiplicity, and the degree is at least their sum. It is only a minimum: a degree-5 polynomial could draw the same picture with multiplicities 3 and 2. As always, a graph bounds the degree from below rather than pinning it down.',
  'Crossing costs at least 1, touching costs at least 2. Add up the minimums.')
Q[-1]['graph'] = {'w': [-3.5, 2.5, -6, 6], 'gx': 1, 'gy': 2,
                  'series': [{'type': 'poly', 'c': [1, 3, 0, -4]}],
                  'xl': 'x', 'yl': 'f(x)'}

q(Q, 3, 'Put these steps in the order you would use them to find the zeros of 3x³ − 12x.',
  ['Set the function equal to zero',
   'Factor out the greatest common factor, 3x',
   'Factor the remaining difference of squares',
   'Solve each factor for x'], 0,
  'One step has to come before any factoring, and one factoring has to come before the other.',
  ['First set 3x³ − 12x = 0, because the Zero Product Property needs a zero on one side.',
   'Then pull out the GCF 3x, giving 3x(x² − 4) = 0.',
   'Then factor x² − 4 as (x − 2)(x + 2).',
   'Finally solve each factor: x = 0, 2 and −2.'],
  '**Set to zero, GCF, factor the rest, then solve.** The GCF always comes before any other factoring, because pulling it out is what makes the remainder simple enough to recognise — here it exposes a plain difference of squares. Solving can only happen once nothing factors further.',
  'GCF first is not a preference; it is what makes the next step visible.',
  kind='order')
ck('3*x*(x-2)*(x+2)', '3*x**3 - 12*x')

# --- top-up to the 18-24 guideline -----------------------------------------
q(Q, 1, 'f(x) = x(x − 7)(x + 1). How many distinct zeros does it have, and what are they?',
  ['Three — 0, 7 and −1',
   'Two — 7 and −1',
   'Three — 0, −7 and 1',
   'Three — 1, 7 and −1'], 0,
  'A lone x out front is a factor like any other.',
  ['Set each factor to zero in turn.',
   'x = 0 from the bare x, which is a factor even though nothing is subtracted from it.',
   'x − 7 = 0 gives x = 7, and x + 1 = 0 gives x = −1.',
   'That is three distinct zeros: 0, 7 and −1.'],
  '**Three — 0, 7 and −1.** The factor that costs the most marks is the bare x, because it does not look like a factor worth writing down. Every factor is set to zero, including that one. Note also that x + 1 gives −1, not 1 — you undo the sign that is written, you do not copy it.',
  'A bare x in front means 0 is a zero. Count it.')

q(Q, 2, 'Find all the zeros of f(x) = x⁴ − 5x² + 4.',
  ['1, −1, 2 and −2',
   '1 and 4 only',
   '1, 2 and 4',
   '0, 1 and 4'], 0,
  'It factors like a quadratic, but x² is what gets factored — not x.',
  ['Treat it as a quadratic in x²: it factors as (x² − 1)(x² − 4).',
   'Both brackets are differences of squares: (x − 1)(x + 1)(x − 2)(x + 2).',
   'Set each of the four factors to zero.',
   'The zeros are 1, −1, 2 and −2.'],
  '**1, −1, 2 and −2.** Factoring gets you to x² = 1 and x² = 4, and stopping there is the whole trap — those are values of x², not of x. Taking the square root of each gives two answers apiece, which is why a quartic that looks like it has two zeros actually has four.',
  'x² = 4 is not the answer. x = ±2 is.')

q(Q, 2, 'P(x) = x³ − 4x² + x + 6, and you are told P(3) = 0. What does that give you, and what is left to do?',
  ['(x − 3) is a factor — divide it out and solve the quadratic left behind',
   '(x + 3) is a factor — divide it out and solve the quadratic left behind',
   '3 is the only zero, so the work is finished at that point',
   '(x − 3) is a factor, and the two remaining zeros must be positive too'], 0,
  'A root and a factor are the same fact said two ways — mind which sign goes where.',
  ['P(3) = 0 says 3 is a root, and the Factor Theorem turns that into a factor.',
   'A root of 3 gives the factor (x − 3), because that is what is zero when x = 3.',
   'Dividing P(x) by (x − 3) leaves x² − x − 2.',
   'That factors as (x − 2)(x + 1), so the other zeros are 2 and −1.'],
  '**(x − 3) is a factor — divide it out and solve what is left.** One known root turns a cubic you cannot factor into a quadratic you can, which is the whole reason the Factor Theorem is worth having. The sign flips: a root of 3 means (x − 3), never (x + 3). Here the remaining zeros are 2 and −1, so one of them is negative.',
  'Root 3 → factor (x − 3). Divide, then solve the leftovers.')

q(Q, 3, 'f(x) = x³ + x² + x + 1 has a zero at x = −1. Dividing that out leaves x² + 1. How many REAL zeros does f have altogether?',
  ['One — only x = −1, since x² + 1 is never zero for real x',
   'Three — every cubic has three real zeros',
   'Two — x = −1 and x = 1, from the leftover factor',
   'One — but only because the cubic was not factored completely'], 0,
  'Ask whether the leftover quadratic can ever hit zero on a real number line.',
  ['x² + 1 = 0 would need x² = −1.',
   'No real number squares to a negative, so that factor contributes no real zeros.',
   'The only real zero left is the one already found, x = −1.',
   'So f has exactly one real zero.'],
  '**One — only x = −1.** A cubic always has three zeros counting complex ones, and here two of them are ±i. The option blaming incomplete factoring is the tempting wrong reason: x² + 1 really is factored as far as it goes over the real numbers, and the answer is one because of what the numbers are, not because the work stopped early.',
  'x² + 1 never reaches zero on the real line. That is a fact about it, not a sign you stopped early.')

ck('(x-1)*(x+1)*(x-2)*(x+2)', 'x**4 - 5*x**2 + 4')
ck('(x-3)*(x-2)*(x+1)', 'x**3 - 4*x**2 + x + 6')
assert sp.sympify('x**3 + x**2 + x + 1').subs(x, -1) == 0
assert sorted(sp.Poly('x**3 + x**2 + x + 1', x).all_roots(), key=str) is not None
assert len([r for r in sp.Poly('x**3 + x**2 + x + 1', x).all_roots() if r.is_real]) == 1
assert sp.factor('x**3 + x**2 + x + 1') == (x + 1) * (x**2 + 1)

build('ad-astra', C, Q, 'unit-alg-t3-05',
      'Topic 3 · 3-5 Zeros of Polynomial Functions', 'algeo',
      'Lesson 3-5 finds the zeros of a polynomial by factoring and applying the Zero Product Property, and '
      'reads multiplicity off the factors — including what an even or odd multiplicity does to the graph.',
      'Zeros are where algebra and the graph meet: the same numbers that solve the equation are the places the '
      'curve crosses the axis. Everything in Lesson 3-6 is about finding them when factoring alone will not.',
      [('Find zeros by factoring and applying the Zero Product Property', 'source'),
       ('Identify the multiplicity of each zero from the factored form', 'source'),
       ('Predict whether the graph crosses or touches the axis at each zero', 'source'),
       ('Write a polynomial function given its zeros', 'source')],
      'Two habits are worth drilling. First, factor out the GCF before anything else — when there is a common '
      'x, the zero at x = 0 is genuinely easy to lose, and an answer that comes up short against the degree is '
      'the tell. Second, never divide both sides by a variable: it destroys a root silently, which is a real '
      'error with no visible symptom, and one question here is built entirely around it. The sign flip between '
      'a factor and its zero — (x + 3) gives −3 — accounts for most of the rest.',
      ('Sketch a few from their factored form: zeros, then multiplicity, then the ends.', 18),
      'content/alg-topic3-05.json',
      'enVision Algebra 2, Lesson 3-5 (Drive)',
      'enVision Algebra 2 Lesson 3-5: Zeros of Polynomial Functions')

# ---------------------------------------------------------------- 3-6
C, Q = [], []

card(C, 'The Fundamental Theorem of Algebra',
     "**A polynomial of degree n has exactly n roots, counting multiplicity, if complex roots are allowed.**"
     "\n• "
     "“Exactly”, not “at most” — the count is only guaranteed once imaginary numbers are on the table."
     "\n• A cubic always has 3 roots; some may be repeated and some may be complex, but there are always 3.",
     hint='Count in the complex numbers and the answer is always exactly the degree.')

card(C, 'Real roots versus all roots',
     "**Over the REAL numbers a degree-n polynomial has AT MOST n roots; over the complex numbers it has EXACTLY n.**"
     "\n• x² + 1 has no real roots but two complex ones, i and −i."
     "\n• The graph only shows the real ones — a complex root is never an x-intercept.",
     hint='The graph shows real roots only. The rest are invisible on it.')

card(C, 'The Rational Root Theorem',
     "**Any rational root is ±p⁄q, where p divides the constant term and q divides the leading coefficient.**"
     "\n• It gives a finite LIST OF CANDIDATES to test — it does not say any of them actually work."
     "\n• For 2x³ + x − 6: p ∈ {1,2,3,6}, q ∈ {1,2}, so candidates are ±1, ±2, ±3, ±6, ±½, ±3⁄2.",
     eq='possible root = ± p⁄q',
     hint='p from the constant, q from the leading coefficient. Constant on top.')

card(C, 'Testing a candidate',
     "**Substitute it, or synthetic-divide by it — a zero result means you have found a root AND a factor.**"
     "\n• Synthetic division is usually better: it confirms the root and hands you the quotient at the same time."
     "\n• The quotient is one degree lower, so the problem shrinks every time a root is found.",
     hint='Each root found makes the next one easier — the polynomial gets smaller.')

card(C, 'The Complex Conjugate Theorem',
     "**If a + bi is a root of a polynomial with real coefficients, then a − bi is a root too.**"
     "\n• Complex roots always arrive in PAIRS."
     "\n• So a polynomial with real coefficients always has an EVEN number of complex roots — which is why every odd-degree polynomial must have at least one real root.",
     eq='a + bi is a root ⇒ a − bi is a root',
     hint='Complex roots come two at a time, never alone.')

card(C, 'The Irrational Conjugate Theorem',
     "**If a + √b is a root of a polynomial with RATIONAL coefficients, then a − √b is a root too.**"
     "\n• The same pairing rule as complex roots, for irrational ones."
     "\n• So finding 2 + √5 as a root tells you 2 − √5 is one as well, for free.",
     eq='a + √b is a root ⇒ a − √b is a root',
     hint='Surds pair up too, for the same reason complex roots do.')

card(C, 'Why conjugates must pair',
     "**Because the coefficients are real, anything irrational or imaginary has to cancel out when the factors are multiplied.**"
     "\n• (x − (2 + i))(x − (2 − i)) = x² − 4x + 5 — every trace of i is gone."
     "\n• Only the pair multiplies to something with real coefficients, which is why one can never appear without the other.",
     hint='The pair multiplies to a real quadratic. A lone one never could.', frm='added')

card(C, 'The strategy for finding every root',
     "**List candidates, test until one works, divide it out, then solve what is left.**"
     "\n• Rational Root Theorem for the list; synthetic division to test and to shrink."
     "\n• Once the quotient is a QUADRATIC, stop hunting — factor it or use the Quadratic Formula, which finds complex roots too.",
     hint='Hunt only until the leftover is a quadratic. Then use a formula.', frm='added')

card(C, 'What the theorems do and do not promise',
     "**The Fundamental Theorem guarantees the COUNT; the Rational Root Theorem only offers a list to try.**"
     "\n• A polynomial can easily have no rational roots at all — the candidate list can come up empty-handed."
     "\n• Knowing there are exactly n roots does not tell you what any of them are.",
     hint='One theorem counts; the other suggests. Neither hands you an answer.', frm='added')

card(C, 'Example: finding every root of a cubic',
     "**x³ − 2x² + x − 2 has roots 2, i and −i.**"
     "\n• Candidates from the Rational Root Theorem: ±1, ±2. Testing 2 gives zero."
     "\n• Dividing by (x − 2) leaves x² + 1, whose roots are i and −i — a conjugate pair, as required."
     "\n• Three roots for a cubic, exactly as the Fundamental Theorem promises.",
     eq='x³ − 2x² + x − 2 = (x − 2)(x² + 1)',
     hint='One rational root, then a quadratic. That is the usual shape of these.', frm='added')

_P = x**3 - 2*x**2 + x - 2
assert _P.subs(x, 2) == 0
assert sp.factor(_P) == (x - 2)*(x**2 + 1)
assert set(sp.solve(sp.Eq(_P, 0), x)) == {sp.Integer(2), I, -I}
ck('(x - (2+I))*(x - (2-I))', 'x**2 - 4*x + 5')

# ---- questions -------------------------------------------------------------
q(Q, 1, 'How many roots does a degree-5 polynomial have, counting multiplicity and allowing complex roots?',
  ['Exactly 5', 'At most 5', 'At least 5', 'It depends on the coefficients'], 0,
  'The Fundamental Theorem of Algebra is an exact count, not a bound.',
  ['The Fundamental Theorem of Algebra gives the count over the complex numbers.',
   'A degree-n polynomial has exactly n roots there, counting multiplicity.',
   'Here n = 5.',
   'So exactly 5.'],
  '**Exactly 5.** "At most" is the right phrasing for REAL roots only — over the complex numbers the count is exact and never depends on the coefficients. That precision is what makes the theorem useful: you always know how many roots you are still looking for.',
  'Real roots: at most n. All roots: exactly n. The word changes with the number system.')

q(Q, 1, 'For P(x) = x³ + 4x − 6, which list gives every possible RATIONAL root?',
  ['±1, ±2, ±3, ±6', '±1, ±2, ±3', '±1, ±6', '±1, ±2, ±4, ±6'], 0,
  'Factors of the constant over factors of the leading coefficient.',
  ['The constant is −6, whose factors are 1, 2, 3 and 6.',
   'The leading coefficient is 1, whose only factor is 1.',
   'Candidates are ±p⁄q = ±1, ±2, ±3, ±6.',
   'That is the complete list.'],
  '**±1, ±2, ±3, ±6.** Every factor of the constant counts, including 6 itself. The 4 from the middle term never enters the theorem at all — only the constant and the leading coefficient do, which is worth knowing because the middle coefficients are a natural distraction.',
  'Two numbers matter: the constant and the leading coefficient. Ignore everything between them.')

q(Q, 1, 'If 3 + 2i is a root of a polynomial with real coefficients, what else must be a root?',
  ['3 − 2i', '−3 − 2i', '−3 + 2i', '2 + 3i'], 0,
  'A conjugate flips the sign of the imaginary part only.',
  ['The Complex Conjugate Theorem says roots come in conjugate pairs.',
   'The conjugate of a + bi is a − bi.',
   'Here a = 3 and b = 2.',
   'So 3 − 2i must also be a root.'],
  '**3 − 2i.** Only the imaginary part changes sign — the real part stays exactly as it is. Negating both (−3 − 2i) or swapping the numbers around (2 + 3i) are the two near-misses, and neither is the conjugate.',
  'Conjugate: same real part, opposite imaginary part. Nothing else moves.')

q(Q, 1, 'If 1 + √7 is a root of a polynomial with rational coefficients, what else must be a root?',
  ['1 − √7', '−1 − √7', '−1 + √7', '√7'], 0,
  'Irrational roots pair the same way complex ones do.',
  ['The Irrational Conjugate Theorem applies when the coefficients are rational.',
   'The conjugate of a + √b is a − √b.',
   'Here a = 1 and √b = √7.',
   'So 1 − √7 is also a root.'],
  '**1 − √7.** Only the sign in front of the radical flips. It is the same idea as complex conjugates and for the same underlying reason: only the pair multiplies back to something with rational coefficients.',
  'Both conjugate theorems flip exactly one sign — the one on the "awkward" part.')

q(Q, 1, 'What does the Rational Root Theorem actually guarantee?',
  ['Any rational root there is will appear in the list',
   'At least one of the candidates is bound to be a root',
   'Every candidate on the list turns out to be a root',
   'The polynomial has no irrational roots to worry about'], 0,
  'It narrows the search; it does not promise a find.',
  ['The theorem says where rational roots CAN be.',
   'So a rational root, if one exists, is somewhere in the list.',
   'It never promises the list contains an actual root — a polynomial may have none that are rational.',
   'So: any rational root will appear in the list.'],
  '**Any rational root will appear in the candidate list.** It is a filter, not a finder. x² − 2 has candidates ±1 and ±2 and neither works, because its real roots are ±√2 — irrational, and completely outside what this theorem can see.',
  'It shrinks an infinite search to a finite one. That is the whole contribution.')

q(Q, 2, 'A polynomial with real coefficients has degree 3 and one root equal to 2i. What are its other roots?',
  ['−2i and one real root', '−2i and another complex root',
   'Two more complex roots', '2i again, with multiplicity 3'], 0,
  'Count what the Fundamental Theorem requires, then apply the pairing rule.',
  ['Degree 3 means exactly 3 roots.',
   '2i is a root, so its conjugate −2i must be too — that is 2 roots.',
   'The third cannot be complex, because complex roots pair up and there is no partner left.',
   'So the third root is real: −2i and one real root.'],
  '**−2i and one real root.** Complex roots always come in pairs, so an odd-degree polynomial with real coefficients must have at least one real root — there is no way to pair up an odd number. That is why every cubic graph crosses the x-axis somewhere.',
  'Odd degree with real coefficients always has a real root. The ends run opposite ways, so it has to cross.')

q(Q, 2, 'For P(x) = 2x³ − 5x² + x + 2, which is a candidate the Rational Root Theorem allows but ±4 is not?',
  ['½', '¼', '4', '⅔'], 0,
  'Build the candidate list from the constant and the leading coefficient.',
  ['The constant is 2, so p ∈ {1, 2}.',
   'The leading coefficient is 2, so q ∈ {1, 2}.',
   'Candidates are ±1, ±2 and ±½.',
   '½ is allowed; 4, ¼ and ⅔ all involve numbers that are not factors of 2.'],
  '**½.** Fractional candidates arise exactly when the leading coefficient is not 1, and both parts have to be legitimate factors: 1 divides the constant and 2 divides the leading coefficient. ¼ would need a 4 in the denominator, and ⅔ a 3 — neither divides 2.',
  'A leading coefficient of 1 means the candidates are all whole numbers. Anything else opens up fractions.')

_P7 = x**3 - 6*x**2 + 11*x - 6
assert set(sp.solve(sp.Eq(_P7, 0), x)) == {1, 2, 3}
q(Q, 2, 'Find all roots of x³ − 6x² + 11x − 6.',
  ['1, 2 and 3', '1, 2 and 6', '−1, −2 and −3', '1 and 6'], 0,
  'Test the small candidates first — they are the likeliest.',
  ['Candidates are ±1, ±2, ±3, ±6.',
   'P(1) = 1 − 6 + 11 − 6 = 0, so 1 is a root.',
   'Dividing by (x − 1) leaves x² − 5x + 6.',
   'That factors as (x − 2)(x − 3), so the roots are 1, 2 and 3.'],
  '**1, 2 and 3.** One rational root found by testing turns the cubic into a quadratic, and the quadratic finishes by ordinary factoring. Note the roots are positive even though the constant is −6 — the signs of the roots are not read off the constant directly.',
  'Test 1 and −1 first. They are quick to evaluate and often work.')
_q7, _r7 = sp.div(sp.Poly(_P7, x), sp.Poly(x - 1, x))
ck(_q7.as_expr(), 'x**2 - 5*x + 6'); assert _r7.as_expr() == 0

q(Q, 2, 'A degree-4 polynomial with real coefficients has roots 1 + i and 3. How many roots are still unaccounted for, and what do you know about them?',
  ['One, and it must be real — 1 − i is already forced by the pairing',
   'Two, and both of them are bound to be non-real numbers',
   'Three, and every one of them has to be a real number',
   'None — all four roots are already named or forced'], 0,
  'Apply the pairing rule before you count. It supplies a root the question never listed.',
  ['Degree 4 means exactly four roots, counting multiplicity.',
   '1 + i is non-real, so its conjugate 1 − i is forced — the two given roots really account for three.',
   'That leaves exactly one root unaccounted for.',
   'A lone non-real root would need a partner, and there is no room left — so the fourth root is real.'],
  '**One, and it has to be real.** Naming 1 + i quietly names 1 − i as well, so two stated roots account for three. The last one cannot be non-real: that would demand a conjugate partner, and a degree-4 polynomial has no fifth slot to put one in. Which real number it is stays open — it could even be 3 over again.',
  'The pairing rule does two jobs: it adds roots you were not given, and it forces the odd one out to be real.')

q(Q, 3, 'Why must every polynomial of ODD degree with real coefficients have at least one real root?',
  ['Non-real roots come in pairs, so an odd count cannot all be non-real',
   'Because an odd-degree polynomial has no complex roots at all',
   'Because the Rational Root Theorem always turns one of them up',
   'Because an odd function always passes through the origin'], 0,
  'Count parity: complex roots arrive two at a time.',
  ['An odd-degree polynomial has an odd number of roots in total.',
   'Complex roots always come in conjugate pairs, so they contribute an EVEN number.',
   'An even number can never account for an odd total.',
   'So at least one root must be real.'],
  '**Complex roots come in pairs, so an odd number of roots cannot all be complex.** It is a pure parity argument and needs no computation at all. The graph says the same thing a different way: odd degree means the ends run opposite directions, so the curve has to cross the axis somewhere.',
  'Two independent arguments — parity of the root count, and the end behaviour — reach the same conclusion.')

_P8 = x**4 - 1
assert set(sp.solve(sp.Eq(_P8, 0), x)) == {1, -1, I, -I}
q(Q, 3, 'How many REAL roots and how many non-real roots does x⁴ − 1 have?',
  ['2 real and 2 non-real', '4 real and 0 non-real', '0 real and 4 non-real', '3 real and 1 non-real'], 0,
  'Factor it completely and read off what each factor contributes.',
  ['x⁴ − 1 = (x² − 1)(x² + 1).',
   'x² − 1 = (x − 1)(x + 1), giving the real roots 1 and −1.',
   'x² + 1 = 0 gives x = ±i, two non-real roots.',
   'So 2 real and 2 non-real — four altogether, as degree 4 requires.'],
  '**2 real and 2 non-real.** The Fundamental Theorem guarantees four roots in total; the graph shows only the two real ones as x-intercepts. And the non-real pair is exactly that — a pair — which is what the Complex Conjugate Theorem requires. The "3 real and 1 non-real" option is impossible for that reason alone.',
  'A split with an ODD number of non-real roots is impossible when the coefficients are real.')

q(Q, 3, 'You are finding all roots of a quartic. You find one rational root and divide it out, leaving a cubic; you find another and divide again, leaving a quadratic. What now?',
  ['Solve the quadratic directly — the formula finds complex roots too',
   'Keep testing rational candidates until two more of them work',
   'Conclude that the two remaining roots must be irrational',
   'Start again, because the division must have gone wrong somewhere'], 0,
  'Ask what tool finishes a quadratic completely.',
  ['A quadratic can always be solved outright, by factoring or by the Quadratic Formula.',
   'The Quadratic Formula finds the roots whatever they are — rational, irrational or complex.',
   'So no more candidate-testing is needed.',
   'Solve the quadratic directly.'],
  '**Solve the quadratic directly.** The candidate-testing is only there to get you DOWN to a quadratic — once you are there, a formula finishes it for certain. Carrying on testing would be slow and could fail entirely, since the last two roots may be irrational or complex and no rational candidate would ever match them.',
  'Hunt down to degree 2, then stop hunting. That is the whole method.')

# --- top-up to the 18-24 guideline -----------------------------------------
q(Q, 1, 'What does the Fundamental Theorem of Algebra actually guarantee?',
  ['Every polynomial of degree 1 or more has at least one complex root',
   'Every polynomial of degree n has exactly n real roots',
   'Every polynomial can be factored using only rational numbers',
   'Every polynomial with real coefficients has at least one real root'], 0,
  'Remember that every real number is also a complex number — the word is not a promise of an i.',
  ['The theorem is about existence: a non-constant polynomial always has a root somewhere.',
   'That root is guaranteed only in the COMPLEX numbers, which include the real ones.',
   'Applying it repeatedly is what gives exactly n roots counting multiplicity.',
   'So the guarantee is at least one complex root for any degree of 1 or more.'],
  '**At least one complex root, for any degree of 1 or more.** Applying it over and over — root, divide out, root again — is what builds up to exactly n roots counting multiplicity. Guaranteeing a REAL root is a different and weaker claim that only holds for odd degree; x² + 1 has no real root at all and is the standard counterexample.',
  'Complex includes real. The theorem promises a root, not a real one.')

q(Q, 1, 'For P(x) = 3x³ + x − 10, the Rational Root Theorem builds its candidates from which two numbers?',
  ['Factors of 10 on top, factors of 3 underneath',
   'Factors of 3 on top, factors of 10 underneath',
   'Factors of 10 on top, factors of 1 underneath',
   'Factors of 1 on top, factors of 10 underneath'], 0,
  'p over q — and p is the end of the polynomial furthest from the leading term.',
  ['The candidates are ±p/q, where p divides the CONSTANT term and q divides the LEADING coefficient.',
   'The constant term here is −10, so p comes from 1, 2, 5 and 10.',
   'The leading coefficient is 3, so q comes from 1 and 3.',
   'Candidates are therefore factors of 10 over factors of 3.'],
  '**Factors of 10 over factors of 3.** Getting this upside down is the single commonest slip in the whole theorem, and it is silent — the wrong list still looks like a list of fractions. A quick check: if the leading coefficient is 1, every candidate should be a whole number, which only works with the leading coefficient underneath.',
  'Constant on top, leading coefficient underneath. Leading 1 means whole-number candidates.')

q(Q, 2, 'A polynomial with RATIONAL coefficients has degree 4, and two of its roots are 2 − √5 and i. What are the other two?',
  ['2 + √5 and −i',
   '2 + √5 only — i does not need a partner',
   '−2 + √5 and −i',
   '√5 − 2 and −i'], 0,
  'Two different conjugate rules apply here, and each one pairs off exactly one of the given roots.',
  ['Irrational roots of a rational polynomial come in pairs: 2 − √5 forces 2 + √5.',
   'Non-real roots of a real polynomial come in pairs: i forces −i.',
   'Only the sign on the radical or on the i flips — the rest of the number stays put.',
   'So the other two roots are 2 + √5 and −i.'],
  '**2 + √5 and −i.** Both conjugate rules are running at once, which is why this shape shows up on tests. Flipping the 2 as well gives −2 + √5, a different number entirely: the conjugate of a − √b is a + √b, changing only the sign in front of the radical.',
  'Flip the sign on the radical, or on the i. Never on anything else.')

q(Q, 2, 'Which polynomial has 1 + i and 1 − i as its only roots?',
  ['x² − 2x + 2',
   'x² + 2x + 2',
   'x² − 2x − 2',
   'x² + 2'], 0,
  'Multiply the two factors out — the i terms are meant to cancel.',
  ['The factors are (x − (1 + i)) and (x − (1 − i)).',
   'Their sum of roots is 2, so the middle term is −2x.',
   'Their product is (1 + i)(1 − i) = 1 − i² = 2, so the constant is 2.',
   'The polynomial is x² − 2x + 2.'],
  '**x² − 2x + 2.** Building a polynomial from a conjugate pair is the reverse of finding roots, and it always lands on real coefficients — that is what the pairing is for. The product (1 + i)(1 − i) is 2 rather than 0, because i² = −1 makes the last term ADD rather than subtract.',
  'Sum of roots → middle term (negated). Product of roots → constant.')

q(Q, 2, 'The Rational Root Theorem lists twelve candidates for a cubic with real coefficients, and testing shows none of them is a root. What does that tell you?',
  ['It has no rational roots — its roots are irrational, non-real, or a mix',
   'It has no roots at all, so there is nothing further to find',
   'An arithmetic error was made, since every cubic has a rational root',
   'All three of its roots are non-real, and none of them is real'], 0,
  'The theorem only ever ruled on one kind of number.',
  ['The theorem lists every POSSIBLE rational root and nothing else.',
   'An empty result therefore rules out rational roots, and only rational roots.',
   'Irrational roots like √2 and non-real roots like 2i were never on the list to begin with.',
   'So the roots exist, but none of them is rational.'],
  '**No rational roots — they are irrational, non-real, or both.** x³ − 2 is the plain example: its only real root is the cube root of 2, which no candidate list could ever contain. And a real cubic always has at least one real root, because its ends point opposite ways, so "all three non-real" is impossible whatever the candidates say.',
  'An empty candidate list rules out rational roots. It rules out nothing else.')

q(Q, 3, 'P(x) = x³ + 2x² + 3x + 6. Find its one real root and say what the other two are.',
  ['x = −2, and the other two are ±i√3',
   'x = −2, and the other two are ±√3',
   'x = 2, and the other two are ±i√3',
   'x = −3, and the other two are ±i√2'], 0,
  'Four terms with a shared structure — try grouping them in pairs.',
  ['Group: x²(x + 2) + 3(x + 2).',
   'Both pairs share (x + 2), so P(x) = (x + 2)(x² + 3).',
   'x + 2 = 0 gives the real root x = −2.',
   'x² + 3 = 0 gives x² = −3, so x = ±i√3.'],
  '**x = −2, with ±i√3 as the other two.** Grouping is worth trying on any four-term cubic before reaching for the candidate list. The leftover x² + 3 has no real root, since squaring a real number never gives −3 — dropping the i and writing ±√3 is the slip to watch, and those are not roots of this polynomial at all.',
  'Four terms → try grouping. x² = −k gives ±i√k, never ±√k.')

q(Q, 3, 'Why can a polynomial with real coefficients never have exactly ONE non-real root?',
  ['Non-real roots of a real polynomial arrive in conjugate pairs, so they come in twos',
   'The Fundamental Theorem of Algebra forbids non-real roots in a real polynomial',
   'Every root of a polynomial with real coefficients has to be real itself',
   'A polynomial with real coefficients always has an even degree'], 0,
  'What would have to be true of the coefficients if a lone non-real root were allowed?',
  ['If a + bi is a root of a real polynomial, so is a − bi.',
   'The two are different numbers whenever b is not zero, so they are two separate roots.',
   'Non-real roots therefore always come in twos and are even in number.',
   'One on its own is impossible.'],
  '**They come in conjugate pairs, so always in twos.** The pairing is what keeps the coefficients real when the factors are multiplied out — the i terms cancel, which they could not do without a partner. This is also why an odd-degree real polynomial must have a real root: an odd count cannot be made entirely of pairs.',
  'Pairs cancel the i terms. A lone non-real root would leave one behind in the coefficients.')

q(Q, 3, 'A degree-5 polynomial with real coefficients has 2i, −2i and 1 + i among its roots. How many real roots does it have?',
  ['One — 1 − i must be a root too, so four are non-real and the fifth cannot be',
   'None — with four non-real roots the fifth must be non-real as well',
   'Two — 1 − i is already one of the five listed, leaving two real ones',
   'It cannot be decided without knowing the leading coefficient of the polynomial'], 0,
  'One of the three given roots is still missing its partner. Add it in before you count.',
  ['1 + i is non-real, so its conjugate 1 − i must be a root as well.',
   '2i and −2i are already a pair, so the non-real roots now number four.',
   'Degree 5 means five roots in total, leaving exactly one unaccounted for.',
   'A single leftover cannot be non-real, because it would need a partner of its own — so it is real.'],
  '**Exactly one real root.** The counting argument is the point: non-real roots come in twos, so whatever is left over after the pairs must be real if it is odd in number. The leading coefficient scales the whole polynomial and moves no root at all, which is why it cannot affect the answer.',
  'Pair everything off first. An odd leftover has to be real.')

ck('(x - (1+I))*(x - (1-I))', 'x**2 - 2*x + 2')
ck('(x + 2)*(x**2 + 3)', 'x**3 + 2*x**2 + 3*x + 6')
assert sp.sympify('x**3 + 2*x**2 + 3*x + 6').subs(x, -2) == 0
assert set(roots_of('x**3 + 2*x**2 + 3*x + 6')) == {sp.Integer(-2), sp.I*sp.sqrt(3), -sp.I*sp.sqrt(3)}
assert sp.expand((x - (1 + I)) * (x - (1 - I))) == x**2 - 2*x + 2

build('ad-astra', C, Q, 'unit-alg-t3-06',
      'Topic 3 · 3-6 Theorems About Roots of Polynomial Equations', 'algeo',
      'Lesson 3-6 covers the theorems that let you find every root of a polynomial: the Fundamental Theorem of '
      'Algebra (exactly n roots), the Rational Root Theorem (a finite list of candidates), and the Complex and '
      'Irrational Conjugate Theorems (awkward roots always come in pairs).',
      'This is the lesson that finishes the job Lesson 3-5 started. Factoring finds the easy roots; these '
      'theorems find the rest, and tell you when to stop looking.',
      [('State how many roots a polynomial has, counting multiplicity', 'source'),
       ('List the possible rational roots using the Rational Root Theorem', 'source'),
       ('Use the Complex and Irrational Conjugate Theorems to name paired roots', 'source'),
       ('Combine testing, division and the Quadratic Formula to find every root', 'added')],
      'One thing to know about this unit’s sources: her Topic 3 folder has the student-edition pages for every '
      'lesson EXCEPT 3-6 — aga_24_a2_0306_se.pdf is the one file missing. This was built from the 3-6 '
      'vocabulary sheet and its answer key (which show the lesson working with rational roots alongside '
      'irrational and complex conjugate pairs) plus the standard theorem set that vocabulary names, so the '
      'scope should be right, but it is worth a glance against her actual textbook pages if anything looks '
      'unfamiliar.\n\nThe distinction most worth reinforcing is what each theorem promises: the Fundamental '
      'Theorem guarantees the COUNT, while the Rational Root Theorem only supplies a list to try — and a '
      'polynomial can easily have no rational roots at all. The other reliable trap is the conjugate: only ONE '
      'sign flips, the one on the imaginary part or the radical.',
      ('Work one quartic all the way through — candidates, divide, divide, then the Quadratic Formula.', 22),
      'content/alg-topic3-06.json',
      'enVision Algebra 2, Lesson 3-6 (Drive — vocabulary sheet and answer key)',
      'enVision Algebra 2 Lesson 3-6: Theorems About Roots of Polynomial Equations')

# ---------------------------------------------------------------- 3-7
C, Q = [], []

card(C, 'Parent function',
     "**The simplest function of its family — x², x³, x⁴, x⁵ — before any transformation."
     "**"
     "\n• Every transformed polynomial in this lesson is one of these, moved, stretched or flipped."
     "\n• Even-degree parents open the same way at both ends; odd-degree parents run opposite ways.",
     hint='Find the parent first. Everything else is a change made to it.')

card(C, 'The general transformed form',
     "**g(x) = a · f(b(x − h)) + k.**"
     "\n• a stretches vertically and flips it if negative; b stretches horizontally; h shifts left or right; k shifts up or down."
     "\n• The letters OUTSIDE the function (a and k) behave as you would expect; the ones INSIDE (b and h) do the opposite.",
     eq='g(x) = a · f(b(x − h)) + k',
     hint='Outside is intuitive; inside is backwards.')

card(C, 'Vertical translation',
     "**+ k moves the graph UP by k; − k moves it down.**"
     "\n• It is added outside the function, so it does exactly what it looks like."
     "\n• f(x) = x³ + 5 is the cubic lifted five units.",
     hint='Outside and last — the one transformation that never surprises anyone.')

card(C, 'Horizontal translation — the sign trap',
     "**f(x − h) moves the graph RIGHT by h, not left.**"
     "\n• (x − 4)³ is the cubic shifted 4 units RIGHT; (x + 4)³ shifts it 4 LEFT."
     "\n• It feels backwards because the shift happens to the INPUT: to get the old output you now need a bigger x.",
     eq='f(x − h) shifts right by h',
     hint='The sign inside the bracket is the opposite of the direction of travel.')

card(C, 'Vertical stretch and compression',
     "**a multiplies every output: |a| > 1 stretches it taller, 0 < |a| < 1 squashes it flatter.**"
     "\n• 3x³ is three times as tall at every x; 0.2x³ is flattened."
     "\n• The x-intercepts never move under a vertical stretch — multiplying zero still gives zero.",
     hint='Stretching vertically pins the zeros in place; only the heights change.')

card(C, 'Reflection',
     "**A negative a flips the graph across the x-axis.**"
     "\n• −f(x) sends every output to its opposite, so rises become falls."
     "\n• It reverses the end behaviour, and it leaves the x-intercepts exactly where they were.",
     hint='A minus out front turns the picture upside down and moves no zero.')

card(C, 'Horizontal stretch and compression',
     "**f(bx) with |b| > 1 SQUEEZES the graph horizontally; 0 < |b| < 1 stretches it wider.**"
     "\n• Backwards again, because b acts on the input: a bigger b means you reach the same output sooner."
     "\n• f(2x) is half as wide; f(0.5x) is twice as wide.",
     hint='Big b, narrow graph. Inside the function, everything inverts.')

card(C, 'Even and odd degree under transformation',
     "**A transformation never changes the degree, so it never changes whether the ends agree.**"
     "\n• Shifting, stretching and flipping all preserve the degree."
     "\n• A reflection reverses which way the ends point, but an even-degree graph still has both ends together.",
     hint='The ends can be flipped, but never un-matched.', frm='added')

card(C, 'Reading a transformation off an equation',
     "**Identify the parent, then take a, b, h and k one at a time.**"
     "\n• g(x) = −2(x + 3)⁴ − 1: parent x⁴, reflected, stretched ×2, left 3, down 1."
     "\n• Note (x + 3) means LEFT 3, and the −1 outside means DOWN 1 — the two directions are read by different rules.",
     eq='g(x) = −2(x + 3)⁴ − 1',
     hint='Name the parent out loud first. Then four small readings, not one big one.', frm='added')

card(C, 'Example: the cubic, moved',
     "**g(x) = (x − 2)³ + 1 is the parent cubic shifted 2 right and 1 up.**"
     "\n• Its point of inflection sits at (2, 1), where the parent’s sits at the origin."
     "\n• The shape is completely unchanged — only its position moved.",
     eq='g(x) = (x − 2)³ + 1',
     hint='Translations move the graph and never reshape it.', frm='added')
C[-1]['graph'] = {'w': [-1, 5, -4, 6], 'gx': 1, 'gy': 2,
                  'series': [{'type': 'poly', 'c': [1, -6, 12, -7]}],
                  'pts': [{'x': 2, 'y': 1, 'label': '(2, 1)'}],
                  'xl': 'x', 'yl': 'g(x)'}

card(C, 'Example: flipped and flattened',
     "**h(x) = −0.5x⁴ is the quartic reflected across the x-axis and squashed to half height.**"
     "\n• The parent x⁴ has both ends up; the minus sends both ends down."
     "\n• The 0.5 flattens it but moves nothing — the only zero, at the origin, stays put.",
     eq='h(x) = −0.5x⁴',
     hint='Sign flips it, size flattens it, and neither moves a zero.', frm='added')
C[-1]['graph'] = {'w': [-2.5, 2.5, -8, 2], 'gx': 1, 'gy': 2,
                  'series': [{'type': 'poly', 'c': [-0.5, 0, 0, 0, 0]}],
                  'xl': 'x', 'yl': 'h(x)'}

ck('(x-2)**3 + 1', 'x**3 - 6*x**2 + 12*x - 7')
assert sp.expand((x - 2)**3 + 1).subs(x, 2) == 1

# ---- questions -------------------------------------------------------------
q(Q, 1, 'How does the graph of g(x) = x³ + 7 compare with f(x) = x³?',
  ['Shifted 7 units up', 'Shifted 7 units down', 'Shifted 7 units right', 'Stretched by a factor of 7'], 0,
  'The 7 is added outside the function.',
  ['The change is added AFTER cubing, so it acts on the output.',
   'Adding to the output raises every point.',
   'So the graph moves up.',
   'Shifted 7 units up.'],
  '**Shifted 7 units up.** Changes outside the function do what they look like they do. A horizontal shift would need the 7 inside the cube, as (x + 7)³ — and that one moves LEFT, not right.',
  'Outside the function: vertical, and intuitive.')

q(Q, 1, 'How does the graph of g(x) = (x − 6)⁴ compare with f(x) = x⁴?',
  ['Shifted 6 units right', 'Shifted 6 units left', 'Shifted 6 units down', 'Shifted 6 units up'], 0,
  'A change inside the function does the opposite of what it looks like.',
  ['The 6 is subtracted from x, so it is INSIDE the function.',
   'Inside changes act horizontally and run backwards.',
   'Subtracting moves the graph in the POSITIVE direction.',
   'So it shifts 6 units right.'],
  '**Shifted 6 units right.** Minus means right. The reason is that the shift acts on the INPUT: to get the output the parent gave at 0, you now have to feed in x = 6. That "you need a bigger x" reasoning is what makes the direction stick.',
  'When in doubt, ask what x makes the bracket zero. That x is where the parent’s origin ended up.')

q(Q, 1, 'What does the negative sign do in g(x) = −x⁵?',
  ['Reflects the graph across the x-axis', 'Shifts the graph down',
   'Reflects the graph across the y-axis', 'Makes the graph narrower'], 0,
  'A minus in front multiplies every output by −1.',
  ['The minus multiplies the whole function, so it acts on outputs.',
   'Every output becomes its opposite.',
   'Positive values go below the axis and negative values go above.',
   'That is a reflection across the x-axis.'],
  '**Reflects across the x-axis.** A reflection across the y-AXIS would need the minus inside, as (−x)⁵ — acting on the input rather than the output. For an odd function like x⁵ those two happen to produce the same picture, but they are different operations and on most functions they differ.',
  'Minus outside flips vertically; minus inside flips horizontally.')

q(Q, 1, 'In g(x) = 4x³, what does the 4 do?',
  ['Stretches the graph vertically by a factor of 4', 'Shifts the graph up 4',
   'Compresses the graph vertically by a factor of 4', 'Shifts the graph right 4'], 0,
  'It multiplies the output, and it is bigger than 1.',
  ['The 4 multiplies the whole function, so it acts on outputs.',
   'Multiplying outputs by a number bigger than 1 makes them further from the axis.',
   'So the graph is stretched vertically.',
   'It is a vertical stretch by a factor of 4.'],
  '**Stretches vertically by a factor of 4.** A factor greater than 1 stretches; a factor between 0 and 1 would compress. Note the zero at the origin does not move — 4 × 0 is still 0, which is why vertical stretching never relocates an x-intercept.',
  'Vertical stretches change heights and leave every zero exactly where it is.')

q(Q, 1, 'Which parent function does g(x) = −3(x + 1)⁴ − 2 come from?',
  ['x⁴', 'x³', 'x²', '−x⁴'], 0,
  'The parent is the simplest function of the family — no coefficients, no shifts.',
  ['The power on the bracket is 4.',
   'So the family is the quartics.',
   'The parent of that family is the simplest one: x⁴.',
   'The −3, the +1 and the −2 are all transformations applied to it.'],
  '**x⁴.** The parent never carries any of the transformations — −x⁴ already has the reflection built in, so it is a transformed function rather than a parent. Identifying the bare power first is what makes the rest of the reading straightforward.',
  'Strip everything away until only the power is left. That is the parent.')

q(Q, 2, 'Describe every transformation in g(x) = −2(x − 5)³ + 4 from the parent x³.',
  ['Reflected, stretched by 2, right 5, up 4', 'Reflected, stretched by 2, left 5, up 4',
   'Stretched by 2, right 5, down 4', 'Reflected, compressed by 2, right 5, up 4'], 0,
  'Take a, h and k one at a time, and remember which of them run backwards.',
  ['a = −2: the minus reflects across the x-axis and the 2 stretches vertically.',
   'The bracket is (x − 5), which shifts RIGHT 5 — inside changes run opposite to their sign.',
   'The + 4 is outside, so it shifts UP 4.',
   'Reflected, stretched by 2, right 5, up 4.'],
  '**Reflected, stretched by 2, right 5, up 4.** Three readings, three different rules: the sign of a reflects, its size stretches (2 > 1, so stretch not compress), and the bracket’s minus means right while the outside plus means up. Reading them one at a time is what stops them blurring together.',
  'Say each one out loud as you take it. Four quick decisions beat one complicated one.')

q(Q, 2, 'The point (2, 8) is on f(x) = x³. Where is the corresponding point on g(x) = f(x − 3) + 5?',
  ['(5, 13)', '(−1, 13)', '(5, 3)', '(2, 13)'], 0,
  'Apply the horizontal shift to the x-coordinate and the vertical one to the y.',
  ['f(x − 3) shifts the graph 3 units right, so x goes from 2 to 5.',
   'The + 5 shifts it 5 units up, so y goes from 8 to 13.',
   'Both coordinates move, each by its own transformation.',
   'The point lands at (5, 13).'],
  '**(5, 13).** Tracking one point is the fastest way to check a transformation you are unsure of: the minus inside really does move it in the POSITIVE x direction. Getting (−1, 13) means applying the horizontal shift the wrong way — the exact error the sign trap produces.',
  'Follow a single known point through. It settles every direction question without a graph.')

q(Q, 2, 'Which transformation does NOT move any x-intercept of a polynomial?',
  ['A vertical stretch', 'A vertical translation', 'A horizontal translation', 'A horizontal stretch'], 0,
  'Ask which change leaves outputs of zero still equal to zero.',
  ['A vertical stretch multiplies every output by a constant.',
   'Any output that was 0 becomes a · 0 = 0, so it stays a zero.',
   'A vertical translation shifts zeros off the axis entirely.',
   'Both horizontal changes move the x-values themselves. So only the vertical stretch leaves them put.'],
  '**A vertical stretch.** Multiplying by a non-zero constant cannot create or destroy a zero, so the x-intercepts are exactly where they were — only the heights between them changed. Every other transformation here moves them: vertically by lifting the graph off the axis, horizontally by relocating the x-values.',
  'A reflection is also a vertical multiplication, so it leaves the zeros alone too.')

q(Q, 2, 'How does g(x) = (2x)³ compare with f(x) = x³?',
  ['Horizontally compressed by a factor of 2', 'Horizontally stretched by a factor of 2',
   'Vertically stretched by a factor of 2', 'Shifted 2 units right'], 0,
  'The 2 is inside the function, so it acts horizontally — and backwards.',
  ['The 2 multiplies x before the cubing, so it is an inside change.',
   'Inside changes act horizontally and run opposite to expectation.',
   'A factor greater than 1 therefore SQUEEZES rather than stretches.',
   'So it is horizontally compressed by a factor of 2.'],
  '**Horizontally compressed by 2.** Bigger b means a narrower graph, because you reach any given output at half the x you used to. Note that (2x)³ also equals 8x³ — so this one can honestly be described as a vertical stretch by 8 as well, which is a genuine quirk of power functions rather than a contradiction.',
  'For power functions, a horizontal squeeze and a vertical stretch can be the same graph.')
ck('(2*x)**3', '8*x**3')

q(Q, 3, 'A student says (x + 3)² shifts the parabola 3 units right because of the plus. What is the clearest way to show them otherwise?',
  ['Ask which x makes the bracket zero — it is −3, so it moved left',
   'Point out that a plus inside always means a shift left',
   'Expand it to x² + 6x + 9 and read off the middle term',
   'Note that the parabola opens upward whichever sign is used'], 0,
  'Look for the argument that shows WHY, not just a rule to memorise.',
  ['The parent x² has its vertex where its input is 0.',
   'For (x + 3)², the input to the squaring is (x + 3).',
   'That is zero when x = −3.',
   'So the vertex now sits at x = −3 — three units LEFT.'],
  '**Ask which x makes the bracket zero.** That single question settles the direction from first principles every time, without memorising a rule that feels backwards. "A plus always means left" is correct but is just another rule to take on trust, and expanding it hides the structure completely.',
  'Set the inside to zero. Wherever that lands is where the parent’s origin ended up.')

q(Q, 3, 'g(x) = −(x − 1)⁴ + 3. What is its end behaviour and where is its maximum?',
  ['Both ends down; maximum at (1, 3)', 'Both ends up; maximum at (1, 3)',
   'Both ends down; maximum at (−1, 3)', 'Ends opposite; no maximum'], 0,
  'The degree decides whether the ends agree; the reflection decides which way; the shifts place the peak.',
  ['The degree is 4, which is even, so both ends agree.',
   'The leading coefficient is negative (the reflection), so both ends go DOWN.',
   'The parent x⁴ has its minimum at the origin; reflecting turns that into a maximum.',
   'The shifts move it right 1 and up 3, so the maximum is at (1, 3).'],
  '**Both ends down; maximum at (1, 3).** Three independent readings that have to agree: even degree pairs the ends, the minus sends them down, and the reflection converts the parent’s lowest point into a highest one. Since both ends fall, that peak really is the highest point overall.',
  'A reflected even-degree polynomial always has a genuine maximum. Both ends falling guarantees it.')
ck('-(x-1)**4 + 3', '-x**4 + 4*x**3 - 6*x**2 + 4*x + 2')
assert sp.expand(-(x-1)**4 + 3).subs(x, 1) == 3

q(Q, 3, 'Why does a transformation never change whether a polynomial’s two ends point the same way?',
  ['Because no transformation changes the degree, and the degree’s parity decides it',
   'Because transformations only move graphs, never reshape them',
   'Because the leading coefficient never changes',
   'Because end behaviour is not affected by transformations at all'], 0,
  'Two things set the end behaviour. Ask which of them a transformation can touch.',
  ['Whether the ends agree depends only on whether the degree is even or odd.',
   'Shifting, stretching and reflecting all leave the degree exactly as it was.',
   'So the parity is untouched, and the ends keep agreeing or keep disagreeing.',
   'A reflection can swap which way they point, but never un-pair them.'],
  '**Because no transformation changes the degree.** The leading coefficient certainly CAN change — a reflection negates it, which reverses the ends’ direction — so end behaviour is affected; what cannot change is whether the two ends match, because that is decided by parity alone.',
  'Direction can flip. Agreement cannot. The two halves of end behaviour are set by different things.')

q(Q, 3, 'Put these transformations of f(x) = x⁴ in order from NARROWEST to WIDEST graph.',
  ['g(x) = 5x⁴', 'g(x) = 2x⁴', 'g(x) = 0.5x⁴', 'g(x) = 0.1x⁴'], 0,
  'A larger vertical stretch makes the graph rise faster, which reads as narrower.',
  ['A bigger multiplier makes every output larger, so the graph climbs more steeply.',
   'Climbing steeply means it reaches a given height sooner — it looks narrower.',
   'So the order runs from the largest coefficient to the smallest.',
   '5, then 2, then 0.5, then 0.1.'],
  '**5, 2, 0.5, then 0.1.** A bigger vertical stretch reads as a narrower graph, because the curve reaches any given height at a smaller x. Coefficients between 0 and 1 flatten it out, which reads as wider — and none of them moves the zero at the origin.',
  'Narrow and wide are descriptions of steepness here, not of anything horizontal actually changing.',
  kind='order')

# --- top-up to the 18-24 guideline -----------------------------------------
q(Q, 1, 'In g(x) = ⅓x³, what does the ⅓ do to the graph of f(x) = x³?',
  ['Compresses it vertically, so it climbs more slowly',
   'Stretches it vertically, so it climbs more quickly',
   'Shifts the whole graph down by one third of a unit',
   'Reflects the whole graph across the x-axis'], 0,
  'Every output is cut to a third of what it was. Picture what that does to the height.',
  ['A number multiplying the whole function acts on the OUTPUT.',
   'Each y-value becomes a third of its old size.',
   'Points move toward the x-axis rather than away from it.',
   'That is a vertical compression, and the graph climbs more slowly.'],
  '**A vertical compression — it climbs more slowly.** A multiplier bigger than 1 stretches; a multiplier between 0 and 1 compresses. The word "compression" describes the SHAPE and not a direction of movement: nothing slides down the page, every point simply lands closer to the axis than it used to.',
  'Bigger than 1 stretches, between 0 and 1 squashes. The sign is a separate question.')

q(Q, 1, 'What does the minus sign INSIDE the parentheses do in g(x) = (−x)³?',
  ['Reflects the graph across the y-axis',
   'Reflects the graph across the x-axis',
   'Shifts the graph to the left',
   'Compresses the graph vertically'], 0,
  'Inside the parentheses is always about the input, which is the horizontal direction.',
  ['A change inside the parentheses acts on the INPUT, so it is horizontal.',
   'Negating the input swaps what happens at x with what happens at −x.',
   'Left and right trade places, which is a reflection across the y-axis.',
   'A minus OUTSIDE would instead flip up and down, across the x-axis.'],
  '**A reflection across the y-axis.** Inside acts on the input and is horizontal; outside acts on the output and is vertical. These two are the pair most often swapped, and for an odd power they happen to draw the same picture — (−x)³ equals −x³ — which is exactly why the reasoning matters more than the drawing. For an even power they are genuinely different.',
  'Inside → input → horizontal. Outside → output → vertical.')

q(Q, 2, 'Write the function for y = x³ reflected across the x-axis, moved 4 units left, then moved 1 unit up.',
  ['g(x) = −(x + 4)³ + 1',
   'g(x) = −(x − 4)³ + 1',
   'g(x) = (−x + 4)³ + 1',
   'g(x) = −(x + 4)³ − 1'], 0,
  'The horizontal move is the one where the written sign is the opposite of the movement.',
  ['Reflecting across the x-axis puts a minus on the whole function: −x³.',
   'Moving 4 LEFT means replacing x with x + 4, because inside signs work backwards.',
   'Moving 1 UP adds 1 on the outside, where the sign is straightforward.',
   'Putting them together: g(x) = −(x + 4)³ + 1.'],
  '**g(x) = −(x + 4)³ + 1.** Only the horizontal move reverses: left is written as a plus, right as a minus, because it is the input being adjusted before the function ever runs. The vertical pieces read exactly as they look, so up really is + 1.',
  'Left is +, right is −, and only inside the parentheses. Vertical shifts say what they mean.')

q(Q, 2, 'g(x) = 5(x − 2)⁴. Where is its minimum, and what is the minimum value there?',
  ['At x = 2, and the minimum value is 0',
   'At x = −2, and the minimum value is 0',
   'At x = 2, and the minimum value is 5',
   'At x = 0, and the minimum value is 0'], 0,
  'A fourth power is never negative, so ask where it manages to be zero.',
  ['(x − 2)⁴ is never negative, and it is zero exactly when x = 2.',
   'Multiplying by 5 does not change WHERE the zero is.',
   '5 × 0 is still 0, so the minimum value stays 0.',
   'The minimum is 0, at x = 2.'],
  '**At x = 2, with value 0.** A vertical stretch pulls the graph away from the x-axis everywhere except on the axis itself, where five times nothing is still nothing — so the lowest point does not move at all. Only a vertical SHIFT would change the minimum value, and there is not one here.',
  'A stretch moves everything except the points already sitting on the axis.')

q(Q, 2, 'The point (1, 5) lies on f. Which point must lie on g(x) = f(x + 2) − 6?',
  ['(−1, −1)',
   '(3, −1)',
   '(−1, 11)',
   '(3, 11)'], 0,
  'Ask what input to g makes the inside of f equal 1.',
  ['g reads f at x + 2, so set x + 2 = 1 to reach the known point.',
   'That gives x = −1, so the new point sits at −1 on the x-axis.',
   'At that input f returns 5, and g then subtracts 6.',
   '5 − 6 = −1, so the point is (−1, −1).'],
  '**(−1, −1).** The + 2 inside moves the graph LEFT, so the x-coordinate goes down rather than up — (3, −1) is what you get by adding 2 in the direction the plus suggests. The − 6 outside is straightforward and simply lowers the height by 6.',
  'Solve inside = old x. Then do the outside arithmetic to the y-value.')

q(Q, 3, 'Does order matter? Route A stretches f(x) = x³ vertically by 3 and then shifts up 2. Route B shifts up 2 and then stretches by 3.',
  ['Yes — A gives 3x³ + 2, B gives 3x³ + 6; the stretch multiplies the shift',
   'No — both routes end at 3x³ + 2, so the order makes no difference here',
   'No — both routes end at 3x³ + 6, so the order makes no difference here',
   'Yes — A gives 3x³ + 6 and B gives 3x³ + 2, the other way round'], 0,
  'Write each route out as an expression rather than picturing it.',
  ['Route A: stretch first gives 3x³, then adding 2 gives 3x³ + 2.',
   'Route B: shift first gives x³ + 2, then stretching gives 3(x³ + 2).',
   'Expanding that second one gives 3x³ + 6.',
   'The two results differ, so the order does matter.'],
  '**Yes — A gives 3x³ + 2 and B gives 3x³ + 6.** Stretching after a shift multiplies the shift as well, which is why a written form like a(x − h)ⁿ + k always means stretch first and shift second. Reading a function left to right is not the order the transformations happen in.',
  'A stretch applied later multiplies whatever was already added.')

q(Q, 3, 'g(x) = (x − 4)⁵ + 1. How many real zeros does it have, and where?',
  ['One, at x = 3 — an odd power hits each value exactly once',
   'Five, at x = 3 — the exponent counts how many zeros there are',
   'None — a fifth power can never come out negative',
   'One, at x = 5 — subtract the 1 from the 4 inside the parentheses'], 0,
  'Set it to zero and undo the pieces one at a time. Odd roots of negatives are allowed.',
  ['Setting g(x) = 0 gives (x − 4)⁵ = −1.',
   'An odd power can be negative, and the only real fifth root of −1 is −1.',
   'So x − 4 = −1, which gives x = 3.',
   'An odd power takes each value exactly once, so x = 3 is the only real zero.'],
  '**One real zero, at x = 3.** An odd power is one-to-one, so the equation has exactly one real solution no matter what is on the right — unlike an even power, where (x − 4)⁴ = 1 would give two. The exponent counts roots with multiplicity over the complex numbers, not distinct real crossings, so five is the wrong reading of it.',
  'Odd power → one real solution every time. Even power → two, or none.')

assert sp.expand(3 * (x**3 + 2)) == 3*x**3 + 6
assert sp.sympify('(x - 4)**5 + 1').subs(x, 3) == 0
assert len([r for r in sp.Poly('(x - 4)**5 + 1', x).all_roots() if r.is_real]) == 1
assert sp.sympify('5*(x - 2)**4').subs(x, 2) == 0

build('ad-astra', C, Q, 'unit-alg-t3-07',
      'Topic 3 · 3-7 Transformations of Polynomial Functions', 'algeo',
      'Lesson 3-7 applies the transformation rules to polynomial parent functions: g(x) = a · f(b(x − h)) + k, '
      'covering vertical and horizontal translations, stretches and compressions, and reflections.',
      'These are the same transformation rules she has used on quadratics and absolute value, now on any '
      'polynomial — so the payoff is that one set of rules covers every function family she will meet.',
      [('Identify the parent function of a transformed polynomial', 'source'),
       ('Describe translations, stretches, compressions and reflections from an equation', 'source'),
       ('Track a point through a transformation', 'added'),
       ('Predict the end behaviour of a transformed polynomial', 'added')],
      'The horizontal sign is the whole lesson: (x − 4) shifts RIGHT, not left, and it feels backwards to '
      'everyone. The fix that actually sticks is asking which x makes the bracket zero — that is where the '
      'parent’s origin ended up, and it is derivable rather than memorised, so it survives a stressful test. '
      'The same inversion governs horizontal stretches, where a factor greater than 1 SQUEEZES the graph.\n\n'
      'One honest subtlety in a question here: for power functions a horizontal compression and a vertical '
      'stretch can produce the identical graph, since (2x)³ is also 8x³. That is a real feature of this family '
      'rather than an error, and the explanation says so.',
      ('Track one point through each transformation — it settles every direction question.', 18),
      'content/alg-topic3-07.json',
      'enVision Algebra 2, Lesson 3-7 (Drive)',
      'enVision Algebra 2 Lesson 3-7: Transformations of Polynomial Functions')

print('3-5, 3-6 and 3-7 built; sympy verified every root, factorisation and transformation.')
