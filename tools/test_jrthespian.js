/* The Junior Thespians' real meeting list (sponsor's email, 2026-09).
   The point of this test is that the PRINTED DATES win over the cadence the
   same email describes: "every other Tuesday" is not what the twelve dates do,
   and the two it names as not meeting are absent rather than encoded as rules. */
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto('http://localhost:'+(process.argv[2]||'8130')+'/index.html',{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const c = await p.evaluate(()=>{
    const c = CLUBS.find(x=>x.id==='jrthespian');
    return { time:c.time, dates:c.dates, day:c.day,
      allTuesdays: c.dates.every(d=>AZ.weekday(d)===2),
      allPlaced:   c.dates.every(d=>clubMeetsOn(c,d)),
      onClosed:    c.dates.filter(d=>!!closedToday(d)),
      /* the two the email names as NOT meeting */
      oct6:  clubMeetsOn(c,'2026-10-06'),  feb23: clubMeetsOn(c,'2027-02-23'),
      oct6Closed: closedToday('2026-10-06'),
      /* a pure bi-weekly from the first meeting would have put these two on
         her afternoon; the real list says otherwise */
      oct13: clubMeetsOn(c,'2026-10-13'), oct27: clubMeetsOn(c,'2026-10-27'),
      beforeFirst: clubMeetsOn(c,'2026-09-15'),
      gaps: c.dates.slice(1).map((d,i)=>AZ.daysBetween(c.dates[i],d)) };
  });
  ck('all twelve dates are honoured', c.allPlaced && c.dates.length===12, c.dates);
  ck('every one of them is a Tuesday', c.allTuesdays, c.dates);
  ck('none lands on a day school is closed', c.onClosed.length===0, c.onClosed);
  ck('it meets 3:50–4:30', c.time==='3:50–4:30', c.time);
  ck('Oct 6 ("Fall Break") is not placed', !c.oct6, c);
  ck('and CAL independently closes school that week, confirming the note',
     c.oct6Closed !== null, c.oct6Closed);
  ck('Feb 23 ("Tech Week") is not placed', !c.feb23, c);
  ck('the schedule is genuinely NOT every-other-Tuesday',
     c.gaps.some(g=>g!==14) && c.gaps.includes(35), c.gaps);
  ck('dates only the bi-weekly math would place are not placed', !c.oct13 && !c.oct27, c);
  ck('nothing is placed before the first meeting', !c.beforeFirst, c);

  /* ---- it reaches her day, and only once she is registered ---- */
  const day = await p.evaluate(()=>{
    const real=AZ.today; AZ.today=()=>'2026-09-29'; AZ.nowMinutes=()=>9*60;
    setClubState('jrthespian','reg'); go('study');
    const reg=[...document.querySelectorAll('#screen .evt.club')]
      .map(n=>n.textContent.replace(/\s+/g,' ').trim());
    setClubState('jrthespian','want'); go('study');
    const want=document.querySelectorAll('#screen .evt.club').length;
    setClubState('jrthespian','reg');
    /* a Tuesday in the same term that is NOT on the list */
    AZ.today=()=>'2026-10-13'; go('study');
    const off=document.querySelectorAll('#screen .evt.club').length;
    AZ.today=real;
    return { reg, wantRows:want, offRows:off };
  });
  ck('a registered meeting joins her line-up',
     day.reg.length===1 && /Thespian/.test(day.reg[0]), day);
  ck('and carries its own time', /3:50/.test(day.reg[0]||''), day.reg);
  ck('merely starring it puts nothing on a day', day.wantRows===0, day);
  ck('an off-week Tuesday stays empty', day.offRows===0, day);

  /* ---- the clubs screen counts it as placed (it reads `dates`, not cadence) ---- */
  const scr = await p.evaluate(()=>{
    setClubState('jrthespian','reg');
    go('clubs');
    const t=document.getElementById('screen').textContent.replace(/\s+/g,' ');
    return { all:/These show up on your schedule/.test(t), partial:/of these show up/.test(t) };
  });
  ck('the signed-up card does not call it unplaced', scr.all && !scr.partial, scr);

  /* ---- this repo is public: no person is named in the club data.
     Checked by SHAPE, never by listing the real name — an assertion that
     spells out the name it forbids has published it. */
  const priv = await p.evaluate(()=>{
    const blob=JSON.stringify(CLUBS.find(x=>x.id==='jrthespian'));
    const hits=[];
    if(/@/.test(blob)) hits.push('an email address');
    if(/\b(mr|mrs|ms|miss|dr|coach|teacher|sponsor)\b\.?/i.test(blob)) hits.push('an honorific or role word');
    /* two capitalised words in a row that are not a known proper noun of the
       club itself — the shape a person's name would take */
    const ok=/^(International|Junior|Thespian|Society|Membership|ParentSquare|The|Meetings|Late|Bird|Tuesday|Sept|Fall|Break|Upper|School)$/;
    const pairs=(blob.match(/\b[A-Z][a-z]+ [A-Z][a-z]+\b/g)||[])
      .filter(x=>!x.split(' ').every(w=>ok.test(w)));
    if(pairs.length) hits.push('a name-shaped pair: '+pairs.join(', '));
    return hits;
  });
  ck('no person is named or contactable in the shipped club', priv.length===0, priv);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(' gaps between meetings (days):', c.gaps.join(', '));
  console.log(' the row on her day:', day.reg[0]);
  console.log(out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
