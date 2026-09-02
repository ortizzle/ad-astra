/* The SELECTED Growth Zone chip (.gz-chip.on): --ac-fg text on an --ac-8
   wash over the page, every accent × sky × theme. Same parse/composite
   helpers as contrast_batch6.js — Chrome reports the wash as
   color(srgb … / 0.08), which a naive probe reads as opaque. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
const parse=c=>{let m=c.match(/color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\)/);
 if(m)return[+m[1]*255,+m[2]*255,+m[3]*255,m[4]==null?1:+m[4]];
 m=c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
 if(m)return[+m[1],+m[2],+m[3],m[4]==null?1:+m[4]]; throw new Error('bad "'+c+'"');};
const over=(f,b)=>f.slice(0,3).map((v,i)=>v*f[3]+b[i]*(1-f[3])).concat([1]);
const lum=c=>{const f=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});
 return .2126*f[0]+.7152*f[1]+.0722*f[2]};
const ratio=(a,b)=>{const[x,y]=[lum(a),lum(b)].sort((m,n)=>n-m);return (x+.05)/(y+.05)};
(async()=>{
  const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  await p.addStyleTag({content:'*,*::before,*::after{transition:none !important;animation:none !important}'});
  await p.evaluate(async()=>{
    for(const path of CONTENT_LIBRARY){
      try{ const j=await (await fetch(path)).json();
        Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
      }catch(e){}
    }
    const us=Object.values(DATA.records).filter(r=>r.type==='unit'&&!r.deleted&&(r.questions||[]).length>=3);
    const u1=us[0], u2=us.find(u=>u.classId!==u1.classId);
    [u1,u2].forEach(u=>u.questions.slice(0,2).forEach(q=>put({
      id:'miss_'+u.id+'_'+q.id, type:'miss', unitId:u.id, classId:u.classId,
      qid:q.id, q:q.q, opts:q.opts, ans:q.ans, right:q.opts[q.ans], box:0, due:AZ.today(), on:AZ.today()})));
    go('growth');
  });
  const accents=await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies=await p.evaluate(()=>SKIES.filter(s=>s.id!=='seasonal').map(s=>s.id));
  const rows=[];
  for(const theme of ['light','dark']) for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({theme,sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c;
      const R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme=theme; R.dataset.sky=sky;
      if(getComputedStyle(R).getPropertyValue('--ac').trim()!==hex) throw new Error('accent stuck');
      const on=document.querySelector('.gz-chip.on'), off=document.querySelector('.gz-chip:not(.on)');
      if(!on||!off) throw new Error('chips missing');
      const grab=n=>({fg:getComputedStyle(n).color, bg:getComputedStyle(n).backgroundColor});
      return { on:grab(on), off:grab(off), page:getComputedStyle(document.body).backgroundColor };
    },{theme,sky,acc});
    const page=parse(g.page);
    for(const k of ['on','off']){
      const bg=over(parse(g[k].bg), page), fg=over(parse(g[k].fg), bg);
      rows.push({theme,sky,acc,chip:k,ratio:+ratio(fg,bg).toFixed(2)});
    }
  }
  rows.sort((a,b)=>a.ratio-b.ratio);
  console.log('samples:',rows.length);
  console.log('worst selected chip  :', JSON.stringify(rows.filter(r=>r.chip==='on')[0]));
  console.log('worst unselected chip:', JSON.stringify(rows.filter(r=>r.chip==='off')[0]));
  const bad=rows.filter(r=>r.ratio<4.5);
  console.log('BELOW 4.5:1 →', bad.length? JSON.stringify(bad.slice(0,6)) : 'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
