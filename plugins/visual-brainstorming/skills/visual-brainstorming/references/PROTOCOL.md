# 本地伴侣协议

## 1. CLI 总览

```text
companion.py start    启动或复用后台服务
companion.py serve    前台运行服务
companion.py status   检查当前项目会话
companion.py paths    输出当前会话路径
companion.py publish  原子发布 HTML
companion.py show     启动/复用、发布并按需打开
companion.py events   读取浏览器事件
companion.py stop     停止当前服务
companion.py prune    预览或按精确计划删除旧会话
companion.py demo     启动并发布内置演示
```

Skill 执行时应显式传入 `--project-dir`，避免因工作目录变化写入错误项目。正常 Agent 路径优先使用 `show`，无需先执行 `start` 和 `status`。

## 2. 运行目录

```text
.visual-brainstorming/
├── .gitignore                 # 自动写入 `*`
├── .launch.lock               # 持久 metadata 文件；启动/prune 时持有 OS lock
├── .server.lock               # 持久 metadata 文件；服务运行时持有 OS lock
├── current.json
└── sessions/
    └── <session-id>/
        ├── content/
        │   ├── *.html
        │   └── local-assets.*
        └── state/
            ├── session-key
            ├── server-info.json
            ├── launcher.json
            ├── launch-error.json       # 仅后台启动失败时出现
            ├── server.log
            ├── events.jsonl
            └── server-stopped.json
```

目录和状态文件在支持权限位的系统上分别限制为 `0700` 和 `0600`。运行根目录会自动生成内容为 `*` 的内部 `.gitignore`；仍建议项目级忽略：

```gitignore
.visual-brainstorming/
```

## 3. `show`

推荐的正常路径：

```bash
python3 -I -S scripts/companion.py show \
  --project-dir /project \
  --source /tmp/layout.html \
  --name layout-options \
  --open
```

`show` 依次完成：

1. 先校验源文件，不为明显无效输入启动服务；
2. 复用健康服务或启动新服务；
3. 原子发布 UTF-8 HTML；
4. 在发布成功后请求打开浏览器；
5. 返回精简的会话和页面信息。

若本次新启动的服务在发布阶段失败，`show` 会尝试关闭它；复用的已有服务不会被误停。

它支持 `start` 的公共参数以及 `--new`、`--source`、`--name`。`--source` 必须是 `.html` 或 `.htm`。

## 4. `start` 与 `serve`

后台启动或复用：

```bash
python3 -I -S scripts/companion.py start \
  --project-dir /project --open
```

前台运行：

```bash
python3 -I -S scripts/companion.py serve \
  --project-dir /project --open
```

公共参数：

| 参数 | 默认 | 含义 |
|---|---|---|
| `--host` | `127.0.0.1` | 监听主机 |
| `--port` | `0` | 自动选择空闲端口 |
| `--url-host` | 非 wildcard 时为监听主机；wildcard 时为 `127.0.0.1` | 写入浏览器 URL 的主机或 IP；远程模式只接受本机实际持有的 literal loopback/private/link-local IP |
| `--allow-remote` | 关闭 | 专家逃生口：允许绑定 `0.0.0.0` 或 `::`；使用明文 HTTP，只能由用户显式要求并限制在受信任网络或安全隧道后 |
| `--idle-timeout` | `7200` | 无页面/资源加载或用户事件后自动停止的秒数；`0` 禁用 |
| `--open` | 关闭 | 打开默认浏览器 |

`start` 额外支持：

| 参数 | 含义 |
|---|---|
| `--new` | 停止当前服务并创建新会话 |

行为：

