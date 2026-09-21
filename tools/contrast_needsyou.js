/* The "Needs you" card's three reading tokens, every accent × sky × theme.
   The card is `.card.ac` — an ACCENT-WASHED surface — so these are the tint
   trap .felt and the Growth Zone chip both hit: --muted and --warm are
   measured against the page and the plain card elsewhere, never against this
   one. Same parse/composite helpers as contrast_gzchip.js; Chrome reports
   the wash as color(srgb … / 0.08), which a naive probe reads as opaque. */
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
  const p=await b.newPage({viewport:{width:390,height:1400}});
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'networkidle'});
  await p.addStyleTag({content:'*,*::before,*::after{transition:none !important;animation:none !important}'});
  await p.evaluate(()=>{
    const cid = STUDY_CLASSES[0].id;
    put({id:'u-ny', type:'unit', classId:cid, status:'draft', title:'A draft',
      cards:[{id:'c1',term:'x',def:'**y**'}], questions:[], updatedAt:Date.now()});
    put({id:'a-ny', type:'assess', classId:cid, kind:'quiz', title:'A quiz', date:'2000-01-01', score:null});
    setSandbox(true); saveLocal(); go('parent');
  });
  const accents=await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies=await p.evaluate(()=>SKIES.filter(s=>s.id!=='seasonal').map(s=>s.id));
  const rows=[];
  for(const theme of ['light','dark']) for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({theme,sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c, R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme=theme; R.dataset.sky=sky;
      if(getComputedStyle(R).getPropertyValue('--ac').trim()!==hex) throw new Error('accent stuck');
      const card=[...document.querySelectorAll('#screen .card')].find(x=>/Needs you/i.test(x.innerText));
      const all=[...card.querySelectorAll('.nyrow')];
      const plain=all.find(r=>!r.classList.contains('warn'));
      const warn =all.find(r=>r.classList.contains('warn'));
      if(!plain||!warn) throw new Error('rows missing');
      const cs=n=>getComputedStyle(n);
      return { page:cs(document.body).backgroundColor, card:cs(card).backgroundColor,
        label:cs(plain.querySelector('.nyl')).color,
        sub:cs(plain.querySelector('small')).color,
        warn:cs(warn.querySelector('.nyl')).color,
        chev:cs(plain.querySelector('.nyv')).color,
        eyebrow:cs(card.querySelector('.eyebrow')).color };
    },{theme,sky,acc});
    const surf=over(parse(g.card), parse(g.page));   // the accent wash over the page
    ['label','sub','warn','chev','eyebrow'].forEach(k=>
      rows.push({theme,sky,acc,what:k,ratio:+ratio(over(parse(g[k]),surf),surf).toFixed(2)}));
  }
  rows.sort((a,b)=>a.ratio-b.ratio);
  console.log('samples:',rows.length);
  [...new Set(rows.map(r=>r.what))].forEach(w=>
    console.log('worst %-9s %s', w, JSON.stringify(rows.find(r=>r.what===w))));
  const bad=rows.filter(r=>r.ratio<4.5);
  console.log('BELOW 4.5:1 →', bad.length? JSON.stringify(bad.slice(0,6)) : 'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
