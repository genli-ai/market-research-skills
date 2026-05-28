# Report visual spec

> English is the authoritative version; the Chinese mirror is `report_style_spec.zh.md`.
> Cross-project report and chart visual spec. Used as a three-piece set with `workflow_heavy.md` (process discipline) + `chart_template.py` (implementation code).
>
> Boundary with `chart_template.py`: this file explains "why it is set this way + the interface contract"; the code is "how it is implemented". The true HEX and rcParams are in the code (`PALETTE` dict + `setup_style()` rcParams); the §5 lookup tables here are a human quick-reference, and **on drift the code wins**.
>
> Design inspiration: the **Financial Times chart-doctor** (github.com/Financial-Times/chart-doctor) open-source spec. FT's financial-report visualisation is the industry benchmark, principles simple to replicate. This document absorbs its design philosophy, adjusted for the Chinese-report scenario.
>
> The project-level CLAUDE.md may override the defaults here (register the reason in the "deviations from the framework" section when overriding).
>
> This document also serves as the analyst-research skill's `references/report_style_spec.md`. In the skill the three-piece set is layered in `references/` (this doc, workflow files) and `scripts/` (chart_template.py); in a user project the three-piece set is flat in `analyst-research/`. All references to the other two files below use the filename without a path, so both structures resolve.

---

## Quick start

**For the AI and human at a new project's scaffolding stage**: this section is the "must-read before charting" summary. Full rules in §1-§6.

### Three-piece-set relationship

| File | Location | Role |
|---|---|---|
| `SKILL.md` | `analyst-research/` | skill entry (frontmatter + load order) |
| `workflow_heavy.md` | `analyst-research/references/` | process discipline: 11-step skeleton, multi-LLM division, retrospective format |
| `report_style_spec.md` | `analyst-research/references/` | visual spec (this doc) + chart_template interface contract |
| `chart_template.py` | `analyst-research/scripts/` | drawing implementation single source of truth: `PALETTE`, `setup_style`, `save_fig`, `legend_above` |
| `publication-style-template.html` | `analyst-research/scripts/` | publication HTML template (optional 10c derivation) |
| `author.jpg` | `analyst-research/scripts/` | author headshot placeholder (optional 10c derivation) |
| `_path.py` | `5_scripts/` | sys.path injection to `../analyst-research/scripts/`. Must be created first at the new-project scaffold stage (content at §6.4 end) |

### Hard rules for drawing scripts

The 5-line boilerplate at the top of each `5_scripts/make_fig_*.py` is non-optional:

```python
import _path  # noqa: F401  -- add analyst-research/scripts/ to sys.path
from chart_template import setup_style, save_fig, PALETTE, FIG_W, DATA_PROC

setup_style()
```

Landing constraints:

1. **No hardcoded HEX colours in scripts.** Colours always reference `PALETTE["primary" / "secondary" / "tertiary" / "accent" / ...]` (semantics in §5.3).
2. **No overriding matplotlib rcParams in scripts.** Fonts, sizes, spines, grid, ticks are all set uniformly by `setup_style()`.
3. **figsize width must be locked to `FIG_W`**: `figsize=(FIG_W, h)`, h free (usually 3-4 inch). Hand-writing `figsize=(10, 5)` etc. makes Quarto shrink the chart to textwidth and shrink the font with it (§3.12).
4. **One plot per chart, no side-by-side subplots**: `plt.subplots(1, 2, ...)` and any side-by-side layout is forbidden (§3.7). Split multi-plot needs into multiple independent charts.
5. **Legend above the plot, horizontal, centered on the image**: default `legend_above(ax, ncol=N, mode="centered")` (**do not** write `bbox_to_anchor=(0.5, 1.02)` directly — that is the plot midpoint, not the image midpoint); use `mode="image_left"` for many-item / single-accent charts. The legend must not cover the plot / overlap graphic elements / stack vertically (§3.8).
6. **Output only via `save_fig`**. It auto-produces PDF (for Quarto embedding) + JPG (with burn-in title / source / note, independent distribution) + `_clean.jpg` (bare raster, for publication-style HTML embedding), **three formats**, JPG long edge auto ≤ 2000px (§3.11). **Tables do not go through the image pipeline; write markdown tables directly (§3.9).** Pass `clean=False` to skip `_clean.jpg` (medium / light).
7. **PDF is bare / JPG is self-contained / `_clean.jpg` is a bare raster**, the three carry different content (§3.3). `save_fig(fig, fig_id, title=, source=, note=)` one call manages all three.

Full boilerplate template in §6.4, interface contract in §6.

### Document navigation

- §1 **document layout**: QMD / heading levels / font-size unification / page breaks / bold
- §2 **chart design principles**: the 5 FT chart-doctor rules (two-level typography / minimal chrome / single accent / title carries the argument / data-ink ratio)
- §3 **chart production rules**: one script per chart / triple output (PDF + JPG + _clean.jpg) / palette / legend / subplots / no overlap / 2000px cap
- §4 **visual check**: AI does not do it, the user self-checks
- §5 **default quick-reference**: Quarto YAML standard header / font-size and font table / palette HEX table
- §6 **chart_template interface contract**: how to call `setup_style` / `PALETTE` / `save_fig` / `legend_above` + full call template + `_path.py` content
- §7 **publication-style HTML derivation** (step 10 optional): consulting / FT long-form HTML → PDF template spec, 1 div = 1 A4, in-HTML page numbers, `_clean.jpg` embedding, manual page balancing, manual browser PDF save, WeChat JPG slicing
- §8 **AI disclosure footer** (mandatory in each PDF): bilingual templates

---

## 1. Document layout

### 1.1 Default format

The main report defaults to **QMD** (Quarto markdown) rendering PDF. MD is only for retrospectives, process notes, state files. MD does not enter the main-report delivery path.

**HTML derivation** (consulting / FT long-form) is done as needed, spec in §7; HTML does not replace the qmd main report, the qmd is always the source of truth.

### 1.2 Heading levels

**Applies to**: **only the main-report PDF** (`7_draft/draft.qmd` rendered version).

**Does not apply to**:

1. **any derivation** (Word docx / WeChat long-form / email brief / tweets / Slack long posts). Derivation platforms have their own levels and folding (Word audiences accept multi-level numbering, WeChat TOC uses bold + numbers, tweets use paragraph breaks; do not apply the main report's strict h1/h2 two-level rule)
2. **methodology docs** (`workflow_heavy.md` / this `report_style_spec.md` / project `CLAUDE.md`)
3. **state files** (`_state.md`)
4. **stage deliverable mds** (`topic.md` / `research.md` / `outline.md` / `data.md` / `scripts.md` / `figures.md` / `retrospective.md`)
5. **process material** (anything under `_process/`)

These all need h3+ as a skim skeleton, not bound by this rule.

**The report body has two levels only: h1 sections / h2 subsections. No h3 and deeper.** Three-level titles make the TOC verbose and the reader lost. If a section has multiple sub-points, let the leading conclusion sentence carry the layering.

If a section truly has so many points it needs h3, that is a structure problem; split it into two h2, not open an h3.

### 1.3 Heading text

- **main title ≤ 15 chars**. Readability first, completeness via the subtitle
- **subtitle font size = main title size**, the subtitle does not repeat the main title's qualifiers
- **section title (h1) ≤ 12 chars**. An argumentative short phrase, not lyrical, no "assessment / exploration / brief analysis" padding
- the section title does not repeat the main title. If the report is "X policy real-effect assessment", §1 writing "the real-effect problem in X policy" is a counter-example
- **do not hand-write §N / N.N / A.N prefixes**. Quarto `number-sections` auto-adds them; hand-writing stacks into "2 §1 real dependence"

### 1.4 Font-size unification

The main-report PDF uses **6 font sizes: 18 / 16 / 14 / 12 / 11 / 10 pt**. The Chinese font is uniformly Songti SC, English uniformly Times New Roman, Arabic uniformly Noto Sans Arabic.

| Element | Size | Weight |
|---|---|---|
| main title (cover) | 18pt | bold |
| subtitle (cover) | 16pt | regular |
| TOC / LoF / LoT titles | 14pt | bold |
| h1 section title | 14pt | bold |
| h2 subsection title | 12pt | bold |
| body paragraph | 11pt | regular |
| author / date | 11pt | regular |
| abstract title "Abstract" | 14pt | bold centered (same tier as the three TOC titles) |
| abstract body | 11pt | regular |
| keyword line (abstract end "**Keywords**: ...") | 11pt | "Keywords" bold, list regular |
| TOC / LoF / LoT entries | 11pt | regular |
| inline citation `[@key]` rendered | 11pt | regular |
| figure caption / table caption | 11pt | regular italic |
| table header | 11pt | bold |
| table body | 11pt | regular |
| inline note / footnote | 11pt | regular italic |
| reference entry | 11pt | regular |
| **figure source / note** (`::: {.figure-source}`) | **10pt** | regular, grey |
| **table source / note** (`::: {.table-source}`) | **10pt** | regular, grey |

**Size-selection logic**:

- **11pt is the baseline**. All body-like elements (body / abstract / author / TOC entries / citations / table caption / table header / table body / footnotes / references) are 11pt. Reading uniformly as one body tier simplifies hierarchy
- **12pt = h2 subsection title**, the only subsection-level emphasis
- **14pt = h1 section title + TOC / LoF / LoT titles**, section-level emphasis
- **18pt = main title**, the only cover top tier, bold
- **16pt = subtitle**, second only to the main title, regular weight; distinguished from the main title by "2pt size diff + weight"
- **10pt = figure / table source and note**. For `::: {.figure-source}` and `::: {.table-source}` only, one tier below body for visual demotion. The figure / table caption (above the figure / table) stays 11pt level with body; only the source / note (below) drops to 10pt
- **no 9pt**. 9pt is near the readable limit at PDF reading size, an unnecessary tier

Implementation in §5.1 YAML header and include-in-header; this table is the target, sample-checked with a PDF reader after rendering.

**Keyword convention**:

**Do not use** Quarto / pandoc's top-level YAML `keywords:` field — it writes only to PDF metadata (hyperref's `pdfkeywords`, visible only in the Acrobat file-properties panel), **not rendered as visible text**, no value for an internal investment report. Keeping it actually causes confusion (the YAML has keywords but the PDF shows none).

