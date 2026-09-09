/* Sync.save must fetch, merge, THEN write — and never write when the fetch
   failed (Wayfinder v158 / Ad Astra v178). Found in a full-app review: the
   pull was wrapped in a swallowing try/catch, so a failed GET fell through to
   a PATCH of the local copy over the remote — the blind overwrite the merge
   exists to prevent. fetch is mocked here; nothing leaves the page. Same file
   in both repos. */
const { chromium } = require('playwright');
const [PORT] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});
  const r = await p.evaluate(async ()=>{
    Store.set('gist_id','g1'); Store.set('gist_token','t1'); Store.set('sandbox', false);
    const calls=[]; const realFetch = window.fetch;
    const remoteNewer = { id:'sync-probe', type:'prefs2', note:'remote', updatedAt: Date.now()+1000 };
    put({ id:'sync-probe', type:'prefs2', note:'local' });   // older than the remote copy
    const mock = (getOk) => async (url, opt={}) => {
      const m = (opt.method||'GET'); calls.push(m);
      if(m==='GET') return getOk
        ? { ok:true, status:200, json: async()=>({ files:{ [Sync.filename]: { content: JSON.stringify({v:SCHEMA_VERSION, records:{ 'sync-probe': remoteNewer }}) } } }) }
        : { ok:false, status:403, json: async()=>({}) };
      return { ok:true, status:200, json: async()=>({}) };
    };
    // 1. the pull fails → save throws and NOTHING is written
    window.fetch = mock(false);
    let threw=null; try{ await Sync.save(); }catch(e){ threw=String(e.message); }
    const noPatch = !calls.includes('PATCH');
    const stillLocal = DATA.records['sync-probe'].note;
    // 2. the pull succeeds → merged (remote newer wins) and PATCHed
    calls.length=0; window.fetch = mock(true);
    let threw2=null; try{ await Sync.save(); }catch(e){ threw2=String(e.message); }
    const patched = calls.join(',');
    const merged = DATA.records['sync-probe'].note;
    window.fetch = realFetch; softDelete('sync-probe'); Store.remove('gist_id'); Store.remove('gist_token');
    return { threw, noPatch, stillLocal, threw2, patched, merged };
  });
  ck('a failed pull makes save() throw rather than proceed', /Gist fetch failed/.test(r.threw||''), r.threw);
  ck('…and NO PATCH is sent — the remote is never overwritten with the local copy', r.noPatch && r.stillLocal==='local', r);
  ck('a successful pull merges (the newer remote copy wins) and then writes', r.threw2===null && r.patched==='GET,PATCH' && r.merged==='remote', r);
  let bad=0; out.forEach(x=>{ if(!x.ok){ bad++; console.log('FAIL', x.n, '→', JSON.stringify(x.got)); } else console.log('  ok', x.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS'); console.log('errors:', errs.length?errs:'none');
  await b.close(); process.exit(bad?1:0);
})();