- 已有健康服务时，`start` 默认复用；
- 只有 companion 版本和 host/URL host/port/remote/idle-timeout 设置一致时才复用；不兼容版本默认拒绝，需显式 `--new` 替换；
- 后台服务使用 Python 隔离模式启动，不加载用户级 site 包；
- 后台子进程在启动超时后会被终止，避免遗留孤儿进程；
- wildcard bind 不执行 hostname 反向解析，启动不依赖 DNS/mDNS 可用性；
- launch/server 使用进程退出自动释放的 OS advisory lock，并叠加同进程 thread lock；`.lock` metadata 文件可保留，是否持锁不以文件存在与否判断；
- 端口、URL host 和空闲时间在启动前验证；remote URL 不能指向另一台内网主机；
- 服务默认只允许回环地址；远程模式仍需要显式 `--allow-remote`。
- Agent 不得为了“浏览器打不开”自行开启远程模式；应先降级为静态图、Mermaid、ASCII 或结构化文字。
- 远程模式没有 TLS，首次 URL、会话 key、选择和备注可能被网络观察者读取；不要用于公网或不受信任局域网。

## 5. `status` 与 `paths`

```bash
python3 -I -S scripts/companion.py status --project-dir /project
python3 -I -S scripts/companion.py paths  --project-dir /project
```

`status` 在没有会话时仍返回 JSON：

```json
{
  "running": false,
  "compatible": false,
  "project_dir": "/project"
}
```

`paths` 只在存在有效当前会话时返回目录；没有会话时会退出并说明 `No current session`。

健康会话示例：

```json
{
  "running": true,
  "compatible": true,
  "server_version": "0.1.0",
  "project_dir": "/project",
  "url": "http://127.0.0.1:54321/#key=...",
  "pid": 12345,
  "session_dir": "/project/.visual-brainstorming/sessions/...",
  "screen_dir": "/project/.visual-brainstorming/sessions/.../content",
  "state_dir": "/project/.visual-brainstorming/sessions/.../state"
}
```

CLI 能连到旧版服务但版本不兼容时会显式区分“运行中”和“可复用”：

```json
{
  "running": true,
  "compatible": false,
  "server_version": "2.3.0",
  "project_dir": "/project",
  "pid": 12345
}
```

此时普通 `start`/`show` 拒绝复用；确认替换后使用 `--new`。

## 6. `publish`

```bash
python3 -I -S scripts/companion.py publish \
  --project-dir /project \
  --source /tmp/layout.html \
  --name layout-options
```

约束：

- 当前会话必须存在，且服务仍然健康；
- 文件后缀为 `.html` 或 `.htm`；
- UTF-8；
- 单个 HTML 画面最大 5 MiB；
- 通过 `/files/` 读取的单个辅助资源最大 10 MiB；
- `--name` 会被规范化；
- 目标文件名唯一；
- 临时文件写完后通过 `os.replace` 原子发布。

返回：

```json
{
  "type": "screen-published",
  "name": "20260712-182010-123-abcd-layout-options.html",
  "path": "/project/.visual-brainstorming/sessions/.../content/...html",
  "size": 4892,
  "version": "...",
  "published_at": "2026-07-12T18:20:10Z"
}
```

## 7. `events`

```bash
python3 -I -S scripts/companion.py events --project-dir /project
python3 -I -S scripts/companion.py events --project-dir /project --latest
python3 -I -S scripts/companion.py events --project-dir /project --tail 20
python3 -I -S scripts/companion.py events --project-dir /project --after 12
```

`--tail N` 在应用 `--after` 后只返回最后 N 个事件，范围为 0–200。`--latest` 与 `--tail` 不能同时使用。正常 Agent 路径推荐 `--tail 20`，以便同时看到最近选择和后续备注，而不是只看到最后一条事件。

选择事件：

```json
{
  "id": 7,
  "ts": "2026-07-12T18:20:31Z",
  "type": "choice",
  "choice": "confidence-cascade",
  "label": "置信度级联",
  "detail": "低置信度时升级",
  "screen": "20260712-182010-123-abcd-model-routing.html"
}
```

备注事件：

```json
{
  "id": 8,
  "ts": "2026-07-12T18:21:04Z",
  "type": "note",
  "label": "提交补充约束",
  "note": "保留 B 的结构，但把左侧筛选改成可折叠。",
  "screen": "20260712-182010-123-abcd-layout.html"
}
```

