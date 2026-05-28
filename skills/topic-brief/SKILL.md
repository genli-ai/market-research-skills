---
name: topic-brief
description: Generate a topic-focused briefing in HTML from public news sources. Use when user asks for a briefing / observation / digest / 简报 / 观察 on any subject — region (Middle East, ASEAN, India), industry (semiconductors, EV supply chain, AI), policy issue (AI regulation, critical minerals, cross-border payments), institution (Fed, ECB, IMF), or theme. Output is a single self-contained HTML file with blue-color "TOPIC BRIEF" branding, optimized for both browser viewing and direct copy-paste into 微信公众号 / WeChat Official Account editor. Walks through 5 steps with one user confirmation midway. Do NOT use this skill for short summaries (<1000 字), single-piece news commentary, or already-defined report templates.
---

# Topic Brief — Thematic Observation Briefing Generator

Generate a public-news-based information briefing for any subject (region / industry / policy issue / institution) and produce a single self-contained HTML file ready to paste into the 微信公众号 / WeChat Official Account editor.

> Bilingual skill. Chinese version: `SKILL.zh.md`. English is the single source of truth; the `.zh.md` is a synchronized translation — always edit the English first, then mirror the change into `.zh.md` in the same change-set, never edit only the Chinese.

## Trigger phrases

User says something like:
- "做一份 5 月下半月的中东观察"
- "Generate a semiconductor industry briefing for the past month"
- "做一期 AI 立法主题观察，时间是 2026 年 Q2"
- "/topic-brief"
- "用 topic-brief 跑一份 ..."

Any descriptive request such as "make a briefing / observation / digest on XX" should activate this skill.

## Scope exclusions

Before producing any briefing, check whether the subject falls into a refused category. The following are out of scope regardless of phrasing:

- **Political issues** — elections, parties, political figures' positions, government legitimacy debates
- **Military issues** — operations, force composition, equipment counts, conflict details, defense policy
- **Religious issues** — doctrines, denominational disputes, religious leaders' statements
- **Entertainment celebrity gossip** — personal life, scandals, fan disputes
- **Other inherently controversial topics** — culture wars, identity disputes, value-judgement debates

If the requested subject is one of the above, reply with exactly one line and stop:

```
Out of scope. (超出能力范围)
```

Do not run search, do not draft anything, do not negotiate the scope.

## Response language

Reply in the language of the user's request. Chinese question → Chinese reply; English question → English reply; mixed input → follow the dominant language. The generated HTML itself follows the language of the source materials and the `subject_name` (Chinese subjects produce Chinese briefings, English subjects produce English briefings). Field labels in user-facing reports (e.g., 来源 / Source) should match the briefing's body language.

## 5-step workflow

### Step 1 — Collect parameters (one user-facing question prompt, 4 questions)

If the user did not provide all parameters in the trigger, ask everything in **one batched user-question prompt**:

| Question | Header | Options |
|---|---|---|
| What is this issue's subject? | 主题 / Subject | free text (region / industry / issue / institution name) |
| Time window? | 时间 / Period | "past two weeks / past month / past quarter / custom range". **Immediately normalize the answer to two ISO dates `[period_start, period_end]`** (YYYY-MM-DD). Example: if today is 2026-05-13 and the user says "past month" → period_start=2026-04-13, period_end=2026-05-13 |
| Source preference? | 信息源 / Sources | "A default authoritative whitelist / B my own whitelist / C block certain sources" |
| Author byline? | 作者 / Author | Prompt: "The cover bottom-left author slot defaults to 'developed by Gen' — what should it show?" Explicit options: "A keep default / B leave blank". The user-question prompt's built-in `Other` option lets the user type a custom byline. |

- The **subject** field lands in JSON as `subject_name` (e.g., "中东", "半导体", "AI 立法")
- The **author** field lands in JSON as `author`, rendered at the cover bottom-left. Three user options map to three JSON states:

  | User choice | JSON action | Rendered effect |
  |---|---|---|
  | A keep default | omit `author` field | shows "developed by Gen" (schema default) |
  | B leave blank | write `"author": ""` | blank |
  | Other custom (e.g., "张三 · 研究院") | write `"author": "张三 · 研究院"` | custom text |

- Within the same session, if the user has already answered the author question, reuse the last value for subsequent runs (unless they change it).

If the trigger already specifies every parameter ("做 5.1–5.12 的中东观察，作者署名 '张三'"), skip the question prompt and proceed.

