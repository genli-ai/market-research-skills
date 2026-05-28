# analyst-research · medium mode workflow

> English is the authoritative version; the Chinese mirror is `workflow_medium.zh.md`.
> Writing-standard examples that illustrate Chinese-prose redlines are kept in Chinese (they apply when the report language is Chinese); the surrounding rules are in English and apply to both languages unless noted.

Scope: 12-15 page topic analysis, 6-10 charts, half-day budget (3-5 h), single LLM, 1 hard stop (step 7 user sign-off, mandatory), optional second hard stop (after the step 2 broad search, decided by the user at onboarding).

light and heavy are sibling modes of the same skill, handling decision memos within 5 pages and 15k-word+ long-form reports respectively. All three share the hypothesis-lock starting point; downstream each mode is self-governing.

---

## 1. New-project onboarding

### Step 0: announce

Briefly confirm: "I have read the medium mode `references/workflow_medium.md` and `report_style_spec.md`, and am ready to start the 8-step flow."

### Step 1: onboarding questions (5 at once, lock and do not re-ask)

**Q1 · Research question or hypothesis (one sentence)**: the user gives the specific question.

**Q2 · Target audience**:

- expert / decision-maker (aligned with light, no explainer background)
- dual (undergraduate-educated non-specialist + professional reader, with necessary term explanations woven in, aligned with heavy)
- other (user describes)

**Q3 · Hard stop after the step 2 broad search?**

- No (default): after the broad search the AI goes straight to step 3 outline and only stops at step 7 sign-off. Fits a clear topic where the user trusts the AI's source selection.
- Yes: after the broad search the AI produces `2_research/research.md` and stops for the user to review the ledger, then proceeds to step 3 after confirmation / gap-filling. Fits a topic that might drift, where the user wants early control over source direction.

**Q4 · Palette / fonts**: default to the FT blue palette and Songti SC / Times New Roman per `report_style_spec.md §5.3 / §5.4`; if the project wants different values, the user says so now and the AI records them in the project `CLAUDE.md` "charts / project-confirmed values" section.

**Q5 · Report language**: English (default) / Chinese / other. If unspecified, write the draft in English (see SKILL.md "Language policy"), lock it into CLAUDE.md. English drafts skip the Chinese colon redline and enforce the unescaped-`$` redline (write amounts as `\$`).

**Items NOT asked** (locked by default):

- Output form: PDF (main) + Word docx (derivation). **No HTML, no WeChat JPG, no slides.**
- Length: 12-15 page target (**< 12 pages is too thin; backfill content or deepen charts, do not ship**; 6-7 pages strong warning + suggest moving to light; 16-20 pages strong warning + suggest trimming; 20+ pages re-assess medium / heavy).
- Charts: 6-10, **charts first** (build charts before writing the body, per heavy step 7 discipline).
- LLM: single LLM only (Claude solo throughout), no multi-LLM critique.
- Summary form: default "three-part summary" (conclusion + key numbers + so-what). The user can ask for a single BLUF paragraph.
- Time expectation: 3-5 hours, single / dual session.
- Author byline / email: read the default from the global `~/.claude/CLAUDE.md` "author byline" section; ask explicitly only if absent.

### Step 2: scaffold

With cwd at the project root, run:

```bash
mkdir -p 1_topic 2_research/pdfs 2_research/_process \
         3_outline 4_data/1_raw 4_data/2_processed \
         5_scripts 6_figures 7_draft && \
cp ~/.claude/skills/analyst-research/references/_quarto-medium.yml _quarto.yml && \
touch _state.md CLAUDE.md
```

7 numbered subdirs (1_topic to 7_draft), **dropping `8_publication/` and `9_retrospective/`** (medium does no long-form derivation or per-section retrospective). `pdfs/` and `_process/` are subdirs of `2_research/` for full-text documents and raw process drafts.

`5_scripts/_path.py` (template):

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "4_data" / "1_raw"
DATA_PROC = PROJECT_ROOT / "4_data" / "2_processed"
FIGURES = PROJECT_ROOT / "6_figures"

# Point this at the analyst-research scripts/ folder (plugin install or dev clone)
SKILL_SCRIPTS = Path.home() / ".claude" / "skills" / "analyst-research" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

