/* Smoke test for the three new content files: the two Kinematics 1 physics
   units (flashcards + quiz, including the kind:'order' ramp-ranking
   question) and the Biology Quiz 1 guide unit (paper entry, grading,
   walkthrough, rescue round). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8106;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  // ---- Physics: seed both units, walk flashcards, run a full quiz round on each ----
  const physSeed = await p.evaluate(async () => {
    const ids = [];
    for (const f of ['phys-kinematics-equations','phys-ramp-lab']) {
      const res = await fetch(`./content/${f}.json`, {cache:'no-store'});
      const j = await res.json();
      const u = Object.values(j.records)[0];
      u.status = 'approved'; u.updatedAt = Date.now() - 1000;
      DATA.records[u.id] = u; ids.push(u.id);
    }
    saveLocal();
    return ids;
  });
  ck('both physics units seeded', physSeed.length === 2, physSeed);

  const physQuiz = await p.evaluate(async (ids) => {
    const results = [];
    for (const id of ids) {
      quizState = null;
      go('quiz', {unitId:id, classId:'physics'});
      let guard = 0;
      while (view === 'quiz' && guard++ < 30) {
        // kind:'order' needs every option tapped before "Lock it in" appears;
        // ordinary MC answers (and disables) on the first tap. Clicking every
        // currently-enabled .opt handles both without knowing which kind it is.
        const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
        if (opts.length) {
          for (const o of opts) { o.click(); await new Promise(r => setTimeout(r, 5)); }
        }
        // kind:'slider' (v149): drag the marker, then Place it.
        const rng = document.querySelector('#screen input[type=range]');
        if (rng && !opts.length && document.getElementById('nplace')) {
          rng.value = String((Number(rng.min) + Number(rng.max)) / 2);
          rng.dispatchEvent(new Event('input', {bubbles:true}));
          await new Promise(r => setTimeout(r, 10));
          const pl = document.getElementById('nplace'); if (pl && !pl.disabled) { pl.click(); opts.push(pl); }
        }
        await new Promise(r => setTimeout(r, 10));
        const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
        if (next) { next.click(); await new Promise(r => setTimeout(r, 10)); continue; }
        if (!opts.length) break;
      }
      results.push({id, logged: all('log').some(l => l.unitId === id), guard});
    }
    return results;
  }, physSeed);
  ck('both physics quiz rounds complete and log', physQuiz.every(r => r.logged), physQuiz);

  const physCards = await p.evaluate(async (ids) => {
    const results = [];
    for (const id of ids) {
      go('cards', {unitId:id, classId:'physics'});
      let steps = 0;
      while (cardState.unitId === id && steps++ < 40) {
        const knowBtn = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
        if (!knowBtn) break;
        knowBtn.click();
        await new Promise(r => setTimeout(r, 5));
      }
      results.push({id, steps});
    }
    return results;
  }, physSeed);
  ck('both flashcard decks complete cleanly (eq strings render)', physCards.every(r => r.steps < 40), physCards);

  // Structural check that the kind:'order' ramp question renders and can be answered.
  const orderCheck = await p.evaluate(() => {
    const u = DATA.records['unit-phys-eqs'];
    const oq = u.questions.find(q => q.kind === 'order');
    return {found: !!oq, optsLen: oq && oq.opts.length, ans: oq && oq.ans};
  });
  ck('the kind:order ramp-ranking question is well-formed', orderCheck.found && orderCheck.optsLen === 4 && orderCheck.ans === 0, orderCheck);

  // ---- Biology Quiz 1: guide flow, mirroring the sg-test2 pattern ----
  const bioGuide = await p.evaluate(async () => {
    const res = await fetch('./content/bio-quiz1-review.json', {cache:'no-store'});
    const j = await res.json();
    const u = Object.values(j.records)[0];
    DATA.records[u.id] = u; u.status = 'approved'; u.updatedAt = Date.now() - 1000;
    saveLocal();
    const o = { guide: !!u.guide, questions: u.questions.length, withVariants: u.questions.filter(q=>q.variant).length };
    // She gets 4 wrong.
    const wrongIdx = [1, 5, 9, 13];
    u.questions.forEach((q,i) => guideSet(u.id, q.id, wrongIdx.includes(i) ? (q.ans+1)%4 : q.ans));
    o.entered = guideCount(u.id);
    gradeGuide(u);
    const lg = logs().filter(l => l.unitId === u.id)[0];
    o.marked = {correct: lg.correct, total: lg.total, paper: lg.paper};
    o.misses = all('miss').filter(m => m.unitId === u.id).length;
    const rq = buildRescueUnit(u.id);
    o.rescue = rq.questions.length;
    o.everyRescueIsFresh = rq.questions.every(rv => {
      const orig = u.questions.find(q => 'rv_'+q.id === rv.id);
      return orig && rv.q !== orig.q && rv.opts.length === 4;
    });
    return o;
  });
  ck('bio guide unit loads with 18 questions, all with variants', bioGuide.questions === 18 && bioGuide.withVariants === 18, bioGuide);
  ck('paper entry: all 18 entered', bioGuide.entered === 18, bioGuide);
  ck('grading: 14 right, 4 wrong, tagged paper:true', bioGuide.marked.correct === 14 && bioGuide.marked.total === 18 && bioGuide.marked.paper, bioGuide.marked);
  ck('4 misses created', bioGuide.misses === 4, bioGuide);
  ck('rescue round serves 4 fresh variants', bioGuide.rescue === 4 && bioGuide.everyRescueIsFresh, bioGuide);

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got).slice(0,300))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
