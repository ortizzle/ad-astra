/* v143 — the physics reference sheet is the teacher's own Equations sheet,
   transcribed in her notation and covering the whole year; and
   the textbook's Describing Motion unit shelves with the other Kinematics 1
   parts and plays end to end. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8142;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  // ---- the reference sheet -------------------------------------------------
  const sheet = await p.evaluate(() => {
    openSheet('physics');
    const box = document.querySelector('.modal, #modal, [class*=modal]');
    const txt = box ? box.textContent : '';
    const heads = [...document.querySelectorAll('.eyebrow')].map(x => x.textContent);
    const eqs = [...document.querySelectorAll('.frow .eq')].map(x => x.textContent);
    return {txt, heads, eqs};
  });
  ck('the physics sheet opens and carries the teacher\'s own section headings',
     ['General','Kinematics',"Newton's Laws",'Work and Energy','Impulse and Momentum',
      'Waves and Light','Electric Circuits','Physical Constants']
       .every(h => sheet.heads.includes(h)), sheet.heads);
  ck('all five of her kinematics equations are on it, in her notation',
     ['a = (v_f \u2212 v_i) / t',
      '\u0394x = v_i t + \u00bdt(v_f \u2212 v_i)',
      '\u0394x = ((v_i + v_f) / 2) t',
      '\u0394x = v_i t + \u00bdat\u00b2',
      '\u0394x = (v_f\u00b2 \u2212 v_i\u00b2) / 2a']
       .every(e => sheet.eqs.includes(e)),
     sheet.eqs.slice(0, 10));
  ck('the later units are there too, not just kinematics',
     ['F_net = ma', 'KE = \u00bdmv\u00b2', 'p = mv', 'v = f\u03bb', '\u0394V = IR']
       .every(e => sheet.eqs.includes(e)),
     sheet.eqs.length);
  ck('it still carries the conversion factors it had before',
     sheet.eqs.some(e => /18 228/.test(e)) && sheet.eqs.some(e => /5280/.test(e)),
     sheet.eqs.filter(e => /ft/.test(e)).slice(0, 4));
  ck('her sheet\'s NEGATIVE g is what is printed, not the textbook\'s +9.80',
     sheet.eqs.some(e => /g = \u22129\.8 m\/s\u00b2/.test(e)) && !/9\.80 m\/s\u00b2/.test(sheet.txt),
     sheet.eqs.filter(e => /9\.8/.test(e)));
  ck('the three-notation note is there, and it names the g conflict',
     /\u0394x/.test(sheet.txt) && /d \u2212 d\u2080/.test(sheet.txt) &&
     /sign of g/i.test(sheet.txt), null);
  ck('the textbook blocks are labelled as the textbook\'s',
     sheet.heads.some(h => /from the textbook/i.test(h)), sheet.heads);

  // ---- the unit ------------------------------------------------------------
  const seed = await p.evaluate(async () => {
    const j = await (await fetch('./content/phys-ch3-describing-motion.json', {cache:'no-store'})).json();
    const u = Object.values(j.records)[0];
    u.status = 'approved'; u.updatedAt = Date.now() - 1000;
    DATA.records[u.id] = u;
    // Seed a sibling so the Kinematics 1 shelf has more than one part.
    const j2 = await (await fetch('./content/phys-kinematics-equations.json', {cache:'no-store'})).json();
    const u2 = Object.values(j2.records)[0];
    u2.status = 'approved'; u2.updatedAt = Date.now() - 1000;
    DATA.records[u2.id] = u2;
    saveLocal();
    return {cards: u.cards.length, questions: u.questions.length, classId: u.classId,
            eqCards: u.cards.filter(c => c.eq).length,
            order: u.questions.filter(q => q.kind === 'order').length,
            ansSpread: [0,1,2,3].map(i => u.questions.filter(q => q.kind !== 'order' && q.ans === i).length)};
  });
  ck('unit seeds: 20 cards, 15 questions, classId physics',
     seed.cards === 20 && seed.questions === 15 && seed.classId === 'physics', seed);
  ck('formulas ride in eq fields, and there is a put-in-order question',
     seed.eqCards >= 4 && seed.order === 1, seed);
  ck('correct answers are spread across all four positions',
     seed.ansSpread.every(n => n > 0), seed.ansSpread);

  // It shelves with the other Kinematics 1 parts.
  const shelf = await p.evaluate(() => {
    go('shelf', {classId:'physics', series:'Kinematics 1', open:'unit-phys-ch3'});
    const titles = [...document.querySelectorAll('#screen .stop .t')].map(x => x.textContent);
    const oc = document.getElementById('shelfopen');
    return {titles, opened: oc ? oc.textContent.slice(0, 90) : null};
  });
  ck('it sits on the Kinematics 1 shelf alongside the other parts',
     shelf.titles.length >= 2 && shelf.titles.some(t => /Describing Motion/.test(t)), shelf.titles);
  ck('the opened card is Describing Motion', /Describing Motion/.test(shelf.opened||''), shelf.opened);

  // A full quiz round, and the sheet is reachable from inside it.
  const quiz = await p.evaluate(async () => {
    quizState = null;
    go('quiz', {unitId:'unit-phys-ch3', classId:'physics'});
    const hasSheet = !!document.querySelector('#screen .tools') &&
                     /Sheet/.test(document.querySelector('#screen .tools').textContent);
    let guard = 0;
    while (view === 'quiz' && guard++ < 30) {
      const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
      if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,4)); }
      await new Promise(r=>setTimeout(r,8));
      const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if (next) { next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
      if (!opts.length) break;
    }
    return {hasSheet, logged: all('log').some(l => l.unitId === 'unit-phys-ch3')};
  });
  ck('the Sheet tool is reachable from inside a physics quiz', quiz.hasSheet, quiz);
  ck('a full quiz round completes and logs', quiz.logged, quiz);

  const cards = await p.evaluate(async () => {
    go('cards', {unitId:'unit-phys-ch3', classId:'physics'});
    let seen = 0, guard = 0;
    while (view === 'cards' && guard++ < 50) {
      const nx = document.querySelector('#screen .btn-primary');
      if (!nx) break;
      nx.click(); seen++;
      await new Promise(r => setTimeout(r, 6));
    }
    return seen;
  });
  ck('the 20-card deck steps through cleanly', cards >= 15, cards);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
