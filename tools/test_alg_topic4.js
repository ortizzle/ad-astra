/* Topic 4 — Rational Functions. All 5 lessons load, shelve in teaching order beside
   Topics 1–3, render flashcards and a full quiz round, and the rational-function graphs
   (drawn as `pts` series, since renderGraph has no rational type) actually draw
   separate branches that never get joined across a vertical asymptote.

   Pins, by their reasoning rather than their current value:
     - classId is 'algeo' (the v136 orphan trap).
     - The shelf ascends 4-1 .. 4-5 on title alone, numbered form on every lesson,
       no `order` anywhere (the v180 mixed-form lesson).
     - Answers are spread across all four slots (the v181 `_balance` bug).
     - No back-reference to a sibling question, no option named by position.
     - Question counts are a MINIMUM, never an exact number.
     - Each lesson's central trap is asserted by its TEACHING, not by question id. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8411;
const FILES = ['alg-topic4-01','alg-topic4-02','alg-topic4-03','alg-topic4-04','alg-topic4-05'];
const NEIGHBOURS = ['alg-topic1-01','alg-topic1-02','alg-topic1-03','alg-topic1-04',
                    'alg-topic2-01','alg-topic2-02','alg-topic2-03','alg-topic2-04',
                    'alg-topic2-05','alg-topic2-06','alg-topic2-07',
                    'alg-topic3-01','alg-topic3-02','alg-topic3-03','alg-topic3-04',
                    'alg-topic3-05','alg-topic3-06','alg-topic3-07'];

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
  ck('all 5 Topic 4 units seeded', seed.length === 5, seed);

  /* Topics 1, 2 and 3 are seeded too, so "Topic 4 is its own shelf" is a claim
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
  ck('Topic 1, 2 and 3 lessons seeded alongside', neighbours >= 17, neighbours);

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
  ck('no structural problems across all 5 units', struct.length === 0, struct);

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

  /* ---- the shelf: one spine, 4-1 .. 4-5 in teaching order, Topics 1–3 intact */
  const shelf = await p.evaluate(() => {
    const sh = shelvesFor('algeo');
    const t4 = sh.shelves.find(s => /^Topic 4/.test(s.name));
    return {
      names: sh.shelves.map(s => s.name),
      t4: t4 ? (t4.lessons || t4.units).map(u => u.title) : null,
      orders: t4 ? (t4.lessons || t4.units).map(u => u.order || 0) : null,
      loose: sh.loose.map(u => u.title)
    };
  });
  ck('Topic 4 is its own shelf, alongside Topics 1, 2 and 3',
     ['1','2','3','4'].every(n => shelf.names.some(s => new RegExp('^Topic ' + n).test(s))), shelf.names);
  ck('nothing from Topic 4 fell out as a loose card',
     !shelf.loose.some(t => /Topic 4/.test(t)), shelf.loose);
  ck('all 5 lessons sit on the Topic 4 shelf', shelf.t4 && shelf.t4.length === 5, shelf.t4);
  ck('every lesson carries the numbered form 4-N',
     shelf.t4 && shelf.t4.every(t => /^Topic 4 · 4-\d /.test(t)), shelf.t4);
  ck('the shelf ascends 4-1 through 4-5 by title alone, with no `order` set',
     shelf.t4 && shelf.t4.map(t => t.match(/4-(\d)/)[1]).join('') === '12345' &&
     shelf.orders.every(o => !o), {t4: shelf.t4, orders: shelf.orders});

  /* ---- rational graphs. renderGraph has no rational series type, so each curve is a
     `pts` series with an off-window point between its branches. Pin that it draws real
     curves, and that a curve with a vertical asymptote comes out as MORE THAN ONE
     polyline (one per branch) — a single polyline would mean the branches were joined
     straight across the asymptote, which is the one way this drawing could lie. */
  const graphs = await p.evaluate(ids => {
    const specs = [];
    ids.forEach(id => {
      const u = DATA.records[id];
      [...u.cards, ...u.questions].forEach(o => { if (o.graph) specs.push({id, oid: o.id, g: o.graph}); });
    });
    const res = specs.map(s => {
      const node = graphNode(s.g);
      document.body.appendChild(node);
      const lines = [...node.querySelectorAll('polyline')];
      const col0 = lines.length ? lines[0].getAttribute('stroke') : null;
      const curveLines = lines.filter(l => l.getAttribute('stroke') === col0);
      const verts = curveLines.reduce((n, el) => n + (el.getAttribute('points') || '').trim().split(/\s+/).filter(Boolean).length, 0);
      const ys = curveLines.flatMap(el => (el.getAttribute('points') || '').trim().split(/\s+/).filter(Boolean).map(pr => +pr.split(',')[1]));
      node.remove();
      return {at: s.id + '/' + s.oid, polylines: lines.length, curvePolylines: curveLines.length, verts,
              spread: ys.length ? Math.max(...ys) - Math.min(...ys) : 0};
    });
    return {count: specs.length, res};
  }, seed);
  ck('Topic 4 carries graphs, in more than one lesson', graphs.count >= 6 &&
     new Set(graphs.res.map(r => r.at.split('/')[0])).size >= 3, graphs.count);
  ck('every graph renders a real curve with real vertical extent',
     graphs.res.every(r => r.verts > 40 && r.spread > 40), graphs.res.filter(r => !(r.verts > 40 && r.spread > 40)));
  ck('the reciprocal-function graph draws its two branches as separate polylines',
     graphs.res.filter(r => /unit-alg-t4-01/.test(r.at)).every(r => r.curvePolylines >= 2), graphs.res.filter(r => /t4-01/.test(r.at)));

  /* ---- each lesson's central trap, asserted by its teaching rather than a question id */
  const teach = await p.evaluate(() => {
    const U = id => DATA.records[id];
    const right = q => q.opts[q.ans];
    const blob = q => [q.q, ...(q.opts||[]), ...(q.steps||[]), (q.ex||{}).main||''].join(' ');
    const t1 = U('unit-alg-t4-01'), t2 = U('unit-alg-t4-02'), t3 = U('unit-alg-t4-03'),
          t4 = U('unit-alg-t4-04'), t5 = U('unit-alg-t4-05');
    return {
      /* 4-1: a decreasing table is not enough — the product must be constant */
      productTest: t1.questions.some(q => /inverse variation/i.test(q.q) && /32/.test(blob(q)) && /48/.test(blob(q))),
      gasTrap:     t1.questions.some(q => /gas left/i.test(q.opts.join(' ')) && !/gas/i.test(right(q))),
      signTrap:    t1.questions.some(q => /x \+ 3\)/.test(q.q) && /Left 3/.test(right(q))),
      /* 4-2: a cancelled factor is a hole, not an asymptote */
      hole:        t2.questions.some(q => /hole/i.test(right(q)) && /asymptote/i.test(right(q))),
      crossHA:     t2.questions.some(q => /cross/i.test(q.q) && /x = −18/.test(right(q))),
      degreeNone:  t2.questions.some(q => /horizontal asymptote/i.test(q.q) && right(q) === 'None'),
      /* 4-3: dividing restricts the divisor's numerator too */
      divDomain:   t3.questions.some(q => /domain/i.test(q.q) && /÷/.test(q.q) && /3/.test(right(q)) && /−5/.test(right(q))),
      termsNot:    t3.cards.some(c => /terms/i.test(c.term) && /factor/i.test(c.def)),
      /* 4-4: restrictions come from the ORIGINAL denominators */
      lostRestr:   t4.questions.some(q => /classmate/i.test(q.q) && /x ≠ −3/.test(right(q))),
      avgSpeed:    t4.questions.some(q => /average speed/i.test(q.q) && right(q) === '48 mph'),
      /* 4-5: extraneous solutions rejected; "no solution" is a real answer; context rejection */
      extraneous:  t5.questions.some(q => /\(x² \+ 5\)/.test(q.q) && right(q) === 'x = −2'),
      noSolution:  t5.questions.some(q => right(q) === 'No solution'),
      context:     t5.questions.some(q => /miles per hour|mph/.test(q.q) && right(q) === '30 mph' && q.opts.some(o => /−9/.test(o))),
      twiceAsFast: t5.cards.some(c => /twice as fast/i.test(c.term)),
      slidesNote:  /slides/i.test((t5.parentNote && t5.parentNote.text) || '') && /slides/i.test(t5.srcName || '')
    };
  });
  Object.entries(teach).forEach(([k, v]) => ck('teaches: ' + k, v, teach));

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
  ck('the algeo reference sheet is reachable from inside a Topic 4 quiz',
     quiz.every(r => r.sawSheet), quiz.map(r => r.sawSheet));

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,400))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
