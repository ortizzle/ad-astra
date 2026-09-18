/* Words for the note from home. The note's premise is that it did NOT come
   from the app, so most of this file is about the suggestions staying
   suggestions: opt-in, filling the box rather than posting, and his hand
   last on the words. Same file in both repos, bar its default port — the
   POOLS differ on purpose (identity, like the companion rosters), so nothing
   here asserts a specific line. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const pool = await p.evaluate(() => ({
    groups: NOTE_IDEAS.length,
    lines: NOTE_IDEAS.flatMap(g=>g.lines),
    keys: NOTE_IDEAS.map(g=>g.k),
    everyGroupHasLines: NOTE_IDEAS.every(g=>g.lines.length >= 2),
  }));
  ck('the pool is grouped by occasion, every group with something to choose from',
     pool.groups >= 5 && pool.everyGroupHasLines, {groups: pool.groups, keys: pool.keys});

  /* THE RULE THAT CARRIES OVER FROM THE APP'S OWN COPY, and matters more from
     a parent than from software: praise the process, never a fixed trait.
     Dweck — "you're so smart" measurably reduces persistence after failure. */
  const trait = /\b(smart|clever|brilliant|genius|talented|gifted|bright one|a natural)\b/i;
  const scored = /\b(grade|score|marks?|percent|%|\bA\+|straight a)\b/i;
  const traity = pool.lines.filter(l => trait.test(l));
  const gradey = pool.lines.filter(l => scored.test(l));
  ck('no line praises a fixed trait, and none of them mentions a grade',
     traity.length === 0 && gradey.length === 0, {traity, gradey});

  /* It renders at 30px in a handwriting face on a sticky note. */
  const fit = await p.evaluate(() => {
    const res = [];
    for(const line of NOTE_IDEAS.flatMap(g=>g.lines)){
      put({id:'pnote', type:'pnote', text:line}); go('today');
      const n = document.querySelector('.card.pnote');
      const pr = n.querySelector('p').getBoundingClientRect();
      res.push({line, rows: Math.round(pr.height/(30*1.22)),
                wide: Math.round(pr.width) > Math.round(n.getBoundingClientRect().width),
                scroll: document.documentElement.scrollWidth > 390});
    }
    softDelete('pnote');
    return res;
  });
  const tooTall = fit.filter(f => f.rows > 3), spill = fit.filter(f => f.wide || f.scroll);
  ck('every line fits the note in three handwritten rows, with nothing spilling off the phone',
     tooTall.length === 0 && spill.length === 0, {tooTall: tooTall.map(f=>f.line), spill});

  /* Opt-in: the app never puts words in front of him unasked. */
  const gate = await p.evaluate(() => {
    localStorage.setItem('trusted','1'); go('parent');
    const before = document.querySelectorAll('.idearow').length;
    const btn = [...document.querySelectorAll('button')].find(b=>/Need words/.test(b.textContent));
    const h = btn ? Math.round(btn.getBoundingClientRect().height) : 0;
    btn.click();
    const rows = [...document.querySelectorAll('.idearow')];
    return {before, after: rows.length, btnH: h,
            minRow: Math.min(...rows.map(r=>Math.round(r.getBoundingClientRect().height))),
            eachNamesAnOccasion: rows.every(r=>r.querySelector('.ik') && r.querySelector('.it'))};
  });
  ck('no suggestion is shown until he asks for one',
     gate.before === 0 && gate.after >= 5, gate);
  ck('the door and every suggestion are real tap targets, each naming its occasion',
     gate.btnH >= 44 && gate.minRow >= 44 && gate.eachNamesAnOccasion, gate);

  /* THE POINT: tapping fills the BOX. It must not post. */
  const tap = await p.evaluate(() => {
    const row = document.querySelector('.idearow');
    const picked = row.querySelector('.it').textContent;
    row.click();
    const ta = [...document.querySelectorAll('#screen textarea')]
      .find(t => t.value === picked);
    return {picked, inBox: !!ta,
            posted: !!(DATA.records['pnote'] && !DATA.records['pnote'].deleted),
            stillOpen: document.querySelectorAll('.idearow').length};
  });
  ck('tapping a suggestion puts it in the box and posts NOTHING — his hand is last on it',
     tap.inBox && tap.posted === false, tap);

  /* And it is still his to change before it goes up. */
  const edited = await p.evaluate(() => {
    const ta = [...document.querySelectorAll('#screen textarea')].find(t=>t.value);
    ta.value = ta.value + ' — Dad';
    [...document.querySelectorAll('button')].find(b=>b.textContent==='Post it').click();
    const rec = DATA.records['pnote'];
    go('today');
    return {text: rec && rec.text, onHerToday: (document.querySelector('.card.pnote')||{}).textContent || ''};
  });
  ck('what he typed is what she sees, verbatim',
     /— Dad$/.test(edited.text||'') && edited.onHerToday.includes('Dad'), edited);

  const reroll = await p.evaluate(() => {
    go('parent');
    [...document.querySelectorAll('button')].find(b=>/Need words/.test(b.textContent)).click();
    const first = [...document.querySelectorAll('.idearow .it')].map(e=>e.textContent);
    [...document.querySelectorAll('button')].find(b=>/different ones/.test(b.textContent)).click();
    const second = [...document.querySelectorAll('.idearow .it')].map(e=>e.textContent);
    // and re-rendering without re-rolling must NOT reshuffle under his thumb
    render();
    const third = [...document.querySelectorAll('.idearow .it')].map(e=>e.textContent);
    return {changed: first.some((l,i)=>l!==second[i]), stable: second.join('|')===third.join('|')};
  });
  ck('"different ones" gives different ones, and an ordinary re-render does not reshuffle them',
     reroll.changed && reroll.stable, reroll);

  ck('no page errors', errs.length === 0, errs.slice(0,3));

  await b.close();
  out.forEach(r => console.log((r.ok?'  ok  ':'  FAIL') + '  ' + r.n + (r.ok?'':'  ' + JSON.stringify(r.got))));
  const bad = out.filter(r => !r.ok).length;
  console.log(bad ? `\n${bad} FAILED of ${out.length}` : `\nALL PASS (${out.length})`);
  process.exit(bad ? 1 : 0);
})();
