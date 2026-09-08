/* The companion doing more work (Chris, 2026-09: "sharing words of
   encouragement during tests and games"). Two new moments, both firing
   exactly once: a mid-round line in an ordinary quiz's explanation card, and
   a Daily-Double line on Junior Jeopardy's one hard tile per board. Neither
   should ever appear on Beat the clock, the review ladder, or the daily
   three — those stay exactly as light-touch as before. Same file, both
   apps. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const seeded = await p.evaluate(()=>{
    put({ id:'prefs', type:'prefs', companion:{sp:'dolphin', nm:'Pip'} });
    const cid = STUDY_CLASSES.find(c => units(c.id).length).id;
    const mk = (i) => ({ id:'q'+i, lv:1, from:'source', q:'CM Q'+i+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4 });
    put({ id:'cm-ord', type:'unit', classId:cid, status:'approved', title:'Companion Mid Lesson', round:9,
      cards:[], questions:[...Array(9).keys()].map(mk) });
    put({ id:'cm-jj', type:'unit', classId:cid, status:'approved', title:'Companion Mid JJ Lesson',
      cards:[], questions:[...Array(9).keys()].map(mk) });
    put({ id:'cm-old', type:'unit', classId:cid, status:'approved', title:'Companion Mid Older Lesson',
      cards:[], questions:[...Array(9).keys()].map(mk) });
    DATA.records['cm-old'].questions.forEach(q=>put({id:'qstat_cm-old_'+q.id,type:'qstat',unitId:'cm-old',qid:q.id,attempts:2,correct:2,plain:2}));
    return { cid };
  });
  const cid = seeded.cid;

  // ---- an ordinary round: no bubble on question 1, one at the midpoint, none after
  const ord = await p.evaluate(()=>{
    const bubbleNow = ()=>document.querySelector('#screen .perch .bubble')?.textContent || null;
    go('quiz', {unitId:'cm-ord', classId: STUDY_CLASSES[0].id});
    const answer = ()=>{ const q = unitFor('cm-ord').questions[quizState.order[quizState.i]];
      document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(q.ans)].click(); };
    const mid = Math.floor(quizState.order.length/2);
    const seenAt = [];
    for(let k=0;k<quizState.order.length;k++){
      answer();
      seenAt.push({ i: quizState.i, bubble: bubbleNow() });
      if(k < quizState.order.length-1) document.getElementById('qnext').click();
    }
    return { mid, seenAt };
  });
  const midHit = ord.seenAt.find(x=>x.i===ord.mid);
  const othersClean = ord.seenAt.filter(x=>x.i!==ord.mid).every(x=>!x.bubble);
  ck('an ordinary round shows the companion bubble at exactly the midpoint question, and nowhere else',
     midHit && !!midHit.bubble && othersClean, ord);

  // ---- Beat the clock and the review ladder never show it (each on its
  //      own fresh unit, so no leftover quizState from the round above)
  const skip = await p.evaluate(([cid])=>{
    const bubbleNow = ()=>document.querySelector('#screen .perch .bubble')?.textContent || null;
    const check = (label, build) => {
      quizState = null;
      build();
      if(!quizState) return { label, hit:false, threw:true };
      const mid = Math.floor(quizState.order.length/2);
      let hit = false;
      for(let k=0;k<quizState.order.length;k++){
        const u = quizState.ladder ? ladderUnit : unitFor(quizState.unitId);
        const qq = u.questions[quizState.order[quizState.i]];
        document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(qq.ans)].click();
        if(quizState.i===mid && bubbleNow()) hit = true;
        if(k < quizState.order.length-1){
          const nb = document.getElementById('qnext');
          if(nb) nb.click(); else break;
        }
      }
      return { label, hit };
    };
    const mk = (i) => ({ id:'q'+i, lv:1, from:'source', q:'CM2 Q'+i+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4 });
    put({ id:'cm-timed', type:'unit', classId:cid, status:'approved', title:'Companion Mid Timed', round:9,
      cards:[], questions:[...Array(9).keys()].map(mk) });
    const results = [];
    results.push(check('timed', ()=>go('quiz',{unitId:'cm-timed', classId:cid, timed:true})));
    // seed enough misses, due TODAY, for a review round
    DATA.records['cm-ord'].questions.slice(0,6).forEach(q=>put({ ...scheduleMiss({
      id:'miss_cm-ord_'+q.id, type:'miss', unitId:'cm-ord', classId:cid, qid:q.id,
      q:q.q, opts:q.opts, ans:q.ans, right:q.opts[q.ans], chose:'x', why:'', on:AZ.today() }, false), due:AZ.today() }));
    results.push(check('review', ()=>{ buildReviewUnit({classId:cid}); go('quiz',{unitId:'__review__', classId:cid}); }));
    return results;
  }, [cid]);
  skip.forEach(r=> ck(`the ${r.label} round never shows the mid-round bubble`, !r.threw && !r.hit, r));

  // ---- Junior Jeopardy: the Daily Double gets a companion line before
  //      answering, and it is gone once answered
  const jj = await p.evaluate(([cid])=>{
    ladderState = null;
    go('ladder', {unitId:'cm-jj', classId:cid});
    const s = ladderState, k = s.dd;
    const tile = [...document.querySelectorAll('.jj-tile')].find(t=>t.getAttribute('aria-label')===`${s.cats[s.catOf[k]].nm} for ${s.values[k]}`);
    tile.click();
    const modalBtn = document.querySelector('.modal-overlay .btn-primary');
    if(modalBtn) modalBtn.click();
    const beforeAnswer = document.querySelector('#screen .perch .bubble')?.textContent || null;
    const q = ladderUnit.questions[quizState.order[quizState.i]];
    document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(q.ans)].click();
    const afterAnswer = document.querySelector('#screen .perch .bubble')?.textContent || null;
    document.getElementById('qnext').click();   // back to the board, for the next check
    return { beforeAnswer, afterAnswer };
  }, [cid]);
  ck('a Junior Jeopardy Daily Double shows a companion line before she answers, and it clears once she does',
     !!jj.beforeAnswer && !jj.afterAnswer, jj);

  // ---- an ordinary (non-Daily-Double) Jeopardy tile never shows this line
  const jjPlain = await p.evaluate(([cid])=>{
    const s = ladderState;
    const plainK = s.order.find(k=>k!==s.dd && s.results[k]===null);
    const tile = [...document.querySelectorAll('.jj-tile')].find(t=>t.getAttribute('aria-label')===`${s.cats[s.catOf[plainK]].nm} for ${s.values[plainK]}`);
    tile.click();
    return { bubble: document.querySelector('#screen .perch .bubble')?.textContent || null };
  }, [cid]);
  ck('an ordinary (non-Daily-Double) Jeopardy tile never shows the Daily-Double line', !jjPlain.bubble, jjPlain);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got).slice(0,500))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
})();
