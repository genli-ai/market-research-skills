---
name: analyst-research
description: End-to-end research workflow skill for investment analysts and policy researchers. Three scope modes the user picks at trigger time — light (5-page decision memo, 60-80 min, 0 charts), medium (10-15 page topic brief, half-day, 3-8 charts), heavy (flagship report 15k+ words, days-weeks, 20-35+ charts, multi-LLM, PDF + WeChat + HTML derivations). Battle-tested on real macro/policy/equity reports (e.g. Saudi Vision 2030 deep-dive). Triggers when user types /analyst-research, /flagship-research, or describes needs like "research report", "topic analysis", "investment research", "做研报", "投研报告", "主题分析", "深度分析", "policy assessment", "industry deep-dive". Not for: pure news commentary (use topic-brief), slide decks (use deckster-slide-generator), one-shot Q&A.
---

# analyst-research · investment research workflow skill

A field-validated AI-assisted research workflow for investment analysts and policy researchers, packaged as a reusable Claude skill. Built on the methodology that produced the Saudi Vision 2030 deep-dive (35 figures, 15k+ words). Three scope modes; user picks at trigger time.

> **License**: MIT. Copyright © 2026 Ligen <ligen.thu@gmail.com>. See `LICENSE`.

## Step 0 — pick a mode (REQUIRED before loading references)

When this skill is triggered, **before** loading any reference file, ask the user to pick a scope. Present these three options verbatim:

```
This skill has three scope modes. Pick one based on your project size:

  light    5-page decision memo, 0 charts, 60-80 min budget
           Single LLM session. Pure markdown footnote citations.
           Use for: exec brief, internal memo, 1-hour decision support.

  medium   10-15 page topic analysis, 3-8 charts, half-day budget (3-5 h)
           Single LLM. PDF + Word derivations. Sign-off checkpoint after draft.
           Use for: topic deep-dive, board memo with data, half-day analysis.

  heavy    Flagship report 15k+ words, 20-35+ charts, days-to-weeks budget
           Single or multi-LLM. PDF + Word + WeChat md + HTML publication.
           Use for: industry deep-dive, macro thesis, policy assessment,
                    flagship investor publication.

Which mode fits your project? (reply with light, medium, or heavy)
```

If the user's trigger message already contains explicit scope hints (page count, chart count, time budget), infer the mode and ask one-line confirmation instead of presenting the full menu:

> "Sounds like ~10 pages with a few charts — medium mode. Going with that?"

## Loading order per mode

After the user confirms a mode, load the reference files for that mode and proceed:

First **always** read `references/workflow.md` (≈40 lines, mode router). It points you to the mode-specific workflow file.

### light mode

1. **Required** `references/workflow.md` — overview + mode router
2. **Required** `references/workflow_light.md` — 6-step skeleton, soft stops only, BLUF executive summary, 12-item grep self-check
3. **Required** `references/_quarto-light.yml` — Quarto template optimized for 5-page memo (no TOC, no number sections, footnote citations, 11pt body)
4. No charts. No bibliography. No HTML/WeChat derivation. Skip `report_style_spec.md` and `chart_template.py`.

Then proceed to `workflow_light.md §1 hypothesis lock` to start the 6-step flow.

### medium mode

1. **Required** `references/workflow.md` — overview + mode router
2. **Required** `references/workflow_medium.md` — 8-step skeleton, single LLM, one sign-off checkpoint after draft
3. **Required** `references/report_style_spec.md` — visual spec for the 3-8 charts (chart_template interface contract, color palette, font policy)
4. **Required** `references/_quarto-medium.yml` — Quarto template (footnote citations, no .bib, 11pt body, Songti SC CJK)
5. **On demand** `scripts/chart_template.py` — chart styling implementation

Then proceed to `workflow_medium.md §一 onboarding` to scaffold the project and start.

### heavy mode

1. **Required** `references/workflow.md` — overview + mode router
2. **Required** `references/workflow_heavy.md` — full 11-step skeleton, multi-LLM optional, 3 sign-off checkpoints (outline / draft / final)
3. **Required** `references/report_style_spec.md` — visual spec including HTML publication derivation
4. **On demand** `scripts/chart_template.py` — chart styling implementation
5. **On demand** `scripts/publication-style-template.html` — HTML publication template
6. **On demand** `scripts/author.jpg` — author photo placeholder for HTML page

Quarto template for heavy mode comes from `report_style_spec.md §5.1` (no separate `_quarto-heavy.yml` file — the spec is the source of truth for heavy mode quarto config).

