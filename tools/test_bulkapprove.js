/* v182 — bulk approval, and the release schedule that makes it safe.
   Chris: "I just asked to approve 30 lessons... I just don't want all of
   the lessons to go live too far ahead of the lessons." So approving and
   RELEASING come apart: he reads a whole topic in one sitting, she meets
   it a lesson at a time. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  // Twelve drafts in one subject, so the queue is the real shape.
  const cid = await p.evaluate(() => {
    const cid = STUDY_CLASSES[0].id;
    for (let i = 1; i <= 12; i++) {
      DATA.records['bt'+i] = {id:'bt'+i, type:'unit', status:'draft', classId:cid,
        title:'Bulk Topic · '+i, updatedAt: Date.now()-1000,
        cards:[{id:'c1',term:'T'+i,def:'**D'+i+'**'}],
        questions:[{id:'q1',lv:1,q:'Q'+i+'?',opts:['a','b','c','d'],ans:0,
          hint:'h',steps:['1','2','3'],ex:{main:'**m**',tip:'t'}}]};
    }
    saveLocal(); return cid;
  });

  const q0 = await p.evaluate(() => {
    go('review');
    const s = document.getElementById('screen');
    return {drafts: drafts().length, boxes: s.querySelectorAll('.selbox').length,
            selAll: (s.querySelector('.selbar .btn-ghost')||{}).textContent,
            okDisabled: (s.querySelector('.selbar .btn-primary')||{}).disabled,
            live: units(ctx.classId).length,
            minTap: Math.min(...[...s.querySelectorAll('.selbox')]
              .map(e=>Math.max(e.getBoundingClientRect().width, 24)))};
  });
  ck('the queue shows a checkbox per draft and a select-all',
     q0.drafts === 12 && q0.boxes === 12 && /Select all 12/.test(q0.selAll || ''), q0);
  ck('Approve is disabled until something is ticked', q0.okDisabled === true, q0.okDisabled);

  // Tapping a card still opens the full read — bulk must not cost the door.
  const opened = await p.evaluate(() => {
    const shown = drafts().map(u => u.id);
    document.querySelectorAll('#screen .selrow .cardbtn')[2].click();
    return {view, unitId: ctx.unitId, shown};
  });
  ck('the queue reads in shelf order, 1 → 12, not insertion order',
     opened.shown.join() === [...Array(12)].map((_,i)=>'bt'+(i+1)).join(), opened.shown);
  ck('tapping a card still opens that unit for a full read',
     opened.view === 'reviewunit' && opened.unitId === opened.shown[2], opened);

  // Select all, approve, one a school day.
  const paced = await p.evaluate(async () => {
    go('review');
    document.querySelector('#screen .selbar .btn-ghost').click();
    const okTxt = document.querySelector('#screen .selbar .btn-primary').textContent;
    document.querySelector('#screen .selbar .btn-primary').click();
    await new Promise(r=>setTimeout(r,40));
    const box = document.querySelector('.modal, .sheet, #modal') || document.body;
    const radios = [...box.querySelectorAll('input[type=radio]')];
    const labels = [...box.querySelectorAll('.trustrow')].map(x=>x.textContent);
    radios[1].click();                       // one a school day
    await new Promise(r=>setTimeout(r,20));
    const hint = (box.querySelector('.hintline')||{}).textContent || '';
    const go2 = [...box.querySelectorAll('button')].find(x=>/^Approve$/.test(x.textContent));
    go2.click();
    await new Promise(r=>setTimeout(r,60));
    const us = [...Array(12)].map((_,i)=>DATA.records['bt'+(i+1)]);
    return {okTxt, paces: radios.length, labels, hint,
            statuses: [...new Set(us.map(u=>u.status))],
            rel: us.map(u=>u.releaseOn || null),
            drafts: drafts().length, live: units().filter(u=>/^Bulk Topic/.test(u.title)).length,
            held: scheduled().length};
  });
  ck('select-all offers all twelve and the modal offers three paces',
     /Approve 12/.test(paced.okTxt) && paced.paces === 3, [paced.okTxt, paced.paces]);
  ck('the modal previews when the last one lands',
     /first lands today/.test(paced.hint) && /last on/.test(paced.hint), paced.hint);
  ck('all twelve are approved and out of the queue',
     paced.statuses.join() === 'approved' && paced.drafts === 0, paced);

  // The whole point: approved, but she only has the first one.
  ck('only the first is live — the other eleven are held back',
     paced.live === 1 && paced.held === 11, {live: paced.live, held: paced.held});
  ck('the first releases today and the rest are dated forward, in shelf order',
     paced.rel[0] === (await p.evaluate(()=>AZ.today())) &&
     paced.rel.slice(1).every((d,i)=> d > paced.rel[i]), paced.rel);
  const weekend = await p.evaluate((rel) => rel.filter(d =>
     d && (AZ.weekday(d) === 0 || AZ.weekday(d) === 6 || !!closedToday(d))), paced.rel);
  ck('no release lands on a weekend or a day off', weekend.length === 0, weekend);

  // A held unit is invisible to HER, everywhere that matters.
  const hidden = await p.evaluate((cid) => {
    const h = scheduled()[0];
    const sh = shelvesFor(cid);
    const onShelf = sh.shelves.concat([{units: sh.loose}])
      .some(x => (x.units||[]).some(u => u.id === h.id));
    return {id: h.id, onShelf, inUnits: units(cid).some(u=>u.id===h.id),
            live: liveUnit(h), held: heldBack(h),
            inShuffle: (buildShuffleUnit(cid)||{questions:[]}).questions
                         .some(q => q._srcUnit === h.id)};
  }, cid);
  ck('a held unit is off the shelf, out of units(), and out of a shuffle round',
     !hidden.onShelf && !hidden.inUnits && !hidden.live && hidden.held && !hidden.inShuffle,
     hidden);

  // The grown-up can still find it, and let it through early.
  const sch = await p.evaluate(() => {
    go('scheduled');
    const s = document.getElementById('screen');
    const rows = s.querySelectorAll('.card').length;
    [...s.querySelectorAll('.btn')].find(x=>/Release it now/.test(x.textContent)).click();
    return {rows, held: scheduled().length, live: units().filter(u=>/^Bulk Topic/.test(u.title)).length};
  });
  ck('the Scheduled screen lists them and "Release it now" lets one through',
     sch.rows >= 11 && sch.held === 10 && sch.live === 2, sch);

  const parent = await p.evaluate(() => {
    go('parent');
    const t = document.getElementById('screen').textContent;
    return {says: /\d+ scheduled · next /.test(t)};
  });
  ck('the parent view says how many are scheduled and when the next lands', parent.says, parent);

  // Releasing everything is one tap, and it is a real confirm.
  const relAll = await p.evaluate(async () => {
    go('scheduled');
    [...document.querySelectorAll('#screen .btn')].find(x=>/Release all/.test(x.textContent)).click();
    await new Promise(r=>setTimeout(r,40));
    const box = document.querySelector('.modal, .sheet, #modal') || document.body;
    [...box.querySelectorAll('button')].find(x=>/^Release all$/.test(x.textContent)).click();
    await new Promise(r=>setTimeout(r,40));
    return {held: scheduled().length, live: units().filter(u=>/^Bulk Topic/.test(u.title)).length};
  });
  ck('"Release all now" clears the hold on every one of them',
     relAll.held === 0 && relAll.live === 12, relAll);

  // "All of them today" writes no hold at all.
  const nowPace = await p.evaluate(async () => {
    for (let i = 1; i <= 3; i++) {
      const u = DATA.records['bt'+i];
      put({...u, status:'draft'});
    }
    go('review');
    document.querySelector('#screen .selbar .btn-ghost').click();
    document.querySelector('#screen .selbar .btn-primary').click();
    await new Promise(r=>setTimeout(r,40));
    const box = document.querySelector('.modal, .sheet, #modal') || document.body;
    const hint = (box.querySelector('.hintline')||{}).textContent || '';
    [...box.querySelectorAll('button')].find(x=>/^Approve$/.test(x.textContent)).click();
    await new Promise(r=>setTimeout(r,60));
    return {hint, held: scheduled().length,
            anyRel: [1,2,3].some(i=>DATA.records['bt'+i].releaseOn)};
  });
  ck('the default pace releases everything today, with no hold written',
     /All 3 land today/.test(nowPace.hint) && nowPace.held === 0 && !nowPace.anyRel, nowPace);

  // A single-unit approve always means now, even over an inherited hold.
  const single = await p.evaluate(async () => {
    put({...DATA.records['bt1'], status:'draft', releaseOn: AZ.shift(AZ.today(), 30)});
    go('reviewunit', {unitId:'bt1'});
    [...document.querySelectorAll('#screen .btn')].find(x=>/Approve — send it to her/.test(x.textContent)).click();
    await new Promise(r=>setTimeout(r,40));
    const u = DATA.records['bt1'];
    return {rel: u.releaseOn || null, live: liveUnit(u)};
  });
  ck('"Approve — send it to her" clears any inherited hold',
     single.rel === null && single.live, single);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
