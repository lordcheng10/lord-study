/**
 * 补拍缺失模块（按钮文案：新建*）
 */
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, '../assets/coze-loop-practice');
const BASE = 'http://localhost:8082';
const acc = JSON.parse(fs.readFileSync(path.join(OUT, 'demo-account.json'), 'utf8'));
const CHROME =
  process.env.HOME +
  '/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function shot(page, rel) {
  const file = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await sleep(700);
  await page.screenshot({ path: file });
  console.log('SHOT', rel);
}

async function clickNew(page, ...patterns) {
  for (const p of patterns) {
    const btn = page.getByRole('button', { name: p }).first();
    if (await btn.isVisible().catch(() => false)) {
      await btn.click();
      return true;
    }
  }
  // fallback: any visible button matching
  const all = page.locator('button:visible');
  const n = await all.count();
  for (let i = 0; i < n; i++) {
    const t = (await all.nth(i).innerText().catch(() => '')) || '';
    if (patterns.some((p) => (p instanceof RegExp ? p.test(t) : t.includes(String(p))))) {
      await all.nth(i).click();
      return true;
    }
  }
  // dump
  console.log(
    'buttons:',
    await Promise.all(
      Array.from({ length: Math.min(n, 20) }, (_, i) => all.nth(i).innerText().catch(() => '')),
    ),
  );
  return false;
}

async function main() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await (
    await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'zh-CN' })
  ).newPage();
  page.setDefaultTimeout(20000);

  await page.goto(`${BASE}/auth/login`, { waitUntil: 'networkidle' });
  await page.getByPlaceholder('请输入邮箱').fill(acc.email);
  await page.getByPlaceholder('请输入密码').fill(acc.password);
  await page.getByRole('button', { name: '登录' }).click();
  await page.waitForURL(/\/console\//, { timeout: 30000 });
  await sleep(2000);
  const prefix = page.url().match(/(\/console\/enterprise\/personal\/space\/\d+)/)[1];
  console.log('prefix', prefix);

  // ---- Dataset ----
  await page.goto(`${BASE}${prefix}/evaluation/datasets`, { waitUntil: 'networkidle' });
  await sleep(1000);
  await shot(page, '02-dataset/01-list.png');
  await clickNew(page, /新建评测集/, /新建/, /创建/);
  await sleep(1500);
  await shot(page, '02-dataset/02-create.png');
  const dsInputs = page.locator('input:visible');
  console.log('ds inputs', await dsInputs.count());
  if (await dsInputs.count()) await dsInputs.first().fill(`评测集问候${Date.now().toString().slice(-4)}`);
  const ta = page.locator('textarea:visible').first();
  if (await ta.count()) await ta.fill('教程演示评测集：input/output');
  await shot(page, '02-dataset/03-named.png');
  await shot(page, '02-dataset/04-schema.png');
  await clickNew(page, /创建/, /完成/, /确定/, /提交/);
  await sleep(2500);
  await shot(page, '02-dataset/05-detail.png');

  // ---- Evaluator ----
  await page.goto(`${BASE}${prefix}/evaluation/evaluators`, { waitUntil: 'networkidle' });
  await sleep(1000);
  await shot(page, '03-evaluator/01-list.png');
  await page.goto(`${BASE}${prefix}/evaluation/evaluators?active_tab=builtin`);
  await sleep(1200);
  await shot(page, '03-evaluator/02-builtin.png');
  await page.goto(`${BASE}${prefix}/evaluation/evaluators/create/llm`);
  await sleep(1500);
  await shot(page, '03-evaluator/05-create-llm.png');
  await page.goto(`${BASE}${prefix}/evaluation/evaluators/create/code`);
  await sleep(1500);
  await shot(page, '03-evaluator/06-create-code.png');
  // 列表上的新建菜单
  await page.goto(`${BASE}${prefix}/evaluation/evaluators`);
  await sleep(800);
  await clickNew(page, /新建评估器/, /新建/, /创建/);
  await sleep(800);
  await shot(page, '03-evaluator/04-create-menu.png');

  // ---- Tag ----
  await page.goto(`${BASE}${prefix}/tag/tag`, { waitUntil: 'networkidle' });
  await sleep(1000);
  await shot(page, '06-tag/01-list.png');
  await clickNew(page, /新建标签/, /新建/, /创建/);
  await sleep(1200);
  await shot(page, '06-tag/02-create.png');
  const tagIn = page.locator('input:visible').first();
  if (await tagIn.count()) await tagIn.fill(`质量标签${Date.now().toString().slice(-4)}`);
  await shot(page, '06-tag/03-filled.png');
  await clickNew(page, /创建/, /确定/, /确认/, /提交/, /完成/);
  await sleep(1500);
  await shot(page, '06-tag/04-result.png');

  // ---- PAT via DOM click on avatar area ----
  await page.goto(`${BASE}${prefix}/pe/prompts`, { waitUntil: 'networkidle' });
  await sleep(1000);
  // Click user name area at bottom of nav
  await page.evaluate(() => {
    const items = [...document.querySelectorAll('[aria-haspopup="dialog"]')];
    items[items.length - 1]?.click();
  });
  await sleep(700);
  await shot(page, '07-pat/00-usermenu.png');
  await page.evaluate(() => {
    const el = [...document.querySelectorAll('*')].find((e) => e.childNodes.length && e.childNodes[0].nodeType === 3 && /账号设置/.test(e.textContent || '') && (e.textContent || '').length < 20);
    el?.click();
  });
  await sleep(1000);
  // try getByText
  if (await page.getByText('账号设置').first().isVisible().catch(() => false)) {
    await page.getByText('账号设置').first().click();
    await sleep(1000);
  }
  await shot(page, '07-pat/01-account.png');
  await page.evaluate(() => {
    const el = [...document.querySelectorAll('div,span,button,li')].find((e) =>
      /API\s*授权|个人访问|Personal Access|令牌/.test(e.textContent || '') && (e.textContent || '').length < 40,
    );
    el?.click();
  });
  await sleep(800);
  await shot(page, '07-pat/02-pat-tab.png');
  await clickNew(page, /创建令牌/, /新建/, /创建/, /添加/);
  await sleep(800);
  await shot(page, '07-pat/03-create.png');
  const patIn = page.locator('input:visible').first();
  if (await patIn.count()) await patIn.fill('教程演示Token');
  await shot(page, '07-pat/04-filled.png');
  await clickNew(page, /创建/, /确定/, /确认/, /生成/);
  await sleep(1000);
  await shot(page, '07-pat/05-created.png');

  // ---- Experiment steps already mostly ok; refresh wizard ----
  await page.goto(`${BASE}${prefix}/evaluation/experiments/create`);
  await sleep(1500);
  await shot(page, '04-experiment/02-wizard.png');

  // ---- Trace ----
  await page.goto(`${BASE}${prefix}/observation/traces`);
  await sleep(1500);
  await shot(page, '05-trace/01-list.png');

  console.log('DONE');
  await browser.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
