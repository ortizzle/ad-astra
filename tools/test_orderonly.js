/* Order-only library updates (Wayfinder v149 / Ad Astra v167): fifty
   shipped units were rebalanced so their correct answers no longer all sit
   in slot A. The app shuffles options at render time, so nothing she sees
   changes — and fetchLibrary() now recognises a unit whose questions keep
   the same four options and the same correct answer with only the order
   moved, carrying her approval across instead of re-drafting it. A real
   change (a reworded option) still takes the ordinary re-draft path. Same
   file in both repos. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const run = async (mutate) => {
    /* The app's service worker fetches library files itself, and page.route
       never sees a worker's requests — so the stubbed library below would
       be bypassed and the real 48 files would load. Block it for this test. */
    const cx = await b.newContext({viewport:{width:390,height:844}, serviceWorkers:'block'});
    const p = await cx.newPage();
    const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
    await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
    const path = await p.evaluate(()=>CONTENT_LIBRARY[0]);
    const orig = await (await p.request.get(`http://localhost:${PORT}/${path.replace(/^\.\//,'')}`)).json();
    const unit = Object.values(orig.records).find(r=>r.type==='unit');
    // the device: this unit, approved an hour ago, exactly as shipped
    await p.evaluate(([u])=>{ const c=JSON.parse(JSON.stringify(u)); c.status='approved'; c.updatedAt=Date.now()-3600e3; DATA.records[c.id]=c; saveLocal(); }, [unit]);
    // the library: the same unit, edited, newer libv, stamped now
    const served = JSON.parse(JSON.stringify(orig));
    const su = served.records[unit.id];
    mutate(su); su.libv = (su.libv||0)+1; su.updatedAt = Date.now();
    await p.route(`**/${path.replace(/^\.\//,'')}`, r => r.fulfill({ contentType:'application/json', body: JSON.stringify(served) }));
    // every OTHER library file must not interfere: serve them as empty
    await p.route('**/content/*.json', r => r.request().url().endsWith(path.replace(/^\.\//,'')) ? r.fallback() : r.fulfill({contentType:'application/json', body:'{"v":4,"records":{}}'}));
    const res = await p.evaluate(async ([id])=>{
      const btn=document.createElement('button'); btn.textContent='Check the library';
      await fetchLibrary(btn);
      const r = DATA.records[id];
      return { status:r.status, libv:r.libv, chg:!!r.chg, wasApproved:!!r.wasApproved, inQueue: drafts().some(u=>u.id===id),
        toast:(document.getElementById('toast')||{}).textContent||'', firstOpts:(r.questions.find(q=>!q.kind||q.kind==='mc')||{}).opts, errs:[] };
    }, [unit.id]);
    res.errs = errs; res.unitId = unit.id;
    await cx.close();
    return res;
  };

  // 1. order only: rotate every MC question's options, keep the answer text
  const swapped = await run(u=>{ u.questions.forEach(q=>{ if((!q.kind||q.kind==='mc'||q.kind==='analogy') && Array.isArray(q.opts) && q.opts.length===4){ const a=q.ans, w=(a+1)%4; [q.opts[a],q.opts[w]]=[q.opts[w],q.opts[a]]; q.ans=w; } }); });
  ck('an order-only update lands (newer libv on the record) and stays APPROVED — no re-draft, not in the queue, not tagged as an update',
     swapped.libv>=1 && swapped.status==='approved' && !swapped.inQueue && !swapped.chg && !swapped.wasApproved && !swapped.errs.length, swapped);
  ck('the toast does not announce an update she has to read', !/update/.test(swapped.toast), swapped);

  // 2. a real change: reword one option — takes the ordinary re-draft path
  const reworded = await run(u=>{ const q=u.questions.find(q=>(!q.kind||q.kind==='mc') && q.opts && q.opts.length===4); q.opts[(q.ans+1)%4] = q.opts[(q.ans+1)%4] + ' (reworded)'; });
  ck('a reworded option is a real change: the unit re-drafts, is tagged as an update, and shows in the queue',
     reworded.status==='draft' && reworded.inQueue && reworded.wasApproved && !reworded.errs.length, reworded);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got).slice(0,500))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  await b.close();
  if(!out.every(r=>r.ok)) process.exit(1);
})();
