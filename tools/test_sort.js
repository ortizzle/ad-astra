/* Swipe sort — two buckets, one card at a time. Engine identical in both
   apps; the sets ride on units. Same file in both repos. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    for (const f of CONTENT_LIBRARY) { try { const j = await (await fetch(f,{cache:'no-store'})).json();
      Object.values(j.records||{}).forEach(r => { if (r.type==='unit') { r.status='approved'; DATA.records[r.id]=r; } }); } catch(e){} }
    saveLocal();
    const u = all('unit').find(u => (u.sorts||[]).length);
    return {id: u.id, cls: u.classId, set: u.sorts[0].id, n: u.sorts[0].items.length, a: u.sorts[0].a, b: u.sorts[0].b, title: u.sorts[0].title,
            withSorts: all('unit').filter(u => (u.sorts||[]).length).length};
  });
  ck('seed: at least one unit carries a sort set', seed.withSorts >= 1, seed);

  const door = await p.evaluate(({id, cls}) => {
    const u = DATA.records[id], c = CLASS_BY_ID[cls];
    const onCard = /⇄  Sort — /.test(unitCard(u, c).textContent);
    const ser = seriesOf(u);
    if (ser) go('shelf',{classId: cls, series: ser, open: id}); else go('unit',{classId: cls});
    return {onCard, onScreen: /⇄  Sort — /.test(document.getElementById('screen').textContent)};
  }, seed);
  ck('the Sort door renders on the unit card and reaches the screen', door.onCard && door.onScreen, door);

  const start = await p.evaluate(({id, cls, set}) => {
    sortState = null; go('sort',{unitId:id, classId:cls, sortId:set});
    const sc = document.getElementById('screen');
    return {queue: sortState.queue.length, card: !!sc.querySelector('.sortcard'), buckets: sc.querySelectorAll('.sortbk span').length,
            btns: [...sc.querySelectorAll('.sortbtns .btn')].map(b=>b.textContent), tally: sc.querySelector('.row .v').textContent,
            minH: Math.min(...[...sc.querySelectorAll('.sortbtns .btn, .sortbk span')].map(e=>e.getBoundingClientRect().height))};
  }, seed);
  ck('the screen deals every item, shows one card, two buckets, two 44px tap buttons',
     start.queue===seed.n && start.card && start.buckets===2 && start.btns.length===2 && /0 of/.test(start.tally) && start.minH>=44, start);

  // Right choice by tap: advances, counts, logs in place.
  const right = await p.evaluate(({id, set}) => {
    const u = DATA.records[id], s = u.sorts.find(x=>x.id===set);
    const it = s.items[sortState.queue[0]];
    const btns = [...document.querySelectorAll('#screen .sortbtns .btn')];
    (it.k==='a' ? btns[0] : btns[1]).click();
    const log = all('log').find(l => l.mode==='sort');
    return {done: sortState.done.length, first: sortState.firstRight, queue: sortState.queue.length,
            log: log && {correct: log.correct, total: log.total, xp: log.xp, label: modeLabel(log)}};
  }, seed);
  ck('a right tap lands the card, counts first-time-right, and logs in place',
     right.done===1 && right.first===1 && right.queue===seed.n-1 && right.log && right.log.correct===1 && right.log.xp===3 && right.log.label==='Sort', right);

  // Wrong choice: verdict with why, needs a tap, item goes to the back.
  await p.waitForTimeout(500);
  const wrong = await p.evaluate(({id, set}) => {
    const u = DATA.records[id], s = u.sorts.find(x=>x.id===set);
    const idx = sortState.queue[0], it = s.items[idx];
    const btns = [...document.querySelectorAll('#screen .sortbtns .btn')];
    (it.k==='a' ? btns[1] : btns[0]).click();
    const sc = document.getElementById('screen');
    const verdict = !!sortState.verdict, why = !!sc.querySelector('.sortcard .why'), was = (sc.querySelector('.sortcard .was')||{}).textContent||'';
    const gotIt = [...sc.querySelectorAll('.btn')].find(b=>/Got it/.test(b.textContent));
    const back = sortState.queue[sortState.queue.length-1] === idx;
    const noBtns = !sc.querySelector('.sortbtns');
    if (gotIt) gotIt.click();
    return {verdict, why, was, hasGotIt: !!gotIt, back, noBtns, cleared: !sortState.verdict, first: sortState.firstRight,
            expectLabel: it.k==='a' ? s.a : s.b};
  }, seed);
  ck('a wrong tap shows where it belonged and why, waits for a tap, sends it to the back',
     wrong.verdict && wrong.why && wrong.was.includes(wrong.expectLabel) && wrong.hasGotIt && wrong.back && wrong.noBtns && wrong.cleared && wrong.first===1, wrong);

  // Swipe by pointer: a long drag right chooses b, a short one snaps back.
  const swipe = await p.evaluate(async ({id, set}) => {
    const u = DATA.records[id], s = u.sorts.find(x=>x.id===set);
    const fire = (el, type, x) => el.dispatchEvent(new PointerEvent(type, {clientX:x, clientY:300, pointerId:1, bubbles:true, isPrimary:true}));
    // short drag: nothing happens
    let card = document.querySelector('#screen .sortcard'); const before = sortState.done.length;
    fire(card,'pointerdown',100); fire(card,'pointermove',130); fire(card,'pointerup',130);
    const shortNoop = sortState.done.length === before && !sortState.verdict;
    // long drag in the correct direction for this card
    await new Promise(r=>setTimeout(r,20));
    card = document.querySelector('#screen .sortcard');
    const it = s.items[sortState.queue[0]]; const dir = it.k==='b' ? 1 : -1;
    fire(card,'pointerdown',200); fire(card,'pointermove',200+dir*120); fire(card,'pointerup',200+dir*120);
    return {shortNoop, landed: sortState.done.length === before+1, first: sortState.firstRight};
  }, seed);
  ck('a short drag snaps back; a long drag sorts the card', swipe.shortNoop && swipe.landed && swipe.first===2, swipe);

  // Finish the pile correctly; the one wrong earlier stays not-first-time.
  await p.waitForTimeout(500);
  const fin = await p.evaluate(async ({id, set, n}) => {
    const u = DATA.records[id], s = u.sorts.find(x=>x.id===set);
    let guard = 0;
    while (sortState.queue.length && guard++ < 40) {
      if (sortState.verdict) { [...document.querySelectorAll('#screen .btn')].find(b=>/Got it/.test(b.textContent)).click(); continue; }
      const it = s.items[sortState.queue[0]];
      const btns = [...document.querySelectorAll('#screen .sortbtns .btn')];
      if (!btns.length) { await new Promise(r=>setTimeout(r,50)); continue; }
      (it.k==='a' ? btns[0] : btns[1]).click();
      await new Promise(r=>setTimeout(r,470));
    }
    const sc = document.getElementById('screen'); const txt = sc.textContent;
    const logs = all('log').filter(l => l.mode==='sort');
    return {queue: sortState.queue.length, first: sortState.firstRight, logs: logs.length, xp: logs[0].xp, correct: logs[0].correct,
            doneCard: /Every card in its place/.test(txt), mentionsHard: /came back around/.test(txt), again: /Again · new order/.test(txt)};
  }, seed);
  ck('finishing: all sorted, first-time count is n-1, ONE log at (n-1)×3 XP, the returned card named',
     fin.queue===0 && fin.first===seed.n-1 && fin.logs===1 && fin.correct===seed.n-1 && fin.xp===(seed.n-1)*3 && fin.doneCard && fin.mentionsHard && fin.again, fin);

  const again = await p.evaluate(() => {
    const before = sortState.queue.slice(); const salt = sortState.salt;
    [...document.querySelectorAll('#screen .btn')].find(b=>/Again/.test(b.textContent)).click();
    return {fresh: sortState.salt === salt+1 && sortState.done.length===0 && sortState.queue.length>0,
            reordered: sortState.queue.join() !== before.join(), card: !!document.querySelector('#screen .sortcard')};
  });
  ck('Again re-deals the pile in a new order', again.fresh && again.reordered && again.card, again);

  // Review screen shows the set; unitDelta notices a sorts change.
  const review = await p.evaluate(({id, cls, title, n}) => {
    ctx.fromParent = true; go('reviewunit',{unitId:id, classId:cls});
    const txt = document.getElementById('screen').textContent;
    const u = DATA.records[id];
    const changed = unitDelta({...u, sorts: []}, u);
    return {shows: txt.includes('Sort sets') && txt.includes(title), rows: (txt.match(/Left: /g)||[]).length,
            delta: changed && changed.meta.includes('sorts')};
  }, seed);
  ck('the review queue shows the set with every item and bucket, and a sorts change flags a re-approval', review.shows && review.rows>=1 && review.delta, review);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,340))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
