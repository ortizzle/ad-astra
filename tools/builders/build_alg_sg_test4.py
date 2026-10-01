#!/usr/bin/env python3
"""Algebra & Geometry II · Test 4 Study Guide, Part 1.

Source: "math study guide.test 4.pdf", Drive, Algebra & Geometry II folder,
uploaded 2026-09-30. Its header reads "Alg 2 SG T6 P1" (the ExamView file
name, as with Test 2's guide), ID: A, 34 numbered multiple-choice items.
A pure scan with NO text layer, so every page was rendered with pypdfium2
and read as an image.

Built exactly like unit-sgt1 / unit-sgt2: guide:true, so it gets the paper
entry grid, instant grading, the walkthrough and a rescue round. Option
order is the PAPER'S, letter for letter, which is why this builder does not
go through unit_common.build() — that calls _balance(), which would reorder
the options and make the app's C stop being the paper's C.

THE UPLOAD IS MISSING A PAGE. Scan pages 2 and 3 are two photos of the
paper's page 3, so the paper's page 2 — questions 9 through 19 — never
arrived. Nothing was invented for them. Each question carries `paperNo`, so
the entry grid shows the printout's own numbers (1-8, 20-30, 32-34) rather
than renumbering 1..n. When page 2 is uploaded, its questions slot in by
paperNo and libv is bumped.

QUESTION 31 HAS TWO RIGHT ANSWERS ON THE PAPER. Options b ("-3, 3, 4") and
c ("3, -3, 4") list the same three zeros and show what is, rendered and
zoomed, the same graph. A single-answer grid would mark one of two correct
letters wrong, so #31 is not graded here; a card teaches its zeros instead.

There is no answer key in the upload. Every answer below was derived
independently with sympy and asserted before it is written, and so was every
rescue variant. Two items are adapted: #24 is fill-in-the-blank on paper
(three blanks, so it is asked as one multiple-choice question about the
remainder), and #27/#30 offer GRAPHS as options, each labelled with its
answer, so the options here are those labels.
"""
import io, json, os, sys, time
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, REPO

x = sp.symbols('x')
I = sp.I

# ------------------------------------------------------------- verification
def vertex(a, b, c):
    h = sp.Rational(-b, 2 * a)
    return h, a * h**2 + b * h + c

assert vertex(-2, 8, -20) == (2, -12)           # 1
assert vertex(2, 24, -16) == (-6, -88)          # 2
assert vertex(2, 28, -8) == (-7, -106)          # 3: minimum -106
assert vertex(-2, 28, -10) == (7, 88)           # 4: maximum 88
assert sp.expand((x - 1)**2 + 7) == x**2 - 2*x + 8                      # 5
assert sp.expand((x + 6)*(x + 8)) == x**2 + 14*x + 48                   # 6
assert sp.expand((x - 2)*(x - 4)) == x**2 - 6*x + 8                     # 7
assert sp.expand(2*(x + 3)*(x + 5)) == 2*x**2 + 16*x + 30               # 8
assert set(sp.solve(sp.Rational(1, 2)*x**2 - x + 5, x)) == {1 + 3*I, 1 - 3*I}   # 20: 1 ± √9 i
assert sp.sqrt(-144) == 12*I                                            # 21
assert sp.sqrt(-360) == 6*sp.sqrt(10)*I                                 # 22
P23 = x**4 + 9*x**3 - 9*x + 2
assert P23.subs(x, -2) == -36                                           # 23
P24 = x**3 + x**2 - 4*x - 5
assert sp.rem(P24, x - 2) == -1 and P24.subs(x, 2) == -1                # 24
assert set(sp.solve(x**3 - 8, x)) == {2, -1 + sp.sqrt(3)*I, -1 - sp.sqrt(3)*I}       # 25
assert set(sp.solve(x**3 - 216, x)) == {6, -3 + 3*sp.sqrt(3)*I, -3 - 3*sp.sqrt(3)*I}  # 26
assert sp.discriminant(x**2 + 2*x + 2) < 0                              # 27: no real solution
assert sp.roots(4*x**3 - 12*x**2 - 16*x) == {0: 1, 4: 1, -1: 1}         # 28
assert sp.roots(x**4 - 4*x**3 + 3*x**2) == {0: 2, 1: 1, 3: 1}           # 29
assert sp.roots(sp.expand(x*(x - 2)*(x + 5))) == {0: 1, 2: 1, -5: 1}    # 30
assert sp.roots(sp.expand((x + 3)*(x - 3)*(x - 4))) == {-3: 1, 3: 1, 4: 1}  # 31 (card only)
assert sp.degree(-12*x**2 - 25*x + 5 + x**3) == 3                       # 32
assert sp.degree(2*x**4 - x**3 - 12*x**2 - 25*x + 5) == 4               # 33
def in34(px, py): return 3*px + 3*py <= 45 and 2*px + py <= 20 and px >= 0 and py >= 0
assert [in34(*p) for p in [(12, 1), (5, 4), (2, 15), (10, 4)]] == [False, True, False, False]  # 34

