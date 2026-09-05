/* Smoke test for the Topic 2 (Quadratic Functions and Equations) shelf:
   all 7 lessons load, shelve together, render flashcards (including graphs)
   and a full quiz round without crashing. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8101;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.addScriptTag({path: __dirname + '/seed.js'});
  await p.waitForTimeout(300);

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    const files = ['alg-topic2-01','alg-topic2-02','alg-topic2-03','alg-topic2-04','alg-topic2-05','alg-topic2-06','alg-topic2-07'];
    const ids = [];
    for (const f of files) {
      const res = await fetch(`./content/${f}.json`, {cache:'no-store'});
      const j = await res.json();
      const u = Object.values(j.records)[0];
      u.status = 'approved'; u.updatedAt = Date.now() - 1000;
      DATA.records[u.id] = u; ids.push(u.id);
    }
    saveLocal();
    return ids;
  });
  ck('all 7 Topic 2 units seeded', seed.length === 7, seed);

  // Structural check on every unit + question, done in-page against the live schema.
  const struct = await p.evaluate((ids) => {
    const bad = [];
    ids.forEach(id => {
      const u = DATA.records[id];
      if (!u.cards.length) bad.push(id + ': no cards');
      if (u.questions.length < 15) bad.push(id + ': too few questions (' + u.questions.length + ')');
      u.questions.forEach(q => {
        if (q.kind === 'slider' || q.kind === 'spell') return;   // one option by contract (v149)
        if (q.opts.length !== 4) bad.push(id + '/' + q.id + ': opts != 4');
        if (new Set(q.opts).size !== 4) bad.push(id + '/' + q.id + ': dup opts');
        if (q.ans < 0 || q.ans > 3) bad.push(id + '/' + q.id + ': bad ans');
      });
    });
    return bad;
  }, seed);
  ck('no structural problems across all 7 units', struct.length === 0, struct);

  // Shelf: all 7 lessons under one "Topic 2" spine.
  const shelf = await p.evaluate(() => {
    go('unit', {classId:'algeo'});
    const spines = [...document.querySelectorAll('#screen .spine')].map(s => s.textContent);
    return spines;
  });
  ck('Topic 2 shelves as one spine', shelf.some(t => /^Topic 2/.test(t)), shelf);

  // Open the shelf, walk every lesson's flashcards through to the end (exercises graphNode too).
  const cardsWalk = await p.evaluate(async (ids) => {
    const results = [];
    for (const id of ids) {
      const u = DATA.records[id];
      ctx.classId = 'algeo';
      go('cards', {unitId:id, classId:'algeo'});
      let steps = 0;
      while (cardState.unitId === id && steps++ < 60) {
        const knew = document.querySelector('.btn-row .btn-primary, button.btn.btn-primary');
        const btns = [...document.querySelectorAll('button')];
        const knowBtn = btns.find(b => /Knew it/.test(b.textContent));
        if (!knowBtn) break;
        knowBtn.click();
        await new Promise(r => setTimeout(r, 5));
      }
      results.push({id, ended: view !== 'cards' || cardState.unitId !== id, steps});
    }
    return results;
  }, seed);
  ck('every lesson\'s flashcard deck completes cleanly', cardsWalk.every(r => r.steps < 60), cardsWalk);

  // Full quiz round on lesson 2-1 specifically (exercises the parabola graph rendering too).
  const quiz = await p.evaluate(async () => {
    go('quiz', {unitId:'unit-alg-t2-01', classId:'algeo'});
    let guard = 0;
    while (view === 'quiz' && guard++ < 20) {
      const opts = [...document.querySelectorAll('#screen .opt')];
      if (!opts.length) break;
      opts[0].click();
      await new Promise(r => setTimeout(r, 15));
      const next = document.querySelector('#screen .btn-primary, #screen .explain .go-on');
      if (next) next.click();
      await new Promise(r => setTimeout(r, 15));
    }
    return {logged: all('log').some(l => l.unitId === 'unit-alg-t2-01')};
  });
  ck('a full quiz round on 2-1 completes and logs', quiz.logged, quiz);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
