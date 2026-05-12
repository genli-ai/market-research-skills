# verifying

> 中文版本见本文件下半部分 / Chinese version below

Information verification skill: trace every statement back to a whitelisted primary source; when nothing fits, plainly say "cannot verify."

## Five scenarios covered

| # | Scenario | Typical triggers |
|---|---|---|
| 1 | Basic truthfulness check | "where is this number from", "is this true" |
| 2 | Completeness — avoid out-of-context quoting | "is this taken out of context", "what's the full statement" |
| 3 | One-level reasoning (Z = P × Q reconciliation) | "check / reconcile X", "does this sales figure add up" |
| 4 | Negative statement | "is it true X never did Y", "X has not entered Y market" |
| 5 | Multi-source conflict | "two sources disagree", "IMF vs World Bank — which is right" |

Full rules and output formats: see [SKILL.md](SKILL.md). A Chinese reference of the rule set is in [SKILL.zh.md](SKILL.zh.md) — both are kept in sync.

## Core rules (summary)

- **Scope exclusions**: refused topics include politics, military, religion, entertainment celebrity gossip, and other inherently controversial subjects. The skill replies "Out of scope" and stops — no verification is attempted.
- **Whitelisted sources**: user-supplied files → official websites & authoritative databases (IMF / World Bank / IEA / FRED / etc.) → authoritative industry sources (NBER, think tanks, investment bank research, mainstream financial media) → aggregator databases (Statista / Wind / CEIC / SWFI / Refinitiv).
- **Three-layer search depth**: dig at most three layers; if still nothing fits, plainly say "cannot verify."
- **Download originals locally**: any cited report / chart / dataset must be downloaded and fully read before a verdict. If download is blocked, hand the link to the user and ask for help.
- **Six mandatory metadata fields**: time point, definition / scope, unit, coverage, revision status, data type (actual · forecast · projection · target · estimate).
- **Chart "meaning" verification**: the existence of a chart ≠ the user's reading of it. Check axes, units, start year, log vs linear, cumulative or not.
- **Negative statements**: negatives are essentially unfalsifiable — switch to a "search for counter-example" path.
- **Multi-source conflicts**: never force a pick; output both sources side-by-side with a difference attribution.
- **Rejected as final source**: Wikipedia, Zhihu, personal blogs, anonymous paraphrases, AI summaries, social media, SERP snippets alone.

## Response language

The skill always replies in the same language as the user's question — Chinese in, Chinese out; English in, English out.

## Cross-LLM adaptation

Tool-call verbs inside SKILL.md (read full text / fetch web body / search-engine query / image recognition / database query) describe semantic actions only, not specific terminal tool names. Claude Code / Claude Desktop / ChatGPT / Gemini / Copilot / Codex all work — each terminal's LLM maps the action verbs to its own local tools.

## Standalone install

```bash
# Option A: direct copy
cp -r skills/verifying ~/.claude/skills/

# Option B: install via packaged .zip
../../scripts/pack.sh verifying
unzip ../../releases/verifying.zip -d ~/.claude/skills/verifying
```

For non-Claude terminals (Codex / Gemini / Copilot), unzip the `.zip` file and place the resulting folder under your terminal's skills directory.

---

# verifying（中文版）

信息核实 skill：把陈述追溯到白名单内的一手来源，找不到就如实说「无法核实」。

## 覆盖五类场景

| # | 场景 | 典型触发语 |
|---|---|---|
| 1 | 基础真伪核实 | 「这个数字哪里来的」「这条信息是真的吗」 |
| 2 | 完整性补充（避免断章取义） | 「这个引用是不是断章取义」「完整说法是什么」 |
| 3 | 一层推理核实（Z = P × Q 拆解对账） | 「帮我核算 / 对账 X」「这个销售额算得对不对」 |
| 4 | 否定性陈述 | 「X 从未做过 Y 是真的吗」「X 没进过 Y 市场」 |
| 5 | 多源冲突 | 「两个来源数字不一致」「IMF 和世行哪个对」 |

完整规则与输出格式：见 [SKILL.md](SKILL.md)（英文权威版）；同义的中文参考版见 [SKILL.zh.md](SKILL.zh.md)——两份保持同步。

## 核心规则（摘要）

- **范围排除**：拒绝核实政治 / 军事 / 宗教 / 娱乐明星八卦 / 其他天然具有争议性的议题。skill 直接回复「超出能力范围」并停止，不做任何核实尝试
- **白名单来源**：用户提供文件 → 官方网站与权威数据库（IMF / World Bank / IEA / FRED 等）→ 权威行业信息源（NBER、智库、投行 Research、主流财经媒体）→ 聚合数据库（Statista / Wind / CEIC / SWFI / Refinitiv）
- **三层搜索深度**：最多向下挖三层，挖不到就明确说「无法核实」
- **下载原文通读**：涉及报告 / 图表 / 数据时必须下载原文通读；下载受阻时把链接交给用户、请用户协助
- **元数据强制 6 项**：时点 / 口径 / 单位 / 范围 / 修订状态 / 数据类型（actual · forecast · projection · target · estimate）
- **图表「图意」核实**：图存在 ≠ 图意被正确解读，要核坐标轴 / 单位 / 起始年份 / 是否对数 / 是否累计
- **否定性陈述**：负面陈述无法证伪，改走「找反例」路径
- **多源冲突**：不强行选一个，并列输出 + 差异归因
- **不接受**：维基、知乎、个人博客、未署名转述、AI 摘要、社交媒体、仅 SERP 摘要

## 回复语言

skill 始终用与用户提问相同的语言回复——中文问 → 中文答；英文问 → 英文答。

## 跨 LLM 适配

SKILL.md 里的工具调用动作（通读全文 / 抓取网页正文 / 搜索引擎检索 / 图像识别 / 数据库查询）只描述动作语义，不写死特定终端的工具名。Claude Code / Claude Desktop / ChatGPT / Gemini / Copilot / Codex 等终端均可使用，由各自的 LLM 映射到本地工具。

## 单独安装

```bash
# 方式 A：直接拷贝
cp -r skills/verifying ~/.claude/skills/

# 方式 B：使用打包好的 .zip 文件
../../scripts/pack.sh verifying
unzip ../../releases/verifying.zip -d ~/.claude/skills/verifying
```

非 Claude 终端（Codex / Gemini / Copilot）：解压 `.zip` 文件，把生成的文件夹放进各自终端的 skills 目录即可。
