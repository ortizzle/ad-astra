# Algebra & Geometry II — Topic 4: Rational Functions, lessons 4-3, 4-4 and 4-5.
#
# Sources (her Drive "Topic 4" folder, uploaded 2026-10-14):
#   aga_24_a2_0403_se.pdf, aga_24_a2_0404_se.pdf  — the student-edition lessons
#   aga_24_a2_na_0403_lps.pptx, _0404_lps.pptx    — lesson slides (mirror the SE pages)
#   aga_24_a2_na_0405_lps.pptx                    — the ONLY 4-5 material: there is no
#       0405_se.pdf in the folder. Its equations are slide images, read by rendering them.
#
# Same discipline as build_alg_topic4_a.py: every result is computed with sympy and every
# displayed answer is asserted equal to it (same) and every distractor asserted NOT equal
# (differs). No textbook or slide numbers are reused.
import sympy as sp
from unit_common import card, q, build
from topic4_common import x, y, z, r, c, E, same, differs, poles, holes, hasym, rgraph, finish

def sol(eq_lhs, eq_rhs, v=x):
    """Solutions of a rational equation, split into (valid, extraneous) against the
    ORIGINAL denominators — computed, never decided by eye."""
    L, R = sp.together(eq_lhs), sp.together(eq_rhs)
    # the LCD, not the product: a product of denominators adds roots the LCD would not
    dens = sp.lcm(sp.denom(L), sp.denom(R))
    raw = sp.denom(L) * sp.denom(R)
    cleared = sp.expand(sp.cancel(L * dens) - sp.cancel(R * dens))
    cands = list(set(sp.solve(cleared, v)))
    bad = [t for t in cands if sp.simplify(raw.subs(v, t)) == 0]
    good = [t for t in cands if t not in bad]
    return sorted(good), sorted(bad)

# ================================================================ 4-3
C, Q = [], []

card(C, 'Simplified form',
     "**A rational expression is simplified when its numerator and denominator share no common factor other than 1.**"
     "\n• (x + 6)/(x + 3) is simplified; x(x + 6)/(x(x + 3)) is not."
     "\n• Simplifying never changes the values — only the domain statement has to travel with it.",
     hint='No shared FACTOR left, top and bottom.')

card(C, 'How to simplify',
     "**Factor the numerator and the denominator completely, then divide out the factors they share.**"
     "\n• (x² − 25)/(x² + 2x − 15) = (x − 5)(x + 5)/((x + 5)(x − 3)) = (x − 5)/(x − 3)."
     "\n• If you cannot see a common factor, you have not finished factoring.",
     hint='Factor everything before you cancel anything.')
same('(x − 5)/(x − 3)', E('(x² − 25)/(x² + 2x − 15)'))

card(C, 'Factors cancel, terms do not',
     "**Only a factor of the WHOLE numerator and the WHOLE denominator can be divided out.**"
     "\n• (x + 6)/x is not 6: the x on top is a term added to 6, not a factor of the top."
     "\n• Test it: at x = 2, (2 + 6)/2 = 4, not 6.",
     hint='If it is joined by + or −, it is a term — hands off.')

card(C, 'Opposite factors',
     "**a − b and b − a are opposites, so (a − b)/(b − a) = −1.**"
     "\n• 4 − x = −(x − 4), so (4 − x)/(x − 4) simplifies to −1, not 1."
     "\n• Pull out the −1 first, then cancel.",
     hint='Same numbers, reversed order: that is a factor of −1.')
same('−1', E('(4 − x)/(x − 4)'))

card(C, 'The domain travels with the answer',
     "**Values that made ANY original denominator zero stay excluded, even after their factor has cancelled.**"
     "\n• (x² − 25)/(x² + 2x − 15) equals (x − 5)/(x − 3) only for x ≠ −5 and x ≠ 3."
     "\n• An identity between two expressions holds only where both are defined.",
     hint='Read the restrictions off the ORIGINAL, before cancelling.')

card(C, 'Writing an equivalent expression',
     "**Multiply top and bottom by the same nonzero expression — a form of 1 — and add its zeros to the domain restrictions.**"
     "\n• (x + 1)/(x − 4) · (x + 2)/(x + 2) = (x² + 3x + 2)/(x² − 2x − 8), for x ≠ 4, −2."
     "\n• The new expression agrees with the old one everywhere both are defined.",
     hint='A form of 1 changes the look, never the value.')
same('(x² + 3x + 2)/(x² − 2x − 8)', E('(x + 1)/(x − 4)'))

card(C, 'Multiplying rational expressions',
     "**Factor every numerator and denominator, multiply straight across, and divide out the common factors.**"
     "\n• Cancelling before you multiply out saves a lot of work."
     "\n• State the domain from every denominator that appeared.",
     hint='Factor, then cancel, then multiply — in that order.')

card(C, 'Multiplying by a polynomial',
     "**Write the polynomial over 1, then multiply as usual.**"
     "\n• (x + 3)/(x² − 25) · (x² − 5x) = (x + 3)/((x − 5)(x + 5)) · x(x − 5)/1 = x(x + 3)/(x + 5)."
     "\n• Restrictions: x ≠ 5 and x ≠ −5.",
     hint='Every polynomial is secretly over 1.')
same('x(x + 3)/(x + 5)', E('(x + 3)/(x² − 25) · (x² − 5x)'))

card(C, 'Dividing rational expressions',
     "**Multiply by the reciprocal of the divisor, then simplify as for multiplication.**"
     "\n• A/B ÷ C/D = A/B · D/C."
     "\n• The divisor's NUMERATOR moves to the bottom, so its zeros join the restrictions too.",
     hint='Keep, change, flip — then watch the new denominator.')

card(C, 'Restrictions when dividing',
     "**For A/B ÷ C/D, exclude the zeros of B, of D, AND of C.**"
     "\n• B and D are denominators from the start."
     "\n• C becomes a denominator once you flip the divisor — and you cannot divide by zero anyway.",
     hint='Three places to look, not two.')

card(C, 'Complex fractions',
     "**A fraction whose numerator or denominator contains a fraction is a division problem in disguise.**"
     "\n• (A/B) over (C/D) means A/B ÷ C/D."
     "\n• Rewrite it as a division, then multiply by the reciprocal.",
     hint='The long fraction bar is a ÷ sign.')

card(C, 'Monomials',
     "**Multiply coefficients, then combine powers of each variable by subtracting exponents across the fraction bar.**"
     "\n• (4x³y)/(6xy²) = 2x²/(3y), for x ≠ 0, y ≠ 0."
     "\n• Every variable that ever sat in a denominator is restricted from being 0.",
     hint='Numbers with numbers, x with x, y with y.')
same('2x²/(3y)', E('(4x³y)/(6xy²)'))

card(C, 'Ratio of surface area to volume',
     "**SA/V compares packaging used to space held; for similar shapes it simplifies to a number over the length, so the shape with the smaller number is more efficient for every size.**"
     "\n• A cube of edge 2x: SA = 24x², V = 8x³, so SA/V = 3/x."
     "\n• Simplifying the ratio is just dividing rational expressions.",
     hint='Smaller SA/V: less wrapping per unit of space.')
same('3/x', E('24x²/(8x³)'))

# ---- level 1 -----------------------------------------------------------------
q(Q, 1, 'When is a rational expression in simplified form?',
  ['When its numerator and denominator share no common factor other than 1',
   'When no variable appears anywhere in its denominator at all',
   'When the degree of its numerator is less than its denominator\'s',
   'When every term appearing on both top and bottom has been crossed out'], 0,
  'Simplifying is about factors.',
  ['Simplifying means dividing out common factors.',
   'You stop when there are none left except 1.',
   'Variables in the denominator are fine, and degrees can be anything.',
   'Simplified form: no common factor other than 1.'],
  '**When the numerator and denominator share no common factor other than 1.** Crossing out matching TERMS is the classic mistake, and it changes the value. A simplified expression can easily have a variable underneath or a top-heavy degree.',
  'Factors, not terms. Always.')

_e = E('(x² − 49)/(x² + 4x − 21)')
same('(x − 7)/(x − 3)', _e)
for s_ in ('(x + 7)/(x + 3)', '(x + 7)/(x − 3)', '7/3'):
    differs(s_, _e)
q(Q, 1, 'Simplify (x² − 49)/(x² + 4x − 21).',
  ['(x − 7)/(x − 3)', '(x + 7)/(x + 3)', '(x + 7)/(x − 3)', '7/3'], 0,
  'Factor top and bottom, then look for the shared factor.',
  ['x² − 49 = (x − 7)(x + 7).',
   'x² + 4x − 21 = (x + 7)(x − 3).',
   'Divide out the common factor x + 7.',
   '(x − 7)/(x − 3), for x ≠ −7, 3.'],
  '**(x − 7)/(x − 3).** The factor x + 7 is shared, so it divides out, leaving the other two. (x + 7)/(x − 3) keeps the factor that cancelled; 7/3 cancels the x² terms as if they were factors.',
  'Factored form makes the shared factor impossible to miss.')

assert sorted(sp.solve(E('x² − 9x'), x)) == [0, 9]
q(Q, 1, 'Which values of x must be excluded from (x + 2)/(x² − 9x)?',
  ['0 and 9', '9 only', '−2 only', '0, 9 and −2'], 0,
  'Exclusions come from the denominator only.',
  ['Factor the denominator: x² − 9x = x(x − 9).',
   'It is zero when x = 0 or x = 9.',
   'The numerator\'s zero, x = −2, just makes the expression 0, which is allowed.',
   'Exclude x = 0 and x = 9.'],
  '**0 and 9.** x(x − 9) = 0 at both. Forgetting the factor x gives "9 only", and −2 makes the whole expression 0 — a perfectly good value.',
  'Factor the denominator fully; a common factor of x is easy to miss.')

same('−1', E('(5 − x)/(x − 5)'))
q(Q, 1, 'Simplify (5 − x)/(x − 5), for x ≠ 5.',
  ['−1', '1', '0', 'x − 5'], 0,
  'Write 5 − x as −1 times something.',
  ['5 − x = −(x − 5).',
   'So the expression is −(x − 5)/(x − 5).',
   'The x − 5 divides out, leaving the −1.',
   'It simplifies to −1.'],
  '**−1.** The top and bottom are opposites, not equals. Try x = 7: (5 − 7)/(7 − 5) = −2/2 = −1. Answering 1 misses the sign that reversing the subtraction brings in.',
  'Reversed subtraction hides a factor of −1.')

q(Q, 1, 'What is the first move when you divide one rational expression by another?',
  ['Multiply the first by the reciprocal of the second',
   'Divide the numerators, then divide the denominators',
   'Cross-multiply so that both fraction bars disappear',
   'Flip the first expression, then multiply by the second'], 0,
  'It works exactly like dividing ordinary fractions.',
  ['A/B ÷ C/D is the same as A/B · D/C.',
   'The first expression stays as it is.',
   'Only the divisor — the second expression — is flipped.',
   'Then multiply and simplify.'],
  '**Multiply by the reciprocal of the divisor.** It is the fraction rule you already know. Flipping the FIRST expression instead gives the reciprocal of the right answer, and cross-multiplying is for solving equations, not simplifying.',
  'Keep the first, flip the second.')

