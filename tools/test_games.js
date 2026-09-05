/* The daily three — one of the "low-hanging fruit" games from the original
   batch (v145 / Wayfinder v124). Same file in both repos. Three questions by
   date as an ordinary round, misses to the Growth Zone, qstats to the real
   units, a door on Today that becomes three squares when done.

   Memory Match, the other game from that batch, was removed in v154 /
   Wayfinder v135 (Chris: "it isn't very helpful") — this file used to test
   it too; those assertions went with the feature. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  await p.evaluate(async () => {
    for (const f of CONTENT_LIBRARY) { try { const j = await (await fetch(f,{cache:'no-store'})).json();
      Object.values(j.records||{}).forEach(r => { if (r.type==='unit') { r.status='approved'; DATA.records[r.id]=r; } }); } catch(e){} }
    saveLocal();
  });

  /* ---------- The daily three ---------- */
  await p.evaluate(() => { go('today'); });
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
