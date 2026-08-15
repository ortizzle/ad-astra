/* The weekday timetable folds on a day off, opens on one tap, and is never
   folded on a school day. Events stay visible either way. */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto('http://localhost:8130/index.html',{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const read = async (date) => p.evaluate((d)=>{
    const real=AZ.today; AZ.today=()=>d; AZ.nowMinutes=()=>9*60;
    go('today');
    const sc=document.getElementById('screen');
    const r={ periods: sc.querySelectorAll('.period').length,
              px: sc.scrollHeight,
              btn: !![...sc.querySelectorAll('button')].find(x=>/Show the weekday timetable/.test(x.textContent)) };
    AZ.today=real; return r;
  }, date);

  const sat = await read('2026-08-15');   // Saturday
  ck('day off folds the timetable', sat.periods===0 && sat.btn, sat);

  const opened = await p.evaluate(()=>{
    const real=AZ.today; AZ.today=()=>'2026-08-15'; AZ.nowMinutes=()=>9*60;
    go('today');
    [...document.querySelectorAll('#screen button')].find(x=>/Show the weekday timetable/.test(x.textContent)).click();
    const sc=document.getElementById('screen');
    const r={ periods: sc.querySelectorAll('.period').length, px: sc.scrollHeight };
    AZ.today=real; return r;
  });
  ck('one tap opens it in full', opened.periods>=10, opened);

  const wed = await read('2026-08-19');   // a school day
  ck('school day is never folded', wed.periods>=10 && !wed.btn, wed);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(` weekend: ${sat.px}px folded → ${opened.px}px open  (saved ${opened.px-sat.px}px)`);
  console.log(` school day: ${wed.periods} periods, ${wed.px}px`);
  console.log(out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
