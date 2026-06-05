# Changelog

> 中文版本见本文件下半部分 / Chinese version below

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.4.0] - 2026-06-05

### Changed

- `local-vault`: **`.html`/`.htm` now convert locally via pandoc instead of MinerU cloud** (no token, no quota, faster). Before conversion the HTML is cleaned — `style`/`class`/`id` attributes and layout-only `div`/`section`/`span` wrappers are stripped — so the vault gets the article content, not the inline-CSS noise. Raw HTML is kept on purpose so complex tables survive losslessly instead of degrading to a `[TABLE]` placeholder.
- `local-vault`: **digital-PDF image extraction tightened.** The size floor went from 5% → 12% of page area (`PYMUPDF4LLM_IMAGE_SIZE_LIMIT`), and extracted images now pass two more filters: a min-bytes drop (`PYMUPDF4LLM_IMAGE_MIN_BYTES`, default 6000 — tiny decorative images are removed, reference and all) and content de-duplication (a logo/header repeated on every page is stored once). This cuts both the slowdown and the no-value-image clutter from v1.3.0.

### Added

- `local-vault`: master switch `PYMUPDF4LLM_WRITE_IMAGES` (`scripts/config.py`, default on; `.env`: `KB_PDF_NO_IMAGES=1`) to turn digital-PDF image extraction off entirely for a text-only, fastest run.

## [1.3.0] - 2026-06-05

### Added

- `local-vault`: **digital PDFs now keep their images.** The pymupdf4llm path previously ran with `write_images=False`, so a text PDF with charts/figures lost every image (text-only output). It now extracts images (≥ `PYMUPDF4LLM_IMAGE_SIZE_LIMIT`, default 5% of page area — small logos/icons are skipped) into `attachments/<stem>/`, renaming them to ASCII-safe names (`img-0.png` …) so source filenames with spaces/CJK don't break the Markdown links, and rewrites the references. On a sparse→MinerU fallback the staged images are discarded.
- `local-vault`: new tuning knob `PYMUPDF4LLM_IMAGE_SIZE_LIMIT` (`scripts/config.py`, default `0.05`) controls the digital-PDF image-extraction floor as a fraction of page area.

### Changed

- `local-vault`: the clickable `sync.command` is now placed in the **knowledge-base root (the parent of the SOURCE folder)** instead of inside the SOURCE folder — the double-click entry and the "drop files here" folder are no longer the same place, and it still works under `/plugin install`. A stale auto-generated launcher left in the SOURCE folder by an older version is **removed automatically** (a user-written one is never touched), resolving the duplicate-launcher confusion.
- `local-vault`: when a *different* `sync.command` already exists at the root, an interactive terminal now **prompts update / skip** instead of silently overwriting. Non-interactively, our own out-of-date launcher self-heals silently while a user-customized one is left alone.

## [1.2.0] - 2026-06-03

### Added

- `local-vault`: the sync pipeline now drops a clickable `sync.command` **into the user's SOURCE folder** (macOS), with the absolute path to `sync.py` baked in. Tool and data live apart — under `/plugin install` the script sits deep in `~/.claude/plugins/cache/…`, so the old relative-path launcher was effectively unreachable for plugin users. The new launcher makes the daily loop "drop files → double-click → read the `.md`" work regardless of install path. It is created both by the setup wizard and idempotently on every run (covering the Claude-writes-`.env` setup path that never hits the wizard), and self-heals — re-pointing itself when a plugin upgrade moves `sync.py`.
- `local-vault`: new `KB_NO_LAUNCHER=1` `.env` flag (`config.INSTALL_CLICKABLE_LAUNCHER`) to opt out of writing the launcher into the source folder.

## [1.1.0] - 2026-06-02

### Added

- New skill: `local-vault` — build and query a local Markdown knowledge base ("vault"). Two distinct jobs:
  - **Convert / sync** raw files (PDF, Word/docx, PowerPoint/pptx, Excel/xlsx, csv/tsv, images, html, md/txt, code) into clean Markdown with retrieval-friendly frontmatter (`abstract` / `auto_tags` / `synonyms` / `key_data` + a `source` backlink to the raw file). Local-first (pandoc / pymupdf4llm / openpyxl / python-pptx); cloud OCR (MinerU) only as a fallback for scanned PDFs, legacy `.doc`/`.ppt`, `.html`, and images.
  - **Retrieve / answer** questions over the resulting vault with retrieval discipline — startup vault health check, coverage self-monitoring, lossy-content flagging, and Maps-of-Content (MOC) proposals that grow from real usage.