_m = E('(6x²y)/(5z) · (10z²)/(3xy³)')
same('4xz/y²', _m)
for s_ in ('4xz/y', '4x²z/y²', '2xz/y²'):
    differs(s_, _m)
q(Q, 1, 'Simplify (6x²y)/(5z) · (10z²)/(3xy³).',
  ['4xz/y²', '4xz/y', '4x²z/y²', '2xz/y²'], 0,
  'Numbers with numbers, then each variable on its own.',
  ['Numbers: (6 × 10)/(5 × 3) = 60/15 = 4.',
   'x: x²/x = x.   z: z²/z = z.',
   'y: y/y³ = 1/y².',
   '4xz/y², for x, y, z ≠ 0.'],
  '**4xz/y².** Each variable is handled on its own: two x\'s on top against one below leaves x; one y on top against three below leaves y² underneath. 4xz/y cancels only one y; 4x²z/y² forgets the x in the second denominator.',
  'Count each variable top and bottom, then subtract.')

q(Q, 1, 'Why is (x + 6)/x NOT equal to 6?',
  ['x is a term of the top, not a factor of it, so it cannot cancel',
   'It does equal 6, because the two x\'s divide out to leave just 6',
   'It does not equal 6 only when x is 0; everywhere else it does',
   'Because the numerator has degree 1 and the denominator does too'], 0,
  'Try a value: x = 2.',
  ['At x = 2: (2 + 6)/2 = 8/2 = 4, not 6.',
   'The top is x + 6, a SUM; x is one of its terms.',
   'Only a factor of the whole numerator can be divided out.',
   '(x + 6)/x is already simplified (it equals 1 + 6/x).'],
  '**Because x is a term of the numerator, not a factor.** A single number check settles it: x = 2 gives 4. The expression can be split as x/x + 6/x = 1 + 6/x, which shows exactly what cancelling really allows.',
  'If one number breaks a "simplification", it was never true.')
assert sp.Rational(2 + 6, 2) == 4

# ---- level 2 -----------------------------------------------------------------
_p = E('(x² − 4)/(x + 5) · (x² + 8x + 15)/(x² + x − 6)')
same('x + 2', _p)
q(Q, 2, 'Multiply and simplify: (x² − 4)/(x + 5) · (x² + 8x + 15)/(x² + x − 6). State the domain.',
  ['x + 2, for x ≠ −5, −3, 2', 'x + 2, for every real number x',
   'x + 2, for x ≠ −5 only', '(x + 2)(x + 3), for x ≠ −5, 2'], 0,
  'Factor all four polynomials; collect restrictions from both denominators BEFORE cancelling.',
  ['x² − 4 = (x − 2)(x + 2) and x² + 8x + 15 = (x + 3)(x + 5).',
   'x² + x − 6 = (x + 3)(x − 2).',
   'Denominators: (x + 5) and (x + 3)(x − 2), so x ≠ −5, −3, 2.',
   'Cancel x + 5, x + 3 and x − 2: the product is x + 2, for x ≠ −5, −3, 2.'],
  '**x + 2, for x ≠ −5, −3, 2.** Every factor except x + 2 cancels, but each one that came from a denominator leaves its restriction behind. "Every real number" is the graph of y = x + 2 with no holes, which is not this expression.',
  'Write the restrictions down before you cross anything out.')
assert sorted(sp.solve((x + 5) * (x**2 + x - 6), x)) == [-5, -3, 2]

_d = E('(x² − 16)/(3x) ÷ ((x + 4)/(6x²))')
same('2x(x − 4)', _d)
for s_ in ('(x − 4)/(2x)', '2x(x + 4)', '(x − 4)(x + 4)²/(18x³)'):
    differs(s_, _d)
q(Q, 2, 'Divide and simplify: (x² − 16)/(3x) ÷ (x + 4)/(6x²).',
  ['2x(x − 4)', '(x − 4)/(2x)', '2x(x + 4)', '(x − 4)(x + 4)²/(18x³)'], 0,
  'Multiply by the reciprocal of (x + 4)/(6x²).',
  ['Rewrite: (x² − 16)/(3x) · 6x²/(x + 4).',
   'Factor: (x − 4)(x + 4)/(3x) · 6x²/(x + 4).',
   'Cancel x + 4, and 6x²/(3x) = 2x.',
   '2x(x − 4), for x ≠ 0, −4.'],
  '**2x(x − 4).** After flipping, x + 4 and 3x both cancel. (x − 4)/(2x) flips the wrong expression, and (x − 4)(x + 4)²/(18x³) is what you get by multiplying without flipping at all.',
  'Flip the divisor, then it is an ordinary product.')

_ok = set(sp.solve((x - 2) * (x + 5) * (x - 3), x))
assert _ok == {2, -5, 3}
q(Q, 2, 'What is the domain of (x + 1)/(x − 2) ÷ (x − 3)/(x + 5)?',
  ['x ≠ 2, −5 and 3', 'x ≠ 2 and −5', 'x ≠ 2 and 3', 'x ≠ −1, 2 and −5'], 0,
  'Check both original denominators — and the divisor\'s numerator.',
  ['The original denominators are x − 2 and x + 5, so x ≠ 2 and x ≠ −5.',
   'Dividing by (x − 3)/(x + 5) means multiplying by (x + 5)/(x − 3).',
   'Now x − 3 is a denominator too, so x ≠ 3 — and at x = 3 you would be dividing by 0.',
   'The domain excludes 2, −5 and 3.'],
  '**x ≠ 2, −5 and 3.** The trap is the divisor\'s numerator: when the divisor is 0 the whole division is undefined, and flipping it puts x − 3 underneath. −1 only makes the first fraction 0, which is allowed.',
  'Dividing: three places to look for restrictions, not two.')

_mp = E('(x + 3)/(x² − 25) · (x² − 5x)')
same('x(x + 3)/(x + 5)', _mp)
for s_ in ('(x + 3)/(x + 5)', 'x(x + 3)/(x − 5)', '(x + 3)/(x(x − 5)(x + 5)²)'):
    differs(s_, _mp)
q(Q, 2, 'Multiply and simplify: (x + 3)/(x² − 25) · (x² − 5x).',
  ['x(x + 3)/(x + 5)', '(x + 3)/(x + 5)', 'x(x + 3)/(x − 5)', '(x + 3)/(x(x − 5)(x + 5)²)'], 0,
  'Write x² − 5x over 1 and factor everything.',
  ['x² − 5x = x(x − 5), written as x(x − 5)/1.',
   'x² − 25 = (x − 5)(x + 5).',
   'The factor x − 5 divides out.',
   'x(x + 3)/(x + 5), for x ≠ 5, −5.'],
  '**x(x + 3)/(x + 5).** The x − 5 cancels but the x stays. (x + 3)/(x + 5) loses that x, x(x + 3)/(x − 5) cancels the wrong factor, and putting x² − 5x underneath treats the multiplication as a division.',
  'A polynomial multiplies the TOP; write it over 1 so it lands there.')

_base = E('(x + 1)/(x − 4)')
same('(x² + 3x + 2)/(x² − 2x − 8)', _base)
differs('(x² + 3x + 2)/(x² + 2x − 8)', _base)
differs('(x + 3)/(x − 2)', _base)
same('(x² + x)/(x² − 4x)', _base)   # equal in value — but it restricts x ≠ 0, not x ≠ −2
q(Q, 2, 'Which expression is equivalent to (x + 1)/(x − 4) over the domain x ≠ 4, −2?',
  ['(x² + 3x + 2)/(x² − 2x − 8)', '(x² + 3x + 2)/(x² + 2x − 8)', '(x + 3)/(x − 2)', '(x² + x)/(x² − 4x)'], 0,
  'Which form of 1 brings in the restriction x ≠ −2?',
  ['To exclude x = −2, multiply top and bottom by (x + 2)/(x + 2).',
   'Top: (x + 1)(x + 2) = x² + 3x + 2.',
   'Bottom: (x − 4)(x + 2) = x² − 2x − 8.',
   '(x² + 3x + 2)/(x² − 2x − 8), valid for x ≠ 4, −2.'],
  '**(x² + 3x + 2)/(x² − 2x − 8).** (x² + x)/(x² − 4x) also has the same values, but it was made with x/x, so its domain is x ≠ 4, 0 — the wrong domain. Adding 2 to top and bottom, as in (x + 3)/(x − 2), changes the value completely.',
  'Equivalent expressions are only equivalent on a stated domain.')

_s = E('(x³ − 4x)/(x² + 4x + 4)')
same('x(x − 2)/(x + 2)', _s)
for s_ in ('x(x − 2)', '(x − 2)/(x + 2)', 'x/(x + 2)'):
    differs(s_, _s)
q(Q, 2, 'Simplify (x³ − 4x)/(x² + 4x + 4).',
  ['x(x − 2)/(x + 2)', 'x(x − 2)', '(x − 2)/(x + 2)', 'x/(x + 2)'], 0,
  'Factor out x first on top, then spot the perfect square underneath.',
  ['x³ − 4x = x(x² − 4) = x(x − 2)(x + 2).',
   'x² + 4x + 4 = (x + 2)².',
   'One factor of x + 2 divides out; one stays underneath.',
   'x(x − 2)/(x + 2), for x ≠ −2.'],
  '**x(x − 2)/(x + 2).** The bottom is (x + 2) TWICE, so only one copy cancels. x(x − 2) cancels both; (x − 2)/(x + 2) drops the common factor x that was pulled out first.',
  'A squared factor cancels once per matching factor, no more.')

_cf = E('((x + 1)/x) / ((x² − 1)/x²)')
same('x/(x − 1)', _cf)
for s_ in ('(x − 1)/x', '1/(x(x − 1))', '(x + 1)²(x − 1)/x³'):
    differs(s_, _cf)
q(Q, 2, 'Simplify the complex fraction whose numerator is (x + 1)/x and whose denominator is (x² − 1)/x².',
  ['x/(x − 1)', '(x − 1)/x', '1/(x(x − 1))', '(x + 1)²(x − 1)/x³'], 0,
  'Rewrite the big fraction bar as ÷.',
  ['(x + 1)/x ÷ (x² − 1)/x² = (x + 1)/x · x²/(x² − 1).',
   'x² − 1 = (x − 1)(x + 1).',
   'Cancel x + 1, and x²/x = x.',
   'x/(x − 1), for x ≠ 0, 1, −1.'],
  '**x/(x − 1).** Once it is a division, flip the bottom fraction and cancel. (x − 1)/x is the reciprocal of the answer — what you get by flipping the top instead — and (x + 1)²(x − 1)/x³ multiplies without flipping.',
  'A complex fraction is just A ÷ B written vertically.')

