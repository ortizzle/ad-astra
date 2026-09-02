/* Memory match and the daily three — the first two of the "low-hanging fruit"
   games. Both are engine, identical in both apps; same file in both repos.
   Match: pairs on any deck, one log updated in place, wrong flips cost
   nothing. Daily: three questions by date as an ordinary round, misses to the
   Growth Zone, qstats to the real units, a door on Today that becomes three
   squares when done. */
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
    const big = all('unit').find(u => matchCards(u).length >= 10 && u.questions.length >= 3 && !u.own && !u.guide && u.classId!=='__all__');
    const small = all('unit').find(u => matchCards(u).length < 4);
    return {big: big && big.id, bigCls: big && big.classId, small: small && small.id, subjects: new Set(all('unit').map(u=>u.classId)).size};
  });
  ck('seed: a big deck and a small one exist', !!seed.big, seed);

  /* ---------- Match ---------- */
  /* unitCard() is the one render site for the door — the loose list and the
     opened shelf card both go through it. Check the card itself, then the
     screen a real tap reaches (the shelf's opened card where the unit shelves,
     else the subject screen). */
  const doors = await p.evaluate(({big, small, bigCls}) => {
    const u = DATA.records[big], c = CLASS_BY_ID[bigCls];
    const onCard = /Match — pair the cards/.test(unitCard(u, c).textContent);
    const ser = seriesOf(u);
    if (ser) go('shelf',{classId: bigCls, series: ser, open: big}); else go('unit',{classId: bigCls});
    const onScreen = /Match — pair the cards/.test(document.getElementById('screen').textContent);
    let onSmall = null;
    if (small) { const su = DATA.records[small]; onSmall = /Match — pair the cards/.test(unitCard(su, CLASS_BY_ID[su.classId] || c).textContent); }
    return {onCard, onScreen, onSmall, ser};
  }, seed);
  ck('the Match door renders on a deck with enough cards, and reaches the screen', doors.onCard && doors.onScreen, doors);
  if (doors.onSmall !== null) ck('a deck with too few matchable cards gets no Match door', doors.onSmall === false, doors);

  const grid = await p.evaluate(({big, bigCls}) => {
    matchState = null; go('match',{unitId: big, classId: bigCls});
    const tiles = [...document.querySelectorAll('#screen .mt')];
    return {n: tiles.length, faceDown: tiles.filter(t => t.querySelector('.pip')).length,
            minH: Math.min(...tiles.map(t => t.getBoundingClientRect().height)),
            pairs: matchState.pairs.length, tally: document.querySelector('#screen .row .v').textContent};
  }, seed);
  ck('the grid deals 6 pairs as 12 face-down tiles, every one at least 44px',
     grid.n === 12 && grid.faceDown === 12 && grid.pairs === 6 && grid.minH >= 44, grid);

  const wrong = await p.evaluate(async () => {
    const st = matchState;
    const i = 0, j = st.tiles.findIndex((t,k) => k!==0 && t.id !== st.tiles[0].id);
    const tiles = () => [...document.querySelectorAll('#screen .mt')];
    tiles()[i].click(); await new Promise(r=>setTimeout(r,10));
    tiles()[j].click(); await new Promise(r=>setTimeout(r,10));
    const upDuring = document.querySelectorAll('#screen .mt.up').length;
    /* No timer: the pair stays up until her next tap. Wait well past the old
       750ms and it must still be readable. */
    await new Promise(r=>setTimeout(r,1200));
    const stillUp = document.querySelectorAll('#screen .mt.up').length;
    const hint = /tap any tile to carry on/i.test(document.getElementById('screen').textContent);
    // tapping a fresh third tile turns the pair back and brings that tile up in one tap
    const k = st.tiles.findIndex((t,idx) => idx!==i && idx!==j);
    tiles()[k].click(); await new Promise(r=>setTimeout(r,10));
    const afterThird = document.querySelectorAll('#screen .mt.up').length;
    // tapping the lone up tile does nothing; tap it again after a wrong pair clears both
    tiles()[k].click(); await new Promise(r=>setTimeout(r,10));
    const lone = st.up.length;
    st.up = []; st.pending = false; render();
    return {upDuring, stillUp, hint, afterThird, lone, found: st.found.length,
            logged: all('log').some(l => l.mode==='match'), flips: st.flips};
  });
  ck('a wrong pair stays up until her next tap, which turns it back and flips the new tile; nothing logged',
     wrong.upDuring===2 && wrong.stillUp===2 && wrong.hint && wrong.afterThird===1 && wrong.lone===1 && wrong.found===0 && !wrong.logged && wrong.flips===1, wrong);

  const right = await p.evaluate(async () => {
    const st = matchState;
    const i = 0, j = st.tiles.findIndex((t,k) => k!==0 && t.id === st.tiles[0].id && t.side !== st.tiles[0].side);
    const tiles = () => [...document.querySelectorAll('#screen .mt')];
    tiles()[i].click(); await new Promise(r=>setTimeout(r,10));
    tiles()[j].click(); await new Promise(r=>setTimeout(r,10));
    const log = all('log').find(l => l.mode==='match');
    return {done: document.querySelectorAll('#screen .mt.done').length, found: st.found.length,
            log: log && {correct: log.correct, total: log.total, xp: log.xp, id: log.id}, tally: document.querySelector('#screen .row .v').textContent};
  });
  ck('a right pair stays up as done and the match log is written in place',
     right.done===2 && right.found===1 && right.log && right.log.correct===1 && right.log.total===6 && right.log.xp===4 && /1 of 6/.test(right.tally), right);

  const finished = await p.evaluate(async () => {
    const st = matchState; const firstLog = all('log').find(l => l.mode==='match').id;
    while (st.found.length < st.pairs.length) {
      const id = st.tiles.find(t => !st.found.includes(t.id)).id;
      const [a, c] = st.tiles.map((t,k)=>({t,k})).filter(x => x.t.id===id).map(x=>x.k);
      const tiles = () => [...document.querySelectorAll('#screen .mt')];
      tiles()[a].click(); await new Promise(r=>setTimeout(r,8));
      tiles()[c].click(); await new Promise(r=>setTimeout(r,8));
    }
    const logs = all('log').filter(l => l.mode==='match');
    const txt = document.getElementById('screen').textContent;
    return {logs: logs.length, sameId: logs[0].id === firstLog, xp: logs[0].xp, doneCard: /That's every pair/.test(txt),
            again: /Play again/.test(txt), quiz: /Take the quiz/.test(txt), label: modeLabel(logs[0])};
  });
  ck('finishing keeps ONE log (updated in place), 24 XP, and offers again / the quiz',
     finished.logs===1 && finished.sameId && finished.xp===24 && finished.doneCard && finished.again && finished.quiz && finished.label==='Match', finished);

  const again = await p.evaluate(async () => {
    const before = matchState.pairs.map(c=>c.id).join(',');
    const label = [...document.querySelectorAll('#screen .btn')].find(b=>/Play again/.test(b.textContent)).textContent;
    [...document.querySelectorAll('#screen .btn')].find(b=>/Play again/.test(b.textContent)).click();
    await new Promise(r=>setTimeout(r,10));
    return {fresh: matchState.pairs.map(c=>c.id).join(',') !== before, label, found: matchState.found.length, tiles: document.querySelectorAll('#screen .mt').length};
  });
  ck('Play again on a deck of ten+ promises and deals a fresh six', /fresh six/.test(again.label) && again.fresh && again.found===0 && again.tiles===12, again);

  /* ---------- The daily three ---------- */
  await p.evaluate(() => { matchState = null; go('today'); });
  const door = await p.evaluate(() => {
    const txt = document.getElementById('screen').textContent;
    const u = buildDailyUnit(AZ.today());
    const u2 = buildDailyUnit(AZ.today());
    const cids = new Set(u.questions.map(q => q._srcClass));
    return {door: /The daily three/.test(txt) && !/done/.test(txt.match(/The daily three[^]*?(done|corner|question)/)?.[1]||''),
            n: u.questions.length, subjects: cids.size, same: u.questions.map(q=>q.id).join() === u2.questions.map(q=>q.id).join(),
            tomorrowDiffers: buildDailyUnit(AZ.shift(AZ.today(),1)).questions.map(q=>q.id).join() !== u.questions.map(q=>q.id).join()};
  });
  ck('Today offers the door; the three come from three subjects, same all day, different tomorrow',
     door.door && door.n===3 && door.subjects===3 && door.same && door.tomorrowDiffers, door);

  const played = await p.evaluate(async () => {
    buildDailyUnit(AZ.today());
    const first = dailyUnit.questions[0];
    quizState = null; go('quiz',{unitId:'__daily__', classId:'__all__'});
    const chk = view === 'quiz';   // no check-in in the way
    let guard = 0, missedOne = false;
    while (view === 'quiz' && guard++ < 20) {
      const u = unitFor('__daily__'); const q = u.questions[quizState.order[quizState.i]];
      const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
      if (opts.length) {
        const want = String(q.opts[q.ans]).trim();
        const rightB = opts.find(o => o.textContent.replace(/^[A-D]\s*/,'').trim() === want) || opts[0];
        const wrongB = opts.find(o => o !== rightB) || opts[0];
        // miss the first question on purpose, get the rest right
        const pick = (!missedOne && q.id === first.id) ? (missedOne = true, wrongB) : rightB;
        pick.click(); await new Promise(r=>setTimeout(r,6));
      }
      const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if (next) { next.click(); await new Promise(r=>setTimeout(r,6)); continue; }
      if (!opts.length) break;
    }
    const modal = document.querySelector('.modal-box');
    const mtxt = modal ? modal.textContent : '';
    const squares = modal ? modal.querySelectorAll('.dsq.big i').length : 0;
    const share = modal && [...modal.querySelectorAll('.btn')].some(b=>/Share today/.test(b.textContent));
    const log = all('log').find(l => l.unitId==='__daily__');
    const miss = all('miss').find(m => m.unitId===first._srcUnit && m.qid===first._srcQid);
    const qs = DATA.records['qstat_'+first._srcUnit+'_'+first._srcQid];
    return {chk, log: log && {correct: log.correct, total: log.total, xp: log.xp, label: modeLabel(log)}, squares, share,
            missOnRealUnit: !!miss && miss.classId === first._srcClass, qstatOnRealUnit: !!qs && qs.attempts>=1};
  });
  ck('the round skips the check-in, logs as the daily three, 2 of 3', played.chk && played.log && played.log.correct===2 && played.log.total===3 && played.log.label==='The daily three', played);
  ck('2 of 3 earns per-question XP only — 20 — with no completion bonus under 80%', played.log && played.log.xp===20, played.log);
  ck('the miss lands on its REAL unit and subject, and the qstat credits it', played.missOnRealUnit && played.qstatOnRealUnit, played);
  ck('the results modal shows three squares and a share button', played.squares===3 && played.share, played);

  const after = await p.evaluate(() => {
    const m = document.querySelector('.modal-overlay'); if (m) m.remove();
    quizState = null; go('today');
    const sc = document.getElementById('screen');
    const done = sc.querySelector('.card.dailydone');
    return {doneCard: !!done, squares: done ? done.querySelectorAll('.dsq i').length : 0,
            doorGone: ![...sc.querySelectorAll('.cardbtn')].some(b=>/The daily three/.test(b.textContent)),
            shareText: dailyShareText()};
  });
  ck('back on Today the door is the done card with three squares, and the door is gone',
     after.doneCard && after.squares===3 && after.doorGone, after);
  ck('the share line says done and carries no score', /✦✦✦ .* · The daily three · .* · done$/.test(after.shareText) && !/\d+ ?%|of 3/.test(after.shareText), after.shareText);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,340))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
