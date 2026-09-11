/* v181 — Kinematics 2 (Ad Astra only): 2-1 Vectors and Components and
   2-2 Projectile Motion, built from the teacher's objective list and
   chapter 7.2.

   The shelf checks are the point: this is a NEW book, not a fifth part of
   Kinematics 1, and its two parts must sort in teaching order — which they
   only do because both carry the numbered form (v180's Biology lesson:
   "Projectile Motion" title-sorts ahead of "Vectors and Components"). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    const files = ['phys-ch3-describing-motion','phys-kinematics-equations',
                   'phys-kinematics-graphs','phys-ramp-lab',
                   'phys-k2-vectors','phys-k2-projectiles'];
    for (const f of files) {
      const j = await (await fetch('./content/'+f+'.json',{cache:'no-store'})).json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u;
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order,
              round:u.round, cards:u.cards, qs:u.questions, blob:JSON.stringify(u)}; };
    return {a: pick('unit-phys-k2-vectors'), b: pick('unit-phys-k2-projectiles')};
  });

  // v136's orphan trap: a classId CLASS_BY_ID doesn't know fails silently.
  ck('both units load under the real physics classId',
     seed.a.classId === 'physics' && seed.b.classId === 'physics',
     [seed.a.classId, seed.b.classId]);
  ck('both carry a libv and no order bucket',
     seed.a.libv >= 1 && seed.b.libv >= 1 && seed.a.order == null && seed.b.order == null,
     [seed.a.libv, seed.b.libv, seed.a.order, seed.b.order]);
  ck('both carry the NUMBERED form, so the shelf sorts structurally',
     /^Kinematics 2 · 2-1 /.test(seed.a.title) && /^Kinematics 2 · 2-2 /.test(seed.b.title),
     [seed.a.title, seed.b.title]);

  const shelf = await p.evaluate(() => {
    const s = shelvesFor('physics');
    return {names: s.shelves.map(x=>x.name), loose: s.loose.map(u=>u.title),
            k2: (s.shelves.find(x=>x.name==='Kinematics 2')||{units:[]}).units.map(u=>lessonLabel(u)),
            k1: (s.shelves.find(x=>x.name==='Kinematics 1')||{units:[]}).units.length};
  });
  ck('Kinematics 2 is its own shelf, 2-1 then 2-2, nothing loose',
     shelf.names.includes('Kinematics 2') && shelf.k2.length === 2 &&
     /^2-1 Vectors/.test(shelf.k2[0]) && /^2-2 Projectile/.test(shelf.k2[1]) &&
     shelf.loose.length === 0, shelf);
  ck('Kinematics 1 still holds its own four parts, untouched',
     shelf.k1 === 4, shelf.k1);

  // Structure.
  ck('2-1: 14 cards, 16 questions, four unique options each',
     seed.a.cards.length === 14 && seed.a.qs.length === 16 &&
     seed.a.qs.every(q => q.opts.length === 4 && new Set(q.opts).size === 4),
     [seed.a.cards.length, seed.a.qs.length]);
  ck('2-2: 16 cards, 17 questions, MC options all valid',
     seed.b.cards.length === 16 && seed.b.qs.length === 17 &&
     seed.b.qs.filter(q=>(q.kind||'mc')==='mc')
             .every(q => q.opts.length === 4 && new Set(q.opts).size === 4),
     [seed.b.cards.length, seed.b.qs.length]);
  // The bug this build actually found: build() never called _balance() here.
  for (const [nm, u] of [['2-1', seed.a], ['2-2', seed.b]]) {
    const slots = [0,1,2,3].map(i => u.qs.filter(q=>(q.kind||'mc')==='mc' && q.ans===i).length);
    ck(nm + ': answers are spread across all four slots, not all A',
       slots.every(n => n > 0), slots);
  }

  // Standalone rule, and the positional rule the shuffle depends on.
  const both = seed.a.qs.concat(seed.b.qs);
  ck('no stem back-references a neighbouring question',
     !both.some(q => /^(That same|The same|For that same|Using the same)\b/i.test(q.q)),
     both.filter(q => /^(That|The) same/i.test(q.q)).map(q=>q.q.slice(0,50)));
  ck('nothing refers to an option by position',
     !both.some(q => /\b(all|none) of the above\b|\b(first|second|third|last) (option|choice)\b/i
                      .test([q.q, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))),
     'ok');
  ck('every question carries 3-6 walkthrough steps',
     both.every(q => q.steps.length >= 3 && q.steps.length <= 6), 'ok');

  // The three traps each unit is built around, checked by their teaching.
  ck('2-1 teaches the radian-mode trap with the cos 60 test',
     /cos 60° = 0\.5/.test(seed.a.blob) && /radian mode/i.test(seed.a.blob), 'card "Degrees, not radians"');
  ck('2-1 teaches the 45° crossover as a CHECK, not just a fact',
     /At 45° the two components are equal/.test(seed.a.blob) &&
     /checking an answer at a glance/.test(seed.a.blob), 'card "The 45° special case"');
  ck('2-1 teaches that a component can never exceed its vector',
     /neither component can exceed the/.test(seed.a.blob), 'card "A component is never bigger…"');
  ck('2-2 teaches a_x = 0 and gravity as vertical-only',
     /no horizontal acceleration/i.test(seed.b.blob) &&
     /All of gravity’s effect is in the vertical direction/.test(seed.b.blob), 'cards');
  ck('2-2 teaches time as the bridge between the two problems',
     /The two problems share exactly one quantity: time/.test(seed.b.blob), 'card "Time is the bridge"');
  ck('2-2 offers the halved-range trap as a real wrong option',
     seed.b.qs.some(q => /range/i.test(q.q) && /20\.1 m/.test(q.opts.join('|'))) &&
     /stopping the clock at the peak/.test(seed.b.blob), 'q: range');
  ck('2-2 names ignoring air resistance as a simplification, not a fact',
     /a genuine '?\s*'?simplification rather than a fact/.test(seed.b.blob.replace(/\\n/g,' ')) ||
     /simplification rather than a fact/.test(seed.b.blob), 'card "Air resistance, set aside"');

  const ord = seed.b.qs.find(q => q.kind === 'order');
  ck('2-2 ships a correctly ordered kind:order ranking',
     ord && ord.opts.length === 4 && ord.ans === 0 && /launched/i.test(ord.opts[0]), ord && ord.opts);

  // The physics reference sheet must still reach these quizzes.
  const play = await p.evaluate(async (uid) => {
    quizState = null;
    go('quiz', {unitId: uid, classId: 'physics'});
    const sheet = [...document.querySelectorAll('#screen .tool')].some(t=>/Sheet/.test(t.textContent));
    let guard = 0;
    while (view === 'quiz' && guard++ < 80) {
      const chips = [...document.querySelectorAll('#screen .ordchip:not([disabled])')];
      if (chips.length) { chips[0].click(); await new Promise(r=>setTimeout(r,4)); continue; }
      const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
      if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,4)); }
      await new Promise(r=>setTimeout(r,8));
      const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if (next) { next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
      if (!opts.length) break;
    }
    const l = all('log').find(x => x.unitId === uid && x.mode === 'quiz');
    return {sheet, logged: !!l, total: l && l.total};
  }, 'unit-phys-k2-projectiles');
  ck('a full 2-2 round plays and logs, with the Sheet tool reachable',
     play.logged && play.total === 9 && play.sheet, play);

  const deck = await p.evaluate(async (uid) => {
    cardState = {}; go('cards', {unitId: uid, classId: 'physics'});
    let seen = 0;
    while (cardState.unitId === uid && seen++ < 40) {
      const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
      if (!knew) break;
      knew.click(); await new Promise(r=>setTimeout(r,5));
    }
    return {seen};
  }, 'unit-phys-k2-vectors');
  ck('the 2-1 flashcard deck steps all the way through', deck.seen >= 14, deck);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
