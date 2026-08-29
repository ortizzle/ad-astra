/* The lesson-picking fixes (UX review, 2026-08): tapping a lesson on the
   topic map must (1) visibly select the tapped row, (2) scroll the opened
   card into view, and (3) the check-in screen must name the unit being
   quizzed. All three exist because a mis-picked lesson used to be invisible
   until question 1. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8113;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  // Seed a 7-lesson series so the map is genuinely taller than the viewport.
  const seeded = await p.evaluate(() => {
    const cid = STUDY_CLASSES[0].id;
    for (let i = 1; i <= 7; i++) {
      put({id:'u-sp'+i, type:'unit', classId:cid, status:'approved',
        title:'Pathtest · '+i+'-'+i+' Lesson Number '+i, cards:[{id:'c0',term:'t',def:'d'}],
        questions:[0,1,2].map(n=>({id:'q'+n, lv:1, q:'Q'+n, opts:['a','b','c','d'], ans:0, ex:{main:'m'}}))});
    }
    go('shelf', {classId:cid, series:'Pathtest', unitId:'u-sp1'});
    return {cid, stops: document.querySelectorAll('#screen .stop').length};
  });
  ck('7-lesson shelf renders with 7 stops', seeded.stops === 7, seeded);

  // Tap lesson 5 (low in the list). The row must become visibly selected and
  // the opened card must scroll into view.
  const picked = await p.evaluate(async () => {
    window.scrollTo(0, 0);
    const stops = [...document.querySelectorAll('#screen .stop')];
    stops[4].click();
    await new Promise(r => setTimeout(r, 900));   // smooth scroll settles
    const here = document.querySelector('#screen .stop.here');
    const hereBg = here ? getComputedStyle(here).backgroundColor : null;
    const oc = document.getElementById('shelfopen');
    const rect = oc ? oc.getBoundingClientRect() : null;
    return {
      openCtx: ctx.open,
      hereTitle: here ? here.querySelector('.t').textContent : null,
      hereBgOpaque: !!hereBg && hereBg !== 'rgba(0, 0, 0, 0)' && hereBg !== 'transparent',
      cardTitle: oc ? oc.querySelector('h3').textContent : null,
      cardTopInView: rect ? (rect.top >= -5 && rect.top < window.innerHeight * 0.6) : false,
      scrolled: window.scrollY > 100
    };
  });
  ck('tapping lesson 5 opens lesson 5', picked.openCtx === 'u-sp5', picked.openCtx);
  ck('the tapped row is visibly selected (real background, not just a pip ring)', picked.hereBgOpaque, picked);
  ck('the selected row is the one she tapped', /5-5/.test(picked.hereTitle||''), picked.hereTitle);
  ck('the opened card scrolled into view', picked.scrolled && picked.cardTopInView, picked);
  ck('the opened card is for the tapped lesson', /5-5/.test(picked.cardTitle||''), picked.cardTitle);

  // The check-in screen names the unit (and the mode when timed).
  const checkin = await p.evaluate((cid) => {
    go('checkin', {unitId:'u-sp5', classId:cid});
    const plain = document.getElementById('screen').innerText;
    go('checkin', {unitId:'u-sp5', classId:cid, timed:true});
    const timed = document.getElementById('screen').innerText;
    return {
      namesUnit: /Lesson Number 5/i.test(plain),
      namesModeWhenTimed: /beat the clock/i.test(timed),
      noModeWhenPlain: !/beat the clock/i.test(plain)
    };
  }, seeded.cid);
  ck('the check-in names the unit she is about to quiz', checkin.namesUnit, checkin);
  ck('Beat the clock is named only in timed mode', checkin.namesModeWhenTimed && checkin.noModeWhenPlain, checkin);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