限制：

- `choice`：非空，最多 200 字符；
- `label`、`detail`：最多 500 字符；
- `note`：非空，最多 5000 字符；
- `payload`：序列化后最多 10 KiB；
- 请求体：最多 64 KiB；
- 每个 session 最多 10,000 个事件；
- `events.jsonl` 最大 5 MiB；达到任一上限后拒绝新事件，事件 ID 不会因拒绝而跳号；
- 无效 JSONL 行和无效历史 ID 会被忽略；新事件从历史最大有效 ID 继续递增。

## 8. `stop` 与 `demo`

停止：

```bash
python3 -I -S scripts/companion.py stop --project-dir /project
```

服务停止后保留会话文件供回看。

演示：

```bash
python3 -I -S scripts/companion.py demo \
  --project-dir /project --open
```

`demo` 启动服务并发布 `assets/templates/demo.html`。

### `prune`

列出满足条件的已停止旧 session，默认不删除：

```bash
python3 -I -S scripts/companion.py prune \
  --project-dir /project \
  --keep 5 \
  --older-than-days 30
```

dry-run 返回 `candidates`、`reclaimable_bytes` 和一个绑定当前精确候选集的 `plan`：

```json
{
  "dry_run": true,
  "plan": "<64-hex-plan>",
  "candidates": [
    {
      "session_dir": "/project/.visual-brainstorming/sessions/old-session",
      "bytes": 4096,
      "modified_at": "2026-05-01T00:00:00Z"
    }
  ],
  "deleted": []
}
```

确认列表后，把**同一次 dry-run** 的 `plan` 原样传给 apply：

```bash
python3 -I -S scripts/companion.py prune \
  --project-dir /project \
  --keep 5 \
  --older-than-days 30 \
  --apply \
  --plan "<64-hex-plan>"
```

- 当前 session 和仍能通过健康检查的活动 session 始终保留；
- session 根目录或候选路径出现 symlink 时拒绝删除；
- `--keep` 或 `--older-than-days` 不能为负数；
- `--apply` 必须带 fresh dry-run 的精确 `--plan`；候选、mtime、大小、current 或 active 状态变化时拒绝删除，要求重新预览；
- apply 成功时 `candidates` 为空，实际删除项只出现在 `deleted`；
- 只有用户明确同意 dry-run 中展示的候选后才使用 `--apply --plan ...`。

## 9. 启动输出

```json
{
  "type": "server-started",
  "version": "0.1.0",
  "pid": 12345,
  "host": "127.0.0.1",
  "url_host": "127.0.0.1",
  "port": 54321,
  "url": "http://127.0.0.1:54321/#key=<secret>",
  "control_url": "http://127.0.0.1:54321/?key=<secret>",
  "allow_remote": false,
  "idle_timeout_seconds": 7200,
  "project_dir": "/project",
  "session_dir": "/project/.visual-brainstorming/sessions/...",
  "screen_dir": "/project/.visual-brainstorming/sessions/.../content",
  "state_dir": "/project/.visual-brainstorming/sessions/.../state",
  "started_at": "2026-07-12T18:20:00Z"
}
```

`url` 用于首次浏览器访问，key 位于 fragment，不会随首次 HTTP 请求发送。Browser Shell 把 key 保存到当前 origin/tab 的 `sessionStorage`，清理地址栏，并使用 `/_vb/<key>/...` capability path 请求会话资源。`control_url` 仅写入本地状态并供 CLI 健康检查与停止。`/api/session` 不返回 key 或 `control_url`。后台启动不会把含 key 的 JSON 写入 `server.log`；routine access log 默认关闭，诊断日志会清理控制字符、脱敏 query、fragment 和 capability key、限制为每行 4 KiB 和每 session 256 KiB，并在支持权限位的系统上保持 `0600`。

## 10. HTTP 接口

