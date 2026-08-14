/* Play a whole round in the real app and check the redesign:
   the tool row replaces the stacked buttons, every tool still clears 44px,
   nothing overflows, and the results modal ends on the drawn shape with the
   score said exactly once. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8099;

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = [];
  p.on('pageerror', e => errs.push(String(e.message)));
  p.on('console', m => { if(m.type()==='error') errs.push('console: '+m.text().slice(0,160)); });
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.addScriptTag({path:__dirname+'/seed.js'});
  await p.waitForTimeout(400);

  // Pull in the shipped library so a real math unit (with hints and a
  // calculator subject) is available, and approve it.
  await p.evaluate(async ()=>{
    for(const path of (typeof CONTENT_LIBRARY!=='undefined'?CONTENT_LIBRARY:[])){
      try{ const r = await fetch(path); const j = await r.json();
        Object.values(j.records||{}).forEach(rec=>{ rec.status='approved'; DATA.records[rec.id]=rec; });
      }catch(e){}
    }
    saveLocal();
  });

  const out = {};
  // Open a math unit's quiz directly.
  out.unit = await p.evaluate(()=>{
    const u = Object.values(DATA.records).find(r=>r.type==='unit' && !r.deleted
      && CALC_CLASSES.has(r.classId) && (r.questions||[]).length>=4 && !r.guide
      && !(r.questions||[]).some(q=>q.kind));
    if(!u) return null;
    go('quiz',{classId:u.classId, unitId:u.id});
    return {id:u.id, title:u.title, n:u.questions.length,
            hints:u.questions.filter(q=>q.hint).length};
  });
  await p.waitForTimeout(350);

  // --- the tool row -------------------------------------------------------
  out.tools = await p.$$eval('.tool', ns => ns.map(n => ({
    label: n.textContent.trim(),
    h: Math.round(n.getBoundingClientRect().height),
    w: Math.round(n.getBoundingClientRect().width),
    clipped: n.scrollWidth > n.clientWidth + 1
  })));
  // The old stacked ghost buttons must be gone from the quiz screen.
  out.stackedGhosts = await p.$$eval('#screen .btn-ghost', ns =>
    ns.map(n=>n.textContent.trim()));
  out.hScroll = await p.evaluate(()=>document.documentElement.scrollWidth > window.innerWidth+1);
  out.bandOnScreen = await p.$$eval('.qband', n=>n.length);

  // Height of everything below the last option — the furniture between her and
  // the next question.
  out.footerPx = await p.evaluate(()=>{
    const opts=[...document.querySelectorAll('#screen .opt')];
    const tools=document.querySelector('#screen .tools');
    if(!opts.length||!tools) return null;
    const last=opts[opts.length-1].getBoundingClientRect();
    const sc=document.getElementById('screen').getBoundingClientRect();
    return Math.round(sc.bottom-last.bottom);
  });

  // --- play the round -----------------------------------------------------
  const n = out.unit.n;
  for(let i=0;i<n;i++){
    // deliberately wrong on every third question, so the finish has dim stars
    const picked = await p.evaluate((i)=>{
      const q = quizState ? unitFor(quizState.unitId).questions[quizState.order[quizState.i]] : null;
      if(!q) return 'noq';
      const opts=[...document.querySelectorAll('#screen .opt')];
      if(!opts.length) return 'noopts';
      const wrongPos = quizState.optArr.findIndex(o=>o!==q.ans);
      const rightPos = quizState.optArr.indexOf(q.ans);
      opts[i%3===2 ? wrongPos : rightPos].click();
      return 'ok';
    }, i);
    if(picked!=='ok'){ out.playFail = {i, picked}; break; }
    await p.waitForTimeout(160);
    await p.evaluate(()=>{
      const b=[...document.querySelectorAll('#screen .btn-primary')]
        .find(x=>/Next question|See results/.test(x.textContent));
      if(b) b.click();
    });
    await p.waitForTimeout(200);
  }
  await p.waitForTimeout(500);

  // --- the results modal --------------------------------------------------
  out.modal = await p.evaluate(()=>{
    const box=document.querySelector('.modal-box');
    if(!box) return null;
    const band=box.querySelector('.qband.drawn');
    const kids=[...box.children].map(k=>k.tagName.toLowerCase()+'.'+(k.className||''));
    return {
      title: box.querySelector('h3')?.textContent,
      bandFirst: box.firstElementChild===band,
      bandH: band?Math.round(band.getBoundingClientRect().height):0,
      lit: box.querySelectorAll('.qband.drawn .star.lit').length,
      dim: box.querySelectorAll('.qband.drawn .star.dim').length,
      now: box.querySelectorAll('.qband.drawn .star.now').length,
      segs: box.querySelectorAll('.qband.drawn .seg').length,
      tally: [...box.querySelectorAll('.tally span')].map(s=>s.textContent),
      message: box.querySelector('p')?.textContent,
      order: kids,
      hScroll: box.scrollWidth > box.clientWidth+1
    };
  });
  // The score must be said once, not three times.
  if(out.modal){
    const all = out.modal.title+' '+out.modal.message+' '+out.modal.tally.join(' ');
    out.pctPrinted = (all.match(/\d+%/g)||[]).length;
    out.fracPrinted = (all.match(/\b\d+ of \d+\b|\b\d+\/\d+\b/g)||[]);
  }
  out.errors = errs.length?errs:'none';
  console.log(JSON.stringify(out,null,1));
  await b.close();
})();
