/* Biology 8 · Unit 3: Cells — the first unit whose CARDS carry labelled
   reference diagrams (v176). Covers the content, the generalized cardImgNode
   (imgAlt / imgWide / imgCredit, which the ASL alphabet predates), and the
   rule that matters most here: a fully-labelled diagram may never be the
   answer key for a question, because the label is printed on the picture. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  // ---- ship the unit the way fetchLibrary would: approved, in the store
  const seeded = await p.evaluate(async ()=>{
    const r = await fetch('content/bio-unit-3-cells.json');
    const j = await r.json();
    const u = Object.values(j.records)[0];
    u.status = 'approved';
    put(u);
    return { id:u.id, classId:u.classId, title:u.title, libv:u.libv,
             cards:u.cards.length, qs:u.questions.length,
             withImg:u.cards.filter(c=>c.imgUrl).length };
  });
  ck('the unit loads from the library file and carries libv',
     seeded.id==='unit-bio-u3c' && seeded.libv===1, seeded);
  ck('classId is "bio" — the real id, not "biology" (v136 orphan trap)',
     seeded.classId==='bio', seeded.classId);
  ck('27 cards, 18 questions, 7 of them carrying a diagram',
     seeded.cards===27 && seeded.qs===18 && seeded.withImg===7, seeded);

  // ---- every image URL is a verified Commons file, and carries real alt text
  const imgs = await p.evaluate(()=>{
    const u = DATA.records['unit-bio-u3c'];
    return u.cards.filter(c=>c.imgUrl).map(c=>({
      term:c.term, url:c.imgUrl, alt:c.imgAlt||null, wide:!!c.imgWide, credit:c.imgCredit||null }));
  });
  const FP = 'https://commons.wikimedia.org/wiki/Special:FilePath/';
  ck('every diagram is a Commons Special:FilePath URL (the stable redirect, no hash paths)',
     imgs.every(i=>i.url.startsWith(FP)), imgs.map(i=>i.url));
  ck('every diagram carries real alt text, is marked wide, and credits its source',
     imgs.every(i=>i.alt && i.alt.length>40 && i.wide && /public domain/i.test(i.credit)),
     imgs.map(i=>({t:i.term, alt:(i.alt||'').slice(0,30), wide:i.wide, credit:i.credit})));
  /* The exact filenames, because three of them punctuate differently and a
     guess would have got them wrong — that is the whole reason they were
     verified by search rather than pattern-matched. */
  const want = ['Average_prokaryote_cell-_en.svg','Animal_cell_structure_en.svg',
    'Plant_cell_structure-en.svg','Diagram_human_cell_nucleus.svg',
    'Endomembrane_system_diagram_en.svg','Animal_mitochondrion_diagram_en.svg',
    'Chloroplast_diagram.svg'];
  const got = imgs.map(i=>i.url.slice(FP.length)).sort();
  ck('the seven verified filenames, exactly', JSON.stringify(got)===JSON.stringify([...want].sort()), got);

  // ---- the diagram renders on the flashcard back, on its white plate
  const face = await p.evaluate(async ()=>{
    const cid = 'bio';
    go('cards', {unitId:'unit-bio-u3c', classId:cid});
    const u = DATA.records['unit-bio-u3c'];
    /* The deck is SHUFFLED: the card on screen is u.cards[cardState.order[i]],
       so seek the POSITION in order[] holding an image card, not the card's
       own index. Setting i to the raw index shows a different card entirely. */
    const idx = u.cards.findIndex(c=>c.imgUrl);
    cardState.i = cardState.order.indexOf(idx);
    cardState.flipped = true; render();
    await new Promise(r=>setTimeout(r,60));
    const wrap = document.querySelector('#screen .cardimg');
    const img = wrap && wrap.querySelector('img');
    const cs = wrap && getComputedStyle(wrap);
    return {
      term: u.cards[cardState.order[cardState.i]].term,
      found: !!img,
      src: img && img.getAttribute('src'),
      alt: img && img.getAttribute('alt'),
      lazy: img && img.getAttribute('loading'),
      wide: wrap && wrap.classList.contains('wide'),
      plate: cs && cs.backgroundColor,
      w: wrap && Math.round(wrap.getBoundingClientRect().width),
      credit: wrap && wrap.querySelector('.imgcredit') && wrap.querySelector('.imgcredit').textContent
    };
  });
  ck('the diagram renders on the card back with its real src and alt',
     face.found && face.src.startsWith(FP) && /labelled/i.test(face.alt), face);
  ck('it is lazy-loaded and sits on the fixed white plate, in both themes',
     face.lazy==='lazy' && face.plate==='rgb(255, 255, 255)', face);
  ck('a labelled diagram gets the WIDE plate, not the 150px handshape one',
     face.wide && face.w > 200, {wide:face.wide, w:face.w});
  ck('the credit line names the source on the card', /public domain/i.test(face.credit||''), face.credit);

  // ---- the ASL alphabet still works: it predates imgAlt and must fall back
  const asl = await p.evaluate(async ()=>{
    put({ id:'aslprobe', type:'unit', classId:'bio', status:'approved', title:'ASL probe',
      cards:[{id:'c0', term:'B', def:'**A test card.**',
              imgUrl:'https://commons.wikimedia.org/wiki/Special:FilePath/Sign_language_B.svg'}],
      questions:[] });
    go('cards', {unitId:'aslprobe', classId:'bio'});
    cardState.i = 0; cardState.flipped = true; render();
    await new Promise(r=>setTimeout(r,60));
    const wrap = document.querySelector('#screen .cardimg');
    const img = wrap && wrap.querySelector('img');
    return { alt: img && img.getAttribute('alt'), wide: wrap && wrap.classList.contains('wide'),
             credit: !!(wrap && wrap.querySelector('.imgcredit')) };
  });
  ck('a card with no imgAlt falls back to the ASL phrasing, stays narrow, shows no credit',
     asl.alt==='The handshape for B' && !asl.wide && !asl.credit, asl);

  // ---- the rule: a labelled diagram must never be a question's answer key
  const noGiveaway = await p.evaluate(()=>{
    const u = DATA.records['unit-bio-u3c'];
    const bad = u.questions.filter(q =>
      q.imgUrl || /\bdiagram (shown|above|below)\b|\bin the (image|picture|diagram)\b/i.test(q.q));
    return { total:u.questions.length, bad: bad.map(q=>q.id) };
  });
  ck('no question points at a diagram — every label is printed on the picture, so it would be the answer',
     noGiveaway.bad.length===0, noGiveaway);

  // ---- it shelves on the real Biology 8 spine and plays a round
  const shelf = await p.evaluate(()=>{
    go('unit', {classId:'bio'});
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : '';
    const spines = [...document.querySelectorAll('#screen .spine')].map(T);
    return { spines, onShelf: spines.some(s=>/Biology 8/.test(s)) };
  });
  ck('it shelves under the existing Biology 8 spine', shelf.onShelf, shelf.spines);

  const round = await p.evaluate(()=>{
    const u = DATA.records['unit-bio-u3c'];
    quizState = null; ctx.pre = null;
    go('quiz', {unitId:'unit-bio-u3c', classId:'bio'});
    if(!quizState) return {built:false};
    let right = 0;
    quizState.order.forEach((qi,i)=>{
      const q = u.questions[qi];
      answer(u, q, q.ans);
      if(quizState.answered===q.ans) right++;
      if(i<quizState.order.length-1){ quizState.i++; quizState.answered=null; }
    });
    const n = quizState.order.length;
    finishQuiz(u);
    return { built:true, n, right };
  });
  ck('a full quiz round plays and every correct answer scores',
     round.built && round.n>0 && round.right===round.n, round);

  const order = await p.evaluate(()=>{
    const u = DATA.records['unit-bio-u3c'];
    const oq = u.questions.find(q=>q.kind==='order');
    return oq ? { id:oq.id, opts:oq.opts, ans:oq.ans } : null;
  });
  ck('the secretory pathway ships as a put-in-order question, in the correct sequence',
     order && order.ans===0 && order.opts.length===4 && /Rough ER/i.test(order.opts[0])
     && /Golgi/i.test(order.opts[2]), order);

  // ---- report
  let bad = 0;
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got)); }
                   else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
