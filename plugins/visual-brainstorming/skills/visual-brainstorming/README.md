# Visual Brainstorming Skill

**发布版本：0.1.0**

一个可独立使用、也可放入插件 `skills/` 目录的**单个 Skill**。本仓库通过 `plugins/visual-brainstorming/` 将它包装成独立 marketplace Plugin。它让 Agent 把 UI 样稿、架构图、流程图、模型路由等候选方案写成 HTML，在本地浏览器中并排展示，并把点击与备注记录为结构化事件。

> 本目录本身仍是 Skill，不包含第二个插件 manifest。Plugin manifest、marketplace metadata 和开发期自动化测试由宿主仓库维护。

## 参考对象与实现关系

核心概念参考 `obra/superpowers` 的 **Visual Companion / Visual Brainstorming**：Agent 生成页面、本地浏览器展示、用户选择回传、下一轮继续收敛。

本 Skill 不是 Superpowers 的复制版、分支或官方移植。本地服务、HTTP 协议、事件格式、浏览器外壳、视觉样式、模板和案例均为独立实现。详细声明见：

- `NOTICE.md`
- `references/SOURCES.md`

## 设计定位

它刻意保持在“够用但不过度工程化”的层级：

- **Agent 侧快路径**：读取 `SKILL.md` 和一个匹配模板，写一个 HTML 片段，执行一条 `show` 命令；
- **运行侧轻依赖**：Python 3.9+ 标准库，不安装第三方包；
- **交互侧够完整**：浏览器自动更新、点击选择、备注、JSONL 事件；
- **维护侧有余量**：脚本、模板、案例与按需参考资料齐全；
- **不扩展到**多人协作、数据库、WebSocket、账号体系或远程托管。

正常使用不需要读取实现脚本、全部示例或全部参考文档。

## 能力边界

适合：

- UI、导航、信息密度和布局方向；
- 系统架构、RAG 边界、数据流和模型路由；
- 流程、状态机、异常路径和实体关系；
- 需要用户在 2–4 个视觉方案中直接选择的问题。

不适合：

- 普通文字问答或简单参数表；
- 代码执行轨迹、日志监视或浏览器自动化；
- 只需一张简单 Mermaid 图的任务；
- 展示模型隐藏思维、Token 轨迹或内部状态。

## 放入现有插件

```bash
cp -R visual-brainstorming /path/to/my-plugin/skills/
```

目标结构：

```text
my-plugin/
├── .codex-plugin/
│   └── plugin.json                 # 继续由现有插件维护
└── skills/
    ├── other-skill/
    └── visual-brainstorming/
        ├── SKILL.md
        ├── agents/
        ├── scripts/
        ├── references/
        ├── assets/
        └── examples/
```

`agents/openai.yaml` 是 Skill 的展示与调用元数据，不是第二个插件注册文件。

## 最短运行路径

准备一个 HTML 片段后：

```bash
SKILL_DIR=/absolute/path/to/visual-brainstorming
PROJECT_ROOT=/absolute/path/to/project

python3 -I -S "$SKILL_DIR/scripts/companion.py" show \
  --project-dir "$PROJECT_ROOT" \
  --source /absolute/path/to/draft.html \
  --name navigation-choice \
  --open
```

读取最近选择与备注：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" events \
  --project-dir "$PROJECT_ROOT" --tail 20
```

停止：

```bash
python3 -I -S "$SKILL_DIR/scripts/companion.py" stop \
  --project-dir "$PROJECT_ROOT"
```

`-I -S` 让运行时忽略用户级 Python 启动配置和第三方 site 包；脚本只依赖标准库。

## 运行行为

- 默认只监听 `127.0.0.1`；
- 每个会话使用随机 key；
- `show` 在页面发布完成后才请求打开浏览器；
- 浏览器连接正常时前台约每秒检查一次新画面，隐藏标签页降低到约每 5 秒一次；连接失败后自动退避，前台最多约 15 秒、后台最多约 30 秒重试一次；
- 轮询和健康检查不刷新活动时间；默认连续 2 小时没有页面加载、资源加载或用户事件后停止；
- 运行数据写入 `PROJECT_ROOT/.visual-brainstorming/`，并自动生成 deny-all `.gitignore`；仍建议项目级忽略该目录。
- `prune` 默认 dry-run，只选择超过保留数量和时间门槛的已停止旧 session；当前和活动 session 始终保留，apply 必须携带 dry-run 返回的精确 plan。

`--allow-remote` 是只供专家显式启用的明文 HTTP 逃生口。Agent 不得自动使用；优先采用本地运行或受信任隧道，不能把它暴露到公网或不受信任网络。远程 URL 只接受本机实际持有的 literal loopback/private/link-local IP，不能指向另一台内网主机。

查看可清理的历史 session：

```bash
python3 -I -S scripts/companion.py prune --project-dir /absolute/path/to/project
```

确认列表后，把 dry-run 输出的 `plan` 原样传给 `--apply --plan "<plan>"`；候选变化时命令会拒绝并要求重新预览。

## 页面契约

最小选择元素：

```html
<article
  data-choice="stable-machine-id"
  data-label="人类可读名称"
  data-detail="可选补充说明">
  ...
</article>
```

备注元素：

```html
<textarea data-vb-note></textarea>
<button data-vb-submit-note data-label="提交备注">提交</button>
```

优先生成 HTML 片段；服务会自动套用 `assets/frame.css` 并注入选择助手。完整 HTML 也可使用，但通常更长、更难维护。

## 目录职责

```text
visual-brainstorming/
├── SKILL.md                         # Agent 快路径与行为边界
├── README.md                        # 维护者入口
├── NOTICE.md                        # 参考对象与实现声明
├── agents/openai.yaml               # 展示与调用元数据
├── scripts/companion.py             # 本地服务与 CLI
├── assets/templates/                # Agent 只需选择一个的页面骨架
├── examples/                        # 四个成品质量案例
└── references/                      # 按需背景、协议和维护资料
```

## 快速试运行

```bash
python3 -I -S scripts/companion.py demo \
  --project-dir /absolute/path/to/demo-project \
  --open
```

## 定制顺序

1. 修改 `SKILL.md` 的触发边界和团队流程；
2. 修改 `agents/openai.yaml` 的隐式调用策略；
3. 用真实业务案例替换 `examples/`；
4. 调整 `assets/frame.css`、`browser-shell.*` 和图标；
5. 最后才考虑扩展协议或多人能力。

迁移、改名、品牌化和裁剪方法见 `references/ADAPTATION.md`。
