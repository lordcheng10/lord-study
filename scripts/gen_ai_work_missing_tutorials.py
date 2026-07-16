#!/usr/bin/env python3
"""Generate the missing AI_WORK 20-day source-code tutorial sites.

The output is intentionally static HTML: learners can open it directly in a
browser, while every source reference remains relative to its project root.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI_WORK = Path("/Users/bitmart/work/codes/github/AI_WORK")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


STAGE_NAMES = (
    ("入口与地图", 1, 3, "先认清入口、配置与顶层分工"),
    ("核心循环", 4, 6, "抓住对象怎样接力工作的主线"),
    ("核心能力", 7, 10, "沿业务闭环进入关键模块"),
    ("状态与协作", 11, 13, "理解消息、状态、存储如何流动"),
    ("模型与扩展", 14, 17, "连接模型、工具、记忆与 RAG"),
    ("复盘与扩展", 18, 20, "把能力串成可演进的工程"),
)

COMMON_CSS = """
.ask,.essence,.baby,.qa,.tradeoff,.pitfall{border-left:3px solid var(--c1);background:color-mix(in srgb,var(--c1) 8%,transparent);border-radius:0 8px 8px 0;padding:11px 14px;margin:10px 0;font-size:13px;line-height:1.72}.ask .t,.essence .t,.baby .t,.qa .t,.tradeoff .t,.pitfall .t{font-weight:800;color:var(--c1);display:block;margin-bottom:4px}.baby{border-color:var(--accent-green);background:rgba(34,197,94,.06)}.baby .t{color:var(--accent-green)}.qa{border-color:#a855f7;background:rgba(168,85,247,.06)}.qa .t{color:#c084fc}.tradeoff{border-color:#ec4899;background:rgba(236,72,153,.07)}.tradeoff .t{color:#f472b6}.pitfall{border-color:#ef4444;background:rgba(239,68,68,.07)}.pitfall .t{color:#f87171}.journey{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:10px;padding:12px 14px;margin:6px 0 16px}.journey .jt{font-size:11px;color:var(--text-muted);margin-bottom:8px}.journey .steps{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.journey .st{font-size:11.5px;padding:5px 10px;border-radius:20px;background:var(--bg-card);border:1px solid var(--border-color);color:var(--text-muted)}.journey .st.on{background:linear-gradient(135deg,var(--c1),var(--c2));color:#fff;border-color:transparent;font-weight:700}.journey .sep{color:var(--text-muted)}.fileref{display:inline-block;font-size:11px;background:color-mix(in srgb,var(--c1) 12%,transparent);color:#a5b4fc;border:1px solid color-mix(in srgb,var(--c1) 35%,transparent);border-radius:5px;padding:1px 7px;font-family:ui-monospace,monospace}.walk{margin:10px 0;border:1px solid var(--border-color);border-radius:8px;overflow:hidden}.walk .r{display:flex;gap:10px;padding:8px 10px;font-size:12.5px;border-top:1px solid var(--border-color);line-height:1.65}.walk .r:first-child{border-top:none}.walk code{color:var(--accent-cyan);min-width:180px;font-size:11.5px}.svgbox{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:12px;padding:16px;margin:12px 0;overflow-x:auto}.svgbox .cap{font-size:12px;color:var(--text-muted);text-align:center;margin-top:8px}.loopd{display:flex;align-items:center;justify-content:center;gap:7px;flex-wrap:wrap;padding:12px 4px}.loopd .n{background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:9px;padding:9px 12px;font-size:12px;text-align:center}.loopd .n b{display:block;color:var(--c1)}.loopd .a{color:var(--c2);font-size:16px;font-weight:800}.arch-anim{position:relative;display:flex;flex-direction:column;gap:9px;padding:18px;background:radial-gradient(120% 120% at 50% 0%,color-mix(in srgb,var(--c1) 10%,transparent),transparent 70%);border-radius:14px}.arch-row{position:relative;border:1px solid var(--lc);border-radius:11px;padding:12px 16px;background:var(--bg-card);overflow:hidden}.arch-row:before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--lc) 14%,transparent),transparent);transform:translateX(-100%);animation:sweep 4.5s linear infinite;animation-delay:var(--d)}@keyframes sweep{0%{transform:translateX(-100%)}60%,100%{transform:translateX(100%)}}.arch-row .lbl{font-size:11px;font-weight:800;letter-spacing:.06em;color:var(--lc);margin-bottom:7px;position:relative}.arch-row .boxes{display:flex;gap:7px;flex-wrap:wrap;position:relative}.arch-row .b{flex:1;min-width:120px;text-align:center;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:7px;padding:8px;font-size:12px}.arch-row .b strong{display:block;color:var(--text-primary);font-size:12.5px;margin-bottom:2px}.week-bar{display:flex;align-items:center;gap:12px;margin:34px 0 14px}.week-bar .wk{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff}.week-bar h2{font-size:17px;margin:0}.week-bar span{font-size:12px;color:var(--text-muted)}.day-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}.day-card{display:flex;flex-direction:column;gap:8px;background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:17px;text-decoration:none;transition:.2s}.day-card:hover{transform:translateY(-4px);border-color:var(--c1);box-shadow:0 12px 34px color-mix(in srgb,var(--c1) 10%,transparent)}.day-card .top{display:flex;align-items:center;gap:10px}.day-card .num{width:39px;height:39px;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800}.day-card h3{font-size:14.5px;color:var(--text-primary);margin:0}.day-card p{font-size:12.5px;color:var(--text-secondary);margin:0;line-height:1.6;flex:1}.day-card .foot{display:flex;justify-content:space-between}.day-card .mins{font-size:11px;color:var(--text-muted)}.day-card .go{font-size:12px;color:var(--c1);font-weight:700}
"""


def project(prefix, repo, title, one_liner, analogy, colors, logo, stack, day_rows, layers, stages=None):
    """day_rows: list of (title, focus, analogy, blurb) length 20."""
    assert len(day_rows) == 20, f"{prefix} needs 20 days, got {len(day_rows)}"
    days = [{"title": t, "focus": f, "analogy": a, "blurb": b} for t, f, a, b in day_rows]
    stage_src = stages or STAGE_NAMES
    stages_out = [
        {"id": n + 1, "name": name, "lo": lo, "hi": hi, "color": colors[0],
         "grad": f"linear-gradient(135deg,{colors[0]},{colors[1]})", "blurb": blurb}
        for n, (name, lo, hi, blurb) in enumerate(stage_src)
    ]
    return {"prefix": prefix, "repo": repo, "title": title, "one_liner": one_liner,
            "analogy": analogy, "colors": colors, "logo": logo, "lang_stack": stack,
            "stages": stages_out, "days": days, "layers": layers}


PROJECTS = [
    project("metagpt", "MetaGPT", "MetaGPT",
            "把软件公司 SOP 抽象为多角色 AI 协作，自动从需求推进到设计、编码与测试",
            "微型软件公司", ("#6366f1", "#8b5cf6"), "MG", "Python", [
        ("从 Team.run 进入软件公司", "metagpt/team.py", "公司总经理启动项目例会", "跟踪需求发布、回合循环、预算检查与归档。"),
        ("Context 如何集中管理依赖", "metagpt/context.py", "公司的共享行政台账", "认识配置、LLM、成本和工作空间如何被统一传递。"),
        ("Message 与共享 Schema", "metagpt/schema.py", "统一格式的工作单", "理解角色之间传递什么数据。"),
        ("Role 基类的运行循环", "metagpt/roles/role.py", "员工收件、判断、办事的日程", "阅读 observe、think、act 的核心职责。"),
        ("产品经理如何产出 PRD", "metagpt/roles/product_manager.py", "把老板口头想法写成需求文档", "连接角色提示词与需求动作。"),
        ("工程师如何消费设计并写代码", "metagpt/roles/engineer.py", "开发拿到设计图后施工", "观察代码任务的选择与执行。"),
        ("Action 抽象与输出注册", "metagpt/actions/action.py", "员工可执行的标准工序卡", "理解 Action 输入、提示词和结构化产出。"),
        ("需求分析动作", "metagpt/actions/analyze_requirements.py", "把模糊需求拆成待办事项", "学习需求从自然语言走向结构化信息。"),
        ("PRD 生成动作", "metagpt/actions/write_prd.py", "产品经理填写正式立项书", "理解文档生成与仓库落盘。"),
        ("设计 API 与代码生成", "metagpt/actions/design_api.py", "先画接口蓝图再安排施工", "对照 design_api 与 write_code 的衔接。"),
        ("Environment 的消息路由", "metagpt/environment/base_env.py", "公司的内部邮件和分派系统", "理解消息如何投递给可响应的角色。"),
        ("软件研发专用环境", "metagpt/environment/software/software_env.py", "为研发团队配置专属办公室", "理解环境如何附加领域行为。"),
        ("角色记忆管理", "metagpt/memory", "员工的会议纪要与个人笔记", "区分长期上下文、历史消息和检索范围。"),
        ("LLM Provider 统一入口", "metagpt/provider/llm_provider_registry.py", "采购部按供应商选择模型", "理解模型实现的注册与选择机制。"),
        ("OpenAI Provider 调用链", "metagpt/provider/openai_api.py", "拨打一个标准化的外部服务电话", "跟踪请求、流式响应和结果处理。"),
        ("成本控制", "metagpt/utils/cost_manager.py", "财务实时盯住项目预算", "理解 token 成本累计与预算熔断。"),
        ("RAG 检索流水线", "metagpt/rag", "图书管理员先找资料再给员工", "串起解析、索引、检索和重排。"),
        ("项目仓库与依赖图", "metagpt/utils/project_repo.py", "工程档案室维护文件与依赖关系", "理解生成代码怎样被组织和追踪。"),
        ("SoftwareCompany 装配案例", "metagpt/software_company.py", "按模板组建一支完整项目团队", "回看默认角色和流程如何组装。"),
        ("增加一个轻量定制角色", "metagpt/roles/assistant.py", "为公司新增一个专业岗位", "用已有 Role 与 Action 完成最小扩展。"),
    ], [("产品入口", ["Team", "SoftwareCompany"]), ("编排通信", ["Environment", "Message", "Context"]),
        ("角色决策", ["Role", "ProductManager", "Engineer"]), ("工作执行", ["Action", "Tools", "ProjectRepo"]),
        ("基础能力", ["Provider", "Memory", "RAG", "CostManager"])],
       (("看懂公司入口", 1, 3, "从 Team、Context、Message 建立总览"),
        ("角色如何接力", 4, 6, "理解 Role 的观察、思考和行动循环"),
        ("软件研发 SOP", 7, 10, "沿着 PRD、设计、编码与测试动作阅读"),
        ("消息与环境", 11, 13, "拆开发布订阅、记忆和环境调度"),
        ("模型与知识能力", 14, 17, "掌握 Provider、成本和 RAG 扩展"),
        ("完整项目复盘", 18, 20, "串起软件公司流程并完成小改造"))),

    project("openmanus", "OpenManus", "OpenManus",
            "以 ReAct/工具调用循环为核心，支持浏览器、代码执行、沙箱和 MCP 的通用任务 Agent",
            "能上网写代码的数字助理", ("#f59e0b", "#ef4444"), "OM", "Python", [
        ("CLI 入口与资源清理", "main.py", "助理上班、接单和下班关机", "跟踪 Manus.create、run 与 cleanup。"),
        ("配置对象如何装配", "app/config.py", "助理的工作偏好设置", "认识模型、工作目录和 MCP 配置来源。"),
        ("状态、消息与 Memory", "app/schema.py", "助理的对话记录和任务状态板", "理解运行中最重要的数据对象。"),
        ("BaseAgent 的步进循环", "app/agent/base.py", "每一步做完才决定下一步", "阅读状态转换、最大步数与卡住检测。"),
        ("ToolCallAgent 的思考与执行", "app/agent/toolcall.py", "助理先选工具再记录执行结果", "理解 LLM 工具调用的循环骨架。"),
        ("Manus 默认能力装配", "app/agent/manus.py", "给通用助理发放电脑、浏览器和工具箱", "查看默认工具和 MCP 工具动态加入。"),
        ("系统提示词控制策略", "app/prompt/manus.py", "给员工的一页工作手册", "理解提示词如何约束下一步行动。"),
        ("Tool 基类和参数契约", "app/tool/base.py", "统一规格的工具插座", "学习怎样定义可供模型调用的工具。"),
        ("ToolCollection 的工具注册", "app/tool/tool_collection.py", "工具柜的目录与借还系统", "理解名称查找、schema 输出与执行分发。"),
        ("Python 执行工具", "app/tool/python_execute.py", "助理临时使用一台计算器", "阅读代码执行、结果收集和错误返回。"),
        ("浏览器工具与上下文", "app/tool/browser_use_tool.py", "助理打开浏览器查资料并记住页面", "连接浏览器动作与下一轮上下文。"),
        ("PlanningFlow 的任务规划", "app/flow/planning.py", "先列旅行行程再逐项执行", "理解计划生成、更新和执行顺序。"),
        ("FlowFactory 选择运行模式", "app/flow/flow_factory.py", "按任务选择直办或项目制流程", "学习流程实例化入口。"),
        ("SWE 专项 Agent", "app/agent/swe.py", "专门处理代码任务的维修师", "比较通用 Agent 与软件工程 Agent 的差异。"),
        ("沙箱客户端", "app/sandbox/client.py", "让助理在隔离实验室操作", "理解执行资源如何获取和释放。"),
        ("沙箱核心管理器", "app/sandbox/core/manager.py", "实验室管理员分配工位", "阅读沙箱创建、缓存和清理逻辑。"),
        ("MCP 客户端工具桥接", "app/tool/mcp.py", "把外包团队的服务接进工具柜", "理解 SSE、stdio 和远程工具注册。"),
        ("内置 MCP Server", "app/mcp/server.py", "把自己的能力开放给其他助理", "认识从 Agent 到 MCP 服务的反向暴露。"),
        ("LLM 调用封装", "app/llm.py", "助理联系大脑服务的总机", "追踪模型消息、工具 schema 与响应解析。"),
        ("添加一个本地工具", "app/tool/file_operators.py", "给工具柜增加一件新工具", "以现有文件工具为模板完成最小扩展。"),
    ], [("入口层", ["main.py", "Config"]), ("Agent 循环", ["BaseAgent", "ToolCallAgent", "Manus"]),
        ("决策层", ["Prompt", "LLM", "Memory"]), ("执行层", ["ToolCollection", "Flow"]),
        ("外部资源", ["Sandbox", "Browser", "MCP"])],
       (("从命令行到 Agent", 1, 3, "理解入口、配置、状态与记忆"),
        ("ReAct 工作循环", 4, 7, "读 BaseAgent、ToolCallAgent、Manus"),
        ("工具系统", 8, 11, "工具定义、收集、调用及浏览器"),
        ("规划与专项能力", 12, 14, "规划流、数据分析和 SWE Agent"),
        ("外部执行与 MCP", 15, 17, "沙箱与远程工具连接"),
        ("端到端改造", 18, 20, "调试、观测并新增小工具"))),

    project("xagent", "XAgent", "XAgent",
            "以任务树、计划迭代、反思和工具服务器为中心的自主任务执行框架",
            "项目经理带着执行小队", ("#0ea5e9", "#6366f1"), "XA", "Python", [
        ("run.py 的任务启动参数", "run.py", "项目经理填写项目启动表", "认识 task、模型、计划树限制等运行参数。"),
        ("全局配置读取", "XAgent/config.py", "项目的统一管理制度", "理解 YAML 配置如何驱动模型和工作流。"),
        ("任务请求对象", "XAgent/workflow/base_query.py", "标准化的项目需求单", "查看用户任务如何变成内部 Query。"),
        ("XAgentCoreComponents 装配", "XAgent/core.py", "为项目组配齐日志、工具、记忆和专员", "沿 register_all 建立系统地图。"),
        ("Agent Dispatcher 能力派工", "XAgent/agent/dispatcher.py", "主管按专长派给不同员工", "理解能力标签到 Agent 类的映射。"),
        ("运行记录器", "XAgent/recorder.py", "项目日志和过程归档员", "理解任务状态、计划和工具结果为何被持久化。"),
        ("Plan 与任务树", "XAgent/data_structure/plan.py", "可展开的项目 WBS 树", "学习父子任务、遍历和状态推进。"),
        ("任务节点数据", "XAgent/data_structure/node.py", "每张子任务卡片", "理解节点关系与任务属性。"),
        ("生成初始计划", "XAgent/workflow/plan_exec.py", "先由规划师把大项目拆成工作包", "跟踪 PlanAgent 和 function-call 拆解。"),
        ("计划生成 Agent", "XAgent/agent/plan_generate_agent/agent.py", "负责首次排期的规划师", "理解提示词、函数 schema 和解析结果。"),
        ("任务处理主流程", "XAgent/workflow/task_handler.py", "项目经理逐项推进待办", "阅读取任务、执行、更新状态的主线。"),
        ("工具执行 Agent", "XAgent/agent/tool_agent/agent.py", "一线员工决定使用哪件工具", "理解任务上下文如何变成工具调用。"),
        ("函数与工具桥接", "XAgent/function_handler.py", "把外部设备说明翻译成员工能用的按钮", "查看工具 schema 汇总与分发。"),
        ("ToolServer 客户端接口", "XAgent/toolserver_interface.py", "项目组向外部实验室提交操作请求", "理解工具服务连接、执行和文件回收。"),
        ("工作记忆跨任务传递", "XAgent/workflow/working_memory.py", "团队共享白板", "学习不同子任务之间如何交接信息。"),
        ("反思 Agent", "XAgent/agent/reflect_agent/agent.py", "项目复盘专员", "理解如何从执行结果提出改进建议。"),
        ("计划细化与修改约束", "XAgent/workflow/plan_exec.py", "只允许修改尚未开工的后续排期", "阅读 split、add、delete 等计划操作。"),
        ("ReAct 内循环搜索", "XAgent/inner_loop_search_algorithms/ReACT.py", "员工边思考边试工具再观察", "理解单个任务内部的推理执行循环。"),
        ("服务端交互对象", "XAgentServer/interaction.py", "项目门户保存每次会话", "连接命令行核心与服务端会话。"),
        ("ToolServer 的工具实现边界", "ToolServer", "外部工具实验室的实际工位", "复盘从计划到远程工具执行的完整路径。"),
    ], [("接入层", ["run.py", "BaseQuery"]), ("核心编排", ["CoreComponents", "Dispatcher"]),
        ("计划决策", ["PlanAgent", "ReflectAgent"]), ("工作流状态", ["Plan", "Node", "TaskHandler"]),
        ("外部执行", ["FunctionHandler", "ToolServer"])],
       (("认识任务执行入口", 1, 3, "从 CLI、配置和查询对象理解启动参数"),
        ("装配 Agent 系统", 4, 6, "掌握 Core、Dispatcher 和记录器"),
        ("任务树与计划生成", 7, 10, "理解 Plan、Node 和初始任务拆分"),
        ("执行、工具与记忆", 11, 14, "跟踪子任务执行和工具协议"),
        ("反思与动态重规划", 15, 17, "阅读计划修改和 ReAct 搜索"),
        ("服务协同与端到端复盘", 18, 20, "串联 ToolServer、Server 和交互"))),

    project("autogen", "autogen", "AutoGen",
            "分层的多 Agent 开发框架：消息运行时为底座，上层提供 Agent、团队编排和模型/工具扩展",
            "有总线的智能体办公室", ("#3b82f6", "#06b6d4"), "AG", "Python", [
        ("Core、AgentChat、Ext 的分层", "python/packages", "乐高的底座、套装和外接配件", "建立包职责边界，避免一开始钻进细节。"),
        ("autogen_core 公共导出", "python/packages/autogen-core/src/autogen_core/__init__.py", "底层工具箱的总目录", "识别用户可直接使用的核心概念。"),
        ("AgentRuntime 抽象", "python/packages/autogen-core/src/autogen_core/_agent_runtime.py", "机器人团队的调度中心接口", "理解运行时需要提供的注册、发送与状态能力。"),
        ("AgentId、AgentType 与身份", "python/packages/autogen-core/src/autogen_core/_agent_id.py", "员工编号与岗位编号", "学习运行时如何定位一个 Agent 实例。"),
        ("Topic 与订阅模型", "python/packages/autogen-core/src/autogen_core/_topic.py", "公司频道和订阅名单", "理解发布订阅如何替代直接调用。"),
        ("RoutedAgent 消息路由", "python/packages/autogen-core/src/autogen_core/_routed_agent.py", "前台按信件类型分派给部门", "阅读 handler 注册与消息分发。"),
        ("单线程运行时调度", "python/packages/autogen-core/src/autogen_core/_single_threaded_agent_runtime.py", "单条传送带依次处理所有工单", "跟踪队列、投递、异常和空闲停止。"),
        ("模型客户端契约", "python/packages/autogen-core/src/autogen_core/models/_model_client.py", "统一规格的大脑插槽", "理解不同模型供应商如何被应用层替换。"),
        ("FunctionTool 包装函数", "python/packages/autogen-core/src/autogen_core/tools/_function_tool.py", "把普通函数包装成机器人可按的按钮", "学习 schema、参数验证和异步执行。"),
        ("模型上下文窗口策略", "python/packages/autogen-core/src/autogen_core/model_context", "秘书决定给老板递交哪些历史材料", "比较缓冲、截断和 token 限制策略。"),
        ("AssistantAgent 的高层循环", "python/packages/autogen-agentchat/src/autogen_agentchat/agents/_assistant_agent.py", "会调用工具并回答的通用员工", "连接模型、消息、工具和反思式调用。"),
        ("ChatAgent 与 TaskResult", "python/packages/autogen-agentchat/src/autogen_agentchat/base/_chat_agent.py", "团队成员的统一工作交付格式", "理解 AgentChat 对 Core 的应用层封装。"),
        ("消息事件类型", "python/packages/autogen-agentchat/src/autogen_agentchat/messages.py", "会议中的发言、工具回执和流式字幕", "认识文本、多模态和事件消息。"),
        ("可组合终止条件", "python/packages/autogen-agentchat/src/autogen_agentchat/conditions/_terminations.py", "会议的散会规则", "学习按消息数、关键词、外部信号停止。"),
        ("BaseGroupChat 连接两层框架", "python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_base_group_chat.py", "会议组织者把成员接到消息传送带", "理解团队初始化、流式输出与状态保存。"),
        ("RoundRobinGroupChat 轮流发言", "python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_round_robin_group_chat.py", "会议按座位顺序轮流说话", "掌握最容易上手的多 Agent 协作策略。"),
        ("SelectorGroupChat 动态选人", "python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_selector_group_chat.py", "主持人按议题点名最合适的人", "理解由模型选择下一位发言者。"),
        ("OpenAI 扩展模型客户端", "python/packages/autogen-ext/src/autogen_ext/models/openai/_openai_client.py", "给标准大脑插槽接上一家具体供应商", "追踪模型适配、消息转换和响应规范化。"),
        ("MCP Workbench 接入远程工具", "python/packages/autogen-ext/src/autogen_ext/tools/mcp/_workbench.py", "把外部工具台接到机器人团队", "理解 MCP 会话与工具发现。"),
        ("代码执行扩展与 Studio 延伸", "python/packages/autogen-ext/src/autogen_ext/code_executors", "让机器人进入隔离实验室运行代码", "以执行器为例复盘 Core—AgentChat—Ext 的扩展路径。"),
    ], [("运行时层", ["AgentRuntime", "AgentId", "Topic"]), ("Agent 基础", ["RoutedAgent", "模型", "工具"]),
        ("应用 Agent", ["AssistantAgent", "消息", "终止条件"]), ("团队编排", ["RoundRobin", "Selector"]),
        ("扩展集成", ["OpenAI", "MCP", "CodeExecutor"])],
       (("认识三层包结构", 1, 3, "区分 Core、AgentChat 与 Extensions"),
        ("Core 消息运行时", 4, 7, "学习 Agent ID、Topic、订阅和路由"),
        ("模型、工具与上下文", 8, 10, "掌握模型客户端、函数工具和记忆"),
        ("高层聊天 Agent", 11, 14, "阅读 AssistantAgent、消息和终止机制"),
        ("团队编排", 15, 17, "理解轮询、选择器和图协作"),
        ("扩展与产品化", 18, 20, "接入 MCP、代码执行和 Studio"))),

    project("babyagi", "babyagi", "BabyAGI（functionz）",
            "把 Python 函数作为可版本化、可依赖解析、可追踪执行的数据库资产管理（新版 functionz，非 2023 经典版）",
            "会自动装配工具的工坊", ("#22c55e", "#14b8a6"), "BA", "Python", [
        ("应用创建与公开 API", "babyagi/__init__.py", "工坊前台", "跟踪 create_app 如何把 functionz、API 和界面接在一起。"),
        ("Functionz 门面对象", "babyagi/functionz/core/framework.py", "工坊总控台", "理解一个对象如何统一管理函数、密钥、版本和执行。"),
        ("函数包自动加载", "babyagi/functionz/packs", "工具箱货架", "认识默认、草稿和插件函数包的装载方式。"),
        ("register_function 装饰器", "babyagi/functionz/core/registration.py", "给机器贴登记标签", "学习源码、元数据和依赖如何被登记。"),
        ("AST 参数推断", "babyagi/functionz/core/registration.py", "自动填写设备说明书", "理解从函数签名和返回值提取输入输出。"),
        ("函数与版本数据模型", "babyagi/functionz/db/models.py", "工具档案柜", "阅读 Function、FunctionVersion、Import 的关系。"),
        ("数据库路由与本地存储", "babyagi/functionz/db", "档案管理员", "理解框架如何隔离具体数据库实现。"),
        ("动态依赖解析", "babyagi/functionz/core/execution.py", "开工前备齐零件", "跟踪依赖函数与 Python 包的递归加载。"),
        ("受控代码执行", "babyagi/functionz/core/execution.py", "执行车间", "理解从数据库代码到 exec 和调用包装器的路径。"),
        ("触发器与调用链", "babyagi/functionz/core/execution.py", "流水线感应器", "学习父子调用、触发执行和递归保护。"),
        ("执行日志模型", "babyagi/functionz/db/models.py", "工单流水账", "查看输入、输出、耗时和调用关系的记录方式。"),
        ("密钥加密存储", "babyagi/functionz/db/models.py", "钥匙保管柜", "理解密钥模型与 Fernet 加密；讨论密钥文件管理风险。"),
        ("版本切换与回滚", "babyagi/functionz/core/framework.py", "启用旧版机器图纸", "跟踪激活某个函数版本的接口。"),
        ("函数查询 API", "babyagi/api", "工坊查询窗口", "阅读函数列表、详情与版本的 HTTP 路由。"),
        ("远程执行 API", "babyagi/api", "远程启动按钮", "理解请求 JSON 如何映射到函数执行。"),
        ("Dashboard 管理界面", "babyagi/dashboard", "工坊监控屏", "把前端操作对应回 API 与数据库。"),
        ("默认 AI 函数包", "babyagi/functionz/packs/default/ai_functions.py", "出厂预装工具", "观察 LLM 能力如何被封装成可注册函数。"),
        ("自构建 Agent 草稿", "babyagi/functionz/packs/drafts/self_build.py", "会设计新机器的机器", "阅读实验性自生成流程，不把它误当生产方案。"),
        ("生成函数草稿流程", "babyagi/functionz/packs/drafts/generate_function.py", "AI 工程师助理", "理解提示、代码生成和函数登记如何串联。"),
        ("安全边界与重构练习", "babyagi/functionz/core/execution.py", "车间安全检查", "复盘动态 pip 安装、exec、密钥输出等不适合直接生产使用的边界。"),
    ], [("交互层", ["Flask App", "api", "dashboard"]), ("函数资产", ["Functionz", "Registrar", "packs"]),
        ("执行编排", ["Executor", "依赖", "触发器"]), ("持久化", ["DB", "Version", "Log", "Secret"])],
       (("认识 functionz", 1, 3, "从应用入口理解函数即资产"),
        ("函数入库", 4, 6, "装饰器、源码提取与版本模型"),
        ("运行引擎", 7, 10, "动态加载、依赖与触发器"),
        ("持久化与安全", 11, 13, "数据库、密钥和审计日志"),
        ("可视化运维", 14, 17, "Flask API 与 Dashboard"),
        ("自构建实验", 18, 20, "函数包、Agent 草稿与风险复盘"))),

    project("langflow", "langflow", "Langflow",
            "用可视化画布构建、运行并部署 LLM 工作流、Agent 和 MCP 工具的平台",
            "给 AI 搭乐高流水线的白板", ("#a855f7", "#ec4899"), "LF", "Python + TypeScript", [
        ("Monorepo 与启动入口", "pyproject.toml", "园区总平面图", "认识 backend、LFx、SDK、frontend 的工作区关系。"),
        ("后端 main 生命周期", "src/backend/base/langflow/main.py", "餐厅开门流程", "追踪应用配置、生命周期和服务器启动。"),
        ("前端 React 入口", "src/frontend/src/index.tsx", "白板开机按钮", "理解浏览器端如何挂载整个编辑器。"),
        ("LFx 组件体系导览", "src/lfx/src/lfx/components", "乐高积木仓库", "按模型、工具、向量库等类别认识组件实现。"),
        ("流程构建器", "src/lfx/src/lfx/graph/flow_builder/builder.py", "把积木摆上底板", "学习 JSON 定义如何变成可执行流程。"),
        ("节点和端口模型", "src/lfx/src/lfx/graph/vertex", "积木的插口规范", "理解节点参数、输入输出类型与校验。"),
        ("边与连线", "src/lfx/src/lfx/graph/edge", "积木连接线", "掌握数据怎样在节点之间传递。"),
        ("Graph 执行状态", "src/lfx/src/lfx/graph/graph", "流水线调度板", "阅读可运行节点管理和图状态模型。"),
        ("运行时默认值", "src/lfx/src/lfx/run", "流水线默认参数册", "理解运行请求怎样转换为执行配置。"),
        ("后端流程运行服务", "src/backend/base/langflow/services/flow/flow_runner.py", "车间调度员", "跟踪一次 API 请求如何触发流程执行。"),
        ("运行接口适配", "src/backend/base/langflow/interface/run.py", "把订单翻译成工单", "理解 UI/API 输入与 LFx 运行时之间的转换。"),
        ("路由注册与版本化 API", "src/backend/base/langflow/api/router.py", "服务大厅分诊台", "识别 v1、v2、健康检查等路由装配。"),
        ("流程 CRUD API", "src/backend/base/langflow/api/v1/flows.py", "保存和取回流程图", "学习流程定义的创建、查询、修改和删除。"),
        ("服务工厂与依赖管理", "src/backend/base/langflow/services/factory.py", "后勤服务总台", "理解数据库、缓存、存储等服务如何被初始化。"),
        ("前端路由与页面", "src/frontend/src/routes.tsx", "白板应用导航图", "认识编辑、设置和其他产品页面。"),
        ("自定义画布节点", "src/frontend/src/CustomNodes", "可视化积木外壳", "把后端组件字段映射成可编辑节点。"),
        ("前端状态与控制器", "src/frontend/src/stores", "白板的记忆", "学习流程图、选中状态和交互状态的管理。"),
        ("MCP 工作流发布", "src/backend/base/langflow/api/v2/mcp.py", "把流水线变成可调用机器", "理解如何把 flow 暴露给 MCP 客户端。"),
        ("自定义组件入口", "src/backend/base/langflow/custom", "制作自己的乐高积木", "阅读自定义 Python 组件的加载和兼容路径。"),
        ("追踪与扩展复盘", "src/backend/base/langflow/services/tracing", "流水线黑匣子", "梳理运行可观测性与新增组件的最小实现路径。"),
    ], [("创作层", ["React", "Canvas", "CustomNodes"]), ("API 层", ["FastAPI", "v1", "v2", "MCP"]),
        ("编排层", ["Interface", "FlowRunner", "FlowBuilder"]), ("执行层", ["Graph", "Vertex", "Components"]),
        ("平台层", ["Services", "DB", "Tracing"])],
       (("全景与启动", 1, 3, "认识 monorepo、前后端和 LFx"),
        ("画布数据模型", 4, 7, "节点、边、流程 JSON 与组件"),
        ("图执行", 8, 11, "构建图、调度节点和流式结果"),
        ("后端产品化", 12, 14, "API、服务容器与持久化"),
        ("前端交互", 15, 17, "画布、状态和自定义节点"),
        ("部署扩展", 18, 20, "MCP、SDK、观测与自定义组件"))),

    project("langfuse", "langfuse", "Langfuse",
            "面向团队的开源 LLM 工程平台：追踪、提示词、评测、数据集和调试",
            "AI 应用的飞行记录仪 + 实验室", ("#f97316", "#eab308"), "LF", "TypeScript", [
        ("Turbo Monorepo 与应用边界", "package.json", "园区组织图", "区分 web、worker 和 shared 三个核心包。"),
        ("共享服务端入口", "packages/shared/src/index.ts", "公共零件目录", "认识跨 Web 与 Worker 复用的基础能力。"),
        ("Web 与 Worker 启动", "worker/src/index.ts", "前台与后台值班员", "理解同步请求服务和异步后台服务的分工。"),
        ("追踪领域模型", "packages/shared/src/server/repositories/traces.ts", "一次飞行总记录", "学习 trace 在产品查询层的基本形态。"),
        ("Observation 查询模型", "packages/shared/src/server/repositories/observations.ts", "飞行中的每个动作", "区分模型生成、工具调用等细粒度观测。"),
        ("事件与会话仓储", "packages/shared/src/server/repositories/events.ts", "把航班串成旅程", "认识事件、session 与 trace 的关联。"),
        ("Public Trace API", "web/src/pages/api/public/traces", "外部设备上传窗口", "跟踪 SDK/用户如何访问追踪数据。"),
        ("摄取服务", "worker/src/services/IngestionService", "机场行李分拣线", "理解输入事件如何被校验、转换和批处理。"),
        ("摄取队列", "worker/src/queues/ingestionQueue.ts", "待处理工单队列", "学习可靠异步摄取的生产者与消费者边界。"),
        ("ClickHouse 写入器", "worker/src/services/ClickhouseWriter", "分析仓库装卸员", "理解高吞吐观测数据写入分析数据库的职责。"),
        ("OTel 摄取队列", "worker/src/queues/otelIngestionQueue.ts", "另一种标准货运通道", "认识 OpenTelemetry 数据接入的专用流程。"),
        ("tRPC 根路由", "web/src/server/api/root.ts", "内部服务总机", "了解 Web 前端调用后端领域能力的组织方式。"),
        ("追踪表查询 API", "web/src/server/api/routers/traces.ts", "记录仪检索台", "阅读筛选、分页和权限后的 trace 查询。"),
        ("Prompt 领域服务", "packages/shared/src/server/services/PromptService", "提示词版本仓库", "理解提示词版本、缓存和服务端规则。"),
        ("数据集领域服务", "packages/shared/src/server/services/DatasetService", "实验样本库", "学习数据集与数据项的验证和管理。"),
        ("追踪产品页面模块", "web/src/features/tracing-tables", "飞行记录仪仪表盘", "将表格、过滤器和后端查询对应起来。"),
        ("提示词产品模块", "web/src/features/prompts", "实验配方编辑器", "理解提示词 UI 如何接入版本化服务。"),
        ("评测与实验队列", "worker/src/queues/evalQueue.ts", "自动质检工位", "学习异步评测任务的触发与处理。"),
        ("Score 查询与配置", "packages/shared/src/server/repositories/scores.ts", "给每次飞行打分", "理解质量分数如何成为可分析数据。"),
        ("保留、删除与数据生命周期", "worker/src/queues/dataRetentionQueue.ts", "档案保管期限", "复盘从摄取到分析、保留和删除的完整闭环。"),
    ], [("接入层", ["SDK", "Public API", "OTel"]), ("应用层", ["Next.js", "tRPC", "Features"]),
        ("领域层", ["Repositories", "Prompt", "Dataset"]), ("异步层", ["Queues", "Worker", "Ingestion"]),
        ("数据层", ["Postgres", "ClickHouse", "Redis"])],
       (("平台全景", 1, 3, "数据流和 monorepo 边界"),
        ("可观测性数据", 4, 7, "Trace、Observation、事件摄取"),
        ("异步数据管道", 8, 11, "Redis 队列与 ClickHouse"),
        ("服务端产品能力", 12, 14, "API、仓储和领域服务"),
        ("产品界面", 15, 17, "追踪、提示词、评测和数据集"),
        ("评估闭环", 18, 20, "实验、保留与扩展方案"))),

    project("letta", "letta", "Letta（Legacy V1）",
            "提供带长期记忆、工具调用和多模型适配的状态化 LLM Agent 服务端（本仓库为 legacy V1）",
            "会做笔记的长期助理", ("#8b5cf6", "#ec4899"), "LT", "Python", [
        ("Legacy V1 服务端定位", "README.md", "阅读旧大楼导览牌", "确认本仓库的维护状态和适合学习的边界。"),
        ("CLI 入口", "letta/main.py", "服务大楼的总开关", "认识命令行如何启动和管理 Letta 服务。"),
        ("FastAPI 应用装配", "letta/server/rest_api/app.py", "服务大厅开门流程", "阅读中间件、路由、异常和应用生命周期。"),
        ("Agent API 路由", "letta/server/rest_api/routers/v1/agents.py", "助理管理柜台", "理解 Agent 创建、查询和配置的 HTTP 接口。"),
        ("Agent 请求与响应模型", "letta/schemas/agent.py", "助理档案表", "掌握 API 数据契约和领域字段。"),
        ("消息与记忆 Schema", "letta/schemas/memory.py", "短期工作台与长期笔记", "理解记忆块、上下文和消息结构。"),
        ("Agent 持久化模型", "letta/orm/agent.py", "助理档案数据库", "阅读 Agent 在关系数据库中的实体表达。"),
        ("Agent 主循环", "letta/agents/agent_loop.py", "助理的思考—行动循环", "跟踪一轮输入如何变成模型调用、工具调用和结果。"),
        ("Letta Agent 实现", "letta/agents/letta_agent.py", "助理的工作手册", "认识具体 Agent 如何组合记忆、消息和配置。"),
        ("上下文窗口计算", "letta/services/context_window_calculator/context_window_calculator.py", "行李箱容量管理员", "理解如何在 token 上限内安排上下文。"),
        ("消息 API 与流式交付", "letta/server/rest_api/routers/v1/messages.py", "助理回话的传递通道", "把消息请求、Agent 运行和 HTTP 响应串起来。"),
        ("Agent Manager", "letta/services/agent_manager.py", "助理人事经理", "学习 Agent 生命周期和业务编排的服务层做法。"),
        ("Message Manager", "letta/services/message_manager.py", "对话记录管理员", "理解消息创建、查询和持久化职责。"),
        ("Block 与长期记忆", "letta/services/block_manager.py", "可编辑的长期笔记页", "掌握记忆块的管理与版本化思路。"),
        ("模型供应商抽象", "letta/llm_api/llm_client.py", "不同品牌电话的统一拨号器", "理解统一接口如何屏蔽模型提供商差异。"),
        ("工具 Schema 生成", "letta/functions/schema_generator.py", "把工具说明翻译给助理", "学习 Python 工具如何成为 LLM 可调用的描述。"),
        ("MCP 工具执行", "letta/services/tool_executor/mcp_tool_executor.py", "接入外部工具柜", "理解 Agent 如何经 MCP 调用外部能力。"),
        ("上下文摘要与压缩", "letta/services/summarizer/compact.py", "把长会议纪要压成要点", "阅读超长对话的记忆保留策略。"),
        ("数据源与文件接入", "letta/data_sources/connectors.py", "给助理导入资料柜", "认识外部资料进入 Agent 系统的边界。"),
        ("V1 架构复盘与迁移判断", "letta/server/server.py", "旧大楼改造评估", "梳理分层，并结合仓库状态判断何时转向新 Letta Agent。"),
    ], [("接入层", ["CLI", "FastAPI", "Routers"]), ("Agent 层", ["AgentLoop", "LettaAgent"]),
        ("领域服务", ["Agent/Message/Block Managers"]), ("集成层", ["LLM", "MCP", "数据源"]),
        ("数据层", ["Schemas", "ORM", "记忆存储"])],
       (("遗留服务端全景", 1, 3, "定位 V1、入口和 API"),
        ("Agent 与记忆模型", 4, 7, "消息、Block、上下文窗口"),
        ("一次对话的运行环", 8, 11, "模型、工具、流式响应"),
        ("服务与存储", 12, 14, "Manager、ORM、数据生命周期"),
        ("扩展能力", 15, 17, "多模型、MCP、数据源"),
        ("可靠运行", 18, 20, "摘要、可观测性与迁移判断"))),

    project("mastra", "mastra", "Mastra",
            "面向 TypeScript 的全栈 AI Agent 应用框架：Agent、工具、工作流、记忆、RAG、部署与可观测",
            "AI 应用装配厂", ("#06b6d4", "#8b5cf6"), "MA", "TypeScript", [
        ("认识 Mastra 单仓库", "package.json", "先看工厂总平面图", "理解 pnpm、Turbo 与 packages、stores 的分工。"),
        ("从公共出口进入核心", "packages/core/src/index.ts", "从工厂前台找到各部门入口", "追踪 @mastra/core 对外导出的主要能力。"),
        ("Mastra 应用容器", "packages/core/src/mastra", "总调度室登记所有员工和流程", "理解 Agent、Workflow、存储等组件如何被统一注册。"),
        ("Agent 基础对象", "packages/core/src/agent/agent.ts", "定义一个有岗位说明书的 AI 员工", "阅读模型、指令、工具与生成接口如何组合。"),
        ("消息与会话状态", "packages/core/src/agent/message-list", "员工的对话记录夹", "理解消息怎样组织、追加与提供给模型。"),
        ("流式回答和工具循环", "packages/core/src/tool-loop-agent", "员工边查资料边汇报进度", "理解模型发起 tool call 后的迭代执行。"),
        ("定义 Tool", "packages/core/src/tools", "给员工配计算器和查询终端", "学习输入 schema、执行函数与工具结果。"),
        ("模型与供应商抽象", "packages/core/src/llm", "为员工接入不同品牌的电话线路", "理解统一模型接口与 provider 适配。"),
        ("创建工作流", "packages/core/src/workflows/create.ts", "画出流水线的第一步", "学习步骤、输入输出与 workflow 声明。"),
        ("工作流执行引擎", "packages/core/src/workflows/execution-engine.ts", "流水线调度员按图派工", "理解步骤调度、状态推进与执行结果。"),
        ("分支与并行", "packages/core/src/workflows", "订单按条件进入不同产线", "阅读 branch、parallel、foreach 等控制流。"),
        ("暂停和恢复", "packages/core/src/agent/durable", "审批未完成时把工单放进待办箱", "理解持久化状态、人工介入与继续执行。"),
        ("短期与长期记忆", "packages/memory/src", "把临时便签升级为长期档案", "学习记忆处理器、线程与上下文压缩。"),
        ("文档与 RAG", "packages/rag/src/document", "把图书拆页、编目再检索", "理解文档切分与可检索内容的形成。"),
        ("检索与 Graph RAG", "packages/rag/src/graph-rag", "不仅找书，还沿人物关系找线索", "学习结构化关系辅助检索的思路。"),
        ("存储适配器", "stores", "同一份档案可放进不同仓库", "比较 PG、Qdrant、Redis 等实现的统一接口。"),
        ("MCP 客户端和服务端", "packages/mcp/src", "让外部工具按统一插座接入工厂", "理解 MCP 资源、工具和传输层。"),
        ("HTTP 服务封装", "packages/server/src/server", "给工厂开一个对外服务窗口", "学习 Agent 与 Workflow 如何成为 API。"),
        ("评测与可观测性", "packages/core/src/evals", "质检员记录每次生产的质量", "理解 trace、评分与回归评测入口。"),
        ("端到端项目复盘", "templates/weather-agent", "用一条完整产线交付样品", "从模板回看 Agent、Tool、服务与运行配置如何落地。"),
    ], [("应用层", ["CLI", "Playground", "模板"]), ("编排层", ["Mastra", "Agent", "Workflow", "Tool"]),
        ("上下文层", ["Memory", "RAG", "MCP"]), ("基础设施", ["Storage", "Server", "Evals"])],
       (("仓库与最小 Agent", 1, 3, "包边界与最小 Agent"),
        ("消息、模型与工具", 4, 6, "消息、模型调用、工具循环"),
        ("工作流与可暂停执行", 7, 10, "工作流与可暂停执行"),
        ("记忆、检索与存储", 11, 13, "记忆、检索与存储"),
        ("MCP、服务与集成", 14, 17, "MCP、服务接口与集成"),
        ("评测与生产化", 18, 20, "评测、观测与生产化阅读"))),

    project("mem0", "mem0", "Mem0",
            "为 AI Agent 提供可抽取、存储、检索和个性化使用的长期记忆层",
            "智能体的长期记忆卡片盒", ("#10b981", "#3b82f6"), "M0", "Python + TypeScript", [
        ("认识记忆层问题", "README.md", "先定义档案管理员要解决什么问题", "区分短上下文、会话记忆与长期个性化记忆。"),
        ("Python 包与依赖", "pyproject.toml", "查看档案室能接哪些柜子和工具", "理解核心依赖与可选 LLM、向量库 extras。"),
        ("配置模型", "mem0/configs/base.py", "填写档案馆运行规则", "阅读 MemoryConfig、记忆项和后端配置。"),
        ("Memory 主入口", "mem0/memory/main.py", "档案管理员的总工作台", "定位 add、search、get、update、delete 的主流程。"),
        ("消息规范化", "mem0/memory/utils.py", "把口语录音整理为可归档文本", "学习消息、视觉消息与模型 JSON 输出解析。"),
        ("事实抽取提示词", "mem0/configs/prompts.py", "给档案员一份摘录准则", "理解 ADD-only 事实抽取与 Agent 上下文提示。"),
        ("记忆抽象与存储", "mem0/memory/base.py", "为不同档案馆规定统一操作手册", "学习 MemoryBase 的职责与扩展边界。"),
        ("向量检索接口", "mem0/vector_stores/base.py", "按语义在档案中找相似卡片", "理解插入、搜索、过滤和删除的统一能力。"),
        ("Qdrant 具体实现", "mem0/vector_stores/qdrant.py", "参观一种具体的智能档案柜", "将接口映射到真实向量数据库操作。"),
        ("Embedding 适配", "mem0/embeddings", "把文字转成可比对的坐标", "理解 OpenAI、本地和云模型的向量化封装。"),
        ("混合检索与评分", "mem0/utils/scoring.py", "语义、关键词和人物线索共同决定档案排序", "学习 BM25、归一化和多信号融合。"),
        ("实体提取", "mem0/utils/entity_extraction.py", "给档案贴上人物、地点和主题标签", "理解实体如何提升关联记忆的召回。"),
        ("LLM 抽象", "mem0/llms/base.py", "允许档案员使用不同品牌的理解引擎", "学习模型提供商可替换的接口设计。"),
        ("工厂模式", "mem0/utils/factory.py", "依据配置自动配发合适设备", "追踪 LLM、Embedding、重排器和向量库的装配。"),
        ("TypeScript 平台客户端", "mem0-ts/src/client/index.ts", "为 JavaScript 应用开设同一档案窗口", "比较 TypeScript SDK 与 Python API。"),
        ("TS 开源实现", "mem0-ts/src/oss", "用另一种语言复建档案管理员", "阅读本地记忆、向量库和示例。"),
        ("TS 社区集成", "mem0-ts/src/community", "把记忆接到常见 Agent 框架", "理解 community 集成包的边界。"),
        ("自托管服务", "server", "把档案室变成团队共用服务台", "理解 API、Dashboard、认证与 Docker 化边界。"),
        ("应用集成示例", "integrations/vercel-ai-sdk", "让客服系统每次接待都查历史档案", "学习在 Agent/UI 框架中插入记忆操作。"),
        ("测试一条记忆闭环", "tests", "用模拟客户验收档案是否找对", "从测试学习 add → extract → search 的可验证行为。"),
    ], [("接入层", ["Python/TS SDK", "CLI", "Server"]), ("记忆编排", ["Memory API", "写入", "搜索"]),
        ("智能处理", ["事实抽取", "实体", "偏好"]), ("检索层", ["向量", "BM25", "重排"]),
        ("持久化", ["向量库", "SQLite 元数据"])],
       (("产品边界与配置", 1, 3, "产品边界、SDK 与配置"),
        ("写入记忆路径", 4, 7, "写入记忆的完整路径"),
        ("多路检索与排序", 8, 11, "多路检索与排序"),
        ("可插拔模型与存储", 12, 14, "可插拔模型和存储"),
        ("TypeScript 与服务化", 15, 17, "TypeScript SDK 与服务化"),
        ("集成、测试与闭环", 18, 20, "集成、测试和完整应用"))),

    project("zep", "zep", "Zep 示例集",
            "Zep Cloud 的 Agent Memory 示例与集成仓库（不是完整产品服务端）",
            "外接式记忆云盘 + 关系图谱导航器的操作手册", ("#6366f1", "#22c55e"), "ZP", "Python + TypeScript", [
        ("确认仓库定位", "README.md", "先分清这是使用手册，不是云盘后端", "理解该仓库提供 examples、integrations、MCP、benchmark，而非完整 Zep 产品。"),
        ("最小 Python 快速开始", "examples/python/quickstart", "第一次向记忆云盘存取信息", "从 SDK 初始化、用户与消息写入开始。"),
        ("最小 TypeScript 记忆", "examples/typescript/memory", "用另一种语言访问同一档案服务", "对照 Python 与 TypeScript SDK 的调用形态。"),
        ("用户建模", "examples/typescript/users", "先给每位客户建立档案卡", "理解 userId、用户属性和隔离边界。"),
        ("聊天历史", "examples/python/chat_history", "把每次对话归入同一客户档案", "学习 thread、message 与会话历史的基本组织。"),
        ("上下文模板", "examples/python/context-templates-example", "把档案摘要整理成给助手看的简报", "理解 Context Block 注入和自定义上下文格式。"),
        ("图谱检索", "examples/python/graph_example", "从一条线索顺着关系网找答案", "学习节点、边、事实和图搜索的基础。"),
        ("默认 Ontology", "ontology/default_ontology.py", "规定档案标签和关系词典", "阅读 User、Preference、Event 等实体及关系约束。"),
        ("可视化知识图", "examples/typescript/zep-graph-visualization", "把档案关系画成可浏览地图", "理解图数据从 API 到前端呈现的链路。"),
        ("文档切分和摄取", "examples/typescript/chunking-example", "先把一本书拆成可索引卡片", "学习文档 chunk 与后续图谱/记忆检索的关系。"),
        ("完整 Agent Memory Demo", "examples/python/agent-memory-full-example", "交付一个带长期记忆的聊天助手", "阅读 Streamlit、上下文检索、流式回答和延迟对比。"),
        ("LangGraph 集成", "integrations/langgraph/python", "把记忆节点插入 Agent 状态图", "理解框架的 memory/context 扩展点。"),
        ("Mastra 自动记忆", "integrations/mastra/typescript", "在模型调用前后自动查档和归档", "学习 ZepInputProcessor 与 ZepOutputProcessor。"),
        ("工具式记忆访问", "integrations/mastra/typescript", "让员工决定何时翻档案", "理解 zepRemember、zepSearch 与自动处理器的取舍。"),
        ("MCP 服务入口", "mcp/zep-mcp-server/cmd", "为外部 AI 助手开一个只读查询窗口", "从 Go 程序入口理解 MCP Server 的启动。"),
        ("MCP 查询处理", "mcp/zep-mcp-server/internal/handlers", "前台把查询单转给图谱档案员", "阅读 search_graph、get_user_context 等只读工具。"),
        ("评测流水线", "zep-eval-harness", "批量验收档案检索是否真正答对问题", "串联用户摄取、文档切分、图谱写入、搜索、生成与评分。"),
        ("检查图谱与结果", "zep-eval-harness/zep_graph_inspect.py", "打开档案馆盘点实体和关系", "学习如何检查节点、边与评测前提。"),
        ("基准测试视角", "benchmarks", "用标准考试比较档案管理员能力", "了解 LoCoMo 与 LongMemEval 在记忆系统中的用途。"),
        ("Legacy 架构辨析", "legacy/src", "参观已停用的旧档案馆", "只阅读旧 Go Community Edition；新项目应采用 Cloud SDK。"),
    ], [("示例应用", ["聊天", "图谱", "用户"]), ("框架连接", ["Mastra", "LangGraph", "ADK"]),
        ("记忆访问", ["SDK", "Context", "图搜索"]), ("工具评测", ["MCP", "Eval", "Benchmark"]),
        ("数据建模", ["Ontology", "时态知识图谱"])],
       (("明确仓库边界", 1, 3, "仓库边界与最小 Cloud API"),
        ("用户、线程与上下文", 4, 6, "用户、线程、消息与上下文"),
        ("图谱与 Ontology", 7, 10, "图谱检索、ontology 与可视化"),
        ("Agent 示例与集成", 11, 14, "完整 Agent 示例与框架集成"),
        ("MCP 与评测闭环", 15, 17, "MCP 服务和评测闭环"),
        ("基准与 Legacy 辨析", 18, 20, "基准、跨语言与 legacy 架构辨析"))),
]


def shell_command(proj: dict, focus: str) -> str:
    return f"""# AI_WORK 中的真实项目根目录
cd {AI_WORK}/{proj["repo"]}
# 先确认本课焦点存在；路径都相对项目根目录
ls {focus}
"""


def nav_script() -> str:
    return """<script>document.addEventListener('DOMContentLoaded',()=>{if(window.hljs)hljs.highlightAll();const b=document.getElementById('sidebarToggle'),s=document.getElementById('sidebar');if(b&&s)b.onclick=()=>s.classList.toggle('open');const links=document.querySelectorAll('[data-section]'),sections=document.querySelectorAll('section[id]');const ob=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)links.forEach(a=>a.classList.toggle('active',a.dataset.section===e.target.id))}),{rootMargin:'-25% 0px -65% 0px'});sections.forEach(x=>ob.observe(x));});</script>"""


def render_hub(proj: dict) -> str:
    c1, c2 = proj["colors"]
    layers = "".join(
        f'<div class="arch-row" style="--lc:{c1 if i % 2 == 0 else c2};--d:{i*.55}s"><div class="lbl">L{len(proj["layers"])-i} · {esc(name)}</div><div class="boxes">'
        + "".join(f'<div class="b"><strong>{esc(item)}</strong>本层职责</div>' for item in items) + "</div></div>"
        for i, (name, items) in enumerate(proj["layers"])
    )
    stage_html = ""
    for stage in proj["stages"]:
        cards = "".join(
            f'<a class="day-card" href="{proj["prefix"]}-day{d:02}.html"><div class="top"><div class="num" style="background:{stage["grad"]}">{d:02}</div><h3>{esc(proj["days"][d-1]["title"])}</h3></div><p><code>{esc(proj["days"][d-1]["focus"])}</code>：{esc(proj["days"][d-1]["blurb"])}</p><div class="foot"><span class="mins">≈30 min · 6 讲</span><span class="go">开始学 →</span></div></a>'
            for d in range(stage["lo"], stage["hi"] + 1)
        )
        stage_html += f'<div class="week-bar" id="stage{stage["id"]}"><div class="wk" style="background:{stage["grad"]}">S{stage["id"]}</div><h2>阶段 {stage["id"]} · {esc(stage["name"])}</h2><span>D{stage["lo"]:02}-D{stage["hi"]:02} · {esc(stage["blurb"])}</span></div><div class="day-grid">{cards}</div>'
    stage_nav = "".join(f'<li><a href="#stage{s["id"]}" class="nav-link">阶段 {s["id"]} · {esc(s["name"])}（D{s["lo"]:02}-D{s["hi"]:02}）</a></li>' for s in proj["stages"])
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(proj["title"])} 源码学习 · 20 天总目录</title><link rel="stylesheet" href="style.css"><style>:root{{--c1:{c1};--c2:{c2}}}{COMMON_CSS}</style></head><body>
<nav class="sidebar" id="sidebar"><div class="sidebar-header"><div class="logo" style="background:linear-gradient(135deg,{c1},{c2})">{esc(proj["logo"])}</div><h2>{esc(proj["title"])}</h2><p class="version">{esc(proj["lang_stack"])} · 20 天源码学习</p></div><ul class="nav-list"><li class="nav-group-title">总目录</li><li><a href="#intro" class="nav-link active">开篇 · 这是什么</a></li><li><a href="#arch" class="nav-link">架构全景（动图）</a></li><li><a href="#how" class="nav-link">怎么使用教程</a></li><li class="nav-group-title">6 阶段 · 20 天</li>{stage_nav}<li class="nav-group-title">导航</li><li><a href="index.html" class="nav-link" style="color:var(--accent-cyan)">← 返回博客首页</a></li></ul></nav><button class="sidebar-toggle" id="sidebarToggle">☰</button>
<main class="content" id="content"><div class="part-header"><span class="part-label">源码深度学习 · 零基础友好 · 20 天</span><h1 class="part-title">{esc(proj["title"])} 源码学习</h1><p class="part-desc"><strong>{esc(proj["one_liner"])}</strong>。这不是 API 速查表，而是一条可以重复走的源码路线：每天用 30 分钟，从一个真实相对路径出发，先用类比建立直觉，再把它接回整条运行链路。</p></div>
<section id="intro" class="section"><div class="section-header"><span class="section-number">00</span><h1>开篇 · 这是个什么项目</h1></div><div class="card"><p><strong>{esc(proj["title"])}</strong> 可以先想成一间<strong>{esc(proj["analogy"])}</strong>。它的代码不是一堆孤立文件：入口接到需求，核心对象做判断，工具或模型完成工作，状态把结果交给下一个环节。</p><div class="essence"><span class="t">💡 20 天的主线</span>先找入口和地图，再跟一次真实任务穿过核心循环；随后研究状态、模型、工具与扩展；最后用复盘把全部概念连成一张可迁移的地图。不要背目录名，要不断问「谁创建它、它把什么交给谁」。</div><div class="baby"><span class="t">大白话</span>读源码像参观工厂：第一天先看门牌和楼层，不急着拆机器。后面每节课只打开一个焦点路径，但始终知道它属于哪层、服务哪个业务动作。</div></div></section>
<section id="arch" class="section"><div class="section-header"><span class="section-number">01</span><h1>架构全景（动起来看）</h1></div><div class="card"><p>发光扫过的每一层都是一次任务可能经过的站点。不同仓库命名不同，但「接入 → 编排 → 核心能力 → 资源」的责任边界很相似。</p><div class="arch-anim">{layers}</div><div class="loopd"><span class="n"><b>输入</b>用户任务</span><span class="a">→</span><span class="n"><b>组织</b>对象 / 流程</span><span class="a">→</span><span class="n"><b>执行</b>模型 / 工具</span><span class="a">→</span><span class="n"><b>沉淀</b>状态 / 记忆</span></div><div class="tradeoff"><span class="t">设计取舍</span>分层会增加跳转文件的次数，却让每层只承担一种职责：入口容易替换，核心逻辑能测试，模型与外部工具可插拔。读代码时先沿箭头追「数据」而不是追每一个类。</div></div></section>
<section id="how" class="section"><div class="section-header"><span class="section-number">02</span><h1>怎么使用这份教程</h1></div><div class="feature-grid"><div class="feature-item"><div class="feature-icon">⏱️</div><h4>每天 30 分钟</h4><p>6 讲，每讲先问问题，再给本质和大白话。</p></div><div class="feature-item"><div class="feature-icon">📍</div><h4>真实相对路径</h4><p>所有路径都从项目根目录算，不把你的机器路径写进源码引用。</p></div><div class="feature-item"><div class="feature-icon">🧪</div><h4>先验证再推理</h4><p>每页都有可复制 bash 命令；文件版本变化时以本地实际内容为准。</p></div><div class="feature-item"><div class="feature-icon">🧭</div><h4>可迁移方法</h4><p>学会从入口、数据结构、循环和扩展点读任何 AI 项目。</p></div></div></section>{stage_html}</main>{nav_script()}</body></html>"""


