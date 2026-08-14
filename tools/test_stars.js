/* Stars: what she has locked in, trophies, deduped counters, folded badges.
   Run: node test_stars.js <port> */
const { chromium } = require('playwright');
const PORT = process.argv[2];
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'});
  await p.waitForTimeout(300);
  await p.evaluate(async ()=>{
    for(const path of CONTENT_LIBRARY){
      try{ const r = await fetch(path); const j = await r.json();
        Object.values(j.records||{}).forEach(rec=>{ rec.status='approved'; DATA.records[rec.id]=rec; });
      }catch(e){}
    }
  });
  const out = []; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  /* ---- empty state: says what the list is FOR, no vanity rows ---- */
  const empty = await p.evaluate(()=>{
    all('cleared').forEach(c=>softDelete(c.id));
    go('stars');
    const t = document.getElementById('screen').textContent;
    return { says: /Nothing here yet/.test(t),
             explains: /survives the whole review ladder/.test(t),
             noVanity: !/Days studied|Study sessions|Questions answered|Focus minutes/.test(t) };
  });
  ck('empty locked-in explains the bar', empty.says && empty.explains, empty);
  ck('vanity counters are gone', empty.noVanity, empty);

  /* ---- with cleared questions ---- */
  await p.addScriptTag({path:__dirname+'/seed_rich.js'});
  await p.waitForTimeout(300);
  const rich = await p.evaluate(()=>{
    go('stars');
    const sc = document.getElementById('screen'), t = sc.textContent;
    const li = lockedIn();
    return {
      total: li.total, rows: li.rows.length,
      chips: [...sc.querySelectorAll('.lk')].map(x=>x.textContent.replace(/\s+/g,' ').trim()),
      headline: [...sc.querySelectorAll('h3')].map(h=>h.textContent),
      hasLocked: /learned for good/.test(t),
      screens: +(sc.scrollHeight/844).toFixed(1)
    };
  });
  ck('locked-in totals and per-subject chips', rich.total>0 && rich.chips.length===rich.rows, rich);
  ck('leads with "learned for good"', rich.hasLocked, rich.headline);

  /* a chip is a door */
  const door = await p.evaluate(()=>{
    document.querySelector('#screen .lk').click();
    return typeof view !== 'undefined' ? view : null;
  });
  ck('locked-in chip opens that subject', door==='unit', door);
  await p.evaluate(()=>go('stars'));
  await p.waitForTimeout(150);

  /* ---- no number printed twice ---- */
  const dedupe = await p.evaluate(()=>{
    const sc = document.getElementById('screen');
    const hdr = document.querySelector('header') || document.body;
    const s = stats();
    const screenTxt = sc.textContent;
    /* the streak and the Growth-due count must not be restated on this tab */
    const streakOnTab = (screenTxt.match(new RegExp('\\\\b'+s.streak+'\\\\s*day','g'))||[]).length;
    const growthOnTab = /Growth Zone items/.test(screenTxt);
    /* textContent runs "Level 4" straight into "85 XP to go", so match the
       rendered label nodes rather than the concatenated string. */
    const levelOnTab = [...sc.querySelectorAll('h2,p,.k,.v')]
      .filter(n=>/^Level \d+$/.test(n.textContent.trim())
                || /Level \d+ ·/.test(n.textContent)).length;
    return { streakOnTab, growthOnTab, levelOnTab };
  });
  ck('streak not restated on the tab', dedupe.streakOnTab===0, dedupe);
  ck('growth count not restated', !dedupe.growthOnTab, dedupe);
  ck('level printed once', dedupe.levelOnTab<=1, dedupe);

  /* ---- badges: earned shown, locked folded ---- */
  const badges = await p.evaluate(()=>{
    const sc = document.getElementById('screen');
    const shown = sc.querySelectorAll('.bdg').length;
    const got = sc.querySelectorAll('.bdg.got').length;
    const more = [...sc.querySelectorAll('button')].find(x=>/more to find/.test(x.textContent));
    return { shown, got, allShown: shown===got, more: more?more.textContent:null };
  });
  ck('only earned badges are shown', badges.allShown && badges.got>0, badges);
  ck('the rest are one tap away', /more to find/.test(badges.more||''), badges);
  const expand = await p.evaluate(()=>{
    [...document.querySelectorAll('#screen button')].find(x=>/more to find/.test(x.textContent)).click();
    return null;
  });
  await p.waitForTimeout(200);
  const expanded = await p.evaluate(()=>{
    const sc=document.getElementById('screen');
    return { shown: sc.querySelectorAll('.bdg').length, total: BADGES.length };
  });
  ck('expanding shows every badge', expanded.shown===expanded.total, expanded);

  /* ---- movement line only when the change is real ---- */
  const mv = await p.evaluate(()=>{
    const before = !!movement(AZ.today());
    /* manufacture a genuine climb in one subject */
    const cid = STUDY_CLASSES[0].id;
    for(let d=45; d>22; d--) put({id:'mv_a'+d,type:'log',mode:'quiz',classId:cid,unitId:'u',
      date:AZ.shift(AZ.today(),-d), at:Date.now()-d*86400000, correct:2, total:5, seconds:100, xp:20});
    for(let d=20; d>0; d--) put({id:'mv_b'+d,type:'log',mode:'quiz',classId:cid,unitId:'u',
      date:AZ.shift(AZ.today(),-d), at:Date.now()-d*86400000, correct:5, total:5, seconds:100, xp:50});
    const m = movement(AZ.today());
    go('stars');
    const t = document.getElementById('screen').textContent;
    return { before, after: !!m, d: m&&m.d, worded: /Worth noticing/.test(t),
             /* scope to the movement card: an unscoped /bad/i matches
                "Badges" and reports a failure that is not there. */
             noGrade: !/\b(bad|poor|weak|behind|worse)\b/i.test(
               [...document.querySelectorAll('#screen .card')]
                 .filter(c=>/Worth noticing/.test(c.textContent))
                 .map(c=>c.textContent).join(' ')) };
  });
  ck('movement appears only on a real climb', mv.after && mv.d>=8, mv);
  ck('movement is worded as change, not a grade', mv.worded && mv.noGrade, mv);

  out.forEach(r=>console.log((r.ok?'  ok ':'FAIL ')+r.n+(r.ok?'':' → '+JSON.stringify(r.got))));
  console.log('--- as rendered ---');
  console.log(' locked-in :', rich.total, 'across', rich.rows, 'subjects');
  console.log(' chips     :', rich.chips.join(' | '));
  console.log(' badges    :', badges.got, 'shown,', badges.more);
  console.log(' screens   :', rich.screens);
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('errors:', errs.length?errs:'none');
  await b.close();
  if(!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
