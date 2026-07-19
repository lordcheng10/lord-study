#!/usr/bin/env python3
"""Generate WorkBuddy 20-day product learning tutorial (hub + day pages).

Source: https://www.codebuddy.cn/docs/workbuddy/ (official docs).
Style matches lord-study practice/source tutorials: 6 stages, analogy, Q&A.
"""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = "https://www.codebuddy.cn/docs/workbuddy"
C1, C2 = "#0052d9", "#00a870"  # Tencent blue + green
LOGO = "WB"
GRAD = f"linear-gradient(135deg,{C1},{C2})"


def esc(v: object) -> str:
    return html.escape(str(v), quote=True)


EXTRA_CSS = f"""
:root{{--c1:{C1};--c2:{C2}}}
.ask,.essence,.baby,.qa,.tradeoff,.pitfall{{border-left:3px solid var(--c1);background:color-mix(in srgb,var(--c1) 8%,transparent);border-radius:0 8px 8px 0;padding:11px 14px;margin:10px 0;font-size:13px;line-height:1.72}}
.ask .t,.essence .t,.baby .t,.qa .t,.tradeoff .t,.pitfall .t{{font-weight:800;color:var(--c1);display:block;margin-bottom:4px}}
.baby{{border-color:var(--accent-green);background:rgba(34,197,94,.06)}}.baby .t{{color:var(--accent-green)}}
.qa{{border-color:#a855f7;background:rgba(168,85,247,.06)}}.qa .t{{color:#c084fc}}.qa .q{{color:#c084fc;font-weight:700}}.qa .a{{color:var(--text-secondary)}}
.tradeoff{{border-color:#ec4899;background:rgba(236,72,153,.07)}}.tradeoff .t{{color:#f472b6}}
.pitfall{{border-color:#ef4444;background:rgba(239,68,68,.07)}}.pitfall .t{{color:#f87171}}
.goal-box{{background:linear-gradient(135deg,color-mix(in srgb,var(--c1) 14%,transparent),color-mix(in srgb,var(--c2) 10%,transparent));border:1px solid color-mix(in srgb,var(--c1) 35%,transparent);border-radius:12px;padding:14px 16px;margin:0 0 18px;font-size:13.5px;line-height:1.75;color:var(--text-secondary)}}
.goal-box .gt{{display:block;font-weight:800;color:var(--c1);margin-bottom:6px;font-size:14px}}
.fileref{{display:inline-block;font-size:11px;background:color-mix(in srgb,var(--c1) 12%,transparent);color:#a5b4fc;border:1px solid color-mix(in srgb,var(--c1) 35%,transparent);border-radius:5px;padding:1px 7px;font-family:ui-monospace,monospace}}
.doclink{{font-size:12px;color:var(--accent-cyan)}}
.journey{{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:12px 14px;margin:6px 0 16px}}
.journey .jt{{font-size:11px;color:var(--text-muted);margin-bottom:8px}}
.journey .steps{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.journey .st{{font-size:11.5px;padding:5px 10px;border-radius:20px;background:var(--bg-card);border:1px solid var(--border-color);color:var(--text-muted)}}
.journey .st.on{{background:{GRAD};color:#fff;border-color:transparent;font-weight:700}}
.journey .sep{{color:var(--text-muted)}}
.walk{{margin:10px 0;border:1px solid var(--border-color);border-radius:8px;overflow:hidden}}
.walk .r{{display:flex;gap:10px;padding:8px 10px;font-size:12.5px;border-top:1px solid var(--border-color);line-height:1.65}}
.walk .r:first-child{{border-top:none}}
.walk code{{color:var(--accent-cyan);min-width:140px;font-size:11.5px;flex-shrink:0}}
.loopd{{display:flex;align-items:center;justify-content:center;gap:7px;flex-wrap:wrap;padding:12px 4px}}
.loopd .n{{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:9px;padding:9px 12px;font-size:12px;text-align:center}}
.loopd .n b{{display:block;color:var(--c1)}}
.loopd .a{{color:var(--c2);font-size:16px;font-weight:800}}
.arch-anim{{position:relative;display:flex;flex-direction:column;gap:9px;padding:18px;background:radial-gradient(120% 120% at 50% 0%,color-mix(in srgb,var(--c1) 10%,transparent),transparent 70%);border-radius:14px}}
.arch-row{{position:relative;border:1px solid var(--lc);border-radius:11px;padding:12px 16px;background:var(--bg-card);overflow:hidden}}
.arch-row:before{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--lc) 14%,transparent),transparent);transform:translateX(-100%);animation:sweep 4.5s linear infinite;animation-delay:var(--d)}}
@keyframes sweep{{0%{{transform:translateX(-100%)}}60%,100%{{transform:translateX(100%)}}}}
.arch-row .lbl{{font-size:11px;font-weight:800;letter-spacing:.06em;color:var(--lc);margin-bottom:7px;position:relative}}
.arch-row .boxes{{display:flex;gap:7px;flex-wrap:wrap;position:relative}}
.arch-row .b{{flex:1;min-width:110px;text-align:center;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:7px;padding:8px;font-size:12px}}
.arch-row .b strong{{display:block;color:var(--text-primary);font-size:12.5px;margin-bottom:2px}}
.week-bar{{display:flex;align-items:center;gap:12px;margin:34px 0 14px}}
.week-bar .wk{{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff}}
.week-bar h2{{font-size:17px;margin:0}}.week-bar span{{font-size:12px;color:var(--text-muted)}}
.day-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}}
.day-card{{display:flex;flex-direction:column;gap:8px;background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:17px;text-decoration:none;transition:.2s}}
.day-card:hover{{transform:translateY(-4px);border-color:var(--c1);box-shadow:0 12px 34px color-mix(in srgb,var(--c1) 10%,transparent)}}
.day-card .top{{display:flex;align-items:center;gap:10px}}
.day-card .num{{width:39px;height:39px;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800}}
.day-card h3{{font-size:14.5px;color:var(--text-primary);margin:0}}
.day-card p{{font-size:12.5px;color:var(--text-secondary);margin:0;line-height:1.6;flex:1}}
.day-card .foot{{display:flex;justify-content:space-between}}
.day-card .mins{{font-size:11px;color:var(--text-muted)}}.day-card .go{{font-size:12px;color:var(--c1);font-weight:700}}
.capsule{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px}}
.capsule .pill{{font-size:12px;padding:6px 12px;border-radius:999px;background:color-mix(in srgb,var(--c1) 12%,transparent);border:1px solid color-mix(in srgb,var(--c1) 30%,transparent);color:var(--text-primary);font-weight:600}}
.gtable{{width:100%;border-collapse:collapse;margin:10px 0;font-size:12.5px}}
.gtable th,.gtable td{{border:1px solid var(--border-color);padding:8px 10px;text-align:left;vertical-align:top;line-height:1.55}}
.gtable th{{background:var(--bg-secondary);color:var(--accent-cyan)}}
.check ul{{margin:6px 0 0;padding-left:18px;line-height:1.7;font-size:13px;color:var(--text-secondary)}}
.story{{font-size:14px;line-height:1.85;color:var(--text-secondary);margin:8px 0 12px}}
.step-list{{margin:8px 0;padding-left:18px;font-size:13px;line-height:1.85;color:var(--text-secondary)}}
.nav-prevnext{{display:flex;justify-content:space-between;gap:12px;margin:28px 0 8px;flex-wrap:wrap}}
.nav-prevnext a{{font-size:13px;font-weight:700;color:var(--c1);text-decoration:none}}
"""

