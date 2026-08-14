/* The runway card's new text surfaces: the big accent number (.rn) and the
   two body lines, across accent x sky x theme. Transitions off, knob asserted. */
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
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(400);
  await p.addStyleTag({content:'*{transition:none !important;animation:none !important}'});
  await p.evaluate(async ()=>{
    for(const path of CONTENT_LIBRARY){
      try{ const r=await fetch(path); const j=await r.json();
        Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
      }catch(e){}
    }
    const cid = STUDY_CLASSES[0].id;
    put({id:'assess_c', type:'assess', classId:cid, kind:'test', title:'T', date:AZ.shift(AZ.today(),3)});
    const us = units(cid).filter(u=>(u.questions||[]).length>=3);
    us.slice(0,1).forEach(u=>u.questions.slice(0,3).forEach(q=>put({
      id:'miss_'+u.id+'_'+q.id, type:'miss', unitId:u.id, classId:cid, qid:q.id,
      q:q.q, opts:q.opts, ans:q.ans, right:q.opts[q.ans], box:0, due:AZ.today(), on:AZ.today()})));
  });
  const accents=await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies=await p.evaluate(()=>SKIES.filter(s=>s.id!=='seasonal').map(s=>s.id));
  const rows=[];
  for(const theme of ['light','dark']) for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({theme,sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c; const R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme=theme; R.dataset.sky=sky;
      if(getComputedStyle(R).getPropertyValue('--ac').trim()!==hex) throw new Error('accent stuck');
      go('today');
      const card=document.querySelector('#screen .runway');
      if(!card) throw new Error('no runway card');
      const rn=card.querySelector('.rn'), rt=card.querySelector('.rt'),
            rh=card.querySelector('.rhours'), row=card.querySelector('.rw');
      return { rn:getComputedStyle(rn).color, rt:getComputedStyle(rt).color,
        rh:rh?getComputedStyle(rh).color:null, rowBg:getComputedStyle(row).backgroundColor,
        cardBg:getComputedStyle(card).backgroundColor,
        page:getComputedStyle(document.body).backgroundColor };
    },{theme,sky,acc});
    const page=parse(g.page);
    const solid=c=>{const x=parse(c);return x[3]<1?over(x,page):x;};
    const rowBg=solid(g.rowBg), cardBg=solid(g.cardBg);
    rows.push({theme,sky,acc,
      rn:+ratio(over(parse(g.rn),rowBg),rowBg).toFixed(2),
      rt:+ratio(over(parse(g.rt),rowBg),rowBg).toFixed(2),
      rh:g.rh?+ratio(over(parse(g.rh),cardBg),cardBg).toFixed(2):99});
  }
  const worst=k=>rows.reduce((m,r)=>Math.min(m,r[k]),99);
  console.log('samples:',rows.length);
  console.log('worst .rn (count)  :', worst('rn').toFixed(2));
  console.log('worst .rt (text)   :', worst('rt').toFixed(2));
  console.log('worst .rhours      :', worst('rh').toFixed(2));
  const bad=rows.filter(r=>r.rn<4.5||r.rt<4.5||r.rh<4.5);
  console.log('BELOW 4.5:1 →', bad.length?JSON.stringify(bad.slice(0,5),null,1):'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
