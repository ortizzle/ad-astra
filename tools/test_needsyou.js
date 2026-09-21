/* "Needs you" — one card at the top of the parent view saying what is
   waiting on a grown-up, and one function (needsYou) behind it.

   Chris: "would there be a way for you to provide me with a summary of what
   needs attention daily?" Four true facts lived four screens apart. The
   assertions that matter are the RULES, not the rows: her own progress is
   never a chore on his list, a real zero is a grade and not an unmarked
   test, and nothing is printed twice on one screen.

   Same file, both apps. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8104;

(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:1400}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});
  const card = () => p.evaluate(() => {
    const c = [...document.querySelectorAll('#screen .card')]
      .find(x => /Needs you/i.test(x.innerText));
    if(!c) return {missing:true};
    return {txt: c.innerText,
      rows: [...c.querySelectorAll('.nyrow')].map(r=>({
        label: r.querySelector('.nyl').textContent,
        sub: r.querySelector('small') ? r.querySelector('small').textContent : null,
        tap: r.classList.contains('tap'), warn: r.classList.contains('warn'),
        tag: r.tagName, h: Math.round(r.getBoundingClientRect().height)}))};
  });

  /* A quiet day says so, rather than rendering empty rows. */
  const quiet = await p.evaluate(() => { go('parent');
    const c = [...document.querySelectorAll('#screen .card')].find(x=>/Needs you/i.test(x.innerText));
    return {txt: c ? c.innerText : '(no card)', rows: c ? c.querySelectorAll('.nyrow').length : -1}; });
  ck('a clean install says nothing is waiting, with no empty rows',
     quiet.rows === 0 && /Nothing is waiting on you/i.test(quiet.txt), quiet);

  /* Now give it one of each. */
  const seed = await p.evaluate(() => {
    AZ.today = () => '2026-09-21';
    const cid = STUDY_CLASSES[0].id;
    put({id:'unit-ny-a', type:'unit', classId:cid, status:'draft', title:'A draft lesson',
         cards:[{id:'c1',term:'x',def:'**y**'}], questions:[], updatedAt:Date.now()});
    put({id:'unit-ny-b', type:'unit', classId:cid, status:'draft', title:'B draft lesson',
         cards:[{id:'c1',term:'x',def:'**y**'}], questions:[], updatedAt:Date.now()});
    /* Sat, unmarked → a chore. */
    put({id:'assess_ny1', type:'assess', classId:cid, kind:'quiet', title:'The unmarked quiz',
         date:'2026-09-15', score:null});
    /* Sat, scored ZERO → a grade, never a chore. The !score trap. */
    put({id:'assess_ny0', type:'assess', classId:cid, kind:'quiz', title:'The zero',
         date:'2026-09-16', points:0, outOf:100, score:0});
    /* Still ahead → waiting on the school, not on him. */
    put({id:'assess_ny2', type:'assess', classId:cid, kind:'test', title:'Next weeks test',
         date:'2026-09-30', score:null});
    put({id:'flag_ny1', type:'flag', unitId:'unit-ny-a', classId:cid, qid:'q1',
         q:'Something looks wrong', note:'', date:'2026-09-20'});
    /* Her own progress: a pile of due reviews and a broken streak. NOT his. */
    for(let i=0;i<9;i++) put({id:'miss_ny'+i, type:'miss', unitId:'unit-ny-a', classId:cid,
      qid:'q'+i, q:'Q'+i, opts:['a','b','c','d'], ans:0, right:'a',
      box:0, due:'2026-09-01', on:'2026-09-01'});
    saveLocal(); go('parent');
    return {n: needsYou('2026-09-21').items.length, keys: needsYou('2026-09-21').items.map(i=>i.k)};
  });
  const c1 = await card();
  ck('drafts, the unmarked test and the flag all surface',
     ['drafts','scores','flags'].every(k=>seed.keys.includes(k)), seed.keys);
  ck('a test scored ZERO is a grade, not a chore', !/The zero/.test(c1.txt), c1.txt);
  ck('a test still ahead is not a chore either — it waits on the school',
     !/Next weeks test/.test(c1.txt), c1.txt);
  ck('her nine due reviews are hers and never appear as his to-do',
     !/review|growth/i.test(c1.txt), c1.txt);
  ck('every row with somewhere to go is a real button at 44px',
     c1.rows.filter(r=>r.tap).every(r=>r.tag==='BUTTON' && r.h>=44), c1.rows);

  /* Nothing on this screen may say the same thing twice — the rule the old
     lead card's own comment was written about. */
  const dupes = await p.evaluate(() => {
    const t = document.getElementById('screen').innerText;
    return {draftCounts: (t.match(/2 units? to read/g)||[]).length,
            oldCard: /units are waiting for you/.test(t),
            scheduledDoors: (t.match(/scheduled · next/g)||[]).length};
  });
  ck('the draft count is printed once, and the old lead card is gone',
     dupes.draftCounts === 1 && !dupes.oldCard, dupes);

  /* Held units report as an aside, and through exactly one door. */
  const held = await p.evaluate(() => {
    const u = DATA.records['unit-ny-a'];
    u.status='approved'; u.releaseOn='2026-10-01'; put(u); saveLocal(); go('parent');
    const t = document.getElementById('screen').innerText;
    const ny = needsYou('2026-09-21');
    return {held: ny.held, inItems: ny.items.some(i=>i.k==='held'),
            doors: (t.match(/scheduled · next/g)||[]).length};
  });
  ck('a held unit is an aside, never a fifth thing owed',
     held.held === 1 && !held.inItems, held);
  ck('and it has exactly one door on the page', held.doors === 1, held);

  /* The two footguns: sandbox left on, and a token that died quietly. */
  const warn = await p.evaluate(() => {
    setSandbox(true); go('parent');
    const c = [...document.querySelectorAll('#screen .card')].find(x=>/Needs you/i.test(x.innerText));
    const row = [...c.querySelectorAll('.nyrow')].find(r=>/Sandbox/.test(r.textContent));
    const col = row ? getComputedStyle(row.querySelector('.nyl')).color : null;
    const warmv = getComputedStyle(document.documentElement).getPropertyValue('--warm').trim();
    const res = {found: !!row, tag: row && row.tagName, col, warmv,
      notPressable: row && !row.classList.contains('tap')};
    setSandbox(false);
    return res;
  });
  ck('sandbox left on is called out', warn.found, warn);
  ck('and reads as a warning, not as a chore with a door',
     warn.tag === 'DIV' && warn.notPressable, warn);

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got).slice(0,400))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
