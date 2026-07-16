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
.purpose{background:rgba(6,182,212,.07);border-left:3px solid #22d3ee;border-radius:0 8px 8px 0;padding:12px 14px;margin:10px 0 14px;font-size:13px;color:var(--text-secondary);line-height:1.8}
.purpose p{margin:0 0 8px}
.purpose p:last-child{margin:0}
.purpose b{color:#67e8f9}
.goal-box{background:linear-gradient(135deg,rgba(6,182,212,.10),rgba(79,70,229,.10));border:1px solid rgba(6,182,212,.35);border-radius:12px;padding:16px 18px;margin:0 0 18px}
.goal-box .gt{font-size:14px;font-weight:800;color:#67e8f9;margin:0 0 10px;letter-spacing:.02em}
.goal-box ul{margin:0;padding-left:20px;font-size:13.5px;color:var(--text-secondary);line-height:1.85}
.goal-box li{margin:4px 0}
.goal-box .done{margin-top:12px;padding-top:10px;border-top:1px dashed rgba(6,182,212,.35);font-size:13px;color:var(--text-secondary);line-height:1.75}
.goal-box .done b{color:#4ade80}
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
        "goals": [
            "在本机用 Docker 把 Coze Loop 整套服务启动起来，浏览器能打开工作台。",
            "配置好 Claude 模型 Key，使后续 Prompt / 实验能真正调用大模型。",
            "完成邮箱注册登录，进入 Personal Space。",
            "认识左侧导航各模块对应什么能力，并找到账户设置入口。",
        ],
        "done_when": "打开 <code>http://localhost:8082</code> 已登录；Prompt 开发页「模型配置」下拉能看到 Claude；你能指出评测集 / Trace / 标签分别在侧栏哪一行。",
        "nav_steps": [
            ("#goal", "本课目标"),
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
      <div class="purpose">
        <p><b>目的：</b>动手前先确认电脑和环境具备条件，避免启动到一半才发现缺 Docker、内存不够或没有 API Key。</p>
        <p><b>作用：</b>把「能不能开课」变成一张清单；清单过关后，后面步骤才有意义，否则会反复踩坑。</p>
      </div>
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
      <div class="purpose">
        <p><b>目的：</b>把 Coze Loop 的前端、后端和依赖中间件（MySQL / Redis / ClickHouse / RocketMQ 等）一次性拉起来，得到可访问的本地网站。</p>
        <p><b>作用：</b>启动成功后，你就有了「教室」——浏览器入口是 <span class="fileref">http://localhost:8082</span>。没有这一步，后面所有界面操作都无从谈起。</p>
      </div>
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
      <div class="purpose">
        <p><b>目的：</b>告诉后端「用哪家大模型、API Key 是什么」。开源版<strong>没有</strong>网页版模型管理，只能改配置文件。</p>
        <p><b>作用：</b>配置并重启后，Prompt 调试页 / 评估器里会出现可选的 Claude。界面上只能<strong>选择</strong>模型，不能粘贴 Key；本课不配好，后面「运行」必失败。</p>
      </div>
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
      <div class="purpose">
        <p><b>目的：</b>在开源版里自建一个邮箱账号，并登录进入自己的工作空间（Personal Space）。</p>
        <p><b>作用：</b>登录后平台才知道「你是谁」，你创建的 Prompt、评测集、实验都会挂在这个空间下；未登录只能停在登录页。</p>
      </div>
      <ol class="steps-ol">
        <li>浏览器打开 <span class="fileref">http://localhost:8082</span>，若未登录会跳到 <code>/auth/login</code></li>
        <li>在「请输入邮箱」框填一个邮箱（本地演示可用任意格式，如 <code>demo@example.com</code>）</li>
        <li>在「请输入密码」框填密码（自己记住即可）</li>
        <li><strong>第一次</strong>：点灰色按钮 <strong>注册</strong>；以后再来点紫色按钮 <strong>登录</strong></li>
        <li>成功后地址栏会变成类似 <code>/console/enterprise/personal/space/一长串数字/pe/prompts</code></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/01-login.png" alt="登录页标注">
      <p class="shot-cap">图：按 <strong>1→2→3→4</strong>：填邮箱 → 填密码 → 点「注册」（新手第一次）→「登录」给以后用。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/02-login-filled.png" alt="已填写">
      <p class="shot-cap">图：按 <strong>1→2</strong>：确认已填好 → 点「注册」。若提示邮箱已存在，改邮箱或改用「登录」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/03-home-prompts.png" alt="进入首页">
      <p class="shot-cap">图：按 <strong>1→2→3</strong> 认首页：侧栏 → 主工作区 → 右上角创建入口。</p>
      <div class="verify">✅ 验收：能看到左侧导航和「Prompt 开发」空列表 / 欢迎插画，不再停留在登录页。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>认识左侧导航（地图）</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>建立「产品地图」——知道每个侧栏入口对应哪一类工作，避免后面找不到模块。</p>
        <p><b>作用：</b>后面 P01～P07 都从侧栏进门。认清地图后，你不会在「评测 / 观测 / 标签」之间迷路。</p>
      </div>
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
      <p class="shot-cap">图：侧栏按 <strong>1→7</strong> 从上到下认模块（Prompt → Playground → 评测集 → 评估器 → 实验 → Trace → 标签）。</p>
      <div class="verify">✅ 验收：你能用手指指出「评测集」「Trace」分别在哪一行。</div>
    </div>
  </section>

  <section id="s5" class="section">
    <div class="step-hdr"><div class="badge">5</div><h2>账户菜单与设置入口</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>找到个人账户相关入口：改资料、开 API 令牌、退出登录。</p>
        <p><b>作用：</b>账户菜单是 P07（创建 PAT）的必经之路；也会用到「退出登录」换账号。文案是「账户」不是「账号」，按字面找即可。</p>
      </div>
      <ol class="steps-ol">
        <li>看侧栏<strong>最底部</strong>：有你的头像 / 用户名</li>
        <li>用鼠标<strong>点一下</strong>头像区域，弹出菜单</li>
        <li>菜单里有：<strong>账户设置</strong>、<strong>退出登录</strong>（文案是「账户」不是「账号」）</li>
        <li>点「账户设置」会弹出大窗口，左侧可切换「账户设置 / API 授权」</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/05-user-menu.png" alt="用户菜单">
      <p class="shot-cap">图：按 <strong>1→2</strong>：点头像 → 选「账户设置 / 退出登录」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/00-setup/06-account-modal.png" alt="账户弹窗">
      <p class="shot-cap">图：按 <strong>1→2</strong>：看账户弹窗 → 左侧可切「API 授权」（PAT 见 P07）。</p>
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
        "goals": [
            "从零创建一条可保存的 Prompt，进入三栏开发调试页。",
            "写好 System / User 模板，选择 Claude，成功跑通一次调试。",
            "把满意的草稿提交成版本，便于实验引用和回滚。",
            "会用 Playground 做不落库的快速试跑，并区分它与「Prompt 开发」的差异。",
        ],
        "done_when": "列表里至少有 1 条 Prompt；调试页右栏出现模型中文回复与 Tokens；版本记录里有版本号；Playground 也能跑出回复。",
        "nav_steps": [
            ("#goal", "本课目标"),
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
      <div class="purpose">
        <p><b>目的：</b>进入 Prompt 的「家」——所有正式 Prompt 都在这里创建、编辑、管理。</p>
        <p><b>作用：</b>这是后续创建、调试、提交版本的统一入口。认准这个页面，才不会误跑到 Playground 或其它模块。</p>
      </div>
      <ol class="steps-ol">
        <li>确认已登录（P00 完成）</li>
        <li>左侧侧栏点 <strong>Prompt 开发</strong>（第一项，通常默认就在这里）</li>
        <li>若是空账号，中间会显示「暂无 Prompt」和插画</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/01-list-empty.png" alt="空列表">
      <p class="shot-cap">图：按 <strong>1→2</strong>：确认在 Prompt 开发 → 点右上角「创建 Prompt」。</p>
      <div class="verify">✅ 验收：面包屑显示「Prompt 工程 / Prompt 开发」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>创建空白 Prompt</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>新建一条可落库的 Prompt 草稿（有 Key、名称），并进入三栏调试工作台。</p>
        <p><b>作用：</b>创建成功后，平台会分配一个 Prompt 实体；你才能写模板、挂模型、保存版本。Key 是程序引用用的「身份证」，名称给人看。</p>
      </div>
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
      <p class="shot-cap">图：按顺序点「空白 Prompt」（图上数字 <strong>1</strong>）。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/03-create-dialog.png" alt="创建弹窗">
      <p class="shot-cap">图：按 <strong>1→2</strong>：填写 Key/名称 → 点「确认」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/04-create-filled.png" alt="填好确认">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：填 Key → 填名称 → 点「确认」进入开发页。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/05-develop.png" alt="三栏布局">
      <p class="shot-cap">图：按 <strong>1→2→3</strong> 认三栏：左模板 / 中模型 / 右预览调试。</p>
      <div class="verify">✅ 验收：顶部出现 Prompt 名称，中间有「请选择模型」，右侧有「运行」按钮（可能暂时灰掉）。</div>
      <div class="pitfall"><span class="t">Key 报错？</span>
      必须以英文字母开头；不能有空格或中文。例如 <code>1abc</code>、<code>我的prompt</code> 都不行。
      </div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>写 System / User 消息模板</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>用自然语言规定模型的角色、任务，以及用户侧输入长什么样。</p>
        <p><b>作用：</b>模板就是发给大模型的「剧本」。空内容直接运行会被 Claude 拒绝（400）；写好后，每次点「运行」都会按这套内容（或变量替换后）去调用模型。</p>
      </div>
      <ol class="steps-ol">
        <li>在左栏找到标着 <strong>System</strong> 的输入框</li>
        <li>点进去，输入例如：<code>你是礼貌助手。请用一句中文问候用户。</code></li>
        <li>若还没有 User 消息：点 <strong>+ 添加消息</strong>，角色选 User（或默认追加）</li>
        <li>在 User 框输入例如：<code>我叫小明</code></li>
        <li>也可以用变量写法：<code>{{user_name}}</code>（后面再在变量区赋值）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/06-edit-template.png" alt="编辑模板">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：写 System → 写 User → 可继续添加消息。</p>
      <div class="verify">✅ 验收：System 框不再是灰色占位符「请输入内容…」，而是你的真实文字。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>选择 Claude 并点击运行</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>把 P00 已配置好的 Claude 挂到当前 Prompt，并发起一次真实 API 调用，验证模板是否可用。</p>
        <p><b>作用：</b>这是本课的「通电时刻」：右栏会显示模型回复、耗时、Tokens。成功说明模型链路通了；失败则要回头查 Key / 参数 / 空消息等问题。</p>
      </div>
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
      <p class="shot-cap">图：按数字 <strong>1</strong> 在下拉里选 Claude Sonnet（说明 P00 的 yaml 已生效）。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/10-model-selected.png" alt="选好模型">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：确认模型 → 看参数 → 点「运行」。运行是灰的就检查是否已选模型、消息是否为空。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/11-debug-result.png" alt="调试成功">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：看回复 → 看耗时/Tokens → 满意后再提交新版。</p>
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
      <div class="purpose">
        <p><b>目的：</b>把当前调试满意的草稿，固化成一个带版本号的快照。</p>
        <p><b>作用：</b>版本可回滚、可对比、可被实验精确引用（例如永远用 <code>0.0.1</code>）。只改草稿不提交，别人/实验可能拿到的仍是旧内容或不稳定草稿。</p>
      </div>
      <ol class="steps-ol">
        <li>确认调试结果满意</li>
        <li>点顶部右侧紫色/蓝色按钮 <strong>提交新版</strong></li>
        <li>在弹窗填写版本号，例如 <code>0.0.1</code>（按你们团队规范即可）</li>
        <li>可写变更说明（可选）</li>
        <li>点确认 / 提交</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/07-submit-version.png" alt="提交弹窗">
      <p class="shot-cap">图：按 <strong>1→2</strong>：填版本号 → 确认提交。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/12-version-done.png" alt="提交完成">
      <p class="shot-cap">图：数字 <strong>1</strong>：确认顶部版本状态已变化；可用「版本记录」查看历史。</p>
      <div class="verify">✅ 验收：顶部「修改未提交」提示消失或版本记录里出现新版本。</div>
    </div>
  </section>

  <section id="s6" class="section">
    <div class="step-hdr"><div class="badge">6</div><h2>用 Playground 快速试跑</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>在不创建正式 Prompt 的情况下，快速试一段提示词 / 模型效果（像草稿纸）。</p>
        <p><b>作用：</b>降低试错成本：想法不定型时先用 Playground；满意后再「快捷创建」落成正式 Prompt。和「Prompt 开发」能力相近，但默认不强调版本管理。</p>
      </div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>Playground</strong></li>
        <li>左栏写 System（例：<code>用一句话介绍你自己：你是 Anthropic 的 Claude。</code>）</li>
        <li>中间选 <strong>Claude Sonnet</strong></li>
        <li>点右下角 <strong>运行</strong></li>
        <li>满意后可用顶部 <strong>快捷创建</strong> 存成正式 Prompt（可选）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/08-playground.png" alt="Playground">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：进 Playground → 选 Claude → 点「运行」。默认不落库。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/13-playground-result.png" alt="Playground 结果">
      <p class="shot-cap">图：数字 <strong>1</strong>：看 Playground 成功回复。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/01-prompt/09-list-with-item.png" alt="列表面板">
      <p class="shot-cap">图：按 <strong>1→2</strong>：确认列表有新 Prompt → 可进详情/调用记录（跳 Trace）。</p>
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
        "goals": [
            "理解评测集 = 考试卷：每一行是一道输入题，可带参考答案。",
            "新建一张评测集，看懂默认列 input / reference_output 的含义。",
            "至少添加 1～3 行真实数据，使后续实验有内容可跑。",
        ],
        "done_when": "评测集列表里有你的表；详情页表格至少 1 行数据；你能说清两列各自干什么。",
        "nav_steps": [
            ("#goal", "本课目标"),
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
      <div class="purpose">
        <p><b>目的：</b>进入「考试卷」管理页，找到创建评测集的入口。</p>
        <p><b>作用：</b>评测集是实验（P04）的必选原料。没有评测集，实验向导选不出数据，整条评测链路走不通。</p>
      </div>
      <ol class="steps-ol">
        <li>左侧侧栏找到分组 <strong>评测</strong></li>
        <li>点 <strong>评测集</strong></li>
        <li>注意按钮文案是 <strong>新建评测集</strong>（不是「创建」）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/01-list.png" alt="评测集列表">
      <p class="shot-cap">图：按 <strong>1→2</strong>：侧栏点「评测集」 → 右上角「新建评测集」。</p>
      <div class="verify">✅ 验收：面包屑为「评测 / 评测集」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>填写名称与描述</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>给这张评测表起一个人和机器都能认的名字，并可选写清用途。</p>
        <p><b>作用：</b>名称会出现在列表和实验向导的下拉里。起得清楚（如「问候评测集」），后面选数据时不会选错表。</p>
      </div>
      <ol class="steps-ol">
        <li>点 <strong>新建评测集</strong> 进入表单页</li>
        <li><strong>名称</strong>（必填）：例如 <code>问候评测集</code>，最多约 50 字</li>
        <li><strong>描述</strong>（可选）：写清楚这张表用来测什么</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/02-create.png" alt="新建页全貌">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：填名称/描述 → 配置列 → 点「创建」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/03-named.png" alt="名称">
      <p class="shot-cap">图：数字 <strong>1</strong>：名称必填，空着点创建会被拦住。</p>
      <div class="verify">✅ 验收：名称框有内容，字数计数在限制内。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>看懂默认列（Schema）</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>理解评测集的「表头」——每一列代表什么字段、后面实验如何取数。</p>
        <p><b>作用：</b>列名是评估器 / 字段映射的钥匙。默认 <code>input</code> 喂给模型，<code>reference_output</code> 当参考答案；名字乱改会导致映射对不上。</p>
      </div>
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
      <p class="shot-cap">图：按 <strong>1→2</strong>：看默认两列 → 需要时再「添加列」。先理解再改名。</p>
      <div class="verify">✅ 验收：你能说清 input 和 reference_output 各干什么。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>点「创建」进入详情</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>把表单里的 Schema 真正保存成平台上的一张评测集，并进入可加数据的详情页。</p>
        <p><b>作用：</b>创建前只是草稿表单；创建后才有 ID，才能「添加数据」「新建实验」「提交版本」。地址栏会出现数据集 ID。</p>
      </div>
      <ol class="steps-ol">
        <li>检查名称和列无误</li>
        <li>点页面右下角蓝色 <strong>创建</strong></li>
        <li>成功后进入评测集详情：可添加数据、看关联实验、提交版本</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/05-detail.png" alt="详情页">
      <p class="shot-cap">图：按 <strong>1→2</strong>：确认进入详情 → 再用右上「添加数据 / 新建实验」。</p>
      <div class="verify">✅ 验收：地址栏变成 <code>.../evaluation/datasets/一串数字</code>。</div>
    </div>
  </section>

  <section id="s5" class="section">
    <div class="step-hdr"><div class="badge">5</div><h2>添加至少一行数据</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>往评测集里写入真实「考题」行，让实验有东西可跑。</p>
        <p><b>作用：</b>空表启动实验等于空跑。至少 1～3 行后，实验才能产出行级结果；也可再「提交新版本」固化数据快照。</p>
      </div>
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
      <p class="shot-cap">图：数字 <strong>1</strong>：在右侧抽屉填一行数据（界面可能略有差异）。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/02-dataset/07-item-list.png" alt="数据列表">
      <p class="shot-cap">图：数字 <strong>1</strong>：确认数据出现在表里。可再「提交新版本」固化。</p>
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
        "goals": [
            "理解评估器 = 自动阅卷老师，知道预置 / 自建的区别。",
            "创建（或配置）一个挂上 Claude 的 LLM 评估器。",
            "认识 Code 评估器适用场景：规则可复现、不消耗 LLM。",
        ],
        "done_when": "自建列表里有你的评估器（或你能打开预置详情）；能说出 LLM 与 Code 各适合什么题型。",
        "nav_steps": [
            ("#goal", "本课目标"),
            ("#s1", "1 打开评估器"),
            ("#s2", "2 浏览预置"),
            ("#s3", "3 创建 LLM 评估器"),
            ("#s4", "4 认识 Code 评估器"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开评估器列表</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>进入自动阅卷工具的管理页，分清「自建」和「预置」。</p>
        <p><b>作用：</b>评估器在实验（P04）里给每行输出打分。先找到入口，才谈得上创建 LLM / Code 评估器。</p>
      </div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>评估器</strong></li>
        <li>顶部通常有页签：<strong>自建</strong> / <strong>预置</strong></li>
        <li>右上角有新建入口</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/01-list.png" alt="评估器列表">
      <p class="shot-cap">图：按 <strong>1→2</strong>：侧栏点「评估器」 → 右上角「新建」。先分清自建/预置页签。</p>
      <div class="verify">✅ 验收：面包屑为「评测 / 评估器」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>浏览预置评估器</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>先看官方模板长什么样，学习「评估维度 / 评判 Prompt」的常见写法。</p>
        <p><b>作用：</b>预置可直接用或复制改造成自建，减少从零写评判规则的成本；也帮你建立「什么叫好的评估器」的直觉。</p>
      </div>
      <ol class="steps-ol">
        <li>点页签 <strong>预置</strong>（或「内置」）</li>
        <li>浏览卡片：常见如准确性、相关性等模板</li>
        <li>点进某张卡片可查看说明；可复制后改成自建</li>
        <li>新手建议：先看懂预置长什么样，再回去建自己的</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/02-builtin.png" alt="预置">
      <p class="shot-cap">图：按 <strong>1→2</strong>：切到「预置」 → 浏览卡片学习评估器长什么样。</p>
      <div class="verify">✅ 验收：你能打开至少一张预置评估器详情。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>创建 LLM 评估器并挂上 Claude</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>创建一个「让大模型当裁判」的评估器，用于开放性语义打分（礼貌度、相关性等）。</p>
        <p><b>作用：</b>实验跑完后，LLM 评估器会对每行「模型输出 vs 参考答案」给分或评语。它同样依赖 P00 的 Claude 配置（含 function_call）。</p>
      </div>
      <ol class="steps-ol">
        <li>回到「自建」页签，点 <strong>新建 / 创建</strong></li>
        <li>选择 <strong>LLM</strong>（或「大模型评估器」）</li>
        <li>填写评估器名称，例如 <code>礼貌度评估</code></li>
        <li>在模型配置里选择 <strong>Claude Sonnet</strong>（与 P01 相同来源）</li>
        <li>按页面提示编写评判 Prompt（说明如何打分、输出格式）</li>
        <li>保存 / 创建；可再点调试用样例试跑</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/04-create-menu.png" alt="新建菜单">
      <p class="shot-cap">图：数字 <strong>1</strong>：新建时选择 LLM 或 Code。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/05-create-llm.png" alt="LLM 创建页">
      <p class="shot-cap">图：数字 <strong>1</strong>：在 LLM 评估器编辑页填写配置（字段可能略有不同）。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/07-llm-configured.png" alt="已选 Claude">
      <p class="shot-cap">图：数字 <strong>1</strong>：评判模型选 Claude（yaml 需打开 function_call）。</p>
      <div class="verify">✅ 验收：自建列表里出现你的评估器；模型下拉不是空的。</div>
      <div class="pitfall"><span class="t">评估器调试失败</span>
      与 P01 相同：检查 Key、temperature/top_p 冲突、消息是否为空。
      </div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>认识 Code 评估器</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>了解「用代码写规则」的评估方式，知道它和 LLM 评估器怎么分工。</p>
        <p><b>作用：</b>Code 评估器跑确定性规则（相等、包含、正则），不花 LLM 费用、结果可复现；适合格式/精确匹配。开放性语义题仍优先 LLM。</p>
      </div>
      <ol class="steps-ol">
        <li>新建 → 选 <strong>Code</strong></li>
        <li>进入代码编辑页，按模板写规则</li>
        <li>适合：精确匹配、格式检查；不适合：开放性语义打分（那用 LLM）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/03-evaluator/06-create-code.png" alt="Code 评估器">
      <p class="shot-cap">图：数字 <strong>1</strong>：在 Code 评估器页写规则（本地 FaaS 执行）。</p>
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
        "goals": [
            "理解实验 = 一次完整考试：评测集逐行跑对象，再用评估器打分。",
            "走完五步向导：基本信息 → 评测集 → 对象 → 评估器 → 确认启动。",
            "启动后能在列表/详情看到运行状态或行级结果。",
        ],
        "done_when": "实验列表出现新记录；详情里能看到行级输出或明确状态；你知道哪一步是必选（评测集）、哪一步可跳过。",
        "nav_steps": [
            ("#goal", "本课目标"),
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
      <div class="purpose">
        <p><b>目的：</b>进入「考试场」列表，并打开创建实验的五步向导。</p>
        <p><b>作用：</b>实验把前面的评测集、Prompt、评估器组装成一次可重复的批量评测任务。本步只负责进门并认识进度条。</p>
      </div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>实验</strong></li>
        <li>点右上角 <strong>新建 / 创建实验</strong></li>
        <li>进入五步向导页，先看顶部进度条</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/01-list.png" alt="实验列表">
      <p class="shot-cap">图：按 <strong>1→2</strong>：侧栏点「实验」 → 右上角「新建实验」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/02-wizard.png" alt="向导">
      <p class="shot-cap">图：按 <strong>1→2</strong>：看五步进度条 → 填步骤1基本信息。</p>
      <div class="verify">✅ 验收：能看到步骤条（基本信息 → 评测集 → …）。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>步骤1：基本信息</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>给这次实验起名，方便在列表里识别（谁跑的、测什么）。</p>
        <p><b>作用：</b>名称会出现在实验列表与详情标题。起名清晰（如「问候实验-Claude」）方便以后对比多次实验。</p>
      </div>
      <ol class="steps-ol">
        <li>填写<strong>实验名称</strong>，例如 <code>问候实验-Claude</code></li>
        <li>描述可选</li>
        <li>点右下角 <strong>下一步</strong></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/03-basic.png" alt="基本信息">
      <p class="shot-cap">图：按 <strong>1→2</strong>：填写实验名称 → 点「下一步」。</p>
      <div class="verify">✅ 验收：进度条高亮移到第 2 步。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>步骤2：选择评测集（必选）</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>指定这次考试用哪张「试卷」（P02 建的评测集）。</p>
        <p><b>作用：</b>评测集是实验的必选项。选中后，系统会按该表的每一行去调用评测对象；空表或选错表会导致结果无意义。</p>
      </div>
      <ol class="steps-ol">
        <li>在下拉 / 列表中选择你在 P02 创建的评测集</li>
        <li>若有版本，选择最新版本</li>
        <li>确认行数 &gt; 0（空集会导致实验无意义）</li>
        <li>点 <strong>下一步</strong></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/04-dataset-step.png" alt="选评测集">
      <p class="shot-cap">图：数字 <strong>1</strong>：选择评测集（必选）。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/04b-dataset-picked.png" alt="已选中">
      <p class="shot-cap">图：数字 <strong>1</strong>：确认已选中。看不到？回 P02 确认已创建。</p>
      <div class="verify">✅ 验收：评测集名称显示在表单中，不是「请选择」。</div>
    </div>
  </section>

  <section id="s4" class="section">
    <div class="step-hdr"><div class="badge">4</div><h2>步骤3～4：评测对象与评估器（可跳过）</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>指定「谁来答题」（评测对象，如 Prompt）以及「谁来阅卷」（评估器）。</p>
        <p><b>作用：</b>选 Prompt 才会真正调用 Claude 生成输出；绑评估器才会自动打分。两者都可跳过以先跑通流程，但跳过则缺少对应能力（无模型输出或无自动分）。</p>
      </div>
      <ol class="steps-ol">
        <li><strong>步骤3 评测对象</strong>：选择 Prompt（P01 创建的），或按界面提示跳过</li>
        <li>若选 Prompt，通常还要选版本</li>
        <li><strong>步骤4 评估器</strong>：勾选 P03 的评估器，或跳过</li>
        <li>每步点 <strong>下一步</strong></li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/05-target-step.png" alt="评测对象">
      <p class="shot-cap">图：数字 <strong>1</strong>：选评测对象（Prompt）或跳过；选 Prompt 才会调 Claude。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/06-evaluator-step.png" alt="评估器">
      <p class="shot-cap">图：数字 <strong>1</strong>：选评估器或跳过；可多选。</p>
      <div class="verify">✅ 验收：到达确认页（步骤5）。</div>
    </div>
  </section>

  <section id="s5" class="section">
    <div class="step-hdr"><div class="badge">5</div><h2>步骤5：确认并启动</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>最后核对配置无误后，真正提交并启动这次批量评测任务。</p>
        <p><b>作用：</b>启动后平台按行执行：调对象 →（可选）评估 → 写结果。你可在详情看每行输出与汇总图表；这是「评测闭环」的终点。</p>
      </div>
      <ol class="steps-ol">
        <li>核对：名称、评测集、对象、评估器</li>
        <li>点 <strong>启动实验 / 创建 / 提交</strong>（按钮文案因版本可能不同）</li>
        <li>等待任务从「运行中」变为完成</li>
        <li>进实验详情：表格看每行输出；Chart 看汇总</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/04-experiment/07-confirm.png" alt="确认启动">
      <p class="shot-cap">图：按 <strong>1→2</strong>：核对配置 → 点「启动实验」。行数多会跑一会儿。</p>
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
        "goals": [
            "理解 Trace = 每次调用的黑匣子（链路、耗时、输入输出）。",
            "会调整过滤器（尤其数据源选 Prompt），避免「明明跑过却没数据」。",
            "打开详情，在调用树里定位到 Claude Sonnet 节点。",
        ],
        "done_when": "列表至少一行 Trace；详情里能指出 Claude 节点，并读出一句 Output。",
        "nav_steps": [
            ("#goal", "本课目标"),
            ("#s1", "1 打开 Trace"),
            ("#s2", "2 调过滤器"),
            ("#s3", "3 看详情"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开 Trace</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>进入可观测性页面，准备查看 Prompt / 实验产生的调用记录。</p>
        <p><b>作用：</b>Trace 用来排查「调用了谁、花了多久、输入输出是什么」。比只看调试页气泡更完整，是确认 Claude 真被调用的证据库。</p>
      </div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>Trace</strong></li>
        <li>若提示「暂无数据」：先去 P01 再点一次「运行」，然后回到这里刷新</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/05-trace/01-list.png" alt="Trace 列表">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：进 Trace → 调过滤器 → 点某行看详情。</p>
      <div class="verify">✅ 验收：页面标题为 Trace。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>把数据源切到 Prompt</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>把筛选条件调到能看到「界面调试」产生的 span，而不是只看 SDK 上报。</p>
        <p><b>作用：</b>过滤器选错（如默认 SDK）会显示「暂无数据」，让人误以为没调用成功。切到 Prompt / 放宽时间后，真实调用才会出现在列表。</p>
      </div>
      <ol class="steps-ol">
        <li>看顶部工具条：时间范围、Span 类型、数据源 / 平台</li>
        <li>时间选「过去 3 天」或更大</li>
        <li>数据源 / 平台选 <strong>Prompt</strong>（或「全部」）</li>
        <li>点刷新；列表应出现行</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/05-trace/02-toolbar.png" alt="工具条">
      <p class="shot-cap">图：数字 <strong>1</strong>：改时间范围 / Span 类型 / 数据源（选 Prompt）。</p>
      <div class="verify">✅ 验收：列表出现至少一行，而不是「暂无数据」。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>点开详情：看到 Claude Sonnet</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>深入一条 Trace，读懂调用树与 Input / Output，验证模型链路。</p>
        <p><b>作用：</b>详情是排障与复盘的主战场：能确认是否打到 Claude、耗时与 Token 是否异常、输入输出是否符合预期。</p>
      </div>
      <ol class="steps-ol">
        <li>点列表中某一行</li>
        <li>左侧看调用树：常见 <code>PromptExecutor</code> → <code>Claude Sonnet</code></li>
        <li>中间看 Input / Output JSON</li>
        <li>右侧看状态 Success、耗时、Tokens</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/05-trace/04-detail.png" alt="Trace 详情">
      <p class="shot-cap">图：按 <strong>1→2→3</strong>：看调用树 → Input/Output → 状态/耗时。确认 Claude 被调用。</p>
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
        "goals": [
            "理解标签 = 人工阅卷时的贴纸，与自动评估器互补。",
            "在标签管理里新建至少一个标签。",
            "知道之后在实验详情做人工标注时可选用这些标签。",
        ],
        "done_when": "标签列表里出现你创建的名称；你能说清标签和评估器的分工。",
        "nav_steps": [
            ("#goal", "本课目标"),
            ("#s1", "1 打开标签"),
            ("#s2", "2 新建标签"),
            ("#s3", "3 确认列表"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开标签管理</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>进入标签体系管理页，为人工标注准备「贴纸库」。</p>
        <p><b>作用：</b>自动评估器覆盖不了的主观问题（幻觉、语气等）靠人工打标。标签要先在这里建好，实验详情里才能选用。</p>
      </div>
      <ol class="steps-ol">
        <li>侧栏点 <strong>标签管理</strong></li>
        <li>进入标签列表页</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/01-list.png" alt="标签列表">
      <p class="shot-cap">图：按 <strong>1→2</strong>：点「标签管理」 → 点「新建标签」。</p>
      <div class="verify">✅ 验收：面包屑含「标签」。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>新建一个标签</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>创建一条可用的标签定义（名称、取值等），加入空间的标签库。</p>
        <p><b>作用：</b>创建成功后，团队在人工阅卷时有统一词汇，便于统计「有多少条被标了某类问题」。</p>
      </div>
      <ol class="steps-ol">
        <li>点 <strong>新建 / 创建标签</strong></li>
        <li>填写标签名称，例如 <code>质量标签</code></li>
        <li>按表单要求配置取值 / 状态（以页面为准）</li>
        <li>点确认创建</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/02-create.png" alt="创建表单">
      <p class="shot-cap">图：数字 <strong>1</strong>：填写标签信息。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/03-filled.png" alt="填好">
      <p class="shot-cap">图：数字 <strong>1</strong>：确认信息后提交（字段名以图上标注为准）。</p>
      <div class="verify">✅ 验收：提交无报错，回到列表。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>在列表确认创建成功</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>确认标签已落库，可被后续人工标注流程使用。</p>
        <p><b>作用：</b>列表可见 = 创建成功。本课到此闭环；真正「贴到某条结果上」通常在实验详情完成。</p>
      </div>
      <ol class="steps-ol">
        <li>在列表搜索或直接浏览，找到刚建的标签</li>
        <li>之后在实验详情做人工标注时，即可选用这些标签</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/06-tag/04-result.png" alt="创建结果">
      <p class="shot-cap">图：数字 <strong>1</strong>：确认列表出现新标签。</p>
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
        "goals": [
            "分清 PAT（访问 Loop 平台 API）与 Claude Key（访问 Anthropic）不是同一个东西。",
            "从账户设置进入 API 授权，创建个人访问令牌。",
            "学会立刻复制并安全保存明文（只显示一次）。",
        ],
        "done_when": "令牌列表出现新条目；明文已存到安全位置；你能说清 PAT 用来调 Loop，不是调 Claude。",
        "nav_steps": [
            ("#goal", "本课目标"),
            ("#s1", "1 打开账户设置"),
            ("#s2", "2 进入 API 授权"),
            ("#s3", "3 创建并保存令牌"),
        ],
        "body": r'''
  <section id="s1" class="section">
    <div class="step-hdr"><div class="badge">1</div><h2>打开「账户设置」</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>进入个人账户弹窗，为创建平台 API 令牌找到正确入口。</p>
        <p><b>作用：</b>PAT 与 Claude Key 完全不同：PAT 证明「你有权调用 Coze Loop OpenAPI」；Claude Key 证明「你有权调用 Anthropic」。别混用。</p>
      </div>
      <ol class="steps-ol">
        <li>点侧栏<strong>左下角头像</strong></li>
        <li>在菜单点 <strong>账户设置</strong>（注意是「账户」）</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/00-usermenu.png" alt="用户菜单">
      <p class="shot-cap">图：按 <strong>1→2</strong>：点头像 → 点「账户设置」。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/01-account.png" alt="账户弹窗">
      <p class="shot-cap">图：按 <strong>1→2</strong>：看账户设置 → 切到「API 授权」。</p>
      <div class="verify">✅ 验收：弹出「账户」大窗口。</div>
    </div>
  </section>

  <section id="s2" class="section">
    <div class="step-hdr"><div class="badge">2</div><h2>切换到「API 授权」</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>从账户弹窗切到「个人访问令牌」管理页。</p>
        <p><b>作用：</b>这里集中管理 PAT 的创建、列表与吊销。脚本 / SDK 调 Loop OpenAPI 时，会把 PAT 放在请求头里做鉴权。</p>
      </div>
      <ol class="steps-ol">
        <li>左侧点 <strong>API 授权</strong></li>
        <li>看到「个人访问令牌」区域</li>
        <li>若为空，会提示去添加</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/02-pat-tab.png" alt="API 授权">
      <p class="shot-cap">图：按 <strong>1→2</strong>：看个人访问令牌区 → 点「添加新令牌」。</p>
      <div class="verify">✅ 验收：能看到「添加新令牌」按钮。</div>
    </div>
  </section>

  <section id="s3" class="section">
    <div class="step-hdr"><div class="badge">3</div><h2>创建令牌并立刻复制</h2></div>
    <div class="card">
      <div class="purpose">
        <p><b>目的：</b>生成一枚新的 PAT，并在明文只显示一次时把它存好。</p>
        <p><b>作用：</b>有了 PAT，你才能用 curl / SDK / 自动化脚本操作 Loop（建评测、拉 Trace 等），而不必每次在浏览器点。泄露等同于账号权限外泄，务必保密。</p>
      </div>
      <ol class="steps-ol">
        <li>点 <strong>添加新令牌</strong></li>
        <li>填写名称，例如 <code>教程演示Token</code></li>
        <li>选择过期时间</li>
        <li>确认创建</li>
        <li><strong>立刻复制</strong>明文令牌——只显示一次，关掉就没了</li>
        <li>存到本地密码管理器；不要发到群里、不要提交 Git</li>
      </ol>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/03-create.png" alt="创建表单">
      <p class="shot-cap">图：数字 <strong>1</strong>：填写令牌名称 / 过期时间。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/04-filled.png" alt="已填写">
      <p class="shot-cap">图：数字 <strong>1</strong>：确认信息后生成。</p>
      <img class="shot" src="assets/coze-loop-practice/marked/07-pat/05-created.png" alt="明文只一次">
      <p class="shot-cap">图：数字 <strong>1</strong>：明文只显示一次——立刻复制！</p>
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
    goal_lis = "\n".join(f"        <li>{g}</li>" for g in L.get("goals", []))
    if not goal_lis:
        goal_lis = "        <li>（本课目标待补充）</li>"
    done_when = L.get("done_when", "完成本课全部绿色验收项。")
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
  <section id="goal" class="section">
    <div class="goal-box">
      <p class="gt">🎯 本课目标（先读再动手）</p>
      <ul>
{goal_lis}
      </ul>
      <div class="done"><b>学完怎样算过关：</b>{done_when}</div>
    </div>
  </section>
  <div class="warn-box">图上<strong>红色圆圈数字 1、2、3…</strong>表示本步操作顺序，请严格按数字从小到大点。数字旁短文是该步要点。做完看每步绿色验收；先读本课目标再动手。</div>
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
