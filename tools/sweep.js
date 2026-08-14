/* Visit every screen with realistic data and report what breaks:
   thrown errors, sub-44px tap targets, horizontal scroll, dead buttons,
   and screens that render nothing at all. */
const { chromium } = require('playwright');
const [PORT, APP] = process.argv.slice(2);

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  p.on('console', m => { if(m.type()==='error') errs.push('console: '+m.text().slice(0,160)); });
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.addScriptTag({path:__dirname+'/seed.js'});
  await p.waitForTimeout(400);

  // give the app enough content that every screen has something to draw
  await p.evaluate(async ()=>{
    for(const path of (typeof CONTENT_LIBRARY!=='undefined'?CONTENT_LIBRARY:[])){
      try{
        const d = await (await fetch('./'+path)).json();
        const rs = Array.isArray(d.records)?d.records:Object.values(d.records);
        rs.forEach(x=>{ DATA.records[x.id]=x; });
      }catch(e){}
    }
    const cid = STUDY_CLASSES[0].id;
    put({id:'assess_s',type:'assess',classId:cid,kind:'test',title:'Unit 3 test',
         date:AZ.shift(AZ.today(),4),points:null,outOf:50,score:null});
    put({id:'assess_d',type:'assess',classId:cid,kind:'quiz',title:'Pop quiz',
         date:AZ.shift(AZ.today(),-4),points:18,outOf:20,score:90});
    put({id:'ask_1',type:'ask',q:'why do i forget things',a:'because…',source:'app',
         date:AZ.today(),at:Date.now()});
    put({id:'teach_x',type:'teach',logId:'log-a',text:'you flip the sign',date:AZ.today()});
  });

  const screens = await p.evaluate(()=>Object.keys(SCREENS));
  const rows = [];
  for(const v of screens){
    const before = errs.length;
    const r = await p.evaluate((v)=>{
      const cid = STUDY_CLASSES[0].id;
      const anyUnit = Object.values(DATA.records).find(u=>u.type==='unit'&&!u.deleted);
      // give each screen the context it expects
      const ctxFor = {
        unit:{classId:cid}, cards:{classId:cid, unitId:anyUnit&&anyUnit.id},
        quiz:{classId:cid, unitId:anyUnit&&anyUnit.id, timed:false},
        brief:{classId:cid, unitId:anyUnit&&anyUnit.id},
        focus:{classId:cid}, checkin:{classId:cid, unitId:anyUnit&&anyUnit.id},
        postmood:{classId:cid, logId:'log-a'},
        reviewunit:{unitId:anyUnit&&anyUnit.id}, shelf:{classId:cid, series:null},
        selfcheck:{classId:cid}, day:{date:AZ.today()},
      }[v] || {};
      try{
        go(v, ctxFor);
      }catch(e){ return {threw:String(e.message)}; }
      const sc = document.getElementById('screen');
      const btns = [...sc.querySelectorAll('button')];
      return {
        threw:null,
        empty: sc.children.length === 0,
        text: (sc.innerText||'').trim().length,
        hScroll: document.documentElement.scrollWidth > window.innerWidth,
        small: btns.filter(x=>{const r=x.getBoundingClientRect();
          return r.height>0 && r.height<44;}).map(x=>x.textContent.trim().slice(0,24)),
        dead: btns.filter(x=>x.disabled).map(x=>x.textContent.trim().slice(0,24)),
      };
    }, v);
    await p.waitForTimeout(120);
    r.screen = v;
    r.newErrors = errs.slice(before);
    rows.push(r);
  }

  const bad = rows.filter(r => r.threw || r.empty || r.hScroll
    || r.small.length || r.dead.length || r.newErrors.length);
  console.log('=== ' + APP + ' — ' + screens.length + ' screens ===');
  if(!bad.length) console.log('clean');
  bad.forEach(r=>{
    const bits = [];
    if(r.threw) bits.push('THREW: '+r.threw);
    if(r.empty) bits.push('rendered nothing');
    if(r.hScroll) bits.push('horizontal scroll');
    if(r.small.length) bits.push('sub-44px: '+JSON.stringify(r.small));
    if(r.dead.length) bits.push('disabled: '+JSON.stringify(r.dead));
    if(r.newErrors.length) bits.push('errors: '+JSON.stringify(r.newErrors));
    console.log('  ' + r.screen.padEnd(12) + ' ' + bits.join(' | '));
  });
  await b.close();
})();
