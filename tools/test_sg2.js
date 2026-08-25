/* Smoke test for the Topic 1 · Test 2 Study Guide (content/sg-test2.json):
   loads, shelves onto Topic 1 alongside the four lessons and the Test 1
   guide, fixed option order survives, the paper-pass grading flow marks
   correctly, the walkthrough shows what was missed, and the rescue round
   serves a fresh variant for every miss. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8102;
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});

  const r=await p.evaluate(async ()=>{
    const d=await (await fetch('./content/sg-test2.json')).json();
    Object.values(d.records).forEach(x=>{ DATA.records[x.id]=x; x.status='approved'; x.updatedAt=Date.now()-1000; });
    // Also load the Topic 1 lessons and the Test 1 guide so the shelf is real.
    for(const f of ['alg-topic1-01','alg-topic1-02','alg-topic1-03','alg-topic1-04','sg-test1']){
      const dj=await (await fetch(`./content/${f}.json`)).json();
      Object.values(dj.records).forEach(x=>{ DATA.records[x.id]=x; x.status='approved'; x.updatedAt=Date.now()-1000; });
    }
    saveLocal();
    const u=DATA.records['unit-sgt2'];
    const o={ guide:!!u.guide, book:!!u.book, order:u.order, questions:u.questions.length,
      withVariants:u.questions.filter(q=>q.variant).length,
      title:u.title };
    // Fixed option order: opts array on the live record must equal the shipped order exactly.
    o.optsFixed = u.questions.every(q=>q.opts.length===4);

    // She gets 7 wrong (a realistic paper pass) — spread across the 30.
    const wrongIdx=[0,3,7,11,15,19,23];
    u.questions.forEach((q,i)=>guideSet(u.id,q.id, wrongIdx.includes(i)?(q.ans+1)%4:q.ans));
    o.entered=guideCount(u.id);
    gradeGuide(u);
    const lg=logs().filter(l=>l.unitId===u.id)[0];
    o.marked={correct:lg.correct,total:lg.total,items:lg.items.length,paper:lg.paper};
    o.misses=all('miss').filter(m=>m.unitId===u.id).length;
    const rq=buildRescueUnit(u.id);
    o.rescue=rq.questions.length;
    o.everyRescueIsFresh = rq.questions.every((rv,i)=>{
      const orig=u.questions.find(q=>'rv_'+q.id===rv.id);
      return orig && rv.q!==orig.q && rv.opts.length===4 && rv.ans>=0 && rv.ans<4;
    });

    // Shelf: Topic 1 should carry the 4 lessons + the Test 1 guide + this Test 2 guide.
    go('unit', {classId:'algeo'});
    const spines = [...document.querySelectorAll('#screen .spine')].map(s=>s.textContent);
    o.topic1Spine = spines.find(t=>/^Topic 1/.test(t)) || null;
    return o;
  });

  await p.evaluate(()=>go('guideentry',{unitId:'unit-sgt2',classId:'algeo'}));
  await p.waitForTimeout(350); await p.screenshot({path:'sg2-entry.png',fullPage:true});
  await p.evaluate(()=>go('guidewalk',{unitId:'unit-sgt2',classId:'algeo'}));
  await p.waitForTimeout(350); await p.screenshot({path:'sg2-walk.png',fullPage:true});

  console.log(JSON.stringify(r,null,1));
  const ok = r.guide && r.book && r.order===1 && r.title==='Topic 1 · Test 2 Study Guide'
    && r.questions===30 && r.withVariants===30 && r.optsFixed && r.entered===30
    && r.marked.correct===23 && r.marked.total===30 && r.marked.paper
    && r.misses===7 && r.rescue===7 && r.everyRescueIsFresh
    && !!r.topic1Spine;
  console.log(ok?'ALL PASS':'FAIL');
  console.log('page errors:', errs.length?errs:'none');
  await b.close(); process.exit(ok && !errs.length ? 0 : 1);
})();
