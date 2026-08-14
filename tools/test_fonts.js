/* Fonts must render with the network BLOCKED — that is the whole point. */
const { chromium } = require('playwright');
const PORT = process.argv[2] || 8130;
(async () => {
  const b = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:390,height:844}});
  await p.route(/^(?!http:\/\/localhost)/, r => r.abort());   // no third parties at all
  await p.goto(`http://localhost:${PORT}/index.html`, {waitUntil:'load', timeout:15000});
  await p.waitForTimeout(600);
  const out = await p.evaluate(async () => {
    await document.fonts.ready;
    /* check() only reports LOADED faces, and loading is lazy — force each. */
    await document.fonts.load('600 20px Fraunces');
    await document.fonts.load('italic 400 16px Fraunces');
    await document.fonts.load('600 14px "Plus Jakarta Sans"');
    return {
      fraunces: document.fonts.check('600 20px Fraunces'),
      frauncesItal: document.fonts.check('italic 400 16px Fraunces'),
      jakarta: document.fonts.check('600 14px "Plus Jakarta Sans"'),
      externalLinks: document.querySelectorAll('link[href*="googleapis"],link[href*="gstatic"]').length
    };
  });
  console.log(JSON.stringify(out));
  const ok = out.fraunces && out.frauncesItal && out.jakarta && out.externalLinks===0;
  console.log(ok ? 'ALL PASS' : 'FAILURES');
  await b.close();
  if(!ok) process.exit(1);
})();
