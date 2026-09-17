# Algebra & Geometry II — Topic 3, lessons 3-3 (Polynomial Identities) and
# 3-4 (Dividing Polynomials).
#
# Sources: aga_24_a2_0303_se.pdf / 0304_se.pdf and the 3-3 / 3-4 Mathematical
# Literacy and Vocabulary sheets, all in her Drive "Topic 3" folder.
#
# Every identity, expansion, division and remainder below is checked with sympy
# before it can reach a question. Nothing is worked by hand.
import sympy as sp
from unit_common import card, q, build

x, y, a, b = sp.symbols('x y a b')

def ck(got, want):
    g, w = sp.expand(sp.sympify(got)), sp.expand(sp.sympify(want))
    assert sp.simplify(g - w) == 0, 'MISMATCH: %s != %s' % (g, w)
    return w

def divmod_(num, den, v=x):
    """Quotient and remainder, computed — never worked by hand."""
    qq, rr = sp.div(sp.Poly(sp.sympify(num), v), sp.Poly(sp.sympify(den), v))
    return sp.expand(qq.as_expr()), sp.expand(rr.as_expr())

# --- the five identities the lesson names, verified as identities ------------
ck('(a-b)*(a+b)', 'a**2 - b**2')
ck('(a+b)**2', 'a**2 + 2*a*b + b**2')
ck('(a-b)**2', 'a**2 - 2*a*b + b**2')
ck('(a+b)*(a**2 - a*b + b**2)', 'a**3 + b**3')
ck('(a-b)*(a**2 + a*b + b**2)', 'a**3 - b**3')

# --- the misprint on her 3-3 vocabulary sheet, confirmed by rendering the PDF
# The sheet's "Square of a Sum" answer is printed 20x² + 40xy + 25y².
ck('(4*x + 5*y)**2', '16*x**2 + 40*x*y + 25*y**2')
assert sp.expand((4*x + 5*y)**2) != sp.sympify('20*x**2 + 40*x*y + 25*y**2')

# ---------------------------------------------------------------- 3-3
C, Q = [], []

card(C, 'Polynomial identity',
     "**An equation between two polynomials that is true for EVERY value of the variable.**"
     "\n• Not something you solve — something you use, in either direction."
     "\n• Left to right it expands; right to left it factors. Same statement, two jobs.",
     hint='An equation you solve has answers. An identity has no answers because it is always true.')

card(C, 'Difference of squares',
     "**a² − b² = (a − b)(a + b).**"
     "\n• Spot it by two perfect squares with a MINUS between them."
     "\n• a² + b² does NOT factor this way — a sum of squares has no real factoring.",
     eq='a² − b² = (a − b)(a + b)',
     hint='Minus between two squares. A plus is a dead end.')

card(C, 'Square of a sum',
     "**(a + b)² = a² + 2ab + b².**"
     "\n• The middle term is the one people lose: there are TWO cross products, so it is 2ab."
     "\n• (a + b)² is never a² + b². Test it with a = 3, b = 4: 49 against 25.",
     eq='(a + b)² = a² + 2ab + b²',
     hint='Two squares and TWICE the product — three terms, not two.')

card(C, 'Square of a difference',
     "**(a − b)² = a² − 2ab + b².**"
     "\n• Only the middle sign changes from the square of a sum."
     "\n• The last term is still POSITIVE — a negative times a negative.",
     eq='(a − b)² = a² − 2ab + b²',
     hint='Middle goes negative; the end stays positive.')

card(C, 'Sum of cubes',
     "**a³ + b³ = (a + b)(a² − ab + b²).**"
     "\n• Unlike a sum of squares, a sum of CUBES does factor."
     "\n• The three-term factor never factors further.",
     eq='a³ + b³ = (a + b)(a² − ab + b²)',
     hint='Cubes are the friendly case: both the sum and the difference factor.')

card(C, 'Difference of cubes',
     "**a³ − b³ = (a − b)(a² + ab + b²).**"
     "\n• Same shape as the sum of cubes with two signs flipped."
     "\n• Note the middle term of the long factor has NO 2 in front — that is what separates it from a squared binomial.",
     eq='a³ − b³ = (a − b)(a² + ab + b²)',
     hint='No 2 on the middle term — that is the giveaway it is a cube factor, not a square.')

card(C, 'SOAP — the signs on the cube identities',
     "**Same, Opposite, Always Positive.**"
     "\n• The binomial factor takes the SAME sign as the original."
     "\n• The middle term of the trinomial takes the OPPOSITE sign."
     "\n• The last term is ALWAYS POSITIVE. That is the whole sign pattern for both cube identities.",
     hint='S-O-AP: same, opposite, always positive.')

card(C, 'Perfect square trinomial',
     "**A trinomial that came from squaring a binomial — spot it when the first and last terms are perfect squares and the middle is twice the product of their roots.**"
     "\n• x² + 10x + 25 qualifies: √x² = x, √25 = 5, and 2 · x · 5 = 10x. So it is (x + 5)²."
     "\n• x² + 11x + 25 does not — the middle term fails the test, so it is not a perfect square.",
     hint='Check the middle term against twice the product. That is the test.')

card(C, 'Identities as a shortcut for arithmetic',
     "**43 × 37 = (40 + 3)(40 − 3) = 40² − 3² = 1600 − 9 = 1591.**"
     "\n• Any pair of numbers equally spaced either side of a round number is a difference of squares."
     "\n• It is the same identity, used on numbers instead of variables — which is the point of calling it an identity.",
     hint='Numbers are just polynomials with the variable already filled in.', frm='added')

card(C, 'The commonest identity error',
     "**(a + b)² ≠ a² + b², and √(a² + b²) ≠ a + b.**"
     "\n• Squaring does not distribute over addition — the cross terms are real and they do not vanish."
     "\n• Whenever you are tempted, test it with two small numbers. One counterexample settles it.",
     hint='Try a = 3, b = 4 on anything that looks too convenient.', frm='added')

card(C, 'Which identity to reach for',
     "**Count the terms first, then look for squares or cubes.**"
     "\n• Two terms, both squares, minus between them → difference of squares."
     "\n• Two terms, both cubes → sum or difference of cubes (either works)."
     "\n• Three terms with the middle equal to twice the product → perfect square trinomial.",
     hint='Term count narrows it to one or two candidates before you do any work.', frm='added')

card(C, 'Example: factoring a difference of cubes',
     "**27x³ − 8 = (3x − 2)(9x² + 6x + 4).**"
     "\n• Write each part as a cube first: 27x³ = (3x)³ and 8 = 2³, so a = 3x and b = 2."
     "\n• Then a² = 9x², ab = 6x, b² = 4, and SOAP places the signs.",
     eq='27x³ − 8 = (3x − 2)(9x² + 6x + 4)',
     hint='Name a and b before substituting — most cube-factoring errors are really a-and-b errors.', frm='added')

ck('(3*x-2)*(9*x**2+6*x+4)', '27*x**3 - 8')
ck('(x+5)**2', 'x**2 + 10*x + 25')
assert 43*37 == 1591 == 40**2 - 3**2

