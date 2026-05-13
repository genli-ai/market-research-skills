# Changelog

> 中文版本见本文件下半部分 / Chinese version below

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.3.1] - 2026-05-13

### Fixed

- `topic-brief`: cover author byline (e.g. "developed by Gen") was offset ~2px to the right of the brand name / issue title above it. Root cause: the nested `<table>` wrapping the author/period row in `templates/briefing.html` relied on the legacy HTML `cellspacing="0"` attribute, which modern browsers no longer fully honor. Fixed by adding CSS `border-collapse:collapse; border-spacing:0;` to the table and explicit `padding:0;` on its two `<td>` cells. Author byline now aligns flush-left with brand name and headline.

## [0.3.0] - 2026-05-13

### Added

- New skill: `topic-brief` — thematic observation briefing generator. Given a subject (region / industry / policy issue / institution) and a time window, produces a single self-contained HTML file with blue "TOPIC BRIEF" branding, pasteable directly into the WeChat Official Account editor. Follows a 5-step workflow with one mandatory user direction-confirmation gate after material gathering.
- `topic-brief` core capabilities:
  - 4-question parameter collection (subject / period / source preference / author byline) with smart defaults
  - Parallel material gathering (≥4 web searches + 1–2 deep fetches of the focus report)
  - Three-state author rendering (default "developed by Gen" / explicit blank / custom byline)
  - Self-contained Python rendering pipeline (Jinja2 template + Chinese-quote auto-repair); only external dep is `jinja2`
  - 4 historical few-shot samples (3 regional + 1 red-brand) under `reference/` to anchor tone and structure
  - Self-check checklist after composition (issue_title ≤24 chars, 4 sub-sections × 3–4 items, every number traceable, every URL complete, etc.)
- Dual-language source files for `topic-brief`:
  - `SKILL.md` (English, canonical, loaded by LLMs)
  - `SKILL.zh.md` (Chinese reference, kept in sync; excluded from `.zip` packaging)
- `topic-brief` scope exclusions (politics / military / religion / celebrity gossip / inherently controversial topics) — replies `Out of scope. (超出能力范围)` and stops, mirroring `verifying`.
- `topic-brief` tool-call mapping section — uses generic verbs (Search-engine query / Fetch web body / User-facing question prompt) so non-Claude terminals can adapt.

### Changed

- `scripts/pack.sh` now also excludes `<skill-name>/output/` (generated artifacts) from the packaged `.zip`, in addition to the existing `downloads/` and `SKILL.zh.md` exclusions.
- Top-level README + CHANGELOG: added `topic-brief` row to the skills table.

## [0.2.0] - 2026-05-12

### Changed

- `verifying`: replaced the "three-layer search depth" rule with a "give-up criterion" — trace until either a whitelisted source is found or obvious paths are exhausted; no fixed depth budget. Transcript review showed the layer-count scaffolding was never actually used by the model in real verification work.
- `verifying`: compressed English `SKILL.md` frontmatter `description` from ~1.4K to under 1024 characters so the skill can be installed on Claude AI Chat. Chinese description in `SKILL.zh.md` trimmed in parallel.
- `verifying`: removed the `Search layer hit` line from the `[Verified]` output template and the `layer-by-layer` wording from the `[Cannot Verify]` template.
- `verifying`: rewrote all output templates to be concise (3-5 lines for the common case) and switched to emoji labels (`✅ ⚠ ❌ 🔎 ⚖ 🔒`). The mandatory 12-field block is gone.
- `verifying`: changed metadata handling from "must list all six fields" to "surface only when divergent." A `⚠` line is printed when any of the six dimensions (time point, definition, unit, coverage, revision status, data type) differs from the user's claim or is non-obvious; silent omission of a divergence remains a red line (equivalent to silent definition swap).
- `verifying`: removed the `Identified as: <scenario>` line from outputs — internal classification is still used to pick the right sub-flow, but the label adds no value to the reader.