根页面和 favicon 只提供无敏感信息的 bootstrap，不需要 key，也不刷新空闲时间。其他接口需要会话 key：浏览器使用 `/_vb/<key>/...` capability path，本地 CLI 使用 loopback `?key=...` 控制 URL。首次 URL 兼容旧 query key，但规范形式是 `#key=...`；Cookie 即使包含正确 key 也不会被接受。

| 方法 | 路径 | 用途 |
|---|---|---|
| `GET` | `/` | Browser Shell |
| `GET` | `/_vb/<key>/api/health` | 浏览器存活检查；CLI 使用 `/api/health?key=...` |
| `GET` | `/_vb/<key>/api/latest` | 最新 HTML 元数据 |
| `GET` | `/_vb/<key>/api/events` | 事件列表 |
| `GET` | `/_vb/<key>/api/session` | 不含密钥的会话元数据 |
| `POST` | `/_vb/<key>/api/events` | 追加用户事件 |
| `POST` | `/_vb/<key>/api/shutdown` | 浏览器停止服务；CLI 使用 `/api/shutdown?key=...` |
| `GET` | `/_vb/<key>/screen/<file>` | 渲染 HTML 页面 |
| `GET` | `/_vb/<key>/files/<path>` | 读取 `content/` 内非 HTML 辅助资源 |

浏览器 path-capability 写请求还要求：

- 与请求 Host 和实际监听端口精确一致的 `Origin`；
- `X-VB-Client: 1`；
- 有效 JSON 对象；
- 请求体不超过上限。

本机 CLI 使用 loopback query key 调用 `/api/shutdown` 时没有浏览器 `Origin`，这是唯一允许缺失 `Origin` 的 POST；它仍必须使用正确的 loopback Host/port、唯一 query key 和 `X-VB-Client: 1`。如果该请求显式携带 `Origin`，也必须与请求 authority 精确一致。

## 11. 页面包装与资源

HTML 片段会自动加入：

- `assets/frame.css`；
- `assets/injected-helper.css`；
- `assets/injected-helper.js`。

完整 HTML 保留原文档，只在最后一个 `</body>` 前注入助手；没有 `</body>` 时追加到末尾。已包含 `vb-injected-helper` 时不会重复注入。

Browser Shell 由以下资源组成：

- `assets/browser-shell.html`；
- `assets/browser-shell.css`；
- `assets/browser-shell.js`。

连接正常时，前台页面约每 1 秒查询新版本；浏览器标签隐藏后约每 5 秒查询。连接失败时采用指数退避，前台最多约 15 秒、隐藏标签页最多约 30 秒重试一次；恢复后回到正常频率。

bootstrap、轮询、健康检查和事件读取不刷新空闲时间。实际画面/辅助资源加载以及用户提交选择或备注会刷新空闲时间，因此打开但无人使用的标签页不会让服务无限存活。

## 12. 访问边界

服务拒绝：

- 无效会话 key、Host 或错误 Host 端口；
- path-capability POST 缺失 Origin，或任意不匹配请求 authority 的 Origin；
- `..` 路径穿越；
- 点文件与点目录；
- 符号链接；
- 当前会话 `content/` 以外的资源；
- 非 HTML 的 `/screen/` 请求；
- 通过 files 路由读取 `.html/.htm`；
- 空的选择 ID 或空备注。

页面响应附带 CSP。iframe 不使用 `allow-same-origin`；sandbox 页面使用不带 `allow-same-origin` 的不透明来源，不能读取父页面 `sessionStorage`。页面引用本地辅助资源时使用 `../files/<path>`，使 capability 保留在路径中；旧绝对 `/files/<path>` 仅在同 origin、同端口且 Referer 来自有效 screen capability 时兼容。每个 screen/version 都从 session key 派生独立 bridge，注入页面的事件必须同时通过 `message.source === frame.contentWindow` 和当前 bridge 校验，避免旧画面事件被归到新画面。bridge 不是针对页面自定义 JavaScript 的秘密或信任边界；Agent 生成页面仍按受控本地产物处理，不应给 iframe 增加 `allow-same-origin`。