# ---- level 3 -----------------------------------------------------------------
_cube = E('24x²/(8x³)'); _tall = E('18x²/(4x³)')
assert sp.simplify(_cube - 3 / x) == 0 and sp.simplify(_tall - sp.Rational(9, 2) / x) == 0
assert sp.Rational(3) < sp.Rational(9, 2)
q(Q, 3, 'Box A is a cube with edge 2x. Box B has a square base x by x and height 4x. The more efficient box has the smaller ratio of surface area to volume. Which is it?',
  ['Box A: its ratio is 3/x, against 9/(2x) for Box B',
   'Box B: its ratio is 9/(2x), which is less than 3/x',
   'Neither: both boxes simplify to the same ratio, 3/x',
   'It depends on x, so neither box is better at every size'], 0,
  'Find SA and V for each box, then simplify SA/V.',
  ['Box A: SA = 6(2x)² = 24x², V = (2x)³ = 8x³, so SA/V = 3/x.',
   'Box B: SA = 2x² + 4(x · 4x) = 18x², V = 4x³, so SA/V = 9/(2x).',
   '9/(2x) = 4.5/x, which is bigger than 3/x for every positive x.',
   'Box A, the cube, is more efficient.'],
  '**Box A.** Both ratios have the form (number)/x, so comparing the numbers 3 and 4.5 decides it once and for all — "it depends on x" is exactly what the simplification rules out. The cube wins, as compact shapes always do.',
  'When two ratios share the same x-part, only the coefficients need comparing.')

_e = E('(x² + 6x)/(x² + 3x)')
same('(x + 6)/(x + 3)', _e)
assert sp.Rational(6, 3) == 2 and _e.subs(x, 1) != 2
q(Q, 3, 'A classmate simplifies (x² + 6x)/(x² + 3x) by crossing out the x² terms and gets 6x/3x = 2. What is the correct result?',
  ['(x + 6)/(x + 3), for x ≠ 0, −3', '2, for every x except 0', '(x + 6)/(x + 3), for x ≠ −3 only', '6/3, which equals 2'], 0,
  'Factor x out of the top and the bottom.',
  ['Top: x² + 6x = x(x + 6). Bottom: x² + 3x = x(x + 3).',
   'The common FACTOR is x.',
   'Dividing it out leaves (x + 6)/(x + 3).',
   'Both 0 and −3 made the original bottom zero, so x ≠ 0, −3.'],
  '**(x + 6)/(x + 3), for x ≠ 0, −3.** The x² terms are terms, not factors, so they cannot be crossed out. A quick check: at x = 1 the original is 7/4, not 2. Dropping the restriction x ≠ 0 is the subtler error — the x cancelled, but x = 0 still breaks the original.',
  'One numerical check would have caught the classmate\'s answer.')

_lhs = E('(3x + 8)/(2x + 8)')
assert sp.solve(sp.Eq(_lhs, sp.Rational(3, 2)), x) == []
assert _lhs.subs(x, 0) == 1
q(Q, 3, 'Is (3x + 8)/(2x + 8) = 3/2 always, sometimes, or never true?',
  ['Never', 'Always', 'Only when x = 0', 'Only when x = 8'], 0,
  'Solve the equation rather than cancelling the 8s.',
  ['Multiply both sides by 2(2x + 8): 2(3x + 8) = 3(2x + 8).',
   'That is 6x + 16 = 6x + 24.',
   'Subtract 6x: 16 = 24, which is false.',
   'No value of x works, so it is never true.'],
  '**Never.** "Cancelling the 8s" suggests always, but 8 is a term, not a factor. At x = 0 the left side is 8/8 = 1, and at x = 8 it is 32/24 = 4/3 — neither is 3/2, and the algebra shows no x ever will be.',
  'A false statement like 16 = 24 at the end means no solution at all.')

_f = E('(x² − 9)/(x − 3)')
assert sp.cancel(_f) == x + 3 and holes(_f) == [3] and (x + 3).subs(x, 3) == 6
q(Q, 3, 'How does the graph of f(x) = (x² − 9)/(x − 3) compare with the graph of g(x) = x + 3?',
  ['The same line, except f has a hole at (3, 6)', 'They are identical at every single point',
   'f has a vertical asymptote at x = 3, and g does not', 'The same line, except f has a hole at (−3, 0)'], 0,
  'Simplify f, then ask which x it cannot accept.',
  ['x² − 9 = (x − 3)(x + 3), so f simplifies to x + 3.',
   'But f is undefined at x = 3, where its original denominator is 0.',
   'The factor x − 3 cancelled, so x = 3 is a hole, not an asymptote.',
   'The hole is at (3, 3 + 3) = (3, 6).'],
  '**The same line, except f has a hole at (3, 6).** The simplification is valid everywhere except x = 3, so the graphs agree at every other point. A cancelled factor gives a hole, never an asymptote, and (−3, 0) is just where the line crosses the x-axis.',
  'This is why the domain has to travel with a simplified answer.')

_q = E('(2x² − 7x − 4)/(x² − 9) ÷ ((2x + 1)/(x + 3))')
same('(x − 4)/(x − 3)', _q)
differs('(x + 4)/(x − 3)', _q)
assert sorted(sp.solve((x**2 - 9) * (2 * x + 1), x)) == [-3, sp.Rational(-1, 2), 3]
q(Q, 3, 'Divide and simplify: (2x² − 7x − 4)/(x² − 9) ÷ (2x + 1)/(x + 3). State the domain.',
  ['(x − 4)/(x − 3), for x ≠ 3, −3, −½', '(x − 4)/(x − 3), for x ≠ 3, −3',
   '(x + 4)/(x − 3), for x ≠ 3, −3, −½', '(x − 4)/(x − 3), for x ≠ 3 only'], 0,
  'Factor 2x² − 7x − 4, flip the divisor, and collect restrictions from all three places.',
  ['2x² − 7x − 4 = (2x + 1)(x − 4), and x² − 9 = (x − 3)(x + 3).',
   'Flip and multiply: (2x + 1)(x − 4)/((x − 3)(x + 3)) · (x + 3)/(2x + 1).',
   'Cancel 2x + 1 and x + 3: (x − 4)/(x − 3).',
   'Restrictions: x ≠ 3, −3 from x² − 9, and x ≠ −½ from the divisor\'s numerator.'],
  '**(x − 4)/(x − 3), for x ≠ 3, −3, −½.** Two options have the right expression with too few restrictions: −3 comes from the original denominators, and −½ from the divisor\'s numerator 2x + 1. (x + 4) is a factoring sign error.',
  'The answer and the domain are both part of "simplify".')

_len = E('((x² + 7x + 10)/(x − 1)) ÷ ((x + 2)/(x² − 1))')
same('(x + 5)(x + 1)', _len)
for s_ in ('(x + 5)/(x + 1)', '(x + 5)(x − 1)', '(x + 2)²(x + 5)/((x − 1)²(x + 1))'):
    differs(s_, _len)
q(Q, 3, 'A rectangle has area (x² + 7x + 10)/(x − 1) square units and width (x + 2)/(x² − 1) units. What is its length?',
  ['(x + 5)(x + 1)', '(x + 5)/(x + 1)', '(x + 5)(x − 1)', '(x + 2)²(x + 5)/((x − 1)²(x + 1))'], 0,
  'Length = area ÷ width.',
  ['Divide: (x² + 7x + 10)/(x − 1) ÷ (x + 2)/(x² − 1).',
   'Flip and factor: (x + 2)(x + 5)/(x − 1) · (x − 1)(x + 1)/(x + 2).',
   'Cancel x + 2 and x − 1.',
   'The length is (x + 5)(x + 1).'],
  '**(x + 5)(x + 1).** Area ÷ width, with the width flipped. (x + 2)²(x + 5)/((x − 1)²(x + 1)) multiplies the area by the width instead of dividing; (x + 5)/(x + 1) flips the area instead of the width.',
  'Check the units: square units ÷ units = units, which only division gives.')

build('ad-astra', C, Q, 'unit-alg-t4-03',
      'Topic 4 · 4-3 Multiplying and Dividing Rational Expressions', 'algeo',
      'Lesson 4-3 simplifies, multiplies and divides rational expressions: factoring and dividing out common factors, '
      'opposite factors that leave −1, writing equivalent expressions over a stated domain, multiplying by a polynomial, '
      'dividing by multiplying by the reciprocal, and simplifying ratios such as surface area to volume.',
      'Every later rational skill — adding, solving equations, graphing — starts with factoring and cancelling correctly. '
      'The domain restriction that travels with each answer is what makes the algebra honest about the holes in the graph.',
      [('Simplify a rational expression and state the values excluded from its domain', 'source'),
       ('Multiply rational expressions, including by a polynomial', 'source'),
       ('Divide rational expressions by multiplying by the reciprocal of the divisor', 'source'),
       ('Explain why only common factors, never terms, can be divided out', 'source')],
      'The single most common error is cancelling TERMS instead of factors — crossing out the x² in (x² + 6x)/(x² + 3x) '
      '— and several questions are built to catch it, along with a one-number check that exposes it. The second is '
      'the domain: restrictions come from the ORIGINAL denominators, and when dividing, from the divisor\'s numerator as '
      'well. Many answers here are marked wrong in class for a missing restriction rather than a wrong expression.',
      ('Start with the "factors, not terms" cards — every question here depends on them.', 20),
      'content/alg-topic4-03.json',
      'enVision Algebra 2, Lesson 4-3 (Drive)',
      'enVision Algebra 2 Lesson 4-3: Multiplying and Dividing Rational Expressions',
      libv_=1)
finish('content/alg-topic4-03.json')

# ================================================================ 4-4
C, Q = [], []

card(C, 'Like denominators',
     "**When the denominators match, add or subtract the numerators and keep the denominator.**"
     "\n• 3x/(x + 2) + 6/(x + 2) = (3x + 6)/(x + 2) = 3(x + 2)/(x + 2) = 3, for x ≠ −2."
     "\n• Never add the denominators: 1/5 + 3/5 is 4/5, not 4/10.",
     hint='Same bottom: work on the top only.')
same('3', E('3x/(x + 2) + 6/(x + 2)'))

card(C, 'LCM of polynomials',
     "**Factor each polynomial, then take every factor the greatest number of times it appears in any ONE of them.**"
     "\n• (x + 3)² and x² + x − 6 = (x + 3)(x − 2) have LCM (x + 3)²(x − 2)."
     "\n• A factor shared by two of them is used once, not twice — just as the LCM of 6 and 15 is 30, not 90.",
     hint='Most copies in any single one — not the total across all of them.')
assert sp.simplify(sp.lcm((x + 3)**2, x**2 + x - 6) - (x + 3)**2 * (x - 2)) == 0

card(C, 'Why the LEAST common denominator',
     "**Any common denominator gives a correct answer, but the least one keeps the numerator small, so there is far less to multiply out, factor and cancel.**"
     "\n• Multiplying all the denominators together always works — and usually buries a common factor you then have to dig back out."
     "\n• The L is about saving work, not about getting a different answer.",
     hint='Bigger common denominators are right, just expensive.', frm='added')

