/* Paper grain on flashcards (v161 / Wayfinder v142): Chris asked whether the
   cards could look more like paper. A fine SVG feTurbulence noise, soft-light
   blended at low opacity, sits behind every card face — subject-painted or
   plain, front or back — so it reads as cardstock rather than a flat color
   tile. Same file in both repos. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
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

  // ---- Every real subject deck: grain on both faces, pattern untouched
  const subjects = await p.evaluate(()=>{
    const cids = STUDY_CLASSES.filter(c => units(c.id).some(u=>!u.own && u.cards.length)).map(c=>c.id);
    return cids.slice(0,4);
  });
  const grainOf = sel => p.evaluate((sel)=>{
    const face = document.querySelector(sel);
    if(!face) return null;
    const before = getComputedStyle(face,'::before');
    return { isSubj: face.classList.contains('subj'),
              patternBg: getComputedStyle(face).backgroundImage,
              grainBg: before.backgroundImage, opacity: before.opacity, blend: before.mixBlendMode };
  }, sel);

  for(const cid of subjects){
    cardState = null;
    await p.evaluate((cid)=>{
      const u = units(cid).find(u=>!u.own && u.cards.length);
      cardState = {unitId:'__none__'};
      go('cards',{unitId:u.id, classId:cid});
    }, cid);
    await p.waitForTimeout(60);
    const front = await grainOf('.face.front');
    ck(`${cid}: front face is subject-painted, keeps its pattern, and gets the grain`,
       front && front.isSubj && front.patternBg !== 'none' && front.grainBg !== 'none'
       && Math.abs(parseFloat(front.opacity)-0.22)<0.001 && front.blend==='soft-light', front);
    await p.evaluate(()=>{ document.querySelector('.flip').click(); });
    await p.waitForTimeout(650);
    const back = await grainOf('.face.back');
    ck(`${cid}: back face also keeps its pattern and gets the grain`,
       back && back.isSubj && back.patternBg !== 'none' && back.grainBg !== 'none', back);
  }

  // ---- A plain face (classId the palette can't resolve): still gets the grain
  const plain = await p.evaluate(async () => {
    put({ id:'papertest-plain', type:'unit', classId:'__all__', status:'approved',
      title:'Plain Face Test', cards:[{id:'c1',term:'Plain term',def:'A plain definition.'}], questions:[] });
    cardState = {unitId:'__none__'};
    go('cards',{unitId:'papertest-plain', classId:'__all__'});
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const front = document.querySelector('.face.front');
    const beforeStyle = getComputedStyle(front, '::before');
    return { isSubj: front.classList.contains('subj'), grainBg: beforeStyle.backgroundImage !== 'none',
             term: T(front.querySelector('.term')) };
  });
  ck('a plain (non-subject) face still gets the grain', !plain.isSubj && plain.grainBg && plain.term==='Plain term', plain);

  // ---- Her own handwritten deck gets it too — same door, same treatment
  const own = await p.evaluate(() => {
    const cid = STUDY_CLASSES[0].id;
    put({ id:'unit-own-'+cid, type:'unit', classId:cid, status:'approved', own:true,
      title:'Your own cards', cards:[{id:'oc1',term:'Her term',def:'Her definition.'}], questions:[] });
    cardState = {unitId:'__none__'};
    go('cards',{unitId:'unit-own-'+cid, classId:cid});
    const front = document.querySelector('.face.front');
    return { isSubj: front.classList.contains('subj'), grainBg: getComputedStyle(front,'::before').backgroundImage !== 'none' };
  });
  ck('her own handwritten deck gets the grain too', own.isSubj && own.grainBg, own);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got).slice(0,400))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
