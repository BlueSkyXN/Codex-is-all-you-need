# 视觉页面编写指南

## 1. 页面契约

每一屏都必须回答一个明确问题，而不是仅仅“展示一些内容”。推荐骨架：

```html
<section class="vb-page">
  <header class="vb-hero">
    <p class="vb-eyebrow">决策类别</p>
    <h1>本屏只解决的一个问题</h1>
    <p class="vb-lead">告诉用户应该观察哪些差异。</p>
    <div class="vb-decision-strip">
      <span class="vb-decision-icon">1</span>
      <div><strong>本屏只决定：</strong>唯一待决策变量。</div>
    </div>
  </header>

  <div class="vb-grid vb-grid-3">
    <article class="vb-option" data-choice="a" data-label="方案 A">...</article>
    <article class="vb-option" data-choice="b" data-label="方案 B">...</article>
    <article class="vb-option" data-choice="c" data-label="方案 C">...</article>
  </div>
</section>
```

页面可以是 HTML 片段。服务会自动加入文档外壳、`assets/frame.css`、`assets/injected-helper.css` 和交互脚本。完整 HTML 会保留原样并在 `</body>` 前注入助手；若文档自带严格的 meta CSP，可能阻止内联助手，优先使用片段。

## 2. 选择协议

每个可选元素至少包含：

```html
data-choice="stable-machine-id"
data-label="人类可读名称"
```

可选补充：

```html
data-detail="一句结构差异或选择含义"
```

规则：

- `data-choice` 在同一任务中保持稳定；
- 使用小写 kebab-case，例如 `side-navigation`；
- `data-label` 适合直接复述给用户；
- 不要把整个页面设为一个选择；
- 不要嵌套两个不同的 `[data-choice]`。

注入助手会自动：

- 添加键盘焦点；
- 支持 Enter 和 Space；
- 添加 `.vb-selected`；
- 通过 `postMessage` 交给外层页面。

不要让页面直接请求 `/api/events`。

## 3. 备注输入

需要收集自由文本时使用：

```html
<div class="vb-note-box">
  <label for="note">补充约束</label>
  <textarea id="note" data-vb-note></textarea>
  <button type="button" data-vb-submit-note data-label="提交补充约束">
    提交备注
  </button>
</div>
```

一屏最多保留一个主备注框。复杂表单应继续留在聊天或专门界面中。

## 4. 方案差异的质量

一个有效方案应当回答：

- 它改变了什么结构？
- 它适合什么条件？
- 它带来什么收益？
- 它付出什么代价？
- 为什么它不是另一个方案的轻微变体？

无效差异：

- 只换颜色；
- 只换标题；
- 只换图标；
- 同一布局做三个主题皮肤；
- 把“激进 / 平衡 / 保守”写成空泛标签，却没有结构变化。

## 5. 控制变量

比较导航时：

- 内容一致；
- 字体和配色一致；
- 功能范围一致；
- 只改变顶栏、侧栏或工作区结构。

比较架构时：

- 业务能力一致；
- 节点粒度一致；
- 图形尺度一致；
- 只改变边界、路径或部署责任。

比较流程时：

- 起点、终点和业务目标一致；
- 异常情况一致；
- 只改变审批、分流或回退策略。

## 6. 使用内置样式

基础类：

| 类 | 用途 |
|---|---|
| `.vb-page` | 页面宽度与外边距 |
| `.vb-hero` | 标题区 |
| `.vb-eyebrow` | 决策类别 |
| `.vb-lead` | 辅助说明 |
| `.vb-decision-strip` | 单一决策声明 |
| `.vb-grid-2/3/4` | 响应式方案网格 |
| `.vb-option` | 可选卡片 |
| `.vb-panel` | 非选择信息块 |
| `.vb-visual` | 图形容器 |
| `.vb-callout` | 关键前提或提醒 |
| `.vb-note-box` | 用户备注 |

方案头部：

```html
<div class="vb-option-head">
  <span class="vb-index">A</span>
  <span class="vb-tag">适用条件</span>
</div>
```

## 7. UI 样稿

内置线框组件：

- `.vb-browser`
- `.vb-browser-bar`
- `.vb-browser-body`
- `.vb-window-dot`
- `.vb-wire`
- `.vb-wire-block`
- `.vb-wire-card-grid`
- `.vb-wire-card`