import chart_template
chart_template.FIGURES = FIGURES
```

`.claude/settings.json` project-level permissions (same as heavy / light, checked into git):

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

### Step 3: write the first CLAUDE.md + _state.md, launch step 1

The `CLAUDE.md` template contains: project direction, target audience, output form, deviations from the framework (initially empty). The `_state.md` template is in §10.

Write the step 1 hypothesis into the `1_topic/topic.md` draft (one-paragraph research question + key constraints). Soft-stop into step 1 and tell the user.

---

## 2. The 8-step skeleton

| Step | Name | Stop | Time budget | Heavy correspondence |
|---|---|---|---|---|
| 1 | topic + thesis | soft | 15 min | merges heavy 1+3, drops heavy 4 topic hard stop |
| 2 | broad search (cover 4+ classes, ~15 sources) | soft / **optional user hard stop** | 45 min | inherits all of heavy 2 + appendix A, compressed scale |
| 3 | outline draft (h1 + h2 + chart list) | soft | 20 min | heavy 6 trimmed |
| 4 | data + 6-10 charts (one script per chart, double-landing, 4-item visual self-check) | soft | 60-90 min | **inherits all heavy 7 discipline**, fewer charts |
| 5 | draft in one pass, 12-15 pages | soft | 45-60 min | heavy 8 default path |
| 6 | self-critique + verifying (one pass in single LLM, calls `market-research-skills:verifying`) | soft | 20 min | heavy 9b + 9c merged/trimmed |
| 7 | user sign-off (user reads v1 PDF, gives feedback, iterates) | **hard** | user's pace | heavy 9d |
| 8 | finalise + Word derivation (quarto render + pandoc qmd→docx) | soft | 10 min | heavy 10 trimmed, drops HTML / WeChat |

**0 hard stops ≠ 0 self-check gates**. After each step lands, the AI briefly tells the user the stage output; **soft stops auto-proceed**. Step 7 is the only mandatory hard stop. Whether step 2 is a hard stop is decided by the user at onboarding Q3. The user can stop, redirect, or roll back at any time.

Heavy steps dropped: 3 (AI suggests directions) / 4 (topic hard stop) / 5 (supplementary search, merged into step 2) / 9a (DS polish) / 9b–9c split / 10c (HTML derivation) / 10d (WeChat derivation) / 11 (per-section retrospective).

---

## 3. Step details

### Step 1: topic + thesis (soft stop)

**Key question**: is the user's direction clear? Can the AI give a defensible research thesis in one pass?

**Operations**:

1. After the user gives the hypothesis at onboarding Q1, the AI writes `1_topic/topic.md` directly:
   ```markdown
   # Title
   <one sentence>

   # Research question
   <one paragraph, 2-3 sentences>

   # Key constraints
   - Time-lock: <YYYY-MM-DD snapshot>
   - Target audience: <expert / dual>
   - Output form: PDF + Word, 12-15 pages, 6-10 charts
   - Report language: <English (default) / Chinese / other>
   - Sub-questions to cover (3-5):
     - ...

   # Research thesis (AI proposes a version)
   <chapter skeleton by sub-question, 4-6 h1. Only h1 coarse outline; h2 refinement left to step 3 outline.>
   ```

2. **Vague-hypothesis nudge**: if the hypothesis is vague (scope / time-lock / sub-topic boundary unclear), the AI **states its own assumptions in the "Key constraints" section** and tells the user "proceeding on these assumptions, stop me to correct". **Do not stop to wait for confirmation.** Under the soft-stop design, transparent assumptions replace hard stops.

3. **Chapter skeleton**: the report body has two levels only (h1 + h2), **no h3** (see `report_style_spec.md §1.2`). At step 1 list only the h1 coarse outline.

**Soft stop**: after `topic.md` lands, tell the user "topic and thesis draft landed, 5 h1 chapters, proceeding to step 2 broad search on this basis". Auto-proceed to step 2 without waiting.

**Forbidden**: do not offer multiple candidate directions for the user to choose at step 1 (that is heavy's step 3). medium assumes the topic is formed at onboarding and the AI advances one thesis in a single pass.

---

### Step 2: broad search (soft stop, optional user hard stop)

**Key question**: what data and material **already exist** around the topic?

**Goal**: fix the topic direction (quantity first, coverage first). Scale compressed to ~15 sources (heavy is usually 30-50).

**Operations**: Claude solo walks through the source classes below, using the iFinD MCP or `financial-data-sources` skill for data. Claude synthesises into `2_research/research.md`.

**Key discipline: source coverage (7 classes, at least 4 mandatory)**

The AI must **proactively search the following 7 source classes**, hitting at least 4 (heavy covers all 7; medium 4, by topic / audience context):

| Class | Examples |
|---|---|
| A.1 international organisations | IMF, World Bank, IEA, OECD, BIS, UN, regional development banks |
| A.2 sovereign / government / central bank | central banks, statistics offices, finance ministries, sovereign funds, sector regulators |
| A.3 academic & think tank | NBER, SSRN, Google Scholar, Brookings, CSIS, Chatham House |
| A.4 investment banks + consulting | GS / JPM / MS / Citi Country Outlooks, McKinsey / BCG sector reports |
| A.5 mainstream financial media | Chinese: Caixin, Wallstreetcn, FT Chinese; English: Bloomberg, Reuters, FT, WSJ, Economist |
| A.6 WeChat / industry communities | finance / regional / vertical Chinese public accounts |
| A.7 databases (programmatic) | available MCP / API / skill: iFinD, `financial-data-sources` skill (FRED / yfinance / SEC EDGAR / AKShare) |

**Class-selection guide**:

- Pure macro topics usually A.1 + A.2 + A.5 + A.7
- Company topics usually A.2 + A.4 + A.5 + A.7
- Policy topics usually A.1 + A.2 + A.3 + A.5
- Regional topics usually A.2 + A.5 + A.6 + A.7

**Both languages**: international orgs, investment banks, academia are mostly English; regional, policy, primary news are often more accurate in Chinese.

**Key discipline: "open the page and download, then judge"**

When scouting data, **download at least one representative point of actual data before judging availability**; do not conclude "data incomplete" from a SERP snippet / impression / site description alone.

**Key discipline: download core PDFs in full**

Documents with a **structural argumentative role** must be downloaded in full to `2_research/pdfs/`, numbered uniformly `<n> <institution> <title>.pdf`, then **summarised first with pypdf** (structured extraction of title, sections, tables is more robust). If pypdf parsing fails, fall back to the Read tool's `pages` parameter for page-limited reads.

Criteria for "structural argumentative role" (any one triggers):
- a section's core argument cites it
- it provides a key number
- its methodology is borrowed or contrasted by this project

medium's core PDF count is ~3-5 (heavy usually 10-15).

**Key discipline: handling IMF / Cloudflare-blocked PDFs**

Direct links from IMF eLibrary, BIS WPs, ECB papers are often blocked by Cloudflare (returns a 462-byte HTML redirect). Standard moves:

1. **NOTES placeholder**: `2_research/pdfs/_NOTES_<institution>_<title>.md` stating "direct link blocked by Cloudflare, tried curl and WebFetch" + recording the SERP summary and press-briefing substitute.
2. **Downgrade citation**: write "per IMF WEO Apr 2026 (press briefing)" to flag second-hand paraphrase, not "per IMF WEO Apr 2026 figure X".
3. **Flag for user**: add `⚠️ user to download manually` to the importance field of that `research.md` entry; give the user the list to fill before step 7 sign-off.

**Key discipline: user-supplied material takes priority**

The user may drop material into `2_research/pdfs/` at any time. These files **rank above the AI's own search results**:

- the AI must proactively **read them in full** (Read full text, not just summary / TOC)
- mark "source: user-supplied" in `research.md`, importance defaults to "core"
- if user material conflicts with the AI's findings, **the user material wins**

**Deliverables**:

- `2_research/research.md`: ~15-source ledger (organised by 4-7 classes), each recording type / institution / title / year / URL / key number / importance / acquisition method
- `2_research/pdfs/`: 3-5 core full-text PDFs
- `2_research/_process/`: raw search records (if multiple query rounds)

**Soft / hard stop**:

- onboarding Q3 = No (default): after landing, tell the user "broad search done, ~15 sources covering X classes. Proceeding to step 3 outline", auto-proceed.
- onboarding Q3 = Yes: **hard stop** for the user to review the `research.md` ledger; proceed to step 3 after confirmation / gap-filling.

**Pitfall warnings**:

- A single LLM's key judgement must be cross-checked against another source class (e.g. IMF estimate vs official sovereign disclosure) before becoming a conclusion. **A single source is not enough.**
- Be cautious concluding "not found"; the search terms may be wrong, try another keyword set or two.

---

### Step 3: outline draft (soft stop)

**Key question**: based on the full source library, what does the detailed outline look like?

**Operations**:

1. Write `3_outline/outline.md` based on the step 2 library.
2. **Chapter skeleton**: h1 / h2 titles are themselves conclusive (not "Fiscal view", but "Fiscal view: the three-tier 30%-90% oil-and-gas share of fiscal revenue"). The body has two levels only, **no h3**.
3. **Each section lists**:
   - research sub-question (one sentence)
   - core take-away (one sentence)
   - planned charts (specific figure number, underlying data source)
   - key citations (specific document name + page)
4. **Mandatory paragraphs**: "what we do not do" + "uncertainty boundary" (data gaps, caliper limits, commercial-information risk, etc.).

**Chart-list generation**: Claude proposes a chart list from the library (which charts in each section support the argument), targeting **6-10**, **pre-screened against the step 4 "6 add-figure criteria"**.

**Link between outline and step 4 add/remove-figure criteria**:

- when listing charts, each is already screened against the add-figure criteria
- before step 4 commit, each passes the remove-figure criteria; remove on trigger
- any chart-list change (a chart found necessary during step 4) must **go back to step 3 to sync the outline**; do not let body and outline drift

**Outline-as-contract (the floor anchor)**: the outline's section count + chart list are the contract that the step 5 draft and step 8 finalise are measured against. Two checks: (1) if the planned outline cannot plausibly reach 12-15 pages / 6-10 charts, it is too thin — deepen it **before** `git tag outline-final`, do not lock a thin contract and discover the shortfall at step 8; (2) the signed counts become the §6 count-gate floor — a final draft with fewer charts than the contract is a breach (restore them, or tell the user which planned item was dropped and why). Silent shrinkage is the classic laziness failure mode.

**Outline version numbers**:

- **v1**: step 3 first draft lands, soft stop, auto-proceed to step 4
- **v2 / v3 / ...**: revisions after step 3 ↔ step 4 bidirectional iteration (charts reveal caliper conflicts, new argument angles, etc., go back to step 3)
- **final**: after all step 4 charts land, the outline final forms, the AI auto-tags `git tag outline-final`, auto-proceeds to step 5

**Soft stop**: after `outline.md` v1 lands, tell the user "outline draft landed, N charts listed. Proceeding to step 4 to complete charts", auto-proceed. The user can stop to review the outline at any time.

---

### Step 4: data + 6-10 charts (soft stop)

**Key question**: build all charts first and see whether the argument stands.

**Why charts first**: building charts before writing is a diamond-grade field insight. A project once wrote the outline and body "Country X policy target 65%" first, only to find during charting that the number did not correspond to that metric at all. Building charts first exposes incomparable-caliper problems immediately.

**Operating flow**:

0. **Pre-flight: chart_template self-test**. Before the first chart, run the chart_template self-test, producing a dummy chart with a `$` dollar amount / multiple plot elements / a horizontal bar / a legend to `/tmp/`, and eyeball: (1) does `$xxx` show a literal backslash (chart_template `_wrap_text_precise` should have a parse_math guard); (2) is the annotation colour swallowed by a same-colour plot; (3) is a long y-tick label clipped. On any trigger, **fix the global chart_template first, then draw real charts**.

1. **Data landing**: raw downloads to `4_data/1_raw/`, processed versions to `4_data/2_processed/`, named `<section>_<topic>.csv`.
2. **Script landing**: **one script per chart** (see `report_style_spec.md §3.1`), named `make_fig_<section>_<n>_<topic>.py`, head docstring stating purpose / input / output. **Each script draws one plot; no side-by-side subplots** (spec §3.7). Script top `import _path` + `from chart_template import ...`.
3. **Chart generation**: each chart outputs PDF + JPG to `6_figures/` (**medium drops `_clean.jpg`** via `save_fig(..., clean=False)`; no publication HTML so no third raster needed), named `fig_<section>_<n>_<topic>.{pdf,jpg}`. `save_fig` takes `title / source / note`: bare PDF (Quarto caption provides these); self-contained burn-in JPG. JPG long edge ≤ 2000px (spec §3.11).
4. **Backfill outline**: after each chart, backfill into the matching section of `3_outline/outline.md` (embed `![]` + caption + a one-line figure-note preview).
5. **Cross-check**: does the chart's conclusion match the outline draft's take-away? If not, go back and fix the outline.

**Key discipline: double-landing**

For any chart / table involving data processing, **the underlying data + the full script must both land** (reproducible). Keep the source even if the chart is simple.

**Key discipline: judge before charting (add and remove criteria)**

No upper/lower bound on chart count. The only reason a chart exists is "text and tables cannot, or inefficiently, express a specific reading". Each chart must answer the test: **without this chart, could the reader understand the passage equally efficiently?** If yes, do not chart; only chart if no.

**Add-figure criteria** (run per section when writing the body; any one triggers):

| Situation | Why text fails |
|---|---|
| **Multi-source comparison**: same metric, 3+ sources side by side | text listing is messy, the reader has to compute the comparison |
| **Time variation**: 5+ year trend, inflection, rhythm | endpoint numbers in text do not show the shape |
| **Cross-dimension comparison**: 2D or multi-D (country × sector, year × metric) | text description loses structure |
| **Magnitude or distribution**: shape, extremes, quartiles | text gives statistics but loses shape |
| **Target vs actual**: two data sets compared visually | a table works but visual comparison is faster |
| **Spatial or process relation**: geography, network, flowchart | the reader cannot reconstruct it from text |

**Remove-figure criteria** (run per chart before commit; any one triggers):

| Anti-pattern | Why not |
|---|---|
| Single-number statement ("metric X = Y%") | one sentence says it |
| 2-3 simple shares ("A 60%, B 40%") | a pie equals text, text is tighter |
| Multiple slices of the same dataset in one section | merge or keep the strongest |
| Trend statement with no specific node numbers | no "what happened in which year", the chart has no anchor |
| Conclusion, bridging, intro, closing paragraphs | these do not anchor data |

**Step 4 "all-or-nothing" principle**:

The N charts listed in the step 3 outline are each screened against the add criteria; **step 4 must complete all N before step 5**. No "do K representative charts, push the rest to step 5 inline text". If a chart triggers the remove criteria during step 4, the **compliant removal path** is: a standalone commit removing the chart + the same commit updating the outline + the same commit inlining that chart's numbers and argument into the body.

**Key discipline: time-lock snapshot numbers must be pulled live in step 4**

For any time-lock snapshot number (prices, valuations, cash flows, central-bank policy rates), **pull it live once via the `financial-data-sources` skill or iFinD MCP before charting in step 4**, and treat the live data as authoritative. Step 2 transmitted numbers are only a sanity-check cross-reference. A difference > 5% must be investigated before deciding.

| Is a time-lock snapshot | Is not |
|---|---|
| stock price, index, FX, yield (current snapshot) | historical fixed value (e.g. "2000 NASDAQ peak 5048") |
| P/E, P/B, CAPE (current snapshot) | company fiscal-year data disclosed in the annual report (10-K primary) |
| central-bank policy rate (current + recent path) | regression coefficients / elasticity estimates from academic papers |
| company fiscal disclosure not taken from the 10-K | key numbers from a downloaded PDF |

**Key discipline: derive title / source / note strings from CSV, do not hardcode numbers**

When `title` cites a specific number (e.g. "fiscal deficit \$32B"), the script **computes max / min / argmax on the spot and f-string-inserts it**, not hardcode. E.g. `title=f"private female +{df.loc['private_female_growth'].max():.0%}"`, not `title="private female +84%"`.

**fail-safe**: add an `assert` at the script top checking that the number cited in title matches the CSV computation; no commit if it disagrees.

**Key discipline: source / note strings "edit one, reconcile all 3"** (medium drops the references.bib location)

The same chart's source / note string exists in **3 places** (heavy has 4; medium drops the bib one):

1. the `save_fig(source=..., note=...)` parameters in `make_fig_*.py` (for the self-contained JPG)
2. the `\begin{figsource}` block after the matching `![](fig.pdf)` in `draft.qmd` (for the report PDF, spec §3.3)
3. the narrative source / time / caliper where the body cites the chart

**Any edit to one must reconcile all 3.**

**Key discipline: AI does logic self-check before commit, leaves visual self-check to the user**

Per spec §4, "the AI does not do visual checks". Before step 4 commit the AI does only a **logic-consistency self-check** per `report_style_spec.md §3.13 4-item chart-script self-check` (title number matches in-chart data, annotation colour not same as the plot below it, horizontal-bar y-tick labels fully shown, legend centered and laid out horizontally); any chart that fails must have its script fixed and re-rendered before commit. The visual self-check itself is left to the user reading the PDF at step 7.

**Soft stop plus four quality gates**: after all charts land, tell the user; the user can review the JPGs and give feedback at any time, default non-blocking into step 5. The four gates the AI self-checks:

1. **all outline-listed charts are complete, or removed from the outline via the compliant removal path** (no "to be filled" / "phased" pushed to step 5)
2. spec §3.13 4-item chart-script logic self-check all pass
3. each drawn chart passes the add criteria and does not trigger the remove criteria
4. any issue exposed in self-check is fixed and re-rendered

**Concrete check for gate 1**: grep all fig numbers listed in `3_outline/outline.md`, compare against the PDF filenames actually produced in `6_figures/`; **the count and numbering must correspond one-to-one on both sides.**

**Pitfall warnings**:

- For cross-country / cross-source comparison, explicitly record caliper differences. A 20+ percentage-point gap for one country under two calipers is common.
- Do not force incomparable-caliper metrics onto one "target vs actual" chart; it misleads the reader.
- When citing an institution's KPI, open the official site to confirm.

---

### Step 5: draft in one pass (soft stop)

**Key question**: organise charts and documents into report language.

**Lead**: Claude solo throughout (first draft + self-polish + format / render tuning). critique is left to step 6.

**Writing discipline**: when Claude writes, **follow §5 writing standards strictly**, targeting a step 5 final quality equal to third-party-edited prose.

**Default: one continuous draft**: Claude writes all chapters in outline order, then **auto-proceeds to step 6 self-critique** after the full v1. The rationale is that the outline is final after step 3 + step 4 bidirectional iteration, take-aways are locked, per-section stop-and-review costs far exceed the value, and fatal errors are caught by step 6 self-critique and step 7 sign-off.

**fallback: per-section hard stop** (enabled on explicit user request). Stop after each section for user review before writing the next. Fits: outline not fully locked, user wants deep involvement in each section's argument-flow calibration.

**Operating order**:

1. Claude writes the first draft per section (v1.0), **self-checking §5 discipline per section** (period continuation / list colon / embedded take-away / "ppts" → "percentage points" / written connectives / numbered lead-ins / no technical symbols as conjunctions). Also a **per-section depth check against the outline contract**: each section carries its planned chart(s) and is more than a 1-2-paragraph gloss; a section thinner than its contract take-away goes back to step 2 / 4 for material, it is not padded with filler.
2. Once a section passes self-check, write the next immediately (default one continuous pass).
3. After the full v1.0, do render / font / YAML tuning (v1.1 → v1.x); the body does not change.
4. The step 5 final = Claude's pure version, **snapshot to `7_draft/_process/draft_v1_claude.qmd`** (this must land before step 6 changes text, or there is no "pure Claude baseline" to revert to).
5. Auto-proceed to step 6.

**Pre-writing self-check list**: when each section's v1 is done, run the lightweight subset (em-dash, emoji, meta-language, lyrical padding) + the "chart-script / CSV / body three-way consistency" check; after the full v1, run the full §6 list.

**The "chart-script / CSV / body three-way consistency" check**: when a section cites a chart, verify item by item:

1. Is the body number actually in the CSV?
2. Do title / source / note in `make_fig_*.py` also write those two numbers? If so, are they consistent?
3. Does the rendered fig PDF (open the JPG) show axis values / data labels that match?

If anything disagrees, **fix it in that section**, do not defer it to step 6 self-critique.

**Draft structure template**:

```markdown
---
title: "<title, derived from 1_topic/topic.md>"
author: "<author string read from ~/.claude/CLAUDE.md at onboarding>"
date: today
---

