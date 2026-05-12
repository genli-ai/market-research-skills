# Changelog

> 中文版本见本文件下半部分 / Chinese version below

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
