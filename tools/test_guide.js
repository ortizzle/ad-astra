const { chromium } = require('playwright');
const [PORT,APP]=process.argv.slice(2);
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  const r=await p.evaluate(()=>{
    const o={}; const cid=STUDY_CLASSES[0].id;
    const mkq=(n)=>({id:'q'+n,lv:2,q:'Guide question '+n,opts:['w'+n,'x'+n,'y'+n,'z'+n],
      ans:n%4,hint:'h',steps:['a','b','c'],ex:{main:'**because**'},
      variant:{q:'Variant of '+n,opts:['p','q','r','s'],ans:1,hint:'h2',
               steps:['d','e','f'],ex:{main:'**v**'}}});
    put({id:'u-g',type:'unit',classId:cid,title:'Topic 9 · Test 9 Study Guide',
      status:'approved',guide:true,book:true,order:1,cards:[],
      questions:[0,1,2,3,4,5].map(mkq)});
    const u=DATA.records['u-g'];

    // ---- the doors: a shelved guide is reached through its shelf, which is
    // how the real Test 1 Study Guide is reached (Topic 1 -> the row).
    go('shelf',{classId:cid, series:'Topic 9', unitId:'u-g'});
    let txt=document.getElementById('screen').innerText;
    if(!/I did it on paper/.test(txt)){
      // fall back to the loose-unit path so the check is about the doors,
      // not about which screen happens to host the card
      const host=document.createElement('div');
      host.appendChild(unitCard(DATA.records['u-g'], CLASS_BY_ID[cid]));
      txt=host.innerText;
    }
    o.doors={paper:/I did it on paper/.test(txt), work:/Work it here/.test(txt),
      noClock: !/Beat the clock/.test(txt)};

    // ---- paper entry: enter 6 answers, 2 of them wrong
    go('guideentry',{unitId:'u-g',classId:cid});
    u.questions.forEach((q,i)=>guideSet('u-g',q.id, i<2 ? (q.ans+1)%4 : q.ans));
    o.entered=guideCount('u-g');
    o.wrongCount=guideWrong(u).length;
    // tapping the same letter twice clears it
    const g=guidePass('u-g'); const nx={...g.answers}; delete nx['q0']; put({...g,answers:nx});
    o.afterClear=guideCount('u-g');
    guideSet('u-g','q0',(u.questions[0].ans+1)%4);

    gradeGuide(u);
    const lg=logs().filter(l=>l.unitId==='u-g');
    o.graded={logs:lg.length, correct:lg[0].correct, total:lg[0].total, paper:!!lg[0].paper};
    o.missesMade=all('miss').filter(m=>m.unitId==='u-g').length;   // expect 2
    o.qstats=Object.values(DATA.records).filter(x=>x.type==='qstat'&&x.unitId==='u-g').length;
    o.submitted=guidePass('u-g').submitted;

    // ---- rescue round: variants only for the missed ones, ladder untouched
    const boxesBefore=all('miss').filter(m=>m.unitId==='u-g').map(m=>m.box);
    const rq=buildRescueUnit('u-g');
    o.rescue={questions:rq.questions.length, isVariant:/^Variant of/.test(rq.questions[0].q),
      id:rq.id};
    quizState=null;
    go('quiz',{unitId:'__rescue__',classId:cid});
    for(let i=0;i<quizState.order.length;i++){
      const qq=rq.questions[quizState.order[i]];
      answer(rq,qq,qq.ans);                       // all correct
      if(i<quizState.order.length-1){quizState.i++;quizState.answered=null;}
    }
    finishQuiz(rq);
    const boxesAfter=all('miss').filter(m=>m.unitId==='u-g').map(m=>m.box);
    o.ladderUntouched = JSON.stringify(boxesBefore)===JSON.stringify(boxesAfter);
    o.rescueWrongMakesNoNewMiss = all('miss').filter(m=>m.unitId==='u-g').length===2;

    // ---- work-here mode: authored order, fixed letters, resumable
    put({id:'u-g2',type:'unit',classId:cid,title:'Topic 9 · Test 9 Guide B',
      status:'approved',guide:true,book:true,cards:[],questions:[0,1,2,3,4,5].map(mkq)});
    const u2=DATA.records['u-g2'];
    quizState=null;
    go('quiz',{unitId:'u-g2',classId:cid,guideMode:'work'});
    o.work={all:quizState.order.length, inOrder:quizState.order.join(',')==='0,1,2,3,4,5'};
    // letters must NOT be shuffled on a guide
    o.lettersFixed = quizState.optArr ? quizState.optArr.join(',')==='0,1,2,3' : 'n/a';
    // answer 2, walk away, come back
    for(let i=0;i<2;i++){ const qq=u2.questions[quizState.order[i]];
      answer(u2,qq,qq.ans); if(i<1){quizState.i++;quizState.answered=null;} }
    o.savedMidway=guideCount('u-g2');
    quizState=null;
    go('quiz',{unitId:'u-g2',classId:cid,guideMode:'work'});
    o.resumed={left:quizState.order.length, startsAt:quizState.order[0]};
    return o;
  });
  // survives a reload?
  await p.reload({waitUntil:'networkidle'});
  const after=await p.evaluate(()=>({saved:guideCount('u-g2'), submitted:guidePass('u-g').submitted}));
  console.log(APP, JSON.stringify({...r, afterReload:after},null,1));
  const ok = r.doors.paper&&r.doors.work&&r.doors.noClock
    && r.entered===6 && r.wrongCount===2 && r.afterClear===5
    && r.graded.logs===1 && r.graded.correct===4 && r.graded.total===6 && r.graded.paper
    && r.missesMade===2 && r.qstats===6 && r.submitted
    && r.rescue.questions===2 && r.rescue.isVariant
    && r.ladderUntouched && r.rescueWrongMakesNoNewMiss
    && r.work.all===6 && r.work.inOrder && r.lettersFixed===true
    && r.savedMidway===2 && r.resumed.left===4 && r.resumed.startsAt===2
    && after.saved===2 && after.submitted===true;
  console.log(ok?'ALL PASS':'FAIL');
  console.log('errors:',errs.length?errs:'none');
  await b.close(); process.exit(ok&&!errs.length?0:1);
})();
