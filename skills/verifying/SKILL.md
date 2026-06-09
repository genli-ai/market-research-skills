---
name: verifying
description: >-
  Use when verifying information (fact, number, quote, event, statement)
  against authoritative primary sources, or cross-checking a number via
  one-level metric decomposition (Z = P × Q). Triggers: "verify X", "is this
  true", "find the original source", "where is this number from", "two sources
  disagree", "is it true X never did Y". Covers five scenarios: (1) basic
  truthfulness check, (2) completeness / out-of-context quoting, (3) one-level
  reasoning verification, (4) negative-statement handling, (5) multi-source
  conflict side-by-side output. Dig into whitelisted primary sources only
  (user-supplied files, official websites & databases, authoritative industry
  sources); cited reports / charts / datasets must be downloaded and read
  locally to count as verified — if download is blocked, hand the link to the
  user. If nothing can be found, plainly state "cannot verify" rather than
  guessing, patching, or citing secondary paraphrases. Always reply in the
  user's question language.
---

# Information Verification Skill

> Bilingual skill. Chinese version: `SKILL.zh.md`. English is the single source of truth; the `.zh.md` is a synchronized translation — always edit the English first, then mirror the change into `.zh.md` in the same change-set, never edit only the Chinese.

## Purpose

The user provides a sentence or paragraph that needs verification. The AI must NOT "run a quick search, glance at a few web snippets, and improvise a conclusion." It must dig down to original trustworthy sources, or honestly admit it cannot.

Five scenarios are covered:

1. **Basic truthfulness check**: whether the numbers / facts / quotes in the statement are accurate.
2. **Completeness**: when the source is correct but the user's quotation is out of context — supply the missing context.
3. **One-level reasoning verification**: when a direct number cannot be traced to a primary source, cross-check via metric decomposition (Z = P × Q).
4. **Negative statements**: detect unfalsifiable claims like "X has never done Y" and switch to a "search for a counter-example" path.
5. **Multi-source conflict**: when two authoritative sources disagree on the same figure, present them side-by-side with a difference attribution.

## Input

The user supplies one statement (or paragraph) to verify. Optional attachments (PDFs, links, screenshots, notes) take priority as material to verify against.

## Scope exclusions (refused topics)

Before any verification work begins, check whether the statement falls into a refused category. The following topics are out of scope regardless of how the request is phrased or how specific the question is:

- **Political issues** — elections, parties, political figures' positions, geopolitical disputes, government legitimacy debates, etc.
- **Military issues** — military operations, force composition, equipment counts, conflict details, defense policy, etc.
- **Religious issues** — doctrines, denominational disputes, religious leaders' statements, inter-faith comparisons, etc.
- **Entertainment celebrity gossip** — personal lives, relationships, family affairs, paparazzi rumors, etc.
- **Other inherently controversial topics** — even attempting verification can be inflammatory regardless of what the answer turns out to be.

When a request falls into any of these categories, reply with exactly one line and stop:

> Out of scope. (超出能力范围)

Do NOT attempt verification, partial verification, "let me try anyway," or step-by-step analysis. Do NOT explain why beyond this one line. Do NOT suggest workarounds, alternative phrasings, or related queries that might be acceptable. The line above is the entire response.

This check happens **before** scenario routing — if it triggers, none of the rest of the skill runs.

## Scenario routing

Internally classify the statement into one of the five scenarios to pick the right sub-flow (one-level reasoning / negative / multi-source conflict use their own emoji label). Do NOT print the scenario label as a separate line — it does not help the user. If a statement spans multiple scenarios, use the dominant path and address the others as supplements.

## Response language

Always reply in the same language as the user's question (Chinese in → Chinese out; English in → English out; mixed → follow the dominant language of the question).

Emoji labels (`✅ ⚠ ❌ 🔎 ⚖ 🔒`) are language-neutral and stay the same in both languages. Translate the prose that follows the emoji — e.g. `✅ Verified.` → `✅ 已核实。`. Metadata field names, when surfaced, translate too: `Time point / Definition / Unit / Coverage / Revision status / Data type` → `时点 / 口径 / 单位 / 范围 / 修订状态 / 数据类型`.

Internal logic, whitelist, and rule structure are language-neutral — do not change them.

## Tool-call mapping (cross-LLM adaptation)

When this skill runs on different LLM terminals, the actions below map to whichever local tools that terminal exposes. The table describes action semantics only — no terminal-specific tool names are hard-coded.

