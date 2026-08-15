/* The real week of 8/17: four quizzes Tue-Fri against hours on Mon/Tue/Thu. */
const { chromium } = require('playwright');
const PORT = process.argv[2];
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const r = await p.evaluate(()=>{
    AZ.today = ()=>'2026-08-17';        // Monday
    AZ.nowMinutes = ()=>9*60;           // 9am, both of Monday's slots relevant
    const out = {};
    // History quiz Tue 8/18; History hours are Tuesdays -> SAME DAY
    out.histTue = nextHoursBefore('history','2026-08-17','2026-08-18');
    // Vocab quiz Wed 8/19; English hours Mondays -> Monday is the last.
    // At 9am the 7:00-7:30 slot is already gone, so the honest answer is the
    // afternoon one -- my first assertion here expected 'am' and was wrong.
    out.engWed  = nextHoursBefore('english','2026-08-17','2026-08-19');
    // Science quiz Thu 8/20; Science hours Thursdays -> SAME DAY
    out.sciThu  = nextHoursBefore('science','2026-08-17','2026-08-20');
    // Math test Fri 8/21; Math hours Thursdays -> Thursday, the day before
    out.mathFri = nextHoursBefore('math','2026-08-17','2026-08-21');
    // before school on Monday: BOTH of the day's slots are still ahead
    AZ.nowMinutes = ()=>6*60;
    out.engWedEarly = nextHoursBefore('english','2026-08-17','2026-08-19');
    // and the already-passed case: it is now 4pm on Monday
    AZ.nowMinutes = ()=>16*60;
    out.engWedLate = nextHoursBefore('english','2026-08-17','2026-08-19');
    return out;
  });
  console.log(JSON.stringify(r,null,1));
  const ok =
    r.histTue && !/pm/i.test(r.histTue.times) && r.histTue.sameDay === true &&
    r.sciThu  && !/pm/i.test(r.sciThu.times)  && r.sciThu.sameDay === true &&
    r.engWed  && r.engWed.times === '3:30–4:00 pm' && r.engWed.inDays === 0 &&
    r.engWedEarly && /am/i.test(r.engWedEarly.times) && /pm/i.test(r.engWedEarly.times) &&
    r.mathFri && r.mathFri.inDays === 3 && /pm/i.test(r.mathFri.times) &&
    r.engWedLate === null;
  console.log(ok ? 'ALL PASS' : 'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!ok) process.exit(1);
})();
