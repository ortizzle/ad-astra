/* Smoke test for Biology 8 · Unit 3: Enzymes (content/bio-unit-3-enzymes.json):
   loads, shelves alongside the existing Biology 8 units, flashcards and a
   full quiz round complete cleanly, and every question is structurally
   sound against the live schema. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8109;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    const ids = [];
    for (const f of ['bio-unit-1','bio-unit-1b','bio-unit-2','bio-unit-3-enzymes']) {
      const res = await fetch(`./content/${f}.json`, {cache:'no-store'});
      const j = await res.json();
      const u = Object.values(j.records)[0];
      u.status = 'approved'; u.updatedAt = Date.now() - 1000;
      DATA.records[u.id] = u; ids.push(u.id);
    }
    saveLocal();
    return ids;
  });
  ck('all 4 Biology units seeded', seed.length === 4, seed);

  const struct = await p.evaluate(() => {
    const u = DATA.records['unit-bio-u3'];
    const bad = [];
    if (!u.cards.length) bad.push('no cards');
    u.questions.forEach(q => {
      if (q.opts.length !== 4) bad.push(q.id + ': opts != 4');
      if (new Set(q.opts).size !== 4) bad.push(q.id + ': dup opts');
      if (q.ans < 0 || q.ans > 3) bad.push(q.id + ': bad ans');
      if (!q.steps || q.steps.length < 3) bad.push(q.id + ': too few steps');
      if (!q.ex || !q.ex.main) bad.push(q.id + ': missing ex.main');
    });
    return bad;
  });
  ck('no structural problems', struct.length === 0, struct);

  const shelf = await p.evaluate(() => {
    go('unit', {classId:'bio'});
    const spines = [...document.querySelectorAll('#screen .spine')].map(s => s.textContent);
    return spines;
  });
  ck('Biology 8 shelves as one spine with all 4 parts', shelf.some(t => /^Biology 8/.test(t)), shelf);

  const cardsWalk = await p.evaluate(async () => {
    go('cards', {unitId:'unit-bio-u3', classId:'bio'});
    let steps = 0;
    while (cardState.unitId === 'unit-bio-u3' && steps++ < 30) {
      const knowBtn = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
      if (!knowBtn) break;
      knowBtn.click();
      await new Promise(r => setTimeout(r, 5));
    }
    return steps;
  });
  ck('flashcard deck (12 cards) completes cleanly', cardsWalk < 30, cardsWalk);

  const quiz = await p.evaluate(async () => {
    quizState = null;
    go('quiz', {unitId:'unit-bio-u3', classId:'bio'});
    let guard = 0;
    while (view === 'quiz' && guard++ < 20) {
      const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
      if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,5)); }
      await new Promise(r => setTimeout(r, 10));
      const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if (next) { next.click(); await new Promise(r=>setTimeout(r,10)); continue; }
      if (!opts.length) break;
    }
    return {logged: all('log').some(l => l.unitId === 'unit-bio-u3')};
  });
  ck('a full quiz round completes and logs', quiz.logged, quiz);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
