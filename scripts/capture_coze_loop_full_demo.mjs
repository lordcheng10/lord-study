/**
 * 配好 Claude 后：补全 Prompt 调试 / 评测集灌数 / 评估器 / 实验 / Trace 截图
 */
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'assets/coze-loop-practice');
const BASE = 'http://localhost:8082';
const EMAIL = `loop-full-${Date.now()}@example.com`;
const PASS = 'LoopDemo123!';
const CHROME =
  process.env.HOME +
  '/Library/Caches/ms-playwright/chromium-1217/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function shot(page, rel) {
  const file = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await sleep(600);
  await page.screenshot({ path: file });
  console.log('SHOT', rel);
}

async function safe(name, fn) {
  try {
    console.log('>>', name);
    await fn();
  } catch (e) {
    console.error('!!', name, (e.message || '').slice(0, 300));
    try {
      if (pageRef) await shot(pageRef, `errors/${name}.png`);
    } catch (_) {}
  }
}
let pageRef;

async function selectModel(page) {
  // 常见：请选择模型 / 模型配置下拉
  const triggers = [
    page.getByText('请选择模型').first(),
    page.locator('text=请选择模型').first(),
    page.locator('[class*="model"]').locator('input, .semi-select').first(),
  ];
  for (const t of triggers) {
    if (await t.isVisible().catch(() => false)) {
      await t.click();
      await sleep(800);
      break;
    }
  }
  // 点 Claude
  const opt = page.getByText(/Claude|claude-sonnet/i).first();
  if (await opt.isVisible().catch(() => false)) {
    await opt.click();
    await sleep(800);
    return true;
  }
  // 列表项
  const item = page.locator('.semi-select-option, [role="option"], .semi-list-item').filter({ hasText: /Claude|Sonnet/i }).first();
  if (await item.isVisible().catch(() => false)) {
    await item.click();
    await sleep(800);
    return true;
  }
  console.log('model select failed, dump options');
  return false;
}

