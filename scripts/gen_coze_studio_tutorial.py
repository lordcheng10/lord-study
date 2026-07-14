#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Coze Studio 80-day HTML tutorial (hub + day pages) for lord-study."""
from __future__ import annotations

import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT
PREFIX = "coze-studio"
TOTAL = 80

# ---------------------------------------------------------------------------
# Stage / day metadata
# ---------------------------------------------------------------------------
STAGES = [
    {"id": 1, "name": "开篇与全景", "lo": 1, "hi": 8, "color": "#4f46e5", "grad": "#4f46e5,#7c3aed",
     "blurb": "认知扣子、DDD 分层、Docker、启动与中间件"},
    {"id": 2, "name": "API · IDL · Crossdomain", "lo": 9, "hi": 16, "color": "#0ea5e9", "grad": "#0ea5e9,#6366f1",
     "blurb": "契约、路由、鉴权、防腐层、一次请求进门"},
    {"id": 3, "name": "Agent 对话主线", "lo": 17, "hi": 28, "color": "#f59e0b", "grad": "#f59e0b,#ef4444",
     "blurb": "SingleAgent、Conversation、AgentRun、agentflow、ReAct"},
    {"id": 4, "name": "Workflow 引擎深水", "lo": 29, "hi": 48, "color": "#ec4899", "grad": "#ec4899,#8b5cf6",
     "blurb": "Canvas→Schema→Compose→Execute→全部节点类型"},
    {"id": 5, "name": "知识库·插件·模型", "lo": 49, "hi": 58, "color": "#10b981", "grad": "#10b981,#14b8a6",
     "blurb": "RAG、Embedding、Plugin、ModelBuilder、Memory"},
    {"id": 6, "name": "横切与基础设施", "lo": 59, "hi": 66, "color": "#64748b", "grad": "#64748b,#0ea5e9",
     "blurb": "权限、用户、搜索、事件总线、存储、Checkpoint"},
    {"id": 7, "name": "前端 Rush 与 IDE", "lo": 67, "hi": 75, "color": "#a855f7", "grad": "#a855f7,#ec4899",
     "blurb": "Monorepo、agent-ide、workflow 画布、chat-area、adapter"},
    {"id": 8, "name": "工程收官", "lo": 76, "hi": 80, "color": "#22c55e", "grad": "#14b8a6,#22c55e",
     "blurb": "安全、二次开发、对比、知识地图、练习项目"},
]

TITLES = [
    "Coze Studio 是什么：扣子开源的心智模型",
    "顶层目录地图：backend / frontend / idl / docker",
    "DDD 四层大楼：api · application · domain · infra",
    "Docker 全家桶：MySQL Redis ES Milvus NSQ MinIO",
    "Make 命令与三种启动姿势",
    "main.go 启动剧本：env → Init → Spin",
    "application.Init：三级装配 + SetDefaultSVC",
    "中间件链条：顺序绝不能乱",
    "IDL / Thrift：前后端的合同本",
    "路由注册：GeneratedRegister 与静态页",
    "Handler 一览：薄薄一层转给 application",
    "SessionAuth 与 OpenapiAuth：两种进门方式",
    "Crossdomain 防腐层：为什么 domain 互不直接引用",
    "一次 Chat 请求的完整旅程（总览）",
    "SSE / Pipe：流式吐字怎么回来",
    "错误码与 types：errno · consts · ddl",
    "SingleAgent 实体：智能体到底存了什么",
    "SingleAgent Service：CRUD · 发布 · StreamExecute",
    "Conversation 域：会话生命周期",
    "Message 域：消息怎么落库",
    "AgentRun 接口：Run · Cancel · List",
    "AgentRun 实现：Pipe + safego.Go",
    "AgentRuntime.Run：加载 Agent 再分支",
    "agentflow.BuildAgent：人格→检索→提示→ReAct",
    "Persona 与 Prompt 节点：人设如何注入",
    "Knowledge Retriever 节点：对话前先查资料",
    "Eino ReAct：有工具就变成自主 Agent",
    "工具全家桶：Plugin · Workflow · Database · Variables",
    "Workflow 域全景：最大的业务心脏",
    "Canvas 画布：前端拖的是什么 JSON",
    "Schema：Canvas 如何变成可执行图",
    "Compose：用 Eino Workflow 组装节点",
    "Node Runner：一个节点怎么被调度",
    "Execute 事件流：前端怎样实时看执行",
    "Entry / Exit：图的大门与出口",
    "LLM 节点：工作流里调模型",
    "Plugin 节点：在图里调第三方 API",
    "Code 节点：Python 沙箱怎么跑",
    "Knowledge 节点：索引 / 检索 / 删除",
    "HTTP Requester：通用 HTTP 积木",
    "Selector 与 IntentDetector：分支决策",
    "Loop 与 Batch：循环与批处理",
    "SubWorkflow：工作流套娃",
    "变量三件套：Assigner · Aggregator · WithinLoop",
    "TextProcessor 与 JSON 节点",
    "Conversation 系列节点：会话也能编排",
    "QA · Emitter · Receiver：人机协作节点",
    "Workflow as Tool：工作流变身 Agent 工具",
    "Knowledge 域总览：文档 · 切片 · 策略",
    "Document Processor：不同文档类型怎么处理",
    "Embedding 基础设施：向量从哪来",
    "检索：ES 关键词 + Milvus 向量",
    "Plugin 域：插件与 Tool 实体",
    "Plugin 执行：exec_tool 与 invocation",
    "ModelBuilder 工厂：统一造 ChatModel",
    "模型供应商全家桶：OpenAI Ark Claude…",
    "Memory：变量与用户数据库",
    "Prompt 资源库：提示词怎么管",
    "Permission：资源级授权怎么查",
    "User · Passport · Space：租户与登录",
    "Search + EventBus：ES 索引与 NSQ",
    "Upload · Storage · MinIO：文件去哪",
    "Cache · ORM · IDGen：基础件地图",
    "Checkpoint：中断与恢复的底座",
    "App · Template · Connector：项目与渠道",
    "OpenAuth：个人访问令牌 PAT",
    "Rush Monorepo：level-1~4 依赖金字塔",
    "apps/coze-studio：壳应用怎么起来",
    "agent-ide：智能体编排页地图",
    "chat-area：对话区是怎么拼出来的",
    "workflow playground：可视化画布前端",
    "workflow/nodes：前端节点与后端的对应",
    "Zustand stores：状态放哪",
    "IDL → TypeScript：合同怎样到前端",
    "Adapter 模式：开源版如何换皮",
    "安全清单：公网部署前必看",
    "二次开发实战：加一个新 API 的路径",
    "横向对比：Coze vs Dify vs LangGraph",
    "80 天知识地图串讲",
    "练习项目与求职建议",
]

assert len(TITLES) == TOTAL

DEEP_NOTES = json.loads((Path(__file__).resolve().parent / "coze_deep_notes.json").read_text(encoding="utf-8"))
DEEP_NOTES = {int(k): v for k, v in DEEP_NOTES.items()}

