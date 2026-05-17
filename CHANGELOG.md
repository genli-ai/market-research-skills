# Changelog

> 中文版本见本文件下半部分 / Chinese version below

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.5.0] - 2026-05-17

### Added

- New skill: `light-research` — lightweight research workflow that produces a 5-page decision memo / executive brief (PDF + Word) in 60–80 min, single LLM session, zero hard stops, BLUF consulting-style summary, plain text with inline footnote citations and no charts.
- `light-research` core capabilities:
  - 6-step skeleton (hypothesis / search / plan / draft / self-check / freeze), all soft stops — the user can interrupt at any time but the workflow does not pause for confirmation
  - 1-question onboarding (hypothesis only), every other parameter locked to defaults (5-page PDF + Word, no HTML / WeChat / slides, no charts, expert audience, single LLM, BLUF summary, 60–80 min budget)
  - 6 source categories drawn from heavy-research (drops the academic-only tier); 20–30 source ledger + 5–8 core PDFs downloaded in full; time-lock numbers pulled live at draft time via `financial-data-sources` skill or iFinD MCP
  - BLUF (Bottom Line Up Front) Executive Summary discipline — single paragraph 80–150 chars, conclusion + key numbers + so-what
  - 12-item grep self-check (subset of heavy's §7.4) — dashes, manual heading numbers, emoji, h3+ headings, bold-in-body, colon/period ratio, filler words, h2 academic anti-patterns, hyphen-as-dash, technical-symbol connectives, academic/colloquial register, vague quantifiers, meta-language, page count, Quarto render
  - Self-check failure rollback: any red line trip → back to step 4 → re-render → re-grep; loop until all pass (no hard-stop user gate, so self-check is the only gate)
  - Pure-Markdown footnote citations (`^[org, title, YYYY-MM-DD. URL.]`), no `references.bib`
  - Page-count handling: 4–6 OK, 7–9 strong warning + trim suggestion, 10+ asks user to choose between further trim or switching to `heavy-research`
- `light-research` bilingual source files:
  - `SKILL.md` (English, canonical, loaded by LLMs)
  - `SKILL.zh.md` (Chinese reference, kept in sync; excluded from `.zip` packaging)
- `light-research` references:
  - `references/workflow.md` — full 6-step workflow + writing discipline + grep red-line table (Chinese; this is the skill's working language)
  - `references/_quarto-light.yml` — Quarto template optimized for 5-page memo (toc: false / number-sections: false / 11pt body / 13pt h1 / Songti SC CJK / footnote 10pt)
- `light-research` cross-LLM tool-call mapping section (Read full text / Fetch web body / Search-engine query / Database query) so non-Claude terminals can adapt.

### Changed

- Top-level README + plugin manifests (`plugin.json` / `marketplace.json`): added `light-research` row / description.

## [0.4.1] - 2026-05-13

### Fixed

- Release packaging: GitHub Release v0.4.0 only attached `topic-brief.zip`, making `verifying` appear missing in the version page. v0.4.1 re-attaches both skill zips. Going forward, every GitHub Release must include the full skill set via `gh release create vX.Y.Z releases/*.zip` (documented in CLAUDE.md).

## [0.4.0] - 2026-05-13

### Changed

- `topic-brief`: tightened time-window discipline across the 5-step workflow. Triggered by user feedback that "past-month" briefings sometimes pulled in items from six months ago (see [FEEDBACK.md](FEEDBACK.md)). Four changes work together:
  - **Step 1** — the time-window answer is now immediately normalized to two ISO dates `[period_start, period_end]`, not kept as a fuzzy phrase
  - **Step 2** — every search query must inject a time filter (`after:YYYY-MM-DD before:YYYY-MM-DD` or equivalent). New explicit policy: focus body may reference earlier background context with an explicit time tag; sub-section items must be strictly in-window
  - **Step 3** — direction-confirmation output now lists each candidate item with its event date, so both the user and the model can spot-check freshness before composition starts
  - **Step 4** — every sub-section `item` now requires an `event_date` field (YYYY-MM-DD; YYYY-MM acceptable for month-only events), and the self-check checklist verifies all dates fall in-window

### Added

- `FEEDBACK.md` at repo root — log of user feedback, each entry kept to three parts (feedback / analysis / resolution).

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

## [0.5.0] - 2026-05-17

### 新增

- 新 skill：`light-research` —— 轻量研究工作流，60–80 min 内单 session 产出 5 页决策备忘 / executive brief（PDF + Word）。单 LLM、0 硬停、BLUF consulting-style 摘要、纯文字 + 内联 footnote 引用，无图表。
- `light-research` 核心能力：
  - 6 步骨架（hypothesis / search / plan / draft / self-check / freeze），全部软停 —— 用户随时可叫停，但工作流不暂停等确认
  - 1 问 onboarding（只问 hypothesis），其余全部锁默认（5 页 PDF + Word、不出 HTML / 公众号 / slide、无图、专家受众、单 LLM、BLUF 摘要、60–80 min 预算）
  - 6 类来源（沿用 heavy 的分类、删「学术」一类）；20–30 条资料台账 + 5–8 份核心 PDF 全文下载；time-lock 快照数字在 draft 引用前用 `financial-data-sources` skill 或 iFinD MCP 实拉
  - BLUF (Bottom Line Up Front) Executive Summary 纪律 —— 单段 80–150 字，结论 + 关键数字 + so-what
  - 12 条 grep 自检（heavy §7.4 的子集）—— 破折号、手写编号前缀、emoji、h3+ 标题、正文加粗、冒号 / 句号比例、抒情铺垫词、h2 学术造作模式、半角连字符当破折号、技术符号代连词、学术 / 口语腔、模糊量化词、meta-language、页数、Quarto 渲染
  - self-check 失败回退路径：任一红线超标 → 回 step 4 → 重渲 → 重 grep；直到全过才进 step 6（0 硬停 ≠ 0 自检门）
  - 纯 Markdown footnote 引用（`^[机构, 标题, YYYY-MM-DD. URL.]`），不用 `references.bib`
  - 超页处置：4–6 页 OK，7–9 页强警告 + 建议精简，10+ 由用户裁定继续精简还是转 `heavy-research`
- `light-research` 双语源文件：
  - `SKILL.md`（英文权威版，被 LLM 加载）
  - `SKILL.zh.md`（中文参考版，与英文同步；打包时排除）
- `light-research` references：
  - `references/workflow.md` —— 完整 6 步工作流 + 写作纪律 + grep 红线表（中文版，本 skill 实际工作语言）
  - `references/_quarto-light.yml` —— 为 5 页 memo 优化的 Quarto 模板（toc: false / number-sections: false / 正文 11pt / h1 13pt / 中文 Songti SC / 脚注 10pt）
- `light-research` 工具调用映射 section（通读全文 / 抓取网页正文 / 搜索引擎检索 / 数据库查询），方便非 Claude 终端适配

### 变更

- 顶层 README + plugin 清单（`plugin.json` / `marketplace.json`）：新增 `light-research` 行 / 描述

## [0.4.1] - 2026-05-13

### 修复

- 发版打包：v0.4.0 的 GitHub Release 只挂了 `topic-brief.zip`，让 `verifying` 看起来在新版"消失"。v0.4.1 补回两个 skill 的 zip。今后每次 GitHub Release 必须挂全部 skill 的 zip——固定流程 `gh release create vX.Y.Z releases/*.zip`（已沉淀到 CLAUDE.md）。

## [0.4.0] - 2026-05-13

### 变更

- `topic-brief`：收紧 5 步工作流的时间窗口纪律。由用户反馈触发——"过去一个月"的简报里偶尔混进半年前的条目（详见 [FEEDBACK.md](FEEDBACK.md)）。四处改动协同：
  - **步骤 1** —— 时间窗口回答后立即归一化为 `[period_start, period_end]` 两个 ISO 日期，不再以自然语言悬置
  - **步骤 2** —— 每次搜索必须注入时间过滤词（`after:YYYY-MM-DD before:YYYY-MM-DD` 或等价语法）。明确策略：焦点正文可引用窗口外背景（须显式标注时点），4 个子板块的 items 必须严格 in-window
  - **步骤 3** —— 方向确认时展示每条候选条目的事件日期，让用户和模型都能在动笔前 spot-check 时效
  - **步骤 4** —— 每条子板块 item 必填 `event_date`（YYYY-MM-DD，月级事件可用 YYYY-MM），自检 checklist 增加"每个 event_date 落在窗口内"

### 新增

- repo 根目录新增 `FEEDBACK.md` —— 用户反馈日志，每条三段（反馈 / 分析 / 方案），保持简洁。

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
