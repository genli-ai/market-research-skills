# Market Research Skills

> 中文版本见本文件下半部分 / Chinese version below

A collection of Claude Skills for **market research / equity research / industry analysis**. Each skill tackles a specific link in the research workflow (information verification, data sourcing, industry mapping, report drafting, …). Use any skill standalone, or chain them into a complete workflow.

## Skills currently included

| Skill | Purpose | Typical triggers |
|---|---|---|
| [verifying](skills/verifying/) | Trace a statement back to whitelisted primary sources | "verify X" / "is this true" / "find the original source" |
| [topic-brief](skills/topic-brief/) | Generate a thematic observation briefing (HTML, paste-into-WeChat-ready) for any subject (region / industry / issue / institution) | "做一份 XX 观察" / "generate a briefing on Y" / "/topic-brief" |
| [analyst-research](skills/analyst-research/) | Three-mode end-to-end research workflow. User picks scope at trigger: **light** (4-5 page memo, 0 charts, 60-80 min), **medium** (12-15p topic analysis, 6-10 charts, half-day), or **heavy** (flagship 30-40p / 15k+ word report, 25-35+ charts, days-weeks, multi-LLM optional). Reports default to English; the AI replies in the user's chat language. Battle-tested on the Saudi Vision 2030 deep-dive. | "research report" / "投研报告" / "深度分析" / "做研报" / "5-page memo" / "/analyst-research" |

> The list grows with each release. Full change history in [CHANGELOG.md](CHANGELOG.md).

## Installation

### Option 1 — Claude Code one-click `/plugin install` (recommended for Claude Code users)

This repo ships with `.claude-plugin/marketplace.json` — it is itself a marketplace. In Claude Code:

```text
/plugin marketplace add https://github.com/genli-ai/market-research-skills.git
/plugin install market-research-skills@market-research-skills
```

Future updates in one command:

```text
/plugin update market-research-skills@market-research-skills
```

### Option 2 — Clone the entire repo to `~/.claude/skills/` (works for Claude Desktop / other LLM terminals)

```bash
git clone https://github.com/genli-ai/market-research-skills.git
cp -r market-research-skills/skills/* ~/.claude/skills/
```

Subsequent updates:

```bash
cd market-research-skills && git pull
cp -r skills/* ~/.claude/skills/
```

### Option 3 — Install only one skill

Use `sparse-checkout` to pull a single subdirectory:

```bash
git clone --filter=blob:none --no-checkout https://github.com/genli-ai/market-research-skills.git
cd market-research-skills
git sparse-checkout init --cone
git sparse-checkout set skills/verifying
git checkout
cp -r skills/verifying ~/.claude/skills/
```

### Option 4 — Download a packaged `.zip` file

Each [Release](https://github.com/genli-ai/market-research-skills/releases) attaches a `.zip` file for every skill. After download:

```bash
unzip verifying.zip -d ~/.claude/skills/verifying
```

### Option 5 — Cross-terminal install (Codex / Gemini / Copilot / etc.)

A `.zip` file simply contains `SKILL.md` and any resources — the format is portable across every LLM terminal. To install on non-Claude terminals:

1. Unzip the `.zip` file:
   ```bash
   unzip verifying.zip -d ./verifying
   ```
2. Move the unzipped folder into your terminal's skills directory (check your terminal's docs):
   - Codex CLI: typically `~/.codex/skills/` (verify in current Codex docs)
   - Gemini CLI: `~/.gemini/skills/` (verify in Gemini docs)
   - Other terminals: see the terminal's plugin / skill loader documentation

Tool-call action verbs inside each `SKILL.md` (read full text / fetch web body / search-engine query / image recognition / database query) are described in generic semantic terms, so each terminal's LLM can map them to its own local tool set.

## Directory layout

```
market-research-skills/
├── README.md                       # This file
├── LICENSE                         # MIT
├── CHANGELOG.md                    # Version history
├── .claude-plugin/
│   ├── plugin.json                 # Plugin manifest
│   └── marketplace.json            # Marketplace manifest (self-registering)
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md                # Canonical English version (loaded by LLM)
│       ├── SKILL.zh.md             # Chinese reference (kept in sync; not loaded)
│       ├── README.md               # Skill-specific docs (optional)
│       ├── references/             # Reference materials (optional)
│       ├── scripts/                # Skill-specific scripts (optional)
│       └── assets/                 # Static assets (optional)
├── scripts/
│   └── pack.sh                     # Package a skill as a .zip file
└── releases/                       # Locally generated .zip artifacts (gitignored)
    └── <skill-name>.zip            # Easy to copy and share directly
```