NAV_JS = (
    "<script>document.addEventListener('DOMContentLoaded',()=>{"
    "const b=document.getElementById('sidebarToggle'),s=document.getElementById('sidebar');"
    "if(b&&s)b.onclick=()=>s.classList.toggle('open');"
    "const links=document.querySelectorAll('[data-section]'),sections=document.querySelectorAll('section[id]');"
    "const ob=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)"
    "links.forEach(a=>a.classList.toggle('active',a.dataset.section===e.target.id))}),"
    "{rootMargin:'-25% 0px -65% 0px'});sections.forEach(x=>ob.observe(x));});</script>"
)

# ─── 20 days curriculum ───────────────────────────────────────────────
# Each day: title, focus (doc path label), analogy, blurb, doc_url, capsules,
# lessons: list of (heading, html body), try_it, pitfalls, qa

DAYS: list[dict] = []


def day(
    title: str,
    focus: str,
    analogy: str,
    blurb: str,
    doc: str,
    capsules: list[str],
    lessons: list[tuple[str, str]],
    try_it: str,
    pitfalls: str,
    qa: list[tuple[str, str]],
) -> None:
    DAYS.append(
        {
            "title": title,
            "focus": focus,
            "analogy": analogy,
            "blurb": blurb,
            "doc": doc,
            "capsules": capsules,
            "lessons": lessons,
            "try_it": try_it,
            "pitfalls": pitfalls,
            "qa": qa,
        }
    )


# Stage 1
day(
    "认识 WorkBuddy：办公搭子不是聊天框",
    "Overview",
    "会动手的全能秘书，不只会说话",
    "搞清它和传统 AI 对话的区别：能规划、能执行、能交付可验收成果。",
    f"{DOC}/Overview",
    [
        "WorkBuddy = 全场景 AI 办公工作台",
        "说出要求 → 自主规划执行 → 交付成果",
        "能操作本地授权文件夹，不只吐文字",
    ],
    [
        (
            "它是什么",
            "<p>腾讯出品的全场景 AI 办公工作台：说出要求、开始执行任务、交付完整成果，并连接腾讯办公生态。</p>"
            "<div class='baby'><span class='t'>大白话</span>传统聊天 AI 像「顾问」：给你建议你自己做；WorkBuddy 像「秘书」：听完就去整理文件、出报告、改 PPT。</div>",
        ),
        (
            "四项核心能力",
            "<table class='gtable'><tr><th>能力</th><th>含义</th></tr>"
            "<tr><td>理解自然语言</td><td>一句话下达任务，无需复杂步骤</td></tr>"
            "<tr><td>自主规划执行</td><td>自动拆解、规划步骤、执行操作</td></tr>"
            "<tr><td>多模态任务</td><td>文档、表格、PPT、数据分析等</td></tr>"
            "<tr><td>本地文件操作</td><td>读取授权文件夹，批量处理</td></tr></table>",
        ),
        (
            "对比传统 AI 对话",
            "<table class='gtable'><tr><th>传统 AI 对话</th><th>WorkBuddy</th></tr>"
            "<tr><td>只能对话建议</td><td>实际执行任务</td></tr>"
            "<tr><td>手动操作文件</td><td>自动操作本地文件</td></tr>"
            "<tr><td>单步简单任务</td><td>多步复杂任务</td></tr>"
            "<tr><td>输出文字回复</td><td>交付可验收结果</td></tr></table>",
        ),
        (
            "适用场景速览",
            "<ul class='step-list'><li>文档生成：报告、技术文档、会议纪要</li>"
            "<li>数据分析与可视化</li><li>PPT / 报告生成</li>"
            "<li>深度研究与调研报告</li><li>邮件、周报等办公场景</li>"
            "<li>批量整理、重命名、格式转换</li></ul>",
        ),
    ],
    "用一句话向同事解释：WorkBuddy 和 ChatGPT 类产品差在哪？（关键词：执行、本地文件、可验收产物）",
    "别把它当成「只会聊天的网页」——核心价值在「任务闭环交付」。",
    [
        ("Q：和 CodeBuddy IDE 是同一个东西吗？", "A：同属腾讯云代码助手产品矩阵。IDE/插件/CLI 偏编程；WorkBuddy 偏全场景办公任务执行。"),
        ("Q：必须会编程吗？", "A：不需要。产品定位覆盖产品、设计、办公与开发协作。"),
    ],
)

day(
    "快速开始：界面三区与第一印象",
    "Quickstart",
    "进办公室先认门牌：左列表、中对话、右结果",
    "进入产品、看清主界面结构，知道任务从哪进、结果从哪出。",
    f"{DOC}/Quickstart",
    ["左侧任务列表", "中间对话执行区", "右侧结果 / 预览区"],
    [
        (
            "怎么进入",
            "<p>从官网下载桌面端，微信扫码登录（个人 / 企业）。安装与登录细节见 Day 03。</p>"
            f"<p class='doclink'>官方：<a href='{DOC}/Quickstart' target='_blank'>{DOC}/Quickstart</a></p>",
        ),
        (
            "界面基本结构",
            "<div class='loopd'><span class='n'><b>左</b>任务列表</span><span class='a'>→</span>"
            "<span class='n'><b>中</b>对话与执行</span><span class='a'>→</span>"
            "<span class='n'><b>右</b>产物与预览</span></div>"
            "<div class='walk'><div class='r'><code>左侧</code>查看、筛选、切换已有任务</div>"
            "<div class='r'><code>中间</code>描述需求、追问、看执行过程</div>"
            "<div class='r'><code>右侧</code>产物、全部文件、变更、浏览器预览</div></div>",
        ),
        (
            "建议阅读顺序（官方）",
            "<ol class='step-list'><li>快速开始</li><li>创建任务</li><li>任务管理</li>"
            "<li>任务对话</li><li>结果查看</li></ol>"
            "<div class='essence'><span class='t'>本教程主线</span>在官方五步之上，再覆盖技能、项目、连接器、助理、自动化与提效。</div>",
        ),
    ],
    "打开 WorkBuddy，指着屏幕说出左/中/右三区各自干什么。",
    "第一次别急着点满所有侧栏入口；先把「创建→对话→看结果」走通。",
    [("Q：小程序和桌面端怎么配合？", "A：移动端发任务可在「助理」里查看；桌面端是完整工作台。")],
)