# ---- questions -------------------------------------------------------------
q(Q, 1, 'Which statement is a polynomial identity?',
  # The three wrong options are all CONDITIONAL equations dressed to look like
  # identities — one factored, one in two variables, one a completed square —
  # so eliminating means testing values rather than spotting the odd shape out.
  ['(a − b)(a + b) = a² − b²',
   '(x − 2)(x − 3)(x + 1) = 0',
   'a² + 2ab + b² = 4ab',
   'x² + 6x + 9 = 25'], 0,
  'Try putting a couple of different numbers in. An identity survives every one of them.',
  ['(a − b)(a + b) = a² − b² holds for any a and b at all — try 5 and 2, or 1 and 1.',
   '(x − 2)(x − 3)(x + 1) = 0 is true only at x = 2, 3 and −1.',
   'a² + 2ab + b² = 4ab rearranges to (a − b)² = 0, so it holds only when a = b.',
   'x² + 6x + 9 = 25 is (x + 3)² = 25, true only at x = 2 and x = −8.'],
  '**(a − b)(a + b) = a² − b².** An identity holds for EVERY value, which is what makes it a rewriting tool you can reach for anywhere. The other three are equations to solve, true only at particular values — and two of them are written in the shape of an identity on purpose, which is why testing numbers beats trusting the look of it.',
  'Equations have solutions. An identity has nothing to solve, because nothing is excluded.')

ck('x**2 - 49', '(x-7)*(x+7)')
q(Q, 1, 'Factor x² − 49.',
  ['(x − 7)(x + 7)', '(x − 7)²', '(x + 7)²', 'It cannot be factored'], 0,
  'Two perfect squares with a minus between them.',
  ['x² is a perfect square and 49 = 7² is a perfect square.',
   'They are separated by a minus, so this is a difference of squares.',
   'a² − b² = (a − b)(a + b) with a = x and b = 7.',
   'So x² − 49 = (x − 7)(x + 7).'],
  '**(x − 7)(x + 7).** One factor of each sign. (x − 7)² would expand to x² − 14x + 49, which has a middle term this expression does not — a fast way to rule it out without expanding fully.',
  'A difference of squares always factors into a matched pair, one plus and one minus.')

q(Q, 1, 'Expand (x + 6)².',
  ['x² + 12x + 36', 'x² + 36', 'x² + 6x + 36', 'x² + 12x + 12'], 0,
  'Two squares and twice the product.',
  ['a = x and b = 6.',
   'a² = x² and b² = 36.',
   'The middle term is 2ab = 2 · x · 6 = 12x.',
   'So (x + 6)² = x² + 12x + 36.'],
  '**x² + 12x + 36.** The middle term is TWICE the product, because there are two cross products when you multiply the bracket by itself. "x² + 36" is the classic error — squaring does not distribute over addition, and testing x = 1 settles it: 49 against 37.',
  'Whenever you are tempted to distribute a square, test it with one number.')

ck('x**3 + 27', '(x+3)*(x**2-3*x+9)')
q(Q, 1, 'Factor x³ + 27.',
  ['(x + 3)(x² − 3x + 9)', '(x + 3)(x² + 3x + 9)', '(x + 3)(x² − 6x + 9)', '(x + 3)³'], 0,
  'Write 27 as a cube first, then let SOAP place the signs.',
  ['27 = 3³, so a = x and b = 3.',
   'The binomial factor takes the SAME sign: (x + 3).',
   'The trinomial’s middle term takes the OPPOSITE sign: −3x. The last term is always positive: +9.',
   'So x³ + 27 = (x + 3)(x² − 3x + 9).'],
  '**(x + 3)(x² − 3x + 9).** SOAP: Same, Opposite, Always Positive. The x² − 6x + 9 option is (x − 3)² — a perfect square trinomial, which is a different shape entirely: a cube identity’s middle term never carries a 2.',
  'No coefficient 2 on the middle term is what tells a cube factor from a squared binomial.')

q(Q, 1, 'Which expression CANNOT be factored using the identities in this lesson?',
  ['x² + 16', 'x² − 16', 'x³ + 64', 'x³ − 64'], 0,
  'One of these is a sum; ask which sums are allowed.',
  ['x² − 16 is a difference of squares and factors.',
   'x³ + 64 is a sum of cubes and factors.',
   'x³ − 64 is a difference of cubes and factors.',
   'x² + 16 is a SUM of squares, which has no factoring over the real numbers.'],
  '**x² + 16.** A sum of squares is the one case that does not factor — which makes cubes the surprising ones, since BOTH the sum and the difference of cubes factor. Squares are fussy about the sign; cubes are not.',
  'Difference of squares yes, sum of squares no, both cubes yes. Worth memorising as three facts.')

q(Q, 1, 'In the identity a³ − b³ = (a − b)(a² + ab + b²), what is the sign of the last term of the trinomial?',
  ['Always positive', 'Always negative', 'The same as the sign in the original', 'The opposite of the sign in the original'], 0,
  'The P in SOAP.',
  ['SOAP stands for Same, Opposite, Always Positive.',
   'The binomial factor takes the SAME sign as the original.',
   'The trinomial’s middle term takes the OPPOSITE sign.',
   'The last term is ALWAYS POSITIVE, in both cube identities.'],
  '**Always positive.** It is +b² in both the sum and the difference of cubes, which is what the final "AP" of SOAP is for. Since b² is a square, a positive value there is also what you would expect.',
  'Two of the three signs move; the last one never does.')

ck('(2*x - 9)*(2*x + 9)', '4*x**2 - 81')
q(Q, 2, 'Factor 4x² − 81.',
  ['(2x − 9)(2x + 9)', '(4x − 9)(x + 9)', '(2x − 9)²', '(4x − 81)(x + 1)'], 0,
  'Both terms are perfect squares — but take the square root of the coefficient too.',
  ['4x² = (2x)², so a = 2x — not x.',
   '81 = 9², so b = 9.',
   'a² − b² = (a − b)(a + b).',
   'So 4x² − 81 = (2x − 9)(2x + 9).'],
  '**(2x − 9)(2x + 9).** The coefficient has to be square-rooted along with the variable: √(4x²) is 2x. Leaving the 4 alone is the usual slip here and produces a pair that does not multiply back.',
  'Multiply your factors back mentally — the middle terms must cancel exactly.')

ck('(x-8)**2', 'x**2 - 16*x + 64')
q(Q, 2, 'Which expression is a perfect square trinomial?',
  ['x² − 16x + 64', 'x² − 16x + 60', 'x² − 10x + 64', 'x² + 16x − 64'], 0,
  'Square-root the ends, double their product, and compare with the middle.',
  ['For x² − 16x + 64: √x² = x and √64 = 8.',
   'Twice their product is 2 · x · 8 = 16x, which matches the middle term.',
   'So it is (x − 8)².',
   'The others fail: 60 is not a perfect square, 2 · x · 8 is not 10x, and a negative last term cannot come from squaring.'],
  '**x² − 16x + 64.** The test is whether the middle term equals twice the product of the square roots of the ends. An option whose constant is NEGATIVE fails for a structural reason: squaring a binomial always gives a positive last term, so a negative one rules itself out before you test anything.',
  'Three quick checks: are both ends squares, is the last one positive, does the middle match 2ab?')

