/* Tutoring today (v140) — a standing weekly appointment read once from her
   calendar, rendered on Today regardless of whether it's a school day. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8140;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);

  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const r = await p.evaluate(() => {
    const readCard = () => {
      const cards = [...document.querySelectorAll('#screen .card.quiet')];
      /* v150: student hours and tutoring share one 'Extra help today' card;
         the tutoring row is the one with the tutor glyph. */
      const c = cards.find(x => (x.querySelector('.eyebrow')||{}).textContent === 'Extra help today');
      const row = c && [...c.querySelectorAll('.row')].find(r => /🧑/.test(r.querySelector('.k').textContent));
      return row ? row.querySelector('.k').textContent + '|' + row.querySelector('small').textContent : null;
    };
    const out = {};

    // Sunday 2026-08-16 — a real non-school day, tutoring should still show.
    AZ.today = () => '2026-08-16';
    go('today'); out.sun = readCard();

    // Wednesday 2026-08-19 — the other weekly slot.
    AZ.today = () => '2026-08-19';
    go('today'); out.wed = readCard();

    // Monday 2026-08-17 — not a tutoring day, no card.
    AZ.today = () => '2026-08-17';
    go('today'); out.mon = readCard();

    return out;
  });

  ck('Sunday shows tutoring, 1:00–3:00 pm, even though school is closed',
     r.sun && /🧑/.test(r.sun) && r.sun.includes('1:00–3:00 pm'), r.sun);
  ck('Wednesday shows tutoring, 3:00–5:30 pm',
     r.wed && r.wed.includes('3:00–5:30 pm'), r.wed);
  ck('Monday (no tutoring) renders no tutoring card', r.mon === null, r.mon);

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
