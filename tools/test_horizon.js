/* Assert the knob turned: on a date whose next milestone IS the quarter end,
   the card must print that fact once; on a date whose next milestone is
   something else, the quarter row must still be there. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8130;
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);

  const r = await p.evaluate(()=>{
    const real = AZ.today;
    /* Read the value CELLS, never the concatenated text: "End of Quarter 1"
       followed by "3 days" reads as "...Quarter 13 days", and a /(\d+) days/
       sweep over that saw "13 days" vs "3 days" and called it no duplicate.
       My first cut of this test passed against the unfixed app because of it. */
    const rowsOn = d => { AZ.today = () => d; go('today');
      const c = [...document.querySelectorAll('#screen .card')].pop();
      const rows = c ? [...c.querySelectorAll('.row')] : [];
      return { txt: c ? c.textContent.replace(/\s+/g,' ').trim() : '',
               vals: rows.map(r => (r.querySelector('.v')||{}).textContent || ''),
               rows: rows.length }; };
    const q = CAL.quarters[0];
    const same = CAL.milestones.find(m => m.date === q.end);
    const out = { qEnd: q.end, sameMs: same && same.name };
    if(same){ const d = AZ.shift(same.date, -3); out.same = rowsOn(d); out.sameDate = d; }
    /* The real invariant, swept rather than sampled: on NO day of the school
       year may this card print the same day-count twice. Every milestone in
       both apps happens to BE a quarter boundary, so a single "different
       milestone" case does not exist to sample — the sweep is the honest test
       and it also catches a future calendar that reintroduces the overlap. */
    out.dupeDays = [];
    for(let d = CAL.firstDay; d <= CAL.lastDay; d = AZ.shift(d,1)){
      const v = rowsOn(d).vals;
      if(new Set(v).size < v.length) out.dupeDays.push(d);
    }
    AZ.today = real;
    return out;
  });

  const ok = [];
  if(r.same){
    ok.push(['a milestone that IS the quarter end prints once',
      r.same.rows === 1 && new Set(r.same.vals).size === r.same.vals.length, r.same]);
  }
  ok.push(['no day of the school year prints the same count twice',
    r.dupeDays.length === 0, {dupes: r.dupeDays.slice(0,5), of: r.dupeDays.length}]);
  ok.forEach(([n,pass,got])=>console.log((pass?'  ok ':'FAIL ')+n+(pass?'':' → '+JSON.stringify(got))));
  console.log(' same-day card:', r.same && r.same.txt);
  const allOk = ok.length && ok.every(x=>x[1]);
  console.log(allOk?'ALL PASS':'FAILURES', '| errors:', errs.length?errs:'none');
  await b.close();
  if(!allOk || errs.length) process.exit(1);
})();
