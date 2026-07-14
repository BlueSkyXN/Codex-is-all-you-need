# 搬入现有插件与定制

## 结论

这个压缩包的顶层目录就是一个 Skill。放入现有插件时，只复制：

```text
visual-brainstorming/
```

到：

```text
<your-plugin>/skills/visual-brainstorming/
```

不要复制或新建第二个 `.codex-plugin/plugin.json`。宿主插件的清单继续由宿主插件维护。

## 1. 最小搬运

```bash
cp -R visual-brainstorming /path/to/your-plugin/skills/
```

结果：

```text
your-plugin/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    ├── existing-skill/
    └── visual-brainstorming/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── scripts/
        ├── references/
        ├── assets/
        └── examples/
```

最低运行文件：

```text
SKILL.md
scripts/companion.py
assets/frame.css
assets/browser-shell.html
assets/browser-shell.css
assets/browser-shell.js
assets/injected-helper.css
assets/injected-helper.js
```

但建议保留整个目录；参考文档、模板和案例能显著降低后续维护成本。

## 2. 是否保留 `agents/openai.yaml`

建议保留。它属于 Skill 的可选元数据，控制：

- 展示名称；
- 简短说明；
- 图标；
- 品牌色；
- 默认提示；
- 是否允许隐式调用。

它不是插件 manifest，也不会把本目录注册成第二个插件。

如果宿主环境不读取该文件，保留它通常也不会影响脚本运行。需要只允许显式调用时，把 `allow_implicit_invocation` 改为 `false`。

## 3. 改名

假设改成 `design-room`：

1. 目录改为 `design-room/`；
2. `SKILL.md` frontmatter 改为 `name: design-room`；
3. 重写 `description` 的触发与排除范围；
4. 修改 `agents/openai.yaml` 的展示名、默认提示和图标；
5. 修改脚本中的运行目录名（可选）；
6. 检查 README、NOTICE、references 与 examples 中是否仍有旧名称；
7. 用内置 demo 和一条真实任务完成一次试运行。

目录名与 frontmatter `name` 保持一致，避免同一插件中发生识别混乱。

## 4. 最值得修改的六处

### 4.1 触发描述

`description` 是 Skill 被发现时最重要的字段。应写清：

- 任务类型：UI、架构、流程、模型路由；
- 输出介质：本地浏览器 HTML；
- 交互方式：点击与事件回传；
- 排除项：普通文字、简单表格、代码轨迹、隐藏推理。

不要写成“用于所有头脑风暴”，否则会过度触发。

### 4.2 用户同意策略

保留两个分支：

- 用户明确要求浏览器展示：不重复询问；
- 隐式触发：首次打开本地 URL 前询问一次。

团队可以调整文案，但应保留这些事实：

- 地址只在本机；
- 页面由 Agent 生成；
- 点击会写入项目临时目录；
- 用户可以继续只用聊天。

### 4.3 视觉基线

修改：

```text
assets/frame.css
assets/browser-shell.html
assets/browser-shell.css
assets/browser-shell.js
assets/injected-helper.css
assets/icon.svg
agents/openai.yaml
```

常见定制项：

- 品牌色；
- 字体栈；
- 卡片圆角和密度；
- 架构节点风格；
- 暗色模式；
- 移动端断点。

保持无外部字体和 CDN 依赖。页面内容视觉主要由 `frame.css` 控制；顶部本地伴侣外壳由 `browser-shell.*` 控制；点击焦点和选中轮廓由 `injected-helper.css` 控制。

### 4.4 模板

在 `assets/templates/` 中加入团队高频图型，例如：

- 双方案 UI 评审；
- 四象限取舍；
- 数据管道；
- 模型路由；
- 审批状态机；
- API 边界；
- 多租户隔离。

模板必须保留 `data-choice` 和 `data-label` 协议。

### 4.5 领域案例

替换或新增 `examples/`：

- 使用你们真实产品的命名方式；
- 删除不相关领域案例；
- 保留事实、估算和示意标签；
- 案例应体现“什么是结构上真实不同”。

示例用于塑造 Agent 输出质量，通常比增加更多文字规则更有效。

### 4.6 最终结论落点

在 `SKILL.md` 中指定团队固定产物位置，例如：

```text
docs/decisions/
docs/design/
architecture/decisions/
```

这样视觉选择不会只留在临时页面和聊天历史中。

## 5. 与其他 Skill 的分工

推荐拆分：

```text
skills/
├── visual-brainstorming/      # 浏览器伴侣、交互协议、通用视觉规则
├── product-ui-review/         # 产品 UI 的领域判断标准
├── architecture-review/       # 架构评审规则
└── model-routing-review/      # 模型路由、指标和降级策略
```

通用 Skill 负责“如何展示和回收选择”；领域 Skill 负责“什么是好方案”。不要把所有领域知识都塞进一个超长 `SKILL.md`。

## 6. 裁剪成更轻版本

### 只展示，不回传点击

可以删除事件 API 与注入助手，只保留：

```text
Agent 生成 HTML → 本地服务显示最新页面
```

复杂度从 L2 降为 L1，但用户选择要回到聊天中说明。

### 只手动打开 HTML

可以删除 `companion.py`，让 Skill 直接生成完整 HTML 文件。复杂度降为 L0，但没有自动刷新和统一样式注入。

### 只服务一种领域

例如只做架构图：

- 重写 `description`；
- 删除 UI 和流程模板；
- 替换所有案例；
- 保留服务、事件和架构组件。

## 7. 扩展事件

当前适合：

- 单选；
- 自由文本备注。

可扩展：

- 多选确认；
- 排序；
- 评分；
- 图上批注；
- 方案合并请求。

扩展时保持：

- `type` 明确；
- `choice` 使用稳定 ID；
- `screen` 能定位来源；
- 事件追加写，不修改历史；
- payload 有大小上限；
- 旧事件读取仍可工作。

## 8. 不建议一开始增加

除非已有明确需求，不要先加入：

- WebSocket；
- 数据库；
- 公网监听；
- 多用户身份；
- 前端框架；
- 浏览器自动化；
- 长期页面版本库。

这些能力会把一个小型 Skill 推向产品化平台。

## 9. 定制后验收

### 运行

```bash
python3 -I -S scripts/companion.py demo \
  --project-dir /tmp/visual-brainstorming-demo \
  --open
```

完成点击和备注后，读取事件并停止服务：

```bash
python3 -I -S scripts/companion.py events \
  --project-dir /tmp/visual-brainstorming-demo --tail 20
python3 -I -S scripts/companion.py stop \
  --project-dir /tmp/visual-brainstorming-demo
```

### 人工检查

- 宿主插件只保留一个 manifest；
- Skill 目录名与 `name` 一致；
- 5 个应触发提示能正确调用；
- 5 个不应触发提示不会误用浏览器；
- 示例在 360px 和桌面宽度可读；
- 点击和备注可被 `events --tail 20` 一并读取；
- 用户拒绝后不会重复询问；
- 项目忽略 `.visual-brainstorming/`；
- 页面没有外部网络依赖；
- 文案没有声称展示隐藏思维。
