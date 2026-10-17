/* Saturday shows next week's brief (Ad Astra v211 / Wayfinder v188). Chris,
   looking at a bare Saturday Today: "seems to be missing some stuff". The
   brief used to return null on Saturdays; it now plans the coming Monday to
   Friday. Pins: Saturday's brief covers NEXT week (and so does Sunday's),
   a test next week reaches the prose as "next week", the ledger has five
   future rows with none marked today, the card says "Next week", and a
   weekday still plans its own week. Dates are found, never hardcoded. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8411;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  /* Real units, approved, so the plan has evenings to hand out. */
  await p.evaluate(async () => {
    for (const f of CONTENT_LIBRARY) {
      try { const j = await (await fetch('./' + f, {cache:'no-store'})).json();
        Object.values(j.records).forEach(u => { if (u.type === 'unit') { u.status = 'approved'; delete u.releaseOn; DATA.records[u.id] = u; } }); } catch(e) {}
    }
  });
  const r = await p.evaluate(() => {
    /* The first Saturday inside the school year whose next Monday is a
       school day, so the coming week is a real one. */
    let sat = AZ.shift(CAL.firstDay, 0);
    while (!(AZ.weekday(sat) === 6 && !closedToday(AZ.shift(sat, 2)) && sat > AZ.today())) sat = AZ.shift(sat, 1);
    const mon = AZ.shift(sat, 2), wed = AZ.shift(sat, 4), sun = AZ.shift(sat, 1);
    const cid = STUDY_CLASSES[0].id;
    put({id:'assess_sat_t', type:'assess', classId:cid, kind:'test', title:'Probe test', date:wed, score:null});
    /* One in the week now ending too, so the weekday case has something to plan. */
    put({id:'assess_sat_p', type:'assess', classId:cid, kind:'quiz', title:'Probe quiz', date:AZ.shift(sat, -1), score:null});
    AZ.today = () => sat; AZ.nowMinutes = () => 600;
    const wk = weekBrief(sat), wkSun = weekBrief(sun);
    const prevMon = AZ.shift(sat, -5), wkWeekday = weekBrief(AZ.shift(sat, -2));
    go('today');
    const s = document.getElementById('screen');
    const card = s.querySelector('.card.brief');
    return { sat, mon, wed,
      has: !!wk, monday: wk && wk.monday, sunMonday: wkSun && wkSun.monday,
      ahead: wk && wk.ahead, sunAhead: wkSun && wkSun.ahead,
      lead1: wk && wk.lead1, lead2: wk && wk.lead2, study: wk ? wk.plan.filter(x => x.kind === 'subject' || x.kind === 'mixed').length : 0, rows: wk ? wk.days.map(d => ({d:d.date, today:d.today, past:d.past})) : [],
      covers: wk && wk.covers(wed), weekdayMonday: wkWeekday && wkWeekday.monday, prevMon,
      card: !!card, eyebrow: card && card.querySelector('.eyebrow').textContent,
      divider: /Your week/.test(s.textContent), cardTxt: card && card.textContent };
  });
  ck('Saturday has a brief', r.has, r);
  ck('it plans the coming Monday to Friday, the same week Sunday plans', r.monday === r.mon && r.sunMonday === r.mon, r);
  ck('flagged as the week ahead on Saturday only', r.ahead === true && r.sunAhead === false, r);
  ck('five future rows, none marked today or past', r.rows.length === 5 && r.rows.every(x => !x.today && !x.past), r.rows);
  ck('a test next Wednesday is named as next week', /next week/.test(r.lead1) && /Probe|test/i.test(r.lead1) && !/this week/.test(r.lead1), r.lead1);
  ck('next week gets study evenings before the test', r.study >= 1 && /evening/.test(r.lead2), {study:r.study, lead2:r.lead2});
  ck('the brief covers that test (so the runway yields)', r.covers, r.covers);
  ck('the card renders on Today under Your week, eyebrow "Next week"', r.card && r.divider && /^Next week/.test(r.eyebrow), r.eyebrow);
  ck('a weekday still plans its own week', r.weekdayMonday === r.prevMon, r);
  ck('no page errors', errs.length === 0, errs);
  await b.close();
  const bad = out.filter(o => !o.ok);
  out.forEach(o => console.log((o.ok ? 'PASS ' : 'FAIL ') + o.n + (o.ok ? '' : '  ' + JSON.stringify(o.got))));
  console.log(bad.length ? `${bad.length} FAILED of ${out.length}` : `ALL PASS (${out.length})`);
  process.exit(bad.length ? 1 : 0);
})();
