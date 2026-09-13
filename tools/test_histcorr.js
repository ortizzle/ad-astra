/* v183 — the History test-correction session on 9/15, and the History student
   hours row the planner never had. Two separate facts: the standing weekly slot
   (STUDENT_HOURS, class-wide) and the one dated commitment (CAL.events).
   Also asserts the thing that must NOT be there: no score, anywhere. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  // 9/15/2026 is a Tuesday and a school day.
  const day = await p.evaluate(() => ({
    wd: AZ.weekday('2026-09-15'), closed: closedToday('2026-09-15'),
    ev: eventsOn('2026-09-15').map(e => ({name:e.name, kind:e.kind, cid:e.classId, note:e.note}))
  }));
  ck('9/15 is a Tuesday', day.wd === 2, day.wd);
  ck('9/15 is a school day', !day.closed, day.closed);
  ck('the correction session lands on 9/15', day.ev.some(e => /test corrections/i.test(e.name)), day.ev);
  ck('it carries its subject so the row is tappable and wears History',
     day.ev.some(e => e.cid === 'history'), day.ev);

  // The standing hours row, which never existed before.
  const hrs = await p.evaluate(() => hoursForAll('history'));
  ck('History 8 now has a student-hours slot', hrs.length === 1, hrs);
  ck('it is Tuesdays, 3:40-4:30, matching the note', hrs[0] &&
     hrs[0].days.join() === '2' && /3:40.*4:30/.test(hrs[0].times), hrs);

  // It actually renders on Today for that day, pinned, with the task on it.
  const today = await p.evaluate(() => {
    const real = AZ.today; AZ.today = () => '2026-09-15';
    go('today'); const t = document.querySelector('#screen').innerText;
    AZ.today = real; return t;
  });
  ck('Today names the correction session', /test corrections/i.test(today), today.slice(0,200));
  ck('Today says when and what to bring',
     /3:40/.test(today) && /Unit 1 exam/i.test(today), /3:40/.test(today));
  ck('Extra help today now names History', /History/.test(today) && /3:40.{0,12}4:30/.test(today),
     (today.match(/.{0,60}3:40.{0,40}/) || [''])[0]);

  // The rule that matters: her mark is nowhere in the shipped file.
  const clean = await p.evaluate(() => {
    const ev = eventsOn('2026-09-15').concat(hoursForAll('history'));
    const blob = JSON.stringify(ev);
    return {blob, bad: /70%|75%|below a|score[d]? at/i.test(blob)};
  });
  ck('no grade, threshold or score appears in the shipped data', !clean.bad, clean.blob);

  // Coming up lists it from a few days out, once, and not twice.
  const up = await p.evaluate(() => upcomingEvents('2026-09-13', 14).map(e => e.name));
  ck('it appears in Coming up from Sunday', up.filter(n => /test corrections/i.test(n)).length === 1, up);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,5) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
