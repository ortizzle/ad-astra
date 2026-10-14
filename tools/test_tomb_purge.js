/* A discarded library unit stays discarded, however long ago it was discarded.
   Same file in both repos.

   Sync.merge purges tombstones older than 60 days, which is right for every
   record nobody re-ships. Units ARE re-shipped: fetchLibrary merges every file
   in CONTENT_LIBRARY on each "Check the library", so once a unit's tombstone
   was purged, nothing remembered the discard and the unit came back as a draft
   in the review queue. Unit tombstones are therefore never purged.

   The unit is discovered from CONTENT_LIBRARY rather than named, so the file
   runs unchanged in both apps. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const r = await p.evaluate(async () => {
    localStorage.clear();
    const d = await (await fetch(CONTENT_LIBRARY[0], {cache:'no-store'})).json();
    const lib = Object.values(d.records).find(x => x && x.type === 'unit');
    const old = Date.now() - 70*86400000;               // ten days past the purge line
    DATA = { v: SCHEMA_VERSION, records: {} };
    DATA.records[lib.id] = { id: lib.id, type: 'unit', deleted: true, updatedAt: old };
    // A unit tombstone written before softDelete kept `type`: the id still says unit.
    const bare = 'unit-zz-legacy-tomb';
    DATA.records[bare] = { id: bare, deleted: true, updatedAt: old };
    // Ordinary progress tombstones still age out, or the store grows forever.
    DATA.records['log-old'] = { id: 'log-old', type: 'log', deleted: true, updatedAt: old };
    DATA.records['log-new'] = { id: 'log-new', type: 'log', deleted: true, updatedAt: Date.now() - 86400000 };
    saveLocal();

    // 1. A sync round trip: the merge itself must keep the unit tombstone.
    const merged = Sync.merge(DATA, { v: SCHEMA_VERSION, records: {} });
    const res = {
      id: lib.id,
      mergeKeptUnit: !!(merged.records[lib.id] && merged.records[lib.id].deleted),
      mergeKeptBare: !!(merged.records[bare] && merged.records[bare].deleted),
      mergeDroppedOldLog: !merged.records['log-old'],
      mergeKeptNewLog: !!merged.records['log-new'],
    };
    // 2. The library check that used to resurrect it. A real discard comes
    //    AFTER the file it discards, so the shipped copy is served stamped
    //    before the tombstone (an ordinary August discard, checked in October).
    //    A copy stamped after it is a deliberate re-ship, which case 3 covers.
    const realFetch = window.fetch;
    window.fetch = async (url, o) => {
      const res = await realFetch(url, o);
      if(String(url).indexOf(CONTENT_LIBRARY[0]) === -1) return res;
      const j = await res.json();
      if(j.records && j.records[lib.id]) j.records[lib.id].updatedAt = old - 7*86400000;
      return new Response(JSON.stringify(j), {status: 200, headers: {'Content-Type': 'application/json'}});
    };
    const btn = document.createElement('button'); btn.textContent = 'x';
    // Twice: under the old purge the first check only erased the tombstone,
    // and it was the NEXT check that put the unit back in the queue.
    await fetchLibrary(btn);
    await fetchLibrary(btn);
    const after = DATA.records[lib.id];
    res.stillDeleted = !!(after && after.deleted);
    res.notInQueue = !drafts().some(u => u.id === lib.id);
    res.notLive = !units().some(u => u.id === lib.id);
    window.fetch = realFetch;
    // 3. A deliberate re-ship (stamped past the discard) still comes through.
    const shipped = { ...lib, updatedAt: old + 3600e3, status: 'draft' };
    DATA = Sync.merge(DATA, { v: SCHEMA_VERSION, records: { [lib.id]: shipped } });
    res.reshipWorks = !!(DATA.records[lib.id] && !DATA.records[lib.id].deleted);
    return res;
  });

  ck('a unit tombstone older than 60 days survives the merge', r.mergeKeptUnit, r);
  ck('so does one written without a type, recognised by its unit- id', r.mergeKeptBare, r);
  ck('an old progress tombstone is still purged', r.mergeDroppedOldLog, r);
  ck('a recent progress tombstone is kept', r.mergeKeptNewLog, r);
  ck('Check the library leaves the discarded unit deleted', r.stillDeleted, r);
  ck('it does not reappear in the review queue', r.notInQueue, r);
  ck('and it does not reach her side', r.notLive, r);
  ck('a deliberate re-ship, stamped past the discard, still comes through', r.reshipWorks, r);

  out.forEach(o => console.log((o.ok ? 'PASS ' : 'FAIL ') + o.n + (o.ok ? '' : '  ' + JSON.stringify(o.got))));
  const fails = out.filter(o => !o.ok).length + errs.length;
  console.log(fails ? `${fails} FAILED` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close(); process.exit(fails ? 1 : 0);
})();
