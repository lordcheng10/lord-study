#!/usr/bin/env python3
"""Generate beginner-friendly Coze Loop practice HTML: step → detail → annotated shot."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSS = """
.content{max-width:1100px}
.step-hdr{display:flex;align-items:center;gap:10px;margin:32px 0 12px}
.step-hdr .badge{width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,#06b6d4,#4f46e5);color:#fff;font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.step-hdr h2{margin:0;font-size:18px}
.why{background:rgba(6,182,212,.07);border-left:3px solid #22d3ee;border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:13px;color:var(--text-secondary);line-height:1.75}
.why b{color:#67e8f9}
.shot{display:block;width:100%;max-width:960px;border-radius:10px;border:1px solid var(--border-color);margin:14px 0 4px;box-shadow:0 8px 24px rgba(0,0,0,.25)}
.shot-cap{font-size:12.5px;color:var(--text-muted);margin:0 0 16px;line-height:1.6}
.verify{font-size:13px;color:var(--accent-green);margin-top:12px;padding:10px 12px;background:rgba(34,197,94,.06);border-radius:8px;border-left:3px solid var(--accent-green);line-height:1.7}
.pitfall{border-left:3px solid #ef4444;background:rgba(239,68,68,.07);border-radius:0 8px 8px 0;padding:10px 14px;margin:12px 0 0;font-size:13px;line-height:1.7}
.pitfall .t{font-weight:700;color:#f87171;display:block;margin-bottom:4px}
.warn-box{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.35);border-radius:8px;padding:11px 14px;margin:10px 0;font-size:13px;line-height:1.7}
.subh{font-size:14px;color:#67e8f9;margin:14px 0 6px}
.steps-ol{font-size:13.5px;color:var(--text-secondary);line-height:1.9;padding-left:20px;margin:0}
.steps-ol li{margin:4px 0}
.chip{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;margin-right:6px;border:1px solid var(--border-color)}
.chip.on{background:rgba(34,197,94,.12);color:#4ade80;border-color:rgba(34,197,94,.35)}
.fileref{display:inline-block;font-size:11px;background:rgba(6,182,212,.12);color:#67e8f9;border:1px solid rgba(6,182,212,.35);border-radius:5px;padding:1px 7px;font-family:ui-monospace,monospace}
.ctable{width:100%;border-collapse:collapse;margin:10px 0;font-size:12.5px}
.ctable th,.ctable td{border:1px solid var(--border-color);padding:8px 10px;text-align:left;vertical-align:top;line-height:1.55}
.ctable th{background:var(--bg-secondary);color:var(--accent-cyan)}
"""

LESSONS = [
    {
        "logo": "P00",
        "file": "coze-loop-practice-00-setup.html",
        "title": "环境启动 · 注册登录 · 侧栏导览",
        "mins": "25 min",
        "desc": "把本地服务跑起来、注册账号、认识侧栏。后面所有课都依赖本课。",
        "nav_steps": [
            ("#prep", "0 前置条件"),
            ("#s1", "1 启动服务"),
            ("#s2", "2 配置 Claude 模型"),
            ("#s3", "3 注册登录"),
            ("#s4", "4 认识侧栏"),
            ("#s5", "5 账户菜单"),
        ],
        "body": r'''
  <section id="prep" class="section">
    <div class="step-hdr"><div class="badge">0</div><h2>前置条件（先核对再动手）</h2></div>
    <div class="card">
      <table class="ctable">
        <tr><th>项</th><th>你需要准备什么</th></tr>
        <tr><td>电脑</td><td>已安装 <strong>Docker Desktop</strong>，并处于 Running（菜单栏有鲸鱼图标）</td></tr>
        <tr><td>内存</td><td>Docker 建议分配 ≥ 8～12GB（越小越容易中途挂掉）</td></tr>
        <tr><td>代码</td><td>已 clone <code>coze-loop</code> 仓库到本机</td></tr>
        <tr><td>模型 Key</td><td>Anthropic Claude API Key（本教程实录用 Claude；也可用其它协议）</td></tr>
        <tr><td>浏览器</td><td>Chrome / Edge 最新版</td></tr>
      </table>
      <div class="warn-box">本课不把模型配好，后面「运行调试 / 实验」都会失败。密钥只放在服务器配置文件里，开源版<strong>没有</strong>网页版「模型管理」。</div>
    </div>
  </section>

  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>启动本地 Coze Loop</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>用 Docker Compose 拉起前端、后端和 MySQL / Redis / ClickHouse / RocketMQ 等中间件。浏览器入口是 <span class="fileref">http://localhost:8082</span>。</div>
      <p class="subh">1.1 打开终端，进入仓库根目录</p>
<pre><code class="language-bash"># 路径换成你自己 clone 的位置
cd /path/to/coze-loop
# 确认能看到 Makefile
ls Makefile</code></pre>
      <p class="subh">1.2（可选）避开端口冲突</p>
      <ol class="steps-ol">
        <li>若本机 <code>8888</code> 已被占用（例如同时跑 Coze Studio），编辑 <code>release/deployment/docker-compose/.env</code></li>
        <li>把 <code>COZE_LOOP_APP_OPENAPI_PORT=8888</code> 改成 <code>8889</code>（只影响 OpenAPI，网页仍是 8082）</li>
      </ol>
      <p class="subh">1.3 一键启动</p>
<pre><code class="language-bash">make compose-up
# 第一次会拉镜像，可能要几分钟到十几分钟
# 看到服务起来后，浏览器打开：
open http://localhost:8082</code></pre>
      <div class="verify">✅ 验收：浏览器打开 <code>http://localhost:8082</code> 能看到「欢迎使用扣子罗盘-开源版」登录页，而不是「无法访问此网站」。</div>
      <div class="pitfall"><span class="t">常见卡点</span>
      RocketMQ 被杀掉（exit 137）：Docker 内存不够，先停掉其它容器再启动。<br>
      端口占用：改 <code>.env</code> 里相关端口后重启。
      </div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>配置 Claude 模型（必做）</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>告诉后端「用哪家大模型、Key 是什么」。界面上只能<strong>选择</strong>已配置好的模型，不能在网页里粘贴 Key。</div>
      <ol class="steps-ol">
        <li>用编辑器打开文件：<code>release/deployment/docker-compose/conf/model_config.yaml</code></li>
        <li>可参考同目录 <code>model_config_example/claude.yaml</code> 整份复制后改</li>
        <li>关键字段：
          <ul>
            <li><code>protocol: "claude"</code></li>
            <li><code>protocol_config.api_key</code>：你的 Anthropic Key（以 <code>sk-ant-</code> 开头）</li>
            <li><code>protocol_config.model</code>：例如 <code>claude-sonnet-4-5</code></li>
            <li><code>ability.function_call: true</code>（评估器需要）</li>
          </ul>
        </li>
        <li><strong>重要：</strong><code>param_schemas</code> 里<strong>不要同时</strong>配置 <code>temperature</code> 和 <code>top_p</code>。Claude 新模型同时传会返回 400。建议只保留 <code>temperature</code> + <code>max_tokens</code>。</li>
        <li>保存后重启应用容器：
<pre><code class="language-bash">docker compose \
  -f release/deployment/docker-compose/docker-compose.yml \
  --env-file release/deployment/docker-compose/.env \
  restart app</code></pre>
        </li>
      </ol>
      <div class="verify">✅ 验收：重启后进 Prompt 调试页，「模型配置」下拉里能看到你配置的名称（如 Claude Sonnet）。</div>
      <div class="pitfall"><span class="t">安全提醒</span>
      Key 不要提交到 Git。演示完建议到 Anthropic 控制台轮换 Key。
      </div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>注册并登录</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>开源版用邮箱自建账号；注册成功后自动进入 Personal Space。</div>
      <ol class="steps-ol">
        <li>浏览器打开 <span class="fileref">http://localhost:8082</span>，若未登录会跳到 <code>/auth/login</code></li>
        <li>在「请输入邮箱」框填一个邮箱（本地演示可用任意格式，如 <code>demo@example.com</code>）</li>
        <li>在「请输入密码」框填密码（自己记住即可）</li>
        <li><strong>第一次</strong>：点灰色按钮 <strong>注册</strong>；以后再来点紫色按钮 <strong>登录</strong></li>
        <li>成功后地址栏会变成类似 <code>/console/enterprise/personal/space/一长串数字/pe/prompts</code></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/01-login.png" alt="登录页标注">
      <p class="shot-cap">图：登录页。红框①邮箱 ②密码 ③注册 ④登录 —— 新手第一次请点「注册」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/02-login-filled.png" alt="已填写">
      <p class="shot-cap">图：填好后点「注册」。若提示邮箱已存在，改邮箱或改用「登录」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/03-home-prompts.png" alt="进入首页">
      <p class="shot-cap">图：注册成功后的 Prompt 开发首页。左侧是导航，右侧是主工作区。</p>
      <div class="verify">✅ 验收：能看到左侧导航和「Prompt 开发」空列表 / 欢迎插画，不再停留在登录页。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>认识左侧导航（地图）</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>后面每一课都从侧栏进模块。先认门，再学操作。</div>
      <table class="ctable">
        <tr><th>侧栏文字</th><th>你能做什么</th><th>对应课</th></tr>
        <tr><td>Prompt 开发</td><td>创建 / 编辑 / 调试 / 提交版本</td><td>P01</td></tr>
        <tr><td>Playground</td><td>不落库的快速试跑</td><td>P01</td></tr>
        <tr><td>评测集</td><td>准备测试数据表</td><td>P02</td></tr>
        <tr><td>评估器</td><td>LLM / Code 自动打分</td><td>P03</td></tr>
        <tr><td>实验</td><td>把数据 + 对象 + 评估器跑一遍</td><td>P04</td></tr>
        <tr><td>Trace</td><td>看每次调用的链路与耗时</td><td>P05</td></tr>
        <tr><td>标签管理</td><td>人工标注用的标签体系</td><td>P06</td></tr>
      </table>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/04-sidebar.png" alt="侧栏标注">
      <p class="shot-cap">图：侧栏模块位置。从上到下依次对应 Prompt → 评测 → 观测 → 标签。</p>
      <div class="verify">✅ 验收：你能用手指指出「评测集」「Trace」分别在哪一行。</div>
    </div>
  </section>

  <section id="s5" class="section">
    <div class="step-hdr"><div class="badge">5</div><h2>账户菜单与设置入口</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>找「账户设置 / API 授权 / 退出登录」。PAT 在 P07 细讲。</div>
      <ol class="steps-ol">
        <li>看侧栏<strong>最底部</strong>：有你的头像 / 用户名</li>
        <li>用鼠标<strong>点一下</strong>头像区域，弹出菜单</li>
        <li>菜单里有：<strong>账户设置</strong>、<strong>退出登录</strong>（文案是「账户」不是「账号」）</li>
        <li>点「账户设置」会弹出大窗口，左侧可切换「账户设置 / API 授权」</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/05-user-menu.png" alt="用户菜单">
      <p class="shot-cap">图：左下角头像 → 弹出「账户设置 / 退出登录」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/06-account-modal.png" alt="账户弹窗">
      <p class="shot-cap">图：账户设置弹窗。左侧可切到「API 授权」创建 PAT（见 P07）。</p>
      <div class="verify">✅ 验收：能打开账户设置弹窗，再按 Esc 或点右上角 × 关闭。</div>
    </div>
  </section>
''',
    },
    {
        "logo": "P01",
        "file": "coze-loop-practice-01-prompt.html",
        "title": "Prompt 开发 · Claude 调试 · Playground",
        "mins": "35 min",
        "desc": "从零创建一个 Prompt，选 Claude 跑通调试，提交版本，再到 Playground 试跑。",
        "nav_steps": [
            ("#s1", "1 打开列表"),
            ("#s2", "2 创建 Prompt"),
            ("#s3", "3 写模板"),
            ("#s4", "4 选模型并运行"),
            ("#s5", "5 提交版本"),
            ("#s6", "6 Playground"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开 Prompt 开发列表</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>进入 Prompt 的「家」。所有 Prompt 都在这里创建和管理。</div>
      <ol class="steps-ol">
        <li>确认已登录（P00 完成）</li>
        <li>左侧侧栏点 <strong>Prompt 开发</strong>（第一项，通常默认就在这里）</li>
        <li>若是空账号，中间会显示「暂无 Prompt」和插画</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/01-list-empty.png" alt="空列表">
      <p class="shot-cap">图：空列表。右上角红框是「创建 Prompt」——下一步要点它。</p>
      <div class="verify">✅ 验收：面包屑显示「Prompt 工程 / Prompt 开发」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>创建空白 Prompt</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>新建一个可保存的 Prompt 草稿，并进入三栏调试页。</div>
      <ol class="steps-ol">
        <li>点右上角蓝色按钮 <strong>+ 创建 Prompt</strong></li>
        <li>弹出菜单里选 <strong>空白 Prompt</strong>（不要点空白处关掉菜单）</li>
        <li>在弹窗中填写：
          <ul>
            <li><strong>Prompt Key</strong>（必填）：英文开头，只能字母数字下划线点。例：<code>demo_greeting</code></li>
            <li><strong>Prompt 名称</strong>（必填）：中文也行。例：<code>Claude问候演示</code></li>
            <li><strong>Prompt 描述</strong>（可选）：写一句用途说明</li>
          </ul>
        </li>
        <li>点右下角 <strong>确认</strong></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/02-create-menu.png" alt="创建菜单">
      <p class="shot-cap">图：创建按钮下拉 → 选「空白 Prompt」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/03-create-dialog.png" alt="创建弹窗">
      <p class="shot-cap">图：创建弹窗。Key 格式错了会红字提示，按规则改即可。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/04-create-filled.png" alt="填好确认">
      <p class="shot-cap">图：填好后点「确认」，进入开发页。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/05-develop.png" alt="三栏布局">
      <p class="shot-cap">图：开发页三栏——左模板 / 中模型参数 / 右预览调试。先认清布局再填内容。</p>
      <div class="verify">✅ 验收：顶部出现 Prompt 名称，中间有「请选择模型」，右侧有「运行」按钮（可能暂时灰掉）。</div>
      <div class="pitfall"><span class="t">Key 报错？</span>
      必须以英文字母开头；不能有空格或中文。例如 <code>1abc</code>、<code>我的prompt</code> 都不行。
      </div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>写 System / User 消息模板</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>告诉模型「你是谁、用户说什么」。空内容直接运行会被 Claude 拒绝（400）。</div>
      <ol class="steps-ol">
        <li>在左栏找到标着 <strong>System</strong> 的输入框</li>
        <li>点进去，输入例如：<code>你是礼貌助手。请用一句中文问候用户。</code></li>
        <li>若还没有 User 消息：点 <strong>+ 添加消息</strong>，角色选 User（或默认追加）</li>
        <li>在 User 框输入例如：<code>我叫小明</code></li>
        <li>也可以用变量写法：<code>{{user_name}}</code>（后面再在变量区赋值）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/06-edit-template.png" alt="编辑模板">
      <p class="shot-cap">图：System / User 写在左栏。红框标出两处输入位置。</p>
      <div class="verify">✅ 验收：System 框不再是灰色占位符「请输入内容…」，而是你的真实文字。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>选择 Claude 并点击运行</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>把后端已配置的 Claude 挂到当前 Prompt，真正调用一次大模型。</div>
      <ol class="steps-ol">
        <li>看中间栏 <strong>模型配置</strong></li>
        <li>点「请选择模型」下拉</li>
        <li>在列表里点 <strong>Claude Sonnet</strong>（名称以你在 yaml 里写的 <code>name</code> 为准）</li>
        <li>参数区会出现 <code>max_tokens</code>、<code>temperature</code> 等滑条——新手可先不改</li>
        <li>到右栏底部输入框（可选）再写一句测试话，或直接依赖模板里的 User 消息</li>
        <li>点蓝色 <strong>运行</strong></li>
        <li>等待 2～10 秒，右栏应出现助手回复，并显示耗时与 Tokens</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/10-model-dropdown.png" alt="模型下拉">
      <p class="shot-cap">图：下拉列表里出现 Claude Sonnet —— 说明 P00 的 yaml 已生效。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/10-model-selected.png" alt="选好模型">
      <p class="shot-cap">图：①已选模型 ②参数 ③右下角「运行」。若运行是灰的，检查是否已选模型、消息是否为空。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/11-debug-result.png" alt="调试成功">
      <p class="shot-cap">图：成功示例——助手回复「你好，小明！…」，并显示耗时约 3s、Tokens。</p>
      <div class="verify">✅ 验收：右栏能看到中文问候回复，而不是报错红框或一直转圈。</div>
      <div class="pitfall"><span class="t">报错对照</span>
      <code>temperature and top_p cannot both be specified</code> → 回到 yaml 删掉其中一个参数后 restart app。<br>
      <code>system/user messages must have non-empty content</code> → 模板消息是空的，先写字再运行。<br>
      下拉没有模型 → yaml 没配好或 app 没重启。
      </div>
    </div>
  </section>

  <section id="s5" class="section">
    <div class="step-hdr"><div class="badge">5</div><h2>提交新版本</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>把当前草稿固化成可回滚的版本，方便实验引用、对比历史。</div>
      <ol class="steps-ol">
        <li>确认调试结果满意</li>
        <li>点顶部右侧紫色/蓝色按钮 <strong>提交新版</strong></li>
        <li>在弹窗填写版本号，例如 <code>0.0.1</code>（按你们团队规范即可）</li>
        <li>可写变更说明（可选）</li>
        <li>点确认 / 提交</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/07-submit-version.png" alt="提交弹窗">
      <p class="shot-cap">图：提交版本弹窗——填版本号后确认。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/12-version-done.png" alt="提交完成">
      <p class="shot-cap">图：提交后状态变化；可用「版本记录」查看历史。</p>
      <div class="verify">✅ 验收：顶部「修改未提交」提示消失或版本记录里出现新版本。</div>
    </div>
  </section>

  <section id="s6" class="section">
    <div class="step-hdr"><div class="badge">6</div><h2>用 Playground 快速试跑</h2></div>
    <div class="card">
      <div class="why"><b>这一步做什么？</b>Playground 像草稿纸：不必先创建正式 Prompt，也能选 Claude 试效果。</div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>Playground</strong></li>
        <li>左栏写 System（例：<code>用一句话介绍你自己：你是 Anthropic 的 Claude。</code>）</li>
        <li>中间选 <strong>Claude Sonnet</strong></li>
        <li>点右下角 <strong>运行</strong></li>
        <li>满意后可用顶部 <strong>快捷创建</strong> 存成正式 Prompt（可选）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/08-playground.png" alt="Playground">
      <p class="shot-cap">图：Playground 布局与开发页类似，但默认不落库。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/13-playground-result.png" alt="Playground 结果">
      <p class="shot-cap">图：成功回复示例——「我是 Claude，由 Anthropic 开发…」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/09-list-with-item.png" alt="列表面板">
      <p class="shot-cap">图：回到 Prompt 开发列表，能看到已创建的条目；「调用记录」可跳 Trace。</p>
      <div class="verify">✅ 验收：Playground 也能跑出模型回复；列表里至少有 1 条 Prompt。</div>
    </div>
  </section>
''',
    },
]

# Continue with P02-P07 in the same file - append to LESSONS
LESSONS += [
    {
        "logo": "P02",
        "file": "coze-loop-practice-02-dataset.html",
        "title": "评测集：建表 · 列配置 · 添加数据",
        "mins": "25 min",
        "desc": "建一张评测数据表（input / 参考答案），为后面的实验准备弹药。",
        "nav_steps": [
            ("#s1", "1 打开评测集"),
            ("#s2", "2 新建并填信息"),
            ("#s3", "3 看懂列配置"),
            ("#s4", "4 创建并进详情"),
            ("#s5", "5 添加数据行"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开评测集列表</h2></div>
    <div class="card">
      <div class="why"><b>评测集是什么？</b>一张「考试卷」：每一行是一道题（输入）和可选的参考答案。实验会按行跑模型再打分。</div>
      <ol class="steps-ol">
        <li>左侧侧栏找到分组 <strong>评测</strong></li>
        <li>点 <strong>评测集</strong></li>
        <li>注意按钮文案是 <strong>新建评测集</strong>（不是「创建」）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/01-list.png" alt="评测集列表">
      <p class="shot-cap">图：侧栏点「评测集」，右上角点「新建评测集」。</p>
      <div class="verify">✅ 验收：面包屑为「评测 / 评测集」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>填写名称与描述</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>点 <strong>新建评测集</strong> 进入表单页</li>
        <li><strong>名称</strong>（必填）：例如 <code>问候评测集</code>，最多约 50 字</li>
        <li><strong>描述</strong>（可选）：写清楚这张表用来测什么</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/02-create.png" alt="新建页全貌">
      <p class="shot-cap">图：新建页结构——上半基本信息，下半列配置，右下角「创建」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/03-named.png" alt="名称">
      <p class="shot-cap">图：名称是必填项，空着点创建会被拦住。</p>
      <div class="verify">✅ 验收：名称框有内容，字数计数在限制内。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>看懂默认列（Schema）</h2></div>
    <div class="card">
      <div class="why"><b>为什么要配列？</b>列 = 字段。后面评估器 / 实验都按列名取数。名字起错了，后面映射会对不上。</div>
      <ol class="steps-ol">
        <li>默认已有两列：
          <ul>
            <li><code>input</code>：投递给评测对象（模型）的输入</li>
            <li><code>reference_output</code>：期望的理想输出，可作评分参考</li>
          </ul>
        </li>
        <li>每列可设：数据类型（String 等）、是否必填、描述</li>
        <li>需要更多字段时点 <strong>添加列</strong></li>
        <li>新手第一张表：先用默认两列，不要改名</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/04-schema.png" alt="列配置">
      <p class="shot-cap">图：红框标出默认两列。先理解再改，避免实验阶段对不上字段。</p>
      <div class="verify">✅ 验收：你能说清 input 和 reference_output 各干什么。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>点「创建」进入详情</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>检查名称和列无误</li>
        <li>点页面右下角蓝色 <strong>创建</strong></li>
        <li>成功后进入评测集详情：可添加数据、看关联实验、提交版本</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/05-detail.png" alt="详情页">
      <p class="shot-cap">图：详情页。右上常见「添加数据」「新建实验」「版本记录」等按钮。</p>
      <div class="verify">✅ 验收：地址栏变成 <code>.../evaluation/datasets/一串数字</code>。</div>
    </div>
  </section>

  <section id="s5" class="section">
    <div class="step-hdr"><div class="badge">5</div><h2>添加至少一行数据</h2></div>
    <div class="card">
      <div class="why"><b>没有数据行，实验就是空跑。</b>至少加 1～3 行，方便后面验证。</div>
      <ol class="steps-ol">
        <li>在详情页点 <strong>添加数据</strong>（或「手动添加」类按钮）</li>
        <li>在弹出的抽屉 / 表单里：
          <ul>
            <li><code>input</code> 例：<code>你好，我叫小明</code></li>
            <li><code>reference_output</code> 例：<code>你好小明，很高兴认识你！</code></li>
          </ul>
        </li>
        <li>点确认 / 保存</li>
        <li>回到表格，应能看到新行</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/05-add-data.png" alt="添加数据">
      <p class="shot-cap">图：添加数据时的侧栏 / 弹层（界面可能随版本略有差异）。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/07-item-list.png" alt="数据列表">
      <p class="shot-cap">图：保存后数据出现在列表中。可再点「提交新版本」固化数据集版本。</p>
      <div class="verify">✅ 验收：表格里至少 1 行；后续建实验时能选到这个评测集。</div>
      <div class="pitfall"><span class="t">找不到「添加数据」？</span>
      确认你在<strong>详情页</strong>而不是列表页；列表页只有「新建评测集」。
      </div>
    </div>
  </section>
''',
    },
    {
        "logo": "P03",
        "file": "coze-loop-practice-03-evaluator.html",
        "title": "评估器：预置 · LLM · Code",
        "mins": "25 min",
        "desc": "学会看预置评估器，并创建 LLM / Code 两类自建评估器。",
        "nav_steps": [
            ("#s1", "1 打开评估器"),
            ("#s2", "2 浏览预置"),
            ("#s3", "3 创建 LLM 评估器"),
            ("#s4", "4 认识 Code 评估器"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开评估器列表</h2></div>
    <div class="card">
      <div class="why"><b>评估器是什么？</b>自动阅卷老师。可以是大模型打分（LLM），也可以是你写的规则代码（Code）。</div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>评估器</strong></li>
        <li>顶部通常有页签：<strong>自建</strong> / <strong>预置</strong></li>
        <li>右上角有新建入口</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/01-list.png" alt="评估器列表">
      <p class="shot-cap">图：评估器入口。先分清「自建」和「预置」两个页签。</p>
      <div class="verify">✅ 验收：面包屑为「评测 / 评估器」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>浏览预置评估器</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>点页签 <strong>预置</strong>（或「内置」）</li>
        <li>浏览卡片：常见如准确性、相关性等模板</li>
        <li>点进某张卡片可查看说明；可复制后改成自建</li>
        <li>新手建议：先看懂预置长什么样，再回去建自己的</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/02-builtin.png" alt="预置">
      <p class="shot-cap">图：预置评估器卡片墙。适合学习「评估器长什么样」。</p>
      <div class="verify">✅ 验收：你能打开至少一张预置评估器详情。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>创建 LLM 评估器并挂上 Claude</h2></div>
    <div class="card">
      <div class="why"><b>LLM 评估器</b>：让 Claude 当裁判，对「模型输出 vs 参考答案」打分或给评语。</div>
      <ol class="steps-ol">
        <li>回到「自建」页签，点 <strong>新建 / 创建</strong></li>
        <li>选择 <strong>LLM</strong>（或「大模型评估器」）</li>
        <li>填写评估器名称，例如 <code>礼貌度评估</code></li>
        <li>在模型配置里选择 <strong>Claude Sonnet</strong>（与 P01 相同来源）</li>
        <li>按页面提示编写评判 Prompt（说明如何打分、输出格式）</li>
        <li>保存 / 创建；可再点调试用样例试跑</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/04-create-menu.png" alt="新建菜单">
      <p class="shot-cap">图：新建时选择 LLM 或 Code。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/05-create-llm.png" alt="LLM 创建页">
      <p class="shot-cap">图：LLM 评估器编辑页（字段随版本可能略有不同）。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/07-llm-configured.png" alt="已选 Claude">
      <p class="shot-cap">图：评判模型同样选 Claude。评估器也依赖 function_call 能力，yaml 里请打开。</p>
      <div class="verify">✅ 验收：自建列表里出现你的评估器；模型下拉不是空的。</div>
      <div class="pitfall"><span class="t">评估器调试失败</span>
      与 P01 相同：检查 Key、temperature/top_p 冲突、消息是否为空。
      </div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>认识 Code 评估器</h2></div>
    <div class="card">
      <div class="why"><b>Code 评估器</b>：用 Python/JS 写确定性规则（相等、包含、正则）。不消耗 LLM，结果可复现。</div>
      <ol class="steps-ol">
        <li>新建 → 选 <strong>Code</strong></li>
        <li>进入代码编辑页，按模板写规则</li>
        <li>适合：精确匹配、格式检查；不适合：开放性语义打分（那用 LLM）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/06-create-code.png" alt="Code 评估器">
      <p class="shot-cap">图：Code 评估器页面。本地有 Python/JS FaaS 容器执行代码。</p>
      <div class="verify">✅ 验收：你知道 LLM 与 Code 评估器分别适合什么场景。</div>
    </div>
  </section>
''',
    },
    {
        "logo": "P04",
        "file": "coze-loop-practice-04-experiment.html",
        "title": "实验：五步向导从创建到启动",
        "mins": "30 min",
        "desc": "跟着向导把「评测集 +（可选）Prompt +（可选）评估器」组装成一次实验。",
        "nav_steps": [
            ("#s1", "1 打开实验"),
            ("#s2", "2 基本信息"),
            ("#s3", "3 选评测集"),
            ("#s4", "4 对象与评估器"),
            ("#s5", "5 确认启动"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开实验并点新建</h2></div>
    <div class="card">
      <div class="why"><b>实验是什么？</b>一次完整考试：用评测集的每一行，调用评测对象（如 Prompt），再用评估器打分。</div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>实验</strong></li>
        <li>点右上角 <strong>新建 / 创建实验</strong></li>
        <li>进入五步向导页，先看顶部进度条</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/01-list.png" alt="实验列表">
      <p class="shot-cap">图：实验列表入口。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/02-wizard.png" alt="向导">
      <p class="shot-cap">图：五步向导首页。红框标出进度条和第一步表单区。</p>
      <div class="verify">✅ 验收：能看到步骤条（基本信息 → 评测集 → …）。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>步骤1：基本信息</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>填写<strong>实验名称</strong>，例如 <code>问候实验-Claude</code></li>
        <li>描述可选</li>
        <li>点右下角 <strong>下一步</strong></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/03-basic.png" alt="基本信息">
      <p class="shot-cap">图：填名称后点「下一步」。</p>
      <div class="verify">✅ 验收：进度条高亮移到第 2 步。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>步骤2：选择评测集（必选）</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>在下拉 / 列表中选择你在 P02 创建的评测集</li>
        <li>若有版本，选择最新版本</li>
        <li>确认行数 &gt; 0（空集会导致实验无意义）</li>
        <li>点 <strong>下一步</strong></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/04-dataset-step.png" alt="选评测集">
      <p class="shot-cap">图：步骤2 选择评测集。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/04b-dataset-picked.png" alt="已选中">
      <p class="shot-cap">图：选中后的状态。看不到评测集？回 P02 确认已创建成功。</p>
      <div class="verify">✅ 验收：评测集名称显示在表单中，不是「请选择」。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>步骤3～4：评测对象与评估器（可跳过）</h2></div>
    <div class="card">
      <div class="why"><b>可跳过？</b>可以。只想先跑通流程：对象选你的 Prompt；评估器可暂不绑，之后人工看结果。</div>
      <ol class="steps-ol">
        <li><strong>步骤3 评测对象</strong>：选择 Prompt（P01 创建的），或按界面提示跳过</li>
        <li>若选 Prompt，通常还要选版本</li>
        <li><strong>步骤4 评估器</strong>：勾选 P03 的评估器，或跳过</li>
        <li>每步点 <strong>下一步</strong></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/05-target-step.png" alt="评测对象">
      <p class="shot-cap">图：步骤3 评测对象。选 Prompt 才会真正调用 Claude。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/06-evaluator-step.png" alt="评估器">
      <p class="shot-cap">图：步骤4 评估器。可多选；没有也可先进入确认页。</p>
      <div class="verify">✅ 验收：到达确认页（步骤5）。</div>
    </div>
  </section>

  <section id="s5" class="section">
    <div class="step-hdr"><div class="badge">5</div><h2>步骤5：确认并启动</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>核对：名称、评测集、对象、评估器</li>
        <li>点 <strong>启动实验 / 创建 / 提交</strong>（按钮文案因版本可能不同）</li>
        <li>等待任务从「运行中」变为完成</li>
        <li>进实验详情：表格看每行输出；Chart 看汇总</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/07-confirm.png" alt="确认启动">
      <p class="shot-cap">图：最后确认页。点启动后去喝口水，行数多会跑一会儿。</p>
      <div class="verify">✅ 验收：实验列表出现新记录；详情里能看到行级结果或状态。</div>
      <div class="pitfall"><span class="t">启动按钮点不了 / 失败</span>
      评测集为空；Prompt 未提交版本；模型 Key 无效；评估器配置不完整。先回 P01 确认调试能跑通。
      </div>
    </div>
  </section>
''',
    },
    {
        "logo": "P05",
        "file": "coze-loop-practice-05-trace.html",
        "title": "观测 Trace：找到 Claude 调用链",
        "mins": "20 min",
        "desc": "在 Trace 里找到 Prompt 调试产生的调用，看清耗时、Token 和输入输出。",
        "nav_steps": [
            ("#s1", "1 打开 Trace"),
            ("#s2", "2 调过滤器"),
            ("#s3", "3 看详情"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开 Trace</h2></div>
    <div class="card">
      <div class="why"><b>Trace 是什么？</b>每次 Prompt 运行的「黑匣子」：谁调用了谁、花了多久、输入输出是什么。</div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>Trace</strong></li>
        <li>若提示「暂无数据」：先去 P01 再点一次「运行」，然后回到这里刷新</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/05-trace/01-list.png" alt="Trace 列表">
      <p class="shot-cap">图：Trace 页。先检查顶部过滤器，不要只盯着空状态插画。</p>
      <div class="verify">✅ 验收：页面标题为 Trace。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>把数据源切到 Prompt</h2></div>
    <div class="card">
      <div class="why"><b>为什么空？</b>默认若选「SDK 上报」，界面调试产生的 span 可能看不到。要改成 <strong>Prompt</strong> 或放宽条件。</div>
      <ol class="steps-ol">
        <li>看顶部工具条：时间范围、Span 类型、数据源 / 平台</li>
        <li>时间选「过去 3 天」或更大</li>
        <li>数据源 / 平台选 <strong>Prompt</strong>（或「全部」）</li>
        <li>点刷新；列表应出现行</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/05-trace/02-toolbar.png" alt="工具条">
      <p class="shot-cap">图：顶部筛选工具条——时间、Span 类型、数据源都要会调。</p>
      <div class="verify">✅ 验收：列表出现至少一行，而不是「暂无数据」。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>点开详情：看到 Claude Sonnet</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>点列表中某一行</li>
        <li>左侧看调用树：常见 <code>PromptExecutor</code> → <code>Claude Sonnet</code></li>
        <li>中间看 Input / Output JSON</li>
        <li>右侧看状态 Success、耗时、Tokens</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/05-trace/04-detail.png" alt="Trace 详情">
      <p class="shot-cap">图：成功 Trace 详情。红框①调用树 ②输入输出 ③元信息。这是确认「Claude 真的被调用了」的铁证。</p>
      <div class="verify">✅ 验收：你能指出 Claude Sonnet 节点，并读出一句 Output 文本。</div>
      <div class="pitfall"><span class="t">仍没有数据</span>
      确认 P01 运行成功；过滤器选 Prompt；时间范围够大；点刷新。
      </div>
    </div>
  </section>
''',
    },
    {
        "logo": "P06",
        "file": "coze-loop-practice-06-tag.html",
        "title": "标签管理：为人工标注做准备",
        "mins": "15 min",
        "desc": "创建标签，供实验详情里人工打标使用。",
        "nav_steps": [
            ("#s1", "1 打开标签"),
            ("#s2", "2 新建标签"),
            ("#s3", "3 确认列表"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开标签管理</h2></div>
    <div class="card">
      <div class="why"><b>标签干什么？</b>人工阅卷时的「贴纸」：例如「有幻觉」「语气生硬」。和自动评估器互补。</div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>标签管理</strong></li>
        <li>进入标签列表页</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/01-list.png" alt="标签列表">
      <p class="shot-cap">图：标签管理入口与新建按钮。</p>
      <div class="verify">✅ 验收：面包屑含「标签」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>新建一个标签</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>点 <strong>新建 / 创建标签</strong></li>
        <li>填写标签名称，例如 <code>质量标签</code></li>
        <li>按表单要求配置取值 / 状态（以页面为准）</li>
        <li>点确认创建</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/02-create.png" alt="创建表单">
      <p class="shot-cap">图：创建标签表单。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/03-filled.png" alt="填好">
      <p class="shot-cap">图：填好后提交。字段名因版本可能不同，以红框区域为准跟着填。</p>
      <div class="verify">✅ 验收：提交无报错，回到列表。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>在列表确认创建成功</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>在列表搜索或直接浏览，找到刚建的标签</li>
        <li>之后在实验详情做人工标注时，即可选用这些标签</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/04-result.png" alt="创建结果">
      <p class="shot-cap">图：列表中出现新标签。</p>
      <div class="verify">✅ 验收：列表至少有 1 个你认识的标签名。</div>
    </div>
  </section>
''',
    },
    {
        "logo": "P07",
        "file": "coze-loop-practice-07-pat.html",
        "title": "账户设置与 OpenAPI PAT",
        "mins": "15 min",
        "desc": "创建个人访问令牌，给脚本 / SDK 调 Loop OpenAPI 用。",
        "nav_steps": [
            ("#s1", "1 打开账户设置"),
            ("#s2", "2 进入 API 授权"),
            ("#s3", "3 创建并保存令牌"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开「账户设置」</h2></div>
    <div class="card">
      <div class="why"><b>PAT ≠ 模型 Key。</b>PAT 是访问 <strong>Coze Loop 平台 API</strong> 的通行证；Claude Key 是访问 Anthropic 的。两个别混。</div>
      <ol class="steps-ol">
        <li>点侧栏<strong>左下角头像</strong></li>
        <li>在菜单点 <strong>账户设置</strong>（注意是「账户」）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/00-usermenu.png" alt="用户菜单">
      <p class="shot-cap">图：①头像 ②账户设置。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/01-account.png" alt="账户弹窗">
      <p class="shot-cap">图：账户弹窗左侧可切换「账户设置 / API 授权」。</p>
      <div class="verify">✅ 验收：弹出「账户」大窗口。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>切换到「API 授权」</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>左侧点 <strong>API 授权</strong></li>
        <li>看到「个人访问令牌」区域</li>
        <li>若为空，会提示去添加</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/02-pat-tab.png" alt="API 授权">
      <p class="shot-cap">图：API 授权页。红框标出「添加新令牌」按钮。</p>
      <div class="verify">✅ 验收：能看到「添加新令牌」按钮。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>创建令牌并立刻复制</h2></div>
    <div class="card">
      <ol class="steps-ol">
        <li>点 <strong>添加新令牌</strong></li>
        <li>填写名称，例如 <code>教程演示Token</code></li>
        <li>选择过期时间</li>
        <li>确认创建</li>
        <li><strong>立刻复制</strong>明文令牌——只显示一次，关掉就没了</li>
        <li>存到本地密码管理器；不要发到群里、不要提交 Git</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/03-create.png" alt="创建表单">
      <p class="shot-cap">图：创建令牌表单。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/04-filled.png" alt="已填写">
      <p class="shot-cap">图：填好名称等信息。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/05-created.png" alt="明文只一次">
      <p class="shot-cap">图：创建成功弹窗。黄字警告「只显示一次」——现在就复制！</p>
      <div class="verify">✅ 验收：令牌列表出现新条目；你已把明文存到安全位置。</div>
      <div class="pitfall"><span class="t">忘记复制怎么办？</span>
      无法再查看明文。只能删除旧令牌，再新建一个。
      </div>
    </div>
  </section>
''',
    },
]


def sidebar(active: str, nav_steps: list[tuple[str, str]]) -> str:
    lesson_links = "\n".join(
        f'<li><a href="{L["file"]}" class="nav-link{" active" if L["logo"]==active else ""}">{L["logo"]} · {L["title"].split("·")[0].strip()}</a></li>'
        for L in LESSONS
    )
    step_links = "\n".join(
        f'<li><a href="{href}" class="nav-link" data-section="{href.lstrip("#")}">{label}</a></li>'
        for href, label in nav_steps
    )
    return f'''
<nav class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <div class="logo" style="background:linear-gradient(135deg,#06b6d4,#4f46e5);">{active}</div>
    <h2>Loop 实战</h2>
    <p class="version">小白跟做 · 步骤带图</p>
  </div>
  <ul class="nav-list">
    <li class="nav-group-title">总目录</li>
    <li><a href="coze-loop-practice-tutorial.html" class="nav-link">总目录 Hub</a></li>
    <li class="nav-group-title">本课步骤</li>
    {step_links}
    <li class="nav-group-title">全部子课</li>
    {lesson_links}
    <li class="nav-group-title">导航</li>
    <li><a href="index.html" class="nav-link" style="color:var(--accent-cyan);">&larr; 首页</a></li>
  </ul>
</nav>'''


def page(L: dict, idx: int) -> str:
    prev = LESSONS[idx - 1] if idx > 0 else None
    nxt = LESSONS[idx + 1] if idx + 1 < len(LESSONS) else None
    prev_btn = (
        f'<a href="{prev["file"]}" class="nav-btn prev"><span class="nav-btn-label">上一课</span><span class="nav-btn-title">{prev["logo"]} · {prev["title"].split("·")[0].strip()}</span></a>'
        if prev
        else '<a href="coze-loop-practice-tutorial.html" class="nav-btn prev"><span class="nav-btn-label">返回</span><span class="nav-btn-title">实战总目录</span></a>'
    )
    next_btn = (
        f'<a href="{nxt["file"]}" class="nav-btn next"><span class="nav-btn-label">下一课</span><span class="nav-btn-title">{nxt["logo"]} · {nxt["title"].split("·")[0].strip()}</span></a>'
        if nxt
        else '<a href="coze-loop-practice-tutorial.html" class="nav-btn next"><span class="nav-btn-label">完成</span><span class="nav-btn-title">回到总目录</span></a>'
    )
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{L["logo"]} · {L["title"]} — Coze Loop 实战</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
<style>{CSS}</style>
</head>
<body>
{sidebar(L["logo"], L["nav_steps"])}
<button class="sidebar-toggle" id="sidebarToggle">&#9776;</button>
<main class="content" id="content">
  <div class="part-header">
    <span class="part-label">Coze Loop 开源实战 · {L["logo"]} / 共 8 课 · ≈{L["mins"]} · <span class="chip on">跟做版</span></span>
    <h1 class="part-title">{L["logo"]} · {L["title"]}</h1>
    <p class="part-desc">{L["desc"]} 截图红框为操作重点。上级：<a href="coze-loop-practice-tutorial.html">总目录</a>。</p>
  </div>
  <div class="warn-box">图上的<strong>红色编号框</strong>标出你要点的位置。请按「文字步骤 → 对照截图」顺序做；做完看每步绿色验收。</div>
{L["body"]}
  <div class="nav-buttons" style="margin-top:40px">
    {prev_btn}
    {next_btn}
  </div>
</main>
<button class="scroll-top" id="scrollTop">↑</button>
<script src="app.js"></script>
<script>hljs.highlightAll();</script>
</body>
</html>'''


def main() -> None:
    for i, L in enumerate(LESSONS):
        path = ROOT / L["file"]
        path.write_text(page(L, i), encoding="utf-8")
        print("wrote", path.name)
    print("ok", len(LESSONS))


if __name__ == "__main__":
    main()
