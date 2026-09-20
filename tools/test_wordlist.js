/* The word list — every word in a vocabulary lesson on one screen.

   Chris: "for the different wordly wise units, can we figure out a way to
   include the complete word list?" The words were always all there, one card
   each; the deck just shuffles and shows one at a time. So this is DERIVED
   from the cards and never authored, and the test pins that: the list and
   the deck can never disagree, because there is only one of them.

   The assertion that matters most is the last one — it must never reach the
   quiz's tool row, where it would be the answer key. Same file, both apps;
   pass the vocabulary unit id as argv[3] (defaults to Ad Astra's). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8104;

(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  /* The unit is DISCOVERED, not named in argv — the same file has to run in
     both apps, whose vocabulary ids and filenames differ, and a hardcoded id
     is exactly the harness rot this repo keeps paying for. Load the whole
     shipped library and take the first unit the app itself says has a word
     list. */
  const seed = await p.evaluate(async () => {
    /* The real files rather than fetchLibrary(), which reaches for the
       parent screen's own toast nodes and is not callable headless. */
    for(const path of CONTENT_LIBRARY){
      try{ const j = await (await fetch(path)).json();
        Object.values(j.records).forEach(r=>{ if(r && r.type){ r.status='approved'; delete r.releaseOn; put(r); } });
      }catch(e){}
    }
    saveLocal();
    const u = Object.values(DATA.records)
      .filter(r=>r.type==='unit' && !r.deleted && hasWordList(r))
      .sort((a,b)=>a.title<b.title?-1:1)[0];
    if(!u) return {missing:true};
    return {UNIT:u.id, cid:u.classId, title:u.title, n:u.cards.length,
            terms: u.cards.map(c=>c.term),
            leads: u.cards.map(c=>String(c.def).split('\n')[0].trim())};
  });
  if(seed.missing){ console.log('FAIL no unit in this library has a word list'); process.exit(1); }
  const UNIT = seed.UNIT;
  ck('a real shipped vocabulary lesson qualifies', seed.n >= 6, seed.title + ' · ' + seed.n + ' words');

  const door = await p.evaluate((UNIT) => {
    const u = unitFor(UNIT), c = CLASS_BY_ID[u.classId];
    const card = unitCard(u, c);
    document.body.appendChild(card);
    const btn = [...card.querySelectorAll('button')].find(x=>/Word list/.test(x.textContent));
    const r = btn && btn.getBoundingClientRect();
    /* The door sits in Practice, and BEFORE the flashcard tile — the list is
       what you read before you drill, the way the book prints it. */
    const kids = [...card.children];
    const secs = kids.map(k=>k.className);
    return {label: btn ? btn.textContent : null, h: btn ? Math.round(r.height) : 0,
            beforeTiles: btn ? kids.indexOf(btn) < kids.findIndex(k=>k.classList.contains('mrow')) : false,
            afterPractice: btn ? kids.indexOf(btn) > secs.indexOf('seclab') : false};
  }, UNIT);
  ck('the lesson card offers a Word list door, naming how many words',
     door.label === '\ud83d\udcd6  Word list \u2014 all ' + seed.n + ' words'
       + 'Every word in this lesson, meanings hidden until you tap', door);
  ck('it is a real tap target', door.h >= 44, door);
  ck('it sits under Practice, ahead of the drill tiles',
     door.afterPractice && door.beforeTiles, door);

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
      names: box.textContent.includes(unitFor(UNIT).title)
    };
  }, UNIT);
  ck('every word in the lesson is listed, in the deck\'s own order',
     JSON.stringify(open.words) === JSON.stringify(seed.terms), {got:open.words, want:seed.terms});
  ck('it names which lesson it is', /Word list/.test(open.title) && open.names, open.title);
  ck('each word shows how to say it', open.sp.filter(Boolean).length === seed.terms.length, open.sp);
  ck('no meaning is given away before she asks', open.hidden, open.hidden);
  ck('every row is a real tap target even folded', open.minH >= 44, open.minH);

  const one = await p.evaluate(() => {
    const rows = [...document.querySelectorAll('.modal-box .wlrow')];
    rows[3].click();
    const vis = r => { const d=r.querySelector('.wld');
      return !d.hidden && getComputedStyle(d).display !== 'none' && d.offsetHeight > 0; };
    return {shown: vis(rows[3]),
            text: rows[3].querySelector('.wld').textContent,
            othersStillHidden: rows.filter((r,i)=>i!==3).every(r=>!vis(r)),
            aria: rows[3].getAttribute('aria-expanded')};
  });
  ck('tapping one word reveals its meaning', one.shown && one.text.length > 5, one);
  ck('and only that one — she can check a word without spoiling the rest',
     one.othersStillHidden, one);
  ck('the row reports its state to a screen reader', one.aria === 'true', one);
  ck('the meaning is the card\'s own bold lead, not a rewritten copy',
     seed.leads[3].replace(/\*\*/g,'') === one.text.trim(), {got:one.text, want:seed.leads[3]});

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

  /* THE RULE. A vocabulary list with its meanings, reachable during a
     vocabulary quiz, is the answer key — so the quiz must not offer it,
     unlike the Sheet and Map doors that deliberately do live there. */
  const quiz = await p.evaluate((UNIT) => {
    document.querySelector('.modal-overlay')?.remove();
    const u = unitFor(UNIT);
    quizState = null;
    go('quiz', {unitId:u.id, classId:u.classId});
    const scr = document.getElementById('screen');
    const tools = [...scr.querySelectorAll('.tool, .tools button')].map(x=>x.textContent.trim());
    return {tools, anyWordList: /word list/i.test(scr.textContent)};
  }, UNIT);
  ck('the quiz never offers the word list in its tool row',
     !quiz.tools.some(t=>/word/i.test(t)), quiz.tools);
  ck('and the word list appears nowhere on the quiz screen at all',
     !quiz.anyWordList, quiz.tools);

  /* Who gets the door. A deck must BE a word list, not merely contain some
     words — a partial list labelled "all N words" is a lie she would revise
     against. And a Spelling Bee deck is all single words and still excluded,
     because that unit's whole design is announcing a word it never shows. */
  const gate = await p.evaluate(() => {
    const cid = STUDY_CLASSES[0].id;
    const mk = (id, cards, extra) => Object.assign({id, type:'unit', classId:cid,
      status:'approved', title:id, updatedAt:Date.now(), cards, questions:[]}, extra||{});
    const word = n => ({id:'c'+n, term:'word'+n, def:'**A meaning.** (noun)'});
    const phrase = n => ({id:'p'+n, term:'Adding whole numbers '+n, def:'**A meaning.**'});
    const six = [1,2,3,4,5,6].map(word);
    const has = u => { const card = unitCard(u, CLASS_BY_ID[cid]);
      return !!([...card.querySelectorAll('button')].find(x=>/Word list/.test(x.textContent))); };
    return {
      allWords:  has(mk('wl-all',  six)),
      mixed:     has(mk('wl-mix',  six.concat([phrase(1), phrase(2)]))),
      bee:       has(mk('wl-bee',  six, {bee:true})),
      tooFew:    has(mk('wl-few',  [1,2,3].map(word)))
    };
  });
  ck('a deck that IS a word list gets the door', gate.allWords, gate);
  ck('a deck with multi-word cards mixed in does NOT — "all N words" would be false',
     !gate.mixed, gate);
  ck('a Spelling Bee deck does NOT — it announces its words, never shows them',
     !gate.bee, gate);
  ck('a deck of three words is not a list worth a door', !gate.tooFew, gate);

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got).slice(0,400))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