| Action | Meaning |
|---|---|
| Read full text | Load and fully understand a PDF / md / txt / csv document |
| Fetch web body | Pull the page text from a URL (NOT just a search-engine snippet) |
| Search-engine query | Run a keyword query on a search engine |
| Image recognition | Multimodal reading of a screenshot or chart |
| Database query | Query a structured data source by field |

## Trusted-source whitelist

Only the source types below count as evidence for "verification succeeded." This section is self-contained and does not depend on external documents.

### On "representative list vs. exhaustive list"

The specific institutions / websites / databases listed under each subcategory below are **representative examples, not an exhaustive enumeration**. Other sources at the **same tier and same nature** qualify equally — for example, central banks of other sovereign nations not listed here, national statistics agencies, well-known international think tanks, regional authoritative media, industry-specific primary databases, etc. Apply the three criteria below by analogy:

| Criterion | Accept | Reject |
|---|---|---|
| **Institution nature** | Official (government / central bank / regulator / multilateral international institution); authoritative specialist (top think tank / peer-reviewed academia / mainstream IB or consulting Research); independent third-party (reputable aggregator databases) | Personal blogs, self-media, content farms, SEO sites |
| **Content nature** | Primary disclosure (annual reports / regulatory filings / policy originals); primary statistics (surveys / censuses / administrative records); authoritative research (reports / papers with methodology) | Secondary paraphrases, machine-scraped pastiche, AI-generated summaries |
| **Traceability** | Clear institutional attribution; explicit publication date; located via original PDF / database field | Anonymous "according to reports" / "industry insiders"; no source link; no specific locator |

Meet all three = trustworthy source, even if not listed in the tables below. Still bound by the "Sources NOT accepted as final" list (Wikipedia / Zhihu / personal blogs / social media / SERP snippets alone, etc.).

### One — User-supplied files (highest priority)

Files the user supplies in the conversation or via local paths: PDFs, markdown notes, Excel, screenshots, cleaned web text, links.

- Text (PDF / md / txt / csv): read full text
- Links: fetch web body
- Images: image recognition

### Two — Official websites and authoritative databases

International institutions.

| Source | Main content | Entry point |
|---|---|---|
| IMF | WEO, Article IV, Working Papers, Policy Papers, Selected Issues Papers | https://www.imf.org/publications, https://www.elibrary.imf.org |
| World Bank | Open Knowledge Repository, WDI, Country Studies | https://openknowledge.worldbank.org, https://databank.worldbank.org |
| IEA | World Energy Outlook, Country Profiles, energy data | https://www.iea.org |
| IRENA | Renewable-energy data and reports | https://www.irena.org |
| OECD | Cross-country macro statistics, policy research | https://www.oecd.org, https://data.oecd.org |
| BIS | Financial stability, cross-border capital flows, central-bank statistics | https://www.bis.org |
| UN Comtrade | International trade statistics | https://comtrade.un.org |
| UNCTAD | Investment and development statistics | https://unctad.org |
| WTO | Trade policy and statistics | https://www.wto.org |
| Eurostat | EU statistics | https://ec.europa.eu/eurostat |
| ECB | Euro-area central bank data | https://www.ecb.europa.eu |
| FRED | U.S. macro data | https://fred.stlouisfed.org |
| Regional development banks | ADB, AfDB, Arab Monetary Fund, IDB, ESCAP, ECLAC | Each institution's official site |

Sovereign / government / central bank / regulator.

