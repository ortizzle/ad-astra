/* Pair up's board: the tile text (plain, selected, paired), the "paired"
   mark, the column label and the verdict note — every accent × sky × theme.
   Selected tiles sit on an --ac-8 wash, which Chrome reports as
   color(srgb … / 0.08); a naive probe reads that as opaque and reports a
   ratio the app does not have, so everything is composited down to the
   opaque page first. Same parse/composite helpers as contrast_gzchip.js. */
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
    for(const path of CONTENT_LIBRARY){ try{ const j=await (await fetch(path)).json();
      Object.values(j.records||{}).forEach(rec=>{ if(rec.type==='unit'){rec.status='approved'; delete rec.releaseOn; DATA.records[rec.id]=rec;} });}catch(e){} }
    saveLocal();
    const u=Object.values(DATA.records).find(r=>r.type==='unit'&&!r.deleted&&pairPool(r).length>=4);
    pairState=null; go('pairup',{unitId:u.id, classId:u.classId});
    /* One of each state on screen at once: paired, selected, plain, plus a
       verdict note in each of its two colours (the ok one is measured; the
       no one differs only in border). */
    const st=pairState;
    st.lefts[0].done=true; st.rights.find(r=>r.qid===st.lefts[0].q.id).done=true;
    st.sel=st.lefts[1];
    st.note={t:'Paired. That one counted.', ok:true};
    render();
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
      const plain=[...document.querySelectorAll('.pairtile')].find(t=>!t.classList.contains('sel')&&!t.classList.contains('done'));
      const sel=document.querySelector('.pairtile.sel'), done=document.querySelector('.pairtile.done');
      const note=document.querySelector('.pairnote'), lab=document.querySelector('.pairlab');
      if(!plain||!sel||!done||!note||!lab) throw new Error('board incomplete');
      const grab=n=>({fg:getComputedStyle(n).color, bg:getComputedStyle(n).backgroundColor, op:+getComputedStyle(n).opacity});
      return {plain:grab(plain), sel:grab(sel), done:grab(done),
              mark:{...grab(done.querySelector('.pmark')), op:+getComputedStyle(done).opacity},
              note:grab(note), lab:grab(lab),
              page:getComputedStyle(document.body).backgroundColor};
    },{theme,sky,acc});
    const page=parse(g.page);
    for(const k of ['plain','sel','done','mark','note','lab']){
      let bg=over(parse(g[k].bg), page);
      let fg=parse(g[k].fg);
      /* A paired tile is dimmed with opacity, which fades its text TOWARD the
         page behind it — that has to be modelled or the dim reads as free. */
      const o = g[k].op==null ? 1 : g[k].op;
      if(o < 1){ bg = over([...bg.slice(0,3), o], page); fg = [...fg.slice(0,3), (fg[3]??1)*o]; }
      rows.push({theme,sky,acc,part:k,ratio:+ratio(over(fg,bg),bg).toFixed(2)});
    }
  }
  rows.sort((a,b)=>a.ratio-b.ratio);
  console.log('samples:',rows.length);
  ['plain','sel','done','mark','note','lab'].forEach(k=>
    console.log(('worst '+k).padEnd(12)+':', JSON.stringify(rows.filter(r=>r.part===k)[0])));
  const bad=rows.filter(r=>r.ratio<4.5);
  console.log('BELOW 4.5:1 →', bad.length? JSON.stringify(bad.slice(0,6)) : 'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
