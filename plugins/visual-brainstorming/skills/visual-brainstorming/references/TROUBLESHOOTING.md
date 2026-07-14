# 故障处理

## 1. `status` 显示未运行

先检查：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" status \
  --project-dir "$PROJECT_ROOT"
```

若返回中仍有 `state_dir`，再查看 `state_dir/server.log`。该日志默认不记录 HTTP access line，且会脱敏和限制为 256 KiB；后台启动失败时还可能出现 `state_dir/launch-error.json`。若没有当前会话，`paths` 会返回 `No current session`，此时直接重新启动：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" start \
  --project-dir "$PROJECT_ROOT" --open
```

常见原因：

- Python 低于 3.9；
- 项目目录不存在或不可写；
- 宿主回收了后台子进程；
- 端口绑定失败；
- 服务达到空闲超时；
- 当前状态文件属于已结束或损坏会话。

若 `status` 显示 `running: true` 但 `compatible: false`，说明旧 companion 仍可达但不能安全复用。确认替换后执行同一启动命令并追加 `--new`。

宿主会回收后台进程时，使用持久 shell 运行：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" serve \
  --project-dir "$PROJECT_ROOT" --open
```

## 2. 服务过早自动停止

默认 `--idle-timeout 7200`，即连续 2 小时没有实际画面/辅助资源加载或用户事件后停止。bootstrap、`/api/latest` 轮询、健康检查和只读事件查询不会刷新活动时间，因此无人使用但仍打开的标签页不会永久保活服务。

需要长时间阅读或保留时：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" start \
  --project-dir "$PROJECT_ROOT" \
  --idle-timeout 0 --open
```

不要用 `0` 掩盖宿主主动回收进程的问题；这种情况应改用持久 shell 的 `serve`。

## 3. 浏览器打不开

检查：

- 使用启动输出中的完整 `url`；
- 首次打开时使用包含 `#key=...` 的完整 URL；页面加载后清理地址栏属于正常行为；
- 服务进程与浏览器是否在同一台机器或可达的网络命名空间；
- 防火墙、容器或远程开发环境是否阻断本地端口；
- `status` 是否仍为 `running: true`。

远程容器中的 `127.0.0.1` 指向容器自身。优先使用宿主已有的端口转发，不要直接把服务暴露到公网。显式 remote 模式的 `--url-host` 只能使用 Agent 主机实际持有的 literal loopback/private/link-local IP；不能填写公网 hostname 或另一台内网主机来“试一下”。

无法建立可达 URL 时，降级为静态 HTML、Mermaid、ASCII 或聊天中的结构化说明。

## 4. 返回 403

可能原因：

- URL 缺少或使用了旧会话 key；
- Host 被手动修改；
- 当前 tab 没有有效的 fragment/query key 或 `sessionStorage` 已被清除；
- 写请求 Origin 不匹配；
- 直接调用事件接口但没有 `X-VB-Client: 1`。

重新运行 `status`，使用返回的当前完整 URL。不要从 `/api/session` 复制密钥；该接口有意不回显密钥。

## 5. 页面一直等待发布

正常路径优先重新执行 `show`：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" show \
  --project-dir "$PROJECT_ROOT" \
  --source /absolute/path/to/draft.html \
  --name draft \
  --open
```

需要保留当前浏览器会话、只发布新页面时再单独执行：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" publish \
  --project-dir "$PROJECT_ROOT" \
  --source /absolute/path/to/draft.html \
  --name draft
```

检查：

- 当前服务仍健康；死服务会拒绝 `publish`；
- `source` 是 `.html` 或 `.htm`；
- HTML 文件为 UTF-8 且不超过 5 MiB；辅助资源不超过 10 MiB；
- `PROJECT_ROOT` 与启动时一致；
- 没有误写入旧会话目录。

## 6. 页面不自动更新

每次修改后重新运行 `publish`，不要直接覆盖旧发布文件。

