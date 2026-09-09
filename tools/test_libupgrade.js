/* The library-upgrade path — what a grown-up actually has to do for a shipped
   content fix to reach her phone.
   Written after Chris reported the Enzymes unit still reading "Unit 3" days
   after the retitle was deployed. Nothing was broken: a content/*.json change
   only enters the record store when someone taps "Check the library" in the
   parent view (fetchLibrary is called from those two buttons and nowhere else).
   This walks the whole path from the state a stale device is really in.
   Self-contained: the "old" record is built here, never read from git. */
const { chromium } = require('playwright');
const port = process.argv[2] || 8402;

(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto(`http://localhost:${port}/index.html`, {waitUntil:'networkidle'});

  /* Her device as it really was: the unit APPROVED, on an older libv, under
     the title it shipped with before the renumber. */
  const before = await pg.evaluate(() => {
    DATA.records['unit-bio-u3'] = {
      id:'unit-bio-u3', type:'unit', classId:'bio',
      title:'Biology 8 · Unit 3: Enzymes',
      status:'approved', libv:2, updatedAt: Date.now() - 864e5,
      cards:[{id:'c1', term:'Enzyme', def:'**A protein that speeds a reaction.**'}],
      questions:[{id:'q1', lv:1, q:'What is an enzyme?',
        opts:['A protein','A sugar','A lipid','A salt'], ans:0,
        steps:['Enzymes are proteins.','So the answer is a protein.'],
        ex:{main:'Enzymes are proteins.'}}]
    };
    saveLocal();
    return DATA.records['unit-bio-u3'].title;
  });
  const shelfBefore = await pg.evaluate(() =>
    shelvesFor('bio').shelves.flatMap(s => s.lessons.map(l => l.title)));

  /* The grown-up taps "Check the library". */
  const after = await pg.evaluate(async () => {
    const btn = document.createElement('button'); btn.textContent = 'Check the library';
    await fetchLibrary(btn);
    const u = DATA.records['unit-bio-u3'];
    return {title:u.title, libv:u.libv, status:u.status, wasApproved:!!u.wasApproved,
            cards:u.cards.length, questions:u.questions.length};
  });
  const shelfDraft = await pg.evaluate(() =>
    shelvesFor('bio').shelves.flatMap(s => s.lessons.map(l => l.title)));

  /* ...and approves the update, the last step before she sees it. */
  const shelfAfter = await pg.evaluate(() => {
    const u = DATA.records['unit-bio-u3'];
    u.status='approved'; delete u.chg; delete u.wasApproved; put(u);
    return shelvesFor('bio').shelves.flatMap(s => s.lessons.map(l => l.title));
  });

  const out = []; const T = (n,c) => out.push((c?'ok   ':'FAIL ') + n);
  T('a stale device really does still read "Unit 3: Enzymes"',
    before === 'Biology 8 · Unit 3: Enzymes' && shelfBefore.some(t=>/Unit 3: Enzymes/.test(t)));
  T('Check the library pulls the retitle in', after.title === 'Biology 8 · Unit 2-2: Enzymes');
  T('the newer libv wins regardless of when she approved', after.libv === 4);
  T('it brings the real unit with it, not just a title',
    after.cards >= 12 && after.questions >= 18);
  T('it re-drafts — one re-approval, by design', after.status === 'draft');
  T('the queue labels it an update, not a stranger', after.wasApproved === true);
  T('while drafted it is correctly hidden from her side',
    !shelfDraft.some(t=>/Enzymes/.test(t)));
  T('once approved the shelf shows the numbered title',
    shelfAfter.some(t=>/Unit 2-2: Enzymes/.test(t)));
  T('and "Unit 3: Enzymes" is gone for good',
    !shelfAfter.some(t=>/Unit 3: Enzymes/.test(t)));

  console.log(out.join('\n'));
  console.log(out.some(l=>l.startsWith('FAIL')) ? 'SOME FAILED' : 'ALL PASS',
              '| page errors:', errs.length ? errs : 'none');
  await b.close();
  if (out.some(l=>l.startsWith('FAIL')) || errs.length) process.exit(1);
})();