card(C, 'Unlike denominators',
     "**Factor each denominator, find the LCD, multiply each fraction by the form of 1 that supplies its missing factors, then combine the numerators.**"
     "\n• x/(x − 3) + 2/(x + 1): the LCD is (x − 3)(x + 1), and x(x + 1) + 2(x − 3) = x² + 3x − 6 goes on top."
     "\n• Then factor the new numerator and cancel anything it shares with the LCD.",
     hint='Missing factors in, top and bottom, then add tops.')
same('(x² + 3x − 6)/((x − 3)(x + 1))', E('x/(x − 3) + 2/(x + 1)'))

card(C, 'Subtracting: distribute the minus',
     "**When you subtract a fraction, the minus sign applies to its WHOLE numerator, so put that numerator in brackets first.**"
     "\n• (4x + 1)/(x + 5) − (x − 3)/(x + 5) = (4x + 1 − x + 3)/(x + 5) = (3x + 4)/(x + 5)."
     "\n• Writing − x − 3 instead of − x + 3 is the commonest slip in this lesson.",
     hint='Brackets around the second numerator, every time.')
same('(3x + 4)/(x + 5)', E('(4x + 1)/(x + 5) − (x − 3)/(x + 5)'))

card(C, 'Finish by simplifying',
     "**After combining, factor the numerator — it often shares a factor with the LCD that can be divided out.**"
     "\n• 4/(x² − 4) + 1/(x + 2) = (x + 2)/((x − 2)(x + 2)) = 1/(x − 2)."
     "\n• The cancelled factor still leaves its restriction behind: here x ≠ −2 as well as x ≠ 2.",
     hint='Factor the new top before you call it finished.')
same('1/(x − 2)', E('4/(x² − 4) + 1/(x + 2)'))

card(C, 'The domain of a sum',
     "**A sum or difference is undefined wherever ANY of the original fractions is, even if that factor cancels later.**"
     "\n• So read the restrictions off the original denominators, not the final answer."
     "\n• A simplified answer with too few restrictions is a different expression.",
     hint='Restrictions come from before, not after.')

card(C, '1/a + 1/b is not 1/(a + b)',
     "**Adding fractions never means adding numerators and denominators separately: 1/a + 1/b = (a + b)/(ab).**"
     "\n• 1/2 + 1/3 = 5/6, not 2/5."
     "\n• Testing with small numbers catches this every time.",
     hint='Try it with 2 and 3 before trusting it with x and y.')
same('(y + x)/(x*y)', E('1/x + 1/y'))

card(C, 'Compound fraction',
     "**A fraction with a rational expression in its numerator, its denominator, or both.**"
     "\n• (1/x + 1/y)/(2/x) is one."
     "\n• Some books call it a complex fraction.",
     hint='Fractions stacked inside a fraction.')

card(C, 'Simplifying a compound fraction',
     "**Multiply the top and the bottom by the LCM of every small denominator; the small fractions clear in one step.**"
     "\n• (1/x + 1/y)/(2/x): multiply top and bottom by xy to get (y + x)/(2y)."
     "\n• Alternatively, combine the top into one fraction, the bottom into one, and divide.",
     hint='One well-chosen multiplier clears every little fraction at once.')
same('(x + y)/(2y)', E('(1/x + 1/y)/(2/x)'))

card(C, 'Travel-time expressions',
     "**Time = distance ÷ rate, so a trip in two legs takes d₁/r₁ + d₂/r₂ — a sum of rational expressions.**"
     "\n• 12 miles at r mph and 12 miles back at r + 4 mph: 12/r + 12/(r + 4) = (24r + 48)/(r(r + 4))."
     "\n• Put the information in a distance–rate–time table first.",
     eq='t = d/r',
     hint='Add the TIMES, never the speeds.')
same('(24r + 48)/(r(r + 4))', E('12/r + 12/(r + 4)'))

card(C, 'Average speed is not the average of the speeds',
     "**Average speed = total distance ÷ total time, and the slower leg lasts longer, so it pulls the average down.**"
     "\n• 60 miles at 40 mph then 60 miles at 60 mph: 120 miles in 2.5 hours = 48 mph, not 50."
     "\n• That is a sum of two rational expressions in disguise.",
     hint='Total distance over total time — never the midpoint of the speeds.', frm='added')
assert sp.Rational(120) / (sp.Rational(60, 40) + 1) == 48

# ---- level 1 -----------------------------------------------------------------
_s = E('3x/(x + 2) + 6/(x + 2)')
same('3', _s)
for s_ in ('(3x + 6)/(2x + 4)', '3x + 6', '(3x + 6)/(x + 2)²'):
    differs(s_, _s)
# (3x + 6)/(2x + 4) is 3/2 — a genuinely different value, from adding the denominators.
q(Q, 1, 'Add and simplify: 3x/(x + 2) + 6/(x + 2).',
  ['3, for x ≠ −2', '(3x + 6)/(2x + 4)', '3x + 6', '(3x + 6)/(x + 2)²'], 0,
  'Same denominators: add the tops only.',
  ['Keep the denominator x + 2 and add the numerators: (3x + 6)/(x + 2).',
   'Factor the top: 3(x + 2).',
   '3(x + 2)/(x + 2) = 3.',
   'The sum is 3, for x ≠ −2.'],
  '**3, for x ≠ −2.** After adding the numerators, the top factors as 3(x + 2) and cancels with the bottom. (3x + 6)/(2x + 4) adds the denominators too, which halves the value, and (x + 2)² multiplies them.',
  'With like denominators, the denominator just comes along for the ride.')

_l = sp.lcm(x**2 - 4, x**2 + 4*x + 4)
assert sp.simplify(_l - (x - 2) * (x + 2)**2) == 0
q(Q, 1, 'What is the LCM of x² − 4 and x² + 4x + 4?',
  ['(x − 2)(x + 2)²', '(x − 2)(x + 2)', '(x − 2)(x + 2)³', '(x + 2)²'], 0,
  'Factor both, then take each factor the most times it appears in either one.',
  ['x² − 4 = (x − 2)(x + 2).',
   'x² + 4x + 4 = (x + 2)².',
   'x − 2 appears at most once; x + 2 appears at most twice (in the second).',
   'LCM = (x − 2)(x + 2)².'],
  '**(x − 2)(x + 2)².** Each factor appears as many times as it does in the polynomial that has the most of it. (x − 2)(x + 2)³ is the plain product, which counts the shared x + 2 three times; (x − 2)(x + 2) is not divisible by (x + 2)².',
  'The plain product is always a common multiple — just rarely the least.')

assert sp.lcm(6 * x**2 * y, 9 * x * y**3) == 18 * x**2 * y**3
q(Q, 1, 'What is the LCM of 6x²y and 9xy³?',
  ['18x²y³', '54x³y⁴', '18x³y⁴', '3xy'], 0,
  'Numbers first, then the highest power of each variable.',
  ['LCM of 6 and 9 is 18.',
   'The highest power of x is x².',
   'The highest power of y is y³.',
   'The LCM is 18x²y³.'],
  '**18x²y³.** Take the least common multiple of the numbers and the HIGHEST power of each variable. 54x³y⁴ is the plain product; 18x³y⁴ gets the number right but ADDS the exponents instead of taking the larger; 3xy is the greatest common FACTOR, the opposite idea.',
  'LCM takes the highest powers; GCF takes the lowest.')

_t = E('2/x + 3/y')
same('(2y + 3x)/(xy)', _t)
for s_ in ('(2x + 3y)/(xy)', '(2 + 3)/(x + y)', '(2 + 3)/(xy)'):
    differs(s_, _t)
q(Q, 1, 'What is 2/x + 3/y?',
  ['(2y + 3x)/(xy)', '(2x + 3y)/(xy)', '(2 + 3)/(x + y)', '(2 + 3)/(xy)'], 0,
  'The common denominator is xy. What does each fraction need to be multiplied by?',
  ['The LCD is xy.',
   '2/x needs a factor of y: 2y/(xy). 3/y needs a factor of x: 3x/(xy).',
   'Add the numerators.',
   '(2y + 3x)/(xy).'],
  '**(2y + 3x)/(xy).** Each numerator is multiplied by the factor its OWN denominator was missing, so the 2 picks up y and the 3 picks up x — (2x + 3y)/(xy) swaps them. (2 + 3)/(x + y) adds tops and bottoms separately, which fails even for numbers: 2/1 + 3/1 = 5, but 5/(1 + 1) = 2.5. (2 + 3)/(xy) uses the right denominator but never scales the numerators.',
  'Check any fraction rule with small numbers before using it.')
assert sp.Rational(5, 2) != 5

q(Q, 1, 'Which of these is a compound fraction?',
  ['(1/x − 2)/(x + 4)', '(x − 2)/(x + 4)', 'x² − 2x + 4', '(x − 2)(x + 4)'], 0,
  'Look for a fraction INSIDE a fraction.',
  ['A compound fraction has a rational expression in its numerator, denominator, or both.',
   '(1/x − 2)/(x + 4) has 1/x inside its numerator.',
   '(x − 2)/(x + 4) is an ordinary rational expression; the others are polynomials.',
   '(1/x − 2)/(x + 4) is the compound fraction.'],
  '**(1/x − 2)/(x + 4).** The 1/x sitting inside the numerator makes it compound. (x − 2)/(x + 4) is a single, ordinary rational expression — a fraction, but not one with a fraction inside it.',
  'Simplify a compound fraction by multiplying top and bottom by every small denominator.')

_s = E('(5x + 1)/(x − 3) − (2x + 10)/(x − 3)')
same('3', _s)
for s_ in ('(3x + 11)/(x − 3)', '(7x + 11)/(x − 3)', '(3x − 11)/(x − 3)'):
    differs(s_, _s)
q(Q, 1, 'Subtract and simplify: (5x + 1)/(x − 3) − (2x + 10)/(x − 3).',
  ['3, for x ≠ 3', '(3x + 11)/(x − 3)', '(7x + 11)/(x − 3)', '(3x − 11)/(x − 3)'], 0,
  'Put brackets round the second numerator before you subtract.',
  ['Same denominator, so subtract the numerators: (5x + 1) − (2x + 10).',
   'Distribute the minus: 5x + 1 − 2x − 10 = 3x − 9.',
   '3x − 9 = 3(x − 3), which cancels with the denominator.',
   'The difference is 3, for x ≠ 3.'],
  '**3, for x ≠ 3.** The minus applies to all of 2x + 10, giving 3x − 9 = 3(x − 3). (3x + 11) subtracts only the 2x and adds the 10, the classic missing-bracket slip; (7x + 11) adds instead of subtracting.',
  'Bracket the second numerator and the sign takes care of itself.')

assert sorted(sp.solve((x - 4) * (x + 1), x)) == [-1, 4]
q(Q, 1, 'For which values of x is 1/(x − 4) + 2/(x + 1) undefined?',
  ['x = 4 and x = −1', 'x = 4 only', 'x = −4 and x = 1', 'It is defined for every x'], 0,
  'Either fraction being undefined is enough.',
  ['1/(x − 4) is undefined at x = 4.',
   '2/(x + 1) is undefined at x = −1.',
   'The sum needs BOTH fractions to exist.',
   'It is undefined at x = 4 and x = −1.'],
  '**x = 4 and x = −1.** Each fraction contributes its own restriction. x = −4 and x = 1 read the signs straight out of the brackets without solving.',
  'Restrictions from every original denominator carry into the sum.')

