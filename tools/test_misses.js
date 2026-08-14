const { chromium } = require('playwright');
const [PORT, APP] = process.argv.slice(2);
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(400);
  const r = await p.evaluate(()=>{
    const o={};
    const rows = ()=>document.querySelectorAll('#screen .sesblock.open .qline').length;
    const cap  = ()=>(document.querySelector('#screen .qcap span')||{}).textContent;
    const tog  = ()=>(document.querySelector('#screen .qtog')||{}).textContent;
    const wrong= ()=>[...document.querySelectorAll('#screen .sesblock.open .qline .mk')]
                      .filter(x=>x.classList.contains('no')).length;
    // ses2 = the 18-question English quiz, 6 wrong
    go('day',{date:AZ.today(),dayView:'order',openSes:'ses2'});
    o.default = {rows:rows(), allWrong: rows()===wrong(), cap:cap(), tog:tog()};
    // expand
    go('day',{date:AZ.today(),dayView:'order',openSes:'ses2',allQ:true});
    o.expanded = {rows:rows(), cap:cap(), tog:tog()};
    // toggle survives the order/subject switch
    go('day',{date:AZ.today(),dayView:'subject',openSes:'ses2',allQ:true});
    o.acrossToggle = rows();
    // opening a DIFFERENT session resets to misses-first
    const btn=[...document.querySelectorAll('#screen .sesrow')].find(x=>/Growth Zone/.test(x.textContent));
    btn.click();
    o.newSession = {rows:rows(), cap:cap()};
    // a perfect round: nothing shown by default, but the count is stated
    const cls=Object.keys(CLASS_BY_ID).filter(id=>!(CLASS_BY_ID[id]||{}).bookend)[0];
    put({id:'log-perf',type:'log',mode:'quiz',classId:cls,unitId:'unit-a',date:AZ.today(),
      at:Date.now(),correct:4,total:4,seconds:120,xp:40,hints:0,
      items:[0,1,2,3].map(i=>({c:1,qt:'Q'+i,ch:'right',ca:''}))});
    const rep=dayReport(AZ.today());
    const idx=rep.sessions.findIndex(x=>x.correct===4&&x.total===4);
    go('day',{date:AZ.today(),dayView:'order',openSes:'ses'+idx});
    o.perfect = {rows:rows(), cap:cap(), tog:tog()};
    go('day',{date:AZ.today(),dayView:'order',openSes:'ses'+idx,allQ:true});
    o.perfectOpen = {rows:rows(), tog:tog()};
    return o;
  });
  console.log(APP, JSON.stringify(r,null,1));
  const ok = r.default.rows===6 && r.default.allWrong && r.default.cap==='6 missed of 18'
    && r.default.tog==='Show all 18' && r.expanded.rows===18 && r.expanded.tog==='Misses only'
    && r.acrossToggle===18 && r.newSession.rows===1
    && r.perfect.rows===0 && r.perfect.cap==='All 4 right' && r.perfect.tog==='Show all 4'
    && r.perfectOpen.rows===4 && r.perfectOpen.tog==='Hide';
  console.log(ok?'ALL PASS':'FAIL');
  console.log('errors:',errs.length?errs:'none');
  await b.close(); process.exit(ok&&!errs.length?0:1);
})();
