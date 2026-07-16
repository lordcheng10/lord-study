#!/usr/bin/env python3
"""Annotate Coze practice screenshots with red boxes + labels; enrich HTML goals/why."""
from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "coze-practice"

# boxes listed in click/edit ORDER → rendered as 1, 2, 3...
# each: (x1,y1,x2,y2, label) in 1440x900 design coords
ANNOTATIONS: dict[str, list[tuple[int, int, int, int, str]]] = {
    # P00
    "00-setup/01-login.png": [
        (520, 280, 920, 400, "输入邮箱"),
        (520, 400, 920, 470, "输入密码"),
        (560, 480, 880, 540, "点「登录」"),
    ],
    "00-setup/02-develop.png": [
        (55, 95, 250, 145, "确认侧栏在「项目开发」"),
        (1280, 70, 1410, 115, "点「+ 创建」"),
    ],
    "00-setup/10-develop-home.png": [
        (55, 95, 250, 145, "确认侧栏在「项目开发」"),
        (1280, 70, 1410, 115, "点「+ 创建」"),
    ],
    "00-setup/11-create-modal.png": [
        (380, 260, 700, 620, "第2课：选「创建智能体」"),
        (740, 260, 1060, 620, "第5课：选「创建应用」"),
    ],
    "00-setup/03-model-admin.png": [(200, 80, 1400, 820, "在列表确认模型为「启用」")],
    "00-setup/12-admin-home.png": [(40, 80, 280, 400, "左侧点「模型管理」")],
    "00-setup/13-model-list.png": [(280, 80, 1400, 820, "确认至少一条「启用」")],
    "00-setup/05-add-claude-form.png": [
        (400, 120, 1040, 280, "填显示名称 / Model"),
        (400, 280, 1040, 480, "填 API Key"),
        (400, 700, 1040, 780, "点保存"),
    ],
    "00-setup/04-model-detail-or-add.png": [(400, 100, 1100, 800, "填写并保存模型")],
    # P02
    "02-agent/01-create-modal.png": [(380, 260, 700, 620, "选「创建智能体」")],
    "02-agent/13-create-agent-form.png": [(480, 300, 960, 520, "填写智能体名称")],
    "02-agent/14-create-agent-filled.png": [
        (480, 300, 960, 450, "确认名称无误"),
        (700, 480, 900, 560, "点确认"),
    ],
    "02-agent/15-new-agent-ide.png": [
        (40, 120, 480, 860, "左栏：人设（下一步粘贴）"),
        (480, 120, 900, 860, "中栏：技能 / 对话体验"),
        (900, 120, 1420, 860, "右栏：预览与调试"),
    ],
    "02-agent/20-ide-full.png": [
        (700, 55, 900, 100, "选已启用模型"),
        (40, 120, 480, 860, "粘贴人设到这里"),
        (480, 120, 900, 400, "认识技能区（后课再用）"),
        (900, 120, 1420, 860, "在此预览调试"),
        (1300, 50, 1410, 100, "发布（本课可后做）"),
    ],
    "02-agent/21-persona.png": [(40, 120, 520, 860, "人设区：全选后粘贴")],
    "02-agent/11-persona-area.png": [(40, 120, 520, 860, "人设与回复逻辑")],
    "02-agent/22-preview.png": [
        (900, 120, 1420, 750, "查看回复区"),
        (920, 780, 1400, 870, "输入测试句并发送"),
    ],
    "02-agent/12-preview-panel.png": [(900, 120, 1420, 860, "预览与调试面板")],
    "02-agent/16-preview-input.png": [(920, 780, 1400, 870, "输入框发送测试句")],
    "02-agent/17-preview-reply.png": [(920, 150, 1400, 700, "检查回复是否符合人设")],
    "02-agent/10-ide-overview.png": [
        (40, 120, 480, 860, "左：人设"),
        (480, 120, 900, 860, "中：技能"),
        (900, 120, 1420, 860, "右：预览"),
    ],
    "02-agent/04-agent-skills-area.png": [(480, 120, 900, 500, "技能区：插件 / 工作流 / 知识")],
    # P03
    "03-skills/10-skills-area.png": [
        (480, 140, 900, 260, "插件入口"),
        (480, 260, 900, 380, "工作流入口（推荐挂）"),
        (480, 380, 900, 500, "知识库入口"),
    ],
    "03-skills/11-plugin-panel.png": [
        (500, 150, 1100, 650, "勾选要添加的插件"),
        (900, 680, 1080, 750, "确认添加"),
    ],
    # P04
    "04-knowledge/01-library.png": [
        (55, 145, 250, 195, "侧栏点「资源库」"),
        (1280, 70, 1410, 115, "点「+ 创建」"),
    ],
    "04-knowledge/10-library.png": [
        (55, 145, 250, 195, "侧栏点「资源库」"),
        (1280, 70, 1410, 115, "点「+ 创建」"),
    ],
    "04-knowledge/02-create-menu.png": [(1100, 100, 1380, 420, "菜单选「知识库」")],
    "04-knowledge/11-create-menu.png": [(1100, 100, 1380, 420, "菜单选「知识库」")],
    "04-knowledge/03-create-knowledge-dialog.png": [
        (420, 180, 1020, 420, "填名称 / 选文本与本地文档"),
        (700, 620, 980, 700, "点「创建并导入」"),
    ],
    "04-knowledge/03b-pick-type.png": [(420, 200, 1020, 650, "选择知识库类型")],
    "04-knowledge/04-knowledge-form-filled.png": [
        (420, 180, 1020, 520, "核对已填字段"),
        (700, 620, 980, 700, "点「创建并导入」"),
    ],
    "04-knowledge/05-after-create.png": [(200, 100, 1240, 800, "进入上传向导")],
    "04-knowledge/05-knowledge-page.png": [(200, 100, 1240, 800, "知识库详情/上传页")],
    "04-knowledge/06-upload-file.png": [(300, 200, 1140, 700, "上传本地 MD 文件")],
    "04-knowledge/07-upload-processing.png": [(300, 200, 1140, 700, "等待处理完成")],
    "03-library/01-library.png": [
        (55, 145, 250, 195, "侧栏「资源库」"),
        (1280, 70, 1410, 115, "点「+ 创建」"),
    ],
    "03-library/02-create-resource.png": [(1100, 100, 1380, 450, "在菜单中选择资源类型")],
    # P05
    "05-plugin/01-explore-plugin.png": [(200, 80, 1400, 850, "点插件卡片查看/添加")],
    "05-plugin/10-explore.png": [
        (40, 80, 200, 200, "侧栏点「探索」"),
        (200, 80, 1400, 850, "进入插件等内容区"),
    ],
    "05-plugin/11-plugin-list.png": [(200, 80, 1400, 850, "点卡片安装插件")],
    "09-explore/01-explore.png": [(40, 80, 200, 200, "探索入口")],
    # P06
    "06-database/10-library.png": [
        (55, 145, 250, 195, "侧栏「资源库」"),
        (1280, 70, 1410, 115, "点「+ 创建」"),
    ],
    "06-database/11-create-menu.png": [(1100, 100, 1380, 480, "菜单选「数据库」")],
    # P07
    "07-project/01-project-ide.png": [
        (40, 80, 320, 860, "左侧资源树找工作流"),
        (320, 80, 1420, 860, "中间编辑当前资源"),
        (1280, 40, 1410, 95, "需要时点「发布」"),
    ],
    "07-project/10-ide.png": [
        (40, 80, 320, 860, "资源树：新建/打开工作流"),
        (320, 80, 1420, 860, "编辑区"),
    ],
    "07-project/02-workflow.png": [(200, 80, 1400, 850, "在画布上编排节点")],
    # P01
    "01-competitor-daily/01-login.png": [(520, 280, 920, 520, "先登录")],
    "01-competitor-daily/02-develop.png": [
        (280, 160, 560, 360, "打开应用「竞品日报实战」"),
        (1280, 70, 1410, 115, "或点「+ 创建」新建应用"),
    ],
    "01-competitor-daily/05-workflow-canvas.png": [(80, 80, 1360, 820, "按 开始→LLM→Code→HTTP→结束 配置")],
    "01-competitor-daily/10-canvas.png": [(80, 80, 1360, 820, "按节点顺序依次配置")],
    "01-competitor-daily/11-from-project.png": [(40, 80, 320, 400, "左侧点开工作流")],
    "01-competitor-daily/06-testrun.png": [
        (1000, 120, 1420, 400, "填写 report_date"),
        (1000, 400, 1420, 600, "填写 lark_hint"),
        (1100, 780, 1380, 860, "点试运行/开始"),
    ],
    # P08
    "08-publish/10-agent-publish.png": [
        (400, 100, 1100, 550, "勾选 API / Chat SDK"),
        (700, 700, 1000, 800, "点「发布」"),
    ],
    "08-publish/11-app-publish.png": [
        (400, 100, 1100, 550, "勾选发布渠道"),
        (700, 700, 1000, 800, "点「发布」"),
    ],
    "08-publish/20-publish-panel.png": [
        (400, 80, 1100, 550, "勾选 API + Chat SDK"),
        (700, 700, 1000, 800, "确认发布"),
    ],
    "08-publish/12-avatar-menu.png": [(1100, 40, 1420, 320, "点头像 → 进设置")],
    "08-publish/21-avatar-menu.png": [(1100, 40, 1420, 320, "点头像 → 进设置")],
    "08-publish/16-account-settings.png": [(40, 80, 320, 500, "左侧点「API 授权」")],
    "08-publish/17-api-auth-tab.png": [
        (320, 80, 1400, 400, "点「添加新令牌」"),
        (320, 400, 1400, 820, "复制 PAT（只显示一次）"),
    ],
    "08-publish/14-workflow-url-id.png": [(200, 20, 1400, 80, "抄地址栏末段 = workflow_id")],
    "08-publish/15-api-configure.png": [(320, 80, 1400, 820, "完成 API / 令牌配置")],
    "08-publish/24-settings-page.png": [(40, 80, 1400, 820, "在设置里找「API 授权」")],
    "08-publish/25-top-menu.png": [(1100, 40, 1420, 320, "打开右上角菜单")],
    "08-publish/03-agent-publish.png": [(400, 100, 1100, 800, "发布智能体")],
    "08-publish/04-app-publish.png": [(400, 100, 1100, 800, "发布应用")],
    "08-publish/01-account-menu.png": [(1100, 40, 1420, 320, "打开账号菜单")],
    "08-publish/13-settings-fallback.png": [(40, 80, 1400, 820, "进入设置")],
    # P09
    "09-chatflow/10-explore.png": [(40, 80, 200, 200, "探索 / 开放能力入口")],
}