- Incremental sync (only source files without a matching `.md` are processed), orphan staging (deleted sources → `orphaned/<date>/`, never hard-deleted), and frontmatter-only enrichment (document **bodies** are never rewritten → zero content-loss risk from the tool).
- Per-type routing: xlsx dual value+formula read, digital PDF via pymupdf4llm, pptx charts + notes + de-duplicated concurrent image OCR (`claude -p`), code/markdown passthrough; unsupported types are reported at the end, never silently dropped.
- Ships `scripts/sync.py` (pipeline + interactive setup wizard), `scripts/config.py` (tuning knobs), `scripts/mineru_client.py` (cloud OCR fallback), and `sync.command` (double-click entry).
- `SKILL.zh.md` Chinese reference (kept in sync with the English `SKILL.md`; excluded from `.zip` packaging).

### Changed

- README, `plugin.json`, and `marketplace.json` updated to list `local-vault` — the collection is now **four skills** (verifying / topic-brief / analyst-research / local-vault).

## [1.0.0] - 2026-05-28

First stable release. Consolidates the `analyst-research` work (the internal 0.6.x development series, never published) into one milestone: a mature three-mode research skill replacing the old `light-research`, with full bilingual source files across all three skills.

### Added

- New skill: `analyst-research` — three-mode end-to-end research workflow for investment analysts and policy researchers. Battle-tested on the Saudi Vision 2030 economic diversification deep-dive (heavy mode, 35 figures, 15k+ words). User picks mode at trigger time:
  - **light mode** — 4-5 page decision memo, 0 charts, 60-80 min budget. Successor to the standalone `light-research` skill; all 6 workflow steps and the grep self-check carried over verbatim (see `references/workflow_light.md`).
  - **medium mode** — 12-15 page topic analysis, 6-10 charts, half-day budget (3-5 h). 8-step skeleton with one hard stop (sign-off after draft). PDF + Word derivations. Footnote citations (`references/workflow_medium.md`, `_quarto-medium.yml`).
  - **heavy mode** — Flagship report 30-40 pages / 15k+ words, 25-35+ charts, days-to-weeks budget. 11-step skeleton, optional multi-LLM (Claude + GPT + DS), three hard stops (outline / draft / final), PDF + Word + WeChat md + HTML publication derivations. BibTeX + APA citations (`references/workflow_heavy.md`, `report_style_spec.md`).
- Mode-picker UX: when `analyst-research` is triggered, the AI first presents the three modes with runtime budgets and chart counts, then loads only the workflow + Quarto template + spec relevant to the chosen mode. If the user's trigger message already contains explicit scope hints (page count, time budget), the AI infers the mode and asks one-line confirmation. After mode confirmation it asks one short report-language question.
- `MODE_REGISTRY.md` — single source of truth for the three modes' parameters (comparison table, per-mode file dependencies, use-case fit / anti-fit, mode-upgrade trajectory, propagation order for future edits). Consolidates per-mode parameters that were previously scattered across `SKILL.md`, `workflow.md` and the workflow headers.
- SessionStart announce hook (`hooks/hooks.json` + `scripts/announce-loaded.sh`) — fires when the plugin loads in Claude Code and emits a short description of the three skills and the mode-picker UX. Bash 3.2 compatible (macOS stock shell).
- AI-usage disclosure footer convention (`report_style_spec.md` §八) — a standard 5-line disclosure paragraph (EN + zh templates) placed before the references chapter; mandatory for medium / heavy modes, optional for light.
- Full Chinese mirrors for `analyst-research`: `SKILL.zh.md`, `MODE_REGISTRY.zh.md`, and `.zh.md` versions of every reference file (`workflow`, `workflow_light/medium/heavy`, `report_style_spec`). English `.md` stays authoritative for the agent; `.zh.md` is for human readers and excluded from packaged zips.
- Cross-mode invariants documented in `references/workflow.md` (router file): hypothesis-first start, source provenance, three-state labeling (fact / estimate / inference), no fabricated numbers, reply language matches question language.
- Mode-upgrade path: a project started in `light` mode can be re-triggered in `medium` or `heavy` since all three share the hypothesis-lock first step. Downgrade is generally not worth it (cut deliverables instead).
- Visual production stack carried over from heavy mode: shared `chart_template.py` (matplotlib styling — McKinsey blue-grey palette, Songti SC CJK, fig number alignment, accent color separation, `lang='en'` switch for English source/note prefixes), `publication-style-template.html`, `author.jpg`.
- `report_style_spec.md` covering: document layout, chart design principles, chart production rules, HTML derivation, `chart_template` interface contract, Quarto config defaults. Loaded by medium + heavy modes; skipped by light mode (no charts).

