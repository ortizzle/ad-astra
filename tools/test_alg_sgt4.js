/* Topic 3 · Test 4 Study Guide, Part 1 (content/alg-sg-test4.json, v201).

   A paper study guide (guide:true) whose upload is MISSING the paper's page 2,
   so the unit carries questions 1-8, 20-30 and 32-34. What must hold:

     * the entry grid shows the PAPER'S numbers (paperNo), never 1..22 — or
       she enters #20's letter on a row labelled 9;
     * option order is the paper's, letter for letter, and every answer is
       the letter the maths gives (re-derived here, not read off the file);
     * #31 — two right letters on the paper — is not graded, and a card
       teaches it; nothing exists for 9-19, and the note says the page is
       missing;
     * the paper pass grades, misses land on the ladder, and the rescue round
       asks a fresh variant for each miss;
     * it shelves on Topic 3 after the seven lessons, wearing the prep band.

   Verified by rendering the grid without paperNo and flipping #23's answer
   letter, and watching exactly four assertions fail: both answer-key checks
   and both grid checks (row "20" then held paper question 32). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
const UID = 'unit-alg-sgt4';

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const seeded = await p.evaluate(async ()=>{
    const files = CONTENT_LIBRARY.filter(f=>/alg-topic3|alg-sg-test4/.test(f));
    const shipped = {};
    for(const f of files){
      const j = await (await fetch(f,{cache:'no-store'})).json();
      Object.values(j.records).forEach(r=>{ shipped[r.id]=JSON.parse(JSON.stringify(r));
        r.status='approved'; delete r.releaseOn; put(r); });
    }
    saveLocal();
    const u = DATA.records['unit-alg-sgt4'];
    if(!u) return null;
    return { files:files.length, classId:u.classId, title:u.title, guide:!!u.guide, book:!!u.book,
             order:u.order, libv:u.libv, n:u.questions.length,
             paperNos:u.questions.map(q=>q.paperNo),
             variants:u.questions.filter(q=>q.variant && q.variant.q!==q.q.replace(/^SG #\d+ — /,'')).length,
             sameAsShipped: JSON.stringify(u.questions.map(q=>q.opts))===JSON.stringify(shipped['unit-alg-sgt4'].questions.map(q=>q.opts)) };
  });
  if(!seeded){ console.log('FAIL unit not in CONTENT_LIBRARY'); process.exit(1); }
  const PAPER = [1,2,3,4,5,6,7,8,20,21,22,23,24,25,26,27,28,29,30,32,33,34];
  ck('classId algeo, guide + book, order 1, libv present', seeded.classId==='algeo' && seeded.guide && seeded.book && seeded.order===1 && seeded.libv>=1, seeded);
  ck('the questions carry the paper\'s own numbers: 1-8, 20-30, 32-34', JSON.stringify(seeded.paperNos)===JSON.stringify(PAPER), seeded.paperNos);
  ck('every question has a fresh rescue variant', seeded.variants===seeded.n, seeded.variants);
  ck('option order on the live record is exactly the shipped (paper) order', seeded.sameAsShipped, seeded.sameAsShipped);

  // ---- the answers, re-derived here rather than read off the file
  const answers = await p.evaluate(()=>{
    const u = DATA.records['unit-alg-sgt4'];
    const L = n => { const q = u.questions.find(x=>x.paperNo===n); return q ? 'abcd'[q.ans] : null; };
    return Object.fromEntries([1,2,3,4,5,6,7,8,20,21,22,23,24,25,26,27,28,29,30,32,33,34].map(n=>[n,L(n)]));
  });
  const vx = (a,b,c)=>{ const h=-b/(2*a); return [h, a*h*h+b*h+c]; };
  const derived = {
    1: JSON.stringify(vx(-2,8,-20))==='[2,-12]' ? 'b' : '?',
    2: JSON.stringify(vx(2,24,-16))==='[-6,-88]' ? 'a' : '?',
    3: vx(2,28,-8)[1]===-106 ? 'c' : '?',
    4: vx(-2,28,-10)[1]===88 ? 'c' : '?',
    23: (16 - 72 + 18 + 2)===-36 ? 'c' : '?',
    24: (8 + 4 - 8 - 5)===-1 ? 'b' : '?',
    34: (3*5+3*4<=45 && 2*5+4<=20 && !(2*12+1<=20) && !(3*2+3*15<=45) && !(2*10+4<=20)) ? 'b' : '?',
  };
  const PAPER_KEY = {1:'b',2:'a',3:'c',4:'c',5:'c',6:'d',7:'b',8:'d',20:'a',21:'c',22:'b',23:'c',24:'b',
                     25:'b',26:'d',27:'a',28:'c',29:'b',30:'c',32:'b',33:'c',34:'b'};
  ck('the answers computed here agree with the file', Object.entries(derived).every(([n,l])=>answers[n]===l), {derived, answers});
  ck('every answer letter matches the independently derived key', Object.entries(PAPER_KEY).every(([n,l])=>answers[n]===l),
     Object.entries(PAPER_KEY).filter(([n,l])=>answers[n]!==l));

  // ---- the gap and the two-answer item
  const gap = await p.evaluate(()=>{
    const u = DATA.records['unit-alg-sgt4'];
    const card31 = u.cards.find(c=>/Question 31/.test(c.term));
    const note = u.parentNote.text;
    return { has9to19: u.questions.some(q=>q.paperNo>=9 && q.paperNo<=19),
             has31: u.questions.some(q=>q.paperNo===31),
             card31: !!card31 && /−3, 3 and 4/.test(card31.def) && /b and c/.test(card31.def),
             noteMissing: /questions 9 to 19/.test(note) && /never arrived/.test(note),
             note31: /QUESTION 31 HAS TWO RIGHT ANSWERS/.test(note),
             adapted: u.questions.filter(q=>/\(adapted/.test(q.q)).map(q=>q.paperNo),
             adaptedFlagged: u.questions.filter(q=>/\(adapted/.test(q.q)).every(q=>q.from==='added') };
  });
  ck('nothing was invented for the missing page — no question numbered 9-19', !gap.has9to19, gap);
  ck('#31 is not graded, and a card teaches its zeros and names b and c', !gap.has31 && gap.card31, gap);
  ck('the parent note says page 2 never arrived and flags #31', gap.noteMissing && gap.note31, gap);
  ck('the three adapted items (#24, #27, #30) say so and are flagged added',
     JSON.stringify(gap.adapted)==='[24,27,30]' && gap.adaptedFlagged, gap);

  // ---- the entry grid shows the paper's numbers, and a tap on row "20" answers #20
  const grid = await p.evaluate(()=>{
    go('guideentry', {unitId:'unit-alg-sgt4', classId:'algeo'});
    const rows = [...document.querySelectorAll('#screen .grow')];
    const labels = rows.map(r=>r.querySelector('.gn').textContent);
    const r20 = rows.find(r=>r.querySelector('.gn').textContent==='20');
    r20.querySelectorAll('.gopt button')[0].click();
    const u = DATA.records['unit-alg-sgt4'];
    const a = guidePass(u.id).answers || {};
    const q20 = u.questions.find(q=>q.paperNo===20);
    const tall = [...document.querySelectorAll('#screen .gopt button')].every(x=>x.getBoundingClientRect().height>=44);
    return { labels, set20: a[q20.id]===0, only: Object.keys(a).length, tall };
  });
  ck('the entry grid rows read 1-8, 20-30, 32-34', JSON.stringify(grid.labels)===JSON.stringify(PAPER.map(String)), grid.labels);
  ck('tapping A on the row labelled 20 records it against #20, and nothing else', grid.set20 && grid.only===1, grid);
  ck('every letter button is at least 44px', grid.tall, grid.tall);

  // ---- a paper pass: four wrong, the rest right, then grade
  const pass = await p.evaluate(()=>{
    const u = DATA.records['unit-alg-sgt4'];
    const wrong = [3, 22, 26, 29];
    u.questions.forEach(q=>guideSet(u.id, q.id, wrong.includes(q.paperNo) ? (q.ans+1)%4 : q.ans));
    gradeGuide(u);
    const lg = logs().filter(l=>l.unitId===u.id)[0];
    const misses = all('miss').filter(m=>m.unitId===u.id).map(m=>m.qid).sort();
    const rq = buildRescueUnit(u.id);
    return { correct:lg.correct, total:lg.total, paper:!!lg.paper, misses,
             rescue: rq.questions.length,
             fresh: rq.questions.every(rv=>{ const o=u.questions.find(q=>'rv_'+q.id===rv.id);
               return o && rv.q!==o.q && rv.opts.length===4 && rv.ans>=0 && rv.ans<4; }) };
  });
  ck('the paper pass grades 18 of 22 and logs it as a paper pass', pass.correct===18 && pass.total===22 && pass.paper, pass);
  ck('the four misses land on the ladder against the right questions',
     JSON.stringify(pass.misses)===JSON.stringify(['q22','q26','q29','q3']), pass.misses);
  ck('the rescue round asks a fresh variant for each of the four', pass.rescue===4 && pass.fresh, pass);

  // ---- shelf and treatment
  const shelf = await p.evaluate((UID)=>{
    go('shelf', {classId:'algeo', series:'Topic 3', open:UID});
    const stops = [...document.querySelectorAll('#screen .stop')].map(s=>({t:s.querySelector('.t').textContent, prep:s.classList.contains('prep')}));
    const oc = document.getElementById('shelfopen');
    return { stops, band: !!oc && !!oc.querySelector('.prepband'),
             clock: !!oc && /Beat the clock/.test(oc.textContent),
             loose: shelvesFor('algeo').loose.some(u=>u.id===UID) };
  }, UID);
  const gi = shelf.stops.findIndex(s=>/Test 4 Study Guide/.test(s.t));
  const lastLesson = shelf.stops.map(s=>/3-\d/.test(s.t)).lastIndexOf(true);
  ck('it shelves on Topic 3 after all seven lessons, not loose', gi>lastLesson && lastLesson===6 && !shelf.loose, shelf.stops.map(s=>s.t));
  ck('its stop is gold-ringed and the open card wears the prep band, with no Beat the clock',
     shelf.stops[gi] && shelf.stops[gi].prep && shelf.band && !shelf.clock, shelf);

  // ---- v198: read for questions, never marked; nothing private
  const priv = await p.evaluate((UID)=>{
    const whole = JSON.stringify(DATA.records[UID]);
    return { names: /Ortiz|Sedona/i.test(whole),
             marks: /she (got|wrote|put|answered)|\bscored\b|\d+\s*out of\s*\d+|she was marked/i.test(whole),
             readNote: /read for its questions only/.test(DATA.records[UID].parentNote.text) };
  }, UID);
  ck('no name and no mark anywhere in the shipped record, and the note says it was read for its questions',
     !priv.names && !priv.marks && priv.readNote, priv);

  let bad=0;
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got).slice(0,400)); }
                   else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
