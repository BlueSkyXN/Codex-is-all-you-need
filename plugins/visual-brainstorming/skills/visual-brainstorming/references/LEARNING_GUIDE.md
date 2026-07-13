# 学习对象与练习路线

## 学习目标

通过这个 Skill 理解：如何把一个纯提示词工作流扩展为带本地界面、确定性脚本和结构化用户反馈的可复用 Agent 能力。

它不是单纯学习“写网页”，而是同时学习五类对象。

## 1. Agent Skill 设计

### 学习对象

- `SKILL.md` frontmatter；
- `name` 与 `description` 的触发作用；
- 核心指令与按需参考资料的渐进加载；
- `scripts/`、`references/`、`assets/` 和 `agents/openai.yaml`；
- 显式调用与隐式调用；
- 触发边界和负面样例。

### 对应文件

```text
SKILL.md
agents/openai.yaml
references/EVALUATION.md
```

### 练习

1. 写 5 个应触发提示；
2. 写 5 个不应触发提示；
3. 将 `description` 缩短 30%，仍保持边界清楚；
4. 把 Skill 改成只服务“架构比较”；
5. 解释为什么详细协议不应全部塞进 `SKILL.md`。

## 2. 视觉决策建模

### 学习对象

- 把开放问题拆成单一决策；
- 控制变量；
- 生成结构上真实不同的方案；
- 事实、估算和示意的区分；
- 用稳定 ID 表示用户选择；
- 逐轮收敛而不是重复发散。

### 对应文件

```text
references/BACKGROUND.md
references/WORKFLOW.md
references/VISUAL_AUTHORING.md
examples/
```

### 练习

把“重做后台”拆成四屏：

```text
导航结构
信息密度
筛选方式
详情呈现
```

每屏写出：

- 固定变量；
- 变化变量；
- 三个真实方案；
- 观察重点；
- 选择后的下一步。

## 3. 本地 HTTP 服务

### 学习对象

- `ThreadingHTTPServer`；
- 路由和内容类型；
- 会话目录；
- 随机密钥；
- URL fragment、`sessionStorage` 与 path capability；
- 本地进程生命周期；
- 跨平台后台启动；
- 健康检查。

### 对应文件

```text
scripts/companion.py
assets/browser-shell.html
assets/browser-shell.css
assets/browser-shell.js
references/ARCHITECTURE.md
references/PROTOCOL.md
```

### 练习

1. 为 `/api/latest` 增加页面标题字段；
2. 为 `status` 增加已记录事件数量；
3. 增加 `list-screens` 命令；
4. 解释为什么默认只绑定 `127.0.0.1`；
5. 比较后台 `start` 与前台 `serve` 的生命周期差异。

## 4. 文件系统与事件日志

### 学习对象

- 原子写入；
- 唯一文件名；
- JSONL；
- 递增事件 ID；
- 路径规范化；
- 路径穿越；
- 符号链接边界；
- 不信任项目状态文件。

### 对应文件

```text
scripts/companion.py
references/PROTOCOL.md
```

### 练习

1. 为事件增加 `session_id`；
2. 写一个脚本导出 Markdown 决策摘要；
3. 增加最大历史页面数量并安全清理旧文件；
4. 构造三种路径穿越输入并解释为什么被拒绝；
5. 把 JSONL 替换为 SQLite，列出收益和新增复杂度。

## 5. 浏览器隔离与事件桥接

### 学习对象

- `<iframe sandbox>`；
- `window.postMessage`；
- 父页面与子页面的职责；
- 父页面 `sessionStorage` 与 sandbox iframe 的 origin 隔离；
- Origin 检查；
- 动态注入脚本；
- 键盘可访问性。

### 对应文件

```text
scripts/companion.py
assets/injected-helper.css
assets/injected-helper.js
references/ARCHITECTURE.md
```

### 练习

1. 增加多选确认事件；
2. 增加“评分 1–5”事件；
3. 保持 iframe 不直接访问事件 API；
4. 解释为什么不加入 `allow-same-origin`；
5. 增加对 Escape 取消选择的支持。

## 6. HTML、CSS 与 SVG 视觉表达

### 学习对象

- CSS Grid 和 Flexbox；
- 响应式布局；
- 内联 SVG；
- 架构节点、箭头、边界和泳道；
- UI 线框稿；
- 暗色模式；
- 可访问性；
- 离线资源。

### 对应文件

```text
assets/frame.css
assets/browser-shell.css
assets/injected-helper.css
assets/templates/
examples/
```

### 练习

1. 把模型路由示例改为四种方案；
2. 让架构图在 390px 宽度仍清楚；
3. 增加一个状态机模板；
4. 不使用颜色，仍能区分正常与异常路径；
5. 将一个复杂 SVG 拆成两层渐进页面。

## 7. 评估与回归设计

### 学习对象

- 结构检查；
- HTTP 与事件闭环验证；
- 触发评估；
- 人工视觉回归；
- 桌面与移动截图；
- 正例、负例和边界提示集。

正式发布包不携带测试实现。需要自动化回归时，应在宿主仓库的开发目录中单独维护，避免把维护工具加入 Agent 的 Skill 分发目录。

### 对应文件

```text
references/EVALUATION.md
references/PROTOCOL.md
```

### 练习

1. 设计无效 UTF-8 和超限页面的回归用例；
2. 自动检查所有示例无外部 URL；
3. 使用无头浏览器截取桌面和移动截图；
4. 建立一组真实用户提示的触发回归集；
5. 记录一次完整闭环所用命令数和生成页面大小。

## 推荐学习顺序

### 第一阶段：理解概念

```text
README.md
→ SKILL.md
→ references/BACKGROUND.md
→ examples/README.md
```

### 第二阶段：跑通闭环

```text
assets/templates/demo.html
→ scripts/companion.py demo
→ 点击页面
→ scripts/companion.py events --tail 20
```

### 第三阶段：理解实现

```text
references/ARCHITECTURE.md
→ references/PROTOCOL.md
→ scripts/companion.py
→ references/EVALUATION.md
```

### 第四阶段：做领域改造

```text
references/ADAPTATION.md
→ 修改 description
→ 替换模板和案例
→ references/EVALUATION.md
→ 运行 demo 与人工验收
```

## 进阶路线

由低到高：

1. 页面缩略图历史；
2. 多选和排序；
3. 评分与理由；
4. 画布批注；
5. 决策摘要自动导出；
6. SSE 或 WebSocket 推送；
7. 会话恢复；
8. 多用户协作；
9. 远程访问和身份体系；
10. 与 Figma 或白板工具双向同步。

每次升级前先回答：当前问题是否真的需要更高实时性、更长期状态或更多用户。不要把技术练习误当成产品需求。