def font(size: int):
    for fp in [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            continue
    return ImageFont.load_default()


def annotate(src: Path, boxes: list[tuple[int, int, int, int, str]], dst: Path) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    # scale from 1440x900 design coords
    sx, sy = w / 1440.0, h / 900.0
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    scale = min(sx, sy)
    f = font(max(16, int(18 * scale)))
    f_num = font(max(20, int(26 * scale)))
    f_small = font(max(14, int(16 * scale)))
    badge_r = max(16, int(22 * scale))
    stroke = max(3, int(4 * scale))

    for i, (x1, y1, x2, y2, label) in enumerate(boxes, start=1):
        a = (int(x1 * sx), int(y1 * sy), int(x2 * sx), int(y2 * sy))
        # red box
        draw.rectangle(a, outline=(239, 68, 68, 255), width=stroke, fill=(239, 68, 68, 28))

        # numbered badge at top-left of box
        cx = a[0] + badge_r + 2
        cy = a[1] + badge_r + 2
        if cy - badge_r < 2:
            cy = badge_r + 4
        if cx - badge_r < 2:
            cx = badge_r + 4
        draw.ellipse(
            (cx - badge_r, cy - badge_r, cx + badge_r, cy + badge_r),
            fill=(239, 68, 68, 255),
            outline=(255, 255, 255, 255),
            width=max(2, stroke - 1),
        )
        num = str(i)
        # center number in circle
        bbox = draw.textbbox((0, 0), num, font=f_num)
        nw, nh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - nw / 2, cy - nh / 2 - 2), num, fill=(255, 255, 255, 255), font=f_num)

        # caption: "1 · 文案"
        caption = f"{i} · {label}"
        tw = draw.textlength(caption, font=f) if hasattr(draw, "textlength") else len(caption) * 11
        pad = 8
        ly1 = max(4, a[1] - int(34 * scale))
        if ly1 < cy + badge_r + 4 and a[1] > 50:
            ly1 = min(h - 40, a[1] + 6)
        lx1 = min(a[0] + badge_r * 2 + 6, w - int(tw) - 20)
        lx2 = min(w - 4, int(lx1 + tw + pad * 2))
        ly2 = ly1 + int(30 * scale)
        draw.rectangle((lx1, ly1, lx2, ly2), fill=(239, 68, 68, 235))
        draw.text((lx1 + pad, ly1 + 5), caption, fill=(255, 255, 255, 255), font=f)

    # bottom banner
    banner_h = max(38, int(44 * sy))
    draw.rectangle((0, h - banner_h, w, h), fill=(15, 23, 42, 220))
    draw.text(
        (14, h - banner_h + 12),
        "数字 1 → 2 → 3 … = 操作顺序 · 请按编号依次点击/填写",
        fill=(248, 250, 252, 255),
        font=f_small,
    )

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG", optimize=True)
    print("marked", dst.relative_to(ROOT))


