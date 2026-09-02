"""Validate every shipped content file against the rules in CLAUDE.md."""
import json, glob, os, re, sys, time

# Compared against the real clock, not a constant — a hardcoded cutoff goes
# stale within hours and then flags correctly-stamped files as future-dated.
NOW_MS = int(time.time() * 1000)

POSITIONAL = re.compile(
    r'\b(the (first|second|third|fourth|last) (option|answer|choice))'
    r'|\b(all|none|both) of the above\b'
    r'|\boption [A-D]\b', re.I)

# A round serves 5 questions from the unit in shuffled order, so a stem that
# OPENS by pointing at a neighbour ("The same student then writes…") can reach
# her with that neighbour nowhere in sight. Chris caught this live: Science
# Quiz 1 asked about "the same student" as question 4 of 5, and one of its
# options mentioned a sidewalk that only existed in the question she never saw.
# Matching only at the start of the stem keeps this precise — an innocent
# mid-sentence "the same" ("the two 3s have the same value") is not a
# back-reference and must not be flagged.
BACKREF = re.compile(
    r'^\s*(the same|that same|for (that|the) same|from the same'
    r'|using the same|in the same|with the same)\b', re.I)

# The mirror failure: pointing at an artefact that is not attached.
SHOWN = re.compile(r'\b(graph|diagram|chart|table)\s+(shown|above|below)\b', re.I)

# How much longer than its nearest rival an option may be before its length
# gives it away. Shuffling (v64) killed "the answer is always first"; it cannot
# touch "the answer is always the wordiest", which is just as learnable and
# just as useless. Reported as a warning, not a problem: it is an authoring
# smell across a lot of already-shipped content, not something the app rejects.
LEN_SLACK = 0.10

def length_tell(opts, ans):
    """Percent by which the correct option outruns the longest wrong one, or 0."""
    if not isinstance(ans, int) or not (0 <= ans < len(opts)) or len(opts) < 2:
        return 0
    lens = [len(str(o)) for o in opts]
    correct = lens[ans]
    rival = max(lens[:ans] + lens[ans + 1:])
    if rival <= 0 or correct <= rival:
        return 0
    over = (correct - rival) / float(rival)
    return int(round(over * 100)) if over > LEN_SLACK else 0

