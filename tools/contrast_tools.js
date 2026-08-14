/* The two new surfaces: the tool row (on the page, under a subject accent) and
   the results tally (inside the modal box). Both across accent x sky x theme.
   Measured against the OPAQUE surface underneath — Chrome reports accent tints
   as color(srgb .. / .08) and a naive probe reads that as opaque. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8099;
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
  await p.evaluate(async ()=>{
    for(const path of CONTENT_LIBRARY){
      try{ const r=await fetch(path); const j=await r.json();
        Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
      }catch(e){}
    }
  });
  /* .tool transitions its colour, so getComputedStyle right after a theme flip
     returns the INTERPOLATED value, not the new one — a probe measuring that
     reports a failure the app does not have. Kill every transition first. */
  await p.addStyleTag({content:'*,*::before,*::after{transition:none !important;animation:none !important}'});
  const accents=await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies=await p.evaluate(()=>SKIES.filter(s=>s.id!=='seasonal').map(s=>s.id));

  // Land on a real quiz, then open the results modal with a hand-made round.
  await p.evaluate(()=>{
    const u=Object.values(DATA.records).find(r=>r.type==='unit'&&!r.deleted
      &&CALC_CLASSES.has(r.classId)&&(r.questions||[]).length>=4&&!r.guide);
    go('quiz',{classId:u.classId,unitId:u.id});
  });
  await p.waitForTimeout(300);

  const rows=[];
  for(const theme of ['light','dark']) for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({theme,sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c;
      const R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme=theme; R.dataset.sky=sky;
      if(getComputedStyle(R).getPropertyValue('--ac').trim()!==hex) throw new Error('accent stuck');
      if(R.dataset.theme!==theme) throw new Error('theme stuck');
      const out={};
      out.muted=getComputedStyle(R).getPropertyValue('--muted').trim();
      const tool=document.querySelector('#screen .tool small');
      if(!tool) throw new Error('no tool row on the quiz screen');
      const S=getComputedStyle(document.getElementById('screen'));
      // #screen overrides --ac with the subject colour; the tools sit on the page ink.
      out.toolFg=getComputedStyle(tool).color;
      out.pageBg=getComputedStyle(document.body).backgroundColor;
      out.screenAc=S.getPropertyValue('--ac').trim();
      // the tally lives in a modal box
      let box=document.querySelector('.modal-box');
      if(!box){
        showModal({title:'x',message:'y',build:(bx)=>{
          const t=document.createElement('div'); t.className='tally';
          const s=document.createElement('span'); s.textContent='9 of 13 first time';
          t.appendChild(s); bx.appendChild(t);
        }});
        box=document.querySelector('.modal-box');
      }
      const ts=box.querySelector('.tally span');
      out.tallyFg=getComputedStyle(ts).color;
      out.tallyBg=getComputedStyle(box).backgroundColor;
      return out;
    },{theme,sky,acc});
    const page=parse(g.pageBg), boxBg=parse(g.tallyBg);
    const boxOpaque = boxBg[3]<1 ? over(boxBg,page) : boxBg;
    rows.push({theme,sky,acc,muted:g.muted,
      tool:+ratio(over(parse(g.toolFg),page),page).toFixed(2),
      tally:+ratio(over(parse(g.tallyFg),boxOpaque),boxOpaque).toFixed(2)});
  }
  if(new Set(rows.map(r=>r.theme+r.sky+':'+r.muted)).size !== rows.length/6)
    throw new Error('--muted did not track theme/sky — the probe is lying');
  const worst=k=>rows.reduce((m,r)=>Math.min(m,r[k]),99);
  console.log('samples:',rows.length,'| distinct tool ratios:',new Set(rows.map(r=>r.tool)).size);
  console.log('worst .tool label :', worst('tool').toFixed(2));
  console.log('worst .tally      :', worst('tally').toFixed(2));
  const bad=rows.filter(r=>r.tool<4.5||r.tally<4.5);
  console.log('BELOW 4.5:1 →', bad.length?JSON.stringify(bad.slice(0,8),null,1):'none');
  await b.close();
})();
