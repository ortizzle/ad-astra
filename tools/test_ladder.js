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

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got).slice(0,600))));
  console.log(TAG, out.every(r=>r.ok)?'ALL PASS':'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok)||errs.length) process.exit(1);
})();
