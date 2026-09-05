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
    /* v150: Study lists the day's line-up as .period rows; a club has no
       period, so it follows the line-up with 'Club' where the time goes. */
    const t = [...document.querySelectorAll('#screen .period.tap')].find(x => /American Sign Language/.test(x.textContent));
    return t ? {text: t.textContent, club: /Club/.test(t.querySelector('.tm')?.textContent||'')} : null;
  });
  ck('ASL row renders on Study, marked as a club', !!tile && tile.club, tile);

  // Subject page: eyebrow must say Extracurricular, not a NaN time/room.
  const subj = await p.evaluate(() => {
    go('unit', {classId:'asl'});
    const eyebrow = document.querySelector('#screen .card.ac .eyebrow');
    return {eyebrow: eyebrow ? eyebrow.textContent : null, html: document.getElementById('screen').innerHTML.slice(0,50)};
  });
  ck('Subject page eyebrow says Extracurricular', subj.eyebrow === 'Extracurricular', subj);

  // Flashcards: the Watch link on a real vocab card (skip c0, the orientation card).
  const cards = await p.evaluate(() => {
    go('cards', {unitId:'unit-asl1', classId:'asl'});
    cardState.i = cardState.order.indexOf(1); // card c1 = "Mom"
    render();
    document.querySelector('.flip').click(); // flip to the back
    const a = document.querySelector('.watchb');
    return a ? {text: a.textContent, href: a.href, target: a.target, rel: a.rel,
      term: document.querySelector('.face.front .term').textContent} : null;
  });
  ck('Watch-the-sign link renders on a vocab card', !!cards, cards);
  ck('Watch link names its real host', cards && /signingsavvy\.com/.test(cards.text), cards);
  ck('Watch link points at the verified sign URL', cards && cards.href === 'https://www.signingsavvy.com/sign/MOM', cards);
  ck('Watch link opens a new tab, safely', cards && cards.target === '_blank' && /noopener/.test(cards.rel), cards);

  // Clicking Watch does not flip the card back (the link's own listener
  // stopPropagation's before the flip container's click handler sees it).
  // href/target/rel above already establish it is a real, safe new-tab link.
  await p.click('.watchb');
  const stillFlipped = await p.evaluate(() => document.querySelector('.flip').classList.contains('on'));
  ck('Clicking Watch does not flip the card back', stillFlipped, stillFlipped);

  // watchNode() itself: once a card carries a verified embedId, it must embed
  // inline (youtube-nocookie.com) instead of falling back to the link.
  const embed = await p.evaluate(() => {
    const node = watchNode({id:'x', term:'Test', watchUrl:'https://example.com/x', embedId:'dQw4w9WgXcQ'}, 'watchb');
    const f = node.querySelector('iframe');
    return {isVidwrap: node.classList.contains('vidwrap'), src: f && f.src, title: f && f.title};
  });
  ck('A card with embedId embeds inline instead of linking out', embed.isVidwrap, embed);
  ck('The embed uses the privacy-enhanced YouTube domain', /^https:\/\/www\.youtube-nocookie\.com\/embed\/dQw4w9WgXcQ/.test(embed.src||''), embed);

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

  // The alphabet deck: 26 letters + orientation card, each with a real image,
  // no quiz/clock tile (0 questions), shelved alongside Class 1.
  const alphaSeed = await p.evaluate(async () => {
    const res = await fetch('./content/asl-alphabet.json', {cache:'no-store'});
    const j = await res.json();
    const u = j.records['unit-asl-alpha'];
    u.status = 'approved'; u.updatedAt = Date.now() - 1000;
    DATA.records[u.id] = u; saveLocal();
    return {cards: u.cards.length, questions: u.questions.length};
  });
  ck('Alphabet unit has 27 cards (orientation + 26 letters)', alphaSeed.cards === 27, alphaSeed);

  const alphaCard = await p.evaluate(() => {
    go('cards', {unitId:'unit-asl-alpha', classId:'asl'});
    const bIdx = unitFor('unit-asl-alpha').cards.findIndex(c=>c.term==='B');
    cardState.i = cardState.order.indexOf(bIdx);
    render();
    document.querySelector('.flip').click();
    const img = document.querySelector('.signimg img');
    return img ? {src: img.src, alt: img.alt} : null;
  });
  ck('Letter card shows its reference image', !!alphaCard, alphaCard);
  ck('Image points at the verified Commons file for B', alphaCard &&
    alphaCard.src === 'https://commons.wikimedia.org/wiki/Special:FilePath/Sign_language_B.svg', alphaCard);

  const alphaShelf = await p.evaluate(() => {
    go('unit', {classId:'asl'});
    const spines = [...document.querySelectorAll('#screen .spine')].map(s=>s.textContent);
    return spines;
  });
  // One shelf ("ASL Club"), both parts inside it — a spine is per SERIES,
  // not per lesson, so "Class 1" and "Alphabet" merge into one spine.
  ck('Alphabet shelves alongside Class 1 (one "ASL Club" spine, 2 parts)',
    alphaShelf.length === 1 && /^ASL Club/.test(alphaShelf[0]), alphaShelf);

  const alphaTiles = await p.evaluate(() => {
    ctx.open = 'unit-asl-alpha';
    go('shelf', {classId:'asl', series:'ASL Club'});
    const tiles = [...document.querySelectorAll('#screen .mtile')].map(t=>t.textContent);
    const pill = [...document.querySelectorAll('#screen .pill')].map(p=>p.textContent).find(t=>/reference only|questions/.test(t));
    return {tiles, pill};
  });
  ck('Alphabet deck offers only Flashcards (no Quiz/Clock tile)', alphaTiles.tiles.length === 1 && /Flashcards/.test(alphaTiles.tiles[0]), alphaTiles);
  ck('Alphabet deck pill says "reference only"', alphaTiles.pill === 'reference only', alphaTiles);

  // Finishing the alphabet deck must not offer a quiz she can't take, and
  // must not claim she wrote cards she didn't.
  const alphaFinish = await p.evaluate(async () => {
    go('cards', {unitId:'unit-asl-alpha', classId:'asl'});
    const u = unitFor('unit-asl-alpha');
    cardState.order.forEach((idx,i)=>{ cardState.i = i; cardState.seen.add(idx); });
    cardState.i = cardState.order.length - 1;
    finishCards(u);
    await new Promise(r=>setTimeout(r,50));
    const modal = document.querySelector('.modal-box');
    return modal ? modal.textContent : null;
  });
  ck('Finishing the deck never claims "you wrote these"', alphaFinish && !/you wrote these/i.test(alphaFinish), alphaFinish);
  ck('Finishing the deck offers no quiz to take', alphaFinish && !/take the quiz/i.test(alphaFinish), alphaFinish);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs : 'none');
  await b.close();
  if(!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
