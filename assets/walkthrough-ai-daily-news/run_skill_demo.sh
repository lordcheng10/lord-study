#!/usr/bin/env bash
# Skill 引导全流程演示 · 逐步落 log（供截图）
set -euo pipefail
LOGDIR="/Users/bitmart/work/codes/github/lord-study/assets/walkthrough-ai-daily-news/logs"
TMP="/Users/bitmart/work/codes/tmp"
AGENT="$TMP/ai-daily-news"
mkdir -p "$LOGDIR"

echo "=== B · 在 Cursor 触发 Skill（示意）===" > "$LOGDIR/step-trigger-skill.log"
cat >> "$LOGDIR/step-trigger-skill.log" <<'EOF'
用户: 按 standalone-repo-agent skill，帮我在独立仓做「AI 最新资讯每日播报」agent，名 ai-daily-news。

Agent 读取 ~/.cursor/skills/standalone-repo-agent/SKILL.md
→ 开始执行 Skill 步骤 0 …
EOF

{
  echo "=== Skill 步骤 0 · 环境检查 ==="
  echo "# SKILL.md: python3 --version · uv --version"
  python3 --version
  uv --version
} | tee "$LOGDIR/step00-env.log"

{
  echo "=== Skill 步骤 1 · 起仓（Skill 规定：平台直链下模板 + 改名）==="
  echo "# Agent 按 SKILL 步骤 1 执行以下命令"
  cd "$TMP"
  curl -fL http://gov-agents-ui.bmaicsaws-prod.com/portal/v1/agent-template/download.zip -o /tmp/ai-daily-tpl.zip
  rm -rf ai-daily-news
  unzip -o /tmp/ai-daily-tpl.zip -d /tmp/ai-daily-unzip
  mv /tmp/ai-daily-unzip/standalone-agent-template ai-daily-news
  cd ai-daily-news
  mv your_agent ai_daily_news
  grep -rl 'your[-_]agent' . | xargs sed -i '' 's/your-agent/ai-daily-news/g; s/your_agent/ai_daily_news/g'
  git init -q && git add -A && git commit -m "init ai-daily-news" -q
  echo ""
  echo "=== 验证（Skill 步骤 1 期望）==="
  grep -r your_agent . 2>/dev/null | head -1 || echo "grep your_agent: clean ✓"
  ls ai_daily_news/builder.py
  grep '^name =' pyproject.toml | head -1
} | tee "$LOGDIR/step01-skill-create.log"

{
  echo "=== Skill 步骤 2 · Nexus 凭据 ==="
  echo "# SKILL.md: ~/.netrc 配 pypi_pull（本机已配置则跳过写入）"
  grep nexus.bitmartpro.com ~/.netrc | sed 's/password .*/password ******/' || echo "netrc 未找到"
} | tee "$LOGDIR/step02-nexus.log"

{
  echo "=== Skill 步骤 3 · uv sync + 首次跑通 ==="
  cd "$AGENT"
  cp .env.example .env
  uv sync 2>&1 | tail -6
  echo ""
  uv run ai-daily-news run "你好"
} | tee "$LOGDIR/step03-first-run.log"

echo "done phase create" 
