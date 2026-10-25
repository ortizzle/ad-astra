/* Biology 8 · Unit 6-1: DNA.

   Modelled on test_bio_meiosis.js, and pins the unit by its TEACHING rather
   than by question id (the v185/v194 rule). The new unit is fetched straight
   from content/ and put into the store, alongside every content/bio-*.json
   file, so it does not depend on CONTENT_LIBRARY listing it yet.

   Every complementary strand, Chargaff percentage, base count and
   hydrogen-bond total is re-derived HERE from the question's own stem,
   independently of the builder. Plus the three places the unit words things
   more carefully than its sources (nucleotide, double-stranded only, even
   width), each flagged in parentNote.

   Usage: node tools/test_bio_dna.js <port> */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8421;
const UID = 'unit-bio-u6';
const BIO_FILES = ['content/bio-quiz1-review.json','content/bio-sg-test1.json','content/bio-sg-test2.json',
  'content/bio-unit-1.json','content/bio-unit-1b.json','content/bio-unit-2.json',
  'content/bio-unit-2b-enzymes.json','content/bio-unit-3-cells.json','content/bio-unit-4-mitosis.json',
  'content/bio-unit-5-meiosis.json','content/bio-unit-6-dna.json'];

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const seeded = await p.evaluate(async ({FILES, UID})=>{
    const files = Array.from(new Set(FILES.concat(CONTENT_LIBRARY.filter(f=>/bio-/.test(f)))));
    const loaded = [];
    for(const f of files){
      try{ const j = await (await fetch(f)).json();
        Object.values(j.records).forEach(r=>{ if(r&&r.type){
          if(r.id===UID) window.__shipped = JSON.parse(JSON.stringify(r));
          r.status='approved'; delete r.releaseOn; put(r); } });
        loaded.push(f);
      }catch(e){}
    }
    saveLocal();
    const s = window.__shipped, u = DATA.records[UID];
    if(!u || !s) return {missing:true, loaded};
    return { loaded:loaded.length, id:u.id, classId:u.classId, title:u.title, libv:s.libv,
             order:s.order, prep:s.prep, status:s.status, quarter:s.quarter, ageH:(Date.now()-s.updatedAt)/3.6e6,
             meiosisClass: (DATA.records['unit-bio-u5']||{}).classId,
             cards:u.cards.length, qs:u.questions.length,
             lv:[1,2,3].map(l=>u.questions.filter(q=>q.lv===l).length) };
  }, {FILES:BIO_FILES, UID});
  if(seeded.missing){ console.log('FAIL '+UID+' not loaded', JSON.stringify(seeded)); await b.close(); process.exit(1); }

  ck('ships as a draft with libv, quarter 2, no order bucket and no prep flag, stamped in the past',
     seeded.status==='draft' && seeded.libv>=1 && seeded.quarter===2 && !seeded.order && !seeded.prep && seeded.ageH>0.5, seeded);
  ck('classId is "bio" — the same id the Meiosis unit uses (the v136 orphan trap)',
     seeded.classId==='bio' && seeded.meiosisClass==='bio', seeded);
  ck('at least 20 cards and 20 questions, with all three levels used',
     seeded.cards>=20 && seeded.qs>=20 && seeded.lv.every(n=>n>=5), seeded);
  ck('it carries the numbered form its shelf requires (v180)',
     /^Biology 8 · Unit 6-1: /.test(seeded.title), seeded.title);

  // ---- the whole shelf, ascending, every lesson numbered, Unit 6-1 after Unit 5-1
  const shelf = await p.evaluate((UID)=>{
    const sh = shelvesFor('bio');
    const book = sh.shelves.find(s=>/Biology 8/.test(s.name));
    return book ? { name:book.name, looseHere: sh.loose.some(u=>u.id===UID),
                    parts: book.lessons.map(u=>u.title.replace(/^Biology 8 · /,'')) } : null;
  }, UID);
  const parts = (shelf&&shelf.parts)||[];
  const lessons = parts.filter(t=>/^Unit \d+-\d+:/.test(t));
  const keyOf = t => { const m=t.match(/^Unit (\d+)-(\d+):/); return m?[+m[1],+m[2]]:null; };
  const ascending = lessons.every((t,i)=>{
    if(!i) return true; const a=keyOf(lessons[i-1]), c=keyOf(t);
    return a && c && (c[0]>a[0] || (c[0]===a[0] && c[1]>a[1]));
  });
  const i5 = lessons.findIndex(t=>/^Unit 5-1:/.test(t)), i6 = lessons.findIndex(t=>/^Unit 6-1:/.test(t));
  ck('the Biology 8 shelf holds the new unit and it is not loose', !!shelf && i6>=0 && !shelf.looseHere, shelf);
  ck('every lesson on the shelf carries the numbered form',
     lessons.length===parts.filter(t=>!/Study Guide|Quiz Review/.test(t)).length, parts);
  ck('the shelf ascends by unit then part, and Unit 6-1 comes right after Unit 5-1',
     ascending && i5>=0 && i6===i5+1, lessons);

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

  // ---- the arithmetic, re-derived HERE from each stem rather than trusted
  const counts = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const A = q => q.opts[q.ans];
    const find = re => u.questions.find(q=>re.test(q.q));
    const PAIR = {A:'T',T:'A',C:'G',G:'C'}, HB = {A:2,T:2,C:3,G:3};
    const comp = s => s.split('').map(b=>PAIR[b]).join('');
    const hb = s => s.split('').reduce((n,b)=>n+HB[b],0);
    const NAME = {adenine:'A',thymine:'T',guanine:'G',cytosine:'C'};
    const r = {};
    let q = find(/partner strand, written base for base/i);
    r.complement = q && A(q)===comp(q.q.match(/reads ([ACGT]+)/)[1]);
    q = find(/breaks the base-pairing rules/i);
    if(q){ const m=q.q.match(/strand ([ACGT]+) as ([ACGT]+)/); const s=m[1], t=m[2];
      const bad=[...s].map((b,i)=>[b,t[i]]).filter(([b,c])=>PAIR[b]!==c);
      r.mismatch = bad.length===1 && A(q)===`The ${bad[0][0]} paired with ${bad[0][1]}`; }
    r.chargaff = u.questions.filter(q=>/is \d+% (adenine|thymine|guanine|cytosine)\. What percentage/i.test(q.q)).map(q=>{
      const m=q.q.match(/is (\d+)% (\w+)\. What percentage of it is (\w+)/i);
      const v=+m[1], g=NAME[m[2].toLowerCase()], w=NAME[m[3].toLowerCase()];
      const want = (w===g || w===PAIR[g]) ? v : (100-2*v)/2;
      return A(q)===want+'%';
    });
    q = find(/adenine and thymine together make up/i);
    r.atSum = q && A(q)===((100-+q.q.match(/(\d+)% of the bases/)[1])/2)+'%';
    q = find(/bases in all/i);
    if(q){ const m=q.q.match(/holds (\d+) bases in all, and (\d+) of them are adenine/); r.count = A(q)===String((+m[1]-2*+m[2])/2); }
    q = find(/How many hydrogen bonds hold/i);
    r.hbonds = q && A(q)===String(hb(q.q.match(/reads ([ACGT]+)/)[1]));
    q = find(/most energy to unzip/i);
    if(q){ const tot=q.opts.map(hb); const mx=Math.max(...tot);
      r.unzip = tot.filter(n=>n===mx).length===1 && tot[q.ans]===mx; }
    q = find(/copied again/i);
    r.semi = q && /^2 of the 4$/.test(A(q));
    q = find(/32% adenine, 18% thymine/i);
    r.badData = q && /cannot be ordinary double-stranded/i.test(A(q));
    // fresh numbers: none of the deck's own knowledge check in a graded stem
    r.deckNums = u.questions.filter(q=>/GATTACATACG|CTAATGTATGC|\b30% (adenine|thymine)|Adenine = 30/i.test(q.q)).map(q=>q.id);
    return r;
  }, UID);
  ck('every strand, percentage, count and bond total agrees with the value re-derived from its stem',
     ['complement','mismatch','atSum','count','hbonds','unzip','semi','badData'].every(k=>counts[k])
       && counts.chargaff.length>=2 && counts.chargaff.every(Boolean), counts);
  ck('no graded stem reuses the deck\'s own knowledge check (GATTACATACG, 30% adenine)',
     !counts.deckNums.length, counts.deckNums);

  // ---- the core teaching, and the three careful wordings
  const t = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const cardText = c => c.term+' '+c.def+' '+(c.hint||'');
    const all = u.cards.map(cardText).join(' \n ');
    const byTerm = re => u.cards.find(c=>re.test(c.term));
    const note = u.parentNote.text;
    const nuc = byTerm(/^Nucleotide$/), pur = byTerm(/^Purines$/), pyr = byTerm(/^Pyrimidines$/);
    const hbc = byTerm(/Hydrogen bonds in each pair/), anti = byTerm(/^Antiparallel/);
    const ch = byTerm(/^Chargaff's rule$/), stop = byTerm(/Where Chargaff/), why = byTerm(/two kinds of bond/i);
    const lag = byTerm(/lagging strand/i), helix = byTerm(/double helix/i), semi = byTerm(/Semi-conservative/i);
    const oq = u.questions.find(q=>q.kind==='order');
    return {
      nucleotide: !!nuc && /phosphate/i.test(nuc.def) && /5-carbon sugar/i.test(nuc.def) && /nitrogenous base/i.test(nuc.def),
      purines: !!pur && /Adenine and guanine/.test(pur.def) && /two rings/i.test(pur.def),
      pyrimidines: !!pyr && /Cytosine, thymine and uracil/.test(pyr.def) && /one ring/i.test(pyr.def),
      pairing: /A always pairs with T, and C always pairs with G/.test(all),
      hb: !!hbc && /A–T pairs are held by 2/.test(hbc.def) && /C–G pairs by 3/.test(hbc.def),
      anti: !!anti && /5′ → 3′/.test(anti.def) && /3′ → 5′/.test(anti.def),
      chargaff: !!ch && /%A = %T/.test(ch.def) && /%G = %C/.test(ch.def) && /50%/.test(ch.def),
      dsOnly: !!stop && /double-stranded/i.test(stop.def) && stop.from==='added',
      whyBonds: !!why && /unzip/i.test(why.def) && why.from==='added',
      lagging: !!lag && lag.from==='added' && /one direction/i.test(lag.def),
      evenWidth: !!helix && /same width/i.test(helix.def),
      semi: !!semi && /one original strand/i.test(semi.def) && /one new strand/i.test(semi.def),
      rna: /GUAC/.test(all) && /uracil/i.test(all) && /ribose/i.test(all),
      enzymes: ['Helicase','Primase','DNA polymerase','Ligase'].every(e=>u.cards.some(c=>c.term.startsWith(e))),
      noteNucleotide: /NUCLEOTIDE/.test(note) && /3 parts/.test(note),
      noteDs: /double-stranded/i.test(note) && /Chargaff/i.test(note),
      noteHelix: /same width/i.test(note) && /double helix/i.test(note),
      noteUnseen: /pictures were not seen/i.test(note) && /10\.7 MB/.test(note),
      noteSources: /Unit 6_ DNA/.test(note) && /Structure and Replication/.test(note) && /blank/i.test(note),
      order: oq ? {ans:oq.ans, opts:oq.opts} : null,
      noImg: u.cards.filter(c=>c.imgUrl).length===0 &&
             !u.questions.some(q=>q.imgUrl || /\b(diagram|image|picture|figure) (shown|above|below)\b/i.test(q.q)),
      marks: /\bshe got\b|\bscored?\b|\d+\s*(\/|out of)\s*\d+\s*(points|marks)?|\bgrade[ds]?\b|\/11\b/i.test(JSON.stringify(u)),
      names: /\b(Mr|Mrs|Ms|Dr)\.? [A-Z]|Sedona|wordpress|schoology|https?:/i.test(JSON.stringify(u)) };
  }, UID);
  ck('a nucleotide is phosphate + 5-carbon sugar + nitrogenous base', t.nucleotide, t.nucleotide);
  ck('purines are A and G (two rings); pyrimidines are C, T and U (one ring)', t.purines && t.pyrimidines, t);
  ck('base pairing A–T, C–G with 2 and 3 hydrogen bonds', t.pairing && t.hb, {pairing:t.pairing, hb:t.hb});
  ck('antiparallel strands taught as 5′ → 3′ against 3′ → 5′', t.anti, t.anti);
  ck("Chargaff's rule, with purines = pyrimidines = 50%", t.chargaff, t.chargaff);
  ck('DNA vs RNA: ribose, uracil, GUAC', t.rna, t.rna);
  ck('helicase, primase, DNA polymerase and ligase each have a card', t.enzymes, t.enzymes);
  ck('semi-conservative = one original strand, one new strand', t.semi, t.semi);
  ck('the even-width reason for the helix is taught', t.evenWidth, t.evenWidth);
  ck('what the sources only ASK or leave unsaid is tagged added: double-stranded only, why two bonds, the lagging strand',
     t.dsOnly && t.whyBonds && t.lagging, {ds:t.dsOnly, why:t.whyBonds, lag:t.lagging});
  ck('parentNote flags all three careful wordings — nucleotide, double-stranded only, even width',
     t.noteNucleotide && t.noteDs && t.noteHelix, {n:t.noteNucleotide, ds:t.noteDs, h:t.noteHelix});
  ck('parentNote names both sources, says the homework was blank and the slide pictures unseen',
     t.noteSources && t.noteUnseen, {src:t.noteSources, unseen:t.noteUnseen});
  ck('the order question is stored in the correct sequence: helicase, primase, polymerase builds, polymerase checks',
     t.order && t.order.ans===0 && t.order.opts.length===4 && /^Helicase/.test(t.order.opts[0])
       && /^Primase/.test(t.order.opts[1]) && /^DNA polymerase builds/.test(t.order.opts[2])
       && /double-checks/.test(t.order.opts[3]), t.order);
  ck('no card or question carries or points at an image', t.noImg, t.noImg);
  ck('no mark, score, name or link anywhere in the shipped record (v198)', !t.marks && !t.names, {marks:t.marks, names:t.names});

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