q(Q, 2, 'Use an identity to compute 52 × 48 without a calculator.',
  ['2496', '2500', '2504', '2596'], 0,
  'The two numbers sit the same distance either side of a round number.',
  ['52 = 50 + 2 and 48 = 50 − 2.',
   'So the product is (50 + 2)(50 − 2), a difference of squares.',
   'That is 50² − 2² = 2500 − 4.',
   'The product is 2496.'],
  '**2496.** Recognising a ± b either side of a round number turns a two-digit multiplication into two squares and a subtraction. Answering 2500 forgets the −b² — which is exactly the middle-term-style omission the identities exist to prevent.',
  'This is the identity doing real work: the same rewriting, on numbers rather than variables.')
assert 52*48 == 2496 == 50**2 - 2**2

ck('(x**2 - 9)', '(x-3)*(x+3)')
q(Q, 2, 'Factor x⁴ − 81 completely.',
  ['(x − 3)(x + 3)(x² + 9)', '(x² − 9)(x² + 9)', '(x − 3)(x + 3)(x − 3)(x + 3)', '(x² − 9)²'], 0,
  'It is a difference of squares — and then check whether either factor is one too.',
  ['x⁴ = (x²)² and 81 = 9², so it factors as (x² − 9)(x² + 9).',
   'That is not finished: x² − 9 is itself a difference of squares.',
   'x² − 9 = (x − 3)(x + 3).',
   'x² + 9 is a SUM of squares and stops there. So the full factoring is (x − 3)(x + 3)(x² + 9).'],
  '**(x − 3)(x + 3)(x² + 9).** "Completely" is the whole instruction: after the first step you have to look again. x² − 9 factors further; x² + 9 does not, because a sum of squares has no real factoring — so the answer keeps it intact rather than forcing it.',
  'After any factoring step, re-examine each factor. Stopping one step early is the usual way to lose the mark.')
ck('(x-3)*(x+3)*(x**2+9)', 'x**4 - 81')

ck('(5*x + 2)**2', '25*x**2 + 20*x + 4')
q(Q, 2, 'Expand (5x + 2)².',
  ['25x² + 20x + 4', '25x² + 4', '25x² + 10x + 4', '10x² + 20x + 4'], 0,
  'Square each end, then double the product of the two terms.',
  ['a = 5x and b = 2.',
   'a² = 25x² and b² = 4.',
   '2ab = 2 · 5x · 2 = 20x.',
   'So (5x + 2)² = 25x² + 20x + 4.'],
  '**25x² + 20x + 4.** The coefficient gets squared too, so 5x becomes 25x², and the middle is 2 · 5x · 2 = 20x. Writing 10x there is the error of forgetting the doubling; 10x² is the error of doubling instead of squaring the first term.',
  'Both a² and 2ab involve the coefficient. Compute them separately rather than in one go.')

ck('8*x**3 + 125', '(2*x+5)*(4*x**2-10*x+25)')
q(Q, 2, 'Factor 8x³ + 125.',
  ['(2x + 5)(4x² − 10x + 25)', '(2x + 5)(4x² + 10x + 25)',
   '(8x + 125)(x² − x + 1)', '(2x + 5)³'], 0,
  'Identify a and b as cube roots before touching the signs.',
  ['8x³ = (2x)³ so a = 2x; 125 = 5³ so b = 5.',
   'Same sign on the binomial: (2x + 5).',
   'a² = 4x², ab = 10x, b² = 25; the middle takes the opposite sign, the last is always positive.',
   'So 8x³ + 125 = (2x + 5)(4x² − 10x + 25).'],
  '**(2x + 5)(4x² − 10x + 25).** Both coefficients need cube-rooting: ∛8 = 2 and ∛125 = 5. Then SOAP places every sign, so the only real work is naming a and b correctly — which is where nearly all the errors in cube factoring actually happen.',
  'Name a and b out loud first. The rest of the identity is mechanical once they are right.')

q(Q, 3, 'A student writes (x + 7)² = x² + 49. Give a single value of x that proves this is wrong.',
  ['x = 1, since 64 ≠ 50', 'x = 0, since 49 = 49', 'No value disproves it', 'x = −7, since 0 = 0'], 0,
  'A counterexample has to make the two sides actually DIFFER.',
  ['At x = 1: (1 + 7)² = 64, while 1² + 49 = 50.',
   '64 ≠ 50, so the claim fails — one counterexample is enough.',
   'x = 0 gives 49 on both sides, and x = −7 gives 0 on both sides, so neither disproves anything.',
   'x = 1 is the value that proves it wrong.'],
  '**x = 1, since 64 ≠ 50.** The missing 2ab term is 14x, which happens to vanish at x = 0 — so testing zero would have wrongly "confirmed" the claim. A counterexample has to be a value where the two sides genuinely differ, which means avoiding the values that make the missing piece zero.',
  'When testing a suspected identity, avoid 0 and any root — those are exactly where a false claim can look true.')

q(Q, 3, 'Why does a² + b² fail to factor while a³ + b³ succeeds?',
  ['A sum of cubes has a matching identity; a sum of squares has none',
   'Because cubes are always larger than squares, so they split',
   'Because a² + b² is not really a polynomial in the first place',
   'Because a³ + b³ has three terms while a² + b² has only two'], 0,
  'One option states the actual mathematical situation; the others state things that are false or beside the point.',
  ['a³ + b³ = (a + b)(a² − ab + b²) — multiply it out and the cross terms cancel.',
   'No comparable real factoring exists for a² + b².',
   'a² + b² is certainly a polynomial, and a³ + b³ has two terms, not three.',
   'The real reason is simply that one has a matching identity and the other does not.'],
  '**A sum of cubes has a matching identity; a sum of squares has none over the reals.** It is worth knowing this is a statement about the REAL numbers specifically — a² + b² does factor once imaginary numbers are allowed, which she met in Topic 2. Over the reals, it stops.',
  'Whenever a factoring rule has an exception, ask which number system the rule is stated over.')

ck('(x + 4)**2 - 25', '(x - 1)*(x + 9)')
q(Q, 3, 'Factor (x + 4)² − 25 completely.',
  ['(x − 1)(x + 9)', '(x + 4 − 5)(x + 4 + 5), which cannot be simplified',
   '(x + 4)(x − 25)', 'x² + 8x − 9, which cannot be factored'], 0,
  'Treat the whole bracket as a single square, then simplify what you get.',
  ['This is A² − b² with A = (x + 4) and b = 5.',
   'So it factors as ((x + 4) − 5)((x + 4) + 5).',
   'Simplify each bracket: (x − 1) and (x + 9).',
   'So the complete factoring is (x − 1)(x + 9).'],
  '**(x − 1)(x + 9).** The identity works with a whole expression in place of a — it never required a single letter. Stopping at ((x + 4) − 5)((x + 4) + 5) applies the identity correctly and then fails to finish the arithmetic, which is not "complete".',
  'An identity applies to any expression in the a slot, not just a bare variable.')