day(
    "安装登录：跑通第一个真实任务",
    "FirstTask",
    "领钥匙、进门、交第一份工单",
    "官网下载安装 → 微信扫码登录 → 新建任务 → 看产物。",
    f"{DOC}/FirstTask",
    ["workbuddy.cn 下载", "微信扫码登录", "新建任务 → 发送 → 右侧产物"],
    [
        (
            "安装五步",
            "<ol class='step-list'><li>访问 <a href='https://www.workbuddy.cn/' target='_blank'>workbuddy.cn</a>，悬停下载选本机版本</li>"
            "<li>双击安装包</li><li>选择安装用户（建议「仅为我安装」）</li>"
            "<li>选择安装位置</li><li>完成安装</li></ol>",
        ),
        (
            "登录",
            "<p>点击登录 → 浏览器微信扫码。个人选「个人」，企业版用户选「企业」。</p>",
        ),
        (
            "第一个任务闭环",
            "<ol class='step-list'><li>点「新建任务」</li>"
            "<li>在对话框描述要求（例如：帮我写一份本周工作周报大纲）</li>"
            "<li>点发送，观察中间执行过程</li>"
            "<li>打开右侧窗口：产物里找目标文件；概览-工作空间文件看其他文件</li></ol>"
            "<div class='baby'><span class='t'>小贴士</span>移动端发的任务在「助理」中查看；桌面「新建任务」是 PC 主路径。</div>",
        ),
    ],
    "完成一次：安装（若未装）→ 登录 → 新建任务 → 在右侧产物里找到生成文件。",
    "登录失败常见于未设默认浏览器或目录权限；详见 Day 19 FAQ。",
    [("Q：企业和个人登录有何不同？", "A：入口分流；企业版能力与套餐以账号侧为准。")],
)

# Stage 2
day(
    "创建任务：一句话怎么说才算工单",
    "Create-Task",
    "写清楚：做什么、有什么、输出成什么样",
    "自然语言描述、选工作空间、@ 引用与上传上下文。",
    f"{DOC}/Create-Task",
    ["自然语言下达", "选择工作空间", "@ 引用 / 粘贴截图 / 上传文件"],
    [
        (
            "好的任务描述示例",
            "<ul class='step-list'>"
            "<li>帮我把这份销售数据生成分析报告，包含图表</li>"
            "<li>整理 Downloads 里的图片，按日期分类</li>"
            "<li>根据会议纪要生成 PPT</li>"
            "<li>分析简历，提取关键信息生成表格</li>"
            "<li>调研某年 AI 趋势，写一份报告</li></ul>",
        ),
        (
            "选择工作空间",
            "<p>点输入框左下角「选择工作空间」指定目录；也可直接开始，在默认目录生成结果。</p>",
        ),
        (
            "添加上下文",
            "<table class='gtable'><tr><th>方式</th><th>说明</th></tr>"
            "<tr><td>引用上下文</td><td>用 @ 引用文件、文档、规则</td></tr>"
            "<tr><td>粘贴截图</td><td>Ctrl/Cmd + V</td></tr>"
            "<tr><td>上传文件</td><td>按钮或拖拽到输入框</td></tr>"
            "<tr><td>补充说明</td><td>目标、范围、约束、预期输出</td></tr></table>"
            "<div class='essence'><span class='t'>优先写清</span>目标是什么 / 输入是什么 / 输出格式 / 约束条件。</div>",
        ),
        (
            "创建成功后发生什么",
            "<ol class='step-list'><li>左侧出现新任务</li><li>中间展示执行过程</li>"
            "<li>右侧展示产物、文件、变更、预览</li><li>可继续追问或并行开新任务</li></ol>",
        ),
    ],
    "用「目标+输入+输出格式+约束」重写一条你昨天发过的模糊需求，再发一次对比结果。",
    "只说「帮我整理一下」几乎必翻车——缺少路径、格式与验收标准。",
    [("Q：必须选工作空间吗？", "A：不必；未选则用默认目录。要处理本地文件时再指定更稳。")],
)

day(
    "任务管理：列表、状态与并行",
    "Task-Management",
    "工单看板：找得到、筛得清、续得上",
    "任务列表、状态筛选、继续处理已有任务。",
    f"{DOC}/Task-Management",
    ["左侧任务列表是入口", "按状态筛选", "点进旧任务可续聊"],
    [
        (
            "任务列表做什么",
            "<p>查看历史任务、切换当前任务、按状态筛选、继续未完成工作。</p>",
        ),
        (
            "常见状态心智",
            "<div class='baby'><span class='t'>大白话</span>把每个任务想成一张工单：进行中、已完成、可继续。切换任务不会丢上下文（在该任务内）。</div>",
        ),
        (
            "并行推进",
            "<p>可以同时创建多个任务并行推进；每个任务有独立对话与工作空间语境。</p>",
        ),
    ],
    "创建两个短任务，用左侧列表来回切换，确认各自上下文独立。",
    "别在一个任务里塞互不相关的大杂烩——难追溯、难分享。",
    [("Q：任务太多找不到？", "A：用状态筛选 + 对话内搜索（Day 06 顶部操作）。")],
)

day(
    "任务对话：追问、上传与中断",
    "Conversation",
    "跟勤奋实习生多轮打磨，而不是一轮定生死",
    "输入追问、顶部操作、文件上传、执行过程与中断继续。",
    f"{DOC}/Conversation",
    ["多轮追问带上下文", "顶部：搜索/分享/历史/详情面板", "可随时停止执行"],
    [
        (
            "对话区怎么用",
            "<ul class='step-list'><li>输入需求或补充说明，回车或点发送</li>"
            "<li>在已有任务中追问，无需重复背景</li>"
            "<li>执行中查看回复、结果与中间步骤</li></ul>",
        ),
        (
            "顶部操作（左→右）",
            "<ol class='step-list'><li>对话内搜索</li><li>分享任务（公开链接）</li>"
            "<li>历史提问（可跳转）</li><li>显示详情面板（右侧产物/文件/变更/浏览器）</li></ol>",
        ),
        (
            "适合直接发的内容",
            "<ul class='step-list'><li>新需求：再加一个饼图</li>"
            "<li>修改意见：表格按销售额排序</li>"
            "<li>继续追问：导出 PDF / 分析环比</li></ul>",
        ),
        (
            "文件与隐私边界",
            "<p>支持 PDF/Word/Excel/PPT/图片/压缩包/代码等。默认本地处理；仅授权文件夹可访问；高危操作需二次确认。</p>"
            "<div class='pitfall'><span class='t'>上传失败</span>检查格式；大文件先压缩拆分；检查网络。</div>",
        ),
        (
            "中断与继续",
            "<p>执行中输入区有停止入口。中断后仍可基于已有进度继续追问或改需求。</p>",
        ),
    ],
    "对同一任务发三轮：出大纲 → 改语气 → 指定导出格式。体会多轮校准。",
    "第一轮不满意就放弃最可惜——先指出「哪里不对」。",
    [("Q：粘贴截图快捷键？", "A：Ctrl/Cmd + V。")],
)

