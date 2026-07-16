#!/usr/bin/env python3
"""Annotate Coze practice screenshots with red boxes + labels; enrich HTML goals/why."""
from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "coze-practice"

# (rel_path, boxes) where box = (x1,y1,x2,y2, label) in 1440x900 coords (scaled if needed)
ANNOTATIONS: dict[str, list[tuple[int, int, int, int, str]]] = {
    # P00
    "00-setup/01-login.png": [(520, 280, 920, 520, "在此输入邮箱与密码 → 登录")],
    "00-setup/02-develop.png": [
        (55, 95, 250, 145, "侧栏：项目开发"),
        (1280, 70, 1410, 115, "点「+ 创建」"),
    ],
    "00-setup/10-develop-home.png": [
        (55, 95, 250, 145, "侧栏：项目开发（当前页）"),
        (1280, 70, 1410, 115, "点这里：+ 创建"),
        (55, 145, 250, 195, "侧栏：资源库"),
    ],
    "00-setup/11-create-modal.png": [
        (380, 260, 700, 620, "第2课选这里：创建智能体"),
        (740, 260, 1060, 620, "第5课选这里：创建应用"),
        (1280, 70, 1410, 115, "从「+ 创建」打开"),
    ],
    "00-setup/03-model-admin.png": [(200, 80, 1400, 820, "模型管理列表 · 确认「启用」")],
    "00-setup/12-admin-home.png": [(40, 80, 280, 400, "左侧进入「模型管理」")],
    "00-setup/13-model-list.png": [(280, 80, 1400, 820, "至少一条状态为「启用」")],
    "00-setup/05-add-claude-form.png": [(400, 120, 1040, 780, "在此填写显示名 / Model / API Key")],
    "00-setup/04-model-detail-or-add.png": [(400, 100, 1100, 800, "添加/编辑模型表单")],
    # P02
    "02-agent/01-create-modal.png": [(380, 260, 700, 620, "选「创建智能体」")],
    "02-agent/13-create-agent-form.png": [(480, 300, 960, 520, "填写智能体名称")],
    "02-agent/14-create-agent-filled.png": [(480, 300, 960, 560, "名称填好后点确认")],
    "02-agent/15-new-agent-ide.png": [
        (40, 120, 480, 860, "左：人设与回复逻辑"),
        (480, 120, 900, 860, "中：技能 / 对话体验"),
        (900, 120, 1420, 860, "右：预览与调试"),
    ],
    "02-agent/20-ide-full.png": [
        (40, 120, 480, 860, "① 粘贴人设到这里"),
        (480, 120, 900, 400, "② 技能区（插件/工作流/知识）"),
        (900, 120, 1420, 860, "③ 在此预览调试"),
        (700, 55, 900, 100, "选已启用模型"),
        (1300, 50, 1410, 100, "发布"),
    ],
    "02-agent/21-persona.png": [(40, 120, 520, 860, "人设编辑区 · 全选后粘贴")],
    "02-agent/11-persona-area.png": [(40, 120, 520, 860, "人设与回复逻辑")],
    "02-agent/22-preview.png": [(900, 120, 1420, 860, "预览与调试 · 在此发测试句")],
    "02-agent/12-preview-panel.png": [(900, 120, 1420, 860, "预览与调试面板")],
    "02-agent/16-preview-input.png": [(920, 780, 1400, 870, "输入框 · 发送测试句")],
    "02-agent/17-preview-reply.png": [(920, 150, 1400, 700, "观察模型回复是否符合人设")],
    "02-agent/10-ide-overview.png": [
        (40, 120, 480, 860, "左：人设"),
        (480, 120, 900, 860, "中：技能"),
        (900, 120, 1420, 860, "右：预览"),
    ],
    "02-agent/04-agent-skills-area.png": [(480, 120, 900, 500, "技能区：插件 / 工作流 / 知识")],
    # P03
    "03-skills/10-skills-area.png": [(480, 120, 900, 520, "技能区 · 在此添加插件/工作流/知识")],
    "03-skills/11-plugin-panel.png": [(500, 150, 1100, 750, "插件添加面板 · 勾选后确认")],
    # P04
    "04-knowledge/01-library.png": [(55, 145, 250, 195, "侧栏：资源库"), (1280, 70, 1410, 115, "+ 创建")],
    "04-knowledge/10-library.png": [(55, 145, 250, 195, "侧栏：资源库"), (1280, 70, 1410, 115, "点「+ 创建」")],
    "04-knowledge/02-create-menu.png": [(1100, 100, 1380, 420, "菜单里选「知识库」")],
    "04-knowledge/11-create-menu.png": [(1100, 100, 1380, 420, "菜单里选「知识库」")],
    "04-knowledge/03-create-knowledge-dialog.png": [(420, 180, 1020, 700, "填名称 · 选文本 · 本地文档")],
    "04-knowledge/03b-pick-type.png": [(420, 200, 1020, 650, "选择知识库类型")],
    "04-knowledge/04-knowledge-form-filled.png": [(420, 180, 1020, 700, "填好后点「创建并导入」")],
    "04-knowledge/05-after-create.png": [(200, 100, 1240, 800, "创建后进入上传向导")],
    "04-knowledge/05-knowledge-page.png": [(200, 100, 1240, 800, "知识库详情/上传页")],
    "04-knowledge/06-upload-file.png": [(300, 200, 1140, 700, "上传区 · 选择本地 MD")],
    "04-knowledge/07-upload-processing.png": [(300, 200, 1140, 700, "等待文档处理完成")],
    "03-library/01-library.png": [(55, 145, 250, 195, "资源库"), (1280, 70, 1410, 115, "+ 创建")],
    "03-library/02-create-resource.png": [(1100, 100, 1380, 450, "创建资源菜单")],
    # P05
    "05-plugin/01-explore-plugin.png": [(200, 80, 1400, 850, "插件列表 · 点卡片查看/添加")],
    "05-plugin/10-explore.png": [(40, 80, 200, 200, "侧栏：探索"), (200, 80, 1400, 850, "探索内容区")],
    "05-plugin/11-plugin-list.png": [(200, 80, 1400, 850, "插件列表 · 点卡片安装")],
    "09-explore/01-explore.png": [(40, 80, 200, 200, "探索入口")],
    # P06
    "06-database/10-library.png": [(55, 145, 250, 195, "资源库"), (1280, 70, 1410, 115, "+ 创建")],
    "06-database/11-create-menu.png": [(1100, 100, 1380, 480, "菜单选「数据库」")],
    # P07
    "07-project/01-project-ide.png": [
        (40, 80, 320, 860, "左侧资源树"),
        (320, 80, 1420, 860, "中间编辑区"),
        (1280, 40, 1410, 95, "发布"),
    ],
    "07-project/10-ide.png": [
        (40, 80, 320, 860, "① 资源树（工作流入口）"),
        (320, 80, 1420, 860, "② 当前资源编辑区"),
    ],
    "07-project/02-workflow.png": [(200, 80, 1400, 850, "应用内工作流画布")],
    # P01
    "01-competitor-daily/01-login.png": [(520, 280, 920, 520, "登录后才能进开发页")],
    "01-competitor-daily/02-develop.png": [(1280, 70, 1410, 115, "创建/打开应用"), (280, 160, 560, 360, "打开「竞品日报实战」")],
    "01-competitor-daily/05-workflow-canvas.png": [(80, 80, 1360, 820, "五节点画布：开始→LLM→Code→HTTP→结束")],
    "01-competitor-daily/10-canvas.png": [(80, 80, 1360, 820, "工作流画布 · 按节点依次配置")],
    "01-competitor-daily/11-from-project.png": [(40, 80, 320, 400, "从左侧点开工作流")],
    "01-competitor-daily/06-testrun.png": [(1000, 80, 1420, 860, "试运行侧栏 · 填 report_date / lark_hint")],
    # P08
    "08-publish/10-agent-publish.png": [(400, 100, 1100, 800, "发布页 · 勾选 API / Chat SDK")],
    "08-publish/11-app-publish.png": [(400, 100, 1100, 800, "应用发布 · 勾选渠道后点发布")],
    "08-publish/20-publish-panel.png": [(400, 80, 1100, 820, "发布面板 · 勾选 API + Chat SDK")],
    "08-publish/12-avatar-menu.png": [(1100, 40, 1420, 320, "头像菜单 · 进设置")],
    "08-publish/21-avatar-menu.png": [(1100, 40, 1420, 320, "头像菜单 · 进设置")],
    "08-publish/16-account-settings.png": [(40, 80, 320, 500, "左侧：API 授权")],
    "08-publish/17-api-auth-tab.png": [(320, 80, 1400, 820, "添加新令牌 · 复制 PAT")],
    "08-publish/14-workflow-url-id.png": [(200, 20, 1400, 80, "地址栏末段数字 = workflow_id")],
    "08-publish/15-api-configure.png": [(320, 80, 1400, 820, "API / 令牌相关配置")],
    "08-publish/24-settings-page.png": [(40, 80, 1400, 820, "账号设置页 · 找 API 授权")],
    "08-publish/25-top-menu.png": [(1100, 40, 1420, 320, "右上角菜单入口")],
    "08-publish/03-agent-publish.png": [(400, 100, 1100, 800, "智能体发布")],
    "08-publish/04-app-publish.png": [(400, 100, 1100, 800, "应用发布")],
    "08-publish/01-account-menu.png": [(1100, 40, 1420, 320, "账号菜单")],
    "08-publish/13-settings-fallback.png": [(40, 80, 1400, 820, "设置入口")],
    # P09
    "09-chatflow/10-explore.png": [(40, 80, 200, 200, "探索 / 开放能力相关入口")],
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
    f = font(max(18, int(22 * min(sx, sy))))
    f_small = font(max(14, int(16 * min(sx, sy))))

    for x1, y1, x2, y2, label in boxes:
        a = (int(x1 * sx), int(y1 * sy), int(x2 * sx), int(y2 * sy))
        # semi-transparent fill
        draw.rectangle(a, outline=(239, 68, 68, 255), width=max(3, int(4 * min(sx, sy))), fill=(239, 68, 68, 35))
        # label background above box or inside top
        tw = draw.textlength(label, font=f) if hasattr(draw, "textlength") else len(label) * 12
        pad = 8
        ly1 = max(4, a[1] - 36)
        if ly1 < 4:
            ly1 = a[1] + 6
        lx1 = a[0]
        lx2 = min(w - 4, int(lx1 + tw + pad * 2))
        ly2 = ly1 + 32
        draw.rectangle((lx1, ly1, lx2, ly2), fill=(239, 68, 68, 230))
        draw.text((lx1 + pad, ly1 + 5), label, fill=(255, 255, 255, 255), font=f)

    # bottom banner
    banner_h = max(36, int(42 * sy))
    draw.rectangle((0, h - banner_h, w, h), fill=(15, 23, 42, 210))
    draw.text((14, h - banner_h + 10), "红框 = 本步重点操作/修改位置 · 请对照文案点击", fill=(248, 250, 252, 255), font=f_small)

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG", optimize=True)
    print("marked", dst.relative_to(ROOT))


def mark_all() -> dict[str, str]:
    """Returns map original_rel -> marked_rel (posix)."""
    mapping = {}
    for rel, boxes in ANNOTATIONS.items():
        src = ASSETS / rel
        if not src.exists():
            print("skip missing", rel)
            continue
        # write as foo.marked.png next to original
        dst = src.with_name(src.stem + ".marked" + src.suffix)
        annotate(src, boxes, dst)
        mapping[f"assets/coze-practice/{rel}"] = f"assets/coze-practice/{Path(rel).with_name(Path(rel).stem + '.marked' + Path(rel).suffix).as_posix()}"
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


def main():
    mapping = mark_all()
    process_html(mapping)
    # also update hub tip
    hub = ROOT / "coze-studio-practice-tutorial.html"
    if hub.exists():
        t = hub.read_text(encoding="utf-8")
        tip = (
            '<div class="warn-box" style="margin-top:12px">'
            "<strong>阅读约定</strong>：每课开头有「本课目标」；每一步有「本步目的/作用」；"
            "截图上的<strong>红框</strong>标出要点击或修改的位置，请对照红框操作。"
            "</div>"
        )
        if "阅读约定" not in t:
            t = t.replace(
                '<section id="path" class="section">',
                tip + '\n  <section id="path" class="section">',
                1,
            )
            # ensure warn-box style exists via style.css already
            hub.write_text(t, encoding="utf-8")
            print("hub tip")
    print("done", len(mapping), "marked images")


if __name__ == "__main__":
    main()