# variants — fresh numbers, same skill
assert vertex(-3, 12, -7) == (2, 5)
assert vertex(3, 18, -4) == (-3, -31)
assert vertex(2, 20, 3) == (-5, -47)
assert vertex(-3, 24, -5) == (4, 43)
assert sp.expand((x - 3)**2 + 2) == x**2 - 6*x + 11
assert sp.expand((x + 3)*(x + 8)) == x**2 + 11*x + 24
assert sp.expand((x - 2)*(x - 7)) == x**2 - 9*x + 14
assert sp.expand(3*(x + 2)*(x + 5)) == 3*x**2 + 21*x + 30
assert set(sp.solve(sp.Rational(1, 2)*x**2 + 2*x + 10, x)) == {-2 + 4*I, -2 - 4*I}
assert sp.sqrt(-81) == 9*I
assert sp.sqrt(-200) == 10*sp.sqrt(2)*I
assert (x**4 + 5*x**3 - 3*x + 4).subs(x, -1) == 3
assert (x**3 - 2*x**2 + 3*x - 4).subs(x, 3) == 14
assert set(sp.solve(x**3 - 27, x)) == {3, sp.Rational(-3, 2) + 3*sp.sqrt(3)*I/2, sp.Rational(-3, 2) - 3*sp.sqrt(3)*I/2}
assert set(sp.solve(x**3 - 64, x)) == {4, -2 + 2*sp.sqrt(3)*I, -2 - 2*sp.sqrt(3)*I}
assert sp.discriminant(x**2 - 4*x + 5) < 0 and vertex(1, -4, 5) == (2, 1)
assert sp.roots(3*x**3 + 3*x**2 - 18*x) == {0: 1, -3: 1, 2: 1}
assert sp.roots(x**4 + 2*x**3 - 8*x**2) == {0: 2, -4: 1, 2: 1}
assert sp.roots(sp.expand(x*(x + 3)*(x - 4))) == {0: 1, -3: 1, 4: 1}
assert sp.degree(x**4 - 3*x**2 + 7 - 2*x**5) == 5
assert sp.degree(6 - x**2 + 4*x**3) == 3
def inV(px, py): return px + py <= 10 and 3*px + py <= 18 and px >= 0 and py >= 0
assert [inV(*p) for p in [(4, 5), (6, 2), (1, 10), (5, 5)]] == [True, False, False, False]

# ------------------------------------------------------------------ helpers
Q = []
def g(n, lv, text, opts, ans, hint, steps, main, tip, var, frm='source'):
    """One guide question. `opts` are the PAPER'S options in the paper's
    order; `ans` is the paper's letter as an index. `var` is the rescue
    variant: (q, opts, ans, hint, steps, main)."""
    assert len(opts) == 4 and len(set(opts)) == 4 and 0 <= ans < 4, n
    assert 3 <= len(steps) <= 6, n
    vq, vo, va, vh, vs, vm = var
    assert len(vo) == 4 and len(set(vo)) == 4 and 0 <= va < 4 and 3 <= len(vs) <= 6, n
    Q.append({'id': 'q%d' % n, 'paperNo': n, 'lv': lv, 'from': frm, 'kind': 'mc',
              'q': 'SG #%d — %s' % (n, text), 'opts': opts, 'ans': ans,
              'hint': hint, 'steps': steps, 'ex': {'main': main, 'tip': tip},
              'variant': {'q': vq, 'opts': vo, 'ans': va, 'hint': vh, 'steps': vs,
                          'ex': {'main': vm}}})

VX = 'Find the axis first: x = −b ÷ 2a. Then substitute it back in for the y-coordinate.'

g(1, 1, "What are the vertex and the axis of symmetry of y = −2x² + 8x − 20?",
  ["vertex: (−2, 12); axis of symmetry: y = −2", "vertex: (2, −12); axis of symmetry: x = 2",
   "vertex: (−2, −12); axis of symmetry: x = −2", "vertex: (2, −12); axis of symmetry: x = −12"], 1,
  VX,
  ["a = −2 and b = 8, so x = −8 ÷ (2 × −2) = −8 ÷ −4 = 2.",
   "Substitute x = 2: y = −2(4) + 8(2) − 20 = −8 + 16 − 20 = −12.",
   "The axis of symmetry is the vertical line through the vertex, x = 2 — always 'x =', never 'y ='.",
   "Vertex (2, −12), axis x = 2."],
  "**Vertex (2, −12), axis of symmetry x = 2.** The axis is a vertical line through the vertex, so it is always written x = (the vertex's x-coordinate).",
  "Two traps on one item: an axis written 'y =', and an axis using the vertex's y-value.",
  ("What are the vertex and the axis of symmetry of y = −3x² + 12x − 7?",
   ["vertex: (2, 5); axis of symmetry: x = 2", "vertex: (−2, 5); axis of symmetry: x = −2",
    "vertex: (2, 5); axis of symmetry: y = 2", "vertex: (2, −5); axis of symmetry: x = 5"], 0, VX,
   ["x = −12 ÷ (2 × −3) = 2.", "y = −3(4) + 24 − 7 = 5.", "Vertex (2, 5), axis x = 2."],
   "**Vertex (2, 5), axis x = 2.**"))

g(2, 1, "What are the vertex and the axis of symmetry of y = 2x² + 24x − 16?",
  ["vertex: (−6, −88); axis of symmetry: x = −6", "vertex: (−6, 88); axis of symmetry: y = −6",
   "vertex: (6, −88); axis of symmetry: x = −88", "vertex: (−6, −88); axis of symmetry: x = −88"], 0,
  VX,
  ["x = −24 ÷ (2 × 2) = −6.",
   "y = 2(36) + 24(−6) − 16 = 72 − 144 − 16 = −88.",
   "The axis passes through the vertex's x-coordinate: x = −6.",
   "Vertex (−6, −88), axis x = −6."],
  "**Vertex (−6, −88), axis of symmetry x = −6.** Two options share the right vertex; only one pairs it with the right axis.",
  "Once you have the vertex, the axis is free — x equals its first coordinate.",
  ("What are the vertex and the axis of symmetry of y = 3x² + 18x − 4?",
   ["vertex: (−3, −31); axis of symmetry: x = −3", "vertex: (3, −31); axis of symmetry: x = 3",
    "vertex: (−3, 31); axis of symmetry: y = −3", "vertex: (−3, −31); axis of symmetry: x = −31"], 0, VX,
   ["x = −18 ÷ 6 = −3.", "y = 27 − 54 − 4 = −31.", "Vertex (−3, −31), axis x = −3."],
   "**Vertex (−3, −31), axis x = −3.**"))

