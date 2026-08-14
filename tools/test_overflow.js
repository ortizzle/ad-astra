// Nothing may exceed the viewport width — including expanded content.
const { chromium } = require('playwright');
const [PORT,APP]=process.argv.slice(2);
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  const r=await p.evaluate(async ()=>{
    const cid=STUDY_CLASSES[0].id;
    const long='Total: E(n) = 400 + 15(n - 40), which simplifies to 15n - 200. '
      + 'Piecewise: 10n up to 40, then this, and a little more text besides.';
    const mkq=n=>({id:'q'+n,lv:2,q:'A deliberately long question '+n+' that keeps going for a while',
      opts:['alpha '+n,'beta '+n,'gamma '+n,'delta '+n],ans:1,hint:'h',
      steps:[long,long,long],ex:{main:'**'+long+'**'},
      variant:{q:'Variant '+n,opts:['p','q','r','s'],ans:0,hint:'h',
        steps:[long,long,long],ex:{main:'**'+long+'**'}}});
    put({id:'u-ovf',type:'unit',classId:cid,title:'Topic 9 · Test 9 Study Guide',
      status:'approved',guide:true,book:true,cards:[],questions:[0,1,2].map(mkq)});
    const u=DATA.records['u-ovf'];
    u.questions.forEach(q=>guideSet('u-ovf',q.id,(q.ans+1)%4));   // all wrong
    gradeGuide(u);
    // open EVERY walkthrough at once — the state the earlier screenshot missed
    go('guidewalk',{unitId:'u-ovf',classId:cid,openW:u.questions.map(q=>q.id)});
    const wide=[...document.querySelectorAll('#screen *')]
      .filter(n=>n.getBoundingClientRect().right > window.innerWidth + 1)
      .map(n=>n.className+' :: '+(n.textContent||'').trim().slice(0,40));
    return { docWidth:document.documentElement.scrollWidth, view:window.innerWidth,
      overflowing:wide.slice(0,6), count:wide.length,
      stepsRendered:document.querySelectorAll('#screen .step').length };
  });
  console.log(APP, JSON.stringify(r,null,1));
  const ok = r.docWidth <= r.view && r.count===0 && r.stepsRendered===9;
  console.log(ok?'ALL PASS':'FAIL');
  console.log('errors:',errs.length?errs:'none');
  await b.close(); process.exit(ok&&!errs.length?0:1);
})();