async function main() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await (
    await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'zh-CN' })
  ).newPage();
  pageRef = page;
  page.setDefaultTimeout(25000);

  // login/register
  await page.goto(`${BASE}/auth/login`, { waitUntil: 'networkidle' });
  await page.getByPlaceholder('请输入邮箱').fill(EMAIL);
  await page.getByPlaceholder('请输入密码').fill(PASS);
  await page.getByRole('button', { name: '注册' }).click();
  await page.waitForURL(/\/console\//, { timeout: 30000 });
  await sleep(2000);
  const prefix = page.url().match(/(\/console\/enterprise\/personal\/space\/\d+)/)[1];
  console.log('prefix', prefix, EMAIL);
  await shot(page, '00-setup/03-home-prompts.png');

  // ========== Prompt + debug ==========
  let promptId = '';
  await safe('prompt-full', async () => {
    await page.getByRole('button', { name: '创建 Prompt' }).first().click();
    await sleep(400);
    await page.getByRole('menuitem', { name: '空白 Prompt' }).click();
    await sleep(600);
    const key = `demo_greet_${Date.now().toString().slice(-5)}`;
    await page.getByRole('textbox', { name: 'Prompt Key*' }).fill(key);
    await page.getByRole('textbox', { name: 'Prompt 名称*' }).fill('问候助手Claude');
    await page.getByRole('textbox', { name: 'Prompt 描述' }).fill('Claude 实战演示 Prompt');
    await page.getByRole('button', { name: '确认' }).click();
    await sleep(2500);
    promptId = (page.url().match(/prompts\/(\d+)/) || [])[1] || '';
    console.log('promptId', promptId);
    await shot(page, '01-prompt/05-develop.png');

    // 添加 system / user 消息
    const addMsg = page.getByRole('button', { name: /添加消息/ }).first();
    if (await addMsg.isVisible().catch(() => false)) {
      await addMsg.click();
      await sleep(500);
    }
    // 填第一个可见 textarea
    const areas = page.locator('textarea:visible');
    const n = await areas.count();
    console.log('textareas', n);
    if (n >= 1) {
      await areas.first().fill('你是一个礼貌的助手，用一句话中文问候用户。');
    }
    // 再加 user 消息
    if (await addMsg.isVisible().catch(() => false)) {
      await addMsg.click();
      await sleep(500);
      const areas2 = page.locator('textarea:visible');
      if ((await areas2.count()) >= 2) {
        await areas2.nth(1).fill('你好，我叫小明');
      }
    }
    await shot(page, '01-prompt/06-edit-template.png');

    // 选模型
    const okModel = await selectModel(page);
    console.log('model selected', okModel);
    await shot(page, '01-prompt/10-model-selected.png');

    // 运行调试
    const run = page.getByRole('button', { name: /^运行$|调试|发送/ }).first();
    // 也可能是预览区底部「运行」
    const runBtn = page.locator('button:visible').filter({ hasText: /^运行$/ }).first();
    if (await runBtn.isVisible().catch(() => false)) {
      await runBtn.click();
    } else if (await run.isVisible().catch(() => false)) {
      await run.click();
    } else {
      // 调试输入框回车
      const debugInput = page.getByPlaceholder(/请输入问题|测试/).first();
      if (await debugInput.isVisible().catch(() => false)) {
        await debugInput.fill('请问候一下');
        await debugInput.press('Enter');
      }
    }
    await sleep(8000); // wait LLM
    await shot(page, '01-prompt/11-debug-result.png');

    // 提交版本
    const submit = page.getByRole('button', { name: /提交新版|提交版本/ }).first();
    if (await submit.isEnabled().catch(() => false)) {
      await submit.click();
      await sleep(1000);
      await shot(page, '01-prompt/07-submit-version.png');
      // 版本号 / 确认
      const ver = page.locator('.semi-modal input:visible, [role="dialog"] input:visible').first();
      if (await ver.count()) {
        await ver.fill('0.0.1');
      }
      const ok = page.locator('.semi-modal button, [role="dialog"] button').filter({ hasText: /确认|确定|提交/ }).last();
      if (await ok.isVisible().catch(() => false)) await ok.click();
      await sleep(1500);
      await shot(page, '01-prompt/12-version-done.png');
    }

    await page.goto(`${BASE}${prefix}/pe/prompts`);
    await sleep(1000);
    await shot(page, '01-prompt/09-list-with-item.png');
  });

  // ========== Dataset with items ==========
  let datasetId = '';
  await safe('dataset-full', async () => {
    await page.goto(`${BASE}${prefix}/evaluation/datasets/create`);
    await sleep(1200);
    await shot(page, '02-dataset/02-create.png');
    await page.getByRole('textbox', { name: '名称*' }).fill(`问候评测集${Date.now().toString().slice(-4)}`);
    await page.getByRole('textbox', { name: '描述' }).fill('Claude 演示用评测集');
    await shot(page, '02-dataset/03-named.png');
    await shot(page, '02-dataset/04-schema.png');
    await page.getByRole('button', { name: '创建' }).click();
    await sleep(2500);
    datasetId = (page.url().match(/datasets\/(\d+)/) || [])[1] || '';
    console.log('datasetId', datasetId);
    await shot(page, '02-dataset/05-detail.png');

    // 添加数据
    const addData = page.locator('button:visible').filter({ hasText: /添加数据|新增数据|手动添加/ }).first();
    if (await addData.isVisible().catch(() => false)) {
      await addData.click();
      await sleep(1000);
      await shot(page, '02-dataset/05-add-data.png');
      // 填 input / reference
      const inputs = page.locator('.semi-modal textarea:visible, [role="dialog"] textarea:visible, .semi-sidesheet textarea:visible');
      const ic = await inputs.count();
      console.log('item textareas', ic);
      if (ic >= 1) await inputs.nth(0).fill('你好，我叫小明');
      if (ic >= 2) await inputs.nth(1).fill('你好小明，很高兴认识你！');
      // 也可能是 input
      const tin = page.locator('.semi-modal input:visible, [role="dialog"] input:visible');
      if ((await tin.count()) >= 1 && ic === 0) {
        await tin.nth(0).fill('你好，我叫小明');
      }
      await shot(page, '02-dataset/06-item-filled.png');
      await page.locator('button:visible').filter({ hasText: /确认|确定|保存|提交|创建/ }).last().click();
      await sleep(1500);
      await shot(page, '02-dataset/07-item-list.png');
    } else {
      // try 导入 or plus
      console.log('no add data button, buttons:', await page.locator('button:visible').allInnerTexts());
    }
  });

  // ========== Evaluator LLM ==========
  let evaluatorId = '';
  await safe('evaluator-full', async () => {
    await page.goto(`${BASE}${prefix}/evaluation/evaluators/create/llm`);
    await sleep(1500);
    await shot(page, '03-evaluator/05-create-llm.png');
    // 名称
    const name = page.locator('input:visible').first();
    await name.fill(`礼貌度评估${Date.now().toString().slice(-4)}`);
    await selectModel(page).catch(() => {});
    await shot(page, '03-evaluator/07-llm-configured.png');
    // 保存 / 创建
    const save = page.locator('button:visible').filter({ hasText: /创建|保存|提交/ }).last();
    if (await save.isVisible().catch(() => false)) {
      await save.click();
      await sleep(2000);
    }
    evaluatorId = (page.url().match(/evaluators\/(\d+)/) || [])[1] || '';
    console.log('evaluatorId', evaluatorId);
    await shot(page, '03-evaluator/08-llm-detail.png');

    // 调试若有
    const dbg = page.locator('button:visible').filter({ hasText: /调试|试运行|运行/ }).first();
    if (await dbg.isVisible().catch(() => false)) {
      await dbg.click();
      await sleep(5000);
      await shot(page, '03-evaluator/09-debug.png');
    }

    await page.goto(`${BASE}${prefix}/evaluation/evaluators?active_tab=builtin`);
    await sleep(1000);
    await shot(page, '03-evaluator/02-builtin.png');
  });

  // ========== Experiment ==========
  await safe('experiment-full', async () => {
    await page.goto(`${BASE}${prefix}/evaluation/experiments/create`);
    await sleep(1500);
    await shot(page, '04-experiment/02-wizard.png');
    const nameInp = page.locator('input:visible').first();
    await nameInp.fill(`问候实验${Date.now().toString().slice(-4)}`);
    await shot(page, '04-experiment/03-basic.png');
    const next = page.getByRole('button', { name: /下一步/ });
    await next.click();
    await sleep(1200);
    await shot(page, '04-experiment/04-dataset-step.png');
    // 选择评测集
    const ds = page.getByText(/问候评测集|评测集/).first();
    // 点选择器
    const selectDs = page.locator('.semi-select, [class*="select"]').filter({ hasText: /请选择|评测集/ }).first();
    if (await selectDs.isVisible().catch(() => false)) {
      await selectDs.click();
      await sleep(600);
      await page.locator('.semi-select-option').first().click().catch(async () => {
        await page.keyboard.press('Enter');
      });
    } else {
      // 表格行勾选
      const row = page.locator('tr, .semi-table-row').nth(1);
      if (await row.isVisible().catch(() => false)) await row.click();
    }
    await sleep(800);
    await shot(page, '04-experiment/04b-dataset-picked.png');
    if (await next.isVisible().catch(() => false)) await next.click();
    await sleep(1200);
    await shot(page, '04-experiment/05-target-step.png');
    // 选 Prompt 作为评测对象（可选）
    const promptOpt = page.getByText(/Prompt|提示词/).first();
    if (await promptOpt.isVisible().catch(() => false)) {
      await promptOpt.click().catch(() => {});
    }
    if (await next.isVisible().catch(() => false)) await next.click();
    await sleep(1200);
    await shot(page, '04-experiment/06-evaluator-step.png');
    if (await next.isVisible().catch(() => false)) await next.click();
    await sleep(1200);
    await shot(page, '04-experiment/07-confirm.png');
    const launch = page.locator('button:visible').filter({ hasText: /启动|创建|提交|完成|确认/ }).last();
    if (await launch.isVisible().catch(() => false)) {
      await launch.click();
      await sleep(5000);
      await shot(page, '04-experiment/08-running.png');
      await sleep(10000);
      await shot(page, '04-experiment/09-result.png');
    }
  });

  // ========== Trace ==========
  await safe('trace-full', async () => {
    await page.goto(`${BASE}${prefix}/observation/traces`);
    await sleep(2000);
    await shot(page, '05-trace/01-list.png');
    // 点第一行
    const row = page.locator('tr.semi-table-row, .semi-table-body tr, [class*="trace"]').nth(1);
    if (await row.isVisible().catch(() => false)) {
      await row.click();
      await sleep(1500);
      await shot(page, '05-trace/04-detail.png');
    } else {
      // 任意可点的 span 卡片
      const card = page.locator('[class*="span"], [class*="trace-item"]').first();
      if (await card.isVisible().catch(() => false)) {
        await card.click();
        await sleep(1500);
        await shot(page, '05-trace/04-detail.png');
      }
    }
    await shot(page, '05-trace/02-toolbar.png');
  });

  // Playground run
  await safe('playground-run', async () => {
    await page.goto(`${BASE}${prefix}/pe/playground`);
    await sleep(1500);
    await shot(page, '01-prompt/08-playground.png');
    await selectModel(page).catch(() => {});
    const areas = page.locator('textarea:visible');
    if (await areas.count()) {
      await areas.first().fill('用一句话介绍你自己');
    }
    const runBtn = page.locator('button:visible').filter({ hasText: /^运行$/ }).first();
    if (await runBtn.isVisible().catch(() => false)) {
      await runBtn.click();
      await sleep(8000);
      await shot(page, '01-prompt/13-playground-result.png');
    }
  });

  fs.writeFileSync(
    path.join(OUT, 'demo-meta.json'),
    JSON.stringify({ email: EMAIL, prefix, promptId, datasetId, evaluatorId, note: 'local only' }, null, 2),
  );
  console.log('DONE');
  await browser.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
