/* Registered vs starred, and registered clubs joining the day they meet.
   The cadence rules are the point: a club only lands on a day when the day,
   the time and the frequency are all genuinely derivable. */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto('http://localhost:8130/index.html',{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  /* ---- three states, and the old `true` still means "want" ---- */
  const st = await p.evaluate(()=>{
    put({id:'clubpicks', type:'clubpicks', picks:{asl:true}});   // legacy value
    const before = clubState('asl');
    setClubState('asl','reg');
    const after = clubState('asl');
    setClubState('asl',null);
    const gone = clubState('asl');
    setClubState('asl','reg');
    return { before, after, gone, now: clubState('asl') };
  });
  ck('a legacy `true` still reads as "want"', st.before==='want', st);
  ck('registered is its own state', st.after==='reg' && st.now==='reg', st);
  ck('and can be cleared', st.gone===null, st);

  /* ---- ASL: Mondays, 3:45–4:30, an EXPLICIT real schedule from the teacher
     (2026-08) — supersedes the inferred bi-weekly cadence, because the real
     dates already account for holidays a pure every-14-days rule can't. */
  const asl = await p.evaluate(()=>{
    const c = CLUBS.find(x=>x.id==='asl');
    const allReal = c.dates.every(d => clubMeetsOn(c, d));
    return { days: clubWeekdays(c), count: c.dates.length, allReal,
      allMondays: c.dates.every(d => AZ.weekday(d) === 1),
      sept14: clubMeetsOn(c,'2026-09-14'),     // a real meeting
      nov9to16: AZ.daysBetween('2026-11-09','2026-11-16'),   // the 7-day gap around Veterans Day
      dec7toJan11: AZ.daysBetween('2026-12-07','2027-01-11'), // the winter-break gap
      presidentsDay: clubMeetsOn(c,'2027-02-15'),   // explicitly "NO MEETING" — also a school holiday
      oldCadenceDate: clubMeetsOn(c,'2026-08-31'),  // the old bi-weekly math would have placed this; the real list doesn't
      beforeFirstReal: clubMeetsOn(c,'2026-08-17'),
      presidentsDayClosed: closedToday('2027-02-15') };
  });
  ck('all 14 real meeting dates are honoured', asl.allReal && asl.count===14, asl);
  ck('every real date is actually a Monday', asl.allMondays, asl);
  ck('a real meeting date lands on the day', asl.sept14, asl);
  ck('the schedule is genuinely irregular (not pure bi-weekly)',
     asl.nov9to16===7 && asl.dec7toJan11===35, asl);
  ck('Presidents Day (explicitly "NO MEETING") is not placed', !asl.presidentsDay, asl);
  ck('a date only the OLD cadence math would have placed is not placed', !asl.oldCadenceDate, asl);
  ck('dates before the real list starts are not placed', !asl.beforeFirstReal, asl);
  ck('CAL actually closes school for Presidents Day, confirming the "no meeting" note',
     asl.presidentsDayClosed !== null, asl.presidentsDayClosed);

  /* ---- clubs that must NOT be placed ---- */
  const skipped = await p.evaluate(()=>{
    const bad = CLUBS.filter(c=>{
      const placeable = c.time && /^(weekly|bi-weekly)/i.test(c.freq||'') && clubFirstDate(c);
      if(placeable) return false;
      /* none of these may ever return true for any day of a whole year */
      for(let i=0;i<365;i++) if(clubMeetsOn(c, AZ.shift('2026-08-03', i))) return true;
      return false;
    });
    const monthly = CLUBS.filter(c=>/monthly/i.test(c.freq||'')).length;
    const noTime  = CLUBS.filter(c=>!c.time).length;
    return { wronglyPlaced: bad.map(c=>c.id), monthly, noTime };
  });
  ck('vague cadence is never placed on a day', skipped.wronglyPlaced.length===0, skipped);

  /* ---- it shows on the day, and only when registered ---- */
  const day = await p.evaluate(()=>{
    const real=AZ.today; AZ.today=()=>'2026-09-14'; AZ.nowMinutes=()=>9*60;
    setClubState('asl','reg');
    /* v150: the timetable — and a registered club with it — lives on Study. */
    go('study');
                                     // The period list (and club rows with it) is folded by default since v106.
    const reg = [...document.querySelectorAll('#screen .evt.club')].map(n=>n.textContent.replace(/\s+/g,' ').trim());
    setClubState('asl','want');
    go('study');
    const want = document.querySelectorAll('#screen .evt.club').length;
    setClubState('asl','reg');
    AZ.today=real;
    return { reg, wantRows: want };
  });
  ck('a registered club joins the day it meets', day.reg.length===1 && /ASL/.test(day.reg[0]), day);
  ck('a merely starred club does not', day.wantRows===0, day);

  /* ---- the clubs screen separates the two ---- */
  const screen = await p.evaluate(()=>{
    setClubState('asl','reg'); setClubState('humane','want');
    go('clubs');
    const t=document.getElementById('screen').textContent;
    const marks=[...document.querySelectorAll('#screen .tocrow .st')].map(n=>n.textContent);
    return { signedUp:/You are signed up for/.test(t), hoping:/hoping to join/.test(t),
             tick: marks.filter(m=>m==='✓').length, star: marks.filter(m=>m==='★').length };
  });
  ck('the screen separates signed-up from starred', screen.signedUp && screen.hoping, screen);
  ck('rows carry three distinct marks', screen.tick===1 && screen.star>=1, screen);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(' ASL on the day:', day.reg[0]);
  console.log(' clubs with no time:', skipped.noTime, '| monthly:', skipped.monthly, '— all correctly unplaced');
  console.log(out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