q(Q, 3, 'You want to factor 16x⁴ − 1. Which sequence gets you there completely?',
  ['Difference of squares twice, then stop at the sum of squares',
   'Difference of squares once, then stop',
   'Difference of cubes, then difference of squares',
   'Perfect square trinomial, then difference of squares'], 0,
  'Plan it before doing it: what shape is it, and what shape is each piece?',
  ['16x⁴ = (4x²)² and 1 = 1², so it is a difference of squares: (4x² − 1)(4x² + 1).',
   '4x² − 1 is itself a difference of squares: (2x − 1)(2x + 1).',
   '4x² + 1 is a SUM of squares, so it stops there.',
   'So: difference of squares twice, then stop at the sum of squares.'],
  '**Difference of squares twice, then stop at the sum of squares.** Planning the route first is what stops you either finishing early or trying to force the sum of squares. There are no cubes here at all, and nothing has three terms, so neither of those identities can apply.',
  'Count terms and check for squares before starting. It rules out most of the identities immediately.')
ck('(2*x-1)*(2*x+1)*(4*x**2+1)', '16*x**4 - 1')

q(Q, 3, 'A rectangle has length (n + 5) and width (n − 5). A square has side n. How much bigger is the square’s area?',
  ['25 square units larger, whatever n happens to be',
   '10n square units larger, so the gap grows with n',
   '25n square units larger, so the gap grows with n',
   'Neither is larger — they are always exactly equal'], 0,
  'Write both areas and subtract — and notice what the rectangle’s area is a difference of.',
  ['Rectangle area: (n + 5)(n − 5) = n² − 25.',
   'Square area: n².',
   'Difference: n² − (n² − 25) = 25.',
   'The square is bigger by 25 square units, regardless of n.'],
  '**25 square units, whatever n is.** This is the difference-of-squares identity read as a fact about area: stretching one side by 5 and shrinking the other by 5 always costs exactly 25 — the amount lost never depends on the starting size. The n² terms cancel, which is what makes the answer a constant.',
  'A constant answer to a question with a variable in it is usually an identity in disguise.')
ck('n**2 - (n+5)*(n-5)'.replace('n','x'), '25')

ck('(x + 2*y)**2', 'x**2 + 4*x*y + 4*y**2')
q(Q, 2, 'Expand (x + 2y)\u00b2.',
  ['x\u00b2 + 4xy + 4y\u00b2', 'x\u00b2 + 2xy + 4y\u00b2', 'x\u00b2 + 4y\u00b2', 'x\u00b2 + 4xy + 2y\u00b2'], 0,
  'Both letters carry their coefficients through the squaring and the doubling.',
  ['a = x and b = 2y.',
   'a\u00b2 = x\u00b2 and b\u00b2 = (2y)\u00b2 = 4y\u00b2 \u2014 the 2 is squared too.',
   '2ab = 2 \u00b7 x \u00b7 2y = 4xy.',
   'So (x + 2y)\u00b2 = x\u00b2 + 4xy + 4y\u00b2.'],
  '**x\u00b2 + 4xy + 4y\u00b2.** Two places the coefficient 2 has to be handled: squared in the last term (giving 4y\u00b2) and doubled in the middle (giving 4xy). They come out the same number here, which is a coincidence of this example, not a rule \u2014 with 3y they would be 6xy and 9y\u00b2.',
  'Compute a\u00b2, b\u00b2 and 2ab as three separate pieces. Doing it in one sweep is what loses a coefficient.')

ck('49*x**2 - 64*y**2', '(7*x - 8*y)*(7*x + 8*y)')
q(Q, 2, 'Factor 49x\u00b2 \u2212 64y\u00b2.',
  ['(7x \u2212 8y)(7x + 8y)', '(7x \u2212 8y)\u00b2', '(49x \u2212 64y)(x + y)', 'It cannot be factored'], 0,
  'Square-root both coefficients as well as both variables.',
  ['49x\u00b2 = (7x)\u00b2, so a = 7x.',
   '64y\u00b2 = (8y)\u00b2, so b = 8y.',
   'A minus between two squares is a difference of squares.',
   'So it factors as (7x \u2212 8y)(7x + 8y).'],
  '**(7x \u2212 8y)(7x + 8y).** Two variables changes nothing about the identity \u2014 a and b can be any expressions at all. What it does change is that there are now two coefficients to square-root, and both have to be done.',
  'Check by multiplying back: the cross terms must cancel to leave exactly two terms.')

q(Q, 3, 'Which of these is NOT a correct polynomial identity?',
  ['(a \u2212 b)\u00b2 = a\u00b2 \u2212 b\u00b2', '(a \u2212 b)(a + b) = a\u00b2 \u2212 b\u00b2',
   'a\u00b3 + b\u00b3 = (a + b)(a\u00b2 \u2212 ab + b\u00b2)', '(a + b)\u00b2 = a\u00b2 + 2ab + b\u00b2'], 0,
  'One of these confuses squaring a difference with a difference of squares.',
  ['(a \u2212 b)\u00b2 expands to a\u00b2 \u2212 2ab + b\u00b2, which has three terms.',
   'a\u00b2 \u2212 b\u00b2 has two terms and comes from (a \u2212 b)(a + b) instead.',
   'Test with a = 5, b = 3: (5 \u2212 3)\u00b2 = 4, while 25 \u2212 9 = 16.',
   'So (a \u2212 b)\u00b2 = a\u00b2 \u2212 b\u00b2 is the false one.'],
  '**(a \u2212 b)\u00b2 = a\u00b2 \u2212 b\u00b2.** It welds two real identities into a false one: squaring a difference gives three terms, while a difference of SQUARES is what factors into a matched pair. The two look alike written down and describe completely different operations, which is exactly why they get swapped.',
  'Squaring a binomial always produces three terms. Any claimed square with only two is wrong.')

build('ad-astra', C, Q, 'unit-alg-t3-03',
      'Topic 3 · 3-3 Polynomial Identities', 'algeo',
      'Lesson 3-3 covers the polynomial identities: difference of squares, the square of a sum and of a '
      'difference, and the sum and difference of cubes — used both to expand and, read backwards, to factor.',
      'These five patterns turn up constantly for the rest of the year, in factoring, in solving, and in '
      'simplifying. Recognising one on sight is worth more than being able to grind it out.',
      [('State and apply the difference of squares, square of a sum, and square of a difference', 'source'),
       ('Factor a sum or difference of cubes, placing the signs with SOAP', 'source'),
       ('Recognise a perfect square trinomial by testing the middle term', 'source'),
       ('Use an identity to simplify arithmetic and to factor completely', 'added')],
      'Two things to watch. The first is (a + b)² = a² + b² — the single most common algebra error there is, '
      'and several questions here are built to catch it; the cure is testing with two small numbers. The second '
      'is stopping one step early on "factor completely", since a first factoring often leaves a factor that '
      'factors again.\n\nWorth knowing: her 3-3 vocabulary worksheet has a genuine misprint. In question 2, the '
      '"Square of a Sum" answer is printed as 20x² + 40xy + 25y², but (4x + 5y)² is 16x² + 40xy + 25y² — the '
      'first coefficient should be 16, not 20. Every other item on that sheet checks out exactly. She can still '
      'match it correctly (it is the only expression of that shape), but if she verifies the algebra she will '
      'find it does not expand, and it is worth her knowing the sheet is wrong rather than her arithmetic.',
      ('Learn the five patterns by their SHAPE first — recognising which one applies is most of the work.', 18),
      'content/alg-topic3-03.json',
      'enVision Algebra 2, Lesson 3-3 (Drive)',
      'enVision Algebra 2 Lesson 3-3: Polynomial Identities')

