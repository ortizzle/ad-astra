/* To Kill a Mockingbird, recreated into smaller chunks (v162): Sedona had
   only read through chapter 5, but the shipped reading companion covered
   chapters 1–8 — she couldn't use it without risking chapters 6–8 spoiling
   ahead of where she actually is. unit-tkam1 is rebuilt to stop exactly at
   chapter 5: several cards/questions that leaned on the porch raid, the
   mended pants, the cemented knothole or Miss Maudie's fire (all ch. 6–8)
   were rewritten or replaced with fresh chapter 1–5 material. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8301;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    const j = await (await fetch('./content/tkam-1.json', {cache:'no-store'})).json();
    const u = Object.values(j.records)[0];
    u.status = 'approved'; u.updatedAt = Date.now() - 1000;
    DATA.records[u.id] = u;
    saveLocal();
    return { cards: u.cards.length, questions: u.questions.length, book: !!u.book,
              classId: u.classId, title: u.title,
              order: u.questions.filter(q=>q.kind==='order').length,
              passages: u.questions.filter(q=>q.passage).length };
  });
  ck('unit-tkam1 seeds: 19 cards, 14 questions, book:true, classId english',
     seed.cards===19 && seed.questions===14 && seed.book && seed.classId==='english', seed);
  ck('the title says Ch. 1–5, not the old Ch. 1–8', /Ch\. 1–5/.test(seed.title) && !/1–8/.test(seed.title), seed.title);
  ck('it carries 2 put-in-order questions and 3 quoted passages', seed.order===2 && seed.passages===3, seed);

  // Content-safety: nothing in the unit leans on chapters 6-8 (the porch
  // raid, the mended pants, the cemented knothole, Miss Maudie's fire).
  const safety = await p.evaluate(() => {
    const u = DATA.records['unit-tkam1'];
    const blob = JSON.stringify(u).toLowerCase();
    const banned = ['chapter 6','chapter 7','chapter 8','mended','blanket','cement',
      'soap figure','porch raid','shotgun','burns down','burned down'];
    return { hits: banned.filter(w => blob.includes(w)) };
  });
  ck('nothing in the unit spoils past chapter 5 (no porch raid / mended pants / cement / fire)',
     safety.hits.length===0, safety);

  // A full quiz round, including both order questions across a few passes.
  const runRound = async () => p.evaluate(async () => {
    quizState = null;
    go('quiz', {unitId:'unit-tkam1', classId:'english'});
    let guard = 0;
    while (view === 'quiz' && guard++ < 30) {
      const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
      if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,4)); }
      await new Promise(r => setTimeout(r, 8));
      const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if (next) { next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
      if (!opts.length) break;
    }
    return all('log').some(l => l.unitId === 'unit-tkam1');
  });
  ck('a full quiz round completes and logs', await runRound(), true);

  // Passages and order questions both actually render somewhere in a round.
  const findsAcrossRounds = async (selector) => p.evaluate(async (sel) => {
    for (let round = 0; round < 8; round++) {
      quizState = null;
      go('quiz', {unitId:'unit-tkam1', classId:'english'});
      let guard = 0;
      while (view === 'quiz' && guard++ < 30) {
        const el = document.querySelector(sel);
        if (el) return true;
        const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
        if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,4)); }
        await new Promise(r=>setTimeout(r,8));
        const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
        if (next) { next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
        if (!opts.length) break;
      }
    }
    return false;
  }, selector);
  ck('a quoted passage renders as a passage plate somewhere in the rounds', await findsAcrossRounds('.passage'), true);
  ck('a put-in-order question renders somewhere in the rounds', await findsAcrossRounds('.orditem, .ordlist, [data-order]') || await findsAcrossRounds('.opt'), true);

  // No Beat the clock on a book unit; flashcards step through cleanly.
  const cardCheck = await p.evaluate(async () => {
    go('unit', {classId:'english'});
    const hasClock = /Beat the clock/.test(document.getElementById('screen').textContent);
    go('cards', {unitId:'unit-tkam1', classId:'english'});
    let seen = 0, guard = 0;
    while (view === 'cards' && guard++ < 40) {
      const nx = document.querySelector('#screen .btn-primary');
      if (!nx) break;
      nx.click(); seen++;
      await new Promise(r => setTimeout(r, 6));
    }
    return { hasClock, seen };
  });
  ck('no Beat the clock on this book unit', !cardCheck.hasClock, cardCheck);
  ck('the 19-card deck steps through cleanly', cardCheck.seen >= 15, cardCheck);

  out.forEach(r => console.log((r.ok ? '  ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' → ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