MM = "The sign of a decides it: a > 0 opens up (a minimum), a < 0 opens down (a maximum). The value is the vertex's y."
g(3, 2, "What is the maximum or minimum value of y = 2x² + 28x − 8, and what is the range?",
  ["minimum value: 7; range: y ≥ 7", "minimum value: −7; range: y ≥ −7",
   "minimum value: −106; range: y ≥ −106", "minimum value: −106; range: y ≥ −7"], 2,
  MM,
  ["a = 2 > 0, so the parabola opens up and has a minimum.",
   "Vertex x = −28 ÷ 4 = −7; y = 2(49) + 28(−7) − 8 = 98 − 196 − 8 = −106.",
   "The minimum VALUE is the y-coordinate, −106 — not the x-coordinate, −7.",
   "Range: every y from −106 up, so y ≥ −106."],
  "**Minimum −106, range y ≥ −106.** The minimum is a y-value, and the range starts at that same y-value.",
  "−7 is where the minimum happens, not what it is.",
  ("What is the maximum or minimum value of y = 2x² + 20x + 3, and what is the range?",
   ["minimum value: −47; range: y ≥ −47", "minimum value: 3; range: y ≥ 3",
    "minimum value: 47; range: y ≥ 47", "minimum value: −47; range: y ≥ 3"], 0, MM,
   ["a = 2 > 0: a minimum.", "x = −20 ÷ 4 = −5; y = 50 − 100 + 3 = −47.", "Minimum −47, range y ≥ −47."],
   "**Minimum −47, range y ≥ −47.**"))

g(4, 2, "What is the maximum or minimum value of y = −2x² + 28x − 10, and what is the range?",
  ["minimum: −88; range: y ≥ −88", "minimum: 88; range: y ≥ 88",
   "maximum: 88; range: y ≤ 88", "maximum: −88; range: y ≤ −88"], 2,
  MM,
  ["a = −2 < 0, so the parabola opens down and has a maximum.",
   "Vertex x = −28 ÷ (2 × −2) = 7; y = −2(49) + 28(7) − 10 = −98 + 196 − 10 = 88.",
   "A maximum caps the range from above: y ≤ 88.",
   "Maximum 88, range y ≤ 88."],
  "**Maximum 88, range y ≤ 88.** A negative a means the vertex is the highest point, so the range runs downward from it.",
  "Decide max or min from the sign of a before doing any arithmetic.",
  ("What is the maximum or minimum value of y = −3x² + 24x − 5, and what is the range?",
   ["maximum: 43; range: y ≤ 43", "minimum: 43; range: y ≥ 43",
    "maximum: −43; range: y ≤ −43", "minimum: −43; range: y ≥ −43"], 0, MM,
   ["a = −3 < 0: a maximum.", "x = −24 ÷ (−6) = 4; y = −48 + 96 − 5 = 43.", "Maximum 43, range y ≤ 43."],
   "**Maximum 43, range y ≤ 43.**"))

CS = "Halve the x-coefficient and square it to complete the square; whatever you add, you also subtract."
g(5, 1, "What is the vertex form of y = x² − 2x + 8?",
  ["y = (x + 1)² + 7", "y = (x + 1)² − 7", "y = (x − 1)² + 7", "y = (x − 1)² − 7"], 2,
  CS,
  ["Half of −2 is −1, and (−1)² = 1.",
   "y = (x² − 2x + 1) + 8 − 1.",
   "y = (x − 1)² + 7.",
   "Check: the vertex is (1, 7), and 1 − 2 + 8 = 7. ✓"],
  "**y = (x − 1)² + 7.** The sign inside the bracket is the sign of half the x-coefficient: −2x gives (x − 1).",
  "Check vertex form by plugging the vertex's x into the original: 1 − 2 + 8 = 7.",
  ("What is the vertex form of y = x² − 6x + 11?",
   ["y = (x − 3)² + 2", "y = (x + 3)² + 2", "y = (x − 3)² − 2", "y = (x + 3)² − 2"], 0, CS,
   ["Half of −6 is −3; (−3)² = 9.", "y = (x² − 6x + 9) + 11 − 9.", "y = (x − 3)² + 2."],
   "**y = (x − 3)² + 2.**"))

FX = "Find two numbers that MULTIPLY to the constant and ADD to the x-coefficient."
g(6, 1, "What is x² + 14x + 48 in factored form?",
  ["(x + 6)(x − 8)", "(x + 8)(x − 6)", "(x − 8)(x − 6)", "(x + 6)(x + 8)"], 3,
  FX,
  ["We need two numbers with product 48 and sum 14.",
   "Both are positive, since the product and the sum are both positive.",
   "6 × 8 = 48 and 6 + 8 = 14.",
   "(x + 6)(x + 8)."],
  "**(x + 6)(x + 8).** A positive constant and a positive middle term means both numbers are positive.",
  "Expand your answer to check: x² + 8x + 6x + 48.",
  ("What is x² + 11x + 24 in factored form?",
   ["(x + 3)(x + 8)", "(x − 3)(x + 8)", "(x + 3)(x − 8)", "(x − 3)(x − 8)"], 0, FX,
   ["Product 24, sum 11.", "3 × 8 = 24 and 3 + 8 = 11.", "(x + 3)(x + 8)."],
   "**(x + 3)(x + 8).**"))

g(7, 1, "What is x² − 6x + 8 in factored form?",
  ["(x + 4)(x + 2)", "(x − 2)(x − 4)", "(x − 4)(x + 2)", "(x − 2)(x + 4)"], 1,
  FX,
  ["We need product +8 and sum −6.",
   "A positive product with a negative sum means BOTH numbers are negative.",
   "(−2)(−4) = 8 and −2 + (−4) = −6.",
   "(x − 2)(x − 4)."],
  "**(x − 2)(x − 4).** Positive constant, negative middle term: both signs are minus.",
  "Read the two signs first; they narrow four options to one before any arithmetic.",
  ("What is x² − 9x + 14 in factored form?",
   ["(x − 2)(x − 7)", "(x + 2)(x + 7)", "(x − 2)(x + 7)", "(x + 2)(x − 7)"], 0, FX,
   ["Product +14, sum −9: both negative.", "(−2)(−7) = 14, −2 − 7 = −9.", "(x − 2)(x − 7)."],
   "**(x − 2)(x − 7).**"))

