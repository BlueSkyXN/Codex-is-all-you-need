# 示例索引

这些文件是可直接通过 `show` 展示的 HTML **片段**。本地伴侣会自动套用 `assets/frame.css` 并注入点击回传脚本。

| 文件 | 决策类型 | 重点学习 |
|---|---|---|
| `01-product-layout.html` | 产品首页布局 | 控制变量、真实 UI 结构差异、同尺度 mockup |
| `02-model-routing.html` | 模型路由 | 节点、分支、示意指标与数据诚实 |
| `03-system-architecture.html` | 系统边界 | 组件职责、同步路径、存储位置与故障边界 |
| `04-process-flow.html` | 审批流程 | 状态、分支、异常升级和泳道表达 |

正常 Agent 执行不需要先阅读全部示例；只在对应模板不足以表达任务时查看最接近的一个案例。

## 单独预览某个示例

```bash
python3 -I -S ../scripts/companion.py show \
  --project-dir /path/to/project \
  --source ./01-product-layout.html \
  --name product-layout \
  --open
```

## 使用原则

- 学习结构，不要机械替换文字；
- 每屏只保留一个主决策；
- 方案之间要有可解释的结构差异；
- 所有数字都要注明事实、估算或示意；
- 保留 `data-choice` 与 `data-label`。
