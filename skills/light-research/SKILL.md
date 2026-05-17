---
name: light-research
description: Lightweight research workflow for producing decision memos / executive briefs in 5 pages or less. 6-step skeleton (hypothesis, search, plan, draft, self-check, freeze), single LLM, 0 hard stops, BLUF consulting-style summary, plain text no charts, PDF + Word output only. Budget 60-80 min. Triggers: user types /light-research or describes needs like "quick analysis", "5-page memo", "internal memo", "exec brief", "decision summary", "1-hour briefing", "快速分析", "5 页备忘", "内部 memo", "决策摘要". Not for: long-form research reports (use heavy-research), slide decks (use deckster-slide-generator), single news commentary (use market-research-skills:topic-brief), pure tool scripts.
---

# light-research — lightweight research workflow

A lightweight sibling to heavy-research. Compresses 11 steps into 6, 2 hours into 1, focused on decision memos that fit in 5 pages. Drops charts, TOC, section numbering, bib files, retrospective, complex derivations — but keeps every data-integrity red line intact.

> **Copyright & license**: Copyright © 2026 Ligen <ligen.thu@gmail.com>. Licensed under the MIT License.

## Load order

1. **Required reading**: `~/.claude/skills/light-research/references/workflow.md` — the 6-step skeleton, writing discipline, and grep self-check rules (written in Chinese — the working language for this skill)
2. **On demand**: `~/.claude/skills/light-research/references/_quarto-light.yml` — copy to `<project-root>/_quarto.yml` during the scaffold step

After reading `workflow.md`, follow its §一「新项目 onboarding 流程」to start the project scaffold.

## Relationship to heavy-research

Two **fully independent** skills — no shared files, no cross-imports. light is not a subset of heavy; it is a separately designed workflow for short-form decision memos.

- **Trigger boundary**: user says "memo / brief / 简报 / exec summary / 内部备忘 / 决策摘要 / 快速分析 / 5 页 / 1 小时" → light; user says "deep research / long-form / 研报 / 综述 / 多角度分析 / 公众号长稿" → heavy
- **No upgrade path**: if a light run grows into something that should have been a heavy report, rerun under heavy from scratch — do not try to in-place upgrade the light output

light and heavy each audit their own workflows independently — both `workflow.md` files may evolve from real-world experience and are not kept in sync with each other.

## Project directory layout

A light project is intentionally minimal — no scaffold subdirectories, everything flat in the project root:

```
<project-root>/
├── hypothesis.md       step 1 output (one-line hypothesis + user-supplied constraints)
├── research.md         step 2 output (20–30 source ledger)
├── pdfs/               step 2 output (5–8 core PDFs, full text)
├── outline.md          step 3 output (single-paragraph outline)
├── draft.qmd           step 4 main draft
├── draft.pdf           step 6 frozen main report
├── draft.docx          step 6 Word derivative
└── _quarto.yml         copied from the skill's light template
```

**No** `_state.md` (single-session run needs no cold-start anchor), **no** project-level `CLAUDE.md` (no project-specific customization), **no** `9_retrospective/` (light does not write retrospectives), **no** `figures/` (light is text-only), **no** `references.bib` (footnote `^[source + URL + date]` inline citations replace bib entries).

## When to use this skill

- User explicitly says "write me a memo / 5-page brief / exec summary / 决策摘要"
- User types `/light-research` to invoke explicitly
- Task granularity: single hypothesis, single audience (experts / decision-makers), 5-page output expected, ~1 hour to complete

## When NOT to use

- Long-form research reports, multiple take-aways, multiple reader tiers, WeChat or HTML derivatives required → use `heavy-research`
- Slide decks → use `deckster-slide-generator`
- Single news commentary / short summary → use `market-research-skills:topic-brief`
- Pure tool scripts with no research deliverable

## Tool-call mapping (cross-LLM)

Tool actions inside `workflow.md` are written in generic verbs so non-Claude terminals can map to their own toolset:

| Generic verb | Meaning |
|---|---|
| Read full text / 通读全文 | Load a PDF / md / txt / csv and read it completely |
| Fetch web body / 抓取网页正文 | Pull main content from a URL (not just SERP snippet) |
| Search-engine query / 搜索引擎检索 | Query a search engine with keywords |
| Database query / 数据库查询 | Query a structured data source by field (FRED, yfinance, iFinD, etc.) |

Map to your local equivalents at runtime.

## Response language

Reply in the language of the user's request. Chinese question → Chinese reply; English question → English reply; mixed input → follow the dominant language. The draft itself follows the language the user briefs the hypothesis in (Chinese hypothesis → Chinese draft, English hypothesis → English draft).

## Skill self-evolution

light does not force an audit / retrospective pass after each run (unlike heavy). But if the AI or user spots a workflow / yml defect mid-execution, fix the skill globally and continue. Significant changes bump a minor version.