g(8, 2, "What is 2x² + 16x + 30 in factored form?",
  ["2(x − 3)(x − 5)", "2(x − 3)(x + 5)", "2(x + 3)(x − 5)", "2(x + 3)(x + 5)"], 3,
  "Take out the common factor first, then factor what is left.",
  ["Every term is even, so factor out 2: 2(x² + 8x + 15).",
   "Inside: product 15, sum 8 — both positive.",
   "3 × 5 = 15 and 3 + 5 = 8.",
   "2(x + 3)(x + 5)."],
  "**2(x + 3)(x + 5).** Pull out the GCF first; the trinomial left inside is an ordinary one.",
  "Forgetting the 2 changes the polynomial — keep it out front.",
  ("What is 3x² + 21x + 30 in factored form?",
   ["3(x + 2)(x + 5)", "3(x − 2)(x − 5)", "3(x + 2)(x − 5)", "3(x − 2)(x + 5)"], 0,
   "Take out the common factor first.",
   ["Factor out 3: 3(x² + 7x + 10).", "2 × 5 = 10 and 2 + 5 = 7.", "3(x + 2)(x + 5)."],
   "**3(x + 2)(x + 5).**"))

QF = "Clear the fraction first (multiply through), then use the quadratic formula. A negative discriminant gives ± something times i."
g(20, 2, "Find the solutions of the equation ½x² − x + 5 = 0.",
  ["1 ± √9 i", "−1 ± √9 i", "1 ± √11 i", "−1 ± √11 i"], 0,
  QF,
  ["Multiply every term by 2: x² − 2x + 10 = 0.",
   "Discriminant: b² − 4ac = 4 − 40 = −36.",
   "x = (2 ± √−36) ÷ 2 = (2 ± 6i) ÷ 2 = 1 ± 3i.",
   "3i is √9 i, which is how the paper writes it: 1 ± √9 i."],
  "**1 ± √9 i** — that is 1 ± 3i. The paper leaves √9 unsimplified, so recognise 3i in either form.",
  "The real part is −b ÷ 2a = 2 ÷ 2 = 1, which rules out the two options starting −1.",
  ("Find the solutions of the equation ½x² + 2x + 10 = 0.",
   ["−2 ± 4i", "2 ± 4i", "−2 ± 2i", "−4 ± 2i"], 0, QF,
   ["Multiply by 2: x² + 4x + 20 = 0.", "Discriminant: 16 − 80 = −64.", "x = (−4 ± 8i) ÷ 2 = −2 ± 4i."],
   "**−2 ± 4i.**"))

SQ = "Split off −1 as i, then take out the largest perfect square."
g(21, 1, "Simplify √−144 using the imaginary unit i.",
  ["12", "−12", "12i", "144i"], 2,
  SQ,
  ["√−144 = √144 × √−1.", "√144 = 12 and √−1 = i.", "12i."],
  "**12i.** The square root of a negative number is never a real number, so 12 and −12 are out.",
  "√−n = i√n for any positive n.",
  ("Simplify √−81 using the imaginary unit i.", ["9i", "9", "−9", "81i"], 0, SQ,
   ["√−81 = √81 × √−1.", "√81 = 9, √−1 = i.", "9i."], "**9i.**"))

g(22, 2, "Simplify √−360 using the imaginary unit i.",
  ["6√−10", "6i√10", "i√360", "−6√10"], 1,
  SQ,
  ["√−360 = i√360.",
   "360 = 36 × 10, and 36 is the largest perfect square in it.",
   "i√360 = i × 6 × √10 = 6i√10.",
   "Simplified form puts i outside and leaves no perfect square under the root: 6i√10."],
  "**6i√10.** Two other options are EQUAL to it but not simplified: 6√−10 still has a negative under the root, and i√360 still holds a perfect square.",
  "\"Simplify\" means no negative and no perfect-square factor left inside the radical.",
  ("Simplify √−200 using the imaginary unit i.", ["10i√2", "−10√2", "2i√10", "20i√5"], 0, SQ,
   ["√−200 = i√200.", "200 = 100 × 2.", "10i√2."], "**10i√2.**"))

SD = "The remainder from synthetic division by (x − k) equals P(k). Remember a 0 for any missing power."
g(23, 2, "Use synthetic division to find P(−2) for P(x) = x⁴ + 9x³ − 9x + 2.",
  ["−2", "0", "−36", "68"], 2,
  SD,
  ["P has no x² term, so the coefficients are 1, 9, 0, −9, 2 — the 0 is essential.",
   "Divide by −2: bring down 1; 1 × −2 = −2, 9 − 2 = 7; 7 × −2 = −14, 0 − 14 = −14; −14 × −2 = 28, −9 + 28 = 19; 19 × −2 = −38, 2 − 38 = −36.",
   "The remainder is −36, so P(−2) = −36.",
   "Check directly: 16 − 72 + 18 + 2 = −36. ✓"],
  "**−36.** The missing x² term needs a 0 placeholder, or every number after it shifts.",
  "Plugging in directly is a fast check on synthetic division.",
  ("Use synthetic division to find P(−1) for P(x) = x⁴ + 5x³ − 3x + 4.", ["3", "7", "13", "−3"], 0, SD,
   ["Coefficients 1, 5, 0, −3, 4 (0 for the missing x²).", "Divide by −1: 1, 4, −4, 1, 3.", "P(−1) = 3."],
   "**3.**"))