day(
    "结果查看：产物、文件、变更、预览",
    "Results",
    "交货验收台：东西在哪、改了啥、能不能打开看",
    "右侧结果区：产物、全部文件、变更、内置预览。",
    f"{DOC}/Results",
    ["产物 = 目标交付物", "工作空间文件 = 过程文件", "变更可追溯"],
    [
        (
            "右侧结果区",
            "<p>按任务类型展示产物、全部文件、变更和预览，无需离开当前任务。</p>",
        ),
        (
            "怎么找文件",
            "<div class='walk'><div class='r'><code>产物</code>生成的目标文件（报告、PPT、表格等）</div>"
            "<div class='r'><code>概览·工作空间</code>任务产生的其他相关文件</div>"
            "<div class='r'><code>变更</code>对话过程中的文件变更</div>"
            "<div class='r'><code>预览</code>内置浏览器 / 文档预览</div></div>",
        ),
        (
            "验收习惯",
            "<div class='essence'><span class='t'>验收口诀</span>打开产物 → 抽查关键页 → 不合意就回中间对话改一刀，别整单重开（除非方向全错）。</div>",
        ),
    ],
    "完成任意任务后，只通过右侧面板导出/打开产物，不依赖聊天里的摘要。",
    "聊天区摘要≠最终文件；以产物区文件为准。",
    [("Q：预览打不开？", "A：先下载产物用本机软件打开；再查格式是否受支持。")],
)

# Stage 3
day(
    "新建任务栏：本地 AI 工作台入口",
    "Task-Bar",
    "前台接待台：从这里开单、选模式、挂技能",
    "任务栏是日常最高频入口：模式、输入、附件与快捷能力。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Task-Bar",
    ["任务栏 = 主开单台", "先选对场景再开写", "技能/连接器可挂在任务上"],
    [
        (
            "为什么单独学任务栏",
            "<p>官方「从入门到精通」把新建任务栏作为功能说明第一站：本地 AI 工作台的主入口。</p>",
        ),
        (
            "使用建议",
            "<ul class='step-list'><li>开单前先想清：本地文件任务还是纯生成</li>"
            "<li>需要外部服务时先确认连接器已授权</li>"
            "<li>需要固定套路时启用相关 Skill</li></ul>",
        ),
    ],
    "从任务栏连续开 2 个不同类型任务（例如：周报 + 表格分析），观察默认选项差异。",
    "不要把任务栏当唯一入口——项目、助理、自动化另有路径。",
    [("Q：和「创建任务」文档什么关系？", "A：Create-Task 讲工单内容；Task-Bar 讲界面入口与控件。")],
)

day(
    "设计创意：从想法到可视稿",
    "Design-Idea",
    "设计工坊：草图/描述进，视觉稿出",
    "用自然语言或草图驱动设计向产出，再迭代风格。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Design-Idea",
    ["自然语言 / 草图 → 设计", "组件与风格可迭代", "设计稿可接后续研发任务"],
    [
        (
            "定位",
            "<p>设计创意能力帮助从需求描述或草图快速得到可讨论的视觉方案，再通过对话调整风格与布局。</p>",
        ),
        (
            "实操建议",
            "<ul class='step-list'><li>先给受众与场景（对内汇报 / 对外官网）</li>"
            "<li>约束尺寸、品牌色、必须出现的模块</li>"
            "<li>第一版只求方向对，第二版再抠细节</li></ul>",
        ),
    ],
    "用一句话描述一个活动海报需求，生成后追问「更简洁、主色改蓝」。",
    "一次要求「完美终稿」容易翻车；先方向后细节。",
    [("Q：能直接当生产设计用吗？", "A：适合快速方案与迭代；最终规范以设计同学确认为准。")],
)

day(
    "助理：手机遥控电脑上的 WorkBuddy",
    "Assistant",
    "遥控器：手机发指令，电脑执行，结果回手机",
    "远程任务 vs 普通任务；微信/企微/飞书/钉钉等接入。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Assistant",
    ["助理 = 远程控制", "专属助理文件夹", "本地优先普通任务"],
    [
        (
            "是什么",
            "<p>通过手机 IM（微信、企微、QQ、钉钉、飞书等）远程控制电脑上的 WorkBuddy 执行任务，完成后回传到手机。</p>",
        ),
        (
            "远程 vs 普通任务",
            "<table class='gtable'><tr><th>对比</th><th>普通任务</th><th>助理</th></tr>"
            "<tr><td>工作目录</td><td>自由指定</td><td>固定助理专属文件夹</td></tr>"
            "<tr><td>对话</td><td>可多任务并行</td><td>单会话集中处理</td></tr>"
            "<tr><td>上下文</td><td>可清空重开</td><td>保留完整历史</td></tr></table>"
            "<div class='essence'><span class='t'>建议</span>本地操作优先普通任务；远程触发再用助理。</div>",
        ),
        (
            "典型场景",
            "<ul class='step-list'><li>出门在外处理文件</li><li>会议中生成纪要</li>"
            "<li>通勤路上准备材料</li><li>临时需求随时下达</li></ul>",
        ),
    ],
    "打开助理页，确认已绑定至少一个 IM；发一条无害测试指令（如生成一段短文）。",
    "注意远程控制安全边界：授权范围、解绑方式见官方助理文档。",
    [("Q：推荐哪个接入？", "A：官方推荐微信助理（WeixinBot-Guide）。")],
)

day(
    "项目：团队共享指令·技能·资料",
    "Project",
    "项目组共享工具箱：进组自动带装备",
    "项目配置注入任务；动态、资产库、分享协作。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Project",
    ["项目 = 共享上下文容器", "指令/连接器/专家/技能自动注入", "资料库以 RAG 注入"],
    [
        (
            "项目是什么",
            "<p>把指令、连接器、专家、技能和资料统一组织；成员在项目中开任务时自动注入，无需每次重复设置。</p>",
        ),
        (
            "项目配置项",
            "<ul class='step-list'><li>名称</li><li>指令（全局行为规则）</li>"
            "<li>连接器</li><li>专家</li><li>技能（Skill）</li></ul>",
        ),
        (
            "动态与资产",
            "<p>动态分：与我有关 / 成员动态 / 自动化通知。资产库支持上传与保存产物，并以 RAG 注入任务上下文。</p>",
        ),
    ],
    "若有团队：建一个测试项目，写一条项目指令「回复必须用表格」，开任务验证是否生效。",
    "个人试用也可建私有项目练「指令+资料」注入，别一上来分享敏感文件。",
    [("Q：任务和项目什么关系？", "A：任务是项目内的一次对话会话，含独立工作空间。")],
)

