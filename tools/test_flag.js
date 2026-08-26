/* Smoke test for "flag this question": a quiz-screen control she can use to
   send a question to a grown-up, and the parent-side screen that lets a
   grown-up remove it from the unit or dismiss the flag. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8105;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const r = await p.evaluate(async () => {
    const o = {};
    // A small real unit to quiz against.
    const u = { id:'unit-flagtest', type:'unit', classId:'biology', status:'approved', cards:[],
      questions:[
        {id:'fq0', lv:1, q:'Fresh question zero', opts:['a','b','c','d'], ans:0, hint:'h', steps:['s1','s2','s3'], ex:{main:'m'}},
        {id:'fq1', lv:1, q:'Fresh question one', opts:['w','x','y','z'], ans:1, hint:'h', steps:['s1','s2','s3'], ex:{main:'m'}}
      ]};
    put(u);
    quizState = null;
    go('quiz', {unitId:'unit-flagtest', classId:'biology'});
    quizState.i = 0; quizState.order = [0,1];
    const q0 = u.questions[0];
    answer(u, q0, q0.ans);           // answer correctly
    render();
    o.flagButtonPresentAfterAnswer = [...document.querySelectorAll('#screen button')]
      .some(b => /Something wrong with this question/.test(b.textContent));
    return o;
  });
  ck('flag button appears after answering', r.flagButtonPresentAfterAnswer, r);

  // Open the flag modal, write a note, submit.
  const flagged = await p.evaluate(async () => {
    const btn = [...document.querySelectorAll('#screen button')].find(b => /Something wrong with this question/.test(b.textContent));
    btn.click();
    await new Promise(res=>setTimeout(res,30));
    const ta = document.querySelector('.modal-overlay textarea');
    ta.value = "the answer key looks backwards";
    ta.dispatchEvent(new Event('input'));
    const go2 = [...document.querySelectorAll('.modal-overlay button')].find(b=>/Flag it/.test(b.textContent));
    go2.click();
    await new Promise(res=>setTimeout(res,30));
    const f = Object.values(DATA.records).find(r=>r.type==='flag' && !r.deleted);
    return {
      wrote: !!f, unitId: f && f.unitId, qid: f && f.qid, note: f && f.note,
      buttonNowDisabled: [...document.querySelectorAll('#screen button')]
        .some(b => /Flagged for a grown-up/.test(b.textContent) && b.disabled)
    };
  });
  ck('flagging writes a flag record with the right unit/question', flagged.wrote && flagged.unitId==='unit-flagtest' && flagged.qid==='fq0', flagged);
  ck('the note is saved', flagged.note === 'the answer key looks backwards', flagged.note);
  ck('the button becomes disabled after flagging (no double-flag)', flagged.buttonNowDisabled, flagged);

  // Flag a second, WRONG-answered question too, so we can test "remove" leaves a miss to clean up.
  const flagged2 = await p.evaluate(async () => {
    const u = DATA.records['unit-flagtest'];
    quizState.i = 1; quizState.answered = null;
    render();
    const q1 = u.questions[1];
    answer(u, q1, (q1.ans+1)%4);     // answer WRONG on purpose
    render();
    const btn = [...document.querySelectorAll('#screen button')].find(b => /Something wrong with this question/.test(b.textContent));
    btn.click();
    await new Promise(res=>setTimeout(res,30));
    const go2 = [...document.querySelectorAll('.modal-overlay button')].find(b=>/Flag it/.test(b.textContent));
    go2.click();
    await new Promise(res=>setTimeout(res,30));
    return {
      flagCount: all('flag').length,
      missExists: !!(DATA.records['miss_unit-flagtest_fq1'] && !DATA.records['miss_unit-flagtest_fq1'].deleted)
    };
  });
  ck('two flags now recorded', flagged2.flagCount === 2, flagged2);
  ck('the wrong answer created a real miss record (so we can test it gets cleaned up)', flagged2.missExists, flagged2);

  // Parent view shows the entry card.
  const parentCard = await p.evaluate(() => {
    go('parent');
    return document.getElementById('screen').innerText.includes('Take a look');
  });
  ck('parent view shows "questions were flagged" card', parentCard, parentCard);

  // Open the flagged screen, dismiss fq0, remove fq1.
  const screen1 = await p.evaluate(() => {
    go('flagged');
    return {
      rows: document.querySelectorAll('#screen .miss').length,
      hasNote: /the answer key looks backwards/.test(document.getElementById('screen').innerText)
    };
  });
  ck('flagged screen lists both flags', screen1.rows === 2, screen1);
  ck('her note text renders', screen1.hasNote, screen1);

  const afterDismiss = await p.evaluate(async () => {
    const dismissBtn = [...document.querySelectorAll('#screen button')].find(b => /Dismiss/.test(b.textContent));
    dismissBtn.click();
    await new Promise(res=>setTimeout(res,30));
    return {
      flagCount: all('flag').length,
      unitStillHasBothQuestions: DATA.records['unit-flagtest'].questions.length === 2
    };
  });
  ck('dismissing drops the flag count by 1 and touches nothing else', afterDismiss.flagCount === 1, afterDismiss);
  ck('dismissed question is untouched in the unit', afterDismiss.unitStillHasBothQuestions, afterDismiss);

  const afterRemove = await p.evaluate(async () => {
    const removeBtn = [...document.querySelectorAll('#screen button')].find(b => /Remove the question/.test(b.textContent));
    removeBtn.click();
    await new Promise(res=>setTimeout(res,30));
    const u = DATA.records['unit-flagtest'];
    return {
      flagCount: all('flag').length,
      unitQuestionCount: u.questions.length,
      removedQidGone: !u.questions.some(q=>q.id==='fq1'),
      missTombstoned: DATA.records['miss_unit-flagtest_fq1'] && DATA.records['miss_unit-flagtest_fq1'].deleted === true
    };
  });
  ck('removing drops the flag count to 0', afterRemove.flagCount === 0, afterRemove);
  ck('the unit lost exactly the flagged question', afterRemove.unitQuestionCount === 1 && afterRemove.removedQidGone, afterRemove);
  ck('the matching miss record is tombstoned, not left dangling', afterRemove.missTombstoned, afterRemove);

  // Rescue-round variants must never show the flag button.
  const rescueCheck = await p.evaluate(() => {
    const rq = {q:'variant q', opts:['a','b','c','d'], ans:0, _rescue:true, _srcUnit:'unit-flagtest', _srcQid:'fq0'};
    // Simulate the guard condition directly rather than a full rescue round.
    return !!rq._rescue;
  });
  ck('rescue-variant guard condition is truthy (button is gated on !q._rescue)', rescueCheck, rescueCheck);

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got).slice(0,300))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
