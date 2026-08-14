/* Light paper got deeper — every reading token re-measured against the new
   grounds (page ink, raised, and the wash-tinted worst case), all accents,
   all skies. Transitions killed; knobs asserted. */
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
  await p.waitForTimeout(500);
  await p.addStyleTag({content:'*{transition:none !important;animation:none !important}'});
  const accents=await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies=await p.evaluate(()=>SKIES.filter(s=>s.id!=='seasonal').map(s=>s.id));
  const rows=[];
  for(const sky of skies) for(const acc of accents){
    const g=await p.evaluate(({sky,acc})=>{
      const hex=ACCENTS.find(x=>x.id===acc).c;
      const R=document.documentElement;
      R.style.setProperty('--ac',hex); R.dataset.theme='light'; R.dataset.sky=sky;
      if(getComputedStyle(R).getPropertyValue('--ac').trim()!==hex) throw new Error('accent stuck');
      const d=document.createElement('div'); document.body.appendChild(d);
      const cs=k=>{ d.style.color='rgb(1,2,3)'; d.style.color=`var(${k})`;
        const v=getComputedStyle(d).color; return v; };
      const bg=k=>{ d.style.backgroundColor='rgb(1,2,3)'; d.style.backgroundColor=`var(${k})`;
        return getComputedStyle(d).backgroundColor; };
      const out={ text:cs('--text'), muted:cs('--muted'), faint:cs('--faint'),
        acfg:cs('--ac-fg'), warm:cs('--warm'), good:cs('--good'),
        ink:bg('--ink'), deep:bg('--deep'), raised:bg('--raised'),
        w1:bg('--wash-1') };
      d.remove(); return out;
    },{sky,acc});
    const ink=parse(g.ink), deep=parse(g.deep), raised=parse(g.raised);
    /* worst ground: the wash at full strength composited on the ink */
    const washed=over(parse(g.w1), ink);
    for(const [nm,fg] of [['muted',g.muted],['faint',g.faint],['acfg',g.acfg],['warm',g.warm],['good',g.good],['text',g.text]]){
      const f=parse(fg);
      for(const [gn,gd] of [['ink',ink],['deep',deep],['raised',raised],['washed',washed]]){
        rows.push({sky,acc,tok:nm,ground:gn,r:+ratio(over(f,gd),gd).toFixed(2)});
      }
    }
  }
  const bad=rows.filter(r=>r.r<4.5);
  const worst={}; rows.forEach(r=>{ const k=r.tok+'/'+r.ground; worst[k]=Math.min(worst[k]||99,r.r); });
  console.log('samples:',rows.length);
  Object.entries(worst).sort((a,b)=>a[1]-b[1]).slice(0,8).forEach(([k,v])=>console.log(' ',k,v.toFixed(2)));
  console.log('BELOW 4.5:1 →', bad.length? JSON.stringify([...new Set(bad.map(r=>r.tok+'/'+r.ground+' '+r.r+' ('+r.sky+','+r.acc+')'))].slice(0,10),null,1) : 'none');
  await b.close();
  if(bad.length) process.exit(1);
})();
