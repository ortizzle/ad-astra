/* Biology 8 · Unit 5-1: Meiosis.

   Modelled on test_bio_mitosis.js, and pins the unit by its TEACHING rather
   than by question id (the v185/v194 rule). The new unit is fetched straight
   from content/ and put into the store, alongside every content/bio-*.json
   file, so it does not depend on CONTENT_LIBRARY listing it yet.

   The assertions that matter most are the two places the sources disagree:
     * the note outline says meiosis starts from "somatic cells"; the deck
       says germline cells, and germline is what the unit must teach;
     * one slide reads as though the cell turns haploid only at the end of
       meiosis II; the outline and the deck's own knowledge check put it at
       the end of meiosis I, and a graded question must say so.
   Plus every chromosome/chromatid count re-derived here from the stem.

   Usage: node tools/test_bio_meiosis.js <port> */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8421;
const UID = 'unit-bio-u5';
const BIO_FILES = ['content/bio-quiz1-review.json','content/bio-sg-test1.json','content/bio-sg-test2.json',
  'content/bio-unit-1.json','content/bio-unit-1b.json','content/bio-unit-2.json',
  'content/bio-unit-2b-enzymes.json','content/bio-unit-3-cells.json','content/bio-unit-4-mitosis.json',
  'content/bio-unit-5-meiosis.json'];

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const seeded = await p.evaluate(async (FILES)=>{
    const files = Array.from(new Set(FILES.concat(CONTENT_LIBRARY.filter(f=>/bio-/.test(f)))));
    const loaded = [];
    for(const f of files){
      try{ const j = await (await fetch(f)).json();
        Object.values(j.records).forEach(r=>{ if(r&&r.type){
          if(r.id==='unit-bio-u5') window.__shipped = JSON.parse(JSON.stringify(r));
          r.status='approved'; delete r.releaseOn; put(r); } });
        loaded.push(f);
      }catch(e){}
    }
    saveLocal();
    const s = window.__shipped, u = DATA.records['unit-bio-u5'];
    if(!u || !s) return {missing:true, loaded};
    return { loaded:loaded.length, id:u.id, classId:u.classId, title:u.title, libv:s.libv,
             order:s.order, prep:s.prep, status:s.status, ageH:(Date.now()-s.updatedAt)/3.6e6,
             mitosisClass: (DATA.records['unit-bio-u4']||{}).classId,
             cards:u.cards.length, qs:u.questions.length,
             lv:[1,2,3].map(l=>u.questions.filter(q=>q.lv===l).length) };
  }, BIO_FILES);
  if(seeded.missing){ console.log('FAIL unit-bio-u5 not loaded', JSON.stringify(seeded)); await b.close(); process.exit(1); }

  ck('ships as a draft with libv, no order bucket and no prep flag, stamped in the past',
     seeded.status==='draft' && seeded.libv>=1 && !seeded.order && !seeded.prep && seeded.ageH>0.5, seeded);
  ck('classId is "bio" — the same id the Mitosis unit uses (the v136 orphan trap)',
     seeded.classId==='bio' && seeded.mitosisClass==='bio', seeded);
  ck('at least 18 cards and 18 questions, with all three levels used',
     seeded.cards>=18 && seeded.qs>=18 && seeded.lv.every(n=>n>=4), seeded);
  ck('it carries the numbered form its shelf requires (v180)',
     /^Biology 8 · Unit 5-1: /.test(seeded.title), seeded.title);

  // ---- the whole shelf, ascending, every lesson numbered, Unit 5-1 after Unit 4-1
  const shelf = await p.evaluate(()=>{
    const sh = shelvesFor('bio');
    const book = sh.shelves.find(s=>/Biology 8/.test(s.name));
    return book ? { name:book.name, looseHere: sh.loose.some(u=>u.id==='unit-bio-u5'),
                    parts: book.lessons.map(u=>u.title.replace(/^Biology 8 · /,'')) } : null;
  });
  const parts = (shelf&&shelf.parts)||[];
  const lessons = parts.filter(t=>/^Unit \d+-\d+:/.test(t));
  const keyOf = t => { const m=t.match(/^Unit (\d+)-(\d+):/); return m?[+m[1],+m[2]]:null; };
  const ascending = lessons.every((t,i)=>{
    if(!i) return true; const a=keyOf(lessons[i-1]), c=keyOf(t);
    return a && c && (c[0]>a[0] || (c[0]===a[0] && c[1]>a[1]));
  });
  const i4 = lessons.findIndex(t=>/^Unit 4-1:/.test(t)), i5 = lessons.findIndex(t=>/^Unit 5-1:/.test(t));
  ck('the Biology 8 shelf holds the new unit and it is not loose', !!shelf && i5>=0 && !shelf.looseHere, shelf);
  ck('every lesson on the shelf carries the numbered form',
     lessons.length===parts.filter(t=>!/Study Guide|Quiz Review/.test(t)).length, parts);
  ck('the shelf ascends by unit then part, and Unit 5-1 comes right after Unit 4-1',
     ascending && i4>=0 && i5===i4+1, lessons);

  // ---- structure: slots, unique options, standalone
  const struct = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const slots = {};
    u.questions.filter(q=>(q.kind||'mc')==='mc').forEach(q=>{ slots[q.ans]=(slots[q.ans]||0)+1; });
    const POS = /\b(all|none) of the above\b|\boptions? [a-d1-4]\b|\b(first|second|third|last) (option|choice)\b/i;
    const BACK = /^\s*(the|that|for (that|the)|from the|using the|in the|with the) same\b|\bthat same\b/i;
    const SRC = /\b(worksheet|the slides?|the deck|your notes|the outline|practice sheet)\b/i;
    return { slots,
      badOpts: u.questions.filter(q=>q.opts.length!==4 || new Set(q.opts).size!==4 || !(q.ans>=0&&q.ans<4)).map(q=>q.id),
      badSteps: u.questions.filter(q=>!(q.steps.length>=3 && q.steps.length<=6) || !q.hint || !/^\*\*/.test(q.ex.main) || !q.ex.tip).map(q=>q.id),
      pos: u.questions.filter(q=>POS.test(JSON.stringify(q))).map(q=>q.id),
      back: u.questions.filter(q=>BACK.test(q.q)).map(q=>q.id),
      src: u.questions.filter(q=>SRC.test(q.q+' '+q.opts.join(' '))).map(q=>q.id),
      // a question may never contain its own answer
      selfAns: u.questions.filter(q=>(q.kind||'mc')==='mc' && q.opts[q.ans].length>6 &&
                 q.q.toLowerCase().includes(q.opts[q.ans].toLowerCase())).map(q=>q.id),
      badDefs: u.cards.filter(c=>!/^\*\*[^*]+\*\*/.test(c.def) || (c.def.match(/\n• /g)||[]).length>3).map(c=>c.id) };
  }, UID);
  ck('correct answers are spread across all four slots (the v181 _balance bug, pinned)',
     Object.keys(struct.slots).length===4, struct.slots);
  ck('every question has exactly 4 unique options and an answer in range', !struct.badOpts.length, struct.badOpts);
  ck('every question has a hint, 3–6 steps, a bold ex.main and a tip', !struct.badSteps.length, struct.badSteps);
  ck('no positional references, no back-referencing stems, no stem pointing at the source',
     !struct.pos.length && !struct.back.length && !struct.src.length, struct);
  ck('no question contains its own answer', !struct.selfAns.length, struct.selfAns);
  ck('every card leads with a bold answer and carries at most three bullets', !struct.badDefs.length, struct.badDefs);

  // ---- the counts, re-derived HERE from each stem rather than trusted
  const counts = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const A = q => q.opts[q.ans];
    const find = re => u.questions.find(q=>re.test(q.q));
    const twoN = q => +((q.q.match(/2N = (\d+)/)||[])[1]);
    const r = {};
    let q = find(/each gamete/i);        r.gamete = q && A(q)===String(twoN(q)/2);
    q = find(/finishes S phase/i);       r.afterS = q && A(q)===`${twoN(q)} chromosomes, ${twoN(q)*2} chromatids`;
    q = find(/end of meiosis I\b/i);     r.afterM1 = q && A(q)===`${twoN(q)/2} chromosomes, ${twoN(q)} chromatids`;
    q = find(/both divisions/i);         r.afterM2 = q && A(q)===`${twoN(q)/2} chromosomes, ${twoN(q)/2} chromatids`;
    q = find(/how many tetrads/i);       r.tetrads = q && A(q)===String(twoN(q)/2);
    q = find(/independent assortment/i); r.assort = q && A(q)===String(2**(twoN(q)/2));
    q = find(/zygote/i);                 r.zygote = q && A(q)===String(2*+(q.q.match(/carries (\d+) chromosomes/)||[])[1]);
    q = find(/anaphase II/i);            r.ana2 = q && A(q)===String(2*+(q.q.match(/with (\d+) X-shaped/)||[])[1]);
    // fresh numbers: none of the deck's own worked example in a graded stem
    r.deckNums = u.questions.filter(q=>/\b30 chromosomes|60 chromatids|2\^23|8,388,608|2N = (4|46)\b/.test(q.q)).map(q=>q.id);
    return r;
  }, UID);
  ck('every chromosome/chromatid count question agrees with the count re-derived from its stem',
     ['gamete','afterS','afterM1','afterM2','tetrads','assort','zygote','ana2'].every(k=>counts[k]), counts);
  ck('no graded stem reuses the deck\'s own worked numbers (30/60, 46, 2^23, 2N = 4)',
     !counts.deckNums.length, counts.deckNums);

  // ---- THE CONTRADICTIONS, and the core teaching
  const t = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const cardText = c => c.term+' '+c.def+' '+(c.hint||'');
    const all = u.cards.map(cardText).join(' \n ');
    const byTerm = re => u.cards.find(c=>re.test(c.term));
    const haploidQ = u.questions.find(q=>/first become haploid/i.test(q.q));
    const note = u.parentNote.text;
    const mei = byTerm(/^Meiosis$/);
    const tet = byTerm(/^Tetrad/);
    const co = byTerm(/^Crossing over/);
    const ia = byTerm(/independent assortment/i);
    const diff = byTerm(/differs from mitosis/i);
    const oq = u.questions.find(q=>q.kind==='order');
    return {
      germline: !!mei && /germline/i.test(mei.def) && !/from (a )?(diploid )?somatic/i.test(JSON.stringify(u.cards)+JSON.stringify(u.questions)),
      haploidQ: haploidQ ? {ans:haploidQ.opts[haploidQ.ans], decoy:haploidQ.opts.some((o,i)=>i!==haploidQ.ans && /end of meiosis II/i.test(o))} : null,
      haploidCard: /end of meiosis I\b/i.test(all) && /still X-shaped/i.test(all),
      noteSomatic: /somatic/i.test(note) && /germline/i.test(note),
      noteHaploid: /haploid/i.test(note) && /meiosis II/i.test(note),
      tetrad: !!tet && /four chromatids/i.test(tet.def) && /homologous/i.test(tet.def),
      crossing: !!co && /prophase I\b/i.test(co.def),
      assort: !!ia && /2\^N/.test(ia.def) && /8,388,608/.test(ia.def) && /random/i.test(ia.def),
      homVsSis: /identical copies/i.test(all) && /one from each parent/i.test(all),
      oneCopy: /NO interphase between meiosis I and meiosis II/i.test(all),
      contrast: !!diff && /identical/i.test(diff.def) && /four/i.test(diff.def) && /two/i.test(diff.def)
                && /haploid/i.test(diff.def) && /diploid/i.test(diff.def),
      polar: /polar bodies/i.test(all),
      addedTags: u.cards.filter(c=>/even number|have to be haploid|Anaphase II and the count|share/i.test(c.term)).map(c=>c.from),
      order: oq ? {ans:oq.ans, opts:oq.opts} : null,
      noImg: u.cards.filter(c=>c.imgUrl).length===0 &&
             !u.questions.some(q=>q.imgUrl || /\b(diagram|image|picture|figure) (shown|above|below)\b/i.test(q.q)),
      marks: /\bshe got\b|\bscored?\b|\d+\s*(\/|out of)\s*\d+\s*(points|marks)?|\bgrade[ds]?\b/i.test(JSON.stringify(u).replace(/2N = \d+/g,'')),
      names: /\b(Mr|Mrs|Ms|Dr)\.? [A-Z]|Sedona/.test(JSON.stringify(u)),
      noteSources: /MEIOSIS/i.test(note) && /note outline/i.test(note) && /directed-reading/i.test(note) };
  }, UID);
  ck('meiosis is taught as starting from a GERMLINE cell, never from a somatic one', t.germline, t.germline);
  ck('a graded question puts the haploid switch at the end of meiosis I, with the end-of-meiosis-II reading as a decoy',
     t.haploidQ && /end of meiosis I\b/i.test(t.haploidQ.ans) && t.haploidQ.decoy, t.haploidQ);
  ck('a card teaches haploid at the end of meiosis I with chromosomes still X-shaped', t.haploidCard, t.haploidCard);
  ck('parentNote flags BOTH source problems — the somatic slip and the haploid slide',
     t.noteSomatic && t.noteHaploid, {somatic:t.noteSomatic, haploid:t.noteHaploid});
  ck('parentNote names all three sources', t.noteSources, t.noteSources);
  ck('tetrad = a homologous pair, four chromatids', t.tetrad, t.tetrad);
  ck('crossing over is placed in prophase I', t.crossing, t.crossing);
  ck('independent assortment: random, 2^N, 8,388,608 in humans', t.assort, t.assort);
  ck('homologous pairs and sister chromatids are kept apart', t.homVsSis, t.homVsSis);
  ck('one round of copying: no interphase between the divisions', t.oneCopy, t.oneCopy);
  ck('the mitosis contrast is taught — two identical diploid vs four different haploid', t.contrast, t.contrast);
  ck('eggs and polar bodies are covered', t.polar, t.polar);
  ck('the cards the material only ASKS about are tagged added', t.addedTags.length>=4 && t.addedTags.every(f=>f==='added'), t.addedTags);
  ck('the order question is stored in the correct sequence: pair, line up, split pairs, split sisters',
     t.order && t.order.ans===0 && t.order.opts.length===4 && /pair up/i.test(t.order.opts[0])
       && /line up/i.test(t.order.opts[1]) && /homologous pairs are pulled apart/i.test(t.order.opts[2])
       && /sister chromatids/i.test(t.order.opts[3]), t.order);
  ck('no card or question carries or points at an image', t.noImg, t.noImg);
  ck('no mark, score or name anywhere in the shipped record (v198)', !t.marks && !t.names, {marks:t.marks, names:t.names});

  // ---- a full round plays and logs, and the deck walks to the end
  const round = await p.evaluate((UID)=>{
    quizState = null; ctx.pre = null;
    const before = Object.values(DATA.records).filter(r=>r.type==='log' && r.unitId===UID && !r.deleted).length;
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
    const after = Object.values(DATA.records).filter(r=>r.type==='log' && r.unitId===UID && !r.deleted);
    return {built:true, n, right, logged: after.length-before,
            last: after.length ? {correct:after[after.length-1].correct, total:after[after.length-1].total} : null};
  }, UID);
  ck('a full quiz round plays, every correct answer scores, and it logs',
     round.built && round.n>0 && round.right===round.n && round.logged>=1, round);

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
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got).slice(0,320)); }
                   else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