### Changed

- Report-language policy: reports default to English; the AI replies in the user's chat language. The mode-picker now asks a one-line report-language question after mode confirmation.
- Bilingual-sync notes added to `topic-brief` and `verifying` `SKILL.md` + `SKILL.zh.md` (English is the single source of truth; edit English first, mirror into `.zh.md` in the same change-set).
- README + plugin manifests (`plugin.json` / `marketplace.json`): `analyst-research` row / description refreshed with the updated mode parameters and report-language policy.

### Fixed

- Repo URL corrected from `reagan475614947/market-research-skills` to `genli-ai/market-research-skills` across README install instructions and the announce hook.

### Removed

- **BREAKING**: `light-research` skill removed as a standalone skill. Its functionality is preserved verbatim as `analyst-research` light mode. Users who previously invoked `/light-research` should now invoke `analyst-research` and pick `light` when prompted. The `workflow_light.md` and `_quarto-light.yml` files inside `analyst-research/references/` are byte-for-byte copies of the original `light-research` skill files.

### Migration

If you had `light-research` installed via this plugin marketplace at v0.5.0, upgrading to v1.0.0 will replace it with `analyst-research`. Trigger keywords that used to fire `light-research` (e.g., "5-page memo", "quick analysis", "决策摘要") now fire `analyst-research`, which will ask you to pick a mode — pick `light` for byte-identical behavior to v0.5.0.

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

## [1.4.0] - 2026-06-05

### 变更

- `local-vault`:**`.html`/`.htm` 改走本地 pandoc,不再用 MinerU 云**(无 token、无 quota、更快)。转换前先清洗 HTML——剥掉 `style`/`class`/`id` 属性和纯布局 `div`/`section`/`span` 包裹——让 vault 拿到的是正文内容,而不是满屏内联 CSS 噪音。刻意保留 raw HTML,使复杂表格无损保留,而不是被降成 `[TABLE]` 占位符丢内容。
- `local-vault`:**数字 PDF 抽图收紧。** 尺寸下限从页面 5% 提到 12%(`PYMUPDF4LLM_IMAGE_SIZE_LIMIT`),抽出的图再过两道:最小字节丢弃(`PYMUPDF4LLM_IMAGE_MIN_BYTES`,默认 6000——装饰小图连引用一起删)+ 内容去重(每页重复的 logo/页眉只存一份)。同时治 v1.3.0 的变慢与无价值图泛滥。

### 新增

- `local-vault`:总开关 `PYMUPDF4LLM_WRITE_IMAGES`(`scripts/config.py`,默认开;`.env`:`KB_PDF_NO_IMAGES=1`)可彻底关掉数字 PDF 抽图,纯文字最快跑。

## [1.3.0] - 2026-06-05

### 新增

- `local-vault`:**数字版 PDF 现在会保留图片。** pymupdf4llm 路径之前用 `write_images=False`,带图表/插图的文字 PDF 转完丢掉所有图(只剩文字)。现在会把图(≥ `PYMUPDF4LLM_IMAGE_SIZE_LIMIT`,默认页面面积 5%——小 logo/图标跳过)抽进 `attachments/<stem>/`,并重命名为 ascii 安全名(`img-0.png` …)以免源文件名含空格/中文破坏 Markdown 链接,同步改写引用。稀疏→MinerU fallback 时丢弃已抽的图。
- `local-vault`:新增可调旋钮 `PYMUPDF4LLM_IMAGE_SIZE_LIMIT`(`scripts/config.py`,默认 `0.05`),按页面面积比例控制数字 PDF 抽图下限。

### 变更

