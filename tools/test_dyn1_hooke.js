/* Dynamics 1 · 1-5 Hooke's Law and the Spring Lab, and the N1L assignment's
   additions to 1-3 (Ad Astra only).

   1-5 is built from the class's Hooke's Law Lab sheet, which has no data yet,
   so it teaches the reasoning and the lab's own questions with fresh numbers.
   1-3 gained an angled pull on a level floor (angle from the horizontal AND
   from the vertical) and two forces that are not at right angles, from the
   "Forces in N1L and N3L" assignment — appended, so every older id keeps its
   meaning, which this test pins against the shipped fingerprints.

   Every numeric answer is RE-DERIVED here from the numbers in its own stem,
   independently of the builder. Traps are pinned by their teaching, never by
   question id; counts are minimums. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8422;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    const files = ['phys-dyn1-newton','phys-dyn1-weight','phys-dyn1-incline','phys-dyn1-circle',
                   'phys-dyn1-hooke'];
    // Later parts may be built in parallel; seed them if they exist so the
    // shelf-order check is a claim about coexistence.
    const maybe = ['phys-dyn1-impulse','phys-dyn1-momentum'];
    for (const f of files.concat(maybe)) {
      const r = await fetch('./content/'+f+'.json',{cache:'no-store'});
      if (!r.ok) { if (files.includes(f)) throw new Error('missing '+f); continue; }
      const j = await r.json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u;
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order, prep:u.prep,
              quarter:u.quarter, status:u.status, cards:u.cards, qs:u.questions, sorts:u.sorts||[],
              note:u.parentNote && u.parentNote.text, blob:JSON.stringify(u)}; };
    return {h: pick('unit-phys-dyn1-hooke'), c: pick('unit-phys-dyn1-incline'), round: QUIZ_ROUND};
  });
  const H = seed.h, I = seed.c;

  // ---- identity and shelf ---------------------------------------------------
  ck('1-5 loads under the real physics classId (v136 orphan trap)', H.classId === 'physics', H.classId);
  ck('1-5 title is numbered and uses the shelf’s curly apostrophe',
     H.title === 'Dynamics 1 · 1-5 Hooke’s Law and the Spring Lab', H.title);
  ck('1-5: libv, quarter 2, no order bucket, no prep flag',
     H.libv >= 1 && H.quarter === 2 && H.order == null && !H.prep, [H.libv, H.quarter, H.order, H.prep]);
  const shelf = await p.evaluate(() => {
    const s = shelvesFor('physics');
    const d = s.shelves.find(x=>x.name==='Dynamics 1');
    return {names: s.shelves.map(x=>x.name), loose: s.loose.map(u=>u.title),
            d1: d ? d.units.map(u=>lessonLabel(u)) : []};
  });
  const L = ['1-1','1-2','1-3','1-4','1-5'];
  ck('Dynamics 1 runs 1-1 → 1-5 in order (later parts tolerated after), nothing loose',
     shelf.d1.length >= 5 && L.every((l,i) => shelf.d1[i].startsWith(l + ' ')) &&
     shelf.d1.slice(5).every(t => /^1-[6-9] /.test(t)) && shelf.loose.length === 0, shelf);

  // ---- structure -------------------------------------------------------------
  ck('1-5: 14–18 cards and 16–20 questions', H.cards.length >= 14 && H.cards.length <= 18 &&
     H.qs.length >= 16 && H.qs.length <= 20, [H.cards.length, H.qs.length]);
  ck('1-5 asks at all three levels', [1,2,3].every(l => H.qs.some(q=>q.lv===l)),
     [1,2,3].map(l=>H.qs.filter(q=>q.lv===l).length));
  for (const U of [H, I]) {
    const mc = U.qs.filter(q=>(q.kind||'mc')==='mc');
    const slots = [0,1,2,3].map(s => mc.filter(q=>q.ans===s).length);
    ck(U.id + ': answers spread across all four slots', slots.every(n=>n>0), slots);
    ck(U.id + ': every MC question has four unique options, answer in range',
       mc.every(q => q.opts.length === 4 && new Set(q.opts).size === 4 && q.ans >= 0 && q.ans < 4), 'ok');
    const BACK = /^\s*(the same|that same|for (that|the) same|from the same|using the same|in the same|with the same)\b/i;
    ck(U.id + ': no stem back-references a neighbour, and "that same" appears nowhere',
       !U.qs.some(q => BACK.test(q.q) ||
         /that same/i.test([q.q, q.hint, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');
    ck(U.id + ': nothing refers to an option by position',
       !U.qs.some(q => /\b(all|none|both) of the above\b|\b(first|second|third|fourth|last) (option|choice|answer)\b|\boptions? [a-d1-4]\b/i
         .test([q.q, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');
  }
  ck('1-5: every card leads bold; every question has 3–6 steps and a bold ex.main',
     H.cards.every(c => /^\*\*/.test(c.def)) &&
     H.qs.every(q => q.steps.length >= 3 && q.steps.length <= 6 && /^\*\*/.test(q.ex.main)), 'ok');
  ck('1-5: "the graph shown" only ever appears with a graph attached',
     H.qs.every(q => !/graph shown/i.test(q.q) || q.graph), 'ok');
  ck('1-5: none of the sources’ own numbers in a graded stem or option (10 in, 30 cm, 200 N/m, 0.15 m, 0.10 m, 250 N/m, 0.12 m)',
     !H.qs.some(q => /(?<![\d.])(10 in\b|10 inch|30 cm|200 N\/m|0\.15 m\b|0\.10 m\b|250 N\/m|0\.12 m\b)/
       .test([q.q].concat(q.opts).join(' '))), 'fresh');
  const newI = I.qs.slice(16);
  ck('1-3 additions: none of the assignment’s own numbers (7900 N, 1100 kg, 15 kg, 53°, 35 N, 400 N, 200 N, 70 kg, 650 N, 10 N, 8 N)',
     !newI.some(q => /(?<![\d.])(7900 N|1100 kg|15 kg|53°|35 N\b|400 N|200 N|70 kg|650 N|10 N\b|8 N\b)/
       .test([q.q].concat(q.opts).join(' '))), newI.map(q=>q.q.slice(0,40)));

  // ---- every numeric answer re-derived from its stem -------------------------
  const g = 9.8;
  const num = s => parseFloat(String(s).replace('−','-').replace(/,/g,''));
  const rad = d => d * Math.PI / 180;
  const n = (re, s) => { const m = s.match(re); return m ? num(m[1]) : NaN; };
  const SOLVERS = [
    // 1-5
    {re:/(\d+) g mass hangs from a spring\. What force/, f:(s)=>n(/(\d+) g mass/,s)/1000*g},
    {re:/is ([\d.]+) cm long with nothing on it/, f:(s)=>{
      const L0=n(/is ([\d.]+) cm long with nothing/,s), L1=n(/it is ([\d.]+) cm long\./,s), m=n(/With ([\d.]+) kg/,s);
      return m*g/((L1-L0)/100); }},
    {re:/g mass hanger carrying/, f:(s)=>{
      const h=n(/A (\d+) g mass hanger/,s), sl=n(/carrying (\d+) g/,s), x=n(/spring ([\d.]+) cm/,s);
      return (h+sl)/1000*g/(x/100); }},
    {re:/graph shown plots the force on a spring/, f:(s,q)=>q.graph.series[0].m},
    {re:/constant of ([\d.]+) N\/m\. How much force/, f:(s)=>n(/constant of ([\d.]+) N\/m/,s)*n(/stretched ([\d.]+) cm/,s)/100},
    {re:/inches\?/, f:(s)=>n(/constant of ([\d.]+) N\/m/,s)*n(/stretch it ([\d.]+) inches/,s)*0.0254/g},
    {re:/N weight stretches a spring ([\d.]+) cm\. Without/, f:(s)=>{
      const F1=n(/A ([\d.]+) N weight/,s), x1=n(/spring ([\d.]+) cm/,s), F2=n(/how far will a ([\d.]+) N/,s);
      return x1*F2/F1; }},
    {re:/On the Moon, where g is about/, f:(s)=>{
      const gm=n(/g is about ([\d.]+) m\/s²/,s), m=n(/a ([\d.]+) kg mass/,s), k=n(/constant of ([\d.]+) N\/m/,s);
      return m*gm/k*100; }},
    {re:/percent error as \|b\|/, f:(s)=>Math.abs(n(/of (−?[\d.]+) N, and/,s))/n(/y_max, is ([\d.]+) N/,s)*100},
    // 1-3 additions
    {re:/kg crate is pulled across a level floor by a rope angled/, f:(s)=>{
      const m=n(/A (\d+) kg crate/,s), th=n(/angled (\d+)° above/,s), T=n(/tension of (\d+) N/,s);
      return m*g - T*Math.sin(rad(th)); }},
    {re:/sled is pulled at constant velocity across level snow by a rope angled/, f:(s)=>{
      const m=n(/A (\d+) kg sled/,s), th=n(/angled (\d+)° above/,s), mu=n(/μ_k = ([\d.]+)/,s);
      return mu*m*g/(Math.cos(rad(th)) + mu*Math.sin(rad(th))); }},
    {re:/What is the horizontal part of the pull\?/, f:(s)=>n(/pulled with (\d+) N/,s)*Math.sin(rad(n(/at (\d+)° to the VERTICAL/,s)))},
    {re:/Kinetic friction on the box is/, f:(s)=>n(/box is (\d+) N/,s)/Math.sin(rad(n(/at (\d+)° to the VERTICAL/,s)))},
    {re:/What is the size of the resultant force on/, f:(s)=>{
      const a=n(/with (\d+) N and/,s), c=n(/and (\d+) N, with/,s), th=n(/with (\d+)° between/,s);
      return Math.sqrt(a*a + c*c + 2*a*c*Math.cos(rad(th))); }},
    {re:/What force does the ground exert on the post\?/, f:(s)=>{
      const a=n(/with (\d+) N and/,s), c=n(/and (\d+) N, with/,s), th=n(/with (\d+)° between/,s);
      return Math.sqrt(a*a + c*c + 2*a*c*Math.cos(rad(th))); },
     // The equilibrant's size is the resultant's; its DIRECTION is the answer.
     dir: o => /opposite the ropes/.test(o)},
  ];
  const agree = (got, want) => { const dec = (String(want).split('.')[1]||'').length;
    return Math.abs(got - want) <= 0.5 * Math.pow(10, -dec) + 1e-9; };
  const numericQs = U => U.qs.filter(q => (q.kind||'mc')==='mc' && /^−?[\d.]+(%| |$)/.test(q.opts[q.ans]));
  const solve = (U, label) => {
    const bad = [], unmatched = [];
    for (const q of numericQs(U)) {
      const sv = SOLVERS.filter(x => x.re.test(q.q));
      if (sv.length !== 1) { unmatched.push(q.q.slice(0,50)); continue; }
      const want = num(q.opts[q.ans]), got = sv[0].f(q.q, q);
      const dir = sv[0].dir || (() => true);
      if (!agree(got, want) || !dir(q.opts[q.ans])) bad.push([q.q.slice(0,40), got, want]);
      // and no distractor is also right at the shown precision (and direction)
      q.opts.forEach((o,i) => { if (i !== q.ans && /^−?[\d.]/.test(o) && agree(got, num(o)) && dir(o)) bad.push(['also right', o]); });
    }
    return {bad, unmatched};
  };
  {
    const r = solve(H);
    ck('1-5: every numeric answer re-derives from its own stem, and no distractor also does',
       !r.bad.length && !r.unmatched.length && numericQs(H).length >= 9, r);
    const newU = {qs: newI};
    const r2 = solve(newU);
    ck('1-3 additions: every numeric answer re-derives from its own stem',
       !r2.bad.length && !r2.unmatched.length && numericQs(newU).length >= 5, r2);
  }
  // The ranking: k = F / x for every option, strictly descending as stored.
  const ord = H.qs.filter(q => q.kind === 'order');
  const ks = ord.length ? ord[0].opts.map(o => { const m = o.match(/([\d.]+) N stretches it ([\d.]+) cm/);
                                                return m ? num(m[1]) / (num(m[2]) / 100) : NaN; }) : [];
  ck('1-5: one order question, stored stiffest-first with ans 0 (k re-derived from each option)',
     ord.length === 1 && ord[0].ans === 0 && ord[0].opts.length === 4 &&
     ks.every((k,i) => !isNaN(k) && (i === 0 || ks[i-1] > k)), ks);
  ck('1-5: the ranking’s biggest force is NOT the stiffest spring (the trap it exists for)',
     ord.length && (() => { const F = ord[0].opts.map(o => num(o.match(/([\d.]+) N/)[1]));
                            return F.indexOf(Math.max(...F)) !== 0; })(), 'ok');

  // ---- the named traps, by their teaching -------------------------------------
  const B = H.blob;
  const qWith = (U, stem, right, wrong) => U.qs.some(q => stem.test(q.q) && right.test(q.opts[q.ans]) &&
                                          (!wrong || q.opts.some((o,i) => i !== q.ans && wrong.test(o))));
  ck('trap · stretch, not length: card, and dividing by the whole length is a real wrong option',
     /x is the stretch — how much LONGER the spring got — not how long the/.test(B) &&
     qWith(H, /cm long with nothing on it/, /^21 N\/m$/, /^7\.7 N\/m$/), 'card + q');
  ck('trap · the hanger counts: card, a question with "forgot the hanger" as wrong, and the intercept it leaves',
     /That includes the mass hanger itself/.test(B) &&
     qWith(H, /mass hanger carrying/, /^24\.5 N\/m$/, /^18\.4 N\/m$/) &&
     qWith(H, /−0\.49 N/, /hanger out of every weight/, /cm instead of m/), 'card + two qs');
  ck('trap · grams or kilograms are not newtons (each offered as a wrong option)',
     qWith(H, /350 g mass/, /^3\.43 N$/, /^350 N$/) && qWith(H, /inches\?/, /^0\.65 kg$/, /^6\.4 kg$/), 'qs');
  ck('trap · inches to metres: the card gives 2.54 cm, and inches-as-metres is wrong',
     /1 in = 2\.54 cm = 0\.0254 m/.test(B) && qWith(H, /inches\?/, /^0\.65 kg$/, /^25\.7 kg$/), 'card + q');
  ck('trap · the Moon: slope unchanged because k belongs to the spring; "a sixth" is wrong',
     /Slope \(k\): unchanged/.test(B) &&
     qWith(H, /Moon.*slope of the line/s, /stays the same, because k belongs to the spring/, /sixth/) &&
     qWith(H, /Moon.*independent values/s, /^Both get smaller/, /masses are the same/), 'card + two qs');
  ck('trap · the Moon numeric: Earth’s g is offered as the wrong answer',
     qWith(H, /On the Moon, where g/, /^6\.0 cm$/, /^36\.8 cm$/), 'q');
  ck('trap · the minus sign means a restoring force, opposite the stretch — not a negative k',
     /points the opposite way to its\s+stretch or squash/.test(B.replace(/\\n/g,' ')) &&
     qWith(H, /minus sign tell you/, /opposite to its stretch/, /constant is negative/) &&
     qWith(H, /6 cm below/, /^Up, back toward/, /^Down/), 'card + two qs');
  ck('the axis choice is named: slope k with force vertical, 1/k the other way round',
     /the slope is\s+1\/k, in m\/N/.test(B.replace(/\\n/g,' ')), 'card');
  ck('the elastic limit is taught and flagged added',
     H.cards.some(c => /elastic limit/i.test(c.term) && c.from === 'added'), 'card');
  ck('her sheet’s percent error is shown and flagged as our reading of b and y_max',
     H.cards.some(c => /Percent error/.test(c.term) && c.from === 'added' && /\|b\| \/ y_max/.test(c.eq||'')), 'card');
  ck('the parent note: no data yet, PhET on her laptop, the 10 in and the axis/percent-error questions',
     /no data yet/.test(H.note) && /PhET/.test(H.note) && /laptop/.test(H.note) &&
     /10 inches/.test(H.note) && /axis/.test(H.note) && /y_max/.test(H.note), 'note');
  const ss = H.sorts;
  ck('1-5 sort: Moon set, both buckets used, k and the slope on the "same" side, no item names its bucket',
     ss.length === 1 && ss[0].items.filter(i=>i.k==='a').length >= 4 && ss[0].items.filter(i=>i.k==='b').length >= 4 &&
     ss[0].items.some(i => /spring constant/.test(i.t) && i.k === 'b') &&
     ss[0].items.some(i => /slope/.test(i.t) && i.k === 'b') &&
     ss[0].items.every(it => it.why && ![ss[0].a, ss[0].b].some(lab => { const w = lab.toLowerCase().split(/\s+/)[0];
       return w.length > 4 && it.t.toLowerCase().includes(w); })), ss.map(s=>s.title));

  // ---- 1-3: what was added, and what must not have moved ----------------------
  const HEAD13 = [["q0","What is the equilibrant of a s","The single force tha"],["q1","Two forces act on a ring: 30 N","50 N, 53.1° south of"],["q2","Drawn head to tail, the forces","form a closed loop, "],["q3","A 240 N sign hangs still from ","240 N"],["q4","A painting hangs from two wire","It increases, becaus"],["q5","A 400 N crate rests on a ramp ","169 N"],["q6","A 400 N crate rests on a ramp ","363 N"],["q7","A box slides down a frictionle","3.35 m/s²"],["q8","A heavy crate and a light box ","They are equal, beca"],["q9","A sled slides down a 35° snow ","4.82 m/s²"],["q10","A sled starts from rest and ac","14.5 m/s"],["q11","A box slides down a 16° ramp a","0.29"],["q12","A block rests on a board tilte","It stays put: tan 22"],["q13","A skier finishes a run and coa","Down the slope, oppo"],["q14","One box is placed on ramps of ","On level ground"],["q15","A car is stuck in mud. A rope ","The rope is nearly s"]];
  ck('1-3: every pre-existing question keeps its id, its stem and its answer',
     HEAD13.every(([id, st, an], i) => I.qs[i].id === id && I.qs[i].q.startsWith(st) && I.qs[i].opts[I.qs[i].ans].startsWith(an)),
     I.qs.slice(0,16).map(q=>q.id));
  ck('1-3: the first 15 cards are unchanged in order, new ones appended',
     I.cards.slice(0,15).map(c=>c.id).join() === Array.from({length:15},(_,i)=>'c'+i).join() &&
     /^Forces at an angle/.test(I.cards[0].term) && /^Which way friction points/.test(I.cards[14].term) &&
     I.cards.length >= 17, I.cards.map(c=>c.term).slice(14));
  ck('1-3: new question ids continue from q16', newI.length >= 4 && newI.every((q,i) => q.id === 'q' + (16 + i)), newI.map(q=>q.id));
  ck('1-3: libv bumped past 1', I.libv >= 2, I.libv);
  ck('1-3: the angled pull is taught — an upward pull shrinks the normal force, with the full weight as the wrong option',
     /A pull at an angle lifts as well as drags/.test(I.blob) &&
     qWith({qs:newI}, /rope angled \d+° above the horizontal, with a tension/, /^156 N$/, /^196 N$/) &&
     qWith({qs:newI}, /constant velocity across level snow/, /^58\.8 N$/, /^67\.0 N$/), 'card + qs');
  ck('1-3: an angle from the VERTICAL is a named trap (the cosine answer is offered as wrong)',
     /Read where the angle is measured from/.test(I.blob) &&
     qWith({qs:newI}, /40° to the VERTICAL/, /^38\.6 N$/, /^46\.0 N$/) &&
     qWith({qs:newI}, /60° to the VERTICAL/, /^27\.7 N$/, /^48\.0 N$/), 'card + qs');
  ck('1-3: two forces NOT at right angles add by components (90° and in-line answers offered as wrong), with the ground’s equilibrant',
     /Adding forces that are not at right angles/.test(I.blob) &&
     qWith({qs:newI}, /40° between the ropes\. What is the size/, /^426 N$/, /^335 N$/) &&
     qWith({qs:newI}, /What force does the ground exert/, /^426 N, opposite/, /^426 N, along/), 'card + qs');
  ck('1-3: the parent note names the additions and still says forces are described in words',
     /N1L assignment/.test(I.note) && /not at right angles/.test(I.note) && /described in words/.test(I.note), 'note');
  ck('1-3: still no graph anywhere (the no-faked-diagram rule)', !/"graph"/.test(I.blob), 'ok');

  // ---- graphs on 1-5 render as real lines --------------------------------------
  const gr = await p.evaluate((qs) => qs.filter(q=>q.graph).map(q => {
    const svg = renderGraph(q.graph); return svg ? svg.querySelectorAll('polyline').length : 0; }), H.qs);
  ck('1-5: every question graph renders its lines', gr.length >= 2 && gr.every(n => n >= 1), gr);

  // ---- a full round and the deck on 1-5; a round on 1-3 -----------------------
  for (const U of [H, I]) {
    const play = await p.evaluate(async (uid) => {
      quizState = null;
      go('quiz', {unitId: uid, classId: 'physics'});
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
      return {logged: !!l, total: l && l.total};
    }, U.id);
    ck(U.id + ': a full quiz round plays and logs', play.logged && play.total === Math.min(seed.round, U.qs.length), play);
  }
  const deck = await p.evaluate(async (uid) => {
    cardState = {}; go('cards', {unitId: uid, classId: 'physics'});
    let seen = 0;
    while (cardState.unitId === uid && seen++ < 40) {
      const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
      if (!knew) break;
      knew.click(); await new Promise(r=>setTimeout(r,5));
    }
    return {seen};
  }, H.id);
  ck('1-5: the flashcard deck steps all the way through', deck.seen >= H.cards.length, deck);
  const fin = await p.evaluate(async (id) => {
    const u = DATA.records[id], s = u.sorts[0];
    sortState = null; go('sort', {unitId:id, classId:'physics', sortId:s.id});
    let guard = 0;
    while (sortState.queue.length && guard++ < 60) {
      const it = s.items[sortState.queue[0]];
      const btns = [...document.querySelectorAll('#screen .sortbtns .btn')];
      if (!btns.length) { await new Promise(r=>setTimeout(r,50)); continue; }
      (it.k==='a' ? btns[0] : btns[1]).click();
      await new Promise(r=>setTimeout(r,470));
    }
    const l = all('log').find(x => x.mode==='sort' && x.sortId===s.id);
    return {left: sortState.queue.length, n: s.items.length, correct: l && l.correct, xp: l && l.xp};
  }, H.id);
  ck('1-5 sort: a clean pass sorts every card and logs n right at 3 XP each',
     fin.left === 0 && fin.correct === fin.n && fin.xp === fin.n * 3, fin);

  // Public repo: nobody named, no marks.
  ck('privacy: no score, mark or "she got" in either shipped record',
     ![H, I].some(u => /she got|\bscored\b|\d+\s*\/\s*\d+\s*(marks|points)|\bout of \d+\b/i.test(u.blob)), 'ok');

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,400))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
