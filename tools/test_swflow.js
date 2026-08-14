/* The update flow, for real: install v-current, bump sw.js on disk, update(),
   expect a WAITING worker (no auto-takeover any more) and the bar; tap
   Refresh; expect exactly one reload with the new worker in control.
   Run: node test_swflow.js <port> <appDir> — restores sw.js afterwards. */
const { chromium } = require('playwright');
const fs = require('fs');
const [PORT, DIR] = process.argv.slice(2);
const SW = DIR + '/sw.js';

(async () => {
  const orig = fs.readFileSync(SW, 'utf8');
  const m = orig.match(/CACHE_VERSION = '([^']+)'/);
  const bumped = orig.replace(m[1], m[1] + '-swtest');
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const cx = await b.newContext({viewport:{width:390,height:844}});
  const p = await cx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  try{
    await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
    await p.waitForFunction(() => navigator.serviceWorker && !!navigator.serviceWorker.controller
      || navigator.serviceWorker.getRegistration().then(r=>!!r), null, {timeout:8000}).catch(()=>{});
    // ensure the first worker is fully active + controlling
    await p.reload({waitUntil:'networkidle'});
    const ctl1 = await p.evaluate(()=>!!navigator.serviceWorker.controller);

    fs.writeFileSync(SW, bumped);
    await p.evaluate(async ()=>{ const r = await navigator.serviceWorker.getRegistration(); await r.update(); });
    await p.waitForSelector('.swbar', {timeout:10000});
    const waiting = await p.evaluate(async ()=>{
      const r = await navigator.serviceWorker.getRegistration();
      return { waiting: !!r.waiting, active: !!r.active };
    });
    /* 'load' can hang on a slow third-party fetch after the swap — wait on
       the committed navigation and the observable end state instead. */
    const nav = p.waitForEvent('framenavigated', {timeout:10000});
    await p.click('.swbar button');           // Refresh
    await nav;
    await p.waitForFunction(()=>document.readyState!=='loading' && typeof AZ!=='undefined', null, {timeout:10000});
    const after = await p.evaluate(async ()=>{
      const r = await navigator.serviceWorker.getRegistration();
      return { controlled: !!navigator.serviceWorker.controller, waiting: !!r.waiting,
               barGone: !document.querySelector('.swbar') };
    });
    const ok = ctl1 && waiting.waiting && after.controlled && !after.waiting && after.barGone;
    console.log(JSON.stringify({ctl1, waiting, after, errors: errs.length?errs:'none'}, null, 1));
    console.log(ok ? 'ALL PASS' : 'FAILURES');
    if(!ok) process.exitCode = 1;
  } finally {
    fs.writeFileSync(SW, orig);
    await b.close();
  }
})();