# Per-day focus paths / analogies / lesson seeds (compact but unique)
FOCUS = {
    1: ("README.zh_CN.md", "把 Coze 想成「智能体装修公司」：你画效果图（Prompt/Workflow），工人（模型/插件/知识库）按图施工。"),
    2: ("仓库根目录", "陌生城市先看行政区：backend 是市政厅，frontend 是商业街，idl 是合同法务处，docker 是水电基础设施。"),
    3: ("backend/{api,application,domain,infra}", "四层大楼：门卫(api)→经理(application)→专家部门(domain)→水电工(infra)。"),
    4: ("docker/docker-compose.yml", "厨房后厨：冰箱(MySQL)、备菜台(Redis)、检索柜(ES)、向量仓(Milvus)、传送带(NSQ)、仓库(MinIO)。"),
    5: ("Makefile", "遥控器：make debug 一键开全屋灯；middleware 只开水电；server 只开客厅。"),
    6: ("backend/main.go", "开机顺序：插电(env)→装零件(Init)→开门营业(Spin)。顺序写死在注释里。"),
    7: ("backend/application/application.go", "搭积木：infra→basic→primary→complex，最后用 SetDefaultSVC 贴「跨部门联络号」。"),
    8: ("backend/main.go 中间件段", "机场安检流水线：先登记(ContextCache)再安检(Auth)最后通关(I18n)，插队就乱套。"),
    9: ("idl/", "合同本：改接口先改 Thrift，两端按合同生成，避免口头约定扯皮。"),
    10: ("backend/api/router/", "总机接线：GeneratedRegister 把所有分机号挂上网，顺便托管静态网站。"),
    11: ("backend/api/handler/coze/", "前台接待：核对身份牌→填单→交后台。自身不写业务大脑。"),
    12: ("backend/api/middleware/session.go", "两种门票：Cookie 会话票（网页）与 PAT 通行令牌（OpenAPI）。"),
    13: ("backend/crossdomain/", "外交部：部门之间不走后门串门，统一走合同窗口 DefaultSVC()。"),
    14: ("handler → agentrun → agentflow", "快递全链路：取件→分拣→仓库取货→装车→签收，每一跳有真实文件对应。"),
    15: ("schema.Pipe / safego.Go", "一边写一边读的水管：goroutine 往里注水，调用方喝流。"),
    16: ("backend/types/", "医院分科编码：errno 是病历号，consts 是公共词典，ddl 是表结构草稿。"),
    17: ("domain/agent/singleagent/entity", "智能体身份证：人设、模型、插件、知识库、工作流都贴在档案袋里。"),
    18: ("single_agent_impl.go StreamExecute", "服务台：建档、改档、发布，以及「开始流式回话」。"),
    19: ("domain/conversation/conversation", "聊天室：开房、关房、换房——会话是消息的容器。"),
    20: ("domain/conversation/message", "聊天记录本：谁说了什么、什么时候、什么角色。"),
    21: ("agentrun/service/agent_run.go", "跑道接口：起跑、取消、查成绩，不关心肌肉怎么发力。"),
    22: ("agent_run_impl.go", "边跑边直播：Pipe(20) 缓冲 + 后台 goroutine 真正跑步。"),
    23: ("agentrun/internal/run.go", "教练临场：先看是工作流模式还是 Agent 模式，再叫对应选手上场。"),
    24: ("agent_flow_builder.go", "流水线装配：人设→变量→知识检索→提示词→ReAct/LLM。"),
    25: ("node_persona_render.go", "给模型戴面具：把人设 Prompt 渲染进系统消息。"),
    26: ("node_retriever.go", "开卷考试前先翻书：对话前检索知识片段塞进上下文。"),
    27: ("eino/flow/agent/react", "会用工具的实习生：思考→调工具→观察→再思考，循环到答完。"),
    28: ("node_tool_*.go", "工具箱：插件电话、工作流、数据库、变量——都挂成 Eino Tool。"),
    29: ("domain/workflow/", "自动化工厂：用户拖节点，后端把图变成可执行程序。"),
    30: ("entity/vo/canvas.go", "设计图纸 JSON：节点盒子 + 连线，前端存的就是这张图。"),
    31: ("internal/canvas/adaptor", "图纸翻译成施工图：Canvas → WorkflowSchema。"),
    32: ("internal/compose/workflow.go", "工头按施工图排班：Eino compose.Workflow 承接节点。"),
    33: ("compose/node_runner.go", "单个工位怎么开工、怎么报完成。"),
    34: ("internal/execute/", "直播进度条：节点开始/结束事件推到前端。"),
    35: ("nodes/entry · nodes/exit", "闸机：进门收参数，出门交结果。"),
    36: ("nodes/llm", "厂里的大脑工位：在图中间调用 ChatModel。"),
    37: ("nodes/plugin", "外包工位：按 OpenAPI 调外部服务。"),
    38: ("nodes/code + infra/coderunner", "沙箱车间：受限跑 Python，防炸厨房。"),
    39: ("nodes/knowledge", "资料室工位：入库索引、检索、删除。"),
    40: ("nodes/httprequester", "万能电话机：任意 HTTP 请求积木。"),
    41: ("nodes/selector · intentdetector", "十字路口：条件分支或意图识别分流。"),
    42: ("nodes/loop · batch", "传送带循环 / 分批装箱。"),
    43: ("nodes/subworkflow", "外包整条产线：嵌套另一张工作流。"),
    44: ("variableassigner · aggregator", "记事本：写变量、汇总变量、循环内赋值。"),
    45: ("textprocessor · json", "文字加工与 JSON 序列化/反序列化。"),
    46: ("nodes/conversation", "把「会话 CRUD」也做成可编排节点。"),
    47: ("qa · emitter · receiver", "人在环：提问等人答、输出流、输入接收。"),
    48: ("compose/workflow_tool.go", "工厂产品也能当 Agent 的扳手。"),
    49: ("domain/knowledge/", "图书馆：馆藏(知识库)、书(文档)、页(切片)。"),
    50: ("knowledge/processor", "入库流水线：PDF/表格/自定义各走各的清洗线。"),
    51: ("infra/embedding", "把句子变成坐标：向量化适配层。"),
    52: ("retrieve.go + milvus + es", "双保险检索：关键词 + 向量，再拼给模型。"),
    53: ("domain/plugin/entity", "插件 = 工具箱，Tool = 一把具体扳手。"),
    54: ("plugin/service/exec_tool.go", "真正拧扳手：鉴权、HTTP、MCP 调用。"),
    55: ("bizpkg/llm/modelbuilder", "模型工厂前台：按 ModelClass 挑师傅。"),
    56: ("modelbuilder/{openai,ark,claude…}.go", "各品牌适配器：同一产品，不同说明书。"),
    57: ("domain/memory/", "长期记忆：变量贴纸 + 用户专属小数据库。"),
    58: ("domain/prompt/", "提示词素材库：可复用的文案模板。"),
    59: ("domain/permission/", "门禁系统：你有没有这间房的钥匙。"),
    60: ("domain/user/", "账号中心：用户、会话 Cookie、空间(租户)。"),
    61: ("domain/search + infra/eventbus", "公告板 + 快递员：写资源→发事件→ES 更新。"),
    62: ("domain/upload + infra/storage", "寄存柜：元数据进库，文件进 MinIO。"),
    63: ("infra/{cache,orm,idgen}", "水电煤：缓存、数据库访问、发号器。"),
    64: ("infra/checkpoint", "游戏存档：工作流/Agent 中断后续关。"),
    65: ("domain/app · template · connector", "项目壳、模板商店、发布渠道。"),
    66: ("domain/openauth", "API 钥匙串：个人访问令牌。"),
    67: ("rush.json", "乐高分层：底层砖不能依赖顶层玩具。"),
    68: ("frontend/apps/coze-studio", "最终拼好的玩具壳：路由、布局、挂载 IDE。"),
    69: ("packages/agent-ide", "智能体装修间：人设、模型、插件、知识面板。"),
    70: ("packages/common/chat-area*", "对话客厅：消息列表、输入框、插件渲染。"),
    71: ("packages/workflow/playground", "可视化画板：拖节点连线。"),
    72: ("packages/workflow/nodes", "前端节点组件 ↔ 后端 NodeType 一一对应。"),
    73: ("packages/studio/stores", "全局小黑板：Zustand 存用户/空间/编辑态。"),
    74: ("frontend/infra/idl", "合同翻译机：Thrift → TypeScript 客户端。"),
    75: ("*-adapter 包", "换皮插头：开源版与商业版插不同适配器。"),
    76: ("README 安全警告", "门锁清单：注册口、代码沙箱、SSRF、水平越权。"),
    77: ("二次开发路径", "加功能六步走：IDL→生成→handler→application→domain→测。"),
    78: ("横向对比表", "选工具：低代码平台 vs 编排引擎 vs 全栈 Studio。"),
    79: ("全图回顾", "把 80 天地图钉在墙上，任意文件能定位到格子。"),
    80: ("作品集建议", "动手做一个「带知识库的客服 Agent」闭环。"),
}

