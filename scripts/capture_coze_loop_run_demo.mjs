/**
 * 精确演示：填 Prompt 消息 → 选 Claude → 运行 → 灌评测集 → 建评估器 → 跑实验 → Trace
 */
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, '../assets/coze-loop-practice');
const BASE = 'http://localhost:8082';
const EMAIL = `loop-run-${Date.now()}@example.com`;
const PASS = 'LoopDemo123!';
const CHROME =
  process.env.HOME +
  '/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function shot(page, rel) {
  const file = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await sleep(500);
  await page.screenshot({ path: file });
  console.log('SHOT', rel);
}

async function typeIntoEditor(page, index, text) {
  // CodeMirror / contenteditable / textarea
  const candidates = [
    page.locator('.cm-content[contenteditable="true"]'),
    page.locator('[contenteditable="true"]'),
    page.locator('.monaco-editor textarea'),
    page.locator('textarea'),
  ];
  for (const loc of candidates) {
    const n = await loc.count();
    if (n > index) {
      const el = loc.nth(index);
      await el.click({ force: true });
      await sleep(200);
      await page.keyboard.press('Meta+A');
      await page.keyboard.type(text, { delay: 15 });
      console.log('typed into', index, 'via', await el.evaluate((e) => e.className || e.tagName));
      return true;
    }
  }
  // click placeholder text then type
  const ph = page.getByText('请输入内容').nth(index);
  if (await ph.isVisible().catch(() => false)) {
    await ph.click();
    await page.keyboard.type(text, { delay: 15 });
    return true;
  }
  return false;
}

async function pickClaude(page) {
  const trigger = page.getByText('请选择模型').first();
  if (await trigger.isVisible().catch(() => false)) {
    await trigger.click();
  } else {
    // already selected? open anyway
    const sel = page.locator('.semi-select').filter({ hasText: /Claude|Sonnet|模型/ }).first();
    if (await sel.isVisible().catch(() => false)) await sel.click();
  }
  await sleep(800);
  const opt = page.getByText('Claude Sonnet', { exact: true }).first();
  await opt.waitFor({ state: 'visible', timeout: 10000 });
  await opt.click();
  await sleep(800);
  console.log('picked Claude');
}

