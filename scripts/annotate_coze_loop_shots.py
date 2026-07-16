#!/usr/bin/env python3
"""Annotate Coze Loop practice screenshots with ordered 1/2/3… callouts."""
from __future__ import annotations

import os
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/coze-loop-practice"
OUT = ROOT / "assets/coze-loop-practice/marked"

# (rel_path, [(x1,y1,x2,y2,label), ...])
# List order = operation order. Labels are short Chinese; numbers are drawn as 1/2/3…
# Coordinates for 1440x900 screenshots captured by Playwright
ANNOTATIONS: list[tuple[str, list[tuple[int, int, int, int, str]]]] = [
    # P00
    ("00-setup/01-login.png", [
        (520, 355, 920, 405, "填邮箱"),
        (520, 420, 920, 470, "填密码"),
        (520, 490, 700, 545, "点「注册」"),
        (720, 490, 920, 545, "点「登录」"),
    ]),
    ("00-setup/02-login-filled.png", [
        (520, 355, 920, 470, "确认已填好"),
        (520, 490, 700, 545, "点「注册」"),
    ]),
    ("00-setup/03-home-prompts.png", [
        (0, 60, 210, 420, "看侧栏模块"),
        (250, 200, 1100, 700, "看主工作区"),
        (1180, 95, 1410, 145, "创建入口在这"),
    ]),
    ("00-setup/04-sidebar.png", [
        (8, 70, 200, 120, "Prompt 开发"),
        (8, 120, 200, 165, "Playground"),
        (8, 200, 200, 250, "评测集"),
        (8, 250, 200, 300, "评估器"),
        (8, 300, 200, 350, "实验"),
        (8, 380, 200, 430, "Trace"),
        (8, 450, 200, 500, "标签管理"),
    ]),
    ("00-setup/05-user-menu.png", [
        (8, 780, 210, 880, "点左下角头像"),
        (40, 680, 220, 780, "选账户设置"),
    ]),
    ("00-setup/06-account-modal.png", [
        (380, 180, 1060, 720, "账户设置弹窗"),
        (400, 220, 560, 280, "可切 API 授权"),
    ]),
    # P01
    ("01-prompt/01-list-empty.png", [
        (8, 70, 200, 120, "确认在 Prompt 开发"),
        (1180, 95, 1410, 145, "点「创建 Prompt」"),
    ]),
    ("01-prompt/02-create-menu.png", [
        (1180, 95, 1410, 200, "选「空白 Prompt」"),
    ]),
    ("01-prompt/03-create-dialog.png", [
        (300, 220, 1140, 620, "填写 Key / 名称"),
        (1000, 640, 1120, 690, "点「确认」"),
    ]),
    ("01-prompt/04-create-filled.png", [
        (360, 260, 1080, 340, "填 Prompt Key"),
        (360, 350, 1080, 420, "填 Prompt 名称"),
        (1000, 640, 1120, 690, "点「确认」"),
    ]),
    ("01-prompt/05-develop.png", [
        (220, 140, 560, 700, "左：写模板"),
        (560, 140, 950, 700, "中：选模型"),
        (950, 140, 1420, 860, "右：预览调试"),
    ]),
    ("01-prompt/06-edit-template.png", [
        (240, 200, 540, 360, "写 System"),
        (240, 380, 540, 520, "写 User"),
        (240, 620, 420, 670, "可添加消息"),
    ]),
    ("01-prompt/10-model-dropdown.png", [
        (560, 180, 920, 420, "下拉选 Claude"),
    ]),
    ("01-prompt/10-model-selected.png", [
        (560, 170, 920, 230, "确认已选模型"),
        (560, 240, 920, 360, "看参数（可选）"),
        (980, 780, 1400, 870, "点「运行」"),
    ]),
    ("01-prompt/11-debug-result.png", [
        (980, 200, 1400, 520, "看模型回复"),
        (980, 520, 1400, 580, "看耗时/Tokens"),
        (1100, 70, 1280, 120, "再提交新版"),
    ]),
    ("01-prompt/07-submit-version.png", [
        (420, 250, 1020, 580, "填版本号"),
        (700, 580, 900, 650, "确认提交"),
    ]),
    ("01-prompt/12-version-done.png", [
        (250, 70, 700, 130, "确认版本状态"),
    ]),
    ("01-prompt/08-playground.png", [
        (8, 120, 200, 165, "进 Playground"),
        (560, 170, 920, 230, "选 Claude"),
        (980, 780, 1400, 870, "点「运行」"),
    ]),
    ("01-prompt/13-playground-result.png", [
        (980, 200, 1400, 480, "看成功回复"),
    ]),
    ("01-prompt/09-list-with-item.png", [
        (250, 200, 1400, 320, "列表有新 Prompt"),
        (1100, 220, 1380, 300, "可进详情/调用记录"),
    ]),
    # P02
    ("02-dataset/01-list.png", [
        (8, 200, 200, 250, "点「评测集」"),
        (1180, 95, 1410, 145, "点「新建评测集」"),
    ]),
    ("02-dataset/02-create.png", [
        (250, 160, 900, 280, "填名称/描述"),
        (250, 320, 1100, 620, "配置列"),
        (1250, 820, 1400, 880, "点「创建」"),
    ]),
    ("02-dataset/03-named.png", [
        (250, 180, 900, 280, "名称必填"),
    ]),
    ("02-dataset/04-schema.png", [
        (250, 320, 1100, 700, "看默认两列"),
        (250, 720, 420, 770, "可添加列"),
    ]),
    ("02-dataset/05-detail.png", [
        (250, 160, 900, 280, "进入详情页"),
        (1180, 95, 1410, 200, "添加数据/新建实验"),
    ]),
    ("02-dataset/05-add-data.png", [
        (800, 120, 1420, 860, "在抽屉填一行数据"),
    ]),
    ("02-dataset/07-item-list.png", [
        (250, 200, 1400, 500, "确认数据出现在表里"),
    ]),
    # P03
    ("03-evaluator/01-list.png", [
        (8, 250, 200, 300, "点「评估器」"),
        (1180, 95, 1410, 145, "点「新建」"),
    ]),
    ("03-evaluator/02-builtin.png", [
        (250, 100, 500, 160, "切到「预置」"),
        (250, 180, 1400, 700, "浏览预置卡片"),
    ]),
    ("03-evaluator/04-create-menu.png", [
        (1100, 140, 1400, 280, "选 LLM 或 Code"),
    ]),
    ("03-evaluator/05-create-llm.png", [
        (250, 140, 1400, 800, "编辑 LLM 评估器"),
    ]),
    ("03-evaluator/07-llm-configured.png", [
        (560, 170, 920, 280, "选 Claude 作评判模型"),
    ]),
    ("03-evaluator/06-create-code.png", [
        (250, 140, 1400, 800, "写 Code 规则"),
    ]),
    # P04
    ("04-experiment/01-list.png", [
        (8, 300, 200, 350, "点「实验」"),
        (1180, 95, 1410, 145, "点「新建实验」"),
    ]),
    ("04-experiment/02-wizard.png", [
        (250, 80, 1400, 160, "看五步进度条"),
        (250, 180, 900, 400, "填步骤1基本信息"),
    ]),
    ("04-experiment/03-basic.png", [
        (250, 180, 900, 320, "填写实验名称"),
        (1200, 820, 1400, 880, "点「下一步」"),
    ]),
    ("04-experiment/04-dataset-step.png", [
        (250, 180, 900, 400, "选择评测集"),
    ]),
    ("04-experiment/04b-dataset-picked.png", [
        (250, 180, 900, 400, "确认已选中"),
    ]),
    ("04-experiment/05-target-step.png", [
        (250, 180, 1100, 500, "选评测对象或跳过"),
    ]),
    ("04-experiment/06-evaluator-step.png", [
        (250, 180, 1100, 500, "选评估器或跳过"),
    ]),
    ("04-experiment/07-confirm.png", [
        (250, 180, 1100, 500, "核对配置"),
        (1200, 820, 1400, 880, "点「启动实验」"),
    ]),
    # P05
    ("05-trace/01-list.png", [
        (8, 380, 200, 430, "点 Trace"),
        (250, 90, 900, 150, "调过滤器"),
        (250, 180, 1400, 700, "点某行看详情"),
    ]),
    ("05-trace/02-toolbar.png", [
        (250, 90, 1100, 150, "改时间/数据源等"),
    ]),
    ("05-trace/04-detail.png", [
        (250, 140, 700, 700, "看调用树"),
        (720, 140, 1150, 700, "看 Input/Output"),
        (1180, 140, 1420, 500, "看状态/耗时"),
    ]),
    # P06
    ("06-tag/01-list.png", [
        (8, 450, 200, 500, "点「标签管理」"),
        (1180, 95, 1410, 145, "点「新建标签」"),
    ]),
    ("06-tag/02-create.png", [
        (400, 200, 1040, 700, "填写标签信息"),
    ]),
    ("06-tag/03-filled.png", [
        (400, 200, 1040, 500, "确认后提交"),
    ]),
    ("06-tag/04-result.png", [
        (250, 180, 1400, 400, "列表出现新标签"),
    ]),
    # P07
    ("07-pat/00-usermenu.png", [
        (8, 780, 220, 880, "点左下角头像"),
        (40, 680, 240, 760, "点「账户设置」"),
    ]),
    ("07-pat/01-account.png", [
        (380, 200, 560, 280, "看账户设置"),
        (400, 280, 560, 340, "切到 API 授权"),
    ]),
    ("07-pat/02-pat-tab.png", [
        (600, 200, 1100, 320, "看个人访问令牌"),
        (1050, 200, 1250, 270, "点「添加新令牌」"),
    ]),
    ("07-pat/03-create.png", [
        (480, 250, 960, 650, "填名称/过期时间"),
    ]),
    ("07-pat/04-filled.png", [
        (480, 250, 960, 500, "确认生成"),
    ]),
    ("07-pat/05-created.png", [
        (480, 220, 960, 620, "立刻复制明文"),
    ]),
]


