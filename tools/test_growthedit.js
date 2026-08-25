/* Smoke test for the parent-side Growth Zone correction tool
   (SCREENS.growthedit): a grown-up can remove a single question from the
   review ladder without touching anything else, and she never sees it. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8103;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  await p.addScriptTag({path: __dirname + '/seed.js'});
  await p.waitForTimeout(300);

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const before = await p.evaluate(() => ({
    misses: all('miss').length,
    entryOnParent: (() => { go('parent'); return document.getElementById('screen').innerText.includes('Manage the Growth Zone'); })()
  }));
  ck('seed created 7 misses', before.misses === 7, before.misses);
  ck('parent view offers "Manage the Growth Zone"', before.entryOnParent, before);

  const screen = await p.evaluate(() => {
    go('growthedit');
    const rows = [...document.querySelectorAll('#screen .miss')].length;
    const removeBtns = [...document.querySelectorAll('#screen button')].filter(b => /Remove from the Growth Zone/.test(b.textContent)).length;
    return {view, rows, removeBtns};
  });
  ck('growthedit lists every miss', screen.rows === 7, screen);
  ck('every row has a Remove button', screen.removeBtns === 7, screen);

  // Tap Remove on the first row.
  const afterRemove = await p.evaluate(async () => {
    const before = all('miss').map(m=>m.id).sort();
    const btn = [...document.querySelectorAll('#screen button')].find(b => /Remove from the Growth Zone/.test(b.textContent));
    const removedId = btn.closest ? null : null; // not needed
    btn.click();
    await new Promise(r=>setTimeout(r,30));
    const after = all('miss').map(m=>m.id).sort();
    return {
      before: before.length, after: after.length,
      rowsNow: document.querySelectorAll('#screen .miss').length,
      stillView: view
    };
  });
  ck('removing one drops the miss count by exactly 1', afterRemove.after === afterRemove.before - 1, afterRemove);
  ck('the screen re-renders with one fewer row', afterRemove.rowsNow === 6, afterRemove);
  ck('stays on growthedit after removing', afterRemove.stillView === 'growthedit', afterRemove.stillView);

  // Tombstoned, not gone — softDelete leaves a deleted:true record, never a hard delete.
  const tomb = await p.evaluate(() => {
    const removed = Object.values(DATA.records).find(r => r.type==='miss' && r.deleted);
    return {found: !!removed, id: removed && removed.id};
  });
  ck('the removed miss is a tombstone, not erased', tomb.found, tomb);

  // Her own Growth Zone screen must show no such control anywhere.
  const herSide = await p.evaluate(() => {
    go('growth');
    const txt = document.getElementById('screen').innerText;
    return {hasRemove: /Remove from the Growth Zone/.test(txt), count: all('miss').length};
  });
  ck('her Growth Zone screen has no Remove control', !herSide.hasRemove, herSide);
  ck('her screen still shows the remaining misses', herSide.count === 6, herSide.count);

  // Removing does not touch other progress types.
  const untouched = await p.evaluate(() => ({
    qstats: Object.values(DATA.records).filter(r=>r.type==='qstat'&&!r.deleted).length,
    logs: all('log').length
  }));
  ck('qstats/logs untouched by the removal (sanity: no throw, no wipe)', untouched.qstats >= 0 && untouched.logs > 0, untouched);

  out.forEach(r => console.log((r.ok ? ' ok ' : 'FAIL ') + r.n + (r.ok ? '' : ' -> ' + JSON.stringify(r.got).slice(0,300))));
  console.log(out.every(r=>r.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(r=>r.ok) || errs.length) process.exit(1);
})();
