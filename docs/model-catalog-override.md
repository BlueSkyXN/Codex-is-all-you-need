# Codex 模型 Catalog Override 教程

本文说明如何用 `model_catalog_json` 自定义 Codex 的模型显示列表，并说明如何从默认缓存 `models_cache.json` 提取模型信息，快速生成可用的 override catalog。

这个方法适合解决一类常见问题：provider/API 已经能调用某个模型，但 Codex 的模型选择列表或 API 模式显示列表没有自动显示它。例如 `gpt-5.3-codex-spark` 能被 provider 返回，也能用于请求，但当前 Codex bundled/remote catalog 没把它列入显示 catalog。

适用场景：

- provider/API 已经支持某个模型，但 Codex 模型选择列表不显示它。
- 想把 `models_cache.json` 里的某个 `ModelInfo` 复用到自定义 catalog。
- 想基于已有模型模板，新增一个自定义模型 slug。

已验证环境：

- `codex-cli 0.133.0`
- 配置目录示例：`~/.codex`

本文里的 `~/.codex` 是用户级配置目录示例。实际路径可以通过 `echo "$CODEX_HOME"` 或 Codex 启动环境确认；没有单独设置时通常就是用户 home 下的 `.codex`。

## 术语和文件职责

本文涉及三个不同来源，不要混用：

- `codex debug models --bundled`：读取当前 Codex binary 自带的 bundled catalog。
- `codex debug models`：读取当前实际生效的模型 catalog，可能来自 bundled、remote、cache 或 `model_catalog_json` override。
- `~/.codex/models_cache.json`：remote model catalog 的本地缓存，带 `fetched_at`、`etag`、`client_version` 等缓存元信息。
- `~/.codex/model_catalog.override.json`：用户主动指定的 override catalog 文件，由 `config.toml` 的 `model_catalog_json` 指向。
- provider `/models`：后端/API 实际可调用模型列表，通常只说明模型 ID 是否存在，不等于 Codex UI 一定会显示。

核心判断顺序：

```text
provider/API supports model
  -> model can be called

Codex ModelInfo catalog includes model
  -> model appears in Codex picker/debug list
```

因此，一个模型能被 API 调用，不代表会自动进入 Codex 显示列表；显示列表需要对应的 `ModelInfo`。

## 核心结论

不要直接改：

```text
~/.codex/models_cache.json
```

它是 remote model catalog 的缓存，不是稳定配置入口。Codex 会根据 `client_version`、`fetched_at`、remote/bundled catalog 等逻辑判断它是否可用，缓存可能被判定为 stale，也可能被重新生成。

正确入口是：

```toml
model_catalog_json = "/absolute/path/to/.codex/model_catalog.override.json"
```

也就是在 `~/.codex/config.toml` 里显式指定一个本地模型 catalog override 文件。

建议在 `config.toml` 里写绝对路径。Shell 命令可以使用 `~/.codex`，但配置文件里的路径展开行为可能随版本变化，绝对路径最少歧义。

## 两个 JSON 的格式规范

### `models_cache.json`

`models_cache.json` 的顶层是缓存对象：

```json
{
  "fetched_at": "...",
  "etag": "...",
  "client_version": "0.131.0",
  "models": [
    {
      "slug": "gpt-5.5"
    }
  ]
}
```

字段含义：

- `fetched_at`：缓存获取时间。
- `etag`：remote catalog 的缓存标识。
- `client_version`：生成缓存的 Codex client 版本。
- `models`：真正的 `ModelInfo` 数组。

这个文件可以作为 `ModelInfo` 的数据来源，但不应该作为配置入口。Codex 可以因为版本不匹配、缓存过期或 remote 结果变化而忽略或覆盖它。

### `model_catalog.override.json`

`model_catalog_json` 指向的文件不能照搬这个结构。当前 Codex 0.133.0 实测可用结构是双层数组：

```json
[
  [
    {
      "slug": "gpt-5.5"
    },
    {
      "slug": "gpt-5.3-codex-spark"
    }
  ]
]
```

可以这样理解：

```text
models_cache.json
= cache metadata + models array

model_catalog.override.json
= catalog response wrapper + ModelInfo array
```

每个模型对象本身都是 `ModelInfo`，可以从 `.models[]` 里提取复用；但外层包装必须换成 `[[...]]`。

最小结构检查：