示例：

```html
<div class="vb-visual">
  <div class="vb-browser">
    <div class="vb-browser-bar">
      <i class="vb-window-dot"></i>
      <i class="vb-window-dot"></i>
      <i class="vb-window-dot"></i>
    </div>
    <div class="vb-browser-body">
      <div class="vb-wire dark medium"></div>
      <div class="vb-wire primary button"></div>
      <div class="vb-wire-block"></div>
    </div>
  </div>
</div>
```

真实 UI 对比建议：

- 使用接近真实长度的文案；
- 标明目标屏幕宽度；
- 同一组内容在各方案中完整出现；
- 不要使用纯装饰性 Lorem Ipsum 填满页面；
- 复杂界面可用内联 SVG 或局部 HTML，而不是截图。

## 8. 架构与流程

内置图形组件：

- `.vb-diagram`
- `.vb-flow-row`
- `.vb-flow-column`
- `.vb-node`
- `.vb-arrow`
- `.vb-branch`
- `.vb-swimlanes`
- `.vb-lane`

架构图至少说明：

- 系统边界；
- 节点职责；
- 主要数据流；
- 同步或异步；
- 持久化位置；
- 与当前决策有关的失败或降级路径。

流程图至少说明：

- 单一入口；
- 一致方向；
- 明确决策条件；
- 终止状态；
- 退回、拒绝、超时或异常路径。

节点超过约 12 个时，优先拆图或先展示高层边界。

## 9. 模型与技术方案对比

必须区分：

- **事实**：来自用户、代码、文档或实测；
- **估算**：有依据但未实测；
- **示意**：只表达相对结构。

没有可靠数据时，可以比较：

- 请求路径；
- 模型路由；
- 缓存、检索和工具位置；
- 升级、回退和重试；
- 故障边界；
- 运维责任。

不要编造具体模型价格、延迟、准确率、吞吐或 SLA。

条形指标应明确标为“示意”，并只用于相对关系：

```html
<div class="vb-metric">
  <span>系统复杂度</span>
  <div class="vb-meter"><span style="--value:58%"></span></div>
  <strong>中</strong>
</div>
```

## 10. 视觉编码

优先使用：

- 网格和分栏；
- 节点、箭头、边界和泳道；
- 同一尺度的并排图；
- 文字与图形双重标注；
- 少量强调色表达类别。

避免：

- 颜色作为唯一信息编码；
- 无刻度、无说明的雷达图；
- 过多渐变、阴影和动画；
- 把装饰当成信息；
- 让视觉层级压过决策本身。

## 11. 可访问性

发布前确认：

- 正文字号不小于约 14px；
- 点击区域不小于约 40px；
- 可用键盘选择；
- 有明确焦点状态；
- 不只靠颜色表达状态；
- SVG 有 `aria-label` 或可读文字；
- 360px 宽度无水平溢出；
- 动画遵守 `prefers-reduced-motion`。

## 12. 离线与资源路径

默认禁止：

- Google Fonts；
- CDN 脚本；
- 远程图片；
- 在线图表库。

优先使用 HTML、CSS 和内联 SVG。

若必须引用本地资源，将文件复制到当前会话 `screen_dir`，并使用：

```html
<img src="../files/architecture-overview.svg" alt="系统架构概览">
```

使用 `../files/<path>`，让浏览器从当前 `/_vb/<key>/screen/<页面名>` 路径解析到同一会话的 files capability。不要使用 `./architecture-overview.svg`；files 路由只用于图片、字体、JSON 等辅助资源，明确拒绝 `.html/.htm`，不要把它当成第二个页面入口。旧绝对 `/files/<path>` 只作为同 origin、同端口 Referer 兼容路径。

## 13. 发布前检查

```text
[ ] 一屏只有一个主问题
[ ] 2–4 个方案结构上真实不同
[ ] 非决策变量保持一致
[ ] data-choice 与 data-label 完整
[ ] 事实、估算和示意已区分
[ ] 无外部网络依赖
[ ] 桌面和移动端可读
[ ] 图形含义可被文字解释
[ ] 没有声称展示模型内部思维
```
