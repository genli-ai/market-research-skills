# Changelog

> 中文版本见本文件下半部分 / Chinese version below

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
