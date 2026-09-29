/* Biology 8 · Test 2 Study Guide (content/bio-sg-test2.json, v200).

   Pins COVERAGE of the teacher's guide, blank by blank, rather than question
   ids — the guide is the syllabus for Wednesday's test, and the thing a later
   edit must not quietly lose is one of its blanks. Also pins the two calls
   the class's own slides forced (the fourth kingdom named both ways, the
   cytoskeleton's prokaryote half left open), the questions-not-scoring rule
   (v198) on a filled-in upload, and the spelling practice a fill-in test
   needs.

   Verified by deleting the endosymbiont card, flipping the anaphase answer
   to 5 and prepending a made-up score to the parent note, and watching
   exactly those three assertions fail. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
const UID = 'unit-bio-sgt2';

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  /* The whole Biology shelf, so shelving is a claim about coexistence. */
  const seeded = await p.evaluate(async ()=>{
    const files = CONTENT_LIBRARY.filter(f=>/bio-/.test(f));
    for(const f of files){
      const j = await (await fetch(f,{cache:'no-store'})).json();
      Object.values(j.records).forEach(r=>{ if(r&&r.type){ r.status='approved'; delete r.releaseOn; put(r); } });
    }
    saveLocal();
    const u = DATA.records['unit-bio-sgt2'];
    return u ? { classId:u.classId, title:u.title, prep:!!u.prep, book:!!u.book, order:u.order,
                 libv:u.libv, cards:u.cards.length, qs:u.questions.length, guide:!!u.guide } : null;
  });
  if(!seeded){ console.log('FAIL unit not in CONTENT_LIBRARY'); process.exit(1); }
  ck('classId is "bio" (the v136 orphan trap)', seeded.classId==='bio', seeded.classId);
  ck('prep and book are set, order 1, libv present — and it is NOT a paper-entry guide (the real test is not multiple choice)',
     seeded.prep && seeded.book && seeded.order===1 && seeded.libv>=1 && !seeded.guide, seeded);
  ck('at least 40 cards and 30 questions (a minimum, never an exact count)',
     seeded.cards>=40 && seeded.qs>=30, seeded);

  // ---- shelf: trails the lessons with the other study guides, gold band on
  const shelf = await p.evaluate((UID)=>{
    go('shelf', {classId:'bio', series:'Biology 8', open:UID});
    const stops = [...document.querySelectorAll('#screen .stop')].map(s=>({
      t:s.querySelector('.t').textContent, prep:s.classList.contains('prep')}));
    const oc = document.getElementById('shelfopen');
    return { stops, loose: shelvesFor('bio').loose.filter(u=>u.id===UID).length,
             prepcard: !!oc && oc.classList.contains('prepcard'),
             band: !!oc && !!oc.querySelector('.prepband'),
             clock: !!oc && /Beat the clock/.test(oc.textContent),
             title: oc && oc.querySelector('h3') ? oc.querySelector('h3').textContent : null };
  }, UID);
  const idx = shelf.stops.findIndex(s=>/Test 2 Study Guide/.test(s.t));
  const lastLesson = shelf.stops.map(s=>/Unit \d+-\d+/.test(s.t)).lastIndexOf(true);
  ck('it shelves on Biology 8, after every numbered lesson, and is not left loose',
     idx>lastLesson && lastLesson>=0 && shelf.loose===0, shelf.stops.map(s=>s.t));
  ck('its stop wears the gold prep ring, and the opened card the TEST PREP band',
     shelf.stops[idx] && shelf.stops[idx].prep && shelf.prepcard && shelf.band, shelf);
  ck('no Beat the clock door (book:true)', !shelf.clock, shelf.clock);

  // ---- structure rules
  const rules = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const POS = /\b(all|none) of the above\b|\boptions? [a-d1-4]\b|\b(first|second|third|last) (option|choice)\b/i;
    const BACK = /^(the|that) same\b|\bthat same\b/i;
    const slots = {};
    u.questions.filter(q=>(q.kind||'mc')==='mc').forEach(q=>{ slots[q.ans]=(slots[q.ans]||0)+1; });
    const mcBad = u.questions.filter(q=>(q.kind||'mc')==='mc' &&
      (q.opts.length!==4 || new Set(q.opts).size!==4 || q.ans<0 || q.ans>3)).map(q=>q.id);
    return { slots, mcBad,
             pos: u.questions.filter(q=>POS.test(JSON.stringify(q))).map(q=>q.id),
             back: u.questions.filter(q=>BACK.test(q.q)).map(q=>q.id),
             boldFirst: u.cards.every(c=>c.def.startsWith('**')) };
  }, UID);
  ck('answers spread across all four slots (the v181 _balance bug)', Object.keys(rules.slots).length===4, rules.slots);
  ck('every MC question has four unique options and a valid answer', !rules.mcBad.length, rules.mcBad);
  ck('no positional references and no back-referencing stems', !rules.pos.length && !rules.back.length, rules);
  ck('every card leads with its bold answer', rules.boldFirst, rules.boldFirst);

  // ---- COVERAGE: every section of the guide, by its teaching
  const cov = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const cards = u.cards.map(c=>c.term+' '+c.def+' '+(c.hint||'')+' '+(c.eq||'')).join(' \n ');
    const has = re => re.test(cards);
    const chartRows = ['Cell membrane','Cell wall','Capsule','Nucleus','Nucleoid region','Ribosome',
      'Plasmid','Chromosome','Cytoplasm','Rough endoplasmic reticulum','Smooth endoplasmic reticulum',
      'Vesicles','Vacuoles','Golgi apparatus','Cytoskeleton','Lysosomes','Centrosomes and centrioles',
      'Mitochondria','Chloroplasts'];
    const term = t => u.cards.find(c=>c.term===t);
    return {
      cellTheory: has(/made of one or more cells/i) && has(/basic unit/i) && has(/come from existing cells/i),
      sixChars: ['obtain and use energy','grow and develop','reproduce','sense and respond','DNA as their hereditary']
                  .every(s=>cards.toLowerCase().includes(s.toLowerCase())),
      virus: has(/protein coat/i) && has(/DNA or RNA/i) && has(/lytic/i) && has(/IMMEDIATELY/) &&
             has(/lysogenic/i) && has(/shingles/i),
      domains: has(/Archaea and bacteria/i) && has(/methane/i),
      autotroph: has(/makes its own food/i) && has(/oxygen/i),
      chartRows: chartRows.filter(t=>!term(t)),
      chartPresence: chartRows.filter(t=>t!=='Cytoskeleton' && term(t) && !/Prokaryotes:/.test(term(t).def)),
      pathway: has(/Ribosome → rough ER → vesicle → Golgi apparatus → vesicle → cell membrane/),
      amounts: ['many mitochondria','NO mitochondria','many lysosomes','smooth ER','Golgi apparatus']
                  .every(s=>cards.includes(s)),
      endo: has(/engulfed an oxygen-using prokaryote/i) && has(/mitochondria and chloroplasts/i) &&
            has(/own DNA and their own ribosomes/i),
      equations: has(/C₆H₁₂O₆ \+ 6O₂ → 6CO₂ \+ 6H₂O/) && has(/6CO₂ \+ 6H₂O \+ sunlight → C₆H₁₂O₆ \+ 6O₂/),
      microscopes: has(/beam of ELECTRONS/) && has(/see living things/i),
      lensOrder: /red lens[\s\S]*Yellow lens[\s\S]*blue lens[\s\S]*fine[\s\S]*gray lens/i.test(cards),
      saRatio: has(/HIGH surface area to a LOW volume/) && has(/6s²/),
      cycle: has(/G0 branches off from G1/) && has(/DNA is replicated/),
      split: has(/about 23 hours of interphase and about 1 hour of mitosis/i),
      g0cells: has(/Red blood cells, mature neurons and the outer layer of skin/i) && has(/lower layer of skin is NEVER in G0/i),
      g1g2: has(/In G1/) && has(/in G2/) && has(/cancer/i),
      chromatin: has(/histones/i) && has(/nucleosome/i) && has(/Prokaryotic chromosomes have NO histones/),
      counting: has(/centromeres for chromosomes/i) && has(/strands for chromatids/i),
      fiveChrom: has(/5 chromosomes as 10 chromatids/) && has(/contractile ring/i),
      cellPlate: has(/cell plate/i),
      purpose: has(/Growth, development, and asexual reproduction/i),
      downside: has(/no variation/i),
      somatic: has(/somatic/i) && has(/diploid/i) && has(/gametes/i) && has(/haploid/i),
    };
  }, UID);
  const missing = Object.entries(cov).filter(([k,v])=> Array.isArray(v) ? v.length : !v).map(([k,v])=>k+(Array.isArray(v)?':'+v.join(','):''));
  ck('every section of the guide has its teaching on a card — Unit 3 and Unit 4, all nineteen chart rows with presence',
     !missing.length, missing);

  // ---- the calls the class's own slides forced
  const calls = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const k = u.cards.find(c=>/eukaryotic kingdoms/i.test(c.term));
    const cs = u.cards.find(c=>c.term==='Cytoskeleton');
    const note = u.parentNote.text;
    const addedTerms = u.cards.filter(c=>c.from==='added').map(c=>c.term);
    return {
      kingdom: !!k && /protists/i.test(k.def) && /algae/i.test(k.def),
      kingdomNote: /protists/i.test(note) && /algae/i.test(note),
      cytoPicks: !!cs && /Prokaryotes:/i.test(cs.def),
      cytoNote: /cytoskeleton/i.test(note),
      added: addedTerms,
      vesicleNote: u.cards.some(c=>c.term==='Vesicles' && /comps/i.test(c.def)) };
  }, UID);
  ck('the fourth kingdom is taught BOTH ways — protists and the class slides\' algae — and the note asks which the key wants',
     calls.kingdom && calls.kingdomNote, calls);
  ck('the cytoskeleton card does not pick a prokaryote answer, and the note says why',
     !calls.cytoPicks && calls.cytoNote, calls);
  ck('what the guide only ASKS is flagged as our addition: viruses-not-alive, the downside of mitosis, the fine knob',
     ['Why viruses are not alive','The downside of reproducing by mitosis','Why only the fine knob at high power']
       .every(t=>calls.added.includes(t)), calls.added);
  ck('the teacher\'s own vesicle note ("not needed for comps") is carried on the card', calls.vesicleNote, calls);

  // ---- the numbers, recomputed here rather than trusted
  const nums = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const find = re => u.questions.find(q=>re.test(q.q));
    const a = q => q ? q.opts[q.ans] : null;
    return {
      sa3: a(find(/sides of 3 µm/)), saCmp: a(find(/sides of 2 µm/)),
      count: a(find(/three X-shaped chromosomes and two single strands/)),
      meta: a(find(/reaches metaphase/)), ana: a(find(/During anaphase/)),
      mito24: a(find(/about how long does mitosis take/)) };
  }, UID);
  const sa = s => 6*s*s/(s**3);
  ck('SA:V for a 3 µm cube is 2 to 1', nums.sa3===`${sa(3)} to 1`, nums.sa3);
  ck('the 2 µm cube wins at 3 to 1 against 1.2 to 1', /^A\b/.test(nums.saCmp||'') && nums.saCmp.includes(`${sa(2)} to 1`) && nums.saCmp.includes(`${sa(5)} to 1`), nums.saCmp);
  ck('three X\'s and two singles: 5 chromosomes, 8 chromatids', nums.count==='5 chromosomes, 8 chromatids', nums.count);
  ck('a 5-chromosome cell lines up 10 chromatids at metaphase and moves 10 chromosomes in anaphase',
     nums.meta==='10' && nums.ana==='10 chromosomes', nums);
  ck('mitosis is about 1 hour of a 24-hour cycle', nums.mito24==='About 1 hour', nums.mito24);

  // ---- the microscope: an order question stored in order, and a spot-the-mistake item
  const micro = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const o = u.questions.find(q=>q.kind==='order');
    const m = u.questions.filter(q=>/A student/.test(q.q) && /lens/.test(q.q));
    return { o: o ? {ans:o.ans, opts:o.opts} : null, mistakes:m.length };
  }, UID);
  ck('the microscope order question is stored light → red → coarse → yellow',
     micro.o && micro.o.ans===0 && /light/i.test(micro.o.opts[0]) && /red/i.test(micro.o.opts[1]) &&
     /coarse/i.test(micro.o.opts[2]) && /yellow/i.test(micro.o.opts[3]), micro.o);
  ck('at least two questions show a student mid-mistake with a lens, as the teacher\'s note warns',
     micro.mistakes>=2, micro.mistakes);

  // ---- spelling: the test is fill-in-the-blank
  const spell = await p.evaluate(async (UID)=>{
    const u = DATA.records[UID];
    const sp = u.questions.filter(q=>q.kind==='spell');
    const words = sp.map(q=>q.opts[0]);
    const leak = sp.filter(q=>q.q.toLowerCase().includes(q.opts[0].toLowerCase())).map(q=>q.id);
    /* Play one for real: render it, type the word, press Check. */
    quizState = null; ctx.pre = null;
    go('quiz', {unitId:UID, classId:'bio'});
    const q0 = sp[0];
    quizState.order = [u.questions.indexOf(q0)]; quizState.i = 0; quizState.answered = null; render();
    const inp = document.querySelector('#screen input[type=text]');
    let right = null;
    if(inp){
      inp.value = q0.opts[0].toUpperCase(); inp.dispatchEvent(new Event('input'));
      const btn = [...document.querySelectorAll('#screen button')].find(x=>/Check my spelling/.test(x.textContent));
      if(btn){ btn.click(); right = quizState.answered === q0.ans; }
    }
    quizState = null;
    return { n:sp.length, words, leak, rendered:!!inp, right };
  }, UID);
  ck('at least six spelling questions, on the words a blank will ask for',
     spell.n>=6 && ['somatic','haploid','gametes','histones','cytokinesis','archaea'].every(w=>spell.words.includes(w)), spell.words);
  ck('no spelling prompt prints its own word', !spell.leak.length, spell.leak);
  ck('a spelling question renders an input and accepts the word typed in any case', spell.rendered && spell.right, spell);

  // ---- v198: a filled-in upload is read for its questions, never marked
  const privacy = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    /* The test's date, 9/30, is a date and not a mark — strip it before the sweep. */
    const whole = JSON.stringify(u).replace(/Wednesday 9\/30/g,'');
    return {
      marks: /\b\d+\s*(\/|out of)\s*\d+\b(?! µm)|she (got|wrote|put|answered)|her answers?|scored|\bmarked (right|wrong)\b|she missed/i.test(whole),
      readForQuestions: /read for what the guide ASKS/.test(u.parentNote.text) && /Nothing on it was marked/i.test(u.parentNote.text),
      names: /Ortiz|Sedona|8Ni\b/i.test(whole) };
  }, UID);
  ck('no mark, tally or "she wrote" anywhere in the shipped record (v198)', !privacy.marks, privacy);
  ck('the parent note says the filled-in copy was read for its questions and not marked', privacy.readForQuestions, privacy);
  ck('no name from the paper reaches the public repo', !privacy.names, privacy);

  // ---- a full round plays, and the deck walks to the end
  const round = await p.evaluate((UID)=>{
    quizState = null; ctx.pre = null;
    go('quiz', {unitId:UID, classId:'bio'});
    if(!quizState) return {built:false};
    const u = unitFor(UID);
    let right=0;
    quizState.order.forEach((qi,i)=>{
      const q = u.questions[qi];
      answer(u, q, q.ans);
      if(quizState.answered===q.ans) right++;
      if(i<quizState.order.length-1){ quizState.i++; quizState.answered=null; }
    });
    const n = quizState.order.length;
    finishQuiz(u);
    return {built:true, n, right, logged: all('log').some(l=>l.unitId===UID)};
  }, UID);
  ck('a full quiz round plays, every correct answer scores, and it logs',
     round.built && round.n>0 && round.right===round.n && round.logged, round);

  const deck = await p.evaluate(async (UID)=>{
    go('cards', {unitId:UID, classId:'bio'});
    const total = DATA.records[UID].cards.length;
    let seen=0;
    for(let i=0;i<total;i++){
      cardState.i=i; cardState.flipped=true; render();
      await new Promise(r=>setTimeout(r,4));
      if(document.querySelector('#screen .face')) seen++;
    }
    return {total, seen};
  }, UID);
  ck('the flashcard deck walks to the end with every card rendering', deck.seen===deck.total, deck);

  let bad=0;
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got).slice(0,400)); }
                   else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
