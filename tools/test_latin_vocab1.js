/* Latin I · Vocabulary Quiz 1 (content/latin-vocab-1.json, v202).

   Pins COVERAGE of the fifteen-word list rather than question ids: every
   word on the list has a card that leads with its meaning, carries a
   hand-authored respelling, and is asked about somewhere. Also pins the trap
   the list sets (agricola is masculine), her two margin notes reaching the
   cards, the derivative hooks flagged as ours, and the questions-not-scoring
   rule (v198) on an upload with her name on it.

   Verified by deleting the multus card, flipping the agricola-magnus answer
   to the feminine form, and prepending a made-up score to the parent note:
   seven assertions failed, and only those three causes — the missing card
   fails all five that count or read the deck, the other two fail one each. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8402;
const UID = 'unit-latin-vocab1';

(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`,{waitUntil:'domcontentloaded'});
  await p.addScriptTag({path:__dirname+'/seed.js'}); await p.waitForTimeout(300);
  const out=[]; const ck=(n,ok,got)=>out.push({n,ok:!!ok,got});

  const seeded = await p.evaluate(async ()=>{
    const files = CONTENT_LIBRARY.filter(f=>/latin-/.test(f));
    for(const f of files){
      const j = await (await fetch(f,{cache:'no-store'})).json();
      Object.values(j.records).forEach(r=>{ if(r&&r.type){ r.status='approved'; delete r.releaseOn; put(r); } });
    }
    saveLocal();
    const u = DATA.records['unit-latin-vocab1'];
    return u ? { files:files.length, classId:u.classId, prep:!!u.prep, libv:u.libv, cards:u.cards.length, qs:u.questions.length } : null;
  });
  if(!seeded){ console.log('FAIL unit not in CONTENT_LIBRARY'); process.exit(1); }
  ck('classId is "latin" (the v136 orphan trap), prep set, libv present', seeded.classId==='latin' && seeded.prep && seeded.libv>=1, seeded);
  ck('at least 15 cards and 20 questions (a minimum, never an exact count)', seeded.cards>=15 && seeded.qs>=20, seeded);

  // ---- every word on the list: a card, its meaning first, a respelling, and asked somewhere
  const LIST = { agricola:'farmer', amicus:'friend', amo:'to love', audio:'to hear', deus:'god', donum:'gift',
                 do:'to give', magnus:'great', multus:'many', '-ne':'yes/no question', sed:'but',
                 puella:'girl', puer:'boy', non:'not', video:'to see' };
  const cov = await p.evaluate((LIST)=>{
    const u = DATA.records['unit-latin-vocab1'];
    const qs = u.questions.map(q=>JSON.stringify([q.q,q.opts[q.ans]])).join(' ').toLowerCase();
    return Object.entries(LIST).map(([w,en])=>{
      const c = u.cards.find(c=>c.term.split(' ')[0]===w);
      return { w, card:!!c, lead: !!c && c.def.startsWith('**') && c.def.toLowerCase().split('**')[1].includes(en),
               sp: !!c && !!c.sp && /^[a-z -]+$/i.test(c.sp),
               asked: qs.includes(w.replace('-','')) };
    });
  }, LIST);
  ck('every one of the fifteen words has a card', cov.every(x=>x.card), cov.filter(x=>!x.card));
  ck('each card leads, in bold, with the meaning the list gives', cov.every(x=>x.lead), cov.filter(x=>!x.lead));
  ck('each card carries a respelling', cov.every(x=>x.sp), cov.filter(x=>!x.sp));
  ck('every word is asked about in at least one question', cov.every(x=>x.asked), cov.filter(x=>!x.asked));

  // ---- the trap, the notes, the provenance
  const t = await p.evaluate(()=>{
    const u = DATA.records['unit-latin-vocab1'];
    const card = w => u.cards.find(c=>c.term===w);
    const gq = u.questions.find(q=>/the great farmer/.test(q.q));
    const derivs = u.questions.filter(q=>/comes from|English word|audience/i.test(q.q));
    return { trapAns: gq && gq.opts[gq.ans], trapCard: /MASCULINE/.test(card('agricola').def),
             amica: /amica/.test(card('amicus').def), big: /big/.test(card('magnus').def),
             derivAdded: derivs.length>=3 && derivs.every(q=>q.from==='added'),
             spell: u.questions.filter(q=>q.kind==='spell').map(q=>q.opts[0]),
             noMacronSpell: u.questions.filter(q=>q.kind==='spell').every(q=>/^[a-z]+$/.test(q.opts[0])),
             noteAgricola: /agricola is masculine/.test(u.parentNote.text) };
  });
  ck('the agricola trap: "the great farmer" is agricola magnus, and the card says MASCULINE', t.trapAns==='agricola magnus' && t.trapCard, t);
  ck('her two margin notes reach the cards (amica, big)', t.amica && t.big, t);
  ck('the derivative questions are flagged added, not source', t.derivAdded, t);
  ck('spelling questions use plain letters only (no macron to type)', t.spell.length>=3 && t.noMacronSpell, t.spell);
  ck('the parent note names the agricola trap', t.noteAgricola, t.noteAgricola);

  // ---- structure: answers spread, four unique options, no back-references or positional ones
  const st = await p.evaluate(()=>{
    const u = DATA.records['unit-latin-vocab1'];
    const mc = u.questions.filter(q=>(q.kind||'mc')==='mc');
    const slots = [0,0,0,0]; mc.forEach(q=>slots[q.ans]++);
    return { slots, uniq: mc.every(q=>q.opts.length===4 && new Set(q.opts).size===4),
             back: u.questions.filter(q=>/^(the same|that same|for that|using the same)/i.test(q.q)).map(q=>q.id),
             pos: u.questions.filter(q=>/of the above|(first|second|last) option/i.test(JSON.stringify(q))).map(q=>q.id) };
  });
  ck('correct answers spread across all four slots (the v181 _balance bug)', st.slots.every(n=>n>0), st.slots);
  ck('every MC question has four unique options', st.uniq, st.uniq);
  ck('no back-references and no positional references', !st.back.length && !st.pos.length, st);

  // ---- shelf: on Latin I with the other two, gold, not loose
  const shelf = await p.evaluate((UID)=>{
    go('shelf', {classId:'latin', series:'Latin I', open:UID});
    const stops = [...document.querySelectorAll('#screen .stop')].map(s=>({t:s.querySelector('.t').textContent, prep:s.classList.contains('prep')}));
    const oc = document.getElementById('shelfopen');
    return { stops, loose: shelvesFor('latin').loose.some(u=>u.id===UID), band: !!oc && !!oc.querySelector('.prepband') };
  }, UID);
  const i = shelf.stops.findIndex(s=>/Vocabulary Quiz 1/.test(s.t));
  ck('it shelves on Latin I beside the other two parts, not loose', i>=0 && shelf.stops.length>=3 && !shelf.loose, shelf.stops.map(s=>s.t));
  ck('its stop is gold-ringed and the open card wears the prep band', shelf.stops[i] && shelf.stops[i].prep && shelf.band, shelf);

  // ---- play: a full round, a spelling question typed in capitals, the deck
  const play = await p.evaluate(async ()=>{
    const u = DATA.records['unit-latin-vocab1'];
    const spq = u.questions.map((x,i)=>x.kind==='spell'?i:-1).filter(i=>i>=0);
    quizState = null;
    go('quiz', {unitId:u.id, classId:'latin'});
    // steer the round it built so a spelling question is in it
    if(!quizState.order.some(i=>spq.includes(i))){ quizState.order[0] = spq[0]; render(); }
    let guard=0, typed=null;
    while(view==='quiz' && guard++<90){
      const inp = document.querySelector('#screen input[type=text]');
      if(inp && quizState.answered===null){
        const q = u.questions[quizState.order[quizState.i]];
        inp.value = q.opts[0].toUpperCase(); inp.dispatchEvent(new Event('input'));
        const chk = document.querySelector('#screen .btn-primary'); chk.click();
        typed = {word:q.opts[0], right: quizState.answered===q.ans};
        await new Promise(r=>setTimeout(r,8)); continue;
      }
      const opts=[...document.querySelectorAll('#screen .opt:not([disabled])')];
      if(opts.length) for(const o of opts){ o.click(); await new Promise(r=>setTimeout(r,4)); }
      await new Promise(r=>setTimeout(r,8));
      const next=document.querySelector('#screen .btn-primary, #screen .explain.go-on');
      if(next){ next.click(); await new Promise(r=>setTimeout(r,8)); continue; }
      if(!opts.length) break;
    }
    document.querySelectorAll('.modal-back, .modal').forEach(m=>m.remove());
    const l = all('log').find(x=>x.unitId===u.id && x.mode==='quiz');
    go('cards', {unitId:u.id, classId:'latin'});
    const deck = cardState && cardState.order ? cardState.order.length : 0;
    return { logged: !!l, total: l && l.total, typed, deck, saidas: !!document.querySelector('#screen .saidas') };
  });
  ck('a spelling question typed in CAPITALS is accepted', play.typed && play.typed.right, play.typed);
  ck('a full five-question round plays through and logs', play.logged && play.total===5, play);
  ck('the 15-card deck opens and shows a respelling', play.deck>=15 && play.saidas, play);

  // ---- v198: read for questions, never marked; no name anywhere
  const priv = await p.evaluate((UID)=>{
    const whole = JSON.stringify(DATA.records[UID]);
    return { names: /Ortiz|Sedona/i.test(whole),
             marks: /she (got|wrote|put|answered)|\bscored\b|\d+\s*out of\s*\d+|she was marked/i.test(whole),
             readNote: /read for what it asks only/.test(DATA.records[UID].parentNote.text) };
  }, UID);
  ck('no name and no mark in the shipped record, and the note says it was read for what it asks', !priv.names && !priv.marks && priv.readNote, priv);

  let bad=0;
  out.forEach(r=>{ if(!r.ok){ bad++; console.log('FAIL', r.n, '→', JSON.stringify(r.got).slice(0,400)); }
                   else console.log('  ok', r.n); });
  console.log(bad ? `${bad} FAILURES` : 'ALL PASS');
  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  process.exit(bad ? 1 : 0);
})();
