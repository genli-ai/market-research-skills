# topic-brief

> 中文版本见本文件下半部分 / Chinese version below

A skill that generates a thematic observation briefing from public news sources. Outputs a single self-contained HTML file with blue "TOPIC BRIEF" branding — ready to paste directly into the **WeChat Official Account editor** (微信公众号).

---

## Folder structure

```
topic-brief/
├── SKILL.md                 ← English workflow (canonical, loaded by LLMs)
├── SKILL.zh.md              ← Chinese reference, kept in sync; excluded from .zip
├── README.md                ← this file (bilingual)
├── lib/
│   ├── __init__.py
│   ├── schema.py            ← Briefing / Section / Item dataclasses
│   ├── renderer.py          ← Jinja2 rendering
│   ├── writer.py            ← write_briefing_mock (JSON → Briefing object)
│   └── fix_quotes.py        ← Chinese-quote pairing repair
├── templates/
│   └── briefing.html        ← Blue inline-CSS template (WeChat-compatible)
├── scripts/
│   └── render.py            ← CLI entry
├── prompts/
│   └── system.md            ← Writer system prompt (discipline + schema)
├── reference/               ← Few-shot style samples
│   ├── region_southeast_asia.example.json
│   ├── region_middle_east.example.json
│   ├── region_india.example.json
│   └── brand_red_belt_and_road.example.json   (red-brand example)
└── output/                  ← Generated artifacts (auto-created)
    ├── seed/<subject>_<date>.json   ← seed JSON written in Step 4
    └── <date>_<title>.html          ← rendered HTML
```

The folder is self-contained: copy-pasting it into any Claude Code project under `.claude/skills/topic-brief/` works without further configuration.

## Dependency

Python 3.9+ with a single dependency:

```bash
python3 -m pip install --user jinja2
```

(User-level install — no virtualenv needed.)

## Usage

### Option 1 — Auto-run via the skill inside Claude Code (recommended)

After installation, tell Claude:

```
做一份 5 月下半月的中东观察
Generate a semiconductor industry briefing for the past month
/topic-brief
```

Claude follows the 5-step workflow in [SKILL.md](SKILL.md):
1. Collect parameters (subject / period / source preference / author)
2. Parallel material gathering (search + fetch)
3. **Direction confirmation** ← key error-prevention gate
4. Compose the seed JSON
5. Render HTML, open browser, report sources

Each run takes 10–20 minutes and produces ~3,000–5,000 characters with 12–16 cited items and full URLs.

### Option 2 — CLI render only (you already have a seed JSON)

```bash
cd /path/to/topic-brief
python3 scripts/render.py reference/region_middle_east.example.json --out output --open
```

`--open` opens the HTML in your browser. `render.py` auto-runs `fix_quotes` to repair Chinese quote pairs.

## Output shape

A single HTML file containing:
- Cover (brand + subject + main title + period label + author byline)
- Issue summary (focus blurb + 4 one-sentence highlights)
- Focus observation (1,500–2,500 chars, 3–5 sections)
- 4 regional / thematic sub-sections (3–4 items each)
- Footer source list
- Disclaimer

**Pasteable into the WeChat editor**: all CSS is inline, layout uses nested `<table>` (no pseudo-elements, no gradients, no CSS variables). WeChat's editor preserves all styling on paste.

## Customization

| What | Where |
|---|---|
| Visual style (colors, fonts, spacing) | inline styles in [templates/briefing.html](templates/briefing.html) |
| Brand name (default `TOPIC BRIEF`) | `brand_name` in seed JSON |
| Sub-section axis (country / theme / time / actor) | `sections[].label` in seed JSON |
| Writing discipline, length caps | [prompts/system.md](prompts/system.md) |
| Workflow (steps, failure handling) | [SKILL.md](SKILL.md) |

For a red-brand version (e.g., a "Belt and Road" look), swap the color tokens `#1e3a5f`, `#d4a259`, `#f0f5fa`, `#c8d4e0` in `templates/briefing.html`. See `reference/brand_red_belt_and_road.example.json`.

## Research discipline

**AI output ≠ conclusion.** After each run, you (the human reviewer) must:
- Check every concrete number against the cited source
- Verify each of the 12–16 cited items actually happened
- Confirm every URL resolves

The human is the final gatekeeper before publication.

## Known limits

- `WebSearch` / `WebFetch` work best with international connectivity. From mainland China, use a VPN or substitute domestic sources (iFinD MCP, Tushare, etc.).
- The WeChat editor moderates **externally hosted images**. Upload the focus image to WeChat's media library first.
- The skill does not call any external LLM API — the writing happens inside the Claude Code session itself (no extra token cost beyond your Claude Code subscription).

## Origin

This skill was extracted and generalized from the "Belt and Road Observation" project. The schema is backward-compatible with the older `region_name` / `regions` fields, so existing seed JSONs render unchanged.

---

# topic-brief（中文版）

主题观察简报生成 skill。基于公开新闻，为任意主题（区域 / 行业 / 议题 / 机构）产出一份信息简报 HTML，**可直接复制粘贴到微信公众号编辑器**。

## 文件结构