def check(root, name):
    problems = []
    warnings = []
    seen_ids = {}
    for f in sorted(glob.glob(os.path.join(root, 'content', '*.json'))):
        base = os.path.basename(f)
        try:
            d = json.load(open(f))
        except Exception as e:
            problems.append((base, 'FILE', 'invalid JSON: %s' % e)); continue
        recs = d.get('records')
        recs = list(recs.values()) if isinstance(recs, dict) else (recs or [])
        for u in recs:
            if not isinstance(u, dict) or u.get('type') != 'unit':
                continue
            uid = u.get('id')
            P = lambda w, m: problems.append((base, uid, m)) if w else None
            W = lambda w, m: warnings.append((base, uid, m)) if w else None

            if uid in seen_ids:
                P(True, 'duplicate id, also in %s' % seen_ids[uid])
            seen_ids[uid] = base

            P(u.get('status') != 'draft', "status is %r, every unit ships as draft"
              % u.get('status'))
            ua = u.get('updatedAt')
            P(ua is None, 'no updatedAt (loses every merge)')
            P(isinstance(ua, (int, float)) and ua > NOW_MS + 3600000,
              'updatedAt is more than an hour in the future')

            title = u.get('title', '')
            P(' · ' in title and title.count(' · ') > 1,
              'title has more than one separator: %r' % title)

            qs = u.get('questions') or []
            P(not qs, 'no questions')
            qids = [q.get('id') for q in qs]
            P(len(qids) != len(set(qids)), 'duplicate question ids')

            for q in qs:
                tag = 'q%s' % q.get('id')
                kind = q.get('kind') or 'mc'
                opts = q.get('opts') or []
                ans = q.get('ans')
                if kind in ('mc', 'analogy'):
                    # A guide unit transcribes a real paper, and a real paper is
                    # allowed a True/False item. The grid in SCREENS.guideentry
                    # is driven by opts.length, so it renders A/B correctly —
                    # forcing two invented extra options onto it would change
                    # what she is entering. Everywhere else, four.
                    ok_counts = (2, 4) if u.get('guide') else (4,)
                    P(len(opts) not in ok_counts,
                      '%s: %d options, must be %s' % (tag, len(opts),
                       ' or '.join(map(str, ok_counts))))
                    P(len(set(map(str, opts))) != len(opts), '%s: duplicate options' % tag)
                    P(not isinstance(ans, int) or not (0 <= ans < len(opts)),
                      '%s: ans %r out of range' % (tag, ans))
                    # Same guide-unit reasoning as the two rules above, with one
                    # extra: these options are the teacher's, copied out word for
                    # word. Editing them to even up the lengths would break the
                    # letter-for-letter contract the whole paper-entry mode rests
                    # on. Variants are ours and shuffled, so they stay checked.
                    over = 0 if u.get('guide') else length_tell(opts, ans)
                    W(over, '%s: correct option %d%% longer than the next longest'
                      % (tag, over))
                if kind == 'order':
                    P(len(opts) != 4, '%s: order needs exactly 4 events' % tag)
                    P(ans != 0, '%s: order must have ans 0' % tag)
                if kind == 'analogy':
                    stem = str(q.get('q', ''))
                    parts = [x.strip() for x in stem.split(':') if x.strip()]
                    P(len(parts) != 2, '%s: analogy stem does not parse: %r' % (tag, stem))
                    P(stem != stem.upper(), '%s: analogy stem not uppercase' % tag)
                blob = ' '.join([str(q.get('q', ''))] + [str(o) for o in opts]
                                + [str(s) for s in (q.get('steps') or [])]
                                + [str((q.get('ex') or {}).get('main', ''))])
                # The rule exists because options shuffle at render time. On a
                # guide unit they explicitly do NOT (index.html scopes the
                # shuffle to `!u.guide`): she is entering the letter she wrote
                # on the paper, so "All of the above" is a faithful
                # transcription, not a smell. The exemption is the MAIN
                # question only — a guide unit's variants run in the rescue
                # round, which shuffles normally, and are checked below.
                m = POSITIONAL.search(blob)
                P(bool(m) and not u.get('guide'),
                  '%s: positional reference %r (options shuffle)' % (tag, m.group(0)) if m else '')

                stem = str(q.get('q', ''))
                b = BACKREF.match(stem)
                P(bool(b), '%s: stem opens %r — leans on another question, which '
                           'a shuffled round may not have served' % (tag, b.group(0).strip())
                  if b else '')
                # "the graph shown" is only meaningful if this question carries one
                s = SHOWN.search(stem) or SHOWN.search(str((q.get('ex') or {}).get('main', '')))
                P(bool(s) and not q.get('graph'),
                  '%s: says %r but has no graph attached' % (tag, s.group(0)) if s else '')
                steps = q.get('steps') or []
                P(not steps, '%s: no steps (walkthrough)' % tag)
                P(steps and not (3 <= len(steps) <= 6), '%s: %d steps, want 3-6' % (tag, len(steps)))
                P(not (q.get('ex') or {}).get('main'), '%s: no ex.main' % tag)
                P(q.get('lv') not in (1, 2, 3), '%s: lv %r' % (tag, q.get('lv')))
                if q.get('passage'):
                    P(len(str(q['passage']).split()) > 45,
                      '%s: passage %d words, cap ~40' % (tag, len(str(q['passage']).split())))

                v = q.get('variant')
                if v:
                    vt = tag + '.variant'
                    P(str(v.get('q','')).strip() == str(q.get('q','')).strip(),
                      '%s: variant repeats the original question' % vt)
                    vo = v.get('opts') or []
                    P(len(vo) != 4, '%s: %d options' % (vt, len(vo)))
                    P(len(set(map(str, vo))) != len(vo), '%s: duplicate options' % vt)
                    P(not isinstance(v.get('ans'), int) or not (0 <= v['ans'] < len(vo)),
                      '%s: ans %r out of range' % (vt, v.get('ans')))
                    vs = v.get('steps') or []
                    P(not (3 <= len(vs) <= 6), '%s: %d steps' % (vt, len(vs)))
                    vover = length_tell(vo, v.get('ans'))
                    W(vover, '%s: correct option %d%% longer than the next longest'
                      % (vt, vover))
                    P(not (v.get('ex') or {}).get('main'), '%s: no ex.main' % vt)
                    vb = ' '.join([str(v.get('q',''))] + [str(x) for x in vo] + [str(x) for x in vs]
                                  + [str((v.get('ex') or {}).get('main',''))])
                    mv = POSITIONAL.search(vb)
                    P(bool(mv), '%s: positional reference %r' % (vt, mv.group(0)) if mv else '')

            if u.get('guide'):
                P(not all(q.get('variant') for q in qs),
                  'guide unit: %d of %d questions have no variant'
                  % (sum(1 for q in qs if not q.get('variant')), len(qs)))

            # Sort sets (v146 / Wayfinder v125): {id, title, a, b, items:[{t, k, why}]}.
            # Left is `a`, right is `b`. An item that names its own bucket
            # tests nothing, exactly as a stem that glosses its word does.
            for sset in (u.get('sorts') or []):
                stag = 'sort %r' % str(sset.get('id'))
                P(not sset.get('id') or not sset.get('title'), '%s: needs id and title' % stag)
                a, b = str(sset.get('a','')), str(sset.get('b',''))
                P(not a or not b or a.lower()==b.lower(), '%s: buckets must be two different labels' % stag)
                items = sset.get('items') or []
                P(len(items) < 6, '%s: %d items, want 6+' % (stag, len(items)))
                ks = [it.get('k') for it in items]
                P(any(k not in ('a','b') for k in ks), '%s: every item needs k of a or b' % stag)
                P(ks.count('a') < 2 or ks.count('b') < 2, '%s: each bucket needs at least 2 items' % stag)
                ts = [str(it.get('t','')).strip().lower() for it in items]
                P(len(set(ts)) != len(ts), '%s: duplicate item text' % stag)
                for it in items:
                    t = str(it.get('t',''))
                    for lab in (a, b):
                        w = lab.lower().split()[0] if lab.split() else ''
                        P(bool(w) and len(w) > 4 and w in t.lower(),
                          '%s: item %r names its own bucket (%r)' % (stag, t[:40], lab))
                    P(not it.get('why'), '%s: item %r has no why' % (stag, t[:40]))
            for c in (u.get('cards') or []):
                P(not c.get('term'), 'a card has no term')
                dfn = str(c.get('def', ''))
                P(not dfn.strip().startswith('**'), 'card %r: def does not lead with a bold answer'
                  % str(c.get('term'))[:34])

            rnd = u.get('round')
            P(rnd is not None and (not isinstance(rnd, int) or rnd < 1),
              'round is %r' % rnd)
            o = u.get('order')
            P(o is not None and not isinstance(o, int), 'order is %r' % o)

    problems = [x for x in problems if x[2]]
    warns = [x for x in warnings if x[2]]
    nfiles = len(glob.glob(os.path.join(root, 'content', '*.json')))
    print('=== %s: %d files, %d units ===' % (name, nfiles, len(seen_ids)))
    if not nfiles:
        print('  NO CONTENT FOUND at %s — checking nothing' % root)
        return 1
    if not problems:
        print('  clean')
    else:
        for base, uid, m in problems:
            print('  %-26s %-18s %s' % (base, uid, m))
    if warns:
        # Warnings do not fail the run: the length tell is spread across a lot
        # of already-shipped content, and failing on it would just get muted.
        print('  --- %d warning(s); worst first%s ---'
              % (len(warns), '' if SHOW_ALL else ', pass --warnings for all'))
        ranked = sorted(warns, key=lambda x: -(int(re.search(r'(\d+)%', x[2]).group(1))
                                               if re.search(r'(\d+)%', x[2]) else 0))
        for base, uid, m in (ranked if SHOW_ALL else ranked[:10]):
            print('  %-26s %-18s %s' % (base, uid, m))
    return len(problems)

SHOW_ALL = '--warnings' in sys.argv

def locate(name):
    """Prefer the checkout this script lives beside; fall back to the sandbox
    path. Without this the hardcoded path simply finds nothing and the run
    reports 'clean' — a checker that silently checks nothing is worse than
    no checker."""
    here = os.path.dirname(os.path.abspath(__file__))          # tools/builders
    siblings = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    for cand in (os.path.join(siblings, name), '/home/user/' + name):
        if os.path.isdir(os.path.join(cand, 'content')):
            return cand
    return os.path.join(siblings, name)

n = check(locate('ad-astra'), 'ad-astra')
n += check(locate('wayfinder'), 'wayfinder')
sys.exit(1 if n else 0)
