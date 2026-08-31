/* v142 — the physics formula sheet now carries the equations of motion, and
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
  ck('the physics sheet opens and lists equations of motion',
     /Equations of motion/i.test(sheet.heads.join('|')), sheet.heads);
  ck('all four constant-acceleration equations are on it',
     ['v = v₀ + at', 'd = d₀ + v₀t + ½at²', 'v² = v₀² + 2a(d − d₀)', 'd = d₀ + ½(v₀ + v)t']
       .every(e => sheet.eqs.includes(e)),
     sheet.eqs.slice(0, 8));
  ck('it still carries the conversion factors it had before',
     sheet.eqs.some(e => /18 228/.test(e)) && sheet.eqs.some(e => /5280/.test(e)),
     sheet.eqs.filter(e => /ft/.test(e)).slice(0, 4));
  ck('g and its sign rule are stated',
     /9\.80 m\/s²/.test(sheet.txt) && /always positive/i.test(sheet.txt), null);
  ck('the worksheet-vs-textbook notation note is there',
     /Δx/.test(sheet.txt) && /d − d₀/.test(sheet.txt), null);

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
