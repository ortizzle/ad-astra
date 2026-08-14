# Builder for Sedona's Wordly Wise 3000 Book 9 units (Ad Astra).
import json, io, time, re

def card(C, term, sp, d, hint=None, frm='source'):
    c = {'id': 'c%d' % len(C), 'term': term, 'sp': sp, 'def': d}
    if hint: c['hint'] = hint
    c['from'] = frm
    C.append(c)

def q(Q, lv, text, opts, ans, hint, steps, main, tip, frm='source'):
    Q.append({'id': 'q%d' % len(Q), 'lv': lv, 'from': frm, 'kind': 'mc', 'q': text,
              'opts': [str(o) for o in opts], 'ans': ans, 'hint': hint, 'steps': steps,
              'ex': {'main': main, 'tip': tip}})

def ana(Q, lv, stem, opts, ans, hint, steps, main, tip, frm='added'):
    """An analogy question. stem is 'WORD : WORD' — two words, one colon, nothing else."""
    Q.append({'id': 'q%d' % len(Q), 'lv': lv, 'from': frm, 'kind': 'analogy', 'q': stem,
              'opts': [str(o) for o in opts], 'ans': ans, 'hint': hint, 'steps': steps,
              'ex': {'main': main, 'tip': tip}})

STEM_RE = re.compile(r'^[A-Za-z][A-Za-z \-]*\s:\s[A-Za-z][A-Za-z \-]*$')
PAIR_RE = re.compile(r'^[a-z][a-z \-]*\s:\s[a-z][a-z \-]*$')
POSREF = re.compile(r'\b(all|none) of the above\b|\boptions? [a-d1-4]\b|\b(first|second|third|last) (option|choice)\b', re.I)

def build(C, Q, uid, title, summary, why, objectives, parentNote, nextUp, path,
          srcName, source, offset_hours=4):
    errs = []
    for c in C:
        if not c['def'].startswith('**'): errs.append('%s: def not bold-first' % c['id'])
        if not c.get('sp'): errs.append('%s: missing sp' % c['id'])
    for x in Q:
        if len(x['opts']) != 4: errs.append('%s: %d opts' % (x['id'], len(x['opts'])))
        if len(set(x['opts'])) != 4: errs.append('%s: duplicate opts' % x['id'])
        if not (0 <= x['ans'] < 4): errs.append('%s: ans out of range' % x['id'])
        if not (3 <= len(x['steps']) <= 6): errs.append('%s: %d steps' % (x['id'], len(x['steps'])))
        if not x['ex']['main'].startswith('**'): errs.append('%s: ex.main not bold' % x['id'])
        if x['lv'] not in (1, 2, 3): errs.append('%s: bad lv' % x['id'])
        blob = ' '.join([x['q'], x['hint'], x['ex']['main'], x['ex']['tip']] + x['steps'] + x['opts'])
        if POSREF.search(blob): errs.append('%s: positional reference' % x['id'])
        if x['kind'] == 'analogy':
            # The stem must parse as exactly two words around one colon, or
            # analogyStem() falls back to plain text and the plate is wasted.
            if not STEM_RE.match(x['q']): errs.append('%s: bad analogy stem %r' % (x['id'], x['q']))
            if x['q'].upper() != x['q']: errs.append('%s: stem not uppercase' % x['id'])
            for o in x['opts']:
                if not PAIR_RE.match(o): errs.append('%s: bad analogy pair %r' % (x['id'], o))
    assert not errs, errs
    unit = {
        'id': uid, 'type': 'unit',
        'updatedAt': int(time.time() * 1000) - int(offset_hours * 3600 * 1000),
        'classId': 'english', 'quarter': 1, 'status': 'draft', 'title': title,
        'srcName': srcName, 'source': source,
        'summary': {'text': summary, 'from': 'source'},
        'why': {'text': why, 'from': 'added'},
        'objectives': [{'text': t, 'from': f} for t, f in objectives],
        'parentNote': {'text': parentNote, 'from': 'added'},
        'nextUp': {'text': nextUp[0], 'minutes': nextUp[1], 'from': 'added'},
        'cards': C, 'questions': Q,
    }
    io.open('/home/user/ad-astra/' + path, 'w', encoding='utf-8').write(
        json.dumps({'v': 4, 'records': {uid: unit}}, ensure_ascii=False, indent=1))
    lv = {1: 0, 2: 0, 3: 0}
    for x in Q: lv[x['lv']] += 1
    na = len([x for x in Q if x['kind'] == 'analogy'])
    print('%-24s %2d cards · %2d questions %s · %d analogies' % (
        path.split('/')[-1], len(C), len(Q), lv, na))
