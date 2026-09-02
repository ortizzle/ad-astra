/* The batch of six, end to end in the real app:
   1  Growth chips filter the review round by subject and by guide material,
      ordered by the nearest test; cleared card sits below the work.
   2  A re-drafted approved unit shows only what changed; approve clears chg;
      ordinary questions collapse to question + answer.
   3  The update bar renders, posts 'skip', and dismisses.
   4  Test within a week reshapes the plan; within 3 days it takes the thread
      (but never over due reviews).
   5  Ad Astra: the calibration card appears at 4+ pairs, not before.
   6  Clubs rows stop repeating the standard time; settings collapses its grids.
   Run: node test_batch6.js <port> <app>   (app: aa | wf) */
const { chromium } = require('playwright');
const [PORT, APP] = process.argv.slice(2);
const A = r => { if(!r.ok) throw new Error('FAIL '+r.name+' → '+JSON.stringify(r.got)); };

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.addScriptTag({path:__dirname+'/seed.js'});
  await p.waitForTimeout(400);
  await p.evaluate(async ()=>{
    for(const path of CONTENT_LIBRARY){
      try{ const r = await fetch(path); const j = await r.json();
        Object.values(j.records||{}).forEach(rec=>{ rec.status='approved'; DATA.records[rec.id]=rec; });
      }catch(e){}
    }
    saveLocal();
  });
  const out = [];
  const ck = (name, ok, got) => out.push({name, ok:!!ok, got});

  /* ---------- seed: misses in two subjects, a test in 2 days ---------- */
  const seedInfo = await p.evaluate((APP)=>{
    const today = AZ.today();
    const us = Object.values(DATA.records).filter(r=>r.type==='unit'&&!r.deleted&&(r.questions||[]).length>=3);
    const mathU = us.find(u=>CALC_CLASSES.has(u.classId) && !u.guide);
    const otherU = us.find(u=>u.classId!==mathU.classId && !CALC_CLASSES.has(u.classId));
    const guideU = us.find(u=>u.guide);
    const mk = (u,q) => put(scheduleMiss({ id:'miss_'+u.id+'_'+q.id, type:'miss', unitId:u.id,
      classId:u.classId==='__all__'?'math':u.classId, qid:q.id, q:q.q, opts:q.opts, ans:q.ans,
      right:q.opts[q.ans], chose:q.opts[(q.ans+1)%4], why:'', on:today }, false));
    mathU.questions.slice(0,3).forEach(q=>mk(mathU,q));
    otherU.questions.slice(0,2).forEach(q=>mk(otherU,q));
    if(guideU) guideU.questions.slice(0,2).forEach(q=>mk(guideU,q));
    /* every miss due today */
    all('miss').forEach(m=>put({...m, due:today, box:0}));
    put({id:'assess_t', type:'assess', classId:mathU.classId, kind:'test', title:'Batch test',
         date:AZ.shift(today,2)});
    return { math:mathU.classId, other:otherU.classId, guide:!!guideU,
             guideInMath: !!guideU && guideU.classId===mathU.classId,
             due:dueMisses().length };
  }, APP);

  /* ---------- 1. growth ---------- */
  await p.evaluate(()=>go('growth'));
  await p.waitForTimeout(250);
  const g = await p.evaluate((seedInfo)=>{
    const chips = [...document.querySelectorAll('.gz-chip')].map(n=>n.textContent);
    const sc = document.getElementById('screen');
    const btn = [...sc.querySelectorAll('.btn-primary')].find(x=>/review/i.test(x.textContent));
    const heads = [...sc.querySelectorAll('.hintline')].map(h=>h.textContent).filter(t=>/test in|test today|test tomorrow/.test(t));
    /* first actionable control's offset from the top of the screen */
    const firstAction = btn ? Math.round(btn.getBoundingClientRect().top - sc.getBoundingClientRect().top) : null;
    /* cleared card must come after the lists */
    const kids = [...sc.children];
    const clearedIdx = kids.findIndex(k=>/learned for good/.test(k.textContent||''));
    const dividerIdx = kids.findIndex(k=>/Settling in|Due today/.test(k.textContent||''));
    return { chips, firstAction, heads,
      clearedBelow: clearedIdx === -1 || (dividerIdx !== -1 && clearedIdx > dividerIdx) };
  }, seedInfo);
  ck('growth: subject chips render', g.chips.length >= 2, g.chips);
  /* Since the filter rework, chips scope the whole screen: an "Everything"
     reset leads, then subjects ranked by nearest test. */
  ck('growth: reset chip leads, then the test subject', /^Everything/.test(g.chips[0]||'') && g.chips[1] && g.chips[1].includes('test in 2 days'), g.chips);
  /* The chip row above the card is itself a row of actions, so the first
     primary button sits one chip row lower than the v92 audit measured. */
  ck('growth: first action high on screen', g.firstAction !== null && g.firstAction < 380, g.firstAction);
  ck('growth: cleared below the lists', g.clearedBelow, g);
  ck('growth: group headers carry test tag', g.heads.length >= 1, g.heads);

  /* subject chip filters the SCREEN; the primary button then starts a round
     scoped to it. A guide unit inside that subject shows as a 📄 unit chip. */
  await p.evaluate(()=>{ document.querySelectorAll('.gz-chip')[1].click(); });
  await p.waitForTimeout(250);
  const unitChips = await p.evaluate(()=>[...document.querySelectorAll('.gz-chips.units .gz-chip')].map(n=>n.textContent));
  if(seedInfo.guideInMath) ck('growth: guide unit shows as a 📄 unit chip inside its subject', unitChips.some(t=>t.includes('📄')), unitChips);
  await p.evaluate(()=>{ [...document.querySelectorAll('#screen .btn-primary')].find(b=>/review/i.test(b.textContent)).click(); });
  await p.waitForTimeout(300);
  const flt = await p.evaluate((mathCls)=>{
    if(!quizState || quizState.unitId!=='__review__') return {state:'no round'};
    const u = unitFor('__review__');
    const all2 = u.questions.map(q=>DATA.records[q._missId]).filter(Boolean);
    return { n:u.questions.length, allMath: all2.every(m=>m.classId===mathCls), ctxCls: ctx.classId };
  }, seedInfo.math);
  ck('growth: chip filters to one subject', flt.allMath === true && flt.n >= 3, flt);
  await p.evaluate(()=>{ quizState = null; go('growth'); });
  await p.waitForTimeout(200);

  /* ---------- 4. ramp ---------- */
  const ramp = await p.evaluate((seedInfo)=>{
    const plan = studyPlan(AZ.today());
    const entry = plan.find(x=>x.classId===seedInfo.math);
    const t1 = threadTarget(AZ.today());           // due misses exist → growth wins
    const dueWins = /back/.test(t1.title);
    all('miss').forEach(m=>put({...m, due:AZ.shift(AZ.today(),5)}));   // push them out
    const t2 = threadTarget(AZ.today());           // now the test should lead
    return { ramp: entry && entry.ramp, dueWins, t2title: t2 ? t2.title : null };
  }, seedInfo);
  ck('ramp: plan entry flagged', ramp.ramp === true, ramp);
  ck('ramp: due reviews still outrank it', ramp.dueWins === true, ramp);
  ck('ramp: thread becomes the mixed round', /test in 2 days/.test(ramp.t2title||''), ramp);
  await p.evaluate(()=>go('study'));
  await p.waitForTimeout(250);
  const mixBtn = await p.evaluate(()=>{
    const b2 = [...document.querySelectorAll('#screen .btn-secondary')].find(x=>/Mixed round/.test(x.textContent));
    if(!b2) return {found:false};
    b2.click(); return {found:true};
  });
  await p.waitForTimeout(300);
  const mixState = await p.evaluate(()=>quizState ? quizState.unitId : null);
  ck('ramp: mixed round button launches shuffle', mixBtn.found && mixState==='__shuffle__', {mixBtn, mixState});
  await p.evaluate(()=>{ quizState = null; });

  /* ---------- 2. review diff ---------- */
  const rd = await p.evaluate(()=>{
    const u = Object.values(DATA.records).find(r=>r.type==='unit'&&!r.deleted&&(r.questions||[]).length>=4&&(r.cards||[]).length>=1);
    /* the "approved copy" she signed off on */
    const approved = JSON.parse(JSON.stringify(u));
    /* the incoming fix: one question edited, one added, one card removed */
    const inc = JSON.parse(JSON.stringify(u));
    inc.questions[0].q = inc.questions[0].q + ' (fixed)';
    inc.questions.push({...inc.questions[1], id:'q_new_test', q:'A brand new question?'});
    const removedTerm = inc.cards[0].term;
    inc.cards = inc.cards.slice(1);
    inc.title = inc.title;
    const d = unitDelta(approved, inc);
    /* what fetchLibrary would store */
    inc.status='draft'; inc.wasApproved = true; inc.chg = d; inc.updatedAt = Date.now();
    DATA.records[u.id] = inc;
    return { id:u.id, delta:d, removedTerm,
      okDelta: d && d.q.m.length===1 && d.q.a.length===1 && d.c.d.length===1 };
  });
  ck('diff: unitDelta sees edit/add/remove', rd.okDelta, rd.delta);
  await p.evaluate((id)=>go('reviewunit',{unitId:id}), rd.id);
  await p.waitForTimeout(250);
  const rview = await p.evaluate((rd)=>{
    const sc = document.getElementById('screen');
    const revs = [...sc.querySelectorAll('.rev')];
    const txt = sc.textContent;
    return { shown: revs.length,
      says: /Since you approved it/.test(txt),
      removedListed: txt.includes(rd.removedTerm),
      showAllBtn: !![...sc.querySelectorAll('button')].find(b2=>/Show the whole unit/.test(b2.textContent)) };
  }, rd);
  ck('diff: only changed items shown', rview.shown === 2, rview);
  ck('diff: summary sentence', rview.says, rview);
  ck('diff: removed card named', rview.removedListed, rview);
  await p.evaluate(()=>{ [...document.querySelectorAll('#screen button')].find(b2=>/Show the whole unit/.test(b2.textContent)).click(); });
  await p.waitForTimeout(250);
  const full = await p.evaluate(()=>{
    const sc = document.getElementById('screen');
    const revs = sc.querySelectorAll('.rev').length;
    const collapsed = sc.querySelectorAll('.rev-more').length;
    const first = [...sc.querySelectorAll('button')].find(b2=>/Check the options/.test(b2.textContent));
    if(first) first.click();
    return { revs, collapsed };
  });
  await p.waitForTimeout(200);
  const expanded = await p.evaluate(()=>{
    const sc = document.getElementById('screen');
    return { folds: [...sc.querySelectorAll('button')].filter(b2=>/Fold it back/.test(b2.textContent)).length,
      opts: sc.querySelectorAll('.rev .o').length };
  });
  ck('diff: full view collapsible', full.revs > 2 && full.collapsed > 2, full);
  ck('diff: a row expands to options', expanded.folds === 1 && expanded.opts > 4, expanded);
  const approved2 = await p.evaluate(()=>{
    const okB = [...document.querySelectorAll('#screen .btn-primary')].find(b2=>/Approve/.test(b2.textContent));
    okB.click();
    const u = Object.values(DATA.records).find(r=>r.chg || r.wasApproved);
    return { cleared: !u };
  });
  ck('diff: approve clears chg + wasApproved', approved2.cleared, approved2);

  /* ---------- 3. update bar ---------- */
  const sw = await p.evaluate(()=>{
    let posted = null;
    offerUpdate({ waiting: { postMessage: m=>{ posted = m; } } });
    const bar = document.querySelector('.swbar');
    if(!bar) return {bar:false};
    const [refresh, x] = bar.querySelectorAll('button');
    const h = refresh.getBoundingClientRect().height;
    refresh.click();
    const postedNow = posted;
    x.click();
    return { bar:true, postedNow, h, gone: !document.querySelector('.swbar') };
  });
  ck('swbar: renders, posts skip, dismisses', sw.bar && sw.postedNow==='skip' && sw.gone && sw.h>=44, sw);

  /* ---------- 5 + 6. per-app ---------- */
  if(APP==='aa'){
    const cal0 = await p.evaluate(()=>{ go('stars'); return true; });
    await p.waitForTimeout(250);
    const noCard = await p.evaluate(()=>!![...document.querySelectorAll('#screen .eyebrow')].find(e=>/How well you call it/.test(e.textContent)));
    ck('calib: absent under 4 pairs', noCard===false, noCard);
    await p.evaluate(()=>{
      for(let i=0;i<5;i++){
        const lid = 'log_cal'+i;
        put({id:lid, type:'log', mode:'quiz', classId:'algeo', unitId:'u', date:AZ.shift(AZ.today(),-i),
             at:Date.now()-i*86400000, correct:3+ (i%2), total:5, seconds:60, xp:30, hints:0});
        put({id:'mood_cal'+i, type:'mood', when:'pre', logId:lid, readiness:5, feeling:3,
             date:AZ.shift(AZ.today(),-i), at:Date.now()-i*86400000});
      }
      go('today'); go('stars');
    });
    await p.waitForTimeout(250);
    const cal = await p.evaluate(()=>{
      const eye = [...document.querySelectorAll('#screen .eyebrow')].find(e=>/How well you call it/.test(e.textContent));
      if(!eye) return {card:false};
      const card = eye.closest('.card');
      return { card:true,
        dots: card.querySelectorAll('circle').length,
        copy: card.textContent.includes('Within 10 points'),
        second: /you|your/i.test(card.textContent) && !/she|her /i.test(card.textContent) };
    });
    ck('calib: card renders with pairs', cal.card && cal.dots >= 10 && cal.copy, cal);
    ck('calib: second person', cal.second, cal);

    await p.evaluate(()=>go('clubs'));
    await p.waitForTimeout(250);
    const clubs = await p.evaluate(()=>{
      const t = document.getElementById('screen').textContent;
      return { count45: (t.match(/3:45/g)||[]).length, morning: /am \(morning\)|am/.test(t) };
    });
    ck('clubs: standard time not repeated', clubs.count45 <= 2, clubs);
  }

  /* settings collapse — both apps */
  await p.evaluate(()=>go('setup'));
  await p.waitForTimeout(250);
  const setup = await p.evaluate(()=>{
    const sc = document.getElementById('screen');
    const before = sc.querySelectorAll('button').length;
    const rows = [...sc.querySelectorAll('.pickrow')];
    if(rows.length) rows[0].click();
    return { before, rows: rows.length };
  });
  await p.waitForTimeout(200);
  const setup2 = await p.evaluate(()=>{
    const sc = document.getElementById('screen');
    return { grid: sc.querySelectorAll('.emoji-pick button').length,
             after: sc.querySelectorAll('button').length };
  });
  ck('setup: three grids collapsed', setup.rows === 3 && setup.before < 40, setup);
  ck('setup: row expands its grid', setup2.grid >= 10, setup2);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.name+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
