/* The physics formula guide and the "Which formula?" finder (v203).

   Pins:
     * the guide has an entry for every formula on her teacher's sheet, 1-28,
       in the sheet's order, and each entry's formula is CHARACTER FOR
       CHARACTER the one the sheet row shows — so the explanation can never
       drift onto a different formula from the one she tapped;
     * every one of those 28 rows is a 44px door into its entry, and nothing
       else on the sheet pretends to be (conversions, textbook blocks, the
       waves and circuits rows the guide does not cover);
     * Back returns to the sheet at the row she tapped;
     * INSIDE A QUIZ the worked example is withheld, through the real tool row
       — a worked example open during a quiz is a template to copy;
     * the finder answers by the guide's own variable sets, and never appears
       in the quiz;
     * the printed sheet's F_net = ma = mv² / r, which the old transcription
       had cut short;
     * the new reading surfaces clear 4.5:1 in both themes.

   Verified by stripping the guide number from one row, letting the worked
   example through in quiz mode, and putting the finder door in the quiz tool
   row: five assertions failed, all from those three causes (the stripped row
   also fails the 28-doors and Back counts). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  // ---- the data
  const data = await p.evaluate(()=>{
    const G = FORMULA_GUIDE;
    const rows = SHEETS.physics.sections.flatMap(s=>s.rows.map(r=>({h:s.h, nm:r[0], eq:r[1], g:r[2]})));
    const guided = rows.filter(r=>r.g);
    return {
      ns: G.map(e=>e.n),
      complete: G.every(e=>e.nm && e.eq && e.does && e.sym.length && e.when && e.ex.lines.length && e.watch.length),
      guidedNs: guided.map(r=>r.g),
      eqMismatch: guided.filter(r=>G.find(e=>e.n===r.g).eq !== r.eq).map(r=>[r.g, r.eq, G.find(e=>e.n===r.g).eq]),
      unguidedSecs: [...new Set(rows.filter(r=>!r.g).map(r=>r.h))],
      second: rows.find(r=>r.g===8),
      notes: G.filter(e=>e.note).map(e=>e.n),
      finderless: G.filter(e=>!e.v).map(e=>e.n),
      names: /Ortiz|Sedona/i.test(JSON.stringify(G)),
    };
  });
  const seq = Array.from({length:28},(_,i)=>i+1);
  ck('the guide has entries 1-28, each one complete', JSON.stringify(data.ns)===JSON.stringify(seq) && data.complete, data.ns);
  ck('the sheet carries guide numbers 1-28, in the sheet\'s own order', JSON.stringify(data.guidedNs)===JSON.stringify(seq), data.guidedNs);
  ck('every guided row shows exactly the formula its entry explains', !data.eqMismatch.length, data.eqMismatch);
  ck('the printed sheet\'s F_net = ma = mv² / r is on the sheet', data.second && data.second.eq==='F_net = ma = mv² / r', data.second);
  ck('no door on rows the guide does not cover (waves, circuits, notation, conversions)',
     ['Waves and Light','Electric Circuits','Time','Length'].every(h=>data.unguidedSecs.includes(h)), data.unguidedSecs);
  ck('the eight entries the guide flags carry a note to ask the teacher', JSON.stringify(data.notes)==='[1,2,8,12,15,18,20,25]', data.notes);
  ck('the finder leaves out what answers no "I know, I want" question', JSON.stringify(data.finderless)==='[1,2,20,24,25,28]', data.finderless);
  ck('no name in the guide', !data.names, data.names);

  // ---- the sheet, the door, the entry, back
  const sheet = await p.evaluate(async ()=>{
    go('unit',{classId:'physics'});
    const door = [...document.querySelectorAll('#screen button')].some(x=>/Which formula\?/.test(x.textContent));
    openSheet('physics');
    const box = document.querySelector('.modal-box');
    const taps = [...box.querySelectorAll('button.frow.tap')];
    const tall = taps.every(x=>x.getBoundingClientRect().height>=44);
    const r7 = taps.find(x=>x.dataset.g==='7');
    r7.scrollIntoView();
    const before = box.scrollTop;
    r7.click();
    const entry = { formula: /Formula 7 · Kinematics/.test(box.textContent),
                    example: box.querySelectorAll('.fg-line').length,
                    answer: /= 40 m/.test(box.textContent), top: box.scrollTop };
    [...box.querySelectorAll('button')].find(x=>/Back to the sheet/.test(x.textContent)).click();
    const backAt = box.scrollTop, back = box.querySelectorAll('button.frow.tap').length;
    document.querySelectorAll('.modal-overlay').forEach(m=>m.remove());
    return { door, taps: taps.length, tall, before, entry, backAt, back };
  });
  ck('the physics page has the finder door', sheet.door, sheet.door);
  ck('28 rows are doors, every one at least 44px', sheet.taps===28 && sheet.tall, sheet);
  ck('tapping a row opens that formula\'s entry, worked example and all, at the top',
     sheet.entry.formula && sheet.entry.example>=3 && sheet.entry.answer && sheet.entry.top===0, sheet.entry);
  ck('Back returns to the sheet at the row she tapped', sheet.back===28 && Math.abs(sheet.backAt - sheet.before) <= 2, sheet);

  // ---- inside a real quiz: the tool row's Sheet withholds the example; no finder
  const quiz = await p.evaluate(async ()=>{
    const f = CONTENT_LIBRARY.find(x=>/phys-kinematics-equations/.test(x));
    const j = await (await fetch(f,{cache:'no-store'})).json();
    Object.values(j.records).forEach(r=>{ r.status='approved'; delete r.releaseOn; put(r); });
    const uid = Object.keys(j.records)[0];
    quizState = null;
    go('quiz',{unitId:uid, classId:'physics'});
    const tools = [...document.querySelectorAll('#screen button')];
    const finder = tools.some(x=>/Which formula/.test(x.textContent));
    const sh = tools.find(x=>/Sheet/.test(x.textContent));
    if(!sh) return {sheet:false};
    sh.click();
    const box = document.querySelector('.modal-box');
    [...box.querySelectorAll('button.frow.tap')].find(x=>x.dataset.g==='6').click();
    const r = { sheet:true, finder, lines: box.querySelectorAll('.fg-line').length,
                withheld: /stays out of the quiz/.test(box.textContent),
                symbols: box.querySelectorAll('.fg-sym').length, watch: box.querySelectorAll('.fg-watch').length };
    document.querySelectorAll('.modal-overlay').forEach(m=>m.remove());
    return r;
  });
  ck('inside a quiz the Sheet entry withholds the worked example, and says so', quiz.sheet && quiz.lines===0 && quiz.withheld, quiz);
  ck('…while the symbols and the mistakes to watch for stay', quiz.symbols>=4 && quiz.watch>=3, quiz);
  ck('the finder is never in the quiz', quiz.sheet && !quiz.finder, quiz);

  // ---- the finder's answers
  const fd = await p.evaluate(()=>{
    const run = (w, k)=> formulaFinder(w, new Set(k));
    const fit = r=> r.filter(x=>!x.missing.length).map(x=>x.n);
    const a = run('dx',['vi','a','t']), b = run('a',['vf','vi','t']), c = run('F',['m','v','r']),
          d = run('vf',['vi','a','dx']), e = run('KE',['m','v']), g = run('th',['opp','hyp']);
    const near = a.filter(x=>x.missing.length===1).map(x=>[x.n, x.missing.join()]);
    const everyN = new Set(['dx','vi','vf','v','a','t','F','m','r','FN','mu','Ff','k','x','W','th','KE','PE','h','P','p','dp','J','dv','opp','adj','hyp']
      .flatMap(w=>run(w,[]).map(x=>x.n)));
    return { a:fit(a), near, b:fit(b), c:fit(c), d:fit(d), e:fit(e), g:fit(g),
             leaked: [1,2,20,24,25,28].filter(n=>everyN.has(n)) };
  });
  ck('Δx from v_i, a, t → formula 6 alone fits', JSON.stringify(fd.a)==='[6]', fd.a);
  ck('…and 4, 5, 7 are one short, each naming v_f', JSON.stringify(fd.near)==='[[4,"vf"],[5,"vf"],[7,"vf"]]', fd.near);
  /* F from m, v, r offers gravitation too, and should: with masses and a
     distance it does fit (G is on the sheet). The entry's "when to use it"
     is what tells a circle from two planets — the finder narrows, she picks. */
  ck('a from v_f, v_i, t → 3; F from m, v, r → 8 and gravitation 12; v_f from v_i, a, Δx → 7; KE → 14; θ from opp, hyp → 26',
     JSON.stringify([fd.b,fd.c,fd.d,fd.e,fd.g])==='[[3],[8,12],[7],[14],[26]]', fd);
  ck('the quadratic, percent error, Δp line and constants are never offered', !fd.leaked.length, fd.leaked);

  // ---- the finder screen: chips, results, a result opening its entry
  const scr = await p.evaluate(()=>{
    go('formulas',{classId:'physics'});
    const want = [...document.querySelectorAll('#screen .gz-chip')].find(x=>x.dataset.pick==='want' && x.dataset.k==='dx');
    want.click();
    ['vi','a','t'].forEach(k=>[...document.querySelectorAll('#screen .gz-chip')].find(x=>x.dataset.pick==='known' && x.dataset.k===k).click());
    const res = [...document.querySelectorAll('#fgresults .fgres')];
    const heads = [...document.querySelectorAll('#fgresults .eyebrow')].map(x=>x.textContent);
    const tall = [...document.querySelectorAll('#screen .gz-chip, #fgresults .fgres')].every(x=>x.getBoundingClientRect().height>=44);
    res[0].click();
    const box = document.querySelector('.modal-box');
    const opened = box && /Displacement from v_i, a and t/.test(box.textContent) && box.querySelectorAll('.fg-line').length>=3;
    document.querySelectorAll('.modal-overlay').forEach(m=>m.remove());
    return { order: res.map(x=>+x.dataset.n), heads, tall, opened, wantNotKnown: !document.querySelector('#screen .gz-chip[data-pick="known"][data-k="dx"]') };
  });
  ck('the screen lists the fit first, then the one-short under its own heading',
     JSON.stringify(scr.order)==='[6,4,5,7]' && /only what you have/.test(scr.heads[0]) && scr.heads.includes('One quantity short'), scr);
  ck('the wanted quantity is not offered again as known', scr.wantNotKnown, scr);
  ck('every chip and result is at least 44px', scr.tall, scr.tall);
  ck('a result opens its full entry, worked example included', scr.opened, scr.opened);

  // ---- contrast on the new reading surfaces, both themes
  const cr = await p.evaluate(()=>{
    const parse = s=>{ const m = s.match(/color\(srgb ([\d.]+) ([\d.]+) ([\d.]+)/);
      if(m) return [m[1],m[2],m[3]].map(v=>+v*255);
      return (s.match(/[\d.]+/g)||[]).slice(0,3).map(Number); };
    const alpha = s=>{ const m = s.match(/\/ ([\d.]+)\)/) || s.match(/rgba\([^)]*,\s*([\d.]+)\)/); return m ? +m[1] : 1; };
    const L = c=>{ const [r,g,b2]=c.map(v=>{v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4);}); return 0.2126*r+0.7152*g+0.0722*b2; };
    const ratio = (a,b2)=>{ const x=L(a), y=L(b2); return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05); };
    const bgOf = n=>{ for(let e=n; e; e=e.parentElement){ const s=getComputedStyle(e).backgroundColor; if(s && alpha(s)>=0.99) return parse(s); } return [255,255,255]; };
    const res = [];
    for(const th of ['dark','light']){
      document.documentElement.dataset.theme = th;
      document.querySelectorAll('*').forEach(n=>n.style.transition='none');
      openSheet('physics', {entry:12});
      const sel = ['.fg-note .eyebrow','.fg-note p','.fg-sym .u','.fg-sym span:nth-child(2)','.fguide .eyebrow','.fg-src'];
      sel.forEach(s=>{ const n=document.querySelector('.modal-box '+s); if(n) res.push([th,s,+ratio(parse(getComputedStyle(n).color), bgOf(n)).toFixed(2)]); });
      document.querySelectorAll('.modal-overlay').forEach(m=>m.remove());
      openSheet('physics', {entry:6});
      const w = document.querySelector('.modal-box .fg-line .why'); res.push([th,'.fg-line .why',+ratio(parse(getComputedStyle(w).color), bgOf(w)).toFixed(2)]);
      document.querySelectorAll('.modal-overlay').forEach(m=>m.remove());
      go('formulas',{classId:'physics'}); ctx._fw='dx'; ctx._fk=new Set(['vi','a']); render();
      ['.fgres .k','.fgres .need','.fg-grp'].forEach(s=>{ const n=document.querySelector('#screen '+s); if(n) res.push([th,s,+ratio(parse(getComputedStyle(n).color), bgOf(n)).toFixed(2)]); });
    }
    return res;
  });
  const worst = cr.reduce((a,x)=> x[2]<a[2]?x:a, ['','',99]);
  ck('every new reading surface clears 4.5:1 in both themes (worst ' + worst[2] + ')', cr.length>=18 && worst[2]>=4.5, {n:cr.length, low:cr.filter(x=>x[2]<4.5), all:cr});

  let bad=0;
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got).slice(0,400)); }
                   else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
