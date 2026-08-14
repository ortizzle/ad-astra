# Shared builder + validator for the Algebra Topic 1 units.
import json, io, time

def card(C, term, d, sp=None, hint=None, eq=None, graph=None, frm='source'):
    c = {'id': 'c%d' % len(C), 'term': term, 'def': d}
    if eq: c['eq'] = eq
    if sp: c['sp'] = sp
    if hint: c['hint'] = hint
    if graph: c['graph'] = graph
    c['from'] = frm
    C.append(c)

def q(Q, lv, text, opts, ans, hint, steps, main, tip, frm='source', kind='mc', graph=None):
    x = {'id': 'q%d' % len(Q), 'lv': lv, 'from': frm, 'kind': kind, 'q': text,
         'opts': opts, 'ans': ans, 'hint': hint, 'steps': steps, 'ex': {'main': main, 'tip': tip}}
    if graph: x['graph'] = graph
    Q.append(x)

def _validate(C, Q, path):
    errs = []
    for c in C:
        if not c['def'].startswith('**'): errs.append('%s %s: def not bold-first' % (path, c['id']))
        if c.get('from') not in ('source','added'): errs.append('%s %s: bad from' % (path, c['id']))
        g = c.get('graph')
        if g and (not isinstance(g.get('w'), list) or len(g['w']) != 4 or not g.get('series')):
            errs.append('%s %s: bad graph' % (path, c['id']))
        if g and not (g['w'][1] > g['w'][0] and g['w'][3] > g['w'][2]):
            errs.append('%s %s: graph window inverted' % (path, c['id']))
    for x in Q:
        if x['kind'] == 'mc':
            if len(x['opts']) != 4: errs.append('%s %s: %d opts' % (path, x['id'], len(x['opts'])))
            if len(set(x['opts'])) != len(x['opts']): errs.append('%s %s: duplicate opts' % (path, x['id']))
        if not (0 <= x['ans'] < len(x['opts'])): errs.append('%s %s: ans out of range' % (path, x['id']))
        if not (3 <= len(x['steps']) <= 6): errs.append('%s %s: %d steps' % (path, x['id'], len(x['steps'])))
        if not x['ex']['main'].startswith('**'): errs.append('%s %s: ex.main not bold' % (path, x['id']))
        if x['lv'] not in (1,2,3): errs.append('%s %s: bad lv' % (path, x['id']))
        g = x.get('graph')
        if g and (not isinstance(g.get('w'), list) or len(g['w']) != 4 or not g.get('series')):
            errs.append('%s %s: bad graph' % (path, x['id']))
    return errs

def build(C, Q, uid, title, summary, why, objectives, parentNote, nextUp, path,
          classId, srcName, source, offset_hours=6):
    errs = _validate(C, Q, path)
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
    out = {'v': 4, 'records': {uid: unit}}
    io.open('/home/user/ad-astra/' + path, 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    lv = {1:0, 2:0, 3:0}
    for x in Q: lv[x['lv']] += 1
    print('%-28s %2d cards (%d graphs) · %2d questions %s' % (
        path.split('/')[-1], len(C), sum(1 for c in C if c.get('graph')), len(Q), lv))

def write(*a, **k): pass