g(24, 2, "(adapted — the paper has three blanks to fill in) By the Remainder Theorem, when P(x) = x³ + x² − 4x − 5 is divided by x − 2, the remainder is P(2). What is that remainder?",
  ["1", "−1", "−9", "−5"], 1,
  "Dividing by x − 2 means evaluating at x = +2.",
  ["Dividing by x − 2 means k = 2.",
   "P(2) = 8 + 4 − 8 − 5 = −1.",
   "Synthetic division with 1, 1, −4, −5 by 2 gives 1, 3, 2 and a remainder of −1.",
   "Both give −1, so the remainder is −1, P(2) = −1, and yes, the theorem is verified."],
  "**−1.** The division and the substitution land on the same number, which is exactly what the Remainder Theorem promises.",
  "On the paper: remainder −1, P(2) = −1, and \"yes\".",
  ("By the Remainder Theorem, what is the remainder when P(x) = x³ − 2x² + 3x − 4 is divided by x − 3?",
   ["14", "−14", "−58", "4"], 0,
   "Dividing by x − 3 means evaluating at x = 3.",
   ["k = 3.", "P(3) = 27 − 18 + 9 − 4 = 14.", "The remainder is 14."], "**14.**"),
  frm='added')

CU = "Factor the cubic: one real root, then the quadratic formula on the leftover quadratic for the complex pair."
g(25, 3, "What are all the real and complex solutions of x³ − 8 = 0?",
  ["1 + i√3 and 1 − i√3", "2, −1 + i√3, and −1 − i√3",
   "2, 1 + 2i√3, and 1 − 2i√3", "2, 2 + 2i√3, and 2 − 2i√3"], 1,
  CU,
  ["2³ = 8, so x = 2 is a root and (x − 2) is a factor.",
   "x³ − 8 = (x − 2)(x² + 2x + 4).",
   "x² + 2x + 4 = 0: x = (−2 ± √(4 − 16)) ÷ 2 = (−2 ± 2i√3) ÷ 2 = −1 ± i√3.",
   "All three: 2, −1 + i√3, −1 − i√3."],
  "**2, −1 + i√3, and −1 − i√3.** A cubic has three solutions; the option with only two is missing the real one.",
  "Difference of cubes: a³ − b³ = (a − b)(a² + ab + b²).",
  ("What are all the real and complex solutions of x³ − 27 = 0?",
   ["3, −3/2 + (3√3/2)i, and −3/2 − (3√3/2)i", "3, 3/2 + (3√3/2)i, and 3/2 − (3√3/2)i",
    "−3, 3/2 + (3√3/2)i, and 3/2 − (3√3/2)i", "3, −3 + 3i√3, and −3 − 3i√3"], 0, CU,
   ["x = 3 is a root; x³ − 27 = (x − 3)(x² + 3x + 9).",
    "x = (−3 ± √(9 − 36)) ÷ 2 = (−3 ± 3i√3) ÷ 2.",
    "3, −3/2 ± (3√3/2)i."],
   "**3, −3/2 + (3√3/2)i, −3/2 − (3√3/2)i.**"))

g(26, 3, "What are all the real and complex solutions of x³ = 216?",
  ["−6, 3 + 3i√7, and 3 − 3i√7", "−6, 3 + 3i√3, and 3 − 3i√3",
   "6, 3 + 3i√7, and 3 − 3i√7", "6, −3 + 3i√3, and −3 − 3i√3"], 3,
  CU,
  ["6³ = 216, so x = 6 (positive — the cube root of a positive number is positive).",
   "x³ − 216 = (x − 6)(x² + 6x + 36).",
   "x = (−6 ± √(36 − 144)) ÷ 2 = (−6 ± √−108) ÷ 2 = (−6 ± 6i√3) ÷ 2 = −3 ± 3i√3.",
   "6, −3 + 3i√3, −3 − 3i√3."],
  "**6, −3 + 3i√3, and −3 − 3i√3.** √108 = √36 × √3 = 6√3, and the real part of the pair is −b ÷ 2a = −3.",
  "The complex pair's real part is negative here because the quadratic's middle term is +6x.",
  ("What are all the real and complex solutions of x³ = 64?",
   ["4, −2 + 2i√3, and −2 − 2i√3", "−4, 2 + 2i√3, and 2 − 2i√3",
    "4, 2 + 2i√3, and 2 − 2i√3", "4, −2 + 2i√7, and −2 − 2i√7"], 0, CU,
   ["x = 4; x³ − 64 = (x − 4)(x² + 4x + 16).", "x = (−4 ± √−48) ÷ 2 = (−4 ± 4i√3) ÷ 2.", "4, −2 ± 2i√3."],
   "**4, −2 + 2i√3, −2 − 2i√3.**"))

g(27, 2, "(adapted — the paper's options are four graphs, each labelled with its answer) Find the real solutions of x² + 2x + 2 = 0 by graphing.",
  ["no solution (graph a)", "x = 4 (graph b)", "x = 0 (graph c)", "x = 2 (graph d)"], 0,
  "Real solutions are where the graph crosses or touches the x-axis. Find the vertex: is it above or below?",
  ["The parabola opens up (a = 1 > 0).",
   "Its vertex is at x = −2 ÷ 2 = −1, y = 1 − 2 + 2 = 1 — ABOVE the x-axis.",
   "An upward parabola whose lowest point is above the axis never reaches it.",
   "No real solution (the discriminant, 4 − 8 = −4, agrees)."],
  "**No solution.** The vertex (−1, 1) sits above the x-axis and the parabola opens up, so it never touches the axis.",
  "The discriminant is the no-graph check: negative means no real solutions.",
  ("The graph of y = x² − 4x + 5 has its vertex at (2, 1). What are the real solutions of x² − 4x + 5 = 0?",
   ["No real solution", "x = 2", "x = 1", "x = 2 and x = 1"], 0,
   "Is the vertex above or below the x-axis, and which way does it open?",
   ["Opens up, lowest point (2, 1) above the axis.", "It never reaches the x-axis.", "No real solution."],
   "**No real solution.**"),
  frm='added')

