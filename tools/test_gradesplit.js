/* The parent view's Tests & quizzes list, split so an ungraded one is the
   thing you see. Chris: "once graded can they get tucked away or ordered
   separately, so I can focus on ungraded quiz and tests?"

   Same file in both apps. It pins the RULE, not the seeded titles: what is
   waiting on a score, what is merely upcoming, and that a score of ZERO is a
   grade rather than a gap (the `!a.score` trap studyPlan already paid for). */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8104;

(async () => {
  const b = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  const errs = []; p.on('pageerror', e => errs.push(String(e.message)));
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'networkidle'});

  const out = [];
  const ck = (n, ok, got) => out.push({n, ok: !!ok, got});

  const seed = await p.evaluate(() => {
    AZ.today = () => '2026-09-01';
    const [c1, c2] = STUDY_CLASSES.map(c=>c.id);
    const A = (id, cid, title, date, score) => put({id:'assess_'+id, type:'assess',
      classId:cid, kind:'quiz', title, date, points:score, outOf:100, score});

    A('sat_old', c1, 'Sat a while ago',  '2026-08-10', null);  // waiting, older
    A('sat_new', c2, 'Sat last week',    '2026-08-27', null);  // waiting, newer
    A('zero',    c1, 'The zero',         '2026-08-20', 0);     // GRADED, not waiting
    A('g1',      c1, 'Marked one',       '2026-08-15', 88);
    A('g2',      c2, 'Marked two',       '2026-08-22', 74);
    A('soon',    c1, 'Next Friday',      '2026-09-04', null);  // ahead, sooner
    A('later',   c2, 'Two weeks out',    '2026-09-15', null);  // ahead, later

    saveLocal();
    go('parent');
    const sec = [...document.querySelectorAll('#screen .card')]
      .find(c => /Waiting on a score|Still to come|already graded/.test(c.innerText));
    return {c1, c2, txt: sec ? sec.innerText : '(card not found)'};
  });

  const T = seed.txt;
  ck('the list leads with what is waiting on a score, and counts it',
     /WAITING ON A SCORE · 2/i.test(T), T.slice(0,160));
  ck('both sat-and-unmarked assessments are in it',
     /Sat a while ago/.test(T) && /Sat last week/.test(T), T.slice(0,300));
  ck('a score of ZERO counts as graded, not as waiting',
     T.indexOf('The zero') === -1, 'zero appeared before the fold was opened');
  ck('upcoming assessments are their own group, not mixed into the waiting list',
     /STILL TO COME/i.test(T)
     && T.indexOf('Next Friday') > T.indexOf('Still to come'.toUpperCase()) - 1,
     T.slice(0,400));

  /* Order inside each group. Waiting is newest-first (the one she just sat is
     the one a grade is about to arrive for); upcoming is soonest-first. */
  const order = await p.evaluate(() => {
    const rows = [...document.querySelectorAll('#screen .card .row .k')].map(k=>k.childNodes[0].textContent);
    return rows;
  });
  const ix = s => order.findIndex(x=>x.includes(s));
  ck('waiting rows read newest first', ix('Sat last week') < ix('Sat a while ago'), order);
  ck('upcoming rows read soonest first', ix('Next Friday') < ix('Two weeks out'), order);
  ck('nothing already graded is rendered while the fold is shut',
     ix('Marked one') === -1 && ix('Marked two') === -1 && ix('The zero') === -1, order);

  /* Only a row that is genuinely waiting on a number says so. An upcoming
     test has no score to add yet, and labelling it "Add score" would put the
     false to-do straight back that the split exists to remove. */
  const labels = await p.evaluate(() => {
    const out = {};
    [...document.querySelectorAll('#screen .card .row')].forEach(r=>{
      const k = r.querySelector('.k'), btn = r.querySelector('button');
      if(!k || !btn) return;                       /* the by-subject rows have no door */
      out[k.childNodes[0].textContent.replace(/^\S+\s*/, '').trim()] = btn.textContent.trim();
    });
    return out;
  });
  ck('a sat-but-unmarked row asks for the score',
     labels['Sat last week'] === 'Add score' && labels['Sat a while ago'] === 'Add score', labels);
  ck('an upcoming row does NOT ask for a score it cannot have',
     labels['Next Friday'] === 'Edit' && labels['Two weeks out'] === 'Edit', labels);

  /* The fold. */
  const fold = await p.evaluate(() => {
    const btn = [...document.querySelectorAll('#screen .card button')]
      .find(x=>/already graded/.test(x.textContent));
    if(!btn) return {missing:true};
    const r = btn.getBoundingClientRect();
    const prev = btn.previousElementSibling;
    const gap = prev ? Math.round(r.top - prev.getBoundingClientRect().bottom) : null;
    return {label: btn.textContent, h: Math.round(r.height), gap};
  });
  ck('one door to the graded ones, naming how many there are',
     /Show the 3 already graded/.test(fold.label || ''), fold);
  ck('that door is a real tap target', fold.h >= 44, fold);
  ck('it is not flush against the row above it', fold.gap >= 8, fold);

  const opened = await p.evaluate(() => {
    [...document.querySelectorAll('#screen .card button')]
      .find(x=>/already graded/.test(x.textContent)).click();
    const rows = [...document.querySelectorAll('#screen .card .row .k')].map(k=>k.childNodes[0].textContent);
    const btn = [...document.querySelectorAll('#screen .card button')]
      .find(x=>/already graded/.test(x.textContent));
    return {rows, label: btn ? btn.textContent : null,
            txt: document.getElementById('screen').innerText};
  });
  ck('opening it shows every graded one, the zero included',
     opened.rows.some(x=>x.includes('Marked one')) && opened.rows.some(x=>x.includes('Marked two'))
     && opened.rows.some(x=>x.includes('The zero')), opened.rows);
  ck('the door flips to Hide, so it can be shut again', /Hide the 3/.test(opened.label||''), opened.label);
  ck('the zero renders as the grade it is, not as "Add score"',
     /0%/.test(opened.txt), opened.txt.slice(0,600));

  /* A group heading partway down a card needs air above it — the row before it
     keeps its own bottom border, so a flush eyebrow reads as that border's
     caption rather than a heading for what follows. Measured, not assumed. */
  const head = await p.evaluate(() => {
    const e = [...document.querySelectorAll('#screen .card .eyebrow')]
      .find(x=>/Still to come/i.test(x.textContent));
    if(!e) return {missing:true};
    const prev = e.previousElementSibling;
    return {gap: Math.round(e.getBoundingClientRect().top - prev.getBoundingClientRect().bottom),
            mt: getComputedStyle(e).marginTop};
  });
  ck('the second group heading is not flush against the row above it',
     head.gap >= 10, head);

  /* Every row is still the door to editing that assessment. */
  const modal = await p.evaluate(() => {
    const r = [...document.querySelectorAll('#screen .card .row')]
      .find(x=>x.innerText.includes('Sat last week'));
    r.querySelector('button').click();
    const m = document.querySelector('.modal-box');
    return {open: !!m, txt: m ? m.innerText.slice(0,200) : null};
  });
  ck('a row still opens its own edit modal', modal.open, modal);

  /* Nothing outstanding says so, rather than rendering an empty group. */
  const clear = await p.evaluate(() => {
    ['sat_old','sat_new','soon','later'].forEach(id=>softDelete('assess_'+id));
    go('parent');
    const sec = [...document.querySelectorAll('#screen .card')]
      .find(c => /already graded|waiting on you/i.test(c.innerText));
    return sec ? sec.innerText : '(not found)';
  });
  ck('with everything marked, it says so instead of showing an empty list',
     /nothing is waiting on you/i.test(clear) && !/WAITING ON A SCORE/i.test(clear), clear.slice(0,300));

  out.forEach(x => console.log((x.ok ? ' ok ' : 'FAIL ') + x.n + (x.ok ? '' : ' -> ' + JSON.stringify(x.got).slice(0,400))));
  console.log(out.every(x=>x.ok) ? 'ALL PASS' : 'FAILURES');
  console.log('page errors:', errs.length ? errs.slice(0,10) : 'none');
  await b.close();
  if (!out.every(x=>x.ok) || errs.length) process.exit(1);
})();