def mark_all() -> dict[str, str]:
    """Returns map original_rel -> marked_rel (posix). Only regenerate images."""
    mapping = {}
    for rel, boxes in ANNOTATIONS.items():
        src = ASSETS / rel
        if not src.exists():
            print("skip missing", rel)
            continue
        dst = src.with_name(src.stem + ".marked" + src.suffix)
        annotate(src, boxes, dst)
        mapping[f"assets/coze-practice/{rel}"] = (
            f"assets/coze-practice/{Path(rel).with_name(Path(rel).stem + '.marked' + Path(rel).suffix).as_posix()}"
        )
    return mapping


LESSON_GOALS = {
    "coze-studio-practice-00-setup.html": (
        "第1课目标",
        "把本地 Coze Studio 跑起来、用邮箱登录成功，并在管理后台<strong>至少启用 1 个大模型</strong>。"
        "本课不过这一关，后面智能体调试、工作流 LLM 节点都会失败（Tokens=0 / 报错）。",
    ),
    "coze-studio-practice-02-agent.html": (
        "第2课目标",
        "从零创建一个「竞品分析」智能体：写好人设与开场白，并在右侧<strong>预览与调试</strong>里拿到符合角色的回复。"
        "这是后续挂知识库、挂技能的统一入口。",
    ),
    "coze-studio-practice-04-knowledge.html": (
        "第3课目标",
        "创建文本知识库、上传样例 Markdown，挂到 P02 智能体上，并用库内暗号 <code>BM-INTEL-2026</code> 提问验证真正命中 RAG（不是模型瞎编）。",
    ),
    "coze-studio-practice-05-plugin.html": (
        "第4课目标",
        "走通「探索官方插件 / 鉴权意识 / 自定义 HTTP 插件」路径，至少完成一种可在智能体里引用的插件能力（官方授权或 httpbin 自定义兜底）。",
    ),
    "coze-studio-practice-07-project.html": (
        "第5课目标",
        "创建应用「竞品日报实战」，认识应用 IDE 的资源树与工作流入口，新建英文名工作流空壳，为下一课编排五节点流水线做准备。",
    ),
    "coze-studio-practice-01-competitor-daily.html": (
        "第6课目标（核心）",
        "在应用内把工作流 <code>daily_competitor_report</code> 编成 "
        "<strong>开始 → LLM → Code(json.dumps) → HTTP(RAW_TEXT) → 结束</strong>，"
        "试运行成功（演示可用 httpbin），并理解飞书 400/19001 为何必须用 Code 转义。",
    ),
    "coze-studio-practice-03-agent-skills.html": (
        "第7课目标",
        "在智能体技能区至少挂载一项能力（推荐：P01 工作流），用人设约束调用时机，并在预览里用明确指令触发，看到调用痕迹。",
    ),
    "coze-studio-practice-06-database.html": (
        "第8课目标",
        "在资源库建表 <code>competitor_campaigns</code>，用工作流 Database 节点完成「插入 + 查询」闭环，理解结构化记忆与知识库 RAG 的分工。",
    ),
    "coze-studio-practice-08-publish-openapi.html": (
        "第9课目标",
        "发布智能体/应用（勾选 API + Chat SDK），创建 PAT，抄出 workflow_id，用 curl 调通 <code>/v1/workflow/run</code>，并配置外部 crontab（开源无内置定时）。",
    ),
    "coze-studio-practice-09-chatflow-openapi.html": (
        "第10课目标",
        "分清 Workflow（批处理）与 Chatflow（多轮对话），创建并调试一条对话流，发布 Chat SDK，理解嵌入自有站点时鉴权与 user_id 注意点。",
    ),
}