Then proceed to `workflow_heavy.md §1.3 new-project onboarding` to scaffold the project (copies the whole `analyst-research/` folder into project root) and start.

## Mode comparison at a glance

Quick summary below; **authoritative source of truth is `MODE_REGISTRY.md`**. Edit that file first when mode parameters change, then propagate here.

| Dimension | light | medium | heavy |
|---|---|---|---|
| Output length | ≤5 pages | 10-15 pages | 15k+ words |
| Charts | 0 | 3-8 | 20-35+ |
| Runtime budget | 60-80 min | 3-5 hours | days-weeks |
| LLM model | single | single | single or multi-LLM |
| Workflow steps | 6 | 8 | 11 |
| Hard stops | 0 | 1 (sign-off after draft) | 3 (outline / draft / final) |
| Derived outputs | PDF + Word | PDF + Word | PDF + Word + WeChat md + HTML |
| Citation | Markdown footnote | Markdown footnote | BibTeX + APA |
| Project scaffolding | minimal | minimal | full (10 numbered dirs) |
| Chart template | n/a | shared (chart_template.py) | shared (chart_template.py) |

For per-mode file dependencies, mode-upgrade trajectory, and retrospective section pointers, see `MODE_REGISTRY.md`.

## When NOT to use this skill

- Single-piece news commentary → use `market-research-skills:topic-brief`
- Slide deck / PPT → use `deckster-slide-generator`
- One-shot Q&A (no written report) → just answer directly, no skill
- Pure literary or marketing copy → not this skill's domain
- Tool/script-only project with no report output → not this skill's domain

## How to upgrade or downgrade scope mid-project

If you start a project in `light` and find it needs more depth, re-trigger the skill in `medium` — the workflow's first step is identical (hypothesis lock), so the early work transfers. Going `medium → heavy` is the same. Downgrading is harder (you've already invested in scaffolding); cut deliverables rather than re-run.

## Project scaffold lives outside the skill

The skill stays read-only in `~/.claude/plugins/.../analyst-research/`. Per-project artifacts live in the user's project directory.

For **light mode**, the skill creates only `_quarto.yml` (copied from `_quarto-light.yml`) and a single working file in the project. No subfolders.

For **medium mode**, the skill creates `_quarto.yml` (from `_quarto-medium.yml`), `5_scripts/_path.py` (sys.path injector to load `chart_template`), and minimal numbered output directories.

For **heavy mode**, the skill copies the entire `analyst-research/` folder into the project root as a local working copy, then creates the full 10-numbered-directory scaffold per `workflow_heavy.md §十一`. This lets project-level overrides (palette, fonts, domain conventions) live in the local copy without polluting the skill.

## Skill evolution

After each project closes, follow the retrospective section of the mode-specific workflow file (workflow_heavy.md §九, workflow_medium.md §八, workflow_light.md §六) to decide which project learnings get promoted back to the skill itself. The skill is git-versioned; each promotion bumps minor version. Major architectural changes bump major version.

## Reply language

Reply in the user's question language. Chinese question → Chinese answer; English question → English answer. The draft's language follows the hypothesis language (Chinese hypothesis → Chinese draft, English hypothesis → English draft).

The workflow.md and report_style_spec.md are written in Chinese (the skill's working language during development). AI agents are expected to read Chinese references and apply them regardless of user-facing reply language.

---

## 中文摘要 (Chinese summary)

本 skill 是为投资分析师与政策研究者设计的 AI 协作研究工作流。提供三档 mode 由用户在触发时选择：

- **light** —— 5 页决策备忘，0 图，60-80 分钟，单 LLM，纯 markdown 脚注引用
- **medium** —— 10-15 页主题分析，3-8 图，半天预算（3-5 小时），单 LLM，PDF + Word 派生
- **heavy** —— 1.5 万字+ 旗舰报告，20-35+ 图，数天到数周，单或多 LLM，PDF + Word + 公众号 md + HTML publication 多渠道派生

触发后 AI 会先用上面英文菜单询问用户选哪档（用户可中文回答 light/medium/heavy），然后加载对应 mode 的 references 启动。

详细工作流见 `references/workflow.md`，视觉规范见 `references/report_style_spec.md`。skill 内部所有 references 文档均为中文（开发工作语言），AI 读中文规范后按用户提问语言回复。

实战验证：本 skill 已在沙特 Vision 2030 经济多元化深度报告（35 图、1.5 万字、heavy mode）项目跑通。
