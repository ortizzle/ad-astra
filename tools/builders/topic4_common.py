# Shared helpers for the Algebra & Geometry II Topic 4 builders (Rational Functions).
#
# Two jobs, both about keeping the file honest:
#   E(s)      parses the DISPLAY string a question actually shows ("(x − 7)/(x − 3)")
#             into sympy, so every option can be asserted against the computed maths
#             rather than typed next to it and trusted.
#   rgraph()  draws a rational curve for renderGraph. The engine has no rational
#             series type (line / abs / poly / vertex-form parabola / pts), and a
#             vertical asymptote cannot be drawn by any of the analytic types, so each
#             curve is a `pts` series sampled here, densely near every pole, with an
#             off-window point between branches. renderGraph drops off-window points
#             and starts a new polyline after one, so the branches never get joined
#             across the asymptote. No engine change was needed.
import json, io, os, math
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)

x, y, z, r, c, a, b, n = sp.symbols('x y z r c a b n')
_T = standard_transformations + (implicit_multiplication_application, convert_xor)
_SUP = {'²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5'}
_LOC = {'x': x, 'y': y, 'z': z, 'r': r, 'c': c, 'a': a, 'b': b, 'n': n, 's': sp.Symbol('s')}

def E(s):
    """Display string -> sympy expression."""
    t = s.replace('−', '-').replace('·', '*').replace('÷', '/').replace('½', '(1/2)')
    for k, v in _SUP.items():
        t = t.replace(k, v)
    return parse_expr(t, local_dict=_LOC, transformations=_T)

def same(s, expr):
    """Assert a display string equals an expression (as rational functions)."""
    d = sp.simplify(sp.cancel(E(s) - sp.sympify(expr)))
    assert d == 0, 'MISMATCH: %r != %s' % (s, expr)
    return s

def differs(s, expr):
    """Assert a distractor is NOT accidentally equal to the answer."""
    d = sp.simplify(sp.cancel(E(s) - sp.sympify(expr)))
    assert d != 0, 'DISTRACTOR ALSO CORRECT: %r == %s' % (s, expr)
    return s

def poles(f, v=x):
    """Real vertical asymptotes of f AFTER cancelling (holes excluded)."""
    num, den = sp.fraction(sp.cancel(sp.together(f)))
    return sorted(set(sp.nsimplify(t) for t in sp.solve(den, v) if t.is_real))

def holes(f, v=x):
    num, den = sp.fraction(sp.together(f))
    raw = set(t for t in sp.solve(den, v) if t.is_real)
    return sorted(raw - set(poles(f, v)))

def hasym(f, v=x):
    """Horizontal asymptote value, or None when there is none."""
    L = sp.limit(f, v, sp.oo)
    R = sp.limit(f, v, -sp.oo)
    if L.is_finite and L == R:
        return L
    return None

def rgraph(curves, w, gx=1, gy=1, vas=(), has=(), pts=None, xl='x', yl='y', N=240):
    """curves: sympy expressions in x. vas/has: asymptote lines drawn as the
    SECOND series so they wear the second graph colour, not the curve's."""
    x0, x1, y0, y1 = w
    big = y1 + 10 * (y1 - y0)            # off-window break marker
    series = []
    for f in curves:
        fn = sp.lambdify(x, f, 'math')
        ps = sorted(float(p) for p in poles(f) + holes(f) if x0 < float(p) < x1)
        xs = set(x0 + (x1 - x0) * i / N for i in range(N + 1))
        for p in ps:
            for k in range(1, 40):
                d = 0.6 * (0.82 ** k)
                xs.add(p - d); xs.add(p + d)
        out, prev_in = [], False
        for xv in sorted(xs):
            if not (x0 <= xv <= x1): continue
            if any(abs(xv - p) < 1e-9 for p in ps): continue
            # a pole lies between this sample and the last one: break the line
            if out and any(out[-1][0] < p < xv for p in ps) and prev_in:
                out.append([round((out[-1][0] + xv) / 2, 4), big]); prev_in = False
            try:
                yv = fn(xv)
            except ZeroDivisionError:
                continue
            inside = y0 - 1e-9 <= yv <= y1 + 1e-9
            if inside:
                out.append([round(xv, 4), round(yv, 4)]); prev_in = True
            elif prev_in:
                out.append([round(xv, 4), big]); prev_in = False
        series.append({'type': 'pts', 'pts': out})
    if vas or has:
        A = []
        for k in has:
            if A: A.append([x0, big])
            A += [[x0, float(k)], [x1, float(k)]]
        for h in vas:
            if A: A.append([x0, big])
            A += [[float(h), y0], [float(h), y1]]
        series.append({'type': 'pts', 'pts': A})
    g = {'w': list(w), 'gx': gx, 'gy': gy, 'series': series, 'xl': xl, 'yl': yl}
    if pts: g['pts'] = pts
    return g

def lines_graph(extra_series, g):
    g['series'] = g['series'][:1] + extra_series + g['series'][1:]
    return g

def finish(path, quarter=2):
    """build() stamps quarter 1; Topic 4 is taught in the second quarter."""
    from unit_common import REPO
    fp = os.path.join(REPO, path)
    d = json.load(io.open(fp, encoding='utf-8'))
    for u in d['records'].values():
        u['quarter'] = quarter
    io.open(fp, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
