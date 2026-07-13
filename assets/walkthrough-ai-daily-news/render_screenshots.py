#!/usr/bin/env python3
"""Render terminal logs as PNG for walkthrough."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
OUT = ROOT / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
]

STEPS = [
    ("step-trigger-skill.png", "B · Cursor 触发 Skill", "step-trigger-skill.log"),
    ("step00-env.png", "Skill 步骤 0 · 环境检查", "step00-env.log"),
    ("step01-skill-create.png", "Skill 步骤 1 · 创建 Agent（Skill 引导执行）", "step01-skill-create.log"),
    ("step02-nexus.png", "Skill 步骤 2 · Nexus 凭据", "step02-nexus.log"),
    ("step03-first-run.png", "Skill 步骤 3 · 安装 + 首次跑通", "step03-first-run.log"),
    ("step04-modify.png", "Skill 步骤 4 · 修改业务图", "step04-modify.log"),
    ("step04-verify-run.png", "Skill 步骤 4 · 验证播报", "step04-verify-run.log"),
    ("step07-pytest.png", "Skill 步骤 7 · 测试验证", "step07-pytest.log"),
    ("step-install-03-list.png", "A3 · install + list", "step-install-03-list.log"),
]


def _font(size: int):
    for path in FONT_CANDIDATES:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def render_terminal(title: str, body: str, out_path: Path, *, width: int = 960, font_size: int = 13) -> None:
    font = _font(font_size)
    title_font = _font(font_size + 1)
    lines = body.rstrip("\n").split("\n")
    line_h = font_size + 6
    title_h = 36
    height = title_h + 28 + line_h * max(len(lines), 1) + 10
    img = Image.new("RGB", (width, height), (28, 28, 30))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, title_h], fill=(45, 45, 48))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([14 + i * 22, 12, 26 + i * 22, 24], fill=c)
    draw.text((72, 10), title, fill=(220, 220, 220), font=title_font)
    y = title_h + 14
    for line in lines:
        color = (80, 200, 120) if any(x in line for x in ("✓", "success=True", "PASSED", "2 passed", "clean")) else (220, 220, 220)
        if "error" in line.lower() or "failed" in line.lower():
            color = (255, 120, 120)
        draw.text((16, y), line[:115], fill=color, font=font)
        y += line_h
    img.save(out_path, "PNG")
    print(f"wrote {out_path}")


def main() -> None:
    for png, title, log_name in STEPS:
        log_path = LOGS / log_name
        if not log_path.exists():
            print(f"skip {log_name}")
            continue
        text = log_path.read_text(encoding="utf-8")
        if log_name == "step03-first-run.log":
            text = "\n".join(text.splitlines()[-12:])
        if log_name == "step01-skill-create.log":
            text = "\n".join(text.splitlines()[-14:])
        render_terminal(title, text, OUT / png)


if __name__ == "__main__":
    main()
