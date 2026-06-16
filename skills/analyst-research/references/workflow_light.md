# analyst-research · light mode workflow

> English is the authoritative version; the Chinese mirror is `workflow_light.zh.md`.

Scope: decision memo / executive brief / internal memo within 4-5 pages. Budget ~15 min, single LLM, 0 hard stops, plain text with no charts, PDF + Word output only.

medium and heavy are sibling modes of the same analyst-research skill, covering 12-15 page topic analysis and 30-40 page / 15k-word+ flagship reports respectively. All three share the hypothesis-lock starting point; downstream differences are governed by each mode.

---

## 1. New-project onboarding

### Step 0: announce

Briefly confirm to the user: "I have read the analyst-research light mode workflow (`references/workflow_light.md`) and am ready to start the 6-step flow."

Then ask **2 onboarding questions** (lock the answers, do not re-ask):

**Q1 · Research question or hypothesis (one sentence)**: the user gives the specific question. E.g. "Will the Fed cut 50bp in September", "Will company X beat consensus on Q3 earnings", "Recent shifts in Middle East sovereign-fund holdings of Chinese AI names".

**Q2 · Report language**: English (default) / Chinese / other. If the user does not specify, write the draft in English (see SKILL.md "Language policy"). Lock it into the hypothesis.md key-constraints section. English drafts skip the Chinese colon redline and enforce the unescaped-`$` redline (write dollar amounts as `\$`).

Items NOT asked (locked by default; the AI must not proactively ask):

- Output form: PDF + Word docx. **No HTML, no WeChat JPG, no slides.**
- Length: 4-5 page target (**< 4 pages is too thin and must be backfilled with content or deeper sub-questions**; 6 pages OK; 7-9 pages strong warning + suggest trimming; 10+ pages ask the user to re-assess light vs heavy; never hard-truncate).
- Charts: **0**, plain text + inline footnote citations.
- Audience: **expert / decision-maker** (not dual-audience, no explainer background).
- LLM: single LLM (Claude solo throughout).
- Summary form: **BLUF** (bottom line up front, single paragraph, 80-150 words / characters giving conclusion + key numbers + so-what).
- Time expectation: ~15 min, single session.
- Author byline / email: read the default from the global `~/.claude/CLAUDE.md` "author byline" section; ask explicitly only if absent.

### Step 1: scaffold

With cwd at the project root, run:

```bash
SKILL_ROOT="${SKILL_ROOT:-$(find ~/.claude/plugins -type d -path '*market-research-skills/skills/analyst-research' | head -1)}"
mkdir -p pdfs && \
cp "$SKILL_ROOT/references/_quarto-light.yml" _quarto.yml && \
touch hypothesis.md research.md outline.md draft.qmd
```

If the plugin-path lookup fails (e.g. installed via clone-and-symlink instead of the plugin marketplace), fall back to:

```bash
cp ~/.claude/skills/analyst-research/references/_quarto-light.yml _quarto.yml
```

Do not create `_state.md`, a project-level `CLAUDE.md`, a retrospective, or chart / scripts subfolders.

`.claude/settings.json` project-level permissions (same as heavy, checked into git):

```json
{
  "permissions": {
    "allow": [
      "Bash", "Read", "Write", "Edit", "MultiEdit",
      "WebSearch", "WebFetch", "TodoWrite", "Task", "Agent", "mcp__*"
    ]
  }
}
```

### Step 2: launch step 1

Write the hypothesis received in Step 0 into `hypothesis.md`:

```markdown
# Research question

<user's one sentence, verbatim>

# Key constraints

- Time-lock: <YYYY-MM-DD snapshot>
- Audience: <decision-maker / peer / investment committee>
- Output form: PDF + Word, within 5 pages
- Report language: <English (default) / Chinese / other>
- Sub-questions to cover (if any):
  - ...
```

Soft-stop into step 2 without waiting for user confirmation.

---

## 2. The 6-step skeleton

| Step | Name | Lead | Time budget |
|---|---|---|---|
| 1 | hypothesis | user + AI restatement | 5 min |
| 2 | search | Claude solo | 25 min |
| 3 | plan | Claude solo | 5 min |
| 4 | draft | Claude solo | 20 min |
| 5 | self-check | Claude solo | 10 min |
| 6 | freeze | Claude | 5 min |

