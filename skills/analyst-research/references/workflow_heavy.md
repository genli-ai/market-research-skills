# analyst-research · heavy mode workflow

> English is the authoritative version; the Chinese mirror is `workflow_heavy.zh.md`.
> Writing-standard examples illustrating Chinese-prose redlines are kept in Chinese (they apply when the report language is Chinese); the surrounding rules are in English and apply to both languages unless noted.

> This document is a methodology framework for "doing investment research with AI", not bound to any specific topic. It is positioned for "synthesis-and-analysis based on an existing body of mature research or large datasets", not original modelling.
>
> Companion relationship: the project-level `CLAUDE.md` holds this project's specific adjustments and conventions; this file holds general accumulated experience. Update both in sync (project for specifics, here for generals).
>
> skill loading and onboarding flow: see §1.3 Step 0.

---

## 1. Positioning & usage guide

### 1.1 What this document is

A cognitive-stage pipeline for AI-assisted investment research. It does not tell you which topic to do; it tells you **what steps any investment-research topic should go through, the deliverable quality gate at each step, and where the human intervenes**.

### 1.2 Who it is for

Your future self opening a new project. The AI assistant also reads it when entering a new project, but its highest priority is to work with the user's judgement rather than execute mechanically.

Relationship to the project-level `CLAUDE.md`: CLAUDE.md is a specific project's "constitution", this file is the shared "methodology" across all projects. For overlapping parts (writing style, PDF render conventions) this file is the baseline; the project level may override with a stated reason.

### 1.3 New-project onboarding flow

**Scenario**: the user wants to scaffold the project and launch the 11-step flow in one main conversation. The skill as a whole (`SKILL.md` + `references/workflow_heavy.md` + `references/report_style_spec.md` + `scripts/chart_template.py` + `scripts/publication-style-template.html` + `scripts/author.jpg`) arrives one of two ways: A. the skill is triggered and the AI copies it wholesale into the project root; B. the user manually copies the `analyst-research/` folder into the new project root. When the AI assistant **first reads this document** in a new-project conversation, it reads the two references/ docs in order, then enters the flow below.

**Step 0: three-piece-set check**

Two arrival paths, same end state: the project root has a complete `analyst-research/` folder, structurally identical to the skill itself.

A. **skill-load scenario** (skill active): wholesale copy, one line:

```bash
cp -r ~/.claude/skills/analyst-research <project root>/
```

B. **direct-copy scenario** (no skill): the user manually copies the `analyst-research/` folder into the new project root (drag or `cp -r`).

End-state structure of the project-root folder:

```
analyst-research/
├── SKILL.md                              ← skill entry, local copy as placeholder
├── references/
│   ├── workflow_heavy.md                 ← process discipline (this document)
│   └── report_style_spec.md              ← visual spec + chart_template interface contract
└── scripts/
    ├── chart_template.py                 ← chart implementation (cross-project seed)
    ├── publication-style-template.html   ← publication HTML template (optional derivation)
    └── author.jpg                        ← author headshot placeholder (optional derivation)
```

Read `references/workflow_heavy.md` + `references/report_style_spec.md` before Step 1. Outside the three-piece set, only add `_quarto.yml`, `.claude/`, and the stage output dirs; add nothing inside `analyst-research/`. Project-specific tailoring (palette, fonts, domain conventions) is edited in the local copy, not polluting the skill body.

**Step 1: announce**

Briefly confirm: "I have read the analyst-research/ three-piece set and am ready to scaffold the project and start step 1. Please confirm."

Ask three onboarding questions at the same time; lock the answers and do not re-ask:

0. **Report language?** English (default) / Chinese / other. If unspecified, write the main report and derivations in English (see SKILL.md "Language policy"). English drafts skip the Chinese colon redline and enforce the unescaped-`$` redline (write amounts as `\$`, else LaTeX treats `$` as a math delimiter and the render fails). Lock into CLAUDE.md.
1. **Multi-LLM collaboration mode?**
   - **No (default)**: Claude solo throughout. Step 2 broad search and supplementary search done by Claude alone; Step 9b critique by Claude self-critique against 6 perspectives (facts, calipers, citations, cross-section consistency, argument flow, language standards), weaker independence than multi-LLM.
   - **Yes**: Step 2 runs three in parallel (Claude + GPT + DS), Step 9b critique by GPT (not DS). Other steps still Claude solo.
   - Multi-LLM mode requires the user to manually switch to the relevant plugin or web app for GPT / DS, a significant rhythm cost; single-LLM has no switching cost but loses critique independence. Default to No; state explicitly when confirming Yes.
2. **Is there a validated Quarto `_quarto.yml` template to reuse?**
   - Field experience: a user's already-validated yml beats Claude's from-scratch "best practice", saving multiple rounds of font / linestretch / TOC-localisation tuning.

After the three answers lock, write them into the project CLAUDE.md (language into the "report language" section, multi-LLM into the "multi-LLM collaboration" section), then proceed to Step 2 scaffolding.

Other toolchain defaults are not asked each time. If the user adjusts a default (e.g. switch to Word), the user states it:

