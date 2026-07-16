/**
 * 生成 Coze Loop 开源实战教程 HTML（风格对齐 Coze Studio 实战）
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const LESSONS = [
  {
    id: '00-setup',
    file: 'coze-loop-practice-00-setup.html',
    logo: 'P00',
    title: '环境启动 · 注册登录 · 侧栏导览',
    mins: '15 min',
    label: 'Coze Loop 开源实战 · P00 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/00-setup/01-login.png', '登录 / 注册页 /auth/login'],
      ['assets/coze-loop-practice/00-setup/02-login-filled.png', '填写邮箱与密码'],
      ['assets/coze-loop-practice/00-setup/03-home-prompts.png', '注册成功后进入 Prompt 开发首页'],
      ['assets/coze-loop-practice/00-setup/04-sidebar.png', '左侧导航：Prompt / 评测 / 观测 / 标签'],
      ['assets/coze-loop-practice/00-setup/05-user-menu.png', '右下角用户菜单'],
      ['assets/coze-loop-practice/00-setup/06-account-modal.png', '账号设置弹窗'],
    ],
    steps: [
      ['启动服务', '在 coze-loop 仓库根目录执行 <code>make compose-up</code>，浏览器打开 <code>http://localhost:8082</code>。若本机 8888 已被占用（例如同时跑 Coze Studio），把 <code>release/deployment/docker-compose/.env</code> 里的 <code>COZE_LOOP_APP_OPENAPI_PORT</code> 改成 <code>8889</code>。'],
      ['配置模型（跑 Prompt / 实验前必做）', '编辑 <code>release/deployment/docker-compose/conf/model_config.yaml</code>，填写火山方舟或 OpenAI 兼容的 <code>api_key</code> 与 <code>model</code>，然后 <code>make compose-restart-app</code>。开源版<strong>没有</strong>「模型管理」页面，密钥只在服务端配置。'],
      ['注册 / 登录', '进入 <code>/auth/login</code>，用邮箱+密码注册；注册成功会自动进入 Personal Space。'],
      ['认识侧栏', '四大模块：<strong>Prompt 工程</strong>（开发 / Playground）、<strong>评测</strong>（评测集 / 评估器 / 实验）、<strong>观测</strong>（Trace）、<strong>标签</strong>。底部有文档 / GitHub 外链与账号入口。'],
    ],
    warn: 'Docker Desktop 内存建议 ≥ 12GB。本机若同时跑大量其它容器，RocketMQ broker 可能被 OOM（exit 137），可先停掉非 Coze 容器再 <code>docker compose up -d</code>。',
  },
  {
    id: '01-prompt',
    file: 'coze-loop-practice-01-prompt.html',
    logo: 'P01',
    title: 'Prompt 开发 · 版本 · Playground',
    mins: '25 min',
    label: 'Coze Loop 开源实战 · P01 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/01-prompt/01-list-empty.png', 'Prompt 列表空态'],
      ['assets/coze-loop-practice/01-prompt/02-create-menu.png', '创建 Prompt → 空白 Prompt'],
      ['assets/coze-loop-practice/01-prompt/03-create-dialog.png', '创建弹窗：Key / 名称 / 描述'],
      ['assets/coze-loop-practice/01-prompt/04-create-filled.png', '填写合法 Prompt Key（字母开头）'],
      ['assets/coze-loop-practice/01-prompt/05-develop.png', '进入 Prompt 编排调试页'],
      ['assets/coze-loop-practice/01-prompt/08-playground.png', 'Playground 沙箱调试'],
      ['assets/coze-loop-practice/01-prompt/09-list-with-item.png', '列表中出现刚创建的 Prompt'],
    ],
    steps: [
      ['打开 Prompt 开发', '侧栏 → <strong>Prompt 开发</strong>，路径形如 <code>.../pe/prompts</code>。'],
      ['创建空白 Prompt', '点右上角 <strong>创建 Prompt</strong> → 菜单选 <strong>空白 Prompt</strong>。填写 Prompt Key（须匹配 <code>^[a-zA-Z][a-zA-Z0-9_.]*$</code>）、名称、描述，点<strong>确认</strong>。'],
      ['编排与调试', '进入开发页后编辑消息模板，可使用 <code>{{变量}}</code>；选择模型后可调试运行（需已配置 model_config）。'],
      ['提交版本', '调试满意后点<strong>提交版本</strong>，留下可回滚的版本记录；列表行可跳转「调用记录」到 Trace。'],
      ['Playground', '侧栏 → <strong>Playground</strong>：不落库的快速试验场，满意后再存成正式 Prompt。'],
    ],
    warn: '未配置模型时仍可创建/编辑 Prompt，但调试运行与实验评测会失败。',
  },
  {
    id: '02-dataset',
    file: 'coze-loop-practice-02-dataset.html',
    logo: 'P02',
    title: '评测集：建表 · 列配置 · 数据',
    mins: '20 min',
    label: 'Coze Loop 开源实战 · P02 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/02-dataset/01-list.png', '评测集列表'],
      ['assets/coze-loop-practice/02-dataset/02-create.png', '新建评测集页'],
      ['assets/coze-loop-practice/02-dataset/03-named.png', '填写名称与描述'],
      ['assets/coze-loop-practice/02-dataset/04-schema.png', '默认列 input / reference_output'],
      ['assets/coze-loop-practice/02-dataset/05-detail.png', '创建后的评测集详情'],
    ],
    steps: [
      ['进入评测集', '侧栏 → <strong>评测集</strong>。按钮文案是<strong>新建评测集</strong>（不是「创建」）。'],
      ['基本信息', '填写名称（必填）与描述。'],
      ['配置列', '默认已有 <code>input</code>（投递给评测对象）与 <code>reference_output</code>（参考答案）。可点<strong>添加列</strong>扩展字段。'],
      ['创建并灌数', '点底部<strong>创建</strong>进入详情；在「评测集」页签添加 / 导入数据行，并管理版本。'],
      ['关联实验', '详情另一页签可看关联的实验，方便从数据集追溯评测结果。'],
    ],
    warn: '列名与后续评估器入参、实验字段映射强相关，建表时先想清楚 schema。',
  },
  {
    id: '03-evaluator',
    file: 'coze-loop-practice-03-evaluator.html',
    logo: 'P03',
    title: '评估器：预置 · LLM · Code',
    mins: '20 min',
    label: 'Coze Loop 开源实战 · P03 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/03-evaluator/01-list.png', '评估器列表（自建）'],
      ['assets/coze-loop-practice/03-evaluator/02-builtin.png', '预置评估器浏览'],
      ['assets/coze-loop-practice/03-evaluator/04-create-menu.png', '新建入口'],
      ['assets/coze-loop-practice/03-evaluator/05-create-llm.png', '创建 LLM 评估器'],
      ['assets/coze-loop-practice/03-evaluator/06-create-code.png', '创建 Code 评估器'],
    ],
    steps: [
      ['打开评估器', '侧栏 → <strong>评估器</strong>。默认「自建」页签；切到「预置」可浏览内置模板。'],
      ['LLM 评估器', '新建 → LLM：用 Prompt 让模型打分（准确度、相关性等）。调试前需模型配置。'],
      ['Code 评估器', '新建 → Code：用 Python/JS（FaaS）写确定性规则，例如字符串相等、正则。'],
      ['版本与调试', '进入详情可改草稿、提交版本、对单条样例调试。'],
    ],
    warn: '实验可以不绑评估器（纯人工标注）；自动化打分再挂 LLM/Code 评估器。',
  },
  {
    id: '04-experiment',
    file: 'coze-loop-practice-04-experiment.html',
    logo: 'P04',
    title: '实验：五步向导 · 结果 · 对比',
    mins: '25 min',
    label: 'Coze Loop 开源实战 · P04 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/04-experiment/01-list.png', '实验列表'],
      ['assets/coze-loop-practice/04-experiment/02-wizard.png', '创建实验向导'],
      ['assets/coze-loop-practice/04-experiment/03-basic.png', '步骤1 基本信息'],
      ['assets/coze-loop-practice/04-experiment/04-dataset-step.png', '步骤2 选择评测集'],
      ['assets/coze-loop-practice/04-experiment/05-target-step.png', '步骤3 评测对象（可跳过）'],
      ['assets/coze-loop-practice/04-experiment/06-evaluator-step.png', '步骤4 评估器（可跳过）'],
    ],
    steps: [
      ['打开实验', '侧栏 → <strong>实验</strong> → 新建。'],
      ['五步向导', '① 基本信息 → ② 评测集（必选）→ ③ 评测对象（可选，如 Prompt）→ ④ 评估器（可选）→ ⑤ 确认启动。'],
      ['启动与查看', '启动后进详情：表格看每条结果，Chart 看聚合；可人工标注。'],
      ['对比实验', '列表勾选多个实验 → 进入对比页，并排看指标差异。'],
    ],
    warn: '若选了 LLM 评测对象或 LLM 评估器，必须先配好 model_config，否则任务会失败。',
  },
  {
    id: '05-trace',
    file: 'coze-loop-practice-05-trace.html',
    logo: 'P05',
    title: '观测 Trace：调用链与筛选',
    mins: '15 min',
    label: 'Coze Loop 开源实战 · P05 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/05-trace/01-list.png', 'Trace 列表（空或有数据）'],
      ['assets/coze-loop-practice/05-trace/02-toolbar.png', '时间范围与筛选工具条'],
    ],
    steps: [
      ['打开 Trace', '侧栏 → <strong>Trace</strong>。'],
      ['产生数据', '在 Prompt 开发页调试运行，或用 OpenAPI / SDK 上报 span；Prompt 列表「调用记录」会深链到带 <code>prompt_key</code> 过滤的 Trace。'],
      ['筛选', '按平台（prompt / cozeloop / ark）、时间、字段过滤；点开 span 看输入输出、耗时、token。'],
    ],
    warn: 'UI 不提供「上传 Trace 文件」；数据来自调试运行或 <code>/open-api/observability/...</code> 上报。',
  },
  {
    id: '06-tag',
    file: 'coze-loop-practice-06-tag.html',
    logo: 'P06',
    title: '标签管理与人工标注',
    mins: '10 min',
    label: 'Coze Loop 开源实战 · P06 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/06-tag/01-list.png', '标签列表'],
      ['assets/coze-loop-practice/06-tag/02-create.png', '新建标签'],
      ['assets/coze-loop-practice/06-tag/03-filled.png', '填写标签信息'],
      ['assets/coze-loop-practice/06-tag/04-result.png', '创建结果'],
    ],
    steps: [
      ['打开标签管理', '侧栏 → <strong>标签管理</strong>。'],
      ['创建标签', '新建标签，定义名称与取值，供实验详情里人工标注列使用。'],
      ['用在实验', '在实验详情对单条结果打标签，沉淀质检结论。'],
    ],
    warn: '标签是标注体系，不替代评估器自动打分，两者常配合使用。',
  },
  {
    id: '07-pat',
    file: 'coze-loop-practice-07-pat.html',
    logo: 'P07',
    title: '账号设置与 OpenAPI PAT',
    mins: '10 min',
    label: 'Coze Loop 开源实战 · P07 / 共 8 课',
    shots: [
      ['assets/coze-loop-practice/07-pat/00-usermenu.png', '用户菜单'],
      ['assets/coze-loop-practice/07-pat/01-account.png', '账号设置'],
      ['assets/coze-loop-practice/07-pat/02-pat-tab.png', 'API 授权 / PAT'],
      ['assets/coze-loop-practice/07-pat/03-create.png', '创建令牌'],
      ['assets/coze-loop-practice/07-pat/04-filled.png', '填写令牌名称'],
      ['assets/coze-loop-practice/07-pat/05-created.png', '创建成功（妥善保存明文）'],
    ],
    steps: [
      ['打开账号设置', '侧栏底部头像 → <strong>账号设置</strong>。'],
      ['创建 PAT', '切到 API 授权，创建个人访问令牌，复制明文（只显示一次）。'],
      ['调用 OpenAPI', '用 PAT 调 Loop OpenAPI（评测 / Trace 上报等）。注意：这是平台 API Token，不是 LLM 的 api_key。'],
      ['登出', '用户菜单 → 退出，回到 <code>/auth/login</code>。'],
    ],
    warn: 'PAT 泄露等同账号权限；教程演示 Token 用完请删除。',
  },
];

const NAV = LESSONS.map(
  (l) =>
    `<li><a href="${l.file}" class="nav-link">{{ACTIVE_${l.logo}}} · ${l.title.split('·')[0].trim()}</a></li>`,
).join('\n');

const SHARED_STYLE = `
.content{max-width:1100px}
.step-hdr{display:flex;align-items:center;gap:10px;margin:28px 0 12px}
.step-hdr .badge{width:34px;height:34px;border-radius:8px;background:linear-gradient(135deg,#06b6d4,#4f46e5);color:#fff;font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.step-hdr h2{margin:0;font-size:17px}
.shot{display:block;width:100%;max-width:920px;border-radius:10px;border:1px solid var(--border-color);margin:12px 0 4px;box-shadow:0 8px 24px rgba(0,0,0,.25)}
.shot-cap{font-size:12px;color:var(--text-muted);margin-bottom:14px}
.warn-box{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.35);border-radius:8px;padding:11px 14px;margin:10px 0;font-size:13px}
.chip{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;margin-right:6px;border:1px solid var(--border-color)}
.chip.on{background:rgba(34,197,94,.12);color:#4ade80;border-color:rgba(34,197,94,.35)}
.chip.mid{background:rgba(245,158,11,.12);color:#fbbf24;border-color:rgba(245,158,11,.35)}
`;

function sidebar(activeLogo) {
  const items = LESSONS.map((l) => {
    const active = l.logo === activeLogo ? ' active' : '';
    return `<li><a href="${l.file}" class="nav-link${active}">${l.logo} · ${l.title.split('·')[0].trim()}</a></li>`;
  }).join('\n');
  return `
<nav class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <div class="logo" style="background:linear-gradient(135deg,#06b6d4,#4f46e5);">${activeLogo}</div>
    <h2>Loop 实战</h2>
    <p class="version">开源版 UI 全功能</p>
  </div>
  <ul class="nav-list">
    <li class="nav-group-title">实战总目录</li>
    <li><a href="coze-loop-practice-tutorial.html" class="nav-link">总目录 Hub</a></li>
    <li class="nav-group-title">子课</li>
    ${items}
    <li class="nav-group-title">关联</li>
    <li><a href="coze-loop-day01.html" class="nav-link">Loop 源码 Day01</a></li>
    <li><a href="coze-studio-practice-tutorial.html" class="nav-link">Studio 实战</a></li>
    <li class="nav-group-title">导航</li>
    <li><a href="index.html" class="nav-link" style="color:var(--accent-cyan);">&larr; 首页</a></li>
  </ul>
</nav>`;
}

function lessonHtml(l, idx) {
  const prev = LESSONS[idx - 1];
  const next = LESSONS[idx + 1];
  const shots = l.shots
    .map(
      ([src, cap]) =>
        `<img class="shot" src="${src}" alt="${cap}"><p class="shot-cap">图：${cap}</p>`,
    )
    .join('\n');
  const steps = l.steps
    .map(
      ([t, body], i) => `
        <div class="step-hdr"><div class="badge">${i + 1}</div><h2>${t}</h2></div>
        <div class="card"><p style="font-size:13px;color:var(--text-secondary);line-height:1.75;margin:0">${body}</p></div>`,
    )
    .join('\n');
  const prevBtn = prev
    ? `<a href="${prev.file}" class="nav-btn prev"><span class="nav-btn-label">上一课</span><span class="nav-btn-title">${prev.logo} · ${prev.title.split('·')[0].trim()}</span></a>`
    : `<a href="coze-loop-practice-tutorial.html" class="nav-btn prev"><span class="nav-btn-label">返回</span><span class="nav-btn-title">实战总目录</span></a>`;
  const nextBtn = next
    ? `<a href="${next.file}" class="nav-btn next"><span class="nav-btn-label">下一课</span><span class="nav-btn-title">${next.logo} · ${next.title.split('·')[0].trim()}</span></a>`
    : `<a href="coze-loop-practice-tutorial.html" class="nav-btn next"><span class="nav-btn-label">完成</span><span class="nav-btn-title">回到总目录</span></a>`;

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${l.logo} · ${l.title} — Coze Loop 实战</title>
<link rel="stylesheet" href="style.css">
<style>${SHARED_STYLE}</style>
</head>
<body>
${sidebar(l.logo)}
<button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>
<main class="content" id="content">
  <div class="part-header">
    <span class="part-label">${l.label} · ≈${l.mins}</span>
    <h1 class="part-title">${l.title}</h1>
    <p class="part-desc">本地 <code>localhost:8082</code> 实录 · <span class="chip on">开源可用</span>
    上级：<a href="coze-loop-practice-tutorial.html">Loop 实战总目录</a></p>
  </div>
  <section class="section">
    <div class="section-header"><span class="section-number">★</span><h1>界面实录</h1></div>
    <div class="card">${shots}</div>
  </section>
  <section class="section">
    <div class="section-header"><span class="section-number">步</span><h1>操作步骤</h1></div>
    ${steps}
    <div class="warn-box" style="margin-top:16px">${l.warn}</div>
  </section>
  <div class="nav-buttons" style="margin-top:40px">
    ${prevBtn}
    ${nextBtn}
  </div>
</main>
<button class="scroll-top" id="scrollTop">↑</button>
<script src="app.js"></script>
</body>
</html>`;
}

function hubHtml() {
  const cards = LESSONS.map((l, i) => {
    const colors = ['#06b6d4', '#4f46e5', '#22c55e', '#f59e0b', '#8b5cf6', '#ef4444', '#14b8a6', '#6366f1'];
    return `<a class="day-card" href="${l.file}">
      <div class="top"><div class="num" style="background:${colors[i % colors.length]}">${l.logo}</div>
      <h3>${l.title}</h3></div>
      <p>${l.steps[0][1].replace(/<[^>]+>/g, '').slice(0, 80)}…</p>
      <div class="foot"><span class="mins">≈${l.mins}</span><span class="go">开始 →</span></div>
    </a>`;
  }).join('\n');

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Coze Loop 实战教程 · 总目录 — Lord Study</title>
<link rel="stylesheet" href="style.css">
<style>
.content{max-width:1180px}
.day-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.day-card{display:flex;flex-direction:column;gap:8px;background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:18px;text-decoration:none;transition:transform .2s,border-color .2s,box-shadow .2s}
.day-card:hover{transform:translateY(-4px);border-color:rgba(6,182,212,.45);box-shadow:0 12px 34px rgba(6,182,212,.10)}
.day-card .top{display:flex;align-items:center;gap:10px}
.day-card .num{width:42px;height:42px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff}
.day-card h3{font-size:15px;font-weight:700;color:var(--text-primary);margin:0;line-height:1.35}
.day-card p{font-size:12.5px;color:var(--text-secondary);margin:0;line-height:1.6;flex:1}
.day-card .foot{display:flex;align-items:center;justify-content:space-between;margin-top:4px}
.day-card .mins{font-size:11px;color:var(--text-muted)}
.day-card .go{font-size:12px;font-weight:600;color:#22d3ee}
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(90px,1fr));gap:8px;margin:12px 0}
.flow .f{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:8px;padding:10px;font-size:11.5px;text-align:center}
.flow .f b{display:block;color:#22d3ee;margin-bottom:3px;font-size:12.5px}
.ctable{width:100%;border-collapse:collapse;margin:12px 0;font-size:12.2px}
.ctable th,.ctable td{border:1px solid var(--border-color);padding:8px 9px;text-align:left;vertical-align:top}
.ctable th{background:var(--bg-secondary);color:var(--accent-cyan)}
.chip{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;border:1px solid var(--border-color)}
.chip.on{background:rgba(34,197,94,.12);color:#4ade80}
.chip.off{background:rgba(239,68,68,.10);color:#f87171}
.chip.mid{background:rgba(245,158,11,.12);color:#fbbf24}
.baby{border-left:3px solid var(--accent-green);background:rgba(34,197,94,.06);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.baby .t{font-weight:700;color:var(--accent-green);display:block;margin-bottom:4px}
</style>
</head>
<body>
<nav class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <div class="logo" style="background:linear-gradient(135deg,#06b6d4,#4f46e5);">实</div>
    <h2>Loop 实战</h2>
    <p class="version">开源版 UI 全功能课程序列</p>
  </div>
  <ul class="nav-list">
    <li class="nav-group-title">总目录</li>
    <li><a href="#intro" class="nav-link active" data-section="intro">开篇 · 怎么用</a></li>
    <li><a href="#map" class="nav-link" data-section="map">能力地图</a></li>
    <li><a href="#days" class="nav-link" data-section="days">全部实战子课</a></li>
    <li class="nav-group-title">子课快捷</li>
    ${LESSONS.map((l) => `<li><a href="${l.file}" class="nav-link">${l.logo} · ${l.title.split('·')[0].trim()}</a></li>`).join('\n')}
    <li class="nav-group-title">关联</li>
    <li><a href="coze-loop-day01.html" class="nav-link">Loop 源码课</a></li>
    <li><a href="coze-studio-practice-tutorial.html" class="nav-link">Studio 实战</a></li>
    <li><a href="index.html" class="nav-link" style="color:var(--accent-cyan);">&larr; 首页</a></li>
  </ul>
</nav>
<button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>
<main class="content" id="content">
  <div class="part-header">
    <span class="part-label">界面实操 · 本地 localhost:8082 · 截图来自真实部署</span>
    <h1 class="part-title">Coze Loop 实战教程（总目录）</h1>
    <p class="part-desc">按开源版<strong>真正能点的核心能力</strong>拆成 8 课：每课含步骤 + 截图。
    与 <a href="coze-loop-day01.html">Loop 源码课</a>互补——那边读引擎，这边点界面闭环。
    推荐起点：<a href="coze-loop-practice-00-setup.html">P00 环境与登录</a> → <a href="coze-loop-practice-01-prompt.html">P01 Prompt</a>。</p>
  </div>

  <section id="intro" class="section">
    <div class="section-header"><span class="section-number">00</span><h1>开篇 · 你要交付什么</h1></div>
    <div class="card">
      <div class="baby"><span class="t">一句话</span>
      在本地开源 Coze Loop 走通：<strong>配模型 → 写 Prompt → 建评测集 / 评估器 → 跑实验 → 看 Trace → 打标签 → 开 PAT</strong>。
      它不负责拖拽搭 Agent（那是 Coze Studio），而是给 Agent / Prompt 做「调优 + 质检 + 巡检」。
      </div>
      <div class="flow">
        <div class="f"><b>P00</b>环境</div>
        <div class="f"><b>P01</b>Prompt</div>
        <div class="f"><b>P02</b>评测集</div>
        <div class="f"><b>P03</b>评估器</div>
        <div class="f"><b>P04</b>实验</div>
        <div class="f"><b>P05</b>Trace</div>
        <div class="f"><b>P06</b>标签</div>
        <div class="f"><b>P07</b>PAT</div>
      </div>
    </div>
  </section>

  <section id="map" class="section">
    <div class="section-header"><span class="section-number">01</span><h1>开源能力地图</h1></div>
    <div class="card">
      <table class="ctable">
        <tr><th>模块</th><th>入口</th><th>开源</th><th>对应课</th></tr>
        <tr><td>登录 / 注册</td><td><code>/auth/login</code></td><td><span class="chip on">可用</span></td><td>P00</td></tr>
        <tr><td>Prompt 开发 / 版本</td><td><code>.../pe/prompts</code></td><td><span class="chip on">可用</span></td><td>P01</td></tr>
        <tr><td>Playground</td><td><code>.../pe/playground</code></td><td><span class="chip on">可用</span></td><td>P01</td></tr>
        <tr><td>评测集</td><td><code>.../evaluation/datasets</code></td><td><span class="chip on">可用</span></td><td>P02</td></tr>
        <tr><td>评估器 LLM/Code</td><td><code>.../evaluation/evaluators</code></td><td><span class="chip on">可用</span></td><td>P03</td></tr>
        <tr><td>实验</td><td><code>.../evaluation/experiments</code></td><td><span class="chip mid">跑通需模型</span></td><td>P04</td></tr>
        <tr><td>Trace</td><td><code>.../observation/traces</code></td><td><span class="chip on">可用</span></td><td>P05</td></tr>
        <tr><td>标签</td><td><code>.../tag/tag</code></td><td><span class="chip on">可用</span></td><td>P06</td></tr>
        <tr><td>PAT / OpenAPI</td><td>账号设置弹窗</td><td><span class="chip on">可用</span></td><td>P07</td></tr>
        <tr><td>模型管理 UI</td><td>—</td><td><span class="chip off">无</span></td><td>改 model_config.yaml</td></tr>
        <tr><td>空间 / 团队管理</td><td>—</td><td><span class="chip off">无</span></td><td>自动 Personal Space</td></tr>
      </table>
    </div>
  </section>

  <section id="days" class="section">
    <div class="section-header"><span class="section-number">02</span><h1>全部实战子课</h1></div>
    <div class="day-grid">${cards}</div>
  </section>
</main>
<button class="scroll-top" id="scrollTop">↑</button>
<script src="app.js"></script>
</body>
</html>`;
}

fs.writeFileSync(path.join(ROOT, 'coze-loop-practice-tutorial.html'), hubHtml());
LESSONS.forEach((l, i) => {
  fs.writeFileSync(path.join(ROOT, l.file), lessonHtml(l, i));
  console.log('wrote', l.file);
});
console.log('hub ok');
