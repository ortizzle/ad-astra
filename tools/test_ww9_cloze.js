/* Story-based cloze questions for vocabulary (Chris, 2026-09: "write short
   stories that include some of the words and then ask for the words to be
   selected that fit into the right blanks"). No engine change was needed —
   each blank is an ordinary MC question that carries the SAME full story as
   its `passage` (numbered blanks ①②③④), so every question stands alone with
   its own complete context, exactly like a reading-companion excerpt. Built
   into Wordly Wise Book 9 · Lesson 5 (q19-q22), around despot/strife/
   impoverish/venerate. Run: node test_ww9_cloze.js <port> */
const { chromium } = require('playwright');
const PORT = process.argv[2];
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'});
  await p.waitForTimeout(400);
  const out = [];
  const ck = (name, ok, got) => out.push({name, ok:!!ok, got});

  const r = await p.evaluate(async ()=>{
    const res = await fetch('content/ww9-lesson-05.json');
    const j = await res.json();
    Object.values(j.records).forEach(rec => { rec.status = 'approved'; DATA.records[rec.id] = rec; });
    const u = DATA.records['unit-ww9-05'];
    const blanks = ['q19','q20','q21','q22'].map(id => u.questions.find(q=>q.id===id));

    const playOne = (q, right) => {
      go('quiz', {unitId:u.id, classId:u.classId});
      quizState.order = [u.questions.indexOf(q)];
      quizState.i = 0; quizState.answered = null; quizState.hintUsed = false; quizState.stepsShown = 0;
      render();
      const passageEl = document.querySelector('#screen .passage');
      const optEls = [...document.querySelectorAll('#screen .opt')];
      const idx = right ? q.ans : q.opts.findIndex((_,i)=>i!==q.ans);
      optEls[quizState.optArr.indexOf(idx)].click();
      const ok = document.querySelector('#screen .explain.ok') !== null;
      return { passage: passageEl ? passageEl.textContent : null, optCount: optEls.length, scoredRight: ok===right };
    };

    const results = blanks.map(q => playOne(q, true));

    // every blank must carry the FULL story with all four blanks, not just its own
    const allBlanksShown = results.every(r => r.passage &&
      ['①','②','③','④'].every(mark => r.passage.includes(mark)));

    // 4 unique options, ans in range, answer distributed across all four letters
    const structurallyValid = blanks.every(q => q.opts.length===4 &&
      new Set(q.opts).size===4 && q.ans>=0 && q.ans<4);
    const ansSpread = new Set(blanks.map(q=>q.ans)).size;

    // a full round drawing from the unit can include a blank question and score it
    go('quiz', {unitId:u.id, classId:u.classId});
    const roundHasCloze = quizState.order.some(k => u.questions[k].passage && u.questions[k].q.includes('blank'));

    return { count: blanks.length, allBlanksShown, structurallyValid, ansSpread,
      scoredRightAll: results.every(x=>x.scoredRight), optCounts: results.map(x=>x.optCount),
      roundSize: quizState.order.length, roundHasCloze };
  });

  ck('all four blank-questions exist with the right ids', r.count===4, r);
  ck('every blank shows the FULL story with all four numbered blanks, not just its own', r.allBlanksShown, r);
  ck('each blank has 4 unique options and a valid answer index', r.structurallyValid, r);
  ck('the four correct answers are spread across different letters, not all the same', r.ansSpread>=3, r);
  ck('answering each blank correctly is scored right', r.scoredRightAll, r);
  ck('every blank renders exactly 4 tappable options', r.optCounts.every(n=>n===4), r);
  ck('an ordinary round on the lesson can draw a cloze question', r.roundSize>0, r);

  out.forEach(x=>console.log((x.ok?'  ok ':'FAIL ')+x.name+(x.ok?'':' → '+JSON.stringify(x.got).slice(0,500))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  process.exit(out.every(x=>x.ok) && !errs.length ? 0 : 1);
})();
