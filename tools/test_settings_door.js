/* The Grown-ups door on Settings (v157 / Wayfinder v138): Chris and Kat open
   it often, mainly to check sandbox mode, so it moved from a quiet dashed
   card to a hero cardButton with sandbox's live state read straight off it
   as an eyebrow — a glance answers "is sandbox on" with no tap, and the
   warn colour flags an accidentally-left-on sandbox. The actual toggle
   stays behind the passcode; this line is read-only. Same file, both apps. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const r = await p.evaluate(()=>{
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    go('setup');
    const sc = document.getElementById('screen');
    const firstCard = [...sc.children].find(c => c.className && c.className.includes('cardbtn'));
    const before = { isFirst: firstCard === sc.querySelector('.cardbtn'),
      isHero: firstCard.classList.contains('hero'),
      eyebrow: T(firstCard.querySelector('.cb-eye')), warnClass: firstCard.querySelector('.cb-eye').className,
      minH: firstCard.getBoundingClientRect().height };
    setSandbox(true);
    go('setup');
    const c2 = document.querySelector('.cardbtn.hero');
    const on = { eyebrow: T(c2.querySelector('.cb-eye')), warnClass: c2.querySelector('.cb-eye').className,
      color: getComputedStyle(c2.querySelector('.cb-eye')).color };
    setSandbox(false);
    return { before, on };
  });
  ck('the door is the FIRST thing on Settings, styled as a hero, 44px+', r.before.isFirst && r.before.isHero && r.before.minH>=44, r.before);
  ck('with sandbox off, the eyebrow says so and carries no warning colour', /Sandbox is off/.test(r.before.eyebrow) && !/warn/.test(r.before.warnClass), r.before);
  ck('with sandbox on, the eyebrow flips and wears the warm warning colour', /Sandbox is on/.test(r.on.eyebrow) && /warn/.test(r.on.warnClass), r.on);

  out.forEach(x=>console.log((x.ok?'  ok ':'FAIL ')+x.n+(x.ok?'':' → '+JSON.stringify(x.got))));
  console.log(TAG, out.every(x=>x.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(x=>x.ok)||errs.length) process.exit(1);
})();