def build_lessons(proj: dict, day: int) -> str:
    info = proj["days"][day - 1]
    focus = esc(info["focus"])
    prev_focus = esc(proj["days"][day - 2]["focus"]) if day > 1 else "项目根目录"
    next_focus = esc(proj["days"][day]["focus"]) if day < 20 else "20 天知识地图"
    labels = (
        ("先问问题", f"为什么今天不是直接背 <code>{focus}</code> 的所有实现？因为它只是 {esc(proj['title'])} 这条链路中的一个站点。先定位它接收什么、产出什么，细节才不会变成孤岛。"),
        ("找到入口", f"从 <span class=\"fileref\">{focus}</span> 打开后，先看导入、公开类或函数和构造参数。它们像岗位说明书：告诉你这个模块需要哪些前置条件，也暴露它依赖的邻居。"),
        ("跟数据走", f"把输入写成一句话：任务从 <code>{prev_focus}</code> 或调用方来到这里，被转换、校验或包装后，再交给下一站。源码阅读最可靠的导航不是文件树，而是参数、返回值和事件。"),
        ("看协作边界", f"今天的焦点属于「{esc(info['title'])}」。把它当作 {esc(info['analogy'])}：它不必独自做完所有事，而是把专业工作交给模型、工具、存储或下一位对象。"),
        ("辨析取舍", f"当逻辑被拆到多个对象时，初看要跳很多文件；换来的好处是可替换、可测试和可观测。遇到抽象层先不要嫌绕，问它隔离了哪一种变化：模型、工具、状态还是流程。"),
        ("动手复盘", f"用命令确认 <code>{focus}</code> 的真实存在和周边文件，再回到本页画三格图：输入 → {esc(info['title'])} → 输出。明天会从 <code>{next_focus}</code> 接着走，今天留下的问题正好成为明天的入口。"),
    )
    rendered = []
    for n, (heading, text) in enumerate(labels, 1):
        kind = ("ask", "essence", "baby")[((n - 1) % 3)]
        title = ("🤔 问题", "💡 本质", "👶 大白话")[((n - 1) % 3)]
        extra = ""
        if n == 2:
            extra = f'<div class="walk"><div class="r"><code>{focus}</code><span>今天的主焦点：先观察命名、导入与主要入口。</span></div><div class="r"><code>调用方</code><span>用编辑器的引用跳转，确认谁把数据送进来。</span></div><div class="r"><code>下游</code><span>沿返回值、await、事件或方法调用找到它交棒的位置。</span></div></div>'
        elif n == 3:
            extra = f'<div class="svgbox"><svg viewBox="0 0 650 120" width="100%" style="min-width:520px"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="{proj["colors"][0]}"/><stop offset="1" stop-color="{proj["colors"][1]}"/></linearGradient></defs><rect x="20" y="35" width="160" height="48" rx="10" fill="none" stroke="url(#g)"/><text x="100" y="64" text-anchor="middle" fill="#cbd5e1" font-size="14">调用方 / 输入</text><path d="M185 59h75" stroke="#94a3b8" marker-end="url(#x)"/><rect x="265" y="35" width="160" height="48" rx="10" fill="url(#g)" opacity=".75"/><text x="345" y="64" text-anchor="middle" fill="white" font-size="14">{esc(info["title"])}</text><path d="M430 59h75" stroke="#94a3b8"/><rect x="510" y="35" width="120" height="48" rx="10" fill="none" stroke="#22c55e"/><text x="570" y="64" text-anchor="middle" fill="#bbf7d0" font-size="14">结果 / 状态</text></svg><div class="cap">动画心智图：先追一条数据的去向，再扩展到异常分支。</div></div>'
        elif n == 5:
            extra = '<div class="qa"><span class="t">Q&A</span><p><strong>Q：看不懂某个函数要停多久？</strong><br> A：先记下输入、输出、调用位置，跳过内部细节；等主链路第二次经过它时再回来。源码学习不是一次读完，是不断缩小未知区域。</p></div>'
        elif n == 6:
            extra = f'<pre><code class="language-bash">{esc(shell_command(proj, info["focus"]))}</code></pre><div class="pitfall"><span class="t">常见卡点</span>AI_WORK 的仓库版本可能与文章调研时不同。如果路径改名，先在项目根目录使用 <code>rg --files | rg "关键词"</code> 查找，而不是把绝对路径复制进笔记。</div>'
        rendered.append(f'<section id="l{n:02}" class="section"><div class="section-header"><span class="section-number">L{n:02}</span><h1>{heading} · {esc(info["title"])}</h1></div><div class="card"><div class="{kind}"><span class="t">{title}</span>{text}</div>{extra}</div></section>')
    return "".join(rendered)