# ---- level 2 -----------------------------------------------------------------
_s = E('2/(x² − 1) + 1/(x + 1)')
same('1/(x − 1)', _s)
for s_ in ('(x + 3)/(x² − 1)', '3/(x² + x)', '1/(x + 1)'):
    differs(s_, _s)
q(Q, 2, 'Add and simplify: 2/(x² − 1) + 1/(x + 1).',
  ['1/(x − 1)', '(x + 3)/(x² − 1)', '3/(x² + x)', '1/(x + 1)'], 0,
  'x² − 1 already contains x + 1. Use it as the LCD.',
  ['x² − 1 = (x − 1)(x + 1), which is the LCD.',
   '1/(x + 1) = (x − 1)/((x − 1)(x + 1)).',
   'Add the tops: 2 + x − 1 = x + 1.',
   '(x + 1)/((x − 1)(x + 1)) = 1/(x − 1), for x ≠ 1, −1.'],
  '**1/(x − 1).** After adding, the numerator x + 1 cancels with the LCD. (x + 3)/(x² − 1) multiplies the 1 by x + 1 instead of x − 1 — the factor it already had — and 3/(x² + x) adds tops and bottoms separately.',
  'Always factor the new numerator; here it is the whole simplification.')

_d = E('x/(x − 2) − 3/(x + 1)')
same('(x² − 2x + 6)/((x − 2)(x + 1))', _d)
for s_ in ('(x² − 2x − 6)/((x − 2)(x + 1))', '(x² + 4x − 6)/((x − 2)(x + 1))', '(x − 3)/(2x − 1)'):
    differs(s_, _d)
q(Q, 2, 'Subtract: x/(x − 2) − 3/(x + 1).',
  ['(x² − 2x + 6)/((x − 2)(x + 1))', '(x² − 2x − 6)/((x − 2)(x + 1))',
   '(x² + 4x − 6)/((x − 2)(x + 1))', '(x − 3)/(2x − 1)'], 0,
  'LCD (x − 2)(x + 1). Bracket the second numerator once it is scaled.',
  ['x/(x − 2) = x(x + 1)/((x − 2)(x + 1)) = (x² + x)/LCD.',
   '3/(x + 1) = 3(x − 2)/LCD = (3x − 6)/LCD.',
   'Subtract: x² + x − (3x − 6) = x² − 2x + 6.',
   '(x² − 2x + 6)/((x − 2)(x + 1)).'],
  '**(x² − 2x + 6)/((x − 2)(x + 1)).** Subtracting 3x − 6 turns the −6 into +6. Writing −6 is the missing-bracket slip; x² + 4x − 6 adds the 3x instead of subtracting; (x − 3)/(2x − 1) subtracts tops and bottoms separately.',
  'A − (B − C) = A − B + C. The second minus is the one people lose.')

_T = E('18/r + 18/(r − 3)')
same('(36r − 54)/(r(r − 3))', _T)
for s_ in ('36/(2r − 3)', '(36r − 54)/(2r − 3)', '36/(r(r − 3))'):
    differs(s_, _T)
q(Q, 2, 'You bike 18 miles out at r miles per hour and the same 18 miles back at r − 3 miles per hour. Which expression gives your total time in hours?',
  ['(36r − 54)/(r(r − 3))', '36/(2r − 3)', '(36r − 54)/(2r − 3)', '36/(r(r − 3))'], 0,
  'Time = distance ÷ rate for each leg, then add the two times.',
  ['Out: 18/r hours. Back: 18/(r − 3) hours.',
   'LCD: r(r − 3).',
   '18(r − 3) + 18r = 36r − 54 on top.',
   'Total time: (36r − 54)/(r(r − 3)).'],
  '**(36r − 54)/(r(r − 3)).** Each leg\'s time is its own distance over its own rate, and the two times add. 36/(2r − 3) adds the distances and adds the rates, which is the averaging-speeds mistake in algebraic form.',
  'Add times, never rates.')

_T = sp.Rational(18, 12) + sp.Rational(18, 9)
assert _T == sp.Rational(7, 2)
q(Q, 2, 'You bike 18 miles out at 12 miles per hour and 18 miles back at 9 miles per hour. How long does the round trip take?',
  ['3.5 hours', '3 hours', '4 hours', 'About 1.7 hours'], 0,
  'Find each leg\'s time separately.',
  ['Out: 18 ÷ 12 = 1.5 hours.',
   'Back: 18 ÷ 9 = 2 hours.',
   'Total: 1.5 + 2.',
   '3.5 hours.'],
  '**3.5 hours.** The slower leg takes longer, so it dominates. 3 hours uses the same 12 mph both ways, 4 hours uses 9 mph both ways, and 1.7 hours is 36 ÷ 21 — adding the speeds together as if they were one speed.',
  'Plug the speed into each leg, not into a blend of the two.')

_cf = E('(2/x − 3/y)/(1/(x*y))')
same('2y − 3x', _cf)
for s_ in ('2x − 3y', '(2y − 3x)/(x²y²)', '−1/(xy)'):
    differs(s_, _cf)
q(Q, 2, 'Simplify the compound fraction whose numerator is 2/x − 3/y and whose denominator is 1/(xy).',
  ['2y − 3x', '2x − 3y', '(2y − 3x)/(x²y²)', '−1/(xy)'], 0,
  'Multiply the top and the bottom by xy.',
  ['The LCM of x, y and xy is xy.',
   'Top: xy(2/x − 3/y) = 2y − 3x.',
   'Bottom: xy · 1/(xy) = 1.',
   'The compound fraction is 2y − 3x.'],
  '**2y − 3x.** Multiplying by xy clears all three small denominators at once: each fraction keeps the OTHER variable. 2x − 3y keeps the wrong variable on each term, and (2y − 3x)/(x²y²) multiplies by the bottom fraction instead of dividing.',
  'Each term loses its own denominator and gains the one it was missing.')

_L = sp.lcm(sp.lcm(x**2 - 3*x - 10, x**2 - 25), 2*x + 4)
assert sp.simplify(_L - 2 * (x - 5) * (x + 2) * (x + 5)) == 0
q(Q, 2, 'What is the LCM of x² − 3x − 10, x² − 25 and 2x + 4?',
  ['2(x − 5)(x + 2)(x + 5)', '(x − 5)(x + 2)(x + 5)', '2(x − 5)(x + 2)', '2(x − 5)²(x + 2)²(x + 5)'], 0,
  'Factor all three; then each distinct factor appears once here.',
  ['x² − 3x − 10 = (x − 5)(x + 2).',
   'x² − 25 = (x − 5)(x + 5).',
   '2x + 4 = 2(x + 2).',
   'Distinct factors 2, x − 5, x + 2, x + 5, each once: 2(x − 5)(x + 2)(x + 5).'],
  '**2(x − 5)(x + 2)(x + 5).** x − 5 and x + 2 each appear in two of the polynomials, but never twice in the SAME one, so each is used once. Forgetting the constant 2 from 2x + 4 is the easy slip; doubling the shared factors is the over-careful one.',
  'Constants are factors too.')

_P = E('2(3/x + 2/(x + 1))')
same('(10x + 6)/(x(x + 1))', _P)
for s_ in ('10/(2x + 1)', '(5x + 3)/(x(x + 1))', '(10x + 6)/(2x + 1)'):
    differs(s_, _P)
q(Q, 2, 'A rectangle has length 3/x and width 2/(x + 1). What is its perimeter?',
  ['(10x + 6)/(x(x + 1))', '10/(2x + 1)', '(5x + 3)/(x(x + 1))', '(10x + 6)/(2x + 1)'], 0,
  'Perimeter = 2(length + width). Add the two fractions first.',
  ['length + width = 3/x + 2/(x + 1).',
   'LCD x(x + 1): 3(x + 1) + 2x = 5x + 3 on top.',
   'Double it for the perimeter: 2(5x + 3) = 10x + 6.',
   'Perimeter = (10x + 6)/(x(x + 1)).'],
  '**(10x + 6)/(x(x + 1)).** (5x + 3)/(x(x + 1)) is length + width — only half the perimeter. The options over 2x + 1 add the denominators together, which no common denominator ever does.',
  'Perimeter goes round all four sides: two lengths and two widths.')

# ---- level 3 -----------------------------------------------------------------
_f = 1 / (1 / sp.Integer(30) + 1 / sp.Integer(15))
assert _f == 10
q(Q, 3, 'For a camera lens, 1/f = 1/dᵢ + 1/dₒ. An object 30 cm from the lens is in focus when the film is 15 cm behind it. What is the focal length f?',
  ['10 cm', '45 cm', '22.5 cm', '0.1 cm'], 0,
  'Add the two fractions, then flip.',
  ['1/f = 1/15 + 1/30.',
   'LCD 30: 2/30 + 1/30 = 3/30 = 1/10.',
   'If 1/f = 1/10, then f = 10.',
   'The focal length is 10 cm.'],
  '**10 cm.** The equation gives 1/f, so the last step is to take the reciprocal. 0.1 cm stops at 1/f; 45 cm adds the distances; 22.5 cm averages them.',
  'When the unknown sits in a denominator, finish by flipping.')

_s = E('1/(x + 3) + 6/(x² − 9)')
same('1/(x − 3)', _s)
q(Q, 3, 'A classmate writes 1/(x + 3) + 6/(x² − 9) = 1/(x − 3), for x ≠ 3. What, if anything, is wrong?',
  ['The restriction x ≠ −3 is missing; the original sum is undefined there',
   'Nothing: restrictions come from the simplified answer, which only needs x ≠ 3',
   'The sum is really 7/(x² − 9), found by adding the two numerators',
   'The answer should be 1/(x + 3), since the x − 3 factor cancels'], 0,
  'Check the original denominators, not the final one.',
  ['LCD (x + 3)(x − 3): (x − 3) + 6 = x + 3 on top.',
   '(x + 3)/((x + 3)(x − 3)) = 1/(x − 3), so the expression is right.',
   'But at x = −3 the original 1/(x + 3) is undefined.',
   'The answer needs x ≠ 3 AND x ≠ −3.'],
  '**The restriction x ≠ −3 is missing.** The simplification is correct, but the factor x + 3 cancelled away a value where the original sum does not exist. 7/(x² − 9) adds numerators without matching the denominators first.',
  'Read restrictions off the problem, never off the answer.')
differs('7/(x² − 9)', _s); differs('1/(x + 3)', _s)

_T = E('6/(r + 2) + 6/(r − 2)')
same('12r/(r² − 4)', _T)
for s_ in ('6/r', '12/(r² − 4)', '12r/(r² + 4)'):
    differs(s_, _T)
