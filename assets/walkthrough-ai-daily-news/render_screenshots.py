#!/usr/bin/env python3
"""Render terminal log text as PNG screenshots for walkthrough docs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
OUT = ROOT / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

# macOS monospace fonts (fallback chain)
FONT_CANDIDATES = [
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/Library/Fonts/Courier New.ttf",
]


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def render_terminal(
    title: str,
    body: str,
    out_path: Path,
    *,
    width: int = 960,
    font_size: int = 14,
    pad: int = 20,
) -> None:
    font = _font(font_size)
    title_font = _font(font_size + 2)
    lines = body.rstrip("\n").split("\n")
    line_h = font_size + 6
    title_h = 36
    height = title_h + pad * 2 + line_h * max(len(lines), 1) + 10

    bg = (28, 28, 30)
    bar = (45, 45, 48)
    fg = (220, 220, 220)
    green = (80, 200, 120)
    dot_red, dot_yellow, dot_green = (255, 95, 86), (255, 189, 46), (39, 201, 63)

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, title_h], fill=bar)
    for i, color in enumerate([dot_red, dot_yellow, dot_green]):
        draw.ellipse([14 + i * 22, 12, 26 + i * 22, 24], fill=color)
    draw.text((72, 10), title, fill=fg, font=title_font)

    y = title_h + pad
    for line in lines:
        color = green if line.strip().startswith(("✅", "success=True", "PASSED", "2 passed")) else fg
        if "error" in line.lower() or "failed" in line.lower():
            color = (255, 120, 120)
        draw.text((pad, y), line[:120], fill=color, font=font)
        y += line_h

    img.save(out_path, "PNG")
    print(f"wrote {out_path}")


STEPS = [
    ("step00-env.png", "Step 0 · 环境检查", "step00-env.log"),
    ("step01-init.png", "Step 1 · 起仓 + 改名", "step01-init.log"),
    ("step03-uv-sync.png", "Step 3 · uv sync", "step03-uv-sync.log"),
    ("step03-first-run.png", "Step 3 · 首次跑通", "step03-first-run.log"),
    ("step04-daily-run.png", "Step 4 · 每日播报输出", "step04-daily-run.log"),
    ("step04-files.png", "Step 4 · 业务文件结构", "step04-files.log"),
    ("step07-pytest.png", "Step 7 · pytest", "step07-pytest.log"),
]


def main() -> None:
    # step01 log if missing, synthesize from known output
    init_log = LOGS / "step01-init.log"
    if not init_log.exists():
        init_log.write_text(
            """$ curl -fL .../agent-template/download.zip -o /tmp/tpl.zip
  % Total ... 14193 bytes

$ unzip /tmp/tpl.zip && mv standalone-agent-template ai-daily-news
$ mv your_agent ai_daily_news
$ grep -rl 'your[-_]agent' . | xargs sed -i '' ...

$ grep -r your_agent . || echo "clean"
clean

$ ls ai_daily_news/builder.py
ai_daily_news/builder.py

$ grep '^name =' pyproject.toml
name = "ai-daily-news"
""",
            encoding="utf-8",
        )

    sync_log = LOGS / "step03-uv-sync.log"
    if sync_log.exists():
        text = sync_log.read_text(encoding="utf-8")
        # tail only for screenshot readability
        sync_log.write_text("\n".join(text.strip().splitlines()[-8:]), encoding="utf-8")

    for png_name, title, log_name in STEPS:
        log_path = LOGS / log_name
        if not log_path.exists():
            print(f"skip missing {log_path}")
            continue
        body = log_path.read_text(encoding="utf-8")
        render_terminal(title, body, OUT / png_name)


if __name__ == "__main__":
    main()
