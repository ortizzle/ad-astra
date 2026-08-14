// Verify kind:'analogy' renders as a test-style stem and behaves as ordinary MC.
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 412, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type()==='error') errors.push('CONSOLE: ' + m.text()); });

  await page.goto('http://localhost:8130/index.html', { waitUntil: 'networkidle' });

  const out = await page.evaluate(async () => {
    const r = {};
    await fetchLibrary({ textContent:'', disabled:false });
    const u = DATA.records['unit-ww9-01'];
    r.unitFound = !!u;
    r.status = u && u.status;
    u.status = 'approved'; u.updatedAt = Date.now();

    const anas = u.questions.filter(q => q.kind === 'analogy');
    r.analogyCount = anas.length;
    r.stems = anas.map(q => q.q);

    // Drive the quiz straight to an analogy question (real quizState shape).
    quizState = { unitId:u.id, i:0, correct:0, answered:null, start:Date.now(),
      order:[u.questions.indexOf(anas[0])], missed:[], hintUsed:false, hints:0, pre:null,
      timed:false, speedBonus:0, fastest:null, deadline:0, seen:[],
      limit:60000, runStreak:0, qShownAt:Date.now(), ansMs:0, ansN:0 };
    go('quiz', { classId:'english', unitId:u.id, timed:false });
    const root = document.getElementById('screen');
    const plate = root.querySelector('.analogy');
    r.plateRendered = !!plate;
    r.plateText = plate && plate.textContent;
    r.plateSpans = plate && [...plate.children].map(c => c.className + '=' + c.textContent);
    r.eyebrow = !!root.textContent.match(/Complete the analogy/);
    r.optionCount = root.querySelectorAll('.opt').length;
    r.optionTexts = [...root.querySelectorAll('.opt')].map(b => b.textContent);
    // No horizontal overflow on a phone-width screen.
    r.bodyScrollW = document.body.scrollWidth;
    r.bodyClientW = document.body.clientWidth;
    // Computed style sanity: text must not be the page canvas colour.
    if(plate){
      const cs = getComputedStyle(plate);
      r.plateColor = cs.color; r.plateBg = cs.backgroundColor;
      r.inkVar = getComputedStyle(document.documentElement).getPropertyValue('--ink').trim();
    } else { r.screenHTMLHead = root.textContent.slice(0,300); }
    return r;
  });

  console.log(JSON.stringify(out, null, 1));

  // Answering an analogy must behave exactly like MC.
  const after = await page.evaluate(() => {
    const u = DATA.records['unit-ww9-01'];
    const q = u.questions[quizState.order[0]];
    answer(u, q, q.ans);                       // answer correctly
    const root = document.getElementById('screen');
    return { answered: quizState.answered, correct: quizState.correct,
             explainShown: !!root.querySelector('.explain.ok'),
             stillPlated: !!root.querySelector('.analogy') };
  });
  console.log('after answering:', JSON.stringify(after));
  await page.screenshot({ path: '/tmp/claude-0/-home-user/8620cdbb-8d61-5574-90fe-da0b5544d932/scratchpad/analogy.png' });
  console.log('errors:', errors.length ? errors : 'none');
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})();