```bash
jq -e '
  type == "array"
  and length == 1
  and (.[0] | type == "array")
  and (.[0] | length > 0)
' ~/.codex/model_catalog.override.json
```

## 从源头寻找可用模型

### 1. 看当前 Codex 实际显示列表

```bash
codex debug models | jq -r '.models[].slug'
```

如果目标模型已经在这里，说明无需配置 `model_catalog_json`。如果这里没有，但 provider 能调用，就需要补 catalog。

### 2. 看当前 binary 自带列表

```bash
codex debug models --bundled | jq -r '.models[].slug'
```

如果 `--bundled` 里没有，说明当前安装版本的 bundled catalog 没带这个模型。

### 3. 看本地 remote cache

```bash
jq -r '.models[].slug' ~/.codex/models_cache.json
```

如果目标模型在 cache 里，可以直接复用对应 `ModelInfo`：

```bash
jq --arg slug "gpt-5.3-codex-spark" '
  .models[] | select(.slug == $slug)
' ~/.codex/models_cache.json
```

### 4. 看 provider/API 实际可用模型

OpenAI-compatible provider 通常有 `/models`。不要把 token 写进仓库；在本机 shell 里通过环境变量传入：

```bash
export CODEX_PROVIDER_BASE_URL="https://example.invalid/v1"
export CODEX_PROVIDER_TOKEN="replace-with-local-token"

curl -sS "$CODEX_PROVIDER_BASE_URL/models" \
  -H "Authorization: Bearer $CODEX_PROVIDER_TOKEN" \
  | jq -r '
      if has("data") then .data[]?.id
      elif has("models") then .models[]?.id // .models[]?.slug
      else empty
      end
    '
```

如果 provider `/models` 返回了目标模型，但 `codex debug models` 没返回，问题就是 Codex catalog 层，而不是 API 层。

### 5. 从日志确认请求实际使用了哪个模型

```bash
rg 'model=|api.path="responses"|api.path="chat/completions"' ~/.codex/log/codex-tui.log
```

日志只能证明请求层是否用过某个模型，不能证明它会显示在 picker 里。

### 6. 查配置入口是否被当前 binary 支持

```bash
strings "$(command -v codex)" | rg 'model_catalog_json|ModelInfo|ModelsCache'
```

这是诊断手段，不是日常配置步骤。能看到 `model_catalog_json` 只能说明当前 binary 有这个配置键，具体 JSON 形状仍要用 `codex debug models -c ...` 验证。

## 比对模型信息

### 比对两个文件的外层结构

```bash
jq '{
  top_type: type,
  keys: keys,
  models_type: (.models | type),
  models_len: (.models | length),
  client_version
}' ~/.codex/models_cache.json

jq '{
  top_type: type,
  top_len: length,
  first_type: (.[0] | type),
  first_len: (.[0] | length),
  first_slug: .[0][0].slug
}' ~/.codex/model_catalog.override.json
```

预期差异：

```text
models_cache.json
  top_type = object
  has keys = fetched_at, etag, client_version, models

model_catalog.override.json
  top_type = array
  top_len = 1
  first_type = array
```

### 比对两个来源里的同一个模型

把 cache 里的模型和当前 catalog 里的同名模型抽出来：

```bash
slug="gpt-5.3-codex-spark"

jq --arg slug "$slug" '
  .models[] | select(.slug == $slug)
' ~/.codex/models_cache.json > /tmp/model-from-cache.json

codex debug models \
  | jq --arg slug "$slug" '
      .models[] | select(.slug == $slug)
    ' > /tmp/model-from-codex.json
```

排序后 diff：

```bash
diff -u \
  <(jq -S . /tmp/model-from-cache.json) \
  <(jq -S . /tmp/model-from-codex.json)
```

如果当前 catalog 还没有这个模型，`/tmp/model-from-codex.json` 会是空文件；这正是需要 override 的信号。

### 比对字段集合

查看某个 `ModelInfo` 有哪些字段：

```bash
jq -r '
  paths(scalars)
  | map(tostring)
  | join(".")
' /tmp/model-from-cache.json | sort
```

常见关键字段：

- `slug`
- `display_name`
- `description`
- `default_reasoning_level`
- `supported_reasoning_levels`
- `base_instructions`
- `model_messages.instructions_template`
- `model_messages.instructions_variables`
- `context_window`
- `max_context_window`
- `auto_compact_token_limit`
- `supported_in_api`
- `supports_reasoning_summaries`
- `default_reasoning_summary`
- `support_verbosity`
- `default_verbosity`
- `apply_patch_tool_type`
- `web_search_tool_type`
- `supports_parallel_tool_calls`
- `supports_search_tool`
- `input_modalities`

