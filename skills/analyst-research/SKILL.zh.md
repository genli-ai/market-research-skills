---
name: analyst-research
description: 为投资分析师与政策研究者设计的端到端研究工作流 skill。三档 mode 由用户在触发时选择 —— light（4-5 页决策备忘，约 15 分钟，0 图）、medium（12-15 页主题分析，约 1 小时，6-10 图）、heavy（30-40 页 / 1.5 万字+ 旗舰报告，约 2-3 小时，25-35+ 图，多阶段工作流，可多 LLM，PDF + Word + 公众号 + HTML 派生）。报告默认英文；AI 按用户聊天语言回复。已在真实宏观 / 政策 / 股票研报（如沙特 Vision 2030 深度报告）实战验证。触发：用户输入 /analyst-research、/flagship-research，或描述「做研报、投研报告、主题分析、深度分析、research report、topic analysis、investment research、policy assessment、industry deep-dive」类需求。不适用：单条新闻评论（用 topic-brief）、slide deck（用 deckster-slide-generator）、一次性快问快答。
---

<!-- 双语 skill：本 SKILL.zh.md 是中文镜像，英文主文件为 SKILL.md。
     references/ 下每个 *.md（英文，agent 读）都配一个 *.zh.md（中文，给人读）。 -->

# analyst-research · 投研工作流 skill

为投资分析师与政策研究者设计、经实战验证的 AI 协作研究工作流，封装成可复用的 Claude skill。基于产出沙特 Vision 2030 深度报告（35 图、1.5 万字+）的方法论。三档 scope mode，由用户在触发时选择。

> **授权**：MIT。Copyright © 2026 Ligen <ligen.thu@gmail.com>。见 `LICENSE`。

## 第 0 步 —— 选 mode（加载 references 前必做）

触发本 skill 时，**先于**加载任何 reference 文件，请用户选一档 scope。逐字呈现以下三个选项：

```
本 skill 有三档 scope mode，按项目规模选一档：

  light    4-5 页决策备忘，0 图，约 15 分钟预算
           单 LLM session。纯 markdown 脚注引用。
           适用：exec brief、内部 memo、快速决策支持。

  medium   12-15 页主题分析，6-10 图，约 1 小时预算
           单 LLM。PDF + Word 派生。draft 后一个 sign-off 检查点。
           适用：主题深挖、带数据的 board memo、当天分析。

  heavy    30-40 页 / 1.5 万字+ 旗舰报告，25-35+ 图，约 2-3 小时预算
           单或多 LLM。PDF + Word + 公众号 md + HTML publication。
           跑完完整 11 步分阶段工作流（框定 → 取数 → 分析 → 起草 →
           复盘），含 3 个 sign-off 检查点。
           适用：行业深度、宏观主题、政策评估、旗舰投资者刊物。

哪一档适合你的项目？（回 light、medium 或 heavy）
```

若用户触发消息已含明确规模线索（页数、图数、时间预算），直接推断 mode 并一句话确认，不必呈现完整菜单：

> 「听起来像 ~10 页带几张图 —— medium 模式，按这个跑？」

mode 确认后，再问一句语言：**「报告语言 —— 英文（默认）还是其他语言？」**（见下方语言策略）。然后加载该 mode 的 references。

## 各 mode 加载顺序

**始终先**读 `references/workflow.md`（约 40 行，mode 路由），它指向 mode 专属工作流文件。（每个 reference 都有 `.zh.md` 中文镜像；agent 读英文 `.md`。）

### light 模式

1. **必读** `references/workflow.md` —— 总览 + mode 路由
2. **必读** `references/workflow_light.md` —— 6 步骨架、仅软停、BLUF 摘要、grep 自检
3. **必读** `references/_quarto-light.yml` —— 为 4-5 页备忘优化的 Quarto 模板（无 TOC、无章节编号、脚注引用、11pt 正文）
4. 无图。无 bibliography。无 HTML/公众号派生。跳过 `report_style_spec.md` 与 `chart_template.py`。

然后进 `workflow_light.md §1 hypothesis lock` 启动 6 步流程。

### medium 模式

1. **必读** `references/workflow.md` —— 总览 + mode 路由
2. **必读** `references/workflow_medium.md` —— 8 步骨架、单 LLM、draft 后一个 sign-off 检查点
3. **必读** `references/report_style_spec.md` —— 6-10 张图的视觉规范（chart_template 接口契约、调色板、字体策略）
4. **必读** `references/_quarto-medium.yml` —— Quarto 模板（脚注引用、无 .bib、11pt 正文、Songti SC CJK）
5. **按需** `scripts/chart_template.py` —— 绘图实现

然后进 `workflow_medium.md §1 onboarding` 搭脚手架并启动。

### heavy 模式

1. **必读** `references/workflow.md` —— 总览 + mode 路由
2. **必读** `references/workflow_heavy.md` —— 完整 11 步骨架、可选多 LLM、3 个 sign-off 硬停（outline / draft / final）
3. **必读** `references/report_style_spec.md` —— 含 HTML publication 派生的视觉规范
4. **按需** `scripts/chart_template.py` —— 绘图实现
5. **按需** `scripts/publication-style-template.html` —— HTML publication 模板
6. **按需** `scripts/author.jpg` —— HTML 页作者头像 placeholder