- Layout: Quarto + xelatex for PDF (**prefer reusing the user's existing _quarto.yml**; otherwise use the spec §5.1 default header)
- Data scripts: Python (no venv, user-level install, see global `~/.claude/CLAUDE.md`)
- Project category: investment-research industry report
- Output forms: main report PDF + Word docx derivation (10b default), plus optional publication HTML (10c) + WeChat JPG slices (10d)
- Target audience: dual (undergraduate-educated non-specialist with basic economics, also suits professional readers)
- Time expectation: no preset pace, advance by the hard / soft stops in §4, the user can stop or accelerate at any time

**Step 2: scaffold**

Create folders and all deliverable mds per §11:

```bash
mkdir -p .claude \
         1_topic/_process \
         2_research/{pdfs,_process} \
         3_outline/_process \
         4_data/{1_raw,2_processed} \
         5_scripts \
         6_figures \
         7_draft/_process \
         8_publication/{1_word,2_HTML,3_wechat_pages} \
         9_retrospective
```

`analyst-research/` is already copied in by the user; do not recreate it.

Then create the following files.

`.claude/settings.local.json`, allowing common tools once to avoid repeated approvals:

```json
{
  "permissions": {
    "allow": [
      "Bash", "Read", "Edit", "Write", "MultiEdit", "NotebookEdit",
      "WebSearch", "WebFetch", "TodoWrite", "Task", "Agent", "mcp__*"
    ]
  }
}
```

`5_scripts/_path.py`, so scripts in `5_scripts/` can import `analyst-research/scripts/chart_template.py`:

```python
"""Add analyst-research/scripts/ to sys.path so make_fig_*.py here can import chart_template."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "analyst-research" / "scripts"))
```

Then each `make_fig_*.py` top has `import _path` + `from chart_template import setup_style, save_fig, PALETTE` (see `analyst-research/references/report_style_spec.md §6.4`).

`_quarto.yml`, copy the standard header from `analyst-research/references/report_style_spec.md §5.1` and adjust the font block per project.

Other files to create:

- `_state.md`, per the §12 template, initialised to "step 1 in progress"
- `CLAUDE.md`, the project constitution. First copy the core conventions from the global `~/.claude/CLAUDE.md`, then add project-specific domain conventions (some content filled in after the topic is confirmed)
- the deliverable mds for each folder (`topic.md` / `research.md` / `outline.md` / `data.md` / `scripts.md` / `figures.md` / `draft.md` / `retrospective.md`), empty per the §11 minimal skeleton with a one-line purpose, filled in by later steps
- `references.bib`, empty, reserved for step 8/9 citations

When done, `git init` + first commit, tag `scaffold-init`.

**Step 3: launch step 1**

Ask the user one question: **What topic do you want to research (one sentence)?**

Other parameters are fixed at Step 1 (dual audience, PDF + WeChat dual version, no preset time) and not re-asked.

**Step 4: advance each step per §4 rules**

- **Soft stop**: after the stage output, announce "this step is done, ready for step N+1, please confirm or stop me".
- **Hard stop**: stop and wait for sign-off, saying clearly "this is a hard stop, you need to review [file path], I proceed to step N+1 only after sign-off".

On each step switch: (1) update `_state.md`'s "▶ Current position" section; (2) git-tag key milestones.

**Step 5: cross-cutting discipline runs automatically**

Without user reminder, the AI runs throughout:
- append a retrospective to `9_retrospective/retrospective.md` right after each section is synthesised (§10)
- download full text before any structural citation of an important document (§step 5)
- data + script must both land (§5.5)
- writing standards, PDF compatibility, CSV hygiene run through all steps
- under multi-LLM parallel output, each LLM produces only under `_process/<llm>/`, synthesised by Claude

**Handling disagreement**:
- user says "skip a step": first ask "why"; hard stops cannot be skipped, soft stops can have depth trimmed
- user says "speed up": trimming a step's depth is OK, hard stops cannot be dropped
- user says "run your own model": per §2.2, exhaust the search for existing research first, simple calculation as an aid only if needed
- user conflicts with this framework: the user wins, but state clearly "this conflicts with this framework's §X, reason Y" and let the user decide whether to override

---

## 2. Boundaries

### 2.1 Applicable scenarios

Investment-research projects with a clear research question that need medium-to-long-form output. Output can be industry reports, macro thesis pieces, company deep-dives, policy assessments, geopolitical-event impact analysis, etc.

### 2.2 Core positioning: synthesis + analysis, no original modelling

All research is "synthesis + analysis based on existing mature research / large datasets". The AI's role in priority order:

1. Collect and aggregate existing research (IMF, World Bank, IEA, major-bank Research, consulting, academic papers, etc.)
2. **Process, compare, visualise, and interpret existing data** (high priority, one of the core value-add steps of AI investment research)
   - descriptive calculation: shares, growth rates, market share, CAGR, cross-country comparison, simple scenario estimates
   - re-compute with an existing method: e.g. re-compute the latest figures with the IMF's public fiscal-breakeven-oil-price formula
   - **visualisation must be crafted with care and highlights**: chart design, palette, caliper labelling, information density all polished. Visualisation is the report's face
3. Organise scattered material into report language with an argument flow

The boundary of item 2 is "simple processing", not expanding into complex analysis of "your own methodology". See below.

The AI does not start these on its own; with user approval they can be aids:

- **Simple econometrics**: OLS, correlation, descriptive-statistics regression, as a sanity check or cross-check of existing research. Not the main conclusion.
- Designing your own calculation formula from scratch (applying an existing formula is fine, inventing one is not)

The AI absolutely does not:

- invent a method to run a novel model (e.g. design your own panel VAR, DSGE, state-space model)
- attempt an amateur reproduction of IMF / academic fine estimates (a crude reproduction harms the whole report's quality, the reader doubts the whole thing)
- reinvent the wheel in a field with existing mature research

Mnemonic: exhaust the search for existing research first → cite what you find → do descriptive calculation and visualisation boldly (these are the report's highlights) → simple econometrics needs user approval → never attempt to reproduce existing academic fine methods.

### 2.3 Inapplicable scenarios

One-shot Q&A, pure literary creation, marketing copy, tool-script-only development.

---

## 3. The 11-step skeleton

| Step | Name | Lead | Stop |
|---|---|---|:-:|
| 1 | initial topic | user proposes | soft |
| 2 | broad search | Claude solo (single-LLM default); three in parallel (multi-LLM) | soft |
| 3 | AI suggests topic directions from material | Claude | soft |
| 4 | confirm topic and thesis | user | **hard #1** |
| 5 | supplementary search (focused depth, full-text download of key material) | Claude solo (multi-LLM may run three in parallel) | soft |
| 6 | detailed outline draft (with chart list) | Claude solo (multi-LLM may run three brainstorm) | **hard #2** |
| 7 | complete charts and tables, backfill outline | Claude lead | soft (announce after landing, user reviews JPGs any time) |
| 8 | draft writing (default one continuous pass) | Claude solo (incl. render and YAML tuning) | soft (per-section hard stop as fallback) |
| 9 | refine: 9b critique → 9c verifying → 9d user sign-off | single-LLM Claude self-critique; multi-LLM GPT critique | soft (9d **hard #3**) |
| 10 | finalise + derive: 10a freeze main PDF, 10b Word, 10c publication HTML (optional), 10d WeChat JPG slices (optional) | Claude | soft (announce after each sub-step lands) |
| 11 | retrospective | Claude + user | anytime (11.2 one-time project-close audit) |

**Hard vs soft stop**:
- **Hard stop**: must stop and wait for user review / sign-off; the AI cannot proceed on its own.
- **Soft stop**: the AI can give a stage output and continue, but the user can stop at any time.

**Key iteration loop**: steps 6 ↔ 7 are bidirectional, not one-way. The outline draft usually needs revising after all step 7 charts are done (caliper traps, data gaps, newly found argument angles) to become the final outline.

---

## 4. Step details

### Step 1: initial topic (soft stop)

**Key question**: what topic is the user interested in?

**Operations**:
- the user gives a one-sentence direction (e.g. "I want to look at the sustainability of GCC wealth accumulation through oil-price volatility")
- the AI does only minimal response: restate to confirm understanding, ask 1-2 clarifying questions (output form, target audience, time expectation). **No divergent topic suggestions** (divergence is step 3).

**Deliverable**: the topic description in conversation (no separate file needed).

**Note**: this step's topic is a "target", not final. It will likely be revised or even replaced after steps 2-4.

---

### Step 2: broad search (soft stop)

**Key question**: what data and material **already exist** around this initial topic?

**Goal**: fix the topic direction (quantity first, coverage first).

**Operations** (per the LLM mode locked at onboarding):

- **Single-LLM mode (default)**: Claude solo walks all seven source classes, using the iFinD MCP or `financial-data-sources` skill for data. **The blind-spot safety net in single-LLM mode is the user manually supplying key PDFs** (field experience: a project once had the user supply 11 core PDFs after step 5, surfacing 8 key findings step 2 had missed). Claude synthesises into `2_research/research.md`.
- **Multi-LLM mode**: Claude / GPT / DeepSeek search independently; their search-engine interfaces, training-data coverage, and retrieval styles differ widely, so parallel runs avoid single-LLM blind spots (field case: one LLM missed a regional statistics-office dataset, another supplied it after the user's follow-up). Claude synthesises, dedupes, and classifies into `research.md`.

Both modes share:

- **Data scouting**: candidate data-source list (institution, caliper, frequency, fields, accessibility)
- **Document scouting**: candidate document list (IMF, World Bank, IEA, major-bank Research, consulting, academic papers)

**Key discipline: full source coverage (seven classes mandatory)**

In the broad search the AI must **proactively search the following seven source classes**, not just the two or three it knows. Full list in §Appendix A, brief:

| Class | Examples |
|---|---|
| A.1 international organisations | IMF, World Bank, IEA, OECD, BIS, UN, regional development banks |
| A.2 sovereign / government / central bank | central banks, statistics offices, finance ministries, sovereign funds, sector regulators |
| A.3 academic & think tank | NBER, SSRN, Google Scholar, Brookings, CSIS, Chatham House |
| A.4 investment banks + consulting | GS / JPM / MS / Citi Country Outlooks, McKinsey / BCG sector reports, Chinese-bank overseas research |
| A.5 mainstream financial media | Chinese: Caixin, Wallstreetcn, FT Chinese; English: Bloomberg, Reuters, FT, WSJ, Economist |
| A.6 WeChat / industry communities | finance / regional / vertical Chinese public accounts |
| A.7 databases (programmatic) | available MCP / API / skill: iFind, OpenBB, `financial-data-sources` skill |

**Both-languages principle**: international orgs, investment banks, academia mostly English; regional, policy, primary news often more accurate in Chinese. In multi-LLM mode the three divide: Claude leans English academic and bank reports, DeepSeek Chinese and regional context, GPT balanced (see §6.2). In single-LLM mode Claude alone walks all seven, filling Chinese regional ones via iFinD MCP and WeChat WebFetch.

**Source-coverage self-check**: at the end of step 2 the AI must self-check whether all seven classes were searched. Any class not searched at all must be done before step 3.

**Deliverable**: `2_research/research.md` first draft (seven sections matching A.1-A.7), raw multi-LLM output kept in `2_research/_process/`.

**Key discipline: "open the page and download, then judge"**

When scouting data, **download at least one representative point of actual data before judging** accessibility; do not conclude "data incomplete" from a SERP snippet / impression / site description. Field lesson: judging a data source "partially accessible" from a SERP impression, only to find full coverage after downloading.

**Pitfall warnings**:

- (multi-LLM only) when the three parallel searches conflict, do not let Claude arbitrate; show the user the raw conflict.
- (single-LLM only) a single LLM's key judgement must be cross-checked against another source class (e.g. IMF estimate vs official sovereign disclosure) before becoming a conclusion. A single source is not enough.
- Be cautious concluding "not found"; the search terms may be wrong, try another keyword set or two.

---

### Step 3: AI suggests topic directions from material (soft stop)

**Key question**: based on the density of material found, which topic directions hold up?

**Operations**:
- based on the step 2 list, give 2-3 viable topic directions
- compare each across **5 fixed dimensions**:
  1. **core research question** (one sentence)
  2. **material density** (strong / medium / weak)
  3. **potential take-away** (the judgement the reader walks away with)
  4. **risk and uncertainty** (data gaps, caliper limits, policy sensitivity)
  5. **uniqueness** (difference from existing research, avoiding duplicate effort)
- **explicitly flag which directions lack material, and dissuade**

**Deliverable**: direction suggestions in conversation (can also land in `1_topic/_process/_options.md`).

**Note**: do not write a "topic direction" as an outline. The outline is step 6; here it is only a coarse direction split.

---

### Step 4: confirm topic and thesis (**hard stop**)

**Key question**: based on the AI's suggestions, which one does the user pick?

**Operations**:
- the user picks from the AI's suggestions, or modifies, or starts over
- land it as `1_topic/topic.md`, containing at minimum:
  - one-sentence title
  - research question (one paragraph)
  - target audience (e.g. "undergraduate-educated non-specialist with basic economics")
  - output form (e.g. "main report PDF plus WeChat derivation"). Scale is by content necessity, but heavy's **target scale is 30-40 pages / 15k words+ / 25-35 charts**. This is a direction floor, not a quota ceiling: **if output is clearly below this (e.g. < 25 pages or < 20 charts), it is almost certainly insufficient coverage depth, and you should go back to step 5 for more search, step 6 for more chapters, step 7 for more charts, rather than ship a "formally complete but thin" draft**. step 7 / 8 do not audit by precise word count, but by "does each of the six dimensions have enough chapter depth + did each add-figure trigger actually produce a chart"; clearly thin = incomplete. Common laziness signals: each section only 1-2 paragraphs, the whole report < 20 charts, sub-questions glossed over without data support. This floor is no longer left to discretion: it is locked as a contract at step 6 sign-off and enforced at the §7.4 finalise count-gate (paste actual page / chart / word counts; below floor = not done).
  - chapter-skeleton draft: **step 4 only h1 coarse outline** (5-7 h1), h2 refinement left to step 6 outline. The report body has two levels only, no h3.

**Hard-stop criterion**: the user must sign off explicitly before step 5. Starting supplementary search before the topic is fixed wastes effort.

---

### Step 5: supplementary search (soft stop)

**Key question**: around the confirmed topic, is there enough deep supporting material?

**Goal**: deepen support (quality first, depth first).

**Operations**:
- based on topic.md's chapter skeleton, list per section the supporting material still needed
- **single-LLM mode (default)**: Claude solo deep-searches the sub-questions, the user supplies key full-text documents
- **multi-LLM mode**: three parallel deep-searches on sub-questions, Claude synthesises
- full-text download of key documents (both modes, see discipline below)

**Key discipline: full-text download of important material**

Documents with a **structural argumentative role** must be downloaded in full to `2_research/pdfs/`, with the `research.md` "importance" field marked "core", then summarised with pypdf to decide how to cite.

Criteria for "structural argumentative role" (any one triggers):
- a section's core argument cites it
- it provides a key number (e.g. fiscal-breakeven oil price, oil-price-GDP elasticity)
- its methodology is borrowed or contrasted by this project

**Operating flow**:
1. Prefer the institution's official original link (IMF eLibrary, World Bank Open Knowledge, IEA, central-bank sites), not a second-hand repost.
2. Naming: `<n> <institution> <title>.pdf`, number from the current max +1.
3. Read after download: **summarise with pypdf first** (structured output is more robust, can extract title, sections, tables programmatically); fall back to the Read tool's `pages` parameter for page-limited reads when pypdf fails or you need a specific page. Extract the method, key parameters, conclusions before deciding how to cite.
4. Sync the bib entry: `url` to the official original link, `urldate` the download date.
5. Restricted handling (paywall / login wall): put a `<n>_<title>_NOTES.md` recording the access path and summary; bib note `note = {access via X, download blocked}`.

**Bad example**: "I saw GCC non-oil GDP loss of 80 bps in a GS report, let me cite it" + did not download the full text + does not know what the number assumes. The right move is to get the full GS report, see its scenario definition, then decide whether to cite.

**Key discipline: user-supplied material takes priority**

The user may drop material into `2_research/pdfs/` at any time (not only PDFs; also md notes, cleaned web text, screenshots, Excel). These rank above the AI's own search results:

- the AI must proactively **read them in full** (Read full text, not just summary / TOC)
- mark "source: user-supplied" in `research.md`
- importance defaults to "core" unless the user says it is reference
- the `pdfs/` dir may have md files besides PDFs (user notes, cleaned web text); name them with the unified numbering
- if user material conflicts with the AI's findings, the user material wins; if further analysis is needed, tell the user the conflict clearly

**Deliverables**:
- the full-text PDF set under `2_research/pdfs/` (flat, named by number)
- `2_research/research.md` complete: each source's type / institution / title / year / PDF path / importance / key fields / acquisition method

---

### Step 6: detailed outline draft (**hard stop**)

**Key question**: based on the full source library, what does the detailed outline look like?

**Operations**:
- write `3_outline/outline.md` based on the full library (steps 2 + 5)
- **chapter skeleton**: h1 / h2 titles are themselves conclusive (not "Fiscal view", but "Fiscal view: the three-tier 30%-90% oil-and-gas share of fiscal revenue"). The body has two levels only, no h3 (see `report_style_spec.md §1.2`).
- **each section lists**:
  - research sub-question (one sentence)
  - core take-away (one sentence)
  - planned data and charts (specific table / figure number, underlying data source)
  - key citations (specific document name + page)
- **mandatory paragraphs**: "what we do not do" + "uncertainty boundary" (data gaps, caliper limits, commercial-information risk, etc.)

**Chart-list generation (by LLM mode)**:

- **single-LLM mode (default)**: Claude alone proposes the chart list from the full library (which charts in each section support the argument), the user decides, lands in the outline
- **multi-LLM mode**: Claude / GPT / DeepSeek each propose a chart plan, Claude synthesises one unified list. Tendencies: data-precision and caliper-analysis charts strong with GPT, historical-time-series and regional-context charts strong with DS, argument-flow anchoring and cross-section bridging strong with Claude

In both modes, the final deliverable is one unified chart list synthesised by Claude, not a stitch of three originals.

**Outline version management**:

- **v1**: step 6 first draft (first version from the full library)
- **v2 / v3 / ...**: revisions after step 6 ↔ step 7 bidirectional iteration (charts reveal caliper conflicts, new argument angles, go back to step 6)
- **signed version**: after the user signs the final v, tag `git tag outline-locked`, proceed to step 7 final

Field experience: a project's outline ran to v3 before sign-off lock (in the v2 phase the user supplied 11 PDFs surfacing 8 new findings, triggering an outline rewrite).

**Link between outline and step 7 add/remove-figure criteria**:

- when listing charts, each is **pre-screened against the step 7 "6 add-figure criteria"** (multi-source comparison, time variation, cross-dimension, magnitude/distribution, target-vs-actual, spatial/process); every chart in the outline satisfies at least one
- before step 7 commit, each passes the "5 remove-figure criteria" (single number, 2-3 simple shares, multiple slices in one section, trend statement with no node numbers, conclusion/bridging paragraphs); remove on trigger
- any chart-list change (a chart found necessary during step 7) must **go back to step 6 to sync the outline**

**Outline-as-contract (the floor anchor)**:

The signed outline is not just a plan, it is a **contract** that step 8 draft and step 10 finalise are measured against. At sign-off, write a one-block contract header at the top of `outline.md`:

- **section count**: N h1 chapters, M h2 subsections
- **planned chart count**: K charts (the unified chart list), each tied to a section
- per section: its one-sentence take-away + its planned chart(s)

Two checks at sign-off:

1. **Does the contract itself clear the heavy band?** If the planned outline is only, say, 4 chapters / 12 charts, the outline is too thin — go back and add chapters / charts **before** the user signs, do not sign a thin contract and discover the shortfall at step 10. The target band is 30-40 pages / 25-35 charts / 15k words (English) or 1.5万字 (Chinese); an outline that cannot plausibly reach it is incomplete.
2. **The signed counts become the step 8 / step 10 floor.** A final draft with fewer sections or charts than the signed contract is a contract breach: either restore them, or explicitly tell the user which planned item was dropped and why (e.g. the data turned out unavailable). Silent shrinkage is the classic laziness failure mode and is not allowed.

Tie the contract to the existing `git tag outline-locked`: the tagged outline is the reference the §7.4 finalise count-gate checks against.

**Hard-stop criterion**: proceed to step 7 only after the user reviews and signs off on outline.md. Sign-off also locks the contract counts above; they become the floor checked at the §7.4 finalise count-gate.

**Note**: this outline is a draft, not final. After step 7 it usually needs revising into the final outline.

---

### Step 7: complete charts and tables, backfill outline (soft stop)

**Key question**: build all charts first and see whether the argument stands.

**Why charts first**: building charts before writing is a diamond-grade field insight. Field counter-example: a project wrote the outline and body "Country X policy target 65%" first, only to find during charting that the number did not correspond to that metric (the 65% was a share under another caliper). Building charts first exposes incomparable-caliper problems immediately.

**Operating flow**:

0. **Pre-flight: confirm the palette**. Before charting, set the palette in `analyst-research/scripts/chart_template.py` (default FT blue, see `report_style_spec.md §5.3`), get user confirmation before drawing. If the colours are not fixed, you redo everything after charting. (Also run the chart_template self-test for the `$` / annotation-colour / long-y-tick checks per spec §3.13.)
1. **Data landing**: raw downloads to `4_data/1_raw/`, processed versions to `4_data/2_processed/`, named `<section>_<topic>.csv`.
2. **Script landing**: **one script per chart** (see `report_style_spec.md §3.1`), named `make_fig_<section>_<n>_<topic>.py`, head docstring stating purpose / input / output. No "one section, one script generating multiple charts". **Each script draws one plot; no side-by-side subplots** (see `report_style_spec.md §3.7`). Script top `import _path` + `from chart_template import ...` (see `report_style_spec.md §6.4`).
3. **Chart generation**: each chart outputs PDF + JPG + `_clean.jpg` to `6_figures/` (see `report_style_spec.md §3.3`), named `fig_<section>_<n>_<topic>.{pdf,jpg}` + `fig_<...>_clean.jpg`. `save_fig` takes `title / source / note`: bare PDF (Quarto caption provides these); self-contained burn-in JPG; `_clean.jpg` is a PDF-synced raster for publication-style HTML embedding (the HTML template provides title/source). JPG long edge ≤ 2000px (see `report_style_spec.md §3.11`).
4. **Backfill outline**: after each chart / table, backfill into the matching section of `3_outline/outline.md` (embed `![]` + caption + a one-line figure-note preview).
5. **Cross-check**: does the chart's conclusion match the outline draft's take-away? If not, go back and fix the outline.

**Key discipline: double-landing**

For any chart / table involving data processing, **the underlying data + the full script must both land** (reproducible). The core of research discipline is "source-traceable, process-reproducible"; a chart with no data / script makes the conclusion a black box. Keep the source even if the chart is simple, for retrospective and future redraws.

**Key discipline: judge before charting (add and remove criteria)**

No upper/lower bound on chart count. The only reason a chart exists is "text and tables cannot, or inefficiently, express a specific reading". Each chart must answer the test: **without this chart, could the reader understand the passage equally efficiently?** If yes, do not chart; only chart if no.

**Add-figure criteria** (run per section when writing the body; any one triggers):

| Situation | Why text fails |
|---|---|
| **Multi-source comparison**: same metric, 3+ sources side by side | text listing is messy, the reader has to compute the comparison |
| **Time variation**: 5+ year trend, inflection, rhythm | endpoint numbers in text do not show the shape |
| **Cross-dimension comparison**: 2D or multi-D (country × sector, year × metric) | text description loses structure, the reader cannot reconstruct it |
| **Magnitude or distribution**: shape, extremes, quartiles | text gives statistics but loses shape |
| **Target vs actual**: two data sets compared visually | a table works but visual comparison is faster |
| **Spatial or process relation**: geography, network, flowchart | the reader cannot reconstruct it from text |

**Remove-figure criteria** (run per chart before commit; any one triggers):

| Anti-pattern | Why not |
|---|---|
| Single-number statement ("metric X = Y%") | one sentence says it, a single bar adds no information |
| 2-3 simple shares ("A 60%, B 40%") | a pie equals text, text is tighter |
| Multiple slices of the same dataset in one section | merge into a multi-panel or keep the strongest |
| Trend statement with no specific node numbers | no "what happened in which year", the chart has no anchor |
| Conclusion, bridging, intro, closing paragraphs | these do not anchor data |

**Anti-laziness**: before step 7 the AI runs the add criteria per section's argument flow; any section with a data statement but no chart is a violation (unless the section is inherently conclusion or bridging).

**Anti-stuffing**: before each chart commit the AI runs the remove criteria; not removing on trigger is also a violation.

**Post-removal action**: inline the removed chart's numbers and argument into the prose; do not let removal break the argument flow.

**Subjective disputes go to step 9d**: for boundary cases, step 9d's user PDF review is the final check, the user decides.

**Key discipline: derive title / source / note strings from CSV, do not hardcode numbers**

This project's 9b critique once exposed 18 chart-script strings (title / source / note) inconsistent with CSV data / body narrative — the highest-frequency step 7 pitfall. Root cause: "title hardcoded from impression, script not synced when the CSV was later revised".

Prevention discipline:

- **when title cites a specific number** (e.g. "fiscal deficit \$32B", "private female +84%"), the script **computes max / min / argmax / latest on the spot and f-string-inserts it**, not hardcode. E.g. `title=f"private female +{df.loc['private_female_growth'].max():.0%}"`, not `title="private female +84%"`
- **when source cites a page / table number** (e.g. "institution Annual Report 2024 page 15"): grep the CSV header / data for the field name before writing, confirm the page matches where you took it from
- **when note cites a specific caliper** / time point: check the CSV metadata columns (`source_year` / `definition`), do not rely on memory

**fail-safe**: add an `assert` at the script top checking the title number matches the CSV computation; no commit if CI fails. E.g. `assert "84%" in title and df.loc['private_female_growth'].max() >= 0.84`

**Key discipline: source / note strings "edit one, reconcile all 4"**

The same chart's source / note string exists in **4 places**:

1. the `save_fig(source=..., note=...)` parameters in `make_fig_*.py` (for the self-contained JPG)
2. the `\begin{figsource}` block after the matching `![](fig.pdf)` in `draft.qmd` (for the report PDF, spec §3.3)
3. the narrative source / time / caliper where the body cites the chart
4. the matching citation key in `references.bib` (if cited with `[@cite]`)

**Any edit to one (delete a source, change a caliper, change a time point) must reconcile all 4.** Field lesson: a project caught a leftover old source label in a figsource block only at 9d (the script was synced but the figsource block, written separately, was missed). This four-way inconsistency is a high-frequency pitfall. Prevention: derive the figsource content from the chart script with a helper, avoiding dual-source manual maintenance.

**Key discipline: AI does logic self-check before commit, leaves visual self-check to the user**

Per spec §4, "the AI does not do visual checks" (CJK font recognition is unstable, multiple images hit the API limit, the user's taste beats the AI's). Before step 7 commit the AI does only a **logic-consistency self-check** per `report_style_spec.md §3.13 4-item chart-script self-check` (title number matches in-chart data, annotation colour not same as the plot below it, horizontal-bar y-tick labels fully shown, legend centered and laid out horizontally); any chart that fails must have its script fixed and re-rendered before commit. The visual self-check itself is left to the user reading the PDF at step 9d.

**Soft stop plus three quality gates**: after all charts land, tell the user; the user reviews JPGs and gives feedback any time, default non-blocking into step 8. The three gates the AI self-checks: (1) spec §3.13 4-item chart-script logic self-check all pass; (2) each chart passes the add criteria and does not trigger the remove criteria (see "judge before charting"); (3) any issue exposed in self-check is fixed and re-rendered. The gates are commit-time AI self-checks, not a hard-stop gate.

Visual problems (caliper conflicts, unit mismatches, annotation misplacement) surface most easily when the user reviews JPGs; the user can stop and go back to step 7, then proceed to step 8. The user's PDF read at step 9d is the final visual review.

**Pitfall warnings**:
- For cross-country / cross-source comparison, explicitly record caliper differences. A 20+ percentage-point gap for one country under two calipers (nominal vs constant price, with vs without a sub-item) is common.
- Do not force incomparable-caliper metrics onto one "target vs actual" chart; it misleads the reader.
- When citing an institution's KPI, open the official site to confirm (the core lesson of the "Vision-target mix-up" counter-example above).

---

### Step 8: draft writing (default one continuous pass, soft stop)

**Key question**: organise charts and documents into report language.

**Lead**: Claude solo throughout (first draft + self-polish + format / render tuning). critique is left to step 9.

**Writing discipline**: when Claude writes, **follow §7.1 and §7.1.1 strictly**, targeting a step 8 final quality equal to third-party-edited prose. The 7 rules of §7.1.1 (same-theme continuation, list expansion, embedded take-away, unit standards, written-register wording, numbered lead-ins, no technical symbols as conjunctions) are reverse-engineered from DS-polishing field practice; Claude applying them proactively achieves no-third-party-polish first-draft quality, so step 9 no longer needs a DS text-polish stage.

**Default: one continuous draft**: Claude writes all chapters in outline order, then hands the full v1 to the user for one review. The rationale is that the outline was hard-stop-signed at step 6, take-aways are locked, per-section stop-and-review costs far exceed the value, and fatal errors are caught by step 9b critique.

**fallback: per-section hard stop** (enabled on explicit user request). Stop after each section for user review before writing the next. Fits: outline not fully locked, take-aways still adjusting, user wants deep involvement in each section's argument-flow calibration.

**Cost comparison of the two paths** (measured on the Saudi project):

| Dimension | per-section hard-stop fallback | one continuous default |
|---|---|---|
| step 8 user review time | N reviews (1 per section) | 1 (after the full draft) |
| step 8 total time | long, gated by user response pace | short, AI usually finishes in 1 hour |
| step 9b critique integration | low, each section already reviewed | **high, ~3x**: ~30 revisions measured (5 fatal, 11 serious, 19 minor, 18 chart-script errors, 3 CSV errors), 9b integration ~half a day, 9 commits |
| step 9 commit count | usually 1-3 (B1, B2, B3 merged) | 9+ (fatal, serious, minor, chart-script each multiple) |
| style and argument-flow rework cost | low, each section reviewed | high, only the full draft reveals a wrong section's argument flow to redo |

**Extra note in single-LLM mode**: in single-LLM mode 9b is Claude self-critique, weaker independence than multi-LLM GPT critique. The one-continuous-pass cost has reduced safety-net ability in single-LLM mode; if the user is sensitive to fatal errors, consider the per-section hard-stop fallback.

**Operating order**:
1. Claude writes the first draft per section (v1.0), **self-checking the §7.1.1 6 rules per section** (period continuation / list colon / embedded take-away / "ppts" → "percentage points" / written connectives / numbered lead-ins). Also **per-section depth self-check against the outline contract**: each section carries its planned chart(s) and is more than the 1-2-paragraph laziness signal (step 4); a section that came out thinner than its contract take-away promised goes back to step 5 / 7 for more material, it is not padded with filler.
2. After each section's v1, hand the user "structure + data + argument".
3. After the full v1.0, do render / font / YAML tuning (v1.1 → v1.x); the body does not change.
4. The step 8 final = Claude's pure version, **snapshot to `_process/draft_v1_claude.qmd`** (this must land before step 9 changes text, or there is no "pure Claude baseline" to revert to).
5. Proceed to step 9 (GPT critique → verifying → user sign-off).

**Pre-writing self-check list** (run when each section's v1 is done):

| Redline | Check command | Expected |
|---|---|---|
| Em-dash `——` | `grep -c "——" draft.qmd` | 0 |
| h3 and deeper titles | `grep -nE "^#{3,}" draft.qmd` | 0 lines |
| Hand-written §N title prefix | `grep -nE "^#{1,3} §" draft.qmd` | 0 lines |
| emoji | `grep -cP "[\\x{1F300}-\\x{1F9FF}\\x{2600}-\\x{27BF}]" draft.qmd` | 0 |
| Unescaped `$` (English drafts) | `grep -nP "(?<!\\\\)\\$" draft.qmd` | 0 (write amounts as `\$`) |
| leftover ppts | `grep -c "ppts" draft.qmd` | 0 (change to "percentage points") |
| lyrical padding | spot-check "实际上 / 事实上 / 值得指出的是" | delete |
| Quarto render | `quarto render draft.qmd` | success |
| **chart-script / CSV / body three-way consistency** (new) | for each `![...](fig_X_Y_*.pdf)`: grep the body number used + grep `make_fig_X_Y_*.py` title / source / note + check the CSV field, **pass only if all three agree** | all pass |

**How to do the "chart-script / CSV / body three-way consistency" check**:

When a section cites a chart (e.g. "fig_X metric rose from A to B"), verify item by item:

1. Are the body numbers "16% / 24%" actually in CSV `s1-3_non_oil_exports_progress.csv`?
2. Do title / source / note in `make_fig_X_*.py` also write those two numbers? If so, consistent?
3. Does the rendered fig PDF (open the JPG) show axis values / data labels matching 16% / 24%?

If anything disagrees, **fix it in that section**, do not defer it to step 9b GPT to catch (this project's 9b once found 18 chart-script strings inconsistent with CSV / body — proactive saves 3x the work of reactive).

**Finalise count-gate (anti-slacking, see §7.4)**: after the full v1 draft, before handing it to the user, run the §7.4 count-gate and **paste the actual measured numbers** (pages, charts, words) into your report-back, exactly like the grep redlines. The signed step-6 outline contract and the heavy band (30-40 pages / 25-35 charts / 15k words) are the floor. **If any dimension is clearly below floor (< 25 pages or < 20 charts, per step 4), do not declare the draft complete** — state which dimension is short and go back to step 5 (more search) / 6 (more chapters) / 7 (more charts). The gate is cleared only by genuine coverage depth: do **not** close the gap by padding (lyrical filler, restating a point, splitting one argument into choppy paragraphs) or by fabricating numbers (§5.2). If the real material honestly cannot reach the band, say so to the user explicitly rather than padding — but a heavy report landing far below the band almost always means the step 5 search or step 6 outline was too shallow, not that the topic is exhausted.

**Process-draft landing** (see the §11 `_process/` guide): step 8 minor versions (v1.0 / v1.1 / …) iterate in place in `draft.qmd`; major versions (v1 final → v2 → v3) land under `_process/draft_<vX>_<who>.qmd`. **`draft.qmd` always points to "the current shippable latest version".**

---

### Step 9: refine (critique, verifying, user sign-off; soft stop plus 9d hard stop)

**Key question**: does the full draft hold up? Are all caveats reconciled? Does the user finally accept it?

**Three sub-steps in series**:

- **9b · critique and Claude's three-batch integration into v2** (two tracks by LLM mode)
- **9c · verifying skill checks unresolved caveats, lands v2.x**
- **9d · user sign-off** (hard-stop gate)

Sub-step numbering keeps 9b / 9c / 9d, not renumbered to 9a / 9b / 9c, to stay stable against earlier versions for cross-version reading. The original 9a DS text-polish sub-step is removed in this version (the DS teaching value is distilled into §7.1.1, Claude applying it at step 8 achieves equal quality).

**Version-number convention**:

- step 8 final = v1
- 9b integration = v2
- 9c verifying = v2.1
- 9d user revision = v2.2 / v3 / v3.2 / ... iterate until sign-off
- core principle: v major = completed sub-steps, v decimal = iteration rounds within the same sub-step

---

#### 9b · critique and Claude's three-batch integration into v2 (two tracks)

**Two-track flow** (by the LLM mode locked at onboarding):

##### Single-LLM mode (default): Claude self-critique

1. In a separate conversation or context, Claude **reloads the step 8 final** (to avoid context bias) and self-critiques the whole draft against the 6 perspectives below, producing a critique list in `_process/critique_v2_self.md`:
   - **Facts and data**: every number, year, person, institution must trace to an original source, the citation key really in `references.bib`
   - **Cross-section caliper consistency**: the same metric's number, unit, caliper consistent across sections
   - **Citation support**: `[@xxx]` genuinely supports the statement (no bait-and-switch)
   - **Argument flow**: sections connect, conclusions support level by level
   - **chart-script / CSV / body three-way consistency**: chart title, source, note aligned with CSV data and body citation (this project once exposed 18 inconsistent chart-script strings at once, a high-frequency pitfall)
   - **Language standards**: see §7 writing standards
2. Claude integrates the critique list in batches B1 / B2 / B3
3. one commit per batch + decision log → `_process/v2_integration_log.md`

**Weak independence in single-LLM mode**: Claude self-evaluating its own draft has no second perspective, higher risk of missing a fatal error than multi-LLM. Three hedges:
- still handle key facts per the "don't blindly trust" principle below, independently reading the original material to verify
- run 9c verifying rigorously, no shortcuts
- the user reads the derivation once more before publishing

##### Multi-LLM mode: GPT critique

1. hand the step 8 final to GPT
2. GPT produces a full critique → `_process/critique_v2_gpt.md`
3. Claude integrates in batches (**> 30 critique items split into three batches, < 30 single batch**)
4. one commit per batch + decision log → `_process/v2_integration_log.md`

**Critique independence principle**: the 9b critique LLM and the step 8 lead LLM do not overlap. In multi-LLM mode step 8 is Claude solo, 9b is GPT critique, independence is satisfied. **Do not use DS critique** (GPT independence is enough, and DS cannot see the PDF, a structural blind spot).

##### Integration batching and the "don't blindly trust" principle (both modes)

**B1 / B2 / B3 three-batch classification**:
- **B1 · light fixes**: language-standard redlines ("ppts" → "percentage points", Chinese-English mixing, lyrical padding) and chart-script / CSV / body "hard number consistency" errors
- **B2 · fatal and serious**: fact-layer, caliper-layer, citation-layer revisions. Key fact judgements Claude must **independently verify** (read the original material), not blindly trust critique; lean toward "downgrade + add caveat", preserving information density while making uncertainty explicit
- **B3 · chart-script string revisions + re-render all + PDF verification**

The human does not adjudicate the B1 / B2 / B3 classification; trust Claude's three-tier handling + post-hoc audit of the decision log.

**Claude's "don't blindly trust" principle when integrating**: for key fact judgements from critique ("number wrong", "source does not support"), Claude must **independently read the original material to verify**. Three handling directions:

- after verifying, judge the critique correct, revise per critique
- after verifying, judge the critique wrong, record the rejection reason in the decision log, keep the original text
- after verifying, judge the critique partly correct, downgrade the strong conclusion to "per media report" / "this study's estimate" / "source pending" caveat wording, preserving information density

Redline: critique is a reference, not collage material. When Claude integrates critique, it must rewrite in a unified narrative voice so the reader cannot tell "which paragraph is from which".

---

#### 9c · verifying skill checks unresolved caveats, lands v2.x

**Trigger**: the 9b decision log usually lists a set of "downgraded to media citation / marked caveat / source pending" citations; these are bypassed by 9b's "downgrade handling", not closed. 9c checks each rigorously with the `market-research-skills:verifying` skill, upgrading what can be upgraded and keeping caveats on what cannot be verified into 9d.

**Flow**:

1. extract all unresolved caveats from the end of the 9b decision log `_process/v2_integration_log.md`
2. call the verifying skill per item:
   - **can find primary (read the full text from a whitelisted source)**: upgrade, remove caveat
   - **multi-source-converging to primary** (e.g. the original site is Cloudflare-blocked, but several whitelisted media cite the same official release): upgrade to "multi-source converging", stating "original site not directly accessed, citation from X, Y, Z"
   - **genuinely cannot find primary**: keep the caveat, add "attempted to verify, not public" explicitly
3. sync the related chart-script strings (source and note) if the source is upgraded
4. produce v2.1 (or v2.x) and the decision log `_process/v2_1_verifying_log.md`

**Why this is a separate sub-step, not part of 9b**:

- 9b critique's "downgrade" handling is a low-cost action; integration cannot stop per item to deep-search the original source
- 9c handles all caveats centrally, running the verifying skill's strict protocol (whitelist, download primary, multi-source converging) once
- 9b integration producing v2 is "accept critique feedback", 9c producing v2.x is "the final fact-layer gate". Splitting the two keeps the commit history and decision log clearer

**verifying field lessons**:

- the same number, statement Z (e.g. "institution X's A metric target \$80B") and source Z' (e.g. "another related B metric target \$80B") may match on the number but be **completely different calipers**. When verifying, identify whether the two are really the same metric, not just that the numbers match.
- a vague "YYYY month MM" time point easily anchors to the first concentrated burst rather than the first report. When verifying, change the time point to a range ("early YYYY") for robustness.
- whitelisted-media multi-source-converging to primary and "unspecified media citation" are two different levels; the former is equivalent to primary, the latter must be downgraded.

---

#### 9d · user sign-off (hard stop)

**Key question**: after the user reads the v2.x PDF, are there problems only a human perspective can find?

9d is the last gate of step 9, **hard stop**: Claude cannot skip 9d to step 10.

**Flow**:

1. after re-rendering the v2.x PDF, Claude hands `7_draft/draft.pdf` to the user
2. the user **reads the full PDF**, focusing on:
   - does the argument flow hold (human read vs LLM-critique blind spots)
   - chart visual effect (spec §4 says the AI does not do visual checks, 9d is the only visual-self-check moment)
   - target-reader immersion for the WeChat or LinkedIn derivation (target reader test)
   - whether wording or stance needs softening or strengthening (the critique LLM does not know the user's real intent)
3. the user produces a revision list (verbal, written, or direct PDF annotation)
4. Claude integrates into v2.2 / v3 (version number by change size)
5. 9d may iterate (v3 → v4) until the user is satisfied
6. the user signs off, 9d passes, proceed to step 10

**Hard-stop criterion**: the user explicitly says "proceed to step 10" (written, or commit message, or state.md entry).

**Difference between 9d and step-10 landing announcements**:

- 9d sign-off is the step-9 hard-stop gate; the user reviews the "content + visual" state and decides whether to freeze the main PDF
- step 10 announces after each sub-step lands (soft stop); derivations are format conversion, content changes go back to 9d

If 9d keeps changing the main report, step 10 has not started.

---

**Whole step soft + 9d hard**: 9b and 9c may iterate (v2 → v2.1 → iterate), soft. 9d is hard.

---

### Step 10: finalise + derive (soft stop, announce after each sub-step lands)

**Key question**: are all channel versions ready?

**Four sub-steps in series**:

- **10a · freeze main PDF**
- **10b · Word derivation**
- **10c · publication-style HTML + PDF** (optional, when the audience needs stronger visual identity)
- **10d · WeChat JPG slices** (optional, after 10c, for the WeChat long-form channel)

Announce after each sub-step lands, soft stop, iterable. No hard-stop gate for the whole step: derivations are format conversion, content was locked at 9d sign-off, no reverse revision in the derivation layer. If the user finds a content problem in a derivation, go back to 9d.

---

#### 10a · freeze main PDF

Re-render qmd → PDF once, confirming layout, citations, charts, TOC numbering, list-of-figures all error-free. The final version lands in `7_draft/draft.pdf`, git-tag the frozen version (e.g. `v1.0-release`). Before tagging, **re-confirm the §7.4 count-gate against the signed step-6 contract** and record the final page / chart / word counts (it should already pass from the step-8 gate; this is the last backstop). A frozen PDF below the floor or short of the contract goes back to step 5/6/7 first — it does not get frozen and shipped thin.

All 10b-10d derivations copy content from this frozen qmd; **no reverse revision in the derivatives**. If a content problem must be changed during 10b-10d, go back to step 9d to re-run sign-off and re-freeze the main report.

---

#### 10b · Word derivation

**Purpose**: a docx for clients, bosses, partners who need Word for review or annotation. The WeChat long-form goes the 10d JPG-slice path, not covered here.

**Tool**: Quarto's built-in docx output, no external tool. One command:

```bash
quarto render draft.qmd --to docx
# lands 7_draft/draft.docx (or 8_publication/1_word/<project>.docx, tidier to move there)
```

**Auto-handled**:

- charts (fig PDF / JPG) auto-embedded
- tables converted to native Word tables
- citations handled by Pandoc (bib metadata works)
- paragraphs and heading levels preserved

**Needs downgrade handling**:

- **figsource / tblsource custom LaTeX envs fail in docx** (LaTeX-only). Two handlings:
  - simple: ignore; the figsource / tblsource blocks show empty or as raw text in docx, not affecting review content
  - clean: in the qmd use a `{=docx}` conditional block or change `\begin{figsource}...\end{figsource}` to markdown raw (e.g. `> Source: ...`) for dual-output compatibility
- formulas (if any LaTeX math) render as images
- custom headers/footers need a `reference-doc:` field pointing to a .docx template (unspecified = Pandoc default)

**Brand template (optional)**:

For a project-branded Word style (fonts, headers, footers), add to the qmd front matter:

```yaml
format:
  docx:
    reference-doc: <project root>/reference.docx
```

reference.docx is a Pandoc style template (first `quarto render --to docx` a default, adjust the style in Word as needed, save as reference.docx). Not needed if the default style is enough.

**Landing location**: `8_publication/1_word/<project>.docx`.

**Derivation discipline**: like 10c HTML and 10d JPG slices, docx is format conversion; content changes go back to 9d, not in 10b.

---

#### 10c · publication-style HTML + PDF (optional)

Do this only when "content is signed off + the audience needs stronger visual identity (consulting style, magazine style, social sharing)". Full spec in `report_style_spec.md §7`. Lands `8_publication/2_HTML/`.

**Starting moves (two paths, see spec §7.1)**:

- **Path A (default)**: copy the skill's `scripts/publication-style-template.html` to project `8_publication/2_HTML/<project>-publication-style.html`, replace placeholders per the spec §7.8 content-mapping table, manually tune pages in VS Code Live Preview per §7.3
- **Path B**: call the `consulting-report-style` skill to generate another consulting style (BCG green, McKinsey blue, etc.) as the template, then fine-tune per §7 sub-sections

Key points (see spec §7, shared by both paths):

- the qmd is the source of truth, the HTML is a derivative; no content revision on the HTML
- embedded figures must use `fig_*_clean.jpg` (not `fig_*.jpg`, else double title)
- each page div is one A4; over/under-flow tuned manually in VS Code Live Preview (no auto-reflow)
- HTML → PDF directly via the browser's Cmd+P "save as PDF", turn off "headers and footers", margins "none"
- after one generation, switch to manual maintenance; do not keep a builder script

---

#### 10d · WeChat JPG slices (optional)

Slice the 10c publication PDF into per-page JPGs for the WeChat long-form editor (it does not take PDF directly but supports image sequences natively). Lands `8_publication/3_wechat_pages/page_NN.jpg` (zero-padded two digits). Full spec in spec §7.9.

Do this only when the WeChat long-form channel is needed. Short pieces use 10b's md + single-figure placeholders.

---

**Whole step soft stop**: announce after each sub-step lands. No explicit hard-stop gate; the user can stop and go back to 9d at any time.

---

### Step 11: retrospective (append anytime + one-time project-close audit)

**Key question**: what did we learn? Which lessons promote to the analyst-research/ three-piece set?

**Two-layer mechanism**:

- **11.1 append anytime**: pitfalls / lessons / experience found during the project land in the retrospective immediately
- **11.2 one-time project-close audit**: after step 10 is fully signed off and before the next project, audit the four-way consistency of workflow / spec / CLAUDE.md / retrospective vs the actual output, and consolidate promotable experience

---

#### 11.1 append anytime

**Trigger conditions** (any one appends):

- append right after each section is synthesised (do not wait for a "consolidated retrospective")
- the user explicitly says "this is a pitfall / lesson / experience" in conversation
- the AI itself identifies a recurring class of problem
- log one line in the retrospective each time a CLAUDE.md entry is made (note which rule, the original trigger)

**Format**: three-part (see §10). **Path**: `9_retrospective/retrospective.md`.

---

#### 11.2 one-time project-close audit (after step 10 is fully signed off)

**Principle**: do not repeatedly audit / promote the workflow itself during the project; do it once at step 11.2 after the flow is stable. Frequent audits make the workflow / spec accretion pace track the development pace, becoming overhead. Append retrospectives anytime during development; whether to promote is adjudicated at 11.2.

**Three actions**:

1. **distil the retrospective into a next-project improvement list**: read all entries in `9_retrospective/retrospective.md`, distil cross-entry recurring patterns into 3-5 core take-aways in the file's final "project-close summary". Focus on "what to do differently next project", not a running re-statement
2. **adjudicate project CLAUDE.md → workflow promotion**: adjudicate each item in the project CLAUDE.md "deviations from the framework" section as "(1) keep in project / (2) promote to the analyst-research/ three-piece set". Promoted items sync into workflow.md or spec, with a note at the project level "promoted cross-project to workflow §X.Y"
3. **grep audit of the three-piece set + actual output**:
   - grep workflow / spec section-number cross-references against actual chapters (avoid section-number drift)
   - grep the three-piece set for stale phrasing ("dual output / dual format / old dir name")
   - compare actual output (e.g. the real `8_publication/` structure, `5_scripts/` scripts) vs the spec description, fix inconsistencies item by item

**Completion criterion**: all three actions done, git-tag the close version (e.g. `final-v1`) before declaring the project closed.

**When not to do 11.2**: a one-off experimental project (not reusing the workflow) / a validation run (not producing a formal report). All other cases should, or the workflow gradually drifts from accumulated experience.

---

## 5. Cross-cutting discipline

These do not belong to any single step but apply to all.

### 5.1 Source traceability

Every number must trace to an original source. Mark what cannot be located "to be verified" or drop it; do not write it into the conclusion.

### 5.2 No fabricated numbers

"Not publicly available / to be verified" beats a plausible guess.

### 5.3 Three-state labelling

**Fact** (directly supported by an original source):

- "per IMF 2024 Article IV, X is Y"
- "after the GASTAT 2025-05 revision, X is Y"
- "PIF annual report 2024 page 15 discloses X is Y"

**Estimate** (a calculation based on a formula or someone else's estimate):

- "per market estimate ~X" (multiple media or bank calibrations)
- "this study estimates X" (re-computed by a known formula or simple calculation)
- "re-computed by the IMF formula, X" (state the formula used)

**Inference** (directional judgement with no direct data support):

- "possibly X"
- "directional judgement X" (state that no absolute value is given)
- "current evidence leans toward X"

Strictly distinguish the three with distinct wording and labels; do not mix them in the body (so the reader does not mistake inference for fact).

### 5.4 AI output ≠ conclusion

The AI provides material and a first draft; the human decides the final conclusion. After each hard-stop output the AI can say "I think this step is done, awaiting your review", but cannot declare "done" and proceed on its own.

### 5.5 Double-landing

For every chart / table involving data processing (cleaning, aggregation, statistics, visualisation), **must** save together:
- the underlying data (CSV / GeoJSON / raw download) to `4_data/`
- the full script to `5_scripts/`
- the chart PDF + JPG + `_clean.jpg` to `6_figures/` (all from one `save_fig` call)

### 5.6 CSV write hygiene

- fields containing commas / quotes / newlines must be double-quoted
- the source column is named `sources` (plural) uniformly, multiple sources separated by `;`, not `,` (conflicts with the field separator)
- **dates in ISO 8601**: `YYYY-MM-DD` (e.g. `2024-12-31`), not Excel-style `12/31/2024` or `31-Dec-2024`. Year-only annual data writes `2024`
- **no thousands separators in numeric fields**: write `1234567`, not `1,234,567` (the thousands comma is misread as an extra column by the csv parser). Add thousands separators with a Python f-string when displaying to the reader
- after each synthesis, validate once with `csv.DictReader`: column alignment + key-field value types as expected

### 5.7 Cross-stage decisions are made by the human

The AI can lead execution within each step, but **"whether to proceed to the next step" must be the human's decision**. Quality gates are for the human, not AI self-assessment.

### 5.8 Hard cross-section number consistency

The same metric's number, unit, and caliper must be identical in five places:

1. **outline.md** planned numbers and arguments
2. **draft.qmd** body numbers
3. **make_fig_*.py** title / source / note / annotation numbers
4. **4_data/2_processed/*.csv** underlying data fields
5. **references.bib** the original number behind the citation key

Any edit to one (change base period, source, time point) must **reconcile all five**.

**Field lesson**: a project's step 9b critique once exposed 18 chart-script strings inconsistent with CSV / body (18 / 41 = 44% of the project's charts). Root cause: step 7 title numbers hardcoded rather than derived from CSV, step 8 body numbers changed without syncing the script.

**Prevention discipline** (echoing the §step 7 / §step 8 self-check lists):

- at step 7 charting: `title=f"{df.loc[...].max():.1%}"` derived from CSV, no hardcode
- at step 8 writing: re-check the CSV when each paragraph cites a specific number
- at step 9b critique: the B1 light-fix batch specifically checks "chart-script / CSV / body / bib" four-way consistency

---

## 6. Multi-LLM collaboration mechanism

### 6.1 Which steps need multi-LLM

The onboarding §1.3 Step 1 user decides "whether to use multi-LLM collaboration", locked throughout. Collaboration per step in the two modes:

| Step | Single-LLM (default) | Multi-LLM |
|---|---|---|
| 2 broad search | Claude solo, with iFinD MCP or `financial-data-sources` skill and user-supplied key PDFs | Claude + GPT + DS three parallel, Claude synthesises |
| 5 supplementary search | Claude solo with user-supplied key full-text documents | three parallel (focused sub-questions), Claude synthesises |
| 6 outline chart brainstorm | Claude one draft, user decides | three propose, Claude synthesises |
| 7 data scripts charts | Claude solo | Claude solo |
| 8 draft lead | Claude solo (self-polish per §7.1 and §7.1.1, target quality equal to third-party-edited) | Claude solo |
| 9b critique | Claude self-critique (6 perspectives: facts, calipers, citations, cross-section consistency, argument flow, language standards), three-batch integration | GPT critique, Claude three-batch integration (B1 / B2 / B3) v3 |
| 9c verifying | Claude solo calls the `market-research-skills:verifying` skill (both modes) | same |
| 9d sign off | user reads PDF, iterates to sign-off (both modes) | same |

**Weak independence of single-LLM self-critique**: Claude self-evaluating its own draft has no independent second perspective, higher fatal-error risk than multi-LLM. Three hedges: (1) the user reads the derivation once more before publishing; (2) key facts still independently verified against the original material per the 9b handling framework; (3) run 9c verifying rigorously, no shortcuts.

**Switching cost of multi-LLM mode**: the user must manually switch to the GPT plugin or web app for critique, a significant rhythm cost. Enable only when the user explicitly asks or the project expects high GPT-independent-critique value (complex cross-source comparison, dense key numbers, a second perspective needed before external publication).

**DS no longer default**: field-measured DS text-polish teaching value is distilled into §7.1.1, Claude self-polishing per the rules achieves equal quality; DS critique in multi-LLM mode is handled by GPT (GPT independence is enough). DS remains a possible future fallback, not on the default path.

### 6.2 Relative strengths of the three (field observation, iterating)

| Tool | Strength |
|---|---|
| **GPT** | structured frameworks, data precision, caliper analysis, research-discipline prompts |
| **DeepSeek** | historical tracing, Chinese / regional context, time series, visual detail, original terminology. **The teaching value of Chinese long-sentence rhythm / connectives / naturalness is distilled into §7.1.1** (learned from DeepSeek polishing); step 9 default no longer calls DS, Claude applies §7.1.1 directly at step 8; DS remains a step-9 fallback (enabled when GPT critique exposes ≥ 10 "clearly needs improvement" text items) |
| **Claude** | data archive, web scraping, report argument flow, synthesis finalisation, end-to-end referee |

Model-generation turnover changes this table; the user updates the observation in the project CLAUDE.md after each project.

### 6.3 The redline of synthesis

Do not stitch three LLMs' text. The synthesised piece must be rewritten in a unified narrative voice so the reader cannot tell "which paragraph is from which". The three originals' value is in the material, not the sentences.

### 6.4 State machine for multi-LLM concurrency

If running multi-LLM collaboration in Claude Code (via sub-agent or manual switching), during concurrency each LLM **produces only under its own subdir** (e.g. `_process/<llm>/`), not directly editing shared state files (outline.md, `_state.md`). Shared state is updated by the synthesiser (Claude) at the end of each round, avoiding last-write-wins conflicts.

### 6.5 Error-diagnosis order: model → prompt → channel

When a cross-LLM / cross-tool call fails, locate the root cause in this order, do not jump around:

1. **Model layer**: is the model itself compatible with the scenario? Key questions:
   - is it a Thinking / reasoner / o-series (long reasoning silence, conflicts with the streaming middle layer)?
   - is the context window insufficient?
   - is the model version too new / too old, tool-call schema mismatch?
2. **Prompt layer**: is the prompt design reasonable? Key questions:
   - task too big / output too long, split?
   - prompt redundant / containing special characters triggering escape problems?
   - output-format constraints the model can follow stably?
3. **Channel layer**: is the access channel stable? Key questions:
   - VSCode Copilot / Claude Code CLI / browser, which link?
   - network / proxy / VPN anomaly?
   - middle layer (Copilot streaming gateway) stream-break?

**Counter-example (field DS debugging pitfall)**: after 3 consecutive DS failures, Claude jumped straight to "prompt too long", shrank the prompt and failed, then jumped to "channel unstable" and recommended switching to Cline. The actual root cause was the user selecting `DeepSeek V4 Pro (Thinking Max)` (model layer); switching to the regular version worked immediately. The 4 wasted rounds were because the model layer was not checked first.

A stack-trace signature is also a misleading trap: `Copilot Request id` in the trace only means Copilot handled the request, not that Copilot is the root cause.

---

## 7. Writing-standards template (companion)

This section is a domain-agnostic writing standard; each project CLAUDE.md can inherit + specialise.

> The examples below illustrate Chinese-prose redlines (they apply when the report is Chinese); the rules apply to both languages. For English reports, apply the spirit (short sentences, no padding, no body bold) with English idiom and skip the Chinese-colon items.

### 7.1 Style

**Scope**: main report, derivations (Word, HTML, WeChat long-form), retrospective docs, and the text-expression parts of AI conversation replies. The main rules and sub-sections §7.1.1 / §7.1.2 / §7.1.3 share this scope. The AI also writes per these rules when conversing with the user, avoiding "→", "+", "half-width - as em-dash", "使得 / 不难看出 / 一定程度上" colloquial / AI-generated / academic residue.

- the target reader is an undergraduate-educated non-specialist with basic economics, also serving professional readers
- **the report body has h1 / h2 only, no h3 and deeper** (see `report_style_spec.md §1.2`). When a section has too many points to need h3, split it into two h1
- each h2 subtitle is that passage's conclusion, e.g. "Fiscal view, the three-tier 30%-90% oil-and-gas share of fiscal revenue". Do not write empty titles like "Fiscal view"
- a paragraph leads with a specific conclusion, e.g. "By official calibrations, GCC non-oil GDP share has risen to 65-80%". No lyrical padding like "discussing X requires an intuitive judgement" / "it is worth noting"
- **keep sentences short**. Avoid long, convoluted complex sentences; one long compound sentence split into two or three short ones reads better. Prefer sentences under 20 characters
- **the body has zero bold**. Bold is for "lead-ins" only: titles (h1 / h2), keyword labels, abstract lead-in, table headers, in-table category labels. Argument paragraphs (incl. take-away / core numbers / key judgements) are never bold; key info is carried by the leading conclusion sentence, h2 titles, tables, visualisation
- prefer continuous prose, use bullets cautiously. Bullets only in three cases: (1) genuinely different dimensions in parallel; (2) a 5+ item list; (3) a list needing visual comparison where a table is inconvenient. Argument content must be paragraphs, not smashed into bullets
- place citations near the corresponding data, do not pile a string of names (Hamilton 1983, Kilian 2009, Mohaddes-Pesaran 2017, Berument 2010, Cherif 2014…) into one paragraph. A "literature-review wall" loses the lay reader
- short paragraphs, one argument each, usually 3-5 sentences. Over 5 sentences consider splitting
- no hypothesis-testing language. Academic-paper skeletons like "H1.2.2 strongly supports", "hypothesis, verify, evidence", "sub-hypothesis…" are all deleted in the main report
- **no invented metaphors**. First drafts often borrow self-invented metaphors ("steel floor", "narrative soft-landing", "accounting magic") for shorthand, but the reader lacks the author's context and re-reads twice, reducing readability. Before finalising, replace each self-invented metaphor with a methodology or industry-standard term so the reader without context understands in one read, e.g. "steel floor" → "hard caliper", "narrative soft-landing" → "lowering or redefining". Only in the intro or conclusion as a hook may a few established industry metaphors stay (e.g. the IMF's own moving goalposts, Dutch disease); body argument uses hard terms
- **the abstract, intro, conclusion must be separately rewritten in a second pass**. These three are "framing paragraphs" carrying the reader's first and last impression. The version written in one pass is usually fragmented, lacks insight, lacks outlook, and the reader cannot grasp a take-away. Before finalising, rewrite these three separately with three goals: (1) remove lyrical padding and rambling, (2) add one core insight (a judgement the reader walks away with), (3) the intro adds an argument map (what this report argues, in what order), the conclusion adds an outlook (which variables to watch in coming years)

#### 7.1.1 Chinese long-sentence rhythm (learned from DeepSeek polishing)

"Keep sentences short" means not writing complex clauses, **not** "break the same argument's supporting detail with periods". Claude's common first-draft anti-pattern is cutting an argument's evidence and take-away into multiple independent short sentences, too choppy; a co-existing anti-pattern is using technical symbols like "→", "/", "+" for written connectives, fast but forcing the reader to mental-decode. The 7 rules below are executable details distilled from DS polishing + field practice; follow them directly when writing the first draft:

1. **continue same-theme supporting sentences with commas / semicolons**, not periods. `「升至 30%。这是真改革。」` → `「升至 30%，这是真改革。」`
2. **list multiple sources / items in "主句：项 1，项 2，项 3。" one go**, not "four numbers. item 1. item 2. item 3."
3. **embed "这是 X / 这意味着 Y" independent short sentences**: continue the take-away into the previous sentence with a comma, joined with the evidence, not a new sentence. Similar phrases like "也就是说 / 换句话说 / 简言之 / 总之" handled the same
4. **number-unit standards**: `ppts` → "个百分点"; small numbers (≤ 10) for years / counts in Chinese characters "九年" "四年" "五项"; shares / years / amounts still in Arabic numerals (`76%`, `2024 年`, `\$92`)
5. **written-register connective preference**: "原因是" → "原因在于"; "亮点是 / 制约是" → "亮点在于 / 制约在于"; "而不是" → "而非"; "已经" → "已"; "悄悄" → "悄然"; "升到" → "升至"; "降到" → "降至"
6. **3+ parallel arguments lead with numbers**: "第一... 第二... 第三..." so the reader keeps the rhythm; two items still "一是 / 二是" or "一方面 / 另一方面"
7. **no technical symbols like "→" "+" "/" "∴" "vs" for connectives**. These are fast in todos / notes / chat but force a mental-decode in report prose, sharply reducing readability. "A → B" → "A 引致 B" or "A 之后 B"; "A + B" → "A 与 B" or "A 加上 B"; "A / B" → "A 或 B"; "A vs B" → "A 与 B 的对照". List with full sentences, not "项 1 / 项 2 / 项 3". The first draft may use symbols as placeholders; grep-replace all with full written expressions before finalising

§7.1 main rules (short sentences / no padding / zero body bold) still take priority. This sub-section only refines the "same-theme expansion rhythm".

#### 7.1.2 Framing-paragraph spec (abstract + intro + conclusion)

The last §7.1 main rule requires rewriting the abstract, intro, conclusion in a second pass. This section gives the structure templates and mandatory elements, so the second-pass rewrite after step 8 / step 9b has a clear target.

##### Abstract

- **length**: 300-500 characters, 3 paragraphs + keyword line
- **structure**:
  - **para 1 topic and angle**: 1 sentence naming the research object, 1-2 sentences of key background numbers
  - **para 2 core evidence and take-away**: 2-3 sentences laying out the core argument (this study's framework and key findings)
  - **para 3 keyword line**: `**关键词**：` 5-7 concrete nouns, separated by `|` (see spec §1.4)
- **anti-patterns**:
  - writing the abstract as a body TOC
  - "this study will…" preview style (give the conclusion, not a preview)
  - hanging an academic hypothesis number in the abstract
  - "另外" "此外" "同时" between paragraphs (means the take-away did not close)

##### Intro

- **length**: 2-3 paragraphs
- **structure**:
  - **para 1 phenomenon setup**: why this question is worth studying, give a contrast or tension
  - **para 2 argument map**: "this study will … chapter 1 … chapter 2 … the conclusion synthesises …" make the argument path explicit, so the reader at chapter 3 still knows where they are
  - **para 3 relation to existing research (optional)**: this study's contrast or contribution vs the literature
- **anti-patterns**:
  - writing the intro as a long background, three paragraphs all history without an argument map
  - opening with empty phrases like "众所周知" "不可否认" "在此背景下"
  - writing the argument map as vague promises like "希望" "试图"

##### Conclusion

- **length**: 2 paragraphs
- **structure**:
  - **para 1 core take-away wrap-up**: 1-sentence leading conclusion, 1-2 sentences of condensed evidence
  - **para 2 outlook**: which key variables to watch in coming years, a forward-looking frame for the reader
- **anti-patterns**:
  - writing the conclusion as a pure "as stated above…" summary
  - only restating without a new judgement or outlook
  - a conclusion so short it is one paragraph or one sentence (if info density is low, better no conclusion)

##### Timing of the second-pass rewrite

In step 8's one-continuous-pass draft these three are usually weakest, because the argument flow is still forming. After step 8 wrap-up or step 9b integration, **separately rewrite these three**, not iterating in sync with the body. After each rewrite, run the anti-pattern list above and rework on a hit.

#### 7.1.3 Chinese written-register lookup table

§7.1.1 rule 5 "written-register connective preference" gave a few; this section expands it into a full table. Claude writes the right column directly in the first draft, saving the step-9 text-polish stage. Three categories.

##### Category 1: colloquial → written

| colloquial | written | note |
|---|---|---|
| 使得 | 使、让 | "使得" is a redundant "使" |
| 采取了 | 采、采用 | delete redundant "了" |
| 进行了 X | direct verb (X) | "进行了研究" → "研究" |
| 给出了 X | 给 X、提出 X | delete redundant "了" |
| 实现了 X | 达成 X | |
| "了" "过" meaningless particles | delete where tense is unaffected | e.g. "数据公布了之后" → "数据公布之后" |

##### Category 2: academic tone → plain

| academic | plain | note |
|---|---|---|
| 就 X 问题进行了深入研究 | 深入研究了 X、详查了 X | |
| 具有重要意义 | 重要、关键 | |
| 做出了重要贡献 | 重要 | evaluative phrasing deleted in reports |
| 在某种程度上 | delete, or specify which degree | |
| 一定意义上 | delete | |
| 综上所述 | 综合上述、总的来看 | "所述" redundant |
| 不难看出 | delete, give the conclusion | "不难看出" is AI lyrical padding |
| 总而言之 | 总之 | |

##### Category 3: vague → precise

| vague | precise | note |
|---|---|---|
| 很大程度上 | delete, or use a number | no number support, do not use |
| 相对较高 / 较低 | replace with a concrete number or comparison object | "relative" to what must be explicit |
| 一般来说、通常 | delete in precise contexts | keep when describing a statistical regularity |
| 大致、大约 | give a concrete range (e.g. "30-40%") | |
| 部分、一些 | give a concrete proportion or count | "部分国家" → "M of N countries" |

##### Scope

This lookup table applies to report body, derivations (Word, HTML, WeChat long-form), retrospective docs. **The AI also writes per this table in conversation replies**, avoiding "使得 / 进行了 / 不难看出 / 一定程度上" colloquial and academic residue.

### 7.2 Punctuation and characters (all writing scenarios)

Scope includes the main report, derivations, retrospective files, this framework file itself, and AI conversation replies.

**General principle**: in writing, all "typical AI-generated traces" are forbidden, including the em-dash, Chinese colon as period, half-width `-` as em-dash, emoji, technical operators (see §7.1.1 rule 7). These make the reader recognise "AI-written" in their mental model, reducing readability and credibility. Listed item by item below.

- **never use the em-dash `——`**, no exception. Two reasons: visually clumsy, and using an em-dash often means the sentence structure was not thought through, welding two independent clauses together. Use periods, transition words ("值得注意的是" "换句话说" "原因是…"), or parentheses `（…）`
- **the half-width hyphen `-` is only for ranges and compound words**. Legal: number ranges (`30-90%`, `2016-2030`, `Q1-Q3`), English compounds (`single-bar`, `McKinsey-style`). **Forbidden** to use half-width `-` as an em-dash or connective, e.g. `「这是真改革 - 也是政治宣示」` is an AI trace, change to `「这是真改革，也是政治宣示」` or `「这是真改革。也是政治宣示」`
- **use Chinese colons `：` sparingly**. Break with a period when you can. A colon drags out a long sentence tail and the reader forgets the first half by the second. Use only for "explicit example / list" or "formal definition", not as a period substitute
- use Chinese corner quotes 「」 uniformly. Exceptions: YAML fields, English terms, code, URLs use ASCII `"..."`
- no emoji or special symbols (✅ ❌ ⏳ 🔍 ⚠️ 🏷️ etc.); in xelatex output they are either swallowed or become tofu boxes. Use plain text for status (verified / not started / researching / falsified / partly supported)

### 7.3 Citation

- any factual statement (institutional definition, historical event, number) should have a citation, format `[@key]`
- multiple citations in parallel: `[@key1; @key2]`
- citation entries go uniformly into `references.bib`, each with `url` + `urldate`
- institutional publications use `@misc`, journal articles `@article`, monographs `@book`
- each bib must have a `year` field. Web / database sources use the `urldate` year as `year`, avoiding rendering `(Author, n.d.)`
- do not embed parenthetical acronyms in the author field. `{{Full Name (Acronym)}}` renders nested parentheses. Rule: well-known acronyms (UNDP, ILO, IMF, OECD, ECB) write the acronym only as the author name, others write the full name without parentheses

### 7.4 Pre-writing grep self-check tooled list

Before draft v1 is done, before revisions are delivered, before derivations are delivered, grep verification is mandatory. Commands use `draft.qmd` as the example; replace with the actual main-report filename.

**Evidence requirement (anti "formality self-check")**: when claiming the self-check passed, you **must paste the numbers from the last actual grep / count output**; a verbal "all clear" is not allowed. This applies to the count-gate rows below as much as to the language redlines.

| Redline | Check command | Expected |
|---|---|---|
| Em-dash `——` | `grep -c "——" draft.qmd` | 0 |
| Hand-written §N title prefix (Quarto number-sections auto-adds, hand-writing stacks into "2 §1 ...") | `grep -nE "^#{1,3} §" draft.qmd` | 0 lines |
| Hand-written A.N title prefix (appendix) | `grep -nE "^## A\.[0-9]" draft.qmd` | 0 lines |
| Emoji | `grep -cP "[\x{1F300}-\x{1F9FF}\x{2600}-\x{27BF}]" draft.qmd` | 0 |
| Unescaped dollar sign `$` (**mandatory for English drafts**; LaTeX treats `$` as a math delimiter, unescaped = render failure) | `grep -nP "(?<!\\\\)\\$" draft.qmd` | 0 (write body amounts as `\$`, e.g. `\$1.5 billion`) |
| h3 and deeper titles (body two levels only) | `grep -nE "^#{3,}" draft.qmd` | 0 lines |
| Body bold (lead-ins only) | `grep -c "\*\*" draft.qmd` | near 0, only `**关键词**` and other lead-ins kept (see §7.1) |
| Chinese colon `：` | `grep -c "：" draft.qmd`, **first deduct the "来源：/注：" label colons inside figsource / tblsource blocks** (2 mandatory colons per chart, many charts push the ratio over; count only body prose colons). English drafts skip this item | keep at 5-10% of body period count |
| Lyrical-padding high-frequency words | `grep -nE "实际上\|事实上\|值得指出\|值得注意\|众所周知\|不可否认\|毫无疑问\|需要指出\|客观地讲\|不难看出\|在此背景下\|在这一过程中" draft.qmd` | spot-check and delete on hit, see §7.1 |
| h2 empty-title anti-pattern | `grep -nE "^## .*(关于\|讨论\|探究\|浅析\|思考\|现状与挑战\|视角$)" draft.qmd` | 0 lines (h2 must be conclusive short sentences, see §7.1) |
| Half-width `-` as em-dash (AI trace) | `grep -nE " - " draft.qmd` | spot-check, legal use only ranges and English compounds; change connective/em-dash uses to comma / period, see §7.2 |
| Technical symbols as conjunctions ("→" "+" "/" "∴" "vs") | `grep -nE "→\|∴" draft.qmd` and spot-check `+` `/` `vs` | replace with full written expressions, see §7.1.1 rule 7 |
| Self-invented metaphor | spot-check | replace with methodology or industry-standard terms, see §7.1 |
| Academic / colloquial high-frequency words | `grep -nE "使得\|进行了\|做出了\|具有重要意义\|一定程度上\|一定意义上\|综上所述\|总而言之" draft.qmd` | replace per §7.1.3 table on hit |
| Vague quantifiers (no number support) | `grep -nE "很大程度上\|相对较高\|相对较低\|大致\|大约\|一些\|部分" draft.qmd` | spot-check, delete or replace with concrete numbers if unsupported, see §7.1.3 |
| Framing paragraphs (abstract / intro / conclusion) rewritten | spot-check the three against §7.1.2 structure | abstract 3 paras + keywords, intro has argument map, conclusion has outlook |
| Rendered TOC numbering | open the PDF TOC page | numbering continuous, no duplicates |
| Quarto render | `quarto render draft.qmd` | success, no mathtext / dimension errors |
| **page-count floor** (completeness, see step 4) | `pdfinfo draft.pdf \| grep -i Pages` (poppler) | heavy band 30-40; **< 25 = stop, go back to step 5/6/7, do not declare done** |
| **chart-count floor** | count embedded charts, e.g. `grep -cE "^!\[" draft.qmd` | heavy band 25-35, and **≥ the signed step-6 contract**; **< 20 = stop** |
| **word-count floor** | English `wc -w draft.qmd`; Chinese count characters | ≈ 15k words / 1.5万字; clearly below = stop |

When self-check fails, go back to the source paragraph to revise, do not patch the derivative. At each project's scaffolding stage, copy this table into the project CLAUDE.md pre-writing self-check section, adjusting redline values per project.

**The last three rows are a completeness (count) gate, not a language redline.** They exist because the field failure mode for heavy is shipping a "formally complete but thin" draft. **Paste the actual measured numbers** when you report the draft done. Below floor = not done: go back to step 5 (more search) / 6 (more chapters) / 7 (more charts), do **not** pad with lyrical filler or fabricate (§5.2). The signed step-6 outline contract is the per-project floor; the 30-40 page / 25-35 chart / 15k word band is the framework floor. If the real material honestly cannot reach the band, say so to the user explicitly — but landing far below it almost always means the search / outline was too shallow.

---

## 8. Document & chart standards

Document layout (fonts, sizes, margins, chapter page breaks, bold), chart design principles (the 5 FT chart-doctor principles), chart production rules (one script per chart, PDF / JPG / `_clean.jpg` triple output, palette, no overlap, 2000px cap), visual check, defaults (Quarto YAML template, font-size table, palette quick-reference), the `chart_template` interface contract, the publication-style HTML derivation spec (§7) — all in the same-dir `report_style_spec.md`. The implementation code is in the same-dir `chart_template.py`.

The project CLAUDE.md confirms this project's specific palette, font sizes in the "inherit workflow defaults" section; overriding a default requires a reason in the "deviations from the framework" section.

## 9. Derivation conversion table (companion)

Standardised conversion rules for main-report qmd → Word docx / publication-style HTML / WeChat JPG slices / other derivations. The table is domain-agnostic; each project can add specialised rows.

| Element in main report | Word docx (10b) | publication-style HTML (10c) | WeChat JPG slices (10d) |
|---|---|---|---|
| generation | `quarto render draft.qmd --to docx`, Pandoc auto | copy skill template, fill manually + Live Preview tuning | slice the 10c PDF with `pdftoppm -jpeg -r 200` per page |
| `[@cite-key]` Pandoc citation | auto-rendered as a reference entry | keep the references page (`.page.references`) | follows 10c |
| hypothesis numbers / sub-hypotheses / "directional evidence" / "lower bound" | keep (Word audience accepts caliper analysis) | keep | follows 10c |
| long caliper analysis | keep | keep | follows 10c |
| table (`tbl-colwidths` / footnotesize note) | Pandoc auto-converts to a native Word table | rewrite with `<table class="report-table">` | follows 10c |
| figsource / tblsource custom LaTeX env | **fails in docx** (LaTeX-only), simple: ignore; clean: change to markdown raw in the qmd for dual-output | use `.exhibit-source` / `.table-source` | follows 10c |
| em-dash `——` | keep (Word audience accepts) | never use | follows 10c |
| corner quotes 「」 | keep | keep | follows 10c |
| emoji | **none** (consistent with body standards) | **none** | follows 10c |
| figure embedding | Pandoc auto-embeds PDF / JPG | `<figure class="exhibit">` template, img src uses `fig_*_clean.jpg` (not `fig_*.jpg`, else double title; see spec §3.3 / §7.4) | follows 10c |
| chapter title page | h1 title + page break | `.chapter-opener` large banner | follows 10c |
| cover | none (or custom via reference.docx template) | `.page.cover` full-screen gradient | follows 10c |
| author byline | one line at the end (YAML `author` field auto) | a separate author page `.page.authors`, local headshot img (skill-bundled `scripts/author.jpg` placeholder) | follows 10c |

**Pause after derivation**: after each sub-step derivation lands, **tell the user** and do not proactively do follow-up (publishing, image work, proofreading).

**Special discipline for publication-style HTML**: do it only after the content is stable (after step 9 sign-off); the qmd is the source of truth, HTML is a derivative, no content revision on the HTML; HTML template details in `report_style_spec.md §7`.

---

## 10. Retrospective format

### 10.1 Path and file

- all retrospective entries in one file, **path `9_retrospective/retrospective.md`** (aligned with the §11 directory structure)
- create the file proactively on the first append, do not scatter

### 10.2 Three-part format

Each entry uses the three-part format below (no H3 titles; use `### YYYY-MM-DD §<section> <one-line title>` as the anchor):

```markdown
### 2026-MM-DD §X.Y <one-line title>

**Pitfall**: describe the problem specifically, incl. trigger scenario, error symptom / wrong number / wrong conclusion.

**Handling**: how it was solved this time, incl. tool / data / method adjustments. If code / data landed, give the path.

**Promote?**: (1) promoted to CLAUDE.md §<section>, rule verbatim excerpt; (2) not promoted for now (one-off); (3) to watch (promote after one more occurrence). Pick one of three.
```

**Column three is a mandatory three-way choice**: you must explicitly answer "is this worth a cross-conversation rule", avoiding the retrospective degrading into a diary. The three-way choice is also a quality gate: if none of the three can be chosen, this retrospective was not thought through.

### 10.3 Trigger conditions

- append right after each section is synthesised (do not wait for a "consolidated retrospective")
- append immediately when the user explicitly says "this is a pitfall / lesson / experience"
- append immediately when the AI identifies a recurring class of problem
- log one line in the retrospective each time a CLAUDE.md entry is made

---

## 11. Directory structure

**Design principles**:

1. **each `N_<name>/` folder holds a "deliverable md" of the same name** (`topic.md` / `research.md` / `outline.md` / `data.md` / `scripts.md` / `figures.md` / `draft.md` / `retrospective.md`). This md is both the output and the folder's purpose statement
2. **process / memo material goes into `_process/`** (only `1_topic/` `2_research/` `3_outline/` `7_draft/` need it; `5_scripts/` `6_figures/` have no `_process/`, iteration managed by git)
3. **parallel subfolders numbered `1_` `2_` `3_`** (e.g. `4_data/1_raw/` + `2_processed/`, `8_publication/1_word/` + `2_HTML/` + `3_wechat_pages/`); a single subfolder is not numbered
4. **PDFs are not split by depth**, all flat in `2_research/pdfs/`, importance marked by `research.md` fields (core / reference)
5. **directory numbering maps to the 11-step skeleton**: steps 1/3/4 → `1_topic/`, steps 2/5 → `2_research/`, step 7 split into `4_data/` + `5_scripts/` + `6_figures/`, steps 8/9 → `7_draft/`

```
project root/
├── CLAUDE.md                         project constitution (unchanging conventions)
├── _state.md                         workflow state panel (updated on step switch; template in §12)
├── _quarto.yml                       Quarto project config (if applicable)
│
├── analyst-research/                 the three-piece set (cross-project seed, copy the whole folder)
│   ├── workflow_heavy.md             process discipline (this document)
│   ├── report_style_spec.md          visual spec + chart_template interface contract
│   └── chart_template.py             chart implementation (PALETTE + setup_style + save_fig + legend_above)
│
├── 1_topic/                          steps 1 + 3 + 4: topic confirmation
│   ├── topic.md                      [deliverable] user-signed version
│   └── _process/                     [process] AI-suggested candidate directions, conversation memos
│
├── 2_research/                       steps 2 + 5: material gathering
│   ├── research.md                   [deliverable] unified ledger (seven-class coverage + importance / path / fields / frequency)
│   ├── pdfs/                         full-text PDFs flat, named `<n> <institution> <title>.pdf`
│   └── _process/                     [process] multi-LLM parallel search originals
│
├── 3_outline/                        step 6: detailed outline
│   ├── outline.md                    [deliverable] draft → backfilled to final after step 7
│   └── _process/                     [process] multi-LLM brainstorm chart-list candidates
│
├── 4_data/                           step 7: data drafts
│   ├── data.md                       [deliverable] data archive index (each CSV's source / caliper / fields / units)
│   ├── 1_raw/                        raw downloads, untouched
│   └── 2_processed/                  validated working version, named sN-M_<topic>.csv
│
├── 5_scripts/                        step 7: scripts
│   ├── scripts.md                    [deliverable] script index (each script's purpose / input / output / dependencies)
│   ├── _path.py                      sys.path injection so scripts here can import analyst-research/scripts/chart_template
│   └── make_fig_*.py                 one script per chart (chart_template is in analyst-research/, not here)
│
├── 6_figures/                        step 7: charts
│   ├── figures.md                    [deliverable] figure index (each figure's section, data source, script, caliper caveat)
│   ├── fig_N_M_<topic>.pdf           figure PDF (for qmd embedding)
│   ├── fig_N_M_<topic>.jpg           figure JPG (burn-in title/source/note, self-contained distribution)
│   └── fig_N_M_<topic>_clean.jpg     figure clean JPG (bare raster, for publication-style HTML embedding)
│
├── 7_draft/                          steps 8 + 9: writing + refining
│   ├── draft.md                      [deliverable] main report (extension `draft.qmd` when using Quarto)
│   ├── references.bib                [deliverable] Pandoc citation library
│   └── _process/                     [process] per-section iterations, DeepSeek text v1.5, Claude integration v2 interim, multi-LLM critique originals (see the §11 `_process/` guide)
│
├── 8_publication/                    step 10: final derivations (main PDF stays in 7_draft/, not copied here)
│   ├── 1_word/                       10b Word docx (Pandoc auto, for client review / annotation)
│   ├── 2_HTML/                       10c publication-style HTML + PDF (consulting / FT long-form, optional; spec §7)
│   └── 3_wechat_pages/               10d WeChat JPG slices (10c PDF per page, optional; spec §7.9)
│
└── 9_retrospective/                  step 11: retrospective
    └── retrospective.md              [deliverable] three-part retrospective (the retrospective is itself a process artifact, no _process/)
```

**Step ↔ directory map**:

| Step | Directory | Key output |
|---|---|---|
| 1 initial topic | `1_topic/` | topic description in conversation (no separate file needed) |
| 2 broad search | `2_research/_process/` + `research.md` draft | material ledger draft (seven-class coverage) |
| 3 AI suggests directions | `1_topic/_process/` | 2-3 candidate directions |
| 4 confirm topic | `1_topic/topic.md` | user-signed version |
| 5 supplementary search | `2_research/pdfs/` + `research.md` complete | full-text PDFs + complete ledger |
| 6 outline draft | `3_outline/outline.md` | outline draft |
| 7 charts first | `4_data/data.md` + `5_scripts/scripts.md` + `6_figures/figures.md` | three indices + outline final |
| 8 draft writing | `7_draft/draft.md` | main report sections |
| 9 refine | `7_draft/_process/` + revisions | v2 / v3 main report |
| 10 finalise derive | `7_draft/` + `8_publication/{1_word,2_HTML,3_wechat_pages}/` | PDF + Word + optional HTML + optional WeChat JPG |
| 11 retrospective | `9_retrospective/retrospective.md` | three-part entries |

**`_process/` content guide** (what goes in, naming):

| Directory | What goes in | Naming |
|---|---|---|
| `1_topic/_process/` | step 3 AI candidate directions, user-AI topic discussion memos | `_options.md` (direction candidates) + memos as needed |
| `2_research/_process/` | step 2 multi-LLM parallel search originals (Claude / GPT / DS each ledger) | `research_<llm>.md` (e.g. `research_gpt.md`) |
| `3_outline/_process/` | step 6 multi-LLM brainstorm chart-list candidates; outline candidates | `outline_<llm>.md` / `figures_brainstorm_<llm>.md` |
| `7_draft/_process/` | step 8 per-section iterations, DeepSeek text v1.5, Claude integration v2 interim; step 9 multi-LLM critique originals (GPT/DS critique) + Claude's per-item decision log | `draft_<vX>_<who>.qmd` (e.g. `draft_v1_claude.qmd` / `draft_v15_deepseek.qmd` / `draft_v2_claude.qmd`); critique `critique_<llm>.md` (e.g. `critique_gpt.md`); decisions `critique_decisions.md` |

General rules:

- **`_process/` is the process-material area, not external-facing**. The latest shippable version is always the parent dir's deliverable md (`topic.md` / `outline.md` / `draft.qmd`)
- **cp a copy to `_process/` before each big change** (e.g. `cp 7_draft/draft.qmd 7_draft/_process/draft_v1_claude.qmd`), then edit in place
- **under multi-LLM concurrency each LLM produces only into its own file**, not directly overwriting the shared deliverable md. The synthesiser (Claude) updates the deliverable md after integration
- `5_scripts/` `6_figures/` have no `_process/`: script and chart iteration is git-managed; keeping interim drafts is confusing

**Minimal skeleton of each deliverable md** (scaffold stage creates an empty file + a purpose line, filled by later steps):

| File | Minimal skeleton |
|---|---|
| `1_topic/topic.md` | title / research question / target audience / output form / chapter skeleton (h2 draft) |
| `2_research/research.md` | seven sections matching appendix A's A.1-A.7 classes, each listing found material (number / type / institution / title / year / PDF path / importance / key fields / acquisition method) |
| `3_outline/outline.md` | h1 / h2 chapter skeleton (conclusive titles) + per-section research sub-question, take-away, planned charts, key citations. Body two levels only, no h3 |
| `4_data/data.md` | table: CSV filename / source / caliper / fields / units / time range / processing script |
| `5_scripts/scripts.md` | table: script filename / purpose / input data / output (chart / CSV) / dependencies (package / template) |
| `6_figures/figures.md` | table: figure number / section / title / data source / script / caliper caveat |
| `7_draft/draft.md` | main report body (per outline chapters), with `[@cite]` citations |
| `9_retrospective/retrospective.md` | three-part retrospective entries, appended per the §10 format |

**On "PDFs not split by depth"**: a `deep/` (structural argument) + `shallow/` (background reference) two-layer design was considered, but the boundary is fuzzy in practice (the same IMF report is background on first read, core when used deeply). Changed to a flat layout, with importance marked by the `research.md` "importance" field. Recommended `research.md` fields:

| Field | Example |
|---|---|
| number | `06` |
| type | document / dataset |
| institution | IMF |
| title | GCC Policy Paper 2024 |
| year | 2024 |
| PDF path | `pdfs/06 IMF GCC Policy Paper 2024.pdf` |
| importance | core (core-argument citation / key number / methodology borrowed) / reference (background / one-off citation) |
| field or key number | fiscal-breakeven oil price, oil-price-GDP elasticity |
| acquisition | official download / NOTES.md placeholder |

**Notes**:
- specific paths follow the project CLAUDE.md; this section is the baseline. If the project uses another toolchain (Word + Excel instead of Quarto + Python), dir names can be localised but **the numbering order stays the same**
- `_process/` is process-material archive; need not be cleaned at publication but can be zipped
- the main PDF is viewed and distributed directly at `7_draft/draft.pdf`, not duplicated in `8_publication/`; the frozen version is managed by git tag or filename suffix (`draft_v3.pdf`)
- `5_scripts/` and `6_figures/` have no `_process/`: scripts and charts are themselves the output, no "process material" concept. Script iteration is git-managed

---

## 12. `_state.md` template

`_state.md` is the **only** progress file in the project root; any LLM / user entering the project looks here first. It solves one core problem: **how a new session quickly picks up context**.

### 12.1 Separation of responsibility

- `CLAUDE.md` = project-level **rules** (unchanging conventions: writing style, Python environment, file organisation)
- `_state.md` = project-level **state** (changing, updated on each step switch)
- the `topic.md` / `research.md` / `outline.md` / `data.md` / `scripts.md` / `figures.md` / `draft.md` / `retrospective.md` in each stage subdir = **content** (the output itself, not state)

Do not mix the three. Rules appearing in the state file, or state appearing in the output file, are both pollution.

### 12.2 Template (copy directly to a new project root)

```markdown
# Project progress panel · _state.md

> The project-level **only** progress file. Any LLM / user entering the project looks here first.
> Separation of responsibility: CLAUDE.md = rules, this file = state, subdir files = content.

---

## ▶ Current position (at a glance)

\`\`\`
[current step] step N <name>
[span]        YYYY-MM-DD ~ in progress
[blocker]     (if any, brief reason; "none" if not)

[x] 1 topic         locked (topic.md, YYYY-MM-DD user signed)
[x] 2 research      locked (research.md + pdfs/ N PDFs)
[x] 3 outline       outline.md draft (final after step 7)
[>] 4-6 data scripts charts  in progress (completed N / M charts)
[ ] 7 draft         not started
[ ] 8 publication   not started
[~] 9 retrospective background activity (N entries appended)
\`\`\`

Status symbols: `[x]` done / `[>]` in progress / `[~]` background activity (cross-cutting, e.g. retrospective) / `[ ]` not started / `[!]` blocked

**Next action**: (one sentence on what this step does, who does it)

**Hard-stop status**: (if awaiting user review, note what; "none" if no hard stop)

---

## Key deliverable index

| Step | Key output | Process material |
|---|---|---|
| 1 topic | [topic.md](1_topic/topic.md) | [_process/](1_topic/_process/) |
| 2 research | [research.md](2_research/research.md) · [pdfs/](2_research/pdfs/) | [_process/](2_research/_process/) |
| 3 outline | [outline.md](3_outline/outline.md) | [_process/](3_outline/_process/) |
| 4-6 data/scripts/charts | [data.md](4_data/data.md) · [scripts.md](5_scripts/scripts.md) · [figures.md](6_figures/figures.md) | [1_raw/](4_data/1_raw/) |
| 7 draft | [draft.md](7_draft/draft.md) · [references.bib](7_draft/references.bib) | [_process/](7_draft/_process/) |
| 8 publication | [1_word/](8_publication/1_word/) · [2_HTML/](8_publication/2_HTML/) · [3_wechat_pages/](8_publication/3_wechat_pages/) | main PDF at [7_draft/draft.pdf](7_draft/) |
| 9 retrospective | [retrospective.md](9_retrospective/retrospective.md) | — |

---

## Cross-stage open items

A to-do pool: items affecting multiple steps, not belonging to the current step. Check here when the current step completes.

- [ ] item 1 (affects steps X / Y)
- [ ] item 2

---

## git timeline (last 10 commits)

\`\`\`
(paste git log --oneline -10 output)
\`\`\`

Tagged milestones: step-completion sign-off lock, version freeze, finalisation.

---

## Maintenance rules

- the trigger (LLM or user) updates the "▶ Current position" section on each step switch
- key milestones (step completion, user sign-off lock) must be git-taggable + synced here
- the "Key deliverable index" holds only file paths, no details (details in the output files)
- the "git timeline" shows the last 10 commits for a quick view of activity
- under multi-LLM concurrency each LLM produces only into its own `_process/<llm>/` subdir, not editing this file directly; the synthesiser (Claude) updates it at the end of each round

---

## Revision history

| Time | Operator | Action |
|---|---|---|
| YYYY-MM-DD | Claude / user | initialise _state.md |
```

### 12.3 When to update

| Trigger | Which section to update |
|---|---|
| step switch (e.g. 6 → 7) | "▶ Current position" + matching "Key deliverable index" row |
| user sign-off hard-stop lock | "▶ Current position" + git tag |
| a cross-stage problem identified | append to "Cross-stage open items" |
| a key commit done | refresh "git timeline" |
| a blocker occurs or clears | "▶ Current position → blocker" section |

### 12.4 Boundary judgement vs CLAUDE.md

If a piece of info **does not change as steps advance** (e.g. "this project renders with Quarto + xelatex", "no em-dash in the body"), it goes into CLAUDE.md.

If it **changes as steps advance** (e.g. "currently at step 6", "awaiting user review of the outline", "3 items in the to-do pool"), it goes into `_state.md`.

Rule of thumb: ask "will this still hold a week from now?" Yes → CLAUDE.md; No → `_state.md`.


## 13. Open questions of this framework

Open questions left for future projects to validate:

1. **Actual benefit of multi-LLM collaboration**: steps 2 / 5 / 6 / 9 all design multi-LLM, but each extra LLM raises cost (switching, maintaining parallel output, synthesis). In which steps is multi-LLM genuinely significantly better than single-LLM? Needs continued observation and recording of marginal benefit.

2. **Iteration depth of charts-first**: steps 6 ↔ 7 are bidirectional, but how many rounds is reasonable? Maybe 1 for a simple project, 3-4 for a complex one. Needs observation.

3. **Standardisation scope of derivations**: the §9 conversion table currently covers main report → Word docx / publication-style HTML / WeChat JPG slices. Conversion rules for LinkedIn / email brief / in-firm version / WeChat md need new-project validation.

4. **Portability of the writing-standards template**: §7 rules originate from the Chinese-report scenario; what adaptations do English reports need? What special conventions for bilingual (Chinese-English) reports? Currently unknown. (Partly addressed in v0.7: the skill is now bilingual and English-report-aware; see SKILL.md "Language policy".)

5. **When to split the retrospective file**: a single appended file suits short-to-medium projects (within half a year); a long project may need year / topic splits. The split threshold needs observation.

---

## Appendix A: broad-search resource list

At the step 2 broad search, the AI should **fully cover the seven source classes below**, not just the few it knows. This appendix gives a representative entry per class, which the AI can search down the list in a new project.

### A.1 international organisations & multilaterals

The "gold standard" for macro and cross-country comparison, methodologically solid, fully public.

- **IMF**: World Economic Outlook (WEO), Article IV Consultation, Working Papers, Policy Papers, Selected Issues Papers, via [imf.org/publications](https://www.imf.org/publications), [elibrary.imf.org](https://www.elibrary.imf.org)
- **World Bank**: Open Knowledge Repository ([openknowledge.worldbank.org](https://openknowledge.worldbank.org)), World Development Indicators ([databank.worldbank.org](https://databank.worldbank.org)), Country Studies
- **IEA**: World Energy Outlook, Country Profiles, energy data ([iea.org](https://www.iea.org))
- **IRENA**: renewables
- **OECD**, **BIS** (Bank for International Settlements, financial stability and cross-border capital flows), **UN Comtrade** (trade), **UNCTAD** (investment), **WTO**
- regional development banks: ADB (Asia), AfDB (Africa), Arab Monetary Fund, IDB (Islamic Development Bank), ESCAP, ECLAC

### A.2 sovereign / government / central bank / regulators

Primary data and policy text, more accurate than second-hand paraphrase.

- **central banks**: monetary policy, FX reserves, banking, cross-border capital flows
- **statistics offices**: GDP, population, industry structure, CPI, employment (caliper per the country)
- **finance ministries**: budget, fiscal revenue, government debt
- **sovereign wealth funds**: annual reports (SWFI database / each SWF site)
- **sector regulators**: energy, finance, telecom, real estate
- **SEC EDGAR**: 13F sovereign-fund disclosures, listed-company filings ([sec.gov/edgar](https://www.sec.gov/edgar))

### A.3 academic & think tank

Sources for theoretical frameworks and literature reviews.

- academic: **NBER Working Papers**, **SSRN**, **Google Scholar**, JSTOR, ScienceDirect
- top journals: AER, QJE, JFE, RFS, JPE, JF, JIE
- think tanks: Brookings, Peterson IIE, Atlantic Council, CSIS, Chatham House, CFR, IISS, Carnegie Endowment

### A.4 investment-bank research & consulting

The latest on industry / company / country, methodologically less rigorous than academia but timely.

- international banks: Goldman Sachs, JPMorgan, Morgan Stanley, Citi, HSBC, BofA, UBS, Credit Suisse Country Outlooks / Sector Reports (mostly subscription, but summaries often leak via media)
- Chinese banks: CICC, CSC, China Merchants Securities, Haitong, Huatai, Guotai Junan overseas research and cross-border strategy. **caveat**: Chinese-bank overseas country research goes through the `market-research-skills:verifying` skill's "resource class kept, but not a primary-source whitelist" handling; when citing their paraphrase of IMF / GS / JPM numbers, trace back to the original institution, do not use the Chinese-bank report as a citation intermediary
- consulting: McKinsey, BCG, Oliver Wyman, Bain, Deloitte, PwC, EY, Accenture industry white papers (mostly public)

### A.5 mainstream financial media

Timely sources for events, people, dynamics.

- **Chinese**: Caixin, Wallstreetcn, Yicai, Economic Observer, 21st Century Business Herald, Bloomberg China, FT Chinese, WSJ Chinese
- **English**: Bloomberg, Reuters, Financial Times, Wall Street Journal, The Economist, NYT, Forbes, Fortune
- **regional specialist**: MEED (Middle East), Argus / Platts (energy), Lloyd's List (shipping), TradeWinds (shipping), Variety (media), Modern Healthcare (healthcare)

### A.6 WeChat / industry communities (Chinese world)

Chinese-world deep analysis and primary observation, often earlier / more accurate than English paraphrase.

- finance public accounts: Wallstreetcn, Zhibenshe, Securities China, Poker Investor, Alpha Works
- regional: niche but deep Gulf-focused accounts
- industry: energy, real estate, consumer, tech, healthcare verticals each have accounts
- in-firm sharing groups, LinkedIn professional authors, Substack independent analysts

### A.7 databases (programmatic access)

Database MCPs and skills available to this project:

- **iFind MCP** (THS): A-shares / HK / China macro / industry data. A-shares prefer this
- **OpenBB MCP**: multi-asset macro, equities, ETF, crypto
- **`financial-data-sources` skill**: FRED (US macro), World Bank / IMF / OECD / Eurostat / ECB (cross-country macro), SEC EDGAR (incl. 13F sovereign-fund disclosures), yfinance (US / HK / global quotes), AKShare / Baostock / Tushare (A-shares / HK / China macro), CoinGecko (crypto)

External (if reachable, mostly paid): Wind, Bloomberg, Refinitiv (Eikon), Capital IQ, PitchBook, FactSet, CEIC, CapitalLine

### A.8 both-languages principle

Chinese and English coverage must be balanced:
- official reports from international orgs / banks / consulting are mostly English, Chinese summaries common in Chinese-bank research and Chinese media
- local data and policy dynamics for China / Middle East / Africa are often more accurate in Chinese primary material than English paraphrase
- policy-document originals often have official multilingual versions (e.g. Middle East development plans in both Arabic and English), cross-checked when needed
- multi-LLM parallel-search division: Claude leans English academic and bank, DeepSeek Chinese and regional context, GPT balanced

### A.9 source-coverage self-check

At the end of step 2 the AI **must self-check** whether each of A.1-A.7 was searched. Any class not searched at all must be done before step 3. Leave a "source-coverage self-check table" at the top of `2_research/research.md` recording each class.

**Self-check table example template** (copy to the top of research.md, status column in plain text per §7.2):

```markdown
## Source-coverage self-check (fill at step 2 completion)

| Class | Status | Key material |
|---|---|---|
| A.1 international orgs | done | IMF Article IV / World Bank Country Update / IEA |
| A.2 sovereign / government / central bank | done | central-bank FSR / finance-ministry Budget / SWF AR |
| A.3 academic & think tank | done | NBER WP / Brookings / Carnegie |
| A.4 investment banks + consulting | done | GS Country Outlook / McKinsey white paper |
| A.5 mainstream financial media | done | Bloomberg / Reuters / FT |
| A.6 WeChat / industry communities | done | Wallstreetcn / Zhibenshe etc. |
| A.7 databases | done | iFind MCP / financial-data-sources skill |
```

Any class not searched, or only one or two examples searched, mark "not searched" or "to fill"; it must reach "done" before step 3.