## 识别用户自定义与官方基线

自定义 catalog 时，最容易出错的不是 JSON 结构，而是把“用户为了本机可用而改的字段”和“应该跟官方/基线模型保持一致的字段”混在一起。

推荐规则：

```text
User intent fields
  可以按本机 provider、显示需求和上下文窗口修改。

Baseline-locked fields
  默认从官方 catalog、当前 bundled catalog 或 cache 里的相近模型复制，不手写。
```

这里的“官方/基线”不是 provider `/models` 的简单 ID 列表，而是 Codex 的 `ModelInfo` 来源。优先级通常是：

```text
same slug in current `codex debug models`
  -> same slug in `models_cache.json`
  -> closest model in current `codex debug models`
  -> closest model in `models_cache.json`
```

### 通常属于用户自定义的字段

这些字段表达本机意图，可以按实际需要修改：

- `slug`：新增模型或 alias 的模型 ID，必须能被 provider/API 调用。
- `display_name`：picker 显示名称。
- `description`：显示说明。
- `priority`：显示排序。
- `visibility`：是否进入显示列表，通常保留 `list`。
- `context_window`：模型真实上下文窗口。
- `max_context_window`：模型最大上下文窗口。
- `auto_compact_token_limit`：自动压缩阈值，必须低于上下文窗口。
- `default_reasoning_level`：默认 reasoning effort，必须是 provider 实际支持的值。
- `default_verbosity`：默认 verbosity，必须和模型能力匹配。

这些配置项也属于用户自定义，但它们在 `config.toml` 里，不在 `ModelInfo` 里：

- `model`：默认启用哪个模型。
- `model_provider`：默认走哪个 provider。
- `model_context_window`：当前默认模型的上下文窗口。
- `model_auto_compact_token_limit`：当前默认模型的自动压缩阈值。
- `[model_providers.<id>]`：provider 的 `base_url`、`wire_api`、auth 方式等。

### 通常应跟官方/基线保持一致的字段

这些字段控制 Codex 如何构造提示词、工具能力、reasoning/service tier 语义。除非你确认 provider 和 Codex 当前版本都支持对应差异，否则不要手写：

- `base_instructions`
- `model_messages`
- `supported_reasoning_levels`
- `supports_reasoning_summaries`
- `default_reasoning_summary`
- `support_verbosity`
- `apply_patch_tool_type`
- `web_search_tool_type`
- `truncation_policy`
- `supports_parallel_tool_calls`
- `supports_image_detail_original`
- `experimental_supported_tools`
- `input_modalities`
- `supports_search_tool`
- `shell_type`
- `service_tiers`
- `default_service_tier`

`service_tiers` 尤其不要随便编。`default_service_tier` 如果存在，必须对应 `service_tiers[].id` 里的可选值。provider 不支持服务层选择时，保留基线模型里的空列表或官方值，不要为了显示“fast/priority”之类的标签自行添加。

`availability_nux` 和 `upgrade` 通常也不该为自定义模型编写。它们是 Codex 用来展示新模型提示、升级提示的元信息；自定义模型一般保留基线值或设为 `null`。

### 提取基线模型和自定义模型

如果目标模型在 cache 里，直接用同名模型作为基线：

```bash
slug="gpt-5.3-codex-spark"

jq --arg slug "$slug" '
  .models[] | select(.slug == $slug)
' ~/.codex/models_cache.json > /tmp/model-baseline.json

jq --arg slug "$slug" '
  .[0][] | select(.slug == $slug)
' ~/.codex/model_catalog.override.json > /tmp/model-custom.json
```

如果是新增模型，选择最接近的已知模型作为基线：

```bash
source_slug="gpt-5.3-codex"
custom_slug="my-custom-model"

codex debug models \
  | jq --arg slug "$source_slug" '
      .models[] | select(.slug == $slug)
    ' > /tmp/model-baseline.json

jq --arg slug "$custom_slug" '
  .[0][] | select(.slug == $slug)
' ~/.codex/model_catalog.override.json > /tmp/model-custom.json
```

### 先看完整差异

