/* The word list — everything in a deck on one screen.

   Chris asked for it first for Wordly Wise ("can we figure out a way to
   include the complete word list?"), then, having lived with it: "I like
   seeing the flashcard words listed out as an option. Can we do that for
   all sections of flashcards?" So it now covers every deck, not just the
   fourteen vocabulary lessons.

   What this file pins is mostly WHO GETS THE DOOR and WHAT IT CLAIMS,
   because the narrow gate existed for a label that lied: "all 6 words" on
   an eighteen-card Biology deck. The count and the noun are both read off
   what actually prints now, so the assertions go after exactly that — and
   after the rule that matters most, which is that a list of meanings must
   never reach the quiz's own tool row, where it would be the answer key.

   Same file, both apps. The units are DISCOVERED from the shipped library
   rather than named in argv: the two libraries use different ids, and a
   hardcoded one is the harness rot this repo keeps paying for. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8104;

(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(async () => {
    /* The real files rather than fetchLibrary(), which reaches for the
       parent screen's own toast nodes and is not callable headless. */
    for(const path of CONTENT_LIBRARY){
      try{ const j = await (await fetch(path)).json();
        Object.values(j.records).forEach(r=>{ if(r && r.type){ r.status='approved'; delete r.releaseOn; put(r); } });
      }catch(e){}
    }
    saveLocal();
    const units = Object.values(DATA.records)
      .filter(r=>r.type==='unit' && !r.deleted && !r.own)
      .sort((a,b)=>a.title<b.title?-1:1);
    const pack = u => u && ({id:u.id, cid:u.classId, title:u.title,
      n: wordListCards(u).length, cards: u.cards.length, noun: wordListNoun(u),
      terms: wordListCards(u).map(c=>c.term),
      leads: wordListCards(u).map(c=>String(c.def).split('\n')[0].trim())});
    return {
      /* A vocabulary deck (every entry one word) and an ordinary lesson
         deck (some entry is a phrase) — the two labels have to be right
         on both, and only the first one is what v191 shipped for. */
      word: pack(units.find(u=>hasWordList(u) && wordListNoun(u)==='word')),
      term: pack(units.find(u=>hasWordList(u) && wordListNoun(u)==='term')),
      /* The claim the widening makes: it needed nothing authored, so every
         subject that has lessons at all should now have a list. */
      subjects: STUDY_CLASSES.map(c=>{
        const mine = units.filter(u=>u.classId===c.id);
        return {id:c.id, lessons:mine.length, withList:mine.filter(hasWordList).length};
      }),
      coverage: units.length ? units.filter(hasWordList).length / units.length : 0
    };
  });
  if(!seed.word || !seed.term){
    console.log('FAIL library has no ' + (!seed.word ? 'word' : 'term') + '-list deck to test against');
    process.exit(1);
  }
  ck('a real shipped vocabulary lesson qualifies, and so does an ordinary lesson',
     seed.word.n >= 3 && seed.term.n >= 3,
     {word: seed.word.title + ' · ' + seed.word.n, term: seed.term.title + ' · ' + seed.term.n});
  /* The point of the change: it is not a vocabulary feature any more. */
  ck('nearly every shipped deck has one now, not just the vocabulary lessons',
     seed.coverage > 0.8, Math.round(seed.coverage*100) + '% of decks');
  ck('every subject with lessons has at least one — nothing was authored for this',
     seed.subjects.filter(s=>s.lessons && !s.withList).length === 0,
     seed.subjects.filter(s=>s.lessons && !s.withList));

  const doorOf = (U) => p.evaluate((UNIT) => {
    document.querySelectorAll('.probecard').forEach(n=>n.remove());
    const u = unitFor(UNIT), c = CLASS_BY_ID[u.classId];
    const card = unitCard(u, c); card.classList.add('probecard');
    document.body.appendChild(card);
    const btn = [...card.querySelectorAll('button')].find(x=>/ list — all /.test(x.textContent));
    const r = btn && btn.getBoundingClientRect();
    /* The door sits in Practice, and BEFORE the flashcard tile — the list is
       what you read before you drill, the way the book prints it. */
    const kids = [...card.children];
    const secs = kids.map(k=>k.className);
    return {label: btn ? btn.textContent : null, h: btn ? Math.round(r.height) : 0,
            beforeTiles: btn ? kids.indexOf(btn) < kids.findIndex(k=>k.classList.contains('mrow')) : false,
            afterPractice: btn ? kids.indexOf(btn) > secs.indexOf('seclab') : false};
  }, U.id);

  const dw = await doorOf(seed.word);
  ck('a vocabulary lesson\'s door says WORDS, and how many',
     dw.label === '📖  Word list — all ' + seed.word.n + ' words'
       + 'Every word in this lesson, meanings hidden until you tap', dw);
  ck('it is a real tap target', dw.h >= 44, dw);
  ck('it sits under Practice, ahead of the drill tiles',
     dw.afterPractice && dw.beforeTiles, dw);

  const dt = await doorOf(seed.term);
  ck('an ordinary lesson\'s door says TERMS — "words" would be the wrong noun',
     dt.label === '📖  Term list — all ' + seed.term.n + ' terms'
       + 'Every term in this lesson, meanings hidden until you tap',
     {got: dt.label, on: seed.term.title});
  ck('and it is a real tap target too', dt.h >= 44, dt);

  const open = await p.evaluate((UNIT) => {
    openWordList(unitFor(UNIT));
    const box = document.querySelector('.modal-box');
    const rows = [...box.querySelectorAll('.wlrow')];
    return {
      words: rows.map(r=>r.querySelector('.wlw').textContent),
      sp:    rows.map(r=>r.querySelector('.wlsp') ? r.querySelector('.wlsp').textContent : null),
      /* Measured, not read off the flag: `hidden` is a property and
         `display:block` silently beats the UA rule that honours it. */
      hidden: rows.every(r=>{ const d=r.querySelector('.wld');
        return d.hidden && getComputedStyle(d).display === 'none' && d.offsetHeight === 0; }),
      minH: Math.min(...rows.map(r=>Math.round(r.getBoundingClientRect().height))),
      title: box.querySelector('h3').textContent,
      note: box.querySelector('.wlnote').textContent,
      names: box.textContent.includes(unitFor(UNIT).title)
    };
  }, seed.word.id);
  ck('every word in the lesson is listed, in the deck\'s own order',
     JSON.stringify(open.words) === JSON.stringify(seed.word.terms), {got:open.words, want:seed.word.terms});
  ck('it names which lesson it is', /Word list/.test(open.title) && open.names, open.title);
  ck('the note counts exactly what is printed',
     open.note.indexOf(seed.word.n + ' words') === 0, open.note);
  ck('each word shows how to say it', open.sp.filter(Boolean).length === seed.word.terms.length, open.sp);
  ck('no meaning is given away before she asks', open.hidden, open.hidden);
  ck('every row is a real tap target even folded', open.minH >= 44, open.minH);

  const one = await p.evaluate(() => {
    const rows = [...document.querySelectorAll('.modal-box .wlrow')];
    rows[2].click();
    const vis = r => { const d=r.querySelector('.wld');
      return !d.hidden && getComputedStyle(d).display !== 'none' && d.offsetHeight > 0; };
    return {shown: vis(rows[2]),
            text: rows[2].querySelector('.wld').textContent,
            othersStillHidden: rows.filter((r,i)=>i!==2).every(r=>!vis(r)),
            aria: rows[2].getAttribute('aria-expanded')};
  });
  ck('tapping one word reveals its meaning', one.shown && one.text.length > 5, one);
  ck('and only that one — she can check a word without spoiling the rest',
     one.othersStillHidden, one);
  ck('the row reports its state to a screen reader', one.aria === 'true', one);
  ck('the meaning is the card\'s own bold lead, not a rewritten copy',
     seed.word.leads[2].replace(/\*\*/g,'') === one.text.trim(), {got:one.text, want:seed.word.leads[2]});

  const all = await p.evaluate(() => {
    const box = document.querySelector('.modal-box');
    const btn = [...box.querySelectorAll('button')].find(x=>/meaning/i.test(x.textContent));
    btn.click();
    const seen = d => !d.hidden && getComputedStyle(d).display !== 'none' && d.offsetHeight > 0;
    const shownAll = [...box.querySelectorAll('.wlrow .wld')].every(seen);
    const lbl = btn.textContent;
    btn.click();
    return {shownAll, lbl, hiddenAgain: [...box.querySelectorAll('.wlrow .wld')].every(d=>!seen(d)),
            lbl2: btn.textContent};
  });
  ck('"Show every meaning" opens the whole list', all.shownAll, all);
  ck('and flips to Hide, so it closes again', /Hide/.test(all.lbl) && all.hiddenAgain, all);
  ck('the label resets', /Show/.test(all.lbl2), all.lbl2);

  /* The ordinary lesson opens the same way, under the right title, with its
     phrases intact — a multi-word term is exactly what the old gate refused. */
  const openT = await p.evaluate((UNIT) => {
    document.querySelector('.modal-overlay')?.remove();
    openWordList(unitFor(UNIT));
    const box = document.querySelector('.modal-box');
    const rows = [...box.querySelectorAll('.wlrow')];
    return {title: box.querySelector('h3').textContent,
            note: box.querySelector('.wlnote').textContent,
            words: rows.map(r=>r.querySelector('.wlw').textContent),
            hidden: rows.every(r=>getComputedStyle(r.querySelector('.wld')).display === 'none')};
  }, seed.term.id);
  ck('an ordinary lesson\'s list opens as a TERM list', /Term list/.test(openT.title)
     && openT.note.indexOf(seed.term.n + ' terms') === 0, openT);
  ck('and prints every one of its terms, phrases and all',
     JSON.stringify(openT.words) === JSON.stringify(seed.term.terms),
     {got:openT.words.slice(0,4), want:seed.term.terms.slice(0,4)});
  ck('with the meanings still covered', openT.hidden, openT);

  /* THE RULE, and widening the gate widened the hazard: a list of meanings
     reachable during that lesson's own quiz is the answer key — so the quiz
     must not offer it, unlike the Sheet and Map doors that deliberately do
     live in the tool row. Checked on the ordinary lesson too, because it is
     the one that was never covered before. */
  for(const U of [seed.word, seed.term]){
    const quiz = await p.evaluate((UNIT) => {
      document.querySelector('.modal-overlay')?.remove();
      document.querySelectorAll('.probecard').forEach(n=>n.remove());
      const u = unitFor(UNIT);
      quizState = null;
      go('quiz', {unitId:u.id, classId:u.classId});
      const scr = document.getElementById('screen');
      const tools = [...scr.querySelectorAll('.tool, .tools button')].map(x=>x.textContent.trim());
      return {tools, any: /word list|term list/i.test(scr.textContent)};
    }, U.id);
    ck('the quiz never offers the list in its tool row (' + U.noun + ' deck)',
       !quiz.tools.some(t=>/word|term list/i.test(t)), quiz.tools);
    ck('and it appears nowhere on that quiz screen at all (' + U.noun + ' deck)',
       !quiz.any, quiz.tools);
  }

  /* Who gets the door. Every deck does now — the widening — but the label
     has to stay true by construction, so the noun and the count are read
     off what prints. A Spelling Bee deck is all single words and is still
     excluded, because that unit's whole design is announcing a word it
     never shows. */
  const gate = await p.evaluate(() => {
    document.querySelector('.modal-overlay')?.remove();
    const cid = STUDY_CLASSES[0].id;
    const mk = (id, cards, extra) => Object.assign({id, type:'unit', classId:cid,
      status:'approved', title:id, updatedAt:Date.now(), cards, questions:[]}, extra||{});
    const word = n => ({id:'c'+n, term:'word'+n, def:'**A meaning.** (noun)'});
    const phrase = n => ({id:'p'+n, term:'Adding whole numbers '+n, def:'**A meaning.**'});
    const ponder = n => ({id:'z'+n, term:'Ponder: what do you reckon '+n, def:'**Think about it.**'});
    const six = [1,2,3,4,5,6].map(word);
    const lbl = u => { document.querySelectorAll('.probecard').forEach(n=>n.remove());
      const card = unitCard(u, CLASS_BY_ID[cid]); card.classList.add('probecard');
      document.body.appendChild(card);
      const btn = [...card.querySelectorAll('button')].find(x=>/ list — all /.test(x.textContent));
      /* .btnstack wraps the label span AND the <small> caption, so reach
         past it for the label alone. */
      return btn ? btn.querySelector('.btnstack span').textContent : null; };
    return {
      allWords:  lbl(mk('wl-all',  six)),
      mixed:     lbl(mk('wl-mix',  six.concat([phrase(1), phrase(2)]))),
      three:     lbl(mk('wl-3',    [1,2,3].map(word))),
      ponders:   lbl(mk('wl-pon',  six.concat([ponder(1), ponder(2)]))),
      bee:       lbl(mk('wl-bee',  six, {bee:true})),
      tooFew:    lbl(mk('wl-few',  [1,2].map(word)))
    };
  });
  ck('a deck that IS a word list says so, with its count',
     /Word list — all 6 words$/.test(gate.allWords || ''), gate);
  ck('a deck with phrases in it gets one too — and calls them TERMS',
     /Term list — all 8 terms$/.test(gate.mixed || ''), gate);
  ck('three entries is a list', /all 3 words$/.test(gate.three || ''), gate);
  ck('ponder prompts are left out, and the count says so — they have no answer to cover',
     /all 6 words$/.test(gate.ponders || ''), gate);
  ck('a Spelling Bee deck does NOT — it announces its words, never shows them',
     gate.bee === null, gate);
  ck('two entries is not a list worth a door', gate.tooFew === null, gate);

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got).slice(0,400))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