day(
    "技能市场：给秘书加专业工具包",
    "Skills-Market",
    "工具柜：安装 Skill = 教会新动作",
    "Skill 扩展可执行能力；安装、启用、安全与积分注意。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market",
    ["Skill = 可执行脚本/工作流", "优先官方推荐", "第三方先审权限"],
    [
        (
            "Skill 是什么",
            "<p>为 WorkBuddy 增加特定工具能力：封装脚本与工作流，在授权下完成发邮件、查股价、读写文件、调 API 等。</p>",
        ),
        (
            "页面两块",
            "<table class='gtable'><tr><th>区域</th><th>内容</th></tr>"
            "<tr><td>技能市场</td><td>推荐技能，一键安装</td></tr>"
            "<tr><td>已安装</td><td>本地技能，对话中可调用</td></tr></table>",
        ),
        (
            "安装方式",
            "<ul class='step-list'><li>上传技能：导入本地技能包</li>"
            "<li>查找技能：描述任务，自动查找相关技能</li></ul>"
            "<div class='pitfall'><span class='t'>安全</span>第三方 Skill 可能外发数据；安装前校验来源、权限与脚本。优先官方推荐。</div>",
        ),
    ],
    "安装 1 个官方推荐 Skill，在对话里明确要求使用它完成一个小动作。",
    "注意积分消耗提醒；不用的技能可关闭/卸载，减少误触发。",
    [("Q：Skill 和连接器区别？", "A：连接器偏外部服务桥梁；Skill 偏可安装的能力包/工作流。")],
)

# Stage 4
day(
    "连接器：邮箱·文档·会议·TAPD",
    "Connector",
    "插线板：把外部服务接进工作流",
    "MCP/CLI 与 Skill/CLI；QQ 邮箱等授权示例。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Connector",
    ["连接器 = 外部能力桥", "支持腾讯文档/乐享/会议/邮箱/TAPD 等", "自定义连接器"],
    [
        (
            "是什么",
            "<p>WorkBuddy 与外部服务的桥梁。技术形态：MCP+CLI 或 Skill+CLI，权限原则一致。</p>",
        ),
        (
            "场景",
            "<table class='gtable'><tr><th>场景</th><th>示例</th></tr>"
            "<tr><td>数据查询</td><td>检索文档、查库</td></tr>"
            "<tr><td>服务调用</td><td>发邮件、建日程</td></tr>"
            "<tr><td>文件管理</td><td>网盘读写</td></tr>"
            "<tr><td>消息通知</td><td>企微/飞书消息</td></tr></table>",
        ),
        (
            "示例：QQ 邮箱",
            "<ol class='step-list'><li>连接器页点 QQ 邮箱 +</li>"
            "<li>用 QQ 邮箱 App 扫码授权</li>"
            "<li>确认账号信息与读信等权限</li></ol>",
        ),
    ],
    "添加一个你常用的连接器（如腾讯文档或邮箱），用自然语言完成一次只读查询。",
    "授权遵循最小权限；不用的连接器及时解除。",
    [("Q：消息框里也能管连接器吗？", "A：可以，支持快捷管理入口。")],
)

day(
    "资料库：腾讯文档 · ima · 乐享",
    "Knowledge-Base",
    "团队书架：资料进库，任务自动参考",
    "腾讯文档、ima 知识库、乐享等资料能力与 RAG 注入。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Knowledge-Base/Tencent-Doc",
    ["资料库支撑 RAG", "腾讯文档/ima/乐享", "先建库再提问质量更高"],
    [
        (
            "为什么需要资料库",
            "<p>项目资产与知识库让 Agent 基于你的真实材料回答，而不是只靠通用模型常识。</p>",
        ),
        (
            "怎么用",
            "<ul class='step-list'><li>把制度、模板、历史报告放入资料库</li>"
            "<li>在项目/任务中引用</li>"
            "<li>提问时写明「仅依据资料库，并标注出处」</li></ul>",
        ),
        (
            "ima 等攻略",
            "<p>官方提供 ima 功能指引、知识复利、OPC/创作者/学业/求职等场景攻略，可按角色深入。</p>",
        ),
    ],
    "上传 1～2 份无敏感文档到资料库，问一个必须引用文中数字的问题，检查是否胡编。",
    "敏感数据先脱敏；确认同步范围与权限。",
    [("Q：和记忆有何不同？", "A：资料库是显式材料；记忆是从会话提取的个人偏好/事实。")],
)

day(
    "记忆与安全沙箱：记住什么、能碰什么",
    "Memory + Permission",
    "备忘录 + 门禁：该记的记，危险的拦",
    "记忆提取/编辑；默认权限与安全沙箱。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Memory",
    ["记忆每晚整理", "可编辑/删除/关闭", "沙箱限制高危与敏感目录"],
    [
        (
            "记忆",
            "<p>从会话提取事实、偏好、人物关系、跟进事项等，后续任务作背景参考。每晚整理，仅本人可见。设置-记忆可查看编辑删除或一键关闭；支持从其他 AI 导入习惯。</p>",
        ),
        (
            "权限与沙箱",
            "<p>只能访问主动授权文件夹；系统敏感目录拦截；高危操作二次确认。先本地后远程，稳扎稳打。</p>"
            f"<p class='doclink'><a href='{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes' target='_blank'>权限模式文档</a></p>",
        ),
    ],
    "打开设置-记忆，看已有摘要；删掉一条不该长期保留的内容。",
    "不要关闭所有安全确认「图省事」——尤其是批量删改文件时。",
    [("Q：记忆会训练模型吗？", "A：按官方隐私说明：服务端处理片段用后即弃，不用于训练；以当前文档为准。")],
)

# Stage 5
day(
    "模型配置与系统设置",
    "Model + Setting",
    "引擎档位与偏好面板",
    "选模型、调设置、管数据与反馈入口。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Model",
    ["模型影响质量与积分", "设置里集中偏好", "数据管理可清理"],
    [
        (
            "模型配置",
            "<p>按任务难度与成本选择合适模型；复杂分析/长文可偏强模型，简单整理可偏快模型。</p>",
        ),
        (
            "系统设置",
            f"<p>系统设置汇集偏好、权限、记忆、数据管理、帮助与反馈等。"
            f"<a class='doclink' href='{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Setting' target='_blank'>设置文档</a></p>",
        ),
    ],
    "对比同一简单任务在两个模型下的耗时与结果差异（记一笔笔记）。",
    "不要默认永远最贵模型——先匹配任务。",
    [("Q：积分不够怎么办？", "A：见套餐/用量/定价页（Day 20）。")],
)

day(
    "自动化：让重复工单自己跑",
    "Automation-Guide",
    "定时/触发的流水线工人",
    "把高频重复任务交给自动化，并关注通知与权限。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide",
    ["自动化减少重复劳动", "通知可在项目动态查看", "先手动跑通再自动化"],
    [
        (
            "适用",
            "<ul class='step-list'><li>每日/每周固定报告</li>"
            "<li>定期整理某文件夹</li>"
            "<li>固定格式的汇总邮件</li></ul>",
        ),
        (
            "落地步骤",
            "<ol class='step-list'><li>先用普通任务手动跑通一遍</li>"
            "<li>固化提示词与输出格式</li>"
            "<li>再配置自动化与通知</li></ol>",
        ),
    ],
    "选一个每周都做的小事，写出可复用的任务描述模板（先不配自动也行）。",
    "未验证的流程不要直接全自动对接生产邮箱/群。",
    [("Q：自动化失败如何排查？", "A：看项目动态中的自动化通知与任务执行日志。")],
)