# ---------------------------------------------------------------- 3-4
C, Q = [], []

card(C, 'Dividing polynomials',
     "**Splitting a polynomial into a quotient and a remainder, exactly like long division with numbers.**"
     "\n• dividend ÷ divisor = quotient + remainder⁄divisor."
     "\n• 17 ÷ 5 = 3 remainder 2 works the same way as a polynomial division — the shape of the answer is identical.",
     eq='P(x) ÷ d(x) = q(x) + r(x)⁄d(x)',
     hint='Same shape as number division: a whole part and a leftover.')

card(C, 'Long division of polynomials',
     "**Works for ANY divisor, of any degree.**"
     "\n• Divide the leading terms, multiply back, subtract, bring down, repeat."
     "\n• The subtraction step is where signs get lost — you are subtracting the whole product, not just its first term.",
     hint='Divide, multiply, subtract, bring down. The subtraction is the dangerous step.')

card(C, 'Synthetic division',
     "**A shortcut that works ONLY when the divisor is linear, of the form x − a.**"
     "\n• Much faster than long division, but it is not general."
     "\n• For a divisor like x² + 1 or 2x − 3, you need long division instead.",
     hint='Linear divisors only. Anything else is long division.')

card(C, 'Reverse the sign',
     "**Dividing by (x − 2) means you synthetic-divide with +2.**"
     "\n• The number you use is the value that makes the divisor ZERO, so the sign flips."
     "\n• Dividing by (x + 5) means using −5, since x + 5 = 0 at x = −5.",
     hint='Use the number that makes the divisor equal zero — not the one you see written.')

card(C, 'Placeholder zeros',
     "**Every missing power needs a 0 in the coefficient row.**"
     "\n• x³ − 7 is really x³ + 0x² + 0x − 7, so its row is 1, 0, 0, −7."
     "\n• Leaving a gap out shifts every later coefficient into the wrong column and makes the whole division wrong.",
     hint='Write the polynomial in standard form with nothing missing before you start.')

card(C, 'Quotient and remainder',
     "**The bottom row of a synthetic division gives the quotient’s coefficients, and the very last number is the remainder.**"
     "\n• The quotient starts one degree LOWER than the dividend."
     "\n• A remainder of 0 means the divisor divided evenly — it is a factor.",
     hint='Last number is the leftover; everything before it is the answer.')

card(C, 'Degree of the quotient',
     "**deg(quotient) = deg(dividend) − deg(divisor).**"
     "\n• A cubic divided by a linear gives a quadratic."
     "\n• Checking this before you start tells you how many coefficients the answer should have — a free check on your work.",
     eq='deg q = deg P − deg d',
     hint='Subtract the degrees to predict the shape of the answer.')

card(C, 'The Remainder Theorem',
     "**Dividing P(x) by (x − a) leaves a remainder of exactly P(a).**"
     "\n• So you can find a remainder by SUBSTITUTING, with no division at all."
     "\n• To find the remainder when P is divided by (x − 3), just compute P(3).",
     eq='P(x) ÷ (x − a) leaves P(a)',
     hint='The remainder is just the function evaluated at the number that zeroes the divisor.')

card(C, 'The Factor Theorem',
     "**(x − a) is a factor of P(x) exactly when P(a) = 0.**"
     "\n• It is the Remainder Theorem with remainder zero — no leftover means it divided evenly."
     "\n• This is the bridge to finding roots, which is what Lessons 3-5 and 3-6 are built on.",
     eq='(x − a) is a factor ⇔ P(a) = 0',
     hint='Zero remainder and "is a factor" are the same statement.')

card(C, 'Writing the answer properly',
     "**Quotient plus remainder over divisor — the remainder never just gets dropped.**"
     "\n• (x² + 4x + 14) + 19⁄(x − 2) is a complete answer; the quotient alone is not."
     "\n• Only when the remainder is 0 does the quotient stand by itself.",
     hint='A leftover has to appear in the answer, written over the divisor.')

card(C, 'Example: a synthetic division, worked',
     "**(x³ − 5x² − 2x + 24) ÷ (x − 3) = x² − 2x − 8, remainder 0.**"
     "\n• Use +3. Row: 1, −5, −2, 24."
     "\n• Bring down 1; 1·3 = 3, −5 + 3 = −2; −2·3 = −6, −2 + (−6) = −8; −8·3 = −24, 24 + (−24) = 0."
     "\n• Remainder 0, so (x − 3) IS a factor.",
     hint='Bring down, multiply, add — and the last add gives the remainder.', frm='added')

card(C, 'Example: a remainder without dividing',
     "**The remainder of (2x³ + x − 5) ÷ (x − 2) is 13, found by substituting.**"
     "\n• P(2) = 2(8) + 2 − 5 = 16 + 2 − 5 = 13."
     "\n• No division was done at all — that is the Remainder Theorem earning its keep.",
     hint='If a question asks only for the remainder, substitute rather than divide.', frm='added')

# --- verify every division and remainder claimed above
_q, _r = divmod_('x**3 - 5*x**2 - 2*x + 24', 'x - 3')
ck(_q, 'x**2 - 2*x - 8'); assert _r == 0
_P = 2*x**3 + x - 5
assert _P.subs(x, 2) == 13
_q2, _r2 = divmod_('x**3 + 2*x**2 + 6*x - 9', 'x - 2')
ck(_q2, 'x**2 + 4*x + 14'); assert _r2 == 19

# ---- questions -------------------------------------------------------------
q(Q, 1, 'To divide a polynomial by (x − 6) using synthetic division, which number do you use?',
  ['6', '−6', '1', '0'], 0,
  'You use the value that makes the divisor zero.',
  ['Set the divisor equal to zero: x − 6 = 0.',
   'Solving gives x = 6.',
   'That is the number synthetic division uses.',
   'So you use 6.'],
  '**6.** The sign flips from the one written, because the number you need is the ZERO of the divisor. The habit that prevents the error is actually solving x − 6 = 0 rather than copying the sign you see.',
  'Same rule for (x + 6): it is zero at −6, so you would use −6.')

q(Q, 1, 'When is synthetic division allowed?',
  ['Only when the divisor is linear, of the form x − a',
   'For any divisor at all',
   'Only when the remainder will be zero',
   'Only when the dividend has degree 3 or less'], 0,
  'Think about what the shortcut’s single row of numbers can represent.',
  ['Synthetic division compresses the divisor down to one number.',
   'That only works when the divisor is x minus a constant.',
   'A divisor like x² + 1, or 2x − 3, cannot be reduced to one number this way.',
   'So it is linear divisors of the form x − a only.'],
  '**Only when the divisor is linear, of the form x − a.** The dividend can be any degree at all, and the remainder can be anything — those are not restrictions. The restriction is entirely on the DIVISOR, which is why long division still has to exist.',
  'When the divisor is anything else, long division is the tool. It always works.')

