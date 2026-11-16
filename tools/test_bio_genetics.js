/* Biology 8 · Unit 7-1: Genetics.

   Modelled on test_bio_dna.js, and pins the unit by its TEACHING rather than
   by question id (the v185/v194 rule). The new unit is fetched straight from
   content/ and put into the store, alongside every content/bio-*.json file,
   so it does not depend on CONTENT_LIBRARY listing it yet.

   Every Punnett percentage and ratio is re-derived HERE by crossing the
   alleles named in the question's own stem, independently of the builder:
   one-gene crosses, a genotype ratio, blood-type crosses, codominant and
   blended crosses, X-linked crosses and the Y-linked case. Plus the four
   careful calls (the "All of the above" knowledge-check item, the
   complete-dominance convention, incomplete dominance, nondisjunction), each
   by its teaching and each in parentNote.

   Usage: node tools/test_bio_genetics.js <port> */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8431;
const UID = 'unit-bio-u7';
const BIO_FILES = ['content/bio-quiz1-review.json','content/bio-sg-test1.json','content/bio-sg-test2.json',
  'content/bio-unit-1.json','content/bio-unit-1b.json','content/bio-unit-2.json',
  'content/bio-unit-2b-enzymes.json','content/bio-unit-3-cells.json','content/bio-unit-4-mitosis.json',
  'content/bio-unit-5-meiosis.json','content/bio-unit-6-dna.json','content/bio-unit-7-genetics.json'];

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
    return { loaded:loaded.length, classId:u.classId, title:u.title, libv:s.libv,
             order:s.order, prep:s.prep, status:s.status, quarter:s.quarter, ageH:(Date.now()-s.updatedAt)/3.6e6,
             dnaClass:(DATA.records['unit-bio-u6']||{}).classId,
             cards:u.cards.length, qs:u.questions.length,
             lv:[1,2,3].map(l=>u.questions.filter(q=>q.lv===l).length) };
  }, {FILES:BIO_FILES, UID});
  if(seeded.missing){ console.log('FAIL '+UID+' not loaded', JSON.stringify(seeded)); await b.close(); process.exit(1); }

  ck('ships as a draft with libv 1, quarter 2, no order and no prep, stamped in the past',
     seeded.status==='draft' && seeded.libv===1 && seeded.quarter===2 && !seeded.order && !seeded.prep && seeded.ageH>0.5, seeded);
  ck('classId is "bio", the same id the DNA unit uses (the v136 orphan trap)',
     seeded.classId==='bio' && seeded.dnaClass==='bio', seeded);
  ck('24–30 cards and 22–25 questions, with all three levels well used',
     seeded.cards>=24 && seeded.cards<=30 && seeded.qs>=22 && seeded.qs<=25 && seeded.lv.every(n=>n>=5), seeded);
  ck('it carries the numbered form its shelf requires (v180)', /^Biology 8 · Unit 7-1: Genetics$/.test(seeded.title), seeded.title);

  // ---- the shelf: Unit 7-1 right after Unit 6-1
  const shelf = await p.evaluate((UID)=>{
    const sh = shelvesFor('bio');
    const book = sh.shelves.find(s=>/Biology 8/.test(s.name));
    return book ? { looseHere: sh.loose.some(u=>u.id===UID),
                    parts: book.lessons.map(u=>u.title.replace(/^Biology 8 · /,'')) } : null;
  }, UID);
  const lessons = ((shelf&&shelf.parts)||[]).filter(t=>/^Unit \d+-\d+:/.test(t));
  const keyOf = t => { const m=t.match(/^Unit (\d+)-(\d+):/); return m?[+m[1],+m[2]]:null; };
  const ascending = lessons.every((t,i)=>{ if(!i) return true; const a=keyOf(lessons[i-1]), c=keyOf(t);
    return a && c && (c[0]>a[0] || (c[0]===a[0] && c[1]>a[1])); });
  const i6 = lessons.findIndex(t=>/^Unit 6-1:/.test(t)), i7 = lessons.findIndex(t=>/^Unit 7-1:/.test(t));
  ck('the shelf ascends by unit then part, and Unit 7-1 sits right after Unit 6-1, not loose',
     shelf && !shelf.looseHere && ascending && i6>=0 && i7===i6+1, lessons);

  // ---- structure
  const struct = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const slots = {};
    u.questions.filter(q=>(q.kind||'mc')==='mc').forEach(q=>{ slots[q.ans]=(slots[q.ans]||0)+1; });
    const POS = /\b(all|none|both) of the above\b|\boptions? [a-d1-4]\b|\b(first|second|third|fourth|last) (option|choice|answer)\b/i;
    const BACK = /^\s*(the|that|for (that|the)|from the|using the|in the|with the) same\b|\bthat same\b|\b(the|that) (cross|square|parents?|plants?|flies) (from|above|before)\b/i;
    const SRC = /\b(worksheet|the slides?|the deck|your notes|knowledge check|practice sheet)\b/i;
    return { slots,
      badOpts: u.questions.filter(q=>q.opts.length!==4 || new Set(q.opts).size!==4 || !(q.ans>=0&&q.ans<4)).map(q=>q.id),
      badSteps: u.questions.filter(q=>!(q.steps.length>=3 && q.steps.length<=6) || !q.hint || !/^\*\*/.test(q.ex.main) || !q.ex.tip).map(q=>q.id),
      pos: u.questions.filter(q=>POS.test(JSON.stringify(q))).map(q=>q.id),
      back: u.questions.filter(q=>BACK.test(q.q)).map(q=>q.id),
      src: u.questions.filter(q=>SRC.test(q.q+' '+q.opts.join(' '))).map(q=>q.id),
      selfAns: u.questions.filter(q=>(q.kind||'mc')==='mc' && q.opts[q.ans].length>4 &&
                 q.q.toLowerCase().includes(q.opts[q.ans].toLowerCase())).map(q=>q.id),
      badDefs: u.cards.filter(c=>!/^\*\*[^*]+\*\*/.test(c.def) || (c.def.match(/\n• /g)||[]).length>3).map(c=>c.id) };
  }, UID);
  ck('correct answers are spread across all four slots (_balance)', Object.keys(struct.slots).length===4, struct.slots);
  ck('every question has exactly 4 unique options and an answer in range', !struct.badOpts.length, struct.badOpts);
  ck('every question has a hint, 3–6 steps, a bold ex.main and a tip', !struct.badSteps.length, struct.badSteps);
  ck('no positional reference, no "all of the above", no back-referencing stem, no stem pointing at the source',
     !struct.pos.length && !struct.back.length && !struct.src.length, struct);
  ck('no question contains its own answer', !struct.selfAns.length, struct.selfAns);
  ck('every card leads with a bold answer and carries at most three bullets', !struct.badDefs.length, struct.badDefs);

  // ---- every ratio, re-derived HERE by crossing the alleles in each stem
  const r = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const A = q => q.opts[q.ans];
    const boxes = (m,d) => { const z=[]; m.forEach(a=>d.forEach(c=>z.push([a,c]))); return z; };
    const pc = (n,t) => Math.round(100*n/t)+'%';
    const res = {mono:[], ratio:[], blood:[], bratio:[], het:[], x:[], xdesc:[], y:null, tb:null};
    u.questions.forEach(q=>{
      let m;
      if((m = q.q.match(/, (.+?) \(([A-Z])\) (?:is|are) dominant over (.+?) \(([a-z])\)\. .*genotypes (\w\w) × (\w\w) are crossed\. What percentage of the offspring are expected to have (.+?)\?/))){
        const [ ,dom,D,rec,d,g1,g2,asked] = m;
        const z = boxes([...g1],[...g2]);
        const want = asked===dom ? z.filter(b=>b.includes(D)).length : z.filter(b=>!b.includes(D)).length;
        res.mono.push(A(q)===pc(want,4));
      }
      if((m = q.q.match(/genotypes (\w\w) × (\w\w) are crossed\. Which genotype ratio/))){
        const z = boxes([...m[1]],[...m[2]]).map(b=>b.slice().sort((a,c)=>(a===a.toLowerCase())-(c===c.toLowerCase())||a.localeCompare(c)).join(''));
        const L = m[1][0].toUpperCase(), l = L.toLowerCase();
        const cnt = g => z.filter(x=>x===g).length;
        res.ratio.push(A(q)===[L+L,L+l,l+l].map(g=>cnt(g)+' '+g).join(' : '));
      }
      const tok = s => s.match(/Iᴬ|Iᴮ|i/g);
      const btype = b => b.includes('Iᴬ')&&b.includes('Iᴮ') ? 'AB' : b.includes('Iᴬ') ? 'A' : b.includes('Iᴮ') ? 'B' : 'O';
      if((m = q.q.match(/blood genotypes (\S+) × (\S+) have children\. What percentage .*have type (AB|A|B|O) blood/))){
        const z = boxes(tok(m[1]),tok(m[2]));
        res.blood.push(A(q)===pc(z.filter(b=>btype(b)===m[3]).length,4));
      }
      if((m = q.q.match(/blood genotypes (\S+) × (\S+) have children\. Which blood types/))){
        const z = boxes(tok(m[1]),tok(m[2])); const c={}; z.forEach(b=>{const t=btype(b); c[t]=(c[t]||0)+1;});
        const ts = ['A','AB','B','O'].filter(t=>c[t]); const gcd=(a,b)=>b?gcd(b,a%b):a; const g = ts.reduce((a,t)=>gcd(a,c[t]),0);
        res.bratio.push(A(q)===ts.map(t=>(c[t]/g)+' type '+t).join(' : '));
      }
      if((m = q.q.match(/genotypes (C\S+) × (C\S+) are (?:mated|crossed)\. What percentage .* to be (roan|pink)\?/))){
        const z = boxes(m[1].match(/C[ᴿᵂ]/g), m[2].match(/C[ᴿᵂ]/g));
        res.het.push(A(q)===pc(z.filter(b=>b[0]!==b[1]).length,4));
      }
      if((m = q.q.match(/genotypes (X\S+) × (X\S+Y) are mated\. (.*)$/))){
        const z = boxes(m[1].match(/X[ᵂʷ]/g), m[2].match(/X[ᵂʷ]|Y/g));
        const white = b => b.filter(a=>a!=='Y').every(a=>a==='Xʷ');
        const sons = z.filter(b=>b[1]==='Y'), daus = z.filter(b=>b[1]!=='Y');
        const ps = 100*sons.filter(white).length/sons.length, pd = 100*daus.filter(white).length/daus.length;
        const ask = m[3];
        if(/percentage of their sons/.test(ask)) res.x.push(A(q)===ps+'%');
        else if(/percentage of their daughters/.test(ask)) res.x.push(A(q)===pd+'%');
        else if(/Which describes/.test(ask)){
          const want = ps===100&&pd===0 ? /^Every son white-eyed; every daughter red-eyed$/
                     : ps===0&&pd===100 ? /^Every daughter white-eyed; every son red-eyed$/
                     : ps===50&&pd===50 ? /^Half of the sons and half of the daughters/ : /^No white-eyed/;
          res.xdesc.push(want.test(A(q)));
        }
      }
      if(/gene found only on the Y chromosome/.test(q.q)){
        const z = boxes(['X','X'],['X','Yt']);
        const sons = z.filter(b=>b.some(a=>a[0]==='Y')), daus = z.filter(b=>!b.some(a=>a[0]==='Y'));
        const ps = sons.filter(b=>b.includes('Yt')).length/sons.length, pd = daus.filter(b=>b.includes('Yt')).length/daus.length;
        res.y = ps===1 && pd===0 && A(q)==='Every son, and no daughter';
      }
      if(/true-breeding plant with smooth seeds/.test(q.q)){
        const z = boxes(['S','S'],['s','s']);
        res.tb = z.every(b=>b.includes('S')&&b.includes('s')) && /^Smooth is dominant, and every offspring is heterozygous$/.test(A(q));
      }
    });
    res.deck = u.questions.filter(q=>/widow|\bbears?\b|\bears?\b|floppy|pointed|hemophilia|webbed|\bRr\b|Iᴬi × Iᴮi|Iᴮi × Iᴬi|Xᴿ|Xʳ|XᵂXʷ × XᵂY/i.test(q.q+' '+q.opts.join(' '))).map(q=>q.id);
    return res;
  }, UID);
  const all = a => a.length>0 && a.every(Boolean);
  ck('one-gene crosses: every percentage matches the cross re-derived from its stem (2+)', r.mono.length>=2 && all(r.mono), r.mono);
  ck('the genotype ratio matches the cross re-derived from its stem', all(r.ratio), r.ratio);
  ck('blood-type crosses: the percentage and the ratio match, re-derived', all(r.blood) && all(r.bratio), {b:r.blood, br:r.bratio});
  ck('codominant and blended crosses: the in-between percentage matches, re-derived (2)', r.het.length>=2 && all(r.het), r.het);
  ck('X-linked crosses: the sons percentage and the offspring description match, re-derived', all(r.x) && all(r.xdesc), {x:r.x, d:r.xdesc});
  ck('the Y-linked case: every son and no daughter, re-derived', r.y===true, r.y);
  ck('the true-breeding cross: all heterozygous, so the shown trait is dominant', r.tb===true, r.tb);
  ck("no graded stem or option reuses the deck's examples (widow's peak, bears, dog ears, Iᴬi × Iᴮi, the colorblind and hemophilia crosses)",
     !r.deck.length, r.deck);

  // ---- the teaching, and the four careful calls
  const t = await p.evaluate((UID)=>{
    const u = DATA.records[UID];
    const by = re => u.cards.find(c=>re.test(c.term));
    const note = u.parentNote.text;
    const A = q => q.opts[q.ans];
    const domQ = u.questions.find(q=>/true of every dominant allele/i.test(q.q));
    const notBetter = by(/not "better"/i), conv = by(/Complete dominance is the default/i);
    const inc = by(/^Incomplete dominance$/), cod = by(/^Codominance$/);
    const nd = by(/extra sex chromosome comes from/i), cond = by(/Sex-chromosome conditions/i);
    const males = by(/Why males/i), six = by(/Six blood genotypes/i), ylink = by(/^Y-linked/);
    const xxy = u.questions.find(q=>/XXY/.test(q.q));
    const cam = u.questions.find(q=>/camellia/.test(q.q));
    const oq = u.questions.find(q=>q.kind==='order');
    const S = JSON.stringify(u);
    return {
      vocab: ['Gene','Chromosome','Trait','Allele','Genotype','Phenotype','Dominant allele','Recessive allele','Heterozygous','Homozygous']
               .every(n=>u.cards.some(c=>c.term===n)),
      laws: ['Law of dominance','Law of segregation','Law of independent assortment'].every(n=>u.cards.some(c=>c.term===n)),
      // call 1: "All of the above" is wrong; a dominant allele hides the recessive, and is not better or more common
      call1: !!notBetter && notBetter.from==='added' && /polydactyly/i.test(notBetter.def) && /rare/i.test(notBetter.def)
             && !!domQ && /hide/i.test(A(domQ)) && domQ.opts.some(o=>/more common/i.test(o)) && domQ.opts.some(o=>/better/i.test(o))
             && !domQ.opts.some(o=>/above/i.test(o)),
      note1: /All of the above/.test(note) && /not correct/i.test(note) && /option C/i.test(note) && /polydactyly/i.test(note),
      // call 2: complete dominance is a class convention, not biology
      call2: !!conv && conv.from==='added' && /unless/i.test(conv.def) && /convention/i.test(conv.def),
      note2: /convention, not biology/i.test(note) && /assume complete dominance/i.test(note),
      // call 3: incomplete dominance defined (added) and contrasted with codominance; dog ears off graded questions
      call3: !!inc && inc.from==='added' && /blend/i.test(inc.def) && /snapdragon/i.test(inc.def) && /pink/i.test(inc.def)
             && /codominance/i.test(inc.def) && !!cod && /AB/.test(cod.def) && /roan/i.test(cod.def)
             && !!cam && /^Codominance/.test(A(cam)) && cam.opts.some(o=>/^Incomplete/.test(o)),
      note3: /incomplete dominance/i.test(note) && /dog-ears/i.test(note) && /off every quiz question/i.test(note),
      // call 4: nondisjunction in meiosis puts the extra chromosome in every cell
      call4: !!nd && nd.from==='added' && /nondisjunction/i.test(nd.def) && /meiosis/i.test(nd.def) && /every cell/i.test(nd.def)
             && !!xxy && /every cell/i.test(A(xxy)) && /egg or sperm/i.test(A(xxy)),
      note4: /nondisjunction/i.test(note) && /every cell/i.test(note) && /Unit 5-1/.test(note),
      addedAnswers: !!males && males.from==='added' && /one X/i.test(males.def) && /mask/i.test(males.def)
             && !!six && six.from==='added' && /IᴬIᴬ/.test(six.def) && /ii is type O/.test(six.def)
             && !!ylink && ylink.from==='added',
      conditions: !!cond && ['Klinefelter syndrome: XXY','Trisomy X: XXX','Turner syndrome: a single X','XYY syndrome: XYY'].every(s=>cond.def.includes(s))
             && !/abnormal|disorder|defect|suffer|victim|normal|wrong|unfortunate|disease/i.test(cond.def+' '+(cond.hint||'')),
      noteUnseen: /pictures were not seen/i.test(note) && /superset/i.test(note),
      order: oq ? {ans:oq.ans, opts:oq.opts} : null,
      marks: /\bshe got\b|\bscored?\b|\d+\s*(\/|out of)\s*\d+\s*(points|marks)?|\bgrade[ds]?\b|\bmarks?\b/i.test(S),
      names: /\b(Mr|Mrs|Ms|Dr)\.? [A-Z]|Sedona|wordpress|schoology|https?:/i.test(S) };
  }, UID);
  ck('the deck vocabulary and Mendel\'s three laws each have a card', t.vocab && t.laws, {v:t.vocab, l:t.laws});
  ck('call 1: a dominant allele hides the recessive; "better" and "more common" are offered and wrong; polydactyly card added',
     t.call1, t.call1);
  ck('call 1 is in parentNote: "All of the above" is not correct, option C is taught', t.note1, t.note1);
  ck('call 2: complete dominance taught as the class default, a convention, flagged added, and in the note', t.call2 && t.note2, {c:t.call2, n:t.note2});
  ck('call 3: incomplete dominance is a blend (added), set against codominance (AB, roan, the camellia); dog ears flagged in the note',
     t.call3 && t.note3, {c:t.call3, n:t.note3});
  ck('call 4: nondisjunction in meiosis puts the extra chromosome in every cell (added), in a question and the note',
     t.call4 && t.note4, {c:t.call4, n:t.note4});
  ck('what the deck asks but does not answer is tagged added: why males, the six blood genotypes, Y-linked', t.addedAnswers, t.addedAnswers);
  ck('the four sex-chromosome conditions: names and karyotypes only, no judgement words', t.conditions, t.conditions);
  ck('parentNote says the slide pictures were not seen and the second copy was used', t.noteUnseen, t.noteUnseen);
  ck('the Punnett order question is stored in order: genotypes, split, fill, count',
     t.order && t.order.ans===0 && /^Write down the genotypes/.test(t.order.opts[0]) && /^Split/.test(t.order.opts[1])
       && /^Fill/.test(t.order.opts[2]) && /^Count/.test(t.order.opts[3]), t.order);
  ck('no mark, score, name or link anywhere in the shipped record (v198)', !t.marks && !t.names, {marks:t.marks, names:t.names});

  // ---- a full round, played through the UI by tapping
  const round = await p.evaluate(async (UID)=>{
    const sleep = ms => new Promise(r=>setTimeout(r,ms));
    quizState = null; ctx.pre = null;
    const before = Object.values(DATA.records).filter(r=>r.type==='log' && r.unitId===UID && !r.deleted).length;
    go('quiz', {unitId:UID, classId:'bio'});
    await sleep(20);
    if(!quizState) return {built:false};
    const u = unitFor(UID); const n = quizState.order.length;
    let right=0, steps=0, kinds=[];
    while(view==='quiz' && steps++<40){
      const q = u.questions[quizState.order[quizState.i]];
      kinds.push(q.kind||'mc');
      const optBtn = text => [...document.querySelectorAll('#screen .opt:not([disabled])')]
        .find(b=>b.lastChild && b.lastChild.textContent===text);
      if(q.kind==='order'){
        for(const text of q.opts){ const bt = optBtn(text); if(!bt) return {stuck:'order', text}; bt.click(); await sleep(5); }
        const lock = [...document.querySelectorAll('#screen .btn-primary')].find(x=>/Lock it in/.test(x.textContent));
        if(!lock) return {stuck:'lock'}; lock.click(); await sleep(5);
      } else {
        const bt = optBtn(q.opts[q.ans]); if(!bt) return {stuck:'mc', id:q.id}; bt.click(); await sleep(5);
      }
      if(quizState.answered===q.ans) right++;
      const next = document.getElementById('qnext'); if(!next) return {stuck:'next'};
      const last = quizState.i===n-1;
      next.click(); await sleep(10);
      if(last) break;
    }
    const after = Object.values(DATA.records).filter(r=>r.type==='log' && r.unitId===UID && !r.deleted);
    return {built:true, n, right, kinds, logged: after.length-before,
            last: after.length ? {correct:after[after.length-1].correct, total:after[after.length-1].total} : null};
  }, UID);
  ck('a full quiz round plays by tapping the right options, every answer scores, and it logs',
     round.built && round.n>0 && round.right===round.n && round.logged>=1 && round.last && round.last.correct===round.n, round);

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
  console.log(`${out.length} assertions`);
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
