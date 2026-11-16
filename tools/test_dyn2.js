/* Dynamics 2 · 2-1 Applying Newton's Second Law, 2-2 Friction and the
   Coefficient, 2-3 The Newton's Second Law Lab (Ad Astra only), from the three
   sheets in Physics 8 › Dynamics 2.

   Seeds EVERY content/phys-dyn*.json on disk (not CONTENT_LIBRARY), so the new
   shelf is a claim about coexistence with Dynamics 1. Every numeric answer is
   re-derived here from the numbers in its own stem; every trap is pinned by
   its TEACHING (the slip offered as a wrong option), never by question id;
   counts are ranges, so a unit stays free to grow a little. */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const PORT = process.argv[2] || 8432;
const FILES = fs.readdirSync(path.join(__dirname, '..', 'content'))
  .filter(f => /^phys-dyn.*\.json$/.test(f)).sort();
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const IDS = ['unit-phys-dyn2-n2l', 'unit-phys-dyn2-friction', 'unit-phys-dyn2-lab'];
  const seed = await p.evaluate(async ({FILES, IDS}) => {
    const loaded = [], raw = {};
    for (const f of FILES) {
      const r = await fetch('./content/' + f, {cache:'no-store'});
      if (!r.ok) continue;
      const j = await r.json();
      for (const u of Object.values(j.records).filter(x => x.type === 'unit')) {
        raw[u.id] = {status: u.status, libv: u.libv, updatedAt: u.updatedAt};
        u.status = 'approved'; u.updatedAt = Date.now() - 1000; DATA.records[u.id] = u; loaded.push(f);
      }
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order, prep:u.prep,
              quarter:u.quarter, cards:u.cards, qs:u.questions, raw: raw[id],
              note:u.parentNote && u.parentNote.text, blob:JSON.stringify(u)}; };
    return {loaded, U: IDS.map(pick), round: QUIZ_ROUND};
  }, {FILES, IDS});
  const U = seed.U, [N2, FR, LB] = U, L = ['2-1', '2-2', '2-3'];

  // ---- identity and shelf ---------------------------------------------------
  ck('all three load under the real physics classId (the v136 orphan trap)',
     U.every(u => u.classId === 'physics'), U.map(u => u.classId));
  ck('titles exactly, with the curly apostrophe',
     N2.title === 'Dynamics 2 · 2-1 Applying Newton’s Second Law' &&
     FR.title === 'Dynamics 2 · 2-2 Friction and the Coefficient' &&
     LB.title === 'Dynamics 2 · 2-3 The Newton’s Second Law Lab: Mass and Acceleration', U.map(u => u.title));
  ck('shipped as drafts with libv 1, updatedAt in the past, quarter 2, no order, no prep',
     U.every(u => u.raw.status === 'draft' && u.raw.libv === 1 && u.raw.updatedAt < Date.now() - 3600e3 &&
                  u.quarter === 2 && u.order == null && !u.prep), U.map(u => [u.raw, u.quarter, u.order, u.prep]));
  const shelf = await p.evaluate(() => {
    const s = shelvesFor('physics');
    const lab = n => { const d = s.shelves.find(x => x.name === n); return d ? d.units.map(u => lessonLabel(u)) : []; };
    return {names: s.shelves.map(x => x.name), loose: s.loose.map(u => u.title), d1: lab('Dynamics 1'), d2: lab('Dynamics 2')};
  });
  ck('Dynamics 2 is its own shelf: 2-1, 2-2, 2-3 in order',
     shelf.d2.length === 3 && ['2-1', '2-2', '2-3'].every((t, i) => shelf.d2[i].startsWith(t + ' ')), shelf.d2);
  ck('Dynamics 1 untouched: 1-1 … 1-7 in order, plus its study guide, nothing loose',
     ['1-1','1-2','1-3','1-4','1-5','1-6','1-7'].every((t, i) => shelf.d1[i] && shelf.d1[i].startsWith(t + ' ')) &&
     shelf.d1.length === 8 && shelf.loose.length === 0 && shelf.names.includes('Dynamics 1'), shelf);

  // ---- shape ----------------------------------------------------------------
  ck('sizes: 2-1 and 2-2 have 14–18 cards / 18–22 qs; 2-3 has 12–16 / 14–18',
     [N2, FR].every(u => u.cards.length >= 14 && u.cards.length <= 18 && u.qs.length >= 18 && u.qs.length <= 22) &&
     LB.cards.length >= 12 && LB.cards.length <= 16 && LB.qs.length >= 14 && LB.qs.length <= 18,
     U.map(u => [u.cards.length, u.qs.length]));
  ck('every question has four unique options and an answer in range',
     U.every(u => u.qs.every(q => q.opts.length === 4 && new Set(q.opts).size === 4 && q.ans >= 0 && q.ans < 4)), 'ok');
  ck('every unit asks at all three levels', U.every(u => [1,2,3].every(l => u.qs.some(q => q.lv === l))),
     U.map(u => [1,2,3].map(l => u.qs.filter(q => q.lv === l).length)));
  for (let i = 0; i < 3; i++) {
    const slots = [0,1,2,3].map(s => U[i].qs.filter(q => (q.kind||'mc') === 'mc' && q.ans === s).length);
    ck(L[i] + ': answers sit in all four slots (_balance ran)', slots.every(n => n > 0), slots);
  }
  ck('every card def leads with a bold answer', U.every(u => u.cards.every(c => /^\*\*/.test(c.def))), 'ok');
  ck('every question carries 3–6 steps and a bold ex.main',
     U.every(u => u.qs.every(q => q.steps.length >= 3 && q.steps.length <= 6 && /^\*\*/.test(q.ex.main))), 'ok');
  const allQ = U.flatMap(u => u.qs);
  ck('no stem opens by back-referencing a neighbour',
     !allQ.some(q => /^\s*(the|that|for the|using the|with the|in the|from the) same\b/i.test(q.q)),
     allQ.filter(q => /^\s*(\w+ )?(the|that) same/i.test(q.q)).map(q => q.q.slice(0, 60)));
  ck('nothing refers to an option by position',
     !allQ.some(q => /\b(all|none|both) of the above\b|\b(first|second|third|fourth|last) (option|choice|answer)\b|\boptions? [a-d1-4]\b/i
                      .test([q.q, q.hint, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');
  ck('no stem contains its own correct option',
     allQ.filter(q => q.kind !== 'order').every(q => !q.q.includes(q.opts[q.ans])),
     allQ.filter(q => q.kind !== 'order' && q.q.includes(q.opts[q.ans])).map(q => q.q.slice(0, 60)));
  ck('a stem that says "the graph shown" carries a graph',
     allQ.filter(q => /graph shown/.test(q.q)).length >= 2 && allQ.filter(q => /graph shown/.test(q.q)).every(q => q.graph), 'ok');

  // ---- fresh numbers: nothing from the three sheets --------------------------
  const SRC = /(?<![\d.])(12(\.0)? kg|60(\.0)? N\b|52 N\b|30°|35°|3\.2 m\/s²|50(\.0)? N\b|4(\.0)? kg|6(\.0)? kg|65(\.0)? kg|520 N\b|2\.0 m\/s²|1\.5 m\/s²|3(\.0)? m\/s(?!²)|3 m\/s²|0\.48|1\.02|1\.49|2\.03|2\.48|140 N\b|60 kg|30 N\b|0\.30\b|0\.20\b|37°|0\.45\b|10 m\/s(?!²)|5(\.0)? m\/s(?!²)|2\.5 m(?![\/\w²]))/;
  const hits = allQ.flatMap(q => [q.q].concat(q.opts)).filter(t => SRC.test(t)).map(t => t.match(SRC)[0] + ' ← ' + t.slice(0, 50));
  ck('none of the three sheets’ numbers is reused in a stem or option', hits.length === 0, hits);

  // ---- every numeric answer re-derived from its own stem --------------------
  const g = 9.8, rad = d => d * Math.PI / 180, S = d => Math.sin(rad(d)), Co = d => Math.cos(rad(d));
  const num = s => (s.match(/\d+(\.\d+)?/g) || []).map(Number);
  const val = o => parseFloat(o.replace('−', '-'));
  const dec = o => { const m = o.match(/\d+\.(\d+)/); return m ? m[1].length : 0; };
  const rounds = (o, x) => Math.abs(val(o) - x) <= 0.5 * Math.pow(10, -dec(o)) + 1e-9;
  const A = q => q.opts[q.ans];
  const slopeOf = gr => { const P = gr.pts; return (P[P.length-1].y - P[0].y) / (P[P.length-1].x - P[0].x); };
  const D = [
    [N2, /pull acts on the 5\.0 kg block\. What is the acceleration/, (n,q) => rounds(A(q), n[2]/(n[0]+n[1]))],
    [N2, /What is the tension in the string\?$/, (n,q) => rounds(A(q), n[0] * n[2]/(n[0]+n[1]))],
    [N2, /now acts on the 3\.0 kg block/, (n,q) => { const a = n[2]/(n[0]+n[1]); const [x, y] = A(q).split(' and ');
                                          return rounds(x, a) && rounds(y, n[1]*a); }],
    [N2, /56 kg student/,          (n,q) => rounds(A(q), n[0]*(g + n[1]))],
    [N2, /70 kg passenger/,        (n,q) => rounds(A(q), n[0]*(g - n[1]))],
    [N2, /58 kg student/,          (n,q) => rounds(A(q), n[0]*g)],
    [N2, /45 kg student/,          (n,q) => { const a = n[1]/n[0] - g; return rounds(A(q), Math.abs(a)) && /upward/.test(A(q)) === a > 0; }],
    [N2, /What is the normal force from the floor/, (n,q) => rounds(A(q), n[0]*g - n[1]*S(n[2]))],
    [N2, /kinetic friction on it is 40 N/, (n,q) => rounds(A(q), (n[1]*Co(n[2]) - n[3])/n[0])],
    [N2, /4\.5 kg block slides down/, (n,q) => rounds(A(q), n[0]*g*S(n[1]) - n[0]*n[2])],
    [N2, /What is the cart’s mass/, (n,q) => rounds(A(q), 1/slopeOf(q.graph))],
    [N2, /3\.5 N net force/,       (n,q) => rounds(A(q), n[0]*n[1])],
    [FR, /85 N horizontal force/,  (n,q) => rounds(A(q), n[0]/(n[1]*g))],
    [FR, /How big is\s+the friction on the 3\.0 kg/, (n,q) => rounds(A(q), n[2]*n[3]*g)],
    [FR, /What is their acceleration/, (n,q) => rounds(A(q), (n[2] - n[4]*g*(n[0]+n[1]))/(n[0]+n[1]))],
    [FR, /What is the tension in the string\?$/, (n,q) => { const a = (n[2] - n[5]*g*(n[0]+n[1]))/(n[0]+n[1]);
                                          return rounds(A(q), n[0]*(a + n[5]*g)); }],
    [FR, /What is the normal force on the block/, (n,q) => rounds(A(q), n[0]*(g + n[1]))],
    [FR, /pushed sideways/,        (n,q) => rounds(A(q), (n[2] - n[3]*n[0]*(g + n[1]))/n[0])],
    [FR, /How big is the friction\?$/, (n,q) => rounds(A(q), n[3]*(n[0]*g - n[2]*S(n[1])))],
    [FR, /What is its acceleration\?$/, (n,q) => { const f = n[3]*(n[0]*g - n[2]*S(n[1]));
                                          return rounds(A(q), (n[2]*Co(n[1]) - f)/n[0]); }],
    [FR, /acceleration while it slides up/, (n,q) => rounds(A(q), g*(S(n[0]) + n[2]*Co(n[0]))) && /down the slope/.test(A(q))],
    [FR, /How far\s+up the ramp/, (n,q) => rounds(A(q), n[1]**2/(2*g*(S(n[0]) + n[2]*Co(n[0]))))],
    [FR, /on the way down\?$/,     (n,q) => rounds(A(q), g*(S(n[0]) - n[1]*Co(n[0])))],
    [FR, /reaches the bottom/,     (n,q) => { const up = g*(S(n[0]) + n[3]*Co(n[0])), dn = g*(S(n[0]) - n[3]*Co(n[0]));
                                          const d = n[1]**2/(2*up); return rounds(A(q), Math.sqrt(2*dn*d)) && val(A(q)) < n[1]; }],
    [FR, /A puck slides/,          (n,q) => rounds(A(q), n[1]**2/(2*n[2])/(g + n[0]))],
    [LB, /120 g mass/,             (n,q) => rounds(A(q), n[0]/1000*g)],
    [LB, /What total mass/,        (n,q) => rounds(A(q), n[0] + n[1] + n[2])],
    [LB, /travels 0\.72 m in 1\.2 s/, (n,q) => rounds(A(q), 2*n[0]/n[1]**2)],
    [LB, /passes through the\s+origin/, (n,q) => n[0] === 1 && rounds(A(q), (n[4]-n[2])/(n[3]-n[1]))],   // n[0] is the 1 in “1 ÷ total mass”
    [LB, /Three lab runs/,         (n,q) => rounds(A(q), (n[0]*n[1] + n[2]*n[3] + n[4]*n[5])/3)],
    [LB, /average force is 0\.90 N/, (n,q) => rounds(A(q), Math.abs(n[0]-n[1])/n[1]*100)],
  ];
  const der = D.map(([u, re, f]) => { const q = u.qs.find(x => re.test(x.q));
    return {re: String(re), found: !!q, ok: !!q && f(num(q.q), q)}; });
  ck(`every numeric answer re-derived from its stem (${D.length} questions)`,
     der.every(d => d.found && d.ok), der.filter(d => !d.found || !d.ok));
  // Compound options ("5.0 m/s² and 25 N") compare every number in them.
  const nums = o => (o.match(/\d+(\.\d+)?/g) || []).join(',') + '|' + o.replace(/[\d.−]/g, '');
  const clash = allQ.filter(q => q.kind !== 'order' && /^[−]?\d/.test(A(q)))
    .filter(q => q.opts.some((o, i) => i !== q.ans && nums(o) === nums(A(q))));
  ck('no numeric distractor rounds to the same value as the answer', clash.length === 0, clash.map(q => q.opts));

  // ---- order questions: stored in order -------------------------------------
  const ords = U.map(u => u.qs.filter(q => q.kind === 'order'));
  ck('each unit carries an order question: four items, ans 0',
     ords.every(o => o.length >= 1 && o.every(q => q.opts.length === 4 && q.ans === 0)), ords.map(o => o.length));
  ck('2-1 order is the connected-blocks routine: diagrams, system a, one block, solve for T',
     /^Draw a free-body/.test(ords[0][0].opts[0]) && /one system/.test(ords[0][0].opts[1]) &&
     /Choose one block/.test(ords[0][0].opts[2]) && /tension/.test(ords[0][0].opts[3]), ords[0][0].opts);
  ck('2-2 order is the up-the-ramp routine: forces, N and f, deceleration, distance',
     /both down the slope/.test(ords[1][0].opts[0]) && /normal force/.test(ords[1][0].opts[1]) &&
     /deceleration/.test(ords[1][0].opts[2]) && /v² = v₀² \+ 2aΔx/.test(ords[1][0].opts[3]), ords[1][0].opts);
  ck('2-3 order is the lab: weight, runs, a = 2Δx ÷ t², then the 1/M graph',
     /weight of the hanging/.test(ords[2][0].opts[0]) && /from rest/.test(ords[2][0].opts[1]) &&
     /2Δx ÷ t²/.test(ords[2][0].opts[2]) && /1 ÷ total mass/.test(ords[2][0].opts[3]), ords[2][0].opts);

  // ---- the named traps, each pinned by its teaching -------------------------
  const qWith = (u, stem, right, wrong) => u.qs.some(q => stem.test(q.q) && right.test(A(q)) &&
                                         (!wrong || q.opts.some((o, i) => i !== q.ans && wrong.test(o))));
  const B = U.map(u => u.blob);
  ck('trap · only one block’s mass in the system (8.0 offered)',
     qWith(N2, /What is the acceleration of the blocks/, /^5\.0 m\/s²$/, /^8\.0 m\/s²$/), 'q');
  ck('trap · tension set equal to the applied force (and taught: tension is less than the pull)',
     qWith(N2, /tension in the string\?$/, /^15 N$/, /^40 N$/) && qWith(FR, /tension in the string\?$/, /^18 N$/, /^45 N$/) &&
     /The tension is less than the pull/.test(B[0]), 'two qs + card');
  ck('trap · pulling the other block keeps a but changes T (old tension offered)',
     qWith(N2, /now acts on the 3\.0 kg/, /5\.0 m\/s² and 25 N/, /5\.0 m\/s² and 15 N/), 'q');
  ck('trap · the g + a sign flipped, and travel read as acceleration',
     qWith(N2, /56 kg/, /^616 N$/, /^482 N$/) && qWith(N2, /70 kg/, /^511 N$/, /^861 N$/) &&
     qWith(FR, /pushed sideways/, /^2\.6/, /^4\.0/), 'three qs');
  ck('trap · a speed is not an acceleration (constant velocity reads mg)',
     qWith(N2, /steady\s+4\.0 m\/s/, /^568 N$/, /^800 N$/), 'q');
  ck('trap · working back from a reading: forgetting to subtract g, and the sign',
     qWith(N2, /reads 504 N/, /1\.4 m\/s² upward/, /1\.4 m\/s² downward/) && qWith(N2, /reads 504 N/, /1\.4/, /^11\.2/), 'q');
  ck('trap · the vertical part of the pull not subtracted from N',
     qWith(N2, /normal force from the floor/, /^113 N$/, /^147 N$/) && qWith(FR, /How big is the friction\?$/, /^58 N$/, /^71 N$/), 'two qs');
  ck('trap · sine and cosine swapped',
     qWith(N2, /normal force from the floor/, /^113/, /^74 N$/) && qWith(FR, /How big is the friction\?$/, /^58/, /^35 N$/) &&
     qWith(FR, /slides up\?$/, /^5\.5/, /^9\.5/), 'three qs');
  ck('trap · friction added instead of subtracted',
     qWith(N2, /kinetic friction on it is 40 N/, /^2\.2/, /^7\.5/) && qWith(FR, /What is their acceleration/, /^5\.6/, /^12 /), 'two qs');
  ck('trap · mass used as weight',
     qWith(FR, /85 N horizontal/, /^0\.22$/, /^2\.1$/) && qWith(FR, /friction on the 3\.0 kg/, /^10 N$/, /^1\.05 N$/) &&
     qWith(LB, /120 g mass/, /^1\.2 N$/, /^0\.12 N$/), 'three qs');
  ck('trap · each block has its own friction (one block’s friction alone offered)',
     qWith(FR, /friction on the 3\.0 kg/, /^10 N$/, /^17 N$/) && qWith(FR, /What is their acceleration/, /^5\.6/, /^6\.9/), 'two qs');
  ck('trap · friction left out of the trailing block’s equation (T too small)',
     qWith(FR, /tension in the string\?$/, /^18 N$/, /^11 N$/), 'q');
  ck('trap · elevator friction: N = m(g + a), so friction grows; ignoring it offered',
     /Friction in an accelerating elevator/.test(B[1]) && qWith(FR, /pushed sideways/, /^2\.6/, /^3\.3/) &&
     qWith(FR, /A puck slides/, /^0\.32$/, /^0\.36$/) && qWith(FR, /DOWNWARD/, /smaller/, /the same/), 'card + three qs');
  ck('trap · friction left pointing UP the slope on the way up',
     /Going up, both arrows point down/.test(B[1]) && qWith(FR, /slides up\?$/, /^5\.5/, /^2\.8/) &&
     qWith(FR, /How far\s+up/, /^3\.3 m$/, /^6\.4 m$/), 'card hint + two qs');
  ck('trap · coming back down, friction flips, so the acceleration is SMALLER',
     qWith(FR, /on the way down\?$/, /^2\.8/, /^5\.5/) && qWith(FR, /reaches the bottom/, /^4\.3/, /^6\.0/), 'two qs');
  ck('trap · v² = 2aΔx: the 2 dropped and the square dropped',
     qWith(FR, /How far\s+up/, /^3\.3/, /^6\.6 m$/) && qWith(FR, /How far\s+up/, /^3\.3/, /^0\.55 m$/) &&
     qWith(LB, /travels 0\.72 m/, /^1\.0/, /^0\.50/), 'two qs');
  ck('μ = f / N at constant velocity, and constant velocity is not zero friction',
     /Constant velocity gives μ directly/.test(B[1]) && qWith(FR, /85 N/, /^0\.22$/, /^0\.00$/), 'card + q');
  ck('the angled pull lowers N and so the friction',
     qWith(FR, /Which\s+box meets less friction/, /pulled upward/, /pulled level/) &&
     qWith(N2, /tilted further/, /decreases/, /increases, because the normal force/), 'two qs');
  ck('the slope of a against F is 1/m',
     /The slope is 1 \/ mass/.test(B[0]) && qWith(N2, /What does the slope of the\s+line stand for/, /1 ÷ the cart’s mass/, /^The cart’s mass$/) &&
     qWith(N2, /What is the cart’s mass/, /^1\.25 kg$/, /^0\.80 kg$/), 'card + two qs');
  ck('g convention named on a card in 2-1 and 2-2 (negative, or 10)',
     [0, 1].every(i => U[i].cards.some(c => /g/.test(c.term) && /−9\.8/.test(c.def) && /10/.test(c.def))), 'cards');

  // ---- the lab, by its teaching ---------------------------------------------
  ck('lab · the hanging mass counts in the total (left-out offered)',
     /Why the hanging mass counts/.test(B[2]) && qWith(LB, /What total mass/, /^0\.80 kg$/, /^0\.75 kg$/) &&
     qWith(LB, /hanging mass be included/, /accelerates along with the cart/), 'card + two qs');
  ck('lab · linearize: a against 1/M, slope = the hanging weight',
     qWith(LB, /straight-line graph/, /1 ÷ total mass/, /Distance against time/) &&
     qWith(LB, /What does the slope of that line/, /hanging weight/, /total mass/) &&
     LB.cards.some(c => /1\/M/.test(c.term) && c.graph) && /slope = F = m_h g/.test(B[2]), 'card + two qs');
  ck('lab · percent difference vs percent error, both formulas on a card',
     LB.cards.some(c => /Percent error and percent difference/.test(c.term) &&
       /\|experimental − actual\| ÷ actual × 100/.test(c.def) && /average of A and B/.test(c.def)) &&
     qWith(LB, /percent DIFFERENCE rather than/, /Two measured values/), 'card + q');
  ck('lab · the Moon: every acceleration is one-sixth, not “nothing changes”',
     qWith(LB, /on the Moon/, /one-sixth as big/, /Nothing would change/), 'q');
  ck('lab · friction’s direction: a low, so the force comes out low',
     qWith(LB, /Friction in the cart’s wheels/, /lower than the hanging weight/, /higher than/) &&
     /makes the measured acceleration too\s+low/.test(B[2].replace(/\s+/g, ' ')), 'card + q');
  ck('lab · do not graph distance against time',
     LB.cards.some(c => /Do not graph distance against time/.test(c.term)), 'card');

  // ---- parent notes ---------------------------------------------------------
  ck('parent notes: sheets read for what they ask; nothing of hers recorded',
     U.every(u => /read for what it asks/.test(u.note)) && /no data yet/.test(LB.note), U.map(u => u.note.slice(0, 80)));
  ck('parent-note flags: FRQ 3 skips (d); friction Q2 picture unseen; 4(f) extra credit; % difference vs printed error formula',
     /problem 3 skips part \(d\)/.test(N2.note) && /\(c\) to \(e\)/.test(N2.note) &&
     /problem 2/.test(FR.note) && /not seen/.test(FR.note) && /4\(f\)/.test(FR.note) && /extra credit/.test(FR.note) &&
     /percent\s+DIFFERENCE/.test(LB.note) && /percent-error formula/.test(LB.note) && /garbled/.test(LB.note), 'notes');

  // ---- a full quiz round on each, and each deck -----------------------------
  for (let i = 0; i < 3; i++) {
    const play = await p.evaluate(async (uid) => {
      quizState = null;
      go('quiz', {unitId: uid, classId: 'physics'});
      let guard = 0;
      while (view === 'quiz' && guard++ < 80) {
        const chips = [...document.querySelectorAll('#screen .ordchip:not([disabled])')];
        if (chips.length) { chips[0].click(); await new Promise(r => setTimeout(r, 4)); continue; }
        const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
        if (opts.length) for (const o of opts) { o.click(); await new Promise(r => setTimeout(r, 4)); }
        await new Promise(r => setTimeout(r, 8));
        const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
        if (next) { next.click(); await new Promise(r => setTimeout(r, 8)); continue; }
        if (!opts.length) break;
      }
      const l = all('log').find(x => x.unitId === uid && x.mode === 'quiz');
      return {logged: !!l, total: l && l.total};
    }, IDS[i]);
    ck(L[i] + ': a full quiz round plays and logs', play.logged && play.total === Math.min(seed.round, U[i].qs.length), play);
  }
  const gr = await p.evaluate((ids) => ids.flatMap(id => DATA.records[id].questions.concat(DATA.records[id].cards)
      .filter(x => x.graph).map(x => { const n = graphNode(x.graph); return n ? n.querySelectorAll('polyline').length : 0; })),
    IDS);
  ck('every graph renders a drawn line', gr.length >= 4 && gr.every(n => n >= 1), gr);
  for (let i = 0; i < 3; i++) {
    const deck = await p.evaluate(async (uid) => {
      cardState = {}; go('cards', {unitId: uid, classId: 'physics'});
      let seen = 0;
      while (cardState.unitId === uid && seen++ < 40) {
        const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
        if (!knew) break;
        knew.click(); await new Promise(r => setTimeout(r, 5));
      }
      return {seen};
    }, IDS[i]);
    ck(L[i] + ': the flashcard deck steps all the way through', deck.seen >= U[i].cards.length, deck);
  }

  // Public repo: no marks or scores of hers anywhere.
  ck('privacy: no score, mark or "she got" anywhere in the shipped records',
     !U.some(u => /she got|\bscored\b|\bout of \d+\b|\d+\s*\/\s*\d+\s*(correct|right|marks|points)|\b\d+(\.\d+)?\s?%/i.test(u.blob)), 'ok');

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0, 500))));
  console.log(`${out.filter(r => r.ok).length}/${out.length}`, out.every(r => r.ok) ? 'ALL PASS' : 'FAILURES',
              '· seeded:', [...new Set(seed.loaded)].join(', '));
  console.log('page errors:', errs.length ? errs.slice(0, 10) : 'none');
  await b.close();
  if (!out.every(r => r.ok) || errs.length) process.exit(1);
})();
