#!/usr/bin/env python3
"""Generate before/after code edit screenshots for walkthrough."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "screenshots" / "edits"
OUT.mkdir(parents=True, exist_ok=True)

FONT = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Menlo.ttc",
]


def _font(size: int):
    for p in FONT:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


EDITS = [
    {
        "file": "step04-edit-01-prompts.png",
        "path": "ai_daily_news/prompts/__init__.py",
        "reason": "定义「每日播报」LLM 输出格式，与业务逻辑分离",
        "before": 'RUN_SYSTEM = "你是一个有用的助手,简洁、准确地回答用户的问题。"',
        "after": 'BROADCAST_SYSTEM = """你是「AI 最新资讯每日播报」编辑...\n📢 AI 资讯每日播报 · {date}\n【今日要闻】..."""',
    },
    {
        "file": "step04-edit-02-state.png",
        "path": "ai_daily_news/state.py",
        "reason": "fetch 与 broadcast 节点之间传递标题列表",
        "before": "class AgentState(TypedDict, total=False):\n    input: str\n    output: str",
        "after": "class AgentState(TypedDict, total=False):\n    input: str\n    output: str\n    raw_items: list\n    headlines_text: str",
    },
    {
        "file": "step04-edit-03-fetch.png",
        "path": "ai_daily_news/nodes/fetch.py  【新建】",
        "reason": "从 HN RSS 抓取 AI 资讯标题；网络失败走 FALLBACK",
        "before": "（模板无此文件 · 原只有 nodes/run.py 回声 demo）",
        "after": "def fetch_node(state):\n    items = _fetch_rss(HN_RSS) or FALLBACK\n    return {\"raw_items\": items, \"headlines_text\": ...}",
    },
    {
        "file": "step04-edit-04-broadcast.png",
        "path": "ai_daily_news/nodes/broadcast.py  【新建】",
        "reason": "用 LLM + BROADCAST_SYSTEM 把标题编排成 📢 播报正文",
        "before": "（模板无此文件）",
        "after": "def broadcast_node(state):\n    get_llm(\"sonnet\").invoke([SystemMessage(...), ...])\n    return {\"output\": out}",
    },
    {
        "file": "step04-edit-05-nodes-init.png",
        "path": "ai_daily_news/nodes/__init__.py",
        "reason": "导出新建节点，供 builder.py 引用",
        "before": "from .run import run_node\n__all__ = [\"run_node\"]",
        "after": "from .fetch import fetch_node\nfrom .broadcast import broadcast_node\n__all__ = [\"fetch_node\", \"broadcast_node\"]",
    },
    {
        "file": "step04-edit-06-builder.png",
        "path": "ai_daily_news/builder.py",
        "reason": "串成两节点图：先抓资讯再出播报（builder 在包根，不在 nodes/）",
        "before": "g.add_node(\"run\", run_node)\n g.set_entry_point(\"run\")\n g.add_edge(\"run\", END)",
        "after": "g.add_node(\"fetch\", fetch_node)\n g.add_node(\"broadcast\", broadcast_node)\n fetch → broadcast → END",
    },
    {
        "file": "step04-edit-07-core.png",
        "path": "ai_daily_news/core.py  【Skill 步骤 5】",
        "reason": "Portal 显示领域效果 briefing_sent；成功判定需有 headlines",
        "before": 'success = bool(final.get("output"))\nrecord_effect("done", 1)',
        "after": 'success = bool(output) and bool(headlines_text)\nrecord_effect("briefing_sent", 1)',
    },
    {
        "file": "step04-edit-08-tests.png",
        "path": "tests/test_smoke.py  【Skill 步骤 7】",
        "reason": "断言每日播报业务：output + headlines_text 非空",
        "before": 'def test_graph_runs():\n    assert out.get("output")',
        "after": 'def test_daily_briefing():\n    assert out.get("output") and out.get("headlines_text")',
    },
]


def render_edit(item: dict) -> None:
    path = item["path"]
    reason = item["reason"]
    before = item["before"]
    after = item["after"]
    font = _font(12)
    small = _font(11)
    title_font = _font(13)

    lines = [
        ("path", path, (96, 165, 250)),
        ("why", f"作用: {reason}", (147, 197, 253)),
        ("lbl1", "改前", (245, 158, 11)),
        ("b", before, (200, 200, 200)),
        ("lbl2", "改后", (34, 197, 94)),
        ("a", after, (200, 200, 200)),
    ]
    wrapped: list[tuple[str, str, tuple]] = []
    for kind, text, color in lines:
        if kind in ("b", "a"):
            for ln in text.split("\n"):
                wrapped.append((kind, ln, color))
        else:
            wrapped.append((kind, text, color))

    w, pad, lh = 920, 16, 18
    h = pad * 2 + lh * (len(wrapped) + 2) + 36
    img = Image.new("RGB", (w, h), (24, 24, 27))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 32], fill=(40, 40, 45))
    draw.text((pad, 8), Path(item["file"]).stem.replace("step04-edit-", "修改 · "), fill=(220, 220, 220), font=title_font)
    y = 40
    for kind, text, color in wrapped:
        if kind.startswith("lbl"):
            y += 4
        draw.text((pad, y), text[:100], fill=color, font=small if kind in ("b", "a", "why") else font)
        y += lh
    out = OUT / item["file"]
    img.save(out, "PNG")
    print(f"wrote {out}")


def main() -> None:
    for item in EDITS:
        render_edit(item)


if __name__ == "__main__":
    main()