```bash
diff -u \
  <(jq -S . /tmp/model-baseline.json) \
  <(jq -S . /tmp/model-custom.json)
```

这个 diff 会很大，尤其是 `base_instructions` 和 `model_messages`。它的用途是发现意外差异，不适合直接作为“应该修改什么”的清单。

### 单独审计用户自定义字段

```bash
jq -S '{
  slug,
  display_name,
  description,
  priority,
  visibility,
  context_window,
  max_context_window,
  auto_compact_token_limit,
  default_reasoning_level,
  default_verbosity
}' /tmp/model-baseline.json > /tmp/model-baseline-user-fields.json

jq -S '{
  slug,
  display_name,
  description,
  priority,
  visibility,
  context_window,
  max_context_window,
  auto_compact_token_limit,
  default_reasoning_level,
  default_verbosity
}' /tmp/model-custom.json > /tmp/model-custom-user-fields.json

diff -u /tmp/model-baseline-user-fields.json /tmp/model-custom-user-fields.json
```

这里出现差异是正常的，但每个差异都应该能解释为用户意图。例如“启用 Spark 模型”“把上下文窗口改成 128000”“把显示名改成本地 provider 名称”。

### 单独审计应继承字段

```bash
jq -S '{
  base_instructions,
  model_messages,
  supported_reasoning_levels,
  supports_reasoning_summaries,
  default_reasoning_summary,
  support_verbosity,
  apply_patch_tool_type,
  web_search_tool_type,
  truncation_policy,
  supports_parallel_tool_calls,
  supports_image_detail_original,
  experimental_supported_tools,
  input_modalities,
  supports_search_tool,
  shell_type,
  service_tiers,
  default_service_tier
}' /tmp/model-baseline.json > /tmp/model-baseline-locked-fields.json

jq -S '{
  base_instructions,
  model_messages,
  supported_reasoning_levels,
  supports_reasoning_summaries,
  default_reasoning_summary,
  support_verbosity,
  apply_patch_tool_type,
  web_search_tool_type,
  truncation_policy,
  supports_parallel_tool_calls,
  supports_image_detail_original,
  experimental_supported_tools,
  input_modalities,
  supports_search_tool,
  shell_type,
  service_tiers,
  default_service_tier
}' /tmp/model-custom.json > /tmp/model-custom-locked-fields.json

diff -u /tmp/model-baseline-locked-fields.json /tmp/model-custom-locked-fields.json
```

如果这组 diff 有差异，要非常谨慎。合理差异常见于“从一个不同能力的模型复制模板”，但不应该是手写、猜测或为了让 UI 好看而改出来的。

### 给自定义差异留审计记录

JSON 不支持注释，不要把说明写进 `model_catalog.override.json`。建议在旁边维护一个 Markdown 记录，例如：

```text
~/.codex/model_catalog.override.notes.md
```

记录每个自定义模型的来源和改动：

```markdown
## my-custom-model

baseline: gpt-5.3-codex from `codex debug models`

intentional changes:
- slug -> my-custom-model
- display_name -> My Custom Model
- context_window -> 128000
- auto_compact_token_limit -> 120000

kept from baseline:
- base_instructions
- model_messages
- service_tiers
- tool capability fields
```

## 快速生成：完全使用 cache 里的模型

如果你想让 override catalog 完全等于 cache 里的模型列表，可以运行：

```bash
jq '[[.models[]]]' \
  ~/.codex/models_cache.json \
  > ~/.codex/model_catalog.override.json
```

这会丢掉 cache metadata，只保留 `ModelInfo` 列表，并改成 `model_catalog_json` 需要的外层格式。

风险：

- 如果 cache 里有旧模型、测试模型或不想显示的模型，它们都会进入列表。
- 如果 cache 是旧版本生成的，里面的字段可能和当前 Codex 版本不完全匹配。

## 推荐生成：当前 catalog 加 cache 里的指定模型

更稳妥的方法是先用当前 Codex 可显示模型作为基线，再从 cache 里追加指定模型。

以追加 `gpt-5.3-codex-spark` 为例：

```bash
codex debug models > /tmp/codex-models-current.json

jq -n \
  --slurpfile base /tmp/codex-models-current.json \
  --slurpfile cache ~/.codex/models_cache.json \
  --arg slug "gpt-5.3-codex-spark" '
    ($base[0].models) as $base_models |
    ($cache[0].models[] | select(.slug == $slug)) as $extra |
    [
      (
        $base_models
        + (
          if any($base_models[]; .slug == $slug)
          then []
          else [$extra]
          end
        )
      )
    ]
  ' > ~/.codex/model_catalog.override.json
```

