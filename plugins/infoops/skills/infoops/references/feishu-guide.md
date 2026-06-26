# 飞书数据源对接指南

InfoOps 通过 lark-cli 从飞书采集数据。本文件定义采集策略、数据流转和 cron 配置。

操作前先阅读 SKILL.md 和 taxonomy.md。

---

## 操作原则

1. **飞书侧只读**：只拉取数据，不发消息、不建群、不改文档、不删文件
2. **先读 skill 再操作**：每次操作飞书前，先读对应内嵌 skill 获取最新命令文档
3. **最小权限**：优先 `--as user`，bot 身份用于应用级操作
4. **命令以 lark-cli 为准**：本文件的命令速查是辅助参考，详细参数以 `lark-cli <domain> +<cmd> --help` 和内嵌 skill 为准

---

## 内嵌 skill 引导

lark-cli 自带完整的领域 skill 文档。**操作前必须先读对应 skill**：

```bash
# 列出所有可用 skill
lark-cli skills list

# 读取认证和安全规则（首次操作或遇权限问题时必读）
lark-cli skills read lark-shared

# 按领域读取
lark-cli skills read lark-im          # IM 消息和群聊
lark-cli skills read lark-drive       # 云空间文件
lark-cli skills read lark-doc         # 云文档内容
lark-cli skills read lark-sheets      # 电子表格
lark-cli skills read lark-base        # 多维表格
lark-cli skills read lark-wiki        # 知识库
lark-cli skills read lark-contact     # 通讯录

# 读取 skill 的 reference 子文档
lark-cli skills list lark-im/references
lark-cli skills read lark-im/references/<文件名>.md
```

---

## InfoOps 常用命令速查

以下命令经过实际验证。详细参数见 `lark-cli <cmd> --help`。

### IM 消息

```bash
# 列出所有群（默认只返回群聊，加 --types 可含单聊）
lark-cli im +chat-list --as user
lark-cli im +chat-list --as user --types p2p,group    # 含单聊
lark-cli im +chat-list --as user --sort active_time    # 按活跃时间排序

# 拉取指定群的最近消息
lark-cli im +chat-messages-list --chat-id <chat_id> --as user
lark-cli im +chat-messages-list --chat-id <chat_id> --as user --start <ISO8601> --end <ISO8601>

# 搜索消息（关键词+时间+发送者）
lark-cli im +messages-search --query <关键词> --as user
lark-cli im +messages-search --sender <open_id> --start <ISO8601> --end <ISO8601> --as user
lark-cli im +messages-search --sender <open_id> --start <7天前ISO8601> --as user    # 找我7天内发言的群

# 搜索群（按群名查 chat_id）
lark-cli im +chat-search --query <群名关键词> --as user

# 获取群信息
lark-cli im chats get --chat-id <chat_id> --as user

# 获取群成员列表
lark-cli im chat.members get --chat-id <chat_id> --as user
```

### 通讯录

```bash
# 搜索用户（姓名/邮箱/open_id）
lark-cli contact +search-user --query <关键词> --as user

# 获取用户信息（不带 --user-id 则返回自己）
lark-cli contact +get-user --as user
lark-cli contact +get-user --user-id <open_id> --as user
```

### 云空间

```bash
# 搜索云空间文件（按关键词、类型、时间范围）
lark-cli drive +search --query <关键词> --as user
lark-cli drive +search --doc-types doc,sheet,bitable --edited-since 7d --as user
lark-cli drive +search --mine --as user    # 我拥有的文件

# 检查文件元信息（类型、标题、token）
lark-cli drive +inspect --url <飞书文档URL> --as user

# 批量获取文件元数据
lark-cli drive metas batch_query --as user    # 需要传 body，详见 lark-drive skill

# 导出文件到本地
lark-cli drive +export --token <file_token> --type <doc_type> --as user
```

### 多维表格

```bash
# 获取 Base 信息
lark-cli base +base-get --base-token <app_token> --as user

# 列出表
lark-cli base +table-list --base-token <app_token> --as user

# 列出记录
lark-cli base +record-list --base-token <app_token> --table-id <table_id> --as user

# 列出字段
lark-cli base +field-list --base-token <app_token> --table-id <table_id> --as user
```

### 知识库

```bash
# 列出知识库空间
lark-cli wiki +space-list --as user

# 获取知识库节点详情
lark-cli wiki +node-get --token <wiki_token> --as user

# 列出节点下的子节点
lark-cli wiki +node-list --space-id <space_id> --as user
```

---

## 采集策略

### IM 群消息

| 优先级 | 范围 | 采集频率 | 方式 | 产出 |
|--------|------|---------|------|------|
| 高 | 7天内我有发言的群 | 每日 | +chat-messages-list | DIGEST 更新 + 信号判定 |
| 中 | 有独立档案但近7天我未发言 | 每周 / 事件触发 | +chat-messages-list | 检查信号节奏 |
| 低 | PULSE 索引中的其他群 | 按需 | +messages-search | — |
| 不采集 | 其余群 | — | — | — |

