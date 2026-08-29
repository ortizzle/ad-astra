/* Biology Test 1 Study Guide (content/bio-sg-test1.json) + the test-prep
   standout treatment: prep-flagged units (and paper guides, which are prep by
   definition) wear the gold band on their card and the gold ring on the map. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8115;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    for (const f of ['bio-unit-1','bio-unit-2','bio-unit-3-enzymes','bio-quiz1-review','bio-sg-test1']) {
      const res = await fetch(`./content/${f}.json`, {cache:'no-store'});
      const j = await res.json();
      const u = Object.values(j.records)[0];
      u.status = 'approved'; u.updatedAt = Date.now() - 1000;
      DATA.records[u.id] = u;
    }
    saveLocal();
    const u = DATA.records['unit-bio-sgt1'];
    return {cards: u.cards.length, questions: u.questions.length, prep: !!u.prep, classId: u.classId};
  });
  ck('unit loads: 27 cards, 24 questions, prep:true, classId bio',
     seed.cards === 27 && seed.questions === 24 && seed.prep && seed.classId === 'bio', seed);

  const shelf = await p.evaluate(() => {
    go('shelf', {classId:'bio', series:'Biology 8', open:'unit-bio-sgt1'});
    const stops = [...document.querySelectorAll('#screen .stop')];
    const prepStops = stops.filter(s => s.classList.contains('prep'));
    const pip = prepStops[0] && prepStops[0].querySelector('.pip');
    const oc = document.getElementById('shelfopen');
    return {
      totalStops: stops.length,
      prepStops: prepStops.map(s => s.querySelector('.t').textContent),
      pipGold: pip ? getComputedStyle(pip).borderColor : null,
      openIsPrepCard: oc ? oc.classList.contains('prepcard') : false,
      bandText: oc && oc.querySelector('.prepband') ? oc.querySelector('.prepband').textContent : null,
      openTitle: oc ? oc.querySelector('h3').textContent : null
    };
  });
  ck('the Biology shelf shows both prep stops (Quiz Review guide + new Study Guide)',
     shelf.prepStops.length === 2, shelf.prepStops);
  ck('prep stops wear the gold pip ring', /242, 202, 99/.test(shelf.pipGold||''), shelf.pipGold);
  ck('the opened Study Guide card is a prepcard with the Test prep band',
     shelf.openIsPrepCard && /Test prep/i.test(shelf.bandText||''), shelf);
  ck('the opened card is the Study Guide', /Test 1 Study Guide/.test(shelf.openTitle||''), shelf.openTitle);

  // A non-prep lesson must NOT get the band.
  const plain = await p.evaluate(() => {
    ctx.open = 'unit-bio-u2'; render();
    const oc = document.getElementById('shelfopen');
    return {isPrep: oc.classList.contains('prepcard'), hasBand: !!oc.querySelector('.prepband')};
  });
  ck('an ordinary lesson gets no prep treatment', !plain.isPrep && !plain.hasBand, plain);

  // Flashcards + a full quiz round (exercises the kind:'order' pH question when drawn).
  const cards = await p.evaluate(async () => {
    go('cards', {unitId:'unit-bio-sgt1', classId:'bio'});
    let steps = 0;
    while (cardState.unitId === 'unit-bio-sgt1' && steps++ < 60) {
      const knowBtn = [...document.querySelectorAll('button')].find(x => /Knew it/.test(x.textContent));
      if (!knowBtn) break;
      knowBtn.click();
      await new Promise(r => setTimeout(r, 4));
    }
    return steps;
  });
  ck('the 27-card deck completes cleanly', cards < 60, cards);

  const quiz = await p.evaluate(async () => {
    quizState = null;
    go('quiz', {unitId:'unit-bio-sgt1', classId:'bio'});
    let guard = 0;
    while (view === 'quiz' && guard++ < 20) {
      const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
      if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,5)); }
      await new Promise(r => setTimeout(r, 10));
      const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if (next) { next.click(); await new Promise(r=>setTimeout(r,10)); continue; }
      if (!opts.length) break;
    }
    return {logged: all('log').some(l => l.unitId === 'unit-bio-sgt1')};
  });
  ck('a full quiz round completes and logs', quiz.logged, quiz);

  // No Beat-the-clock door: study guides are book:true.
  const noClock = await p.evaluate(() => {
    ctx.open = 'unit-bio-sgt1'; go('shelf', {classId:'bio', series:'Biology 8', open:'unit-bio-sgt1'});
    return !/Beat the clock/.test(document.getElementById('shelfopen').textContent);
  });
  ck('no Beat the clock on the study guide (book:true)', noClock, noClock);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