def stage_of(day: int) -> dict:
    for s in STAGES:
        if s["lo"] <= day <= s["hi"]:
            return s
    return STAGES[-1]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# Lesson content factory — unique per day, beginner-friendly
# ---------------------------------------------------------------------------
def build_lessons(day: int, title: str, focus: str, analogy: str) -> list[dict]:
    """Return 6 lessons with ask/essence/baby/walk/tradeoff/pitfall/qa."""
    s = stage_of(day)
    prev = TITLES[day - 2] if day > 1 else "（起点）"
    nxt = TITLES[day] if day < TOTAL else "（结业）"

    # Stage-tuned "why it matters"
    why = {
        1: "没有全局地图，后面任何文件都会迷路。",
        2: "契约与鉴权错了，业务再强也进不了门。",
        3: "对话主线是产品体验的心脏，必须走通。",
        4: "工作流引擎是 Coze 差异化最强的部分。",
        5: "RAG/插件/模型是 Agent「外挂能力」来源。",
        6: "横切能力决定能不能上生产。",
        7: "前端是用户每天摸的面，要能对照后端概念。",
        8: "收官是为了能独立改代码、讲清楚。",
    }[s["id"]]

    lessons = [
        {
            "t": f"痛点：为什么要学「{title.split('：')[0]}」",
            "ask": f"很多小白打开仓库就慌：文件太多、名字陌生、不知道今天该盯哪一块。",
            "essence": f"今天的靶心是 <code>{esc(focus)}</code>。学完你应能用一句话说清它在整条链路里的位置。",
            "baby": f"🍼 类比：{analogy}",
            "extra": f"<div class='essence'><span class='t'>🎯 阶段定位</span>你在「{s['name']}」阶段（D{s['lo']:02d}-D{s['hi']:02d}）。{why}</div>",
        },
        {
            "t": "先建立坐标：它挂在哪一层",
            "ask": "读源码第一问永远是：这个东西属于门卫、经理、专家，还是水电工？",
            "essence": "用 DDD 尺子量：<code>api/</code> 收请求，<code>application/</code> 编排用例，"
                       "<code>domain/</code> 写规则，<code>infra/</code> 对接中间件，"
                       "<code>crossdomain/</code> 做部门间外交。",
            "baby": "把「层」记成楼层，把「域」记成房间号。今天的主角房间是："
                    f"<span class='fileref'>{esc(focus)}</span>",
            "extra": _layer_svg(),
        },
        {
            "t": "真源码走读：关键入口怎么读",
            "ask": "有了地图还不够，要练「打开文件第一眼看什么」。",
            "essence": "优先看：类型/接口定义 → 构造函数/New → 被谁调用 → 调用谁。"
                       "Coze 里大量 <code>interface</code> + <code>_impl.go</code> 对：先读接口门牌，再进实现。",
            "baby": "接口像菜单，实现像厨房。菜单短好懂，厨房再乱也不慌。",
            "extra": _walk_for_day(day, focus),
        },
        {
            "t": "动态理解：一次请求/一次执行怎么经过这里",
            "ask": "静态目录脑中要动画起来：用户点「发送」之后，数据如何流过今天的模块。",
            "essence": "记住主链路：浏览器 → Hertz 中间件 → Handler → Application → Domain"
                       "（可能经 Crossdomain）→ Infra/Eino → 流式回写。",
            "baby": "把发光小球想象成「用户的一句话」——看它经过哪些盒子。",
            "extra": _flow_anim(day),
        },
        {
            "t": "设计取舍与边界坑",
            "ask": "作者为什么这样写？哪些地方一改就炸？",
            "essence": _tradeoff_for_day(day),
            "baby": "好设计通常是在「解耦」和「省事」之间做交换。今天记住那个交换。",
            "extra": f"<div class='pitfall'><span class='t'>⚠️ 坑</span>{_pitfall_for_day(day)}</div>"
                     f"<div class='qa'><p class='q'>👶 小白问：我可以跳过吗？</p>"
                     f"<p class='a'>👨‍🏫 不建议。昨天学的是「{esc(prev)}」，明天是「{esc(nxt)}」。"
                     f"今天是中间的承重墙。</p></div>",
        },
        {
            "t": "今日小结 · 动手 · 预告",
            "ask": "学完能否用自己的话复述？动手验证了吗？",
            "essence": "闭环学习：概念 → 源码坐标 → 动手命令 → 能教别人。",
            "baby": "把今日关键词写在便利贴上，贴到你自己的「知识地图」对应格子。",
            "extra": _summary_block(day, title, focus, nxt),
        },
    ]
    return lessons


def _layer_svg() -> str:
    return """
<div class="svgbox">
<svg viewBox="0 0 640 220" width="100%" style="max-width:640px;display:block;margin:0 auto" font-family="system-ui,sans-serif" font-size="12">
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient>
  </defs>
  <text x="320" y="22" text-anchor="middle" fill="#e2e8f0" font-weight="700">Coze 后端四层（心智模型）</text>
  <rect x="40" y="40" width="560" height="36" rx="8" fill="rgba(79,70,229,.15)" stroke="#818cf8"/>
  <text x="60" y="63" fill="#a5b4fc">api/ · 门卫：Handler + Middleware + Router（IDL 生成）</text>
  <rect x="40" y="84" width="560" height="36" rx="8" fill="rgba(14,165,233,.12)" stroke="#38bdf8"/>
  <text x="60" y="107" fill="#7dd3fc">application/ · 经理：用例编排、组装参数、调用 domain</text>
  <rect x="40" y="128" width="560" height="36" rx="8" fill="rgba(245,158,11,.12)" stroke="#fbbf24"/>
  <text x="60" y="151" fill="#fcd34d">domain/ · 专家部门：Agent / Workflow / Knowledge / Plugin…</text>
  <rect x="40" y="172" width="560" height="36" rx="8" fill="rgba(34,197,94,.12)" stroke="#4ade80"/>
  <text x="60" y="195" fill="#86efac">infra/ · 水电工：DB / Redis / ES / Milvus / NSQ / MinIO / Checkpoint</text>
  <!-- animated pulse -->
  <circle r="6" fill="#fff">
    <animate attributeName="cy" values="58;102;146;190;58" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="cx" values="560;560;560;560;560" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;1;1;1;0.2" dur="4s" repeatCount="indefinite"/>
  </circle>
</svg>
<div class="cap">发光点模拟一次请求从上到下穿过四层（并经 crossdomain 横向协作）</div>
</div>"""