q(Q, 3, 'In still water you paddle at r miles per hour. A river\'s current is 2 miles per hour. You paddle 6 miles downstream and 6 miles back upstream. Which expression is your total time?',
  ['12r/(r² − 4)', '6/r', '12/(r² − 4)', '12r/(r² + 4)'], 0,
  'Downstream the current helps; upstream it fights you.',
  ['Downstream speed r + 2, so time 6/(r + 2).',
   'Upstream speed r − 2, so time 6/(r − 2).',
   'LCD (r + 2)(r − 2): 6(r − 2) + 6(r + 2) = 12r.',
   'Total time 12r/(r² − 4).'],
  '**12r/(r² − 4).** The ±2 cancel in the numerator but NOT in the denominator, which is why the round trip always takes longer than in still water. 6/r is the trap: it assumes the current helps on the way down exactly as much as it hurts on the way back.',
  'A current costs more time upstream than it saves downstream.')
assert sp.simplify(_T.subs(r, 4) - 12 / sp.Integer(4)) > 0

q(Q, 3, 'Why is it worth finding the LEAST common denominator rather than just multiplying all the denominators together?',
  ['Both work, but the LCD keeps the numerator smaller and easier to simplify',
   'Only the LCD gives a correct answer; any other gives a wrong sum',
   'The product of the denominators is never a common denominator at all',
   'The LCD gives fewer domain restrictions, so the answer is more general'], 0,
  'Try 1/6 + 1/15 both ways.',
  ['With 90 (6 × 15): 15/90 + 6/90 = 21/90, which reduces to 7/30.',
   'With 30 (the LCD): 5/30 + 2/30 = 7/30 directly.',
   'Same answer either way, but more simplifying with the bigger denominator.',
   'The L saves work; it does not change the result.'],
  '**Both work, but the LCD keeps the numbers smaller.** The plain product is always a common denominator and always gives a correct (if unsimplified) answer. And the restrictions come from the original fractions, so the choice of denominator cannot change them.',
  'With polynomials, the saving is bigger still: less to expand, less to factor.')
assert sp.Rational(21, 90) == sp.Rational(7, 30)

_cf = E('(x/(x − 2) − 1)/(4/(x² − 4))')
same('(x + 2)/2', _cf)
for s_ in ('(x − 2)/2', '2(x + 2)', '8/((x − 2)²(x + 2))'):
    differs(s_, _cf)
q(Q, 3, 'Simplify the compound fraction whose numerator is x/(x − 2) − 1 and whose denominator is 4/(x² − 4).',
  ['(x + 2)/2', '(x − 2)/2', '2(x + 2)', '8/((x − 2)²(x + 2))'], 0,
  'Combine the top into one fraction first, then divide.',
  ['Top: x/(x − 2) − (x − 2)/(x − 2) = 2/(x − 2).',
   'Divide: 2/(x − 2) ÷ 4/((x − 2)(x + 2)).',
   'Flip and multiply: 2/(x − 2) · (x − 2)(x + 2)/4.',
   'Cancel: (x + 2)/2, for x ≠ 2, −2.'],
  '**(x + 2)/2.** The top collapses to 2/(x − 2), because x − (x − 2) = 2 — the bracket matters again. 8/((x − 2)²(x + 2)) multiplies by the bottom fraction instead of dividing; 2(x + 2) inverts the 2 and the 4.',
  'Write 1 as (x − 2)/(x − 2) before subtracting it.')

_avg = sp.Rational(120) / (sp.Rational(60, 40) + sp.Rational(60, 60))
assert _avg == 48
q(Q, 3, 'You drive 60 miles at 40 miles per hour and then another 60 miles at 60 miles per hour. What is your average speed for the whole 120 miles?',
  ['48 mph', '50 mph', '45 mph', '52 mph'], 0,
  'Average speed = total distance ÷ total time.',
  ['First leg: 60 ÷ 40 = 1.5 hours.',
   'Second leg: 60 ÷ 60 = 1 hour.',
   'Total: 120 miles in 2.5 hours.',
   '120 ÷ 2.5 = 48 mph.'],
  '**48 mph.** 50 mph averages the two speeds, but you spend LONGER at 40 mph than at 60, so the slow leg counts for more. The times are rational expressions in the speeds, which is why the true average is not the midpoint.',
  'Equal distances do not mean equal times.', frm='added')

build('ad-astra', C, Q, 'unit-alg-t4-04',
      'Topic 4 · 4-4 Adding and Subtracting Rational Expressions', 'algeo',
      'Lesson 4-4 adds and subtracts rational expressions: with like denominators, finding the least common multiple of '
      'polynomials, rewriting over the least common denominator, subtracting with the minus distributed, simplifying '
      'compound fractions, and writing travel-time expressions as sums.',
      'Adding rational expressions is fraction arithmetic with polynomials in place of numbers, and it is the step every '
      'rational equation in 4-5 depends on. Travel, work and lens problems all reduce to adding terms of the form d/r.',
      [('Find the least common multiple of two or more polynomials', 'source'),
       ('Add and subtract rational expressions with like and unlike denominators, and state the domain', 'source'),
       ('Simplify a compound fraction', 'source'),
       ('Write and evaluate a sum of rational expressions for a travel-time situation', 'source')],
      'Three slips account for most lost marks. Adding the denominators (1/a + 1/b written as 2/(a + b)) — every such '
      'question here offers it, and a two-number check exposes it. Losing the minus sign on the second numerator when '
      'subtracting. And stating the domain from the simplified answer instead of the original denominators. The '
      'average-speed question is our addition: it is the classic real-world version of the same idea, and the answer is '
      'deliberately not the midpoint of the two speeds.',
      ('Start with the LCM cards — the rest of the lesson is built on them.', 22),
      'content/alg-topic4-04.json',
      'enVision Algebra 2, Lesson 4-4 (Drive)',
      'enVision Algebra 2 Lesson 4-4: Adding and Subtracting Rational Expressions',
      libv_=1)
finish('content/alg-topic4-04.json')

# ================================================================ 4-5
# Built from the lesson SLIDES alone (aga_24_a2_na_0405_lps.pptx): no 4-5 student-edition
# pages were in the folder. The slides carry the full lesson — vocabulary, all five worked
# examples, the concept summary and the practice prompts — so the lesson can be taught
# honestly, but every equation on them is an image, read by rendering it.
#
# One slide label is wrong, checked here: the intersection of 1/(x − 5) + x/(x − 3) and
# 2/(x² − 8x + 15) is labelled (−1, 0.063). Both sides equal 1/12 ≈ 0.083 at x = −1.
_fs, _gs = 1 / (x - 5) + x / (x - 3), 2 / (x**2 - 8 * x + 15)
assert _fs.subs(x, -1) == _gs.subs(x, -1) == sp.Rational(1, 12)
assert sol(_fs, _gs) == ([-1], [5])            # the slide's own solution, re-derived
# Jake's river: 16/(5 + c) + 1 = 6/(5 − c) has roots 3 and −25 — the slide is right.
assert sorted(sp.solve(sp.Eq(16 / (5 + c) + 1, 6 / (5 - c)), c)) == [-25, 3]
C, Q = [], []

card(C, 'Rational equation',
     "**An equation that contains at least one rational expression.**"
     "\n• 5/(x + 1) = 2 and x/(x − 3) + 1/x = 4 are both rational equations."
     "\n• Solving one usually means clearing the denominators first.",
     hint='A variable somewhere in a denominator.')

card(C, 'The method',
     "**State the excluded values, multiply every term on both sides by the LCD, solve the equation that is left, then throw out any solution that was excluded.**"
     "\n• Multiplying by the LCD clears every fraction in one step."
     "\n• Every term means every term — including the ones with no fraction.",
     hint='Domain first, clear, solve, then check against the domain.')

card(C, 'Extraneous solution',
     "**A value that solves the cleared equation but not the original, because it makes an original denominator zero.**"
     "\n• It appears honestly from the algebra — and must still be rejected."
     "\n• (x² + 3)/(x − 1) = 4/(x − 1) clears to x² + 3 = 4, so x = ±1; but x = 1 is excluded, leaving only x = −1.",
     hint='Solved the new equation, broke the old one.')
assert sol(E('(x² + 3)/(x − 1)'), E('4/(x − 1)')) == ([-1], [1])

card(C, 'Why extraneous solutions appear',
     "**Multiplying both sides by an expression that can equal zero lets in values the original equation forbids.**"
     "\n• At those values you multiplied by 0, and 0 = 0 balances anything."
     "\n• That is why the check is against the ORIGINAL equation.",
     hint='Multiplying by zero makes every equation true.')

card(C, 'Check in the original, not a middle step',
     "**Test each solution in the equation as first written; a later step has already lost the denominators that would reject it.**"
     "\n• An extraneous value satisfies every line after the fractions were cleared."
     "\n• Comparing it with the excluded values is the fastest check.",
     hint='Only the original still has the denominators that matter.')

card(C, 'When there is no solution',
     "**If every value the algebra produces is excluded, the equation has no solution.**"
     "\n• 2x/(x − 4) = 3 + 8/(x − 4) clears to 2x = 3x − 4, so x = 4 — which is excluded."
     "\n• \"No solution\" is a complete, correct answer.",
     hint='An empty answer is still an answer.')
assert sol(E('2x/(x − 4)'), E('3 + 8/(x − 4)')) == ([], [4])

card(C, 'The graphical view',
     "**Solving f(x) = g(x) means finding where the two graphs meet; an extraneous value is an x where at least one graph does not exist.**"
     "\n• Shown: y = 4/(x − 2) and y = 2 meet once, at x = 4."
     "\n• An excluded value sits on an asymptote or a hole, so no intersection can be there.",
     hint='No point on the graph, no intersection.')
_g1 = 4 / (x - 2)
assert sp.solve(sp.Eq(_g1, 2), x) == [4]
# No asymptote lines here: with two curves, a third series would cycle back to the
# curve's own colour and the asymptote x = 2 would read as part of the curve. The gap
# between the branches shows it on its own.
C[-1]['graph'] = rgraph([_g1, sp.Integer(2) + 0 * x], [-4, 8, -5, 6],
                        pts=[{'x': 4, 'y': 2, 'label': '(4, 2)'}])

card(C, 'Work rate',
     "**If a job takes t hours alone, the rate is 1/t of the job per hour, and people working together ADD their rates.**"
     "\n• 1/a + 1/b = 1/T, where T is the time together."
     "\n• A painter who takes 6 hours does 1/6 of the room each hour.",
     eq='1/a + 1/b = 1/T',
     hint='Add rates, never times.')

card(C, '"Twice as fast" means half the time',
     "**If one worker is twice as fast as another who takes x hours, the faster one takes x/2 hours — a rate of 2/x, not 1/(2x).**"
     "\n• Doubling the speed doubles the RATE and halves the TIME."
     "\n• Writing 2x for the faster worker's time is the commonest set-up error.",
     hint='Faster → less time.')

card(C, 'Current problems',
     "**With the current your speed is b + c; against it, b − c, where b is your speed in still water and c the current's.**"
     "\n• Each leg's time is distance ÷ that leg's speed."
     "\n• Write the equation from what the problem says about the TIMES — equal, or one an hour longer.",
     eq='t = d/(b + c),  t = d/(b − c)',
     hint='The current adds one way and subtracts the other.')