def get_font(size: int) -> ImageFont.ImageFont:
    for name in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ):
        if os.path.exists(name):
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                continue
    return ImageFont.load_default()


_NUM_PREFIX = re.compile(
    r"^(?:[0-9]+|[①②③④⑤⑥⑦⑧⑨⑩]|[一二三四五六七八九十])[\s\.\、:：\)）\-]*"
)


def clean_label(label: str) -> str:
    return _NUM_PREFIX.sub("", label).strip() or label


def annotate(src: Path, boxes: list[tuple[int, int, int, int, str]], dest: Path) -> None:
    im = Image.open(src).convert("RGBA")
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_num = get_font(26)
    font_sm = get_font(17)
    red = (220, 38, 38, 255)
    red_soft = (239, 68, 68, 40)
    white = (255, 255, 255, 255)

    for i, (x1, y1, x2, y2, label) in enumerate(boxes, start=1):
        text = clean_label(label)
        # highlight region
        draw.rectangle([x1, y1, x2, y2], outline=red, width=4)
        draw.rectangle([x1, y1, x2, y2], fill=red_soft)

        # big numbered circle (primary order marker)
        r = 18
        cx = min(max(x1 + 6, r + 4), im.width - r - 4)
        cy = min(max(y1 + 6, r + 4), im.height - r - 4)
        # if box is tiny, park badge just outside top-left
        if (x2 - x1) < 80 or (y2 - y1) < 50:
            cx = max(r + 4, x1 - 4)
            cy = max(r + 4, y1 - 4)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=red, outline=(255, 255, 255, 255), width=2)
        num = str(i)
        nb = draw.textbbox((0, 0), num, font=font_num)
        nw, nh = nb[2] - nb[0], nb[3] - nb[1]
        draw.text((cx - nw / 2, cy - nh / 2 - 2), num, fill=white, font=font_num)

        # short Chinese caption pill to the right of the circle
        if text:
            tw = draw.textbbox((0, 0), text, font=font_sm)
            tw, th = tw[2] - tw[0], tw[3] - tw[1]
            pad_x, pad_y = 8, 5
            lx1 = min(im.width - tw - pad_x * 2 - 8, cx + r + 6)
            ly1 = max(4, cy - th // 2 - pad_y)
            lx2 = lx1 + tw + pad_x * 2
            ly2 = ly1 + th + pad_y * 2
            if lx2 > im.width - 4:
                lx1 = max(4, cx - r - 6 - (tw + pad_x * 2))
                lx2 = lx1 + tw + pad_x * 2
            draw.rounded_rectangle([lx1, ly1, lx2, ly2], radius=6, fill=(185, 28, 28, 235))
            draw.text((lx1 + pad_x, ly1 + pad_y - 1), text, fill=white, font=font_sm)

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=92)
    print("annotated", dest.relative_to(ROOT), f"({len(boxes)} steps)")


def main() -> None:
    for rel, boxes in ANNOTATIONS:
        src = SRC / rel
        if not src.exists():
            print("SKIP missing", rel)
            continue
        annotate(src, boxes, OUT / rel)
    print("done", len(ANNOTATIONS))


if __name__ == "__main__":
    main()