**Practice**: add an inline keyword line at the end of the abstract text in the `abstract:` YAML field:

```yaml
abstract: |
  ... abstract body ...

  **Keywords**: core theme | country or region | key policy | key institution | ...
```

Keywords separated by ` | `, avoiding visual confusion with Chinese / English commas. "Keywords" bold, list regular.

**Keyword-selection spec**:

- **count**: 5-7
- **must include five classes** (in order): (1) research object (a policy name, a sovereign fund) (2) core issue or event (3) key institution (4) research method or angle (5) geographic or time anchor
- **all concrete nouns**, avoid abstractions ("economy" "analysis" "research" "problem" "challenge" "thinking")
- **avoid sweeping phrases** ("economic diversification" acceptable, "global economic integration" too broad)
- **capitalisation**: English proper names per official form (IMF, PIF all-caps, NEOM all-caps, Vision 2030 with the number); Chinese proper names per common translation

**Exception**: if the report enters an academic database / indexing system needing PDF-metadata indexing, add the YAML `keywords:` field and accept the cost of manually syncing the "YAML + inline" two copies.

### 1.5 First-line indent and paragraph spacing

**No first-line indent throughout, incl. abstract and body.** Override ctexart's default `\parindent=2em`, set `\parindent=0pt` explicitly.

Without indent, paragraphs need visual whitespace or they clump. Default `\parskip=0.5em` (half a line, auto-scaling with font size).

The ctexart abstract environment follows the same rule, no exception. Implementation in §5.1 YAML header.

### 1.6 Margins

Uniform throughout. **Abstract / TOC / index page margins = body margins.** Standard top/bottom 25mm, left/right 20mm.

### 1.7 Page-break rules

**Forced page breaks** at the following positions (others flow by natural LaTeX pagination):

| Position | Implementation |
|---|---|
| cover | `\maketitle` defaults to `\thispagestyle{empty}` |
| **before the TOC** | LaTeX `\AtBeginDocument` + `\pretocmd{\tableofcontents}{\clearpage}` (see §5.1) |
| **before the LoF** | LaTeX `\AtBeginDocument` + `\pretocmd{\listoffigures}{\clearpage}` (see §5.1) |
| **before the LoT** | LaTeX `\AtBeginDocument` + `\pretocmd{\listoftables}{\clearpage}` (see §5.1) |
| **after the LoT** (entering the body) | LaTeX `\AtBeginDocument` + `\apptocmd{\listoftables}{\clearpage}` (see §5.1) |
| **before an appendix** | hand-write `{{< pagebreak >}}` before the appendix H1 in the qmd body |
| **before references** | hand-write `{{< pagebreak >}}` before `# References` in the qmd body |

**Layout result**: cover + abstract (one page) → TOC (standalone) → LoF (standalone) → LoT (standalone) → body → appendix (standalone) → references (standalone). Each "navigation" block is standalone, avoiding title-content separation.

**Why the LoF / LoT need a forced break**: when tocloft centres the title with `\begin{center}...\end{center}` (see §1.8), the title in vertical mode is a standalone paragraph, and LaTeX pushes the "orphan title" to the bottom of the previous page with the content on the next, separating title and content. `\clearpage` forces the LoF / LoT to start on a new page, keeping title and entries together. This is an engineering compromise, not an aesthetic choice.

### 1.8 LoF / LoT

- the List of Figures and List of Tables **must both exist**
- numbering **continuous**: Figure 1 / Figure 2 / ... / Figure N, Table 1 / ... / Table M
- **no in-section numbering** (Figure 1.1 / Table 6.1)
- Quarto `lof: true` + `lot: true` auto-generates both
- **the three index titles (TOC / LoF / LoT) are uniformly centered** — directly override tocloft's `\@cftmaketoctitle` / `\@cftmakeloftitle` / `\@cftmakelottitle` hooks, forcing the title centered with `\begin{center}...\end{center}` (see §5.1). **Do not use tocloft's built-in `\hfill` wrap method** — unreliable in article mode when the title follows preceding text (like an abstract), often offset right
- **forced break before the LoF / LoT** — `\begin{center}` centering triggers the title as a standalone paragraph, LaTeX pushes the orphan title to the previous page bottom. `\clearpage` before LoF / LoT forces the break, keeping title and entries together (see §1.7)
- **forced break after the LoT entering the body** (consistent with §1.7)
- implementation summary — `\AtBeginDocument` + `\pretocmd{\listoffigures}{\clearpage}` + `\pretocmd{\listoftables}{\clearpage}` + `\apptocmd{\listoftables}{\clearpage}` (see §5.1)

**Key pitfall**: tocloft redefines `\listoffigures` / `\listoftables` inside `\AtBeginDocument`, so the patch must also be wrapped in `\AtBeginDocument` and rely on hook FIFO order to run after tocloft — otherwise the patch is overwritten by tocloft's redefinition. A bare `\let + \renewcommand` in the preamble, or `\apptocmd` / `\pretocmd` not wrapped in `\AtBeginDocument`, **does not take effect**.

### 1.9 No dividers between sections

No `---` / `\hrule` / `***` horizontal rules between sections. Sections are separated by page breaks or blank lines.

### 1.10 Bold usage

**The ideal is zero bold in the body.** Emphasis is carried by the leading conclusion sentence, h2 titles, table row highlights, the chart accent colour. If bold is necessary, only: first definition of a term, single-point emphasis. **≤ 1 bold per paragraph, ≤ 3 bold per section.**

### 1.11 Header / footer

**No header throughout.** **The footer shows only a centered page number.**

Implementation: `\pagestyle{plain}` overrides the ctex `chinese-article` scheme default `\pagestyle{headings}` (the latter shows `\rightmark`, i.e. the previous section title + page number, in the header; index overflow pages often show leftover "List of Figures N" etc.).

The cover page is auto-set to `\thispagestyle{empty}` by `\maketitle` to suppress the page number, no extra config.

Reasons: (1) Chinese investment-report readers scan structure (TOC and section titles are enough), no need for a header repeating the section name each page; (2) the headings style shows the previous chapter's leftover `\rightmark` on index overflow pages, causing "List of Figures", "Contents" misplacements; (3) simplicity is beauty.