def _walk_for_day(day: int, focus: str) -> str:
    walks = {
        1: [
            ("README.zh_CN.md", "产品一句话：一站式 AI Agent 可视化开发"),
            ("功能清单表格", "模型 / 智能体 / 应用 / 工作流 / 资源 / API"),
            ("技术栈声明", "后端 Go + 前端 React/TS + 微服务心态 + DDD"),
        ],
        6: [
            ("loadEnv()", "读 .env / .env.$APP_ENV"),
            ("application.Init", "装配全部服务与 crossdomain"),
            ("startHttpServer", "Hertz + 中间件 + GeneratedRegister + Spin"),
        ],
        7: [
            ("appinfra.Init", "先起基础设施依赖"),
            ("initBasicServices", "user/prompt/modelmgr/upload…"),
            ("initPrimaryServices", "plugin/memory/knowledge/workflow"),
            ("initComplexServices", "singleagent/conversation/search/app"),
            ("SetDefaultSVC × N", "把外交窗口注册到全局"),
        ],
        8: [
            ("ContextCacheMW", "必须第一：上下文缓存"),
            ("RequestInspectorMW", "必须第二：识别 WebAPI vs OpenAPI"),
            ("OpenapiAuthMW → SessionAuthMW", "两种鉴权"),
            ("I18nMW", "必须在 Session 之后"),
        ],
        22: [
            ("schema.Pipe(20)", "创建有缓冲的双向流"),
            ("safego.Go", "后台跑 AgentRuntime，防崩"),
            ("defer sw.Close()", "写端关闭，读端结束"),
            ("return sr", "调用方只拿读端去消费"),
        ],
        24: [
            ("persona_render", "渲染人设"),
            ("knowledge_retriever", "预检索知识"),
            ("prompt_template", "拼最终 Prompt"),
            ("react_agent / llm", "有工具走 ReAct，否则纯聊"),
        ],
        55: [
            ("modelClass2NewModelBuilder", "ModelClass → 构造函数映射表"),
            ("NewModelBuilder", "校验 connection 后返回 Service"),
            ("BuildModelByID", "按模型 ID 取配置再 Build"),
        ],
    }
    rows = walks.get(day)
    if not rows:
        rows = [
            (focus, "今天的主坐标，先 ls / 打开文件头部看 package 与类型"),
            ("接口 or 门面", "找 type Xxx interface / func New / func Init"),
            ("调用方", "用 IDE / grep 找谁引用了它"),
            ("被调方", "它依赖了哪些 crossdomain / infra"),
        ]
    body = "".join(f"<div class='r'><code>{esc(a)}</code><span>{b}</span></div>" for a, b in rows)
    return f"<div class='walk'>{body}</div><p class='anno'>对照仓库路径阅读，行号以你本地版本为准；关注<strong>调用关系</strong>多于死记行号。</p>"


def _flow_anim(day: int) -> str:
    if 17 <= day <= 28:
        steps = ["Handler", "Application", "AgentRun.Pipe", "AgentRuntime", "BuildAgent", "Eino Stream", "SSE 回前端"]
    elif 29 <= day <= 48:
        steps = ["Canvas JSON", "Validate", "To Schema", "Compose", "Node Run", "Execute Event", "前端进度"]
    elif 67 <= day <= 75:
        steps = ["页面点击", "TS API Client", "Hertz API", "Application", "Domain", "流式回包", "chat-area 渲染"]
    else:
        steps = ["请求进入", "Middleware", "Handler", "Application", "Domain", "Infra", "响应/流"]
    pills = " <span class='a'>→</span> ".join(f"<span class='n'><b>{esc(s)}</b></span>" for s in steps)
    return f"<div class='loopd'>{pills}</div>"


def _tradeoff_for_day(day: int) -> str:
    table = {
        3: "为什么硬拆四层？短期写得慢，长期多人协作、测业务不被 DB 绑死；Coze 体量决定必须付这笔「架构税」。",
        7: "SetDefaultSVC 是服务定位器：方便、有全局可变状态。换 DI 框架更「纯」但改造成本巨大——开源版选了实用。",
        8: "中间件顺序写死：I18n 依赖 Session；Cache 必须最先。调换顺序会出现「偶发空用户 / 错语言」级 Bug。",
        13: "domain 互不 import，改走 crossdomain：多写一层 contract，换来无环与可单测。",
        22: "异步 Pipe：接口立即返回读端，真正跑在后台。优点是流式低延迟；代价是错误/取消要额外通道处理。",
        27: "有工具才上 ReAct：无工具时纯 LLM 更便宜更稳；有工具才付「多轮思考」成本。",
        32: "工作流执行栈用 Eino compose：复用成熟图执行/中断，而不是自研一套 Pregel。",
        38: "代码节点独立 Python 运行时：能力强但攻击面大——公网务必沙箱与鉴权。",
        64: "Checkpoint 换「可中断」：要存状态、要考虑序列化，但 QA/人在环体验成立。",
        75: "前端 adapter：核心包干净，产品差异塞适配器——开源与商业可并行演进。",
        76: "开箱默认方便本地体验，不等于生产安全默认；公网要主动收紧。",
    }
    return table.get(day, "作者优先「边界清晰 + 可替换实现」：接口在 domain，脏细节进 infra/crossdomain。代价是文件更多，收益是改一处不易拖垮全局。")


def _pitfall_for_day(day: int) -> str:
    table = {
        4: "只起 server 不起 middleware → 连不上 MySQL/Redis，表现为 Init panic。",
        5: "Windows 用户直接 make web 前要先复制 docker/.env.example。",
        8: "自写中间件插错位置，Session 未就绪就读用户。",
        12: "OpenAPI 路径却走 Session 校验，或反过来——看 RequestInspector 打的 AuthType。",
        22: "忘记 Close 写端 → 读端永久阻塞。",
        38: "代码节点可执行任意逻辑：未隔离等于给服务器装了「远程 Shell」。",
        52: "只配了 Embedding 没起 Milvus，或 ES 索引未 setup_es_index。",
        67: "跨 level 乱引用：Rush 会报依赖违规，别用相对路径偷渡。",
    }
    return table.get(day, "不要在 domain 里直接 new 基础设施客户端；不要绕过 crossdomain 去 import 别的 domain 内部包。")


def _summary_block(day: int, title: str, focus: str, nxt: str) -> str:
    cmd = _hands_on(day, focus)
    return f"""
<div class="card highlight-card">
  <h3>🧠 今天你应该能回答</h3>
  <ul>
    <li>今天主题「{esc(title)}」一句话是什么？</li>
    <li>关键路径 <code>{esc(focus)}</code> 属于哪一层/哪个域？</li>
    <li>它上游谁调用、下游它调用谁？</li>
    <li>对应的类比你能讲给完全不懂代码的人听吗？</li>
  </ul>
</div>
<div class="card">
  <h3>✋ 约 10 分钟动手</h3>
  <pre><code class="language-bash">{esc(cmd)}</code></pre>
</div>
<div class="tip"><strong>明日预告</strong>：Day {day+1 if day<TOTAL else TOTAL} · {esc(nxt)}。今晚把今日便利贴贴到知识地图上即可。</div>
"""


