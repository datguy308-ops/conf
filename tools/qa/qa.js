/* Final QA for the built site. Serves public/ on a local port and checks:
   links/assets, canonical + hreflang, JSON-LD, sitemap/robots, titles/descriptions,
   headings, console errors, 404, placeholder text, banned marketing phrases,
   EN/ES parity, language switching, mobile menu, keyboard (lightbox, form),
   horizontal overflow at 9 widths, and axe-core (WCAG 2.x A/AA + best practice).
   Usage: cd tools/qa && npm install && node qa.js   (CHROME_PATH optional) */
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const PUB = path.resolve(__dirname, "../../public");
const SITE = "https://www.confidenceaviation.com";
const PAGES = ["index.html", "about.htm", "capabilities.htm", "certificates.htm", "shop.htm", "contact.htm"];
const ALL = [...PAGES, ...PAGES.map(p => "es/" + p)];
const BANNED = /world[- ]class|industry[- ]leading|best[- ]in[- ]class|unparalleled|revolutionary|#1\b|trusted by thousands|lorem ipsum|placeholder text|\{\{|\}\}/i;
const DEVMARK = /\b(TODO|FIXME|XXX)\b/;   // case-sensitive: Spanish "todo" is a normal word
let fails = 0; const fail = (m) => { fails++; console.log("  FAIL " + m); }; const ok = (m) => console.log("  ok   " + m);