MU = "Factor out the GCF, then factor the rest. The power on each factor is that zero's multiplicity."
g(28, 2, "What are the zeros of f(x) = 4x³ − 12x² − 16x, and what are their multiplicities?",
  ["the numbers 1, −4, and 0 are zeros of multiplicity 2", "the numbers −1, 4, and 0 are zeros of multiplicity 2",
   "the numbers −1, 4, and 0 are zeros of multiplicity 1", "the numbers 1, −4, and 0 are zeros of multiplicity 1"], 2,
  MU,
  ["Factor out 4x: 4x(x² − 3x − 4).",
   "x² − 3x − 4 = (x − 4)(x + 1).",
   "f(x) = 4x(x − 4)(x + 1): zeros 0, 4, −1, each factor to the first power.",
   "−1, 4 and 0, each of multiplicity 1."],
  "**−1, 4 and 0, each of multiplicity 1.** A factor (x − 4) gives the zero +4 — the sign flips.",
  "A degree-3 polynomial's multiplicities add to 3; three zeros of multiplicity 2 would make degree 6.",
  ("What are the zeros of f(x) = 3x³ + 3x² − 18x, and what are their multiplicities?",
   ["0, −3 and 2, each of multiplicity 1", "0, 3 and −2, each of multiplicity 1",
    "0, −3 and 2, each of multiplicity 2", "−3 and 2 of multiplicity 1; 0 of multiplicity 3"], 0, MU,
   ["3x(x² + x − 6).", "= 3x(x + 3)(x − 2).", "0, −3, 2, each multiplicity 1."],
   "**0, −3 and 2, each of multiplicity 1.**"))

g(29, 3, "What are the zeros of f(x) = x⁴ − 4x³ + 3x², and what are their multiplicities?",
  ["the numbers −1 and −3 are zeros of multiplicity 2; the number 0 is a zero of multiplicity 1",
   "the number 0 is a zero of multiplicity 2; the numbers 1 and 3 are zeros of multiplicity 1",
   "the numbers 0 and 1 are zeros of multiplicity 2; the number 3 is a zero of multiplicity 1",
   "the number 0 is a zero of multiplicity 2; the numbers −1 and −3 are zeros of multiplicity 1"], 1,
  MU,
  ["Factor out x²: x²(x² − 4x + 3).",
   "x² − 4x + 3 = (x − 1)(x − 3).",
   "f(x) = x²(x − 1)(x − 3): x² gives 0 with multiplicity 2.",
   "0 (multiplicity 2); 1 and 3 (multiplicity 1)."],
  "**0 of multiplicity 2; 1 and 3 of multiplicity 1.** The x² factored out is where the multiplicity 2 comes from.",
  "Multiplicities 2 + 1 + 1 = 4, matching the degree.",
  ("What are the zeros of f(x) = x⁴ + 2x³ − 8x², and what are their multiplicities?",
   ["0 of multiplicity 2; −4 and 2 of multiplicity 1", "0 of multiplicity 2; 4 and −2 of multiplicity 1",
    "0 of multiplicity 1; −4 and 2 of multiplicity 2", "−4, 0 and 2, each of multiplicity 1"], 0, MU,
   ["x²(x² + 2x − 8).", "= x²(x + 4)(x − 2).", "0 (mult. 2); −4 and 2 (mult. 1)."],
   "**0 of multiplicity 2; −4 and 2 of multiplicity 1.**"))

g(30, 2, "(adapted — the paper's options are four graphs, each labelled with its zeros) What are the zeros of y = x(x − 2)(x + 5)?",
  ["2, −5 (graph a)", "0, −2, 5 (graph b)", "0, 2, −5 (graph c)", "2, −5, −2 (graph d)"], 2,
  "Set each factor equal to zero — including the lone x.",
  ["x = 0 from the factor x.",
   "x − 2 = 0 gives 2; x + 5 = 0 gives −5.",
   "Three factors, three zeros: 0, 2, −5.",
   "On the graph, the curve crosses the x-axis at −5, 0 and 2."],
  "**0, 2, −5.** The bare x is a factor too, so 0 is a zero; dropping it leaves only two.",
  "Each zero is the OPPOSITE sign of the number in its bracket.",
  ("What are the zeros of y = x(x + 3)(x − 4)?", ["0, −3, 4", "0, 3, −4", "−3, 4", "0, −3, −4"], 0,
   "Set each factor equal to zero.",
   ["x = 0.", "x + 3 = 0 → −3; x − 4 = 0 → 4.", "0, −3, 4."], "**0, −3, 4.**"),
  frm='added')

RT = "By the Fundamental Theorem of Algebra, a polynomial equation has as many roots as its degree (counting multiplicity and complex roots)."
g(32, 1, "How many roots does −12x² − 25x + 5 + x³ = 0 have?", ["2", "3", "4", "5"], 1,
  RT,
  ["The terms are out of order; the highest power present is x³.",
   "So the degree is 3.",
   "A degree-3 equation has 3 roots."],
  "**3.** The degree is the highest exponent wherever it sits, not the first term's.",
  "Scan for the biggest exponent before anything else.",
  ("How many roots does x⁴ − 3x² + 7 − 2x⁵ = 0 have?", ["5", "3", "4", "7"], 0, RT,
   ["The highest power is x⁵ (at the end).", "Degree 5.", "5 roots."], "**5.**"))

