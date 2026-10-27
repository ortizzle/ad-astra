/* Dynamics 1 · 1-6 Impulse and Momentum and 1-7 Conservation of Momentum
   (Ad Astra only), from chapter 9 of the textbook, the momentum homework and
   the spring-cart explosion lab.

   Seeds the four earlier Dynamics 1 parts alongside (and 1-5 Hooke's Law if
   it has shipped), so "shelves after 1-4" is a claim about coexistence. Every
   trap is pinned by its TEACHING, never by question id; every numeric answer
   that can be is re-derived here from the numbers in its own stem; counts are
   minimums, so a unit stays free to grow. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8421;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const IDS = {i:'unit-phys-dyn1-impulse', m:'unit-phys-dyn1-momentum'};
  const seed = await p.evaluate(async (IDS) => {
    const files = ['phys-dyn1-newton','phys-dyn1-weight','phys-dyn1-incline','phys-dyn1-circle',
                   'phys-dyn1-hooke','phys-dyn1-impulse','phys-dyn1-momentum'];
    const loaded = [];
    for (const f of files) {
      const r = await fetch('./content/'+f+'.json',{cache:'no-store'});
      if (!r.ok) continue;                       // 1-5 may not have shipped yet
      const j = await r.json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u; loaded.push(f);
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order, prep:u.prep,
              quarter:u.quarter, cards:u.cards, qs:u.questions, sorts:u.sorts||[],
              note:u.parentNote && u.parentNote.text, blob:JSON.stringify(u)}; };
    return {loaded, i: pick(IDS.i), m: pick(IDS.m), round: QUIZ_ROUND};
  }, IDS);
  const U = [seed.i, seed.m], L = ['1-6', '1-7'];

  ck('both load under the real physics classId (the v136 orphan trap)',
     U.every(u => u.classId === 'physics'), U.map(u=>u.classId));
  ck('both titles, exactly',
     seed.i.title === 'Dynamics 1 · 1-6 Impulse and Momentum' &&
     seed.m.title === 'Dynamics 1 · 1-7 Conservation of Momentum', U.map(u=>u.title));
  ck('both: libv 1+, quarter 2, no order bucket, no prep flag',
     U.every(u => u.libv >= 1 && u.quarter === 2 && u.order == null && !u.prep),
     U.map(u=>[u.libv,u.quarter,u.order,u.prep]));

  const shelf = await p.evaluate(() => {
    const s = shelvesFor('physics');
    const d = s.shelves.find(x=>x.name==='Dynamics 1');
    return {names: s.shelves.map(x=>x.name), loose: s.loose.map(u=>u.title),
            d1: d ? d.units.map(u=>lessonLabel(u)) : []};
  });
  const want = shelf.d1.some(t => /^1-5 /.test(t)) ? ['1-1','1-2','1-3','1-4','1-5','1-6','1-7']
                                                   : ['1-1','1-2','1-3','1-4','1-6','1-7'];
  ck('Dynamics 1 runs 1-1 … 1-4, (1-5), 1-6, 1-7 in order, nothing loose',
     shelf.d1.length === want.length && shelf.d1.every((t,i) => t.startsWith(want[i] + ' ')) &&
     shelf.loose.length === 0, shelf);

  ck('each unit: 14–20 cards and 18–22 questions',
     U.every(u => u.cards.length >= 14 && u.cards.length <= 20 && u.qs.length >= 18 && u.qs.length <= 22),
     U.map(u=>[u.cards.length,u.qs.length]));
  ck('every MC question has four unique options and an answer in range',
     U.every(u => u.qs.filter(q=>(q.kind||'mc')==='mc')
       .every(q => q.opts.length === 4 && new Set(q.opts).size === 4 && q.ans >= 0 && q.ans < 4)), 'ok');
  ck('both ask at all three levels', U.every(u => [1,2,3].every(l => u.qs.some(q=>q.lv===l))),
     U.map(u=>[1,2,3].map(l=>u.qs.filter(q=>q.lv===l).length)));
  for (let i = 0; i < 2; i++) {
    const slots = [0,1,2,3].map(s => U[i].qs.filter(q=>(q.kind||'mc')==='mc' && q.ans===s).length);
    ck(L[i] + ': answers sit in all four slots (_balance ran)', slots.every(n=>n>0), slots);
  }
  ck('every card def leads with a bold answer', U.every(u => u.cards.every(c => /^\*\*/.test(c.def))), 'ok');
  ck('every question carries 3–6 steps and a bold ex.main',
     U.every(u => u.qs.every(q => q.steps.length >= 3 && q.steps.length <= 6 && /^\*\*/.test(q.ex.main))), 'ok');

  const allQ = U.flatMap(u => u.qs);
  ck('no stem opens by back-referencing a neighbour',
     !allQ.some(q => /^(the|that) same\b/i.test(q.q.trim())), allQ.filter(q=>/^(the|that) same/i.test(q.q)).map(q=>q.q));
  ck('nothing refers to an option by position',
     !allQ.some(q => /\b(all|none|both) of the above\b|\b(first|second|third|fourth|last) (option|choice|answer)\b|\boptions? [a-d1-4]\b/i
                      .test([q.q, q.hint, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');
  ck('a stem that says "the graph shown" carries a graph',
     allQ.filter(q => /graph shown/.test(q.q)).every(q => q.graph), 'ok');
  /* A stem needs a positive direction when its answer is a signed number,
     or when things move both ways in it. */
  const needsSign = q => q.opts.some(o => /^[−+]/.test(o)) || (/\beast\b/.test(q.q) && /\bwest\b/i.test(q.q));
  ck('every stem that needs a sign names its positive direction',
     allQ.filter(needsSign).length >= 4 && allQ.filter(needsSign).every(q => /as positive/.test(q.q)),
     allQ.filter(q => needsSign(q) && !/as positive/.test(q.q)).map(q=>q.q.slice(0,60)));

  // Fresh numbers: none of the textbook's or the homework's own figures.
  const stems = allQ.map(q => [q.q].concat(q.opts).join(' ')).join(' ');
  const BOOK = /(?<![\d.])(2200 kg|725 kg|0\.144 kg|240(\.0)? kg|0\.060 kg|2275 kg|875 kg|0\.105 kg|0\.355 kg|84 kg|875 m\/s|4\.00 kg|625 m\/s|225 kg|0\.115 kg|845 kg|2575 kg|0\.265 kg|92 kg|1\.4 N·s|38(\.0)? m\/s|0\.150 kg)/;
  ck('none of the textbook’s worked-example or practice numbers is reused', !BOOK.test(stems), (stems.match(BOOK)||[])[0]);
  const HW = [['2.0','5.0'],['3.0','4.0'],['2.0','6.0'],['1.0','8.0'],['0.20','15'],['0.50','10'],
              ['1.5','4.0'],['4.0','3.0'],['3.0','10'],['0.10','20'],['1.0','6.0'],['2.0','4.0'],
              ['0.40','5.0'],['2.0','3.0'],['0.20','10'],['0.50','8.0'],['60','10']];
  const esc = s => s.replace('.', '\\.');
  const hwHit = allQ.flatMap(q => (q.kind === 'order' ? [q.q].concat(q.opts) : [[q.q].concat(q.opts).join(' ')])
      .flatMap(t => t.split(/(?<=[.?;:])\s/))
      .filter(sn => HW.some(([m,v]) => new RegExp(`(?<![\\d.])${esc(m)} kg\\b[^.?;]*?(?<![\\d.])${esc(v)} m/s`).test(sn))));
  ck('none of the homework’s (mass, speed) pairings is reused', hwHit.length === 0, hwHit);

  // ---- every numeric answer re-derived from its own stem -------------------
  const num = s => s.replace(/(\d) (\d{3})\b/g, '$1$2').match(/\d+(\.\d+)?/g).map(Number);
  const val = o => parseFloat(o.replace('−','-').replace('+',''));
  const area = g => { const P = g.series[0].pts; let a = 0;
    for (let k = 1; k < P.length; k++) a += (P[k][0]-P[k-1][0]) * (P[k][1]+P[k-1][1]) / 2; return a; };
  const close = (a, b, tol) => Math.abs(a - b) <= (tol || 0.051);
  const D = [
    [/0\.45 kg ball rolls west/,      (n,q) => val(q.opts[q.ans]) === -Math.round(n[0]*n[1]*10)/10],
    [/1600 kg car rolls/,             (n,q) => close(val(q.opts[q.ans]), n[0]*n[1]/n[2])],
    [/average force of 48 N/,         (n,q) => close(val(q.opts[q.ans]), n[0]*n[1])],
    [/0\.36 kg ball at rest is kicked/,(n,q) => close(val(q.opts[q.ans]), n[1]/n[0]) && /east/.test(q.opts[q.ans])],
    [/0\.14 kg ball moving at 25/,    (n,q) => close(val(q.opts[q.ans]), n[0]*n[1]/n[2])],
    [/0\.40 kg ball moving east/,     (n,q) => close(val(q.opts[q.ans]), n[0]*(-n[2]-n[1]))],
    [/rises from 0 to 900 N/,         (n,q) => close(val(q.opts[q.ans]), area(q.graph)/1000) && close(area(q.graph), n[1]*n[4]/2)],
    [/\+6 N for the first 2 s/,       (n,q) => close(val(q.opts[q.ans]), area(q.graph)) && close(area(q.graph), n[0]*n[1]-n[2]*n[3])],
    [/2\.5 kg cart moves east/,       (n,q) => { const v = (n[0]*n[1] - n[2]*n[3]) / n[0];
                                        return close(Math.abs(v), val(q.opts[q.ans])) && (v < 0) === /west/.test(q.opts[q.ans]); }],
    [/change a barge’s momentum/,     (n,q) => close(val(q.opts[q.ans]), n[0]/n[1])],
    [/1\.2 kg cart moving east at 5\.0/,(n,q) => close(val(q.opts[q.ans]), n[0]*n[1]/(n[0]+n[2]))],
    [/0\.90 kg cart moving east/,     (n,q) => { const v = (n[0]*n[1] - n[2]*n[3])/(n[0]+n[2]);
                                        return close(val(q.opts[q.ans]), Math.abs(v)) && /east/.test(q.opts[q.ans]) === v > 0; }],
    [/2\.4 kg cart moving east at 4\.0/,(n,q) => close(val(q.opts[q.ans]), (n[0]*n[1] - n[3]*n[4])/n[2])],
    [/48 kg skater/,                  (n,q) => close(val(q.opts[q.ans]), n[1]*n[2]/n[0]) && /west/.test(q.opts[q.ans])],
    [/1\.5 kg object at rest bursts/, (n,q) => close(val(q.opts[q.ans]), n[1]*n[2]/n[3]) && /west/.test(q.opts[q.ans])],
    [/3\.0 kg object moving east/,    (n,q) => { const v = (n[0]*n[1] - n[2]*n[3])/(n[0]-n[2]);
                                        return close(val(q.opts[q.ans]), Math.abs(v)) && /west/.test(q.opts[q.ans]) === v < 0; }],
    [/0\.80 kg cart moving at 6\.0/,  (n,q) => { const vf = n[0]*n[1]/(n[0]+n[2]);
                                        return close(val(q.opts[q.ans]), n[0]*n[1]**2/2 - (n[0]+n[2])*vf**2/2); }],
    [/0\.75 kg cart and a 0\.50 kg/,  (n,q) => close(val(q.opts[q.ans]), n[3]*n[0]/n[1])],
    [/1\.2 kg puck slides east/,      (n,q) => close(val(q.opts[q.ans]), Math.hypot(n[0]*n[1], n[2]*n[3])/(n[0]+n[2]))],
    [/one moves at\s+0\.80 m\/s/i,     (n,q) => close(val(q.opts[q.ans]), 0.80)],
  ];
  const der = D.map(([re, f]) => { const q = allQ.find(x => re.test(x.q)); return {re: String(re), found: !!q, ok: !!q && f(num(q.q), q)}; });
  ck(`every numeric answer re-derived from its stem (${D.length} questions)`, der.every(d => d.found && d.ok),
     der.filter(d => !d.ok));
  // Distractors are never quietly also correct.
  ck('no numeric distractor equals the answer',
     allQ.filter(q => (q.kind||'mc')==='mc' && /^[−+]?\d/.test(q.opts[q.ans]))
         .every(q => q.opts.every((o,i) => i === q.ans || !/^[−+]?\d/.test(o) || val(o) !== val(q.opts[q.ans]) || o.replace(/[\d.−+ ]/g,'') !== q.opts[q.ans].replace(/[\d.−+ ]/g,''))), 'ok');

  // Order questions: stored in order, and the order recomputes.
  const ordI = seed.i.qs.filter(q => q.kind === 'order'), ordM = seed.m.qs.filter(q => q.kind === 'order');
  ck('each unit carries an order question: four items, ans 0',
     ordI.length >= 1 && ordM.length >= 1 && ordI.concat(ordM).every(q => q.opts.length === 4 && q.ans === 0),
     [ordI.length, ordM.length]);
  const dpOf = o => { const n = num(o); if (/bounces back/.test(o)) return n[0]*(n[1]+n[2]);
                      if (/speeds up/.test(o)) return n[0]*(n[2]-n[1]); return n[0]*n[1]; };
  const dpv = ordI[0].opts.map(dpOf);
  ck('1-6 order (change in momentum) recomputes as strictly descending, a bounce first',
     dpv.every((v,i) => i === 0 || v < dpv[i-1]) && /bounces back at 2\.4/.test(ordI[0].opts[0]), dpv);
  const vfOf = o => { const n = num(o); return /coming toward it/.test(o) ? (n[0]*n[1]-n[2]*n[3])/(n[0]+n[2]) : n[0]*n[1]/(n[0]+n[2]); };
  const vfv = ordM[0].opts.map(vfOf);
  ck('1-7 order (stuck-together speed) recomputes as strictly descending, the head-on one third',
     vfv.every((v,i) => i === 0 || v < vfv[i-1]) && /coming toward it/.test(ordM[0].opts[2]), vfv);

  // ---- the named traps, each pinned by its teaching ------------------------
  const I = seed.i.blob, M = seed.m.blob;
  const qWith = (u, stem, right, wrong) => u.qs.some(q => stem.test(q.q) && right.test(q.opts[q.ans]) &&
                                          (!wrong || q.opts.some((o,i) => i !== q.ans && wrong.test(o))));
  ck('trap · a bounce changes momentum more than a stop (subtracted speeds offered as wrong)',
     /A bounce changes momentum more than a stop/.test(I) &&
     qWith(seed.i, /bounces back west at 5\.0/, /^−5\.0/, /^−1\.0/) &&
     qWith(seed.i, /leaves moving\s+up at 6/, /twice/, /It is zero/) &&
     qWith(seed.i, /clay and sticks/, /rubber ball/, /Neither/), 'card + three questions');
  ck('trap · momentum has a direction: dropped sign and "south is less" offered as wrong',
     qWith(seed.i, /0\.45 kg ball rolls west/, /^−6\.3/, /^\+6\.3/) &&
     qWith(seed.i, /north at 20 m\/s/, /opposite directions/, /less momentum/), 'q');
  ck('trap · an impulse is not a force: forgetting to divide by the time is offered',
     qWith(seed.i, /brought to rest in\s+0\.010 s/, /^350 N$/, /^3\.5 N$/), 'q');
  ck('trap · the air bag changes the TIME, not the change in momentum',
     /The air bag changes t, not Δp/.test(I) &&
     qWith(seed.i, /air bag reduce injuries/, /stop take longer/, /change in momentum smaller/) &&
     qWith(seed.i, /crash pad/, /^Same impulse; the pad’s average force is 12\.5 times smaller/, /times larger/), 'card + two questions');
  ck('trap · force–time graph: milliseconds converted, triangle halved, below-axis subtracted',
     qWith(seed.i, /rises from 0 to 900 N/, /^2\.7 N·s$/, /^2700 N·s$/) &&
     qWith(seed.i, /rises from 0 to 900 N/, /^2\.7/, /^5\.4 N·s$/) &&
     qWith(seed.i, /−4 N for the next/, /^8 N·s$/, /^16 N·s$/) &&
     /Area below the axis counts as negative/.test(I), 'two graph questions + card');
  ck('trap · momentum is not kinetic energy (mv² offered as wrong; doubling speed)',
     /Momentum is not kinetic energy/.test(I) &&
     qWith(seed.i, /0\.45 kg ball/, /^−6\.3/, /^−88/) &&
     qWith(seed.i, /Doubling a car’s speed/, /four times/, /doubles too/), 'card + two qs');
  ck('trap · starting momentum counts: "as if from rest" offered as wrong',
     qWith(seed.i, /5\.0 N force pointing WEST/, /^1\.0 m\/s west$/, /^4\.0 m\/s west$/), 'q');
  ck('trap · conservation is about the TOTAL, not each object',
     qWith(seed.m, /law of conservation of momentum say/, /total momentum stays the same/, /each object keeps/), 'q');
  ck('trap · sticky collisions: both masses, and kinetic energy NOT conserved (0 J offered)',
     qWith(seed.m, /1\.8 kg cart at rest/, /^2\.0 m\/s east$/, /^3\.3 m\/s east$/) &&
     qWith(seed.m, /How much kinetic energy is lost/, /^9\.6 J$/, /^0 J$/) &&
     /Momentum: always\. Kinetic energy: only if nothing dents\./.test(M), 'two qs + card hint');
  ck('trap · head-on collisions subtract (the dropped sign offered as wrong)',
     qWith(seed.m, /meets\s+a 1\.5 kg cart moving west/, /^1\.0 m\/s east$/, /^3\.5 m\/s east$/), 'q');
  ck('trap · recoil gives equal MOMENTA, never equal speeds; inverted ratio offered',
     qWith(seed.m, /48 kg skater/, /^0\.60 m\/s west$/, /^12 m\/s west$/) &&
     qWith(seed.m, /0\.90 kg\s+piece/, /^6\.0 m\/s west$/, /^13\.5 m\/s west$/) &&
     qWith(seed.m, /36 kg skater and a 54 kg/, /1\.5 times as fast/, /equal speeds/), 'three qs');
  ck('trap · a moving object that explodes does not start from zero',
     qWith(seed.m, /3\.0 kg object moving east/, /^1\.5 m\/s west$/, /^4\.5 m\/s west$/), 'q');
  ck('trap · equal momenta, different masses: the lighter carries more kinetic energy',
     /KE = p² \/ 2m/.test(M) && qWith(seed.m, /three times the mass/, /one-third/, /three times the kinetic/), 'card + q');
  ck('trap · short collisions: external impulse is negligible, not absent',
     qWith(seed.m, /dry road/, /so brief/, /stops acting/) && /Short collisions/.test(M), 'card + q');
  ck('trap · rockets push on their own exhaust, not on space',
     qWith(seed.m, /deep space/, /carries momentum backward/, /empty space/), 'q');
  ck('trap · two dimensions: momenta at right angles are not added in a line',
     qWith(seed.m, /north at 5\.0 m\/s/, /^3\.6 m\/s$/, /^5\.0 m\/s$/), 'q');
  ck('lab · the mass ratio equals the distance ratio because total momentum is zero and the times are equal',
     /m₁ \/ m₂ = Δx₂ \/ Δx₁/.test(M) &&
     qWith(seed.m, /Why\s+should m₁ ÷ m₂ equal Δx₂ ÷ Δx₁/, /Total momentum stays zero/, /Kinetic energy is conserved/) &&
     qWith(seed.m, /0\.75 kg cart and a 0\.50 kg/, /^0\.60 m$/, /^0\.27 m$/), 'card + two qs');
  ck('lab · the spring is internal',
     qWith(seed.m, /spring NOT counted as an\s+external/, /part of the cart system/, /only one of the carts/), 'q');
  ck('lab · kinetic energy was NOT conserved, and kinetic energies cannot cancel',
     /Kinetic energy in the explosion/.test(M) &&
     qWith(seed.m, /Is kinetic energy\s+conserved too/, /^No: it was zero before/, /total is still zero/), 'card + q');
  ck('lab cards and questions are flagged as study suggestions (from:added)',
     seed.m.cards.filter(c => /explosion lab|times have to be equal|spring is an internal|in the explosion/.test(c.term)).every(c => c.from === 'added') &&
     seed.m.qs.filter(q => /spring-cart/.test(q.q)).every(q => q.from === 'added'), 'flags');

  // Her sheet's notation, and what the parent note says.
  ck('her sheet’s notation is used (J = Ft = Δp, p = mv, m₂Δv₂ = −m₁Δv₁, the i/f conservation form)',
     /J = Ft = Δp/.test(I) && /p = mv/.test(I) && /m₂Δv₂ = −m₁Δv₁/.test(M) &&
     /m₁v₁_i \+ m₂v₂_i = m₁v₁_f \+ m₂v₂_f/.test(M), 'notation');
  ck('parent notes: homework and lab read for what they ask; no lab data, taught as reasoning',
     /read for what they ask/.test(seed.i.note) && /read for what they\s+ask/.test(seed.m.note) &&
     /no data yet/.test(seed.m.note) && /reasoning/.test(seed.m.note), 'notes');
  ck('parent note flags the sources’ sloppy spots (unlabelled Δp = −Δp, two items with no right choice, KE that grows)',
     /Δp = −Δp/.test(seed.m.note) && /item 32/.test(seed.m.note) && /33/.test(seed.m.note) &&
     /MORE kinetic energy/.test(seed.m.note), 'note');

  // Sort set: never names its own bucket; a clean pass logs.
  const s = seed.m.sorts[0];
  ck('1-7 ships a 12-item elastic/inelastic sort, both buckets used, every item says why',
     s && s.items.length >= 10 && s.items.filter(i=>i.k==='a').length >= 4 && s.items.filter(i=>i.k==='b').length >= 4 &&
     s.items.every(it => it.why), s && s.title);
  ck('no sort item contains either bucket’s label word',
     s.items.every(it => ![s.a, s.b].some(lab => it.t.toLowerCase().includes(lab.toLowerCase().split(/\s+/)[0]))), 'ok');
  const fin = await p.evaluate(async ({id, set}) => {
    const u = DATA.records[id], s = u.sorts.find(x=>x.id===set);
    sortState = null; go('sort', {unitId:id, classId:'physics', sortId:set});
    let guard = 0;
    while (sortState.queue.length && guard++ < 60) {
      const it = s.items[sortState.queue[0]];
      const btns = [...document.querySelectorAll('#screen .sortbtns .btn')];
      if (!btns.length) { await new Promise(r=>setTimeout(r,50)); continue; }
      (it.k==='a' ? btns[0] : btns[1]).click();
      await new Promise(r=>setTimeout(r,470));
    }
    const l = all('log').find(x => x.mode==='sort' && x.sortId===set);
    return {left: sortState.queue.length, n: s.items.length, correct: l && l.correct, xp: l && l.xp};
  }, {id: seed.m.id, set: s.id});
  ck('sort: a clean pass sorts every card and logs n right at 3 XP each',
     fin.left === 0 && fin.correct === fin.n && fin.xp === fin.n * 3, fin);

  // A full quiz round on each, with the physics Sheet reachable.
  for (let i = 0; i < 2; i++) {
    const play = await p.evaluate(async (uid) => {
      quizState = null;
      go('quiz', {unitId: uid, classId: 'physics'});
      const sheet = [...document.querySelectorAll('#screen .tool')].some(t=>/Sheet/.test(t.textContent));
      let guard = 0, graphs = 0;
      while (view === 'quiz' && guard++ < 80) {
        if (document.querySelector('#screen .graph-wrap')) graphs++;
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
    }, U[i].id);
    ck(L[i] + ': a full round plays and logs, with the Sheet tool reachable',
       play.logged && play.total === Math.min(seed.round, U[i].qs.length) && play.sheet, play);
  }
  // The graph questions render a real polyline.
  const gr = await p.evaluate((uid) => {
    const u = DATA.records[uid];
    return u.questions.filter(q => q.graph).map(q => { const n = graphNode(q.graph);
      return n ? n.querySelectorAll('polyline').length : 0; });
  }, seed.i.id);
  ck('1-6: every graph question renders a drawn force–time curve', gr.length >= 2 && gr.every(n => n >= 1), gr);

  // Each deck walks to the end.
  for (let i = 0; i < 2; i++) {
    const deck = await p.evaluate(async (uid) => {
      cardState = {}; go('cards', {unitId: uid, classId: 'physics'});
      let seen = 0;
      while (cardState.unitId === uid && seen++ < 40) {
        const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
        if (!knew) break;
        knew.click(); await new Promise(r=>setTimeout(r,5));
      }
      return {seen};
    }, U[i].id);
    ck(L[i] + ': the flashcard deck steps all the way through', deck.seen >= U[i].cards.length, deck);
  }

  // Public repo: no marks or scores of hers anywhere.
  ck('privacy: no score, mark or "she got" anywhere in the shipped records',
     !U.some(u => /she got|\bscored\b|\bout of \d+\b|\d+\s*\/\s*\d+\s*(correct|right|marks|points)|\b\d+(\.\d+)?\s?%/i.test(u.blob)), 'ok');

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,400))));
  console.log(`${out.filter(r=>r.ok).length}/${out.length}`, out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES', '· seeded:', seed.loaded.join(', '));
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
