/* The Growth Zone, filtered. Chris: the ladder had grown large and unappealing,
   and in test week there was no way to pick "just maths, just the recent
   topic". Chips now scope the WHOLE ladder (due and settling) by subject, then
   by unit ranked most-recently-missed; a second door reviews everything in the
   filter ahead of time; rows fold to the question and its ladder bar.
   Same file in both apps. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  /* Seed: two subjects; the first has TWO units, one missed recently and one
     missed a week ago; only some misses are due. A test in 3 days on subject A. */
  const seed = await p.evaluate(async () => {
    const files = CONTENT_LIBRARY.slice();
    const units = [];
    for (const f of files) {
      try {
        const j = await (await fetch(f, {cache:'no-store'})).json();
        Object.values(j.records||{}).forEach(r => {
          if (r.type==='unit' && !r.deleted && (r.questions||[]).length >= 4 && !r.guide && !r.own && r.classId!=='__all__'
              && r.questions.slice(0,3).every(q => !q.kind || q.kind==='mc')) {
            r.status='approved'; DATA.records[r.id]=r; units.push(r);
          }
        });
      } catch(e){}
    }
    const byC = {};
    units.forEach(u => (byC[u.classId] = byC[u.classId]||[]).push(u));
    const cidA = Object.keys(byC).find(c => byC[c].length >= 2);
    const cidB = Object.keys(byC).find(c => c !== cidA);
    const [uA1, uA2] = byC[cidA]; const uB = byC[cidB][0];
    const today = AZ.today(), now = Date.now();
    const WHY = 'The right answer follows from the definition rather than the example: check which quantity the question actually asks for, then match it to the rule you learned, and the other three options fall away one by one.';
    const mk = (u, q, due, box, on) => put({ id:'miss_'+u.id+'_'+q.id, type:'miss', unitId:u.id, classId:u.classId,
      qid:q.id, q:q.q, opts:q.opts, ans:q.ans, right:q.opts[q.ans], chose:q.opts[(q.ans+1)%q.opts.length],
      why:WHY, on, box, due });
    // uA1: recent (missed today), 3 misses, 2 due + 1 settling
    uA1.questions.slice(0,3).forEach((q,i) => mk(uA1, q, i<2 ? today : AZ.shift(today,4), i<2 ? 0 : 2, today));
    // uA2: old (missed a week ago), 2 misses, both settling
    uA2.questions.slice(0,2).forEach((q,i) => mk(uA2, q, AZ.shift(today,6), 3, AZ.shift(today,-7)));
    // uB: 2 misses, 1 due
    uB.questions.slice(0,2).forEach((q,i) => mk(uB, q, i===0 ? today : AZ.shift(today,2), i, AZ.shift(today,-3)));
    put({id:'assess_gz', type:'assess', classId:cidA, kind:'test', title:'Filter test', date:AZ.shift(today,3)});
    saveLocal();
    return {cidA, cidB, uA1:uA1.id, uA2:uA2.id, uB:uB.id, total: all('miss').length, due: dueMisses().length};
  });
  ck('seed: 7 misses across 2 subjects and 3 units, 3 due', seed.total===7 && seed.due===3, seed);

  const read = () => p.evaluate(() => {
    const sc = document.getElementById('screen');
    const chips = [...sc.querySelectorAll('.gz-chips:not(.units) .gz-chip')].map(n=>({t:n.textContent, on:n.classList.contains('on')}));
    const uchips = [...sc.querySelectorAll('.gz-chips.units .gz-chip')].map(n=>({t:n.textContent, on:n.classList.contains('on')}));
    const card = [...sc.querySelectorAll('.card')].find(c => [...c.querySelectorAll('.btn')].some(b=>/review/i.test(b.textContent)));
    const btns = card ? [...card.querySelectorAll('.btn')].map(b=>b.textContent) : [];
    const h2 = card ? ((card.querySelector('h2')||{}).textContent || '') : '';
    const rows = [...sc.querySelectorAll('.miss')];
    const lastBtn = card ? [...card.querySelectorAll('.btn')].pop() : null;
    const capP = card ? card.querySelector('p') : null;
    return {chips, uchips, btns, h2, rows: rows.length,
            folded: rows.filter(r=>r.classList.contains('fold')).length,
            open: rows.filter(r=>!r.classList.contains('fold')).length,
            height: sc.scrollHeight,
            btnCapGap: (lastBtn && capP) ? capP.getBoundingClientRect().top - lastBtn.getBoundingClientRect().bottom : null};
  });

  await p.evaluate(() => { gzFilter = {cid:null, unitId:null}; gzOpen = {}; go('growth'); });
  await p.waitForTimeout(150);
  let v = await read();
  ck('unfiltered: "Everything · 7" leads and the test subject is next',
     /^Everything · 7/.test(v.chips[0].t) && v.chips[0].on && /test in 3 days/.test(v.chips[1].t), v.chips);
  ck('unfiltered: no unit chips', v.uchips.length === 0, v.uchips);
  ck('unfiltered: 3 are back, and the ahead-of-time door offers all 7',
     /^3 questions are back$/.test(v.h2) && v.btns.some(t=>/Review all 7 · ahead of time/.test(t)), {h2:v.h2, btns:v.btns});
  ck('every row starts folded', v.rows === 7 && v.folded === 7, v);
  ck('the caption under "Start review" keeps a real gap, not flush against the button', v.btnCapGap === 10, v.btnCapGap);
  const hFolded = v.height;

  // Tap a row: it opens, shows the answer, and only that one opens.
  const opened = await p.evaluate(() => {
    document.querySelector('#screen .miss .mhead').click();
    const r = document.querySelector('#screen .miss');
    return {open: !r.classList.contains('fold'), hasAnswer: !!r.querySelector('.a'), chose: !!r.querySelector('.n'),
            others: [...document.querySelectorAll('#screen .miss')].slice(1).every(x=>x.classList.contains('fold'))};
  });
  ck('tapping a row unfolds just that row, with its answer', opened.open && opened.hasAnswer && opened.chose && opened.others, opened);

  // Pick subject A.
  await p.evaluate(() => { document.querySelectorAll('#screen .gz-chips:not(.units) .gz-chip')[1].click(); });
  await p.waitForTimeout(150);
  v = await read();
  ck('subject chip scopes the screen: 5 rows, chip lit, headline names the subject',
     v.rows === 5 && v.chips[1].on && !v.chips[0].on && /in /.test(v.h2), {rows:v.rows, h2:v.h2});
  ck('unit chips appear, most recently missed unit first',
     v.uchips.length === 3 && /^Every unit · 5/.test(v.uchips[0].t) && /· 3$/.test(v.uchips[1].t) && /· 2$/.test(v.uchips[2].t), v.uchips);
  ck('the ahead-of-time door now offers the 5 in that subject',
     v.btns.some(t=>/Review all 5 in .* · ahead of time/.test(t)), v.btns);

  // Pick the old unit (no due questions in it) — the ahead-of-time door becomes primary.
  await p.evaluate(() => { document.querySelectorAll('#screen .gz-chips.units .gz-chip')[2].click(); });
  await p.waitForTimeout(150);
  v = await read();
  const primaryAhead = await p.evaluate(() => {
    const card = [...document.querySelectorAll('#screen .card')].find(c => [...c.querySelectorAll('.btn')].some(b=>/review/i.test(b.textContent)));
    const b = card && card.querySelector('.btn-primary');
    return b ? b.textContent : null;
  });
  ck('unit chip narrows to 2 rows and says nothing is due there',
     v.rows === 2 && /^Nothing due in/.test(v.h2), {rows:v.rows, h2:v.h2});
  ck('with nothing due, "ahead of time" is the primary button',
     /Review all 2 .* ahead of time/.test(primaryAhead||''), primaryAhead);

  // Take that door: the round holds exactly those 2 settling questions.
  const round = await p.evaluate((uA2) => {
    const card = [...document.querySelectorAll('#screen .card')].find(c => [...c.querySelectorAll('.btn')].some(b=>/review/i.test(b.textContent)));
    card.querySelector('.btn-primary').click();
    if (!quizState || quizState.unitId!=='__review__') return {state:'no round'};
    const u = unitFor('__review__');
    const ms = u.questions.map(q=>DATA.records[q._missId]).filter(Boolean);
    return {n:u.questions.length, allUnit: ms.every(m=>m.unitId===uA2), title:u.title, cls: ctx.classId};
  }, seed.uA2);
  ck('the round asks exactly the 2 questions from that unit, due or not',
     round.n===2 && round.allUnit && round.cls===seed.cidA, round);

  // Answer them right: box 3 → 4 promotes to LAST_BOX and clears (ordinary rule, no new rule).
  const settled = await p.evaluate(async (uA2) => {
    let guard = 0;
    while (view === 'quiz' && guard++ < 20) {
      const u = unitFor('__review__'); const q = u.questions[quizState.order[quizState.i]];
      const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
      if (opts.length) {
        const want = String(q.opts[q.ans]).trim();
        const right = opts.find(o => o.textContent.replace(/^[A-D]\s*/,'').trim() === want) || opts.find(o => o.textContent.trim().endsWith(want));
        (right || opts[0]).click(); await new Promise(r=>setTimeout(r,6));
      }
      const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if (next) { next.click(); await new Promise(r=>setTimeout(r,6)); continue; }
      if (!opts.length) break;
    }
    // dismiss results modal if present
    const close = document.querySelector('.modal .btn-primary, .modal .btn'); if (close) close.click();
    return {left: all('miss').filter(m=>m.unitId===uA2).length, cleared: all('cleared').filter(c=>c.unitId===uA2).length};
  }, seed.uA2);
  ck('an early review settles through the ordinary ladder: both box-3 misses clear',
     settled.left===0 && settled.cleared===2, settled);

  // Coming back: the filter is remembered, and its unit emptied so it falls back to the subject.
  await p.evaluate(() => go('growth'));
  await p.waitForTimeout(150);
  v = await read();
  ck('back on the screen the subject filter survives, the emptied unit chip is gone',
     v.chips[1].on && v.uchips.length === 0 && v.rows === 3, {chips:v.chips, uchips:v.uchips, rows:v.rows});

  // Height: folded list is much shorter than the same list fully open.
  const hOpen = await p.evaluate(() => {
    gzFilter = {cid:null, unitId:null};
    all('miss').forEach(m => gzOpen[m.id] = true); render();
    return document.getElementById('screen').scrollHeight;
  });
  ck('folding roughly halves the screen against the fully open list', hFolded < hOpen * 0.7, {folded:hFolded, open:hOpen});

  // Tap targets on the new controls.
  const taps = await p.evaluate(() => {
    gzOpen = {}; render();
    const small = [...document.querySelectorAll('#screen .gz-chip, #screen .mhead')]
      .map(b => ({t: b.textContent.slice(0,20), h: b.getBoundingClientRect().height})).filter(x => x.h < 44);
    return small;
  });
  ck('every chip and row head is at least 44px tall', taps.length === 0, taps);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,320))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