card(C, 'Rejected by the situation',
     "**A solution can satisfy the equation and still be impossible in context — a negative speed, time or length — and is rejected for that reason.**"
     "\n• This is different from an extraneous solution, which fails the equation's own domain."
     "\n• Your slides call both kinds \"extraneous\"; either way, it is not the answer.",
     hint='Ask whether the number could actually happen.')

card(C, 'Proportions',
     "**When each side is a single fraction, a/b = c/d, multiplying both sides by bd gives ad = bc — cross-multiplication is the LCD method in one step.**"
     "\n• With number-only denominators, multiply by their LCM to clear decimals and fractions."
     "\n• The excluded values still apply.",
     hint='Cross-multiplying is just clearing the denominators.')

# ---- level 1 -----------------------------------------------------------------
_v = sol(E('3/(x − 2)'), sp.Integer(6))
assert _v == ([sp.Rational(5, 2)], [])
assert sp.solve(sp.Eq(6 * x - 2, 3), x) == [sp.Rational(5, 6)]
q(Q, 1, 'Solve 3/(x − 2) = 6.',
  ['x = 5/2', 'x = 5/6', 'x = 4', 'x = 3/2'], 0,
  'Multiply both sides by x − 2.',
  ['x ≠ 2.',
   'Multiply by x − 2: 3 = 6(x − 2) = 6x − 12.',
   '6x = 15, so x = 15/6 = 5/2.',
   'x = 5/2 is not excluded, so it is the solution.'],
  '**x = 5/2.** Check: 3/(5/2 − 2) = 3/(1/2) = 6. x = 5/6 comes from writing 6x − 2 without distributing the 6 over the −2; x = 4 flips the fraction to x − 2 = 6/3.',
  'Distribute across the whole bracket after clearing.')

q(Q, 1, 'What is an extraneous solution of a rational equation?',
  ['A value the algebra produces that makes an original denominator zero',
   'Any solution of the equation that turns out to be a negative number',
   'A solution that is a fraction instead of a whole-number answer',
   'The second solution of an equation that has two solutions'], 0,
  'It comes out of the algebra but fails the original.',
  ['Clearing the denominators can produce new values.',
   'Some of them make an original denominator zero.',
   'Those are not in the domain, so they cannot solve the original.',
   'They are extraneous.'],
  '**A value the algebra produces that makes an original denominator zero.** Negative and fractional solutions are perfectly fine when they are in the domain. The test is the excluded values, not the size or sign of the number.',
  'Extraneous is about the domain, nothing else.')

q(Q, 1, 'You want to solve 5/(x + 1) + 2/x = 3. What is the most efficient first step after noting x ≠ −1 and x ≠ 0?',
  ['Multiply every term on both sides by x(x + 1)',
   'Subtract 3 from both sides, then cross-multiply',
   'Add the two numerators to get 7/(2x + 1)',
   'Multiply only the two fractions by x(x + 1)'], 0,
  'One multiplier can clear every denominator at once.',
  ['The LCD of x + 1 and x is x(x + 1).',
   'Multiply EVERY term by it — the 3 as well.',
   'That leaves 5x + 2(x + 1) = 3x(x + 1), with no fractions.',
   'Then solve and check.'],
  '**Multiply every term on both sides by x(x + 1).** Multiplying only the fractions breaks the equation, because the 3 has to be scaled too. 7/(2x + 1) adds tops and bottoms separately, which is never valid.',
  'Every term, both sides — including the plain numbers.')

assert set(sp.solve((x + 1) * (x - 6), x)) == {-1, 6}
q(Q, 1, 'Which values can never be solutions of 2/(x + 1) + x/(x − 6) = 3?',
  ['x = −1 and x = 6', 'x = 1 and x = −6', 'x = 0 only', 'x = 3 only'], 0,
  'Which inputs make a denominator zero?',
  ['x + 1 = 0 at x = −1.',
   'x − 6 = 0 at x = 6.',
   'At those values the original equation is undefined.',
   'x = −1 and x = 6 can never be solutions.'],
  '**x = −1 and x = 6.** Write them down before solving, so that an extraneous value is spotted the moment it appears. x = 1 and x = −6 read the signs out of the brackets without solving.',
  'List the excluded values first — it makes the final check instant.')

assert sol(1 / x + 3 / x, sp.Rational(1, 5)) == ([20], [])
q(Q, 1, 'Solve 1/x + 3/x = 1/5.',
  ['x = 20', 'x = 4/5', 'x = 15', 'x = 1/20'], 0,
  'Combine the left side first: same denominator.',
  ['1/x + 3/x = 4/x.',
   '4/x = 1/5.',
   'Multiply both sides by 5x: 20 = x.',
   'x = 20, which is not excluded.'],
  '**x = 20.** Check: 1/20 + 3/20 = 4/20 = 1/5. x = 1/20 stops one step short, at 1/x; x = 4/5 multiplies 4 by 1/5 as if x were in the numerator.',
  'When the unknown is in the denominator, the answer often comes out larger than the numbers you see.')

q(Q, 1, 'A painter can paint a room alone in 8 hours. What fraction of the room does the painter finish in one hour?',
  ['1/8', '8', '7/8', '1/16'], 0,
  'Rate = one job ÷ time for the job.',
  ['The whole job is 1 room.',
   'It takes 8 hours.',
   'Rate = 1 room ÷ 8 hours.',
   '1/8 of the room each hour.'],
  '**1/8.** In 8 hours at 1/8 per hour, the painter finishes 8 × 1/8 = 1 room. 7/8 is what is LEFT after the first hour, not what is done.',
  'Rates are what add when people work together.')

q(Q, 1, 'You graph y = f(x) and y = g(x). What do the solutions of f(x) = g(x) correspond to?',
  ['The x-coordinates of the points where the two graphs meet',
   'The x-intercepts of either of the two graphs separately',
   'The vertical asymptotes of the two graphs taken together',
   'The y-coordinates of the points where the two graphs meet'], 0,
  'At a solution, both sides give the same output for the same input.',
  ['A solution is an x for which f(x) and g(x) are equal.',
   'Equal outputs at the same input means a shared point on the two graphs.',
   'The solution is that point\'s x-coordinate.',
   'Solutions are the x-coordinates of the intersections.'],
  '**The x-coordinates of the intersections.** The y-coordinate is the value both sides share there, not the solution itself. A vertical asymptote is the one place a solution can NEVER be, because at least one graph does not exist there.',
  'An extraneous value always sits where a graph is missing.')

# ---- level 2 -----------------------------------------------------------------
assert sol(E('(x² + 5)/(x − 2)'), E('9/(x − 2)')) == ([-2], [2])
q(Q, 2, 'Solve (x² + 5)/(x − 2) = 9/(x − 2).',
  ['x = −2', 'x = 2 and x = −2', 'x = 2', 'No solution'], 0,
  'Note the excluded value before you clear the denominators.',
  ['x ≠ 2.',
   'Multiply both sides by x − 2: x² + 5 = 9.',
   'x² = 4, so x = 2 or x = −2.',
   'x = 2 is excluded, so the only solution is x = −2.'],
  '**x = −2.** Both ±2 solve x² = 4, but x = 2 makes the original denominators zero, so it is extraneous. Answering both forgets the check; answering "no solution" throws out the good one with the bad.',
  'Check each candidate on its own.')

assert sol(E('3x/(x + 2)'), E('1 + 6/(x + 2)')) == ([4], [])
assert sp.solve(sp.Eq(3 * x, 7), x) == [sp.Rational(7, 3)]
q(Q, 2, 'Solve 3x/(x + 2) = 1 + 6/(x + 2).',
  ['x = 4', 'x = 7/3', 'x = −2', 'No solution'], 0,
  'Multiply EVERY term by x + 2, the 1 included.',
  ['x ≠ −2.',
   'Multiply every term by x + 2: 3x = (x + 2) + 6.',
   '3x = x + 8, so 2x = 8 and x = 4.',
   'x = 4 is allowed, so it is the solution.'],
  '**x = 4.** Check: 12/6 = 2 and 1 + 6/6 = 2. x = 7/3 comes from forgetting to multiply the 1 by x + 2 (3x = 1 + 6). x = −2 is the excluded value, so it could never be the answer.',
  'The plain number is the term people forget to multiply.')

_l, _r = E('2/(x − 4) + x/(x − 1)'), E('6/((x − 4)(x − 1))')
assert sol(_l, _r) == ([-2], [4])
q(Q, 2, 'Solve 2/(x − 4) + x/(x − 1) = 6/((x − 4)(x − 1)).',
  ['x = −2', 'x = 4 and x = −2', 'x = 4', 'x = 2 and x = −4'], 0,
  'The LCD is already on the right: (x − 4)(x − 1).',
  ['x ≠ 4 and x ≠ 1.',
   'Multiply every term by (x − 4)(x − 1): 2(x − 1) + x(x − 4) = 6.',
   'x² − 2x − 8 = 0, so (x − 4)(x + 2) = 0.',
   'x = 4 is excluded; the solution is x = −2.'],
  '**x = −2.** The quadratic gives 4 and −2, and 4 makes two of the original denominators zero. x = 2 and x = −4 come from a sign slip in the factoring.',
  'Excluded values listed at the start make this check a glance.')

assert 1 / (sp.Rational(1, 6) + sp.Rational(1, 3)) == 2
q(Q, 2, 'Pipe A fills a tank in 6 hours and pipe B fills it in 3 hours. How long do they take together?',
  ['2 hours', '4.5 hours', '9 hours', '1/2 hour'], 0,
  'Add the rates, then flip the total rate into a time.',
  ['Rates: A does 1/6 of the tank per hour, B does 1/3.',
   'Together: 1/6 + 1/3 = 1/6 + 2/6 = 1/2 of the tank per hour.',
   'Half a tank per hour means the whole tank takes 2 hours.',
   'Together: 2 hours.'],
  '**2 hours.** Together they must be faster than the faster pipe alone, so any answer over 3 hours is impossible: 4.5 averages the times and 9 adds them. 1/2 hour stops at the combined RATE without turning it back into a time.',
  'Sanity check: together is always quicker than the quicker one alone.')

_X = sp.Symbol('X', positive=True)
assert sp.solve(sp.Eq(1 / _X + 2 / _X, sp.Rational(1, 10)), _X) == [30]
assert sp.solve(sp.Eq(1 / _X + 1 / (2 * _X), sp.Rational(1, 10)), _X) == [15]
q(Q, 2, 'Two printers together finish a job in 10 minutes. One prints twice as fast as the other. How long would the slower printer take on its own?',
  ['30 minutes', '15 minutes', '20 minutes', '5 minutes'], 0,
  'If the slower one takes x minutes, its rate is 1/x. Twice as fast is a rate of 2/x.',
  ['Slower rate: 1/x. Faster rate: 2/x (it takes x/2 minutes).',
   'Together: 1/x + 2/x = 1/10.',
   '3/x = 1/10, so x = 30.',
   'The slower printer takes 30 minutes; the faster takes 15.'],
  '**30 minutes.** 15 minutes is the FASTER printer\'s time — and it is also what you get by writing the faster printer\'s time as 2x, which makes it slower instead of faster. Twice as fast means half the time.',
  'Write rates, not times, and "twice as fast" can only mean 2/x.')

