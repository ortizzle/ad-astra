/* Junior Jeopardy (Wayfinder v149 / Ad Astra v167) — the Trivia Ladder
   rebuilt as a game show at Chris's request: categories × values on a
   board of blue screens, harder questions on higher values, a Daily
   Double, a wrong answer that costs the tile, sounds, and a Double round
   (bigger values, harder tiers, one category from an older lesson) once a
   board has been finished. Answering still runs through the real quiz
   screen and answer() via a synthetic __ladder__ unit carrying _srcUnit —
   same qstat/miss/XP crediting as any untimed round. Same file in both
   repos. */
const { chromium } = require('playwright');
const [PORT, TAG] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  // ---- seed: a 12-question lesson with an even spread of levels, an older
  //      lesson on the same shelf she has already worked, and a too-thin unit
  const seeded = await p.evaluate(()=>{
    const cid = STUDY_CLASSES.find(c => units(c.id).length).id;
    const mk = (i, lv) => ({ id:'q'+i, lv, from:'source', q:'JJ Q'+i+' (lv'+lv+')?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4,
      hint:'h'+i, steps:['s1','s2','s3'], ex:{main:'because '+i} });
    put({ id:'jj-unit', type:'unit', classId:cid, status:'approved', title:'Topic 9 · 9-2 Test Lesson',
      cards:[], questions:[...Array(12).keys()].map(i=>mk(i,(i%3)+1)) });
    put({ id:'jj-older', type:'unit', classId:cid, status:'approved', title:'Topic 9 · 9-1 Older Lesson',
      cards:[], questions:[...Array(9).keys()].map(i=>mk(i,(i%3)+1)) });
    DATA.records['jj-older'].questions.forEach(q=>put({id:'qstat_jj-older_'+q.id,type:'qstat',unitId:'jj-older',qid:q.id,attempts:2,correct:2,plain:2}));
    put({ id:'jj-thin', type:'unit', classId:cid, status:'approved', title:'Too Thin For A Board',
      cards:[], questions:[0,1,2,3].map(i=>mk(i,1)) });
    return { cid };
  });
  const cid = seeded.cid;

  // ---- the door: renamed, gated on 6+ eligible questions
  const doors = await p.evaluate(([cid])=>{
    const full = unitCard(DATA.records['jj-unit'], CLASS_BY_ID[cid]).textContent;
    const thin = unitCard(DATA.records['jj-thin'], CLASS_BY_ID[cid]).textContent;
    return { full: /Junior Jeopardy — play for points/.test(full), thin: /Junior Jeopardy/.test(thin), old: /Trivia Ladder/.test(full) };
  }, [cid]);
  ck('the lesson door says Junior Jeopardy (never Trivia Ladder) and renders on a 12-question unit', doors.full && !doors.old, doors);
  ck('the door is absent on a 4-question unit', !doors.thin, doors);

  // ---- Round 1: 3 categories × 3 values, 100/200/300 down each column,
  //      harder questions on higher values, a Daily Double below the top row
  const r1 = await p.evaluate(([cid])=>{
    ladderState = null;
    go('ladder',{unitId:'jj-unit', classId:cid});
    const cats=[...document.querySelectorAll('.jj-cat')].map(x=>x.textContent);
    const tiles=[...document.querySelectorAll('.jj-tile')];
    const lv = k => ladderUnit.questions[k].lv;
    const rows = ladderState.rows;
    let monotone = true;
    for(let c=0;c<ladderState.cats.length;c++) for(let r=1;r<rows;r++) if(lv(c*rows+r) < lv(c*rows+r-1)) monotone = false;
    return { cats, tiles: tiles.map(t=>t.textContent), enabled: tiles.every(t=>!t.disabled),
      minH: Math.min(...tiles.map(t=>t.getBoundingClientRect().height)),
      values: ladderState.values.join(','), monotone, ddRow: ladderState.dd % rows, mode: ladderState.mode,
      round: document.querySelector('.jj-round').textContent, srcs: [...new Set(ladderUnit.questions.map(q=>q._srcUnit))],
      tileBg: getComputedStyle(tiles[0]).color };
  }, [cid]);
  ck('Round 1 deals 3 categories × 3 screens, 100/200/300 down each column, all open, 44px+',
     r1.cats.length===3 && r1.tiles.length===9 && r1.values==='100,200,300,100,200,300,100,200,300' && r1.enabled && r1.minH>=44 && r1.mode==='single' && r1.round==='Round 1', r1);
  ck('categories are named (the lesson, split I/II/III) and every question is the lesson\'s own', r1.cats.every(c=>/9-2 Test Lesson (I|II|III)/.test(c)) && r1.srcs.join()==='jj-unit', r1);
  ck('questions get harder down each column (level never drops as the value rises)', r1.monotone, r1);
  ck('one Daily Double, never in the top row', r1.ddRow > 0, r1);
  ck('the screens are gold-on-blue, not the subject accent', r1.tileBg==='rgb(255, 204, 51)', r1);

  // ---- opening the Daily Double reveals it first, then hands the real quiz
  //      screen the question with the category as its eyebrow and double stakes
  const dd = await p.evaluate(()=>{
    const k = ladderState.dd, s = ladderState;
    const tile = [...document.querySelectorAll('.jj-tile')].find(t=>t.getAttribute('aria-label')===`${s.cats[s.catOf[k]].nm} for ${s.values[k]}`);
    tile.click();
    const modal = document.querySelector('.modal-overlay');
    const modalTxt = modal ? modal.textContent : '';
    modal.querySelector('.btn-primary').click();
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    return { modalTxt, view, ladder: quizState.ladder, unitId: quizState.unitId,
      eyebrow: T(document.querySelector('#screen .eyebrow')), worth: T(document.querySelector('#screen .ladderworth')), expect: s.values[k]*2 };
  });
  ck('the Daily Double announces itself, then opens the real quiz screen at double stakes with the category as eyebrow',
     /Daily Double!/.test(dd.modalTxt) && dd.view==='quiz' && dd.ladder && dd.unitId==='__ladder__' && /📺 9-2 Test Lesson/.test(dd.eyebrow) && dd.worth==='★ Daily Double · '+dd.expect, dd);

  // ---- scoring: wrong costs the tile (double on the DD), right pays it, and
  //      the score floors at zero as she goes — a miss at zero costs nothing
  const sc = await p.evaluate(()=>{
    const u = ladderUnit, s = ladderState, out=[];
    const play = (k, right)=>{
      s.current=k; go('quiz',{unitId:'__ladder__',classId:s.classId,ladder:true},{back:true});
      const qq = u.questions[quizState.order[quizState.i]];
      const idx = right ? qq.ans : qq.opts.findIndex((_,i)=>i!==qq.ans);
      document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(idx)].click();
      const nextLabel = document.getElementById('qnext').textContent;
      document.getElementById('qnext').click();
      out.push({k, right, pts: ladderPoints(), view, nextLabel});
    };
    play(s.dd, false);
    const k300 = s.values.findIndex((v,k)=>v===300 && k!==s.dd && !s.results[k]);
    play(k300, true);
    const k100 = s.values.findIndex((v,k)=>v===100 && !s.results[k]);
    play(k100, false);
    const ddTile = [...document.querySelectorAll('.jj-tile')].find(t=>/\bdd\b/.test(t.className));
    return { out, strip: document.querySelector('.jj-strip .ladderworth').textContent,
      ddTile: ddTile && ddTile.className, ddText: ddTile && ddTile.textContent, ddWorth: s.values[s.dd]*2,
      missOnRealUnit: Object.keys(DATA.records).some(id=>id.startsWith('miss_jj-unit_')),
      qstatPlain: DATA.records['qstat_jj-unit_'+u.questions[s.dd]._srcQid]?.plain };
  });
  ck('a wrong Daily Double at zero costs nothing (floor), a right 300 pays 300, a wrong 100 leaves 200',
     sc.out.map(o=>o.pts).join()==='0,300,200' && sc.strip==='200 pts' && sc.out.every(o=>o.view==='ladder' && o.nextLabel==='Back to the board →'), sc);
  ck('the played Daily Double screen goes dark showing ✕ and double its value, with its star; the miss and qstat land on the REAL lesson',
     /done wrong/.test(sc.ddTile) && sc.ddText==='✕ '+sc.ddWorth && sc.missOnRealUnit && sc.qstatPlain===1, sc);

  // ---- sounds: synthesized, and silent under the quiet opt-down
  const snd = await p.evaluate(()=>{
    const before = prefs().fx;
    try{ sfx('right'); sfx('wrong'); sfx('dd'); }catch(e){ return {threw:String(e)}; }
    const made = !!sfxCtx;
    sfxCtx = null;
    put({ ...(DATA.records['prefs']||{}), id:'prefs', type:'prefs', fx:'quiet' });
    sfx('right');
    const quietMade = !!sfxCtx;
    put({ ...(DATA.records['prefs']||{}), id:'prefs', type:'prefs', fx:before||'fireworks' });
    return { made, quietMade };
  });
  ck('the show sounds play through WebAudio without throwing, and stay silent when celebrations are set to quiet', snd.made && !snd.quietMade, snd);

  // ---- finishing: log carries done/points/round, the door remembers, Stars summarizes
  const fin = await p.evaluate(([cid])=>{
    const u = ladderUnit, s = ladderState;
    for(let k=0;k<s.order.length;k++){ if(s.results[k]) continue;
      s.current=k; go('quiz',{unitId:'__ladder__',classId:s.classId,ladder:true},{back:true});
      const qq = u.questions[quizState.order[quizState.i]];
      document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(qq.ans)].click();
      document.getElementById('qnext').click(); }
    const logs2 = Object.values(DATA.records).filter(r=>r.type==='log'&&r.mode==='ladder'&&r.unitId==='jj-unit');
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const screen = T(document.getElementById('screen'));
    const door = T(unitCard(DATA.records['jj-unit'], CLASS_BY_ID[cid]));
    go('stars',{});
    const stars = T(document.getElementById('screen'));
    return { view, logCount: logs2.length, log: logs2[0], pts: ladderPoints(), screen, door, stars, attempted: unitAttempted(DATA.records['jj-unit']) };
  }, [cid]);
  ck('finishing shows the score in gold, 7 of 9, real XP, and promises Double Jeopardy next — one log with done/points/round',
     fin.logCount===1 && fin.log.done && fin.log.points===fin.pts && fin.log.round==='single' && fin.log.xp===70
     && fin.screen.includes(fin.pts.toLocaleString()+' pts') && /7 of 9/.test(fin.screen) && /Next time is Double Jeopardy/.test(fin.screen), fin);
  ck('all nine questions count toward the lesson (qstat.plain), the door says when it was last played, Stars summarizes',
     fin.attempted===9 && fin.door.includes('Last played') && fin.door.includes(fin.pts.toLocaleString()+' pts') && /Junior Jeopardy/.test(fin.stars) && /1 board finished/.test(fin.stars), fin);

  // ---- Play again = Double Jeopardy: 200/400/600, harder tiers, and the
  //      last category from the older lesson on the same shelf
  const r2 = await p.evaluate(([cid])=>{
    go('ladder',{unitId:'jj-unit', classId:cid});
    document.querySelector('#screen .btn-primary').click();
    const s = ladderState;
    const cats = s.cats.map(c=>c.nm), older = s.cats.map(c=>!!c.older);
    const src = s.order.map(k=>ladderUnit.questions[k]._srcUnit);
    const lvTop = [0,1].map(c=>ladderUnit.questions[c*s.rows].lv);
    return { mode:s.mode, values:s.values.join(','), cats, older, src, lvTop, round: document.querySelector('.jj-round').textContent,
      tiles: document.querySelectorAll('.jj-tile').length };
  }, [cid]);
  ck('the second board is Double Jeopardy: 200/400/600 and harder tiers (the top row asks level 2+)',
     r2.mode==='double' && r2.values==='200,400,600,200,400,600,200,400,600' && r2.round==='Double Jeopardy' && r2.lvTop.every(l=>l>=2) && r2.tiles===9, r2);
  ck('its last category is the older lesson from the same shelf — three questions, tagged to that lesson',
     r2.cats[2]==='9-1 Older Lesson' && r2.older.join()==='false,false,true' && r2.src.slice(6).every(x=>x==='jj-older') && r2.src.slice(0,6).every(x=>x==='jj-unit'), r2);

  // ---- the wager (Chris, 2026-09: "let's make double jeopardy a wager they
  // can make, I think this might show confidence in how well they know
  // their material"). Scoped to Double Jeopardy's Daily Double only — Round
  // 1's stays the old flat double, already exercised above (the `dd`/`sc`
  // blocks ran entirely in Round 1 and never saw a wager slider). Play the
  // Double board's Daily Double twice over: once at zero score (the
  // degraded flat-bet path, since the wager range would otherwise collapse
  // to nothing), once after banking points (the real slider, bounded
  // [tile value, current score], and a wrong answer costs exactly what was
  // wagered rather than the tile's flat value).
  const wagerLow = await p.evaluate(()=>{
    const s = ladderState;
    const k = s.dd;
    const tile = [...document.querySelectorAll('.jj-tile')].find(t=>t.getAttribute('aria-label')===`${s.cats[s.catOf[k]].nm} for ${s.values[k]}`);
    tile.click();
    const modal = document.querySelector('.modal-overlay');
    const modalTxt = modal.textContent;
    const hasSlider = !!modal.querySelector('.wager input[type=range]');
    modal.querySelector('.btn-primary').click();
    return { modalTxt, hasSlider, wager: s.wager, tileVal: s.values[k], view, worth: document.querySelector('#screen .ladderworth')?.textContent };
  });
  ck('at zero score the Daily Double degrades to a flat bet (no slider, worth the tile either way)',
     !wagerLow.hasSlider && /isn.t ahead of this tile yet/.test(wagerLow.modalTxt) && wagerLow.wager===wagerLow.tileVal
     && wagerLow.view==='quiz' && wagerLow.worth===('★ Daily Double · '+wagerLow.tileVal), wagerLow);

  const wagerHigh = await p.evaluate(([cid])=>{
    const u = ladderUnit, s = ladderState;
    // bank the flat-bet DD from the current (already-degraded) board, then
    // finish it so a fresh Double board is dealt with an unplayed DD of its own
    const qq0 = u.questions[quizState.order[quizState.i]];
    document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(qq0.ans)].click();
    document.getElementById('qnext').click();
    const play = (unit, st, k)=>{ st.current=k; go('quiz',{unitId:'__ladder__',classId:st.classId,ladder:true},{back:true});
      const qq = unit.questions[quizState.order[quizState.i]];
      document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(qq.ans)].click();
      document.getElementById('qnext').click(); };
    s.order.forEach((_,k)=>{ if(k!==s.dd && !s.results[k]) play(u, s, k); });
    // a fresh Double board: score resets to 0 per board, so bank every
    // NON-Daily-Double tile first — that is what makes the wager range real
    // rather than degrading to the flat-bet path again
    go('unit',{classId:cid});
    go('ladder',{unitId:'jj-unit', classId:cid});
    document.querySelector('#screen .btn-primary').click();
    const s2 = ladderState, u2 = ladderUnit;
    s2.order.forEach((_,k)=>{ if(k!==s2.dd) play(u2, s2, k); });
    const scoreBefore = ladderPoints();
    const k2 = s2.dd, tileVal2 = s2.values[k2];
    const tile2 = [...document.querySelectorAll('.jj-tile')].find(t=>t.getAttribute('aria-label')===`${s2.cats[s2.catOf[k2]].nm} for ${s2.values[k2]}`);
    tile2.click();
    const modal = document.querySelector('.modal-overlay');
    const inp = modal.querySelector('.wager input[type=range]');
    const bounds = inp ? { min:+inp.min, max:+inp.max, step:+inp.step, startVal:+inp.value } : null;
    let mid = null, readAfterDrag = null;
    if(inp){
      // setting .value snaps to the nearest step from min, same as a real
      // drag would — read the SNAPPED value back rather than trusting the
      // unsnapped midpoint arithmetic
      inp.value = String(Math.round((+inp.min + +inp.max) / 2));
      inp.dispatchEvent(new Event('input',{bubbles:true}));
      mid = +inp.value;
      readAfterDrag = modal.querySelector('.wagerread').textContent;
      modal.querySelector('.btn-primary').click();
    }
    const wager = s2.wager;
    const scoreAtQuestion = ladderPoints();
    // answer wrong: should cost exactly the wager, not the tile's flat value
    const q2 = ladderUnit.questions[quizState.order[quizState.i]];
    const wrongIdx = q2.opts.findIndex((_,i)=>i!==q2.ans);
    document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(wrongIdx)].click();
    document.getElementById('qnext').click();
    const scoreAfter = ladderPoints();
    return { scoreBefore, tileVal2, bounds, mid, readAfterDrag, wager, scoreAtQuestion, scoreAfter, delta: scoreAtQuestion-scoreAfter };
  }, [cid]);
  ck('with a banked score, the wager slider is bounded [tile value, current score] and the live readout tracks it',
     wagerHigh.bounds && wagerHigh.bounds.min===wagerHigh.tileVal2 && wagerHigh.bounds.max===wagerHigh.scoreBefore
     && wagerHigh.wager===wagerHigh.mid && wagerHigh.readAfterDrag===wagerHigh.mid.toLocaleString()+' pts', wagerHigh);
  ck('a wrong answer on the wagered Daily Double costs exactly the wager, not the tile\'s flat value',
     wagerHigh.delta===wagerHigh.wager && wagerHigh.wager!==wagerHigh.tileVal2*2, wagerHigh);

  const wagerLog = await p.evaluate(()=>{
    const logs = Object.values(DATA.records).filter(r=>r.type==='log'&&r.mode==='ladder'&&r.round==='double');
    const l = logs[logs.length-1];
    return { wager: l.wager, wagerWon: l.wagerWon };
  });
  ck('the log records the wager and that it was lost', wagerLog.wager===wagerHigh.wager && wagerLog.wagerWon===false, wagerLog);

  // ---- the subject-screen board: every column a different lesson
  const mix = await p.evaluate(([cid])=>{
    go('unit',{classId:cid});
    const btn=[...document.querySelectorAll('#screen .btn-secondary')].find(b=>/Junior Jeopardy — a mix/.test(b.textContent));
    if(!btn) return {found:false};
    btn.click();
    return { found:true, view, unitId: ctx.unitId, cats: ladderState.cats.map(c=>c.nm),
      srcs:[...new Set(ladderState.order.map(k=>ladderUnit.questions[k]._srcUnit))] };
  },[cid]);
  ck('the subject screen offers a mix board whose categories are lessons, each drawing its own questions',
     mix.found && mix.view==='ladder' && mix.unitId==='__shuffle__' && mix.cats.length>=2 && mix.srcs.length===mix.cats.length, mix);

  // ---- modeLabel knows the new name
  const label = await p.evaluate(()=> modeLabel({mode:'ladder'}));
  ck('modeLabel names it Junior Jeopardy for the day view', label==='Junior Jeopardy', label);

  // ---- the parent-side report (Chris, 2026-09: "It would nice to see a
  // report of this game on the parent side too"). Derived entirely from
  // ladderGames() at render time — no new record types — and deliberately
  // fuller than the Stars-tab card (which stays the small, curated "smaller
  // degree" version on her own side, per Chris's own framing). By this
  // point in the run there are 3 finished boards (Round 1, and two Double
  // boards from the wager tests, one of which carries a lost wager).
  const rep = await p.evaluate(()=>{
    go('parent',{});
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const screen = T(document.getElementById('screen'));
    const usingRow = [...document.querySelectorAll('.row')].find(r=>/Junior Jeopardy boards finished/.test(r.textContent));
    const recentHead = [...document.querySelectorAll('.eyebrow')].find(e=>e.textContent==='Recent boards');
    const recentCard = recentHead && recentHead.closest('.card');
    const jjRep = ladderParentReport();
    return {
      screen, usingRow: T(usingRow),
      hasJJDivider: /Junior Jeopardy/.test(screen),
      boardsFinishedRow: [...document.querySelectorAll('.row')].some(r=>/Boards finished/.test(r.textContent) && new RegExp(jjRep.games.length+' \\(').test(r.textContent)),
      bestScoreRow: [...document.querySelectorAll('.row')].some(r=>/Best score/.test(r.textContent) && r.textContent.includes(jjRep.best.points.toLocaleString())),
      wagerRow: [...document.querySelectorAll('.row')].some(r=>/Daily Double wagers/.test(r.textContent) && r.textContent.includes(jjRep.wagerWins+' won of '+jjRep.wagers.length)),
      recentRows: recentCard ? recentCard.textContent : null,
      gamesCount: jjRep.games.length, wagers: jjRep.wagers.length, wagerWins: jjRep.wagerWins
    };
  });
  ck('the parent view carries a Junior Jeopardy boards-finished line in "What she is using"',
     rep.usingRow && rep.usingRow.includes(String(rep.gamesCount)), rep);
  ck('a "Junior Jeopardy" card reports boards finished (with the Double count), best score, and accuracy',
     rep.hasJJDivider && rep.boardsFinishedRow && rep.bestScoreRow, rep);
  ck('the card also reports the Daily Double wager win rate, since one was wagered and lost',
     rep.wagerRow && rep.wagers>0 && rep.wagerWins < rep.wagers, rep);
  ck('a "Recent boards" list names each board with its round, score, and wager outcome',
     rep.recentRows && /Double Jeopardy/.test(rep.recentRows) && /Round 1/.test(rep.recentRows) && /wagered/.test(rep.recentRows) && /lost/.test(rep.recentRows), rep);

  // ---- "Recent sessions" used to mislabel every session, quiz or not:
  // ANY non-focus/non-quiz mode (Junior Jeopardy included) fell through a
  // ternary straight to "Flashcards", and every quiz-mode session said the
  // bare word "Quiz" whether it was Beat the clock, a Growth Zone review,
  // a shuffle round, or the daily three. Both bugs are fixed by routing
  // through modeLabel() like every other render site already does.
  const sessions = await p.evaluate(()=>{
    const T = n => n ? n.textContent.replace(/\s+/g,' ').trim() : null;
    const rows = [...document.querySelectorAll('.row')].map(T);
    return { jjRow: rows.find(t=>/Junior Jeopardy/.test(t) && /pts/.test(t)),
      anyBareFlashcardsForJJ: rows.some(t=>/Junior Jeopardy/.test(t) && /Flashcards/.test(t)),
      reviewRow: rows.find(t=>/Growth Zone review/.test(t)) };
  });
  ck('a Recent sessions row for a Junior Jeopardy log names it correctly with its points, never "Flashcards"',
     sessions.jjRow && !sessions.anyBareFlashcardsForJJ && /pts/.test(sessions.jjRow), sessions);
  ck('the seeded Growth Zone review session is named correctly too, not the bare word "Quiz"',
     !!sessions.reviewRow && !/^[^·]*·\s*Quiz\s*·/.test(sessions.reviewRow), sessions);

  // ---- Chris, 2026-09: "I tested out a jeopardy question, left the game and
  // tested a quiz question, but after the how do you feel questions, I was
  // brought back to the jeopardy game." Real bug: leaving a Junior Jeopardy
  // question by anything OTHER than the board's own Leave button or
  // answering through — a nav tab, the back chip, the brand logo — left
  // quizState dangling with ladder:true and unitId:'__ladder__'. go()'s own
  // leave-hook explicitly skips a ladder round (the board handles its own
  // return), so nothing else cleared it; the NEXT quiz's rebuild logic in
  // SCREENS.quiz only rebuilds `if(!quizState)`, so a merely WRONG (not
  // absent) quizState survived untouched when no saved round existed for
  // the new unit — silently routing that quiz's own "Next" taps through
  // ladderReturn() instead of finishQuiz(), which is what sent her back to
  // the old board once she reached it. Fixed in two places: go()'s
  // leave-hook now always clears an abandoned ladder quizState, and
  // SCREENS.quiz's rebuild unconditionally discards a mismatched quizState
  // before trying to load or build a replacement, so the same class of bug
  // can't recur from a different leave path.
  const contaminated = await p.evaluate(async ([cid])=>{
    const mk = (i) => ({ id:'q'+i, lv:1, from:'source', q:'CX Q'+i+'?', opts:['a'+i,'b'+i,'c'+i,'d'+i], ans:i%4 });
    put({ id:'cx-jj', type:'unit', classId:cid, status:'approved', title:'Contamination Lesson',
      cards:[], questions:[...Array(8).keys()].map(mk) });
    put({ id:'cx-plain', type:'unit', classId:cid, status:'approved', title:'Plain Lesson', round:5,
      cards:[], questions:[...Array(5).keys()].map(mk) });

    // Open a Junior Jeopardy question, then leave it via a NAV TAB —
    // never the tile's own Leave button — while it is still unanswered.
    ladderState = null;
    go('ladder', {unitId:'cx-jj', classId:cid});
    ladderState.current = 0;
    go('quiz', {unitId:'__ladder__', classId:cid, ladder:true}, {back:true});
    const midLadder = quizState && quizState.ladder;
    go('study', {});                          // tapping a bottom nav tab
    const clearedByNav = quizState;            // must be null right away

    // Take a completely ordinary quiz on a different lesson, start to finish.
    // The check-in is one readiness tap now, which moves straight into the
    // quiz on its own beat (no Start button to click any more).
    go('checkin', {unitId:'cx-plain', classId:cid});
    document.querySelectorAll('#screen .scale')[0].querySelectorAll('button')[2].click();
    await new Promise(r=>setTimeout(r,450));
    const rebuiltCorrectly = quizState && !quizState.ladder && quizState.unitId==='cx-plain';
    let guard=0;
    while (view==='quiz' && guard++<20){
      const u = unitFor('cx-plain');
      const q = u.questions[quizState.order[quizState.i]];
      document.querySelectorAll('#screen .opt')[quizState.optArr.indexOf(q.ans)].click();
      document.getElementById('qnext').click();
    }
    const reachedResults = view==='unit' && !!document.querySelector('.modal-overlay .btn-primary');
    document.querySelector('.modal-overlay .btn-primary').click();  // "How did that feel?"
    const atPostmood = view==='postmood';
    const doneBtn = [...document.querySelectorAll('#screen button')].find(b=>/Done|Skip/.test(b.textContent));
    doneBtn.click();
    return { midLadder, clearedByNav, rebuiltCorrectly, reachedResults, atPostmood, finalView: view, finalClassId: ctx.classId };
  }, [cid]);
  ck('leaving a Jeopardy question via a nav tab clears quizState immediately, rather than leaving ladder:true dangling',
     contaminated.midLadder===true && contaminated.clearedByNav===null, contaminated);
  ck('an ordinary quiz opened afterward rebuilds correctly for its own unit, never inheriting the stale ladder state',
     contaminated.rebuiltCorrectly===true, contaminated);
  ck('it reaches the results modal and the postmood check-in exactly like any other ordinary round',
     contaminated.reachedResults===true && contaminated.atPostmood===true, contaminated);
  ck('after "How did that feel?" she lands on the subject page — NOT back on the old Jeopardy board',
     contaminated.finalView==='unit' && contaminated.finalClassId===cid, contaminated);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got).slice(0,600))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