heavy 模式的 Quarto 模板来自 `report_style_spec.md §5.1`（无独立 `_quarto-heavy.yml`，spec 是 heavy quarto 配置的真相之源）。

然后进 `workflow_heavy.md §1.3 新项目 onboarding` 搭脚手架（把整个 `analyst-research/` 文件夹拷进项目根）并启动。

## Mode 速查对照

下表为速查；**真相之源是 `MODE_REGISTRY.md`**。mode 参数变更时先改那个文件，再传播到这里。

| 维度 | light | medium | heavy |
|---|---|---|---|
| 篇幅 | 4-5 页 | 12-15 页 | 30-40 页 / 1.5 万字+ |
| 图表 | 0 | 6-10 | 25-35+ |
| 时间预算 | 约 15 分钟 | 约 1 小时 | 约 2-3 小时 |
| LLM | 单 | 单 | 单或多 LLM |
| 工作流步数 | 6 | 8 | 11 |
| 硬停 | 0 | 1（draft 后 sign-off） | 3（outline / draft / final） |
| 派生形态 | PDF + Word | PDF + Word | PDF + Word + 公众号 md + HTML |
| 引用 | Markdown 脚注 | Markdown 脚注 | BibTeX + APA |
| 项目脚手架 | 最小 | 最小 | 完整（10 编号目录） |
| 图模板 | n/a | 共用（chart_template.py） | 共用（chart_template.py） |

各 mode 文件依赖、升降档路径、复盘段指针见 `MODE_REGISTRY.md`。

## 何时不该用本 skill

- 单条新闻评论 → 用 `market-research-skills:topic-brief`
- Slide deck / PPT → 用 `deckster-slide-generator`
- 一次性快问快答（无书面报告） → 直接答，不用 skill
- 纯文学或营销文案 → 非本 skill 领域
- 只有工具脚本、无报告产出 → 非本 skill 领域

本 skill 为**对已有研究与数据的综述加分析**而建（不做原创建模，见 `workflow_heavy.md §2.2`）。它在「已有深厚存量文献」的题目上最有效（IMF / World Bank / IEA / BIS、投行与咨询研究、学术论文、监管披露）。前沿、新闻驱动、机构覆盖稀薄的题目并不适合。

## 项目中途如何升降档

若 `light` 项目跑着发现需要更深，重新以 `medium` 触发 —— 工作流第一步相同（hypothesis lock），早期工作可迁移。`medium → heavy` 同理。降档较难（已投入脚手架），砍交付物而非重跑。

## 项目脚手架在 skill 之外

skill 在 `~/.claude/plugins/.../analyst-research/` 里保持只读。各项目产物落在用户项目目录。

**light**：skill 只建 `_quarto.yml`（拷自 `_quarto-light.yml`）与一个工作文件，无子目录。

**medium**：建 `_quarto.yml`（拷自 `_quarto-medium.yml`）、`5_scripts/_path.py`（注入 sys.path 以加载 `chart_template`）、最小编号目录。

**heavy**：把整个 `analyst-research/` 文件夹拷进项目根作本地工作副本，再建完整 10 编号目录脚手架（见 `workflow_heavy.md §11`）。这让项目级覆盖（调色板、字体、领域约定）住在本地副本里，不污染 skill。

## skill 演化

每个项目结案后，按 mode 专属工作流的复盘段（workflow_heavy.md §9、workflow_medium.md §8、workflow_light.md §6）决定哪些项目经验上溯回 skill 本身。skill 用 git 版本化，每次上溯 bump minor，重大架构变更 bump major。

## 语言策略

本 skill 为**中英双语**，遵循 marketplace 惯例。每份文档存两个文件：英文 `.md`（如 `SKILL.md`、`references/workflow_heavy.md`）与中文镜像 `.zh.md`（如 `SKILL.zh.md`、`references/workflow_heavy.zh.md`）。**英文是唯一权威源；`.zh.md` 是同步翻译，不是独立版本。** 编辑协议，无例外：**永远先改英文 `.md`，再在同一次改动里把同样的修改同步到 `.zh.md` 翻译。** 绝不只改中文，绝不让两者漂移；措辞冲突时以英文 `.md` 为准。

1. **对话回复跟随用户聊天语言。** 英文聊→英文回，中文聊→中文回，其他语言同理。运行时行为，非存储文件。
2. **报告默认英文。** 第 0 步 onboarding mode 选定后问一句「报告语言 —— 英文（默认）还是其他？」用户不指定就英文写 draft，指定其他就按其他。选择锁进项目 `CLAUDE.md`。覆盖旧的「draft 随 hypothesis 语言」规则。
3. **语言条件化的 grep 红线。** 英文稿跳过中文冒号比例红线、强制未转义 `$` 红线（金额写 `\$`）；中文稿反之。

本文件英文主文件为 `SKILL.md`。English version: `SKILL.md`.