---

## 2. Chart design principles (FT chart-doctor inspired)

Five principles by importance. Specific HEX values are in §5.3; this section covers principles, not colours.

### 2.1 Two-level typography

Font hierarchy is carried by **size + colour**, **not weight** (FT titles use regular weight):

| Element | Size | Weight | Colour |
|---|---|---|---|
| chart title (in JPG) | 14pt | regular | text |
| axis label / source / note | 9pt | regular | text_light |

**Only one title level**, no subtitle. Press the argument into the main title (e.g. "after rebasing nominal +14% / non-oil +20%").

### 2.2 Chrome minimalism

Maximise the data-ink ratio (Tufte principle + FT practice):

- remove top / right spine
- **keep bottom + left spine** (on a white background the axes need to be visible). FT's original uses a cream bg with "no left spine"; this project uses white (embedding in Quarto white-paper PDF), restoring the left spine for a visual boundary
- spine colour: axis colour (FT warm dark grey `#66605C`, see §5.3)
- ticks visible (clear on a white bg)
- baseline (0 / reference line, baseline colour)
- grid only in the y direction (FT actually extends the y-axis tick line across the plot width into a horizontal line), slightly darkened on white

### 2.3 Single accent principle

A chart **allows only one data element in the accent colour** to stand out; all others in primary / neutral / tertiary. Use the accent on "the one you really want the reader to see".

Counter-example: 5 bars in 5 different colours, the eye wanders. Positive example: all 5 bars in tertiary, the tallest in accent, the reader instantly knows who you emphasise.

FT's words: "make sure the blue line is on top as this is the primary line colour".

### 2.4 Title carries the argument

- **the title states "fact + number"**: "institution A and B's growth diverge by 1.5 percentage points in year X" / "after the policy, nominal GDP +14%"
- do not write a vague title like "X country non-oil GDP growth"
- the reader gets the main take-away by scanning the title, no need to read the chart

### 2.5 Data-ink ratio

- 5 ticks beats 10 ticks (less is more)
- integers beat decimals (unless precision matters)
- grid very faint or omitted
- low colour saturation (saturated colours tire the eye)
- delete all unnecessary labels / borders / shadows / gradients
- **no change-rate labels between bars** (e.g. "+14%" with an arrow). Error-prone, and FT does not do it. The change rate goes in the title

---

## 3. Chart production rules

### 3.1 One script per chart

Each chart corresponds to an independent script, named `make_fig_<section>_<n>_<topic>.py`.

No "one section, one script generating multiple charts". Reasons:

- a single-chart iteration does not need to re-run the whole section
- a single-chart script ≤ 150 lines, readable
- precise visual-problem location
- no failure cascade

Exception: identical-content, parameter-only batch charts (per-country sub-charts) can be merged into one looping script.

### 3.2 Shared style template (chart_template.py)

Each project's `analyst-research/scripts/chart_template.py` is the drawing-style single source of truth. All `5_scripts/make_fig_*.py` tops have `import _path; from chart_template import setup_style, save_fig, PALETTE` (`_path.py` in §6.4). This guarantees consistent fonts, palette, margins, grid, spines, sizes, DPI, output formats. **No script may override these styles** unless the user explicitly approves.

Interface contract in §6.

### 3.3 PDF / JPG / clean-JPG triple output + content separation (core)

The three outputs **deliberately carry different content**, for three embedding scenarios:

| Element | PDF single-chart file (bare, for qmd) | JPG (independent distribution, self-contained) | _clean.jpg (for publication HTML) |
|---|---|---|---|
| chart core | yes | yes | yes |
| title (one level, carries the argument) | no (Quarto caption provides) | yes. top 14pt regular text colour | no (HTML template provides) |
| source | no (`\begin{figsource}` provides) | yes. bottom 9pt "Source: ..." | no (HTML `.exhibit-source` provides) |
| note | no (`\begin{figsource}` provides) | yes. bottom 9pt "Note: ..." | no (HTML `.exhibit-source` provides) |
| file suffix | `fig_*.pdf` | `fig_*.jpg` | `fig_*_clean.jpg` |

**Key discipline**:

- **single-chart PDF** (`6_figures/fig_*.pdf`): always bare. `chart_template.save_fig()` does not embed title / source / note in the PDF output, avoiding duplication with the Quarto caption. **For main-report qmd embedding.**
- **qmd-rendered report PDF**: each `![](fig.pdf)` reference **must be immediately followed by a `\begin{figsource}` environment**; each table's `: caption {#tbl-id}` **must be immediately followed by a `\begin{tblsource}` environment**. Fill source + note inside, rendered as 10pt grey (see §1.4)
- **JPG independent distribution** (`fig_*.jpg`): self-contained, title / source / note all embedded, 9pt bottom. **For WeChat, social distribution, and scenarios needing a single self-readable chart.**
- **_clean.jpg** (`fig_*_clean.jpg`): the no-burn-in raster landing with the PDF. **For publication-style HTML embedding** — the HTML template already provides `.exhibit-title` / `.exhibit-source`; embedding a burn-in JPG would double the title. (medium / light pass `clean=False` to skip generation.)
- **only one title level**, no subtitle. Press the argument into the title (e.g. "after rebasing nominal +14% / non-oil +20% / oil-and-gas -5.7%"), per FT "title carries the argument" (§2.4)
- **the three outputs produced in one `save_fig()` call**, the caller need not care; the script author writes `save_fig(fig, fig_id, title=..., source=..., note=...)` once and the three files land together

**Quarto qmd figure reference pattern**:

```markdown
![Metric X comparison, year X vs year Y](../6_figures/fig_1_1_topic.pdf){#fig-topic}

\begin{figsource}
Source: institution A annual report YYYY | Note: caliper supplement
\end{figsource}
```

**Quarto qmd table reference pattern**:

```markdown
| Metric | 2016 | 2024 |
|---|---|---|
| metric (%) | 19.3 | 35.85 |

: Metric comparison 2016 vs 2024 {#tbl-topic}

\begin{tblsource}
Source: institution B annual report YYYY Table 1 | Note: caliper supplement
\end{tblsource}
```

**Why raw LaTeX instead of a `:::` div**: Pandoc's div-class mapping has escape issues for hyphenated class names (`.figure-source`) on the LaTeX output side, with version-inconsistent behaviour across Quarto / Pandoc. A raw LaTeX environment is 100% reliable.

**Render-rule implementation** (add the LaTeX in the `_quarto.yml` `include-in-header`):

```latex
% figure-source / table-source environments 10pt grey (spec §1.4 + §3.3)
\usepackage{xcolor}
\definecolor{sourcegray}{gray}{0.4}
\newenvironment{figsource}
  {\par\smallskip\noindent\begingroup\fontsize{10pt}{12pt}\color{sourcegray}\selectfont}
  {\par\endgroup\medskip}
\newenvironment{tblsource}
  {\par\smallskip\noindent\begingroup\fontsize{10pt}{12pt}\color{sourcegray}\selectfont}
  {\par\endgroup\medskip}
```

**Where source / note info comes from**: copy directly from the matching `make_fig_*.py` script's `save_fig(source=..., note=...)` parameter values. The source / note strings written in the script are the figure's acknowledged source / note. When writing the figure-source block in draft.qmd, **keep the string consistent with the script**, do not rewrite it in the qmd (avoiding dual-source inconsistency).

One data set, three uses. chart_template manages the single chart and JPG, Quarto manages report-PDF embedding, mutually non-interfering.

### 3.4 In-chart fonts

- Chinese font = body Chinese font (e.g. Songti SC)
- English font = body English font (e.g. Times New Roman)
- size ≥ 9pt (FT print floor), max ≤ section-title size

### 3.5 Palette

Each project **fixes the palette before charting** (before workflow step 7 starts). Default FT palette (full HEX + semantics in §5.3).

No arbitrary colours, **no "big red + big green", no rainbow**. Scripts may not write colour strings directly; reference via the `PALETTE` interface.

### 3.6 Legend language consistency

- the report's main language decides the legend language (Chinese report → Chinese legend)
- exception: fixed professional acronyms (IMF / OECD / OPEC / GCC / GDP / FY / WACC / common central-bank, statistics-office, sovereign-fund acronyms) keep English
- **the legend does not overlap data elements**