GOAL_CSS = """
.goal-box{background:linear-gradient(135deg,rgba(34,197,94,.12),rgba(79,70,229,.10));border:1px solid rgba(34,197,94,.35);border-radius:12px;padding:14px 16px;margin:0 0 22px;font-size:13.5px;line-height:1.75;color:var(--text-secondary)}
.goal-box .gt{display:block;font-weight:800;color:#4ade80;margin-bottom:6px;font-size:14px}
.shot-wrap{position:relative;margin:12px 0 4px}
.shot-note{display:inline-block;margin:0 0 10px;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;background:rgba(239,68,68,.12);color:#f87171;border:1px solid rgba(239,68,68,.35)}
"""


def ensure_goal_css(html: str) -> str:
    if ".goal-box{" in html:
        return html
    return html.replace("</style>", GOAL_CSS + "\n</style>", 1)


def inject_goal(html: str, title: str, body: str) -> str:
    if 'class="goal-box"' in html:
        # replace existing
        html = re.sub(
            r'<div class="goal-box">.*?</div>\s*',
            "",
            html,
            count=1,
            flags=re.S,
        )
    block = f'''  <div class="goal-box"><span class="gt">🎯 {title}</span>{body}</div>
'''
    # after part-desc paragraph closing within part-header
    m = re.search(r'(<div class="part-header">.*?</div>\s*)', html, re.S)
    if not m:
        return html
    # insert after part-header
    idx = m.end()
    return html[:idx] + "\n" + block + html[idx:]


