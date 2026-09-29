/* v199 — Sedona's US History Unit 2 (Revolution and Independence), three parts
   from the teacher's 2.1–2.3 test-topics list.

   The list NAMES what is tested and says nothing about it, and her class notes
   for Unit 2 are not in Drive — so the substance is standard US history and
   every card and question must be flagged `added`, never `source`. That
   provenance rule is pinned here, alongside the two traps the list itself
   sets: "Treaty of Paris" under BOTH 2.1 and 2.3 (two treaties, 1763 and 1783),
   and "Phyllis Wheatley", whom the card teaches as Phillis.

   Teaching is pinned by what the units SAY, never by question id. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
const IDS = ['unit-hist-u2p1','unit-hist-u2p2','unit-hist-u2p3'];
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    // Unit 1 is seeded alongside so "its own shelf" is a claim about coexisting.
    const files = ['history-u2-p1','history-u2-p2','history-u2-p3',
                   'history-u1-p1','history-u1-p2','history-u1-p3','history-u1-p4','history-u1-p5'];
    for (const f of files) {
      const j = await (await fetch('./content/'+f+'.json',{cache:'no-store'})).json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u;
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id, classId:u.classId, title:u.title, libv:u.libv, prep:!!u.prep, order:u.order,
              cards:u.cards, qs:u.questions, objectives:u.objectives,
              note:(u.parentNote||{}).text||'', blob:JSON.stringify(u)}; };
    return ['unit-hist-u2p1','unit-hist-u2p2','unit-hist-u2p3'].map(pick);
  });
  const [p1, p2, p3] = seed;
  const allQ = seed.flatMap(u => u.qs), allC = seed.flatMap(u => u.cards);

  // ── the shelf ──
  const sh = await p.evaluate(() => {
    const r = shelvesFor('history');
    return {loose: r.loose.map(u=>u.title), books: r.shelves.map(s => ({name:s.name, parts:s.lessons.map(u=>u.title)}))};
  });
  const u2 = sh.books.find(s => s.name === 'Unit 2'), u1 = sh.books.find(s => s.name === 'Unit 1');
  ck('every part is classId history (the v136 orphan trap)', seed.every(u => u.classId === 'history'), seed.map(u=>u.classId));
  ck('Unit 2 is its own shelf beside Unit 1, nothing loose',
     !!u2 && !!u1 && sh.loose.length === 0, sh);
  ck('Unit 2 runs 1 → 2 → 3 in teaching order',
     u2 && u2.parts.length === 3 && u2.parts.every((t,i) => t.startsWith(`Unit 2 · ${i+1} `)), u2 && u2.parts);
  ck('Unit 1 still holds its five parts', u1 && u1.parts.length === 5, u1 && u1.parts);
  ck('all three are prep, carry libv, and set no order (v194)',
     seed.every(u => u.prep && u.libv >= 1 && u.order == null), seed.map(u => [u.prep, u.libv, u.order]));

  // ── provenance: a topic list is not a source of facts ──
  ck('every card and question is flagged added, never source',
     allC.every(c => c.from === 'added') && allQ.every(q => q.from === 'added'),
     allC.concat(allQ).filter(x => x.from !== 'added').map(x => x.id));
  ck('the objectives ARE the list, so they say source',
     seed.every(u => u.objectives.every(o => o.from === 'source')));
  ck('every parent note says the notes were not in Drive and the facts are added',
     seed.every(u => /not in Drive/.test(u.note)), seed.map(u => u.note.slice(0,80)));

  // ── structure ──
  const mc = allQ.filter(q => q.kind !== 'order');
  ck('answers are spread across all four slots in each part (the v181 _balance bug)',
     seed.every(u => [0,1,2,3].every(i => u.qs.filter(q => q.kind !== 'order' && q.ans === i).length > 0)),
     seed.map(u => [0,1,2,3].map(i => u.qs.filter(q => q.kind !== 'order' && q.ans === i).length)));
  ck('every MC question has four unique options', mc.every(q => q.opts.length === 4 && new Set(q.opts).size === 4));
  ck('each part carries a chronology question stored in order (ans 0)',
     seed.every(u => u.qs.some(q => q.kind === 'order' && q.ans === 0)));
  const leans = allQ.filter(q => /^(the|that) same\b/i.test(q.q.trim()) || /\b(topic list|your list|your notes|the worksheet)\b/i.test(q.q)).map(q => q.id);
  ck('no stem leans on a sibling or points at her list', leans.length === 0, leans);
  ck('no positional options', !allQ.some(q => /\b(all|none) of the above\b/i.test(q.opts.join(' '))));

  // ── the two traps the list itself sets ──
  const q1763 = p1.qs.find(q => /Treaty of Paris of 1763/.test(q.q));
  const q1783 = p3.qs.find(q => /Treaty of Paris of 1783/.test(q.q));
  const qBoth = p3.qs.find(q => /1763 AND in 1783/.test(q.q));
  ck('1763 is taught as the end of the French and Indian War',
     q1763 && /French and Indian War/.test(q1763.opts[q1763.ans]), q1763 && q1763.opts[q1763.ans]);
  ck('1783 is taught as the end of the Revolution',
     q1783 && /Revolution/.test(q1783.opts[q1783.ans]), q1783 && q1783.opts[q1783.ans]);
  ck('one question asks why there are two, and its answer says two treaties',
     qBoth && /two treaties/i.test(qBoth.opts[qBoth.ans]), qBoth && qBoth.opts[qBoth.ans]);
  // The other wrong option on each treaty question is the OTHER treaty.
  ck('each treaty question offers the other treaty as a real wrong option',
     q1763 && q1763.opts.some((o,i) => i !== q1763.ans && /Revolution/.test(o)) &&
     q1783 && q1783.opts.some((o,i) => i !== q1783.ans && /French and Indian War/.test(o)));
  const wheat = p3.cards.find(c => /Wheatley/.test(c.term));
  /* Only what SHE sees is swept. The parent note names the list's spelling
     on purpose, and third person is correct there. */
  const seen3 = JSON.stringify(p3.cards) + JSON.stringify(p3.qs);
  ck('the card teaches PHILLIS, and names Phyllis only as a variant',
     wheat && wheat.term === 'Phillis Wheatley' && /spelled "Phyllis"/.test(wheat.def) &&
     !/Phyllis Wheatley/.test(seen3), wheat && wheat.term);

  // ── teaching, by what it says ──
  ck('2.1: the war was over land and trade in the Ohio River Valley', /Ohio River/.test(p1.blob));
  ck("2.1: Pontiac's Rebellion is the reason for the Proclamation", /Pontiac/.test(p1.blob) && /Appalachian/.test(p1.blob));
  ck('2.2: salutary neglect ended because Britain needed money', /needed money/.test(p2.blob));
  const tea = p2.qs.find(q => /Tea Act of 1773 actually do/.test(q.q));
  ck('2.2: the Tea Act made tea CHEAPER, and "doubled the price" is a wrong option',
     tea && /kept the tax/.test(tea.opts[tea.ans]) && tea.opts.some(o => /doubled the price/.test(o)),
     tea && tea.opts);
  ck('2.2: Locke = natural rights, Montesquieu = separation of powers, asked both ways',
     p2.qs.some(q => /John Locke best known/.test(q.q) && /natural rights/.test(q.opts[q.ans])) &&
     p2.qs.some(q => /split into separate branches/.test(q.q) && q.opts[q.ans] === 'Montesquieu'));
  ck('2.2: the Revere engraving is read as propaganda — a source can be real AND biased',
     /real AND biased/.test(p2.blob));
  ck('2.3: every advantages question uses the OTHER side\'s traits as wrong options',
     p3.qs.some(q => /biggest DISADVANTAGE for Britain/.test(q.q)) &&
     p3.qs.some(q => /colonial DISADVANTAGE/.test(q.q)));
  ck('2.3: Saratoga won France, and France won Yorktown',
     /Saratoga won France/.test(p3.blob) && /French navy/.test(p3.blob));
  ck('2.3: Freeman used the constitution\'s own words, quoted', /all men are born free and equal/.test(p3.blob));

  // ── primary sources, quoted exactly ──
  const DECL = 'We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness.';
  const passQ = allQ.filter(q => q.passage);
  ck('the Declaration passage is quoted exactly, twice, under 45 words',
     passQ.filter(q => q.passage === DECL).length === 2 && DECL.split(/\s+/).length < 45);
  ck('the Common Sense passage is under 45 words', passQ.every(q => q.passage.split(/\s+/).length < 45));

  // ── privacy: this repo is public ──
  ck('no student name, teacher name or mark anywhere in the shipped records',
     !seed.some(u => /Sedona|Ortiz|Guevara|score:|she got|\/\s*\d+\s*points/i.test(u.blob)));

  // ── the gold prep treatment on the shelf ──
  const gold = await p.evaluate(() => {
    go('shelf', {classId:'history', series:'Unit 2', open:'unit-hist-u2p2'});
    const stops = [...document.querySelectorAll('#screen .stop')];
    const oc = document.getElementById('shelfopen');
    return {stops: stops.length, prep: stops.filter(s => s.classList.contains('prep')).length,
            band: oc && oc.querySelector('.prepband') ? oc.querySelector('.prepband').textContent : null};
  });
  ck('all three stops are gold-ringed and the opened card wears the band',
     gold.stops === 3 && gold.prep === 3 && /Test prep/i.test(gold.band||''), gold);

  // ── a full round on each part ──
  for (const u of seed) {
    const play = await p.evaluate(async (uid) => {
      quizState = null;
      go('quiz', {unitId: uid, classId: 'history'});
      let guard = 0;
      while (view === 'quiz' && guard++ < 90) {
        const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
        if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,4)); }
        await new Promise(r=>setTimeout(r,8));
        const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
        if (next) { next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
        if (!opts.length) break;
      }
      document.querySelectorAll('.modal-back, .modal').forEach(m => m.remove());
      const l = all('log').find(x => x.unitId === uid && x.mode === 'quiz');
      return {logged: !!l, total: l && l.total};
    }, u.id);
    ck(u.title + ': a full quiz round plays and logs', play.logged && play.total === 5, play);
  }

  // A passage renders on its own plate.
  const pass = await p.evaluate(() => {
    const u = DATA.records['unit-hist-u2p2'];
    const q = u.questions.find(x => x.passage);
    quizState = null;
    go('quiz', {unitId:u.id, classId:'history'});
    quizState.order = [u.questions.indexOf(q)]; quizState.i = 0;
    render();
    const n = document.querySelector('#screen .passage');
    return {shown: !!n, text: n ? n.textContent.slice(0,40) : null, want: q.passage.slice(0,40)};
  });
  ck('a primary-source passage renders as its own plate', pass.shown && pass.text === pass.want, pass);

  const deck = await p.evaluate(async (uid) => {
    go('cards', {unitId: uid, classId: 'history'});
    const total = cardState.order.length; let seen = 0;
    while (cardState && cardState.unitId === uid && seen < 40) {
      const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
      if (!knew) break;
      seen++; knew.click(); await new Promise(r=>setTimeout(r,5));
    }
    return {seen, total};
  }, 'unit-hist-u2p2');
  ck('the Road to Revolution deck walks to the end', deck.seen >= deck.total && deck.total >= 12, deck);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + String(JSON.stringify(r.got)).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,5) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
