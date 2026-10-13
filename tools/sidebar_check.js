#!/usr/bin/env node
// SPDX-License-Identifier: GPL-2.0-or-later
// Copyright (C) 2026 Beibit Sakhanov
// Checks the administrator sidebar of a running Joomla in headless Chromium: for every section it looks for menu rows
// whose label wraps or whose "+" button dropped to the next line (the long-label problem), and can save screenshots.
//   npm i @sparticuz/chromium puppeteer-core
//   node tools/sidebar_check.js --base http://127.0.0.1:8099 --user admin --password '...' [--width 1366] [--shots DIR]
const chromium = require('@sparticuz/chromium').default || require('@sparticuz/chromium');
const puppeteer = require('puppeteer-core');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > -1 ? process.argv[i + 1] : d; };
const base = arg('base', 'http://127.0.0.1:8099'), user = arg('user', 'admin'), pass = arg('password'), width = parseInt(arg('width', '1366')), shots = arg('shots');
if (!pass) { console.error('--password is required'); process.exit(2); }
(async () => {
  const browser = await puppeteer.launch({ args: [...chromium.args, '--no-sandbox', '--disable-gpu'], executablePath: await chromium.executablePath(), headless: 'shell', defaultViewport: { width, height: 900 } });
  const page = await browser.newPage();
  await page.goto(base + '/administrator/', { waitUntil: 'networkidle2', timeout: 60000 });
  await page.type('#mod-login-username', user); await page.type('#mod-login-password', pass);
  await Promise.all([page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 60000 }), page.click('button[type=submit]')]);
  const closeTour = () => page.evaluate(() => { const b = [...document.querySelectorAll('button')].find(x => /Мәңгілікке|Болдырмау|Dismiss|Cancel/.test(x.textContent)); if (b) b.click(); });
  // top-level sidebar items that have a submenu (found by structure, not by id or class names)
  const titles = () => page.evaluate(() => [...document.querySelectorAll('#sidebar-wrapper .sidebar-item-title')]
    .filter(e => { const li = e.closest('li'); return li && li.querySelector(':scope > ul') && !li.parentElement.closest('li'); })
    .map(e => e.textContent.trim()));
  await closeTour();
  const parents = await titles(); const bad = []; let rows = 0;
  if (!parents.length) { console.error('ERROR: no sidebar sections found, the page structure may have changed'); await browser.close(); process.exit(2); }
  for (const text of parents) {
    await page.goto(base + '/administrator/index.php', { waitUntil: 'networkidle2' }); await closeTour();
    await page.evaluate((text) => { const s = [...document.querySelectorAll('#sidebar-wrapper .sidebar-item-title')].find(x => x.textContent.trim() === text && x.closest('li').querySelector(':scope > ul')); if (s) s.closest('a').click(); }, text);
    await new Promise(r => setTimeout(r, 700));
    const res = await page.evaluate(() => {
      const out = []; let n = 0;
      document.querySelectorAll('#sidebar-wrapper li').forEach(li => {
        const a = li.querySelector(':scope > a'); if (!a || !a.offsetParent) return; n++;
        const t = a.querySelector('.sidebar-item-title'); const txt = (t || a).textContent.trim();
        const qt = li.querySelector(':scope > .menu-quicktask, :scope > a.menu-quicktask-link, :scope > .menu-quicktask a');
        const r = a.getBoundingClientRect();
        const drop = qt && qt.offsetParent ? qt.getBoundingClientRect().top - r.top > 8 : false;
        if (drop || r.height > 40) out.push({ txt, height: Math.round(r.height), plusDropped: drop });
      });
      return { out, n };
    });
    rows += res.n; res.out.forEach(x => bad.push(Object.assign({ section: text }, x)));
    if (shots) { const box = await (await page.$('#sidebar-wrapper')).boundingBox(); await page.screenshot({ path: `${shots}/sidebar_${parents.indexOf(text)}.png`, clip: { x: 0, y: 0, width: Math.ceil(box.width), height: 900 } }); }
  }
  console.log(`sections: ${parents.length} (${parents.join(', ')}), visible rows checked: ${rows}, broken rows: ${bad.length}`);
  if (rows === 0) { console.error('ERROR: no visible rows were measured'); await browser.close(); process.exit(2); }
  bad.forEach(x => console.log('  !', JSON.stringify(x)));
  await browser.close(); process.exit(bad.length ? 1 : 0);
})().catch(e => { console.error('ERROR', String(e).slice(0, 500)); process.exit(2); });
