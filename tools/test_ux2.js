/* Kat's review (v150 / Wayfinder v131): status on the doors, practice before
   the test, the lesson opening under its own stop, the post-quiz return, and
   test prompts opening the Growth Zone for their subject. Seeds its own
   lesson series so it never depends on which app's content is approved. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});
  const txt = 'n => n ? n.textContent.replace(/\\s+/g," ").trim() : null';

  // ---- seed: a 3-lesson series, 12 questions each (rounds of 5 → 3 rounds)
  await p.evaluate(()=>{
    /* The topmost modal's confirm; then out of the check-in whichever way it
       offers (a strong round adds teach-it-back, so a feeling tap alone stays). */
    window.closeModal = () => { const b = [...document.querySelectorAll('.modal-box .btn-primary')].pop(); if(b) b.click(); };
    window.leavePostmood = () => { if(view !== 'postmood') return;
      const f = document.querySelector('#screen .scale button'); if(f) f.click();
      if(view === 'postmood'){ const d = [...document.querySelectorAll('#screen .btn')].find(b=>/^(Done|Skip)$/.test(b.textContent.trim())); if(d) d.click(); } };
  });
  const seeded = await p.evaluate(()=>{
    const cid = STUDY_CLASSES.find(c => units(c.id).length).id;
    const mk = (n, i) => ({ id:'q'+i, lv:1, from:'source', q:'Q'+i+' of '+n+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4,
      hint:'h', steps:['s1','s2','s3'], ex:{main:'because', tip:'t'} });
    ['One','Two','Three'].forEach((nm,k)=>{
      put({ id:'ux-'+k, type:'unit', classId:cid, status:'approved', title:'UX Series · Lesson '+nm,
        cards:[0,1,2,3,4,5].map(i=>({id:'c'+i, term:'Term '+i, def:'**Def '+i+'**', hint:'k'})),
        questions:[...Array(12).keys()].map(i=>mk(12,i)) });
    });
    return { cid, ok: units(cid).filter(u=>u.id.startsWith('ux-')).length === 3 };
  });
  ck('series seeded', seeded.ok, seeded);
  const cid = seeded.cid;

  // ---- the card: practice first, quiz door last, no "What this covers"
  const card = await p.evaluate(([cid])=>{
    go('shelf', {classId:cid, series:'UX Series', open:'ux-1'});
    const sc = document.getElementById('screen');
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const oc = sc.querySelector('#shelfopen');
    const here = sc.querySelector('.stop.here');
    const kids = [...oc.children].map(k => k.className.split(' ')[0] + ':' + T(k).slice(0,40));
    return {
      inMap: !!oc.closest('.tmap'), underStop: here && here.nextElementSibling === oc,
      hereIsTwo: /Lesson Two/.test(T(here)),
      seclabs: [...oc.querySelectorAll('.seclab')].map(T),
      tiles: [...oc.querySelectorAll('.mtile')].map(T),
      door: T(oc.querySelector('.qdoor')),
      doorAfterTiles: [...oc.querySelectorAll('.mtile, .qdoor')].pop().classList.contains('qdoor'),
      cover: /What this covers/.test(T(oc)), pillsHidden: oc.querySelector('.dtl').hidden,
      ttlH: oc.querySelector('.ttl').getBoundingClientRect().height,
      kids };
  }, [cid]);
  ck('the opened lesson sits inside the map, directly under its stop', card.inMap && card.underStop && card.hereIsTwo, card);
  ck('Practice, then Test yourself', card.seclabs.join('|') === 'Practice|Test yourself', card.seclabs);
  ck('tiles run Flashcards, Beat the clock', card.tiles.length===2 && /^Flashcards/.test(card.tiles[0]) && /^Beat the clock/.test(card.tiles[1]), card.tiles);
  ck('the quiz is the last door, and says round 1 of 3', card.doorAfterTiles && /round 1 of 3/.test(card.door) && /finishes the lesson/.test(card.door), card.door);
  ck('no "What this covers" button; details folded behind the title', !card.cover && card.pillsHidden && card.ttlH >= 44, card);

  const dtl = await p.evaluate(()=>{
    const oc = document.querySelector('#shelfopen');
    oc.querySelector('.ttl').click();
    const oc2 = document.querySelector('#shelfopen');
    return { open: !oc2.querySelector('.dtl').hidden, txt: oc2.querySelector('.dtl').textContent, exp: oc2.querySelector('.ttl').getAttribute('aria-expanded') };
  });
  ck('a tap on the title opens the details', dtl.open && /6 cards/.test(dtl.txt) && /12 questions/.test(dtl.txt) && dtl.exp==='true', dtl);

  // ---- flashcards: a full deck run marks the tile done
  const fc = await p.evaluate(([cid])=>{
    cardState = {start:0};
    go('cards', {unitId:'ux-1', classId:cid});
    for(let i=0;i<6;i++){ cardState.seen.add(cardState.order[cardState.i]); cardState.i = Math.min(5, cardState.i+1); }
    const u = DATA.records['ux-1'];
    finishCards(u);
    const log = all('log').filter(l=>l.mode==='cards' && l.unitId==='ux-1').pop();
    // finishCards lands on the lesson (its shelf), where the tile now reads done
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const tile = document.querySelector('#shelfopen .mtile');
    return { view, seen: log && log.seen, deck: log && log.deck, tile: T(tile), done: tile && tile.classList.contains('done'),
      prog: cardsProgress(u) };
  }, [cid]);
  ck('cards log carries seen and deck; the tile reads done and lands on the lesson', fc.view==='shelf' && fc.seen===6 && fc.deck===6 && fc.done && /deck done/.test(fc.tile), fc);
  const fcOld = await p.evaluate(()=>{
    put({ id:'ux-log-old', type:'log', mode:'cards', classId:'x', unitId:'ux-2', date:AZ.today(), at:Date.now(), correct:0, total:0, seconds:30, xp:20 });
    return cardsProgress(DATA.records['ux-2']);
  });
  ck('a pre-v150 cards log is read back from its xp (20 xp → 4 of 6 seen)', fcOld.best===4 && !fcOld.done, fcOld);

  // ---- Beat the clock does NOT move the map; the quiz does
  const clock = await p.evaluate(([cid])=>{
    quizState = null;
    go('quiz', {unitId:'ux-0', classId:cid, timed:true});
    const u = DATA.records['ux-0'];
    const firstQ = u.questions[quizState.order[0]].id;
    quizState.order.forEach((qi,i)=>{ const q=u.questions[qi]; answer(u,q,q.ans); if(i<quizState.order.length-1){quizState.i++;quizState.answered=null;} });
    finishQuiz(u); closeModal(); leavePostmood();
    const qs = DATA.records['qstat_ux-0_'+firstQ];
    return { attempts: qs && qs.attempts, plain: qs && qs.plain, met: unitAttempted(u), prog: quizProgress(u) };
  }, [cid]);
  ck('a timed round records attempts but no plain sighting: 0 of 12 met', clock.attempts===1 && clock.plain===0 && clock.met===0 && clock.prog.roundsDone===0, clock);

  const legacy = await p.evaluate(()=>{
    put({ id:'qstat_ux-2_q0', type:'qstat', unitId:'ux-2', classId:'x', qid:'q0', q:'?', attempts:2, correct:1 });
    return unitAttempted(DATA.records['ux-2']);
  });
  ck('a qstat written before v150 still counts as met', legacy===1, legacy);

  // ---- an ordinary round: 5 met → round 1 of 3 done, door says round 2 of 3,
  //      postmood returns to the LESSON (rounds remain) even with a miss
  const round1 = await p.evaluate(([cid])=>{
    quizState = null; ctx.pre = null;
    go('quiz', {unitId:'ux-0', classId:cid});
    const u = DATA.records['ux-0'];
    quizState.order.forEach((qi,i)=>{ const q=u.questions[qi]; answer(u,q, i===0 ? (q.ans+1)%4 : q.ans); if(i<quizState.order.length-1){quizState.i++;quizState.answered=null;} });
    finishQuiz(u);
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const modal = T([...document.querySelectorAll('.modal-box')].pop());
    const landed = view;
    // confirm → postmood; the check-in → leaves
    closeModal();
    const pm = view;
    leavePostmood();
    const after = { view, open: ctx.open, series: ctx.series };
    const door = T(document.querySelector('#shelfopen .qdoor'));
    const stopS = T(document.querySelector('#screen .stop.here .s'));
    return { modal, landed, pm, after, door, prog: quizProgress(u), stopS, missed: all('miss').filter(m=>m.unitId==='ux-0').length };
  }, [cid]);
  ck('the results say round 1 of 3 · 2 more', /Round 1 of 3 · 2 more/.test(round1.modal), round1.modal);
  ck('the modal opens over the lesson on its shelf', round1.landed==='shelf' && round1.after.open==='ux-0', round1);
  ck('with rounds left, the check-in returns to the lesson — not the Growth Zone — despite a miss',
     round1.pm==='postmood' && round1.after.view==='shelf' && round1.after.series==='UX Series' && round1.missed===1, round1.after);
  ck('the door now reads round 2 of 3 with 5 of 12 met and a bar', /round 2 of 3/.test(round1.door) && /5 of 12/.test(round1.door) && /2 rounds to go/.test(round1.door), round1.door);
  ck('the map stop agrees: 5 of 12 met', /5 of 12 met/.test(round1.stopS), round1.stopS);

  // ---- finish the lesson with a miss → Growth Zone
  const fin = await p.evaluate(([cid])=>{
    const u = DATA.records['ux-0'];
    for(let r=0;r<2;r++){
      quizState = null; ctx.pre = null;
      go('quiz', {unitId:'ux-0', classId:cid});
      quizState.order.forEach((qi,i)=>{ const q=u.questions[qi]; answer(u,q, (r===1&&i===0) ? (q.ans+1)%4 : q.ans); if(i<quizState.order.length-1){quizState.i++;quizState.answered=null;} });
      finishQuiz(u);
      closeModal();
      if(r===0) leavePostmood();
    }
    leavePostmood();
    return { view, prog: quizProgress(u), done: unitDone(u) };
  }, [cid]);
  ck('once the lesson is finished, a miss sends the check-in to the Growth Zone', fin.view==='growth' && fin.done && fin.prog.roundsDone===3, fin);
  const doneDoor = await p.evaluate(([cid])=>{
    go('shelf', {classId:cid, series:'UX Series', open:'ux-0'});
    const d = document.querySelector('#shelfopen .qdoor');
    return { txt: d.textContent.replace(/\s+/g,' ').trim(), done: d.classList.contains('done'), pip: document.querySelector('#screen .stop.here .pip').textContent };
  }, [cid]);
  ck('a finished lesson: the door says finished, stays open, and the stop wears the gold pip', /finished/.test(doneDoor.txt) && doneDoor.done && doneDoor.pip==='✦', doneDoor);

  // ---- test prompts open the Growth Zone for the subject
  const prompts = await p.evaluate(([cid])=>{
    const real = AZ.today; const d = AZ.today();
    put({ id:'ux-assess', type:'assess', classId:cid, kind:'test', title:'UX test', date:AZ.shift(d, 10), score:null });
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    go('today');
    const rows = [...document.querySelectorAll('#screen .row')];
    const row = rows.find(r => /UX test/.test(T(r)));
    let coming = null;
    if(row){ row.click(); coming = { view, cid: gzFilter.cid }; }
    go('unit', {classId:cid});
    const r2 = [...document.querySelectorAll('#screen .row')].find(r => /UX test/.test(T(r)));
    let subj = null;
    if(r2){ r2.click(); subj = { view, cid: gzFilter.cid }; }
    // runway: 3 days out
    AZ.today = () => AZ.shift(d, 7);
    go('today');
    const rh = document.querySelector('#screen .runway .rwhead');
    let run = null;
    if(rh){ rh.click(); run = { view, cid: gzFilter.cid }; }
    AZ.today = real;
    softDelete('ux-assess');
    return { coming, subj, run, hasMiss: all('miss').some(m=>m.classId===cid) };
  }, [cid]);
  ck('Coming up test row → Growth Zone, filtered to the subject', prompts.coming && prompts.coming.view==='growth' && prompts.coming.cid===cid, prompts);
  ck("the subject screen's test row → Growth Zone, same filter", prompts.subj && prompts.subj.view==='growth' && prompts.subj.cid===cid, prompts);
  ck('the runway head → Growth Zone, same filter', prompts.run && prompts.run.view==='growth' && prompts.run.cid===cid, prompts);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
