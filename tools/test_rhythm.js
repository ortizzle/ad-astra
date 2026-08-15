/* One rhythm, three steps — and no gap smaller than the scale allows. */
const { chromium } = require('playwright');
const [PORT,TAG] = process.argv.slice(2);
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

  const gaps = await p.evaluate(()=>{
    const seen = {};
    ['today','study','growth','stars'].forEach(v=>{
      go(v);
      const sc=document.getElementById('screen'), kids=[...sc.children];
      kids.forEach((k,i)=>{
        const nx=kids[i+1]; if(!nx) return;
        const g=Math.round(nx.getBoundingClientRect().top - k.getBoundingClientRect().bottom);
        if(g>=0) (seen[g]=seen[g]||[]).push(v+':'+(k.className||k.tagName).split(' ')[0]);
      });
    });
    return Object.fromEntries(Object.entries(seen).map(([g,v])=>[g,v.length]));
  });
  const vals = Object.keys(gaps).map(Number).sort((a,b)=>a-b);
  ck('no gap under 8px between blocks', vals.every(v=>v===0||v>=8), gaps);
  ck('rhythm is a small set of steps', vals.filter(v=>v>0).length<=4, vals);

  const wknd = await p.evaluate(()=>{
    const sat = '2026-08-15';                       // a Saturday
    const real = AZ.today; AZ.today = ()=>sat;
    go('today');
    const c = document.querySelector('#screen .daycard');
    const eyebrow = c.querySelector('.eyebrow').textContent;
    const head = c.querySelector('h3').textContent;
    const body = c.querySelector('p').textContent;
    AZ.today = real;
    return { eyebrow, head, body,
      dayTwice: (eyebrow+' '+head).match(/Saturday/g)?.length || 0 };
  });
  ck('weekday is not printed twice', wknd.dayTwice===1, wknd);
  ck('weekend says when school is back', /Back on Monday/.test(wknd.body), wknd);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(TAG, 'gaps seen:', JSON.stringify(gaps));
  console.log(' weekend:', wknd.eyebrow, '/', wknd.head, '/', wknd.body);
  console.log(out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