def render_day(proj: dict, day: int) -> str:
    info, (c1, c2) = proj["days"][day - 1], proj["colors"]
    stages = " → ".join(f"D{s['lo']:02}-D{s['hi']:02} {s['name']}" for s in proj["stages"])
    lecture_nav = "".join(f'<li><a href="#l{i:02}" class="nav-link{" active" if i == 1 else ""}" data-section="l{i:02}">L{i:02} · {label}</a></li>' for i, label in enumerate(("先问问题", "找到入口", "跟数据走", "看协作边界", "辨析取舍", "动手复盘"), 1))
    prev_link = f'<li><a href="{proj["prefix"]}-day{day-1:02}.html" class="nav-link" style="color:var(--accent-cyan)">← Day {day-1:02}</a></li>' if day > 1 else ""
    next_link = f'<li><a href="{proj["prefix"]}-day{day+1:02}.html" class="nav-link" style="color:var(--accent-green)">Day {day+1:02} →</a></li>' if day < 20 else f'<li><a href="{proj["prefix"]}-tutorial.html" class="nav-link" style="color:var(--accent-green)">收官 · 返回总目录 →</a></li>'
    steps = "".join(f'<span class="st{" on" if d == day else ""}">D{d:02} {esc(proj["days"][d-1]["title"])}</span>{"" if d == 20 else "<span class=sep>→</span>"}' for d in range(max(1, day - 2), min(20, day + 2) + 1))
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Day {day:02} · {esc(info["title"])} — {esc(proj["title"])} 20 天源码学习</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css"><script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script><style>:root{{--c1:{c1};--c2:{c2}}}{COMMON_CSS}</style></head><body>
<nav class="sidebar" id="sidebar"><div class="sidebar-header"><div class="logo" style="background:linear-gradient(135deg,{c1},{c2})">{day:02}</div><h2>Day {day:02}</h2><p class="version">{esc(info["title"])} · 6 讲</p></div><ul class="nav-list"><li class="nav-group-title">本日 6 讲</li>{lecture_nav}<li class="nav-group-title">导航</li>{prev_link}<li><a href="{proj["prefix"]}-tutorial.html" class="nav-link">20 天总目录</a></li>{next_link}</ul></nav><button class="sidebar-toggle" id="sidebarToggle">☰</button>
<main class="content" id="content"><div class="part-header"><span class="part-label">Day {day:02} / 共 20 天 · {esc(next(s["name"] for s in proj["stages"] if s["lo"] <= day <= s["hi"]))}</span><h1 class="part-title">{esc(info["title"])}：从 <code>{esc(info["focus"])}</code> 读出一段工作流</h1><p class="part-desc">{esc(info["blurb"])}。今天不追求把每行代码翻译成中文；目标是建立可验证的因果链：<strong>谁调用它、它如何处理输入、状态留下在哪里、它下一步交给谁。</strong></p></div><div class="journey"><div class="jt">📍 20 天路线 · {esc(stages)}</div><div class="steps">{steps}</div></div><div class="essence"><span class="t">💡 今日类比</span><strong>{esc(info["analogy"])}</strong>。先用这个类比理解职责，再回到真实路径 <span class="fileref">{esc(info["focus"])}</span> 校正它；类比帮你记住结构，源码负责告诉你边界。</div>{build_lessons(proj, day)}</main>{nav_script()}</body></html>"""


def render_langchain_day20() -> str:
    """Final LangChain day: map core / classic / partners to LangGraph & LangSmith."""
    rows = [
        ("项目全景", "libs/core", "积木箱说明书", "占位"),
        ("环境搭建", "libs/core", "占位", "占位"),
        ("Runnable", "libs/core/langchain_core/runnables", "占位", "占位"),
        ("invoke 旅程", "libs/core/langchain_core/runnables", "占位", "占位"),
        ("ChatModel", "libs/core/langchain_core/language_models", "占位", "占位"),
        ("消息体系", "libs/core/langchain_core/messages", "占位", "占位"),
        ("Prompt", "libs/core/langchain_core/prompts", "占位", "占位"),
        ("输出解析", "libs/core/langchain_core/output_parsers", "占位", "占位"),
        ("Document", "libs/core/langchain_core/documents", "占位", "占位"),
        ("文本切分", "libs/text-splitters", "占位", "占位"),
        ("Embeddings", "libs/core/langchain_core/embeddings", "占位", "占位"),
        ("Retriever", "libs/core/langchain_core/retrievers", "占位", "占位"),
        ("Tool", "libs/core/langchain_core/tools", "占位", "占位"),
        ("工具闭环", "libs/core/langchain_core/tools", "占位", "占位"),
        ("Agent", "libs/langchain_v1", "占位", "占位"),
        ("记忆", "libs/core/langchain_core/runnables", "占位", "占位"),
        ("回调与流式", "libs/core/langchain_core/callbacks", "占位", "占位"),
        ("LCEL 高级", "libs/core/langchain_core/runnables", "占位", "占位"),
        ("追踪", "libs/core/langchain_core/tracers", "占位", "占位"),
        ("收官·知识地图串讲", "libs/core/langchain_core",
         "把 20 天积木装回一只工具箱",
         "把 core / classic / partners 与 LangGraph、LangSmith 的边界串回一条可继续学习的路线。"),
    ]
    proj = project(
        "langchain", "langchain", "LangChain",
        "把模型、数据、工具与运行链组合成可调用应用",
        "AI 应用积木箱", ("#1c3c3c", "#2f6feb"), "LC", "Python", rows,
        [("生态", ["core", "classic", "partners"]), ("运行时", ["runnables", "messages", "prompts"]),
         ("能力", ["retrievers", "tools", "agents"]), ("工程", ["callbacks", "tracers", "stores"])],
    )
    return render_day(proj, 20)


def card_html(proj: dict) -> str:
    c1, c2 = proj["colors"]
    return f'''            <a class="blog-card" href="{proj["prefix"]}-tutorial.html" data-ps="{proj["prefix"]}" data-pd="20">
                <div class="blog-card-icon" style="background:linear-gradient(135deg,{c1},{c2});">{esc(proj["logo"])}</div>
                <h3>{esc(proj["title"])} 源码学习（20 天）</h3>
                <p class="blog-desc">{esc(proj["one_liner"])}</p>
                <div class="blog-card-tags"><span class="blog-tag">{esc(proj["lang_stack"])}</span><span class="blog-tag">20 天</span></div>
                <div class="blog-card-arrow">查看教程 &rarr;</div>
            </a>'''


def patch_index() -> bool:
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    if 'data-ps="metagpt"' in text:
        return False
    marker = '            <a class="blog-card" href="gov-agents-tutorial.html"'
    if marker not in text:
        raise RuntimeError("index.html 中找不到 gov-agents 插入锚点")
    text = text.replace(marker, "\n".join(card_html(p) for p in PROJECTS) + "\n" + marker, 1)
    index.write_text(text, encoding="utf-8")
    return True


def patch_langchain_hub() -> bool:
    """Mark the existing Day 20 card ready without rewriting its hand-authored hub."""
    hub = ROOT / "langchain-tutorial.html"
    text = hub.read_text(encoding="utf-8")
    old = '<span class="mins">≈30 min</span><span class="go">敬请期待</span></div>'
    anchor = 'href="langchain-day20.html"'
    start = text.find(anchor)
    if start < 0:
        raise RuntimeError("langchain-tutorial.html 中找不到 Day 20 卡片")
    end = text.find("</a>", start)
    card = text[start:end]
    if "开始学" in card:
        return False
    if old not in card:
        raise RuntimeError("LangChain Day 20 卡片格式已变化，未安全更新")
    text = text[:start] + card.replace(old, '<span class="mins">≈30 min · 已就绪</span><span class="go">开始学 →</span></div>') + text[end:]
    hub.write_text(text, encoding="utf-8")
    return True


def generate(include_langchain_day20: bool = True) -> dict[str, int]:
    counts = {}
    for proj in PROJECTS:
        (ROOT / f'{proj["prefix"]}-tutorial.html').write_text(render_hub(proj), encoding="utf-8")
        for day in range(1, 21):
            (ROOT / f'{proj["prefix"]}-day{day:02}.html').write_text(render_day(proj, day), encoding="utf-8")
        counts[proj["prefix"]] = 21
    if include_langchain_day20:
        (ROOT / "langchain-day20.html").write_text(render_langchain_day20(), encoding="utf-8")
        counts["langchain-day20"] = 1
    counts["index"] = 1 if patch_index() else 0
    counts["langchain-hub"] = 1 if patch_langchain_hub() else 0
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--langchain-day20", action="store_true", help="保留兼容参数；Day20 默认也生成")
    args = parser.parse_args()
    # Kept as an opt-in flag for callers, while the requested default is on.
    counts = generate(include_langchain_day20=True)
    print("Generated:", ", ".join(f"{name}={count}" for name, count in counts.items()))
    print(f"Total HTML written: {sum(counts.values())}")


if __name__ == "__main__":
    main()
