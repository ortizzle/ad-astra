/* Topic 3 — Polynomial Functions. All 7 lessons load, shelve in teaching order,
   render flashcards and a full quiz round, and the new `poly` graph series type
   actually draws a curve.

   Pins, by their reasoning rather than their current value:
     - classId is 'algeo' (the v136 orphan trap: a wrong classId shelves nowhere
       and throws nothing at all).
     - The shelf ascends 3-1 .. 3-7 on title alone, with no `order` anywhere —
       a mixed numbering form inside one shelf is what the v180 Biology work had
       to unpick, so the numbered form is asserted on every lesson.
     - Answers are spread across all four slots (the v181 `_balance` bug: the
       function had been ported without its call site and shipped all-answer-A).
     - No stem back-references a sibling question, and no option is named by
       position — both invisible on the page and both fatal under the v64
       render-time option shuffle.
     - Question counts are a MINIMUM, never an exact number: a unit should be
       free to grow when her work shows a gap (the Wayfinder v165 lesson). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8101;
const FILES = ['alg-topic3-01','alg-topic3-02','alg-topic3-03','alg-topic3-04',
               'alg-topic3-05','alg-topic3-06','alg-topic3-07'];
const NEIGHBOURS = ['alg-topic1-01','alg-topic1-02','alg-topic1-03','alg-topic1-04',
                    'alg-topic2-01','alg-topic2-02','alg-topic2-03','alg-topic2-04',
                    'alg-topic2-05','alg-topic2-06','alg-topic2-07'];

(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.addScriptTag({path: __dirname + '/seed.js'});
  await p.waitForTimeout(300);

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async (files) => {
    const ids = [];
    for (const f of files) {
      const res = await fetch(`./content/${f}.json`, {cache:'no-store'});
      const j = await res.json();
      const u = Object.values(j.records)[0];
      u.status = 'approved'; u.updatedAt = Date.now() - 1000;
      DATA.records[u.id] = u; ids.push(u.id);
    }
    saveLocal();
    return ids;
  }, FILES);
  ck('all 7 Topic 3 units seeded', seed.length === 7, seed);

  /* Topics 1 and 2 are seeded too, so "Topic 3 is its own shelf" is a claim
     about coexistence rather than a claim about an empty subject screen. */
  const neighbours = await p.evaluate(async files => {
    let n = 0;
    for (const f of files) {
      try {
        const j = await (await fetch(`./content/${f}.json`, {cache:'no-store'})).json();
        const u = Object.values(j.records)[0];
        u.status = 'approved'; u.updatedAt = Date.now() - 2000;
        DATA.records[u.id] = u; n++;
      } catch (e) { /* a file that is not on disk simply is not seeded */ }
    }
    saveLocal();
    return n;
  }, NEIGHBOURS);
  ck('Topic 1 and Topic 2 lessons seeded alongside', neighbours >= 10, neighbours);

  /* ---- the orphan trap: a classId CLASS_BY_ID does not know fails silently */
  const cls = await p.evaluate(ids => ids.map(id => ({
    id, classId: DATA.records[id].classId,
    known: !!CLASS_BY_ID[DATA.records[id].classId]
  })), seed);
  ck('every unit carries a classId the app recognises',
     cls.every(c => c.classId === 'algeo' && c.known), cls);

  /* ---- structure, against the live schema rather than the authoring script */
  const struct = await p.evaluate(ids => {
    const bad = [];
    ids.forEach(id => {
      const u = DATA.records[id];
      if (!u.cards.length) bad.push(id + ': no cards');
      if (u.questions.length < 18) bad.push(id + ': under 18 questions (' + u.questions.length + ')');
      if (u.status !== 'approved') bad.push(id + ': seeded wrong');
      u.questions.forEach(q => {
        if (q.kind === 'slider' || q.kind === 'spell') return;  // one option by contract
        if (q.opts.length !== 4) bad.push(id + '/' + q.id + ': opts != 4');
        if (new Set(q.opts).size !== 4) bad.push(id + '/' + q.id + ': duplicate options');
        if (!(q.ans >= 0 && q.ans <= 3)) bad.push(id + '/' + q.id + ': ans out of range');
        if (!Array.isArray(q.steps) || q.steps.length < 3) bad.push(id + '/' + q.id + ': steps < 3');
        if (!/^\*\*/.test(q.ex && q.ex.main || '')) bad.push(id + '/' + q.id + ': ex.main not bold-first');
      });
    });
    return bad;
  }, seed);
  ck('no structural problems across all 7 units', struct.length === 0, struct);

  /* ---- the _balance bug, pinned so it cannot come back */
  const slots = await p.evaluate(ids => {
    const t = {0:0,1:0,2:0,3:0};
    ids.forEach(id => DATA.records[id].questions.forEach(q => {
      if (q.kind === 'slider' || q.kind === 'spell') return;
      t[q.ans] = (t[q.ans] || 0) + 1;
    }));
    return t;
  }, seed);
  ck('authored answers use all four slots', [0,1,2,3].every(i => slots[i] > 5), slots);

  /* ---- standalone rule: no back-reference, no option named by position */
  const lang = await p.evaluate(ids => {
    const bad = [];
    /* The documented failure is a stem that OPENS on a neighbour's scenario —
       "The same student…", "For that same data…", "That same stone…". A bare
       /the same/ also matches "point the same way", which means "as each
       other" inside its own stem and is perfectly standalone, so anchor it. */
    const BACK = /^(the same|that same|for (that|the) same|using the same)\b/i;
    const BACK2 = /\b(that same|as (above|before)|in the previous|from the previous)\b/i;
    const POS  = /\b(all|none) of the above\b|\boptions? [a-d]\b|\b(first|second|third|last) (option|choice|answer)\b/i;
    ids.forEach(id => DATA.records[id].questions.forEach(q => {
      const stem = (q.q || '').trim();
      if (BACK.test(stem) || BACK2.test(stem)) bad.push(id + '/' + q.id + ': back-reference in stem');
      const blob = [q.q, ...(q.opts||[]), ...(q.steps||[]), (q.ex||{}).main||''].join(' ');
      if (POS.test(blob)) bad.push(id + '/' + q.id + ': positional reference');
      if (/the graph shown/i.test(q.q) && !q.graph) bad.push(id + '/' + q.id + ': names a graph it does not carry');
    }));
    return bad;
  }, seed);
  ck('no back-references, no positional references, no phantom graphs', lang.length === 0, lang);

  /* ---- the shelf: one spine, 3-1 .. 3-7 in teaching order, Topics 1 and 2 intact */
  const shelf = await p.evaluate(() => {
    const sh = shelvesFor('algeo');
    const t3 = sh.shelves.find(s => /^Topic 3/.test(s.name));
    return {
      names: sh.shelves.map(s => s.name),
      t3: t3 ? (t3.lessons || t3.units).map(u => u.title) : null,
      orders: t3 ? (t3.lessons || t3.units).map(u => u.order || 0) : null,
      loose: sh.loose.map(u => u.title)
    };
  });
  ck('Topic 3 is its own shelf, alongside Topics 1 and 2',
     shelf.names.some(n => /^Topic 3/.test(n)) &&
     shelf.names.some(n => /^Topic 1/.test(n)) &&
     shelf.names.some(n => /^Topic 2/.test(n)), shelf.names);
  ck('nothing from Topic 3 fell out as a loose card',
     !shelf.loose.some(t => /Topic 3/.test(t)), shelf.loose);
  ck('all 7 lessons sit on the Topic 3 shelf', shelf.t3 && shelf.t3.length === 7, shelf.t3);
  ck('every lesson carries the numbered form 3-N',
     shelf.t3 && shelf.t3.every(t => /^Topic 3 · 3-\d/.test(t)), shelf.t3);
  ck('the shelf ascends 3-1 through 3-7 by title alone, with no `order` set',
     shelf.t3 && shelf.t3.map(t => t.match(/3-(\d)/)[1]).join('') === '1234567' &&
     shelf.orders.every(o => !o), {t3: shelf.t3, orders: shelf.orders});

  /* ---- the `poly` series type: it must actually draw a curve, not an empty path */
  const graphs = await p.evaluate(ids => {
    let polySpecs = 0;
    ids.forEach(id => {
      const u = DATA.records[id];
      const all = [...u.cards, ...u.questions];
      all.forEach(o => { if (o.graph && (o.graph.series||[]).some(s => s.type === 'poly')) polySpecs++; });
    });
    // render one for real
    const u = DATA.records[ids[0]];
    const spec = [...u.cards, ...u.questions].find(o => o.graph && (o.graph.series||[]).some(s => s.type === 'poly'));
    if (!spec) return {polySpecs, drawn: null};
    const node = graphNode(spec.graph);
    document.body.appendChild(node);
    /* renderGraph draws a series as a <polyline points=...>, NOT a <path d=...>.
       The only <path> elements in the SVG are the two axis arrowheads, so a
       probe that counts path commands reports 2 on a perfectly good curve and
       looks exactly like a rendering bug. Count the polyline vertices. */
    const verts = [...node.querySelectorAll('polyline')]
      .reduce((n, el) => n + (el.getAttribute('points') || '').trim().split(/\s+/).filter(Boolean).length, 0);
    const ys = [...node.querySelectorAll('polyline')]
      .flatMap(el => (el.getAttribute('points') || '').trim().split(/\s+/).filter(Boolean).map(pr => +pr.split(',')[1]));
    node.remove();
    return {polySpecs, drawn: verts, spread: ys.length ? Math.max(...ys) - Math.min(...ys) : 0};
  }, seed);
  ck('the poly graph type is actually used by Topic 3 content', graphs.polySpecs > 0, graphs);
  ck('a poly spec renders a real curve with real vertical extent',
     graphs.drawn > 50 && graphs.spread > 20, graphs);

  /* ---- every deck walks to the end */
  const cardsWalk = await p.evaluate(async ids => {
    const results = [];
    for (const id of ids) {
      ctx.classId = 'algeo';
      go('cards', {unitId:id, classId:'algeo'});
      let steps = 0;
      while (cardState.unitId === id && steps++ < 80) {
        const knowBtn = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
        if (!knowBtn) break;
        knowBtn.click();
        await new Promise(r => setTimeout(r, 5));
      }
      results.push({id, steps});
    }
    return results;
  }, seed);
  ck('every lesson\'s flashcard deck completes cleanly',
     cardsWalk.every(r => r.steps > 0 && r.steps < 80), cardsWalk);

  /* ---- a full quiz round on every lesson, with the algeo Sheet reachable inside it */
  const quiz = await p.evaluate(async ids => {
    const res = [];
    for (const id of ids) {
      go('quiz', {unitId:id, classId:'algeo'});
      let guard = 0, sawSheet = false;
      while (view === 'quiz' && guard++ < 30) {
        if (!sawSheet) sawSheet = [...document.querySelectorAll('#screen .tool')].some(t => /Sheet/.test(t.textContent));
        const opts = [...document.querySelectorAll('#screen .opt')];
        if (!opts.length) break;
        opts[0].click();
        await new Promise(r => setTimeout(r, 12));
        const next = document.querySelector('#screen .btn-primary, #screen .explain .go-on');
        if (next) next.click();
        await new Promise(r => setTimeout(r, 12));
      }
      res.push({id, logged: all('log').some(l => l.unitId === id), sawSheet});
    }
    return res;
  }, seed);
  ck('a full quiz round on every lesson completes and logs',
     quiz.every(r => r.logged), quiz);
  ck('the algeo reference sheet is reachable from inside a Topic 3 quiz',
     quiz.every(r => r.sawSheet), quiz.map(r => r.sawSheet));

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,400))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
