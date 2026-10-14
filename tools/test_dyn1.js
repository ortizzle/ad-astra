/* Dynamics 1 (Ad Astra only): four numbered parts built from chapter 6
   (Forces) and chapter 7.1 + 7.3 (Forces and Motion in Two Dimensions).

   Chapter 7.2 — projectile motion — is deliberately NOT here: Kinematics 2 ·
   2-2 was built from that exact section in v181. The shelf checks seed both
   Kinematics shelves alongside, so "its own shelf" is a claim about
   coexistence. Every trap is pinned by its TEACHING, never by question id,
   which would not survive a renumber; counts are minimums (a unit must stay
   free to grow — the rot test_phases/test_k2/test_cells all paid for). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8412;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const IDS = {a:'unit-phys-dyn1-newton', b:'unit-phys-dyn1-weight',
               c:'unit-phys-dyn1-incline', d:'unit-phys-dyn1-circle'};
  const seed = await p.evaluate(async (IDS) => {
    const files = ['phys-ch3-describing-motion','phys-kinematics-equations',
                   'phys-kinematics-graphs','phys-ramp-lab',
                   'phys-k2-vectors','phys-k2-projectiles','phys-k2-lab','phys-k2-quiz1-review',
                   'phys-dyn1-newton','phys-dyn1-weight','phys-dyn1-incline','phys-dyn1-circle'];
    for (const f of files) {
      const j = await (await fetch('./content/'+f+'.json',{cache:'no-store'})).json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u;
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order, prep:u.prep,
              status:u.status, cards:u.cards, qs:u.questions, sorts:u.sorts||[],
              note:u.parentNote && u.parentNote.text, blob:JSON.stringify(u)}; };
    const r = {}; for (const k in IDS) r[k] = pick(IDS[k]);
    r.round = QUIZ_ROUND;
    return r;
  }, IDS);
  const U = [seed.a, seed.b, seed.c, seed.d];
  const L = ['1-1','1-2','1-3','1-4'];

  // v136's orphan trap: a classId CLASS_BY_ID doesn't know fails silently.
  ck('all four load under the real physics classId',
     U.every(u => u.classId === 'physics'), U.map(u=>u.classId));
  ck('all four carry libv, no order bucket and no prep flag (lessons, not test prep)',
     U.every(u => u.libv >= 1 && u.order == null && !u.prep),
     U.map(u=>[u.libv,u.order,u.prep]));
  ck('all four carry the NUMBERED form, so the shelf sorts structurally',
     U.every((u,i) => new RegExp('^Dynamics 1 · ' + L[i] + ' ').test(u.title)), U.map(u=>u.title));

  const shelf = await p.evaluate(() => {
    const s = shelvesFor('physics');
    const get = n => (s.shelves.find(x=>x.name===n)||{units:[]}).units.map(u=>lessonLabel(u));
    return {names: s.shelves.map(x=>x.name), loose: s.loose.map(u=>u.title),
            d1: get('Dynamics 1'), k1: get('Kinematics 1'), k2: get('Kinematics 2')};
  });
  ck('Dynamics 1 is its own shelf, 1-1 → 1-4 in teaching order, nothing loose',
     shelf.names.includes('Dynamics 1') && shelf.d1.length === 4 &&
     shelf.d1.every((t,i) => t.startsWith(L[i] + ' ')) && shelf.loose.length === 0, shelf);
  ck('Kinematics 1 still holds its four parts and Kinematics 2 its four, untouched',
     shelf.k1.length === 4 && shelf.k2.length === 4 &&
     /^2-1 /.test(shelf.k2[0]) && /^2-2 /.test(shelf.k2[1]) && /^2-3 /.test(shelf.k2[2]), shelf);

  // Structure, as minimums.
  ck('each unit: at least 14 cards and 16 questions',
     U.every(u => u.cards.length >= 14 && u.qs.length >= 16),
     U.map(u=>[u.cards.length,u.qs.length]));
  ck('every MC question has four unique options and an answer in range',
     U.every(u => u.qs.filter(q=>(q.kind||'mc')==='mc')
       .every(q => q.opts.length === 4 && new Set(q.opts).size === 4 && q.ans >= 0 && q.ans < 4)), 'ok');
  ck('every unit asks at all three levels', U.every(u => [1,2,3].every(l => u.qs.some(q=>q.lv===l))),
     U.map(u=>[1,2,3].map(l=>u.qs.filter(q=>q.lv===l).length)));
  for (let i = 0; i < 4; i++) {
    const slots = [0,1,2,3].map(s => U[i].qs.filter(q=>(q.kind||'mc')==='mc' && q.ans===s).length);
    ck(L[i] + ': answers spread across all four slots (the v181 _balance bug)', slots.every(n=>n>0), slots);
  }
  ck('every card def leads with a bold answer', U.every(u => u.cards.every(c => /^\*\*/.test(c.def))), 'ok');
  ck('every question carries 3-6 steps and a bold ex.main',
     U.every(u => u.qs.every(q => q.steps.length >= 3 && q.steps.length <= 6 && /^\*\*/.test(q.ex.main))), 'ok');

  // Standalone and positional rules.
  const allQ = U.flatMap(u => u.qs);
  const BACK = /^\s*(the same|that same|for (that|the) same|from the same|using the same|in the same|with the same)\b/i;
  ck('no stem opens by back-referencing a neighbour, and "that same" appears nowhere',
     !allQ.some(q => BACK.test(q.q) ||
       /that same/i.test([q.q, q.hint, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))),
     allQ.filter(q => BACK.test(q.q)).map(q=>q.q.slice(0,50)));
  ck('nothing refers to an option by position',
     !allQ.some(q => /\b(all|none) of the above\b|\b(first|second|third|last) (option|choice)\b|\boptions? [a-d1-4]\b/i
                      .test([q.q, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');

  // Scope: chapter 7.2 belongs to Kinematics 2 and is not re-asked here.
  ck('no Dynamics 1 card re-teaches projectile motion (Kinematics 2 · 2-2 owns 7.2)',
     !U.some(u => u.cards.some(c => /projectile|trajectory|(^|\s)range\b|hang time/i.test(c.term))),
     U.flatMap(u=>u.cards.map(c=>c.term)).filter(t=>/projectile|trajectory/i.test(t)));
  ck('the 1-3 parent note says 7.2 was left out on purpose and why',
     /projectile/i.test(seed.c.note) && /Kinematics 2/.test(seed.c.note), 'note');
  ck('no diagram is faked: nothing carries a graph, and every note says forces are described in words',
     !/"graph"/.test(U.map(u=>u.blob).join('')) && U.every(u => /described in words/.test(u.note)), 'ok');
  /* Anchored with a lookbehind: a bare \b75 kg matched the fresh 0.75 kg
     and \b25 kg the fresh 0.25 kg ball — the v195 "sweep for the sheet's
     pairings, never loose numbers" lesson, met again on the first run. */
  ck('none of the textbook’s own worked-example numbers is reused',
     !U.some(u => /(?<![\d.])(168 N|562 N|62 kg|75 kg|0\.18 kg|13 g\b|0\.93 m|8\.8 m\/s|32 m\/s|25 kg|585 N|650 N|22\.5°|4\.47 m\/s)/
       .test(u.qs.map(q=>[q.q].concat(q.opts).join(' ')).join(' '))), 'fresh numbers');

  // ---- the named traps, each pinned by its teaching ------------------------
  const A = seed.a.blob, B = seed.b.blob, Cc = seed.c.blob, D = seed.d.blob;
  const qWith = (u, stem, right, wrong) => u.qs.some(q => stem.test(q.q) && right.test(q.opts[q.ans]) &&
                                          (!wrong || q.opts.some((o,i) => i !== q.ans && wrong.test(o))));
  // Mass vs weight.
  ck('trap · mass vs weight: mass is unchanged on the Moon, and the kg-for-N swap is a real wrong option',
     /Mass is the amount of matter.+same everywhere/.test(B) &&
     qWith(seed.b, /mass on the Moon/, /^54 kg$/, /^9\.0 kg$/) &&
     qWith(seed.b, /weight on the Moon/, /^86 N$/, /^54 N$/), 'cards + Moon questions');
  ck('trap · mass vs weight: a sort set drills it, with both buckets used',
     seed.b.sorts.some(s => s.a === 'Mass' && s.b === 'Weight' &&
       s.items.filter(i=>i.k==='a').length >= 4 && s.items.filter(i=>i.k==='b').length >= 4), 'sort');
  // Newton's first law.
  ck('trap · moving does not need a net force: card, and "the pull must win" offered as wrong',
     /A force is needed to CHANGE motion, not to keep it going/.test(A) &&
     qWith(seed.a, /constant 1\.5 m\/s/, /at constant speed the forces balance/, /pull must win/) &&
     qWith(seed.a, /puck/, /^None/, /inertia/), 'card + two questions');
  // Third-law pairs.
  ck('trap · a third-law pair acts on DIFFERENT objects, so it never cancels',
     /act on different objects, so they\s+can never cancel/.test(A.replace(/\\n/g,' ')) &&
     qWith(seed.a, /third-law pair/, /both act on the book/, /equal in size and opposite/) &&
     qWith(seed.a, /horse/, /forces ON the cart/, /cancel/), 'card + book + horse');
  // Normal force is not the weight.
  ck('trap · normal force ≠ weight with an extra push (weight alone is the wrong option)',
     /Normal force with an extra push/.test(B) &&
     qWith(seed.b, /press straight down/, /^147\.6 N$/, /^117\.6 N$/), '1-2');
  ck('trap · normal force ≠ weight on a slope: F_g cos θ, with the full weight offered as wrong',
     /The normal force on a slope is LESS than the weight/.test(Cc) &&
     qWith(seed.c, /normal\s+force from the ramp/, /^363 N$/, /^400 N$/), '1-3');
  ck('trap · on a slope friction uses the NORMAL force, not the weight',
     /friction uses the normal force, F_g cos θ — never the full weight/i.test(Cc) &&
     qWith(seed.c, /35° snow slope/, /^4\.82/, /^5\.06/), '1-3');
  // Net force, not a single force.
  ck('trap · the NET force sets the acceleration; one force on its own is a real wrong option',
     /It is the NET force that goes in, never just one of the forces/.test(A) &&
     qWith(seed.a, /1350 kg car/, /^2\.0 m\/s²$/, /^2\.7 m\/s²$/) &&
     qWith(seed.b, /pushed horizontally with\s+150 N/, /^2\.24/, /^4\.69/), '1-1 + 1-2');
  // Others the chapter names.
  ck('static friction is an up-to force: the ≤ read as = is offered as wrong',
     qWith(seed.b, /does not move\. What is the static/, /^60 N$/, /^79\.4 N$/), 'q');
  ck('apparent weight follows the acceleration, not the direction of travel',
     /It is the acceleration, not the direction of travel/.test(B) &&
     qWith(seed.b, /moving DOWN at a\s+constant/, /true weight/, /going down/), 'card + q');
  ck('tug-of-war tension is the pull at one end, not both added',
     qWith(seed.a, /tug-of-war/, /^450 N$/, /^900 N$/), 'q');
  ck('constant velocity on a slope does NOT mean no friction',
     qWith(seed.c, /16° ramp at a constant velocity/, /^0\.29$/, /^Zero/), 'q');
  ck('there is no centrifugal force; a released object goes along the tangent',
     /There is no centrifugal force/.test(D) &&
     qWith(seed.d, /suddenly\s+released/, /tangent/, /outward/) &&
     qWith(seed.d, /turns sharply to the left/, /keep moving straight/, /centrifugal/), 'card + two qs');
  ck('her sheet’s notation and g convention are used (F_net, μ_k, F_N; |g| = 9.8 with the minus explained)',
     /F_net = ma/.test(A) && /F_fk = μ_k F_N/.test(B) && /F_fs ≤ μ_s F_N/.test(B) &&
     /Your sheet writes g = −9\.8 m\/s²; the minus sign is the direction/.test(B) &&
     /F_net = mv² \/ r/.test(D), 'notation');
  ck('formulas NOT on her sheet say so (pendulum period, torque)',
     /T = 2π √\(l \/ g\)/.test(B) && /not on your sheet/.test(B) && /not on your sheet/.test(D), 'cards');

  // Order questions really stored in order.
  const ords = U.map(u => u.qs.filter(q => q.kind === 'order'));
  ck('every order question stores four items in order with ans 0',
     ords.every(a => a.length >= 1 && a.every(q => q.opts.length === 4 && q.ans === 0)), ords.map(a=>a.length));
  ck('the stored orders are the right ones',
     /^Cart A/.test(ords[0][0].opts[0]) && /^Cart D/.test(ords[0][0].opts[3]) &&
     /^Speeding up while going up/.test(ords[1][0].opts[0]) && /^Falling freely/.test(ords[1][0].opts[3]) &&
     /level ground/.test(ords[2][0].opts[0]) && /60°/.test(ords[2][0].opts[3]) &&
     /^A: 10 m\/s/.test(ords[3][0].opts[0]) && /^D: 20 m\/s/.test(ords[3][0].opts[3]),
     ords.map(a=>a[0].opts.map(o=>o.slice(0,18))));

  // Sort sets: never name their own bucket; a clean pass logs.
  const sets = U.flatMap(u => u.sorts.map(s => ({u: u.id, s})));
  ck('two sort sets ship (balanced/unbalanced in 1-1, mass/weight in 1-2)',
     seed.a.sorts.length === 1 && seed.b.sorts.length === 1 && /Balanced/.test(seed.a.sorts[0].title), sets.map(x=>x.s.title));
  ck('no sort item names its own bucket, and every item says why',
     sets.every(({s}) => s.items.every(it => it.why &&
        ![s.a, s.b].some(lab => { const w = lab.toLowerCase().split(/\s+/)[0];
                                   return w.length > 4 && it.t.toLowerCase().includes(w); }))), 'ok');
  for (const {u, s} of sets) {
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
    }, {id: u, set: s.id});
    ck(`sort "${s.title}": a clean pass sorts every card and logs n right at 3 XP each`,
       fin.left === 0 && fin.correct === fin.n && fin.xp === fin.n * 3, fin);
  }

  // A full quiz round per unit, with the physics Sheet reachable from inside it.
  for (let i = 0; i < 4; i++) {
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
    }, U[i].id);
    ck(L[i] + ': a full round plays and logs, with the Sheet tool reachable',
       play.logged && play.total === Math.min(seed.round, U[i].qs.length) && play.sheet, play);
  }

  // Each deck walks to the end.
  for (let i = 0; i < 4; i++) {
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

  // Public repo: nobody named, no marks.
  ck('privacy: no score, mark or "she got" anywhere in the shipped records',
     !U.some(u => /she got|\bscored\b|\d+\s*\/\s*\d+\s*(marks|points)|\bout of \d+\b/i.test(u.blob)), 'ok');

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
