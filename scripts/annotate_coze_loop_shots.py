#!/usr/bin/env python3
"""Annotate Coze Loop practice screenshots with numbered red callouts."""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/coze-loop-practice"
OUT = ROOT / "assets/coze-loop-practice/marked"

# (rel_path, [(x1,y1,x2,y2,label), ...])
# Coordinates for 1440x900 screenshots captured by Playwright
ANNOTATIONS: list[tuple[str, list[tuple[int, int, int, int, str]]]] = [
    # P00
    ("00-setup/01-login.png", [
        (520, 355, 920, 405, "1 填邮箱"),
        (520, 420, 920, 470, "2 填密码"),
        (520, 490, 700, 545, "3 注册"),
        (720, 490, 920, 545, "4 登录"),
    ]),
    ("00-setup/02-login-filled.png", [
        (520, 355, 920, 470, "已填好账号密码"),
        (520, 490, 700, 545, "点「注册」"),
    ]),
    ("00-setup/03-home-prompts.png", [
        (0, 60, 210, 420, "侧栏四大模块"),
        (1180, 95, 1410, 145, "创建 Prompt"),
        (250, 200, 1100, 700, "主工作区"),
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
        (8, 780, 210, 880, "点头像打开菜单"),
        (40, 680, 220, 780, "账户设置 / 退出"),
    ]),
    ("00-setup/06-account-modal.png", [
        (380, 180, 1060, 720, "账户设置弹窗"),
        (400, 220, 560, 280, "切到 API 授权"),
    ]),
    # P01
    ("01-prompt/01-list-empty.png", [
        (1180, 95, 1410, 145, "点这里创建"),
        (8, 70, 200, 120, "当前：Prompt 开发"),
    ]),
    ("01-prompt/02-create-menu.png", [
        (1180, 95, 1410, 200, "选「空白 Prompt」"),
    ]),
    ("01-prompt/03-create-dialog.png", [
        (300, 220, 1140, 680, "填写 Key / 名称 / 描述"),
        (1000, 640, 1120, 690, "点确认"),
    ]),
    ("01-prompt/04-create-filled.png", [
        (360, 260, 1080, 340, "① Prompt Key"),
        (360, 350, 1080, 420, "② Prompt 名称"),
        (1000, 640, 1120, 690, "③ 确认"),
    ]),
    ("01-prompt/05-develop.png", [
        (220, 140, 560, 700, "左：写 Prompt 模板"),
        (560, 140, 950, 700, "中：选模型 / 参数"),
        (950, 140, 1420, 860, "右：预览与调试"),
    ]),
    ("01-prompt/06-edit-template.png", [
        (240, 200, 540, 360, "System 消息写这里"),
        (240, 380, 540, 520, "User 消息写这里"),
        (240, 620, 420, 670, "可继续添加消息"),
    ]),
    ("01-prompt/10-model-dropdown.png", [
        (560, 180, 920, 420, "下拉选 Claude Sonnet"),
    ]),
    ("01-prompt/10-model-selected.png", [
        (560, 170, 920, 230, "① 已选 Claude Sonnet"),
        (560, 240, 920, 360, "② 参数（勿同时开 top_p）"),
        (980, 780, 1400, 870, "③ 输入问题后点「运行」"),
    ]),
    ("01-prompt/11-debug-result.png", [
        (980, 200, 1400, 520, "模型回复出现在这里"),
        (980, 520, 1400, 580, "耗时 / Tokens 统计"),
        (1100, 70, 1280, 120, "调试成功后再提交新版"),
    ]),
    ("01-prompt/07-submit-version.png", [
        (420, 250, 1020, 650, "填写版本号并确认提交"),
    ]),
    ("01-prompt/12-version-done.png", [
        (250, 70, 700, 130, "版本已提交（看状态变化）"),
    ]),
    ("01-prompt/08-playground.png", [
        (8, 120, 200, 165, "侧栏进 Playground"),
        (560, 170, 920, 230, "同样选 Claude"),
        (980, 780, 1400, 870, "点运行试一试"),
    ]),
    ("01-prompt/13-playground-result.png", [
        (980, 200, 1400, 480, "Playground 成功回复"),
    ]),
    ("01-prompt/09-list-with-item.png", [
        (250, 200, 1400, 320, "列表里能看到新 Prompt"),
        (1100, 220, 1380, 300, "详情 / 调用记录"),
    ]),
    # P02
    ("02-dataset/01-list.png", [
        (8, 200, 200, 250, "点「评测集」"),
        (1180, 95, 1410, 145, "新建评测集"),
    ]),
    ("02-dataset/02-create.png", [
        (250, 160, 900, 280, "① 填名称 / 描述"),
        (250, 320, 1100, 620, "② 配置列 input / reference"),
        (1250, 820, 1400, 880, "③ 点创建"),
    ]),
    ("02-dataset/03-named.png", [
        (250, 180, 900, 280, "名称必填"),
    ]),
    ("02-dataset/04-schema.png", [
        (250, 320, 1100, 700, "默认两列：input + reference_output"),
        (250, 720, 420, 770, "可添加列"),
    ]),
    ("02-dataset/05-detail.png", [
        (1180, 95, 1410, 200, "添加数据 / 新建实验"),
        (250, 160, 900, 280, "评测集详情页"),
    ]),
    ("02-dataset/05-add-data.png", [
        (800, 120, 1420, 860, "右侧抽屉填写一条数据"),
    ]),
    ("02-dataset/07-item-list.png", [
        (250, 200, 1400, 500, "数据行会出现在表里"),
    ]),
    # P03
    ("03-evaluator/01-list.png", [
        (8, 250, 200, 300, "点「评估器」"),
        (1180, 95, 1410, 145, "新建评估器"),
    ]),
    ("03-evaluator/02-builtin.png", [
        (250, 100, 500, 160, "切到「预置」页签"),
        (250, 180, 1400, 700, "浏览内置评估器卡片"),
    ]),
    ("03-evaluator/04-create-menu.png", [
        (1100, 140, 1400, 280, "选 LLM 或 Code"),
    ]),
    ("03-evaluator/05-create-llm.png", [
        (250, 140, 1400, 800, "LLM 评估器编辑页"),
    ]),
    ("03-evaluator/07-llm-configured.png", [
        (560, 170, 920, 280, "选 Claude 作评判模型"),
    ]),
    ("03-evaluator/06-create-code.png", [
        (250, 140, 1400, 800, "Code 评估器：写规则代码"),
    ]),
    # P04
    ("04-experiment/01-list.png", [
        (8, 300, 200, 350, "点「实验」"),
        (1180, 95, 1410, 145, "新建实验"),
    ]),
    ("04-experiment/02-wizard.png", [
        (250, 80, 1400, 160, "顶部五步进度条"),
        (250, 180, 900, 400, "步骤1：基本信息"),
    ]),
    ("04-experiment/03-basic.png", [
        (250, 180, 900, 320, "填写实验名称"),
        (1200, 820, 1400, 880, "下一步"),
    ]),
    ("04-experiment/04-dataset-step.png", [
        (250, 180, 900, 400, "步骤2：选择评测集（必选）"),
    ]),
    ("04-experiment/04b-dataset-picked.png", [
        (250, 180, 900, 400, "已选中评测集 / 版本"),
    ]),
    ("04-experiment/05-target-step.png", [
        (250, 180, 1100, 500, "步骤3：评测对象（可选，可跳过）"),
    ]),
    ("04-experiment/06-evaluator-step.png", [
        (250, 180, 1100, 500, "步骤4：评估器（可选）"),
    ]),
    ("04-experiment/07-confirm.png", [
        (250, 180, 1100, 500, "步骤5：确认并启动"),
        (1200, 820, 1400, 880, "启动实验"),
    ]),
    # P05
    ("05-trace/01-list.png", [
        (8, 380, 200, 430, "点 Trace"),
        (250, 90, 900, 150, "过滤器：选 Prompt 平台"),
        (250, 180, 1400, 700, "有数据时点某一行看详情"),
    ]),
    ("05-trace/04-detail.png", [
        (250, 140, 700, 700, "① 调用树：PromptExecutor→Claude"),
        (720, 140, 1150, 700, "② Input / Output JSON"),
        (1180, 140, 1420, 500, "③ 状态 / 耗时 / Tokens"),
    ]),
    ("05-trace/02-toolbar.png", [
        (250, 90, 1100, 150, "时间范围 · Span 类型 · 数据源"),
    ]),
    # P06
    ("06-tag/01-list.png", [
        (8, 450, 200, 500, "点「标签管理」"),
        (1180, 95, 1410, 145, "新建标签"),
    ]),
    ("06-tag/02-create.png", [
        (400, 200, 1040, 700, "填写标签名称与取值"),
    ]),
    ("06-tag/03-filled.png", [
        (400, 200, 1040, 500, "确认信息后提交"),
    ]),
    ("06-tag/04-result.png", [
        (250, 180, 1400, 400, "列表出现新标签"),
    ]),
    # P07
    ("07-pat/00-usermenu.png", [
        (8, 780, 220, 880, "① 点左下角头像"),
        (40, 680, 240, 760, "② 点「账户设置」"),
    ]),
    ("07-pat/01-account.png", [
        (380, 200, 560, 280, "账户设置"),
        (400, 280, 560, 340, "切到 API 授权"),
    ]),
    ("07-pat/02-pat-tab.png", [
        (600, 200, 1100, 320, "个人访问令牌"),
        (1050, 200, 1250, 270, "添加新令牌"),
    ]),
    ("07-pat/03-create.png", [
        (480, 250, 960, 650, "填写令牌名称 / 过期时间"),
    ]),
    ("07-pat/04-filled.png", [
        (480, 250, 960, 500, "确认后生成"),
    ]),
    ("07-pat/05-created.png", [
        (480, 220, 960, 620, "⚠️ 明文只显示一次！立刻复制"),
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


def annotate(src: Path, boxes: list[tuple[int, int, int, int, str]], dest: Path) -> None:
    im = Image.open(src).convert("RGBA")
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = get_font(22)
    font_sm = get_font(18)
    for x1, y1, x2, y2, label in boxes:
        # translucent fill
        draw.rectangle([x1, y1, x2, y2], outline=(239, 68, 68, 255), width=4)
        draw.rectangle([x1, y1, x2, y2], fill=(239, 68, 68, 35))
        # label pill
        tw, th = draw.textbbox((0, 0), label, font=font_sm)[2:]
        pad = 8
        ly1 = max(8, y1 - th - pad * 2 - 4)
        lx2 = min(im.width - 8, x1 + tw + pad * 2)
        draw.rounded_rectangle([x1, ly1, lx2, ly1 + th + pad * 2], radius=6, fill=(239, 68, 68, 230))
        draw.text((x1 + pad, ly1 + pad - 1), label, fill=(255, 255, 255, 255), font=font_sm)
    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=92)
    print("annotated", dest.relative_to(ROOT))


def main() -> None:
    for rel, boxes in ANNOTATIONS:
        src = SRC / rel
        if not src.exists():
            print("SKIP missing", rel)
            continue
        dest = OUT / rel
        annotate(src, boxes, dest)
    print("done", len(ANNOTATIONS))


if __name__ == "__main__":
    main()
