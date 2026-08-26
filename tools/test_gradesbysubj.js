/* Smoke test for the parent-view "Grades by subject" tabulation
   (gradesBySubject() + the new card in SCREENS.parent): every real grade
   rolls up under its subject automatically, and every subject renders even
   with nothing entered — the visible gap is the point. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8104;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const r = await p.evaluate(() => {
    // A stable "today" inside Quarter 1 (2026-08-03 to 2026-10-02).
    AZ.today = () => '2026-09-01';
    const [c1, c2, c3] = STUDY_CLASSES.map(c=>c.id);

    // c1: two graded assessments this quarter -> average of 90 and 70 = 80.
    put({id:'assess_1', type:'assess', classId:c1, kind:'test', title:'Unit test',
      date:'2026-08-20', points:90, outOf:100, score:90});
    put({id:'assess_2', type:'assess', classId:c1, kind:'quiz', title:'Pop quiz',
      date:'2026-08-25', points:70, outOf:100, score:70});

    // c2: one added, not marked yet (score null).
    put({id:'assess_3', type:'assess', classId:c2, kind:'test', title:'Chapter test',
      date:'2026-08-28', points:null, outOf:100, score:null});

    // c1 also has a grade from a PRIOR quarter (2026-06 — before Q1 even starts,
    // so it should never appear at all, but definitely not pull into Q1's average).
    put({id:'assess_4', type:'assess', classId:c1, kind:'test', title:'Summer placement',
      date:'2026-06-01', points:50, outOf:100, score:50});

    // c3 gets nothing at all — the visible-gap case.

    saveLocal();
    go('parent');
    return {
      c1, c2, c3,
      rows: gradesBySubject('2026-09-01')
    };
  });

  const byId = id => r.rows.find(x=>x.cls.id===id);
  ck('c1 shows 2 graded, average 80 (excludes the pre-quarter grade)',
     byId(r.c1).graded===2 && byId(r.c1).avg===80 && byId(r.c1).count===2, byId(r.c1));
  ck('c2 shows 0 graded, 1 pending', byId(r.c2).graded===0 && byId(r.c2).pending===1, byId(r.c2));
  ck('c3 (no assessments at all) shows count 0, avg null', byId(r.c3).count===0 && byId(r.c3).avg===null, byId(r.c3));
  ck('every STUDY_CLASSES subject is represented, none dropped',
     r.rows.length === new Set(r.rows.map(x=>x.cls.id)).size && r.rows.every(x=>x.cls), r.rows.length);

  const dom = await p.evaluate(() => {
    const txt = document.getElementById('screen').innerText;
    return {
      hasByHeader: /By subject · Quarter 1/i.test(txt),
      hasNoGradesLine: /No grades entered yet/.test(txt),
      hasPendingLine: /1 grade · 1 not marked yet/.test(txt) || /0 grade.*1 not marked yet/.test(txt),
      has80pct: /80%/.test(txt)
    };
  });
  ck('card header names the quarter', dom.hasByHeader, dom);
  ck('the empty subject visibly says "No grades entered yet"', dom.hasNoGradesLine, dom);
  ck('the pending subject shows its not-marked-yet count', dom.hasPendingLine, dom);
  ck('the graded subject shows its 80% average', dom.has80pct, dom);

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got).slice(0,300))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
