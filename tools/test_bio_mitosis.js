/* Biology 8 · Unit 4-1: The Cell Cycle and Mitosis (v197).

   Pins the unit by its TEACHING rather than by question id, which would not
   survive a renumber — the v185/v194 rule. The two assertions that matter
   most are the ones about the sources disagreeing with each other:

     * checkpoints and apoptosis are GRADED on the video worksheet and appear
       nowhere in the 39-slide deck, so the unit has to carry them;
     * the deck's cytokinesis slide says "(chromosome reduction)", which is
       meiosis's property, not mitosis's — and the worksheet's own fruit-fly
       question grades the opposite. The unit must teach that a daughter cell
       keeps the parent's chromosome number, and must never say otherwise.

   Verified by stripping the checkpoint/apoptosis cards and flipping the
   chromosome-number question, and watching exactly those assertions fail. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
const UID = 'unit-bio-u4';

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  /* Seed the WHOLE Biology shelf, not just the new unit — "it shelves in the
     right place" is a claim about coexistence, and the v180 ordering bug was
     only ever visible with every lesson present at once. */
  const seeded = await p.evaluate(async ()=>{
    const files = CONTENT_LIBRARY.filter(f=>/bio-/.test(f));
    for(const f of files){
      try{ const j = await (await fetch(f)).json();
        Object.values(j.records).forEach(r=>{ if(r&&r.type){ r.status='approved'; delete r.releaseOn; put(r); } });
      }catch(e){}
    }
    saveLocal();
    const u = DATA.records['unit-bio-u4'];
    if(!u) return {missing:true};
    return { id:u.id, classId:u.classId, title:u.title, libv:u.libv, order:u.order,
             cards:u.cards.length, qs:u.questions.length,
             withImg:u.cards.filter(c=>c.imgUrl).length };
  });
  if(seeded.missing){ console.log('FAIL unit-bio-u4 not in the library'); process.exit(1); }

  ck('the unit loads with libv and no order bucket',
     seeded.id===UID && seeded.libv>=1 && !seeded.order, seeded);
  ck('classId is "bio" — the real id, not "biology" (the v136 orphan trap)',
     seeded.classId==='bio', seeded.classId);
  /* A MINIMUM, never an exact count: a unit must be free to grow when her
     work shows a gap (the v195 / test_phases lesson). */
  ck('at least 20 cards and 18 questions', seeded.cards>=20 && seeded.qs>=18, seeded);
  ck('it carries the numbered form its shelf requires (v180)',
     /^Biology 8 · Unit 4-1: /.test(seeded.title), seeded.title);

  // ---- the whole shelf, ascending, every lesson numbered
  const shelf = await p.evaluate(()=>{
    const sh = shelvesFor('bio');
    const book = sh.shelves.find(s=>/Biology 8/.test(s.name));
    return book ? { name:book.name, loose:sh.loose.length,
                    parts: book.lessons.map(u=>u.title.replace(/^Biology 8 · /,'')) } : null;
  });
  const lessons = (shelf&&shelf.parts||[]).filter(t=>/^Unit \d+-\d+:/.test(t));
  const keyOf = t => { const m=t.match(/^Unit (\d+)-(\d+):/); return m?[+m[1],+m[2]]:null; };
  const ascending = lessons.every((t,i)=>{
    if(!i) return true; const a=keyOf(lessons[i-1]), c=keyOf(t);
    return a && c && (c[0]>a[0] || (c[0]===a[0] && c[1]>a[1]));
  });
  ck('the Biology 8 shelf exists and holds the new unit', !!shelf && shelf.parts.some(t=>/Unit 4-1/.test(t)), shelf);
  ck('every lesson on the shelf carries the numbered form — one bare title reintroduces the v180 inversion',
     lessons.length===(shelf&&shelf.parts||[]).filter(t=>!/Study Guide|Quiz Review/.test(t)).length,
     shelf&&shelf.parts);
  ck('the shelf ascends by unit then part, Unit 1-1 through Unit 4-1', ascending, lessons);

  // ---- the v181 _balance bug: answers must not all sit in one slot
  const slots = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const c = {};
    u.questions.filter(q=>(q.kind||'mc')==='mc').forEach(q=>{ c[q.ans]=(c[q.ans]||0)+1; });
    return c;
  }, UID);
  ck('correct answers are spread across all four slots (the v181 _balance bug, pinned)',
     Object.keys(slots).length===4, slots);

  // ---- standalone rules
  const clean = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const POS = /\b(all|none) of the above\b|\boptions? [a-d1-4]\b|\b(first|second|third|last) (option|choice)\b/i;
    const BACK = /^(the|that) same\b|\bthat same\b/i;
    return { pos: u.questions.filter(q=>POS.test(JSON.stringify(q))).map(q=>q.id),
             back: u.questions.filter(q=>BACK.test(q.q)).map(q=>q.id) };
  }, UID);
  ck('no positional references and no back-referencing stems', !clean.pos.length && !clean.back.length, clean);

  // ---- THE GAP: checkpoints and apoptosis are graded and are not in the deck
  const gap = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const blob = c => (c.term+' '+c.def+' '+(c.hint||''));
    const cp = u.cards.find(c=>/checkpoint/i.test(blob(c)));
    const ap = u.cards.find(c=>/apoptosis/i.test(blob(c)));
    const cpq = u.questions.find(q=>/how many checkpoints/i.test(q.q));
    const apq = u.questions.find(q=>/apoptosis/i.test(JSON.stringify(q)));
    return {
      cpCard: cp ? {term:cp.term, three:/\bthree\b/i.test(cp.def), from:cp.from} : null,
      apCard: ap ? {term:ap.term, from:ap.from,
                    programmed:/programmed cell death/i.test(ap.def)} : null,
      cpQ: cpq ? {id:cpq.id, ans:cpq.opts[cpq.ans]} : null,
      apQ: !!apq };
  }, UID);
  ck('a card teaches the three checkpoints, tagged as our addition since the deck cannot source it',
     gap.cpCard && gap.cpCard.three && gap.cpCard.from==='added', gap.cpCard);
  ck('a card teaches apoptosis as programmed cell death, also tagged added',
     gap.apCard && gap.apCard.programmed && gap.apCard.from==='added', gap.apCard);
  ck('a graded question asks how many checkpoints, and the answer is three',
     gap.cpQ && /three/i.test(gap.cpQ.ans), gap.cpQ);
  ck('apoptosis is asked about too, not just defined', gap.apQ, gap.apQ);

  // ---- THE SLIDE CONTRADICTION: mitosis preserves the chromosome number
  const number = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const q = u.questions.find(x=>/how many chromosomes are in EACH daughter cell/i.test(x.q));
    const whole = JSON.stringify(u);
    return {
      q: q ? {id:q.id, stem:q.q, ans:q.opts[q.ans], opts:q.opts} : null,
      // the slide's own wording must not appear anywhere in what she sees
      reduction: /chromosome reduction/i.test(whole),
      // and the parentNote must flag it for a grown-up
      noteFlags: /chromosome reduction/i.test(u.parentNote.text),
      noteFlagsCheckpoints: /checkpoint/i.test(u.parentNote.text) };
  }, UID);
  const stated = number.q && (number.q.stem.match(/(\d+) chromosomes/)||[])[1];
  ck('a question asks what each daughter cell ends up with, and the answer PRESERVES the parent count',
     number.q && stated && number.q.ans===stated, {q:number.q, stated});
  ck('the deck\'s "chromosome reduction" wording never reaches her side of the app',
     !number.reduction || number.noteFlags, {anywhere:number.reduction, inNote:number.noteFlags});
  ck('parentNote flags BOTH source problems — the missing checkpoints and the reduction slide',
     number.noteFlags && number.noteFlagsCheckpoints,
     {reduction:number.noteFlags, checkpoints:number.noteFlagsCheckpoints});

  // ---- the counting rule, and mitosis vs cytokinesis
  const taught = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    /* Sweep the HINT too. She reads it, so it counts as taught — and the
       first version of this test failed on a card whose teaching was
       perfectly present, just one field over. */
    const all = u.cards.map(c=>c.term+' '+c.def+' '+(c.hint||'')).join(' \n ');
    const cyto = u.cards.find(c=>/^Cytokinesis$/i.test(c.term));
    const mit = u.cards.find(c=>/^Mitosis/i.test(c.term));
    return {
      centromeres: /centromeres for chromosomes/i.test(all) && /strands for chromatids/i.test(all),
      g0: /NOT (one of )?the cell cycle's phases|not one of them|NOT in the cycle/i.test(all),
      sphase: /ONLY phase where the DNA is copied/i.test(all),
      cytoDividesCytoplasm: !!cyto && /cytoplasm/i.test(cyto.def),
      mitDividesNucleus: !!mit && /nucleus/i.test(mit.def),
      plantVsAnimal: /cleavage furrow/i.test(all) && /cell plate/i.test(all) };
  }, UID);
  ck('the counting rule is taught explicitly — centromeres for chromosomes, strands for chromatids',
     taught.centromeres, taught);
  ck('G0 is taught as being OUTSIDE the cycle, not as one of its phases', taught.g0, taught);
  ck('S phase is named as the only place DNA is copied', taught.sphase, taught);
  ck('mitosis divides the nucleus and cytokinesis divides the cytoplasm — kept distinct',
     taught.mitDividesNucleus && taught.cytoDividesCytoplasm, taught);
  ck('both cytokinesis routes are taught: cleavage furrow and cell plate', taught.plantVsAnimal, taught);

  // ---- no images anywhere: the deck's own are Pearson's, deliberately not reused
  const noImg = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    return { cards: u.cards.filter(c=>c.imgUrl).length,
             qs: u.questions.filter(q=>q.imgUrl ||
                 /\b(diagram|image|picture) (shown|above|below)\b/i.test(q.q)).map(q=>q.id) };
  }, UID);
  ck('no card or question carries or points at an image — the deck\'s figures are copyrighted',
     noImg.cards===0 && noImg.qs.length===0, noImg);

  // ---- the kind:'order' question really is stored in the correct sequence
  const ord = await p.evaluate((UID)=>{
    const oq = DATA.records[UID].questions.find(q=>q.kind==='order');
    return oq ? {id:oq.id, ans:oq.ans, opts:oq.opts} : null;
  }, UID);
  ck('the cell-cycle ordering question ships in the correct sequence: replicate, line up, separate, pinch',
     ord && ord.ans===0 && ord.opts.length===4 && /replicated/i.test(ord.opts[0])
       && /line up|lined up|across the middle/i.test(ord.opts[1])
       && /opposite ends/i.test(ord.opts[2]) && /cleavage furrow/i.test(ord.opts[3]), ord);

  // ---- a full round plays, and the deck walks to the end
  const round = await p.evaluate((UID)=>{
    /* go('quiz') builds its own quizState, so navigate FIRST and steer the
       round it built — one assembled beforehand is thrown away (v194). */
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
    return {built:true, n, right};
  }, UID);
  ck('a full quiz round plays and every correct answer scores',
     round.built && round.n>0 && round.right===round.n, round);

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
  ck('the flashcard deck walks to the end with every card rendering',
     deck.seen===deck.total, deck);

  let bad=0;
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got).slice(0,320)); }
                   else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