```
topic-brief/
├── SKILL.md                 ← 英文工作流（权威版，被 LLM 加载）
├── SKILL.zh.md              ← 中文参考版，与英文同步；打包时排除
├── README.md                ← 本文件（双语）
├── lib/
│   ├── __init__.py
│   ├── schema.py            ← Briefing / Section / Item dataclass
│   ├── renderer.py          ← Jinja2 渲染
│   ├── writer.py            ← write_briefing_mock（JSON → Briefing 对象）
│   └── fix_quotes.py        ← JSON 中文引号修复工具
├── templates/
│   └── briefing.html        ← 蓝色 inline-CSS 模板（公众号兼容）
├── scripts/
│   └── render.py            ← CLI 入口
├── prompts/
│   └── system.md            ← 撰写器 system prompt（含纪律 + schema）
├── reference/               ← few-shot 风格样本
│   ├── region_southeast_asia.example.json
│   ├── region_middle_east.example.json
│   ├── region_india.example.json
│   └── brand_red_belt_and_road.example.json（红色品牌示例）
└── output/                  ← 生成产物（自动创建）
    ├── seed/<subject>_<date>.json   ← 撰写产出的 seed JSON
    └── <date>_<title>.html          ← 渲染产出的 HTML
```

**self-contained**：本目录不依赖外部代码。整目录复制到其他 Claude Code 项目即可用。

## 依赖

Python 3.9+，单一依赖：

```bash
python3 -m pip install --user jinja2
```

（用户级安装，不污染系统 Python；不需要 venv）

## 怎么用

### 方式 1：在 Claude Code 里通过 skill 自动跑（推荐）

把这个目录放到任何 Claude Code 项目的 `.claude/skills/topic-brief/` 下，然后跟 Claude 说：

```
做一份 5 月下半月的中东观察
生成半导体行业过去一个月的简报
做一期 AI 立法主题观察
/topic-brief
```

Claude 会按 [SKILL.md](SKILL.md) 的 5 步工作流自动执行：
1. 询问参数（主题 / 时间 / 信息源偏好 / 作者）
2. 并行 WebSearch + WebFetch 拉素材
3. **停下来让用户确认焦点和子板块** ← 关键防错点
4. 撰写 JSON
5. 渲染 HTML + 浏览器打开 + 汇报来源清单

每份耗时约 10-20 分钟，输出 3000-5000 字 + 12-16 条新闻 + 完整脚注。

### 方式 2：命令行直接渲染（已有 seed JSON）

```bash
cd /path/to/topic-brief
python3 scripts/render.py reference/region_middle_east.example.json --out output --open
```

`--open` 会自动用浏览器打开生成的 HTML。`render.py` 会自动跑 `fix_quotes` 修中文引号。

## 输出形态

**单一 HTML 文件**：
- 蓝色品牌（主色 `#1e3a5f`，辅金 `#d4a259`）
- 封面（品牌名 + 主题名 + 主标题 + 期号 + 作者署名）
- 本期要点（焦点摘要 + 4 条速览）
- 焦点观察长文（1500-2500 字，3-5 sections）
- 区域动态（4 个子板块各 3-4 条新闻）
- 脚注 URL 清单
- 免责声明

**可直接粘进微信公众号编辑器**——CSS 全部 inline，`<table>` 嵌套布局，无伪元素 / 无渐变 / 无 CSS 变量，公众号编辑器复制粘贴时能保留全部样式。

## 自定义

| 改什么 | 改哪 |
|---|---|
| 视觉样式（颜色、字号、间距） | [templates/briefing.html](templates/briefing.html) 里的 inline style |
| 品牌名（默认 `TOPIC BRIEF`） | seed JSON 里 `brand_name` 字段 |
| 4 子板块如何分（按国家 / 按主题 / 按时间 / 按主体） | seed JSON 里 `sections[].label` 自由命名 |
| 撰写纪律、字数限制 | [prompts/system.md](prompts/system.md) |
| 工作流（步骤、失败处理） | [SKILL.md](SKILL.md) |

如果要做红色品牌（比如复刻中金一带一路那种），把 `templates/briefing.html` 里的 `#1e3a5f`、`#d4a259`、`#f0f5fa`、`#c8d4e0` 这几个色值改成对应红色调即可。参考 `reference/brand_red_belt_and_road.example.json`。

## 投研纪律提醒

**AI 输出 ≠ 结论**。每期 Claude 写完后，**你必须人工过一遍**：
- 焦点的核心数字是不是真的来自原报告
- 12-16 条新闻是不是真发生过
- URL 是不是真的能打开

发出去之前，**你才是最终把关人**。

## 已知限制

- WebSearch / WebFetch 在墙外才能拉到大部分国际机构原文；国内网络可能要 VPN 或者改用 iFinD MCP 之类的本土数据源
- 微信公众号编辑器对**外链图片**有审查；焦点图片要先上传到公众号图库再用
- skill 默认不接 LLM API；撰写是由 Claude Code 主对话承担（你用 Claude Code 订阅，零额外 token 成本）

## 来源

本 skill 从"一带一路观察"项目抽象而来。schema 兼容老的 `region_name` / `regions` 字段，老 JSON 文件能直接用新 skill 渲染。
