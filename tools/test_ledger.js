/* The week ledger's study rows in LIGHT mode (Wayfinder v158 / Ad Astra v178).
   Found in a full-app screenshot review: a study row carried the class `subj`
   to wear its subject colour (v108 / v125) — but `.subj` is the painted-tile
   treatment, whose ::after lays a dark bottom scrim and whose base rule sets
   color:#fff. On the light card the subject name rendered white on near-white:
   invisible. Dark mode masked it completely, which is why it lived for fifty
   versions. The modifier is `ofsubj` now; this test measures the light-mode
   row rather than reading the stylesheet. Same file in both repos. */
const { chromium } = require('playwright');
const [PORT] = process.argv.slice(2);
const lum = c => { const m = c.match(/[\d.]+/g).map(Number); const f = v => { v/=255; return v<=.03928 ? v/12.92 : Math.pow((v+.055)/1.055,2.4); }; return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2]); };
const ratio = (a,b) => { const [x,y]=[lum(a),lum(b)].sort((p,q)=>q-p); return (x+.05)/(y+.05); };
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}, colorScheme:'light', reducedMotion:'reduce'});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});
  const r = await p.evaluate(async ()=>{
    put({...(DATA.records.prefs||{id:'prefs',type:'prefs'}), theme:'light'}); applyTheme();
    go('today'); await new Promise(r=>setTimeout(r,400));
    const rows=[...document.querySelectorAll('.ledger-row')].filter(x=>x.classList.contains('ofsubj'));
    const plain = rows.find(x=>!x.classList.contains('now')) || rows[0];
    if(!plain) return null;
    const card = plain.closest('.card');
    const after = getComputedStyle(plain,'::after');
    const what = plain.querySelector('.ledger-what'), day = plain.querySelector('.ledger-day');
    return { theme: document.documentElement.dataset.theme, rows: rows.length, cls: plain.className,
      leaked: plain.classList.contains('subj'),
      afterContent: after.content, afterBg: after.backgroundImage,
      rowColor: getComputedStyle(plain).color, whatColor: getComputedStyle(what).color,
      dayColor: getComputedStyle(day).color, textTok: getComputedStyle(document.body).color,
      cardBg: getComputedStyle(card).backgroundColor };
  });
  ck('the seeded week renders study rows wearing their subject (ofsubj), none of them still tagged subj',
     r && r.rows>0 && !r.leaked && /ofsubj/.test(r.cls), r);
  ck('in light mode the row carries no painted-tile scrim (::after is empty)',
     r && (r.afterContent==='none' || r.afterContent==='') && (r.afterBg==='none'), r && {afterContent:r.afterContent, afterBg:r.afterBg});
  ck('the subject name reads in the text token, not white',
     r && r.whatColor!=='rgb(255, 255, 255)' && r.whatColor===r.textTok, r && {whatColor:r.whatColor, textTok:r.textTok});
  const bg = r && /^rgba?\(/.test(r.cardBg) && !/, 0\)$/.test(r.cardBg) ? r.cardBg : 'rgb(255, 255, 255)';
  ck('the subject name measures 4.5:1+ against the card',
     r && ratio(r.whatColor, bg) >= 4.5, r && {ratio: ratio(r.whatColor, bg).toFixed(2), bg});
  ck('the day label wears the deepened subject colour and clears 4.5:1',
     r && r.dayColor!==r.whatColor && ratio(r.dayColor, bg) >= 4.5, r && {dayColor:r.dayColor, ratio: ratio(r.dayColor, bg).toFixed(2)});
  let bad=0; out.forEach(x=>{ if(!x.ok){ bad++; console.log('FAIL', x.n, '→', JSON.stringify(x.got)); } else console.log('  ok', x.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS'); console.log('errors:', errs.length?errs:'none');
  await b.close(); process.exit(bad?1:0);
})();