q(Q, 1, 'Writing 2x⁴ − 3x + 1 as a row of coefficients for synthetic division gives',
  ['2, 0, 0, −3, 1', '2, −3, 1', '2, 0, −3, 1', '2, 0, 0, 0, −3, 1'], 0,
  'Every power from the highest down to the constant needs a slot.',
  ['The degree is 4, so there are five slots: x⁴, x³, x², x, constant.',
   'x⁴ has coefficient 2.',
   'x³ and x² are missing, so both are 0.',
   'Then −3 for x and 1 for the constant: 2, 0, 0, −3, 1.'],
  '**2, 0, 0, −3, 1.** A degree-4 polynomial always needs exactly five coefficients. Writing only the terms you can see shifts everything into the wrong column and the whole division comes out wrong — with no obvious sign that anything went astray.',
  'Count the slots first: degree + 1. If your row is shorter, a placeholder is missing.')

q(Q, 1, 'What does the Remainder Theorem say?',
  ['Dividing P(x) by (x − a) leaves a remainder of P(a)',
   'Dividing P(x) by (x − a) always leaves a remainder of zero',
   'The remainder is always smaller than the divisor',
   'The remainder equals the leading coefficient of P(x)'], 0,
  'It connects dividing to substituting.',
  ['The theorem links the remainder to the function’s value.',
   'Specifically, the remainder of P(x) ÷ (x − a) is P(a).',
   'That lets you find a remainder by substituting instead of dividing.',
   'So: dividing P(x) by (x − a) leaves P(a).'],
  '**Dividing P(x) by (x − a) leaves a remainder of P(a).** A remainder of zero is the special case — that is the Factor Theorem, and it is what makes (x − a) a factor. The theorem’s real value is that it replaces a whole division with one substitution.',
  'Remainder Theorem: any remainder. Factor Theorem: the remainder is zero.')

q(Q, 1, 'A degree-5 polynomial is divided by a degree-2 polynomial. What degree is the quotient?',
  ['3', '7', '10', '2'], 0,
  'Degrees subtract on division, the way they add on multiplication.',
  ['Multiplying adds degrees, so dividing subtracts them.',
   'deg(quotient) = deg(dividend) − deg(divisor).',
   'That is 5 − 2 = 3.',
   'The quotient has degree 3.'],
  '**3.** Degrees subtract on division for the same reason they add on multiplication — quotient times divisor has to rebuild the dividend, and 3 + 2 = 5. Knowing the answer’s degree in advance tells you how many coefficients to expect, which catches a dropped placeholder.',
  'Predict the degree first; then a quotient with the wrong number of terms announces itself.')

q(Q, 1, 'A synthetic division ends with a last number of 0. What does that mean?',
  ['The divisor is a factor of the polynomial',
   'The polynomial itself is equal to zero everywhere',
   'A mistake was made somewhere in the working',
   'The quotient has to come out as zero as well'], 0,
  'The last number of the bottom row is the remainder.',
  ['The final number is the remainder.',
   'A remainder of 0 means the division came out evenly.',
   'Dividing evenly is exactly what "is a factor" means.',
   'So the divisor is a factor of the polynomial.'],
  '**The divisor is a factor.** This is the Factor Theorem showing up in the arithmetic. It says nothing about the polynomial itself being zero — P(x) is zero only at that one x-value, not everywhere — and the quotient is certainly not zero.',
  'Zero remainder is good news: you have found a factor and can keep factoring the quotient.')

_qa, _ra = divmod_('x**3 + 4*x**2 - 7*x - 10', 'x - 2')
ck(_qa, 'x**2 + 6*x + 5'); assert _ra == 0
q(Q, 2, 'Divide x³ + 4x² − 7x − 10 by (x − 2).',
  ['x² + 6x + 5, remainder 0', 'x² + 2x − 3, remainder −4',
   'x² + 6x + 5, remainder 10', 'x² + 4x − 7, remainder −10'], 0,
  'Use +2, and take the row as 1, 4, −7, −10.',
  ['Bring down 1. Multiply 1 · 2 = 2; add to 4 to get 6.',
   'Multiply 6 · 2 = 12; add to −7 to get 5.',
   'Multiply 5 · 2 = 10; add to −10 to get 0.',
   'Bottom row 1, 6, 5, 0: the quotient is x² + 6x + 5 with remainder 0.'],
  '**x² + 6x + 5, remainder 0.** The quotient drops one degree from the dividend, as it must. The zero remainder means (x − 2) is a factor — and since x² + 6x + 5 factors further into (x + 1)(x + 5), the whole cubic is (x − 2)(x + 1)(x + 5).',
  'A zero remainder is an invitation to keep factoring the quotient.')
ck('(x-2)*(x+1)*(x+5)', 'x**3 + 4*x**2 - 7*x - 10')

_P2 = x**3 - 4*x**2 + x + 6
assert _P2.subs(x, 3) == 0
q(Q, 2, 'Use the Remainder Theorem: what is the remainder when x³ − 4x² + x + 6 is divided by (x − 3)?',
  ['0', '6', '18', '−6'], 0,
  'Substitute the value that makes the divisor zero — no division needed.',
  ['The divisor is zero at x = 3, so compute P(3).',
   'P(3) = 27 − 4(9) + 3 + 6.',
   'That is 27 − 36 + 3 + 6 = 0.',
   'The remainder is 0.'],
  '**0.** One substitution replaces the whole division. And the zero is informative: it means (x − 3) is a factor of this cubic, which is the Factor Theorem arriving for free.',
  'When a question asks only for the remainder, substituting is always faster than dividing.')

_P3 = x**4 - 3*x**2 + 2*x - 1
assert _P3.subs(x, -1) == -5
q(Q, 2, 'What is the remainder when x⁴ − 3x² + 2x − 1 is divided by (x + 1)?',
  ['−5', '5', '−1', '3'], 0,
  'Careful with the sign of the value you substitute.',
  ['x + 1 = 0 gives x = −1, so compute P(−1).',
   '(−1)⁴ = 1 and −3(−1)² = −3.',
   '2(−1) = −2, and the constant is −1.',
   '1 − 3 − 2 − 1 = −5.'],
  '**−5.** The divisor (x + 1) is zero at −1, not +1 — substituting +1 instead gives −1, which is offered as a wrong option precisely because it is what the sign slip produces. Note (−1)⁴ is positive while 2(−1) is negative; even and odd powers behave differently.',
  'Solve divisor = 0 rather than reading the sign off the bracket.')

q(Q, 2, 'Which division requires LONG division rather than synthetic division?',
  ['(x³ + 2x − 1) ÷ (x² + 3)', '(x³ + 2x − 1) ÷ (x − 4)',
   '(x⁵ + x) ÷ (x + 2)', '(x⁴ − 16) ÷ (x − 2)'], 0,
  'Check the DIVISOR in each, not the dividend.',
  ['Synthetic division needs a divisor of the form x − a.',
   '(x − 4), (x + 2) and (x − 2) are all that shape.',
   '(x² + 3) is degree 2, so it cannot be reduced to a single number.',
   'That one needs long division.'],
  '**(x³ + 2x − 1) ÷ (x² + 3).** Only the divisor decides. The dividends here range from degree 3 to degree 5 and none of that matters — a degree-5 dividend with a linear divisor is still perfectly fine for synthetic division.',
  'Look only at what you are dividing BY. The thing being divided is never the constraint.')