async function main() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await (
    await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'zh-CN' })
  ).newPage();
  page.setDefaultTimeout(30000);

  await page.goto(`${BASE}/auth/login`, { waitUntil: 'networkidle' });
  await page.getByPlaceholder('请输入邮箱').fill(EMAIL);
  await page.getByPlaceholder('请输入密码').fill(PASS);
  await page.getByRole('button', { name: '注册' }).click();
  await page.waitForURL(/\/console\//, { timeout: 30000 });
  await sleep(2000);
  const prefix = page.url().match(/(\/console\/enterprise\/personal\/space\/\d+)/)[1];
  console.log(EMAIL, prefix);

  // ---- Prompt create ----
  await page.getByRole('button', { name: '创建 Prompt' }).first().click();
  await sleep(300);
  await page.getByRole('menuitem', { name: '空白 Prompt' }).click();
  await sleep(500);
  const key = `run_greet_${Date.now().toString().slice(-5)}`;
  await page.getByRole('textbox', { name: 'Prompt Key*' }).fill(key);
  await page.getByRole('textbox', { name: 'Prompt 名称*' }).fill('Claude问候演示');
  await page.getByRole('button', { name: '确认' }).click();
  await sleep(2500);
  await shot(page, '01-prompt/05-develop.png');

  // fill system + user
  const ok1 = await typeIntoEditor(page, 0, '你是礼貌助手，用一句中文问候用户，称呼对方名字。');
  console.log('system', ok1);
  // ensure user message exists
  const add = page.getByRole('button', { name: /添加消息/ });
  // 默认可能已有 System + User
  const ok2 = await typeIntoEditor(page, 1, '我叫小明，请问候我');
  console.log('user', ok2);
  if (!ok2) {
    await add.click();
    await sleep(400);
    await typeIntoEditor(page, 1, '我叫小明，请问候我');
  }
  await shot(page, '01-prompt/06-edit-template.png');

  await pickClaude(page);
  await shot(page, '01-prompt/10-model-selected.png');

  // debug input + run
  const debugBox = page.getByPlaceholder(/请输入问题测试/);
  if (await debugBox.isVisible().catch(() => false)) {
    await debugBox.fill('请按模板问候');
  }
  const runBtn = page.locator('button').filter({ hasText: /^运行$/ }).last();
  await runBtn.click({ timeout: 10000 });
  console.log('clicked run, waiting...');
  // wait for assistant content or error toast
  await sleep(12000);
  await shot(page, '01-prompt/11-debug-result.png');

  // submit version
  const submit = page.getByRole('button', { name: /提交新版/ });
  if (await submit.isEnabled().catch(() => false)) {
    await submit.click();
    await sleep(800);
    await shot(page, '01-prompt/07-submit-version.png');
    const ver = page.locator('.semi-modal input:visible').first();
    if (await ver.count()) await ver.fill('0.0.1');
    await page.locator('.semi-modal button').filter({ hasText: /确认|确定|提交/ }).last().click();
    await sleep(1500);
    await shot(page, '01-prompt/12-version-done.png');
  }

  // ---- Playground with content ----
  await page.goto(`${BASE}${prefix}/pe/playground`);
  await sleep(1500);
  await typeIntoEditor(page, 0, '用一句话介绍你自己，说你是 Claude。');
  await pickClaude(page).catch(() => {});
  await shot(page, '01-prompt/08-playground.png');
  await page.locator('button').filter({ hasText: /^运行$/ }).last().click();
  await sleep(12000);
  await shot(page, '01-prompt/13-playground-result.png');

  // ---- Dataset ----
  await page.goto(`${BASE}${prefix}/evaluation/datasets/create`);
  await sleep(1200);
  await page.getByPlaceholder('请输入评测集名称').fill(`问候集${Date.now().toString().slice(-4)}`);
  await page.getByPlaceholder('请输入评测集描述').fill('Claude 闭环演示');
  await shot(page, '02-dataset/03-named.png');
  await shot(page, '02-dataset/04-schema.png');
  await page.getByRole('button', { name: '创建', exact: true }).click();
  await sleep(2500);
  const dsUrl = page.url();
  const datasetId = (dsUrl.match(/datasets\/(\d+)/) || [])[1];
  console.log('dataset', datasetId, dsUrl);
  await shot(page, '02-dataset/05-detail.png');

  // add item - try several buttons
  for (const name of ['添加数据', '新增数据', '手动添加', '添加']) {
    const b = page.getByRole('button', { name: new RegExp(name) }).first();
    if (await b.isVisible().catch(() => false)) {
      console.log('click', name);
      await b.click();
      break;
    }
  }
  await sleep(1000);
  await shot(page, '02-dataset/05-add-data.png');
  // fill fields in drawer/modal
  const fields = page.locator('.semi-sidesheet textarea, .semi-modal textarea, [role="dialog"] textarea, .semi-sidesheet input, .semi-modal input');
  console.log('item fields', await fields.count());
  // Prefer labeled areas - type into all visible text inputs in panel
  const panel = page.locator('.semi-sidesheet, .semi-modal, [role="dialog"]').last();
  const tas = panel.locator('textarea:visible, input:visible');
  const tc = await tas.count();
  console.log('panel inputs', tc);
  if (tc >= 1) await tas.nth(0).fill('你好，我叫小明');
  if (tc >= 2) await tas.nth(1).fill('你好小明，很高兴认识你！');
  await shot(page, '02-dataset/06-item-filled.png');
  await panel.locator('button').filter({ hasText: /确认|确定|保存|提交|创建/ }).last().click().catch(() => {});
  await sleep(1500);
  await shot(page, '02-dataset/07-item-list.png');

  // ---- Evaluator ----
  await page.goto(`${BASE}${prefix}/evaluation/evaluators/create/llm`);
  await sleep(2000);
  await page.locator('input:visible').first().fill(`礼貌评估${Date.now().toString().slice(-4)}`);
  await pickClaude(page).catch(() => {});
  await shot(page, '03-evaluator/07-llm-configured.png');
  // 可能需要保存草稿
  const saveEv = page.locator('button:visible').filter({ hasText: /保存|创建|提交/ }).first();
  if (await saveEv.isVisible().catch(() => false)) await saveEv.click();
  await sleep(2000);
  await shot(page, '03-evaluator/08-llm-detail.png');

  // ---- Experiment ----
  await page.goto(`${BASE}${prefix}/evaluation/experiments/create`);
  await sleep(1500);
  await page.locator('input:visible').first().fill(`问候实验${Date.now().toString().slice(-4)}`);
  await shot(page, '04-experiment/03-basic.png');
  await page.getByRole('button', { name: /下一步/ }).click();
  await sleep(1500);
  await shot(page, '04-experiment/04-dataset-step.png');
  // pick dataset - click select
  const dsSelect = page.locator('.semi-select').first();
  await dsSelect.click();
  await sleep(600);
  await page.locator('.semi-select-option').first().click().catch(async () => {
    await page.getByText(/问候集/).first().click();
  });
  await sleep(500);
  // version select if any
  const verSel = page.locator('.semi-select').nth(1);
  if (await verSel.isVisible().catch(() => false)) {
    await verSel.click();
    await sleep(400);
    await page.locator('.semi-select-option').first().click().catch(() => {});
  }
  await shot(page, '04-experiment/04b-dataset-picked.png');
  await page.getByRole('button', { name: /下一步/ }).click();
  await sleep(1200);
  await shot(page, '04-experiment/05-target-step.png');
  // skip or pick prompt
  const next = page.getByRole('button', { name: /下一步/ });
  if (await next.isVisible()) await next.click();
  await sleep(1200);
  await shot(page, '04-experiment/06-evaluator-step.png');
  if (await next.isVisible()) await next.click();
  await sleep(1200);
  await shot(page, '04-experiment/07-confirm.png');
  const go = page.locator('button:visible').filter({ hasText: /启动实验|创建实验|提交|启动|确认创建|完成/ }).last();
  await go.click().catch(async () => {
    await page.getByRole('button', { name: /启动|创建|提交/ }).last().click();
  });
  await sleep(8000);
  await shot(page, '04-experiment/08-running.png');
  await sleep(15000);
  await shot(page, '04-experiment/09-result.png');

  // ---- Trace ----
  await page.goto(`${BASE}${prefix}/observation/traces`);
  await sleep(2500);
  await shot(page, '05-trace/01-list.png');
  const firstRow = page.locator('table tbody tr, .semi-table-body .semi-table-row').first();
  if (await firstRow.isVisible().catch(() => false)) {
    await firstRow.click();
    await sleep(1500);
    await shot(page, '05-trace/04-detail.png');
  }

  // check logs hint
  fs.writeFileSync(path.join(OUT, 'demo-meta.json'), JSON.stringify({ email: EMAIL, prefix, key }, null, 2));
  console.log('DONE');
  await browser.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