_b = sp.Symbol('b', positive=True)
assert sp.solve(sp.Eq(10 / (_b + 2), 6 / (_b - 2)), _b) == [8]
q(Q, 2, 'A boat travels 10 km downstream in the same time it takes to travel 6 km upstream. The current flows at 2 km/h. What is the boat\'s speed in still water?',
  ['8 km/h', '4 km/h', '16 km/h', '6 km/h'], 0,
  'Equal times: set distance ÷ speed equal for the two legs.',
  ['Downstream speed b + 2; upstream speed b − 2.',
   'Equal times: 10/(b + 2) = 6/(b − 2).',
   'Cross-multiply: 10(b − 2) = 6(b + 2), so 10b − 20 = 6b + 12.',
   '4b = 32, so b = 8 km/h.'],
  '**8 km/h.** Check: 10/10 = 1 hour and 6/6 = 1 hour. 16 km/h comes from 10b − 20 = 6b − 12 (a sign slip on the right), and 4 km/h divides 32 by 8 instead of by 4.',
  'Check both legs give the same time — it takes seconds.')
assert sp.solve(sp.Eq(10 * (_b - 2), 6 * (_b - 2)), _b) == [2]

_c1, _c2 = 6 / x, x - 1
assert sorted(sp.solve(sp.Eq(_c1, _c2), x)) == [-2, 3]
q(Q, 2, 'The graph shown plots y = 6/x and y = x − 1. What are the solutions of 6/x = x − 1?',
  ['x = 3 and x = −2', 'x = 2 and x = −3', 'x = 0 and x = 1', 'x = 3 only'], 0,
  'Read the x-coordinates of the crossing points.',
  ['The curve and the line cross twice.',
   'One crossing is at (3, 2); the other at (−2, −3).',
   'The solutions are the x-coordinates.',
   'x = 3 and x = −2. Algebra agrees: x² − x − 6 = 0, so (x − 3)(x + 2) = 0.'],
  '**x = 3 and x = −2.** 2 and −3 are the y-coordinates of the crossings, not the solutions. x = 0 is the curve\'s vertical asymptote and x = 1 is where the line crosses the x-axis; neither is a meeting point.',
  'Two crossing points, two solutions — the graph shows how many to expect.')
Q[-1]['graph'] = rgraph([_c1, _c2], [-6, 6, -6, 6], gy=2,
                        pts=[{'x': 3, 'y': 2, 'label': '(3, 2)'}, {'x': -2, 'y': -3, 'label': '(−2, −3)'}])

# ---- level 3 -----------------------------------------------------------------
assert sol(E('(x² + 1)/(x + 4)'), E('17/(x + 4)')) == ([4], [-4])
q(Q, 3, 'A classmate solves (x² + 1)/(x + 4) = 17/(x + 4), gets x² = 16, checks x = −4 in x² = 16, and says both x = 4 and x = −4 are solutions. What went wrong?',
  ['x = −4 was checked in a later step; in the original it makes the denominators 0',
   'Nothing is wrong: both 4 and −4 square to 16, so both are solutions',
   'x = 4 is the extraneous one, because it is the positive root',
   'The equation should have been cross-multiplied, giving x² + 1 = 17(x + 4)'], 0,
  'Where should a candidate be checked?',
  ['Clearing the denominators gives x² + 1 = 17, so x² = 16 and x = ±4.',
   'x² = 16 no longer has the denominators that forbid x = −4.',
   'In the original, x = −4 makes x + 4 = 0, so it is excluded.',
   'Only x = 4 is a solution.'],
  '**x = −4 was checked in the wrong place.** After clearing, the equation has lost the denominators that rule −4 out, so every line from there on will happily accept it. Check in the original, or simply against the excluded values listed at the start.',
  'A check is only as good as the equation you check it in.')

q(Q, 3, 'For 2/(x − 4) + x/(x − 1) = 6/((x − 4)(x − 1)), the algebra produces x = 4 and x = −2. Why do the graphs of the two sides not meet at x = 4?',
  ['Neither side has a value at x = 4, so there is no point there to share',
   'The two graphs do meet at x = 4, but only at a single point',
   'They meet at x = 4, but the point lies too far up to show',
   'At x = 4 the left side is 0 while the right side is undefined'], 0,
  'What happens to each side\'s denominators at x = 4?',
  ['On the left, 2/(x − 4) is undefined at x = 4.',
   'On the right, (x − 4)(x − 1) is 0 at x = 4.',
   'Neither graph has any point above x = 4 — both have an asymptote there.',
   'With no points, there is nothing to intersect, so x = 4 is extraneous.'],
  '**Neither side has a value at x = 4.** That is exactly what an extraneous solution looks like on a graph: a vertical line where at least one graph is missing. The graphs meet only once, at x = −2.',
  'Extraneous values hide on asymptotes and holes.')

assert sp.solve(sp.Eq(sp.Rational(1, 30) + sp.Rational(1, 60) + 1 / _X, sp.Rational(1, 15)), _X) == [60]
q(Q, 3, 'Ana can weed a garden alone in 30 minutes and Ben in 60 minutes. With Cara helping, the three finish in 15 minutes. How long would Cara take alone?',
  ['60 minutes', '15 minutes', '45 minutes', '20 minutes'], 0,
  'Add all three rates and set them equal to the rate together.',
  ['Rates: Ana 1/30, Ben 1/60, Cara 1/c, together 1/15 of the garden per minute.',
   '1/30 + 1/60 + 1/c = 1/15.',
   '2/60 + 1/60 + 1/c = 4/60, so 1/c = 1/60.',
   'Cara would take 60 minutes alone.'],
  '**60 minutes.** Ana and Ben together already do 3/60 per minute; the team needs 4/60, so Cara supplies 1/60. 45 minutes subtracts the times (60 − 15) as if times added; 20 minutes is Ana and Ben\'s combined time, not Cara\'s.',
  'Times never add or subtract in a work problem — rates do.')
assert 1 / (sp.Rational(1, 30) + sp.Rational(1, 60)) == 20

q(Q, 3, 'Why can multiplying both sides of a rational equation by the LCD create an extraneous solution?',
  ['The LCD can equal 0, and multiplying by 0 makes both sides balance at that value',
   'Every rational equation has exactly two solutions, and one is always false',
   'Multiplying by the LCD changes the signs of some of the solutions',
   'Multiplying by the LCD rounds some of the solutions to whole numbers'], 0,
  'What is special about multiplying both sides by zero?',
  ['At an excluded value, the LCD equals 0.',
   'Multiplying both sides by 0 gives 0 = 0, which is true.',
   'So the cleared equation can accept a value the original forbids.',
   'That value is extraneous, and only a check against the original catches it.'],
  '**Because the LCD can equal 0.** Multiplying by an expression is only reversible where it is nonzero. Where the LCD is zero, the new equation can be satisfied even though the original is undefined there. Plenty of rational equations have one solution, or none.',
  'This is why the excluded values are worth writing first.')

_l, _r = E('x/(x + 2) + 2/(x − 2)'), E('8/(x² − 4)')
assert sol(_l, _r) == ([], [-2, 2])
q(Q, 3, 'Solve x/(x + 2) + 2/(x − 2) = 8/(x² − 4).',
  ['No solution', 'x = 2 and x = −2', 'x = 2', 'x = 4'], 0,
  'x² − 4 = (x + 2)(x − 2) is the LCD.',
  ['Excluded: x ≠ 2 and x ≠ −2.',
   'Multiply every term by (x + 2)(x − 2): x(x − 2) + 2(x + 2) = 8.',
   'x² − 2x + 2x + 4 = 8, so x² = 4 and x = ±2.',
   'Both are excluded, so there is no solution.'],
  '**No solution.** Both candidates make a denominator zero. Answering with them is the check left undone; x = 4 stops at x² = 4 and reads off the 4.',
  'When every candidate is excluded, "no solution" is the full answer.')

_rr = sp.Symbol('rr')
assert sorted(sp.solve(sp.Eq(90 / _rr + 90 / (_rr + 15), 5), _rr)) == [-9, 30]
q(Q, 3, 'You drive 90 miles to a game and 90 miles home, driving 15 miles per hour faster on the way home. The round trip takes 5 hours of driving. How fast did you drive on the way there?',
  ['30 mph', '30 mph or −9 mph', '45 mph', '36 mph'], 0,
  'Time out + time back = 5, with time = distance ÷ speed.',
  ['Let r be the speed there: 90/r + 90/(r + 15) = 5.',
   'Multiply by r(r + 15): 90(r + 15) + 90r = 5r(r + 15).',
   '5r² − 105r − 1,350 = 0, so r² − 21r − 270 = 0, so (r − 30)(r + 9) = 0.',
   'r = −9 is impossible for a speed, so r = 30 mph.'],
  '**30 mph.** Check: 3 hours there and 90/45 = 2 hours back. −9 does solve the equation, but a speed cannot be negative, so the situation rejects it. 36 mph is 180 ÷ 5, the average speed for the whole trip, which is not the speed on either leg.',
  'After the algebra, ask whether each answer could actually happen.')

build('ad-astra', C, Q, 'unit-alg-t4-05',
      'Topic 4 · 4-5 Solving Rational Equations', 'algeo',
      'Lesson 4-5 solves rational equations by multiplying by a common denominator, identifies extraneous solutions that '
      'fall outside the original domain, and uses rational equations to solve work-rate and river-current problems.',
      'Rational equations are where the domain stops being a formality: a correct-looking answer can be wrong because it '
      'breaks the original equation. Work-rate and current problems show up again in physics and on standardised tests.',
      [('Solve a rational equation by clearing the denominators with the LCD', 'source'),
       ('Identify and reject extraneous solutions, including when there is no solution', 'source'),
       ('Set up and solve work-rate problems by adding rates', 'source'),
       ('Set up and solve current and travel problems, rejecting answers the situation does not allow', 'source')],
      'Built from the 4-5 lesson SLIDES only — there were no 4-5 textbook pages in the Topic 4 folder. The slides carry '
      'the whole lesson (vocabulary, five worked examples, the concept summary and practice prompts), so nothing here goes '
      'beyond them, but every number is fresh. Two things worth knowing: the slides call a negative current speed '
      '"extraneous", when strictly it is a valid solution of the equation that the situation rejects — the unit teaches '
      'both ideas and says the slides use one word for them. And one slide graph labels its intersection (−1, 0.063); '
      'both sides actually equal 1/12 ≈ 0.083 there. The biggest single trap is "twice as fast", which means half the '
      'time, not double it.',
      ('Start with the extraneous-solution cards — they are the heart of the lesson.', 22),
      'content/alg-topic4-05.json',
      'enVision Algebra 2, Lesson 4-5 presentation slides (Drive)',
      'enVision Algebra 2 Lesson 4-5: Solving Rational Equations (lesson slides; no textbook pages were provided)',
      libv_=1)
finish('content/alg-topic4-05.json')