判定「7天内我有发言」：
```bash
lark-cli im +messages-search --sender <我的open_id> --start <7天前> --as user
```
从结果中提取 chat_id 去重，即为我近7天有发言的群/单聊列表。

### IM 单聊

不主动批量拉取（隐私考虑），仅在以下场景采集：
- 30天内我有发言的人（优先级高）
- 用户主动问"<人名>最近找我了吗"
- 线程关联人有待回复消息
- +messages-search 命中关联人

判定「30天内我有发言」：
```bash
lark-cli im +messages-search --sender <我的open_id> --start <30天前> --chat-type p2p --as user
```

### 云空间文件

| 优先级 | 范围 | 采集频率 | 检测方式 | 产出 |
|--------|------|---------|---------|------|
| 高 | L3 独立追踪文件 | 每日 | drive +search --edited-since 1d | 变更日志更新 |
| 中 | L2 聚合追踪中的主线文件 | 每周 | drive +search 按 token 检查 | 变更日志更新 |
| 低 | L1 _index 中的文件 | 按需 | 事件触发或手动 | 检查是否需升格 |
| 不采集 | L0 排除的文件 | — | — | — |

### Wiki 文章

Wiki 文章采集后的处理：

1. `lark-cli wiki +node-get --token <wiki_token>` 获取节点 → 拿到实际文件类型和 doc_token/sheet_token
2. 按文件类型归入对应目录：
   - wiki 文章是云文档 → sources/space/docs/
   - wiki 文章是电子表格 → sources/space/sheets/
3. 追踪文件头部标注 `(Wiki)` 来源和 wiki_token

---

## 排除过滤

采集到的文件在写入 InfoOps 前，需经过排除过滤（详细规则见 taxonomy.md）。

### 排除判断流程

```
采集到一个文件
  ↓
是书籍/论文？（ISBN/DOI/出版社标记） → 排除
  ↓
是工具/软件包/安装包？（.exe/.dmg/.tar.gz/.whl/...） → 排除
  ↓
是被分享的阅读材料？（无协作编辑） → 排除
  ↓
是工作产出物或协作文档？ → 纳入
```

---

## 数据流转

### 采集到写入的处理流程

```
lark-cli 输出（原始数据）
  ↓
Agent 处理：
  1. 排除过滤（非工作信息不入库）
  2. 内外部判定（群→internal/external，人→内部/外部）
  3. 信号节奏判定（对比基线数据）
  4. 线程关联（匹配已有线程或判断是否开新线程）
  5. 跨源关联（同时段多源信号是否指向同一事）
  ↓
写入 InfoOps 文件：
  - 事件细节 → threads/active/<线程名>.md
  - 群摘要 → sources/groups/.../<群名>/DIGEST.md
  - 人物行为 → sources/people/<人名>.md 或 ROSTER.md
  - 文件变更 → sources/space/.../<追踪文件>.md
  - 态势总览 → PULSE.md
```

### 处理原则

1. 不存原始消息，写摘要和判断
2. 排除规则先行，不满足条件的不进入后续处理
3. 内外部分类一次确定，不重复判断
4. 关联线程优先，无匹配线程的看是否需开新线程

---

## ID 体系对接

| 飞书 ID | 用途 | InfoOps 中的位置 |
|---------|------|-----------------|
| open_id | 用户唯一标识 | ID-MAP Self 表 + 跨群匹配用 |
| chat_id | 群/单聊标识 | ID-MAP 各分区 |
| doc_token | 云文档标识 | sources/space/docs/ 追踪文件头部 |
| sheet_token | 电子表格标识 | sources/space/sheets/ 追踪文件头部 |
| app_token | 多维表格 App 标识 | sources/space/bitables/ 追踪文件头部 |
| table_id | 多维表格内具体表 | 同上，与 app_token 一起记录 |
| file_token | 通用文件标识 | sources/space/pdfs/ 追踪文件头部 |
| wiki_token | 知识库节点标识 | 追踪文件头部附加字段 |

### 跨群人物识别的执行

```bash
# 1. 拉重点群成员列表
lark-cli im chat.members get --chat-id <chat_id> --as user

# 2. 提取每个成员的 open_id

# 3. 对所有重点群执行步骤 1-2

# 4. 用 open_id 交叉匹配，找出跨群人物

# 5. 结果写入各群 ROSTER.md 的「跨群出现」列
```

---

## Cron 配置

### 建议的定时任务