_qb, _rb = divmod_('2*x**3 - 3*x**2 + 4', 'x + 1')
ck(_qb, '2*x**2 - 5*x + 5'); assert _rb == -1
q(Q, 2, 'Divide 2x³ − 3x² + 4 by (x + 1).',
  ['2x² − 5x + 5, remainder −1', '2x² − 5x + 5, remainder 9',
   '2x² − x + 4, remainder 0', '2x² − 3x + 4, remainder −1'], 0,
  'There is a missing term — write the row carefully — and the divisor is zero at −1.',
  ['The x term is missing, so the row is 2, −3, 0, 4.',
   'Use −1. Bring down 2; 2 · (−1) = −2, and −3 + (−2) = −5.',
   '−5 · (−1) = 5, and 0 + 5 = 5.',
   '5 · (−1) = −5, and 4 + (−5) = −1. So 2x² − 5x + 5, remainder −1.'],
  '**2x² − 5x + 5, remainder −1.** Two traps in one question: the missing x term needs a 0 placeholder, and the divisor (x + 1) is zero at −1. Checking with the Remainder Theorem confirms it — P(−1) = −2 − 3 + 4 = −1.',
  'You can always check a synthetic division’s remainder independently by substituting. Two methods agreeing is real confidence.')

q(Q, 3, 'A student divides x³ + 2x − 5 by (x − 1) and writes the row as 1, 2, −5. What will go wrong?',
  ['The x² placeholder is missing, so every column shifts over by one',
   'Nothing is wrong — the row lists every coefficient there is',
   'The divisor sign is wrong: (x − 1) should be entered as −1',
   'The coefficients belong in ascending order, lowest power first'], 0,
  'Count the slots a degree-3 polynomial needs.',
  ['A cubic needs four coefficients: x³, x², x, constant.',
   'x³ + 2x − 5 has no x² term, so that slot is 0.',
   'The correct row is 1, 0, 2, −5.',
   'Writing only three numbers shifts the 2 and the −5 left, so the division is wrong throughout.'],
  '**The x² placeholder is missing, so every column shifts over by one.** A degree-3 dividend always needs four coefficients, and the answer will come out as a quadratic-looking thing that is simply wrong — with nothing obviously broken to alert her. Predicting the quotient’s degree first is the check that catches it.',
  'Degree + 1 slots, always. A short row is a missing placeholder every time.')

_P4 = x**3 + x**2 - 10*x + 8
assert _P4.subs(x, 1) == 0 and _P4.subs(x, 2) == 0 and _P4.subs(x, -4) == 0
q(Q, 3, 'For P(x) = x³ + x² − 10x + 8, which of these is a factor?',
  ['(x − 2)', '(x + 2)', '(x − 3)', '(x + 1)'], 0,
  'The Factor Theorem turns this into four quick substitutions.',
  ['(x − a) is a factor exactly when P(a) = 0.',
   'P(2) = 8 + 4 − 20 + 8 = 0. That one works.',
   'P(−2) = −8 + 4 + 20 + 8 = 24, not zero.',
   'P(3) = 27 + 9 − 30 + 8 = 14 and P(−1) = −1 + 1 + 10 + 8 = 18. So (x − 2) is the factor.'],
  '**(x − 2).** Testing candidates by substitution is far faster than dividing by each one. And the sign matters: (x − 2) asks about P(2), while (x + 2) asks about P(−2) — which here is 24, nowhere near zero.',
  'This is exactly the tool Lesson 3-6 builds on to find all the roots of a polynomial.')

q(Q, 3, 'P(x) divided by (x − 4) gives a quotient of x² + 3x − 1 and a remainder of 6. What is P(x)?',
  ['x³ − x² − 13x + 10', 'x³ + 3x² − x + 6',
   'x³ − x² − 13x + 4', 'x² + 3x + 5'], 0,
  'Reverse the division: multiply the quotient by the divisor and add the remainder.',
  ['Division says P(x) = divisor × quotient + remainder.',
   '(x − 4)(x² + 3x − 1) = x³ + 3x² − x − 4x² − 12x + 4.',
   'Combine: x³ − x² − 13x + 4.',
   'Add the remainder 6: x³ − x² − 13x + 10.'],
  '**x³ − x² − 13x + 10.** The relationship runs both ways, and reversing it is the standard way to CHECK a division. Forgetting to add the remainder gives x³ − x² − 13x + 4 — offered here because it is the near-miss that catches most people.',
  'Check any division by multiplying back and adding the remainder. It should rebuild the dividend exactly.')
ck('(x-4)*(x**2+3*x-1) + 6', 'x**3 - x**2 - 13*x + 10')

_Pk = x**3 - 2*x**2 + x
# P(-2) = -8 - 8 - 2 + k = -18 + k, so k = 18. (Drafted as 12; the option and
# the explanation disagreed with each other, which is what exposed it.)
assert (_Pk + 18).subs(x, -2) == 0
assert (_Pk + 12).subs(x, -2) != 0
q(Q, 3, 'For what value of k is (x + 2) a factor of x³ − 2x² + x + k?',
  ['18', '16', '−2', '−18'], 0,
  'Use the Factor Theorem and solve for k.',
  ['(x + 2) is a factor exactly when P(−2) = 0.',
   'P(−2) = −8 − 2(4) + (−2) + k = −8 − 8 − 2 + k.',
   'That is −18 + k, and it must equal 0.',
   'So k = 18.'],
  '**18.** Substituting x = −2 gives −8 − 8 − 2 + k = −18 + k, and setting that to zero gives k = 18. Using +2 by mistake would give k = −2, and dropping the lone x term would give 16 — both offered here, because both are what the two usual slips actually produce.',
  'The Factor Theorem turns "make this a factor" into a plain equation in k.')

_qc, _rc = divmod_('x**3 - 8', 'x - 2')
ck(_qc, 'x**2 + 2*x + 4'); assert _rc == 0
q(Q, 2, 'Divide x\u00b3 \u2212 8 by (x \u2212 2).',
  ['x\u00b2 + 2x + 4, remainder 0', 'x\u00b2 \u2212 2x + 4, remainder 0',
   'x\u00b2 + 4, remainder 0', 'x\u00b2 + 2x + 4, remainder \u221216'], 0,
  'Two missing terms \u2014 build the coefficient row before anything else.',
  ['x\u00b3 \u2212 8 is x\u00b3 + 0x\u00b2 + 0x \u2212 8, so the row is 1, 0, 0, \u22128.',
   'Use +2. Bring down 1; 1 \u00b7 2 = 2, and 0 + 2 = 2.',
   '2 \u00b7 2 = 4, and 0 + 4 = 4.',
   '4 \u00b7 2 = 8, and \u22128 + 8 = 0. So x\u00b2 + 2x + 4, remainder 0.'],
  '**x\u00b2 + 2x + 4, remainder 0.** Both placeholder zeros were needed. The zero remainder is no accident \u2014 x\u00b3 \u2212 8 is a difference of cubes, and Lesson 3-3\u2019s identity gives exactly (x \u2212 2)(x\u00b2 + 2x + 4). Division and factoring agreeing is a real check on both.',
  'When a division comes out even, look for the identity that predicted it.')