生成后可以检查列表：

```bash
jq -r '.[0][].slug' ~/.codex/model_catalog.override.json
```

这个方法的优点：

- 保留当前 Codex 版本默认显示的模型。
- 只从 cache 里补一个指定模型。
- 不需要手写复杂的 `base_instructions`、`model_messages`、tool 能力字段和 context 参数。

## 自定义一个不存在于 cache 的模型

如果模型不在 `models_cache.json` 里，可以找一个最接近的模型作为模板，然后修改必要字段。

示例：基于 `gpt-5.3-codex` 复制一个自定义模型：

```bash
codex debug models > /tmp/codex-models-current.json

jq -n \
  --slurpfile base /tmp/codex-models-current.json \
  --arg source_slug "gpt-5.3-codex" \
  --arg new_slug "my-custom-model" \
  --arg display_name "My Custom Model" '
    ($base[0].models) as $base_models |
    (
      $base_models[]
      | select(.slug == $source_slug)
      | .slug = $new_slug
      | .display_name = $display_name
      | .description = "Custom model exposed by the configured provider."
      | .priority = 50
    ) as $custom |
    [
      (
        $base_models
        + (
          if any($base_models[]; .slug == $new_slug)
          then []
          else [$custom]
          end
        )
      )
    ]
  ' > ~/.codex/model_catalog.override.json
```

需要按实际模型调整的字段：

- `slug`：必须匹配 provider/API 实际可调用的模型 ID，除非 provider 自己做了 alias 映射。
- `display_name`：模型选择列表里的显示名称。
- `description`：模型描述。
- `default_reasoning_level`：默认 reasoning effort，例如 `low`、`medium`、`high`、`xhigh`。
- `supported_reasoning_levels`：允许的 reasoning effort 列表。
- `context_window`：模型上下文窗口。
- `max_context_window`：最大上下文窗口。
- `auto_compact_token_limit`：自动压缩阈值，必须低于上下文窗口。
- `base_instructions`：默认系统提示词主体。
- `model_messages`：模型相关提示词模板和变量。
- `supports_reasoning_summaries`：是否支持 reasoning summary。
- `default_reasoning_summary`：默认 reasoning summary 设置。
- `support_verbosity` / `default_verbosity`：是否支持 verbosity 以及默认值。
- `apply_patch_tool_type`、`web_search_tool_type`、`supports_parallel_tool_calls`、`supports_search_tool`：工具能力声明。
- `input_modalities`：输入模态，例如 `["text"]` 或 `["text", "image"]`。

通常不建议手写 `base_instructions` 和 `model_messages`。更稳妥的做法是从一个行为接近的已知模型复制，然后只改模型 ID、展示名、描述、context 参数和 priority。

## 模型参数怎么配

### `slug`

`slug` 是 Codex 向 provider 发送请求时使用的模型 ID。它必须满足至少一个条件：

- provider/API 原生支持这个 ID。
- provider/API 有 alias，把这个 ID 映射到真实模型。

仅仅把 `slug` 写进 catalog，不会让后端凭空支持这个模型。

### `display_name`、`description`、`priority`

这些字段主要影响显示：

- `display_name`：picker 里的名字。
- `description`：模型说明。
- `priority`：排序优先级，数值越小通常越靠前。

### reasoning 配置

相关字段：

- `default_reasoning_level`
- `supported_reasoning_levels`
- `supports_reasoning_summaries`
- `default_reasoning_summary`

如果 provider 不支持某些 reasoning effort，不要为了显示完整而照抄高阶模型。最稳妥做法是从行为最接近的已知模型复制。

### context 配置

相关字段：

- `context_window`
- `max_context_window`
- `auto_compact_token_limit`
- `effective_context_window_percent`

原则：

- `model_context_window` 不要超过模型真实上下文窗口。
- `model_auto_compact_token_limit` 要低于上下文窗口。
- 如果默认模型切到更小窗口的模型，要同步改 `config.toml` 的 `model_context_window` 和 `model_auto_compact_token_limit`。

示例：

```toml
model = "gpt-5.3-codex-spark"
model_context_window = 128000
model_auto_compact_token_limit = 120000
```

### 提示词和工具能力

相关字段：

