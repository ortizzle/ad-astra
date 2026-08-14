// Backgrounding / closing mid-quiz must record the round — and only once.
const { chromium } = require('playwright');
const PORT = process.argv[2], APP = process.argv[3];

(async () => {
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:412,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});

  const r = await p.evaluate(()=>{
    const out={};
    const cls=Object.keys(CLASS_BY_ID).filter(id=>!(CLASS_BY_ID[id]||{}).bookend)[1];
    const mk=id=>{ const qs=[]; for(let i=0;i<6;i++) qs.push({id:'q'+i,lv:1,q:'Q'+i,
      opts:['a','b','c','d'],ans:0,hint:'h',steps:['s1','s2','s3'],ex:{main:'**m**',tip:'t'}});
      put({id,type:'unit',classId:cls,title:id,status:'approved',cards:[],questions:qs});
      return DATA.records[id]; };

    // A) answer 3, then the phone is locked / app switched (visibilitychange)
    const u1=mk('u-close-1');
    go('quiz',{classId:cls,unitId:'u-close-1',timed:false});
    for(let i=0;i<3;i++){ const q=u1.questions[quizState.order[i]];
      answer(u1,q, i<2?q.ans:(q.ans+1)%4); if(i<2){quizState.i++;quizState.answered=null;} }
    document.dispatchEvent(new Event('visibilitychange'));   // not hidden yet
    out.notHidden = logs().filter(l=>l.unitId==='u-close-1').length;   // expect 0
    Object.defineProperty(document,'hidden',{value:true,configurable:true});
    document.dispatchEvent(new Event('visibilitychange'));   // hidden now
    const l1=logs().filter(l=>l.unitId==='u-close-1')[0];
    out.afterHide = l1?{correct:l1.correct,total:l1.total,partial:!!l1.partial,items:(l1.items||[]).length}:null;
    out.roundSurvives = !!quizState && quizState.unitId==='u-close-1';  // must NOT be cleared

    // B) she comes back and finishes the round — must UPDATE, not duplicate
    Object.defineProperty(document,'hidden',{value:false,configurable:true});
    const N=quizState.order.length;
    for(let i=3;i<N;i++){ quizState.i++; quizState.answered=null;
      const q=u1.questions[quizState.order[i]]; answer(u1,q,q.ans); }
    out.roundSize=N;
    finishQuiz(u1);
    const all1=logs().filter(l=>l.unitId==='u-close-1');
    out.logCount = all1.length;                              // expect 1
    out.finalLog = {correct:all1[0].correct,total:all1[0].total,partial:!!all1[0].partial};

    // C) hidden fires repeatedly mid-round — still one log
    const u2=mk('u-close-2');
    go('quiz',{classId:cls,unitId:'u-close-2',timed:false});
    const q2=u2.questions[quizState.order[0]]; answer(u2,q2,q2.ans);
    Object.defineProperty(document,'hidden',{value:true,configurable:true});
    document.dispatchEvent(new Event('visibilitychange'));
    document.dispatchEvent(new Event('visibilitychange'));
    window.dispatchEvent(new Event('pagehide'));
    out.repeatLogs = logs().filter(l=>l.unitId==='u-close-2').length;   // expect 1

    // D) opened but never answered — must log nothing
    const u3=mk('u-close-3');
    Object.defineProperty(document,'hidden',{value:false,configurable:true});
    go('quiz',{classId:cls,unitId:'u-close-3',timed:false});
    Object.defineProperty(document,'hidden',{value:true,configurable:true});
    document.dispatchEvent(new Event('visibilitychange'));
    out.zeroAnswered = logs().filter(l=>l.unitId==='u-close-3').length; // expect 0

    // E) the day view sees it
    const rep = dayReport(AZ.today());
    out.dayQuizzes = rep.quizzes;
    return out;
  });

  console.log(APP, JSON.stringify(r,null,1));
  const ok = r.notHidden===0 && r.afterHide && r.afterHide.total===3 && r.roundSurvives
          && r.logCount===1 && r.finalLog.total===r.roundSize && r.finalLog.partial===false
          && r.repeatLogs===1 && r.zeroAnswered===0;
  console.log(ok?'ALL PASS':'FAIL');
  console.log('errors:',errs.length?errs:'none');
  await b.close(); process.exit((ok&&!errs.length)?0:1);
})();
