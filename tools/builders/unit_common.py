# Generic unit builder for either app (non-vocab units).
import json, io, time, re

POSREF = re.compile(r'\b(all|none) of the above\b|\boptions? [a-d1-4]\b|\b(first|second|third|last) (option|choice)\b', re.I)

def card(C, term, d, hint=None, eq=None, frm='source'):
    c = {'id': 'c%d' % len(C), 'term': term, 'def': d}
    if eq: c['eq'] = eq
    if hint: c['hint'] = hint
    c['from'] = frm
    C.append(c)

def q(Q, lv, text, opts, ans, hint, steps, main, tip, frm='source', kind='mc'):
    Q.append({'id': 'q%d' % len(Q), 'lv': lv, 'from': frm, 'kind': kind, 'q': text,
              'opts': [str(o) for o in opts], 'ans': ans, 'hint': hint, 'steps': steps,
              'ex': {'main': main, 'tip': tip}})


def _balance(Q):
    """Spread correct answers across positions deterministically. The app
    shuffles options at render time (v64), so file order never reaches the
    student — but a biased file is still a biased file: the parent review
    queue and any future fixed-order mode read it as written, and every
    authoring session so far has drifted to ans:0. Rotate instead of trusting
    the author. Skips order/spell, whose opts order is semantic.
    Ported from Wayfinder's copy — keep the two in step."""
    slot = 0
    for x in Q:
        if x.get('kind') in ('order', 'spell'): continue
        want = slot % 4; slot += 1
        if x['ans'] != want:
            x['opts'][x['ans']], x['opts'][want] = x['opts'][want], x['opts'][x['ans']]
            x['ans'] = want

def build(app, C, Q, uid, title, classId, summary, why, objectives, parentNote, nextUp,
          path, srcName, source, offset_hours=4, round_=None):
    errs = []
    for c in C:
        if not c['def'].startswith('**'): errs.append('%s: def not bold-first' % c['id'])
    for x in Q:
        kind = x.get('kind', 'mc')
        # kind:'spell' carries opts:[word] (one option), ans:0 — the 4-option
        # rule is an MC rule. Matches Wayfinder's copy and check_content.py.
        if kind in ('mc', 'analogy', 'order'):
            if len(x['opts']) != 4: errs.append('%s: %d opts' % (x['id'], len(x['opts'])))
            if len(set(x['opts'])) != 4: errs.append('%s: duplicate opts' % x['id'])
            if not (0 <= x['ans'] < 4): errs.append('%s: ans out of range' % x['id'])
        elif kind == 'spell':
            if len(x['opts']) != 1: errs.append('%s: spell must carry exactly opts:[word]' % x['id'])
            if x['ans'] != 0: errs.append('%s: spell must have ans 0' % x['id'])
        if not (3 <= len(x['steps']) <= 6): errs.append('%s: %d steps' % (x['id'], len(x['steps'])))
        if not x['ex']['main'].startswith('**'): errs.append('%s: ex.main not bold' % x['id'])
        if x['lv'] not in (1, 2, 3): errs.append('%s: bad lv' % x['id'])
        blob = ' '.join([x['q'], x['hint'], x['ex']['main'], x['ex']['tip']] + x['steps'] + x['opts'])
        if POSREF.search(blob): errs.append('%s: positional reference' % x['id'])
    assert not errs, errs
    unit = {
        'id': uid, 'type': 'unit',
        'updatedAt': int(time.time()*1000) - int(offset_hours*3600*1000),
        'classId': classId, 'quarter': 1, 'status': 'draft', 'title': title,
        'srcName': srcName, 'source': source,
        'summary': {'text': summary, 'from': 'source'},
        'why': {'text': why, 'from': 'added'},
        'objectives': [{'text': t, 'from': f} for t, f in objectives],
        'parentNote': {'text': parentNote, 'from': 'added'},
        'nextUp': {'text': nextUp[0], 'minutes': nextUp[1], 'from': 'added'},
        'cards': C, 'questions': Q,
    }
    if round_: unit['round'] = round_
    io.open('/home/user/%s/%s' % (app, path), 'w', encoding='utf-8').write(
        json.dumps({'v': 4, 'records': {uid: unit}}, ensure_ascii=False, indent=1))
    lv = {1:0,2:0,3:0}
    for x in Q: lv[x['lv']] += 1
    print('%-28s %2d cards · %2d questions %s' % (path.split('/')[-1], len(C), len(Q), lv))
