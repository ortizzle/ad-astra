/* DATA lives in IndexedDB, not localStorage (v216 / Wayfinder v196, both apps).
   Same file in both repos.

   Every app at ortizzle.github.io shares one ~5 MB localStorage allowance, and
   this engine's content library alone grew to half of it — the phone filled up
   and every family app started failing to save. This checks the move:
   1. data saved by an older version (in localStorage) is moved into IndexedDB
      on first launch and the localStorage copy is removed;
   2. a save survives a reload, from IndexedDB, with nothing back in localStorage;
   3. a copy left in localStorage by an old tab is merged in, not dropped;
   4. sandbox writes nothing;
   5. a large library fits even when localStorage is nearly full;
   6. a change made while the first load is still in flight survives it;
   7. the app asks Chrome once to keep its storage persistent (v217 / Wayfinder v197). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const ctx = await b.newContext({viewport:{width:390,height:844}, serviceWorkers:'block'});
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});
  const url = `http://localhost:${PORT}/index.html`;
  const ready = () => p.waitForFunction(() => typeof booted !== 'undefined' && DataDB.ok !== undefined)
    .then(() => p.evaluate(() => booted));
  const idbData = () => p.evaluate(() => DataDB.get('data'));
  const settle = () => p.waitForFunction(() => !dataWriting);

  // Start clean: no IndexedDB, no localStorage.
  await p.goto(url, {waitUntil:'networkidle'}); await ready();
  await p.evaluate(async () => { localStorage.clear(); await DataDB.put('data', null); });

  // 1. An older version's save, sitting in localStorage.
  const ns = await p.evaluate(() => Store.ns);
  await p.evaluate(ns => localStorage.setItem(ns+'data', JSON.stringify({ v:1, records:{
    'log-legacy': { id:'log-legacy', type:'log', mode:'quiz', date:'2026-10-01', correct:3, total:4, updatedAt: Date.now()-86400000 } } })), ns);
  await p.reload({waitUntil:'networkidle'}); await ready(); await settle();
  let r = await p.evaluate(ns => ({ inMemory: !!DATA.records['log-legacy'], ls: localStorage.getItem(ns+'data') }), ns);
  let d = await idbData();
  ck('1 legacy save is loaded', r.inMemory);
  ck('1 …and moved into IndexedDB', d && d.records && d.records['log-legacy']);
  ck('1 …and removed from localStorage', r.ls === null, r.ls && r.ls.slice(0,40));

  // 2. A new save survives a reload, from IndexedDB alone.
  await p.evaluate(() => put({ id:'log-new', type:'log', mode:'cards', date:'2026-10-02', correct:0, total:0 }));
  await settle();
  await p.reload({waitUntil:'networkidle'}); await ready();
  r = await p.evaluate(ns => ({ both: !!(DATA.records['log-new'] && DATA.records['log-legacy']), ls: localStorage.getItem(ns+'data') }), ns);
  ck('2 a save survives a reload', r.both);
  ck('2 nothing is written back to localStorage', r.ls === null);

  // 3. An old tab wrote to localStorage after the move: merged, newest wins per record.
  await p.evaluate(ns => localStorage.setItem(ns+'data', JSON.stringify({ v:SCHEMA_VERSION, records:{
    'log-fromtab': { id:'log-fromtab', type:'log', mode:'quiz', date:'2026-10-03', correct:1, total:1, updatedAt: Date.now() } } })), ns);
  await p.reload({waitUntil:'networkidle'}); await ready(); await settle();
  r = await p.evaluate(ns => ({ ids: Object.keys(DATA.records).filter(k => k.startsWith('log-')).sort(), ls: localStorage.getItem(ns+'data') }), ns);
  ck('3 the old tab\'s record is merged in', r.ids.includes('log-fromtab') && r.ids.includes('log-new') && r.ids.includes('log-legacy'), r.ids);
  ck('3 …and the leftover copy is cleared', r.ls === null);

  // 4. Sandbox writes nothing to either store.
  const before = JSON.stringify((await idbData()).records['log-new']);
  await p.evaluate(() => { Store.set('sandbox', true); put({ id:'log-sandbox', type:'log', mode:'quiz', date:'2026-10-04', correct:1, total:1 }); });
  await p.waitForTimeout(150);
  d = await idbData();
  ck('4 sandbox activity never reaches IndexedDB', !d.records['log-sandbox'] && JSON.stringify(d.records['log-new']) === before);
  await p.evaluate(() => setSandbox(false));
  await p.waitForFunction(() => !DATA.records['log-sandbox']);
  ck('4 leaving sandbox discards it', true);

  // 5. A library far bigger than localStorage's share still saves.
  await p.evaluate(ns => { localStorage.setItem('someotherapp_data', 'x'.repeat(4500000)); }, ns);
  await p.evaluate(() => { for(let i=0;i<40;i++) DATA.records['unit-big-'+i] = { id:'unit-big-'+i, type:'unit', status:'draft',
    title:'Big '+i, cards:[], questions:[], blob:'q'.repeat(100000), updatedAt:Date.now() }; saveLocal(); });
  await settle();
  d = await idbData();
  ck('5 a 4 MB library saves even with localStorage nearly full', d.records['unit-big-39'] && d.records['unit-big-39'].blob.length === 100000);
  await p.evaluate(() => localStorage.removeItem('someotherapp_data'));

  // 6. Records put() while the first load is still in flight are kept, not overwritten.
  r = await p.evaluate(async () => {
    dataReady = false;                       // as at boot, before the load lands
    const pending = loadLocal();
    put({ id:'log-early', type:'log', mode:'quiz', date:'2026-10-05', correct:2, total:2 });  // arrives mid-load
    await pending;
    await new Promise(res => { const t = () => dataWriting ? setTimeout(t, 20) : res(); t(); });
    return { kept: !!DATA.records['log-early'], old: !!DATA.records['log-new'], stored: !!(await DataDB.get('data')).records['log-early'] };
  });
  ck('6 a change made during the first load survives it', r.kept && r.old, r);
  ck('6 …and is written once the load lands', r.stored, r);

  // 7. Persistent storage is requested once, and not again when it's already granted.
  const asks = async granted => {
    const c = await b.newContext({serviceWorkers:'block'});
    await c.addInitScript(g => { window.__persistCalls = 0;
      Object.defineProperty(navigator, 'storage', { configurable:true, value: {
        persisted: () => Promise.resolve(g), persist: () => { window.__persistCalls++; return Promise.resolve(true); },
        estimate: () => Promise.resolve({}) } }); }, granted);
    const q = await c.newPage(); await q.goto(url, {waitUntil:'networkidle'});
    await q.waitForFunction(() => typeof booted !== 'undefined').then(() => q.evaluate(() => booted));
    await q.waitForTimeout(100);
    const n = await q.evaluate(() => window.__persistCalls); await c.close(); return n;
  };
  ck('7 asks for persistent storage when it isn\'t granted yet', (await asks(false)) === 1);
  ck('7 …and doesn\'t ask again once it is', (await asks(true)) === 0);

  ck('no page errors', errs.length === 0, errs);
  const bad = out.filter(x => !x.ok);
  out.forEach(x => console.log((x.ok ? 'ok   ' : 'FAIL ') + x.n + (x.ok ? '' : '  → ' + JSON.stringify(x.got))));
  console.log(bad.length ? `${bad.length} FAILED` : `all ${out.length} passed`);
  await b.close();
  process.exit(bad.length ? 1 : 0);
})();
