const { chromium } = require('playwright');
const PORT = process.argv[2] || 8098;
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  const r=await p.evaluate(async ()=>{
    const d=await (await fetch('./content/sg-test1.json')).json();
    Object.values(d.records).forEach(x=>{ DATA.records[x.id]=x; x.status='approved'; });
    const u=DATA.records['unit-sgt1'];
    const o={ guide:!!u.guide, questions:u.questions.length,
      withVariants:u.questions.filter(q=>q.variant).length };
    // she gets 8 wrong (a realistic paper pass)
    const wrongIdx=[1,4,8,12,16,21,25,29];
    u.questions.forEach((q,i)=>guideSet(u.id,q.id, wrongIdx.includes(i)?(q.ans+1)%4:q.ans));
    o.entered=guideCount(u.id);
    gradeGuide(u);
    const lg=logs().filter(l=>l.unitId===u.id)[0];
    o.marked={correct:lg.correct,total:lg.total,pct:Math.round(lg.correct/lg.total*100),
      items:lg.items.length};
    o.misses=all('miss').filter(m=>m.unitId===u.id).length;
    const rq=buildRescueUnit(u.id);
    o.rescue=rq.questions.length;
    o.everyRescueIsFresh = rq.questions.every((rv,i)=>{
      const orig=u.questions.find(q=>'rv_'+q.id===rv.id);
      return orig && rv.q!==orig.q && rv.opts.length===4;
    });
    return o;
  });
  // screenshots of the three new surfaces
  await p.evaluate(()=>go('guideentry',{unitId:'unit-sgt1',classId:'algeo'}));
  await p.waitForTimeout(350); await p.screenshot({path:'g-entry.png',fullPage:true});
  await p.evaluate(()=>go('guidewalk',{unitId:'unit-sgt1',classId:'algeo'}));
  await p.waitForTimeout(350); await p.screenshot({path:'g-walk.png',fullPage:true});
  await p.evaluate(()=>{const u=DATA.records['unit-sgt1'];
    go('guidewalk',{unitId:'unit-sgt1',classId:'algeo',openW:[guideWrong(u)[0].id]});});
  await p.waitForTimeout(350); await p.screenshot({path:'g-walkopen.png',fullPage:true});
  console.log(JSON.stringify(r,null,1));
  const ok=r.guide&&r.questions===30&&r.withVariants===30&&r.entered===30
    &&r.marked.correct===22&&r.marked.total===30&&r.misses===8&&r.rescue===8
    &&r.everyRescueIsFresh;
  console.log(ok?'ALL PASS':'FAIL');
  console.log('errors:',errs.length?errs:'none');
  await b.close(); process.exit(ok&&!errs.length?0:1);
})();
