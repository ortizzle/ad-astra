/* v189 — Kinematics 2 gains two parts (Ad Astra only):

   · Quiz 1 Review: Vectors and Trig — built from the BLANK quiz paper her
     teacher shared as study material. Fresh numbers throughout, so what is
     asserted here is the five SKILLS the paper tests, never its own items.
   · 2-3 Horizontal Projectile Motion Lab — the reasoning behind a lab whose
     data does not exist yet, the same call the Ramp Lab unit made.

   The shelf check is the structural one: four parts, the three numbered
   lessons in teaching order and the order:1 review trailing them. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    const files = ['phys-kinematics-equations','phys-kinematics-graphs','phys-ramp-lab',
                   'phys-ch3-describing-motion','phys-k2-vectors','phys-k2-projectiles',
                   'phys-k2-quiz1-review','phys-k2-lab'];
    for (const f of files) {
      const j = await (await fetch('./content/'+f+'.json',{cache:'no-store'})).json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u;
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order,
              round:u.round, prep:!!u.prep, cards:u.cards, qs:u.questions,
              note:(u.parentNote||{}).text||'', blob:JSON.stringify(u)}; };
    return {r: pick('unit-phys-k2-sgq1'), l: pick('unit-phys-k2-lab')};
  });

  // v136's orphan trap — a classId CLASS_BY_ID doesn't know fails silently.
  ck('both units load under the real physics classId',
     seed.r.classId === 'physics' && seed.l.classId === 'physics',
     [seed.r.classId, seed.l.classId]);
  ck('both carry a libv so a later fix survives the approval race',
     seed.r.libv >= 1 && seed.l.libv >= 1, [seed.r.libv, seed.l.libv]);
  ck('the review is prep:true and order:1; the lab is a numbered lesson with neither',
     seed.r.prep && seed.r.order === 1 && !seed.l.prep && seed.l.order == null,
     [seed.r.prep, seed.r.order, seed.l.prep, seed.l.order]);
  ck('the lab carries the numbered form, so it sorts after 2-2 structurally',
     /^Kinematics 2 · 2-3 /.test(seed.l.title), seed.l.title);

  const shelf = await p.evaluate(() => {
    const s = shelvesFor('physics');
    return {loose: s.loose.map(u=>u.title),
            k2: (s.shelves.find(x=>x.name==='Kinematics 2')||{units:[]}).units.map(u=>lessonLabel(u)),
            k1: (s.shelves.find(x=>x.name==='Kinematics 1')||{units:[]}).units.length};
  });
  ck('Kinematics 2 holds four parts: 2-1, 2-2, 2-3, then the review',
     shelf.k2.length === 4 && /^2-1 /.test(shelf.k2[0]) && /^2-2 /.test(shelf.k2[1]) &&
     /^2-3 /.test(shelf.k2[2]) && /Quiz 1 Review/.test(shelf.k2[3]), shelf.k2);
  ck('Kinematics 1 is untouched and nothing fell loose',
     shelf.k1 === 4 && shelf.loose.length === 0, shelf);

  // Structure + the v181 _balance bug, pinned.
  for (const [nm, u] of [['review', seed.r], ['lab', seed.l]]) {
    const mc = u.qs.filter(q => (q.kind||'mc') === 'mc');
    ck(nm + ': every MC question has four unique options and a valid answer',
       mc.length > 0 && mc.every(q => q.opts.length === 4 && new Set(q.opts).size === 4 &&
                                      q.ans >= 0 && q.ans < 4), mc.length);
    const slots = [0,1,2,3].map(i => mc.filter(q => q.ans === i).length);
    ck(nm + ': answers are spread across all four slots, not all A',
       slots.every(n => n > 0), slots);
    ck(nm + ': at least 18 questions across all three levels',
       u.qs.length >= 18 && [1,2,3].every(lv => u.qs.some(q => q.lv === lv)), u.qs.length);
  }

  const both = seed.r.qs.concat(seed.l.qs);
  ck('no stem opens on a neighbouring question’s scenario',
     !both.some(q => /^(That same|The same|For that same|Using the same)\b/i.test(q.q)) &&
     !both.some(q => /that same/i.test(q.q)),
     both.filter(q => /same/i.test(q.q)).map(q=>q.q.slice(0,46)));
  ck('nothing refers to an option by position',
     !both.some(q => /\b(all|none) of the above\b|\b(first|second|third|last) (option|choice)\b/i
                      .test([q.q, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');
  ck('every question carries 3-6 walkthrough steps',
     both.every(q => q.steps.length >= 3 && q.steps.length <= 6), 'ok');

  /* The five gaps the blank quiz tests that 2-1 does not already teach.
     Asserted by their TEACHING, so a renumber cannot break them. */
  ck('review: collapses an opposing pair before reaching for a triangle',
     /Collapse the opposing pair first/.test(seed.r.blob) &&
     seed.r.qs.some(q => /180 N north, 80 N south/.test(q.q)), 'card + question');
  ck('review: teaches head-to-tail AND that the order cannot change the resultant',
     /tail of the FIRST to the tip of the LAST/.test(seed.r.blob) &&
     /the same set of vectors gives the same/i.test(seed.r.blob), 'cards');
  ck('review: names the north-of-west / west-of-north trap and its 40°',
     /North of west is not west of north/.test(seed.r.blob) &&
     /they are 40° apart/.test(seed.r.blob), 'card');
  ck('review: teaches a ratio as a unit bridge, and rounding a COUNT up',
     /Round up when you are counting objects/.test(seed.r.blob) &&
     seed.r.qs.some(q => /ream/.test(q.q) && /lb/.test(q.opts.join('|'))), 'card + question');
  ck('review: carries the plain definitions of vector, scalar and resultant',
     ['Vector','Scalar','Resultant'].every(t => seed.r.cards.some(c => c.term === t)),
     seed.r.cards.map(c=>c.term).slice(0,5));
  ck('review: says a bare angle with no axis named is not an answer',
     seed.r.qs.some(q => /not yet an answer/i.test(q.q)) &&
     /could describe four different directions/.test(seed.r.blob), 'q + option');

  // The lab's own three load-bearing ideas.
  ck('lab: derives the merged equation the handout asks for',
     /Δx = v √\(2Δy \/ g\)/.test(seed.l.blob), 'card "Merging them into one"');
  ck('lab: the slope is v√(2/g), NOT the launch speed itself',
     /so it is not the speed itself/.test(seed.l.blob) &&
     seed.l.qs.some(q => /slope of 5\.72/.test(q.q)), 'card + question');
  ck('lab: the Moon steepens the line by about 2.46, never "six times"',
     /2\.46/.test(seed.l.blob) && /nothing like six times/.test(seed.l.blob), 'question');
  ck('lab: quadrupling the height only doubles the range',
     seed.l.qs.some(q => /0\.50 m/.test(q.q) && /2\.0 m/.test(q.q) &&
                         /It doubles/.test(q.opts.join('|'))), 'question');
  ck('lab: percent error divides by the ACCEPTED value',
     /accepted value goes on the bottom/.test(seed.l.blob), 'card');
  ck('lab: names ignoring air resistance as a simplification with a direction',
     /reads a little low/.test(seed.l.blob), 'card + question');
  ck('lab: the parentNote says the data does not exist yet rather than inventing it',
     /does not exist yet/.test(seed.l.note) && /Δx = v √\(2Δy \/ g\)/.test(seed.l.note),
     seed.l.note.slice(0, 80));

  const ord = seed.l.qs.find(q => q.kind === 'order');
  ck('lab: ships a kind:order ranking whose stored order really is longest-first',
     ord && ord.opts.length === 4 && ord.ans === 0 &&
     /4\.0 m\/s from 1\.25 m/.test(ord.opts[0]) && /8\.0 m\/s from 0\.20 m/.test(ord.opts[3]),
     ord && ord.opts);

  /* The head-to-tail graph must actually DRAW. renderGraph emits a
     <polyline>, never a <path> (the only paths are the axis arrowheads) —
     so count vertices and their extent, per the v185 probe lesson. */
  const gq = seed.r.qs.find(q => q.graph);
  const graph = await p.evaluate((g) => {
    const n = graphNode(g); document.body.appendChild(n);
    const pl = [...n.querySelectorAll('polyline')];
    const ys = pl.map(l => l.getAttribute('points').split(' ')
                            .map(pt => parseFloat(pt.split(',')[1])));
    const out = {lines: pl.length,
                 verts: ys.map(a => a.length),
                 extent: ys.map(a => Math.max(...a) - Math.min(...a))};
    n.remove(); return out;
  }, gq && gq.graph);
  ck('the head-to-tail question’s graph draws two real polylines with height',
     graph.lines === 2 && graph.verts.every(v => v >= 2) &&
     graph.extent.every(e => e > 10), graph);
  ck('the graph question says "the graph shown" and carries one',
     gq && /graph shown/.test(gq.q), gq && gq.q.slice(0,50));

  // Both units play end to end, with the physics Sheet reachable inside.
  for (const [nm, uid, want] of [['review','unit-phys-k2-sgq1',10],
                                 ['lab','unit-phys-k2-lab',9]]) {
    const play = await p.evaluate(async (uid) => {
      quizState = null;
      go('quiz', {unitId: uid, classId: 'physics'});
      const sheet = [...document.querySelectorAll('#screen .tool')].some(t=>/Sheet/.test(t.textContent));
      let guard = 0;
      while (view === 'quiz' && guard++ < 90) {
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
    }, uid);
    ck(nm + ': a full round plays and logs, with the Sheet tool reachable',
       play.logged && play.total === want && play.sheet, play);
  }

  // The prep treatment, and that the lab beside it does NOT get it.
  const gold = await p.evaluate(() => {
    go('shelf', {classId:'physics', series:'Kinematics 2', open:'unit-phys-k2-sgq1'});
    const stops = [...document.querySelectorAll('#screen .stop')];
    const prep = stops.filter(s => s.classList.contains('prep'));
    const pip = prep[0] && prep[0].querySelector('.pip');
    const oc = document.getElementById('shelfopen');
    const o = {prepStops: prep.length, pipGold: pip ? getComputedStyle(pip).borderColor : null,
               isPrepCard: oc ? oc.classList.contains('prepcard') : false,
               band: oc && oc.querySelector('.prepband') ? oc.querySelector('.prepband').textContent : null};
    ctx.open = 'unit-phys-k2-lab'; render();
    const lc = document.getElementById('shelfopen');
    o.labIsPrep = lc.classList.contains('prepcard');
    o.labBand = !!lc.querySelector('.prepband');
    o.labTitle = lc.querySelector('h3').textContent;
    return o;
  });
  ck('exactly one prep stop on the shelf, gold-ringed',
     gold.prepStops === 1 && /242, 202, 99/.test(gold.pipGold||''), gold);
  ck('the opened review wears the Test prep band',
     gold.isPrepCard && /Test prep/i.test(gold.band||''), gold);
  ck('the lab beside it gets no prep treatment',
     !gold.labIsPrep && !gold.labBand && /2-3 /.test(gold.labTitle||''), gold);

  const deck = await p.evaluate(async (uid) => {
    cardState = {}; go('cards', {unitId: uid, classId: 'physics'});
    let seen = 0;
    while (cardState.unitId === uid && seen++ < 40) {
      const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
      if (!knew) break;
      knew.click(); await new Promise(r=>setTimeout(r,5));
    }
    return {seen};
  }, 'unit-phys-k2-sgq1');
  ck('the review’s flashcard deck steps all the way through', deck.seen >= 16, deck);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