g(33, 1, "How many roots does 2x⁴ − x³ − 12x² − 25x + 5 = 0 have?", ["2", "3", "4", "5"], 2,
  RT,
  ["The highest power is x⁴.", "Degree 4.", "4 roots."],
  "**4.** Degree four, four roots — some may be complex.",
  "The count includes complex roots, not just where the graph crosses.",
  ("How many roots does 6 − x² + 4x³ = 0 have?", ["3", "2", "4", "6"], 0, RT,
   ["The highest power is x³.", "Degree 3.", "3 roots."], "**3.**"))

SY = "Test each point in EVERY inequality. One failure rules it out."
g(34, 2, "Which point is in the solution set of the system 3x + 3y ≤ 45, 2x + y ≤ 20, x ≥ 0, y ≥ 0?",
  ["(12, 1)", "(5, 4)", "(2, 15)", "(10, 4)"], 1,
  SY,
  ["(12, 1): 3(13) = 39 ≤ 45 ✓, but 2(12) + 1 = 25 > 20 ✗.",
   "(5, 4): 3(9) = 27 ≤ 45 ✓, 10 + 4 = 14 ≤ 20 ✓, both coordinates ≥ 0 ✓.",
   "(2, 15): 3(17) = 51 > 45 ✗. (10, 4): 2(10) + 4 = 24 > 20 ✗.",
   "Only (5, 4) satisfies all four."],
  "**(5, 4).** Every other point passes the first inequality and fails the second, or fails the first outright.",
  "Points that pass one inequality can still fail another — check them all.",
  ("Which point is in the solution set of the system x + y ≤ 10, 3x + y ≤ 18, x ≥ 0, y ≥ 0?",
   ["(4, 5)", "(6, 2)", "(1, 10)", "(5, 5)"], 0, SY,
   ["(4, 5): 9 ≤ 10 ✓, 17 ≤ 18 ✓.", "(6, 2): 20 > 18 ✗; (1, 10): 11 > 10 ✗; (5, 5): 20 > 18 ✗.", "(4, 5)."],
   "**(4, 5).**"))

paper = [q['paperNo'] for q in Q]
assert paper == list(range(1, 9)) + list(range(20, 31)) + [32, 33, 34], paper

# -------------------------------------------------------------------- cards
C = []
A = 'added'
card(C, 'How to use this unit',
     "**Paper first. Then enter what you actually wrote, by the paper's own question numbers.**\n"
     "• The grid here skips 9–19 and 31 — 9–19 are not uploaded yet, and 31 has two right answers on the paper\n"
     "• #24, #27 and #30 are adapted, so their choices are not the paper's letters — answer those under Work it here, or leave them blank on the grid",
     hint="Blanks are never marked wrong. Skip any you did not do.", frm=A)
card(C, 'Vertex and axis of symmetry',
     "**x = −b ÷ 2a gives the axis; substitute it back for the vertex's y.**\n"
     "• The axis is a vertical line: always written x = …\n"
     "• y = −2x² + 8x − 20 → x = 2, y = −12, vertex (2, −12)",
     eq="x = −b / 2a", hint="Axis first, then plug in.", frm=A)
card(C, 'Maximum, minimum and range',
     "**a > 0 opens up (a minimum); a < 0 opens down (a maximum). The value is the vertex's y.**\n"
     "• Minimum k → range y ≥ k; maximum k → range y ≤ k\n"
     "• The x-coordinate is WHERE it happens, never the value itself",
     hint="Smile has a bottom, frown has a top.", frm=A)
card(C, 'Vertex form by completing the square',
     "**Halve the x-coefficient, square it, add and subtract it: x² − 2x + 8 = (x − 1)² + 7.**\n"
     "• y = a(x − h)² + k has vertex (h, k)\n"
     "• The sign inside the bracket matches half the x-coefficient",
     eq="y = a(x − h)² + k", hint="Check: the vertex's y equals the original at x = h.", frm=A)
card(C, 'Factoring a trinomial',
     "**Find two numbers that multiply to c and add to b; take out any common factor first.**\n"
     "• + constant, + middle → both plus; + constant, − middle → both minus\n"
     "• 2x² + 16x + 30 = 2(x² + 8x + 15) = 2(x + 3)(x + 5)",
     hint="Read the two signs before you hunt for numbers.", frm=A)
card(C, 'Square roots of negatives',
     "**√−n = i√n, then take out the largest perfect square: √−360 = i√(36·10) = 6i√10.**\n"
     "• Simplified means no negative and no perfect square left under the root\n"
     "• √9 i and 3i are the same number — the paper may write either",
     hint="Pull out −1 as i first, then simplify as usual.", frm=A)
card(C, 'Complex solutions from the quadratic formula',
     "**A negative discriminant gives a ± pair with i: ½x² − x + 5 = 0 → 1 ± 3i.**\n"
     "• Clear any fraction first by multiplying every term\n"
     "• Real part = −b ÷ 2a; imaginary part = √|b² − 4ac| ÷ 2a",
     eq="x = (−b ± √(b² − 4ac)) / 2a", hint="Discriminant negative → no real solutions, two complex ones.", frm=A)
card(C, 'Synthetic division and the Remainder Theorem',
     "**Dividing P(x) by (x − k) leaves a remainder equal to P(k).**\n"
     "• Write a 0 for every missing power — x⁴ + 9x³ − 9x + 2 is 1, 9, 0, −9, 2\n"
     "• Divide by x − 2 → use k = +2; to find P(−2), use k = −2",
     hint="The sign of k is the opposite of the sign in (x − k).", frm=A)
card(C, 'Cubes: one real root and a complex pair',
     "**x³ − a³ = (x − a)(x² + ax + a²): the real root is a, the quadratic gives a complex pair.**\n"
     "• x³ − 8 → 2, −1 ± i√3 · x³ = 216 → 6, −3 ± 3i√3\n"
     "• A cubic always has three solutions in total",
     eq="a³ − b³ = (a − b)(a² + ab + b²)", hint="Spot the perfect cube, then the quadratic does the rest.", frm=A)