| 任务 | 频率 | cron 示例 | 动作 |
|------|------|---------|------|
| 重点群每日摘要 | 每日 08:00 | `0 8 * * *` | 拉消息→更新 DIGEST→标记信号 |
| 云空间变更检测 | 每日 09:00 | `0 9 * * *` | drive +search --edited-since 1d→更新变更日志 |
| 线程待办检查 | 每日 08:30 | `30 8 * * *` | 扫描 active 线程待办→标记逾期 |
| PULSE 全量刷新 | 每日 09:30 | `30 9 * * *` | 合成 PULSE.md |
| PULSE 快照 | 每周一 10:00 | `0 10 * * 1` | 备份到 archive/snapshots/ |
| DIGEST 季度归档 | 每季度首日 | `0 10 1 1,4,7,10 *` | 归档旧 DIGEST |
| Cooling 检查 | 每周五 16:00 | `0 16 * * 5` | 扫描 14+ 天无动静的对象 |
| 跨群人物刷新 | 每月 1 日 | `0 10 1 * *` | 重新拉取群成员→交叉匹配 |

### 执行流程

```
cron 触发
  → 读对应 lark-cli 内嵌 skill
  → lark-cli 采集（只读）
  → 排除过滤
  → Agent 处理（分类、关联）
  → 写入 InfoOps 文件（本地）
  → 如有 Surge → 推送提醒
```

---

## 初始化流程

首次部署 InfoOps 的步骤：

```
1. 确认 lark-cli 可用
   command -v lark-cli && lark-cli --version
   lark-cli skills read lark-shared    # 了解认证规则

2. 创建目录结构
   mkdir -p workspace/infoops/{threads/active,threads/closed/archive}
   mkdir -p workspace/infoops/sources/groups/{internal,external}
   mkdir -p workspace/infoops/sources/people
   mkdir -p workspace/infoops/sources/space/{docs,sheets,bitables,pdfs}
   mkdir -p workspace/infoops/archive/{threads,digests,snapshots}

3. 初始化 ID-MAP.md
   lark-cli im +chat-list --as user                         # 群列表
   lark-cli im +chat-list --as user --types p2p,group       # 含单聊
   → 按内部群/外部群/内部单聊/外部单聊/Bot 分区填入 ID-MAP

4. 初始化 MISSION.md
   → 填入身份、职责、优先级、决策原则
   → 标注各数据源接入状态

5. 识别重点对象（我有参与的）
   lark-cli im +messages-search --sender <我的open_id> --start <7天前> --as user
   → 从结果提取我近7天有发言的群 → 满足条件的建 sources/ 文件
   lark-cli im +messages-search --sender <我的open_id> --start <30天前> --chat-type p2p --as user
   → 从结果提取我近30天有发言的人 → 满足条件的建 sources/ 文件
   → 确认需要追踪的云空间文件 → 建 _index 或追踪文件

6. 识别活跃线程
   → 拉取重点群近 7 天消息
   → 提取正在进行的事务 → 创建 threads/active/ 文件

7. 生成首版 PULSE.md

8. 配置 cron 任务

9. 部署 _RULES.md（从 SKILL.md 各 reference 提取关键参数）
```

### 最小启动（快速跑起来）

只需 3 个文件即可开始运行：

```
workspace/infoops/
├── MISSION.md      填入身份和优先级
├── ID-MAP.md       从 chat-list 灌入
└── PULSE.md        首版，哪怕只有 Active 和 Directory 两个分区
```

其余目录和文件在实际使用中按需创建。

---

## 常见操作场景

### 场景 1："帮我看看<群名>最近在聊什么"

```
1. 读 sources/groups/.../<群名>/DIGEST.md（或简单群 md）
2. 如 DIGEST 过期 → lark-cli skills read lark-im → +chat-messages-list
3. 处理消息：排除→分类→信号判定
4. 更新 DIGEST
5. 检查关联线程
6. 向用户汇报 + 行动建议
```

### 场景 2："<文件名>最近有人改吗"

```
1. 在 sources/space/ 下找到对应追踪文件（或 _index 条目）
2. lark-cli skills read lark-drive → drive +search 或 +inspect 检查变更
3. 如有变更：更新变更日志，标注谁改了什么
4. 检查变更是否影响关联线程
5. 向用户汇报
```

### 场景 3："<人名>最近有找我吗"

```
1. 从 ID-MAP Internal/External Chats 找到 chat_id
2. lark-cli skills read lark-im → +messages-search 或 +chat-messages-list
3. 读 sources/people/<人名>.md 获取上下文
4. 总结消息，关联线程
5. 汇报 + 是否需要回复
```

### 场景 4："Wiki 里那篇<文章名>更新了吗"

```
1. 确认此文件在 sources/space/ 中的追踪文件
2. lark-cli skills read lark-wiki → +node-get 用 wiki_token 检查
3. 如有变更：更新变更日志
4. 汇报变更内容和影响
```

### 场景 5：每日自动刷新

```
1. 遍历 MISSION 中标记为"每日"的数据源
2. IM：对每个重点群执行 +chat-messages-list → 更新 DIGEST
3. 空间：drive +search --edited-since 1d → 更新变更日志
4. 检查线程待办到期
5. 合成 PULSE.md
6. 如有 Surge → 推送
```
