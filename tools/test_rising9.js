/* Rising 9th Grade Night (8th-grade post of 11/13), as the app carries it.
   Pins the date, the time from the flyer, the community tone, and the row
   reaching Coming up with the clock pointed at Monday 11/30, so it cannot rot.
   Also sweeps the event for a name or an address: the repo is public. */
const { chromium } = require('playwright');
const port = process.argv[2] || 8411;
let fails = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto(`http://localhost:${port}/index.html`, {waitUntil:'networkidle'});
  const r = await pg.evaluate(() => {
    const ev = CAL.events.find(e => e.name === 'Rising 9th Grade Night');
    AZ.today = () => '2026-11-30';
    AZ.nowMinutes = () => 6 * 60;
    go('today');
    const txt = document.getElementById('screen').textContent;
    return {ev, on: eventsOn('2026-12-02').some(e => e.name === 'Rising 9th Grade Night'),
            off: eventsOn('2026-12-03').some(e => e.name === 'Rising 9th Grade Night'),
            coming: /Rising 9th Grade Night/.test(txt),
            wd: new Date('2026-12-02T12:00:00Z').getUTCDay()};
  });
  ok(r.ev && r.ev.start === '2026-12-02' && !r.ev.end, 'one evening, Wednesday 12/2');
  ok(r.wd === 3, '12/2 really is a Wednesday, as the flyer says');
  ok(r.ev && /6:00–7:00 PM/.test(r.ev.note), 'the flyer\'s time, 6:00–7:00 PM');
  ok(r.ev && r.ev.kind === 'community', 'a community evening, not an exam');
  ok(r.on && !r.off, 'on 12/2 only');
  ok(r.coming, 'reaches Coming up from Monday 11/30');
  ok(r.ev && !/@|Gengler|Chandler Heights|basised/i.test(JSON.stringify(r.ev)), 'no name, email or address');
  ok(errs.length === 0, 'no page errors ' + JSON.stringify(errs));
  await b.close();
  console.log(fails ? `${fails} FAILED` : 'ALL PASS');
  process.exit(fails ? 1 : 0);
})();
