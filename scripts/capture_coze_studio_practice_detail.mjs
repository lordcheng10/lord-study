/**
 * Coze Studio 实战教程 · 逐步截图（小白跟做）
 * 账号：fake@ponyft.com / 123456
 */
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'assets/coze-practice');
const BASE = 'http://localhost:8888';
const EMAIL = 'fake@ponyft.com';
const PASS = '123456';
const SPACE = '7662408410528219136';
const BOT = '7662560621514194944';
const APP = '7662918773040480256';
const WF = '7662919178956832768';

const CHROME_CANDIDATES = [
  process.env.HOME +
    '/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
  process.env.HOME +
    '/Library/Caches/ms-playwright/chromium-1200/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function chromePath() {
  for (const p of CHROME_CANDIDATES) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error('Chrome not found');
}

async function shot(page, rel, fullPage = false) {
  const file = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await sleep(600);
  await page.screenshot({ path: file, fullPage });
  console.log('SHOT', rel);
}

async function safe(name, fn) {
  try {
    console.log('>>', name);
    await fn();
  } catch (e) {
    console.error('!!', name, String(e.message || e).slice(0, 240));
  }
}

async function ensureLogin(page) {
  await page.goto(BASE + '/sign', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await sleep(1500);
  if (!page.url().includes('/sign')) {
    console.log('already logged in', page.url());
    return;
  }
  // try email/password fields
  const email = page.locator('input[type="email"], input[placeholder*="邮箱"], input[placeholder*="邮"], input').first();
  await email.click({ timeout: 10000 });
  await email.fill(EMAIL);
  const pass = page.locator('input[type="password"]').first();
  await pass.fill(PASS);
  await page.getByRole('button', { name: /登录|登 录|Log ?in|Sign/i }).first().click();
  await sleep(2500);
  console.log('after login', page.url());
}

async function main() {
  const browser = await chromium.launch({
    executablePath: chromePath(),
    headless: true,
    args: ['--window-size=1440,900'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  await ensureLogin(page);

  // ---- P00 / develop ----
  await safe('00 develop', async () => {
    await page.goto(`${BASE}/space/${SPACE}/develop`, { waitUntil: 'networkidle', timeout: 60000 });
    await shot(page, '00-setup/10-develop-home.png');
  });

  await safe('00 create modal', async () => {
    await page.getByRole('button', { name: /创建/ }).first().click();
    await sleep(800);
    await shot(page, '00-setup/11-create-modal.png');
    await page.keyboard.press('Escape');
  });

  await safe('00 admin model', async () => {
    await page.goto(`${BASE}/admin`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await sleep(2000);
    await shot(page, '00-setup/12-admin-home.png');
    // try model management
    const modelLink = page.getByText(/模型管理|Model/).first();
    if (await modelLink.count()) {
      await modelLink.click();
      await sleep(1200);
      await shot(page, '00-setup/13-model-list.png');
    }
  });

  // ---- P02 agent ----
  await safe('02 agent ide', async () => {
    await page.goto(`${BASE}/space/${SPACE}/bot/${BOT}`, { waitUntil: 'networkidle', timeout: 90000 });
    await sleep(2000);
    await shot(page, '02-agent/20-ide-full.png');
    await shot(page, '02-agent/21-persona.png');
  });

  await safe('02 preview focus', async () => {
    const preview = page.getByText(/预览与调试|预览/).first();
    if (await preview.count()) await preview.click().catch(() => {});
    await sleep(500);
    await shot(page, '02-agent/22-preview.png');
  });

  // ---- P04 knowledge / library ----
  await safe('04 library', async () => {
    await page.goto(`${BASE}/space/${SPACE}/library`, { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(1500);
    await shot(page, '04-knowledge/10-library.png');
    await page.getByRole('button', { name: /创建/ }).first().click();
    await sleep(800);
    await shot(page, '04-knowledge/11-create-menu.png');
    await page.keyboard.press('Escape');
  });

  // ---- P05 plugin ----
  await safe('05 explore', async () => {
    await page.goto(`${BASE}/explore`, { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(1500);
    await shot(page, '05-plugin/10-explore.png');
  });
  await safe('05 plugin list', async () => {
    await page.goto(`${BASE}/explore/plugin`, { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(1500);
    await shot(page, '05-plugin/11-plugin-list.png');
  });

  // ---- P07 project ----
  await safe('07 project', async () => {
    await page.goto(`${BASE}/space/${SPACE}/project-ide/${APP}`, { waitUntil: 'networkidle', timeout: 90000 });
    await sleep(2500);
    await shot(page, '07-project/10-ide.png');
  });

  // ---- P01 workflow ----
  await safe('01 workflow', async () => {
    // try common workflow URL patterns
    const urls = [
      `${BASE}/work_flow?space_id=${SPACE}&workflow_id=${WF}&project_id=${APP}`,
      `${BASE}/space/${SPACE}/project-ide/${APP}/workflow/${WF}`,
      `${BASE}/space/${SPACE}/workflow/${WF}`,
    ];
    for (const u of urls) {
      await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(() => {});
      await sleep(2500);
      if (page.url().includes('workflow') || page.url().includes('work_flow')) {
        await shot(page, '01-competitor-daily/10-canvas.png');
        break;
      }
    }
    // from project click workflow
    await page.goto(`${BASE}/space/${SPACE}/project-ide/${APP}`, { waitUntil: 'networkidle', timeout: 90000 });
    await sleep(2000);
    const wf = page.getByText(/daily_competitor|工作流/).first();
    if (await wf.count()) {
      await wf.click();
      await sleep(2500);
      await shot(page, '01-competitor-daily/11-from-project.png');
    }
  });

  // ---- P03 skills on agent ----
  await safe('03 skills', async () => {
    await page.goto(`${BASE}/space/${SPACE}/bot/${BOT}`, { waitUntil: 'networkidle', timeout: 90000 });
    await sleep(2000);
    await shot(page, '03-skills/10-skills-area.png');
    const addPlugin = page.getByText(/插件/).first();
    if (await addPlugin.count()) {
      await addPlugin.click();
      await sleep(1000);
      await shot(page, '03-skills/11-plugin-panel.png');
    }
  });

  // ---- P06 database create menu ----
  await safe('06 database menu', async () => {
    await page.goto(`${BASE}/space/${SPACE}/library`, { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(1200);
    await page.getByRole('button', { name: /创建/ }).first().click();
    await sleep(800);
    await shot(page, '06-database/10-create-menu.png');
    const db = page.getByText(/数据库/).first();
    if (await db.count()) {
      await db.click();
      await sleep(1200);
      await shot(page, '06-database/11-create-form.png');
      await page.keyboard.press('Escape');
    } else {
      await page.keyboard.press('Escape');
    }
  });

  // ---- P08 publish / settings ----
  await safe('08 agent publish', async () => {
    await page.goto(`${BASE}/space/${SPACE}/bot/${BOT}`, { waitUntil: 'networkidle', timeout: 90000 });
    await sleep(1500);
    const pub = page.getByRole('button', { name: /发布/ }).first();
    if (await pub.count()) {
      await pub.click();
      await sleep(1500);
      await shot(page, '08-publish/20-publish-panel.png');
      await page.keyboard.press('Escape');
    }
  });

  await safe('08 api auth', async () => {
    // avatar → settings
    await page.goto(`${BASE}/space/${SPACE}/develop`, { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(1000);
    // try open account menu - top right
    const avatar = page.locator('[class*="avatar"], [class*="Avatar"], img').last();
    await avatar.click({ timeout: 5000 }).catch(() => {});
    await sleep(800);
    await shot(page, '08-publish/21-avatar-menu.png');
    const settings = page.getByText(/设置|账号|API/).first();
    if (await settings.count()) {
      await settings.click();
      await sleep(1500);
      await shot(page, '08-publish/22-settings.png');
      const api = page.getByText(/API 授权|API授权|个人访问令牌|令牌/).first();
      if (await api.count()) {
        await api.click();
        await sleep(1000);
        await shot(page, '08-publish/23-api-auth.png');
      }
    }
  });

  // ---- P09 explore / chatflow hints ----
  await safe('09 explore', async () => {
    await page.goto(`${BASE}/explore`, { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(1200);
    await shot(page, '09-chatflow/10-explore.png');
  });

  await browser.close();
  console.log('DONE');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
