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

  /* ---- ASL: Mondays, 3:45–4:30, bi-weekly, first Aug 17 ---- */
  const asl = await p.evaluate(()=>{
    const c = CLUBS.find(x=>x.id==='asl');
    return { first: clubFirstDate(c), days: clubWeekdays(c),
      mon17: clubMeetsOn(c,'2026-08-17'),   // first meeting
      mon24: clubMeetsOn(c,'2026-08-24'),   // off week (bi-weekly)
      mon31: clubMeetsOn(c,'2026-08-31'),   // on week
      tue18: clubMeetsOn(c,'2026-08-18'),   // wrong weekday
      aug10: clubMeetsOn(c,'2026-08-10') }; // before the first meeting
  });
  ck('ASL anchors to its first meeting', asl.first==='2026-08-17' && asl.days.join()==='1', asl);
  ck('bi-weekly lands on alternate Mondays only',
     asl.mon17 && !asl.mon24 && asl.mon31 && !asl.tue18 && !asl.aug10, asl);

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
    const real=AZ.today; AZ.today=()=>'2026-08-17'; AZ.nowMinutes=()=>9*60;
    setClubState('asl','reg');
    go('today');
    const reg = [...document.querySelectorAll('#screen .evt.club')].map(n=>n.textContent.replace(/\s+/g,' ').trim());
    setClubState('asl','want');
    go('today');
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