## [0.1.0] - 2026-05-12

### Added

- Monorepo skeleton (`skills/` + `scripts/` + `.claude-plugin/` + `releases/`).
- New skill: `verifying` — information verification, covering five scenarios:
  - Basic truthfulness check
  - Completeness — avoid out-of-context quoting
  - One-level reasoning verification (Z = P × Q decomposition)
  - Negative statements (unfalsifiable / find counter-example)
  - Multi-source conflicts (side-by-side + difference attribution)
- Core rules for `verifying`:
  - Scope exclusions: politics / military / religion / entertainment celebrity gossip / other inherently controversial topics are refused upfront — the skill replies "Out of scope" and stops
  - Whitelisted primary sources (official institutions + authoritative industry + aggregator databases Statista / Wind / CEIC / SWFI / Refinitiv)
  - Three-layer search depth + download originals locally and read in full
  - Chart "meaning" verification (axes / units / start year / log vs linear)
  - Six mandatory metadata fields (time point / definition / unit / coverage / revision status / data type)
  - When download is blocked, hand the link to the user and request assistance
  - Cross-LLM adaptation — tool-call actions describe semantics only; no terminal-specific tool names hard-coded
  - Response language matches the user's question language
- Dual-language source files for `verifying`:
  - `SKILL.md` (English, canonical, loaded by LLMs)
  - `SKILL.zh.md` (Chinese reference, kept in sync; excluded from `.zip` packaging)
- Plugin manifest (`.claude-plugin/plugin.json`) + self-registering marketplace (`.claude-plugin/marketplace.json`) so Claude Code users can install with `/plugin install`.
- `scripts/pack.sh` — one-command packaging of a single skill into a portable `.zip` file, output to `releases/<skill-name>.zip`. The Chinese reference `SKILL.zh.md` is excluded from the packaged zip.

---

# 版本变更（中文版）

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [未发布]

## [0.3.1] - 2026-05-13

### 修复

- `topic-brief`：封面作者署名（如 "developed by Gen"）相对上方品牌名 / 主标题向右偏移约 2px。根因是 `templates/briefing.html` 中包裹作者/期号行的嵌套 `<table>` 只依赖了 HTML 旧属性 `cellspacing="0"`，现代浏览器已不再完全遵守该属性。修复办法是在该表上加 CSS `border-collapse:collapse; border-spacing:0;`、并在两个 `<td>` 上显式 `padding:0;`。作者署名现在与上方品牌名、标题严格左对齐

## [0.3.0] - 2026-05-13

### 新增

- 新 skill：`topic-brief` —— 主题观察简报生成器。输入一个主题（区域 / 行业 / 议题 / 机构）+ 时间窗口，产出一份蓝色品牌的 self-contained HTML 文件，可直接粘进微信公众号编辑器。走 5 步工作流，中途**强制 1 次方向确认**避免错方向写 5000 字。
- `topic-brief` 核心能力：
  - 4 问参数收集（主题 / 时间 / 信息源偏好 / 作者署名），带智能默认
  - 并行素材采集（≥4 次搜索 + 1-2 次焦点报告深读）
  - 作者署名三态渲染（默认 "developed by Gen" / 显式留白 / 自定义文本）
  - self-contained Python 渲染管道（Jinja2 模板 + 中文引号自动修复）；唯一外部依赖 `jinja2`
  - `reference/` 下 4 份历史样本（3 份区域 + 1 份红色品牌示例）锚定语气与结构
  - 撰写后自检 checklist（issue_title ≤24 字 / 4 个子板块 × 3-4 条 / 数字可溯源 / URL 完整 等）
- `topic-brief` 双语源文件：
  - `SKILL.md`（英文权威版，被 LLM 加载）
  - `SKILL.zh.md`（中文参考版，与英文同步；打包时排除）