Every skill must have a `SKILL.md` (English, canonical, loaded by LLMs) whose frontmatter contains at minimum:

```yaml
---
name: <skill-name>           # Must match the folder name
description: <When to trigger and what the skill does — written in English>
---
```

A `SKILL.zh.md` may co-exist as a Chinese reference. The two files must be kept in sync when edited.

## Packaging a skill as `.zip`

```bash
./scripts/pack.sh verifying
# Output: releases/verifying.zip
```

The packaged `.zip` only includes the canonical `SKILL.md` plus other resources — the Chinese reference `SKILL.zh.md` is excluded.

## Distributing the `.zip`

There are two distribution paths:

- **Manual sharing**: copy `releases/<skill-name>.zip` and send to anyone directly (chat, email, Slack, etc.).
- **Public download via GitHub Release**: when you publish a Release on GitHub, attach the `.zip` file. Users download it from the Releases page.

The `releases/` folder is `.gitignored` — the repo does not store binary artifacts. Each Release on GitHub carries the `.zip` as an attached asset.

## Contributing / adding a new skill

1. Create a new folder under `skills/`. Folder name = skill name (lowercase + hyphens).
2. Create a `SKILL.md` (English, canonical) with proper frontmatter.
3. Optionally maintain a `SKILL.zh.md` Chinese reference — keep both in sync when modified.
4. Add a row to the "Skills currently included" table in this README.
5. Record the addition in `CHANGELOG.md`.

## License

[MIT](LICENSE)

---

# 市场研究 Skills（中文版）

一组面向**市场研究 / 投研 / 行业分析**场景的 Claude Skills 合集。每个 skill 解决一个具体的研究环节（信息核实、数据查找、行业地图、报告撰写……），可单独使用，也可组合成完整工作流。

## 当前包含的 Skills

| Skill | 用途 | 典型触发语 |
|---|---|---|
| [verifying](skills/verifying/) | 信息核实：把陈述追溯到白名单内的一手来源 | 「帮我核实 X」「这条信息是真的吗」「找一下原始出处」 |
| [topic-brief](skills/topic-brief/) | 主题观察简报生成器：为任意主题（区域 / 行业 / 议题 / 机构）产出可粘贴公众号的 HTML 简报 | 「做一份 XX 观察 / 简报」「`/topic-brief`」 |
| [analyst-research](skills/analyst-research/) | 三档端到端研究工作流。用户触发时选档：**light**（4-5 页备忘、0 图、60-80 分钟）/ **medium**（12-15 页主题分析、6-10 图、半天）/ **heavy**（30-40 页 / 1.5 万字+ 旗舰报告、25-35+ 图、数天到数周、可选多 LLM 协作）。报告默认英文，AI 按用户聊天语言回复。已在沙特 Vision 2030 深度报告项目跑通。 | 「写研报」「投研报告」「深度分析」「主题分析」「5 页 memo」「`/analyst-research`」 |

> 列表会随版本更新。完整变更见 [CHANGELOG.md](CHANGELOG.md)。

## 安装

### 方式一：Claude Code 一键 `/plugin install`（推荐 Claude Code 用户）

本 repo 自带 `.claude-plugin/marketplace.json`，本身就是一个 marketplace。在 Claude Code 里：

```text
/plugin marketplace add https://github.com/genli-ai/market-research-skills.git
/plugin install market-research-skills@market-research-skills
```

未来更新一键完成：

```text
/plugin update market-research-skills@market-research-skills
```

### 方式二：整体克隆到 ~/.claude/skills/（适合 Claude Desktop / 其他 LLM 终端）

```bash
git clone https://github.com/genli-ai/market-research-skills.git
cp -r market-research-skills/skills/* ~/.claude/skills/
```

后续更新：

```bash
cd market-research-skills && git pull
cp -r skills/* ~/.claude/skills/
```

### 方式三：只装某一个 skill