_P5 = 3*x**3 - 2*x**2 + 5
assert _P5.subs(x, 1) == 6
q(Q, 2, 'What is the remainder when 3x\u00b3 \u2212 2x\u00b2 + 5 is divided by (x \u2212 1)?',
  ['6', '0', '5', '\u22126'], 0,
  'Substitute rather than divide.',
  ['The divisor is zero at x = 1, so compute P(1).',
   '3(1)\u00b3 = 3 and \u22122(1)\u00b2 = \u22122.',
   'The x term is absent and the constant is 5.',
   '3 \u2212 2 + 5 = 6.'],
  '**6.** Substituting 1 is about as fast as this gets \u2014 every power of 1 is 1, so the remainder is just the sum of the coefficients. That shortcut works for any division by (x \u2212 1) and is worth remembering on its own.',
  'Divide by (x \u2212 1) and the remainder is always the coefficients added up.')

q(Q, 2, 'Which statement about a remainder of 0 is TRUE?',
  ['The divisor is a factor, so the polynomial factors further',
   'The polynomial has no roots at all, of any kind',
   'The quotient must come out as 0 as well, for the same reason',
   'The division was done incorrectly and should be worked again'], 0,
  'A remainder of zero is the Factor Theorem speaking.',
  ['A zero remainder means the divisor divided evenly.',
   'Dividing evenly is what being a factor means.',
   'So P(x) = (divisor)(quotient), and the quotient may factor further still.',
   'The divisor is a factor and factoring can continue.'],
  '**The divisor is a factor, so the polynomial factors further.** It is the opposite of a problem \u2014 a zero remainder is progress, because it has split the polynomial into two pieces and the quotient is now a smaller problem to attack.',
  'Every zero remainder reduces the degree of what is left to factor.')

_qd, _rd = divmod_('x**4 - 3*x**2 + 1', 'x**2 - 2')
ck(_qd, 'x**2 - 1'); assert _rd == -1
q(Q, 3, 'Divide x\u2074 \u2212 3x\u00b2 + 1 by (x\u00b2 \u2212 2). What is the quotient?',
  ['x\u00b2 \u2212 1', 'x\u00b2 \u2212 3', 'x\u00b2 + 1', 'x\u00b2 \u2212 2x \u2212 1'], 0,
  'The divisor is not linear, so synthetic division is out \u2014 and predict the quotient\u2019s degree first.',
  ['deg 4 \u2212 deg 2 = 2, so the quotient is a quadratic.',
   'x\u2074 \u00f7 x\u00b2 = x\u00b2. Multiply back: x\u2074 \u2212 2x\u00b2. Subtract: \u2212x\u00b2 + 1.',
   '\u2212x\u00b2 \u00f7 x\u00b2 = \u22121. Multiply back: \u2212x\u00b2 + 2. Subtract: \u22121.',
   'So the quotient is x\u00b2 \u2212 1 with remainder \u22121.'],
  '**x\u00b2 \u2212 1.** A quadratic divisor rules synthetic division out entirely \u2014 this one has to be long division. Predicting the quotient\u2019s degree as 2 first is what tells you the answer is a quadratic, so an option with an x term in it can be ruled out before any arithmetic.',
  'Degree subtraction predicts the SHAPE of the answer, which narrows the options before you start.')

_P6 = x**3 + 2*x**2 - 5*x - 6
assert _P6.subs(x, 2) == 0 and _P6.subs(x, -1) == 0 and _P6.subs(x, -3) == 0
q(Q, 3, 'You find that P(2) = 0 for P(x) = x\u00b3 + 2x\u00b2 \u2212 5x \u2212 6. What is the most useful next step?',
  ['Divide P(x) by (x \u2212 2) and factor the quadratic that comes out',
   'Conclude that 2 must therefore be the only root it has',
   'Divide P(x) by (x + 2) and factor whatever is left over',
   'Substitute more values one by one until another gives zero'], 0,
  'A known root gives you a known factor \u2014 use it to shrink the problem.',
  ['P(2) = 0 means (x \u2212 2) is a factor, by the Factor Theorem.',
   'Dividing by it turns the cubic into a quadratic, which is far easier to handle.',
   'Here the quotient is x\u00b2 + 4x + 3, which factors as (x + 1)(x + 3).',
   'So P(x) = (x \u2212 2)(x + 1)(x + 3), and all three roots fall out at once.'],
  '**Divide by (x \u2212 2) and factor the quotient.** One known root converts a cubic into a quadratic, and a quadratic can be finished by factoring or the Quadratic Formula \u2014 no more guessing needed. Note the sign: P(2) = 0 gives the factor (x \u2212 2), not (x + 2). Hunting for more roots by substitution would work eventually but throws away the shortcut you have just earned.',
  'This is the whole method of Lesson 3-6: find one root, divide it out, finish the smaller polynomial.')
_qe, _re = divmod_('x**3 + 2*x**2 - 5*x - 6', 'x - 2')
ck(_qe, 'x**2 + 4*x + 3'); assert _re == 0

build('ad-astra', C, Q, 'unit-alg-t3-04',
      'Topic 3 · 3-4 Dividing Polynomials', 'algeo',
      'Lesson 3-4 covers polynomial long division and synthetic division, and the two theorems that come with '
      'them: the Remainder Theorem (dividing by x − a leaves P(a)) and the Factor Theorem (it is a factor '
      'exactly when P(a) = 0).',
      'Division is how a polynomial gets broken down, and the Factor Theorem is the doorway into finding roots '
      '— which is what the next two lessons are entirely about. Getting fluent here pays off twice.',
      [('Divide polynomials by long division and, where the divisor is linear, by synthetic division', 'source'),
       ('Write an answer as quotient plus remainder over divisor', 'source'),
       ('Apply the Remainder Theorem to find a remainder by substitution', 'source'),
       ('Apply the Factor Theorem to test whether a linear expression is a factor', 'source')],
      'Two mechanical traps account for most lost marks here, and both are in the questions. The first is the '
      'SIGN: dividing by (x + 5) means synthetic-dividing with −5, because you use the value that makes the '
      'divisor zero — solving "divisor = 0" rather than copying the sign is the habit that fixes it. The second '
      'is MISSING TERMS: x³ − 7 needs the row 1, 0, 0, −7, and leaving the zeros out silently shifts every '
      'coefficient into the wrong column, producing a confident wrong answer with nothing visibly broken. '
      'Predicting the quotient’s degree first (dividend minus divisor) catches that one every time.',
      ('Do a couple of divisions both ways — synthetically and by substituting — so the two agree.', 20),
      'content/alg-topic3-04.json',
      'enVision Algebra 2, Lesson 3-4 (Drive)',
      'enVision Algebra 2 Lesson 3-4: Dividing Polynomials')

print('3-3 and 3-4 built; sympy verified every identity, division and remainder.')
