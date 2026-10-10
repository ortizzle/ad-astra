/* A note on your week, and the Wonder Jar door. Same file in both repos, bar
   its default port.

   The note is written by a scheduled session every Sunday and deployed on its
   own, so most of this file pins the guards that make an unattended deploy
   safe: a malformed or stale file must cost a note, never the app; the note
   expires with its week; it renders as text, never as markup; and the shipped
   file — public, like everything in this repo — says what is coming and never
   how she is doing. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const PORT = process.argv[2] || 8201;
const REPO = process.argv[3] || '.';
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const ctx = await b.newContext({viewport:{width:390,height:844}, serviceWorkers:'block'});
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  /* The file the app fetches, swapped per case. null = 404. */
  let serve = null;
  await p.route('**/week-note.json', r => serve === null
    ? r.fulfill({status:404, body:'nope'})
    : r.fulfill({status:200, contentType: typeof serve === 'string' ? 'text/html' : 'application/json',
        body: typeof serve === 'string' ? serve : JSON.stringify(serve)}));

  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.evaluate(() => localStorage.clear());
  await p.reload({waitUntil:'networkidle'});
  const wk = await p.evaluate(() => AZ.weekStart(AZ.today()));
  const lastWk = await p.evaluate(w => AZ.shift(w, -7), wk);

  const refetch = async () => { await p.evaluate(async () => { await fetchWeekNote(); go('today'); }); await p.waitForTimeout(150); };
  const state = () => p.evaluate(() => {
    const card = document.querySelector('.card.weeknote');
    const kids = [...document.getElementById('screen').children];
    const ci = kids.indexOf(card);
    const brief = document.querySelector('.card.brief');
    const prev = card && card.previousElementSibling;
    const jar = document.querySelector('a.wn-jar');
    return {
      card: !!card,
      paras: card ? [...card.querySelectorAll('p.brief-prose')].map(x => x.textContent) : [],
      bold: card ? [...card.querySelectorAll('p.brief-prose b')].map(x => x.textContent) : [],
      imgs: card ? card.querySelectorAll('img').length : 0,
      src: card ? (card.querySelector('p.wn-src')||{}).textContent : null,
      eyebrow: card ? card.querySelector('.eyebrow').textContent : null,
      underDivider: !!(prev && prev.classList.contains('divider') && /your week/i.test(prev.textContent)),
      beforeBrief: !!(brief && card && (card.compareDocumentPosition(brief) & Node.DOCUMENT_POSITION_FOLLOWING)),
      jar: jar ? {href: jar.href, target: jar.target, rel: jar.rel, h: jar.getBoundingClientRect().height,
                  text: jar.textContent} : null,
      stored: Store.get(WEEK_NOTE_KEY, null),
    };
  });

  /* 1. No file yet: nothing breaks, nothing renders, the jar door stands alone. */
  serve = null; await refetch();
  let s = await state();
  ck('with no note file, Today renders and shows no note card', !s.card && errs.length === 0, {errs});
  ck('the Wonder Jar door is on Today regardless, opening the jar in a new tab',
     s.jar && s.jar.href === 'https://ortizzle.github.io/wonder-jar/' && s.jar.target === '_blank'
       && /noopener/.test(s.jar.rel), s.jar);
  ck('the jar door is a 44px target', s.jar && s.jar.h >= 44, s.jar && s.jar.h);

  /* 2. A note for THIS week. */
  const good = {v:1, week: wk, written: wk,
    text: 'First paragraph with a **bold run** in it.\n\nSecond paragraph <img src=x onerror=alert(1)> stays text.'};
  serve = good; await refetch();
  s = await state();
  ck('a note for this week renders as its own card', s.card, s);
  ck('it sits under the Your week divider, above the brief', s.underDivider && (s.beforeBrief || !(await p.$('.card.brief'))), s);
  ck('a blank line splits paragraphs', s.paras.length === 2, s.paras);
  ck('**bold** renders as bold, and markup in the text stays text', s.bold[0] === 'bold run' && s.imgs === 0
     && /<img/.test(s.paras[1]), {bold: s.bold, p2: s.paras[1]});
  ck('it says who wrote it and from what', /Written by Claude/.test(s.src) && /newsletters/.test(s.src), s.src);

  /* 3. It expires with its week: a stale note never shows. */
  serve = {...good, week: lastWk, written: lastWk, text: 'Last week.'}; await refetch();
  s = await state();
  ck('a note for LAST week is stored but not shown', !s.card && s.stored && s.stored.week === lastWk, s.stored);

  /* 3b. Daily notes (v205 / Wayfinder v180): a `day` note shows on that date
     only, says "today", and yesterday's never lingers into this morning. */
  const today = await p.evaluate(() => AZ.today());
  const yday = await p.evaluate(t => AZ.shift(t, -1), today);
  serve = {v:1, day: today, written: today, text: 'Today has **one** thing in it.'}; await refetch();
  s = await state();
  ck('a day note for TODAY renders, labelled as today', s.card && /for today/i.test(s.eyebrow) && s.bold[0] === 'one',
     {eyebrow: s.eyebrow, bold: s.bold});
  serve = {v:1, day: yday, written: yday, text: 'Yesterday.'}; await refetch();
  s = await state();
  ck('a day note for YESTERDAY is stored but not shown', !s.card && s.stored && s.stored.day === yday, s.stored);

  /* 4. Malformed files cost a note, never the app — and never the copy already held. */
  serve = good; await refetch();
  for(const bad of [
    {v:1, week: AZ_mon(wk), text:'Not a Sunday.'},
    {v:1, week: wk, text:'   '},
    {v:1, week: wk, text: 'x'.repeat(1600)},
    {v:1, text:'No week.'},
    {v:1, day:'10/10/2026', text:'Not an ISO day.'},
    {v:1, day: today, week: wk, text:'Both a day and a week.'},
    '<!doctype html><title>offline fallback</title>',
  ]){
    serve = bad; await refetch();
  }
  s = await state();
  ck('a non-Sunday week, empty text, an oversized note, no date, a malformed day, a note claiming both, and an HTML fallback are all ignored',
     s.card && s.stored && s.stored.text === good.text && errs.length === 0, {stored: s.stored && s.stored.text, errs});

  /* 5. Offline: the device keeps the last good note. */
  await p.unroute('**/week-note.json');
  await p.route('**/week-note.json', r => r.abort());
  await p.reload({waitUntil:'load'}); await p.waitForTimeout(400);
  s = await state();
  ck('offline, the last good note still renders', s.card && s.paras.length === 2, s.paras);

  /* 6. It is not a record: nothing syncs, nothing reaches the Gist. */
  const rec = await p.evaluate(() => Object.values(DATA.records).some(r => /week/i.test(r.type||'') && /note/i.test(r.type||'')));
  ck('the note never enters the record store', !rec);

  /* 7. The shipped file, if there is one. It is public and written unattended. */
  const f = path.join(REPO, 'week-note.json');
  if(fs.existsSync(f)){
    const n = JSON.parse(fs.readFileSync(f, 'utf8'));
    const ok = await p.evaluate(n => validWeekNote(n), n);
    ck('the shipped week-note.json is valid', ok, n.week);
    const t = n.text || '';
    const marks = [/\b\d+\s*(%|percent)/i, /\bout of \d+/i, /\b\d+\s*\/\s*\d+\b(?![-\/]\d)/, /\bscored?\b/i,
                   /\byou got\b/i, /\bshe got\b/i, /\bgrades? (?:of|was|is)\b/i, /@/, /https?:/i];
    const hit = marks.filter(r => r.test(t)).map(String);
    ck('the shipped note carries no mark, no score, no address and no link', hit.length === 0, hit);
    ck('the shipped note talks TO her, never about her', !/\b(she|her)\b/i.test(t), t.match(/\b(she|her)\b/gi));
    ck('the shipped note has no exclamation marks', !/!/.test(t));
  } else {
    ck('no week-note.json shipped yet (the Sunday session writes it)', true);
  }

  out.forEach(o => console.log((o.ok ? 'PASS ' : 'FAIL ') + o.n + (o.ok ? '' : '  ' + JSON.stringify(o.got))));
  const fails = out.filter(o => !o.ok).length;
  console.log(fails ? `${fails} FAILED` : 'ALL PASS');
  await b.close();
  process.exit(fails ? 1 : 0);
})();

/* The Monday after a Sunday, as an ISO date — a week key that is not a Sunday. */
function AZ_mon(ds){ const [y,m,d] = ds.split('-').map(Number);
  return new Date(Date.UTC(y, m-1, d+1)).toISOString().slice(0,10); }
