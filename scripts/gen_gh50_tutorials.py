#!/usr/bin/env python3
"""Analyze AI_WORK clones and generate 20-day tutorials for 50 high-star GitHub projects."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from gen_ai_work_missing_tutorials import (
    STAGE_NAMES,
    project,
    render_day,
    render_hub,
)

ROOT = Path(__file__).resolve().parents[1]
AI_WORK = Path("/Users/bitmart/work/codes/github/AI_WORK")
META = ROOT / "scripts" / "gh50_projects.json"

SKIP_DIR = {
    ".git", "node_modules", "dist", "build", "out", "target", "__pycache__",
    ".venv", "venv", "vendor", "coverage", ".next", ".turbo", ".cache",
    "fixtures", "testdata", "snapshots", "static", "public", "assets",
    "images", "img", "fonts", "locales", "i18n", "changelog",
}
CODE_EXT = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".cs",
    ".kt", ".md", ".toml", ".yaml", ".yml", ".json",
}
SKIP_FILE_PARTS = ("lock", "min.js", "bundle", ".map", "package-lock", "pnpm-lock", "yarn.lock")

KEYWORD_WEIGHT = [
    (r"(^|/)(main|cli|app|server|index)\.(py|ts|tsx|js|go|rs)$", 40),
    (r"(^|/)(agent|agents|agentic)(/|$)", 28),
    (r"(^|/)(tool|tools|toolkit)(/|$)", 24),
    (r"(^|/)(mcp)(/|$|\.)", 26),
    (r"(^|/)(memory|memories|remember)(/|$)", 24),
    (r"(^|/)(llm|model|models|provider)(/|$)", 22),
    (r"(^|/)(workflow|flow|graph|pipeline|orchestr)(/|$)", 22),
    (r"(^|/)(runtime|executor|engine|loop|runner)(/|$)", 22),
    (r"(^|/)(retriev|rag|embed|vector|index)(/|$)", 20),
    (r"(^|/)(prompt|message|schema|state|session)(/|$)", 18),
    (r"(^|/)(browser|sandbox|plugin|skill|connector)(/|$)", 18),
    (r"(^|/)(config|settings|env)(/|$|\.)", 14),
    (r"(^|/)(example|examples|demo|tutorial)(/|$)", 12),
    (r"README\.md$", 35),
    (r"(package\.json|pyproject\.toml|Cargo\.toml|go\.mod)$", 30),
]

ROLE_HINTS = [
    ("入口地图", ["readme", "package", "pyproject", "cargo", "go.mod", "main", "cli", "app", "index", "cmd"]),
    ("核心循环", ["agent", "runtime", "executor", "engine", "loop", "runner", "core", "orchestr"]),
    ("核心能力", ["tool", "workflow", "flow", "graph", "pipeline", "browser", "plugin", "skill", "node"]),
    ("状态协作", ["memory", "state", "message", "schema", "session", "store", "db", "cache"]),
    ("模型扩展", ["llm", "model", "provider", "mcp", "prompt", "rag", "retriev", "embed", "server"]),
    ("复盘扩展", ["example", "demo", "test", "integration", "extension", "contrib", "sdk"]),
]

ANALOGY_BANK = {
    "readme": "项目说明书前台",
    "package": "物料清单与依赖货架",
    "config": "控制室面板",
    "main": "上班打卡入口",
    "agent": "会决策的岗位员工",
    "tool": "工具柜里的标准件",
    "memory": "档案室与便签墙",
    "llm": "外接大脑总机",
    "mcp": "标准化工具插座",
    "workflow": "流水线调度台",
    "runtime": "工位运转机芯",
    "browser": "会点网页的双手",
    "rag": "先查资料再作答的图书员",
    "example": "样板间参观路线",
}


def detect_stack(root: Path) -> str:
    tags = []
    if (root / "pyproject.toml").exists() or (root / "setup.py").exists() or list(root.glob("**/requirements*.txt"))[:1]:
        tags.append("Python")
    if (root / "package.json").exists() or (root / "pnpm-workspace.yaml").exists():
        tags.append("TypeScript")
    if (root / "go.mod").exists():
        tags.append("Go")
    if (root / "Cargo.toml").exists():
        tags.append("Rust")
    if (root / "pom.xml").exists() or list(root.glob("**/*.csproj"))[:1]:
        tags.append("Java/.NET" if (root / "pom.xml").exists() else "C#")
    return " + ".join(dict.fromkeys(tags)) or "Multi"


NOISE_PARTS = (
    "terraform", "deploy/", "deployment", "docker/", "helm/", "charts/",
    "benchmark", "benchmarks", "third_party", "vendor/", "website/",
    "docs/img", "docs/images", "changelo", "migration", "migrations",
    "proto/", "generated/", ".github/", "codex-rs/", "schema/typescript",
)


def score_path(rel: str) -> int:
    low = rel.lower().replace("\\", "/")
    if any(p in low for p in SKIP_FILE_PARTS):
        return -100
    if any(p in low for p in NOISE_PARTS):
        return -50
    score = 0
    depth = low.count("/")
    score -= depth * 2
    for pat, w in KEYWORD_WEIGHT:
        if re.search(pat, low):
            score += w
    # Prefer source-ish roots
    if low.startswith(("src/", "packages/", "apps/", "lib/", "libs/", "pkg/", "crates/", "python/", "ts/",
                        "browser_use/", "aider/", "nanobot/", "lightrag/", "dspy/", "smolagents/",
                        "openai_agents/", "semantic_kernel/", "haystack/", "cognee/", "graphiti/",
                        "gpt_researcher/", "agentscope/", "fastmcp/", "composio/")):
        score += 10
    if low.endswith((".md",)) and "readme" not in low:
        score -= 6
    # Prefer shallower high-signal files
    if low in {"readme.md", "main.py", "app.py", "cli.py", "pyproject.toml", "package.json", "go.mod", "cargo.toml"}:
        score += 20
    return score


def collect_candidates(root: Path, limit: int = 200) -> list[tuple[int, str, bool]]:
    """Return scored (score, relpath, is_dir) candidates."""
    found: list[tuple[int, str, bool]] = []
    for path in root.rglob("*"):
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        parts = set(rel.split("/"))
        if parts & SKIP_DIR:
            continue
        if path.is_dir():
            if len(rel.split("/")) > 5:
                continue
            kids = list(path.iterdir())[:40]
            if not any(c.suffix in CODE_EXT or c.is_dir() for c in kids if c.name not in SKIP_DIR):
                continue
            sc = score_path(rel + "/")
            if sc >= 6:
                found.append((sc, rel, True))
        else:
            if path.suffix.lower() not in CODE_EXT and path.name not in {
                "README.md", "package.json", "pyproject.toml", "Cargo.toml", "go.mod",
            }:
                continue
            if len(rel.split("/")) > 7:
                continue
            sc = score_path(rel)
            if sc >= 4:
                found.append((sc, rel, False))
    found.sort(key=lambda x: (-x[0], x[1]))
    out = []
    seen = set()
    for sc, rel, is_dir in found:
        key = rel.rstrip("/")
        if key in seen:
            continue
        if any(s.startswith(key + "/") for s in seen) and is_dir:
            continue
        seen.add(key)
        out.append((sc, rel, is_dir))
        if len(out) >= limit:
            break
    # Ensure enough breadth: add shallow source files even with low scores
    if len(out) < 40:
        extras = []
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".go", ".rs", ".cs"}:
                continue
            rel = path.relative_to(root).as_posix()
            if set(rel.split("/")) & SKIP_DIR:
                continue
            if rel.count("/") > 4:
                continue
            if any(p in rel.lower() for p in NOISE_PARTS):
                continue
            if rel not in {x[1] for x in out}:
                extras.append((3, rel, False))
            if len(out) + len(extras) >= 60:
                break
        out.extend(extras)
    return out


def pick_role_path(cands: list[tuple[int, str, bool]], hints: list[str], used: set[str]) -> str | None:
    for sc, rel, _ in cands:
        if rel in used:
            continue
        low = rel.lower()
        if any(h in low for h in hints):
            used.add(rel)
            return rel
    for sc, rel, _ in cands:
        if rel not in used:
            used.add(rel)
            return rel
    return None


def analogy_for(path: str) -> str:
    low = path.lower()
    for key, text in ANALOGY_BANK.items():
        if key in low:
            return text
    base = Path(path).name
    return f"专门负责 {base} 的工位"


def title_for(day: int, path: str, role: str) -> str:
    name = Path(path).name
    templates = [
        f"从 {name} 认识项目大门",
        f"配置与依赖：{name}",
        f"顶层入口与启动路径",
        f"核心对象：{name}",
        f"运转循环里的 {name}",
        f"协作主线穿过 {name}",
        f"能力模块：{name}",
        f"业务动作落在 {name}",
        f"把任务交给 {name}",
        f"扩展点附近的 {name}",
        f"状态如何进入 {name}",
        f"消息与协作：{name}",
        f"持久化视角下的 {name}",
        f"模型侧连接：{name}",
        f"工具/MCP 桥：{name}",
        f"检索与知识：{name}",
        f"集成层：{name}",
        f"样例与复盘：{name}",
        f"测试与边界：{name}",
        f"收官：沿 {name} 串回全图",
    ]
    return templates[day - 1]


def blurb_for(path: str, role: str) -> str:
    return f"打开相对路径 <code>暂替</code>".replace("<code>暂替</code>", "") + f"跟踪 {path} 在「{role}」阶段的输入、输出与邻居依赖。"


def build_layers(paths: list[str]) -> list[tuple[str, list[str]]]:
    buckets = defaultdict(list)
    for p in paths:
        low = p.lower()
        if any(k in low for k in ("readme", "package", "main", "cli", "app", "cmd")):
            buckets["接入层"].append(Path(p).name)
        elif any(k in low for k in ("agent", "runtime", "executor", "engine", "loop")):
            buckets["编排层"].append(Path(p).name)
        elif any(k in low for k in ("tool", "workflow", "browser", "plugin", "flow")):
            buckets["能力层"].append(Path(p).name)
        elif any(k in low for k in ("memory", "state", "message", "store", "rag")):
            buckets["状态层"].append(Path(p).name)
        else:
            buckets["扩展层"].append(Path(p).name)
    order = ["接入层", "编排层", "能力层", "状态层", "扩展层"]
    layers = []
    for name in order:
        items = list(dict.fromkeys(buckets[name]))[:4] or ["模块"]
        layers.append((name, items))
    return layers


def first_existing(root: Path, names: list[str]) -> str | None:
    for name in names:
        if (root / name).exists():
            return name
    return None


def top_source_dirs(root: Path) -> list[str]:
    prefer = [
        "src", "lib", "libs", "app", "apps", "packages", "pkg", "crates",
        "python", "ts", "backend", "server", "core", "agent", "agents",
        "browser_use", "aider", "nanobot", "lightrag", "dspy", "smolagents",
        "openai", "semantic_kernel", "haystack", "cognee", "graphiti",
        "gpt_researcher", "agentscope", "fastmcp", "composio", "litellm",
        "cmd", "internal", "pkg",
    ]
    out = []
    for name in prefer:
        p = root / name
        if p.is_dir():
            out.append(name)
    # also include shallow high-score dirs
    for child in sorted(root.iterdir()):
        if child.is_dir() and child.name not in SKIP_DIR and child.name not in out:
            if score_path(child.name + "/") >= 14:
                out.append(child.name)
        if len(out) >= 12:
            break
    return out


def curriculum_for(meta: dict, root: Path) -> dict:
    cands = collect_candidates(root)
    used: set[str] = set()

    def take_unique(candidates: list[str], n: int) -> list[str]:
        out: list[str] = []
        for c in candidates:
            if not c or c in out or c in used:
                continue
            if c != "README.md" and not (root / c).exists():
                continue
            out.append(c)
            if len(out) >= n:
                break
        return out

    early_pool = [
        first_existing(root, ["README.md", "README.rst", "Readme.md", "readme.md"]),
        first_existing(root, ["pyproject.toml", "package.json", "Cargo.toml", "go.mod", "setup.py"]),
        first_existing(root, [
            "main.py", "app.py", "cli.py", "index.ts", "index.js", "src/index.ts",
            "src/main.py", "cmd", "apps", "packages", "src", "lib", "crates",
            "backend", "server", "python", "haystack", "dspy", "aider", "browser_use",
        ]),
        *top_source_dirs(root),
        *[rel for _, rel, _ in cands],
    ]
    focus_paths = take_unique([x for x in early_pool if x], 3)
    while len(focus_paths) < 3:
        # extremely small repos: reuse with stage-specific subcopy note via sibling files
        for _, rel, _ in cands:
            if rel not in focus_paths:
                focus_paths.append(rel)
                break
        else:
            focus_paths.append(focus_paths[-1] if focus_paths else "README.md")
            break
    focus_paths = focus_paths[:3]
    used.update(focus_paths)

    for day in range(4, 21):
        stage_idx = next(i for i, (_, lo, hi, _) in enumerate(STAGE_NAMES) if lo <= day <= hi)
        hints = ROLE_HINTS[stage_idx][1]
        path = pick_role_path(cands, hints, used)
        if not path:
            for td in top_source_dirs(root):
                if td not in used:
                    path = td
                    break
        if not path:
            for _, rel, _ in cands:
                if rel not in used:
                    path = rel
                    break
        if not path:
            # last resort: any unused shallow code file
            for pth in root.rglob("*"):
                if not pth.is_file() or pth.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".go", ".rs"}:
                    continue
                rel = pth.relative_to(root).as_posix()
                if set(rel.split("/")) & SKIP_DIR or rel in used or rel.count("/") > 5:
                    continue
                path = rel
                break
        path = path or focus_paths[0]
        used.add(path)
        focus_paths.append(path)

    day_rows = []
    for day, path in enumerate(focus_paths, 1):
        stage_idx = next(i for i, (_, lo, hi, _) in enumerate(STAGE_NAMES) if lo <= day <= hi)
        role_name = STAGE_NAMES[stage_idx][0]
        day_rows.append((
            title_for(day, path, role_name),
            path,
            analogy_for(path),
            f"围绕 {path} 建立因果链：谁调用、处理什么、交给谁；对应阶段是「{role_name}」。",
        ))
    stack = detect_stack(root)
    return project(
        meta["prefix"],
        meta["dir"],
        meta["title"],
        meta["one_liner"],
        meta["analogy"],
        tuple(meta["colors"]),
        meta["logo"],
        stack,
        day_rows,
        build_layers(focus_paths),
    )


CAT_LABEL = {
    "platform": "LLM 应用平台",
    "framework": "编排与框架",
    "multi": "多智能体",
    "auto": "自主 / 编码 Agent",
    "memory": "Agent 记忆",
    "tools": "AI 编程工具",
    "mcp": "MCP",
    "eval": "评测 · 治理",
}


def card_html(proj: dict, meta: dict) -> str:
    c1, c2 = proj["colors"]
    cat = meta["cat"]
    level = meta["level"]
    lang = proj["lang_stack"].split(" + ")[0]
    title = f'{proj["title"]} 源码学习（20 天）'
    desc = proj["one_liner"]
    cat_label = CAT_LABEL.get(cat, cat)
    search = f"{title} {desc} {cat_label} {level} {lang} 20 天".lower()
    return f'''<a class="blog-card" href="{proj["prefix"]}-tutorial.html" data-ps="{proj["prefix"]}" data-pd="20" data-cat="{cat}" data-level="{level}" data-lang="{lang}" data-area="ai" data-title="{title}" data-desc="{desc}" data-search="{search}">
  <div class="card-top"><div class="blog-card-icon" style="background:linear-gradient(135deg,{c1},{c2});">{proj["logo"]}</div></div>
  <h3>{title}</h3>
  <p class="blog-desc">{desc}</p>
  <div class="blog-card-tags"><span class="blog-tag">{cat_label}</span><span class="blog-tag">{proj["lang_stack"]}</span><span class="blog-tag">20 天</span></div>
  <div class="blog-card-arrow">查看教程 &rarr;</div>
</a>'''


def patch_index(cards: list[str]) -> bool:
    """Idempotent: strip any existing gh50 cards, then insert once before gov-agents (or grid start)."""
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    if 'data-filter="mcp"' not in text:
        text = text.replace(
            'data-filter="tools">AI 编程工具</button>',
            'data-filter="tools">AI 编程工具</button><button type="button" class="filter-chip" data-filter="mcp">MCP</button>',
            1,
        )
    metas = json.loads(META.read_text(encoding="utf-8"))
    for meta in metas:
        prefix = meta["prefix"]
        pat = re.compile(
            rf'<a class="blog-card" href="{re.escape(prefix)}-tutorial\.html"[\s\S]*?</a>\n?',
            re.M,
        )
        text = pat.sub("", text)
    block = "\n".join(cards) + "\n"
    marker = '            <a class="blog-card" href="gov-agents-tutorial.html"'
    if marker in text:
        text = text.replace(marker, block + marker, 1)
    else:
        marker2 = '<div class="blog-grid" id="lib-grid">'
        at = text.find(marker2)
        if at < 0:
            raise RuntimeError("无法在 index.html 找到插入点")
        at += len(marker2)
        text = text[:at] + "\n" + block + text[at:]
    index.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    metas = json.loads(META.read_text(encoding="utf-8"))
    generated = []
    missing = []
    cards = []
    for meta in metas:
        root = AI_WORK / meta["dir"]
        if not root.exists():
            missing.append(meta["fullName"])
            print("MISSING clone:", meta["fullName"])
            continue
        proj = curriculum_for(meta, root)
        (ROOT / f'{proj["prefix"]}-tutorial.html').write_text(render_hub(proj), encoding="utf-8")
        for day in range(1, 21):
            (ROOT / f'{proj["prefix"]}-day{day:02}.html').write_text(render_day(proj, day), encoding="utf-8")
        cards.append(card_html(proj, meta))
        generated.append(proj["prefix"])
        print(f"OK {proj['prefix']} stack={proj['lang_stack']} day1={proj['days'][0]['focus']}")
    if cards:
        patch_index(cards)
    # write analysis summary
    summary = ROOT / "scripts" / "gh50_generate_summary.json"
    summary.write_text(json.dumps({"generated": generated, "missing": missing, "count": len(generated)}, indent=2), encoding="utf-8")
    print(f"Generated {len(generated)} / {len(metas)}; missing={len(missing)}")


if __name__ == "__main__":
    main()
