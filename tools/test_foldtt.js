/* The timetable moved from Today to Study (v150): the day's line-up IS the
   subject list. Today carries no period rows; Study lists every subject in
   the day's order with the live one painted, and on a day off still lists
   them (the weekday order) with nothing painted NOW. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8130;
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const read = async (date, mins) => p.evaluate(([d,m])=>{
    const real=AZ.today; AZ.today=()=>d; AZ.nowMinutes=()=>m;
    go('today');
    const sc=document.getElementById('screen');
    const today={ periods: sc.querySelectorAll('.period').length, px: sc.scrollHeight,
      divs:[...sc.querySelectorAll('.divider')].map(x=>x.textContent.trim()) };
    go('study');
    const rows=[...sc.querySelectorAll('.period.tap')];
    const study={ periods: rows.length, now: sc.querySelectorAll('.period.now').length,
      divs:[...sc.querySelectorAll('.divider')].map(x=>x.textContent.trim()),
      times: rows.map(r=>(r.querySelector('.tm')||{}).textContent||'NOW'),
      subjects: rows.map(r=>r.querySelector('.nm').textContent),
      tiles: sc.querySelectorAll('.tile').length };
    AZ.today=real; return {today, study};
  }, [date, mins]);

  const wed = await read('2026-08-19', 9*60);   // a school day, mid-morning
  ck('Today carries no period rows', wed.today.periods===0, wed.today);
  ck('Today has no schedule section', !wed.today.divs.some(d=>/schedule|school day/i.test(d)), wed.today.divs);
  ck('Study lists every study subject as a row', wed.study.periods >= STUDY_MIN(), wed.study);
  ck('Study paints exactly one row NOW on a school day', wed.study.now===1, wed.study);
  ck("Study's divider says it is today's order", wed.study.divs.some(d=>/today's order/.test(d)), wed.study.divs);
  ck('the old tile grid is gone', wed.study.tiles===0, wed.study.tiles);
  const inOrder = wed.study.times.filter(t=>/[AP]M/.test(t)).every((t,i,a)=>i===0 || toMin(a[i-1]) <= toMin(t));
  ck('rows run in clock order', inOrder, wed.study.times);

  const sat = await read('2026-08-15', 9*60);   // Saturday
  ck('a day off still lists the subjects', sat.study.periods === wed.study.periods, sat.study);
  ck('nothing is painted NOW on a day off', sat.study.now===0, sat.study);
  ck("a day off says which order it shows", sat.study.divs.some(d=>/order/.test(d)) && !sat.study.divs.some(d=>/today's order/.test(d)), sat.study.divs);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log(` school day: ${wed.study.periods} rows on Study, Today ${wed.today.px}px`);
  console.log(' subjects:', wed.study.subjects.join(' · '));
  console.log(out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
  function STUDY_MIN(){ return 6; }
  function toMin(t){ const m=t.match(/(\d+):(\d+)\s*([AP]M)/); if(!m) return 0;
    return (Number(m[1])%12 + (m[3]==='PM'?12:0))*60 + Number(m[2]); }
})();