def _hands_on(day: int, focus: str) -> str:
    cmds = {
        1: "cd /path/to/coze-studio && head -40 README.zh_CN.md",
        2: "ls -la && ls backend frontend idl docker",
        3: "ls backend && ls backend/domain && ls backend/application",
        4: "grep -E '^  [a-z].*:$' docker/docker-compose.yml | head -30",
        5: "grep -E '^[a-z].*:' Makefile | head -25",
        6: "sed -n '44,120p' backend/main.go",
        7: "sed -n '120,180p' backend/application/application.go",
        8: "sed -n '90,120p' backend/main.go",
        9: "ls idl && head -40 idl/api.thrift",
        10: "sed -n '1,80p' backend/api/router/register.go",
        12: "sed -n '1,80p' backend/api/middleware/session.go",
        13: "ls backend/crossdomain && head -40 backend/crossdomain/agent/contract.go",
        22: "sed -n '50,100p' backend/domain/conversation/agentrun/service/agent_run_impl.go",
        24: "sed -n '1,120p' backend/domain/agent/singleagent/internal/agentflow/agent_flow_builder.go",
        29: "ls backend/domain/workflow && ls backend/domain/workflow/internal",
        35: "ls backend/domain/workflow/internal/nodes",
        55: "sed -n '40,100p' backend/bizpkg/llm/modelbuilder/model_builder.go",
        67: "head -80 rush.json",
        68: "ls frontend/apps/coze-studio && head -40 frontend/apps/coze-studio/package.json",
    }
    return cmds.get(day, f"# 围绕今日焦点浏览\nls -la {focus.split()[0] if focus else 'backend'}\n# 用编辑器打开关键文件，搜索 type / func / interface")


# ---------------------------------------------------------------------------
# Day HTML
# ---------------------------------------------------------------------------
DAY_CSS = """
.ask{border-left:3px solid #f59e0b;background:rgba(245,158,11,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.ask .t{font-weight:700;color:#f59e0b;display:block;margin-bottom:4px}
.essence{border-left:3px solid #4f46e5;background:rgba(79,70,229,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.essence .t{font-weight:700;color:#a5b4fc;display:block;margin-bottom:4px}
.baby{border-left:3px solid var(--accent-green);background:rgba(34,197,94,.06);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.baby .t{font-weight:700;color:var(--accent-green);display:block;margin-bottom:4px}
.qa{border-left:3px solid #a855f7;background:rgba(168,85,247,.06);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.qa p{margin:5px 0}.qa .q{color:#c084fc;font-weight:600}.qa .a{color:var(--text-secondary)}
.journey{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:12px 14px;margin:6px 0 16px}
.journey .jt{font-size:11px;color:var(--text-muted);margin-bottom:8px;letter-spacing:.04em}
.journey .steps{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.journey .st{font-size:11.5px;padding:5px 10px;border-radius:20px;background:var(--bg-card);border:1px solid var(--border-color);color:var(--text-muted);white-space:nowrap}
.journey .st.on{background:linear-gradient(135deg,VARGRAD);color:#fff;border-color:transparent;font-weight:700}
.journey .sep{color:var(--text-muted);font-size:12px}
.svgbox{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:12px;padding:16px;margin:12px 0;overflow-x:auto}
.svgbox .cap{font-size:12px;color:var(--text-muted);text-align:center;margin-top:8px}
.anno{font-size:12px;color:var(--text-muted);margin:2px 0 12px;padding-left:12px;border-left:2px solid var(--border-color)}.anno b{color:var(--accent-orange)}
.fileref{display:inline-block;font-size:11px;background:rgba(79,70,229,.12);color:#a5b4fc;border:1px solid rgba(79,70,229,.35);border-radius:5px;padding:1px 7px;font-family:ui-monospace,monospace}
.walk{margin:10px 0;border:1px solid var(--border-color);border-radius:8px;overflow:hidden}
.walk .r{display:flex;gap:10px;padding:7px 10px;font-size:12.5px;border-top:1px solid var(--border-color)}
.walk .r:first-child{border-top:none}
.walk .r code{color:var(--accent-cyan);flex-shrink:0;min-width:170px;font-size:11.5px}
.walk .r span{color:var(--text-secondary)}
.tradeoff{border-left:3px solid #ec4899;background:rgba(236,72,153,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.tradeoff .t{font-weight:700;color:#f472b6;display:block;margin-bottom:4px}
.pitfall{border-left:3px solid #ef4444;background:rgba(239,68,68,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px}
.pitfall .t{font-weight:700;color:#f87171;display:block;margin-bottom:4px}
.loopd{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;padding:12px 4px}
.loopd .n{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:9px;padding:10px 12px;font-size:12px;text-align:center}
.loopd .n b{display:block;color:#818cf8;font-size:12.5px}.loopd .a{color:#a78bfa;font-weight:800;font-size:16px}
"""


def journey_bar(day: int) -> str:
    s = stage_of(day)
    pills = []
    for st in STAGES:
        cls = "on" if st["id"] == s["id"] else ""
        pills.append(f'<span class="st {cls}">S{st["id"]} {esc(st["name"])}</span>')
    sep = '<span class="sep">·</span>'
    return (
        '<div class="journey"><div class="jt">📍 你在 80 天里的位置 · '
        f'阶段 {s["id"]} {esc(s["name"])} · Day {day:02d}/{TOTAL}</div>'
        f'<div class="steps">{sep.join(pills)}</div></div>'
    )


def render_day(day: int) -> str:
    s = stage_of(day)
    title = TITLES[day - 1]
    focus, analogy = FOCUS[day]
    lessons = build_lessons(day, title, focus, analogy)
    grad = s["grad"]
    css = DAY_CSS.replace("VARGRAD", grad)
    num = f"{day:02d}"
    prev_link = f'{PREFIX}-day{day-1:02d}.html' if day > 1 else f'{PREFIX}-tutorial.html'
    next_link = f'{PREFIX}-day{day+1:02d}.html' if day < TOTAL else f'{PREFIX}-tutorial.html'
    prev_label = f'Day {day-1:02d}' if day > 1 else '总目录'
    next_label = f'Day {day+1:02d} {TITLES[day][:12]}…' if day < TOTAL else '返回总目录'

    nav_lessons = "\n".join(
        f'<li><a href="#l{i:02d}" class="nav-link{" active" if i==1 else ""}" data-section="l{i:02d}">'
        f'L{i:02d} · {esc(les["t"][:18])}</a></li>'
        for i, les in enumerate(lessons, 1)
    )

    sections = []
    for i, les in enumerate(lessons, 1):
        sections.append(f"""
        <section id="l{i:02d}" class="section">
            <div class="section-header"><span class="section-number">L{i:02d}</span><h1>{esc(les['t'])}</h1></div>
            <div class="card">
                <div class="ask"><span class="t">🤔 痛点 / 提问</span>{les['ask']}</div>
                <div class="essence"><span class="t">💡 本质</span>{les['essence']}</div>
                <div class="baby"><span class="t">大白话</span>{les['baby']}</div>
                {les.get('extra','')}
            </div>
        </section>""")

    special = _special_code_block(day)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day {num} · {esc(title)} — Coze Studio 80 天源码</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/go.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
    <style>{css}</style>