- `local-vault`:可双击的 `sync.command` 落点从 SOURCE 文件夹内改到**知识库根目录(SOURCE 的父目录)**——双击入口和「往里拖文件」的目录不再是同一个,且对 `/plugin install` 仍成立。旧版本遗留在 SOURCE 里的自动生成 launcher 会被**自动删除**(用户手写的不碰),消除重复 launcher 的困惑。
- `local-vault`:根目录已有一个**不同的** `sync.command` 时,交互终端现在会**提示更新 / 跳过**,不再静默覆盖。非交互时,我们自己的过期 launcher 静默自愈,用户自定义的保留不动。

## [1.2.0] - 2026-06-03

### 新增

- `local-vault`：同步管线现在会往**用户的原始文件目录**（macOS）放一个可双击的 `sync.command`，里面硬编码 `sync.py` 的绝对路径。工具与数据是分离的——`/plugin install` 时脚本埋在 `~/.claude/plugins/cache/…` 深处，旧的相对路径 launcher 对插件用户基本不可达。新 launcher 让「拖文件 → 双击 → 读 `.md`」的日常闭环在任何安装方式下都成立。它由配置向导创建，也在每次运行时幂等补放（覆盖「Claude 帮写 `.env`」这条不走向导的首配路径），并能自愈——插件升级使 `sync.py` 路径变化时自动重新指向。
- `local-vault`：新增 `KB_NO_LAUNCHER=1` 的 `.env` 开关（`config.INSTALL_CLICKABLE_LAUNCHER`），可关掉往原始文件目录写 launcher 的行为。

## [1.1.0] - 2026-06-02

### 新增

- 新 skill：`local-vault` —— 构建并查询一个本地 Markdown 知识库（"vault"）。两件不同的事：
  - **转换 / 同步**：把原始文件（PDF、Word/docx、PowerPoint/pptx、Excel/xlsx、csv/tsv、图片、html、md/txt、代码）转成干净的 Markdown，带检索友好的 frontmatter（`abstract` / `auto_tags` / `synonyms` / `key_data` + 双链回原文的 `source`）。本地优先（pandoc / pymupdf4llm / openpyxl / python-pptx）；云端 OCR（MinerU）仅作兜底，用于扫描版 PDF、老式 `.doc`/`.ppt`、`.html` 和图片。
  - **检索 / 回答**：基于生成的 vault 负责任地回答问题 —— 会话首问做 vault 健康检查、自我监控覆盖度、标注有损内容、按真实使用沉淀 Maps-of-Content（MOC）。
- 增量同步（只处理 SOURCE 中没有对应 `.md` 的文件）、孤儿暂存（源文件被删 → 工具生成的 `.md` 移到 `orphaned/<日期>/`，绝不硬删）、仅改 frontmatter 的增强（文档**正文**永不被改写 → 工具本身零内容丢失风险）。
- 按类型路由：xlsx 值+公式双读、数字版 PDF 走 pymupdf4llm、pptx 图表 + 备注 + 去重并发图片 OCR（`claude -p`）、代码/markdown 原样透传；不支持的类型在结尾统一报告，绝不静默丢弃。
- 自带 `scripts/sync.py`（管线 + 交互式配置向导）、`scripts/config.py`（调参）、`scripts/mineru_client.py`（云端 OCR 兜底）、`sync.command`（双击入口）。
- `SKILL.zh.md` 中文参考版（与英文 `SKILL.md` 同步；打包 zip 时排除）。

### 变更

- README、`plugin.json`、`marketplace.json` 更新，列入 `local-vault` —— 合集现为**四个 skill**（verifying / topic-brief / analyst-research / local-vault）。

## [1.0.0] - 2026-05-28

首个稳定版。把 `analyst-research` 的开发成果（内部 0.6.x 系列，从未公开发布）收敛为一个里程碑：一个成熟的三档研究 skill 取代旧的 `light-research`，并为三个 skill 补齐完整的中英双语源文件。

### 新增

