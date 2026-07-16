/**
 * Coze Loop 开源实战教程 · 界面演示截图（容错版）
 */
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'assets/coze-loop-practice');
const BASE = 'http://localhost:8082';
const EMAIL = `loop-demo-${Date.now()}@example.com`;
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

async function safe(name, fn) {
  try {
    console.log('>>', name);
    await fn();
  } catch (e) {
    console.error('!!', name, e.message?.slice(0, 200));
  }
}

async function goModule(page, name) {
  await page.getByRole('menuitem', { name, exact: true }).click();
  await sleep(1200);
}

async function main() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await (await browser.newContext({
    viewport: { width: 1440, height: 900 },
    locale: 'zh-CN',
  })).newPage();
  page.setDefaultTimeout(12000);

  // ===== P00 =====
  await page.goto(`${BASE}/auth/login`, { waitUntil: 'networkidle' });
  await shot(page, '00-setup/01-login.png');
  await page.getByPlaceholder('请输入邮箱').fill(EMAIL);
  await page.getByPlaceholder('请输入密码').fill(PASS);
  await shot(page, '00-setup/02-login-filled.png');
  await page.getByRole('button', { name: '注册' }).click();
  await page.waitForURL(/\/console\//, { timeout: 30000 });
  await sleep(2000);
  await shot(page, '00-setup/03-home-prompts.png');
  await shot(page, '00-setup/04-sidebar.png');

  await safe('user-menu', async () => {
    await page.locator('[aria-haspopup="dialog"]').last().click();
    await sleep(600);
    await shot(page, '00-setup/05-user-menu.png');
    const acc = page.getByText('账号设置');
    if (await acc.isVisible()) {
      await acc.click();
      await sleep(800);
      await shot(page, '00-setup/06-account-modal.png');
      await page.keyboard.press('Escape');
      await sleep(300);
    }
  });

  // ===== P01 Prompt =====
  await safe('prompt-create', async () => {
    await goModule(page, 'Prompt 开发');
    await shot(page, '01-prompt/01-list-empty.png');

    // 顶部带下拉的创建按钮 → 空白 Prompt
    await page.getByRole('button', { name: '创建 Prompt' }).first().click();
    await sleep(400);
    await shot(page, '01-prompt/02-create-menu.png');
    await page.getByRole('menuitem', { name: '空白 Prompt' }).click();
    await sleep(600);
    await shot(page, '01-prompt/03-create-dialog.png');

    const key = `demo_greeting_${Date.now().toString().slice(-6)}`;
    await page.getByRole('textbox', { name: 'Prompt Key*' }).fill(key);
    await page.getByRole('textbox', { name: 'Prompt 名称*' }).fill('问候助手Demo');
    await page.getByRole('textbox', { name: 'Prompt 描述' }).fill('实战教程演示：礼貌问候用户');
    await shot(page, '01-prompt/04-create-filled.png');
    await page.getByRole('button', { name: '确认' }).click();
    await sleep(2500);
    await shot(page, '01-prompt/05-develop.png');

    // 编辑系统/用户消息：找可见 textarea
    const areas = page.locator('textarea:visible');
    if (await areas.count()) {
      await areas.first().fill('你是友好助手，请用一句话问候 {{user_name}}');
      await sleep(400);
      await shot(page, '01-prompt/06-edit-template.png');
    }

    // 提交版本（若有）
    const submit = page.getByRole('button', { name: /提交版本|提交/ }).first();
    if (await submit.isVisible().catch(() => false)) {
      await submit.click();
      await sleep(800);
      await shot(page, '01-prompt/07-submit-version.png');
      const ok = page.getByRole('button', { name: /确认|确定/ }).last();
      if (await ok.isVisible().catch(() => false)) await ok.click();
      await sleep(1000);
    }
  });

  await safe('playground', async () => {
    await goModule(page, 'Playground');
    await shot(page, '01-prompt/08-playground.png');
  });

  await safe('prompt-list', async () => {
    await goModule(page, 'Prompt 开发');
    await shot(page, '01-prompt/09-list-with-item.png');
  });

  // ===== P02 Dataset =====
  await safe('dataset', async () => {
    await goModule(page, '评测集');
    await shot(page, '02-dataset/01-list.png');
    await page.getByRole('button', { name: /创建/ }).first().click();
    await sleep(1500);
    await shot(page, '02-dataset/02-create.png');

    // 名称
    const nameInput = page.locator('input:visible').first();
    await nameInput.fill(`评测集问候${Date.now().toString().slice(-4)}`);
    await shot(page, '02-dataset/03-named.png');

    // 尝试添加列名
    const colName = page.getByPlaceholder(/列名|字段|name/i).first();
    if (await colName.isVisible().catch(() => false)) {
      await colName.fill('input');
    }
    // 完成创建
    const done = page.getByRole('button', { name: /创建|完成|确定|提交|下一步/ }).last();
    if (await done.isVisible().catch(() => false)) {
      await done.click();
      await sleep(2000);
    }
    await shot(page, '02-dataset/04-after-create.png');

    // 详情页可能已进入
    const addData = page.getByRole('button', { name: /添加数据|新增|导入/ }).first();
    if (await addData.isVisible().catch(() => false)) {
      await addData.click();
      await sleep(800);
      await shot(page, '02-dataset/05-add-data.png');
      await page.keyboard.press('Escape');
    }
  });

  // ===== P03 Evaluator =====
  await safe('evaluator', async () => {
    await goModule(page, '评估器');
    await shot(page, '03-evaluator/01-list.png');

    // 预置 tab
    const tabs = page.locator('[role="tab"], .semi-tabs-tab');
    for (let i = 0; i < (await tabs.count()); i++) {
      const t = tabs.nth(i);
      const txt = await t.innerText();
      if (/预置|内置|builtin/i.test(txt)) {
        await t.click();
        await sleep(800);
        await shot(page, '03-evaluator/02-builtin.png');
      }
      if (/自建|自定义/i.test(txt)) {
        await t.click();
        await sleep(500);
      }
    }
    await shot(page, '03-evaluator/03-custom.png');

    await page.getByRole('button', { name: /创建/ }).first().click();
    await sleep(800);
    await shot(page, '03-evaluator/04-create-menu.png');

    // LLM
    const llm = page.getByText(/LLM|大模型评估器|Prompt 评估器/).first();
    if (await llm.isVisible().catch(() => false)) {
      await llm.click();
    } else {
      // 菜单项
      await page.getByRole('menuitem').first().click().catch(() => {});
    }
    await sleep(1500);
    await shot(page, '03-evaluator/05-create-llm.png');

    // 返回再进 Code
    await goModule(page, '评估器');
    await page.getByRole('button', { name: /创建/ }).first().click();
    await sleep(600);
    const code = page.getByText(/Code|代码评估器/).first();
    if (await code.isVisible().catch(() => false)) {
      await code.click();
      await sleep(1500);
      await shot(page, '03-evaluator/06-create-code.png');
    } else {
      // 直接拼 URL
      const m = page.url().match(/(\/console\/enterprise\/personal\/space\/\d+)/);
      if (m) {
        await page.goto(`${BASE}${m[1]}/evaluation/evaluators/create/code`);
        await sleep(1500);
        await shot(page, '03-evaluator/06-create-code.png');
      }
    }
  });

  // ===== P04 Experiment =====
  await safe('experiment', async () => {
    await goModule(page, '实验');
    await shot(page, '04-experiment/01-list.png');
    await page.getByRole('button', { name: /创建|新建/ }).first().click();
    await sleep(1500);
    await shot(page, '04-experiment/02-wizard.png');
    const inp = page.locator('input:visible').first();
    if (await inp.count()) {
      await inp.fill(`实验问候对比${Date.now().toString().slice(-4)}`);
      await shot(page, '04-experiment/03-basic.png');
    }
    const next = page.getByRole('button', { name: /下一步/ }).first();
    if (await next.isVisible().catch(() => false)) {
      await next.click();
      await sleep(1000);
      await shot(page, '04-experiment/04-dataset-step.png');
      if (await next.isVisible().catch(() => false)) {
        await next.click();
        await sleep(1000);
        await shot(page, '04-experiment/05-target-step.png');
      }
      if (await next.isVisible().catch(() => false)) {
        await next.click();
        await sleep(1000);
        await shot(page, '04-experiment/06-evaluator-step.png');
      }
    }
  });

  // ===== P05 Trace =====
  await safe('trace', async () => {
    await goModule(page, 'Trace');
    await shot(page, '05-trace/01-list.png');
    // 时间/筛选控件
    await shot(page, '05-trace/02-toolbar.png');
    const filter = page.getByRole('button', { name: /筛选|过滤/ }).first();
    if (await filter.isVisible().catch(() => false)) {
      await filter.click();
      await sleep(600);
      await shot(page, '05-trace/03-filters.png');
    }
  });

  // ===== P06 Tag =====
  await safe('tag', async () => {
    await goModule(page, '标签管理');
    await shot(page, '06-tag/01-list.png');
    await page.getByRole('button', { name: /创建|新建/ }).first().click();
    await sleep(1000);
    await shot(page, '06-tag/02-create.png');
    const inp = page.locator('input:visible').first();
    if (await inp.count()) {
      await inp.fill(`质量标签${Date.now().toString().slice(-4)}`);
      await shot(page, '06-tag/03-filled.png');
    }
    const ok = page.getByRole('button', { name: /创建|确定|确认|提交|完成/ }).last();
    if (await ok.isVisible().catch(() => false)) {
      await ok.click();
      await sleep(1500);
    }
    await shot(page, '06-tag/04-result.png');
  });

  // ===== P07 PAT =====
  await safe('pat', async () => {
    await page.locator('[aria-haspopup="dialog"]').last().click();
    await sleep(500);
    await page.getByText('账号设置').click();
    await sleep(800);
    await shot(page, '07-pat/01-account.png');
    // 找 PAT tab
    const tabs = page.locator('[role="tab"], .semi-tabs-tab, .semi-tabs-tab-button');
    for (let i = 0; i < (await tabs.count()); i++) {
      const txt = await tabs.nth(i).innerText();
      if (/API|授权|令牌|Personal/i.test(txt)) {
        await tabs.nth(i).click();
        await sleep(800);
        break;
      }
    }
    // 也可能是侧栏文字
    const patLabel = page.getByText(/API 授权|个人访问令牌|Personal Access/i).first();
    if (await patLabel.isVisible().catch(() => false)) await patLabel.click();
    await sleep(600);
    await shot(page, '07-pat/02-pat-tab.png');
    const create = page.getByRole('button', { name: /创建|新建|添加/ }).first();
    if (await create.isVisible().catch(() => false)) {
      await create.click();
      await sleep(800);
      await shot(page, '07-pat/03-create.png');
      const name = page.locator('[role="dialog"] input:visible, .semi-modal input:visible').first();
      if (await name.count()) {
        await name.fill('教程演示Token');
        await shot(page, '07-pat/04-filled.png');
      }
      const ok = page.getByRole('button', { name: /创建|确定|确认|生成/ }).last();
      if (await ok.isVisible().catch(() => false)) {
        await ok.click();
        await sleep(1000);
        await shot(page, '07-pat/05-created.png');
      }
    }
  });

  fs.writeFileSync(
    path.join(OUT, 'demo-account.json'),
    JSON.stringify({ email: EMAIL, password: PASS }, null, 2),
  );
  console.log('DONE', EMAIL);
  await browser.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
