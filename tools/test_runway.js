/* The runway card and the Today dedupe.
   Run: node test_runway.js <port> <mathClassId> <hoursWeekday> */
const { chromium } = require('playwright');
const [PORT, CID] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'});
  await p.waitForTimeout(400);
  await p.evaluate(async ()=>{
    for(const path of CONTENT_LIBRARY){
      try{ const r = await fetch(path); const j = await r.json();
        Object.values(j.records||{}).forEach(rec=>{ rec.status='approved'; DATA.records[rec.id]=rec; });
      }catch(e){}
    }
  });
  const out = []; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  /* ---- 1. no test coming → no runway card ---- */
  const none = await p.evaluate(()=>{
    all('assess').forEach(a=>softDelete(a.id));
    AZ.nowMinutes = ()=>9*60;
    go('today');
    return !document.querySelector('#screen .runway');
  });
  ck('no upcoming test → no card', none, none);

  /* ---- 2. a test in 4 days, with review + an open lesson ---- */
  const set = await p.evaluate((CID)=>{
    const today = AZ.today();
    put({id:'assess_rw', type:'assess', classId:CID, kind:'test', title:'Topic 1 Test',
         date:AZ.shift(today,4)});
    const us = units(CID).filter(u=>(u.questions||[]).length>=3);
    us.slice(0,2).forEach(u=>u.questions.slice(0,3).forEach(q=>put({
      id:'miss_'+u.id+'_'+q.id, type:'miss', unitId:u.id, classId:CID, qid:q.id,
      q:q.q, opts:q.opts, ans:q.ans, right:q.opts[q.ans], box:0, due:today, on:today})));
    go('today');
    const card = document.querySelector('#screen .runway');
    if(!card) return {card:false};
    return { card:true,
      eyebrow: card.querySelector('.eyebrow').textContent,
      head: card.querySelector('h3').textContent,
      rows: [...card.querySelectorAll('.rw')].map(r=>r.textContent.replace(/\s+/g,' ').trim()),
      hours: card.querySelector('.rhours') ? card.querySelector('.rhours').textContent : null,
      taps: [...card.querySelectorAll('.rw')].map(r=>!r.disabled) };
  }, CID);
  ck('card renders with the test named', set.card && /Before your/.test(set.eyebrow), set);
  ck('card says when', /in 4 days/.test(set.head||''), set.head);
  ck('review row present and tappable', set.rows.some(r=>/review question/.test(r)) && set.taps[0], set);

  /* the review row runs a round filtered to that subject */
  const filt = await p.evaluate((CID)=>{
    [...document.querySelectorAll('#screen .runway .rw')].find(r=>/review question/.test(r.textContent)).click();
    if(!quizState || quizState.unitId!=='__review__') return {ok:false};
    const u = unitFor('__review__');
    const all2 = u.questions.map(q=>DATA.records[q._missId]).filter(Boolean);
    return { ok:true, n:u.questions.length, allSubject: all2.every(m=>m.classId===CID) };
  }, CID);
  ck('review row filters to the test subject', filt.ok && filt.allSubject, filt);
  await p.evaluate(()=>{ quizState=null; go('today'); });
  await p.waitForTimeout(150);

  /* ---- 3. no duplication with the strip ---- */
  const dup = await p.evaluate(()=>{
    const tile = document.querySelector('#screen .stat');
    const hero = document.querySelector('#screen .hero');
    return { tile: tile.textContent.replace(/\s+/g,' '),
             hero: hero ? hero.textContent.replace(/\s+/g,' ').slice(0,44) : null,
             heroIsGrowth: hero ? /questions are back/.test(hero.textContent) : false };
  });
  ck('hero no longer repeats the Growth tile', !dup.heroIsGrowth, dup);

  const dup2 = await p.evaluate(()=>{
    all('miss').forEach(m=>softDelete(m.id));   // nothing due → strip shows the plan
    go('today');
    const tile = document.querySelector('#screen .stat').textContent.replace(/\s+/g,' ');
    const hero = document.querySelector('#screen .hero');
    const h = hero ? hero.textContent.replace(/\s+/g,' ') : null;
    /* the old bug: tile "15m suggested Theatre" + hero "Start: Theatrical Design" */
    const sameSubject = h && /^Start: /.test(h) &&
      tile.toLowerCase().includes(h.replace('Start: ','').split('·')[0].trim().slice(0,6).toLowerCase());
    return { tile, hero:h, sameSubject:!!sameSubject };
  });
  ck('hero no longer repeats the plan tile', !dup2.sameSubject, dup2);

  /* ---- 4. everything covered → says so rather than showing empty rows ---- */
  const clean = await p.evaluate((CID)=>{
    units(CID).forEach(u=>(u.questions||[]).forEach(q=>put({
      id:'qstat_'+u.id+'_'+q.id, type:'qstat', qid:q.id, unitId:u.id, classId:CID,
      attempts:2, correct:2})));
    go('today');
    const card = document.querySelector('#screen .runway');
    return { rows: card ? card.querySelectorAll('.rw').length : -1,
             says: card ? /Every question in/.test(card.textContent) : false };
  }, CID);
  ck('nothing outstanding → says so, no empty rows', clean.rows===0 && clean.says, clean);

  /* ---- 5. "Before the bell" only when the bell is close ---- */
  const bell = await p.evaluate(()=>{
    /* target the school-day card explicitly — it drops its accent wash when
       the runway card is carrying the screen, so '.card.ac' is not it. */
    const read = m => { AZ.nowMinutes = ()=>m; go('today');
      const c = document.querySelector('#screen .daycard');
      return c.querySelector('h3').textContent + ' | ' + c.querySelector('p').textContent; };
    /* pick a minute genuinely INSIDE a class — 8:20 is mid-lesson in one app
       and a passing gap in the other, so hardcoding it tests the schedule,
       not the code. */
    const list = (typeof dayClasses==='function' ? dayClasses(AZ.today()) : CLASSES)
      .filter(c=>!c.break && !c.bookend);
    const live = list[Math.floor(list.length/2)];
    const mid = Math.floor((live.start + live.end)/2);
    const bell = list.find(c=>c.start > 6*60);
    return { early: read(4*60+14), close: read(bell.start - 5),
             during: read(mid), after: read(16*60), liveName: live.name };
  });
  ck('4am no longer says "Before the bell"', !/Before the bell/.test(bell.early), bell.early);
  ck('4am says the shape of the day', /classes today|School today/.test(bell.early), bell.early);
  ck('close to a bell still says so', /Before the bell/.test(bell.close), bell.close);
  ck('during class unchanged', /until/.test(bell.during), bell.during);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log('--- copy as rendered ---');
  console.log(' eyebrow:', set.eyebrow);
  console.log(' head   :', set.head);
  set.rows.forEach(r=>console.log(' row    :', r));
  console.log(' hours  :', set.hours);
  console.log(' 4am    :', bell.early);
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
