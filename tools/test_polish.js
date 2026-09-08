/* The polish release, behavior by behavior:
   thread hero on Today; right answer's feedback advances; the one-question
   check-in moves straight into the quiz on its own beat; a low post-quiz
   feeling shows the care note and waits for Done; the parent's synced line;
   the live period's progress; the nav's active pill.
   Run: node test_polish.js <port> */
const { chromium } = require('playwright');
const PORT = process.argv[2];
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
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
  const out = [];
  const ck = (name, ok, got) => out.push({name, ok:!!ok, got});

  /* thread on Today */
  await p.evaluate(()=>{ AZ.nowMinutes = ()=>9*60+40; go('today'); });
  await p.waitForTimeout(250);
  const today = await p.evaluate(()=>{
    const hero = document.querySelector('#screen .hero');
    const pleft = document.querySelector('#screen .period .pleft i');
    return { hero: hero ? hero.textContent.slice(0,40) : null,
             pleftW: pleft ? pleft.style.width : null,
             nowRow: !!document.querySelector('#screen .period.now') };
  });
  ck('today: thread hero present', !!today.hero, today);
  ck('today: live period progress', !today.nowRow || (today.pleftW && parseInt(today.pleftW) > 0), today);

  /* nav pill */
  const nav = await p.evaluate(()=>{
    const onb = document.querySelector('.nav-btn.on');
    return onb ? getComputedStyle(onb).backgroundColor : null;
  });
  ck('nav: active tab has a pill', nav && nav !== 'rgba(0, 0, 0, 0)', nav);

  /* right answer's feedback advances */
  await p.evaluate(()=>{
    const u = Object.values(DATA.records).find(r=>r.type==='unit' && !r.deleted
      && (r.questions||[]).length>=4 && !r.guide && !(r.questions||[]).some(q=>q.kind));
    go('quiz',{classId:u.classId, unitId:u.id});
  });
  await p.waitForTimeout(300);
  const adv = await p.evaluate(()=>{
    const q = unitFor(quizState.unitId).questions[quizState.order[quizState.i]];
    const opts=[...document.querySelectorAll('#screen .opt')];
    opts[quizState.optArr.indexOf(q.ans)].click();
    return { i0: quizState.i };
  });
  await p.waitForTimeout(200);
  const adv2 = await p.evaluate(()=>{
    const ex = document.querySelector('#screen .explain');
    const goOn = ex && ex.classList.contains('go-on');
    if(ex) ex.click();
    return { goOn };
  });
  await p.waitForTimeout(250);
  const adv3 = await p.evaluate(()=>({ i1: quizState.i, answered: quizState.answered }));
  ck('quiz: feedback card advances a right answer', adv2.goOn && adv3.i1 === adv.i0+1 && adv3.answered===null, {adv, adv2, adv3});

  /* a wrong answer's feedback must NOT advance on tap */
  const wr = await p.evaluate(()=>{
    const q = unitFor(quizState.unitId).questions[quizState.order[quizState.i]];
    const opts=[...document.querySelectorAll('#screen .opt')];
    opts[quizState.optArr.findIndex(o=>o!==q.ans)].click();
    return quizState.i;
  });
  await p.waitForTimeout(200);
  const wr2 = await p.evaluate(()=>{
    const ex = document.querySelector('#screen .explain');
    const goOn = ex.classList.contains('go-on');
    ex.click();
    return { goOn };
  });
  await p.waitForTimeout(250);
  const wr3 = await p.evaluate(()=>quizState.i);
  ck('quiz: wrong answer keeps the deliberate path', !wr2.goOn && wr3 === wr, {wr, wr2, wr3});
  await p.evaluate(()=>{ quizState = null; });

  /* check-in (2026-09): one readiness tap, no Start button, no Skip — the
     tap itself moves into the quiz on its own short beat. A unit of its own
     (not the one the feedback tests above just quizzed) — reusing that one
     let a parked/resumed round win over the fresh readiness tap, which is a
     separate, real resume-path question and not what this check is about. */
  await p.evaluate(()=>{
    const cid = Object.values(DATA.records).find(r=>r.type==='unit'&&!r.deleted)?.classId || STUDY_CLASSES[0].id;
    const mk = (i) => ({ id:'q'+i, lv:1, from:'source', q:'Checkin Q'+i+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4 });
    put({ id:'checkin-fresh', type:'unit', classId:cid, status:'approved', title:'Checkin Test Unit',
      cards:[], questions:[...Array(5).keys()].map(mk) });
    go('checkin',{unitId:'checkin-fresh', classId:cid});
  });
  await p.waitForTimeout(250);
  const oneScale = await p.evaluate(()=>document.querySelectorAll('#screen .scale').length);
  await p.evaluate(()=>{
    document.querySelectorAll('#screen .scale')[0].querySelectorAll('button')[3].click();
  });
  await p.waitForTimeout(500);
  const auto = await p.evaluate(()=>({ inQuiz: !!quizState, pre: quizState && quizState.pre ? quizState.pre.readiness : null }));
  ck('check-in: a single tap moves straight into the quiz on its own', oneScale===1 && auto.inQuiz && auto.pre === 4, {oneScale, auto});
  await p.evaluate(()=>{ quizState = null; });

  /* postmood: a low feeling shows the care note and waits for a real Done
     tap — the explicit-permission-to-stop message this used to carry
     pre-quiz now lives here, since the pre-quiz feeling tap is gone. */
  await p.evaluate(()=>{
    put({ id:'log-polish', type:'log', mode:'quiz', classId:STUDY_CLASSES[0].id, unitId:'unit-a',
      date:AZ.today(), correct:3, total:4, seconds:60, xp:20 });
    go('postmood',{logId:'log-polish', classId:STUDY_CLASSES[0].id, unitId:'unit-a'});
  });
  await p.waitForTimeout(150);
  await p.evaluate(()=>{ document.querySelectorAll('#screen .scale button')[1].click(); }); // low (v=2)
  await p.waitForTimeout(150);
  const low = await p.evaluate(()=>({
    stayed: view==='postmood',
    careNote: /tell someone you trust today/.test(document.getElementById('screen').textContent),
    doneBtn: [...document.querySelectorAll('#screen button')].find(x=>/^Done$/.test(x.textContent.trim()))?.className
  }));
  ck('postmood: a low feeling shows the care note and waits for Done', low.stayed && low.careNote && /btn-primary/.test(low.doneBtn||''), low);

  /* parent synced line */
  await p.evaluate(()=>{
    Store.set('gist_id','x'); Store.set('gist_token','y');
    Store.set('last_sync', Date.now() - 7*60000);
    Store.set('parent_hash','h'); Store.set('parent_trust', true);
    go('parent');
  });
  await p.waitForTimeout(300);
  const par = await p.evaluate(()=>{
    const t = document.getElementById('screen').textContent;
    return /Synced 7 min ago/.test(t) || /Synced [67] min ago/.test(t);
  });
  ck('parent: last-synced line', par, par);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.name+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
