const { chromium } = require('playwright');
const PORT = process.argv[2] || 8098;
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  const r=await p.evaluate(async ()=>{
    // she discarded it AFTER the file was stamped — a newer libv must NOT resurrect it
    const d=await (await fetch('./content/sg-test1.json',{cache:'no-store'})).json();
    const lib=d.records['unit-sgt1'];
    DATA.records['unit-sgt1']={...lib, deleted:true, updatedAt: lib.updatedAt + 3600e3};
    delete DATA.records['unit-sgt1'].libv;
    saveLocal();
    const btn=document.createElement('button'); btn.textContent='x';
    await fetchLibrary(btn);
    const after=DATA.records['unit-sgt1'];
    const out={ stayedDeleted: !!after.deleted, inQueue: drafts().some(u=>u.id==='unit-sgt1') };
    // and a deliberate re-ship (updatedAt past the discard) still works
    DATA.records['unit-sgt1']={...lib, deleted:true, updatedAt: lib.updatedAt - 3600e3};
    saveLocal();
    await fetchLibrary(btn);
    out.deliberateReshipWorks = !DATA.records['unit-sgt1'].deleted;
    return out;
  });
  console.log(JSON.stringify(r,null,1));
  const ok = r.stayedDeleted && !r.inQueue && r.deliberateReshipWorks;
  console.log(ok?'ALL PASS':'FAIL');
  console.log('errors:',errs.length?errs:'none');
  await b.close(); process.exit(ok&&!errs.length?0:1);
})();