day(
    "微信助理接入（推荐）",
    "WeixinBot-Guide",
    "把遥控器绑到微信",
    "按官方推荐路径接入微信助理，完成远程闭环。",
    f"{DOC}/WeixinBot-Guide",
    ["官方推荐微信助理", "电脑在线才能执行", "注意解绑与权限"],
    [
        (
            "为何先学微信",
            "<p>助理多平台中官方推荐微信助理；打通后最容易形成「手机下达 → 电脑执行」习惯。</p>",
        ),
        (
            "接入要点",
            "<ol class='step-list'><li>打开官方微信助理接入指南逐步操作</li>"
            "<li>确认电脑端 WorkBuddy 在线</li>"
            "<li>用无害指令验收回传</li></ol>"
            "<p>其他：企微 / QQ / 元宝 / 飞书 / 钉钉见对应 Guide。</p>",
        ),
    ],
    "按 WeixinBot-Guide 完成绑定（或读完标注卡点），发一条测试任务。",
    "公共场合勿口述含密码/密钥的指令。",
    [("Q：解绑后怎样？", "A：远程指令失效；历史记录处理见助理文档「解绑」节。")],
)

# Stage 6
day(
    "提效技巧 + FAQ 排障",
    "Efficient-Tips / FAQ",
    "高手清单 + 检修手册",
    "三要素/小步/多轮提效法，以及安装登录与工作空间常见故障。",
    f"{DOC}/From-Beginner-to-Expert-Guide/Efficient-Tips",
    ["做什么+有什么+怎么样", "小步多轮", "工作空间可找回"],
    [
        (
            "三要素公式",
            "<div class='essence'><span class='t'>清晰表达</span>做什么 + 有什么（路径/材料）+ 怎么样（格式/约束）。别让 AI 猜意图。</div>"
            "<p><b>反面</b>：帮我把上次会议纪要整理一下。<br>"
            "<b>正面</b>：把 <code>D:/会议纪要/0320.docx</code> 整理成清单：结论、责任人、截止日期；争议项标记；表格输出，不要开场白。</p>",
        ),
        (
            "小步快跑与多轮打磨",
            "<p>大任务拆三轮：先提炼结论 → 再大纲 → 再扩写单页。不满意就指出问题、补约束、换角色视角，别一轮放弃。</p>"
            "<p>敏感操作：先本地后远程。</p>",
        ),
        (
            "FAQ：工作空间消失",
            "<p>升级/重启后界面看不到原工作空间时，到本机目录找回：</p>"
            "<ul class='step-list'><li>Windows：<code>C:\\Users\\&lt;用户名&gt;\\workbuddy</code></li>"
            "<li>Mac：<code>/Users/用户名/WorkBuddy</code></li></ul>"
            f"<p class='doclink'>完整 FAQ：<a href='{DOC}/From-Beginner-to-Expert-Guide/FAQ' target='_blank'>FAQ</a></p>",
        ),
        (
            "FAQ：登录失败",
            "<ul class='step-list'><li>设置默认浏览器后重试，或复制链接到浏览器验证</li>"
            "<li>检查 CodeBuddyExtension 目录权限（官方 chown / icacls）</li>"
            "<li>排查安全软件拦截</li>"
            "<li>仍未解决：<a href='mailto:workbuddy@tencent.com'>workbuddy@tencent.com</a></li></ul>",
        ),
    ],
    "把一条失败需求按三要素重写；并确认本机 WorkBuddy 数据目录路径记在笔记里。",
    "不要随手删整个 workbuddy 目录；也不要一口气丢「重构整个项目」类需求。",
    [
        ("Q：不会写提示词？", "A：先问：「我想做 XX，你需要我提供哪些信息？」"),
        ("Q：Mac 权限命令？", "A：见官方 FAQ 的 chown 示例。"),
    ],
)

day(
    "收官：矩阵复盘 · 积分套餐 · 多端",
    "Pricing + 复盘",
    "毕业答辩：能讲清全链路，并知道成本与多端",
    "串起 20 天地图；了解定价积分；小程序/移动端定位。",
    f"{DOC}/Pricing",
    ["任务闭环主线已通", "扩展：技能/项目/连接器/助理", "关注用量与套餐"],
    [
        (
            "20 天能力地图",
            "<div class='loopd'><span class='n'><b>认识</b></span><span class='a'>→</span>"
            "<span class='n'><b>开单</b></span><span class='a'>→</span>"
            "<span class='n'><b>对话</b></span><span class='a'>→</span>"
            "<span class='n'><b>验收</b></span><span class='a'>→</span>"
            "<span class='n'><b>扩展</b></span><span class='a'>→</span>"
            "<span class='n'><b>远程</b></span></div>",
        ),
        (
            "账号与成本",
            f"<p>阅读 <a href='{DOC}/Pricing' target='_blank'>定价</a>、"
            f"<a href='{DOC}/Credits' target='_blank'>积分</a>、"
            f"<a href='{DOC}/Usage' target='_blank'>用量</a>、"
            f"<a href='{DOC}/Plan' target='_blank'>套餐</a>，建立成本意识。</p>",
        ),
        (
            "多端",
            "<p>WorkBuddy 小程序 / 移动端与桌面协同；远程任务走助理。文档站顶栏可切换。</p>",
        ),
        (
            "和 CodeBuddy 编程矩阵",
            "<p>编程深潜用 IDE/插件/CLI；办公交付用 WorkBuddy。按场景选工具，而不是互斥。</p>",
        ),
    ],
    "用 3 分钟向同事演示：创建任务 → 追问 → 右侧打开产物；并说明何时用助理。",
    "别只会聊天不会验收文件——产物区才是交付物。",
    [
        ("Q：学完下一步？", "A：选 1 个真实周报/研究任务固化模板；再接 1 个连接器 + 微信助理。"),
        ("Q：官方文档入口？", "A：https://www.codebuddy.cn/docs/workbuddy/Overview"),
    ],
)

assert len(DAYS) == 20

STAGES = [
    {"id": 1, "name": "认识与上手", "lo": 1, "hi": 3, "blurb": "是什么、界面、安装跑通首任务"},
    {"id": 2, "name": "任务主循环", "lo": 4, "hi": 7, "blurb": "创建、管理、对话、结果验收"},
    {"id": 3, "name": "核心能力区", "lo": 8, "hi": 12, "blurb": "任务栏、设计、助理、项目、技能"},
    {"id": 4, "name": "连接与记忆", "lo": 13, "hi": 15, "blurb": "连接器、资料库、记忆与沙箱"},
    {"id": 5, "name": "设置与远程", "lo": 16, "hi": 18, "blurb": "模型设置、自动化、微信助理"},
    {"id": 6, "name": "提效与收官", "lo": 19, "hi": 20, "blurb": "提效+排障、复盘与多端成本"},
]


def stage_of(d: int) -> dict:
    for s in STAGES:
        if s["lo"] <= d <= s["hi"]:
            return s
    return STAGES[-1]


