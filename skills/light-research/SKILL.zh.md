---
name: light-research
description: 用于快速产出 5 页内决策备忘 / executive brief 的轻量研究工作流，6 步骨架（hypothesis、search、plan、draft、self-check、freeze），单 LLM，0 硬停，BLUF consulting-style 摘要，纯文字无图，仅 PDF + Word 产出。预算 60-80 min。触发：用户输入 /light-research 或描述「快速分析、5 页备忘、内部 memo、exec brief、决策摘要、1 小时简报」类需求时使用。不适用：长篇研报（用 heavy-research）、slide deck（用 deckster-slide-generator）、单条新闻评论（用 market-research-skills:topic-brief）、纯工具脚本。
---

# light-research · 轻量研究工作流 skill

heavy-research 的轻量姐妹版。把 11 步压成 6 步、2 小时压成 1 小时，专攻 5 页内的决策备忘。砍掉图表、TOC、章节编号、bib、retrospective、复杂派生，但保留所有数据真实性红线。

> **版权与授权**：Copyright © 2026 Ligen <ligen.thu@gmail.com>. Licensed under the MIT License.

## 加载顺序

1. **必读** `~/.claude/skills/light-research/references/workflow.md`：6 步骨架 + 写作纪律 + grep self-check
2. **按需** `~/.claude/skills/light-research/references/_quarto-light.yml`：项目脚手架阶段拷到 `<项目根>/_quarto.yml`

读完 workflow.md 后按 workflow.md §一「新项目 onboarding 流程」启动项目脚手架。

## 与 heavy-research 的关系

两个**完全独立**的 skill，不共用文件，不互相 import。light 不是 heavy 的子集——是另一套针对短稿场景重新设计的工作流。

- **触发边界**：用户说「memo / brief / 简报 / exec summary / 内部备忘 / 决策摘要 / 快速分析 / 5 页 / 1 小时」类→ light；用户说「深度研究 / 长篇 / 研报 / 综述 / 多角度分析 / 公众号长稿」类 → heavy
- **不支持升级路径**：light 跑完想做成研报，重新用 heavy 跑一遍，不要尝试把 light 的产出 in-place 升级为 heavy

light 与 heavy 在跨项目沉淀上**各自独立 audit**——两个 skill 各自的 workflow.md 都可能因实战经验更新，互不同步。

## 项目目录结构

light 项目极简，无脚手架目录，全部文件平铺在项目根：

```
<项目根>/
├── hypothesis.md       step 1 产出（一句话假设 + 用户给的关键约束）
├── research.md         step 2 产出（20-30 条资料台账）
├── pdfs/               step 2 产出（5-8 份核心 PDF 全文）
├── outline.md          step 3 产出（一段话 outline）
├── draft.qmd           step 4 主稿
├── draft.pdf           step 6 冻结主报告
├── draft.docx          step 6 Word 派生
└── _quarto.yml         从 skill 拷贝的 light 版模板
```

**无** `_state.md`（单 session 完成不需要 cold-start anchor）、**无** 项目级 `CLAUDE.md`（无项目特化）、**无** `9_retrospective/`（light 不写复盘）、**无** `figures/`（light 不出图）、**无** `references.bib`（用 footnote `^[来源 + URL + 日期]` 内联引用替代）。

## 何时使用本 skill

- 用户明确说「写个 memo / 5 页 brief / exec summary / 决策摘要」
- 用户输入 `/light-research` 命令显式唤起
- 任务粒度：单一 hypothesis、单一读者群（专家 / 决策者）、产出预期 5 页内、1 小时左右完成

## 何时不要用

- 长篇研报、多 take-away、多读者层、需要派生公众号或 HTML → 用 `heavy-research`
- Slide deck → 用 `deckster-slide-generator`
- 单条新闻评论 / 短摘要 → 用 `market-research-skills:topic-brief`
- 纯工具脚本，无研究产出

## skill 自身演化

light 跑完不强制走 audit / retrospective（与 heavy 不同）。但若 AI 或用户在执行中发现 workflow / yml 缺陷，可立即改 skill 全局再继续。重大改动打 minor version。
