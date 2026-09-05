/* "On the horizon" folded into Coming up (v150): the next milestone is one
   quiet row when it is within three weeks, and nothing at all when it is not.
   The quarter countdown row is gone entirely — so the old "same count
   printed twice" bug (v99) cannot come back: there is only one row to print. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8130;
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);

  const r = await p.evaluate(()=>{
    const real = AZ.today;
    const screenOn = d => { AZ.today = () => d; go('today');
      const sc = document.getElementById('screen');
      const divs = [...sc.querySelectorAll('.divider')].map(x=>x.textContent.trim());
      const rows = [...sc.querySelectorAll('.card .row')].map(x=>({
        k:(x.querySelector('.k')||{}).textContent||'', v:(x.querySelector('.v')||{}).textContent||'' }));
      return { divs, rows, txt: sc.textContent.replace(/\s+/g,' ') }; };
    const ms = CAL.milestones.slice().sort((a,b)=>a.date.localeCompare(b.date))
      .find(m => m.date > CAL.firstDay);
    const near = AZ.shift(ms.date, -3), far = AZ.shift(ms.date, -40);
    const out = { ms: ms.name, near, far };
    const n = screenOn(near), f = screenOn(far);
    out.near = { divs:n.divs, msRows: n.rows.filter(x=>x.k.includes(ms.name)), qEnds: /Quarter \d ends/.test(n.txt) };
    out.far  = { divs:f.divs, msRows: f.rows.filter(x=>x.k.includes(ms.name)) };
    AZ.today = real;
    return out;
  });

  const ok = [];
  ok.push(['no "On the horizon" section on either day',
    !r.near.divs.includes('On the horizon') && !r.far.divs.includes('On the horizon'), r]);
  ok.push(['three days out, the milestone is one Coming up row', r.near.msRows.length===1 && /3 days/.test(r.near.msRows[0].v), r.near]);
  ok.push(['the quarter countdown row is gone', !r.near.qEnds, r.near]);
  ok.push(['forty days out, no milestone row at all', r.far.msRows.length===0, r.far]);
  ok.forEach(([n,pass,got])=>console.log((pass?'  ok ':'FAIL ')+n+(pass?'':' → '+JSON.stringify(got))));
  console.log(' milestone:', r.ms, 'near', r.near.msRows[0] && r.near.msRows[0].v);
  const allOk = ok.every(x=>x[1]);
  console.log(allOk?'ALL PASS':'FAILURES', '| errors:', errs.length?errs:'none');
  await b.close();
  if(!allOk || errs.length) process.exit(1);
})();
