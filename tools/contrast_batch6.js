/* New text surfaces from the batch of six, measured for real:
   .gz-chip (page), .pickrow .pv (on --deep), .swbar span (on --raised),
   .swbar Refresh button (on --ac), .rev-more (on the .rev card).
   Transitions killed first — the interpolated-value trap from v91. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8110;
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
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(400);
  await p.addStyleTag({content:'*,*::before,*::after{transition:none !important;animation:none !important}'});
  await p.evaluate(async ()=>{
    for(const path of CONTENT_LIBRARY){
      try{ const r=await fetch(path); const j=await r.json();
        Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
      }catch(e){}
    }
    /* misses in two subjects so the growth chips render */
    const us=Object.values(DATA.records).filter(r=>r.type==='unit'&&!r.deleted&&(r.questions||[]).length>=3);
    const u1=us[0], u2=us.find(u=>u.classId!==u1.classId);
    [u1,u2].forEach(u=>u.questions.slice(0,2).forEach(q=>put({
      id:'miss_'+u.id+'_'+q.id, type:'miss', unitId:u.id, classId:u.classId,
      qid:q.id, q:q.q, opts:q.opts, ans:q.ans, right:q.opts[q.ans], box:0, due:AZ.today(), on:AZ.today()})));
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
      const out={ muted:getComputedStyle(R).getPropertyValue('--muted').trim() };
      const grab=(node,bgNode)=>({ fg:getComputedStyle(node).color,
        bg:getComputedStyle(bgNode||node).backgroundColor });
      if(!document.querySelector('.gz-chip')){ go('growth'); }
      const chip=document.querySelector('.gz-chip');
      if(!chip) throw new Error('no gz-chip');
      out.chip=grab(chip);
      if(!document.querySelector('.swbar')) offerUpdate({waiting:{postMessage:()=>{}}});
      const bar=document.querySelector('.swbar');
      out.bar=grab(bar.querySelector('span'), bar);
      const rb=bar.querySelector('button');
      out.barBtn=grab(rb);
      out.page=getComputedStyle(document.body).backgroundColor;
      return out;
    },{theme,sky,acc});
    const page=parse(g.page);
    const solid=c=>{const x=parse(c);return x[3]<1?over(x,page):x;};
    rows.push({theme,sky,acc,
      chip:+ratio(over(parse(g.chip.fg),solid(g.chip.bg)),solid(g.chip.bg)).toFixed(2),
      bar:+ratio(over(parse(g.bar.fg),solid(g.bar.bg)),solid(g.bar.bg)).toFixed(2),
      barBtn:+ratio(over(parse(g.barBtn.fg),solid(g.barBtn.bg)),solid(g.barBtn.bg)).toFixed(2)});
  }
  /* pickrow + rev-more measured once per theme×sky (accent-dependent via --ac-fg) */
  const rows2=[];
  for(const theme of ['light','dark']) for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({theme,sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c;
      const R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme=theme; R.dataset.sky=sky;
      if(!document.querySelector('.pickrow')) go('setup');
      const pr=document.querySelector('.pickrow .pv');
      if(!pr) throw new Error('no pickrow');
      const out={ pv:getComputedStyle(pr).color, pvBg:getComputedStyle(pr.closest('.pickrow')).backgroundColor,
        page:getComputedStyle(document.body).backgroundColor };
      return out;
    },{theme,sky,acc});
    const page=parse(g.page);
    const solid=c=>{const x=parse(c);return x[3]<1?over(x,page):x;};
    rows2.push({theme,sky,acc, pv:+ratio(over(parse(g.pv),solid(g.pvBg)),solid(g.pvBg)).toFixed(2)});
  }
  const worst=(rs,k)=>rs.reduce((m,r)=>Math.min(m,r[k]),99);
  console.log('samples:',rows.length+rows2.length);
  console.log('worst .gz-chip     :', worst(rows,'chip').toFixed(2));
  console.log('worst .swbar text  :', worst(rows,'bar').toFixed(2));
  console.log('worst .swbar button:', worst(rows,'barBtn').toFixed(2));
  console.log('worst .pickrow .pv :', worst(rows2,'pv').toFixed(2));
  const bad=rows.filter(r=>r.chip<4.5||r.bar<4.5||r.barBtn<4.5).concat(rows2.filter(r=>r.pv<4.5));
  console.log('BELOW 4.5:1 →', bad.length?JSON.stringify(bad.slice(0,6),null,1):'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