def render_hub() -> str:
    layers = [
        ("接入层", ["桌面端", "小程序", "移动端", "IM 助理"]),
        ("任务层", ["创建任务", "对话追问", "任务管理"]),
        ("能力层", ["技能", "连接器", "设计创意", "自动化"]),
        ("协作层", ["项目", "资料库", "专家", "分享"]),
        ("安全层", ["授权文件夹", "沙箱", "记忆可控", "二次确认"]),
    ]
    arch = ""
    for i, (name, items) in enumerate(layers):
        lc = C1 if i % 2 == 0 else C2
        boxes = "".join(f"<div class='b'><strong>{esc(x)}</strong>本层</div>" for x in items)
        arch += f"<div class='arch-row' style='--lc:{lc};--d:{i*0.55}s'><div class='lbl'>L{len(layers)-i} · {esc(name)}</div><div class='boxes'>{boxes}</div></div>"

    stage_html = ""
    for s in STAGES:
        cards = ""
        for d in range(s["lo"], s["hi"] + 1):
            info = DAYS[d - 1]
            cards += (
                f"<a class='day-card' href='workbuddy-day{d:02}.html'><div class='top'>"
                f"<div class='num' style='background:{GRAD}'>{d:02}</div>"
                f"<h3>{esc(info['title'])}</h3></div>"
                f"<p><code>{esc(info['focus'])}</code>：{esc(info['blurb'])}</p>"
                f"<div class='foot'><span class='mins'>≈30 min · 产品实战</span><span class='go'>开始学 →</span></div></a>"
            )
        stage_html += (
            f"<div class='week-bar' id='stage{s['id']}'><div class='wk' style='background:{GRAD}'>S{s['id']}</div>"
            f"<h2>阶段 {s['id']} · {esc(s['name'])}</h2>"
            f"<span>D{s['lo']:02}-D{s['hi']:02} · {esc(s['blurb'])}</span></div>"
            f"<div class='day-grid'>{cards}</div>"
        )

    stage_nav = "".join(
        f"<li><a href='#stage{s['id']}' class='nav-link'>阶段 {s['id']} · {esc(s['name'])}（D{s['lo']:02}-D{s['hi']:02}）</a></li>"
        for s in STAGES
    )

    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WorkBuddy 学习 · 20 天总目录</title>
<link rel="stylesheet" href="style.css"><style>{EXTRA_CSS}</style></head><body>
<nav class="sidebar" id="sidebar"><div class="sidebar-header"><div class="logo" style="background:{GRAD}">{LOGO}</div>
<h2>WorkBuddy</h2><p class="version">腾讯 AI 办公 · 20 天产品学习</p></div>
<ul class="nav-list"><li class="nav-group-title">总目录</li>
<li><a href="#intro" class="nav-link active">开篇 · 这是什么</a></li>
<li><a href="#arch" class="nav-link">能力全景（动图）</a></li>
<li><a href="#how" class="nav-link">怎么使用教程</a></li>
<li class="nav-group-title">6 阶段 · 20 天</li>{stage_nav}
<li class="nav-group-title">导航</li>
<li><a href="index.html" class="nav-link" style="color:var(--accent-cyan)">← 返回博客首页</a></li>
<li><a href="{DOC}/Overview" class="nav-link" target="_blank" style="color:var(--accent-cyan)">官方文档 ↗</a></li>
</ul></nav>
<button class="sidebar-toggle" id="sidebarToggle">☰</button>
<main class="content" id="content">
<div class="part-header"><span class="part-label">产品实战学习 · 零基础友好 · 官方文档驱动 · 20 天</span>
<h1 class="part-title">WorkBuddy 学习教程</h1>
<p class="part-desc"><strong>腾讯出品的全场景 AI 办公工作台：说出要求、自主执行、交付可验收成果</strong>。
这不是源码精读，而是按官方文档拆成的 20 天上手路线：每天约 30 分钟，先类比建立直觉，再对照文档动手开任务。</p></div>

<section id="intro" class="section"><div class="section-header"><span class="section-number">00</span><h1>开篇 · 这是个什么产品</h1></div>
<div class="card">
<div class="goal-box"><span class="gt">🎯 学完 20 天你能做到</span>独立完成：安装登录 → 创建并多轮打磨任务 → 在右侧验收产物 → 按需使用技能/连接器/项目 → 用微信助理远程下达任务；并能讲清它和「只会聊天的 AI」差在哪。</div>
<p class="story"><strong>WorkBuddy</strong> 可以先想成一位<strong>会动手的全能办公秘书</strong>：你下工单，它规划步骤、读写授权文件、生成报告/PPT/表格，把结果放到可验收的产物区。
它和 CodeBuddy IDE/插件/CLI 同属腾讯云代码助手矩阵，但主战场是<strong>办公任务交付</strong>而非写代码。</p>
<div class="essence"><span class="t">💡 20 天主线</span>认识产品 → 跑通任务闭环（创建·对话·结果）→ 扩展能力（技能·项目·连接器）→ 远程助理与自动化 → 提效技巧与排障收官。</div>
<div class="baby"><span class="t">👶 大白话</span>别背功能清单。每天只练一个动作，但始终知道自己在「开单 → 执行 → 验收」哪一环。</div>
<p class="doclink">官方入口：<a href="{DOC}/Overview" target="_blank">{DOC}/Overview</a> · 下载：<a href="https://www.workbuddy.cn/" target="_blank">workbuddy.cn</a></p>
</div></section>

<section id="arch" class="section"><div class="section-header"><span class="section-number">01</span><h1>能力全景（动起来看）</h1></div>
<div class="card"><p>发光扫过的每一层，都是一次办公任务可能经过的站点。</p>
<div class="arch-anim">{arch}</div>
<div class="loopd"><span class="n"><b>输入</b>自然语言工单</span><span class="a">→</span>
<span class="n"><b>规划</b>拆解步骤</span><span class="a">→</span>
<span class="n"><b>执行</b>文件/技能/连接器</span><span class="a">→</span>
<span class="n"><b>交付</b>产物验收</span></div>
<div class="tradeoff"><span class="t">设计取舍</span>「能执行」意味着权限与安全沙箱必须存在：授权文件夹、二次确认、远程边界——换来的是可落地的自动化办公。</div>
</div></section>