### 3.7 One plot per chart (no side-by-side subplots) (hard rule)

**`make_fig_*.py` is single-axes only; `plt.subplots(1, 2, ...)` and any side-by-side layout is forbidden.**

**Reasons**:

- side-by-side subplots bring a chain of edge problems: (a)(b) subtitle height alignment, legend not overlapping a subplot, dual-subplot font shrink, single-side long y-label shifting everything right, (a)(b) vs suptitle visual confusion
- a single chart gets the full `FIG_W = 6.69 inch` horizontal width, a more spacious aspect ratio, 10pt font without compression
- on derivation (WeChat / Slack / email) each chart distributes independently, no slicing
- chart_template simplification: removes the multi-subplot branch, `TOP_PAD_PDF_MULTI_IN`, `SUBPLOT_TITLE_EXTRA_IN`, zero edge cases across projects

**Alternatives for "side-by-side comparison"**:

| Originally wanted side-by-side subplots | Single-chart alternative |
|---|---|
| before vs after / A vs B same-metric comparison | grouped bars (two-colour bars) or dual time-series lines |
| different metrics side by side | split into two independent charts, body says "the chart below ... the chart above ..." |
| multi-region / multi-country small-multiples | draw the 1-2 most critical countries in detail, the rest in a table |
| pie + scatter heterogeneous combo | split into two independent charts, one per passage |

**Implementation constraint**: `save_fig` prints a warning when it detects `len(fig.axes) > 1`; not allowed by spec, runs but visual risk is yours.

### 3.8 No element overlap (hard rule)

- data labels do not overlap the axes / data lines / bars
- **data-label / annotation text colour is not the same as any plot element below it**. Same colour makes the text "disappear" when a character falls on a same-colour bar (field lesson: an accent-colour annotation right on the accent-colour target bar top, text invisible). Two legal handlings: (1) move the text to blank space outside the bar; (2) change the text to `PALETTE["text"]` (black) or another neutral colour
- **legend hard rules** (no exception, uniform across all charts):
  - not covering the plot area (not occupying data space). **Forbidden** `loc="upper right" / "upper left" / "lower right" / "lower left" / "center" / "best"` and any in-plot legend placement
  - not overlapping data lines / bars / scatter / graphic elements
  - not below the plot (`bbox_to_anchor` y must not be negative)
  - **must lay out horizontally**: `ncol` takes "number of legend items" so all items spread in one row, **no** vertical stacking. **ncol fallback**: if the total item width estimate > image width (widest item × count + spacing), one row does not fit, fall back to `ncol = ceil(N / 2)` two rows (avoiding legend clipping). The judgement is rough; write `ncol=N` first, drop on overflow. Field case: a 7-item legend with a long item "市场驱动 (旅游 + 消费)" overflowed right at `ncol=7`, fixed at `ncol=4` two rows
  - **positioning is based on "the whole image", not the plot midpoint**. Two legal modes:
    - (1) **centered (default)**: the legend centre at figure-x = 0.5 (image center). **Do not** write `bbox_to_anchor=(0.5, 1.02)` directly — that is the plot midpoint, and in a horizontal bar with long y-tick labels the plot midpoint shifts right, the legend visually skews right. Convenience wrapper: `legend_above(ax, ncol=N, mode="centered")`, equivalent to `ax.legend(loc="lower center", bbox_to_anchor=((0.5-pos.x0)/pos.width, 1.02), ncol=N, frameon=False)` (pos = ax.get_position())
    - (2) **image-left (fallback when centered does not fit)**: with very many items / a row too wide, centered overflows both sides; image-left starts the legend from the figure's leftmost edge (incl. the y-axis label area, **not** the in-plot x=0), giving all available horizontal space to the legend. Convenience wrapper: `legend_above(ax, ncol=N, mode="image_left")`, equivalent to `ax.legend(loc="lower left", bbox_to_anchor=(-pos.x0/pos.width, 1.02), ncol=N, frameon=False)`. **Default stays centered, fall back here only when centered truly does not fit**
  - **leave about one line of space between title and legend**: `save_fig` auto-detects a plot-top legend (measuring with `leg.get_window_extent()` whether the legend bottom is ≥ the plot top), and on a hit auto-adds extra_top +`LEGEND_ABOVE_EXTRA_IN = 0.30 inch` to separate title and legend visually. **The script author need not adjust manually**, just call `ax.legend(...)` as usual
- dual-Y-axis data uses different markers / line styles, and the legend marks RHS / LHS
- caption / title text does not overlap axis ticks

### 3.9 Tables written directly in the body

**Tables use markdown / Quarto native table syntax in the qmd / md**, not the image pipeline. The reader can ctrl+F, copy, and Quarto handles cross-page tables by table semantics on PDF render.

No `save_table` to render a table to a PDF/JPG image — losing ctrl+F / copy, and visual consistency is not a strong enough reason to take a table out of the body flow.

### 3.10 Unusable elements

