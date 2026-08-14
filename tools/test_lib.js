const { chromium } = require('playwright');
const PORT = process.argv[2] || 8098;
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const scenario = async (name, seed) => {
    const p=await b.newPage({viewport:{width:390,height:844}});
    const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
    await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
    const out = await p.evaluate(async (seed)=>{
      // what the device already has
      if(seed){
        const d=await (await fetch('./content/sg-test1.json',{cache:'no-store'})).json();
        const u=JSON.parse(JSON.stringify(d.records['unit-sgt1']));
        delete u.guide; delete u.libv; u.questions.forEach(q=>delete q.variant);
        u.title='Topic 1 · Test 1 Study Guide';
        u.status='approved'; u.updatedAt=seed;
        DATA.records[u.id]=u; saveLocal();
      }
      const before = DATA.records['unit-sgt1'];
      // exactly what the button does
      const btn=document.createElement('button'); btn.textContent='Check the library';
      await fetchLibrary(btn);
      const after = DATA.records['unit-sgt1'];
      return {
        had: before ? {status:before.status, guide:!!before.guide, at:before.updatedAt} : null,
        now: after ? {status:after.status, guide:!!after.guide,
          variants:(after.questions||[]).filter(q=>q.variant).length,
          wasApproved:!!after.wasApproved} : null,
        inQueue: drafts().some(u=>u.id==='unit-sgt1'),
        toast: (document.querySelector('.toast')||{}).textContent || ''
      };
    }, seed);
    console.log(name.padEnd(46), JSON.stringify(out));
    if(errs.length) console.log('   errors:', errs);
    await p.close();
    return out;
  };
  const FILE = Date.now();                  // the shipped file is stamped ~now
  const A = await scenario('A. device has NO copy', null);
  const B = await scenario('B. approved BEFORE the file was stamped', FILE - 6*3600e3);
  const C = await scenario('C. approved AFTER the file was stamped', FILE + 2*3600e3);
  console.log();
  console.log('A appears in queue:', A.inQueue);
  console.log('B re-drafts:       ', B.inQueue, '| tagged as an update:', B.now.wasApproved);
  const D = await scenario('D. approved AFTER, but file has a newer libv', FILE + 4*3600e3);
  console.log('C appears in queue:', C.inQueue);
  console.log('D appears in queue:', D.inQueue, '| guide:', D.now.guide,
              '| variants:', D.now.variants, '| tagged update:', D.now.wasApproved);
  await b.close();
})();
