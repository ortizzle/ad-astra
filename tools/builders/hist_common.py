import json, io, time

def card(C, term, d, hint=None, frm='source'):
    c = {'id': 'c%d' % len(C), 'term': term, 'def': d}
    if hint: c['hint'] = hint
    c['from'] = frm
    C.append(c)

def q(Q, lv, text, opts, ans, hint, steps, main, tip, frm='source'):
    Q.append({'id': 'q%d' % len(Q), 'lv': lv, 'from': frm, 'kind': 'mc', 'q': text,
              'opts': opts, 'ans': ans, 'hint': hint, 'steps': steps,
              'ex': {'main': main, 'tip': tip}})

# The repo is public, so nothing from the worksheet header may reach a unit.
# 'Sedona' and 'Ortiz' are unambiguous. The younger sister's name is also a
# common noun, so a blanket match flags "Mississippi River"; require instead a
# capitalised River that is NOT preceded by a proper noun naming it.
import re
PRIVACY_PLAIN = ('sedona', 'ortiz', 'score:', 'name:')
_NAMED_RIVER = re.compile(r'[A-Z][a-z]+ River\b')
_ANY_RIVER = re.compile(r'\bRiver\b')

def privacy_hits(blob_lower, blob_raw):
    hits = [p for p in PRIVACY_PLAIN if p in blob_lower]
    # Count capitalised "River"s and subtract the ones that are named rivers
    # ("Mississippi River"). Anything left over is a bare River — a name.
    if len(_ANY_RIVER.findall(blob_raw)) > len(_NAMED_RIVER.findall(blob_raw)):
        hits.append('bare capitalised River')
    return hits

def build(C, Q, uid, title, summary, why, objectives, parentNote, nextUp, path, offset_hours=6):
    errs = []
    for c in C:
        if not c['def'].startswith('**'): errs.append('%s: def not bold-first' % c['id'])
        if c.get('from') not in ('source','added'): errs.append('%s: bad from' % c['id'])
    for x in Q:
        if len(x['opts']) != 4: errs.append('%s: %d opts' % (x['id'], len(x['opts'])))
        if len(set(x['opts'])) != len(x['opts']): errs.append('%s: duplicate opts' % x['id'])
        if not (0 <= x['ans'] < 4): errs.append('%s: ans out of range' % x['id'])
        if not (3 <= len(x['steps']) <= 6): errs.append('%s: %d steps' % (x['id'], len(x['steps'])))
        if not x['ex']['main'].startswith('**'): errs.append('%s: ex.main not bold' % x['id'])
        if x['lv'] not in (1,2,3): errs.append('%s: bad lv' % x['id'])
    unit = {
        'id': uid, 'type': 'unit',
        'updatedAt': int(time.time()*1000) - int(offset_hours*3600*1000),
        'classId': 'history', 'quarter': 1, 'status': 'draft', 'title': title,
        'srcName': 'History 8, Unit 1 Key Terms',
        'source': 'History 8, Unit 1 key-terms list (Drive folder)',
        'summary': {'text': summary, 'from': 'source'},
        'why': {'text': why, 'from': 'added'},
        'objectives': [{'text': t, 'from': f} for t, f in objectives],
        'parentNote': {'text': parentNote, 'from': 'added'},
        'nextUp': {'text': nextUp[0], 'minutes': nextUp[1], 'from': 'added'},
        'cards': C, 'questions': Q,
    }
    raw = json.dumps(unit, ensure_ascii=False)
    for p in privacy_hits(raw.lower(), raw):
        errs.append('PRIVACY: %r appears in the unit' % p)
    assert not errs, errs
    io.open('/home/user/ad-astra/' + path, 'w', encoding='utf-8').write(
        json.dumps({'v': 4, 'records': {uid: unit}}, ensure_ascii=False, indent=1))
    lv = {1:0, 2:0, 3:0}
    for x in Q: lv[x['lv']] += 1
    print('%-30s %2d cards · %2d questions %s' % (path.split('/')[-1], len(C), len(Q), lv))
