/* Dynamics 1 · Test Study Guide: Newton’s Laws and Momentum (Ad Astra only),
   from the teacher's N1L, N3L, COM study guide. The 30-item quiz and the
   keyed momentum practice that arrived with it were read for what they ask
   only, so this test also pins that none of their numbers comes back.

   Seeds all eight Dynamics 1 parts, so "trails 1-1 … 1-7" is a claim about
   coexistence. Every objective cluster is pinned by its TEACHING, never by
   question id; every numeric answer is re-derived from the numbers in its
   own stem; counts are minimums, so the unit stays free to grow. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8411;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const UID = 'unit-phys-dyn1-sg';
  const seed = await p.evaluate(async (UID) => {
    const files = ['phys-dyn1-newton','phys-dyn1-weight','phys-dyn1-incline','phys-dyn1-circle',
                   'phys-dyn1-hooke','phys-dyn1-impulse','phys-dyn1-momentum','phys-dyn1-sg'];
    const loaded = [];
    for (const f of files) {
      const r = await fetch('./content/'+f+'.json',{cache:'no-store'});
      if (!r.ok) continue;
      const j = await r.json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u; loaded.push(f);
    }
    saveLocal();
    const raw = await (await fetch('./content/phys-dyn1-sg.json',{cache:'no-store'})).json();
    const shipped = raw.records[UID];
    const u = DATA.records[UID];
    return {loaded, shippedStatus: shipped.status, shippedAt: shipped.updatedAt,
            u: {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order, prep:u.prep,
                quarter:u.quarter, round:u.round, cards:u.cards, qs:u.questions,
                note:u.parentNote && u.parentNote.text, blob:JSON.stringify(u)}};
  }, UID);
  const U = seed.u, allQ = U.qs;
  const ref = await p.evaluate(async () => {
    const j = await (await fetch('./content/phys-dyn1-newton.json',{cache:'no-store'})).json();
    return Object.values(j.records)[0].classId;
  });

  ck('all eight Dynamics 1 parts seed', seed.loaded.length === 8, seed.loaded);
  ck('classId matches the shipped Dynamics 1 parts (the v136 orphan trap)',
     U.classId === 'physics' && U.classId === ref, [U.classId, ref]);
  ck('title, exactly', U.title === 'Dynamics 1 · Test Study Guide: Newton’s Laws and Momentum', U.title);
  ck('prep:true, order 1, libv 1+, quarter 2, a round near 12',
     U.prep === true && U.order === 1 && U.libv >= 1 && U.quarter === 2 && U.round >= 10 && U.round <= 14,
     [U.prep, U.order, U.libv, U.quarter, U.round]);
  ck('shipped as a draft, stamped in the past',
     seed.shippedStatus === 'draft' && seed.shippedAt < Date.now() - 3600e3, [seed.shippedStatus, seed.shippedAt]);

  const shelf = await p.evaluate(() => {
    const s = shelvesFor('physics');
    const d = s.shelves.find(x=>x.name==='Dynamics 1');
    return {loose: s.loose.map(u=>u.title), d1: d ? d.units.map(u=>lessonLabel(u)) : []};
  });
  const want = ['1-1','1-2','1-3','1-4','1-5','1-6','1-7'];
  ck('Dynamics 1 runs 1-1 … 1-7, then the study guide last, nothing loose',
     shelf.d1.length === 8 && want.every((w,i) => shelf.d1[i].startsWith(w + ' ')) &&
     /^Test Study Guide/.test(shelf.d1[7]) && shelf.loose.length === 0, shelf);

  ck('20–28 cards and 28–36 questions', U.cards.length >= 20 && U.cards.length <= 28 && allQ.length >= 28 && allQ.length <= 36,
     [U.cards.length, allQ.length]);
  ck('every MC question has four unique options and an answer in range',
     allQ.filter(q=>(q.kind||'mc')==='mc').every(q => q.opts.length === 4 && new Set(q.opts).size === 4 && q.ans >= 0 && q.ans < 4), 'ok');
  ck('asks at all three levels', [1,2,3].every(l => allQ.filter(q=>q.lv===l).length >= 5),
     [1,2,3].map(l=>allQ.filter(q=>q.lv===l).length));
  const slots = [0,1,2,3].map(s => allQ.filter(q=>(q.kind||'mc')==='mc' && q.ans===s).length);
  ck('answers spread across all four slots (_balance ran)', slots.every(n=>n >= 5), slots);
  ck('every card def leads with a bold answer', U.cards.every(c => /^\*\*/.test(c.def)), 'ok');
  ck('every question: 3–6 steps, a hint, a bold ex.main and a tip',
     allQ.every(q => q.steps.length >= 3 && q.steps.length <= 6 && q.hint && /^\*\*/.test(q.ex.main) && q.ex.tip), 'ok');
  ck('every card and question declares its origin', U.cards.concat(allQ).every(x => x.from === 'source' || x.from === 'added'), 'ok');

  const BACK = /^\s*(the same|that same|for (that|the) same|from the same|using the same|in the same|with the same)\b/i;
  ck('no stem leans on a neighbour', !allQ.some(q => BACK.test(q.q) || /\bthat same\b/i.test(q.q) || /\b(as before|from before|the previous)\b/i.test(q.q)),
     allQ.filter(q => BACK.test(q.q)).map(q=>q.q));
  ck('nothing refers to an option by position',
     !allQ.some(q => /\b(all|none|both) of the above\b|\b(first|second|third|fourth|last) (option|choice|answer)\b|\boptions? [a-d1-4]\b/i
                      .test([q.q, q.hint, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');
  ck('a stem that says "the graph shown" carries a graph',
     allQ.filter(q => /graph shown/.test(q.q)).length >= 1 && allQ.filter(q => /graph shown/.test(q.q)).every(q => q.graph), 'ok');
  /* A momentum stem needs a positive direction when its answer is signed or
     things move both ways in it. (A force stem whose answer NAMES its
     direction, "15 N east", does not.) */
  const needsSign = q => q.opts.some(o => /^[−+]/.test(o)) || (/m\/s\b/.test(q.q) && /\beast\b/.test(q.q) && /\bwest\b/i.test(q.q));
  ck('every momentum stem that needs a sign names its positive direction',
     allQ.filter(needsSign).length >= 3 && allQ.filter(needsSign).every(q => /as positive/.test(q.q)),
     allQ.filter(q => needsSign(q) && !/as positive/.test(q.q)).map(q=>q.q.slice(0,60)));
  ck('every stem that uses g says g = 9.8 m/s²',
     allQ.filter(q => /\d+(\.\d+)? kg\b/.test(q.q) && /(normal force|tension)/.test(q.q)).every(q => /g = 9\.8 m\/s²/.test(q.q)), 'ok');

  // ---- none of the quiz's or the practice's own numbers -------------------
  const QUIZ = /(?<![\d.])(12 kg|45 N(?![/·])|75 kg|20 kg|60 N(?![/·])|5\.0 kg|70 kg|140 N|15 kg|25 kg|80 N(?![/·])|50 kg|100 N(?![/·])|120 N(?![/·])|10 kg|35 N(?![/·])|40 kg|60 kg|30 kg|6\.0 kg|12 N(?![/·])|1000 kg|2000 kg|6000 N|25°|30°|73\.5|117\.6|735 N|588 N|266 N|156\.8|39\.2 N|86\.6)/;
  const graded = allQ.flatMap(q => q.kind === 'order' ? [q.q].concat(q.opts) : [[q.q].concat(q.opts).join(' ')]);
  ck('none of the 30-item quiz’s figures is reused in a stem or option',
     !graded.some(t => QUIZ.test(t)), graded.map(t => (t.match(QUIZ)||[])[0]).filter(Boolean));
  const HW = [['2.0','5.0'],['3.0','4.0'],['2.0','6.0'],['1.0','8.0'],['0.20','15'],['0.50','10'],
              ['1.5','4.0'],['4.0','3.0'],['3.0','10'],['0.10','20'],['1.0','6.0'],['2.0','4.0'],
              ['0.40','5.0'],['2.0','3.0'],['1.0','12'],['0.20','10'],['0.50','8.0'],['60','10'],['0.50','6.0']];
  const esc = s => s.replace('.', '\\.');
  const hwHit = graded.flatMap(t => t.split(/(?<=[.?;:])\s/))
      .filter(sn => HW.some(([m,v]) => new RegExp(`(?<![\\d.])${esc(m)} kg\\b[^.?;]*?(?<![\\d.])${esc(v)} m/s`).test(sn)));
  ck('none of the momentum practice’s (mass, speed) pairings is reused', hwHit.length === 0, hwHit);
  ck('no quiz scenario lifted wholesale (hockey puck, horse and cart, swimmer, astronaut push, rocket exhaust)',
     !allQ.some(q => /hockey puck|horse|swimmer|astronaut pushes|exhaust/i.test(q.q)), 'ok');

  // ---- every numeric answer re-derived from its own stem ------------------
  const num = s => s.replace(/(\d) (\d{3})\b/g, '$1$2').match(/\d+(\.\d+)?/g).map(Number);
  const val = o => parseFloat(o.replace('−','-').replace('+',''));
  const A = q => q.opts[q.ans];
  const close = (a, b, tol) => Math.abs(a - b) <= (tol == null ? 0.051 : tol);
  const rad = d => d * Math.PI / 180;
  const D = [
    [/160 N\/m is stretched 4\.5 cm/,   (n,q) => close(val(A(q)), n[0]*n[1]/100)],
    [/marked point\s+is \(16 cm, 5\.6 N\)/, (n,q) => { const pt = q.graph.pts[0], L = q.graph.series[0];
                                          return close(L.m*pt.x, pt.y) && close(val(A(q)), pt.y/(pt.x/100)) && /N\/m$/.test(A(q)); }],
    [/weight on Mars/,                  (n,q) => close(val(A(q)), n[1]/n[0], 0.5) && /kg$/.test(A(q))],
    [/36 kg trunk/,                     (n,q) => close(val(A(q)), n[0]*9.8 - n[1], 0.5)],
    [/flower pots/,                     (n,q) => close(val(A(q)), (n[0]+n[1])*9.8)],
    [/N banner hangs/,                  (n,q) => close(val(A(q)), n[0]/(2*Math.sin(rad(n[1]))), 0.5)],
    [/free-body diagram shows 260 N/,   (n,q) => new RegExp(`^Net force ${n[2]-n[3]} N east: its velocity changes`).test(A(q))],
    [/1500 kg car and a 6000 kg truck/, (n,q) => n[1]/n[0] === 4 && /^Four times/.test(A(q))],
    [/130 N east, 85 N west/,           (n,q) => A(q) === `${n[0]-n[1]-n[2]} N east`],
    [/3000 kg bus hits a 0\.0020 kg bug/, (n,q) => /pushes on the bus with 1\.5 N; the bug’s acceleration is far larger/.test(A(q)) &&
                                          n[2]/n[1] > n[2]/n[0]],
    [/36 N east, 15 N north, and 39 N/, (n,q) => close(n[2]*Math.cos(rad(n[3])), n[0], 0.05) && close(n[2]*Math.sin(rad(n[3])), n[1], 0.05) && /^Yes: the east–west/.test(A(q))],
    [/160 N at 35° above/,              (n,q) => close(val(A(q)), n[0]*Math.cos(rad(n[1])), 0.5)],
    [/20 N east and 21 N north/,        (n,q) => close(val(A(q)), Math.hypot(n[0], n[1]))],
    [/16 N east and 30 N north/,        (n,q) => close(val(A(q)), Math.atan2(n[1], n[0])*180/Math.PI) && /north of east$/.test(A(q))],
    [/0\.35 kg cart moves east at 2\.4/, (n,q) => close(val(A(q)), n[0]*n[1] - n[2]*n[3]) && /^\+/.test(A(q))],
    [/1\.8 kg cart moving east at 4\.5/, (n,q) => close(val(A(q)), n[0]*(n[2]-n[1])) && /^−/.test(A(q))],
    [/2\.5 kg cart moving east at 2\.0 m\/s hits a\s+1\.5 kg/, (n,q) => close(val(A(q)), (n[0]*n[1] - n[3]*n[4])/n[2]) && /east$/.test(A(q))],
    [/480 kg cannon/,                   (n,q) => close(val(A(q)), n[1]*n[2]/n[0]) && /west$/.test(A(q))],
    [/1\.2 kg cart moves east at 1\.5 m\/s and a\s+0\.90 kg/, (n,q) => close(n[0]*n[1] - n[2]*n[3], 0, 1e-9) && /stop/.test(A(q))],
    [/loses 3\.0 kg·m\/s/,               (n,q) => /^It gains 3\.0 kg·m\/s, in the direction the first cart moved$/.test(A(q))],
  ];
  const der = D.map(([re, f]) => { const q = allQ.find(x => re.test(x.q)); return {re: String(re), found: !!q, ok: !!q && f(num(q.q), q)}; });
  ck(`every numeric answer re-derived from its stem (${D.length} questions)`, der.every(d => d.found && d.ok),
     der.filter(d => !d.ok));
  ck('no numeric distractor equals the answer (same number, same unit)',
     allQ.filter(q => (q.kind||'mc')==='mc' && /^[−+]?\d/.test(A(q)))
         .every(q => q.opts.every((o,i) => i === q.ans || !/^[−+]?\d/.test(o) || val(o) !== val(A(q)) ||
                                   o.replace(/[\d.−+ ]/g,'') !== A(q).replace(/[\d.−+ ]/g,''))), 'ok');

  // Order questions: stored in order, ans 0, and the momentum ranking recomputes.
  const ords = allQ.filter(q => q.kind === 'order');
  ck('one or two order questions, four items each, ans 0',
     ords.length >= 1 && ords.length <= 2 && ords.every(q => q.opts.length === 4 && q.ans === 0), ords.length);
  const pq = ords.find(q => /momentum/.test(q.q));
  const pv = pq ? pq.opts.map(o => { const n = num(o); return n[0]*n[1]; }) : [];
  ck('momentum ranking recomputes strictly descending, with the fastest object last',
     pv.length === 4 && pv.every((v,i) => i === 0 || v < pv[i-1]) && /bullet at 400/.test(pq.opts[3]), pv);

  // ---- every objective cluster on the guide, pinned by its teaching -------
  const card = re => U.cards.some(c => re.test(c.term + ' ' + c.def + ' ' + (c.eq||'') + ' ' + (c.hint||'')));
  const qWith = (stem, right, wrong) => allQ.some(q => stem.test(q.q) && right.test(A(q)) &&
                                         (!wrong || q.opts.some((o,i) => i !== q.ans && wrong.test(o))));
  const COV = {
    'SI · fundamental vs derived units':
      card(/fundamental \(base\) SI unit/) && card(/N = kg·m\/s²/) && qWith(/derived SI unit/, /newton/, /kilogram/),
    'Hooke · proportional, opposite, F = −kx':
      card(/proportional/) && card(/F = −kx/) && qWith(/squeezes it 4 cm/, /^Away from the wall/, /^Toward the wall/),
    'Hooke · calculate a spring force (cm converted)':
      qWith(/160 N\/m/, /^7\.2 N$/, /^720 N$/),
    'Hooke · k from a force–extension graph':
      card(/slope of the straight line is the spring constant/) && qWith(/graph shown/, /^35 N\/m$/, /^0\.35 N\/m$/),
    'Forces · normal, tension, friction, spring defined and identified':
      card(/Normal: a surface pushing/) && card(/Tension: a rope/) && card(/Friction: a surface resisting/) &&
      card(/Spring force: a stretched/) && qWith(/climber hangs/, /^Tension$/, /^Normal force$/),
    'Weight · Fg = mg, and mass from weight':
      card(/Fg = mg/) && qWith(/weight on Mars/, /^300 kg$/, /^113 kg$/),
    'Mass · two jobs, independent of gravity, mass vs weight':
      card(/measures how hard the object is to speed up/) && card(/sets how strongly gravity pulls/) &&
      card(/same on Earth, on the Moon/) && qWith(/floats weightless/, /^Just as hard/, /no inertia/),
    'Normal force · level surface, at rest':
      card(/normal force equals the weight, mg/) && qWith(/36 kg trunk/, /^203 N$/, /^503 N$/),
    'Tension · parallel forces in equilibrium':
      card(/upward tensions add up/) && qWith(/flower pots/, /^58\.8 N$/, /^34\.3 N$/),
    'Tension · at angles, verticals hold the weight':
      card(/2T sin θ = weight/) && qWith(/banner/, /^163 N$/, /^137 N$/),
    'System · forces on it vs forces it exerts':
      card(/only forces acting ON it count/) && qWith(/free-body diagram of the CART/, /girl’s push on the cart/, /cart’s push back on the girl/),
    'Free-body diagrams · construct and analyze':
      card(/drawn as a dot/) && ords.some(q => /free-body diagram/.test(q.q)) &&
      qWith(/free-body diagram shows/, /^Net force 25 N east/, /^Net force 165 N/),
    'Inertia · related to mass, compared quantitatively':
      card(/Inertia is that resistance/) && qWith(/inertia compare/, /^Four times/, /^The same: neither is moving/),
    'Newton’s first law · predict motion':
      card(/keeps its velocity/) && qWith(/coin sits on a card/, /drops into the glass/, /sideways with the card/),
    'Net force · from a description of motion; change only with a net force':
      card(/Speeding up, slowing down OR changing direction/) && qWith(/nonzero net force/, /around a bend/, /terminal velocity/),
    'Net force · the vector sum':
      card(/vector sum of all the forces/) && qWith(/Three horizontal forces/, /^15 N east$/, /^245 N east$/),
    'Third law · state and apply; partners by swapping names':
      card(/B exerts a force on A of equal\s+size/) && qWith(/bus pushes on the bug/, /1\.5 N; the bug’s acceleration is far larger/, /far less than 1\.5 N/),
    'Third law · the four characteristics':
      card(/equal in size, opposite in direction, simultaneous,\s+and acts on two DIFFERENT objects/) &&
      qWith(/NOT true of a Newton’s third-law/, /same object/, /start and stop at the same moment/),
    'Third law · weight and normal force offered as the tempting non-pair':
      card(/NOT a third-law\s+pair/) && qWith(/Earth pulls the dictionary down/, /dictionary pulls up on Earth/, /desk pushes up on the dictionary/),
    'Equilibrium · static vs dynamic':
      card(/static\s+if it is at rest, dynamic if it moves at constant velocity/) &&
      qWith(/elevator rises at a steady/, /^Dynamic equilibrium/, /^Static equilibrium/),
    'Balanced vs unbalanced · predict the motion':
      card(/Balanced forces \(net force zero\)/) && qWith(/free-body diagram shows/, /velocity changes/, /constant speed/),
    'Components · resolve an angled force (sin/cos swap offered)':
      card(/F cos θ/) && qWith(/160 N at 35°/, /^131 N$/, /^92 N$/),
    'Resultant · Pythagoras':
      card(/R = √\(Fx² \+ Fy²\)/) && qWith(/20 N east and 21 N north/, /^29 N$/, /^41 N$/),
    'Resultant · angle by inverse tangent (flipped ratio and radian mode offered)':
      card(/tan⁻¹/) && qWith(/16 N east and 30 N north/, /^61\.9° north of east$/, /^28\.1° north of east$/) &&
      qWith(/16 N east and 30 N north/, /61\.9/, /^1\.1°/),
    'Equilibrium · two dimensions, each axis separately':
      card(/ΣFx = 0 and ΣFy = 0/) && qWith(/Is the ring in equilibrium/, /^Yes: the east–west/, /36 N \+ 15 N/),
    'Momentum · p = mv, a vector, kg·m/s = N·s':
      card(/p = mv/) && card(/kg·m\/s \(the same as N·s\)/) && qWith(/BOTH measure momentum/, /^kg·m\/s and N·s$/, /^kg·m\/s² and N$/),
    'Momentum · mass and velocity both scale it; compare by multiplying':
      card(/double either\s+and p doubles/) && !!pq,
    'System · total momentum with signs, direction from the sign':
      card(/group of interacting objects/) && qWith(/total momentum of the\s+two-cart system/, /^\+0\.24/, /^\+1\.44/),
    'Change in momentum · Δp = pf − pi':
      card(/Δp = p_f − p_i/) && qWith(/slows to\s+1\.5 m\/s/, /^−5\.4/, /^\+5\.4/),
    'Conservation · the law, and a closed system = no net external force':
      card(/no net external force/) && qWith(/“closed”/, /^No net external force/, /No forces of any kind/),
    'Conservation · solve a 2-object problem':
      qWith(/1\.5 kg cart at rest/, /^2\.5 m\/s east$/, /^3\.3 m\/s east$/) && qWith(/cannon/, /^1\.25 m\/s west$/, /^150 m\/s west$/),
    'Collisions · momentum transfer':
      card(/whatever momentum one object loses, the other gains/) && qWith(/loses 3\.0 kg·m\/s/, /^It gains 3\.0/, /lost as sound/),
    'Predict motion after an interaction':
      qWith(/stick together\.\s+What happens next/, /^They stop dead$/, /heavier/),
  };
  const miss = Object.entries(COV).filter(([k,v]) => !v).map(([k]) => k);
  ck(`every objective cluster on the guide is taught and asked (${Object.keys(COV).length} clusters)`, miss.length === 0, miss);

  // Provenance and the parent note.
  ck('the guide-names-only cards are flagged as study suggestions',
     ['Fundamental and derived SI units','Drawing a free-body diagram','Static and dynamic equilibrium']
       .every(t => (U.cards.find(c => c.term === t)||{}).from === 'added'), 'flags');
  ck('parent note: built from the guide; quiz and practice read for what they ask, not transcribed',
     /study guide/.test(U.note) && /read for what they ask only and not transcribed/.test(U.note) &&
     /nothing written on either paper is recorded/.test(U.note), 'note');
  ck('parent note offers the 30-item quiz as a paper-entry guide if confirmed as practice',
     /confirmed as practice/.test(U.note) && /paper-entry/.test(U.note), 'note');
  ck('parent note names g = 9.8 against the practice’s g = 10', /g = 10 m\/s²/.test(U.note) && /9\.8/.test(U.note), 'note');

  // The gold prep treatment on the shelf and on the opened card.
  const gold = await p.evaluate((UID) => {
    go('shelf', {classId:'physics', series:'Dynamics 1', open: UID});
    const stops = [...document.querySelectorAll('#screen .stop')];
    const prep = stops.filter(s => s.classList.contains('prep'));
    const pip = prep[0] && prep[0].querySelector('.pip');
    const oc = document.getElementById('shelfopen');
    return {stops: stops.length, prepStops: prep.length, pipGold: pip ? getComputedStyle(pip).borderColor : null,
            isPrepCard: oc ? oc.classList.contains('prepcard') : false,
            band: oc && oc.querySelector('.prepband') ? oc.querySelector('.prepband').textContent : null,
            title: oc && oc.querySelector('h3') ? oc.querySelector('h3').textContent : null};
  }, UID);
  ck('exactly one gold-ringed prep stop among the eight', gold.stops === 8 && gold.prepStops === 1 && /242, 202, 99/.test(gold.pipGold||''), gold);
  ck('the opened study guide wears the Test prep band', gold.isPrepCard && /TEST PREP/i.test(gold.band||''), gold);

  // A full round plays and logs.
  const play = await p.evaluate(async (uid) => {
    quizState = null;
    go('quiz', {unitId: uid, classId: 'physics'});
    const sheet = [...document.querySelectorAll('#screen .tool')].some(t=>/Sheet/.test(t.textContent));
    let guard = 0, graphs = 0;
    while (view === 'quiz' && guard++ < 120) {
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
  }, UID);
  ck('a full round plays and logs one round’s worth, with the physics Sheet reachable',
     play.logged && play.total === Math.min(U.round, allQ.length) && play.sheet, play);
  const gr = await p.evaluate((uid) => DATA.records[uid].questions.filter(q => q.graph)
      .map(q => { const n = graphNode(q.graph); return n ? n.querySelectorAll('polyline').length : 0; }), UID);
  ck('the graph question renders a drawn line', gr.length >= 1 && gr.every(n => n >= 1), gr);

  // The deck opens and walks to the end.
  const deck = await p.evaluate(async (uid) => {
    cardState = {}; go('cards', {unitId: uid, classId: 'physics'});
    const opened = view === 'cards' && !!document.querySelector('#screen .face');
    let seen = 0;
    while (cardState.unitId === uid && seen++ < 40) {
      const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
      if (!knew) break;
      knew.click(); await new Promise(r=>setTimeout(r,5));
    }
    return {opened, seen};
  }, UID);
  ck('the flashcard deck opens and steps all the way through', deck.opened && deck.seen >= U.cards.length, deck);

  // Public repo: no marks, no names.
  ck('privacy: no score, mark, circled letter or "she got" anywhere in the shipped record',
     !/she got|\bscored\b|\bout of \d+\b|\d+\s*\/\s*\d+\s*(correct|right|marks|points)|\b\d+(\.\d+)?\s?%|\bcircled\b|\bher (answer|working|mark)s?\b|\bkey (says|letter)\b/i.test(U.blob), 'ok');
  ck('privacy: no names', !/Sedona|Ortiz|River\b|Chris\b|\bKat\b/.test(U.blob), 'ok');

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,500))));
  console.log(`${out.filter(r=>r.ok).length}/${out.length}`, out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES', '· seeded:', seed.loaded.join(', '));
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
