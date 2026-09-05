/* The number line — kind:'slider'. She drags a marker to where a number
   belongs; right means within line.tol of line.ans. Mirrors kind:'spell'
   everywhere else: one option carrying the answer as text, a -4 sentinel for
   off the mark, never served in a timed round, misses re-asked live.
   Same file in both apps: it seeds its own unit so it does not depend on
   which app's content carries sliders. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(() => {
    const cid = STUDY_CLASSES[0].id;
    const mk = (id, text, line) => ({id, lv:1, kind:'slider', q:text, opts:[String(line.ans)], ans:0, hint:'h',
      steps:['a','b','c'], ex:{main:'**'+line.ans+'.** why', tip:'t'}, line});
    const u = { id:'unit-nl-test', type:'unit', classId:cid, title:'Number line test', status:'approved', round:3, cards:[],
      questions:[ mk('q0','Place 0.35 on the line.', {lo:0,hi:1,ans:0.35,tol:0.025,step:0.01,ticks:0.1,labels:[0,0.5,1]}),
                  mk('q1','Place 2.6 on the line.',  {lo:2,hi:3,ans:2.6,tol:0.03,step:0.01,ticks:0.1,labels:[2,2.5,3]}),
                  mk('q2','Estimate 50 m.',           {lo:0,hi:100,ans:50,tol:6,step:1,ticks:10,labels:[0,50,100],unit:' m'}) ],
      updatedAt: Date.now()-1000 };
    DATA.records[u.id] = u; saveLocal();
    return {cid, timedRound: pickRound(u, true).length, untimedRound: pickRound(u, false).length};
  });
  ck('a timed round never serves a slider; an untimed one serves all three', seed.timedRound===0 && seed.untimedRound===3, seed);

  const first = await p.evaluate((cid) => {
    quizState = null; go('quiz',{unitId:'unit-nl-test', classId:cid});
    const sc = document.getElementById('screen');
    const inp = sc.querySelector('.nline input[type=range]');
    const q = unitFor('unit-nl-test').questions[quizState.order[quizState.i]];
    return {qid:q.id, hasLine: !!inp, min: inp && inp.min, max: inp && inp.max, step: inp && inp.step,
            read: (sc.querySelector('.nread')||{}).textContent, placeDisabled: (document.getElementById('nplace')||{}).disabled,
            ticks: sc.querySelectorAll('.nline .tk').length, labels: [...sc.querySelectorAll('.nline .lb')].map(x=>x.textContent),
            noOpts: sc.querySelectorAll('.opt').length === 0};
  }, seed.cid);
  ck('a slider question renders a range control with the line\'s bounds and step, ticks and labels, and no option buttons',
     first.hasLine && first.noOpts && first.ticks >= 10 && first.labels.length === 3 && first.placeDisabled === true, first);

  // Drag (set the value and fire input), miss on purpose, place.
  const miss = await p.evaluate((cid) => {
    const q = unitFor('unit-nl-test').questions[quizState.order[quizState.i]];
    const L = q.line, wrong = L.ans + L.tol*3 <= L.hi ? L.ans + L.tol*3 : L.ans - L.tol*3;
    const inp = document.querySelector('.nline input[type=range]');
    inp.value = String(wrong); inp.dispatchEvent(new Event('input', {bubbles:true}));
    const readAfterDrag = document.querySelector('.nread').firstChild.nodeValue;
    const enabled = !document.getElementById('nplace').disabled;
    // a hint re-render must not move the marker
    const before = quizState.sliderVal; render();
    const kept = quizState.sliderVal === before && +document.querySelector('.nline input[type=range]').value === before;
    document.getElementById('nplace').click();
    const sc = document.getElementById('screen');
    const m = all('miss').find(x => x.unitId==='unit-nl-test' && x.qid===q.id);
    return {readAfterDrag, enabled, kept, answered: quizState.answered, correct: quizState.correct,
            markers: sc.querySelectorAll('.nline .mk').length, verdict: (sc.querySelector('.nverdict')||{}).textContent,
            miss: m && {right: m.right, chose: m.chose, kind: m.kind}, item: (quizState.items||[]).slice(-1)[0], wrong, ans: L.ans};
  }, seed.cid);
  ck('dragging updates the readout and enables Place it; a re-render keeps the marker where she left it',
     /\d/.test(miss.readAfterDrag) && miss.enabled && miss.kept, miss);
  ck('placing off the mark answers with the -4 sentinel, shows both markers, and records her value against the answer',
     miss.answered===-4 && miss.correct===0 && miss.markers===2 && /it belongs at/.test(miss.verdict||'')
     && miss.miss && miss.miss.kind==='slider' && miss.miss.right===String(miss.ans) && Number(miss.miss.chose.replace(/[^\d.]/g,''))===miss.wrong
     && miss.item && miss.item.c===0 && miss.item.ca===String(miss.ans), miss);

  // Next question: land within tolerance.
  const hit = await p.evaluate(() => {
    const next = document.querySelector('#screen .btn-primary'); next.click();
    const q = unitFor('unit-nl-test').questions[quizState.order[quizState.i]];
    const L = q.line;
    const inp = document.querySelector('.nline input[type=range]');
    inp.value = String(+(L.ans + L.tol*0.5).toFixed(3)); inp.dispatchEvent(new Event('input', {bubbles:true}));
    document.getElementById('nplace').click();
    const sc = document.getElementById('screen');
    return {answered: quizState.answered, correct: quizState.correct, verdict: (sc.querySelector('.nverdict')||{}).textContent,
            missed: !!all('miss').find(x => x.unitId==='unit-nl-test' && x.qid===q.id)};
  });
  ck('placing within tolerance counts as right and writes no miss', hit.answered===0 && hit.correct===1 && /within reach/.test(hit.verdict||'') && !hit.missed, hit);

  // The miss is re-asked live from the Growth Zone as a slider, not as four options.
  const gz = await p.evaluate(() => {
    all('miss').filter(m => m.unitId==='unit-nl-test').forEach(m => put({...m, due: AZ.today()}));
    const r = buildReviewUnit({unitId:'unit-nl-test', all:true});
    const q = r && r.questions[0];
    quizState = null; go('quiz',{unitId:'__review__', classId:'__all__'});
    return {kind: q && q.kind, hasLine: !!q && !!q.line, renders: !!document.querySelector('#screen .nline input[type=range]')};
  });
  ck('a missed slider comes back in the Growth Zone as a slider with its line intact', gz.kind==='slider' && gz.hasLine && gz.renders, gz);

  await p.evaluate(() => { quizState = null; softDelete('unit-nl-test'); all('miss').filter(m=>m.unitId==='unit-nl-test').forEach(m=>softDelete(m.id)); });
  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,360))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