</head>
<body>
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="logo" style="background:linear-gradient(135deg,{grad});">{num}</div>
            <h2>Day {num}</h2>
            <p class="version">{esc(title.split('：')[0])} · 6 讲</p>
        </div>
        <ul class="nav-list">
            <li class="nav-group-title">本日 6 讲</li>
            {nav_lessons}
            <li class="nav-group-title">导航</li>
            <li><a href="{PREFIX}-tutorial.html" class="nav-link" style="color:var(--accent-cyan);">&larr; 80 天总目录</a></li>
            <li><a href="{prev_link}" class="nav-link">{esc(prev_label)}</a></li>
            <li><a href="{next_link}" class="nav-link" style="color:var(--accent-green);">{esc(next_label)} &rarr;</a></li>
            <li><a href="index.html" class="nav-link">返回博客首页</a></li>
        </ul>
    </nav>
    <button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>

    <main class="content" id="content">
        <div class="part-header">
            <span class="part-label">Day {num} / 共 {TOTAL} 天 · 阶段{s['id']} {esc(s['name'])}</span>
            <h1 class="part-title">{esc(title)}</h1>
            <p class="part-desc">每天约 30 分钟。焦点：<span class="fileref">{esc(focus)}</span>。
            用类比把抽象钉住，用动图看请求流过，用真源码坐标对齐仓库。</p>
        </div>
        {journey_bar(day)}
        <div class="essence" style="margin:0 0 8px"><span class="t">💡 今日兜底类比</span>{esc(analogy)}</div>
        <div class="card" style="margin:10px 0">
          <div class="baby"><span class="t">📖 深度笔记</span>{DEEP_NOTES[day]}</div>
          <h3 style="margin:10px 0 8px;font-size:15px">💊 今日知识胶囊（30 分钟怎么吃）</h3>
          <ol style="margin:0;padding-left:18px;font-size:13px;color:var(--text-secondary);line-height:1.7">
            <li><strong>0–5 分</strong>：读完本页类比与阶段定位，在脑中标出「我在哪一层」。</li>
            <li><strong>5–15 分</strong>：打开焦点路径 <code>{esc(focus)}</code>，只看类型/接口/入口函数。</li>
            <li><strong>15–25 分</strong>：对照本页动图，口述「一次请求如何路过这里」。</li>
            <li><strong>25–30 分</strong>：跑「动手」命令，把 3 个关键词记到你的知识地图。</li>
          </ol>
        </div>
        {special}
        {''.join(sections)}
        <div class="nav-buttons">
            <a href="{prev_link}" class="nav-btn prev"><span class="nav-btn-label">上一篇</span><span class="nav-btn-title">{esc(prev_label)}</span></a>
            <a href="{next_link}" class="nav-btn next"><span class="nav-btn-label">下一篇</span><span class="nav-btn-title">{esc(next_label)}</span></a>
        </div>
    </main>
    <button class="scroll-top" id="scrollTop">↑</button>
    <script src="app.js"></script>
    <script>hljs.highlightAll();</script>
</body>
</html>
"""


def _special_code_block(day: int) -> str:
    """Inject real coze-studio snippets for high-value days."""
    blocks = {
        6: (
            "backend/main.go — 启动顺序（注释强调勿乱序）",
            """func main() {
    ctx := context.Background()
    // Please do not change the order of the function calls below
    setCrashOutput()
    if err := loadEnv(); err != nil { panic(...) }
    setLogLevel()
    if err := application.Init(ctx); err != nil { panic(...) }
    startHttpServer()
}""",
            "go",
        ),
        8: (
            "backend/main.go — 中间件顺序",
            """s.Use(middleware.ContextCacheMW())     // must be first
s.Use(middleware.RequestInspectorMW()) // must be second
s.Use(middleware.SetHostMW())
s.Use(middleware.SetLogIDMW())
s.Use(corsHandler)
s.Use(middleware.AccessLogMW())
s.Use(middleware.OpenapiAuthMW())
s.Use(middleware.SessionAuthMW())
s.Use(middleware.I18nMW()) // must after SessionAuthMW
router.GeneratedRegister(s)
s.Spin()""",
            "go",
        ),
        22: (
            "agent_run_impl.go — Pipe + 后台执行",
            """func (c *runImpl) AgentRun(ctx context.Context, arm *entity.AgentRunMeta) (*schema.StreamReader[*entity.AgentRunResponse], error) {
    sr, sw := schema.Pipe[*entity.AgentRunResponse](20)
    art := &internal.AgentRuntime{ RunMeta: arm, SW: sw, /* ... */ }
    safego.Go(ctx, func() {
        defer sw.Close()
        _ = art.Run(ctx)
    })
    return sr, nil
}""",
            "go",
        ),
        24: (
            "agent_flow_builder.go — 图节点钥匙名",
            """const (
    keyOfPersonRender           = "persona_render"
    keyOfKnowledgeRetriever     = "knowledge_retriever"
    keyOfPromptVariables        = "prompt_variables"
    keyOfPromptTemplate         = "prompt_template"
    keyOfReActAgent             = "react_agent"
    keyOfLLM                    = "llm"
    keyOfToolsPreRetriever      = "tools_pre_retriever"
)
// BuildAgent: 装配上述节点；有工具 → eino/react.NewAgent，否则走纯 LLM""",
            "go",
        ),
        55: (
            "model_builder.go — 供应商工厂表",
            """var modelClass2NewModelBuilder = map[developer_api.ModelClass]func(*config.Model) Service{
    developer_api.ModelClass_SEED:     newArkModelBuilder,
    developer_api.ModelClass_GPT:      newOpenaiModelBuilder,
    developer_api.ModelClass_Claude:   newClaudeModelBuilder,
    developer_api.ModelClass_DeekSeek: newDeepseekModelBuilder,
    developer_api.ModelClass_Gemini:   newGeminiModelBuilder,
    developer_api.ModelClass_Llama:    newOllamaModelBuilder,
    developer_api.ModelClass_QWen:     newQwenModelBuilder,
}""",
            "go",
        ),
    }
    if day not in blocks:
        return ""
    cap, code, lang = blocks[day]
    return f"""
<div class="card">
  <div class="fileref">{esc(cap)}</div>
  <pre><code class="language-{lang}">{esc(code)}</code></pre>
  <div class="baby"><span class="t">怎么读这段</span>先圈出「入口函数」和「分支条件」，再问：数据从哪来、到哪去、失败怎么办。</div>
</div>"""