不想要全套时，用 `sparse-checkout` 只拉某个子目录：

```bash
git clone --filter=blob:none --no-checkout https://github.com/genli-ai/market-research-skills.git
cd market-research-skills
git sparse-checkout init --cone
git sparse-checkout set skills/verifying
git checkout
cp -r skills/verifying ~/.claude/skills/
```

### 方式四：下载打包好的 `.zip` 文件

每个 [Release](https://github.com/genli-ai/market-research-skills/releases) 会附上每个 skill 单独的 `.zip` 文件。下载后：

```bash
unzip verifying.zip -d ~/.claude/skills/verifying
```

### 方式五：跨终端安装（Codex / Gemini / Copilot 等）

`.zip` 文件里装着 `SKILL.md` 与资源文件——zip 是通用格式，任意 LLM 终端都能直接解压使用。安装到非 Claude 终端的步骤：

1. 解压 `.zip` 文件：
   ```bash
   unzip verifying.zip -d ./verifying
   ```
2. 把解压后的文件夹放进你终端的 skills 目录（具体路径查阅各自文档）：
   - Codex CLI：一般在 `~/.codex/skills/`（以最新 Codex 文档为准）
   - Gemini CLI：一般在 `~/.gemini/skills/`（以 Gemini 文档为准）
   - 其他终端：见各自的 plugin / skill 加载器文档

每个 `SKILL.md` 里的工具调用动作（通读全文 / 抓取网页正文 / 搜索引擎检索 / 图像识别 / 数据库查询）都用通用语义动词描述，让各终端的 LLM 映射到自家工具。

## 目录约定

```
market-research-skills/
├── README.md                       # 本文件
├── LICENSE                         # MIT
├── CHANGELOG.md                    # 版本变更
├── .claude-plugin/
│   ├── plugin.json                 # 本 repo 作为 Claude Code plugin 的清单
│   └── marketplace.json            # 本 repo 同时作为 marketplace（自我注册）
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md                # 英文权威版（被 LLM 加载）
│       ├── SKILL.zh.md             # 中文参考版（与 SKILL.md 同步；不被 LLM 加载）
│       ├── README.md               # 该 skill 的独立说明（可选）
│       ├── references/             # 引用的资料（可选）
│       ├── scripts/                # 该 skill 自带的脚本（可选）
│       └── assets/                 # 静态资源（可选）
├── scripts/
│   └── pack.sh                     # 打包某个 skill 为 .zip 文件
└── releases/                       # 本地生成的 .zip 产物（.gitignored）
    └── <skill-name>.zip            # 方便你直接拷贝发给别人
```

每个 skill 必须有一个 `SKILL.md`（英文权威版，被 LLM 加载），文件顶部 frontmatter 至少包含：

```yaml
---
name: <skill-name>           # 与文件夹名一致
description: <一句话英文：什么时候该触发、做什么事>
---
```

可同时维护一个 `SKILL.zh.md` 中文参考版。两份在修改时必须保持同步。

## 打包 skill 成 `.zip`

```bash
./scripts/pack.sh verifying
# 输出 releases/verifying.zip
```

打包好的 `.zip` 只包含权威的 `SKILL.md` 及其他资源——**中文参考版 `SKILL.zh.md` 不会被打进 zip**。

## 分发 `.zip`

两条分发路径：

- **手动分发**：把 `releases/<skill-name>.zip` 拷出来，微信 / 邮件 / Slack 直接发给任何人
- **GitHub Release 公开下载**：发 Release 时把 `.zip` 作为附件挂上去，用户在 Releases 页一键下载

`releases/` 文件夹本身在 `.gitignore` 里——repo 历史不存二进制产物。每次发版的 `.zip` 走 GitHub Release 的 attachment 路径。

## 贡献 / 新增 skill

1. 在 `skills/` 下新建一个文件夹，名字 = skill name（小写 + 短横线）
2. 创建 `SKILL.md`（英文权威版），写好 frontmatter
3. 可选维护 `SKILL.zh.md` 中文参考——修改时两份同步
4. 在本 README 上半部分（英文版）+ 下半部分（中文版）的 Skills 表格里各加一行
5. 在 `CHANGELOG.md` 记录本次新增

## 许可

[MIT](LICENSE)
