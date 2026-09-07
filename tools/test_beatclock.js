/* Beat the clock, shortened and slowed down (Chris, 2026-09: "Rivers beat
   the clock seems long ... let's increase the time per question and bring
   her question volume back down to 5 questions or so"). Two independent
   changes, both engine, same file in both apps:
   - quizLimit()'s clamp moved from 8-40s (20s default) to 12-60s (30s
     default) — 1.5x more generous across the board.
   - pickRound(u, true) now always deals BEAT_CLOCK_ROUND (5) questions,
     ignoring a lesson's own u.round (10 for a math lesson-a-day, 12 for a
     Topic Review) — that sizing is for the ORDINARY quiz, where clearing
     the whole lesson is the point; racing a countdown through the same
     10-12 questions was a different, longer thing. pickRound(u, false) is
     completely unaffected. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  // ---- quizLimit(): no data yet -> the new 30s default
  const cold = await p.evaluate(()=> quizLimit());
  ck('with no untimed history, quizLimit() defaults to 30s (was 20s)', cold===30000, cold);

  // ---- quizLimit(): a slow real pace clamps to the new 60s ceiling (was 40s)
  const slow = await p.evaluate(()=>{
    const cid = STUDY_CLASSES.find(c=>units(c.id).length).id;
    put({ id:'bc-slow', type:'log', mode:'quiz', classId:cid, timed:false, date:AZ.today(), at:Date.now(),
          correct:3, total:3, seconds:270, xp:15, hints:0, ansSeconds:270, ansCount:3 }); // 90s/answer average
    return quizLimit();
  });
  ck('a slow real average (90s/answer) clamps to the new 60s ceiling (was 40s)', slow===60000, slow);

  // ---- quizLimit(): a fast real pace clamps to the new 12s floor (was 8s)
  const fast = await p.evaluate(()=>{
    softDelete('bc-slow');
    const cid = STUDY_CLASSES.find(c=>units(c.id).length).id;
    put({ id:'bc-fast', type:'log', mode:'quiz', classId:cid, timed:false, date:AZ.today(), at:Date.now(),
          correct:5, total:5, seconds:20, xp:25, hints:0, ansSeconds:20, ansCount:5 }); // 4s/answer average
    return quizLimit();
  });
  ck('a fast real average (4s/answer) clamps to the new 12s floor (was 8s)', fast===12000, fast);
  await p.evaluate(()=> softDelete('bc-fast'));

  // ---- pickRound: a lesson-a-day math unit (round:10) still deals all 10
  //      untimed, but only BEAT_CLOCK_ROUND (5) when timed
  const seeded = await p.evaluate(()=>{
    const cid = STUDY_CLASSES.find(c => units(c.id).length).id;
    const mk = i => ({ id:'q'+i, lv:1, from:'source', q:'BC Q'+i+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4,
      hint:'h'+i, steps:['s1','s2','s3'], ex:{main:'because '+i} });
    put({ id:'bc-unit', type:'unit', classId:cid, status:'approved', title:'Beat Clock Test Unit', round:10,
      cards:[], questions:[...Array(10).keys()].map(mk) });
    const u = DATA.records['bc-unit'];
    return { cid, untimed: pickRound(u, false).length, timed: pickRound(u, true).length };
  });
  ck('pickRound(u, false) still deals the unit\'s own round size (10)', seeded.untimed===10, seeded);
  ck('pickRound(u, true) caps at BEAT_CLOCK_ROUND (5), ignoring u.round', seeded.timed===5, seeded);

  // ---- end to end: launching Beat the clock on that same unit actually
  //      serves a 5-question round in the live quiz screen
  const live = await p.evaluate(([cid])=>{
    quizState = null;
    go('quiz', {unitId:'bc-unit', classId:cid, timed:true});
    return { order: quizState.order.length, timed: quizState.timed, limit: quizState.limit };
  }, [seeded.cid]);
  ck('launching Beat the clock live serves exactly 5 questions',
     live.timed===true && live.order===5, live);
  ck('the live round\'s countdown sits inside the new 12-60s range', live.limit>=12000 && live.limit<=60000, live);

  // ---- the ordinary (untimed) quiz on the same unit is unaffected
  const ordinary = await p.evaluate(([cid])=>{
    quizState = null;
    go('quiz', {unitId:'bc-unit', classId:cid});
    return { order: quizState.order.length, timed: quizState.timed };
  }, [seeded.cid]);
  ck('the ordinary quiz on the same unit still serves all 10, untimed',
     ordinary.timed===false && ordinary.order===10, ordinary);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got).slice(0,400))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
