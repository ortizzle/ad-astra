/* A Junior Jeopardy board survives leaving it (Wayfinder v157 / Ad Astra v177).
   Chris, 2026-09: River lost a game to a stray Back. Two bugs, and the first
   is the one that actually cost her the board — the doors called buildLadder()
   unconditionally, minting a fresh board over a game the screen itself would
   have resumed. The second is the reload/app-kill case ladderState was always
   open to, now covered by a device-local save shaped exactly like the parked
   round (ROUND_KEY). Same file in both repos. */
const { chromium } = require('playwright');
const [PORT] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  // ---- one 12-question lesson, enough for a 3×3 board
  const cid = await p.evaluate(()=>{
    const cid = STUDY_CLASSES.find(c => units(c.id).length).id;
    const mk = (i, lv) => ({ id:'q'+i, lv, from:'source', q:'RS Q'+i+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i],
      ans:i%4, hint:'h'+i, steps:['s1','s2','s3'], ex:{main:'because '+i} });
    put({ id:'rs-unit', type:'unit', classId:cid, status:'approved', title:'Resume Lesson',
      cards:[], questions:[...Array(12).keys()].map(i=>mk(i,(i%3)+1)) });
    Store.remove('ladder'); ladderState = null; ladderUnit = null;
    return cid;
  });

  /* Tap the lesson's own Junior Jeopardy door, the way she does — never
     go('ladder') directly, since the door is where the bug lived. */
  const tapDoor = () => p.evaluate(([cid])=>{
    go('unit', {classId:cid});
    const btn = [...document.querySelectorAll('#screen button')].find(x=>/Junior Jeopardy — play for points/.test(x.textContent));
    if(!btn) return {found:false};
    const line = btn.querySelector('small');
    btn.click();
    return { found:true, door: line && line.textContent, view,
      qids: ladderUnit ? ladderUnit.questions.map(q=>q._srcQid) : null,
      results: ladderState ? ladderState.results.slice() : null };
  }, [cid]);

  /* One tile, answered right or wrong, back to the board. */
  const playTile = (right) => p.evaluate(([right])=>{
    const s = ladderState, u = ladderUnit;
    const k = s.results.findIndex(x=>x===null);
    s.current = k;
    go('quiz', {unitId:'__ladder__', classId:s.classId, ladder:true}, {back:true});
    if(s.wagerAsk){} // no-op: Round 1's Daily Double is a plain modal, handled below
    const overlay = document.querySelector('.modal-overlay');
    if(overlay) overlay.querySelector('.btn-primary').click();
    const qq = u.questions[quizState.order[quizState.i]];
    const pick = right ? qq.ans : (qq.ans+1)%4;
    document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(pick)].click();
    document.getElementById('qnext').click();
    return { k, view };
  }, [right]);

  // ---- deal a board and play two screens
  const first = await tapDoor();
  ck('the door opens a fresh board when nothing is in progress', first.found && first.view==='ladder' && first.results.every(x=>x===null), first);
  await playTile(false); await playTile(true);   // a mixed board, and a running score that is not zero
  const mid = await p.evaluate(()=>({ played: ladderState.results.filter(x=>x!==null).length,
    qids: ladderUnit.questions.map(q=>q._srcQid), results: ladderState.results.slice(),
    pts: ladderPoints(), saved: !!Store.get('ladder') }));
  ck('two screens played, and the board is written to the device-local save', mid.played===2 && mid.saved, mid);

  // ---- the accident: leave by a nav tab, then tap the door again
  await p.evaluate(()=>{ go('today'); });
  const again = await tapDoor();
  ck('the door says the board is still in progress, not what the last one scored',
     /Still playing · 2 of 9 screens/.test(again.door||''), again.door);
  ck('tapping it RESUMES the same board — same questions, same two results — instead of re-dealing',
     again.view==='ladder' && again.qids.join()===mid.qids.join() && again.results.join()===mid.results.join(), {door:again.qids, was:mid.qids});
  const ptsBack = await p.evaluate(()=>ladderPoints());
  ck('her running score comes back with it, not reset to zero', ptsBack===mid.pts && mid.pts>0, {ptsBack, was:mid.pts});

  // ---- the harder case: a reload, an app-kill, a long background
  const reload = await p.evaluate(()=>{ ladderState = null; ladderUnit = null; return !!Store.get('ladder'); });
  ck('the save outlives the in-memory board', reload, reload);
  const after = await tapDoor();
  ck('after a reload the door still says the board is in progress', /Still playing · 2 of 9 screens/.test(after.door||''), after.door);
  ck('and tapping it rebuilds the identical board from the save, results intact',
     after.view==='ladder' && after.qids.join()===mid.qids.join() && after.results.join()===mid.results.join(), {got:after.results, was:mid.results});

  // ---- finishing clears it: a done board has nothing to come back to
  const fin = await p.evaluate(async ()=>{
    const s = ladderState, u = ladderUnit;
    while(s.results.some(x=>x===null)){
      const k = s.results.findIndex(x=>x===null);
      s.current = k;
      go('quiz', {unitId:'__ladder__', classId:s.classId, ladder:true}, {back:true});
      const ov = document.querySelector('.modal-overlay');
      if(ov) ov.querySelector('.btn-primary').click();
      const qq = u.questions[quizState.order[quizState.i]];
      document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(qq.ans)].click();
      document.getElementById('qnext').click();
    }
    return { saved: !!Store.get('ladder'), done: ladderState.results.every(x=>x!==null) };
  });
  ck('finishing the board clears the save — its log is written and the next tap should deal fresh',
     fin.done && !fin.saved, fin);
  const doneDoor = await p.evaluate(([cid])=>{
    go('unit', {classId:cid});
    const btn = [...document.querySelectorAll('#screen button')].find(x=>/Junior Jeopardy — play for points/.test(x.textContent));
    return btn.querySelector('small').textContent;
  }, [cid]);
  ck('the door goes back to reporting the last finished board', /Last played/.test(doneDoor), doneDoor);

  // ---- a stale save is discarded rather than resumed
  const stale = await p.evaluate(([cid])=>{
    ladderState = null; ladderUnit = null;
    go('unit',{classId:cid});
    const btn = [...document.querySelectorAll('#screen button')].find(x=>/Junior Jeopardy — play for points/.test(x.textContent));
    btn.click();                                   // deal a board
    const qids = ladderUnit.questions.map(q=>q._srcQid);
    ladderState.results[0] = 'right'; saveLadder();
    const sv = Store.get('ladder');
    Store.set('ladder', {...sv, date: AZ.shift(AZ.today(), -1)});   // yesterday's board
    ladderState = null; ladderUnit = null;
    const u = DATA.records['rs-unit'];
    const yesterday = loadLadder(u);
    const clearedAfterStale = !Store.get('ladder');
    // and a board whose lesson has since been re-drafted
    ladderState = null; ladderUnit = null;
    btn.click(); ladderState.results[0] = 'right'; saveLadder();
    put({ ...u, status:'draft' });
    ladderState = null; ladderUnit = null;
    const drafted = loadLadder(DATA.records['rs-unit']);
    put({ ...DATA.records['rs-unit'], status:'approved' });
    return { yesterday, clearedAfterStale, drafted, clearedAfterDraft: !Store.get('ladder'), qids };
  }, [cid]);
  ck('yesterday\'s board is not today\'s game — it is discarded, and the slot cleared',
     !stale.yesterday && stale.clearedAfterStale, stale);
  ck('a board whose lesson was re-drafted underneath it is discarded too, never silently asked',
     !stale.drafted && stale.clearedAfterDraft, stale);

  let bad = 0;
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got)); } else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
