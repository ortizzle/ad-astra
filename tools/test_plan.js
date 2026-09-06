/* The plan of attack (v151 / Wayfinder v132): Study opens on the companion's
   line — the thread itself — and the affirmation card and the thread hero are
   gone. Roughly one day in three with nothing pressing, the line is the
   affirmation instead; never over a due review. */
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
    const sc = document.getElementById('screen');
    const read = () => { go('study'); const k = [...sc.children];
      return { first: k[0] && k[0].className, perch: T(sc.querySelector('.perch')), tap: !!sc.querySelector('.perch.tap'),
        aff: !!sc.querySelector('.perch.aff'), lede: !!sc.querySelector('.lede'), acts: !!sc.querySelector('.affirm-acts'),
        divs: [...sc.querySelectorAll('.divider')].map(T), pet: T(sc.querySelector('.perch .pet')) }; };
    const o = {};
    /* a day with reviews due (the seed has misses): the line is the thread */
    const real = AZ.today; AZ.today = () => '2026-09-09';
    setPref('companion', {sp: COMPANIONS[0].id, nm:'Pip'});
    o.dueN = dueMisses().length;
    o.due = read();
    /* the line names the subject leading the queue, not a bare total */
    const bySubj = {}; dueMisses().forEach(m=>(bySubj[m.classId]=bySubj[m.classId]||[]).push(m));
    const topCid = Object.keys(bySubj).sort((a,b)=>bySubj[b].length-bySubj[a].length)[0];
    o.topCl = CLASS_BY_ID[topCid].name; o.topN = bySubj[topCid].length;
    const bubble = sc.querySelector('.perch .bubble');
    o.bubbleStyle = { fontStyle: getComputedStyle(bubble).fontStyle, fontSize: parseFloat(getComputedStyle(bubble).fontSize) };
    sc.querySelector('.perch').click(); o.dueLands = view; o.dueLandsCid = gzFilter.cid;
    /* find a swap day and a non-swap day with nothing due */
    all('miss').forEach(m => softDelete(m.id));
    const days = []; for(let i=0;i<9;i++) days.push(AZ.shift('2026-09-14', i));
    const swapDay = days.find(d => mixHash('plan:'+d) % 3 === 0), plainDay = days.find(d => mixHash('plan:'+d) % 3 !== 0);
    AZ.today = () => swapDay; o.swap = read(); o.swapAff = affirmationFor(swapDay);
    AZ.today = () => plainDay; o.plain = read(); o.plainTh = (threadTarget(plainDay)||{}).kind;
    if(o.plain.tap){ sc.querySelector('.perch').click(); o.plainLands = view; }
    /* no companion chosen: the perch still carries the plan, with the star */
    setPref('companion', null);
    o.none = read();
    AZ.today = real;
    return o;
  });
  ck('the affirmation card is gone', !r.due.lede && !r.due.acts, r.due);
  ck('"Pick up the thread" is gone', !r.due.divs.includes('Pick up the thread'), r.due.divs);
  ck('Study opens on the perch', r.due.first === 'perch plan tap' || /^perch/.test(r.due.first), r.due.first);
  ck('with reviews due, the line is the thread and taps to the Growth Zone', r.dueN > 0 && /question/.test(r.due.perch) && r.due.tap && !r.due.aff && r.dueLands==='growth', r);
  ck('the due line names the subject leading the queue, and the tap lands filtered to it', r.due.perch.includes(r.topCl) && r.due.perch.includes(String(r.topN)) && r.dueLandsCid, r);
  ck('the plan-line bubble is upright and 18px+, not the italic default', r.bubbleStyle.fontStyle==='normal' && r.bubbleStyle.fontSize>=18, r.bubbleStyle);
  ck('a swap day with nothing due says the affirmation', r.swap.aff && r.swap.perch.includes(r.swapAff) && !r.swap.tap, r.swap);
  ck('a plain day says the plan (lesson or subject) and is a door', !r.plain.aff && r.plain.tap && ['lesson','plan','ramp'].includes(r.plainTh) && /checkin|unit|quiz/.test(r.plainLands||''), {plain:r.plain, th:r.plainTh, lands:r.plainLands});
  ck('no companion: the star carries the plan', r.none.perch && r.none.pet === '✦' && /Plan of attack/i.test(r.none.perch), r.none);

  out.forEach(x=>console.log((x.ok?'  ok ':'FAIL ')+x.n+(x.ok?'':' → '+JSON.stringify(x.got))));
  console.log(' due line:', r.due.perch); console.log(' swap line:', r.swap.perch); console.log(' plain line:', r.plain.perch);
  console.log(TAG, out.every(x=>x.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(x=>x.ok)||errs.length) process.exit(1);
})();