# ---------------------------------------------------------------------------
# Tutorial hub
# ---------------------------------------------------------------------------
def render_hub() -> str:
    stage_html = []
    for s in STAGES:
        cards = []
        for d in range(s["lo"], s["hi"] + 1):
            title = TITLES[d - 1]
            short = title.split("：")[0]
            desc = title if "：" not in title else title.split("：", 1)[1]
            cards.append(f"""
            <a class="day-card" href="{PREFIX}-day{d:02d}.html">
              <div class="top"><div class="num" style="background:linear-gradient(135deg,{s['grad']});">{d:02d}</div>
              <h3>{esc(short)}</h3></div>
              <p>{esc(desc)}</p>
              <div class="foot"><span class="mins">≈30 min · 已就绪 <span class="badge">NEW</span></span>
              <span class="go">开始学 &rarr;</span></div>
            </a>""")
        stage_html.append(f"""
        <div class="week-bar" id="stage{s['id']}">
          <div class="wk" style="background:linear-gradient(135deg,{s['grad']});">S{s['id']}</div>
          <h2>阶段 {s['id']} · {esc(s['name'])}</h2>
          <span>{s['lo']:02d}-{s['hi']:02d} · {esc(s['blurb'])}</span>
        </div>
        <div class="day-grid">{''.join(cards)}</div>""")

    nav_stages = "\n".join(
        f'<li><a href="#stage{s["id"]}" class="nav-link">阶段 {s["id"]} · {esc(s["name"])}（{s["lo"]}-{s["hi"]}）</a></li>'
        for s in STAGES
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coze Studio 源码学习 · 80 天总目录（扣子开源）</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .content {{ max-width: 1180px; }}
        .arch-anim {{ position:relative; display:flex; flex-direction:column; gap:9px; padding:18px; margin:10px 0 4px;
            background:radial-gradient(120% 120% at 50% 0%, rgba(79,70,229,.10), transparent 70%); border-radius:14px; }}
        .arch-row {{ position:relative; border:1px solid var(--lc,var(--border-color)); border-radius:11px; padding:12px 16px;
            background:var(--bg-card); overflow:hidden; transition:transform .25s,box-shadow .25s; }}
        .arch-row:hover {{ transform:translateY(-3px); box-shadow:0 10px 26px rgba(0,0,0,.35); }}
        .arch-row::before {{ content:''; position:absolute; inset:0;
            background:linear-gradient(90deg,transparent,var(--glow,rgba(79,70,229,.14)),transparent);
            transform:translateX(-100%); animation:sweep 4.5s linear infinite; animation-delay:var(--d,0s); }}
        @keyframes sweep {{ 0%{{transform:translateX(-100%)}} 60%,100%{{transform:translateX(100%)}} }}
        .arch-row .lbl {{ font-size:11px; font-weight:800; letter-spacing:.06em; color:var(--lc); margin-bottom:7px; position:relative; }}
        .arch-row .boxes {{ display:flex; gap:7px; flex-wrap:wrap; position:relative; }}
        .arch-row .b {{ flex:1; min-width:110px; text-align:center; background:var(--bg-secondary); border:1px solid var(--border-color);
            border-radius:7px; padding:8px 9px; font-size:12px; color:var(--text-secondary); }}
        .arch-row .b strong {{ display:block; color:var(--text-primary); font-size:12.5px; margin-bottom:2px; }}
        .L1{{--lc:#4f46e5;--glow:rgba(79,70,229,.14)}} .L2{{--lc:#0ea5e9;--glow:rgba(14,165,233,.14)}}
        .L3{{--lc:#f59e0b;--glow:rgba(245,158,11,.12)}} .L4{{--lc:#10b981;--glow:rgba(16,185,129,.12)}}
        .flow-dot {{ position:absolute; left:50%; width:10px; height:10px; margin-left:-5px; border-radius:50%; background:#fff;
            box-shadow:0 0 10px 3px rgba(79,70,229,.8); animation:fall 3.4s cubic-bezier(.6,0,.4,1) infinite; z-index:3; opacity:0; }}
        @keyframes fall {{ 0%{{top:7%;opacity:0}} 10%{{opacity:1}} 90%{{opacity:1}} 100%{{top:93%;opacity:0}} }}
        .loopd{{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;padding:12px 4px}}
        .loopd .n{{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:9px;padding:10px 14px;font-size:12.5px;text-align:center}}
        .loopd .n b{{display:block;color:#818cf8;font-size:13px}}.loopd .a{{color:#a78bfa;font-weight:800;font-size:16px}}
        .week-bar {{ display:flex; align-items:center; gap:12px; margin:36px 0 14px; padding-left:2px; }}
        .week-bar .wk {{ width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff;flex-shrink:0; }}
        .week-bar h2 {{ font-size:17px; font-weight:700; margin:0; }} .week-bar span {{ font-size:12px; color:var(--text-muted); }}
        .day-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; }}
        .day-card {{ display:flex; flex-direction:column; gap:8px; background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:18px; text-decoration:none; transition:transform .2s,border-color .2s,box-shadow .2s; }}
        .day-card:hover {{ transform:translateY(-4px); border-color:rgba(79,70,229,.45); box-shadow:0 12px 34px rgba(79,70,229,.10); }}
        .day-card .top {{ display:flex; align-items:center; gap:10px; }}
        .day-card .num {{ width:40px;height:40px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:800;color:#fff;font-family:'SF Mono',monospace; }}
        .day-card h3 {{ font-size:15px; font-weight:700; color:var(--text-primary); margin:0; line-height:1.35; }}
        .day-card p {{ font-size:12.5px; color:var(--text-secondary); margin:0; line-height:1.6; flex:1; }}
        .day-card .foot {{ display:flex; align-items:center; justify-content:space-between; margin-top:4px; }}
        .day-card .mins {{ font-size:11px; color:var(--text-muted); }}
        .day-card .go {{ font-size:12px; font-weight:600; color:#818cf8; }}
        .badge {{ display:inline-block; font-size:10px; font-weight:700; padding:2px 8px; border-radius:20px; background:rgba(34,197,94,.12); color:var(--accent-green); }}
    </style>
</head>
<body>
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="logo" style="background:linear-gradient(135deg,#4f46e5,#7c3aed);">Cz</div>
            <h2>Coze Studio</h2>
            <p class="version">扣子开源 · 80 天源码深度</p>
        </div>
        <ul class="nav-list">
            <li class="nav-group-title">总目录</li>
            <li><a href="#intro" class="nav-link active">开篇 · 这是什么</a></li>
            <li><a href="#arch" class="nav-link">架构全景（动图）</a></li>
            <li><a href="#how" class="nav-link">怎么用这份教程</a></li>
            <li class="nav-group-title">8 阶段 · 80 天</li>
            {nav_stages}
            <li class="nav-group-title">导航</li>
            <li><a href="index.html" class="nav-link" style="color:var(--accent-cyan);">&larr; 返回博客首页</a></li>
        </ul>
    </nav>
    <button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>

    <main class="content" id="content">
        <div class="part-header">
            <span class="part-label">源码深度学习 · 零基础友好 · 80 天</span>
            <h1 class="part-title">Coze Studio 源码学习</h1>
            <p class="part-desc">80 天 · 每天约 30 分钟 · 读懂字节开源的「一站式 AI Agent 开发平台」。
            后端 Go（Hertz + Eino + DDD）· 前端 React/TS（Rush 海量包）· 核心在
            <code>AgentRun → agentflow → ReAct</code> 与 <code>Workflow Canvas→Compose→Execute</code>。
            <strong>真路径走读 + 大白话类比 + CSS/SVG 动图，AI 小白也能跟上。</strong></p>
        </div>

        <section id="intro" class="section">
            <div class="section-header"><span class="section-number">00</span><h1>开篇 · 这是个什么平台</h1></div>
            <div class="card">
                <p><strong>Coze Studio</strong>（扣子工作室开源版）是一站式 <strong>AI Agent 可视化开发平台</strong>：
                搭智能体、拖工作流、挂知识库与插件、调模型，还能用 OpenAPI / Chat SDK 集成到你的产品。</p>
                <div class="card highlight-card" style="margin:14px 0;">
                    <p style="margin:0;font-size:15px;">🎯 一句话：Coze = <strong>后端 <code>backend/</code>（Go/DDD）+ 前端 <code>frontend/</code>（Rush+React）+ 合同 <code>idl/</code>（Thrift）</strong>。
                    用户发一句话，主线是 <strong>Handler → Application → AgentRun(Pipe) → agentflow(BuildAgent) → Eino ReAct/LLM → 流式回写</strong>；
                    复杂业务则走 <strong>Workflow 画布 → Schema → Compose → 节点执行</strong>。</p>
                </div>
                <div class="feature-grid">
                    <div class="feature-item"><div class="feature-icon">🤖</div><h4>智能体</h4><p>人设 + 模型 + 插件 + 知识 + 工作流，ReAct 可自主调工具。</p></div>
                    <div class="feature-item"><div class="feature-icon">🕸️</div><h4>工作流引擎</h4><p>几十种节点，Canvas 可视化，底层 Eino compose。</p></div>
                    <div class="feature-item"><div class="feature-icon">📚</div><h4>知识库 RAG</h4><p>切片、Embedding、ES + Milvus 检索。</p></div>
                    <div class="feature-item"><div class="feature-icon">🔌</div><h4>插件与模型</h4><p>OpenAPI 插件 + ModelBuilder 多供应商。</p></div>
                </div>
                <div class="info-box"><strong>仓库在哪读</strong>：业务大脑几乎全在 <code>backend/domain/</code>；
                启动看 <code>backend/main.go</code> 与 <code>application/application.go</code>；
                跨域协作看 <code>backend/crossdomain/</code>；前端从 <code>frontend/apps/coze-studio</code> 与 <code>packages/agent-ide</code>、<code>packages/workflow</code> 入手。</div>
            </div>
        </section>

        <section id="arch" class="section">
            <div class="section-header"><span class="section-number">01</span><h1>架构全景（动起来看）</h1></div>
            <div class="card">
                <p>发光小球 = 「用户的一句话」从进门到吐字的旅程。</p>
                <div class="arch-anim">
                    <div class="flow-dot"></div>
                    <div class="arch-row L1" style="--d:0s"><div class="lbl">L1 · 接入 · frontend + api/</div><div class="boxes">
                        <div class="b"><strong>React IDE</strong>编排界面</div>
                        <div class="b"><strong>Hertz</strong>HTTP 服务</div>
                        <div class="b"><strong>Middleware</strong>鉴权/日志</div>
                        <div class="b"><strong>Handler</strong>IDL 生成路由</div>
                    </div></div>
                    <div class="arch-row L2" style="--d:.6s"><div class="lbl">L2 · 编排 · application/ + crossdomain/</div><div class="boxes">
                        <div class="b"><strong>Application</strong>用例编排</div>
                        <div class="b"><strong>Crossdomain</strong>外交窗口</div>
                        <div class="b"><strong>AgentRun</strong>Pipe 流</div>
                        <div class="b"><strong>Workflow App</strong>画布用例</div>
                    </div></div>
                    <div class="arch-row L3" style="--d:1.2s"><div class="lbl">L3 · 领域核心 · domain/</div><div class="boxes">
                        <div class="b"><strong>agentflow</strong>BuildAgent</div>
                        <div class="b"><strong>workflow</strong>Compose执行</div>
                        <div class="b"><strong>knowledge</strong>RAG</div>
                        <div class="b"><strong>plugin</strong>工具调用</div>
                    </div></div>
                    <div class="arch-row L4" style="--d:1.8s"><div class="lbl">L4 · 基础设施 · infra/ + docker</div><div class="boxes">
                        <div class="b"><strong>MySQL/Redis</strong></div>
                        <div class="b"><strong>ES/Milvus</strong></div>
                        <div class="b"><strong>NSQ/MinIO</strong></div>
                        <div class="b"><strong>Eino/Checkpoint</strong></div>
                    </div></div>
                </div>
                <div class="loopd">
                    <span class="n"><b>发消息</b></span><span class="a">→</span>
                    <span class="n"><b>AgentRun</b></span><span class="a">→</span>
                    <span class="n"><b>BuildAgent</b></span><span class="a">→</span>
                    <span class="n"><b>ReAct/LLM</b></span><span class="a">→</span>
                    <span class="n"><b>流式吐字</b></span>
                </div>
                <div class="tip"><strong>和 Dify 的差别直觉</strong>：Dify 核心偏 Python Flask「应用生成器」；
                Coze 开源版是 Go DDD + 字节 Eino 编排，智能体与工作流都深度嵌在同一套后端域模型里。</div>
            </div>
        </section>

        <section id="how" class="section">
            <div class="section-header"><span class="section-number">02</span><h1>怎么用这份教程</h1></div>
            <div class="feature-grid">
                <div class="feature-item"><div class="feature-icon">⏱️</div><h4>每天 30 分钟</h4><p>一页一天：类比 → 动图 → 源码坐标 → 动手命令 → 明日预告。</p></div>
                <div class="feature-item"><div class="feature-icon">👶</div><h4>零基础友好</h4><p>不假设你会 Go/DDD/Eino；术语第一次出现都有大白话。</p></div>
                <div class="feature-item"><div class="feature-icon">📍</div><h4>真仓库路径</h4><p>焦点文件来自真实 coze-studio 树，可对照本地 clone。</p></div>
                <div class="feature-item"><div class="feature-icon">🎨</div><h4>取舍与坑</h4><p>每天讲「为什么这样设计」和「一改就炸」的边界。</p></div>
            </div>
            <div class="tip"><strong>建议节奏</strong>：第 1–2 周建立地图与启动（S1–S2）；第 3–4 周打通对话主线（S3）；
            第 5–7 周沉浸工作流深水（S4）；随后补齐 RAG/插件/前端（S5–S7）；最后收官做作品（S8）。</div>
        </section>

        {''.join(stage_html)}

        <div class="nav-buttons" style="margin-top:48px;">
            <a href="index.html" class="nav-btn prev"><span class="nav-btn-label">返回</span><span class="nav-btn-title">博客首页</span></a>
            <a href="{PREFIX}-day01.html" class="nav-btn next"><span class="nav-btn-label">开始学习</span><span class="nav-btn-title">Day 01 · 心智模型</span></a>
        </div>
    </main>
    <button class="scroll-top" id="scrollTop">↑</button>
    <script src="app.js"></script>
</body>
</html>
"""


def patch_index() -> None:
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    marker = 'href="dify-tutorial.html"'
    card = f'''            <a class="blog-card" href="{PREFIX}-tutorial.html" data-ps="coze-studio" data-pd="80">
                <div class="blog-card-icon" style="background:linear-gradient(135deg,#4f46e5,#7c3aed);">Cz</div>
                <h3>Coze Studio 源码学习（80 天）</h3>
                <p class="blog-desc">扣子开源一站式 Agent 平台：Go DDD + Eino、Workflow 引擎、RAG/插件、Rush 前端。真路径走读 + 类比动图。</p>
                <div class="blog-card-tags"><span class="blog-tag">扣子</span><span class="blog-tag">Go</span><span class="blog-tag">80 天</span></div>
                <div class="blog-card-arrow">查看教程 &rarr;</div>
            </a>
'''
    if f'href="{PREFIX}-tutorial.html"' in text:
        print("index.html already linked")
        return
    if marker not in text:
        raise SystemExit("Could not find insertion point in index.html")
    # Insert Coze card before Dify card
    text = text.replace(
        '            <a class="blog-card" href="dify-tutorial.html"',
        card + '            <a class="blog-card" href="dify-tutorial.html"',
        1,
    )
    index.write_text(text, encoding="utf-8")
    print("patched index.html")


def main() -> None:
    hub = render_hub()
    (OUT / f"{PREFIX}-tutorial.html").write_text(hub, encoding="utf-8")
    print("wrote hub", f"{PREFIX}-tutorial.html", "bytes", len(hub))
    for d in range(1, TOTAL + 1):
        html_doc = render_day(d)
        path = OUT / f"{PREFIX}-day{d:02d}.html"
        path.write_text(html_doc, encoding="utf-8")
    print(f"wrote {TOTAL} day pages")
    patch_index()


if __name__ == "__main__":
    main()
