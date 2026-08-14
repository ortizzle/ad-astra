const { chromium } = require('playwright');
const [PORT,APP]=process.argv.slice(2);
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  const r=await p.evaluate(()=>{
    const o={}; const cid=STUDY_CLASSES[0].id;
    const mkq=n=>({id:'q'+n,lv:1,q:'Q'+n,opts:['a','b','c','d'],ans:0,hint:'h',
      steps:['1','2','3'],ex:{main:'**m**'}});
    // ---- round bar
    put({id:'u-band',type:'unit',classId:cid,title:'Topic 9 · 9-1 One',status:'approved',
      cards:[],questions:[0,1,2,3,4].map(mkq)});
    const u=DATA.records['u-band'];
    go('quiz',{classId:cid,unitId:'u-band',timed:false});
    const band=()=>document.querySelector('#screen .qband');
    o.bandExists=!!band();
    o.starsAtStart=document.querySelectorAll('#screen .qband .star').length;
    o.segsAtStart=document.querySelectorAll('#screen .qband .seg').length;
    for(let i=0;i<3;i++){ const q=u.questions[quizState.order[i]];
      answer(u,q, i===1?(q.ans+1)%4:q.ans);
      if(i<2){quizState.i++;quizState.answered=null;} }
    o.lit=document.querySelectorAll('#screen .qband .star.lit').length;
    o.dim=document.querySelectorAll('#screen .qband .star.dim').length;
    o.segs=document.querySelectorAll('#screen .qband .seg').length;
    o.missSegs=document.querySelectorAll('#screen .qband .seg.miss').length;
    // shape is stable per unit, and different units differ
    const pA=JSON.stringify(roundPoints('u-band:5',5,320,54));
    const pA2=JSON.stringify(roundPoints('u-band:5',5,320,54));
    const pB=JSON.stringify(roundPoints('u-other:5',5,320,54));
    o.stable = pA===pA2; o.varies = pA!==pB;
    // never clips
    const all=[...roundPoints('u-band:12',12,320,54), ...roundPoints('zz:2',2,320,54),
               ...roundPoints('q:1',1,320,54)];
    o.inBounds = all.every(([x,y])=>x>=0&&x<=320&&y>=8&&y<=46);
    o.noName = !/constellation|The Otter/i.test(document.getElementById('screen').innerText);

    // ---- topic map
    const mk=(id,t,cap)=>{const x={id,type:'unit',classId:cid,title:t,status:'approved',
      cards:[],questions:[0,1,2,3].map(mkq)}; if(cap)x.capstone=true; put(x); return x;};
    mk('m1','Topic 8 · 8-1 A'); mk('m2','Topic 8 · 8-2 B'); mk('m3','Topic 8 · 8-3 C');
    mk('mr','Topic 8 · Topic Review', true);
    go('shelf',{classId:cid, series:'Topic 8'});
    o.stops=document.querySelectorAll('#screen .stop').length;
    o.crestShown=!!document.querySelector('#screen .tcrest');
    o.crestWon=!!document.querySelector('#screen .tcrest.won');
    o.cardBelow=!!document.querySelector('#screen .card h3');
    // a series with no capstone offers no crest
    mk('w1','Wordly · Lesson 1'); mk('w2','Wordly · Lesson 2'); mk('w3','Wordly · Lesson 3');
    go('shelf',{classId:cid, series:'Wordly'});
    o.noCapstoneNoCrest = !document.querySelector('#screen .tcrest');
    // finish the capstone -> crest is won, and stays won when a lesson is added after
    ['q0','q1','q2','q3'].forEach(qid=>put({id:'qstat_mr_'+qid,type:'qstat',unitId:'mr',
      classId:cid,qid,q:'x',attempts:1,correct:1}));
    go('shelf',{classId:cid, series:'Topic 8'});
    o.wonAfterReview=!!document.querySelector('#screen .tcrest.won');
    mk('m4','Topic 8 · 8-4 D');   // a lesson shipped afterwards
    go('shelf',{classId:cid, series:'Topic 8'});
    o.stillWon=!!document.querySelector('#screen .tcrest.won');
    o.hScroll=document.documentElement.scrollWidth>window.innerWidth;
    o.smallTargets=[...document.querySelectorAll('#screen button')]
      .filter(x=>{const r=x.getBoundingClientRect();return r.height>0&&r.height<44;}).length;
    return o;
  });
  console.log(APP, JSON.stringify(r,null,1));
  const ok = r.bandExists && r.starsAtStart===5 && r.segsAtStart===0
    && r.lit===2 && r.dim===1 && r.segs===2 && r.missSegs===1
    && r.stable && r.varies && r.inBounds && r.noName
    && r.stops===4 && r.crestShown && !r.crestWon && r.cardBelow
    && r.noCapstoneNoCrest && r.wonAfterReview && r.stillWon
    && !r.hScroll && r.smallTargets===0;
  console.log(ok?'ALL PASS':'FAIL');
  console.log('errors:',errs.length?errs:'none');
  await b.close(); process.exit(ok&&!errs.length?0:1);
})();
