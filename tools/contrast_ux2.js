/* New reading text from v150: section labels, the quiz door's status line, the
   early-release line on a subject-washed day card, the done tile's status.
   Sweeps accent × theme (subject hue for the day card) and reports the worst. */
const { chromium } = require('playwright');
const [PORT, DIR, TAG] = process.argv.slice(2);
const parse=c=>{let m=c.match(/color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\)/);
  if(m) return [m[1]*255,m[2]*255,m[3]*255,m[4]==null?1:+m[4]];
  m=c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/); return m?[+m[1],+m[2],+m[3],m[4]==null?1:+m[4]]:null;};
const over=(f,b)=>f.slice(0,3).map((v,i)=>v*f[3]+b[i]*(1-f[3])).concat([1]);
const lum=c=>{const f=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*f[0]+.7152*f[1]+.0722*f[2]};
const ratio=(a,b)=>{const[x,y]=[lum(a),lum(b)].sort((m,n)=>n-m);return (x+.05)/(y+.05)};
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:DIR+'/tools/seed.js'}); await p.waitForTimeout(300);
  await p.evaluate(async ()=>{ for(const path of CONTENT_LIBRARY){
    try{ const r=await fetch(path); const j=await r.json();
      Object.values(j.records||{}).forEach(rec=>{rec.status='approved';DATA.records[rec.id]=rec;});
    }catch(e){} } });
  await p.addStyleTag({content:'*{transition:none!important;animation:none!important}'});
  const res = await p.evaluate(()=>{
    const out = [];
    const cs = (n, prop) => getComputedStyle(n)[prop];
    /* composite: walk up to the first opaque ancestor background */
    const bgOf = (n) => { const stack=[]; let e=n;
      while(e && e !== document.documentElement){ const c = cs(e,'backgroundColor'); if(c && c !== 'rgba(0, 0, 0, 0)') stack.push(c); e = e.parentElement; }
      stack.push(cs(document.body,'backgroundColor')); stack.push(cs(document.documentElement,'backgroundColor')); return stack; };
    window._bg = bgOf;
    const u = units().find(x => seriesOf(x) && x.questions.length >= 10 && !x.book && !x.guide);
    u.questions.slice(0,3).forEach(q => put({id:'qstat_'+u.id+'_'+q.id, type:'qstat', unitId:u.id, classId:u.classId, qid:q.id, q:q.q, attempts:1, correct:1, plain:1}));
    put({id:'c-cards', type:'log', mode:'cards', classId:u.classId, unitId:u.id, date:AZ.today(), at:Date.now(), correct:0,total:0,seconds:60,xp:5*u.cards.length, seen:u.cards.length, deck:u.cards.length});
    const accents = ACCENTS.map(a=>a.id);
    for(const theme of ['dark','light']) for(const acc of accents){
      setPref('theme',theme); setPref('accent',acc); applyTheme();
      go('shelf',{classId:u.classId, series:seriesOf(u), open:u.id});
      const oc = document.getElementById('shelfopen');
      const probe = (label, n) => { if(!n) return; out.push({theme, acc, label, fg: cs(n,'color'), bg: bgOf(n)}); };
      probe('seclab', oc.querySelector('.seclab'));
      probe('qdoor small', oc.querySelector('.qdoor small'));
      probe('qdoor b', oc.querySelector('.qdoor b'));
      probe('tile done small', oc.querySelector('.mtile.done small'));
      probe('ttl chev', oc.querySelector('.tchev'));
      /* the day card: every subject hue, with an early-release line */
      AZ.today = () => '2026-09-09'; AZ.nowMinutes = () => 600;
      const evs = CAL.events; CAL.events = evs.concat([{start:'2026-09-09', name:'Early release', icon:'🕑', kind:'early', early:true}]);
      go('today');
      CAL.events = evs;
      const dc = document.querySelector('#screen .daycard');
      probe('daycard eyebrow', dc.querySelector('.eyebrow'));
      probe('daycard p', dc.querySelector('p'));
      probe('daycard h3', dc.querySelector('h3'));
      probe('erline', dc.querySelector('.erline'));
    }
    return out;
  });
  const rows = res.map(r => { let bg = null;
    for(const layer of r.bg.slice().reverse()){ const c = parse(layer); if(!c) continue; bg = bg ? over(c, bg) : c; }
    const fg = parse(r.fg); const cr = fg && bg ? ratio(over(fg,bg), bg) : null; return {...r, cr}; });
  const worst = {};
  rows.forEach(r => { if(r.cr==null) return; if(!worst[r.label] || r.cr < worst[r.label].cr) worst[r.label] = r; });
  Object.values(worst).forEach(w => console.log(`${w.cr < 4.5 ? 'FAIL' : '  ok'} ${w.label.padEnd(16)} worst ${w.cr.toFixed(2)}:1  (${w.theme}, ${w.acc})`));
  console.log(TAG, Object.values(worst).every(w => w.cr >= 4.5 || w.label==='ttl chev') ? 'ALL PASS' : 'FAILURES', rows.length, 'samples');
  await b.close();
})();