# Abstract

<three-part: (1) conclusion (2) key numbers (3) so-what. Default three parts; switch to a single BLUF paragraph if the user asks>

# <First section title, conclusive phrasing>

<body...>

# <Second section title>

...

# Conclusion

<pull the conclusion + decision implication + open questions>
```

**Do not write a `format:` block in the template**. `_quarto.yml` already fully defines the PDF / docx formats and include-in-header; a draft.qmd that rewrites the format block may revert some settings to Quarto defaults.

`{.unnumbered}` is not needed. `_quarto.yml` already has `number-sections: true`, so the whole document is auto-numbered.

**Process-draft landing**: step 5 minor versions (v1.0 / v1.1 / …) iterate in place in `draft.qmd`; major versions (v1 final → v2 → v3) land under `7_draft/_process/draft_<vX>_<who>.qmd`. **`draft.qmd` always points to "the current shippable latest version".**

**Soft stop**: after v1 lands and renders successfully, tell the user "draft v1 done, ~X pages, proceeding to step 6 self-critique + verifying", auto-proceed to step 6.

---

### Step 6: self-critique + verifying (soft stop)

**Key question**: does the full draft hold up? Are all caveats reconciled?

**Lead**: Claude self-critique (single LLM, no external GPT critique).

**Sub-steps in series**:

#### 6a · self-critique (6 perspectives, lands `7_draft/_process/critique_self.md`)

Self-evaluate draft v1 against these 6 perspectives:

1. **Facts and data**: every number, year, person, institution traces to an original source (research.md / pdfs/ / live-pulled data). time-lock numbers live-pulled.
2. **Caliper analysis**: are cross-country / cross-source / cross-time numbers caliper-consistent? Are caliper differences flagged explicitly?
3. **Citation support**: each footnote `^[...]` genuinely supports the statement, no bait-and-switch. URLs reachable, dates noted.
4. **Cross-section consistency**: same number across sections, values consistent? caliper consistent?
5. **Argument flow**: does each section's take-away follow the outline? Do sections connect smoothly?
6. **Language standards**: run the full §6 grep self-check list.

The self-critique output lands in `7_draft/_process/critique_self.md`, recording issues by the 6 categories, each with: location / issue / fix suggestion / priority (fatal / serious / minor).

Integration: fatal + serious are all fixed, minor as time permits. Revisions land in minor versions v1.1 / v1.2.

#### 6b · verifying (call the `market-research-skills:verifying` skill)

For the step 3 outline's "uncertainty boundary" + the doubts caught by self-critique, call the `verifying` skill to check rigorously. Close what can be closed; keep what cannot as a caveat in the final draft.

**verifying-skill call discipline (non-negotiable)**: medium has no separate 9c verifying sub-step like heavy, but the verifying call itself may not be skipped.

#### 6c · integrate into v2, proceed to step 7

After integrating self-critique and verifying revisions into `7_draft/draft.qmd` v2, **render successfully** (quarto render no errors), **§6 grep self-check all pass**.

After landing, tell the user "draft v2 done (critique fixes X / verifying closed Y doubts / Z caveats retained), proceeding to step 7 sign-off", auto-proceed to step 7.

---

### Step 7: user sign-off (**hard stop**)

**Key question**: does the user finally accept it?

**Hard-stop criterion**: the user must explicitly sign off before step 8.

**Operations**:

1. The AI hands the user the v2 PDF and critique_self.md together.
2. The user reads the PDF and gives feedback.
3. The AI iterates until the user signs off (v2.1 / v2.2 / ... minor versions land in `7_draft/_process/`).
4. After sign-off, proceed to step 8.

**What the user reviews**:

- **Visual self-check** (spec §4 says the AI does not do visual checks): chart font size, fonts, palette, annotation position, long-label truncation.
- **Final fact check**: the user knows the domain and may catch fact errors the AI missed.
- **Final argument-flow judgement**: do the take-aways hold, does the so-what persuade the user.
- **Caveat completeness**: is unresolved uncertainty adequately disclosed.

**User rollback paths**: the user can send the AI back to step 5 (rewrite a section), step 4 (redo a chart), step 3 (change the outline), step 2 (more searching) at any time. After sign-off it is the final draft; proceed to step 8 render derivation.

---

### Step 8: finalise + Word derivation (soft stop)

**Key question**: both PDF and Word generated, eyeball-clean?

**Operations**:

```bash
quarto render draft.qmd                    # → 7_draft/draft.pdf
quarto render draft.qmd --to docx          # → 7_draft/draft.docx
git tag v1.0                                # tag the final
```

**Completion criteria**:

- Both `draft.pdf` and `draft.docx` are generated.
- Eyeball the PDF: no ctex / xelatex errors, no leftover figure captions, page count in the 12-15 target range (8-11 backfill, see Length handling below; run the §6 count-gate and paste the actual page / chart numbers).
- Eyeball the Word: figures embedded correctly, footnotes converted correctly (Quarto's Pandoc-footnote-to-Word-endnote handling needs an eyeball check).

**Length handling**:

- 12-15 pages: target range, close normally.
- 8-11 pages: thin, backfill content or deepen charts and re-render (chart-list target 6-10).
- 6-7 pages: strong warning "content thin, suggest moving to light".
- 16-20 pages: strong warning "content thick, suggest trimming the 1-2 weakest sections".
- 20+ pages: tell the user "content has reached heavy scale; re-assess whether to keep trimming on the medium path to within 15 pages, or re-trigger in heavy mode for a fresh plan", user decides, AI does not hard-truncate.

**Completion message**: "draft v1.0 final, PDF and Word generated, X pages + Y charts. git tag v1.0 set. For further revisions, continue v1.1 / v1.2 iteration."

---

## 4. Document & chart standards

medium and heavy share one visual spec (file at `~/.claude/skills/analyst-research/references/report_style_spec.md`):

- document layout: §1
- chart design principles: §2
- chart production rules: §3 (**key: §3.1 one script per chart, §3.7 no side-by-side subplots, §3.11 JPG long edge ≤ 2000px, §3.13 4-item chart-script self-check**)
- AI does not do visual checks: §4
- default YAML / fonts / palette: §5 (**palette §5.3, fonts §5.4**)
- chart_template interface contract: §6

**Two medium-vs-heavy deviations from the spec**:

1. **No `_clean.jpg`**: medium drops publication HTML and WeChat derivation; call `save_fig(..., clean=False)` to skip the `_clean.jpg` raster, outputting PDF + JPG only. (Note: `clean` defaults to True; medium scripts must pass `clean=False` explicitly, else a harmless but unused `_clean.jpg` is still produced.)
2. **No references.bib + csl**: medium uses inline footnotes `^[source, title, YYYY-MM-DD. URL.]`; the spec §3.3 "figsource block + bib `[@cite]` citation" is simplified to "figsource block + footnote".

Record both deviations in the project `CLAUDE.md` "deviations from the framework" section, not in the spec file itself (the spec is the SoT; medium and heavy each deviate per project as needed).

---

## 5. Writing standards

> The examples below illustrate Chinese-prose redlines (they apply when the report is Chinese); the rules apply to both languages. For English reports, apply the spirit (period continuation, no padding, no body bold) with English idiom and skip the Chinese-colon items.

### 5.1 Style

- **Declarative first**, target audience locked at onboarding Q2 (expert / dual). Under the expert assumption, **no explainer background**; for dual audience, briefly gloss a term on first use.
- Short, dense sentences.
- Subject-verb-object structure, few nested clauses.
- Precise numbers (specific number + unit + time point).

**Period continuation** (continue the same theme with periods, not commas / semicolons):

- ❌ 「沙特财政赤字 2024 年达 \$32B，主要受油价下跌影响，预计 2025 年扩大至 \$45B」
- ✅ 「沙特财政赤字 2024 年达 \$32B。主因油价下跌。2025 年预计扩大至 \$45B」

**List expansion** (3+ items use a colon lead-in + semicolon or period separators):

- ❌ 「Vision 2030 的三个支柱包括充满活力的社会、繁荣的经济、雄心勃勃的国家」
- ✅ 「Vision 2030 三个支柱：充满活力的社会；繁荣的经济；雄心勃勃的国家」

**Embedded take-away** (lead each paragraph with a conclusion, then expand with data / citations):

- ❌ 「2024 年 GDP +2.7%，2025 年预测 +3.5%。这说明经济增长在加速」
- ✅ 「沙特经济增长在加速：2024 年 GDP +2.7%，IMF 2025 年预测 +3.5%」

**"ppts" → "percentage points"**: "+45 ppts" → "+45 percentage points" (stable PDF rendering, no mathtext dependency).

**Written-register wording** (Chinese):

| ❌ colloquial / academic | ✅ written |
|---|---|
| 使得 | 致 / 让 |
| 进行了 | 做 / 完成 |
| 做出了 | 作出 / 给出 |
| 具有重要意义 | 重要 / 关键 |
| 一定程度上 | 部分 / 在 X 维度上 |
| 综上所述 | 综合上述 / (delete, give the conclusion directly) |
| 总而言之 | (delete, give the conclusion directly) |

**Numbered lead-ins** (in-section lists lead with numbers, no bullet/colon mix).

**No technical symbols as conjunctions** (`→` `∴` `+` `/` `vs`):

- ❌ 「PIF → 海外配置 + 国内 giga-projects」
- ✅ 「PIF 同时配置海外资产与国内 giga-projects」

### 5.2 Punctuation and characters (redlines)

- **Never use the em-dash `——`**.
- **The half-width hyphen `-` is only for ranges and compound words** (`30-90%` / `2026-2030` / `single-bar`). Never as an em-dash substitute.
- **Use Chinese colons `：` sparingly**. Break with a period when you can. Keep the colon-to-period ratio at 5-15%.
- Use Chinese corner quotes 「」 uniformly.
- **No emoji or special symbols.**

### 5.3 Citation

medium does not use references.bib; use inline Pandoc footnotes uniformly:

```markdown
SOFR 3M rate latest 4.51%^[FRED, SOFR 3-Month Term Rate, 2026-05-15. https://fred.stlouisfed.org/series/SOFR3M.], consistent with Powell's language.
```

- Footnote content: `institution, title or field name, YYYY-MM-DD. URL.` (English field / series names plain, no 《》; Chinese book / report titles get 《》).
- URLs must be reachable (spot-check 3-5 during step 6 self-critique).
- Repeat the source on multiple citation; **do not introduce a shared bib key**.

### 5.4 Summary form

**Default: three-part summary** (aligned with heavy, suits 12-15 page topic analysis):

```markdown
# Abstract

**Core conclusion**: <2-3 sentences with the strongest conclusion + 1-2 critical numbers>

**Key findings**:
- <finding 1: number + so-what>
- <finding 2: number + so-what>
- <finding 3: number + so-what>

**Decision implication**: <one paragraph of so-what for the target reader>
```

**Optional: single BLUF paragraph** (enabled on explicit user request, aligned with light): single paragraph 80-150 words, the first sentence gives conclusion + key numbers + so-what, no bullets.

### 5.5 What not to write (red flags)

- **No methodology section** (unless data processing involves a non-public caliper that needs explaining).
- **No TOC numbering down to h3** (only h1 + h2 auto-numbered).
- **No "Background" / "Significance"** academic framing sections.
- **No meta-language** ("this study will", "this section will explore", "this study does not").
- **No self-invented metaphors** (undefined terms like "steel floor / soft floor"); use methodology terms ("hard caliper / soft caliper").

---

## 6. grep self-check text redlines

Before draft v1 is done and before any revision is delivered, grep verification is **mandatory**. Commands use `7_draft/draft.qmd` as the example.

**Evidence requirement (anti "formality self-check")**: when claiming the self-check passed, you **must paste the numbers from the last actual grep / count output**; a verbal "all clear" is not allowed. This applies to the count-gate rows (page / chart count) as much as to the language redlines.

| Redline | Check command | Expected |
|---|---|---|
| Em-dash `——` | `grep -c "——" 7_draft/draft.qmd` | 0 |
| Hand-written section-number prefix | `grep -nE "^#{1,3} (§\|A\.\|[0-9]\|[一二三四五六七八九十]、)" 7_draft/draft.qmd` | 0 lines |
| Emoji | `grep -cP "[\x{1F300}-\x{1F9FF}\x{2600}-\x{27BF}]" 7_draft/draft.qmd` | 0 |
| Unescaped dollar sign `$` (**mandatory for English drafts**; LaTeX treats `$` as a math delimiter, unescaped = render failure) | `grep -nP "(?<!\\\\)\\$" 7_draft/draft.qmd` | 0 (write body dollar amounts as `\$`) |
| h3 and deeper titles | `grep -nE "^#{3,}" 7_draft/draft.qmd` | 0 lines (medium is h1 + h2 only) |
| Body bold | `grep -c "\*\*" 7_draft/draft.qmd` | ≤ 5 (lead-in words excepted) |
| Chinese colon `：` to period ratio | total colons ÷ period count, **first deduct the "来源：/注：" label colons inside figsource / tblsource blocks** (consistent with heavy §7.4; without deducting, a report with 3+ charts is pushed past 15% by the mandatory label colons; measured: 5-chart body 5.5% but naive 20%). English drafts skip this item (no Chinese colons) | 5-15% |
| Lyrical-padding high-frequency words | `grep -nE "实际上\|事实上\|值得指出\|值得注意\|众所周知\|不可否认\|毫无疑问\|需要指出\|客观地讲\|不难看出\|在此背景下\|在这一过程中" 7_draft/draft.qmd` | spot-check and delete on hit |
| h2 empty-title anti-pattern | `grep -nE "^## .*(关于\|讨论\|探究\|浅析\|思考\|现状与挑战\|视角$)" 7_draft/draft.qmd` | 0 lines |
| Half-width `-` as em-dash | `grep -nE " - " 7_draft/draft.qmd` | spot-check; legal use is only ranges and English compounds |
| Technical symbols as conjunctions | `grep -nE "→\|∴" 7_draft/draft.qmd` + spot-check `+` `/` `vs` | replace with full written expressions |
| Academic / colloquial tone | `grep -nE "使得\|进行了\|做出了\|具有重要意义\|一定程度上\|综上所述\|总而言之" 7_draft/draft.qmd` | replace per §5.1 table on hit |
| Vague quantifiers | `grep -nE "很大程度上\|相对较高\|相对较低\|大致\|大约\|一些\|部分" 7_draft/draft.qmd` | spot-check; delete or replace with concrete numbers if unsupported |
| meta-language | `grep -nE "本研究不\|本章不\|本研究将\|本研究为.*而设\|本章构造\|研究边界明确\|需要明示\|本节将\|本章将\|本节强调\|本章强调" 7_draft/draft.qmd` | 0 lines |
| chart-script / CSV / body consistency | spot-check 3 charts | numbers consistent |
| outline-figures correspondence | `grep -oE "fig_[0-9]+_[0-9]+_[a-z_]+" 3_outline/outline.md` vs `ls 6_figures/*.pdf` | one-to-one |
| **page-count floor** (completeness) | `pdfinfo 7_draft/draft.pdf \| grep -i Pages` (poppler) | 12-15 target; 8-11 backfill or deepen; **< 8 move to light**; 16-20 trim; 20+ user decides on heavy |
| **chart-count floor** | count: `grep -cE "^!\[" 7_draft/draft.qmd` | 6-10, and **≥ the step-3 contract**; below = back to step 4 |
| Quarto render | `quarto render 7_draft/draft.qmd` | success, no mathtext / dimension errors |

**Count-gate (anti-slacking)**: the page / chart rows are a completeness gate, not a language redline. **Paste the actual numbers** when reporting the draft done. Below the floor = not done: backfill with genuine coverage (more sources at step 2, more charts at step 4), do **not** pad with lyrical filler or fabricate. If the topic honestly only supports 8-11 pages, say so and consider light mode — but a thin draft usually means the search / outline was shallow.

**Versus heavy §7.4**: medium drops 5 references.bib-related redlines (`_quarto.yml` lof / lot alignment, unreferenced fig/tbl labels, framing-section second rewrite, bib fields, figsource/tblsource colon deduction). The other 13 are kept.

**Versus light §6**: medium adds 2 chart-related ones (chart-script / CSV / body consistency, outline-figures correspondence).

---

## 7. Cross-cutting discipline

### 7.1 Source traceability (non-negotiable)

Every number must trace to an original source (research.md entry / pdfs/ PDF name / live-pulled series). Mark what cannot be located with ⚠️ or drop it; **do not write it into the conclusion**.

### 7.2 No fabricated numbers (non-negotiable)

"Not publicly available" / "to be verified" beats a plausible guess.

### 7.3 Three-state labelling (non-negotiable)

Fact ("per IMF") / estimate ("per market estimate ~X") / inference ("possibly X"); label the three with distinct wording.

### 7.4 AI output ≠ conclusion (non-negotiable)

The AI provides material and a first draft; the human decides the final conclusion. medium's 1 hard stop (step 7 sign-off) means the user has final review; the user does not blind-sign what the AI writes.

### 7.5 verifying-skill call (non-negotiable)

step 6b must call the `market-research-skills:verifying` skill to rigorously check unresolved caveats. This is medium's final verification gate, not skippable.

### 7.6 Double-landing (non-negotiable)

For all step 4 data-processing charts: **the underlying data (CSV) + the full script must both land**. Keep the source even if the chart is simple.

### 7.7 Hard cross-section number consistency (non-negotiable)

When the same number appears in different sections, **value and caliper must be consistent**. The step 6a self-critique perspective 4 checks this specifically.

### 7.8 Cross-stage decisions are made by the human (non-negotiable)

step 1 topic direction, step 4 add/remove-figure boundary cases, step 7 sign-off are all human decisions; the AI does not override them.

---

## 8. Retrospective mechanism (optional)

medium **does not mandate per-section retrospective** (heavy appends per section + a one-time project-close audit).

**Optional**: after project close, if the user feels there is cross-cutting experience worth promoting to the skill, write a `9_retrospective/retrospective.md` (create the dir ad hoc in the project), in heavy §11.2 three-part format (project facts → cross-project patterns → what should be promoted to the skill). The AI assists.

**Trigger conditions** (any one):

- the user subjectively feels "this run had important lessons"
- the run revealed an improvement point in workflow_medium.md / report_style_spec.md / chart_template.py
- a recurring pitfall surfaced across multiple medium projects

If not triggered, skip; medium does not do a retrospective for the sake of a "complete" feeling.

---

## 9. Boundary with light / heavy

Do not mix them up. The table draws the clean line:

| Dimension | light | **medium** | heavy |
|---|---|---|---|
| Steps | 6 | **8** | 11 |
| Time budget | 60-80 min | **3-5 h** | multi-day |
| Length | 5 pages / 2500-3000 chars | **12-15 pages** | 15k+ words / 35+ pages |
| Charts | 0 | **6-10** | usually 15+, often 30+ |
| Citation | inline footnote | **inline footnote** | references.bib |
| LLM | single only | **single only** | single / multi-LLM optional |
| Hard stops | 0 | **1 (step 7 sign-off) + optional 1 (after step 2)** | 3 (outline / draft / final) |
| Derivations | PDF + Word | **PDF + Word** | PDF + Word + HTML + WeChat |
| Retrospective | none | **optional** | mandatory (§11.2 audit) |
| _state.md | none | **yes** | mandatory |
| Directory structure | flat + pdfs/ single subdir | **7 numbered subdirs (drops 8 / 9)** | 10 numbered subdirs |
| Summary form | BLUF single paragraph | **three-part (default) or BLUF (optional)** | three-part (with keyword line) |
| Audience | expert / decision-maker | **expert / decision-maker or dual (onboarding choice)** | dual (expert + non-specialist) |
| TOC / numbering | none | **yes (h1 + h2)** | yes |
| Upgrade path | re-run medium / heavy | **re-run heavy (no in-place upgrade on the medium project)** | n/a |

**Trigger examples**:

| User phrasing | skill |
|---|---|
| "Write me a 5-page memo on whether the Fed cuts in September" | light |
| "Half-day analysis of PIF's recent overseas allocation shift" | **medium** |
| "8-page report: Middle East sovereign-fund 13F quarterly changes" | **medium** |
| "Quarterly review of industry X with 3-5 charts" | **medium** |
| "Do a deep study of US AI-bubble risk" | heavy |
| "Write a long WeChat piece on Saudi Vision 2030" | heavy |
| "Get me a brief for the boss within the hour" | light |
| "Quick analysis of recent Middle East sovereign-fund holdings" | light |

When unsure, **default to the lighter mode** (light → medium → heavy). Re-running a heavier mode when too thin is cheap; finding mid-run that a heavy topic only supports a light memo is awkward.

**No in-place upgrade on the original skill**: if a medium run reveals the topic is really heavy, re-run heavy from step 1; do not bolt 8_publication / 9_retrospective into the medium project dir. Reverse likewise.

---

## 10. _state.md and the project-level CLAUDE.md

### 10.1 _state.md template

Cross-session progress panel, maintained by the AI, updated once before each session ends.

```markdown
# Project progress panel · _state.md

> Single source of truth, the cold-start anchor for cross-session work. AI updates before each session ends.

## ▶ Current position (at a glance)

- Current step: <step N>
- Current subtask: <what specifically is being done>
- Next: <what is about to be done>
- Last session: <YYYY-MM-DD HH:MM>

## Key deliverable index

| step | deliverable | path | status |
|---|---|---|---|
| 1 | topic.md | 1_topic/topic.md | done / in-progress / pending |
| 2 | research.md | 2_research/research.md | ... |
| 2 | core PDFs | 2_research/pdfs/ | ... |
| 3 | outline.md | 3_outline/outline.md | ... |
| 4 | figures | 6_figures/ | ... |
| 4 | scripts | 5_scripts/ | ... |
| 4 | data | 4_data/2_processed/ | ... |
| 5 | draft v1 | 7_draft/draft.qmd | ... |
| 6 | critique | 7_draft/_process/critique_self.md | ... |
| 6 | draft v2 | 7_draft/draft.qmd | ... |
| 7 | sign off | (user verbal sign-off) | ... |
| 8 | PDF + Word | 7_draft/draft.{pdf,docx} | ... |

## Cross-stage open items

- [ ] <unresolved caveat 1>
- [ ] <undownloaded core PDF X>
- [ ] <boundary case Y awaiting user decision>

## git timeline (last 10 commits)

<AI pastes git log --oneline -10 on each update>

## Maintenance rules

- Update once before each session ends (not per commit).
- The AI treats "Current position" and "Cross-stage open items" as the single source of truth.
- Boundary with the project CLAUDE.md: this file records **progress and state**, CLAUDE.md records **conventions and decisions**.
```

### 10.2 Project-level CLAUDE.md template

```markdown
# Project CLAUDE.md · <project name>

> Project "constitution". Complements the global ~/.claude/CLAUDE.md: global holds cross-project conventions, this file holds project-specific ones.
>
> **Skill dependency**: analyst-research medium mode

## Project basics

- **Topic direction**: <one sentence>
- **Output form**: PDF main report + Word docx derivation (default)
- **Target audience**: <expert / dual>
- **Toolchain**: Quarto + xelatex for PDF; Python user-level install (no venv)
- **LLM mode**: single LLM (Claude solo), locked at medium workflow §1 onboarding

## Writing & layout

### Inherited defaults

Style, punctuation, citation in `references/workflow_medium.md §5`; document layout in `references/report_style_spec.md §1`; chart production in spec §2 / §3; YAML / fonts / palette defaults in spec §5. **All inherited, not repeated.**

### Project-restated redlines

- No em-dash `——` in the body
- Sparse Chinese colons `：` (break with periods)
- Uniform Chinese corner quotes 「」
- No hand-written section-number prefix in titles
- h3 forbidden (h1 + h2 only)

## Charts

- Palette: <project palette, cite spec §5.3 default or project-specific>
- Chinese font: <Songti SC or project-specific>
- English font: Times New Roman
- Chart script naming: `make_fig_<section>_<n>_<topic>.py`
- Chart file naming: `fig_<section>_<n>_<topic>.{pdf,jpg}`

## Domain conventions

<project data calipers, term translations, source conventions>

## Deviations from the framework

<if this project deviates from a medium workflow / spec rule, record it here>
```

### 10.3 Boundary between _state.md and CLAUDE.md

- `_state.md`: progress panel. **State, position, open items.** High-frequency AI updates (once per session).
- `CLAUDE.md`: conventions and decisions. **Palette, calipers, terms, deviations.** Low-frequency updates (once per decision).

Do not write progress into CLAUDE.md, nor conventions into _state.md.

---

## Appendix A: broad-search resource list (compressed)

7 resource classes, representative items per class. Full version in heavy workflow.md appendix A (medium users need not read it; the items here cover medium's ~15-source scale).

### A.1 international organisations & multilaterals (English)

- **IMF**: WEO (World Economic Outlook) / GFSR / Article IV country reports / Fiscal Monitor
- **World Bank**: Open Knowledge Repository / Global Economic Prospects / regional outlooks
- **IEA**: World Energy Outlook / Oil Market Report
- **OECD**: Economic Outlook / Statistics
- **BIS**: Quarterly Review / Working Papers
- **UN**: UNCTAD / UNDP / specialised agencies
- regional development banks: ADB / EBRD / AIIB / IsDB

### A.2 sovereign / government / central bank / regulators

- central banks: Fed / ECB / BoE / BoJ / PBoC / SAMA / etc.
- statistics offices: BEA / Eurostat / NBS / GASTAT / etc.
- finance ministries / regulators
- sovereign funds: PIF / GIC / Temasek / ADQ / ADIA / Mubadala annual reports and 13F disclosures
- sector regulators: CSRC / FCA / SEC / etc.

### A.3 academic & think tank

- **NBER**: Working Papers
- **SSRN**: search + full-text download
- **Google Scholar**: search + citation-network tracing
- think tanks: Brookings / CSIS / Chatham House / Atlantic Council / Carnegie / RAND / etc.

### A.4 investment-bank research & consulting

- international banks: GS / JPM / MS / Citi / BofA / DB / Barclays / HSBC Country Outlooks, sector deep-dives
- consulting: McKinsey Global Institute / BCG / Bain / Deloitte / EY / KPMG / Roland Berger
- rating agencies: Moody's / S&P / Fitch sovereign ratings and commentary

### A.5 mainstream financial media

- English: Bloomberg / Reuters / FT / WSJ / The Economist / Nikkei Asia
- Chinese: Caixin / Wallstreetcn / FT Chinese / Yicai / 21st Century Business Herald
- regional: Arab News / Gulf News / Saudi Gazette / etc.

### A.6 WeChat / industry communities (Chinese world)

- finance: Zhibenshe / Spruce (智堡) / Caijing Eleven / CICC Research / CITIC Securities
- regional: Middle East-focused public accounts / Belt and Road forums
- vertical: by project topic

### A.7 databases (programmatic access)

- **FRED**: US macro
- **yfinance**: US / HK / global quotes
- **SEC EDGAR**: US regulatory filings, incl. 13F
- **iFinD MCP**: A-shares / HK / China macro
- **AKShare / Baostock / Tushare**: A-shares / HK / China macro
- **CoinGecko**: crypto
- **World Bank / IMF / OECD / Eurostat / ECB**: open APIs
- unified via the `financial-data-sources` skill

### A.8 both-languages principle

International orgs, investment banks, academia mostly English; regional, policy, primary news often more accurate in Chinese. In medium single-LLM mode, Claude alone walks 4-7 classes, filling Chinese regional ones via iFinD MCP and WeChat WebFetch.
