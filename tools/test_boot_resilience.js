/* v218 / Wayfinder v198 — the app always comes up.
   Since v216 the app reads its data from IndexedDB before drawing anything,
   and IndexedDB on Android can hang: open() or a read never answers. A hang
   meant an app that never started. This pins the four ways out:
     1. open() hangs → boot falls back to localStorage within DB_WAIT
     2. a read hangs → same, and IndexedDB's full copy is left untouched
     3. start-up throws → a card with a Reload button, never a blank screen
     4. Refresh on the update bar asks the worker waiting NOW, not the one
        the bar was built for (two deploys close together replaced it)
   Same file in both repos; it reads the storage namespace from the page. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8411;
const base = `http://localhost:${PORT}`;
const HANG_OPEN = `(() => { const real = indexedDB.open.bind(indexedDB);
  indexedDB.open = () => ({}); })();`;
const HANG_GET = `(() => { IDBObjectStore.prototype.get = function(){ return {}; }; })();`;
(async () => {
  const b = await chromium.launch();
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});
  const errs = [];
  const watch = p => p.on('pageerror', e => errs.push(e.message));
  const state = p => p.evaluate(() => ({
    screen: (document.getElementById('screen') || {}).innerText || '',
    recs: Object.keys(DATA.records).length, ok: DataDB.ok, gaveUp: DataDB.gaveUp,
    ns: Store.ns }));

  // Seed a context with a record the way an older build left it: in localStorage.
  const ctx = await b.newContext({viewport:{width:390,height:844}});
  let p = await ctx.newPage(); watch(p);
  await p.goto(base + '/index.html', {waitUntil:'networkidle'});
  const ns = (await state(p)).ns;
  const legacy = {v:4, records:{}};
  for (let i = 0; i < 30; i++) legacy.records['log_t' + i] = {id:'log_t'+i, type:'log', mode:'cards',
    classId:'english', date:'2026-10-20', correct:0, total:0, seconds:60, xp:5, updatedAt: Date.now() - 864e5};
  await p.evaluate(([k, d]) => localStorage.setItem(k, d), [ns + 'data', JSON.stringify(legacy)]);
  await p.close();

  // 1. open() never answers.
  p = await ctx.newPage(); watch(p); await p.addInitScript(HANG_OPEN);
  const t0 = Date.now();
  await p.goto(base + '/index.html');
  await p.waitForFunction(() => document.querySelector('#screen') && document.querySelector('#screen').innerText.length > 50, null, {timeout: 9000}).catch(() => {});
  const s1 = await state(p); const took = Date.now() - t0;
  ck('1 open() hangs: the app still draws its screen', s1.screen.length > 50, s1.screen.length);
  ck('1 …within a few seconds, not never', took < 7000, took);
  ck('1 …from the localStorage copy, all 30 records', s1.recs >= 30 && !s1.ok && s1.gaveUp, s1);
  await p.evaluate(() => put({id:'log_hang', type:'log', mode:'cards', classId:'english', date:'2026-10-28', correct:0, total:0, seconds:30, xp:5}));
  const kept = await p.evaluate(k => !!(JSON.parse(localStorage.getItem(k)).records.log_hang), ns + 'data');
  ck('1 …and a change made meanwhile is saved to localStorage', kept, kept);
  await p.close();

  // A normal launch moves everything into IndexedDB and clears localStorage.
  p = await ctx.newPage(); watch(p);
  await p.goto(base + '/index.html', {waitUntil:'networkidle'}); await p.waitForTimeout(500);
  const s2 = await state(p);
  const lsLeft = await p.evaluate(k => localStorage.getItem(k), ns + 'data');
  ck('a normal launch afterwards merges the hang-session change into IndexedDB',
     s2.ok && s2.recs >= 31 && lsLeft === null, [s2.recs, s2.ok, !!lsLeft]);
  await p.close();

  // 2. A read never answers: boot falls back, and IndexedDB is not overwritten.
  p = await ctx.newPage(); watch(p); await p.addInitScript(HANG_GET);
  await p.goto(base + '/index.html');
  await p.waitForFunction(() => document.querySelector('#screen') && document.querySelector('#screen').innerText.length > 50, null, {timeout: 9000}).catch(() => {});
  const s3 = await state(p);
  ck('2 a read hangs: the app still draws its screen', s3.screen.length > 50 && s3.gaveUp && !s3.ok, s3);
  await p.evaluate(() => put({id:'log_hang2', type:'log', mode:'cards', classId:'english', date:'2026-10-28', correct:0, total:0, seconds:30, xp:5}));
  await p.waitForTimeout(300); await p.close();
  p = await ctx.newPage(); watch(p);
  await p.goto(base + '/index.html', {waitUntil:'networkidle'}); await p.waitForTimeout(500);
  const s4 = await state(p);
  const has = await p.evaluate(() => !!DATA.records.log_hang2 && !!DATA.records.log_t29);
  ck('2 …the next launch still has every record, old and new', s4.ok && s4.recs >= 32 && has, [s4.recs, has]);
  await p.close();

  // 3. Start-up throws: a card says so and offers Reload.
  p = await ctx.newPage();
  await p.addInitScript(() => { Object.defineProperty(window, 'OrtizDrive', {get(){ throw new Error('planted boot failure'); }}); });
  await p.goto(base + '/index.html', {waitUntil:'networkidle'}); await p.waitForTimeout(500);
  const card = await p.evaluate(() => {
    const s = document.getElementById('screen'); const btn = [...s.querySelectorAll('button')].find(x => /Reload/.test(x.textContent));
    return {text: s.innerText, btn: !!btn, h: btn ? btn.getBoundingClientRect().height : 0}; });
  ck('3 a start-up error shows a card instead of a blank screen', /didn’t start properly/.test(card.text) && /planted boot failure/.test(card.text), card.text.slice(0,200));
  ck('3 …with a Reload button at 44px', card.btn && card.h >= 44, card.h);
  await p.close();

  // 4. The update bar asks the worker that is waiting at the moment of the tap.
  p = await ctx.newPage(); watch(p);
  await p.goto(base + '/index.html', {waitUntil:'networkidle'});
  const sent = await p.evaluate(() => {
    const got = []; const A = {postMessage: m => got.push('A:' + m)}, B = {postMessage: m => got.push('B:' + m)};
    const reg = {waiting: A}; document.querySelectorAll('.swbar').forEach(x => x.remove());
    offerUpdate(reg); reg.waiting = B;
    [...document.querySelectorAll('.swbar button')].find(x => /Refresh/.test(x.textContent)).click();
    return got; });
  ck('4 Refresh asks the worker waiting now, not the replaced one', JSON.stringify(sent) === '["B:skip"]', sent);
  await p.close();

  out.forEach(x => console.log((x.ok ? 'ok   ' : 'FAIL ') + x.n + (x.ok ? '' : ' → ' + JSON.stringify(x.got).slice(0, 300))));
  console.log(out.every(x => x.ok) ? `all ${out.length} passed` : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0, 5) : 'none');
  await b.close();
  if (!out.every(x => x.ok) || errs.length) process.exit(1);
})();
