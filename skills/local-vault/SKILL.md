---
name: local-vault
description: >-
  Build and query a local Markdown knowledge base ("vault"). TWO functions —
  (1) CONVERT raw files (PDF, Word/docx, PowerPoint/pptx, Excel/xlsx, csv/tsv,
  images, html, md/txt, json/yaml/code, audio/video) into clean Markdown with
  retrieval-friendly frontmatter; local-first (pandoc / python-pptx / openpyxl /
  pymupdf4llm / whisper), with cloud OCR (MinerU) only as a fallback. (2) ANSWER questions
  over the resulting vault with retrieval discipline — self-monitor coverage,
  flag missing/lossy content, and propose Maps-of-Content (MOCs). Triggers:
  "build/sync my local knowledge base", "convert these files to markdown for
  AI", "整理我的资料库", "把文件转成 md 给 AI 读", "本地知识库", "读我的本地 vault
  回答", "这个主题我的资料里怎么说". Not for: one-off web research, or files that
  are already in a single doc you can read directly.
---

# local-vault

Turn a folder of raw files into a **Markdown vault** that an LLM can grep, and
then answer questions over that vault responsibly.

**Mental model:** `SOURCE` = raw files (source of truth). `VAULT` = one `.md` per
source file, carrying retrieval frontmatter (abstract / tags / synonyms) + a
`source` backlink. The vault is the layer the LLM reads; the raw files are where
the user goes to verify.

There are **two distinct jobs** — figure out which the user wants:

- **A. Convert / sync** — they dropped files in and want them in the vault → run
  the pipeline (`scripts/sync.py`).
- **B. Retrieve / answer** — they want answers from an existing vault → follow
  the *Retrieval & feedback protocol* below. Do **not** run the pipeline for this.

---

## A. Convert / sync

### One-time setup (do this for the user if not already done)

1. **Python deps** (user-level, no venv):
   ```
   python3 -m pip install --user requests python-dotenv pypdf pymupdf4llm openpyxl python-pptx
   ```
2. **pandoc** (for docx/rtf/odt/epub): `brew install pandoc` (macOS) / distro pkg.
3. **ffmpeg** (only for audio/video transcription): `brew install ffmpeg` (macOS) /
   distro pkg. The **whisper engine is auto-selected by platform** — `mlx-whisper`
   on Apple Silicon (GPU), `faster-whisper` elsewhere (cross-platform CPU/CUDA) — and
   **auto-installed after the user consents** at the first-run prompt (no manual pip
   needed). On that first run with audio/video present, the tool shows the model-size
   options (tiny ~75 MB / small ~480 MB / turbo ~1.6 GB / large-v3 ~3 GB) and lets the
   user pick or skip; the choice is saved to `.env` (`KB_WHISPER_MODEL`) so it never
   re-asks. Fully local — no token/quota; the model downloads once, then offline.
4. **`claude` CLI on PATH** — the pipeline shells out to `claude -p` for frontmatter
   enrichment and PPT-image OCR. If absent, those steps are skipped (not fatal).