### Step 2 — Parallel material gathering

**Every search query must include a time filter.** For Google / Bing: `after:YYYY-MM-DD before:YYYY-MM-DD` (using the period_start / period_end normalized in Step 1); for other engines, use the equivalent syntax. Without a time filter, the engine returns results by relevance — older "big events" with high SEO weight get pulled in and stale the briefing.

**Time policy**:
- **Focus body** may reference earlier background context for contrast (e.g., "last year a similar report by X said..."), but **must explicitly tag the time point** (e.g., "in 2025 Q3..."), so readers can tell background from in-period events at a glance
- **Items in the 4 sub-sections** must strictly fall in-window (event_date within `[period_start, period_end]`). Out-of-window material is either cut or moved to the focus body as labeled background

**Search-engine query at least 4–6 times**, covering these dimensions (adapt to subject type):

| Subject type | Recommended search dimensions (4–6) |
|---|---|
| Region | central-bank decisions / macro data (GDP, inflation, trade) / major policies / international cooperation / breaking events |
| Industry | bellwether company moves / regulation / capacity investment / upstream inputs / end-market demand / international competition |
| Policy issue | legislative progress / enforcement cases / academic discussion / cross-border spillovers / public controversy |
| Institution | key decisions / senior official speeches / data releases / research output / legislative hearings |

**Fetch web body 1–2 times** to deep-read the focus report's primary text (extract specific numbers, scenarios, policy implications).

**Default authoritative whitelist** (unless the user specified otherwise in Step 1):
- International institutions: IMF, World Bank, OECD, ADB, UNCTAD, IADB, AIIB, IEA, WTO
- Central banks: Federal Reserve, ECB, Bundesbank, individual country central banks
- Governments: European Commission, national statistical offices
- Mainstream financial media: Reuters, Bloomberg, FT, Economist, Nikkei Asia, Xinhua, Business Standard

### Step 3 — Direction confirmation (mandatory user check-in) ⚠️

**Stop after material gathering** and confirm direction before writing:

```
Report to user:
- Time window: [period_start, period_end]
- Proposed focus report: <title> by <institution>, published <YYYY-MM-DD> (URL: ...)
- Proposed 4 sub-sections with candidate items (each tagged with event date):
  A. <section> — 3–5 items:
     · [YYYY-MM-DD] <headline> · <source institution>
     · [YYYY-MM-DD] <headline> · <source institution>
  B. ...
  C. ...
  D. ...

Ask:
- Confirm the direction?
- Swap the focus?
- Adjust the 4 sub-sections?
- Any candidate items falling outside the window (check the dates)?
```

**Every candidate item must show its event date** — this gate lets both the user and the model spot-check freshness, preventing stale items from leaking into the final draft.

If the user adjusts, revise and confirm once more. **Only after sign-off proceed to Step 4.**

Skipping this gate causes 5,000-character rewrites when the focus turns out wrong.

### Step 4 — Compose the JSON

Follow the schema and discipline in [prompts/system.md](prompts/system.md):

**Length and structure**:
- Focus body 1,500–2,500 characters (3–5 sections, 200–500 chars each)
- 4 sub-sections × 3–4 items each (headline ≤30 chars + body 100–300 chars)
- summary: focus blurb 150–250 chars + 4 region_items one sentence each
- Total: 3,000–5,000 characters

**Top discipline — no fabricated numbers**
Every concrete number (percentage, currency amount, date, count) must be traceable to the materials gathered in Step 2. **After writing, re-read the draft and ask "where did this number come from?" at every figure.** If you cannot answer, fix it.

**Time-window discipline**:
- Every sub-section `item` must carry an `event_date` field (YYYY-MM-DD; YYYY-MM is acceptable when only the month is known)
- Every `event_date` must fall within `[period_start, period_end]`
- When the focus body references earlier background, tag the time point explicitly ("in 2025 Q3..." / "last year...")

**JSON quote discipline**: Chinese inline quotes must use paired `"` and `"`, **never** straight `"` (breaks JSON parsing).

**Style reference**: [reference/](reference/) contains 4 historical samples (3 regional + 1 red-brand institutional). Mirror their phrasing, cadence, and tone.

**Save path**: `output/seed/<subject>_<period_end>.json` so seed data is traceable.

### Step 5 — Render and report

```bash
python3 scripts/render.py output/seed/<subject>_<period_end>.json --out output --open
```

