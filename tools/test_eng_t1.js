/* v194 — Sedona's English Test 1 shelf, all seven parts.

   Built from her own handwritten unit notes. What this file pins is the
   SHELF (seven parts in teaching order, structural numbering, every one
   prep-flagged) and, per part, the teaching rather than the question ids —
   a renumber must not be able to break an assertion.

   The two source-fidelity checks are the ones worth having: "style and
   voice" belongs under why-to-use-tone (Drive's OCR filed it under "tone is
   NOT", which would have taught the opposite), and part 7 must not repeat
   the ch.1-5 reading companion she already has. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
const FILES = ['eng-t1-plot','eng-t1-context','eng-t1-diction','eng-t1-tone',
               'eng-t1-fig','eng-t1-sym','eng-t1-tkam'];
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async (files) => {
    // The ch.1-5 reading companion is seeded alongside on purpose: "its own
    // shelf" has to be a claim about coexisting with what English already has.
    for (const f of files.concat(['tkam-1','ww9-lesson-01'])) {
      const j = await (await fetch('./content/'+f+'.json',{cache:'no-store'})).json();
      const u = Object.values(j.records).find(x=>x.type==='unit');
      u.status='approved'; u.updatedAt=Date.now()-1000; DATA.records[u.id]=u;
    }
    saveLocal();
    const pick = id => { const u = DATA.records[id];
      return {id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order,
              prep:!!u.prep, cards:u.cards, qs:u.questions,
              note:(u.parentNote||{}).text||'', blob:JSON.stringify(u)}; };
    const ids = ['plot','context','diction','tone','fig','sym','tkam']
                  .map(k => 'unit-eng-t1-'+k);
    const o = {}; ids.forEach((id,i) => o[['plot','context','diction','tone','fig','sym','tkam'][i]] = pick(id));
    return o;
  }, FILES);

  const parts = Object.values(seed);

  // v136's orphan trap: a classId CLASS_BY_ID doesn't know fails silently.
  ck('all seven load under the real english classId',
     parts.every(u => u.classId === 'english'), parts.map(u=>u.classId));
  ck('all seven are prep:true — a test-prep unit wears the gold band',
     parts.every(u => u.prep), parts.map(u=>u.prep));
  ck('all seven carry a libv, so a later fix survives the approval race',
     parts.every(u => u.libv >= 1), parts.map(u=>u.libv));
  ck('no part sets order — the numbering in the title does the sorting',
     parts.every(u => u.order == null), parts.map(u=>u.order));
  ck('every title carries the structural "Test 1 · N " form',
     parts.every((u,i) => u.title.startsWith('Test 1 · ' + (i+1) + ' ')),
     parts.map(u=>u.title));

  const shelf = await p.evaluate(() => {
    const s = shelvesFor('english');
    const f = n => (s.shelves.find(x=>x.name===n)||{units:[]}).units.map(u=>lessonLabel(u));
    return {names: s.shelves.map(x=>x.name), t1: f('Test 1'),
            tkam: f('To Kill a Mockingbird').length, loose: s.loose.map(u=>u.title)};
  });
  ck('a "Test 1" shelf exists holding exactly seven parts',
     shelf.t1.length === 7, shelf.t1);
  ck('the shelf ascends 1..7 in teaching order, by title alone',
     shelf.t1.every((l,i) => l.startsWith(String(i+1) + ' ')), shelf.t1);
  ck('the reading companion keeps its own shelf and nothing fell loose',
     shelf.tkam === 1 && shelf.loose.length === 0, shelf);

  // Structure, plus the v181 _balance bug pinned per unit.
  for (const [nm, u] of Object.entries(seed)) {
    const mc = u.qs.filter(q => (q.kind||'mc') === 'mc');
    const ord = u.qs.filter(q => q.kind === 'order');
    ck(nm + ': every question has four unique options and a valid answer',
       mc.length + ord.length === u.qs.length &&
       u.qs.every(q => q.opts.length === 4 && new Set(q.opts).size === 4) &&
       mc.every(q => q.ans >= 0 && q.ans < 4) && ord.every(q => q.ans === 0),
       {mc: mc.length, order: ord.length, total: u.qs.length});
    const slots = [0,1,2,3].map(i => mc.filter(q => q.ans === i).length);
    ck(nm + ': answers are spread across all four slots, not all A', slots.every(n => n > 0), slots);
    ck(nm + ': at least 12 questions across all three levels',
       u.qs.length >= 12 && [1,2,3].every(lv => u.qs.some(q => q.lv === lv)), u.qs.length);
  }

  const all7 = parts.reduce((a,u) => a.concat(u.qs), []);
  ck('no stem opens on a neighbouring question’s scenario',
     !all7.some(q => /^(That same|The same|For that same|Using the same)\b/i.test(q.q)) &&
     !all7.some(q => /that same/i.test(q.q)),
     all7.filter(q => /same/i.test(q.q)).map(q=>q.q.slice(0,46)).slice(0,4));
  ck('nothing refers to an option by position',
     !all7.some(q => /\b(all|none) of the above\b|\b(first|second|third|last) (option|choice)\b/i
       .test([q.q, q.ex.main, q.ex.tip].concat(q.steps, q.opts).join(' '))), 'ok');
  ck('every question carries 3-6 walkthrough steps',
     all7.every(q => q.steps.length >= 3 && q.steps.length <= 6), 'ok');
  ck('no question points a reader back at her own notes',
     !all7.some(q => /\b(your|her|the) (notes?|worksheet|packet|page)\b/i.test(q.q)),
     all7.filter(q => /notes?|worksheet/i.test(q.q)).map(q=>q.q.slice(0,50)));

  /* Per part, asserted by its TEACHING. */
  ck('diction: all eight kinds are on the cards',
     ['Formal diction','Informal diction','Pedantic diction','Colloquial diction',
      'Slang diction','Abstract diction','Concrete diction','Poetic diction']
       .every(t => seed.diction.cards.some(c => c.term === t)),
     seed.diction.cards.map(c=>c.term));
  ck('diction: both blurred pairs get a card of their own',
     seed.diction.cards.some(c => /Formal or pedantic/.test(c.term)) &&
     seed.diction.cards.some(c => /Colloquial or slang/.test(c.term)),
     seed.diction.cards.map(c=>c.term).slice(4,8));
  ck('diction: teaches concrete as appealing to the SENSES',
     /appeal to the senses/i.test(seed.diction.blob), 'card');
  ck('diction: the parentNote flags the "appeal to the specific" line for a grown-up',
     /appeal to the specific/.test(seed.diction.note) && /SENSES/.test(seed.diction.note),
     seed.diction.note.slice(0,60));
  ck('diction: none of her own example sentences is reused as a graded question',
     !seed.diction.qs.some(q => /right away|I’ve got this|expound on|pretty sus|ate an apple/i.test(q.q)),
     'fresh');

  /* The OCR trap: "style and voice" is a reason to USE tone, not a thing
     tone is not. Getting this backwards would teach the opposite. */
  ck('tone: style and voice is taught as something tone DOES',
     /Six reasons[\s\S]{0,220}establishes style and voice/.test(seed.tone.blob) &&
     seed.tone.qs.some(q => /style and voice is listed as one of the things tone DOES/i.test(q.q)),
     'card + question');
  ck('tone: the three things tone is NOT each get their own card',
     ['Tone is not: character','Tone is not: narrator','Tone is not: mood']
       .every(t => seed.tone.cards.some(c => c.term === t)),
     seed.tone.cards.map(c=>c.term));
  ck('tone: both determiner lists are taught, and diction is named as the overlap',
     /diction, imagery, details and syntax/i.test(seed.tone.blob) &&
     /setting, figurative language, diction, and genre and plot/i.test(seed.tone.blob) &&
     /Diction appears on BOTH lists/i.test(seed.tone.blob), 'cards');
  ck('tone: the whose-feeling-is-it test is stated outright',
     /the author['’]s is tone, the reader['’]s is mood/i.test(seed.tone.blob), 'card');
  ck('tone: three questions carry an original passage, each under 45 words',
     seed.tone.qs.filter(q => q.passage).length === 3 &&
     seed.tone.qs.filter(q => q.passage).every(q => q.passage.split(/\s+/).length < 45),
     seed.tone.qs.filter(q=>q.passage).map(q=>q.passage.split(/\s+/).length));

  ck('figurative: all seventeen devices are on the cards',
     ['Simile','Standard metaphor','Implied metaphor','Extended metaphor','Personification',
      'Imagery','Hyperbole','Understatement','Litotes','Euphemism','Synecdoche','Oxymoron',
      'Pun','Allusion','Alliteration','Anaphora','Idioms']
       .every(t => seed.fig.cards.some(c => c.term === t)),
     seed.fig.cards.map(c=>c.term));
  ck('figurative: all five kinds of imagery are named with their senses',
     /visual is sight/i.test(seed.fig.blob) && /auditory is hearing/i.test(seed.fig.blob) &&
     /olfactory is smell/i.test(seed.fig.blob) && /tactile is touch/i.test(seed.fig.blob) &&
     /gustatory\s+is taste/i.test(seed.fig.blob), 'card');
  ck('figurative: litotes is taught as a KIND of understatement, not a rival to it',
     /All litotes is understatement; not all understatement is litotes/.test(seed.fig.blob),
     'card');
  ck('figurative: the parentNote flags her narrow pun definition',
     /pun line/.test(seed.fig.note) && /two meanings at\s*once/.test(seed.fig.note),
     seed.fig.note.slice(0,60));
  ck('figurative: the extended-metaphor question carries its own passage',
     seed.fig.qs.some(q => q.passage && /Extended metaphor/.test(q.opts[q.ans])),
     'passage');

  ck('symbolism: repetition is what makes a motif, and it is pinned',
     /A symbol can appear once; a motif has to repeat/.test(seed.sym.blob) &&
     seed.sym.qs.some(q => /repeats throughout the text/i.test(q.opts[q.ans])), 'card + question');
  ck('symbolism: motif against theme is taught as concrete against idea',
     /A motif is concrete and repeats; the theme is the idea it leads back to/.test(seed.sym.blob),
     'card');
  ck('symbolism: says outright the traditional meanings are a starting point',
     /starting point/i.test(seed.sym.blob) &&
     seed.sym.qs.some(q => /starting points, not fixed rules/.test(q.opts[q.ans])),
     'card + question');
  ck('symbolism: her class’s own three literature examples are on the cards',
     /Flipped/.test(seed.sym.blob) && /Frederick\s+Douglass/.test(seed.sym.blob) &&
     /Midsummer Night’s Dream/.test(seed.sym.blob), 'card');

  ck('tkam: the four hard facts are all on the cards',
     /Harper Lee/.test(seed.tkam.blob) && /published in 1960/i.test(seed.tkam.blob) &&
     /Maycomb, Alabama, 1933/.test(seed.tkam.blob) && /father was a lawyer/i.test(seed.tkam.blob),
     'cards');
  ck('tkam: all three conditions of the 1930s are taught',
     /Great Depression/.test(seed.tkam.blob) && /legal segregation/i.test(seed.tkam.blob) &&
     /Ignorance is named as the third condition/.test(seed.tkam.blob), 'cards');
  ck('tkam: the 1933-1935 against 1960 gap is taught, not just the two dates',
     /looking BACK at that decade/.test(seed.tkam.blob) &&
     seed.tkam.qs.some(q => /looks back on the 1930s from later/.test(q.opts[q.ans])),
     'card + question');
  /* The scoping claim: this must not re-ask the ch.1-5 companion's material. */
  const tkamSeen = JSON.stringify([seed.tkam.cards, seed.tkam.qs]);
  ck('tkam: nothing SHE sees re-asks the chapters 1-5 reading companion',
     !/Boo Radley|Scout|Jem|Atticus|Dill|knothole|Calpurnia/i.test(tkamSeen),
     (tkamSeen.match(/Boo Radley|Scout|Jem|Atticus|Dill/gi)||[]).slice(0,5));
  ck('tkam: the parentNote says it was scoped against that companion',
     /chapters 1 to 5/i.test(seed.tkam.note), seed.tkam.note.slice(0,70));

  // The gold prep treatment, on the shelf and on an opened card.
  const gold = await p.evaluate(() => {
    go('shelf', {classId:'english', series:'Test 1', open:'unit-eng-t1-tone'});
    const stops = [...document.querySelectorAll('#screen .stop')];
    const prep = stops.filter(s => s.classList.contains('prep'));
    const pip = prep[0] && prep[0].querySelector('.pip');
    const oc = document.getElementById('shelfopen');
    return {stops: stops.length, prepStops: prep.length,
            pipGold: pip ? getComputedStyle(pip).borderColor : null,
            isPrepCard: oc ? oc.classList.contains('prepcard') : false,
            band: oc && oc.querySelector('.prepband') ? oc.querySelector('.prepband').textContent : null,
            title: oc ? oc.querySelector('h3').textContent : null};
  });
  ck('every one of the seven stops is gold-ringed as test prep',
     gold.stops === 7 && gold.prepStops === 7 && /242, 202, 99/.test(gold.pipGold||''), gold);
  ck('the opened part wears the Test prep band and is the one that was tapped',
     gold.isPrepCard && /Test prep/i.test(gold.band||'') && /4 Tone and Mood/.test(gold.title||''),
     gold);

  // Every part plays a full round end to end.
  for (const [nm, u] of Object.entries(seed)) {
    const play = await p.evaluate(async (uid) => {
      quizState = null;
      go('quiz', {unitId: uid, classId: 'english'});
      let guard = 0;
      while (view === 'quiz' && guard++ < 90) {
        const opts = [...document.querySelectorAll('#screen .opt:not([disabled])')];
        if (opts.length) for (const o of opts) { o.click(); await new Promise(r=>setTimeout(r,4)); }
        await new Promise(r=>setTimeout(r,8));
        const next = document.querySelector('#screen .btn-primary, #screen .explain.go-on');
        if (next) { next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
        if (!opts.length) break;
      }
      const l = all('log').find(x => x.unitId === uid && x.mode === 'quiz');
      return {logged: !!l, total: l && l.total};
    }, u.id);
    ck(nm + ': a full quiz round plays and logs', play.logged && play.total === 5, play);
  }

  // A passage really renders on the question it belongs to.
  const pass = await p.evaluate(() => {
    const u = DATA.records['unit-eng-t1-tone'];
    const q = u.questions.find(x => x.passage);
    quizState = null;
    go('quiz', {unitId:u.id, classId:'english'});
    quizState.order = [u.questions.indexOf(q)]; quizState.i = 0;
    render();
    const n = document.querySelector('#screen .passage');
    return {shown: !!n, text: n ? n.textContent.slice(0,40) : null,
            want: q.passage.slice(0,40)};
  });
  ck('a passage renders as its own plate above the question',
     pass.shown && pass.text === pass.want, pass);

  const deck = await p.evaluate(async (uid) => {
    cardState = {}; go('cards', {unitId: uid, classId: 'english'});
    let seen = 0;
    while (cardState.unitId === uid && seen++ < 40) {
      const knew = [...document.querySelectorAll('button')].find(b => /Knew it/.test(b.textContent));
      if (!knew) break;
      knew.click(); await new Promise(r=>setTimeout(r,5));
    }
    return {seen};
  }, 'unit-eng-t1-fig');
  ck('the figurative-language deck steps all the way through its 22 cards',
     deck.seen >= 22, deck);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