const types = { ".html": "text/html", ".htm": "text/html", ".css": "text/css", ".js": "text/javascript", ".png": "image/png",
  ".jpg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".ico": "image/x-icon", ".xml": "application/xml", ".txt": "text/plain", ".webmanifest": "application/manifest+json" };
// Send the production Content-Security-Policy from public/.htaccess so violations surface as console errors.
const CSP = (fs.readFileSync(path.join(PUB, ".htaccess"), "utf8").match(/Content-Security-Policy "([^"]+)"/) || [])[1];
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0].split("#")[0]);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(PUB, p);
  if (!f.startsWith(PUB) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
    res.writeHead(404, { "content-type": "text/html" }); return res.end(fs.readFileSync(path.join(PUB, "404.html")));
  }
  const hdr = { "content-type": types[path.extname(f)] || "application/octet-stream" };
  if (CSP && /\.html?$/.test(f)) hdr["content-security-policy"] = CSP;
  res.writeHead(200, hdr); res.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(r => server.listen(0, r));
  console.log(CSP ? "   (serving with production Content-Security-Policy)" : "   (no CSP found in .htaccess)");
  const BASE = `http://localhost:${server.address().port}/`;
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const consoleErrors = [];
  page.on("console", m => { if (m.type() === "error") consoleErrors.push(page.url() + " " + m.text()); });
  page.on("pageerror", e => consoleErrors.push(page.url() + " " + e.message));
  const failedReq = [];
  page.on("response", r => { if (r.url().startsWith(BASE) && r.status() >= 400) failedReq.push(r.status() + " " + r.url()); });

  console.log("1. Crawl, links, assets, metadata");
  const info = {};
  for (const p of ALL) {
    await page.goto(BASE + p, { waitUntil: "load" });
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 20)); } });
    const d = await page.evaluate(() => {
      const q = s => [...document.querySelectorAll(s)];
      return {
        lang: document.documentElement.lang, title: document.title,
        desc: document.querySelector('meta[name=description]')?.content || "",
        canonical: document.querySelector('link[rel=canonical]')?.href,
        hreflang: Object.fromEntries(q('link[rel=alternate][hreflang]').map(l => [l.hreflang, l.href])),
        h1: q("h1").length, headings: q("h1,h2,h3,h4").map(h => +h.tagName[1]),
        links: q("a[href]").map(a => a.href), imgsBroken: q("img").filter(i => i.complete && i.naturalWidth === 0 && !i.closest("dialog")).map(i => i.currentSrc || i.src),
        ld: q('script[type="application/ld+json"]').map(s => s.textContent),
        text: document.body.innerText, ctas: q('a[href*="contact.htm#quote"]').length,
        sections: q("main section").length, ids: q("[id]").map(e => e.id),
        switchTo: document.querySelector('.topbar .lang a:not([aria-current])')?.getAttribute("href"),
      };
    });
    info[p] = d;
    if (d.h1 !== 1) fail(`${p}: ${d.h1} h1 elements`);
    for (let i = 1; i < d.headings.length; i++) if (d.headings[i] > d.headings[i - 1] + 1) { fail(`${p}: heading level skips h${d.headings[i - 1]}→h${d.headings[i]}`); break; }
    if (d.title.length < 20 || d.title.length > 95) fail(`${p}: title length ${d.title.length}`);
    if (d.desc.length < 70 || d.desc.length > 320) fail(`${p}: description length ${d.desc.length}`);
    const expectCanon = SITE + "/" + p.replace(/index\.html$/, "");
    if (d.canonical !== expectCanon) fail(`${p}: canonical ${d.canonical} (expected ${expectCanon})`);
    const lang = p.startsWith("es/") ? "es" : "en";
    if (d.lang !== lang) fail(`${p}: html lang=${d.lang}`);
    if (d.hreflang[lang] !== expectCanon) fail(`${p}: self hreflang mismatch`);
    if (!d.hreflang["x-default"]) fail(`${p}: no x-default`);
    for (const s of d.ld) { try { const j = JSON.parse(s); if (!j["@graph"]?.length) fail(`${p}: JSON-LD has no @graph`); } catch (e) { fail(`${p}: invalid JSON-LD`); } }
    if (BANNED.test(d.text)) fail(`${p}: banned/placeholder phrase: ${d.text.match(BANNED)[0]}`);
    if (DEVMARK.test(d.text)) fail(`${p}: developer marker: ${d.text.match(DEVMARK)[0]}`);
    if (d.imgsBroken.length) fail(`${p}: broken images ${d.imgsBroken.join(", ")}`);
    if (!d.ctas) fail(`${p}: no Request a Repair Quote link`);
  }
  // hreflang reciprocity
  for (const p of PAGES) {
    const en = info[p], es = info["es/" + p];
    if (en.hreflang.es !== es.canonical || es.hreflang.en !== en.canonical) fail(`${p}: hreflang not reciprocal`);
  }
  // every internal link resolves (and anchors exist)
  const checked = new Set();
  for (const p of ALL) for (const href of info[p].links) {
    if (!href.startsWith(BASE) || checked.has(href)) continue; checked.add(href);
    const [u, frag] = href.split("#");
    const r = await page.request.get(u);
    if (r.status() !== 200) { fail(`${p}: link ${href} → ${r.status()}`); continue; }
    if (frag && /\.html?$|\/$/.test(u.split("?")[0])) {
      const rel = u.slice(BASE.length) || "index.html"; const key = rel.endsWith("/") ? rel + "index.html" : rel;
      if (info[key] && !info[key].ids.includes(frag)) fail(`${p}: missing anchor #${frag} on ${key}`);
    }
  }
  ok(`${ALL.length} pages crawled, ${checked.size} unique internal URLs checked`);
  if (failedReq.length) [...new Set(failedReq)].forEach(r => fail("asset request " + r)); else ok("no failed asset requests");
  if (consoleErrors.length) consoleErrors.forEach(c => fail("console: " + c)); else ok("no console errors");

  console.log("2. Sitemap, robots, 404, legacy URL");
  const sm = await (await page.request.get(BASE + "sitemap.xml")).text();
  const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
  const expected = ALL.map(p => SITE + "/" + p.replace(/index\.html$/, ""));
  if (JSON.stringify(locs.sort()) !== JSON.stringify(expected.sort())) fail("sitemap URLs differ from page set"); else ok(`sitemap lists ${locs.length} canonical URLs`);
  const robots = await (await page.request.get(BASE + "robots.txt")).text();
  if (!/Sitemap: https:\/\/www\.confidenceaviation\.com\/sitemap\.xml/.test(robots) || /Disallow: \/\s*$/m.test(robots)) fail("robots.txt"); else ok("robots.txt allows crawling and names the sitemap");
  const nf = await page.goto(BASE + "no-such-page.htm");
  if (nf.status() !== 404 || !(await page.content()).includes('content="noindex"')) fail("404 page"); else ok("404 page returned with noindex");
  await page.goto(BASE + "index.htm"); await page.waitForURL(u => !u.pathname.endsWith("index.htm"), { timeout: 3000 }).catch(() => {});
  if (page.url().endsWith("index.htm")) fail("legacy /index.htm does not forward"); else ok("legacy /index.htm forwards to /");

  console.log("3. English / Spanish parity");
  for (const p of PAGES) {
    const en = info[p], es = info["es/" + p];
    if (en.sections !== es.sections) fail(`${p}: sections EN ${en.sections} vs ES ${es.sections}`);
    if (en.ctas !== es.ctas) fail(`${p}: quote CTAs EN ${en.ctas} vs ES ${es.ctas}`);
    const setOf = t => [...new Set((t.match(/V9DR072Y|EASA\.145\.5139|1998|2004|\b55\b|305-392-629[12]|33166|A003/g) || []))].sort().join();
    if (setOf(en.text) !== setOf(es.text)) fail(`${p}: key facts differ EN [${setOf(en.text)}] vs ES [${setOf(es.text)}]`);
    if (!en.switchTo?.includes("es/") || !es.switchTo) fail(`${p}: language switch link missing`);
  }
  ok("parity checks done");

  console.log("4. Mobile menu, keyboard, form");
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await m.goto(BASE + "index.html");
  const navVisible = () => m.isVisible('#site-nav a[href="about.htm"]');
  if (await navVisible()) fail("mobile nav visible before toggle");
  await m.focus(".nav-toggle"); await m.keyboard.press("Enter");
  if (!(await navVisible()) || !(await m.isVisible("#site-nav .header-cta"))) fail("mobile nav/CTA not shown after toggle");
  await m.keyboard.press("Escape"); if (await navVisible()) fail("Escape does not close mobile nav");
  ok("mobile menu toggles with keyboard; CTA inside menu");
  await m.goto(BASE + "index.html"); await m.keyboard.press("Tab");
  if ((await m.evaluate(() => document.activeElement.className)) !== "skip-link") fail("first tab stop is not the skip link"); else ok("skip link is first tab stop");
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(BASE + "shop.htm"); await page.focus("#shop-radar-bench-1 a"); await page.keyboard.press("Enter");
  const dlgOpen = () => page.evaluate(() => document.querySelector("dialog.lightbox")?.open);
  if (!(await dlgOpen())) fail("lightbox did not open");
  await page.keyboard.press("ArrowRight");
  const cap = await page.textContent(".lightbox__caption");
  await page.keyboard.press("Escape");
  const back = await page.evaluate(() => document.activeElement.closest("li")?.id);
  if (cap !== "Aviation Workshop NAV/COMM Bench" || (await dlgOpen()) || back !== "shop-radar-bench-1") fail(`lightbox keyboard (caption ${cap}, focus ${back})`); else ok("lightbox: Enter opens, → advances, Esc closes, focus returns");
  for (const lang of ["", "es/"]) {
    await page.goto(BASE + lang + "contact.htm#quote");
    // Stop the mailto: navigation from leaving the page; the form reports success in its status line.
    await page.evaluate(() => { window.addEventListener("beforeunload", e => e.preventDefault()); });
    await page.click("#contact-form button[type=submit]");
    const errs = await page.$$eval("#contact-form [aria-invalid=true]", els => els.map(e => e.id));
    const focusedSummary = await page.evaluate(() => document.activeElement.classList.contains("form-errors"));
    if (errs.join() !== "f-name,f-email,f-manufacturer,f-part,f-message" || !focusedSummary) fail(`${lang}form empty-submit validation: ${errs}`);
    await page.fill("#f-name", "Test Person"); await page.fill("#f-email", "not-an-email");
    await page.click("#contact-form button[type=submit]");
    if (!(await page.textContent("#f-email-err")).length) fail(`${lang}invalid email not reported`);
    await page.fill("#f-email", "test@example.com"); await page.fill("#f-manufacturer", "Bendix/King");
    await page.fill("#f-part", "066-1234-00"); await page.fill("#f-message", "Intermittent display"); await page.check("#f-aog");
    const href = await page.evaluate(() => new Promise(res => {
      const f = document.getElementById("contact-form");
      f.addEventListener("submit", () => setTimeout(() => res(document.querySelector(".form-status").textContent), 50), { once: true });
      f.requestSubmit();
    }));
    if (!href) fail(`${lang}form did not report success status`); else ok(`${lang || "en/"}form: validation, error summary focus, success status`);
  }

  console.log("5. Layout: horizontal overflow at 9 widths");
  let over = 0;
  for (const w of [320, 360, 390, 414, 768, 1024, 1280, 1920, 2560]) {
    const v = await browser.newPage({ viewport: { width: w, height: 800 } });
    for (const p of [...ALL, "404.html"]) {
      await v.goto(BASE + p);
      const o = await v.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      if (o > 0) { over++; fail(`overflow ${o}px at ${w}px on ${p}`); }
    }
    await v.close();
  }
  if (!over) ok(`no horizontal overflow on ${ALL.length + 1} pages × 9 widths`);

  console.log("6. Accessibility (axe-core)");
  const axe = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");
  let viol = 0;
  for (const w of [1280, 390]) {
    const a = await browser.newPage({ viewport: { width: w, height: 900 }, bypassCSP: true });  // lets axe-core inject its script
    for (const p of [...ALL, "404.html"]) {
      await a.goto(BASE + p);
      await a.evaluate(() => document.querySelectorAll("details").forEach(d => d.open = true));
      await a.addScriptTag({ content: axe });
      const r = await a.evaluate(() => axe.run(document, { runOnly: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] }));
      for (const v of r.violations) { viol++; fail(`axe ${w}px ${p}: ${v.id} (${v.impact}) ${v.nodes[0].target.join(" ")}`); }
    }
    await a.close();
  }
  if (!viol) ok(`0 axe violations on ${ALL.length + 1} pages at desktop and mobile`);

  await browser.close(); server.close();
  console.log(fails ? `\nQA RESULT: ${fails} failure(s)` : "\nQA RESULT: PASS");
  process.exit(fails ? 1 : 0);
})();
