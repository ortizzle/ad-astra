/* Trivia Ladder (v156 / Wayfinder v137): a phone-sized, solo Jeopardy-style
   spin on the real quiz bank. Up to ten MC/analogy questions dealt onto
   point tiles she opens in any order; answering runs through the real,
   unmodified quiz screen and answer() — same qstat/miss/XP crediting as any
   other untimed round. Same file in both repos. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  await p.evaluate(async ()=>{ for(const path of CONTENT_LIBRARY){
    try{ const r=await fetch(path); const j=await r.json();
      Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
    }catch(e){} } });
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  // ---- seed a 10-question lesson so the test never depends on which real
  //      content happens to be shipped
  const seeded = await p.evaluate(()=>{
    const cid = STUDY_CLASSES.find(c => units(c.id).length).id;
    const mk = i => ({ id:'q'+i, lv:1, from:'source', q:'Ladder Q'+i+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4,
      hint:'h'+i, steps:['s1','s2','s3'], ex:{main:'because '+i} });
    put({ id:'ladder-unit', type:'unit', classId:cid, status:'approved', title:'Ladder Test Unit',
      cards:[], questions:[...Array(10).keys()].map(mk) });
    put({ id:'ladder-thin', type:'unit', classId:cid, status:'approved', title:'Too Thin For A Board',
      cards:[], questions:[0,1,2,3].map(mk) });
    return { cid };
  });
  const cid = seeded.cid;

  // ---- the door: gated on 6+ eligible questions, absent below that
  const doors = await p.evaluate(([cid])=>{
    const uFull = DATA.records['ladder-unit'], uThin = DATA.records['ladder-thin'];
    const cardFull = unitCard(uFull, CLASS_BY_ID[cid]);
    const cardThin = unitCard(uThin, CLASS_BY_ID[cid]);
    return {
      full: /Trivia Ladder — play for points/.test(cardFull.textContent),
      thin: /Trivia Ladder — play for points/.test(cardThin.textContent),
    };
  }, [cid]);
  ck('the lesson door renders on a 10-question unit', doors.full, doors);
  ck('the lesson door is absent on a 4-question unit', !doors.thin, doors);

  // ---- the board deals 10 ascending point tiles, none pre-played
  const board = await p.evaluate(([cid])=>{
    const u = DATA.records['ladder-unit'];
    ladderState = null;
    const built = buildLadder(u);
    go('ladder', {unitId:u.id, classId:cid});
    const tiles = [...document.querySelectorAll('.ladder-tile')];
    return { built, count: tiles.length, values: tiles.map(t=>t.textContent),
      allEnabled: tiles.every(t=>!t.disabled), minH: Math.min(...tiles.map(t=>t.getBoundingClientRect().height)) };
  }, [cid]);
  ck('the board deals exactly 10 tiles, ascending 100..1000, none played, each 44px+', board.built
    && board.count===10 && board.values.join(',')==='100,200,300,400,500,600,700,800,900,1000'
    && board.allEnabled && board.minH>=44, board);

  // ---- tapping a tile opens the REAL quiz screen for that one question, in
  //      any order (open tile index 6, not tile 0)
  const opened = await p.evaluate(()=>{
    ladderState.current = 6;
    go('quiz', {unitId:ladderState.unitId, classId:ladderState.classId, ladder:true}, {back:true});
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    return { view, ladderFlag: quizState.ladder, worth: T(document.querySelector('#screen .ladderworth')),
      hasRoundBand: !!document.querySelector('#screen .qstars'),
      question: T(document.querySelector('#screen h3')) };
  });
  ck('tapping tile 7 opens the real quiz screen for a real ladder question, worth 700 in gold, no constellation — the shuffled order means it need not be seed question #6', 
     opened.view==='quiz' && opened.ladderFlag && /700/.test(opened.worth) && /^Ladder Q\d\?$/.test(opened.question) && !opened.hasRoundBand, opened);

  // ---- answering wrong: real miss + qstat.plain written, "Back to the board"
  const wrongPlay = await p.evaluate(()=>{
    const u = DATA.records['ladder-unit'];
    const q = u.questions[quizState.order[quizState.i]];
    const wrongIdx = q.opts.findIndex((_,i)=>i!==q.ans);
    const pos = quizState.optArr.indexOf(wrongIdx);
    document.querySelectorAll('#screen .opt')[pos].click();
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const nextLabel = T(document.getElementById('qnext'));
    document.getElementById('qnext').click();
    return { nextLabel, view, missWritten: !!DATA.records['miss_ladder-unit_'+q.id],
      qstatPlain: DATA.records['qstat_ladder-unit_'+q.id]?.plain,
      tile6: T(document.querySelectorAll('.ladder-tile')[6]), tile6Class: document.querySelectorAll('.ladder-tile')[6].className,
      histNotGrown: HIST[HIST.length-1] && HIST[HIST.length-1][0] !== 'quiz' };
  });
  ck('"Next" reads "Back to the board", a wrong answer writes a real miss and counts toward the lesson', 
     wrongPlay.nextLabel==='Back to the board →' && wrongPlay.view==='ladder' && wrongPlay.missWritten && wrongPlay.qstatPlain===1, wrongPlay);
  ck('the played tile shows ✕ 700 and locks', /✕ 700/.test(wrongPlay.tile6) && /done wrong/.test(wrongPlay.tile6Class), wrongPlay);

  // ---- leaving mid-question (unanswered) does not consume the tile
  const leftEarly = await p.evaluate(()=>{
    ladderState.current = 2;
    go('quiz', {unitId:ladderState.unitId, classId:ladderState.classId, ladder:true}, {back:true});
    const leaveBtn = [...document.querySelectorAll('#screen .tool')].find(b=>/Leave/.test(b.textContent));
    leaveBtn.click();
    return { view, tile2Class: document.querySelectorAll('.ladder-tile')[2].className,
      tile2Disabled: document.querySelectorAll('.ladder-tile')[2].disabled };
  });
  ck('leaving before answering returns to the board with the tile still open', 
     leftEarly.view==='ladder' && leftEarly.tile2Class==='ladder-tile' && !leftEarly.tile2Disabled, leftEarly);

  // ---- finishing the whole board: tally, points, real XP (10/correct + bonus), one log
  const finished = await p.evaluate(()=>{
    const u = DATA.records['ladder-unit'];
    // tile 6 and some other are already 'wrong'/unplayed from above; play everything else right,
    // and answer tile 2 (left open) correctly too, for a clean, checkable total.
    for(let k=0;k<10;k++){
      if(ladderState.results[k]!==null) continue;
      ladderState.current = k;
      go('quiz', {unitId:u.id, classId:u.classId, ladder:true}, {back:true});
      const q = u.questions[quizState.order[quizState.i]];
      const pos = quizState.optArr.indexOf(q.ans);
      document.querySelectorAll('#screen .opt')[pos].click();
      document.getElementById('qnext').click();
    }
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const logs = Object.values(DATA.records).filter(r=>r.type==='log' && r.mode==='ladder' && r.unitId==='ladder-unit');
    const correct = ladderState.results.filter(x=>x==='right').length;
    const points = ladderState.order.reduce((n,_,k)=> n + (ladderState.results[k]==='right'?ladderState.values[k]:0), 0);
    const scoreEl = document.querySelector('.ladderscore');
    return { view, screenTxt: T(document.querySelector('#screen')), logCount: logs.length, log: logs[0],
      correct, points, attempted: unitAttempted(u),
      scoreGold: scoreEl && getComputedStyle(scoreEl).backgroundColor,
      scoreText: T(scoreEl) };
  });
  const expectXp = finished.correct*10 + (finished.correct===10?50:finished.correct>=8?25:0);
  ck('finishing shows the tally, points and real XP, one log record only', 
     finished.logCount===1 && finished.log.total===10 && finished.log.correct===finished.correct
     && finished.log.xp===expectXp && new RegExp(finished.correct+' of 10').test(finished.screenTxt)
     && new RegExp(finished.points.toLocaleString()+' pts').test(finished.screenTxt), finished);
  ck('the final score is the same gold reveal as the in-question badge (#f2ca63)', 
     finished.scoreGold==='rgb(242, 202, 99)' && finished.scoreText===finished.points.toLocaleString()+' pts', finished);
  ck('every one of the 10 questions counts toward the lesson (qstat.plain)', finished.attempted===10, finished);

  // ---- Play again deals a fresh board
  const again = await p.evaluate(()=>{
    const before = ladderState.order.slice();
    document.querySelector('#screen .btn-primary').click();
    return { resultsReset: ladderState.results.every(r=>r===null), sameLength: ladderState.order.length===before.length };
  });
  ck('Play again deals a fresh board with every tile open', again.resultsReset && again.sameLength, again);

  // ---- the mix-mode door on the subject screen, gated the same way
  const mix = await p.evaluate(([cid])=>{
    go('unit', {classId:cid});
    const btn = [...document.querySelectorAll('#screen .btn-secondary')].find(b=>/Trivia Ladder — a mix/.test(b.textContent));
    if(!btn) return {found:false};
    btn.click();
    const tagged = ladderState.order.every(i => !!shuffleUnit.questions[i]._srcUnit);
    return { found:true, view, unitId: ctx.unitId, tagged };
  }, [cid]);
  ck('the subject screen offers a mix-mode ladder door, drawing from __shuffle__ with real source ids', 
     mix.found && mix.view==='ladder' && mix.unitId==='__shuffle__' && mix.tagged, mix);

  // ---- modeLabel knows the mode
  const label = await p.evaluate(()=> modeLabel({mode:'ladder'}));
  ck('modeLabel names it Trivia Ladder for the day view', label==='Trivia Ladder', label);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got).slice(0,500))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