def ensure_why_in_sections(html: str) -> str:
    """If a .card in a section starts without .why, prepend a generic purpose from h2."""

    def repl_section(m: re.Match) -> str:
        sec = m.group(0)
        # find h2 text
        hm = re.search(r"<h2>(.*?)</h2>", sec, re.S)
        if not hm:
            return sec
        title = re.sub(r"<[^>]+>", "", hm.group(1)).strip()
        # card after step-hdr
        cm = re.search(r'(<div class="card">)(\s*)', sec)
        if not cm:
            return sec
        after = sec[cm.end() : cm.end() + 80]
        if 'class="why"' in after or 'class="why"' in sec[cm.start() : cm.start() + 200]:
            return sec
        why = (
            f'<div class="why"><b>本步目的</b>：完成「{title}」。'
            f"请先看懂下方红框标注的截图，再按编号逐步操作；做完用验收行自检。</div>\n      "
        )
        return sec[: cm.end()] + why + sec[cm.end() :]

    return re.sub(
        r'<section\b[^>]*>.*?</section>',
        repl_section,
        html,
        flags=re.S,
    )


def swap_imgs(html: str, mapping: dict[str, str]) -> str:
    for old, new in mapping.items():
        if old in html:
            html = html.replace(f'src="{old}"', f'src="{new}"')
    # add shot-note after each marked shot if missing nearby
    def add_note(m: re.Match) -> str:
        block = m.group(0)
        if "shot-note" in block:
            return block
        return (
            block
            + '\n      <p class="shot-note">红框标注 = 本步要点击 / 填写 / 观察的位置</p>'
        )

    html = re.sub(
        r'<img class="shot" src="assets/coze-practice/[^"]+\.marked\.png"[^>]*>\s*<p class="shot-cap">[^<]*</p>',
        add_note,
        html,
    )
    return html