Browser Shell 在前台约每 1 秒查询一次，标签隐藏时约每 5 秒查询。仍不更新时：

1. 刷新 Browser Shell；
2. 查看 `/api/latest` 是否返回新文件名；
3. 查看 `server.log`；
4. 确认新文件修改时间晚于旧文件；
5. 确认没有在另一个项目目录启动第二个会话。

## 7. 页面样式或交互助手没有加载

HTML 片段会自动加入：

- `assets/frame.css`；
- `assets/injected-helper.css`；
- `assets/injected-helper.js`。

完整 HTML 保留自己的 CSS，只注入交互助手。若完整文档含严格的 `<meta http-equiv="Content-Security-Policy">`，它可能阻止注入的内联脚本。优先改为片段，或调整文档 CSP。

`assets/browser-shell.*` 只控制顶部本地伴侣外壳，不控制方案内容页面。

## 8. 点击后读不到事件

可选元素必须包含：

```html
<article data-choice="stable-id" data-label="方案名称">...</article>
```

读取：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" events \
  --project-dir "$PROJECT_ROOT" --tail 20
```

检查：

- `data-choice` 非空；
- 不嵌套多个 `[data-choice]`；
- 不把页面再放进第二层 iframe；
- 页面脚本没有阻止事件传播或替换 DOM；
- toast 是否显示“已记录”；
- `events.jsonl` 是否可写；
- 页面属于当前会话。

若最后一条是备注而不是选择，`--latest` 只会返回备注；正常路径使用 `--tail 20`，同时检查最近选择及其后的备注。

空选择和空备注会返回 422，而不是写入无意义事件。

## 9. 本地图片或 SVG 读不到

把辅助资源复制到当前会话 `screen_dir`，并使用：

```html
<img src="../files/architecture-overview.svg" alt="系统架构概览">
```

限制：

- 不允许 `..`、点文件、符号链接或会话目录之外的路径；
- files 路由明确拒绝 `.html/.htm`；页面本身只能通过 screen 路由展示；
- 使用 `../files/<path>`，使浏览器保留当前会话的 capability path；旧绝对 `/files/<path>` 只作为同源 Referer 兼容路径。

## 10. 备注无法提交

需要同时存在：

```html
<textarea data-vb-note></textarea>
<button data-vb-submit-note data-label="提交备注">提交</button>
```

一屏只保留一个主备注框；空文本不会写入事件。

## 11. 页面横向溢出或暗色模式异常

常见处理：

- SVG 使用 `viewBox` 和 `width="100%"`；
- Grid 子项设置 `min-width: 0`；
- 长文本允许换行；
- 避免固定宽度和大面积 `white-space: nowrap`；
- SVG 使用 `currentColor`；
- 在 390px 与桌面宽度检查；
- 不只依赖颜色表达状态。

## 12. Windows 后台进程立即停止

某些 Agent 宿主会主动结束脱离终端的子进程。使用宿主持久终端：

```powershell
python "$SKILL_DIR\scripts\companion.py" serve `
  --project-dir "$PROJECT_ROOT" --open
```

这类问题不能通过增加空闲超时解决。

## 13. 会话状态损坏

先确认旧进程不存在，再删除项目临时目录：

```bash
rm -rf "$PROJECT_ROOT/.visual-brainstorming"
```

PowerShell：

```powershell
Remove-Item -Recurse -Force "$PROJECT_ROOT\.visual-brainstorming"
```

删除前确认没有需要保留的页面或备注。

## 14. 放入插件后无法识别 Skill

逐项检查：

- 目录名与 `SKILL.md` frontmatter 的 `name` 一致；
- Skill 位于宿主插件的 `skills/` 目录内；
- 没有在本 Skill 内误放第二份插件 manifest；
- `SKILL.md`、`scripts/companion.py` 和浏览器资源均完整；
- 文档与模板没有被复制工具改名；
- Python 版本不低于 3.9；
- 修改 `agents/openai.yaml` 后重新加载宿主环境。
