/* The 8/14 newsletter, wired: four one-tap suggestions, the vocab unit's new
   parts-of-speech questions, and the runway card those two produce together. */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto('http://localhost:8131/index.html',{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  await p.evaluate(async ()=>{ for(const path of CONTENT_LIBRARY){
    try{ const r=await fetch(path); const j=await r.json();
      Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
    }catch(e){} } });
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const sug = await p.evaluate(()=>SUGGESTED_ASSESS.filter(a=>a.date>='2026-08-18')
    .map(a=>`${a.date} ${a.classId} ${a.kind} — ${a.title}`));
  ck('four assessments suggested', sug.length===4, sug);
  const cls = await p.evaluate(()=>SUGGESTED_ASSESS.every(a=>!!CLASS_BY_ID[a.classId]));
  ck('every suggestion maps to a real subject', cls, cls);

  const vocab = await p.evaluate(()=>{
    const u = Object.values(DATA.records).find(r=>r.type==='unit'&&/Wordly Wise · Lesson 1$/.test(r.title||''));
    const pos = u.questions.filter(q=>/part of speech|odd one out|different job/i.test(q.q));
    return { total:u.questions.length, pos:pos.length, libv:u.libv,
             sample: pos.map(q=>q.q.slice(0,52)),
             allValid: pos.every(q=>q.opts.length===4 && new Set(q.opts).size===4
                        && q.ans>=0 && q.ans<4 && q.steps && q.steps.length>=3 && q.ex && q.ex.main) };
  });
  ck('five parts-of-speech questions added', vocab.pos===5 && vocab.total===20, vocab);
  ck('each is well formed', vocab.allValid, vocab);
  ck('libv bumped so the fix survives a re-approval', vocab.libv>=1, vocab.libv);

  /* the runway card, on the real Monday of that week */
  const rw = await p.evaluate(()=>{
    AZ.today = ()=>'2026-08-17'; AZ.nowMinutes = ()=>6*60;
    SUGGESTED_ASSESS.filter(a=>a.date>='2026-08-18').forEach(a=>put({
      id:'assess_'+a.id, type:'assess', classId:a.classId, kind:a.kind,
      title:a.title, date:a.date}));
    go('today');
    const c=document.querySelector('#screen .runway');
    return c ? { eyebrow:c.querySelector('.eyebrow').textContent,
                 head:c.querySelector('h3').textContent,
                 hours:c.querySelector('.rhours')?.textContent } : null;
  });
  ck('runway points at the nearest of the four', rw && /History/.test(rw.eyebrow), rw);
  ck('history hours trimmed to the morning', rw && rw.hours && /7:00/.test(rw.hours) && !/3:30/.test(rw.hours), rw);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log('--- suggestions ---'); sug.forEach(s=>console.log('  '+s));
  console.log('--- runway on Mon 8/17 ---');
  console.log('  '+rw.eyebrow+' / '+rw.head); console.log('  '+rw.hours);
  console.log(out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