**All soft stops (0 hard stops)** — after each step lands, the AI briefly tells the user the stage output and immediately proceeds. The user can stop, redirect, or roll back at any time.

---

## 3. Step details

### Step 1: hypothesis (no stop)

After asking the user's one-sentence research question in Step 0, the AI writes `hypothesis.md` with three parts: the research question verbatim + key constraints (time-lock / audience / output form / report language / sub-questions to cover) + the AI's restatement.

No divergent direction brainstorm (that is heavy's step 3 multi-direction triage). light assumes the hypothesis is already formed at onboarding.

**0-hard-stop nudge for a vague hypothesis**: if the hypothesis is vague in scope (e.g. "look at US AI stocks" with no time-lock / sub-topic boundary, or "analyse Middle East sovereign funds" without naming which one), the AI **states its own assumptions in the hypothesis.md key-constraints section** and, on landing, tells the user in one line: "Proceeding on these assumptions: time-lock X / scope Y / excluding Z; stop me to correct." **Do not stop to wait for confirmation** — under the 0-hard-stop design, transparent assumptions replace hard stops. The user can stop and roll back at any time.

Proceed to step 2 immediately after landing.

---

### Step 2: search (no stop)

**Goal**: 20-30 sources covering the key facts in the hypothesis + 5-8 core PDFs downloaded in full.

**6 source classes** (drops heavy's "academic & think tank" class; keeps the other 6):

| Class | Examples |
|---|---|
| A.1 international organisations | IMF, World Bank, IEA, OECD, BIS, UN, regional development banks |
| A.2 sovereign / government / central bank | central banks, statistics offices, finance ministries, sovereign funds, sector regulators |
| A.4 investment banks + consulting | GS / JPM / MS / Citi Country Outlooks, McKinsey / BCG sector reports |
| A.5 mainstream financial media | Chinese: Caixin, Wallstreetcn, FT Chinese; English: Bloomberg, Reuters, FT, WSJ, Economist |
| A.6 WeChat / industry communities / public social | finance / regional / vertical Chinese public accounts, LinkedIn / Substack / public X discussion |
| A.7 databases (programmatic) | available MCP / API / skill: iFind, `financial-data-sources` skill, etc. Used in step 2 for historical background numbers; time-lock snapshot numbers (latest prices / rates / valuation multiples) are re-pulled live before citation in step 4, see §step 4 |

The class numbering follows heavy's A.x naming for cross-reference; A.3 is skipped because light does not treat academia as a mandatory coverage dimension among the 6 classes (an individual academic paper that needs citing goes in as a single source under A.1 or A.4, not its own class).

**Discipline**:

1. **Class coverage**: search at least 3 classes by hypothesis type; do not settle for the 1-2 familiar classes. Pure macro topics usually A.1+A.2+A.7; company topics usually A.2+A.4+A.5+A.7; policy topics usually A.1+A.2+A.5.
2. **Order of magnitude**: 20-30 sources is enough; do not pursue heavy's 100+ coverage. Record type / institution / title / year / URL / key number / importance per source.
3. **Download core PDFs in full**: documents that play a **structural argumentative role** (a section's core argument cites it / it provides a key number / its methodology is borrowed) must be downloaded in full to `pdfs/`, numbered uniformly `<n> <institution> <title>.pdf`, then summarised with pypdf before deciding how to cite.
4. **Pull time-lock numbers live in step 4**: time-lock snapshot numbers like prices / valuations / yields / central-bank policy rates are **not** taken from second-hand paraphrase in step 2 — pull them live with the `financial-data-sources` skill just before citing in the step 4 draft.
5. **Public social provenance**: public X / LinkedIn / Substack / community posts are lead-generation and sentiment texture, not primary evidence. Record query, capture date, URL / post ID, author handle, and retrieval tool. Tools such as [TweetClaw](https://github.com/Xquik-dev/tweetclaw) can capture public X/Twitter posts and replies; verify every factual claim against A.1-A.5 or A.7 before using it in the argument.

**"Open the page and download, then judge"**: when scouting data, download at least one representative point of actual data before concluding on availability; do not conclude "data incomplete" from a SERP snippet alone.

**Handling IMF / Cloudflare-blocked PDFs**: put a `_NOTES_<institution>_<title>.md` placeholder in `pdfs/`, stating "direct link blocked by Cloudflare, tried curl and WebFetch" + recording the SERP summary and press-briefing substitutes. When citing in draft.qmd, annotate the footnote inline `^[<institution>, <title> (press briefing), YYYY-MM-DD. URL. Note: direct PDF blocked by Cloudflare, citation from press-briefing paraphrase]`, downgrading the citation to "press briefing" (write "per IMF WEO Apr 2026 (press briefing)" rather than "per IMF WEO Apr 2026 figure X").

**Deliverable**: `research.md` with a 20-30 source ledger (organised by the 6 classes) + `pdfs/` with 5-8 core full-text PDFs.

Proceed to step 3 immediately after landing.

---

### Step 3: plan (no stop)

**Goal**: a one-paragraph outline, plain text, no chart list.

**Structure**:

```markdown
# Outline

**Hypothesis**: <restate the step 1 question>

**BLUF summary** (80-150 words): <conclusion + key numbers + so-what>

**Supporting arguments** (3-5):
1. <argument 1>: <one-line take-away + key number + cited source>
2. <argument 2>: ...
3. <argument 3>: ...

**Caveats / Open questions**:
- <unresolved question 1>
- <unresolved question 2>
```

No "methodology" section. No TOC. No reserved section numbers.

**Self-check**:

- Each supporting argument must have at least 1 source from step 2's `research.md` or `pdfs/`.
- Arguments must not overlap.
- A Caveat section must exist (even one item), making unresolved uncertainty explicit.

Proceed to step 4 immediately after landing.

---

### Step 4: draft (no stop)

**Goal**: write the full 4-5 page draft in one pass.

**Structure**:

```markdown
---
title: "<title, derived from hypothesis.md>"
author: "<author string read from ~/.claude/CLAUDE.md at onboarding, e.g. 'Ligen'>"
date: today                # Quarto built-in keyword, auto-fills today's date on render
---

# Executive Summary

<BLUF single paragraph, 80-150 words. Conclusion + key numbers + so-what. No bullets.>

# <First section title, state the point directly, do not write "Background">

<body>

# <Second section title>

<body>

...

# Bottom Line

<restate the conclusion + next-step recommendation for the decision-maker>
```

**Do not write a `format:` block in the template** — `_quarto.yml` already fully defines the pdf / docx formats and include-in-header. A draft.qmd that rewrites the format block usually deep-merges OK in Quarto, but at nested-field boundaries it can drop the `_quarto.yml` include-in-header settings, reverting title size / paragraph spacing / CJK font to Quarto defaults.

**`{.unnumbered}` is not needed** — `_quarto.yml` already has `number-sections: false`, so the whole document is unnumbered; adding `{.unnumbered}` is redundant and easily over-propagated.

**Writing discipline** (inherits all of heavy §7.1; not repeated here — see §4 "Writing standards"):

- Style: declarative, compact, expert audience, **no explainer background**.
- Punctuation: no em-dash `——`, sparse Chinese colons, uniform Chinese corner quotes 「」, no emoji.
- Citation: inline footnote `^[institution, title, YYYY-MM-DD. URL.]`, **no references.bib**.
- Write "percentage points" instead of "ppts".
- No technical symbols as conjunctions (`→ + / vs`).
- No lyrical padding ("actually / in fact / it is worth noting / as is well known").
- No meta-language ("this study does not", "this section will", "this study is designed for...").

**Live-pull discipline for time-lock numbers**:

Before citing any time-lock snapshot number in the body (stock price / index / yield / valuation multiple / central-bank policy rate / company quarterly data not taken from the 10-K), first pull it once via the `financial-data-sources` skill (FRED / yfinance / SEC EDGAR / AKShare) or the iFinD MCP, and treat the live data as authoritative. Step 2 transmitted numbers are only a sanity-check cross-reference — a difference > 5% must be investigated before deciding which to use.

This is the same spirit as heavy's "pull time-lock numbers live in step 7", except light has no step 7 (no charts), so the live-pull moment moves to just before citing in the draft.

**Executive Summary style (BLUF)**:

- **B**ottom **L**ine **U**p **F**ront: the first sentence is the conclusion.
- Single paragraph, 80-150 words, no bullets (no markdown bullets, but 2-3 complete short sentences within the paragraph can carry the conclusion / numbers / so-what).
- Contains: conclusion + key numbers (1-2 most critical) + so-what (decision implication).
- Bad example: "This paper studies X's Y problem and finds..." (that is academic style, not BLUF).
- Good example (~75 words): "Fed Sept 50bp cut probability < 30%. The current SOFR 3M rate implies a 25bp cut, consistent with Powell's Jackson Hole language. Rate-derivatives long positioning can be paced conservatively over 2-3 weeks."

Proceed to step 5 immediately after landing.

---

### Step 5: self-check (no stop)

**Goal**: 3 critique passes + caveat reconciliation + §6 grep text redlines, finalise.

**3 critique passes** (heavy's 6 compressed to 3 — within 5 pages, cross-section consistency / argument flow / three-way consistency are absent or easy to catch):

1. **Facts and data**: every number, year, person, institution traces to an original source (research.md or pdfs/ or live-pulled data). Time-lock numbers have been live-pulled.
2. **Citation support**: each footnote `^[...]` genuinely supports the statement, no bait-and-switch. URLs reachable, dates noted.
3. **Language standards**: run the full §6 grep self-check list and paste the actual output numbers into the commit message or chat reply.

**Caveat reconciliation**:

Check whether the "Caveats / Open questions" listed in the step 3 outline are all handled explicitly at the end of the draft or in the relevant paragraphs. Close what can be closed (re-run the `verifying` skill once); keep what cannot as a caveat in the final draft.

**Absolutely not allowed**: skipping the §6 grep on the grounds that "light is short, self-check is a formality". Short drafts still get grepped, and the all-clear claim must paste numbers (see §6 grep self-check).

**Fallback path when self-check fails**:

If any §6 grep redline is over threshold (e.g. em-dash ≥ 1, colon/period ratio > 15%, body bold > 2, emoji ≥ 1, lyrical-padding hits):

1. **Back to step 4** to rewrite the specific paragraph that triggered it.
2. Re-render `quarto render draft.qmd`.
3. **Back to step 5** to re-run the full §6 grep list.
4. **Only proceed to step 6 when all pass** — 0 hard stops ≠ 0 self-check gates. light has no user-PDF-review hard-stop gate, so going to step 6 with a failed self-check just dumps the redlines on the user.

Infinite-loop safety net: if the same redline cannot be fixed after 3 consecutive rollbacks, report to the user "self-check item X repeatedly failing, recommend manual intervention" and stop for the user's call.

Proceed to step 6 immediately after landing.

---

### Step 6: freeze (no stop)

**Goal**: PDF freeze + docx derivation.

```bash
quarto render draft.qmd                  # → draft.pdf
quarto render draft.qmd --to docx        # → draft.docx
```

No git-tag requirement (light projects do not enforce version management; tag if you want). No publication-style HTML, no WeChat JPG slicing.

**Completion criteria**:

- Both `draft.pdf` and `draft.docx` are generated.
- Eyeball the PDF: no ctex / xelatex errors, no leftover figure captions (light has no charts; a leftover figure reference is a bug), page count in the 4-6 range (over 7 strong warning, see below).

**Over/under-length handling**:

- **< 4 pages: too thin, backfill content or deepen sub-questions and re-render, do not ship.**
- 4-5 pages: target range, close normally.
- 6 pages: OK.
- 7-9 pages: strong warning "content over light's boundary", suggest trimming the 1-2 weakest arguments; ship if the user accepts the overage.
- 10+ pages: tell the user "the content has reached mini-report scale; re-assess whether to keep trimming on the light path to within 6 pages, or re-trigger in heavy mode for a fresh plan", user decides, AI does not hard-truncate.

---

## 4. Writing standards

### 4.1 Style

- Declarative first, **no explainer background** (expert-audience assumption).
- Short, dense sentences.
- Subject-verb-object structure, few nested clauses.
- Precise numbers (specific number + unit + time point).

### 4.2 Punctuation and characters (equivalent to heavy §7.2; restated here)

- **Never use the em-dash `——`**.
- **The half-width hyphen `-` is only for ranges and compound words** (`30-90%` / `2026-2030` / `single-bar`). Never use `-` as an em-dash substitute.
- **Use Chinese colons `：` sparingly**. Break with a period when you can.
- Use Chinese corner quotes 「」 uniformly.
- **No emoji or special symbols.**

### 4.3 Citation

light does not use references.bib; use inline Pandoc footnotes uniformly:

```markdown
SOFR 3M rate latest 4.51%^[FRED, SOFR 3-Month Term Rate, 2026-05-15. https://fred.stlouisfed.org/series/SOFR3M.], consistent with Powell's language.
```

- Footnote content: `institution, title or field name, YYYY-MM-DD. URL.` (English field names / database series names written plainly, no 《》; Chinese book / report titles get 《》).
- URLs must be reachable (spot-check 3-5 during step 5 self-check).
- Repeat the source if it is cited multiple times; **do not introduce a shared bib key**.

### 4.4 BLUF Executive Summary

See the BLUF style section under §step 4. Key points:

- Single paragraph, 80-150 words.
- Conclusion + key numbers + so-what.
- The first sentence gives the conclusion.

### 4.5 What not to write (light redlines)

- **No methodology section** (no explaining "what method this study uses").
- **No TOC** (_quarto-light.yml defaults to `toc: false`).
- **No section numbering** (`number-sections: false`).
- **No "Background" / "Significance"** academic framing sections.
- **No meta-language** ("this study will", "this section will explore", "this study does not").
- **No charts** (light is plain text by design).

---

## 5. Cross-cutting discipline

### 5.1 Source traceability (non-negotiable)

Every number must trace to an original source (research.md entry / pdfs/ PDF name / live-pulled data series). Mark what cannot be located with ⚠️ or drop it; **do not write it into the conclusion**.

### 5.2 No fabricated numbers (non-negotiable)

"Not publicly available" / "to be verified" beats a plausible guess.

### 5.3 Three-state labelling (non-negotiable)

Fact ("per IMF") / estimate ("per market estimate ~X") / inference ("possibly X") — label the three with distinct wording.

### 5.4 AI output ≠ conclusion (non-negotiable)

The AI provides material and a first draft; the human decides the final conclusion. light's 0 hard stops mean the user "can stop at any time", not that the user blind-signs whatever the AI writes.

### 5.5 verifying-skill call (non-negotiable)

During the step 5 self-check, unresolved caveats must be checked once with the `market-research-skills:verifying` skill. light has no separate 9c verifying sub-step like heavy, but the verifying call itself may not be skipped.

---

## 6. §6 grep self-check text redlines

Before draft v1 is done and before any revision is delivered, grep verification is **mandatory**. Commands use `draft.qmd` as the example.

**Evidence requirement (anti "formality self-check" discipline)**: when claiming the self-check passed, you **must paste the numbers from the last actual grep output**; a verbal "all clear" is not allowed. See the same-named section in heavy workflow §7.4 — light applies the same.

| Redline | Check command | Expected |
|---|---|---|
| Em-dash `——` | `grep -c "——" draft.qmd` | 0 |
| Hand-written section-number prefix in titles | `grep -nE "^#{1,3} (§\|A\.\|[0-9]\|[一二三四五六七八九十]、)" draft.qmd` | 0 lines |
| Emoji | `grep -cP "[\x{1F300}-\x{1F9FF}\x{2600}-\x{27BF}]" draft.qmd` | 0 |
| Unescaped dollar sign `$` (**mandatory for English drafts**; LaTeX treats `$` as a math delimiter, unescaped = render failure) | `grep -nP "(?<!\\\\)\\$" draft.qmd` | 0 (write body dollar amounts as `\$`, e.g. `\$1.5 billion`) |
| h3 and deeper titles (light is h1 + h2 only) | `grep -nE "^#{3,}" draft.qmd` | 0 lines |
| Body bold | `grep -c "\*\*" draft.qmd` | ≤ 2 (lead-in words excepted) |
| Chinese colon `：` to period ratio | total colons `grep -c "：" draft.qmd` over period count `grep -c "。" draft.qmd` | 5-15% (light short drafts have no figsource/tblsource colons, so compute the ratio directly without deducting). English drafts skip this item |
| Lyrical-padding high-frequency words | `grep -nE "实际上\|事实上\|值得指出\|值得注意\|众所周知\|不可否认\|毫无疑问\|需要指出\|客观地讲\|不难看出\|在此背景下\|在这一过程中" draft.qmd` | spot-check and delete on hit |
| h2 empty-title anti-pattern (academic affectation) | `grep -nE "^## .*(关于\|讨论\|探究\|浅析\|思考\|现状与挑战\|视角$)" draft.qmd` | 0 lines |
| Half-width `-` as em-dash | `grep -nE " - " draft.qmd` | spot-check; legal use is only ranges and English compounds |
| Technical symbols as conjunctions | `grep -nE "→\|∴" draft.qmd` + spot-check `+` `/` `vs` | replace with full written expressions |
| Academic / colloquial tone | `grep -nE "使得\|进行了\|做出了\|具有重要意义\|一定程度上\|综上所述\|总而言之" draft.qmd` | replace per the lookup table on hit |
| Vague quantifiers (no number support) | `grep -nE "很大程度上\|相对较高\|相对较低\|大致\|大约\|一些\|部分" draft.qmd` | spot-check; delete or replace with concrete numbers if unsupported |
| meta-language / meta-commands | `grep -nE "本研究不\|本章不\|本研究将\|本研究为.*而设\|本章构造\|研究边界明确\|需要明示\|本节将\|本章将\|本节强调\|本章强调" draft.qmd` | 0 lines (light has no "chapter"/"section" concept; rewrite on hit) |
| Page count | eyeball after rendering PDF | 4-5 target, < 4 too thin needs backfill, 6 OK, 7-9 strong warning + suggest trimming, 10+ user decides whether to keep trimming or move to heavy |
| Quarto render | `quarto render draft.qmd` | success, no mathtext / dimension errors |

**Versus heavy §7.4**: light drops 5 chart / publication / bib-related redlines (`_quarto.yml` lof / lot alignment, unreferenced fig/tbl labels, framing-section second rewrite, bib fields, figsource/tblsource colon deduction). The other 12 are kept.

---

## 7. Boundary with heavy mode

Do not mix them up. The table draws the clean line:

| Dimension | light | heavy |
|---|---|---|
| Steps | 6 | 11 |
| Time budget | ~15 min | >1 h |
| Length | 4-5 pages / 2500-3000 chars | 30-40 pages / 15k+ words |
| Charts | 0 | usually 25+, one script per chart |
| Citation | inline footnote | references.bib |
| LLM | single LLM only | single / multi-LLM optional |
| Hard stops | 0 | 3 (outline / draft / final) |
| Derivations | PDF + Word | PDF + Word + HTML + WeChat |
| Retrospective | none | mandatory (§11.2 audit) |
| _state.md | none | mandatory |
| Directory structure | flat + pdfs/ single subfolder | 10 numbered subdirs |
| Summary form | BLUF single paragraph | three-part (with keyword line) |
| Audience | expert / decision-maker | dual (expert + non-specialist) |
| TOC / numbering | none | yes |
| Upgrade path | none (re-run heavy) | n/a |

**Trigger examples**:

| User phrasing | skill |
|---|---|
| "Write me a 5-page memo on whether the Fed cuts in September" | light |
| "Do a deep study of US AI-bubble risk" | heavy |
| "Get me a brief for the boss within the hour" | light |
| "Write a long WeChat piece on Saudi Vision 2030" | heavy |
| "Quick analysis of recent Middle East sovereign-fund holdings" | light |
| "Industry report: the full China battery supply chain" | heavy |

When unsure, **default to light** — being short is the short draft's biggest advantage; if it turns out too thin, upgrading (re-running heavy) is cheap, whereas running heavy and finding the topic only supports 5 pages is awkward.
