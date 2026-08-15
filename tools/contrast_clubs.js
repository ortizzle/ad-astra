/* The two surfaces the club change introduced:
     .evt.club — the row on the day (quiet plate, accent left rule)
     .tocrow .st.want / .st.reg — the marks in the catalog list
   Transitions off BEFORE reading anything: .tool taught me that a colour read
   immediately after a theme flip is the interpolated value, not the resting
   one. And assert the knob actually turned. */
const { chromium } = require('playwright');

const px = c => { const m = c.match(/[\d.]+/g).map(Number); return {r:m[0],g:m[1],b:m[2],a:m.length>3?m[3]:1}; };
const over = (f, b) => ({ r:f.r*f.a+b.r*(1-f.a), g:f.g*f.a+b.g*(1-f.a), b:f.b*f.a+b.b*(1-f.a), a:1 });
const lum = c => { const f = v => { v/=255; return v<=.03928 ? v/12.92 : Math.pow((v+.055)/1.055,2.4); };
  return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b); };
const ratio = (a,b) => { const [x,y]=[lum(a),lum(b)].sort((m,n)=>n-m); return (x+.05)/(y+.05); };

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  await p.goto('http://localhost:8130/index.html',{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  await p.addStyleTag({content:'*,*::before,*::after{transition:none!important;animation:none!important}'});

  const accents = await p.evaluate(()=>ACCENTS.map(a=>a.id));
  const skies   = await p.evaluate(()=>SKIES.map(s=>s.id).filter(s=>s!=='seasonal'));
  const worst = {};
  let samples = 0, sanity = new Set();

  for(const theme of ['dark','light']) for(const ac of accents) for(const sky of skies){
    const r = await p.evaluate(([theme,ac,sky])=>{
      const pr = {...(DATA.records['prefs']||{}), id:'prefs', type:'prefs', theme, accent:ac, sky};
      put(pr); applyTheme();
      setClubState('asl','reg'); setClubState('humane','want');
      const real = AZ.today; AZ.today = () => '2026-08-17';
      go('today');
      const row = document.querySelector('#screen .evt.club');
      const read = (n, surf) => n ? {fg:getComputedStyle(n).color, bg:getComputedStyle(surf).backgroundColor} : null;
      const out = {};
      if(row){
        out.nm = read(row.querySelector('.nm'), row);
        out.dt = read(row.querySelector('.dt'), row);
        out.tm = read(row.querySelector('.tm'), row);
        out.rule = {fg:getComputedStyle(row).borderLeftColor, bg:getComputedStyle(row).backgroundColor};
      }
      go('clubs');
      const marks = [...document.querySelectorAll('#screen .tocrow .st')];
      const reg = marks.find(n=>n.textContent==='✓'), want = marks.find(n=>n.textContent==='★');
      if(reg)  out.reg  = {fg:getComputedStyle(reg).color,  bg:getComputedStyle(reg.parentElement).backgroundColor};
      if(want) out.want = {fg:getComputedStyle(want).color, bg:getComputedStyle(want.parentElement).backgroundColor};
      AZ.today = real;
      out._page = getComputedStyle(document.body).backgroundColor;
      out._theme = document.documentElement.dataset.theme;
      return out;
    },[theme,ac,sky]);

    sanity.add(r._theme + '|' + r._page);
    const page = px(r._page);
    for(const k of ['nm','dt','tm','rule','reg','want']){
      if(!r[k]) { console.log('MISSING', k, theme, ac, sky); continue; }
      const bg = over(px(r[k].bg), page);          // rows are transparent over the page
      const v = ratio(over(px(r[k].fg), bg), bg);
      samples++;
      if(!worst[k] || v < worst[k].v) worst[k] = {v, theme, ac, sky};
    }
  }

  /* Did the knob actually turn? Two themes must give two different page colours. */
  const themes = new Set([...sanity].map(s=>s.split('|')[0]));
  const pages  = new Set([...sanity].map(s=>s.split('|')[1]));
  console.log('themes seen:', [...themes].join(','), '| distinct page colours:', pages.size);
  if(themes.size !== 2 || pages.size < 2){ console.log('PROBE BROKEN — theme did not track'); process.exit(1); }

  console.log('samples:', samples);
  let bad = 0;
  for(const [k,w] of Object.entries(worst)){
    /* The left rule is a 3px mark, not text: 3:1 is the non-text bar. */
    const bar = k === 'rule' ? 3 : 4.5;
    const ok = w.v >= bar;
    if(!ok) bad++;
    console.log(`${ok?'  ok ':'FAIL '}${k.padEnd(5)} worst ${w.v.toFixed(2)}:1 (bar ${bar}) — ${w.theme}/${w.ac}/${w.sky}`);
  }
  console.log(bad ? 'FAILURES' : 'ALL PASS');
  await b.close();
  if(bad) process.exit(1);
})();