| Source | Content |
|---|---|
| National central banks | Monetary policy, FX reserves, banking sector, cross-border capital flows |
| National statistics offices | GDP, population, industry structure, CPI, employment (definitions per each country) |
| Ministries of finance | Budget, fiscal revenue, government debt |
| Sovereign wealth funds | Annual reports, disclosure filings (official site or SWFI database) |
| Industry regulators | Energy, finance, telecom, real-estate, etc. — the relevant national regulator |
| SEC EDGAR | 13F sovereign-fund disclosures, listed-company filings (https://www.sec.gov/edgar) |

Action: fetch official site text, or query the database by field.

### Three — Authoritative industry sources

Academia and think tanks.

| Type | Examples |
|---|---|
| Academic working papers | NBER Working Papers (https://www.nber.org), SSRN (https://www.ssrn.com) |
| Academic search | Google Scholar, JSTOR, ScienceDirect |
| Top journals | AER, QJE, JFE, RFS, JPE, JF, JIE (most require subscription; abstracts often accessible) |
| Think tanks | Brookings, Peterson IIE, Atlantic Council, CSIS, Chatham House, CFR, IISS, Carnegie Endowment |

**Important**: a scholar's personal working paper / personal view is NOT the official position of the institution they belong to. Do not conflate the two when citing.

Investment banks and consulting.

| Type | Examples |
|---|---|
| Global IB Research | Goldman Sachs, JPMorgan, Morgan Stanley, Citi, HSBC, BofA, UBS, Credit Suisse — Country Outlooks / Sector Reports (mostly subscription-only; excerpts often appear via Bloomberg / Reuters — search first to find the relay, then locate the original report) |
| Chinese IBs | CICC, CSCI, China Merchants Securities, Haitong, Huatai, Guotai Junan — international research |
| Consulting white papers | McKinsey, BCG, Oliver Wyman, Bain, Deloitte, PwC, EY, Accenture (most are public) |

Mainstream financial media.

| Language | Examples |
|---|---|
| Chinese | Caixin, Wallstreetcn, Yicai, Economic Observer, 21st Century Business Herald, Bloomberg China, FT Chinese, WSJ Chinese |
| English | Bloomberg, Reuters, Financial Times, Wall Street Journal, The Economist, NYT, Forbes, Fortune (paywalls partial — quote the snippet and flag the paywall when full text is unavailable) |
| Regional / specialist | MEED (Middle East), Argus / Platts (energy), Lloyd's List / TradeWinds (shipping), Variety (media), Modern Healthcare (healthcare) |

Aggregator databases (acceptable as a trusted source — cite the source; no need to chase further to the original primary source).

| Source | Main content |
|---|---|
| Statista | Cross-industry market size, share, consumer data |
| Wind / CEIC | China and Asia macro, financial, and industry data |
| Refinitiv (Eikon) | Global market data, company fundamentals |
| SWFI | Sovereign wealth fund / public pension disclosure aggregator |
| Bloomberg Terminal | Market data and company financials (screenshot / export usable) |

### Sources NOT accepted as final

- Wikipedia, Baidu Baike, Zhihu, personal blogs
- Unattributed media paraphrases, content farms, SEO sites
- AI-generated summaries (including ChatGPT, Perplexity, Gemini, etc.)
- Vague phrasings like "according to reports," "industry insiders," "rumored that," "market participants disclose"
- Social-media content (except formal announcements from officially verified institutional accounts)
- Secondary translations — must be traced back to the original institution's official version
- SERP (search-engine results page) snippets alone — must click through to the original page to confirm; otherwise classify as "Cannot verify"

### Bilingual / multilingual principle

Reports from international institutions / IBs / consulting are mostly in English. For local data and policy developments in China, the Middle East, Africa, etc., Chinese (or local-language) primary materials are often more accurate. Policy documents (e.g. Saudi Vision 2030) often have official Arabic + English versions — cross-reference when needed. Switch language based on the region / institution the statement involves.

## Give-up criterion

Keep tracing sources until either:

- **(a)** a whitelisted primary source is located and (where applicable) downloaded and read in full — produce a `✅ Verified` output;
- **(b)** the obvious paths have been exhausted (direct keyword search → keyword and language variants → tracing the source cited in the statement back to its issuing institution) — produce a `❌ Cannot verify` output plainly. Do not guess, infer, or substitute with secondary sources.

There is no fixed depth budget. Stop when leads are genuinely exhausted, not at an arbitrary count.

## Download-the-original rule

Looking only at search-engine snippets, page fragments, or secondary paraphrases and then claiming "verified" does NOT count. When the statement involves a report or chart, the original / raw data must be downloaded locally, fully read by the AI, and only then can a conclusion be drawn.

Trigger conditions (any one triggers):

- The statement cites a specific report (IMF Country Report, PIF Annual Report, central-bank Working Paper, consulting white paper, etc.).
- The statement cites a specific chart, dataset, or number.
- The statement cites a policy text, regulatory filing, or annual report disclosure.

Download steps:

1. **Locate the original file**: prefer the official site's original link, not a secondary republisher.
2. **Download locally**: do not assume a save path. On the first download, ask the user where to save; if the user does not specify, place the file in the current working directory named `<institution> <title>.<extension>`.
3. **Read in full before concluding**: read the entire PDF or extract a full-text summary — pull out the methodology, key parameters, and supporting passages; for data files, read the first and last few rows to confirm fields and definitions.
4. **Chart sources**: if the statement points to a specific chart, find the original report / database page that contains the chart, download it, and locate the page number or data table where the chart appears.

### Chart "meaning" verification

A chart existing ≠ the user's reading of it being correct. After downloading, also verify:

- Axis units and definitions (linear vs. log, absolute vs. year-over-year, local currency vs. USD).
- Start year and base period (avoid selectively misleading starting points).
- Whether the series is cumulative / moving-average / seasonally-adjusted.
- Footnotes and chart notes specifying scope ("excluding X," "Y region only," etc.).

If the user's reading does not match what the chart actually shows, explicitly correct it.

### Download-blocked handling

If automated download is blocked (403, paywall, Cloudflare, login required, geo-restriction, JS-rendered text not retrievable, etc.), **pause verification** and output in the format below, handing the link to the user:

```
🔒 Needs user help to download.
Source: <full official link>
Blocked by: <paywall / login wall / anti-scrape / geo-restriction>
Please: download and tell me the local path, or paste the relevant section into the chat.
```

Once the user provides it, return to step 3 (read in full) and judge. **Only when the user also cannot obtain it** should a downgrade be taken — in that case, explicitly flag "did not obtain full text; verification is based on snippet only with reduced confidence." Do not pretend it is fully verified.

Counter-examples (NOT acceptable as "verified"):

- "I found a Reuters article saying PIF's AUM is $925 B — verified." Reuters is secondary paraphrase. Must trace to PIF's official annual report and download it.
- "I saw an IMF web page saying Saudi Arabia's fiscal-breakeven oil price is $96." A snippet does not count — must download the corresponding IMF Country Report PDF and locate the specific table and footnote.

## One-level reasoning sub-flow

Use this when the direct number cannot be traced to a primary source but the statement can be cross-checked via metric decomposition. **Only one level of decomposition** — the sub-metrics must each be verifiable against a primary or aggregator-database source. If a sub-metric still requires further decomposition (multi-level reasoning), tell the user this is out of scope for this skill and suggest splitting into steps or human follow-up.

Steps:

1. **Decomposition formula**: state Z = f(P, Q) explicitly (e.g. revenue = unit price × volume; profit = revenue × margin; market share = company volume ÷ total market volume).
2. **Verify P and Q separately**: each follows the basic verification flow, independently traced to a primary or aggregator source.
3. **Compute Z'**: use the verified P and Q to compute Z'.
4. **Reconcile**: compare Z' to the user's Z, with a qualitative verdict (the AI estimates — no hard-coded percentage threshold):
   - Broadly consistent: deviation within a reasonable range.
   - Notable deviation: clear gap, needs explanation.
   - Severe mismatch: gap large enough to suspect the original statement itself.
5. **Attribution of deviation**: when inconsistent, analyze which sub-metric's assumption is most likely the issue; whether the definitions / time points / coverage of P and Q are aligned.

Output format:

```
🔎 One-level reasoning. Z = f(P, Q) → Z' = <computed value>; statement Z = <user value>; <broadly consistent / notable deviation / severe mismatch>.
P = <value>, source: <institution + link>
Q = <value>, source: <institution + link>
[⚠ Attribution: <only when inconsistent — name the likely problem sub-metric and flag any P/Q definition / time-point / coverage mismatch>]
```

## Negative-statement handling

When the statement contains negation markers like "never," "has not," "no," "not," "did not" (or 「从未」「没有」「未曾」「不曾」「无」in Chinese), first tell the user:

> This is a negative statement. Negatives are essentially unfalsifiable by search — failing to find a counter-example is NOT proof of truth. I will try to find a counter-example: if one is found, the statement is refuted; if none is found, I cannot apply a "Verified" label and can only state "no public counter-example found."

Then run the "search for counter-example" path under the same whitelist and give-up criterion. Output labels are adjusted:

- `❌ Statement refuted. <counter-example + primary source>` — explicit refutation.
- `⚠ No public counter-example found.` — "not found ≠ proven true"; list 2-3 keywords/sites tried.

## Multi-source conflict sub-flow

When two whitelisted sources disagree on the same number, **do not force a pick**. Output side-by-side:

```
⚖ Multi-source conflict on <statement>.
A: <X> — <institution + link>
B: <Y> — <institution + link>
Difference: <the 1-2 most material reasons — definition / time point / revision status / coverage>
Suggest: <user picks based on context, or specifies which definition they need>
```

## Metadata: surface only when divergent

Internally check the six dimensions below for every verification. **Do NOT print them by default** — when they match the user's stated question, listing them adds noise without insight.

**Print a `⚠` line ONLY when one of them diverges from the user's statement or is non-obvious enough to mislead.** Examples that warrant a `⚠`:

- User asked "Saudi 2023 GDP" but the figure found is **non-oil GDP** → flag `Definition` divergence
- User asked about "Q4 2024" but the data is **preliminary, not final** → flag `Revision status`
- The number is a **target / forecast**, not an actual → flag `Data type`
- Currency / FY-vs-CY / consolidated-vs-parent / coverage mismatches → flag accordingly

| Dimension | When it matters |
|---|---|
| **Time point** | When the year / quarter / as-of-date in the source ≠ what the user implied |
| **Definition / scope** | When statistical scope or method differs (nominal vs. real, included items, etc.) |
| **Unit** | When currency / quantity unit could be confused (CNY 100M vs. USD million, FY vs. CY) |
| **Coverage** | When geographic or business coverage is narrower / broader than implied |
| **Revision status** | Initial / revised / final, when the user might confuse vintages |
| **Data type** | actual / forecast / projection / target / estimate — flag whenever it is anything other than `actual` |

This is the binding rule that replaces "silent definition swap." The point is to surface divergence, not to mechanically list six fields.

## Output formats

Keep outputs tight. Three to five lines is the target for the common case; add a `⚠` line only when something actually diverges (see the metadata section).

### ✅ Verified

```
✅ Verified. <one-sentence conclusion in plain language>.
Source: <institution + report name> (<YYYY-MM>, <page / table / figure locator>) → <local path if downloaded>
Quote: "<verbatim excerpt supporting the claim>"
[⚠ <single line, only when a metadata dimension diverges from the user's statement — e.g. "this is the non-oil GDP definition, not headline GDP">]
```

### ⚠ Partially Verified

```
⚠ Partially verified.
Verified: <sub-claim> — <source>
Unverified: <sub-claim>
Suggest: <ask user for source / rewrite as "to be verified" / drop>
```

### ❌ Cannot Verify

```
❌ Cannot verify. <one-sentence likely reason>.
Tried: <2-3 most relevant keywords / sites / leads>
Suggest: <ask user for the original source / soften the claim / drop it>
```

The four sub-flow outputs — `🔎 One-level reasoning`, `❌ Statement refuted` / `⚠ No public counter-example found`, `⚖ Multi-source conflict`, `🔒 Needs user help to download` — use the formats specified in their own sections above.

## Red lines

- **No fabrication**: prefer outputting "Cannot Verify" over producing a plausible-but-unverified number or date.
- **No silent definition swap**: if the user asks about definition A but only definition B is available, explicitly flag the gap — do not silently substitute B and claim verification.
- **No non-whitelisted citation**: Wikipedia, paraphrases, AI summaries, social media are not acceptable as final source.
- **No missing link**: every "Verified" conclusion must allow the user to click back to the original page or locate the local file.
- **Three-state discipline**: clearly distinguish "fact" (whitelisted source with original text) / "estimate" (methodology + parameter inference) / "inference" (no direct source — only plausible guess). The latter two cannot enter the "Verified" output.
- **Snippet ≠ verification**: for statements involving reports / charts / data, the original must be downloaded and read in full before claiming verified. Claiming "verified" based on SERP snippets, web fragments, or secondary paraphrases crosses the line.
- **No conflating personal and institutional positions**: a scholar's personal working paper or personal view ≠ the official position of their institution.
- **No skipping the download-blocked prompt**: when automated download fails, the `🔒 Needs user help to download` block must be output to hand the link to the user — do not silently skip or fabricate.
- **No beyond-one-level reasoning**: this skill only supports one level of metric decomposition (Z = P × Q). If a sub-metric still requires further decomposition (multi-level reasoning), tell the user this is out of scope and suggest step-by-step verification or human follow-up.
- **Surface divergence**: when any metadata dimension (time point / definition / unit / coverage / revision status / data type) differs from the user's stated claim, you MUST flag it on a `⚠` line. Silent omission of a divergence is equivalent to silent definition swap.
- **No verifying refused topics**: politics / military / religion / entertainment celebrity gossip / other inherently controversial topics are out of scope. Reply with exactly "Out of scope. (超出能力范围)" and stop — no partial verification, no workaround suggestions, no explanation beyond that one line.
