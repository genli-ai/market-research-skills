# Mode Registry · analyst-research

Single source of truth for the three modes. SKILL.md, workflow.md, CHANGELOG, and downstream tooling all reference this file. **When mode parameters change, edit this file first, then propagate.**

---

## Mode table

| Dimension | light | medium | heavy |
|---|---|---|---|
| **Tagline** | 5-page decision memo | 10-15 page topic analysis | Flagship report 15k+ words |
| **Output length** | 4-5 pages (< 4 视为过薄,需补充) | 12-15 pages (< 12 偏薄) | 30-40 pages / 15k+ words |
| **Chart count** | 0 | 6-10 | 25-35+ |
| **Runtime budget** | 60-80 min | 3-5 hours | days-to-weeks |
| **LLM model** | single (Claude solo) | single (Claude solo) | single or multi-LLM (Claude + GPT critique optional) |
| **Workflow steps** | 6 | 8 | 11 |
| **Hard stops** | 0 (soft only) | 1 (sign-off after draft) | 3 (outline / draft / final) |
| **Citation style** | Markdown footnote (`^[org, title, date. URL.]`) | Markdown footnote (or .bib if heavy queued) | BibTeX (`references.bib`) + APA via Quarto |
| **PDF derivation** | ✅ | ✅ | ✅ |
| **Word derivation** | ✅ | ✅ | ✅ |
| **WeChat md derivation** | ❌ | ❌ | ✅ |
| **HTML publication derivation** | ❌ | ❌ | ✅ |
| **Project scaffolding depth** | minimal (4 files) | medium (`5_scripts/_path.py` + numbered dirs) | full 10-numbered-dir + local skill copy |
| **Chart template** | n/a (no charts) | shared `chart_template.py` | shared `chart_template.py` |
| **Onboarding questions** | 1 (hypothesis only) | 2-3 (hypothesis + optional second hard stop) | 6-7 (hypothesis + multi-LLM decision + Quarto reuse + audience + bib readiness + output formats + LLM mix) |

## Per-mode file dependencies

| Mode | Workflow file | Quarto template | Spec file | Scripts |
|---|---|---|---|---|
| light | `references/workflow_light.md` | `references/_quarto-light.yml` | n/a (no charts) | n/a |
| medium | `references/workflow_medium.md` | `references/_quarto-medium.yml` | `references/report_style_spec.md` | `scripts/chart_template.py` |
| heavy | `references/workflow_heavy.md` | spec §5.1 (no separate `.yml`) | `references/report_style_spec.md` | `scripts/{chart_template.py, publication-style-template.html, author.jpg}` |

## Use cases (trigger fit)

| User signals | Pick |
|---|---|
| "5-page memo" / "exec brief" / "1-hour briefing" / "决策摘要" / "内部 memo" | **light** |
| "topic analysis" / "half-day brief" / "10-page report" / "board memo with data" / "主题分析" / "半天分析" | **medium** |
| "flagship report" / "long-form research" / "industry deep-dive" / "policy assessment" / "投研报告" / "深度报告" / "长篇综述" | **heavy** |

## Anti-fit (don't trigger this skill)

| User signals | Pick instead |
|---|---|
| Single-piece news commentary | `market-research-skills:topic-brief` |
| Slide deck / PPT | `deckster-slide-generator` |
| One-shot Q&A (no written report) | Just answer directly, no skill |
| Pure literary or marketing copy | Not this skill's domain |
| Tool/script-only project, no report output | Not this skill's domain |

## Mode-upgrade trajectory

If a project starts in `light` and outgrows the scope, re-trigger in `medium` — all three modes share the **hypothesis lock first step**, so the early work transfers. Same path `medium → heavy`. Downgrading (`heavy → medium`) is generally not worth it; cut deliverables rather than re-run.

## Retrospective section per mode

After project closes, run the mode-specific retrospective rule:

| Mode | Retrospective section |
|---|---|
| light | `workflow_light.md §六` |
| medium | `workflow_medium.md §八` |
| heavy | `workflow_heavy.md §九` |

Each retrospective decides which project learnings get promoted back to the skill itself (skill versioning).

## When to revise this registry

Edit this file (and bump the skill's minor version) whenever:

- A mode's hard-stop count changes
- A mode adds / removes a derivation format
- A mode's workflow file is split, merged, or renamed
- A new mode is introduced

Propagation order after edit:
1. **MODE_REGISTRY.md** (this file) — change source-of-truth
2. **SKILL.md** "Mode comparison at a glance" — re-sync table; or replace with a link to this file
3. **CHANGELOG.md** — note the registry change
4. **workflow.md** (router) — if mode count or naming changed, update the router pointer
5. **README.md** (top-level) — update the "Skills currently included" row if user-facing description changed