- `topic-brief` 范围排除（政治 / 军事 / 宗教 / 八卦 / 天然争议议题）—— 回 `Out of scope. (超出能力范围)` 一行就停，与 `verifying` 风格一致
- `topic-brief` 工具调用映射 section —— 用通用语义动词（搜索引擎检索 / 抓取网页正文 / 用户提问入口），方便非 Claude 终端适配

### 变更

- `scripts/pack.sh` 现在也排除 `<skill-name>/output/`（生成产物）不打进 zip；原有的 `downloads/` 与 `SKILL.zh.md` 排除规则保留
- 顶层 README 与 CHANGELOG：skills 表格新增 `topic-brief` 行

## [0.2.0] - 2026-05-12

### 变更

- `verifying`：把「三层搜索深度」规则替换为「放弃判定标准」——持续溯源直到找到白名单内一手来源、或主流路径试完仍未命中；不设固定的层数预算。复盘历史调用记录发现，"层数计数"的脚手架在真实核实工作里从未被模型实际采用
- `verifying`：把英文 `SKILL.md` 的 frontmatter `description` 从约 1.4K 压缩到 1024 字符以内，让 Claude AI Chat 可以加载该 skill。中文版 `SKILL.zh.md` 的 description 同步精简
- `verifying`：从 `[已核实]` 输出模板里删除「搜索层数」一行，从 `[无法核实]` 模板里删除「逐层列出三层」的措辞
- `verifying`：所有输出模板改写为精简形式（常见场景 3-5 行），标签改用 emoji（`✅ ⚠ ❌ 🔎 ⚖ 🔒`）。原本固定的 12 字段块取消
- `verifying`：元数据处理从「必填六项」改为「差异时才暴露」。六个维度（时点 / 口径 / 单位 / 范围 / 修订状态 / 数据类型）任一与用户陈述 diverge 时单写一行 `⚠`；diverge 而不写仍是红线（等同于隐式口径偷换）
- `verifying`：去掉输出里的「识别为 X 类」一行——内部仍做场景分类来选子流程，但标签对读者无价值

## [0.1.0] - 2026-05-12

### 新增

- monorepo 骨架（`skills/` + `scripts/` + `.claude-plugin/` + `releases/`）
- 新 skill：`verifying`——信息核实，覆盖五类场景：
  - 基础真伪核实
  - 完整性补充（避免断章取义）
  - 一层推理核实（Z = P × Q 拆解对账）
  - 否定性陈述（不可证伪 / 找反例）
  - 多源冲突（并列输出 + 差异归因）
- `verifying` 核心规则：
  - 范围排除：政治 / 军事 / 宗教 / 娱乐明星八卦 / 其他争议议题入口拒绝——skill 直接回复「超出能力范围」并停止
  - 白名单一手来源（官方机构 + 权威行业源 + 聚合数据库 Statista / Wind / CEIC / SWFI / Refinitiv）
  - 三层搜索深度 + 下载原文通读
  - 图表「图意」核实（坐标轴 / 单位 / 起始年份 / 是否对数）
  - 元数据强制六项（时点 / 口径 / 单位 / 范围 / 修订状态 / 数据类型）
  - 下载受阻时把链接交给用户、请其协助
  - 跨 LLM 适配：工具调用动作只描述语义，不写死特定终端工具名
  - 回复语言与用户提问语言一致
- `verifying` 双语源文件：
  - `SKILL.md`（英文权威版，被 LLM 加载）
  - `SKILL.zh.md`（中文参考版，与英文版同步；打包成 `.zip` 时被排除）
- Plugin 清单（`.claude-plugin/plugin.json`）+ 自我注册 marketplace（`.claude-plugin/marketplace.json`），支持 Claude Code 的 `/plugin install` 一键安装
- `scripts/pack.sh`——一键打包单个 skill 为通用 `.zip` 文件，产物在 `releases/<skill-name>.zip`。中文参考版 `SKILL.zh.md` 不会被打进 zip