- `base_instructions`
- `model_messages`
- `apply_patch_tool_type`
- `web_search_tool_type`
- `supports_parallel_tool_calls`
- `supports_image_detail_original`
- `experimental_supported_tools`
- `input_modalities`
- `supports_search_tool`

这些字段会影响 Codex 如何构造系统提示词、暴露工具能力和描述模型行为。除非你明确知道差异，否则不要从零手写；优先从 cache 或当前 catalog 中复制相近模型。

## 启用 override catalog

编辑 `~/.codex/config.toml`，加入或更新：

```toml
model_catalog_json = "/absolute/path/to/.codex/model_catalog.override.json"
```

建议放在顶部模型配置附近，例如：

```toml
model_provider = "my-provider"
model = "gpt-5.5"
model_catalog_json = "/absolute/path/to/.codex/model_catalog.override.json"
```

如果要把新增模型设为默认模型，再改：

```toml
model = "gpt-5.3-codex-spark"
```

如果新增模型上下文窗口小于原默认模型，还要同步调整：

```toml
model_context_window = 128000
model_auto_compact_token_limit = 120000
```

不要让 `model_auto_compact_token_limit` 高于或接近模型真实上下文窗口。

如果只想让模型出现在列表里，不想改变当前默认模型，只需要加 `model_catalog_json`，不要改 `model`。

完整示例：

```toml
model_provider = "my-provider"
model = "gpt-5.5"
model_catalog_json = "/absolute/path/to/.codex/model_catalog.override.json"
model_reasoning_effort = "xhigh"
model_context_window = 272000
model_auto_compact_token_limit = 256000

[model_providers.my-provider]
name = "My Provider"
base_url = "https://example.invalid/v1"
wire_api = "responses"
env_key = "MY_PROVIDER_API_KEY"
```

说明：

- `model_provider` 指向下面的 `[model_providers.<id>]`。
- `base_url` 是 provider endpoint。
- `wire_api` 要和 provider 支持的协议一致，例如 `responses` 或 `chat`。
- `env_key` 表示 token 从环境变量读取，适合公开文档。
- 私有 token 不要写进公开仓库、README、截图或日志。

## 验证

先验证 JSON 外层结构：

```bash
jq -e '
  type == "array"
  and length == 1
  and (.[0] | type == "array")
  and (.[0] | length > 0)
' ~/.codex/model_catalog.override.json
```

再验证 Codex 能读取 override：

```bash
catalog_path="$HOME/.codex/model_catalog.override.json"

codex debug models \
  -c "model_catalog_json=\"$catalog_path\"" \
  | jq -r '.models[].slug'
```

启用到 `config.toml` 后，验证默认读取：

```bash
codex debug models | jq -r '.models[].slug'
```

如果输出里能看到目标模型，例如：

```text
gpt-5.3-codex-spark
```

说明模型已经进入 Codex 的显示 catalog。

## 常见错误

错误写法一：把 cache 原样当 override。

```json
{
  "fetched_at": "...",
  "models": []
}
```

这会失败，因为 `model_catalog_json` 当前要求的不是 cache 对象。

错误写法二：只写一层模型数组。

```json
[
  {
    "slug": "gpt-5.3-codex-spark"
  }
]
```

这会失败，因为 Codex 当前解析期望的是外层 sequence 包装。

错误写法三：每个模型各包一层数组。

```json
[
  [
    {
      "slug": "gpt-5.5"
    }
  ],
  [
    {
      "slug": "gpt-5.3-codex-spark"
    }
  ]
]
```

这也会失败。实测会出现类似 `trailing characters` 的解析错误。

正确写法是：

```json
[
  [
    {
      "slug": "gpt-5.5"
    },
    {
      "slug": "gpt-5.3-codex-spark"
    }
  ]
]
```

## 注意事项

- `model_catalog_json` 是当前 Codex 可用但不算公开稳定的配置入口，未来升级后格式可能变化。
- 显示在模型列表里不代表 API 一定能调用成功；provider 必须实际支持该 `slug`。
- 如果 provider `/models` 已经返回某模型，但 Codex 不显示，通常就是 catalog 层没有对应 `ModelInfo`。
- 如果升级 Codex 后模型又消失，先重新运行 `codex debug models` 和上面的 override 验证命令。
- 如果默认模型切到自定义模型，要同步检查 context window、auto compact limit、reasoning effort 和 tool 能力声明。
