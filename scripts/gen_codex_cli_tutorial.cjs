#!/usr/bin/env node
/**
 * Generate Codex CLI tutorial: index + 20 day pages.
 * Source of truth for content: openai/codex (codex-rs Rust workspace).
 * Usage: node scripts/gen_codex_cli_tutorial.js
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const ACCENT = "#10a37f";
const ACCENT2 = "#0d8c6d";
const GRAD = `linear-gradient(135deg,${ACCENT},${ACCENT2})`;

const DAYS = [
  { n: "01", title: "项目全景与目录地图", week: 1, mins: 30, blurb: "Codex CLI 是什么、和桌面端/IDE 的边界、仓库顶层与 codex-rs 关键 crate。" },
  { n: "02", title: "安装、登录与第一次对话", week: 1, mins: 30, blurb: "安装方式、ChatGPT / API Key 登录、交互模式发第一条任务、doctor 自检。" },
  { n: "03", title: "沙箱与审批（必读）", week: 1, mins: 35, blurb: "SandboxMode / AskForApproval 两层防护、常用 flag、源码枚举对照。" },
  { n: "04", title: "CLI 子命令全家桶", week: 1, mins: 30, blurb: "MultitoolCli：exec / login / mcp / resume / review / features … 用法地图。" },
  { n: "05", title: "TUI 交互与 Slash 命令", week: 1, mins: 35, blurb: "终端界面结构、高频 /model /permissions /plan /skills、!shell 捷径。" },
  { n: "06", title: "启动链：从 npm 到 TUI", week: 2, mins: 35, blurb: "codex.js 选平台二进制 → cli/main.rs 分发 → tui 挂载 in-process app-server。" },
  { n: "07", title: "Op 协议与 app-server", week: 2, mins: 35, blurb: "protocol::Op、JSON-RPC v2、TUI/exec/IDE 共用同一条控制面。" },
  { n: "08", title: "Agent Turn 主循环", week: 2, mins: 40, blurb: "UserInput → run_turn → 流式模型 → 工具调用 → 回填，核心引擎纵切。" },
  { n: "09", title: "配置分层与 config.toml", week: 2, mins: 30, blurb: "~/.codex/config.toml、profile、-c 覆盖、features 开关、schema。" },
  { n: "10", title: "认证与模型 Provider", week: 2, mins: 30, blurb: "login 流程、API Key、OSS/Ollama、model_provider 配置。" },
  { n: "11", title: "工具系统总览", week: 3, mins: 35, blurb: "spec_plan / router / handlers：shell、patch、MCP、web_search…" },
  { n: "12", title: "Shell、apply_patch 与沙箱执行", week: 3, mins: 40, blurb: "命令怎么进 Seatbelt/bwrap、补丁语言、execpolicy 规则。" },
  { n: "13", title: "MCP、Plugins 与扩展工具", week: 3, mins: 35, blurb: "codex mcp add、/mcp、Codex 自身当 MCP server、插件安装。" },
  { n: "14", title: "Skills 与 AGENTS.md", week: 3, mins: 30, blurb: "项目指令如何注入上下文、SKILL.md 发现与 /skills、/init。" },
  { n: "15", title: "Plan 模式与协作模式", week: 3, mins: 30, blurb: "Default vs Plan、/plan /goal /agent、多 agent 工具入口。" },
  { n: "16", title: "会话：resume / fork / rollout", week: 4, mins: 30, blurb: "会话如何落盘、恢复与分叉、compact 压缩上下文。" },
  { n: "17", title: "codex exec：非交互与 CI", week: 4, mins: 35, blurb: "--json / -o / schema、CI 安全默认、review 子命令。" },
  { n: "18", title: "TypeScript SDK 嵌入", week: 4, mins: 30, blurb: "sdk/typescript 如何包一层 CLI JSONL，脚本化控制 Agent。" },
  { n: "19", title: "app-server 与 IDE/桌面桥", week: 4, mins: 35, blurb: "富客户端共用协议、daemon / remote-control、和桌面端的关系。" },
  { n: "20", title: "收官串讲与学习路线", week: 4, mins: 30, blurb: "全链路回顾、必读文件清单、和 Claude Code / 桌面端对照、下一步。" },
];

const weekMeta = {
  1: { label: "第 1 周 · 会用 + 建立心智", span: "安装登录、安全默认、命令与 TUI" },
  2: { label: "第 2 周 · 核心引擎", span: "启动链、协议、Turn、配置、认证" },
  3: { label: "第 3 周 · 工具与扩展", span: "工具、沙箱执行、MCP、Skills、Plan" },
  4: { label: "第 4 周 · 工程化与收官", span: "会话、exec/CI、SDK、app-server、串讲" },
};

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function commonHead(title) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(title)} — Lord Study</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/rust.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/toml.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/javascript.min.js"></script>
<style>
.content{max-width:1100px}
.step-hdr{display:flex;align-items:center;gap:10px;margin:28px 0 12px}
.step-hdr .badge{width:34px;height:34px;border-radius:8px;background:${GRAD};color:#fff;font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.step-hdr h2{margin:0;font-size:17px}
.why{background:rgba(16,163,127,.07);border-left:3px solid ${ACCENT};border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px;color:var(--text-secondary);line-height:1.7}
.why b{color:#34d399}
.verify{font-size:12.5px;color:var(--accent-green);margin-top:10px;padding:8px 12px;background:rgba(34,197,94,.06);border-radius:8px;border-left:3px solid var(--accent-green)}
.warn-box{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.35);border-radius:8px;padding:11px 14px;margin:10px 0;font-size:13px}
.pitfall{border-left:3px solid #ef4444;background:rgba(239,68,68,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.pitfall .t{font-weight:700;color:#f87171;display:block;margin-bottom:4px}
.baby{border-left:3px solid var(--accent-green);background:rgba(34,197,94,.06);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.baby .t{font-weight:700;color:var(--accent-green);display:block;margin-bottom:4px}
.ask{border-left:3px solid #f59e0b;background:rgba(245,158,11,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.ask .t{font-weight:700;color:#f59e0b;display:block;margin-bottom:4px}
.essence{border-left:3px solid ${ACCENT};background:rgba(16,163,127,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.essence .t{font-weight:700;color:#6ee7b7;display:block;margin-bottom:4px}
.glossary{border-left:3px solid var(--accent-cyan);background:rgba(6,182,212,.06);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.glossary b{color:var(--accent-cyan)}
.ctable{width:100%;border-collapse:collapse;margin:12px 0;font-size:12.2px}
.ctable th,.ctable td{border:1px solid var(--border-color);padding:8px 9px;text-align:left;vertical-align:top;line-height:1.55}
.ctable th{background:var(--bg-secondary);color:#34d399;font-weight:700}
.ctable code{color:var(--accent-cyan);font-size:11px}
.fileref{display:inline-block;font-size:11px;background:rgba(16,163,127,.12);color:#6ee7b7;border:1px solid rgba(16,163,127,.35);border-radius:5px;padding:1px 7px;font-family:ui-monospace,monospace}
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:8px;margin:12px 0}
.flow .f{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:8px;padding:10px;font-size:11.5px;text-align:center}
.flow .f b{display:block;color:#34d399;margin-bottom:3px;font-size:12.5px}
.kbd{display:inline-block;font-family:ui-monospace,monospace;font-size:11px;padding:1px 6px;border-radius:4px;border:1px solid var(--border-color);background:var(--bg-secondary)}
.src{font-size:11.5px;color:var(--text-muted);margin-top:10px}
.src a{color:#6ee7b7}
.journey{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:12px 14px;margin:6px 0 16px}
.journey .jt{font-size:11px;color:var(--text-muted);margin-bottom:8px;letter-spacing:.04em}
.journey .steps{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.journey .st{font-size:11.5px;padding:5px 10px;border-radius:20px;background:var(--bg-card);border:1px solid var(--border-color);color:var(--text-muted);white-space:nowrap}
.journey .st.on{background:${GRAD};color:#fff;border-color:transparent;font-weight:700}
.journey .sep{color:var(--text-muted);font-size:12px}
.mod-map{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin:12px 0}
.mm{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:13px;border-left:3px solid var(--mc,${ACCENT})}
.mm h4{font-size:13.5px;margin:0 0 3px;color:var(--mc,${ACCENT});font-family:'SF Mono',monospace}
.mm p{font-size:12px;color:var(--text-secondary);margin:5px 0 0}
@media(max-width:768px){.mod-map{grid-template-columns:1fr}}
.term-hero{border-radius:10px;overflow:hidden;border:1px solid var(--border-color);margin:10px 0;font-family:ui-monospace,monospace}
.term-hero .bar{background:#2d2d3a;padding:7px 12px;display:flex;gap:6px;align-items:center}
.term-hero .bar i{width:10px;height:10px;border-radius:50%;display:block}
.term-hero .bar .r{background:#ff5f57}.term-hero .bar .y{background:#ffbd2e}.term-hero .bar .g{background:#28c840}
.term-hero .bar span{flex:1;text-align:center;font-size:11px;color:var(--text-muted)}
.term-hero .body{background:#0a0a12;padding:14px 16px;font-size:12.5px;line-height:1.7}
.term-hero .p{color:${ACCENT};font-weight:700}.term-hero .u{color:var(--accent-cyan)}.term-hero .o{color:var(--text-secondary)}.term-hero .k{color:var(--accent-green)}
.week-bar{display:flex;align-items:center;gap:12px;margin:36px 0 14px;padding-left:2px}
.week-bar .wk{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff;flex-shrink:0;background:${GRAD}}
.week-bar h2{font-size:17px;font-weight:700;margin:0}.week-bar span{font-size:12px;color:var(--text-muted)}
.day-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.day-card{display:flex;flex-direction:column;gap:8px;background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:18px;text-decoration:none;transition:transform .2s,border-color .2s,box-shadow .2s}
.day-card:hover{transform:translateY(-4px);border-color:rgba(16,163,127,.45);box-shadow:0 12px 34px rgba(16,163,127,.12)}
.day-card .top{display:flex;align-items:center;gap:10px}
.day-card .num{width:40px;height:40px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:#fff;font-family:'SF Mono',monospace;background:${GRAD}}
.day-card h3{font-size:15px;font-weight:700;color:var(--text-primary);margin:0;line-height:1.35}
.day-card p{font-size:12.5px;color:var(--text-secondary);margin:0;line-height:1.6;flex:1}
.day-card .foot{display:flex;align-items:center;justify-content:space-between;margin-top:4px}
.day-card .mins{font-size:11px;color:var(--text-muted)}
.day-card .go{font-size:12px;font-weight:600;color:${ACCENT}}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;background:rgba(34,197,94,.12);color:var(--accent-green)}
.loop-wrap{display:flex;justify-content:center;padding:14px 0 4px}
.aloop{position:relative;width:320px;height:320px}
.aloop .center{position:absolute;inset:0;margin:auto;width:120px;height:120px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:radial-gradient(circle,rgba(16,163,127,.14),transparent 70%);border-radius:50%}
.aloop .center b{font-size:15px;color:#34d399}.aloop .center small{font-size:10px;color:var(--text-muted)}
.aloop .ring{position:absolute;inset:0;border:1px dashed rgba(16,163,127,.35);border-radius:50%}
.aloop .node{position:absolute;width:96px;margin-left:-48px;left:50%;top:50%;margin-top:-26px;background:var(--bg-card);border:1px solid var(--border-color);border-radius:10px;padding:8px 6px;font-size:11px;text-align:center;color:var(--text-secondary)}
.aloop .node b{display:block;font-size:11.5px;color:var(--text-primary)}
.aloop .orbit{position:absolute;width:20px;height:20px;left:50%;top:50%;margin:-10px;border-radius:50%;background:#fff;box-shadow:0 0 12px 3px rgba(16,163,127,.8)}
@media(max-width:600px){.aloop{transform:scale(.85)}}
</style>
</head>
<body>`;
}

function dayShell({ day, navItems, journey, body, next, prev }) {
  const d = DAYS.find((x) => x.n === day);
  const prevLink = prev
    ? `<a href="codex-cli-day${prev.n}.html" class="nav-link" style="color:var(--accent-cyan);">&larr; Day ${prev.n} · ${esc(prev.title)}</a>`
    : `<a href="codex-cli-tutorial.html" class="nav-link" style="color:var(--accent-cyan);">&larr; 20 天总目录</a>`;
  const nextLink = next
    ? `<a href="codex-cli-day${next.n}.html" class="nav-link" style="color:var(--accent-green);">下一天 · ${esc(next.title)} &rarr;</a>`
    : `<a href="codex-cli-tutorial.html" class="nav-link" style="color:var(--accent-green);">返回总目录 &rarr;</a>`;

  return `${commonHead(`Day ${day} · ${d.title} — Codex CLI`)}
<nav class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <div class="logo" style="background:${GRAD};">${day}</div>
    <h2>Day ${day}</h2>
    <p class="version">${esc(d.title)} · Codex CLI</p>
  </div>
  <ul class="nav-list">
    <li class="nav-group-title">本日讲次</li>
    ${navItems}
    <li class="nav-group-title">导航</li>
    <li>${prevLink}</li>
    <li>${nextLink}</li>
  </ul>
</nav>
<button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>
<main class="content" id="content">
  <div class="part-header">
    <span class="part-label">Day ${day} / 共 20 天 · ${esc(weekMeta[d.week].label)}</span>
    <h1 class="part-title">${esc(d.title)}</h1>
    <p class="part-desc">${esc(d.blurb)}</p>
  </div>
  ${journey}
  ${body}
  <div style="display:flex;justify-content:space-between;margin:32px 0 16px;gap:12px;flex-wrap:wrap">
    ${prev ? `<a href="codex-cli-day${prev.n}.html" style="color:var(--accent-cyan);">&larr; Day ${prev.n}</a>` : `<a href="codex-cli-tutorial.html" style="color:var(--accent-cyan);">&larr; 总目录</a>`}
    ${next ? `<a href="codex-cli-day${next.n}.html" style="color:var(--accent-green);">Day ${next.n} · ${esc(next.title)} &rarr;</a>` : `<a href="codex-cli-tutorial.html" style="color:var(--accent-green);">返回总目录 &rarr;</a>`}
  </div>
</main>
<button class="scroll-top" id="scrollTop">↑</button>
<script src="app.js"></script>
<script>hljs.highlightAll();</script>
</body>
</html>`;
}

function journeyHtml(day) {
  const d = DAYS.find((x) => x.n === day);
  const weekDays = DAYS.filter((x) => x.week === d.week);
  const steps = weekDays
    .map((x, i) => {
      const on = x.n === day ? " on" : "";
      const sep = i < weekDays.length - 1 ? `<span class="sep">→</span>` : "";
      return `<span class="st${on}">D${x.n} ${esc(x.title.split("：")[0].split("（")[0])}</span>${sep}`;
    })
    .join("");
  return `<div class="journey"><div class="jt">📍 你在整门课的位置 · ${esc(weekMeta[d.week].label)}</div><div class="steps">${steps}</div></div>`;
}

function navFromLessons(lessons) {
  return lessons
    .map(
      (l, i) =>
        `<li><a href="#${l.id}" class="nav-link${i === 0 ? " active" : ""}" data-section="${l.id}">${esc(l.label)}</a></li>`
    )
    .join("\n    ");
}

function section(id, num, title, html) {
  return `<section id="${id}" class="section">
  <div class="section-header"><span class="section-number">${num}</span><h1>${esc(title)}</h1></div>
  <div class="card">${html}</div>
</section>`;
}

/* ===================== DAY CONTENTS ===================== */

