/* To Kill a Mockingbird chapter quizzes, chapters 6–13 (v210). One unit per
   chapter, shelved behind the chapters 1–5 companion on the same spine. The
   rules pinned here are the ones a reading companion lives or dies by:
   chapter order on the shelf, no quiz reaching past its own chapter, the
   slur never printed, every question standalone, and a full round on each. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8301;
const CH = [6,7,8,9,10,11,12,13];
const pad = n => String(n).padStart(2,'0');
// Tells that only exist in LATER chapters. Written here independently of the
// builders' own lists, so a builder that forgets one is still caught.
const LATER = {
  6:  ['cement','soap','blanket','snow','tom robinson','mad dog','tim johnson','dubose','alexandra','sin to kill'],
  7:  ['blanket','snowman','burned','tom robinson','mad dog','tim johnson','dubose','alexandra','sin to kill'],
  8:  ['tom robinson','cecil','francis','uncle jack','mad dog','tim johnson','dubose','alexandra','sin to kill'],
  9:  ['mad dog','tim johnson','one-shot','dubose','camellia','first purchase','sin to kill'],
  10: ['dubose','camellia','morphine','first purchase','zeebo','meridian'],
  11: ['first purchase','zeebo','lula','meridian','blackstone'],
  12: ['streak','gentle breeding','feminine influence','fine folks'],
  13: [],
};
const ALWAYS = ['verdict','guilty','lynch','jailhouse','the mob','mr. underwood','under scout','under her bed'];
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const files = ['content/tkam-1.json', ...CH.map(c => `content/tkam-c${pad(c)}.json`)];
  const seed = await p.evaluate(async (files) => {
    const ids = [];
    for (const f of files) {
      const j = await (await fetch('./' + f, {cache:'no-store'})).json();
      const u = Object.values(j.records)[0];
      u.status = 'approved'; u.updatedAt = Date.now() - 1000;
      DATA.records[u.id] = u; ids.push(u.id);
    }
    saveLocal();
    const inLib = files.every(f => CONTENT_LIBRARY.includes(f));
    return { ids, inLib };
  }, files);
  ck('all nine TKAM files are in CONTENT_LIBRARY', seed.inLib, seed);

  const shelf = await p.evaluate(() => {
    const sh = shelvesFor('english');
    const book = sh.shelves.find(s => s.name === 'To Kill a Mockingbird');
    return { order: book ? book.units.map(u => u.id) : null,
             loose: sh.loose.filter(u => /tkam/.test(u.id)).map(u => u.id) };
  });
  ck('one spine, in chapter order: 1–5, then 6 through 13',
     JSON.stringify(shelf.order) === JSON.stringify(['unit-tkam1', ...CH.map(c => 'unit-tkam-c' + pad(c))]), shelf);
  ck('no TKAM unit is loose', shelf.loose.length === 0, shelf);

  for (const c of CH) {
    const id = 'unit-tkam-c' + pad(c);
    const r = await p.evaluate(({id, c, later, always}) => {
      const u = DATA.records[id];
      const { title, ...rest } = u;
      const blob = JSON.stringify(rest).toLowerCase();
      const qs = u.questions;
      const laterCh = [];
      for (let m = c + 1; m <= 31; m++)
        if (new RegExp('(chapter|ch\\.)\\s*' + m + '\\b').test(blob)) laterCh.push(m);
      const seen = qs.map(x => x.q + ' ' + x.opts.join(' ') + ' ' + (x.passage||'')).join(' ');
      return {
        title, classId: u.classId, book: !!u.book, libv: u.libv, status: u.status,
        n: qs.length, cards: u.cards.length,
        lv: [1,2,3].map(l => qs.filter(x => x.lv === l).length),
        order: qs.filter(x => x.kind === 'order').length,
        mcOk: qs.filter(x => x.kind !== 'order').every(x => x.opts.length === 4 && new Set(x.opts).size === 4 && x.ans >= 0 && x.ans < 4),
        slots: [...new Set(qs.filter(x => x.kind !== 'order').map(x => x.ans))].length,
        hits: later.concat(always).filter(w => blob.includes(w)), laterCh,
        slur: /n[i1]gg/i.test(JSON.stringify(u)),
        backref: qs.filter(x => /^(the|that|this) same\b/i.test(x.q)).map(x => x.id),
        posref: qs.filter(x => /\b(all|none) of the above\b|\b(first|second|third|last) (option|choice)\b/i.test(seen)).map(x => x.id),
        boldDefs: u.cards.every(k => k.def.startsWith('**')),
        ponder: u.cards.filter(k => /^Ponder/.test(k.term)).length,
        steps: qs.every(x => x.steps.length >= 3 && x.steps.length <= 6),
        passLen: qs.filter(x => x.passage).every(x => x.passage.split(/\s+/).length <= 45),
        title2: new RegExp('Ch\\. ' + c + ':').test(title),
      };
    }, {id, c, later: LATER[c], always: ALWAYS});
    ck(`Ch. ${c}: english, book, draft, libv, titled "Ch. ${c}:"`,
       r.classId === 'english' && r.book && r.status === 'approved' && r.libv >= 1 && r.title2, r);
    ck(`Ch. ${c}: 10+ questions across all three levels, one put-in-order`,
       r.n >= 10 && r.lv.every(x => x > 0) && r.order >= 1, {n: r.n, lv: r.lv, order: r.order});
    ck(`Ch. ${c}: 4 unique options everywhere, answers in all four slots`, r.mcOk && r.slots === 4, r.slots);
    ck(`Ch. ${c}: nothing reaches past chapter ${c}`, r.hits.length === 0 && r.laterCh.length === 0, {hits: r.hits, ch: r.laterCh});
    ck(`Ch. ${c}: the slur is never printed`, !r.slur, r.slur);
    ck(`Ch. ${c}: no back-references, no positional references`, !r.backref.length && !r.posref.length, r);
    ck(`Ch. ${c}: bold-first defs, one ponder card, 3–6 steps, passages ≤45 words`,
       r.boldDefs && r.ponder === 1 && r.steps && r.passLen, r);

    const round = await p.evaluate(async ({id}) => {
      quizState = null;
      go('quiz', {unitId:id, classId:'english'});
      let guard = 0;
      while (view === 'quiz' && guard++ < 40) {
        const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
        if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,4)); }
        await new Promise(r => setTimeout(r, 8));
        const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
        if (next) { next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
        if (!opts.length) break;
      }
      document.querySelectorAll('.modal-bg, .modal').forEach(m => m.remove());
      const log = all('log').find(l => l.unitId === id);
      go('cards', {unitId:id, classId:'english'});
      let seen = 0, g2 = 0;
      while (view === 'cards' && g2++ < 40) {
        const nx = document.querySelector('#screen .btn-primary');
        if (!nx) break; nx.click(); seen++;
        await new Promise(r => setTimeout(r, 6));
      }
      return { logged: !!log, total: log && log.total, seen, cards: DATA.records[id].cards.length };
    }, {id});
    ck(`Ch. ${c}: a full round plays the whole chapter in one sitting, and the deck walks`,
       round.logged && round.total >= 10 && round.seen >= round.cards - 1, round);
  }

  const clock = await p.evaluate(() => {
    go('shelf', {classId:'english', series:'To Kill a Mockingbird', open:'unit-tkam-c10'});
    return /Beat the clock/.test(document.getElementById('screen').textContent);
  });
  ck('no Beat the clock on a chapter quiz (book units)', !clock, clock);

  out.forEach(r => console.log((r.ok ? '  ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' → ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
