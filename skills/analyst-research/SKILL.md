---
name: analyst-research
description: >-
  End-to-end research workflow skill for investment analysts and policy
  researchers. Three scope modes the user picks at trigger time — light (4-5
  page decision memo, ~15 min, 0 charts), medium (12-15 page topic brief, ~1
  h, 6-10 charts), heavy (flagship report 30-40 pages / 15k+ words, ~2-3 h,
  25-35+ charts, multi-stage workflow, multi-LLM, PDF + Word + WeChat + HTML
  derivations). Reports default to English; the AI replies in the user's chat
  language. Battle-tested on real macro/policy/equity reports (e.g. Saudi
  Vision 2030 deep-dive). Triggers when user types /analyst-research,
  /flagship-research, or describes needs like "research report", "topic
  analysis", "investment research", "做研报", "投研报告", "主题分析", "深度分析", "policy
  assessment", "industry deep-dive". Not for: pure news commentary (use
  topic-brief), slide decks (use deckster-slide-generator), one-shot Q&A.
---

<!-- Bilingual skill: this SKILL.md is the English primary; the Chinese mirror is SKILL.zh.md.
     Each references/*.md has a Chinese mirror references/*.zh.md (same content, two languages).
     The .md files are authoritative for the agent; the .zh.md files are for human readers. -->

# analyst-research · investment research workflow skill

A field-validated AI-assisted research workflow for investment analysts and policy researchers, packaged as a reusable Claude skill. Built on the methodology that produced the Saudi Vision 2030 deep-dive (35 figures, 15k+ words). Three scope modes; user picks at trigger time.

> **License**: MIT. Copyright © 2026 Ligen <ligen.thu@gmail.com>. See `LICENSE`.

## Step 0 — pick a mode (REQUIRED before loading references)

When this skill is triggered, **before** loading any reference file, ask the user to pick a scope. Present these three options verbatim:

```
This skill has three scope modes. Pick one based on your project size:

  light    4-5 page decision memo, 0 charts, ~15 min budget
           Single LLM session. Pure markdown footnote citations.
           Use for: exec brief, internal memo, quick decision support.

  medium   12-15 page topic analysis, 6-10 charts, ~1 h budget
           Single LLM. PDF + Word derivations. Sign-off checkpoint after draft.
           Use for: topic deep-dive, board memo with data, same-day analysis.

  heavy    Flagship report 30-40 pages / 15k+ words, 25-35+ charts, ~2-3 h budget
           Single or multi-LLM. PDF + Word + WeChat md + HTML publication.
           Runs the full 11-step staged workflow (framing → sourcing →
           analysis → drafting → review), with 3 sign-off checkpoints.
           Use for: industry deep-dive, macro thesis, policy assessment,
                    flagship investor publication.

Which mode fits your project? (reply with light, medium, or heavy)
```

If the user's trigger message already contains explicit scope hints (page count, chart count, time budget), infer the mode and ask one-line confirmation instead of presenting the full menu:

> "Sounds like ~10 pages with a few charts — medium mode. Going with that?"

After the mode is confirmed, ask one short language question: **"Report language — English (default), or another language?"** (see Language policy below). Then load the reference files for that mode.

## Loading order per mode

First **always** read `references/workflow.md` (≈40 lines, mode router). It points you to the mode-specific workflow file. (Each reference also has a `.zh.md` Chinese mirror; the agent reads the English `.md`.)

### light mode

1. **Required** `references/workflow.md` — overview + mode router
2. **Required** `references/workflow_light.md` — 6-step skeleton, soft stops only, BLUF executive summary, grep self-check
3. **Required** `references/_quarto-light.yml` — Quarto template optimized for a 4-5 page memo (no TOC, no number sections, footnote citations, 11pt body)
4. No charts. No bibliography. No HTML/WeChat derivation. Skip `report_style_spec.md` and `chart_template.py`.

Then proceed to `workflow_light.md §1 hypothesis lock` to start the 6-step flow.

### medium mode

1. **Required** `references/workflow.md` — overview + mode router
2. **Required** `references/workflow_medium.md` — 8-step skeleton, single LLM, one sign-off checkpoint after draft
3. **Required** `references/report_style_spec.md` — visual spec for the 6-10 charts (chart_template interface contract, color palette, font policy)
4. **Required** `references/_quarto-medium.yml` — Quarto template (footnote citations, no .bib, 11pt body, Songti SC CJK)
5. **On demand** `scripts/chart_template.py` — chart styling implementation

Then proceed to `workflow_medium.md §1 onboarding` to scaffold the project and start.

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
| Output length | 4-5 pages | 12-15 pages | 30-40 pages / 15k+ words |
| Charts | 0 | 6-10 | 25-35+ |
| Runtime budget | ~15 min | ~1 h | ~2-3 h |
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

This skill is built for **synthesis-and-analysis of an existing body of research and data** (it does not build original models, per `workflow_heavy.md §2.2`). It works best on topics with a deep existing literature (IMF / World Bank / IEA / BIS, investment-bank and consulting research, academic papers, regulatory disclosure). Bleeding-edge, news-driven topics with thin institutional coverage are a poor fit.

## How to upgrade or downgrade scope mid-project

If you start a project in `light` and find it needs more depth, re-trigger the skill in `medium` — the workflow's first step is identical (hypothesis lock), so the early work transfers. Going `medium → heavy` is the same. Downgrading is harder (you've already invested in scaffolding); cut deliverables rather than re-run.

## Project scaffold lives outside the skill

The skill stays read-only in `~/.claude/plugins/.../analyst-research/`. Per-project artifacts live in the user's project directory.

For **light mode**, the skill creates only `_quarto.yml` (copied from `_quarto-light.yml`) and a single working file in the project. No subfolders.

For **medium mode**, the skill creates `_quarto.yml` (from `_quarto-medium.yml`), `5_scripts/_path.py` (sys.path injector to load `chart_template`), and minimal numbered output directories.

For **heavy mode**, the skill copies the entire `analyst-research/` folder into the project root as a local working copy, then creates the full 10-numbered-directory scaffold per `workflow_heavy.md §11`. This lets project-level overrides (palette, fonts, domain conventions) live in the local copy without polluting the skill.

## Skill evolution

After each project closes, follow the retrospective section of the mode-specific workflow file (workflow_heavy.md §9, workflow_medium.md §8, workflow_light.md §6) to decide which project learnings get promoted back to the skill itself. The skill is git-versioned; each promotion bumps minor version. Major architectural changes bump major version.

## Language policy

This skill is **bilingual (English + Chinese)** following the marketplace convention. Every authored doc exists in two files: an English `.md` (e.g. `SKILL.md`, `references/workflow_heavy.md`) and a Chinese mirror `.zh.md` (e.g. `SKILL.zh.md`, `references/workflow_heavy.zh.md`). **English is the single source of truth; the `.zh.md` is a synchronized translation, not an independent version.** Edit protocol, no exceptions: **always write or change the English `.md` first, then propagate the same change to the `.zh.md` translation in the same change-set.** Never edit only the Chinese, and never let the two drift; when wording conflicts, the English `.md` wins.

1. **Conversation replies follow the user's chat language.** English chat → reply in English; Chinese chat → reply in Chinese; likewise for any other language. This is runtime behaviour, not a stored artifact.
2. **Report language defaults to English.** At Step 0 / onboarding, after the mode is picked, ask one short question: "Report language — English (default), or another language?" If the user does not specify, write the draft in English; if they name another language, write in that. Lock the choice in the project `CLAUDE.md`. This supersedes any older "draft follows hypothesis language" rule.
3. **Language-conditioned grep redlines.** For an English report the Chinese colon-ratio redline is skipped and the unescaped-`$` redline is mandatory (escape dollar amounts as `\$`). For a Chinese report the reverse applies.

The Chinese mirror of this file is `SKILL.zh.md`. 中文版见 `SKILL.zh.md`。