- Auto-runs `fix_quotes` to repair Chinese quotation pairs
- Renders HTML to `output/<period_end>_<title>.html`
- Opens it in the browser

**Reporting checklist**:
- File path
- Character count / items per sub-section
- Source URL list grouped by the 4 sub-sections
- Reminder: human review of every number and URL is required before publishing — AI output ≠ conclusion

## Tool-call mapping (cross-LLM adaptation)

This skill describes tool actions in generic semantic terms so non-Claude terminals can map them to their own toolset:

| Generic verb | Maps to (Claude Code) | Maps to (other terminals) |
|---|---|---|
| Search-engine query | `WebSearch` | terminal's web-search tool |
| Fetch web body | `WebFetch` | terminal's URL-fetch tool |
| User-facing question prompt | `AskUserQuestion` | terminal's interactive-prompt tool or plain stdout question |
| Read full text | `Read` | terminal's file-read tool |
| Execute shell command | `Bash` | terminal's shell-exec tool |

If the running terminal lacks an equivalent for one of these verbs (e.g., no interactive prompt), the LLM should degrade gracefully — for instance, ask the parameter questions as one plain message and wait for the user's reply.

## Failure handling

| Symptom | Action |
|---|---|
| Search returns no material for one dimension | Tell the user which queries were tried; ask whether to change keywords |
| A specific number cannot be verified | **Cut the item** or rephrase without the number; do not invent |
| JSON parse failure | 99% of the time it's Chinese-quote mis-pairing; `render.py` auto-runs `fix_quotes` as backup; if still broken, hand-inspect |
| Subject too narrow, 4 sub-sections cannot be filled | Ask user to widen the time window or broaden the subject (e.g., "domestic EDA tools" → "semiconductors") |
| No suitable focus report | Fall back to the period's most important central-bank decision / sovereign-rating report / major bank research |

## Quick command reference

```bash
# Enter the skill directory (path inside the market-research-skills monorepo)
cd /path/to/market-research-skills/skills/topic-brief

# Render (auto-fixes quotes + opens browser)
python3 scripts/render.py reference/region_middle_east.example.json --out output --open

# Quote-fix only
python3 -c "from lib.fix_quotes import fix_file; from pathlib import Path; fix_file(Path('output/seed/xxx.json'))"

# Install dependency (first time)
python3 -m pip install --user jinja2
```

## Self-check checklist (run after Step 4)

- [ ] **issue_title ≤ 24 chars (including punctuation)** — longer titles wrap on the cover, fix it
- [ ] Exactly 4 sub-sections, each with 3–4 items
- [ ] `summary.items` has exactly 4 entries, aligned with the 4 sub-sections
- [ ] Every number is traceable to a source from Step 2
- [ ] Every `item.source` has a full URL
- [ ] **Every `item.event_date` falls within `[period_start, period_end]`**
- [ ] **If the focus body references out-of-window background, the time point is explicitly tagged** (e.g., "in 2025 Q3...")
- [ ] `item.headline` ≤ 30 chars
- [ ] Focus sections 3–5; total focus body 1,500–2,500 chars
- [ ] Chinese quotes use paired `"` `"`, no straight `"`
- [ ] `subject_name` field is filled
- [ ] `period_start` / `period_end` filled with ISO dates

## Red lines

- **Do not fabricate any number, date, or quote.** If the source material does not contain it, rewrite without the number or cut the item entirely.
- **Do not use a non-whitelisted source as the focus report.** Pop-econ blogs, social-media posts, and unattributed paraphrases cannot anchor the focus section.
- **Sub-section items must be strictly in-window.** Any item whose event_date falls outside `[period_start, period_end]` must be cut or moved to the focus body as labeled background (with an explicit time tag).
- **Every search must include a time filter.** Searching without `after:/before:` lets the engine return SEO-weighted older content — this is the root cause of stale briefings.
- **Do not skip Step 3 (direction confirmation).** Writing 5,000 characters in the wrong direction wastes the user's review budget.
- **Do not produce a briefing on a refused subject** (politics / military / religion / celebrity gossip / inherently controversial topics). Reply `Out of scope. (超出能力范围)` and stop.
- **Do not pad the briefing with non-substantive narration** ("令人震惊" / "标志着" / "势必"). Keep it factual, dense, source-anchored.
- **Do not omit human-review reminder in Step 5.** AI output is draft material, not a publishable conclusion.