<section id="how" class="section"><div class="section-header"><span class="section-number">02</span><h1>怎么使用这份教程</h1></div>
<div class="feature-grid">
<div class="feature-item"><div class="feature-icon">⏱️</div><h4>每天 ≈30 分钟</h4><p>先问问题，再本质与大白话，最后动手验收。</p></div>
<div class="feature-item"><div class="feature-icon">📘</div><h4>对照官方文档</h4><p>每天标注文档路径，细节以官网最新版为准。</p></div>
<div class="feature-item"><div class="feature-icon">🧪</div><h4>先验证再扩展</h4><p>先跑通本地任务闭环，再接技能/远程/自动化。</p></div>
<div class="feature-item"><div class="feature-icon">🧭</div><h4>可迁移方法</h4><p>学会「工单三要素 + 小步多轮」，换任何 Agent 产品都通用。</p></div>
</div></section>
{stage_html}
</main>{NAV_JS}</body></html>"""


def render_day(n: int) -> str:
    info = DAYS[n - 1]
    stage = stage_of(n)
    capsules = "".join(f"<span class='pill'>{esc(c)}</span>" for c in info["capsules"])
    lessons_html = ""
    for i, (h, body) in enumerate(info["lessons"], 1):
        lessons_html += (
            f"<section id='l{i}' class='section'><div class='section-header'>"
            f"<span class='section-number'>{i:02}</span><h1>{esc(h)}</h1></div>"
            f"<div class='card'>{body}</div></section>"
        )
    qa_html = "".join(
        f"<p class='q'>Q：{esc(q)}</p><p class='a'>A：{esc(a)}</p>" for q, a in info["qa"]
    )
    lesson_nav = "".join(
        f"<li><a href='#l{i}' class='nav-link' data-section='l{i}'>{esc(h)}</a></li>"
        for i, (h, _) in enumerate(info["lessons"], 1)
    )
    prev_link = (
        f"<a href='workbuddy-day{n-1:02}.html'>← Day {n-1:02}</a>"
        if n > 1
        else "<a href='workbuddy-tutorial.html'>← 总目录</a>"
    )
    next_link = (
        f"<a href='workbuddy-day{n+1:02}.html'>Day {n+1:02} →</a>"
        if n < 20
        else "<a href='workbuddy-tutorial.html'>回总目录 →</a>"
    )
    journey_steps = []
    for d in range(1, 21):
        cls = " on" if d == n else ""
        journey_steps.append(f"<span class='st{cls}'>D{d:02}</span>")
        if d < 20:
            journey_steps.append("<span class='sep'>·</span>")

    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Day {n:02} · {esc(info['title'])} — WorkBuddy</title>
<link rel="stylesheet" href="style.css"><style>{EXTRA_CSS}</style></head><body>
<nav class="sidebar" id="sidebar"><div class="sidebar-header"><div class="logo" style="background:{GRAD}">{n:02}</div>
<h2>WorkBuddy</h2><p class="version">Day {n:02} · {esc(stage['name'])}</p></div>
<ul class="nav-list">
<li class="nav-group-title">本课</li>
<li><a href="#goal" class="nav-link active" data-section="goal">今日目标</a></li>
{lesson_nav}
<li><a href="#try" class="nav-link" data-section="try">动手验收</a></li>
<li><a href="#qa" class="nav-link" data-section="qa">Q&A</a></li>
<li class="nav-group-title">导航</li>
<li><a href="workbuddy-tutorial.html" class="nav-link" style="color:var(--accent-green)">总目录 Hub</a></li>
<li><a href="{esc(info['doc'])}" class="nav-link" target="_blank" style="color:var(--accent-cyan)">官方文档 ↗</a></li>
<li><a href="index.html" class="nav-link" style="color:var(--accent-cyan)">← 首页</a></li>
</ul></nav>
<button class="sidebar-toggle" id="sidebarToggle">☰</button>
<main class="content" id="content">
<div class="part-header">
<span class="part-label">WorkBuddy · 第 {n} 天 / 共 20 天 · 阶段 {stage['id']} {esc(stage['name'])}</span>
<h1 class="part-title">{esc(info['title'])}</h1>
<p class="part-desc">焦点：<span class="fileref">{esc(info['focus'])}</span> · 类比：{esc(info['analogy'])}</p>
</div>

<div class="journey"><div class="jt">20 天进度</div><div class="steps">{''.join(journey_steps)}</div></div>

<section id="goal" class="section"><div class="section-header"><span class="section-number">00</span><h1>今日目标</h1></div>
<div class="card">
<div class="goal-box"><span class="gt">🎯 今天学完你能</span>{esc(info['blurb'])}</div>
<div class="ask"><span class="t">先问自己</span>如果用不懂术语的话讲给同事：今天这个能力解决什么麻烦？</div>
<div class="capsule">{capsules}</div>
<p class="doclink">对照阅读：<a href="{esc(info['doc'])}" target="_blank">{esc(info['doc'])}</a></p>
</div></section>

{lessons_html}

<section id="try" class="section"><div class="section-header"><span class="section-number">✓</span><h1>动手验收</h1></div>
<div class="card">
<div class="essence"><span class="t">今天就做</span>{esc(info['try_it'])}</div>
<div class="pitfall"><span class="t">常见坑</span>{esc(info['pitfalls'])}</div>
<div class="check"><ul><li>能用自己的话复述知识胶囊三句话</li><li>完成「今天就做」并留下产物或截图</li><li>知道官方文档里对应章节入口</li></ul></div>
</div></section>

<section id="qa" class="section"><div class="section-header"><span class="section-number">?</span><h1>Q&A</h1></div>
<div class="card"><div class="qa"><span class="t">答疑</span>{qa_html}</div></div></section>

<div class="nav-prevnext">{prev_link}{next_link}</div>
</main>{NAV_JS}</body></html>"""


def patch_index() -> None:
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    marker = '<div class="blog-grid" id="lib-grid">'
    card = f"""
<a class="blog-card" data-new="1" href="workbuddy-tutorial.html" data-ps="workbuddy" data-pd="20" data-cat="platform" data-level="入门" data-lang="实战" data-area="ai" data-title="WorkBuddy 学习（20 天）" data-desc="腾讯全场景 AI 办公工作台：任务创建/对话/产物验收，技能·项目·连接器·微信助理；官方文档驱动。" data-search="workbuddy 学习（20 天） 腾讯 ai 办公 任务 技能 连接器 助理 codebuddy 实战 入门 20 天 最新 new">
  <div class="card-top"><div class="blog-card-icon" style="background:{GRAD};">{LOGO}</div><span class="rec-badge" style="background:rgba(34,197,94,.15);color:#4ade80;border-color:rgba(34,197,94,.35)">最新</span></div>
  <h3>WorkBuddy 学习（20 天）</h3>
  <p class="blog-desc">腾讯全场景 AI 办公工作台：任务创建/对话/产物验收，技能·项目·连接器·微信助理；官方文档驱动。</p>
  <div class="meta-row"><span class="meta-pill level-入门">入门</span><span class="meta-pill">实战</span><span class="meta-pill muted">LLM 应用平台</span></div>
  <div class="blog-card-tags"><span class="blog-tag">WorkBuddy</span><span class="blog-tag">腾讯</span><span class="blog-tag">20 天</span></div>
  <div class="blog-card-arrow">查看教程 &rarr;</div>
</a>"""
    if "workbuddy-tutorial.html" in text:
        print("index.html already has workbuddy card, skip")
        return
    if marker not in text:
        raise SystemExit("lib-grid marker not found in index.html")
    text = text.replace(marker, marker + "\n" + card, 1)
    index.write_text(text, encoding="utf-8")
    print("patched index.html")


def main() -> None:
    hub = ROOT / "workbuddy-tutorial.html"
    hub.write_text(render_hub(), encoding="utf-8")
    print(f"wrote {hub.name}")
    for i in range(1, 21):
        path = ROOT / f"workbuddy-day{i:02}.html"
        path.write_text(render_day(i), encoding="utf-8")
        print(f"wrote {path.name}")
    patch_index()
    print("done")


if __name__ == "__main__":
    main()
