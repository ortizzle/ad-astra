/* The word list's three reading tokens, every accent × sky × theme.
   Two surfaces per row, because an OPEN row lays --ac-8 over --raised —
   the tint trap .felt and the Growth Zone chip both hit. Same parse and
   composite helpers as contrast_gzchip.js; Chrome reports the wash as
   color(srgb … / 0.08), which a naive probe reads as opaque. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;

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
  const p=await b.newPage({viewport:{width:390,height:1200}});
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  await p.addStyleTag({content:'*,*::before,*::after{transition:none !important;animation:none !important}'});
  await p.evaluate(async()=>{
    /* Discovered, not named — the same file runs in both apps. */
    for(const path of CONTENT_LIBRARY){
      try{ const j=await (await fetch(path)).json();
        Object.values(j.records).forEach(r=>{ if(r&&r.type){ r.status='approved'; delete r.releaseOn; put(r);} });
      }catch(e){}
    }
    saveLocal();
    /* Every deck has a list since the widening, so pick one that actually
       renders all three tokens — the say-as line only exists on a
       vocabulary card, and measuring a deck without it reads as null. */
    const live=Object.values(DATA.records).filter(r=>r.type==='unit'&&!r.deleted&&hasWordList(r));
    const u=live.find(r=>wordListCards(r).every(c=>c.sp)) || live[0];
    if(!u) throw new Error('no unit with a word list');
    openWordList(u);
    document.querySelectorAll('.modal-box .wlrow')[0].click();   // one open, one shut
  });
  const accents=await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies=await p.evaluate(()=>SKIES.filter(s=>s.id!=='seasonal').map(s=>s.id));
  const rows=[];
  for(const theme of ['light','dark']) for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({theme,sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c, R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme=theme; R.dataset.sky=sky;
      if(getComputedStyle(R).getPropertyValue('--ac').trim()!==hex) throw new Error('accent stuck');
      const all=[...document.querySelectorAll('.modal-box .wlrow')];
      const on=all[0], off=all[1];
      const cs=n=>getComputedStyle(n);
      return { box: cs(document.querySelector('.modal-box')).backgroundColor,
        onBg: cs(on).backgroundColor,  offBg: cs(off).backgroundColor,
        onW: cs(on.querySelector('.wlw')).color,   offW: cs(off.querySelector('.wlw')).color,
        onSp: on.querySelector('.wlsp') ? cs(on.querySelector('.wlsp')).color : null,
        offSp: off.querySelector('.wlsp') ? cs(off.querySelector('.wlsp')).color : null,
        onD: cs(on.querySelector('.wld')).color,
        note: cs(document.querySelector('.wlnote')).color };
    },{theme,sky,acc});
    const box=parse(g.box);
    const onBg=over(parse(g.onBg),box), offBg=over(parse(g.offBg),box);
    const put=(what,fg,bg)=>rows.push({theme,sky,acc,what,ratio:+ratio(over(parse(fg),bg),bg).toFixed(2)});
    put('word (open)',g.onW,onBg);   put('word (shut)',g.offW,offBg);
    if(g.onSp) put('say-as (open)',g.onSp,onBg);
    if(g.offSp) put('say-as (shut)',g.offSp,offBg);
    put('meaning',g.onD,onBg);        put('the note',g.note,box);
  }
  rows.sort((a,b)=>a.ratio-b.ratio);
  console.log('samples:',rows.length);
  [...new Set(rows.map(r=>r.what))].forEach(w=>
    console.log('worst %-16s %s', w, JSON.stringify(rows.find(r=>r.what===w))));
  const bad=rows.filter(r=>r.ratio<4.5);
  console.log('BELOW 4.5:1 →', bad.length? JSON.stringify(bad.slice(0,6)) : 'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
