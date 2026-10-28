/* v218 — Wordly Wise Book 9 · Lessons 8, 9 and 10.
   Seeds the whole Book 9 shelf (Lessons 1–10) so "Lessons 8–10 shelve after 7"
   is a claim about coexistence, then pins, per lesson:
     - fifteen cards, each with a bold lead and a respelling
     - every word the subject or answer of at least one question
     - four analogies with four different relationships, each stem two words
     - no stem containing its own correct answer (the glossed-stem rule)
     - four unique options, answers spread across all four slots
     - quarter 2, draft, libv
     - a full round that logs, and the deck walking to the end
     - the two near-miss traps each lesson was built around, by their teaching */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8411;
const FILES = [1,2,3,4,5,6,7,8,9,10].map(n => 'ww9-lesson-' + String(n).padStart(2,'0'));
const WORDS = {
  8: ['adroit','affront','avocation','crusade','definitive','demeanor','erudite','induct','lapse','militant','pariah','prodigy','protégé','raucous','tacit'],
  9: ['allure','antiquity','appraise','cleave','depreciate','facet','facsimile','impervious','nondescript','quandary','repose','scintillate','scrutinize','synthetic','transmute'],
  10: ['amputate','aptitude','beneficiary','boon','commiserate','garner','gratis','incapacitate','inception','magnanimous','myriad','practicable','remunerate','solicit','trite'],
};
const STEM = w => w.replace(/(e|ate|ize|y|ity|ous)$/,'').slice(0, Math.max(5, w.length - 3));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.evaluate(() => booted);
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const shelf = await p.evaluate(async FILES => {
    const shipped = {};
    for (const f of FILES) {
      const k = await (await fetch('./content/' + f + '.json', {cache:'no-store'})).json();
      for (const x of Object.values(k.records)) { shipped[x.id] = {status:x.status, q:x.quarter, libv:x.libv};
        x.status = 'approved'; DATA.records[x.id] = x; } }
    saveLocal();
    const sh = shelvesFor('english').shelves.find(s => /Wordly Wise Book 9/.test(s.name));
    return { inLib: FILES.every(f => CONTENT_LIBRARY.includes('content/' + f + '.json')), shipped,
             ids: sh ? sh.lessons.map(u => u.id) : [] };
  }, FILES);
  ck('Lessons 8–10 are in CONTENT_LIBRARY', shelf.inLib, null);
  ck('the Book 9 shelf runs Lesson 1 to Lesson 10 in order',
     JSON.stringify(shelf.ids) === JSON.stringify([1,2,3,4,5,6,7,8,9,10].map(n => 'unit-ww9-' + String(n).padStart(2,'0'))), shelf.ids);

  for (const n of [8, 9, 10]) {
    const id = 'unit-ww9-' + String(n).padStart(2,'0');
    const s = shelf.shipped[id];
    ck(`L${n} ships as a Quarter 2 draft with libv`, s && s.status === 'draft' && s.q === 2 && s.libv >= 1, s);
    const r = await p.evaluate(([id, words, stems]) => {
      const u = DATA.records[id];
      const cards = u.cards.map(c => c.term);
      const okCards = u.cards.every(c => /^\*\*[^*]+\*\*/.test(c.def) && c.sp && c.hint && c.hint !== c.def);
      const blob = q => (q.q + ' ' + q.opts[q.ans]).toLowerCase();
      const uncovered = words.filter((w, i) => !u.questions.some(q => blob(q).includes(stems[i].toLowerCase())));
      const an = u.questions.filter(q => q.kind === 'analogy');
      const rel = an.map(q => (q.ex.main.match(/\*\*Both pairs are ([^.]+)\./) || [])[1]);
      const anShape = an.every(q => /^[A-ZÀ-Ý]+ : [A-ZÀ-Ý]+$/.test(q.q) && q.opts.every(o => /^[a-zà-ÿ]+ : [a-zà-ÿ]+$/.test(o)));
      const leaks = u.questions.filter(q => q.kind !== 'analogy' && q.q.toLowerCase().includes(q.opts[q.ans].toLowerCase())).map(q => q.id);
      const slots = new Set(u.questions.map(q => q.ans)).size;
      const uniq = u.questions.every(q => q.opts.length === 4 && new Set(q.opts).size === 4 && q.ans >= 0 && q.ans < 4);
      const steps = u.questions.every(q => q.steps.length >= 3 && q.steps.length <= 6 && /^\*\*/.test(q.ex.main));
      return { cards, okCards, uncovered, rel, anShape, leaks, slots, uniq, steps, nq: u.questions.length };
    }, [id, WORDS[n], WORDS[n].map(STEM)]);
    ck(`L${n} has the fifteen list words as cards`, JSON.stringify(r.cards) === JSON.stringify(WORDS[n]), r.cards);
    ck(`L${n} every card leads in bold, carries a respelling and a hook`, r.okCards, null);
    ck(`L${n} every word is asked about`, r.uncovered.length === 0, r.uncovered);
    ck(`L${n} four analogies, four different named relationships`, r.rel.length === 4 && new Set(r.rel).size === 4 && r.rel.every(Boolean), r.rel);
    ck(`L${n} analogy stems and options are WORD : WORD pairs`, r.anShape, null);
    ck(`L${n} no stem contains its own correct answer`, r.leaks.length === 0, r.leaks);
    ck(`L${n} 18+ questions, four unique options, all four slots, steps and a bold explanation`,
       r.nq >= 18 && r.uniq && r.slots === 4 && r.steps, r);

    const play = await p.evaluate(async id => {
      const u = DATA.records[id];
      quizState = null; go('quiz', {unitId:id, classId:'english'});
      let guard = 0, plate = false;
      while (view === 'quiz' && guard++ < 90) {
        if (document.querySelector('#screen .analogy .blank')) plate = true;
        const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
        if (opts.length) for (const o of opts) { o.click(); await new Promise(r => setTimeout(r, 4)); }
        await new Promise(r => setTimeout(r, 8));
        const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
        if (next) { next.click(); await new Promise(r => setTimeout(r, 8)); continue; }
        if (!opts.length) break;
      }
      document.querySelectorAll('.modal-back, .modal').forEach(m => m.remove());
      const l = all('log').find(x => x.unitId === id && x.mode === 'quiz');
      go('cards', {unitId:id, classId:'english'});
      const deck = cardState && cardState.order ? cardState.order.length : 0;
      return { logged: !!l, total: l && l.total, deck, saidas: !!document.querySelector('#screen .saidas'), plate };
    }, id);
    ck(`L${n} a full round plays and logs`, play.logged && play.total === 5, play);
    ck(`L${n} the 15-card deck opens with a respelling`, play.deck === 15 && play.saidas, play);
  }

  // The traps each lesson was built around, asserted by their teaching.
  const traps = await p.evaluate(() => {
    const u = n => DATA.records['unit-ww9-' + String(n).padStart(2,'0')];
    const ans = (n, re) => { const q = u(n).questions.find(q => re.test(q.q)); return q && q.opts[q.ans]; };
    const opts = (n, re) => { const q = u(n).questions.find(q => re.test(q.q)); return q ? q.opts : []; };
    return {
      prodigy: ans(8, /At age seven/), prodigyHasProtege: opts(8, /At age seven/).includes('Protégé'),
      protege: ans(8, /trained for years under/),
      avocation: ans(8, /Dana is a surgeon/), avocationHasVocation: opts(8, /Dana is a surgeon/).includes('Vocation'),
      cleaveSplit: ans(9, /butcher cleaved/), cleaveCling: ans(9, /cleaved to her family/),
      beneficiary: ans(10, /leaves her fortune/), benefactorNamed: /benefactor/.test(JSON.stringify(u(10).questions.find(q => /leaves her fortune/.test(q.q)))),
      gratis: ans(10, /concert in the park is gratis/), gratisTrap: opts(10, /concert in the park is gratis/).includes('Must thank the performers'),
      aptitudeTrap: opts(10, /logic puzzles/).includes('Attitude'),
      lacksHas: opts(8, /^PARIAH : ACCEPTANCE$/).includes('prodigy : talent'),
    };
  });
  ck('L8 a prodigy is early talent, with protégé offered as the trap', traps.prodigy === 'Prodigy' && traps.prodigyHasProtege, traps);
  ck('L8 a protégé is the one a mentor helps', traps.protege === 'Protégé', traps.protege);
  ck('L8 an avocation is the hobby, with vocation offered as the trap', traps.avocation === 'Avocation' && traps.avocationHasVocation, traps);
  ck('L8 the "lacks" analogy offers "has" (prodigy : talent) as a wrong option', traps.lacksHas, null);
  ck('L9 cleave is taught in both opposite senses', traps.cleaveSplit === 'Split' && traps.cleaveCling === 'Held on to them faithfully', traps);
  ck('L10 the beneficiary receives, and the giver is named the benefactor', traps.beneficiary === 'The hospital' && traps.benefactorNamed, traps);
  ck('L10 gratis means free, with gratitude offered as the trap', traps.gratis === 'Pay nothing to attend' && traps.gratisTrap, traps);
  ck('L10 aptitude is offered against attitude', traps.aptitudeTrap, null);

  // Privacy sweep: nothing about her in the shipped records.
  const priv = await p.evaluate(() => [8,9,10].map(n => JSON.stringify(DATA.records['unit-ww9-' + String(n).padStart(2,'0')]))
    .some(s => /Ortiz|Sedona|she (got|wrote|put|answered)|\bscored\b|\d+\s*out of\s*\d+/i.test(s)));
  ck('no name and no mark anywhere in the three records', !priv, null);

  out.forEach(x => console.log((x.ok ? 'ok   ' : 'FAIL ') + x.n + (x.ok ? '' : ' → ' + JSON.stringify(x.got).slice(0, 300))));
  console.log(out.every(x => x.ok) ? `all ${out.length} passed` : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0, 5) : 'none');
  await b.close();
  if (!out.every(x => x.ok) || errs.length) process.exit(1);
})();
