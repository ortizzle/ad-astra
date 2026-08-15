/* Ad Astra's algeo hours are Tuesdays 3:45-4:45 pm — afternoon ONLY. A test
   on a Tuesday therefore has no usable window that day at all. */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  await p.goto('http://localhost:8130/index.html',{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const r = await p.evaluate(()=>{
    AZ.today = ()=>'2026-08-17'; AZ.nowMinutes = ()=>9*60;
    return {
      // algeo test on Tuesday, algeo hours Tuesday PM only -> no window in time
      algeoSameDay: nextHoursBefore('algeo','2026-08-17','2026-08-18'),
      // algeo test Wednesday -> Tuesday afternoon works
      algeoWed:     nextHoursBefore('algeo','2026-08-17','2026-08-19'),
      // english also holds a Tuesday afternoon, which is legitimately EARLIER
      // than a Wednesday test — so that is the honest next window, not the
      // Wednesday morning one. (My first assertion here got this backwards.)
      engFromMon:   nextHoursBefore('english','2026-08-17','2026-08-19'),
      // isolate the same-day path: ask from Wednesday itself, test Wednesday.
      // English's Wednesday slot is 7:45-8:15 AM, so the clock has to be
      // BEFORE it or the slot is correctly reported as gone.
      engSameDay:   (AZ.nowMinutes = ()=>6*60,
                     nextHoursBefore('english','2026-08-19','2026-08-19'))
    };
  });
  console.log(JSON.stringify(r,null,1));
  const ok = r.algeoSameDay===null
    && r.algeoWed && /pm/i.test(r.algeoWed.times)
    && r.engFromMon && r.engFromMon.date === '2026-08-18'
    && r.engSameDay && r.engSameDay.sameDay === true
    && /am/i.test(r.engSameDay.times) && !/pm/i.test(r.engSameDay.times);
  console.log(ok?'ALL PASS':'FAILURES');
  await b.close();
  if(!ok) process.exit(1);
})();