5. **Configure paths** — two ways:
   - **Guided (recommended for the user):** just run `python3 scripts/sync.py` in a
     terminal. On first run (when paths aren't configured yet) it launches an
     interactive wizard: it asks for the raw-files folder + the vault folder
     (+ optional MinerU token), creates them, writes `scripts/.env`, and prints how
     to use the tool. Then they re-run to convert.
   - **Manual:** copy `scripts/.env.example` → `scripts/.env` and set
     `KB_SOURCE_DIR` (raw files) and `KB_TARGET_DIR` (the Markdown vault), both
     absolute. `MINERU_TOKEN` is optional (only for legacy .doc/.ppt, .html, scanned
     PDFs, images — get one at https://mineru.net).
   - When **you (Claude)** run the setup for the user, prefer the manual path: ask
     them for the two folders, then write `scripts/.env` directly (the wizard only
     fires on an interactive TTY, which a `claude -p` subprocess is not).

### Run it

```
python3 scripts/sync.py
```

On macOS, the first run (wizard or any normal run) also drops a clickable
`sync.command` **into the knowledge-base root — the parent of the SOURCE folder**,
with the absolute path to `sync.py` baked in (tool and data live apart — under
`/plugin install` the script sits in `~/.claude/plugins/cache/…`, far from the data
folders, so a relative launcher can't work). After that the daily loop is: drop
files into SOURCE → double-click `sync.command` → read the `.md` in VAULT. The
launcher is idempotent; a stale auto-generated copy left in the SOURCE folder by an
older version is removed automatically (a user-written one is never touched). If a
*different* `sync.command` already exists at the root, an interactive terminal
prompts **update / skip**; non-interactively, our own out-of-date launcher self-heals
silently while a user-customized one is left alone.

First terminal run with no config → the setup wizard (above). Once `.env` exists:

- **Incremental**: only files in SOURCE without a matching `.md` in VAULT are
  processed. To force a re-convert, delete that `.md` first, then re-run.
- **No MinerU token needed** for the local paths (xlsx/csv/docx/pptx/md/txt/code +
  digital PDF). Token is validated lazily, only when a file actually needs MinerU.
- **Orphan staging**: if a source file is deleted, its tool-generated `.md` —
  together with its `attachments/<stem>/` images — is moved to an `orphaned/<date>/`
  folder (never hard-deleted — the user may have added notes), and the now-empty
  `attachments/` is pruned. User-written `.md` (no converter marker) is never touched.

### Routing (which tool per file type)

| Type | Tool | Notes |
|---|---|---|
| `.xlsx` | openpyxl dual-read | per sheet: value grid (with A/B/C + row coords) **+ formulas list** |
| `.csv` / `.tsv` | csv → Markdown table | truncates past `CSV_MAX_ROWS` |
| `.pdf` (digital) | pymupdf4llm | local, fast, no quota; if `PYMUPDF4LLM_WRITE_IMAGES` (default on), images ≥ `PYMUPDF4LLM_IMAGE_SIZE_LIMIT` (12% of page) → `attachments/`, then filtered by min-bytes + de-dup. If pymupdf4llm crashes (e.g. missing-font), a local plain-text pass is tried before MinerU |
| `.pdf` (scanned) | MinerU vlm (fallback) | triggered when chars/page is too low |
| `.docx`/`.rtf`/`.odt`/`.epub` | pandoc | images extracted to `attachments/` |
| `.html`/`.htm` | pandoc (local) | style/class/id attrs + layout `div`/`section`/`span` stripped first, so only content survives; tables kept lossless. No MinerU/token needed |
| `.pptx` | python-pptx | title/body/tables/**charts**/**notes** + images; smart OCR (see below) |
| `.md`/`.markdown`/`.txt` | passthrough | copied verbatim; only frontmatter added, **body untouched** |
| `.json`/`.yaml`/`.py`/… | code passthrough | wrapped in a fenced code block + frontmatter |
| audio `.mp3`/`.m4a`/`.wav`/… + video `.mp4`/`.mov`/`.m4v` | whisper (local; engine auto-selected: mlx-whisper on Apple Silicon, else faster-whisper) | speech-to-text, **no token/quota**; first run asks which model (shows sizes) + auto-installs the engine on consent (a model already cached on this machine is reused without re-asking); per-segment `[mm:ss]` timestamps + detected language; video = audio-track only (ffmpeg pulls it from the container). Needs ffmpeg; **best on clear speech — songs/music transcribe poorly** |
| legacy `.doc`/`.ppt`, images | MinerU (cloud) | local libs can't read these |
| anything else (numbers/pages/zip/…) | **skipped** | reported at the end with a fix hint — never silently dropped |

### PPT smart OCR

Images embedded in slides are OCR'd via `claude -p` (its Read tool reads the
image), but to avoid spawning one slow `claude` per decorative logo:
de-duplicates identical images (OCR once), skips images below
`OCR_MIN_IMAGE_BYTES`, and runs unique content images concurrently
(`OCR_MAX_WORKERS`). Native PowerPoint **chart objects** are read directly
(categories + series values → a table). Set `OCR_PPTX_IMAGES = False` to turn OCR
off entirely (images are still extracted + referenced).

### Frontmatter written to every `.md`

```yaml
---
source: "[[…/<file>.<ext>]]"   # backlink to the raw file
source_type: pdf | xlsx | docx | pptx | md | …
converted_by: pymupdf4llm | pandoc | python-pptx | excel-openpyxl | csv | passthrough | whisper | "MinerU vlm" | …
# enrich (best-effort via claude -p, may be missing on failure):
abstract: |
  3-sentence summary.
auto_tags: [..]
synonyms: [English + 中文 同义词]   # so any phrasing greps the right doc
key_data: ["important numbers/facts"]
---
```

### Tuning (`scripts/config.py`)

`PYMUPDF4LLM_MIN_CHARS_PER_PAGE` (scanned-PDF threshold) ·
`PYMUPDF4LLM_WRITE_IMAGES` (digital-PDF image extraction on/off; `.env`:
`KB_PDF_NO_IMAGES=1` to disable) · `PYMUPDF4LLM_IMAGE_SIZE_LIMIT` (extraction
floor as fraction of page area; default 0.12) · `PYMUPDF4LLM_IMAGE_MIN_BYTES`
(drop images smaller than this; default 6000) · `OCR_PPTX_IMAGES` /
`OCR_MIN_IMAGE_BYTES` / `OCR_MAX_WORKERS` (PPT image OCR) ·
`EXCEL_MAX_CELLS_PER_SHEET` · `CSV_MAX_ROWS` · `ENRICH_FRONTMATTER`.

---

## B. Retrieval & feedback protocol (answering over the vault)

When the user asks you to answer from / compare across their vault, **read the
vault directly** (grep + read `.md`). While doing so, self-monitor and surface
problems — don't just answer.

### Startup vault health check (first vault question of a session)

```
find "$KB_TARGET_DIR" -name "*.md" -not -path "*/.obsidian/*" | wc -l   # file count
```

Set a rough scale and only mention it if there's a problem:
small (<100 files) agentic grep is plenty · medium (100–500) watch keyword hit
counts · large (500–2000) suggest a semantic-search layer (e.g. Smart
Connections) · huge (>2000) recommend a real RAG layer.

### Self-checks after a complex query (warn only when triggered)

| Signal | Tell the user |
|---|---|
| one grep hits >30 files | keyword too broad — give a narrower one, or add semantic search |
| read 5+ files, still no answer | maybe a synonym gap, or it's genuinely not in the vault — list what you read |
| same topic asked repeatedly | offer to build an index/MOC for it |
| "which chapter covers X" needs full read-through | offer to enrich an outline for that doc |
| a doc is missing `abstract` | its enrich likely failed — offer to redo it |
| question needs exact numbers/formulas | remind them to click the `source` backlink and verify against the original |

### Topic queries → MOC entry order + evolution

A **MOC** (Map of Content) is the user's entry note for a theme — frontmatter
`type: moc`, living in `<vault>/索引/` (or `index/`).

1. For a cross-document topic question, first check for a relevant MOC; if one
   exists, read it first and use it as the answer skeleton.
2. If none and the user keeps asking about this theme, **offer** to create a
   minimal MOC (frontmatter + a `## related files` list — nothing more).
3. The MOC's structure should **grow from real usage**, never be pre-designed.
   When you notice a pattern (a sub-topic asked a lot, a recurring judgment, an
   open question), **propose** sedimenting it — the user decides, you draft.

**Frequency limits (avoid nagging):** at most **one** MOC-evolution proposal per
session; skip if this MOC was proposed-on <7 days ago; require a real multi-signal
pattern, not one offhand question; keep proposals to a single `> 💡 …` blockquote.

### Do not

- Don't append a "tips" wall to every answer — only speak up when a signal fires.
- Don't run the conversion pipeline just to answer a question.
- Don't batch-edit the vault's `.md` files (user notes and tool output coexist).
- Don't invent content because grep missed — "it's not in the vault" beats a guess.
- Don't copy source text into a MOC — wiki-link + one-line annotation only.

---

## Notes

- The pipeline does **not** depend on a running Claude session — it's a CLI; it
  only shells out to `claude -p` for the optional enrich/OCR steps.
- It never rewrites document **bodies** — all automation is frontmatter-only, so
  there's zero content-loss risk from the tool itself.
- Canonical, test-covered source lives in the author's dev project; the
  `scripts/` here are a packaged snapshot.