def strengthen_existing_why(html: str) -> str:
    """Ensure .why starts with 本步目的/作用 wording."""
    def fix(m: re.Match) -> str:
        inner = m.group(1)
        if "本步目的" in inner or "本步作用" in inner or "作用" in inner[:20] or "目的" in inner[:20]:
            # already has purpose-ish
            if not inner.strip().startswith("<b>"):
                return f'<div class="why"><b>本步目的 / 作用</b>：{inner}</div>'
            if "本步目的" not in inner and "作用" in inner:
                inner2 = inner.replace("<b>作用</b>", "<b>本步目的 / 作用</b>", 1)
                return f'<div class="why">{inner2}</div>'
            return m.group(0)
        return f'<div class="why"><b>本步目的 / 作用</b>：{inner}</div>'

    return re.sub(r'<div class="why">(.*?)</div>', fix, html, flags=re.S)


def process_html(mapping: dict[str, str]) -> None:
    for fname, (gtitle, gbody) in LESSON_GOALS.items():
        path = ROOT / fname
        if not path.exists():
            print("missing html", fname)
            continue
        html = path.read_text(encoding="utf-8")
        html = ensure_goal_css(html)
        html = inject_goal(html, gtitle, gbody)
        html = ensure_why_in_sections(html)
        html = strengthen_existing_why(html)
        html = swap_imgs(html, mapping)
        path.write_text(html, encoding="utf-8")
        print("html", fname)


def refresh_shot_notes() -> None:
    """Update caption under marked screenshots to mention numbered order."""
    old = "红框标注 = 本步要点击 / 填写 / 观察的位置"
    new = "数字 1→2→3 = 操作顺序 · 请按编号依次点击 / 填写"
    for path in ROOT.glob("coze-studio-practice-0*.html"):
        t = path.read_text(encoding="utf-8")
        if old in t:
            path.write_text(t.replace(old, new), encoding="utf-8")
            print("notes", path.name)
    hub = ROOT / "coze-studio-practice-tutorial.html"
    if hub.exists():
        t = hub.read_text(encoding="utf-8")
        t2 = t.replace(
            "截图上的<strong>红框</strong>标出要点击或修改的位置，请对照红框操作。",
            "截图上用<strong>数字 1、2、3…</strong>标出操作顺序，请按编号依次点击或填写。",
        )
        if t2 != t:
            hub.write_text(t2, encoding="utf-8")
            print("hub tip updated")


def main():
    import sys

    mapping = mark_all()
    if "--images-only" in sys.argv:
        refresh_shot_notes()
        print("done", len(mapping), "marked images (images-only)")
        return
    process_html(mapping)
    refresh_shot_notes()
    hub = ROOT / "coze-studio-practice-tutorial.html"
    if hub.exists():
        t = hub.read_text(encoding="utf-8")
        tip = (
            '<div class="warn-box" style="margin-top:12px">'
            "<strong>阅读约定</strong>：每课开头有「本课目标」；每一步有「本步目的/作用」；"
            "截图上用<strong>数字 1、2、3…</strong>标出操作顺序，请按编号依次点击或填写。"
            "</div>"
        )
        if "阅读约定" not in t:
            t = t.replace(
                '<section id="path" class="section">',
                tip + "\n  <section id=\"path\" class=\"section\">",
                1,
            )
            hub.write_text(t, encoding="utf-8")
            print("hub tip")
        else:
            refresh_shot_notes()
    print("done", len(mapping), "marked images")


if __name__ == "__main__":
    main()