- no ±, ∓, ≈, ≤, ≥ math symbols in chart titles, axis labels, tick labels (the PDF backend's mathtext errors easily)
- no emoji
- no box / special geometric symbols for 1/2/3. Write 1 / 2 / 3 or Chinese "一、二、三" directly

### 3.11 JPG pixel cap (hard rule)

**Single-JPG long edge ≤ 2000px.** The Anthropic API's multi-image request has a 2000px long-edge hard cap; exceeding rejects the whole conversation. The PDF vector is not bound by this; this rule applies to JPG only.

Implementation: `save_fig` dynamically computes the JPG dpi by `dpi = min(200, floor(2000 / max(fig_w_in, fig_h_in)))`. The script author need not compute; just call `save_fig`.

Verification: during dev, after any script generates a JPG, sample-check the long edge with `sips -g pixelWidth -g pixelHeight 6_figures/*.jpg`. Any > 2000 is a bug, fix in `chart_template.py`.

### 3.12 Lock figure width to FIG_W (hard rule)

**All `make_fig_*.py` must use `figsize=(FIG_W, h)`** — `FIG_W` is a constant exported by `chart_template.py`, value **6.69 inch** (= A4 21cm − 20mm × 2 margins). Height `h` free by chart type (usually 3-4 inch).

**Why it must be locked**: Quarto scales the embedded PDF vector chart to `\textwidth`. If `figsize.width > 6.69`, the whole chart (incl. font) is scaled down proportionally. matplotlib's 10pt becomes 6-7pt in the PDF, breaking §5.2 spec. Locking `figsize.width = FIG_W = 6.69` gives a scale ratio of 1.0, so **matplotlib rcParams font size = actual PDF font size**.

**Positive example**:

```python
import _path  # noqa: F401
from chart_template import setup_style, save_fig, PALETTE, FIG_W

setup_style()
fig, ax = plt.subplots(figsize=(FIG_W, 3.5))
```

**Counter-example**: `figsize=(10, 5)` / `figsize=(11, 4.8)` or any hand-written width. Not even for temporary debugging — it leaves a hidden bug, and the next re-render finds the font shrunk.

**Height reference values**:

| Chart type | Recommended h |
|---|---|
| single-subplot bar / line | 3.0 - 3.5 |
| dual-subplot side by side | 3.0 - 3.5 |
| timeline / multi-layer structure | 3.5 - 4.5 |
| info-dense quadrant / heatmap | 3.5 - 4.0 |

**`subplots_adjust(left=…)` empirical values** (horizontal bars with long y-tick labels must be tuned manually, or the label is clipped by the left margin):

| Longest y-tick label chars | Recommended left |
|---|---|
| ≤ 3 chars ("2024", "日本") | 0.10 (default, no tuning) |
| 4-5 chars ("建筑业", "批零餐饮") | 0.20 |
| 6-10 chars ("教育与医疗", "某基金 AUM USD Bn") | 0.22-0.28 |
| 11+ chars / long English project names | 0.30-0.34 |

Tune to just enclose the longest label + one char of breathing room. **Self-check**: after rendering, look at whether the leftmost y-tick label in the JPG is complete (field debug: clipped a label prefix at 0.22, fully shown only at 0.34).

**PDF / JPG size relationship**:

| Output | Width | Height |
|---|---|---|
| caller figsize | `FIG_W = 6.69` | `h` (script-specified) |
| **PDF output** | `~6.4-6.7` (slightly < 6.69 due to `bbox_inches='tight'`) | `~h ± decoration` |
| **JPG output** | `FIG_W + 2 × 0.30 = 7.29` | `h + extra_top + extra_bottom` (heightened by actual suptitle / source / note line count) |

**The plot body's absolute size is identical in PDF and JPG** — the JPG just shifts the whole plot right 0.30 inch and down `extra_bottom`, no compression. This lets the script author control the plot aspect ratio (`figsize=(FIG_W, h)`, h sets the plot aspect), with the JPG's extra size auto-computed by save_fig by content.

### 3.13 4-item chart-script self-check

Each new or modified `make_fig_*.py` must self-check the 4 items below before commit; fix the script and re-render on a miss. These 4 are high-frequency cross-project pitfalls, **not visual checks** (visual check in §4, AI does not do it), but script-logic consistency self-checks.

| Redline | Expected |
|---|---|
| title number matches in-chart data | when title cites a specific number, f-string-insert via `df.loc[...].max()` or `argmax()`, do not write from impression; optional `assert` fail-safe |
| data-label / annotation colour not same as the plot element below it | accent text on an accent bar disappears. annotation defaults to text colour, accent data labels in white or a contrast colour |
| horizontal-bar y-tick labels fully shown | long labels need `subplots_adjust(left=...)`, empirical table in §3.12 |
| legend centered and horizontal | use `legend_above(ax, ncol=N, mode="centered")`; fall back to `ncol=ceil(N/2)` two rows if it does not fit |

Visual self-check is still the user's, see §4.

---

## 4. Visual check

**The AI does not do visual checks.** After rendering, the AI only lists the JPG / PDF paths; the user opens them. Reasons: (1) the AI's vision model is unstable on CJK fonts and misjudges; (2) many images hit the API pixel cap (§3.11); (3) the user's taste and emphasis judgement beat the AI's.

No checklist, no hard-stop gate. The user goes back to the specific script to fix on finding a problem.

---

## 5. Defaults & templates

### 5.1 Quarto YAML standard header (Chinese report)

Project-level `_quarto.yml`:

```yaml
lang: zh
format:
  # 10b Word docx derivation (workflow §step 10b): default Pandoc style is enough;
  # for a project-branded Word template (fonts / header / footer), add:
  #   docx:
  #     reference-doc: reference.docx
  pdf:
    toc: true
    toc-depth: 2
    lof: true
    lot: true
    lof-title: "图目录"
    lot-title: "表目录"
    number-sections: true
    fig-cap-location: top
    tbl-cap-location: top
    pdf-engine: xelatex
    documentclass: ctexart
    fontsize: "11pt"
    linestretch: 1.5
    indent: false
    geometry:
      - top=25mm
      - bottom=25mm
      - left=20mm
      - right=20mm
    include-in-header:
      text: |
        % === fonts ===
        \usepackage{fontspec}
        \setmainfont{Times New Roman}
        \setCJKmainfont{Songti SC}
        \newfontfamily\arabicfont[Script=Arabic]{Noto Sans Arabic}

        % === first-line indent / paragraph spacing (see §1.5) ===
        \setlength{\parindent}{0pt}
        \setlength{\parskip}{0.5em}

        % === 6-size forced alignment (18 / 16 / 14 / 12 / 11 / 10 pt, see §1.4) ===
        % main title 18pt bold, subtitle 16pt regular, author / date 11pt
        \usepackage{titling}
        % \droptitle controls the main title's distance from the page top; cannot use
        % \pretitle{\vskip ...} because a page-top \vskip is dropped by TeX default
        % (vmode + page-start glue auto-consumed)
        \setlength{\droptitle}{4em}
        \pretitle{\begin{center}\fontsize{18}{22}\bfseries\selectfont}
        \posttitle{\par\end{center}\vskip 2em}
        \preauthor{\begin{center}\fontsize{11}{14}\selectfont}
        \postauthor{\par\end{center}}
        \predate{\begin{center}\fontsize{11}{14}\selectfont}
        \postdate{\par\end{center}\vskip 2em}
        % override Quarto/pandoc default \subtitle (default \large ≈ 12pt shrinks size)
        % \makeatletter needed because \@title contains @ requiring letter catcode
        \usepackage{etoolbox}
        \makeatletter
        \providecommand{\subtitle}[1]{%
          \apptocmd{\@title}{\par\medskip {\normalfont\fontsize{16}{20}\selectfont #1 \par}}{}{}%
        }
        \makeatother

        % h1 section title 14pt bold, h2 subsection title 12pt bold
        \usepackage{titlesec}
        \titleformat{\section}{\fontsize{14}{17}\bfseries\selectfont}{\thesection}{1em}{}
        \titleformat{\subsection}{\fontsize{12}{15}\bfseries\selectfont}{\thesubsection}{1em}{}

        % TOC / LoF / LoT: title 14pt bold centered, entries 11pt regular
        % implementation: directly override the three \@cftmake?title hooks, wrapping
        % the title with \begin{center}...\end{center}. Reason: tocloft's built-in \hfill
        % centering is unreliable in article mode when the title follows preceding text
        % (like an abstract), often offset right
        \usepackage{tocloft}
        \renewcommand{\cfttoctitlefont}{\fontsize{14}{17}\bfseries\selectfont}
        \renewcommand{\cftloftitlefont}{\fontsize{14}{17}\bfseries\selectfont}
        \renewcommand{\cftlottitlefont}{\fontsize{14}{17}\bfseries\selectfont}
        \renewcommand{\cftsecfont}{\fontsize{11}{14}\selectfont}
        \renewcommand{\cftfigfont}{\fontsize{11}{14}\selectfont}
        \renewcommand{\cfttabfont}{\fontsize{11}{14}\selectfont}
        \makeatletter
        \renewcommand{\@cftmaketoctitle}{%
          \addpenalty\@secpenalty\vspace{\cftbeforetoctitleskip}\@cftpagestyle
          \begin{center}{\cfttoctitlefont\contentsname}\end{center}%
          \cftmarktoc\par\nobreak\vskip\cftaftertoctitleskip\@afterheading}
        \renewcommand{\@cftmakeloftitle}{%
          \addpenalty\@secpenalty\vspace{\cftbeforeloftitleskip}\@cftpagestyle
          \begin{center}{\cftloftitlefont\listfigurename}\end{center}%
          \cftmarklof\par\nobreak\vskip\cftafterloftitleskip\@afterheading}
        \renewcommand{\@cftmakelottitle}{%
          \addpenalty\@secpenalty\vspace{\cftbeforelottitleskip}\@cftpagestyle
          \begin{center}{\cftlottitlefont\listtablename}\end{center}%
          \cftmarklot\par\nobreak\vskip\cftafterlottitleskip\@afterheading}
        \makeatother
        % Forced breaks (§1.7 / §1.8):
        % - \clearpage before TOC (standalone, not after the abstract)
        % - \clearpage before LoF (prevents the orphan title to the previous page bottom)
        % - \clearpage before LoT (same)
        % - \clearpage after LoT (entering the body)
        % Note: tocloft redefines \tableofcontents / \listoffigures / \listoftables inside
        % \AtBeginDocument, so the patch must also be wrapped in \AtBeginDocument and take
        % effect after tocloft registers
        \AtBeginDocument{%
          \pretocmd{\tableofcontents}{\clearpage}{}{}%
          \pretocmd{\listoffigures}{\clearpage}{}{}%
          \pretocmd{\listoftables}{\clearpage}{}{}%
          \apptocmd{\listoftables}{\clearpage}{}{}%
        }

        % No header throughout, centered footer page number (§1.11)
        % overrides the ctex chinese-article scheme default \pagestyle{headings}
        \pagestyle{plain}

        % Abstract: title 14pt bold centered (same tier as TOC/LoF/LoT titles), body 11pt regular
        \renewenvironment{abstract}
          {\par\medskip{\centering\fontsize{14}{17}\bfseries\selectfont 摘要\par}\medskip\normalsize}
          {\par\medskip}

        % figure / table caption 11pt italic
        \usepackage{caption}
        \captionsetup{font={normalsize,it},labelfont={normalsize,bf,it}}

        % footnote 11pt (override LaTeX default \footnotesize=9pt)
        \renewcommand\footnotesize{\fontsize{11}{14}\selectfont}
execute:
  echo: false
  warning: false
  message: false
  freeze: auto
```

For a non-Chinese project, replace the CJK font block, `documentclass`, `lang` as needed (e.g. an English report uses `lang: en` and an English abstract title). The 6-size forced override is in the §1.4 table and LaTeX-header comments.

### 5.2 In-chart font sizes (chart_template quick-reference)

Document-layout sizes in §1.4, not repeated here. This section **only lists in-JPG self-contained elements**; the true values are set by `chart_template.setup_style()`.

In-chart **only two sizes**: 12pt suptitle + 10pt everything else. Simplifies the hierarchy, avoiding visual fragmentation from too many in-chart text tiers.

| Element | Chinese | English | Size | Weight | Colour (see §5.3) |
|---|---|---|---|---|---|
| chart title (in JPG, suptitle) | Songti SC | Times New Roman | 12pt | **regular** (FT) | text |
| in-chart data label / emphasis note | Songti SC | Times New Roman | 10pt | regular | text |
| axis text / legend / tick | Songti SC | Times New Roman | 10pt | regular | text_light |
| in-chart table body | Songti SC | Times New Roman | 10pt | regular | text |
| in-chart table header | Songti SC | Times New Roman | 10pt | bold | text |
| in-chart source / note | Songti SC | Times New Roman | 10pt | regular italic | text_light |

**Size alignment with document layout**: chart title 12pt = h2 subsection title; all other in-chart 10pt, one tier below body 11pt, so chart text does not dominate the body when embedded. In-chart fonts strictly match the body.

**Alignment and layout detail** (save_fig implementation, §6.3):

- **three texts left-aligned to the PDF left edge**: title / source / note uniformly `x_frac = JPG_HMARGIN_IN / fig_w_jpg`, i.e. the "PDF original left boundary" in the JPG. This line = the chart's leftmost visible content (y-label leftmost char). Usable width = `fig_w_pdf = 6.69 inch` (full PDF width, covering the y-label area + plot data area), text wraps to the PDF right edge
- **JPG adds `JPG_HMARGIN_IN = 0.30 inch` whitespace on each side**: total JPG width = PDF width + 2 × 0.30 = 7.29 inch. The plot shifts 0.30 inch right vs the PDF, absolute size unchanged
- **precise-pixel wrap** (`_wrap_text_precise`): renders the candidate string with matplotlib, measures the real pixel width, binary-searches the longest fitting prefix. **The only line-break constraint** is that English words / numbers cannot be split (protected charset `[A-Za-z0-9.,%+\-]`). Chinese characters break at any position. **No more char-count estimation + punctuation back-break** — precise measurement + word-only protection, text fits almost to the PDF right edge before wrapping
- **continuation hanging indent**: when source / note wraps to a second line, indent with 3 full-width spaces (source) / 2 (note), aligning the continuation to the first char after "Source:" / "Note:"
- **1 extra blank line between plot bottom ↔ source** (in the save_fig constant `PLOT_BOTTOM_GAP_IN = 0.45`). After one-plot-per-chart, no extra top space for (a)(b) subtitles

ctexart defaults to 11pt + Chinese-punctuation compression. **The first-line indent is explicitly overridden to zero by §5.1**, replaced by half-line paragraph spacing (§1.5).

### 5.3 Palette (FT colour quick-reference)

**The true values are in `chart_template.PALETTE` dict.** This table is a human quick-reference of the FT chart-doctor defaults; **when the project overrides HEX, this table drifts from the code; the code wins.**

| Interface name | HEX (FT default) | Use |
|---|---|---|
| `primary` | `#0F5499` Oxford blue | main data series / current subject |
| `secondary` | `#208FCE` Medium blue | secondary data series / comparison / historical |
| `tertiary` | `#C2B7AF` Warm gray | weakened data series / third group / background bar |
| `accent` | `#7F062E` Claret | **single-point emphasis** (single accent principle, §2.3) |
| `accent_alt` | `#EB5E8D` Warm pink | alternative accent |
| `accent_light` | `#FCE2D1` Claret light | table highlight row background |
| `neutral` | `#66605C` Warm dark gray | reference line / average |
| `grid` | `#D6D0CA` light warm gray | y-axis horizontal grid line |
| `axis` | `#66605C` warm dark gray | axis spine + tick |
| `baseline` | `#999999` neutral gray | 0 / reference line |
| `bg` | `#FFFFFF` white | chart background (embedding in Quarto white-paper PDF) |
| `text` | `#000000` black | main text (title) |
| `text_light` | `#66605C` warm dark gray | secondary text (axis label / source / note / legend) |

Multi-series extension `PALETTE_EXTENDED` 7 colours (in FT categorical_line order) + single-colour progression `PALETTE_SEQUENTIAL` 7 colours, HEX read directly from `chart_template.py`.

The interface name `PALETTE` is preserved cross-project. HEX values can be project-overridden (register the reason in the project CLAUDE.md "deviations from the framework" section); scripts **may not write colour strings directly**, must reference via `PALETTE['xxx']`.

---

## 6. chart_template interface contract

Implementation in the same-dir `chart_template.py`. This section covers "how an external script calls it". The script author only needs to read this section, not the chart_template source.

### 6.1 `setup_style()`

No arguments. Call once at the top of each drawing script, configuring matplotlib global rcParams (fonts, colours, spines, grid, line width, ticks, legend, output dpi, etc.).

```python
import _path  # noqa: F401  -- see §6.4
from chart_template import setup_style
setup_style()
```

### 6.2 `PALETTE` / `PALETTE_EXTENDED` / `PALETTE_SEQUENTIAL`

dict / list. Colour references must go through this interface, no hardcoded HEX in scripts.

```python
from chart_template import PALETTE
ax.bar(x, y, color=PALETTE["primary"])
ax.axhline(0, color=PALETTE["baseline"])
```

Two more constants exported from `chart_template`:

- `FIG_W = 6.69` (float, inch): the figsize width all `make_fig_*.py` must use, see §3.12
- `DATA_PROC` (Path): points to `4_data/2_processed/`, avoiding hardcoded relative paths in scripts

### 6.3 `save_fig(fig, fig_id, title=None, source=None, note=None, subdir="", lang="zh", clean=True)`

PDF (bare, for qmd) + JPG (with burn-in, independent distribution) + `_clean.jpg` (bare raster, for publication-style HTML) triple output. One call, all land.

| Param | Type | Description |
|---|---|---|
| `fig` | matplotlib Figure | the figure the caller assembled |
| `fig_id` | str | filename prefix, e.g. `"fig_1_1_topic"` |
| `title` | str / None | JPG top one-level title; not written to PDF |
| `source` | str / None | JPG bottom "Source: ..." on its own line; not written to PDF |
| `note` | str / None | JPG bottom "Note: ..." on its own line (below source); not written to PDF |
| `subdir` | str | subdirectory (default lands directly in `6_figures/`) |
| `clean` | bool | whether to generate `_clean.jpg` (default True, needed for heavy publication HTML). medium / light pass `clean=False` to skip |

Behaviour guarantees:

- **PDF uses the caller figsize** (`figsize=(FIG_W, h)`), keeping plot + necessary axis decoration + above/below legend, **not drawing** suptitle / source / note (provided by the Quarto caption + `{.figure-source}` block in the qmd). No (a)(b) subtitles after one-plot-per-chart
- **PDF top padding uniformly 0.10 inch**. After one-plot-per-chart (§3.7) there are no (a)(b) subtitles, no extra top reserve needed
- **PDF saved with `bbox_inches='tight'`**: auto-expands to include all visible content (plot-bottom legend, long y-label). The cost is the PDF actual size may be slightly < `figsize`; Quarto scales it to textwidth on embedding (about 5% enlargement), font scaling accordingly. This is the trade-off for not clipping a "legend in plot bottom" chart's legend
- **JPG three-way expansion**: `figsize=(fig_w_pdf + 2 × JPG_HMARGIN_IN, fig_h_pdf + extra_top + extra_bottom)`, where `JPG_HMARGIN_IN = 0.30 inch` is the left/right whitespace, `extra_top` holds the suptitle area, `extra_bottom` holds the source / note area. **The plot body's absolute size is identical to the PDF** — save_fig shifts the plot right / down via `fig.set_size_inches` + `subplots_adjust`, not compresses
- **three texts left-aligned to the PDF left edge, right-wrapping to the PDF right edge**: title / source / note all `x_frac = JPG_HMARGIN_IN / fig_w_jpg` (= the PDF left boundary in the JPG), usable width = `fig_w_pdf` (covering y-label area + plot data area). The text box aligns to the chart's leftmost / rightmost
- **precise-pixel wrap**: `_wrap_text_precise` renders the candidate text with matplotlib, measures the real pixel width, binary-searches the longest fitting prefix; **the only line-break constraint** is that English words / numbers cannot be split (protect `[A-Za-z0-9.,%+\-]`). Chinese characters break anywhere. Continuation hanging indent (source 3 full-width spaces, note 2) aligns to the first char after "Source:" / "Note:"
- design rationale: (1) the script author only cares about the plot's aspect ratio (writing `figsize=(FIG_W, 3.5)` is the desired plot shape), suptitle / source / note vertical space auto-heightened by save_fig by content, not squashing the plot; (2) the three texts align to the PDF edge for a consistent visual frame; (3) precise wrap avoids the right-edge jaggedness of char-count estimation, text fills almost the full PDF width before wrapping
- JPG long edge auto ≤ 2000px (§3.11 hard rule). At fig_w_jpg ≈ 7.3 inch + dynamic dpi, the long edge is ~2000px near the cap
- **`_clean.jpg` saved right after the PDF lands, before the JPG adds text** (when `clean=True`): using the PDF's then figsize + `bbox_inches='tight'` + `dpi=200` + white bg. At `FIG_W=6.69` about 1338px wide, well below the 2000px cap. For publication-style HTML direct `<img src>` embedding

### 6.4 Call template

Boilerplate at the top of each `5_scripts/make_fig_*.py`:

```python
"""make_fig_<section>_<n>_<topic>.py · <one-line purpose>

Input: 4_data/2_processed/<src>.csv
Output: 6_figures/<fig_id>.{pdf,jpg} + <fig_id>_clean.jpg
"""
import pandas as pd
import matplotlib.pyplot as plt
import _path  # noqa: F401  -- add analyst-research/scripts/ to sys.path
from chart_template import setup_style, save_fig, PALETTE, FIG_W, DATA_PROC

setup_style()


def main():
    df = pd.read_csv(DATA_PROC / "<src>.csv")
    # width must be locked to FIG_W (see §3.12); height free by chart type, table in §3.12
    fig, ax = plt.subplots(figsize=(FIG_W, 3.5))
    ax.bar(df["x"], df["y"], color=PALETTE["primary"])
    save_fig(fig, "fig_1_1_topic",
             title="<fact + number carries the argument>",
             source="<institution + year + report name>",
             note="<optional>")
    plt.close(fig)


if __name__ == "__main__":
    main()
```

**`_path.py` is required**: path `5_scripts/_path.py`, 4 lines:

```python
"""Add analyst-research/scripts/ to sys.path so 5_scripts/ scripts can import chart_template."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "analyst-research" / "scripts"))
```

At the new-project scaffold stage, `5_scripts/_path.py` must be created first to import `chart_template`.

---

## 7. publication-style HTML derivation (step 10 optional derivation)

After the main-report qmd → PDF is done, you can optionally make a "consulting / FT long-form style" HTML → PDF, for WeChat long-form, client distribution, social sharing, and other scenarios needing stronger visual identity. This section is the **spec** for that HTML template. The skill bundles a neutral long-form-style HTML template at `scripts/publication-style-template.html`; all specs below are implemented against this template.

### 7.1 When to do, when not to

**Conditions to do**:

- the main report has finished step 9 (user signed off)
- content is relatively stable, no big changes expected
- the audience or scenario needs stronger visual identity (consulting style, magazine style, social sharing)

**When not to**:

- content still changing (HTML / qmd dual-source sync is a hidden burden)
- time is tight or it is unnecessary
- the main-report PDF already meets the audience's expectation

**Important principles**:

- **the qmd is the source of truth**. The HTML is a derivative, content copied from the signed qmd, no content revision on the HTML
- **the HTML template is not regenerated repeatedly with a builder script**. After one generation, switch to manual maintenance; write the builder, use it once, delete it, avoiding re-render overwriting manual adjustments

**Template starting point (two paths)**:

- **Path A (default, recommended)**: the skill-bundled `scripts/publication-style-template.html` is a neutral long-form ready-to-use template. At step 10c, copy it to project `8_publication/2_HTML/<project>-publication-style.html`, fill each page per the §7.8 content-mapping table, manually tune pages in VS Code Live Preview per §7.3
- **Path B (alternative style)**: for other consulting-style differentiation (BCG green, McKinsey blue, Bain red), call the `consulting-report-style` skill to generate a substitute template, then fine-tune per §7 sub-sections (the 1 div = 1 A4, `_clean.jpg` embedding, footer-in-HTML disciplines are universal across styles)

The skill bundles only one template, as "a ready-to-use start + a style-reference implementation". It does not maintain multiple styles inside the skill.

### 7.2 Core model: 1 div = 1 A4 page (WYSIWYG)

The core discipline of the HTML → PDF link is **"what you see is what you get"**: what the HTML looks like in the browser is what the PDF looks like, the PDF converter adds no visual elements.

- each `<div class="page">` is physically one A4: `width: 210mm; height: 297mm; overflow: hidden`
- `@page { size: 210mm 297mm; margin: 0; }` locks the PDF page size
- the footer / page number **must go into the HTML's own `<div class="page-footer">`**, not `@page { @bottom-* }` letting Chrome overlay it at the PDF stage
- the page number uses a CSS counter (`counter-reset: pagenum`/`counter-increment: pagenum`/`::before { content: counter(pagenum) }`), auto-incrementing, cover and back-cover skipped
- when manually saving the PDF in the browser (§7.6), turn off the print dialog's "headers and footers" option, forbidding browser auto-add

**Iron rule**: any visual / layout adjustment → edit the HTML → see immediately in the browser. **Never add visual logic in the PDF-conversion script** — the script's only job is "convert format".

### 7.3 Handling content overflow

A fixed-height page div has no auto-pagination; overflow or whitespace must be tuned manually. **There is no reliable auto-reflow** (paged.js changes the page model and is occasionally inconsistent with Chromium `--print-to-pdf`; a JS dependency is not worth it).

**Operating flow**:

1. install the VS Code **Live Preview** extension (`ms-vscode.live-server`), open the HTML and click "Open Preview to the Side" (`Cmd+Shift+V`), edit code on the left / live-refresh browser on the right
2. look page by page in the browser: which overflows, which has whitespace
3. in VS Code `Cmd+F` the page's signature text to locate the matching `<div class="page body-page">`
4. **cut a `<p>` or `<figure>` to the next page's start** (or pull the next page's start paragraph to this page's end)
5. save → browser refreshes → re-look
6. **scan front to back**: a front-page change affects the back pages' crowding, flatten in page order in one chained pass

A WYSIWYG HTML editor (BlueGriffon) is not recommended: it rewrites your class structure. **A plain-text editor + browser preview** is most stable for this custom CSS template.

### 7.4 Figure embedding: use `_clean.jpg` not `.jpg`

The publication-style HTML template provides its own `.exhibit-title` / `.exhibit-source` blocks. **Must use `fig_*_clean.jpg`** — `fig_*.jpg` already burns in title / source, embedding it again gives "double title + double source".

```html
<figure class="exhibit">
  <div class="exhibit-label">Exhibit 1</div>
  <div class="exhibit-title">title provided by the HTML template</div>
  <div class="exhibit-figure">
    <img src="../../6_figures/fig_1_1_topic_clean.jpg" alt="...">
  </div>
  <div class="exhibit-source"><strong>Source:</strong> ...</div>
</figure>
```

`_clean.jpg` is auto-produced by `chart_template.save_fig()` (§3.3 / §6.3), the script author needs no extra action.

### 7.5 Cover / chapter title page / author headshot

- **cover**: full-bleed gradient / photo bg + large title + subtitle + date; accent bar at the bottom-right, recommended above an "independent research report" corner-mark
- **chapter title page**: the banner holds the chapter Chinese label (e.g. "第一章" 42pt) + English small-caps ("CHAPTER ONE" 9pt). Do not repeat the chapter number in the body, the banner already carries the identifier
- **author headshot**: place a local `Gen.jpg` (or author name), embed with CSS `<img>` `.author-headshot { border-radius: 50% }` circular crop. Compress under 1MB (recommended long edge ≤ 1200px)
- **headshot composition trap**: with a 1:1 container and a 1:1 image, CSS `object-fit` has no croppable space. If the original's high forehead is cut by the circle, use PIL to add white space at the top to push the face down:
  ```python
  from PIL import Image
  im = Image.open('Gen.jpg')
  new = Image.new('RGB', (im.width, im.height + 140), 'white')
  new.paste(im, (0, 140))
  new.save('Gen.jpg', 'JPEG', quality=85)
  ```

### 7.6 HTML → PDF conversion

Save manually in the browser, do not write a script. Open the HTML in Chrome or Safari, Cmd+P for the print dialog, change the target to "Save as PDF", turn off "headers and footers", margins "none", save to `8_publication/2_HTML/`. Combined with §7.2 "page number in HTML" and §7.5 "footer div" for WYSIWYG.

Manual save's advantage is zero config, zero environment dependency, most stable for a single publication. Command-line renderers (headless Chrome `--print-to-pdf` / prince / weasyprint) are worth introducing only for batch automation or CI integration; do not take this path for a first publication.

### 7.7 Directory convention

publication-style HTML + PDF land in `8_publication/2_HTML/`. Three subdirs numbered by generation order:

```
8_publication/
├── 1_word/                             10b Word docx derivation
│   └── <project>.docx                  Pandoc auto-generated, for client review / annotation
├── 2_HTML/                             10c publication-style HTML + PDF
│   ├── <project>-publication-style.html
│   ├── <project>-publication-style.pdf
│   └── author.jpg                      author headshot (skill-bundled placeholder, replace per §7.5)
└── 3_wechat_pages/                     10d WeChat JPG slices (10c PDF per page)
    ├── page_01.jpg
    └── ...
```

**The main-report PDF is not in this directory**: the qmd-rendered `draft.pdf` stays in `7_draft/` for direct view and distribution, avoiding dual maintenance. The frozen version is managed by git tag or filename suffix (`draft_v3.pdf`).

**Iron rule**: do not leave a builder script in `2_HTML/`. After a one-time generation, switch to manual maintenance; re-running the builder overwrites manual adjustments.

### 7.8 Content mapping: qmd main report → publication HTML

See `workflow_heavy.md §9` (derivation conversion table). The HTML template additionally carries:

| Element | How to write in the HTML template |
|---|---|
| chapter title-page large text | `.chapter-opener .banner .ch-label` |
| chapter English small-caps | `.chapter-opener .banner .ch-label-en` |
| Pull quote | `<div class="pull-quote">` |
| Exhibit number | `<div class="exhibit-label">Exhibit N</div>` |
| abstract page | `.page.abstract` + eyebrow + accent-bar + h2 + body |
| TOC page | `.page.contents` + `.toc-list` |
| references page | `.page.references` + `.references-list` with hanging indent (`padding-left: 34mm; text-indent: -34mm`), ref-key fixed width 32mm to avoid a long key wrapping wrong |
| author page | `.page.authors` + author-card flex layout + local headshot img |
| cover / back cover | `.page.cover` / `.page.back-cover`, full-screen padding: 0 |

**h2 text rule for chapter-title-page classes (abstract / contents / references / authors)**: use the **plain section name** ("Abstract", "Contents", "References", "About the Author"), not a distilled hook sentence.

- counter-example: `<h2>Three layers of accounting processing systematically amplify book achievements at the narrative level</h2>`
- positive example: `<h2>Abstract</h2>`
- reason: a distilled hook overlaps the eyebrow (`ABSTRACT · 摘要`) and steals body focus; the plain section name keeps h2's visual anchor (the first-line 30+pt large text) as page-structure positioning, the hook belongs to the body's first sentence or a pull-quote

### 7.9 WeChat JPG slices (optional derivation)

After the publication-style PDF renders, the WeChat long-form channel can slice the PDF into per-page JPGs (the WeChat editor supports image sequences natively, does not take PDF directly). Land in `8_publication/3_wechat_pages/`, named `page_NN.jpg` (zero-padded two digits).

The specific slicing tool and DPI are set by the user per scenario (200 DPI is common; the WeChat body image width is responsive, insensitive to long-edge pixels). Common CLI options: `pdftoppm -jpeg -r 200 input.pdf page` or the macOS Automator "Render PDF Pages as Images" action.

Do this only when the WeChat long-form channel is needed; the main-report PDF is already paginated and needs no such derivation.

---

## 8. AI disclosure footer (mandatory in each PDF)

At the end of each PDF, immediately before the references, add an AI-use disclosure. Professionalism + transparency + traceability, done in 5 lines.

### 8.1 Standard copy (bilingual ready)

English version (for EN PDFs):

```markdown
::: {.callout-note appearance="minimal" icon=false}
**About this report.** This report was produced using the [analyst-research](https://github.com/genli-ai/market-research-skills) workflow, an open-source Claude skill that codifies investment-research methodology (source provenance, three-state labelling, multi-source caliper analysis). Every numerical claim traces to a primary source listed in the bibliography; verifying records are preserved in the project's `_process/` folder. The analysis, judgement, and final sign-off are the author's; AI handled source aggregation, drafting, and citation formatting under explicit human checkpoints.
:::
```

Chinese version (for zh PDFs):

```markdown
::: {.callout-note appearance="minimal" icon=false}
**关于本报告**：本报告使用 [analyst-research](https://github.com/genli-ai/market-research-skills) 工作流生成。该工作流是一个开源 Claude skill，封装了投研方法论（来源可追溯、三态标注、多源口径辨析）。所有数字均可追溯至参考文献列出的一手来源，verifying 记录保存在项目 `_process/` 目录。分析判断与最终签字由作者负责；AI 在显式人工检查点下承担素材汇总、初稿撰写、引用格式化工作。
:::
```

### 8.2 Placement

Insert at the end of `draft.qmd`, **before** the `# 参考文献 / # References` section title. Quarto renders it as the last body paragraph, unnumbered.

```qmd
... final body paragraph ...

{{< pagebreak >}}

::: {.callout-note appearance="minimal" icon=false}
**About this report**: ... (pick the EN / zh template above)
:::

{{< pagebreak >}}

# References {.unnumbered}

::: {#refs}
:::
```

### 8.3 Three-mode differences

| mode | include? | reason |
|---|---|---|
| light | optional | a 5-page memo is tight; the author may judge; if included, a footer line is enough, not a separate block |
| medium | **mandatory** | a half-day product, professionalism matters; add per the 8.1 template |
| heavy | **mandatory** | a flagship report often externally published, high transparency + compliance value |

### 8.4 Cross-tool compatibility

`::: {.callout-note ...}` is native Quarto syntax; rendering PDF it becomes a light-grey box + "Note" prefix (with `appearance="minimal" icon=false` per the 8.1 template it becomes an undecorated plain-text block). If the user derives Word, Pandoc converts the callout to a left-bordered blockquote; HTML derivation keeps the callout style. Visually consistent across channels.

### 8.5 Design principle (why not a longer disclaimer)

- **within 5 lines**: a long disclaimer (like an academic venue's half-page AI policy) is redundant for an investment-research product doc.
- **not stealing focus**: `appearance="minimal" icon=false` keeps it visually low-key, seen only on the last page.
- **not disclaiming responsibility**: state "the analysis, judgement, and final sign-off are the author's", with the AI role limited to "source aggregation, drafting, citation formatting under explicit human checkpoints". This pins the checkpoint responsibility on the author, not letting the reader think this is "AI auto-generated, author hands-off".
- **traceable**: state that the `_process/` folder has the verifying records, giving a reader who really wants to audit a foothold.