- 新 skill：`analyst-research` —— 面向投研分析师与政策研究者的三档端到端研究工作流。已在沙特 Vision 2030 经济多元化深度报告跑通（heavy 档，35 张图、1.5 万字+）。用户在触发时选档：
  - **light 档** —— 4-5 页决策备忘，0 图，60-80 分钟预算。继承独立的 `light-research` skill；6 步工作流与 grep 自检逐字搬运（见 `references/workflow_light.md`）。
  - **medium 档** —— 12-15 页主题分析，6-10 图，半天预算（3-5 h）。8 步骨架，1 个硬停（draft 后 sign-off）。PDF + Word 派生。Footnote 引用（`references/workflow_medium.md`、`_quarto-medium.yml`）。
  - **heavy 档** —— 旗舰报告 30-40 页 / 1.5 万字+，25-35+ 图，数天到数周预算。11 步骨架，可选多 LLM（Claude + GPT + DS），3 个硬停（outline / draft / final），PDF + Word + 公众号 md + HTML publication 派生。BibTeX + APA 引用（`references/workflow_heavy.md`、`report_style_spec.md`）。
- 选档 UX：触发 `analyst-research` 时，AI 先列出三档及各自的时间预算与图表数，再只加载所选档对应的 workflow + Quarto 模板 + spec。若触发语已含明确范围线索（页数、时间预算），AI 推断档位并一句话确认。确认档位后再问一句报告语言。
- `MODE_REGISTRY.md` —— 三档参数的单一事实源（对比表、各档文件依赖、适用 / 不适用场景、升档路径、未来改参数时的传播顺序）。把原先散落在 `SKILL.md`、`workflow.md` 和各 workflow 头部的参数收口。
- SessionStart announce hook（`hooks/hooks.json` + `scripts/announce-loaded.sh`）—— 插件在 Claude Code 加载时触发，输出三个 skill 与选档 UX 的简短说明。兼容 Bash 3.2（macOS 自带 shell）。
- AI 使用披露 footer 约定（`report_style_spec.md` §八）—— 标准 5 行披露段（中英模板），置于 references 章节之前；medium / heavy 档必填，light 档可选。
- `analyst-research` 全套中文版：`SKILL.zh.md`、`MODE_REGISTRY.zh.md`，以及每个 reference 文件的 `.zh.md` 版（`workflow`、`workflow_light/medium/heavy`、`report_style_spec`）。英文 `.md` 对 agent 为权威版；`.zh.md` 供人阅读，打包 zip 时排除。
- 跨档不变量写入 `references/workflow.md`（router 文件）：hypothesis 先行、来源可追溯、三态标注（事实 / 估算 / 推断）、不造数、回复语言与提问语言一致。
- 升档路径：从 `light` 档起步的项目可重新以 `medium` / `heavy` 触发，三档共享 hypothesis-lock 第一步。降档一般不值得（直接砍交付物即可）。
- 视觉生产栈从 heavy 档沿用：共享 `chart_template.py`（matplotlib 样式 —— McKinsey 蓝灰配色、Songti SC CJK、图号对齐、强调色分离、`lang='en'` 切换英文 source/note 前缀）、`publication-style-template.html`、`author.jpg`。
- `report_style_spec.md`：文档版式、图表设计原则、图表生产规则、HTML 派生、`chart_template` 接口契约、Quarto 配置默认值。medium + heavy 档加载；light 档跳过（无图）。

### 变更

- 报告语言政策：报告默认英文；AI 按用户聊天语言回复。选档后新增一句报告语言确认。
- 为 `topic-brief` 与 `verifying` 的 `SKILL.md` + `SKILL.zh.md` 补双语同步说明（英文为单一事实源；先改英文，同一改动集里同步进 `.zh.md`）。
- README + 插件清单（`plugin.json` / `marketplace.json`）：`analyst-research` 行 / description 按更新后的档位参数与报告语言政策刷新。

### 修复

- 仓库 URL 从 `reagan475614947/market-research-skills` 修正为 `genli-ai/market-research-skills`，覆盖 README 安装说明与 announce hook。

### 移除

- **BREAKING**：`light-research` 不再作为独立 skill。其功能逐字保留为 `analyst-research` 的 light 档。原先用 `/light-research` 的用户现在改触发 `analyst-research`，在提示时选 `light`。`analyst-research/references/` 内的 `workflow_light.md` 与 `_quarto-light.yml` 是原 `light-research` 文件的逐字节副本。

### 迁移

如果你在 v0.5.0 通过本插件 marketplace 装过 `light-research`，升级到 v1.0.0 会用 `analyst-research` 取代它。原先触发 `light-research` 的关键词（如「5 页 memo」「快速分析」「决策摘要」）现在触发 `analyst-research`，它会让你选档 —— 选 `light` 即与 v0.5.0 行为逐字节一致。

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
