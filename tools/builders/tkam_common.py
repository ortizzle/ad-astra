# Shared helper for the To Kill a Mockingbird chapter quizzes (ch. 6–13).
# unit_common.build() does not know about book units, so this wraps it:
# build first (validation + _balance), then reopen the file to add the
# book-only fields. Passages are attached AFTER _balance by question id —
# _balance swaps options inside a question but never reorders questions.
import json, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unit_common import card, q, build, REPO

# A chapter quiz must never reach past its own chapter. Each builder passes
# the tells of LATER chapters; any hit in the shipped record fails the build.
def chapter(ch, sub, C, Q, summary, why, objectives, parentNote, nextUp,
            passages=None, later_tells=()):
    uid = 'unit-tkam-c%02d' % ch
    path = 'content/tkam-c%02d.json' % ch
    title = 'To Kill a Mockingbird · Ch. %d: %s' % (ch, sub)
    build('ad-astra', C, Q, uid, title, 'english', summary, why, objectives,
          parentNote, nextUp, path,
          'To Kill a Mockingbird, chapter %d' % ch,
          'To Kill a Mockingbird (Harper Lee), chapter quiz — chapter %d' % ch,
          offset_hours=3, round_=len(Q), libv_=1)
    fp = os.path.join(REPO, path)
    d = json.load(io.open(fp, encoding='utf-8'))
    u = d['records'][uid]
    u['book'] = True
    for qid, text in (passages or {}).items():
        x = next(x for x in u['questions'] if x['id'] == qid)
        assert len(text.split()) <= 45, (qid, len(text.split()))
        x['passage'] = text
    blob = json.dumps(u, ensure_ascii=False).lower()
    hits = [t for t in later_tells if t.lower() in blob]
    assert not hits, ('spoils past chapter %d' % ch, hits)
    # Back-references to sibling questions (the standalone rule).
    for x in u['questions']:
        assert not re.match(r'^(the same|that same|this same)\b', x['q'], re.I), x['id']
    io.open(fp, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