const dayBodies = {
  "01": () => {
    const lessons = [
      { id: "l01", label: "L01 · Codex CLI 是什么" },
      { id: "l02", label: "L02 · 和桌面端 / IDE 的边界" },
      { id: "l03", label: "L03 · 仓库顶层目录" },
      { id: "l04", label: "L04 · codex-rs 关键 crate" },
      { id: "l05", label: "L05 · Agent 循环心智图" },
      { id: "l06", label: "L06 · 今日小结 + 动手" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "Codex CLI 是什么",
        `<div class="ask"><span class="t">🤔 痛点</span>想在终端里让 AI 读仓库、改代码、跑测试，还要能脚本化进 CI——浏览器聊天框不够用。</div>
<div class="essence"><span class="t">💡 本质</span>OpenAI 开源的<strong>本地编码 Agent CLI</strong>：交互模式是 TUI，非交互是 <code>codex exec</code>，核心逻辑在 Rust 工作区 <span class="fileref">codex-rs/</span>。</div>
<div class="baby"><span class="t">🍼 一句话</span>你在终端说人话 → 模型决定调哪些工具（读文件/跑 shell/打补丁）→ 沙箱里执行 → 结果喂回模型，直到任务完成。</div>
<p class="src">仓库 README：<span class="fileref">README.md</span> · 官方文档 <a href="https://developers.openai.com/codex" target="_blank" rel="noopener">developers.openai.com/codex</a></p>`
      ),
      section(
        "l02",
        "L02",
        "和桌面端 / IDE 的边界",
        `<table class="ctable">
<tr><th>形态</th><th>本仓库？</th><th>适合</th></tr>
<tr><td><strong>Codex CLI</strong>（本教程）</td><td>✅ 主体</td><td>终端、脚本、CI</td></tr>
<tr><td>ChatGPT Desktop / Codex 模式</td><td>❌ UI 不在仓内；CLI 有 <code>codex app</code> 拉起</td><td>本地项目 GUI、预览</td></tr>
<tr><td>IDE 扩展</td><td>❌；靠 <code>codex app-server</code></td><td>编辑器内联</td></tr>
<tr><td>Codex Web</td><td>❌</td><td>云端任务</td></tr>
</table>
<div class="why"><b>关键</b>：桌面/IDE 与 CLI <strong>共用</strong> <code>codex-core</code> + <code>app-server</code> 协议；本仓开源的是 CLI 与服务端，不是 Electron/桌面 UI。</div>
<p>已有桌面端教程：<a href="codex-desktop-tutorial.html">Codex 桌面端使用教程</a>。</p>`
      ),
      section(
        "l03",
        "L03",
        "仓库顶层目录",
        `<table class="ctable">
<tr><th>路径</th><th>角色</th></tr>
<tr><td><span class="fileref">codex-cli/</span></td><td>npm 包 <code>@openai/codex</code>：Node 薄包装，spawn 平台原生二进制</td></tr>
<tr><td><span class="fileref">codex-rs/</span></td><td>★ Rust workspace：几乎全部产品逻辑；二进制名 <code>codex</code></td></tr>
<tr><td><span class="fileref">sdk/</span></td><td>TypeScript / Python SDK，脚本化驱动 CLI</td></tr>
<tr><td><span class="fileref">docs/</span></td><td>贡献者/安装说明；多数用法指向官网</td></tr>
<tr><td><span class="fileref">AGENTS.md</span></td><td>本仓库给 Agent 的工程约定（读源码时必看）</td></tr>
<tr><td><span class="fileref">.codex/skills/</span></td><td>仓库级 Skills</td></tr>
</table>
<div class="glossary"><b>心智模型</b>：<code>npm i -g @openai/codex</code> 装的是发射器；真正干活的是 <code>codex-rs</code> 编出来的原生 <code>codex</code>。</div>`
      ),
      section(
        "l04",
        "L04",
        "codex-rs 关键 crate 地图",
        `<div class="mod-map">
<div class="mm" style="--mc:#10a37f"><h4>cli</h4><p>二进制入口 MultitoolCli，子命令分发。<strong>Day 04/06</strong></p></div>
<div class="mm" style="--mc:#34d399"><h4>tui</h4><p>ratatui 交互界面、slash、composer。<strong>Day 05</strong></p></div>
<div class="mm" style="--mc:#0ea5e9"><h4>core</h4><p>会话、turn、工具、配置胶水——大脑。<strong>Day 08/11</strong></p></div>
<div class="mm" style="--mc:#6366f1"><h4>protocol</h4><p>Op / Event / SandboxMode 共享类型。<strong>Day 07</strong></p></div>
<div class="mm" style="--mc:#8b5cf6"><h4>app-server</h4><p>JSON-RPC：TUI/exec/IDE 共用控制面。<strong>Day 07/19</strong></p></div>
<div class="mm" style="--mc:#f59e0b"><h4>exec</h4><p>非交互 runner + JSONL。<strong>Day 17</strong></p></div>
<div class="mm" style="--mc:#ec4899"><h4>login / config</h4><p>认证与分层配置。<strong>Day 09/10</strong></p></div>
<div class="mm" style="--mc:#22c55e"><h4>apply-patch · sandbox · mcp</h4><p>补丁、沙箱、MCP。<strong>Day 12/13</strong></p></div>
</div>
<div class="pitfall"><span class="t">坑</span>crate 一百多个，别按字母表扫。<strong>先抓 cli → tui/exec → app-server → core → protocol</strong> 这条链。</div>`
      ),
      section(
        "l05",
        "L05",
        "Agent 循环心智图",
        `<p>先把圈刻进脑子（细节 Day 08）：</p>
<div class="flow">
  <div class="f"><b>① 输入</b>TUI / exec</div>
  <div class="f"><b>② app-server</b>turn/start</div>
  <div class="f"><b>③ core</b>submit(Op)</div>
  <div class="f"><b>④ 模型</b>Responses API</div>
  <div class="f"><b>⑤ 工具</b>shell/patch/MCP</div>
  <div class="f"><b>⑥ 沙箱</b>Seatbelt/bwrap</div>
  <div class="f"><b>⑦ 回填</b>下一轮</div>
</div>
<div class="term-hero">
  <div class="bar"><i class="r"></i><i class="y"></i><i class="g"></i><span>codex — 终端里的样子</span></div>
  <div class="body">
    <div><span class="p">›</span> <span class="u">修一下 README 里过期的安装命令，并跑相关检查</span></div>
    <div class="o">● 我先读 README 和 docs/install.md…</div>
    <div class="k">  ⎿ shell(rg …)  ⎿ apply_patch  ✓ 已更新两处链接</div>
  </div>
</div>
<div class="ask"><span class="t">读源顺序（后面 19 天都按这个走）</span>
① <code>cli/src/main.rs</code> 看命令怎么进 →
② <code>protocol::Op</code> 看动词表 →
③ <code>session/turn.rs::run_turn</code> 看主循环 →
④ <code>tools/handlers/</code> 看手脚 →
⑤ <code>exec/</code> 与 <code>app-server/</code> 看非交互与 IDE 复用。
</div>`
      ),
      section(
        "l06",
        "L06",
        "今日小结 + 动手",
        `<div class="verify">✅ 能回答：CLI 是什么；和桌面端边界；顶层目录；8 个关键 crate；一次任务的七步环。</div>
<pre><code class="language-bash"># 假设你已 clone openai/codex
cd /path/to/codex
ls -la
ls codex-rs | head -40
head -40 README.md
head -30 AGENTS.md
ls codex-cli/bin/
sed -n '100,212p' codex-rs/cli/src/main.rs   # MultitoolCli + Subcommand</code></pre>
<div class="why"><b>明天</b>：真正装起来、登录、完成第一次交互对话。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "02": () => {
    const lessons = [
      { id: "l01", label: "L01 · 安装" },
      { id: "l02", label: "L02 · 登录" },
      { id: "l03", label: "L03 · 第一次交互" },
      { id: "l04", label: "L04 · doctor 自检" },
      { id: "l05", label: "L05 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "安装",
        `<pre><code class="language-bash"># macOS / Linux
curl -fsSL https://chatgpt.com/codex/install.sh | sh

# Windows PowerShell
irm https://chatgpt.com/codex/install.ps1 | iex

# 包管理器
npm install -g @openai/codex
brew install --cask codex

codex --version</code></pre>
<div class="why"><b>源码对应</b>：npm 入口 <span class="fileref">codex-cli/bin/codex.js</span> 按 <code>platform/arch</code> 选 <code>@openai/codex-darwin-arm64</code> 等包，再 <code>spawn</code> 原生二进制。</div>`
      ),
      section(
        "l02",
        "L02",
        "登录（两种主流方式）",
        `<table class="ctable">
<tr><th>方式</th><th>命令</th><th>计费</th></tr>
<tr><td>ChatGPT（推荐）</td><td><code>codex login</code></td><td>走 Plus/Pro/… 套餐</td></tr>
<tr><td>API Key</td><td><code>printenv OPENAI_API_KEY | codex login --with-api-key</code></td><td>按 API 计价</td></tr>
</table>
<pre><code class="language-bash">codex login status
codex logout</code></pre>
<div class="pitfall"><span class="t">安全</span>凭证在 <code>~/.codex/</code>（或钥匙串）。别提交 Git、别贴聊天。</div>
<p class="src">实现：<span class="fileref">codex-rs/login/</span> · 官方 <a href="https://developers.openai.com/codex/auth" target="_blank" rel="noopener">Auth</a></p>`
      ),
      section(
        "l03",
        "L03",
        "第一次交互对话",
        `<pre><code class="language-bash">cd your-project
codex
# 或带初始 prompt
codex "阅读 README，用三句话总结如何本地跑测试"</code></pre>
<ol style="font-size:13px;line-height:1.85;padding-left:18px;color:var(--text-secondary)">
<li>确认工作目录是仓库根（或用 <code>-C /path</code>）</li>
<li>先用会询问审批的模式，别开 <code>--yolo</code></li>
<li>任务说清目标 + 验收（「改什么 / 怎么证明改对」）</li>
</ol>
<div class="verify">✅ 终端出现 Codex TUI，能看到模型回复或工具调用轨迹。</div>`
      ),
      section(
        "l04",
        "L04",
        "doctor 自检",
        `<pre><code class="language-bash">codex doctor</code></pre>
<div class="baby"><span class="t">🍼 作用</span>诊断安装、config、auth、运行时健康——登录失败或奇怪报错时先跑它。</div>
<p>子命令在 <span class="fileref">codex-rs/cli/src/main.rs</span> 的 <code>Subcommand::Doctor</code>。</p>`
      ),
      section(
        "l05",
        "L05",
        "今日小结",
        `<div class="verify">✅ 已安装；已登录；完成一次只读任务；知道 <code>doctor</code>。</div>
<div class="why"><b>明天</b>：沙箱与审批——CLI 最重要的安全课。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "03": () => {
    const lessons = [
      { id: "l01", label: "L01 · 两层防护" },
      { id: "l02", label: "L02 · 用法与 flag" },
      { id: "l03", label: "L03 · 源码枚举" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "Sandbox + Approval 两层防护",
        `<div class="baby"><span class="t">🍼 大白话</span><strong>Sandbox</strong> = 技术上能碰哪（读/写/网）；<strong>Approval</strong> = 什么时候必须停下来问你。</div>
<table class="ctable">
<tr><th>Sandbox</th><th>含义</th></tr>
<tr><td><code>read-only</code></td><td>默认倾向：只读工作区</td></tr>
<tr><td><code>workspace-write</code></td><td>可写当前工作区</td></tr>
<tr><td><code>danger-full-access</code></td><td>几乎不限——慎用</td></tr>
</table>
<table class="ctable">
<tr><th>Approval</th><th>含义</th></tr>
<tr><td><code>untrusted</code></td><td>只有「已知安全只读」自动过</td></tr>
<tr><td><code>on-request</code></td><td>默认：模型请求时再问你</td></tr>
<tr><td><code>never</code></td><td>不问人，失败直接回模型</td></tr>
</table>`
      ),
      section(
        "l02",
        "L02",
        "常用命令行开关",
        `<pre><code class="language-bash">codex -s read-only -a on-request
codex -s workspace-write
# 危险：跳过审批 + 沙箱（仅隔离 CI 等极端场景）
codex --dangerously-bypass-approvals-and-sandbox
# 别名
codex --yolo</code></pre>
<div class="pitfall"><span class="t">官方级警告</span>本地开发别习惯性 <code>--yolo</code>。优先用 Rules / 精准放行，而不是全局放开。</div>
<p>TUI 内也可用 <code>/permissions</code>、<code>/setup-default-sandbox</code> 调整。</p>`
      ),
      section(
        "l03",
        "L03",
        "源码对照",
        `<p><span class="fileref">codex-rs/protocol/src/config_types.rs</span> ≈ L86：</p>
<pre><code class="language-rust">pub enum SandboxMode {
    #[serde(rename = "read-only")]
    ReadOnly,           // default
    #[serde(rename = "workspace-write")]
    WorkspaceWrite,
    #[serde(rename = "danger-full-access")]
    DangerFullAccess,
}</code></pre>
<p><span class="fileref">codex-rs/protocol/src/protocol.rs</span> ≈ L911：</p>
<pre><code class="language-rust">pub enum AskForApproval {
    UnlessTrusted,  // "untrusted"
    OnRequest,      // default
    Granular(...),
    Never,
}</code></pre>
<div class="why"><b>执行门禁</b>在 <span class="fileref">codex-rs/core/src/tools/sandboxing.rs</span> + OS 实现（macOS Seatbelt、Linux bwrap/Landlock、Windows sandbox）。</div>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 能解释两层防护；能默写出三个 sandbox 值；知道默认 approval 是 on-request。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "04": () => {
    const lessons = [
      { id: "l01", label: "L01 · MultitoolCli" },
      { id: "l02", label: "L02 · 子命令地图" },
      { id: "l03", label: "L03 · 共享 flag" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "入口：无子命令 = 交互 TUI",
        `<p><span class="fileref">codex-rs/cli/src/main.rs</span>：</p>
<pre><code class="language-rust">struct MultitoolCli {
    // ... config / features / remote / interactive
    subcommand: Option&lt;Subcommand&gt;,
}
// 无 subcommand → 跑 TUI；有则分发</code></pre>
<div class="glossary"><b>Multitool</b>：一个二进制里塞很多子工具——像 <code>git</code>，而不是每个功能一个 exe。</div>`
      ),
      section(
        "l02",
        "L02",
        "子命令地图（用法向）",
        `<table class="ctable">
<tr><th>命令</th><th>干什么</th></tr>
<tr><td><code>codex</code> / <code>codex "…"</code></td><td>交互 TUI</td></tr>
<tr><td><code>exec</code> (<code>e</code>)</td><td>非交互跑一轮任务</td></tr>
<tr><td><code>review</code></td><td>非交互 code review</td></tr>
<tr><td><code>login</code> / <code>logout</code></td><td>认证</td></tr>
<tr><td><code>mcp</code></td><td>管理 MCP servers（list/add/remove/login…）</td></tr>
<tr><td><code>plugin</code></td><td>插件管理</td></tr>
<tr><td><code>mcp-server</code></td><td>把 Codex 自己当 MCP server（stdio）</td></tr>
<tr><td><code>app-server</code></td><td>给 IDE/桌面的 JSON-RPC 服务</td></tr>
<tr><td><code>app</code></td><td>拉起桌面端（macOS/Windows）</td></tr>
<tr><td><code>resume</code> / <code>fork</code></td><td>恢复 / 分叉会话</td></tr>
<tr><td><code>archive</code> / <code>unarchive</code> / <code>delete</code></td><td>会话生命周期</td></tr>
<tr><td><code>apply</code> (<code>a</code>)</td><td><code>git apply</code> 最新 agent diff</td></tr>
<tr><td><code>sandbox</code></td><td>在 Codex 沙箱里跑一条命令</td></tr>
<tr><td><code>doctor</code> / <code>update</code> / <code>completion</code></td><td>诊断 / 自更新 / 补全脚本</td></tr>
<tr><td><code>features</code></td><td>list/enable/disable 功能开关</td></tr>
<tr><td><code>cloud</code></td><td>浏览云端任务（实验）</td></tr>
</table>`
      ),
      section(
        "l03",
        "L03",
        "共享重要 flag",
        `<table class="ctable">
<tr><th>Flag</th><th>含义</th></tr>
<tr><td><code>-m / --model</code></td><td>模型</td></tr>
<tr><td><code>-s / --sandbox</code></td><td>沙箱模式</td></tr>
<tr><td><code>-a</code>（TUI）</td><td>审批策略</td></tr>
<tr><td><code>-C / --cd</code></td><td>工作目录</td></tr>
<tr><td><code>--add-dir</code></td><td>额外可写目录</td></tr>
<tr><td><code>-p / --profile</code></td><td>配置 profile</td></tr>
<tr><td><code>-c key=value</code></td><td>临时覆盖 config</td></tr>
<tr><td><code>--oss</code></td><td>本地 Ollama 等</td></tr>
<tr><td><code>--search</code></td><td>打开 hosted web_search</td></tr>
<tr><td><code>--enable / --disable</code></td><td>feature 开关</td></tr>
</table>
<p>定义散落在 <span class="fileref">codex-rs/utils/cli/</span> 与各子命令 <code>Cli</code> 结构体。</p>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<pre><code class="language-bash">codex --help
codex exec --help
codex mcp --help
codex features list</code></pre>
<div class="verify">✅ 能从 help 里找到 exec/mcp/resume；知道无子命令进 TUI。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "05": () => {
    const lessons = [
      { id: "l01", label: "L01 · TUI 结构" },
      { id: "l02", label: "L02 · Slash 高频" },
      { id: "l03", label: "L03 · 源码 SlashCommand" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "交互界面在干什么",
        `<div class="flow">
  <div class="f"><b>消息区</b>chatwidget</div>
  <div class="f"><b>底部输入</b>composer</div>
  <div class="f"><b>弹层</b>审批 / slash</div>
  <div class="f"><b>footer</b>状态</div>
</div>
<p>主目录：<span class="fileref">codex-rs/tui/src/</span>——<code>chatwidget.rs</code>（编排）、<code>bottom_pane/</code>（输入）、<code>slash_command.rs</code>。</p>
<div class="glossary"><b>ratatui</b>：Rust 终端 UI 库。Codex TUI 用它画布局，不是 Electron。</div>`
      ),
      section(
        "l02",
        "L02",
        "高频 Slash 命令（用法）",
        `<table class="ctable">
<tr><th>命令</th><th>用途</th></tr>
<tr><td><code>/model</code></td><td>切模型</td></tr>
<tr><td><code>/permissions</code></td><td>审批 / 权限</td></tr>
<tr><td><code>/plan</code></td><td>进入/围绕 Plan 协作模式</td></tr>
<tr><td><code>/skills</code></td><td>技能</td></tr>
<tr><td><code>/mcp</code></td><td>MCP</td></tr>
<tr><td><code>/review</code></td><td>代码审查</td></tr>
<tr><td><code>/diff</code></td><td>看变更</td></tr>
<tr><td><code>/compact</code></td><td>压缩上下文</td></tr>
<tr><td><code>/new</code> <code>/resume</code> <code>/fork</code></td><td>会话</td></tr>
<tr><td><code>/init</code></td><td>生成项目 AGENTS.md</td></tr>
<tr><td><code>/status</code> <code>/usage</code></td><td>状态与用量</td></tr>
<tr><td><code>/quit</code></td><td>退出</td></tr>
</table>
<p>输入框前缀 <code>!</code> 可直接跑用户 shell（走 <code>Op::RunUserShellCommand</code> 一类路径）。</p>`
      ),
      section(
        "l03",
        "L03",
        "源码：枚举顺序 = 弹层展示顺序",
        `<p><span class="fileref">codex-rs/tui/src/slash_command.rs</span> 注释写明：<strong>不要按字母排序</strong>——枚举顺序就是 popup 展示顺序，高频靠前。</p>
<pre><code class="language-rust">pub enum SlashCommand {
    Model, Ide, Permissions, Keymap, Vim,
    ElevateSandbox, // /setup-default-sandbox
    // ... Skills, Review, Plan, Agent, Diff, Mcp ...
}</code></pre>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 会用 /model /permissions /plan /init；知道 slash 定义文件位置。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "06": () => {
    const lessons = [
      { id: "l01", label: "L01 · npm 发射器" },
      { id: "l02", label: "L02 · main 分发" },
      { id: "l03", label: "L03 · TUI 挂载 app-server" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "codex.js：选对原生二进制（逐段）",
        `<p><span class="fileref">codex-cli/bin/codex.js</span> 可以按三段读：</p>
<ol style="font-size:13px;line-height:1.85;color:var(--text-secondary);padding-left:18px">
<li><strong>L16–L23</strong>：<code>PLATFORM_PACKAGE_BY_TARGET</code> 把 Rust target triple 映射到可选依赖包名。</li>
<li><strong>L25–L77</strong>：用 <code>process.platform/arch</code> 算出 <code>targetTriple</code>；不支持就直接 throw。</li>
<li><strong>L79–L108</strong>：<code>findCodexExecutable()</code> 用 <code>require.resolve(平台包/package.json)</code> 找到 <code>vendor/&lt;triple&gt;/bin/codex</code>；缺失则提示重新 <code>npm i -g</code>。</li>
</ol>
<pre><code class="language-javascript">const codexExecutable = path.join(
  vendorRoot, targetTriple, "bin",
  process.platform === "win32" ? "codex.exe" : "codex",
);</code></pre>
<div class="why"><b>为什么异步 spawn？</b>文件后半注释写明：用异步 <code>spawn</code> 而不是 <code>spawnSync</code>，以便 Node 能收 SIGINT 并转发给子进程——Ctrl-C 才能干净退出。</div>
<div class="baby"><span class="t">🍼</span>Node 只做「找对平台包 → 转交参数」。业务全在 Rust。</div>`
      ),
      section(
        "l02",
        "L02",
        "cli/main.rs 分发",
        `<pre><code class="language-bash">你敲: codex "fix flaky test"
  → MultitoolCli 解析
  → subcommand == None
  → 进入交互路径（TuiCli 参数 + prompt）
  → codex_tui::run_…</code></pre>
<p>有子命令则 match 到 Exec / Login / Mcp…（同一文件后半部分巨大的 match 臂）。</p>`
      ),
      section(
        "l03",
        "L03",
        "TUI 与 in-process app-server",
        `<div class="essence"><span class="t">现代架构</span>TUI <strong>不直接</strong>调 core 细节；它通过 <strong>in-process app-server client</strong> 发 JSON-RPC（和 IDE 同协议）。</div>
<p>关键文件：</p>
<ul style="font-size:13px;line-height:1.8;color:var(--text-secondary)">
<li><span class="fileref">codex-rs/tui/src/lib.rs</span> — 启动客户端与 App</li>
<li><span class="fileref">codex-rs/tui/src/chatwidget/input_submission.rs</span> — 提交输入</li>
<li><span class="fileref">codex-rs/app-server-client/</span> — 客户端实现</li>
</ul>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 能画出 npm→Rust→TUI→app-server 四段；知道 TUI 与 IDE 同协议。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "07": () => {
    const lessons = [
      { id: "l01", label: "L01 · Op 是什么" },
      { id: "l02", label: "L02 · 关键 Op" },
      { id: "l03", label: "L03 · app-server v2" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "协议层：一切操作是 Op",
        `<p><span class="fileref">codex-rs/protocol/src/protocol.rs</span> 的 <code>Op</code> 是 core 提交队列上的「动词」。</p>
<div class="glossary"><b>类比</b>：浏览器有 DOM 事件；Codex 有 Op。UI 只负责产生 Op，core 负责执行。</div>`
      ),
      section(
        "l02",
        "L02",
        "你一定会碰到的 Op",
        `<table class="ctable">
<tr><th>Op</th><th>含义</th></tr>
<tr><td><code>UserInput</code></td><td>用户发一轮（可带 schema / 额外上下文）</td></tr>
<tr><td><code>ExecApproval</code> / <code>PatchApproval</code></td><td>你点允许/拒绝</td></tr>
<tr><td><code>Interrupt</code></td><td>打断当前 turn</td></tr>
<tr><td><code>ThreadSettings</code></td><td>改线程设置但不发消息</td></tr>
</table>
<pre><code class="language-rust">Op::UserInput {
    items: Vec&lt;UserInput&gt;,
    final_output_json_schema: Option&lt;Value&gt;,
    // ...
    thread_settings: ThreadSettingsOverrides,
}</code></pre>`
      ),
      section(
        "l03",
        "L03",
        "app-server：对外 JSON-RPC",
        `<p>对外方法风格：<code>thread/*</code>、<code>turn/*</code>（见 <span class="fileref">codex-rs/app-server/README.md</span>、<span class="fileref">app-server-protocol/src/protocol/v2.rs</span>）。</p>
<div class="why"><b>为什么多这一层？</b>同一套 core 可被 TUI、VS Code、桌面、远程 daemon 复用，避免每个 UI 复制 agent 逻辑。</div>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 能解释 Op vs Event；知道 UserInput / ExecApproval；知道 app-server 是控制面。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "08": () => {
    const lessons = [
      { id: "l01", label: "L01 · 调用链" },
      { id: "l02", label: "L02 · run_turn" },
      { id: "l03", label: "L03 · 工具回合" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "从回车到 run_turn",
        `<pre><code class="language-bash">Composer 提交
  → app-server turn/start
  → CodexThread::submit(Op::UserInput)
  → session/handlers 派发
  → tasks/regular → run_turn()</code></pre>
<table class="ctable">
<tr><th>文件</th><th>角色</th></tr>
<tr><td><span class="fileref">core/src/codex_thread.rs</span></td><td>线程公开 API</td></tr>
<tr><td><span class="fileref">core/src/session/handlers.rs</span></td><td>Op 分发</td></tr>
<tr><td><span class="fileref">core/src/tasks/regular.rs</span></td><td>发起常规任务</td></tr>
<tr><td><span class="fileref">core/src/session/turn.rs</span></td><td>★ <code>run_turn</code>（约 2500+ 行）</td></tr>
<tr><td><span class="fileref">core/src/client.rs</span></td><td>ModelClient 流式请求</td></tr>
</table>`
      ),
      section(
        "l02",
        "L02",
        "run_turn 开头在干什么（对照源码）",
        `<p><span class="fileref">core/src/session/turn.rs</span> 文件头注释概括了契约：工具结果要回填；只有 assistant 消息则 turn 结束。函数签名约在 <strong>L144</strong>：</p>
<pre><code class="language-rust">pub(crate) async fn run_turn(
    sess: Arc&lt;Session&gt;,
    turn_context: Arc&lt;TurnContext&gt;,
    // ...
    input: Vec&lt;TurnInput&gt;,
    cancellation_token: CancellationToken,
) -&gt; CodexResult&lt;Option&lt;String&gt;&gt;</code></pre>
<p>开头几步（约 L152–L210）建议按注释跳读：</p>
<ol style="font-size:13px;line-height:1.85;color:var(--text-secondary);padding-left:18px">
<li><code>run_pre_sampling_compact</code> — 采样前先压缩，避免撑爆窗口</li>
<li><code>capture_step_context</code> + <code>record_context_updates…</code> — 固定本 turn 模型可见状态</li>
<li><code>build_skills_and_plugins</code> — 注入 Skills / Plugins 相关 items</li>
<li><code>run_hooks_and_record_inputs</code> — 生命周期 hooks + 记录用户输入</li>
<li>之后进入「采样 ↔ 工具」大循环（同文件后半）</li>
</ol>
<div class="flow">
  <div class="f"><b>拼 prompt</b>历史+工具定义</div>
  <div class="f"><b>流式读</b>文本/reasoning</div>
  <div class="f"><b>遇 tool_call</b>路由执行</div>
  <div class="f"><b>写回上下文</b></div>
  <div class="f"><b>直到</b>结束/打断</div>
</div>
<div class="essence"><span class="t">精读建议</span>不要一次读完 2500 行。今天只求：能指着函数签名 + 开头五步讲清楚；采样循环放到你自己用 <code>rg "tool"</code> 在同文件里追。</div>`
      ),
      section(
        "l03",
        "L03",
        "工具回合",
        `<p><span class="fileref">core/src/tools/spec_plan.rs</span> 决定本回合暴露哪些工具；<span class="fileref">tools/router.rs</span> 把 call 分到 <span class="fileref">tools/handlers/</span>。</p>
<div class="pitfall"><span class="t">注意</span>AGENTS.md 提醒：避免再往已经臃肿的 <code>codex-core</code> 无塞无关功能——读代码时也会感到 core 很「胖」。</div>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<pre><code class="language-bash">rg -n "pub(crate) async fn run_turn" codex-rs/core/src/session/turn.rs
rg -n "enum Op" -n codex-rs/protocol/src/protocol.rs | head</code></pre>
<div class="verify">✅ 能默写回车后的 5 步文件链。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "09": () => {
    const lessons = [
      { id: "l01", label: "L01 · 配置住哪" },
      { id: "l02", label: "L02 · 关键项" },
      { id: "l03", label: "L03 · 覆盖顺序" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "配置住哪",
        `<ul style="font-size:13px;line-height:1.85;color:var(--text-secondary)">
<li>主目录：<code>$CODEX_HOME</code> 或 <code>~/.codex</code></li>
<li>主文件：<code>config.toml</code></li>
<li>Profile：<code>~/.codex/&lt;name&gt;.config.toml</code> + <code>-p</code></li>
<li>Schema：<span class="fileref">codex-rs/core/config.schema.json</span></li>
</ul>`
      ),
      section(
        "l02",
        "L02",
        "你会改的键",
        `<pre><code class="language-toml">model = "…"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[mcp_servers.my_server]
command = "npx"
args = ["-y", "some-mcp-server"]

[features]
# 功能开关…</code></pre>
<p>临时覆盖：<code>codex -c model=… -c sandbox_mode=read-only</code></p>`
      ),
      section(
        "l03",
        "L03",
        "分层与 features",
        `<pre><code class="language-bash">codex features list
codex features enable some_feature
codex features disable some_feature</code></pre>
<div class="why"><b>源码</b>：加载逻辑在 <span class="fileref">codex-rs/config/</span> 与 <span class="fileref">core/src/config/</span>；覆盖解析 <span class="fileref">utils/cli/src/config_override.rs</span>。</div>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 知道 CODEX_HOME；会写 sandbox/approval；会用 -c 与 features。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "10": () => {
    const lessons = [
      { id: "l01", label: "L01 · 登录路径" },
      { id: "l02", label: "L02 · Provider" },
      { id: "l03", label: "L03 · OSS 本地" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "login 实现落点",
        `<p>crate：<span class="fileref">codex-rs/login/</span>。支持 ChatGPT OAuth、API Key stdin、access token、device auth。</p>
<pre><code class="language-bash">codex login
codex login --device-auth
codex login status</code></pre>`
      ),
      section(
        "l02",
        "L02",
        "模型与 Provider",
        `<p><code>model</code> + <code>model_provider</code> 决定打哪家 API。相关：<span class="fileref">models-manager/</span>、<span class="fileref">codex-api/</span>、<span class="fileref">codex-client/</span>。</p>
<div class="baby"><span class="t">🍼</span>TUI 里 <code>/model</code> 改的是当前会话模型偏好，最终仍落到 config/线程设置。</div>`
      ),
      section(
        "l03",
        "L03",
        "本地 OSS",
        `<pre><code class="language-bash">codex --oss
# 或配置指向 Ollama / LM Studio
# crates: ollama/  lmstudio/</code></pre>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 分清 ChatGPT 登录 vs API Key；知道 --oss 入口。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "11": () => {
    const lessons = [
      { id: "l01", label: "L01 · 工具管线" },
      { id: "l02", label: "L02 · handlers 目录" },
      { id: "l03", label: "L03 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "工具管线三件套",
        `<table class="ctable">
<tr><th>模块</th><th>职责</th></tr>
<tr><td><span class="fileref">tools/spec_plan.rs</span></td><td>本回合开放哪些工具定义</td></tr>
<tr><td><span class="fileref">tools/router.rs</span></td><td>把 call_id 路由到 handler</td></tr>
<tr><td><span class="fileref">tools/handlers/*</span></td><td>真正执行</td></tr>
</table>`
      ),
      section(
        "l02",
        "L02",
        "handlers 里有什么",
        `<table class="ctable">
<tr><th>区域</th><th>例子</th></tr>
<tr><td>Shell / unified exec</td><td><code>shell*</code>、<code>unified_exec*</code></td></tr>
<tr><td>补丁</td><td><code>apply_patch.rs</code> + crate <code>apply-patch/</code></td></tr>
<tr><td>MCP</td><td><code>mcp.rs</code>、<code>mcp_resource/</code></td></tr>
<tr><td>协作 / 多 agent</td><td><code>plan.rs</code>、<code>multi_agents*</code></td></tr>
<tr><td>其它</td><td><code>view_image</code>、<code>request_permissions</code>、<code>tool_search</code>…</td></tr>
</table>
<p>Hosted <code>web_search</code> 常由 config / <code>--search</code> 打开（见 tools hosted_spec）。</p>`
      ),
      section(
        "l03",
        "L03",
        "今日小结",
        `<pre><code class="language-bash">ls codex-rs/core/src/tools/handlers | head -40</code></pre>
<div class="verify">✅ 能说出 spec_plan → router → handler。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "12": () => {
    const lessons = [
      { id: "l01", label: "L01 · Shell 进沙箱" },
      { id: "l02", label: "L02 · apply_patch" },
      { id: "l03", label: "L03 · execpolicy" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "Shell 如何进沙箱",
        `<p>审批通过后，命令经 <span class="fileref">tools/sandboxing.rs</span> 策略，再落到：</p>
<ul style="font-size:13px;line-height:1.8;color:var(--text-secondary)">
<li>macOS：Seatbelt（sandbox-exec）</li>
<li>Linux：bubblewrap + Landlock（<span class="fileref">linux-sandbox/</span>、<span class="fileref">bwrap/</span>）</li>
<li>Windows：平台 sandbox</li>
</ul>
<pre><code class="language-bash"># 手动体验沙箱包装
codex sandbox -- help
codex sandbox -- ls</code></pre>`
      ),
      section(
        "l02",
        "L02",
        "apply_patch：结构化改文件",
        `<div class="baby"><span class="t">🍼</span>模型不总是直接 <code>cat &gt; file</code>；常用专用补丁工具，便于审阅与回放。</div>
<p>实现：handler <span class="fileref">apply_patch.rs</span> + 独立 crate <span class="fileref">codex-rs/apply-patch/</span>。CLI 还有 <code>codex apply</code> 把最新 diff <code>git apply</code> 到工作树。</p>`
      ),
      section(
        "l03",
        "L03",
        "execpolicy",
        `<p><span class="fileref">codex-rs/execpolicy/</span>：用 Starlark 规则约束「哪些命令前缀可自动过」。隐藏子命令 <code>codex execpolicy</code> 用于检查规则。</p>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 知道三平台沙箱后端；知道 patch 与裸 shell 的分工。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "13": () => {
    const lessons = [
      { id: "l01", label: "L01 · MCP 用法" },
      { id: "l02", label: "L02 · 源码落点" },
      { id: "l03", label: "L03 · Plugins" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "把外部工具接进 Codex",
        `<pre><code class="language-bash">codex mcp list
codex mcp add my-server -- npx -y @some/mcp-server
codex mcp get my-server
codex mcp remove my-server
codex mcp login my-server   # 若需 OAuth</code></pre>
<p>配置写入 <code>~/.codex/config.toml</code> 的 <code>[mcp_servers]</code>。TUI 内 <code>/mcp</code>。</p>`
      ),
      section(
        "l02",
        "L02",
        "源码",
        `<ul style="font-size:13px;line-height:1.8;color:var(--text-secondary)">
<li>CLI：<span class="fileref">cli/src/mcp_cmd.rs</span></li>
<li>连接管理：<span class="fileref">codex-mcp/</span>（AGENTS.md 建议改 MCP 时优先动这里）</li>
<li>Handler：<span class="fileref">core/src/tools/handlers/mcp.rs</span></li>
<li>反向：<code>codex mcp-server</code> 让 Codex 作为 MCP 被其它宿主调用</li>
</ul>`
      ),
      section(
        "l03",
        "L03",
        "Plugins",
        `<pre><code class="language-bash">codex plugin --help
# TUI: /plugins</code></pre>
<p>相关 crate：<span class="fileref">plugin/</span>、<span class="fileref">core-plugins/</span>。</p>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 会 mcp add/list；知道 MCP 工具最终也走 tool handler。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "14": () => {
    const lessons = [
      { id: "l01", label: "L01 · AGENTS.md" },
      { id: "l02", label: "L02 · Skills" },
      { id: "l03", label: "L03 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "项目说明书 AGENTS.md",
        `<div class="essence"><span class="t">作用</span>告诉 Agent：怎么 build/test、目录约定、禁止事项。从项目根到 cwd 会拼接多层。</div>
<pre><code class="language-bash"># TUI 内生成模板
/init</code></pre>
<p>加载：<span class="fileref">codex-rs/core/src/agents_md.rs</span>。本仓库自己的 <span class="fileref">AGENTS.md</span> 就是范例（Rust 规范、测试规矩、别碰某些 env）。</p>
<div class="pitfall"><span class="t">上限</span>有 <code>project_doc_max_bytes</code> 之类上限——说明书别写成小说。</div>`
      ),
      section(
        "l02",
        "L02",
        "Skills",
        `<p><code>SKILL.md</code> 描述可复用流程；发现与注入在 <span class="fileref">core-skills/</span>。用户/项目/插件多根目录；TUI <code>/skills</code>。</p>
<p>本仓示例：<span class="fileref">.codex/skills/*/SKILL.md</span>。</p>`
      ),
      section(
        "l03",
        "L03",
        "今日小结",
        `<div class="verify">✅ 会写简短 AGENTS.md；知道 /init 与 Skills 入口。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "15": () => {
    const lessons = [
      { id: "l01", label: "L01 · Default vs Plan" },
      { id: "l02", label: "L02 · 相关命令" },
      { id: "l03", label: "L03 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "协作模式",
        `<p><span class="fileref">tui/src/collaboration_modes.rs</span>：<strong>Default</strong>（直接干）vs <strong>Plan</strong>（先计划再动手）。模板在 <span class="fileref">collaboration-mode-templates/</span>。</p>
<div class="baby"><span class="t">🍼 何时 Plan</span>大改动、不确定范围、想先审方案——先 <code>/plan</code>。</div>`
      ),
      section(
        "l02",
        "L02",
        "相关 slash / 工具",
        `<table class="ctable">
<tr><th>入口</th><th>用途</th></tr>
<tr><td><code>/plan</code> <code>/goal</code></td><td>计划与目标</td></tr>
<tr><td><code>/agent</code> <code>/side</code></td><td>多线程 / 侧聊</td></tr>
<tr><td>handlers <code>plan.rs</code> <code>multi_agents*</code></td><td>模型侧工具</td></tr>
</table>`
      ),
      section(
        "l03",
        "L03",
        "今日小结",
        `<div class="verify">✅ 能说明 Plan 模式适用场景。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "16": () => {
    const lessons = [
      { id: "l01", label: "L01 · 会话生命周期" },
      { id: "l02", label: "L02 · compact" },
      { id: "l03", label: "L03 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "resume / fork / archive",
        `<pre><code class="language-bash">codex resume          # 选择器
codex resume --last
codex fork --last
codex archive &lt;id-or-name&gt;
codex unarchive …
codex delete …</code></pre>
<p>落盘相关：<span class="fileref">rollout/</span>、<span class="fileref">thread-store/</span>、<span class="fileref">state/</span>。</p>`
      ),
      section(
        "l02",
        "L02",
        "上下文压缩",
        `<p>长会话用 TUI <code>/compact</code> 压缩历史，避免撑爆上下文。turn 循环里也有自动 compact 相关逻辑。</p>`
      ),
      section(
        "l03",
        "L03",
        "今日小结",
        `<div class="verify">✅ 会 resume --last；知道会话可 archive/delete。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "17": () => {
    const lessons = [
      { id: "l01", label: "L01 · exec 基本用法" },
      { id: "l02", label: "L02 · JSONL / schema" },
      { id: "l03", label: "L03 · CI 建议" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "非交互跑一轮",
        `<pre><code class="language-bash">codex exec "修复失败的单元测试并说明改动"
codex e "summarize this repo in 5 bullets"
codex exec resume --last "继续"</code></pre>
<p>实现：<span class="fileref">codex-rs/exec/</span>——同样走 in-process app-server，事件经 human 或 JSONL processor 输出。</p>`
      ),
      section(
        "l02",
        "L02",
        "给机器读的输出",
        `<pre><code class="language-bash">codex exec --json "…"
codex exec -o last.txt "…"
codex exec --output-schema schema.json "生成符合 schema 的结果"</code></pre>
<table class="ctable">
<tr><th>Flag</th><th>用途</th></tr>
<tr><td><code>--json</code></td><td>stdout 打 JSONL 事件</td></tr>
<tr><td><code>-o</code></td><td>最终消息落盘</td></tr>
<tr><td><code>--ephemeral</code></td><td>不持久化会话</td></tr>
<tr><td><code>--skip-git-repo-check</code></td><td>非 git 目录也跑</td></tr>
</table>
<p>还有 <code>codex review</code> / <code>codex exec review</code> 做非交互审查。</p>`
      ),
      section(
        "l03",
        "L03",
        "CI 注意",
        `<div class="pitfall"><span class="t">安全</span>CI 才考虑 bypass；仍要限制可写目录与密钥。默认能严则严。</div>
<pre><code class="language-bash"># 示例：只读分析（按你环境调整）
codex exec -s read-only --json "列出可能的安全问题，不要改文件"</code></pre>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 会 exec --json 与 -o；知道和 TUI 共用 core。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "18": () => {
    const lessons = [
      { id: "l01", label: "L01 · SDK 定位" },
      { id: "l02", label: "L02 · 怎么用" },
      { id: "l03", label: "L03 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "SDK = 包一层 CLI",
        `<p><span class="fileref">sdk/typescript/</span> 的 <code>@openai/codex-sdk</code> 通过 JSONL 协议驱动本机 <code>codex</code> 二进制——适合 Node 脚本/服务嵌入，而不是重新实现 agent。</p>
<p>另有 <span class="fileref">sdk/python/</span>。</p>`
      ),
      section(
        "l02",
        "L02",
        "阅读入口",
        `<pre><code class="language-bash">ls sdk/typescript/src
# 关注 Codex / Thread / events 一类封装
cat sdk/typescript/README.md | head -80</code></pre>
<div class="why"><b>何时用 SDK</b>：要在应用里「开线程、发 prompt、订阅事件」；纯 shell 流水线用 <code>codex exec --json</code> 往往够。</div>`
      ),
      section(
        "l03",
        "L03",
        "今日小结",
        `<div class="verify">✅ 分清 SDK 与重新实现；知道它依赖本机 CLI。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "19": () => {
    const lessons = [
      { id: "l01", label: "L01 · 为什么需要 app-server" },
      { id: "l02", label: "L02 · 怎么跑" },
      { id: "l03", label: "L03 · 和桌面端关系" },
      { id: "l04", label: "L04 · 今日小结" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "富客户端控制面",
        `<p><span class="fileref">codex-rs/app-server/README.md</span>：JSON-RPC 双向通道，给 VS Code 扩展等「富界面」用。方法名 <code>resource/method</code>（如 <code>thread/read</code>），payload camelCase。</p>`
      ),
      section(
        "l02",
        "L02",
        "命令",
        `<pre><code class="language-bash">codex app-server --help
codex app-server generate-ts --out DIR
codex remote-control --help   # daemon + 远程控制（实验）</code></pre>
<p>协议类型：<span class="fileref">app-server-protocol/src/protocol/v2.rs</span>。守护：<span class="fileref">app-server-daemon/</span>。</p>`
      ),
      section(
        "l03",
        "L03",
        "和桌面端",
        `<div class="baby"><span class="t">🍼</span>桌面 UI 不在本仓；但桌面/移动可通过 app-server daemon / remote-control 连上同一套 agent 能力。<code>codex app</code> 只负责拉起安装器/应用。</div>
<p>对照阅读：<a href="codex-desktop-tutorial.html">桌面端教程</a>。</p>`
      ),
      section(
        "l04",
        "L04",
        "今日小结",
        `<div class="verify">✅ 明白 IDE 不复制 core，而是连 app-server。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },

  "20": () => {
    const lessons = [
      { id: "l01", label: "L01 · 全链路回顾" },
      { id: "l02", label: "L02 · 必读文件 10 个" },
      { id: "l03", label: "L03 · 对照与下一步" },
      { id: "l04", label: "L04 · 验收清单" },
    ];
    const body = [
      section(
        "l01",
        "L01",
        "全链路回顾",
        `<div class="flow">
  <div class="f"><b>用法</b>安装登录安全 TUI</div>
  <div class="f"><b>入口</b>npm→cli</div>
  <div class="f"><b>协议</b>Op/app-server</div>
  <div class="f"><b>引擎</b>run_turn</div>
  <div class="f"><b>手脚</b>tools/MCP</div>
  <div class="f"><b>工程化</b>exec/SDK</div>
</div>
<p>你现在应能：<strong>会用</strong> Codex CLI 主路径，并在源码里<strong>定位</strong>任一行为对应的 crate/文件。</p>`
      ),
      section(
        "l02",
        "L02",
        "必读文件清单",
        `<ol style="font-size:13px;line-height:1.9;color:var(--text-secondary);padding-left:18px">
<li><span class="fileref">codex-cli/bin/codex.js</span></li>
<li><span class="fileref">codex-rs/cli/src/main.rs</span></li>
<li><span class="fileref">codex-rs/protocol/src/protocol.rs</span>（Op）</li>
<li><span class="fileref">codex-rs/core/src/session/turn.rs</span></li>
<li><span class="fileref">codex-rs/core/src/tools/spec_plan.rs</span></li>
<li><span class="fileref">codex-rs/tui/src/slash_command.rs</span></li>
<li><span class="fileref">codex-rs/app-server/README.md</span></li>
<li><span class="fileref">codex-rs/exec/src/cli.rs</span></li>
<li><span class="fileref">codex-rs/core/src/agents_md.rs</span></li>
<li><span class="fileref">AGENTS.md</span>（仓库约定）</li>
</ol>`
      ),
      section(
        "l03",
        "L03",
        "对照与下一步",
        `<table class="ctable">
<tr><th>若你想…</th><th>去看</th></tr>
<tr><td>桌面产品用法</td><td><a href="codex-desktop-tutorial.html">桌面端教程</a></td></tr>
<tr><td>同类 CLI 源码对比</td><td><a href="claude-code-src-tutorial.html">Claude Code CLI 20 天</a></td></tr>
<tr><td>官方持续文档</td><td><a href="https://developers.openai.com/codex" target="_blank" rel="noopener">developers.openai.com/codex</a></td></tr>
</table>
<div class="why"><b>深入课题</b>：自己加一个 tool handler；写一条 execpolicy；用 SDK 包一个「自动修测试」脚本。</div>`
      ),
      section(
        "l04",
        "L04",
        "验收清单",
        `<ul style="font-size:13px;line-height:1.9;color:var(--text-secondary);padding-left:18px">
<li>□ 安装并登录，完成一次交互任务</li>
<li>□ 解释 sandbox × approval，未滥用 yolo</li>
<li>□ 用过 exec --json 与至少一个 mcp 命令</li>
<li>□ 仓库里写过或读过 AGENTS.md</li>
<li>□ 能指出 run_turn / Op / MultitoolCli 文件位置</li>
<li>□ 说清 CLI 与桌面/IDE 如何共用 app-server</li>
</ul>
<div class="verify" style="margin-top:12px">全部勾完：你已经具备 Codex CLI 的使用与源码导航能力。</div>`
      ),
    ].join("\n");
    return { lessons, body };
  },
};

function writeIndex() {
  const weeks = [1, 2, 3, 4]
    .map((w) => {
      const cards = DAYS.filter((d) => d.week === w)
        .map(
          (d) => `<a class="day-card" href="codex-cli-day${d.n}.html">
  <div class="top"><div class="num">${d.n}</div><h3>${esc(d.title)}</h3></div>
  <p>${esc(d.blurb)}</p>
  <div class="foot"><span class="mins">≈${d.mins} min · 已就绪 ${d.n === "01" ? '<span class="badge">NEW</span>' : ""}</span><span class="go">开始学 &rarr;</span></div>
</a>`
        )
        .join("\n");
      return `<div class="week-bar" id="week${w}"><div class="wk">W${w}</div><h2>${esc(weekMeta[w].label)}</h2><span>${esc(weekMeta[w].span)}</span></div>
<div class="day-grid">${cards}</div>`;
    })
    .join("\n");

  const html = `${commonHead("Codex CLI 源码与用法 · 20 天总目录")}
<nav class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <div class="logo" style="background:${GRAD};">Cx</div>
    <h2>Codex CLI</h2>
    <p class="version">用法 + 源码 · 20 天 · openai/codex</p>
  </div>
  <ul class="nav-list">
    <li class="nav-group-title">总目录</li>
    <li><a href="#intro" class="nav-link active">开篇 · 这是什么</a></li>
    <li><a href="#loop" class="nav-link">Agent 循环总图</a></li>
    <li><a href="#how" class="nav-link">怎么用这份教程</a></li>
    <li class="nav-group-title">四周课表</li>
    <li><a href="#week1" class="nav-link">Day 01 - 05</a></li>
    <li><a href="#week2" class="nav-link">Day 06 - 10</a></li>
    <li><a href="#week3" class="nav-link">Day 11 - 15</a></li>
    <li><a href="#week4" class="nav-link">Day 16 - 20</a></li>
    <li class="nav-group-title">导航</li>
    <li><a href="codex-desktop-tutorial.html" class="nav-link">桌面端教程</a></li>
    <li><a href="index.html" class="nav-link" style="color:var(--accent-cyan);">&larr; 返回博客首页</a></li>
  </ul>
</nav>
<button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>
<main class="content" id="content">
  <div class="part-header">
    <span class="part-label">用法 + 源码深度学习 · 零基础友好</span>
    <h1 class="part-title">Codex CLI 学习教程</h1>
    <p class="part-desc">20 天 · 每天约 30 分钟 · 基于开源仓库 <strong>openai/codex</strong>（Rust <code>codex-rs</code>）
    学会<strong>怎么用</strong>终端编码 Agent，并<strong>对照源码</strong>看清从回车到工具执行的全链路。
    桌面 GUI 不在本仓——见 <a href="codex-desktop-tutorial.html">桌面端教程</a>。</p>
  </div>

  <section id="intro" class="section">
    <div class="section-header"><span class="section-number">00</span><h1>开篇 · 这是什么</h1></div>
    <div class="card">
      <div class="baby"><span class="t">一句话</span>
      Codex CLI = 跑在你电脑终端里的 OpenAI 编码 Agent：交互用 TUI，脚本/CI 用 <code>codex exec</code>，
      核心是 Rust，npm 只是发射器。
      </div>
      <table class="ctable">
        <tr><th>你将学会</th><th>对应周</th></tr>
        <tr><td>安装登录、沙箱审批、子命令、TUI slash</td><td>第 1 周</td></tr>
        <tr><td>启动链、Op/app-server、run_turn、配置认证</td><td>第 2 周</td></tr>
        <tr><td>工具/沙箱/MCP/Skills/Plan</td><td>第 3 周</td></tr>
        <tr><td>会话、exec/CI、SDK、IDE 桥、收官</td><td>第 4 周</td></tr>
      </table>
      <p class="src">源码：<a href="https://github.com/openai/codex" target="_blank" rel="noopener">github.com/openai/codex</a> ·
      文档：<a href="https://developers.openai.com/codex" target="_blank" rel="noopener">developers.openai.com/codex</a></p>
    </div>
  </section>

  <section id="loop" class="section">
    <div class="section-header"><span class="section-number">01</span><h1>Agent 循环总图</h1></div>
    <div class="card">
      <p>灵魂是一个圈：输入 → app-server → core turn → 模型 → 工具（沙箱）→ 回填 → … 直到完成。</p>
      <div class="loop-wrap">
        <div class="aloop" id="aloop">
          <div class="ring"></div>
          <div class="center"><b>Codex<br>Turn</b><small>run_turn</small></div>
          <div class="node" data-a="0"><b>① 用户</b>TUI/exec</div>
          <div class="node" data-a="1"><b>② 协议</b>Op / RPC</div>
          <div class="node" data-a="2"><b>③ 模型</b>Responses</div>
          <div class="node" data-a="3"><b>④ 工具</b>shell/patch</div>
          <div class="node" data-a="4"><b>⑤ 沙箱</b>审批执行</div>
          <div class="orbit" id="orbit"></div>
        </div>
      </div>
      <div class="term-hero">
        <div class="bar"><i class="r"></i><i class="y"></i><i class="g"></i><span>codex</span></div>
        <div class="body">
          <div><span class="p">›</span> <span class="u">把 flaky 测试修稳，并说明根因</span></div>
          <div class="o">● 先定位失败用例…</div>
          <div class="k">  ⎿ shell(just test -p …)  ⎿ apply_patch  ✓</div>
        </div>
      </div>
    </div>
  </section>

  <section id="how" class="section">
    <div class="section-header"><span class="section-number">02</span><h1>怎么用这份教程</h1></div>
    <div class="card">
      <div class="flow">
        <div class="f"><b>每天 30min</b>一页一主题</div>
        <div class="f"><b>用法优先</b>先会跑再读码</div>
        <div class="f"><b>真路径</b>fileref 可跳转</div>
        <div class="f"><b>对照桌面</b>产品边界清晰</div>
      </div>
      <div class="warn-box">源码路径以你本地的 <code>openai/codex</code> 为准；行号会随 upstream 漂移，以符号搜索（<code>rg</code>）为准。</div>
    </div>
  </section>

  ${weeks}

  <div class="nav-buttons" style="margin-top:40px">
    <a href="index.html" class="nav-btn prev"><span class="nav-btn-label">返回</span><span class="nav-btn-title">博客首页</span></a>
    <a href="codex-cli-day01.html" class="nav-btn next"><span class="nav-btn-label">开始</span><span class="nav-btn-title">Day 01 · 项目全景</span></a>
  </div>
</main>
<button class="scroll-top" id="scrollTop">↑</button>
<script src="app.js"></script>
<script>
(function(){
  const nodes=[...document.querySelectorAll('#aloop .node')];
  const orbit=document.getElementById('orbit');
  if(!nodes.length||!orbit) return;
  const R=118;
  nodes.forEach((n,i)=>{
    const a=(-90+i*72)*Math.PI/180;
    n.style.transform='translate('+Math.cos(a)*R+'px,'+Math.sin(a)*R+'px)';
  });
  let t=0;
  setInterval(()=>{
    t=(t+1)%360;
    const a=(-90+t)*Math.PI/180;
    orbit.style.transform='translate('+Math.cos(a)*R+'px,'+Math.sin(a)*R+'px)';
    const idx=Math.floor(((t%360)/72))%5;
    nodes.forEach((n,i)=>n.style.borderColor=i===idx?'#10a37f':'');
  },40);
})();
</script>
</body>
</html>`;
  fs.writeFileSync(path.join(ROOT, "codex-cli-tutorial.html"), html);
  console.log("wrote codex-cli-tutorial.html");
}

function writeDays() {
  for (let i = 0; i < DAYS.length; i++) {
    const d = DAYS[i];
    const prev = i > 0 ? DAYS[i - 1] : null;
    const next = i < DAYS.length - 1 ? DAYS[i + 1] : null;
    const { lessons, body } = dayBodies[d.n]();
    const html = dayShell({
      day: d.n,
      navItems: navFromLessons(lessons),
      journey: journeyHtml(d.n),
      body,
      prev,
      next,
    });
    const out = path.join(ROOT, `codex-cli-day${d.n}.html`);
    fs.writeFileSync(out, html);
    console.log("wrote", path.basename(out));
  }
}

writeIndex();
writeDays();
console.log("done");
