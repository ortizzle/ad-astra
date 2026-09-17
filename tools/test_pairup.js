/* Pair up — matching that COUNTS, built on the lesson's own questions.
   The whole point of the feature is the crediting, so most of this file is
   about what lands in DATA.records after a tap, not about what renders.
   Same file in both repos. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8201;
(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});
  const out = []; const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    for (const f of CONTENT_LIBRARY) { try { const j = await (await fetch(f,{cache:'no-store'})).json();
      Object.values(j.records||{}).forEach(r => { if (r.type==='unit') { r.status='approved'; delete r.releaseOn; DATA.records[r.id]=r; } }); } catch(e){} }
    saveLocal();
    const units = all('unit');
    const rich = units.filter(u => pairPool(u).length >= 4);
    const thin = units.filter(u => u.questions && pairPool(u).length > 0 && pairPool(u).length < 4);
    /* Every SUBJECT should have at least one board — the claim this game
       makes is that it works on the library as it already stands, with no
       content authored for it, so per-subject coverage is the real check. */
    const subjects = [...new Set(units.map(u => u.classId))];
    const covered = subjects.filter(c => rich.some(u => u.classId === c));
    const u = rich.find(x => pairPool(x).length >= 7) || rich[0];
    return {id:u.id, cls:u.classId, title:u.title, pool:pairPool(u).length,
            rich:rich.length, thinId: thin[0] ? thin[0].id : null,
            subjects: subjects.length, covered: covered.length,
            gaps: subjects.filter(c => !covered.includes(c))};
  });
  ck('the library has boards to deal, with no content authored for them', seed.rich >= 10, {rich: seed.rich});
  ck('every subject with units has at least one board, with nothing authored for it',
     seed.covered === seed.subjects, {subjects: seed.subjects, covered: seed.covered, gaps: seed.gaps});

  /* Eligibility: the pool is mc/analogy only, deduped by answer text — two
     identical right-hand tiles would make a pairing genuinely ambiguous. */
  const pool = await p.evaluate(({id}) => {
    const u = DATA.records[id], ps = pairPool(u);
    const txt = ps.map(q => String(q.opts[q.ans]).trim().toLowerCase());
    // a unit carrying a non-pairable kind, to prove they are filtered
    const odd = all('unit').find(x => (x.questions||[]).some(q => q.kind && q.kind!=='mc' && q.kind!=='analogy'));
    const oddLeft = odd ? pairPool(odd).filter(q => q.kind && q.kind!=='mc' && q.kind!=='analogy').length : 0;
    return {dupes: txt.length - new Set(txt).size, kinds: [...new Set(ps.map(q=>q.kind||'mc'))], oddLeft, oddId: odd && odd.id};
  }, seed);
  ck('no two prompts on a board can share an answer, and only mc/analogy are pairable',
     pool.dupes === 0 && pool.kinds.every(k => k==='mc'||k==='analogy') && pool.oddLeft === 0, pool);

  const door = await p.evaluate(({id, cls, thinId}) => {
    const u = DATA.records[id], c = CLASS_BY_ID[cls];
    const onCard = /🃏  Pair up/.test(unitCard(u, c).textContent);
    let onThin = null;
    if (thinId) { const t = DATA.records[thinId]; onThin = /🃏  Pair up/.test(unitCard(t, CLASS_BY_ID[t.classId]).textContent); }
    return {onCard, onThin};
  }, seed);
  ck('the door renders on a unit with a board and not on one without',
     door.onCard && door.onThin !== true, door);

  const deal = await p.evaluate(({id, cls}) => {
    pairState = null; go('pairup',{unitId:id, classId:cls});
    const sc = document.getElementById('screen');
    const st = pairState;
    const promptIds = st.lefts.map(x => x.q.id);
    const decoys = st.rights.filter(r => r.decoy);
    return {lefts: st.lefts.length, rights: st.rights.length, decoys: decoys.length,
            decoyOrphan: decoys.every(d => d.qid === null),
            tilesL: sc.querySelectorAll('.paircol .pairtile:not(.ans)').length,
            tilesR: sc.querySelectorAll('.paircol .pairtile.ans').length,
            minH: Math.min(...[...sc.querySelectorAll('.pairtile')].map(e=>e.getBoundingClientRect().height)),
            overflow: document.documentElement.scrollWidth <= 390,
            rightsMatch: st.rights.filter(r => r.qid).every(r => promptIds.includes(r.qid))};
  }, seed);
  ck('the board deals five prompts, seven answers, and the two extras belong to nothing on it',
     deal.lefts === 5 && deal.rights === 7 && deal.decoys === 2 && deal.decoyOrphan && deal.rightsMatch, deal);
  ck('every tile renders, is at least 44px tall, and nothing overflows the phone',
     deal.tilesL === 5 && deal.tilesR === 7 && deal.minH >= 44 && deal.overflow, deal);

  /* THE POINT: a first-time-right pairing is credited exactly as a quiz
     answer — the tally, the plain count that finishes the lesson, and XP. */
  const hit = await p.evaluate(() => {
    const st = pairState, L = st.lefts[0];
    const key = 'qstat_'+st.unitId+'_'+L.q.id;
    const before = DATA.records[key];
    const sc = document.getElementById('screen');
    [...sc.querySelectorAll('.pairtile:not(.ans)')][0].click();
    const rTile = [...document.querySelectorAll('#screen .pairtile.ans')]
      .find(b => b.textContent.trim() === String(L.q.opts[L.q.ans]).trim());
    rTile.click();
    const q = DATA.records[key];
    const log = all('log').find(l => l.mode==='pair');
    return {qid: L.q.id,
            attempts: q.attempts, correct: q.correct, plain: q.plain,
            grew: q.attempts === ((before?.attempts)||0)+1,
            plainGrew: q.plain === qstatPlain(before)+1,
            miss: !!DATA.records['miss_'+st.unitId+'_'+L.q.id],
            met: st.met, xp: st.xp,
            log: log && {mode: log.mode, correct: log.correct, total: log.total, xp: log.xp, label: modeLabel(log)},
            note: document.querySelector('#screen .pairnote.ok') ? document.querySelector('#screen .pairnote').textContent : null};
  });
  ck('a right pairing writes a real qstat, increments plain, and writes no miss',
     hit.grew && hit.correct >= 1 && hit.plainGrew && !hit.miss, hit);
  ck('it earns XP and logs one session in place, named for the day view',
     hit.met === 1 && hit.xp === 10 && hit.log && hit.log.mode === 'pair' && hit.log.correct === 1
     && hit.log.total === 5 && hit.log.xp === 10 && hit.log.label === 'Pair up', hit);
  ck('the explanation is said in plain words, with no ** markers left on screen',
     hit.note && !/\*\*/.test(hit.note), {note: hit.note});

  /* A wrong pairing is a real Growth Zone miss — box 0, back tomorrow. */
  const missed = await p.evaluate(() => {
    const st = pairState, L = st.lefts.find(x => !x.done);
    const key = 'qstat_'+st.unitId+'_'+L.q.id, mkey = 'miss_'+st.unitId+'_'+L.q.id;
    const beforeA = (DATA.records[key]?.attempts)||0;
    const sc = document.getElementById('screen');
    [...sc.querySelectorAll('.pairtile:not(.ans)')].find(b => !b.disabled && b.textContent.includes(L.q.q.slice(0,20))).click();
    const wrong = [...document.querySelectorAll('#screen .pairtile.ans')]
      .find(b => !b.disabled && b.textContent.trim() !== String(L.q.opts[L.q.ans]).trim());
    wrong.click();
    const m = DATA.records[mkey], q = DATA.records[key];
    return {qid: L.q.id, box: m && m.box, due: m && m.due, tomorrow: AZ.shift(AZ.today(),1),
            right: m && m.right, chose: m && m.chose, why: m && m.why,
            attempts: q.attempts, grew: q.attempts === beforeA+1, correctSame: q.correct === ((DATA.records[key]?.correct)||0),
            gzN: pairState.gzN, xp: pairState.xp, met: pairState.met,
            due2: dueMisses().some(x => x.qid === L.q.id)};
  });
  ck('a wrong pairing lands the question on the review ladder at box 0, due tomorrow',
     missed.box === 0 && missed.due === missed.tomorrow && missed.grew && !!missed.right, missed);
  ck('it earns nothing, and the Growth Zone counts it',
     missed.gzN === 1 && missed.xp === 10 && missed.met === 1, missed);

  /* One miss per prompt per board: a second wrong guess at the same question
     would reset a box she has not been re-tested on. */
  const again = await p.evaluate(({qid}) => {
    const st = pairState, L = st.lefts.find(x => x.q.id === qid);
    const key = 'qstat_'+st.unitId+'_'+qid;
    const beforeA = DATA.records[key].attempts, beforeM = DATA.records['miss_'+st.unitId+'_'+qid].updatedAt;
    const sc = document.getElementById('screen');
    [...sc.querySelectorAll('.pairtile:not(.ans)')].find(b => !b.disabled && b.textContent.includes(L.q.q.slice(0,20))).click();
    const wrong = [...document.querySelectorAll('#screen .pairtile.ans')]
      .find(b => !b.disabled && b.textContent.trim() !== String(L.q.opts[L.q.ans]).trim());
    wrong.click();
    return {attemptsSame: DATA.records[key].attempts === beforeA,
            missSame: DATA.records['miss_'+st.unitId+'_'+qid].updatedAt === beforeM,
            gzN: pairState.gzN};
  }, {qid: missed.qid});
  ck('a second wrong guess at the same prompt records nothing new',
     again.attemptsSame && again.missSame && again.gzN === 1, again);

  /* And pairing it correctly afterwards must NOT undo the miss she just made. */
  const recover = await p.evaluate(({qid}) => {
    const st = pairState, L = st.lefts.find(x => x.q.id === qid);
    const key = 'qstat_'+st.unitId+'_'+qid;
    const beforeC = DATA.records[key].correct, beforeXp = st.xp;
    const sc = document.getElementById('screen');
    [...sc.querySelectorAll('.pairtile:not(.ans)')].find(b => !b.disabled && b.textContent.includes(L.q.q.slice(0,20))).click();
    [...document.querySelectorAll('#screen .pairtile.ans')]
      .find(b => !b.disabled && b.textContent.trim() === String(L.q.opts[L.q.ans]).trim()).click();
    return {paired: L.done, correctSame: DATA.records[key].correct === beforeC,
            stillDue: !!DATA.records['miss_'+st.unitId+'_'+qid] && !DATA.records['miss_'+st.unitId+'_'+qid].deleted,
            xpSame: st.xp === beforeXp, met: st.met};
  }, {qid: missed.qid});
  ck('finding it after missing it clears the tile but keeps it on the ladder',
     recover.paired && recover.correctSame && recover.stillDue && recover.xpSame && recover.met === 1, recover);

  /* Finish the board: the completion bonus is scaled so a 5-pair board cannot
     out-earn a 5-question quiz round. */
  const fin = await p.evaluate(() => {
    let guard = 40;
    while (pairState.lefts.some(x => !x.done) && guard--) {
      const L = pairState.lefts.find(x => !x.done);
      const sc = document.getElementById('screen');
      [...sc.querySelectorAll('.pairtile:not(.ans)')].find(b => !b.disabled && b.textContent.includes(L.q.q.slice(0,20))).click();
      [...document.querySelectorAll('#screen .pairtile.ans')]
        .find(b => !b.disabled && b.textContent.trim() === String(L.q.opts[L.q.ans]).trim()).click();
    }
    const st = pairState;
    const logs = all('log').filter(l => l.mode==='pair');
    const sc = document.getElementById('screen');
    return {met: st.met, xp: st.xp, logs: logs.length, logXp: logs[0].xp,
            text: sc.textContent.includes('Round done'),
            again: !!([...sc.querySelectorAll('button')].find(b => /Deal another board/.test(b.textContent)))};
  });
  /* 4 of 5 first time = 40 XP + the 80% bonus (25). */
  ck('finishing pays per pair plus a scaled completion bonus, in ONE log updated in place',
     fin.met === 4 && fin.xp === 40 + 25 && fin.logs === 1 && fin.logXp === fin.xp, fin);
  ck('the finish card says so and offers another board', fin.text && fin.again, fin);

  /* The lesson itself moved — the reason this game exists rather than Match. */
  const moved = await p.evaluate(({id, cls}) => {
    const u = DATA.records[id];
    const qp = quizProgress(u);
    const anyPlain = (u.questions||[]).filter(q => qstatPlain(DATA.records['qstat_'+u.id+'_'+q.id]) > 0).length;
    return {met: qp.met, anyPlain, total: qp.total};
  }, seed);
  ck('the lesson door and the topic map now count those questions as met',
     moved.met >= 5 && moved.anyPlain >= 5, moved);

  ck('no page errors', errs.length === 0, errs.slice(0,3));

  await b.close();
  out.forEach(r => console.log((r.ok?'  ok  ':'  FAIL') + '  ' + r.n + (r.ok?'':'  ' + JSON.stringify(r.got))));
  const bad = out.filter(r => !r.ok).length;
  console.log(bad ? `\n${bad} FAILED of ${out.length}` : `\nALL PASS (${out.length})`);
  process.exit(bad ? 1 : 0);
})();
