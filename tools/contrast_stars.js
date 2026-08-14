/* New Stars surfaces: the locked-in chip (number + subject on --deep, with a
   subject-coloured edge) and the trophy row, across accent x sky x theme. */
const { chromium } = require('playwright');
const PORT = process.argv[2];
const parse=c=>{let m=c.match(/color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\)/);
 if(m)return[+m[1]*255,+m[2]*255,+m[3]*255,m[4]==null?1:+m[4]];
 m=c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
 if(m)return[+m[1],+m[2],+m[3],m[4]==null?1:+m[4]]; throw new Error('bad "'+c+'"');};
const over=(f,b)=>f.slice(0,3).map((v,i)=>v*f[3]+b[i]*(1-f[3])).concat([1]);
const lum=c=>{const f=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});
 return .2126*f[0]+.7152*f[1]+.0722*f[2]};
const ratio=(a,b)=>{const[x,y]=[lum(a),lum(b)].sort((m,n)=>n-m);return (x+.05)/(y+.05)};
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  await p.evaluate(async ()=>{ for(const path of CONTENT_LIBRARY){
      try{ const r=await fetch(path); const j=await r.json();
        Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
      }catch(e){} } });
  await p.addScriptTag({path:__dirname+'/seed_rich.js'}); await p.waitForTimeout(300);
  await p.evaluate(()=>{
    STUDY_CLASSES.forEach(c=>shelvesFor(c.id).shelves.forEach(sh=>{
      const cap=capstoneOf(sh.units);
      if(cap) cap.questions.forEach(q=>put({id:'qstat_'+cap.id+'_'+q.id,type:'qstat',qid:q.id,
        unitId:cap.id, classId:cap.classId, attempts:2, correct:2, updatedAt:Date.now()}));
    }));
    put({id:'log_f',type:'log',mode:'readfin',classId:'english',book:'A Book',
         date:AZ.today(),at:Date.now(),correct:0,total:0,seconds:0,xp:50});
  });
  await p.addStyleTag({content:'*{transition:none !important;animation:none !important}'});
  const accents=await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies=await p.evaluate(()=>SKIES.filter(s=>s.id!=='seasonal').map(s=>s.id));
  const rows=[];
  for(const theme of ['light','dark']) for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({theme,sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c; const R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme=theme; R.dataset.sky=sky;
      if(getComputedStyle(R).getPropertyValue('--ac').trim()!==hex) throw new Error('accent stuck');
      go('stars');
      const lk=document.querySelector('#screen .lk');
      const tr=document.querySelector('#screen .trophy');
      if(!lk) throw new Error('no locked-in chip');
      if(!tr) throw new Error('no trophy row');
      return { ln:getComputedStyle(lk.querySelector('.ln')).color,
               lt:getComputedStyle(lk.querySelector('.lt')).color,
               lkBg:getComputedStyle(lk).backgroundColor,
               tn:getComputedStyle(tr.querySelector('.tn')).color,
               tk:getComputedStyle(tr.querySelector('.tk')).color,
               trBg:getComputedStyle(tr).backgroundColor,
               page:getComputedStyle(document.body).backgroundColor };
    },{theme,sky,acc});
    const page=parse(g.page);
    const solid=c=>{const x=parse(c);return x[3]<1?over(x,page):x;};
    const lkBg=solid(g.lkBg), trBg=solid(g.trBg);
    rows.push({theme,sky,acc,
      ln:+ratio(over(parse(g.ln),lkBg),lkBg).toFixed(2),
      lt:+ratio(over(parse(g.lt),lkBg),lkBg).toFixed(2),
      tn:+ratio(over(parse(g.tn),trBg),trBg).toFixed(2),
      tk:+ratio(over(parse(g.tk),trBg),trBg).toFixed(2)});
  }
  const worst=k=>rows.reduce((m,r)=>Math.min(m,r[k]),99);
  console.log('samples:',rows.length);
  ['ln','lt','tn','tk'].forEach(k=>console.log('  worst .'+k+':', worst(k).toFixed(2)));
  const bad=rows.filter(r=>r.ln<4.5||r.lt<4.5||r.tn<4.5||r.tk<4.5);
  console.log('BELOW 4.5:1 →', bad.length?JSON.stringify(bad.slice(0,5),null,1):'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
