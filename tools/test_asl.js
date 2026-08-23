/* Smoke test for the new ASL extracurricular subject: it must appear as a
   Study tile and get a working subject page, flashcards (with the video
   button) and a quiz — but it must NEVER show up on the fixed weekday
   timetable, which has no slot for it. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8099;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.addScriptTag({path: __dirname + '/seed.js'});
  await p.waitForTimeout(300);

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const r1 = await p.evaluate(async () => {
    const res = await fetch('./content/asl-1.json', {cache:'no-store'});
    const j = await res.json();
    const u = j.records['unit-asl1'];
    u.status = 'approved'; u.updatedAt = Date.now() - 1000;
    DATA.records[u.id] = u; saveLocal();
    AZ.today = () => '2026-08-24';           // a real Monday in the school year
    AZ.nowMinutes = () => 6 * 60;
    applyTheme();
    return {
      inStudyClasses: STUDY_CLASSES.some(c => c.id === 'asl'),
      inClassById: !!CLASS_BY_ID['asl'],
      inTimetable: CLASSES.some(c => c.id === 'asl'),
      pal: CLASS_BY_ID['asl'] && CLASS_BY_ID['asl'].icon
    };
  });
  ck('ASL is a study subject', r1.inStudyClasses, r1);
  ck('ASL resolves via CLASS_BY_ID', r1.inClassById, r1);
  ck('ASL is NOT in the fixed timetable', !r1.inTimetable, r1);
  ck('ASL keeps its icon', r1.pal === '🤟', r1.pal);

  // Today: the weekday timetable must render with no ASL row and no NaN.
  const today = await p.evaluate(() => {
    go('today');
    const rows = [...document.querySelectorAll('#screen .period')].map(r => r.textContent);
    return {rows, hasAsl: rows.some(t => /ASL/.test(t)), hasNaN: rows.some(t => /NaN/.test(t))};
  });
  ck('Today schedule has no ASL row', !today.hasAsl, today.rows);
  ck('Today schedule has no NaN time', !today.hasNaN, today.rows);

  // Study tab: the subject tile.
  const tile = await p.evaluate(() => {
    ctx._showTT = false;
    go('study');
    const t = [...document.querySelectorAll('#screen .tile')].find(x => /American Sign Language/.test(x.textContent));
    return t ? {text: t.textContent} : null;
  });
  ck('ASL tile renders on Study', !!tile, tile);

  // Subject page: eyebrow must say Extracurricular, not a NaN time/room.
  const subj = await p.evaluate(() => {
    go('unit', {classId:'asl'});
    const eyebrow = document.querySelector('#screen .card.ac .eyebrow');
    return {eyebrow: eyebrow ? eyebrow.textContent : null, html: document.getElementById('screen').innerHTML.slice(0,50)};
  });
  ck('Subject page eyebrow says Extracurricular', subj.eyebrow === 'Extracurricular', subj);

  // Flashcards: the Watch button on a real vocab card (skip c0, the orientation card).
  const cards = await p.evaluate(() => {
    go('cards', {unitId:'unit-asl1', classId:'asl'});
    cardState.i = cardState.order.indexOf(1); // card c1 = "Mom"
    render();
    document.querySelector('.flip').click(); // flip to the back
    const btn = document.querySelector('.watchb');
    return btn ? {text: btn.textContent, term: document.querySelector('.face.front .term').textContent} : null;
  });
  ck('Watch-the-sign button renders on a vocab card', !!cards, cards);
  ck('Watch button names its real host', cards && /signingsavvy\.com/.test(cards.text), cards);

  // Clicking Watch opens a new tab to the right URL and does not flip the card back.
  const popupUrl = await p.evaluate(() => new Promise(resolve => {
    window.open = (url) => { resolve(url); return null; };
    document.querySelector('.watchb').click();
  }));
  ck('Watch button opens the verified sign URL', popupUrl === 'https://www.signingsavvy.com/sign/MOM', popupUrl);
  const stillFlipped = await p.evaluate(() => document.querySelector('.flip').classList.contains('on'));
  ck('Clicking Watch does not flip the card back', stillFlipped, stillFlipped);

  // Quiz: a full round answers cleanly and logs.
  const quiz = await p.evaluate(async () => {
    go('quiz', {unitId:'unit-asl1', classId:'asl'});
    let guard = 0;
    while (view === 'quiz' && guard++ < 20) {
      const opts = [...document.querySelectorAll('#screen .opt')];
      if(!opts.length) break;
      opts[0].click();
      await new Promise(r=>setTimeout(r,20));
      const next = document.querySelector('#screen .btn-primary, #screen .explain .go-on');
      if(next) next.click();
      await new Promise(r=>setTimeout(r,20));
    }
    return {finalView: view, logged: all('log').some(l=>l.unitId==='unit-asl1')};
  });
  ck('Quiz round completes and logs', quiz.logged, quiz);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs : 'none');
  await b.close();
  if(!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
