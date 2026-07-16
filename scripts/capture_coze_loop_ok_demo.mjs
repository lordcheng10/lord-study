/**
 * 修复 temperature/top_p 冲突后：跑通 Claude Prompt 调试 + Playground + Trace
 */
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, '../assets/coze-loop-practice');
const BASE = 'http://localhost:8082';
const EMAIL = `loop-ok-${Date.now()}@example.com`;
const PASS = 'LoopDemo123!';
const CHROME =
  process.env.HOME +
  '/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function shot(page, rel) {
  const file = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await sleep(400);
  await page.screenshot({ path: file });
  console.log('SHOT', rel);
}

async function fillCm(page, index, text) {
  const el = page.locator('.cm-content[contenteditable="true"]').nth(index);
  await el.click({ force: true });
  await sleep(150);
  await page.keyboard.press('Meta+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.type(text, { delay: 10 });
  // blur to commit
  await page.keyboard.press('Tab');
  await sleep(300);
  await page.locator('body').click({ position: { x: 10, y: 10 } });
  await sleep(300);
}

async function pickClaude(page) {
  const already = page.locator('.semi-select').filter({ hasText: 'Claude Sonnet' }).first();
  if (await already.isVisible().catch(() => false)) {
    console.log('already Claude');
    return;
  }
  await page.getByText('请选择模型').first().click();
  await sleep(600);
  await page.getByText('Claude Sonnet', { exact: true }).first().click();
  await sleep(600);
}

async function main() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await (
    await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'zh-CN' })
  ).newPage();
  page.setDefaultTimeout(20000);

  await page.goto(`${BASE}/auth/login`, { waitUntil: 'networkidle' });
  await page.getByPlaceholder('请输入邮箱').fill(EMAIL);
  await page.getByPlaceholder('请输入密码').fill(PASS);
  await page.getByRole('button', { name: '注册' }).click();
  await page.waitForURL(/console/, { timeout: 30000 });
  await sleep(2000);
  const prefix = page.url().match(/(\/console\/enterprise\/personal\/space\/\d+)/)[1];

  // Create prompt
  await page.getByRole('button', { name: '创建 Prompt' }).first().click();
  await page.getByRole('menuitem', { name: '空白 Prompt' }).click();
  await sleep(400);
  await page.getByRole('textbox', { name: 'Prompt Key*' }).fill(`ok_${Date.now().toString().slice(-6)}`);
  await page.getByRole('textbox', { name: 'Prompt 名称*' }).fill('Claude成功问候');
  await page.getByRole('button', { name: '确认' }).click();
  await sleep(2500);

  // Only System message by default? Add user if needed
  let cmCount = await page.locator('.cm-content[contenteditable="true"]').count();
  console.log('cm before', cmCount);
  if (cmCount < 2) {
    await page.getByRole('button', { name: /添加消息/ }).click();
    await sleep(500);
  }
  cmCount = await page.locator('.cm-content[contenteditable="true"]').count();
  console.log('cm after', cmCount);

  await fillCm(page, 0, '你是礼貌助手。请用一句中文问候用户。');
  if (cmCount >= 2) {
    await fillCm(page, 1, '我叫小明');
  }
  await shot(page, '01-prompt/06-edit-template.png');

  await pickClaude(page);
  await shot(page, '01-prompt/10-model-selected.png');

  // Run — use template messages; also put debug question
  const debugBox = page.getByPlaceholder(/请输入问题测试/);
  if (await debugBox.isVisible()) {
    await debugBox.fill('你好');
  }
  await page.locator('button').filter({ hasText: /^运行$/ }).last().click();
  console.log('running...');
  // wait until assistant text appears or 20s
  for (let i = 0; i < 20; i++) {
    await sleep(1000);
    const body = await page.locator('text=小明').count();
    const err = await page.locator('text=失败').count();
    const hasReply = await page.evaluate(() => {
      const t = document.body.innerText;
      return t.includes('你好') && (t.includes('小明') || t.includes('高兴') || t.includes('欢迎') || t.includes('助手'));
    });
    if (hasReply) {
      console.log('got reply at', i);
      break;
    }
    if (await page.locator('.coz-toast, .semi-toast').filter({ hasText: /失败|错误|error/i }).count()) {
      console.log('toast error');
      break;
    }
  }
  await shot(page, '01-prompt/11-debug-result.png');

  // submit version
  const submit = page.getByRole('button', { name: /提交新版/ });
  if (await submit.isEnabled().catch(() => false)) {
    await submit.click();
    await sleep(800);
    const ver = page.locator('.semi-modal input:visible').first();
    if (await ver.count()) await ver.fill('0.0.1');
    await page.locator('.semi-modal button').filter({ hasText: /确认|确定|提交/ }).last().click();
    await sleep(1200);
    await shot(page, '01-prompt/12-version-done.png');
  }

  // Playground
  await page.goto(`${BASE}${prefix}/pe/playground`);
  await sleep(1500);
  await fillCm(page, 0, '用一句话介绍你自己：你是 Anthropic 的 Claude。');
  await pickClaude(page);
  await shot(page, '01-prompt/08-playground.png');
  await page.locator('button').filter({ hasText: /^运行$/ }).last().click();
  await sleep(15000);
  await shot(page, '01-prompt/13-playground-result.png');

  // Trace
  await page.goto(`${BASE}${prefix}/observation/traces`);
  await sleep(3000);
  await shot(page, '05-trace/01-list.png');
  const row = page.locator('.semi-table-body .semi-table-row, table tbody tr').first();
  if (await row.isVisible().catch(() => false)) {
    await row.click();
    await sleep(1500);
    await shot(page, '05-trace/04-detail.png');
  }

  // Dataset add item via URL detail - inspect buttons
  await page.goto(`${BASE}${prefix}/evaluation/datasets/create`);
  await sleep(1000);
  await page.getByPlaceholder('请输入评测集名称').fill(`闭环集${Date.now().toString().slice(-4)}`);
  await page.getByRole('button', { name: '创建', exact: true }).click();
  await sleep(2000);
  await shot(page, '02-dataset/05-detail.png');
  console.log('detail buttons', (await page.locator('button:visible').allInnerTexts()).slice(0, 20));

  // Experiment list after
  await page.goto(`${BASE}${prefix}/evaluation/experiments/list`);
  await sleep(1000);
  await shot(page, '04-experiment/01-list.png');

  fs.writeFileSync(path.join(OUT, 'demo-meta.json'), JSON.stringify({ email: EMAIL, prefix }, null, 2));
  console.log('DONE');
  await browser.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