card(C, 'Zeros and multiplicity',
     "**Factor completely; each factor's exponent is its zero's multiplicity.**\n"
     "• x⁴ − 4x³ + 3x² = x²(x − 1)(x − 3): 0 (multiplicity 2), 1 and 3 (multiplicity 1)\n"
     "• A factor (x − 4) gives the zero +4 — the sign flips; a bare x gives the zero 0",
     hint="Multiplicities always add up to the degree.", frm=A)
card(C, 'Question 31 — two right answers',
     "**y = (x + 3)(x − 3)(x − 4) has zeros −3, 3 and 4.**\n"
     "• On the paper, options b and c both list those three zeros and show the same graph, so either letter is right\n"
     "• That is why #31 is not on the grid here — the grid can only accept one letter",
     hint="Set each bracket to zero: −3, 3, 4.", frm=A)
card(C, 'How many roots',
     "**A polynomial equation has as many roots as its degree, counting complex roots and repeats.**\n"
     "• −12x² − 25x + 5 + x³ = 0 is degree 3 → 3 roots, even written out of order\n"
     "• 2x⁴ − x³ − 12x² − 25x + 5 = 0 is degree 4 → 4 roots",
     hint="Find the biggest exponent, wherever it sits.", frm=A)
card(C, 'A point in a system of inequalities',
     "**A point is in the solution set only if it satisfies EVERY inequality.**\n"
     "• (5, 4) in 3x + 3y ≤ 45, 2x + y ≤ 20: 27 ≤ 45 and 14 ≤ 20 ✓\n"
     "• (12, 1) passes the first but fails 2x + y ≤ 20 — one failure is enough",
     hint="Test them all; stop at the first one that fails.", frm=A)

# --------------------------------------------------------------------- unit
UID = 'unit-alg-sgt4'
unit = {
    'id': UID, 'type': 'unit',
    'updatedAt': int(time.time() * 1000) - 3 * 3600 * 1000,
    'classId': 'algeo', 'quarter': 1, 'status': 'draft',
    'book': True, 'order': 1, 'guide': True, 'libv': 1,
    'title': 'Topic 3 · Test 4 Study Guide, Part 1',
    'srcName': 'math study guide.test 4 — Alg 2 SG T6 P1 (Drive)',
    'source': 'The class study guide for Test 4, Part 1, imported as issued',
    'summary': {'text': "The class study guide for Test 4, Part 1, question for question — quadratics (vertex and axis of "
                        "symmetry, maximum or minimum and range, vertex form, factoring), complex solutions and "
                        "simplifying with i, synthetic division and the Remainder Theorem, real and complex roots of "
                        "cubics, zeros and multiplicity, counting roots, and a point in a system of inequalities. "
                        "Work the printout first, then enter your answers here. Question numbers match the paper.",
                'from': 'source'},
    'why': {'text': "The test is on paper, so the guide on paper is the real rehearsal. Entering your answers here "
                    "afterwards grades it on the spot, walks you through each one you missed, and files those into the "
                    "Growth Zone — so the exact skills you dropped come back before Test 4.",
            'from': 'added'},
    'objectives': [
        {'text': "Find a parabola's vertex, axis of symmetry, maximum or minimum, and range.", 'from': 'source'},
        {'text': "Rewrite a quadratic in vertex form and factor quadratic expressions.", 'from': 'source'},
        {'text': "Simplify square roots of negative numbers and find complex solutions.", 'from': 'source'},
        {'text': "Use synthetic division and the Remainder Theorem to evaluate a polynomial.", 'from': 'source'},
        {'text': "Find the real and complex roots, zeros and multiplicities of a polynomial.", 'from': 'source'},
    ],
    'parentNote': {'text': (
        "Built from the class study guide in her Algebra & Geometry II folder — the file is named \"math study guide.test 4\" "
        "and the paper's own header reads \"Alg 2 SG T6 P1\", the ExamView file name (the same mismatch Test 2's guide had). "
        "\"P1\" suggests a Part 2 exists; it was not in the folder. Same approach as the two earlier algebra guides: paper "
        "first, then the app grades it, walks through each miss and sends them to the Growth Zone. The copy in Drive was "
        "read for its questions only; nothing on it was marked or recorded.\n\n"
        "ONE PAGE IS MISSING. The upload's second and third pages are two photos of the same page, so the paper's page 2 — "
        "questions 9 to 19 — never arrived. Nothing was invented for them. The entry grid shows the paper's own numbers "
        "(1–8, 20–30, 32–34), so her letters still line up with the printout. If page 2 is uploaded, those eleven questions "
        "can be added to this same unit.\n\n"
        "QUESTION 31 HAS TWO RIGHT ANSWERS ON THE PAPER. Options b and c both list the zeros −3, 3 and 4 and show the same "
        "graph, so either letter is correct. A one-letter grid would mark one of them wrong, so #31 is taught on a card "
        "instead of graded. Worth a word to her so she does not second-guess it on the test.\n\n"
        "There was no answer key in the upload, so every answer was worked out independently and checked, and every one "
        "of the 22 graded questions has a verified \"try it again\" version with new numbers for the rescue round. #24 is "
        "fill-in on paper and #27 and #30 offer graphs as choices, so those three are adapted and their letters do not "
        "match the paper; the first card tells her to leave them blank on the grid or answer them under Work it here."),
        'from': 'added'},
    'nextUp': {'text': "Work the paper guide fully first, then come back and enter what you WROTE, by question number. "
                       "The misses are the valuable part.", 'minutes': 40, 'from': 'added'},
    'cards': C, 'questions': Q,
}
path = os.path.join(REPO, 'content', 'alg-sg-test4.json')
io.open(path, 'w', encoding='utf-8').write(json.dumps({'v': 4, 'records': {UID: unit}}, ensure_ascii=False, indent=1))
print('alg-sg-test4.json  %d cards · %d questions · paper numbers %s' % (len(C), len(Q), paper))
