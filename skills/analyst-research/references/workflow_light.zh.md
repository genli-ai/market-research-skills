# analyst-research · light 模式工作流

> 英文主文件为 `workflow_light.md`（中文镜像）。

适用对象：5 页内决策备忘 / executive brief / 内部 memo。预算约 15 分钟，单 LLM，0 硬停，纯文字无图，仅 PDF + Word 产出。

medium 与 heavy 是 analyst-research 同 skill 内的姐妹模式，分别覆盖 10-15 页主题分析与 1.5 万字+ 旗舰报告。三档共用 hypothesis-lock 起点，下游差异由本模式自治。

---

## 一、新项目 onboarding 流程

### 第 0 步：宣告

向用户简短确认：「我已读完 analyst-research light 模式工作流（`references/workflow_light.md`），准备启动 6 步流程。」

确认后问 **2 个 onboarding 问题**（问完锁定不再追问）：

**Q1 · 研究问题或 hypothesis（一句话）**：用户给出要研究的具体问题。如「美联储 9 月是否会降息 50bp」「公司 X 的 Q3 财报会不会 beat consensus」「中东主权基金对中国 AI 板块持仓最近变化」。

**Q2 · 报告语言**：英文（default）/ 中文 / 其他。用户不指定即按英文写 draft（见 SKILL.md「Reply language」）。锁定后记入 hypothesis.md 关键约束段。英文稿跳过中文冒号红线、强制执行 unescaped `$` 红线（金额写 `\$`）。

不问的事项（default 锁定，不允许 AI 主动询问）：

- 产出形态：PDF + Word docx，**不出 HTML、不出公众号 JPG、不出 slide**
- 篇幅：4-5 页目标（**< 4 页视为过薄，必须回补内容或加子问题深度**；6 页 OK；7-9 页强警告 + 建议精简；10+ 页要求用户重新评估是 light 还是 heavy，不强行硬截）
- 图表：**0 张**，纯文字 + 内联 footnote 引用
- 目标读者：**专家 / 决策者**（非双兼，不写科普）
- LLM：单 LLM（Claude solo 全程）
- 摘要形态：**BLUF**（bottom line up front 单段，80-150 字开场给结论 + 关键数字 + so-what）
- 时间预期：约 15 分钟单 session 跑完
- 作者署名 / 邮箱：从全局 `~/.claude/CLAUDE.md`「作者署名」段读 default，无此段才显式问

### 第 1 步：搭建脚手架

cwd 切到项目根后跑：

```bash
SKILL_ROOT="${SKILL_ROOT:-$(find ~/.claude/plugins -type d -path '*market-research-skills/skills/analyst-research' | head -1)}"
mkdir -p pdfs && \
cp "$SKILL_ROOT/references/_quarto-light.yml" _quarto.yml && \
touch hypothesis.md research.md outline.md draft.qmd
```

If the plugin path lookup fails (e.g., installed via clone-and-symlink instead of plugin marketplace), fall back to:

```bash
cp ~/.claude/skills/analyst-research/references/_quarto-light.yml _quarto.yml
```

不创建 `_state.md`、不创建项目级 `CLAUDE.md`、不创建 retrospective、不创建图表 / scripts 子目录。

`.claude/settings.json` 项目级权限（与 heavy 相同，签入 git）：

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

### 第 2 步：启动 step 1

把第 0 步收到的 hypothesis 写到 `hypothesis.md`：

```markdown
# 研究问题

<用户原话一句话>

# 关键约束

- 时间锁：<YYYY-MM-DD 快照>
- 受众：<决策者 / 同行 / 投委>
- 输出形态：PDF + Word，5 页内
- 必须覆盖的子问题（如有）：
  - ...
```

软停推进到 step 2，不等用户确认。

---

## 二、6 步骨架

| 步骤 | 名称 | 主导 | 时间预算 |
|---|---|---|---|
| 1 | hypothesis | 用户 + AI 复述 | 5 min |
| 2 | search | Claude solo | 25 min |
| 3 | plan | Claude solo | 5 min |
| 4 | draft | Claude solo | 20 min |
| 5 | self-check | Claude solo | 10 min |
| 6 | freeze | Claude | 5 min |

**全部 0 硬停**——AI 各步落盘后简短告知用户阶段产出，立即推进下一步。用户随时可叫停、调整方向、要求回退。

---

## 三、各步骤细则

### 步骤 1：hypothesis（无停点）

第 0 步问完用户的一句话研究问题后，AI 写 `hypothesis.md` 包含三段：研究问题原话 + 关键约束（时间锁 / 受众 / 输出形态 / 必须覆盖的子问题）+ AI 的复述确认。

不做发散性方向 brainstorm（用 heavy 才有 step 3 多方向劝退）。light 假设 hypothesis 在 onboarding 时已成形。

**模糊 hypothesis 的 0 硬停 nudge**：若用户给的 hypothesis 范围模糊（如「看美股 AI 板块」未指定时间锁 / 子主题边界、「分析中东主权基金」未指定具体哪家），AI **自行给出 assumption 写入 hypothesis.md 关键约束段**，并在落盘告知用户时一句话明示「按以下假设推进：时间锁 X / 范围 Y / 排除 Z，您可叫停修正」。**不停下来等用户确认**——0 硬停设计下用 assumption 透明化代替硬停。用户随时可叫停回退。

落盘后立即进 step 2。

---

### 步骤 2：search（无停点）

**目标**：20-30 条资料覆盖 hypothesis 涉及的关键事实 + 5-8 份核心 PDF 全文下载。

**6 类来源**（删 heavy 的「学术与智库」一类，其他 6 类全保留）：

| 类别 | 代表 |
|---|---|
| A.1 国际机构 | IMF、World Bank、IEA、OECD、BIS、UN、地区开发银行 |
| A.2 主权 / 政府 / 央行 | 央行、统计局、财政部、主权基金、行业监管 |
| A.4 投行 + 咨询 | GS / JPM / MS / Citi 等 Country Outlook，麦肯锡 / BCG 等行业报告 |
| A.5 主流财经媒体 | 中文：财新、华尔街见闻、FT 中文等；英文：Bloomberg、Reuters、FT、WSJ、Economist |
| A.6 公众号 / 行业社群 / 公共社交平台 | 财经 / 区域 / 垂直行业的中文公众号，LinkedIn / Substack / 公开 X 讨论 |
| A.7 数据库（程序化） | 项目可用的 MCP / API / skill：iFind、`financial-data-sources` skill 等。step 2 用于抓历史背景数字；time-lock 快照数字（最新行情 / 利率 / 估值倍数）在 step 4 引用前再次实拉，详见 §步骤 4 |

类别编号沿用 heavy 的 A.x 命名以便互查，跳号 A.3 是因为 light 不把学术作为 6 大类强制覆盖维度（个别学术论文需要引用时直接以单条 source 进 A.1 或 A.4，不另起一类）。

**纪律**：

1. **类别覆盖**：按 hypothesis 类型至少检索过 3 类，不能只挑 1-2 类熟悉的就交差。纯宏观议题通常 A.1+A.2+A.7；公司议题通常 A.2+A.4+A.5+A.7；政策议题通常 A.1+A.2+A.5
2. **数量级**：20-30 条资料即可，不追求 heavy 的 100+ 条覆盖面。每条记录类型 / 机构 / 标题 / 年份 / URL / 关键数字 / 重要性
3. **核心 PDF 全文下载**：承担**结构性论证作用**的文献（章节核心论点引用 / 提供关键数字 / 方法论被借鉴）必须下载全文 PDF 到 `pdfs/`，统一编号 `<编号> <机构> <标题>.pdf`，下载后用 pypdf 抽全文摘要再决定引用
4. **time-lock 数字 step 4 实拉**：行情 / 估值 / 收益率 / 央行政策利率等 time-lock 快照数字，**不在 step 2 抓二手转述**——在 step 4 draft 引用前用 `financial-data-sources` skill 实拉
5. **公共社交平台溯源**：公开 X / LinkedIn / Substack / 社群帖只用于发现线索和观察情绪，不是一手证据。记录 query、抓取日期、URL / post ID、作者 handle、抓取工具。可用 [TweetClaw](https://github.com/Xquik-dev/tweetclaw) 等工具抓取公开 X/Twitter 帖子与回复；任何事实性结论进入论证前，必须回到 A.1-A.5 或 A.7 交叉核实。

**「打开网页下载，再判断」**：数据侦察时至少下载一个代表性时点的实际数据再判断可达性，不要只看 SERP 摘要就下结论「数据不全」。

**IMF / Cloudflare 类 PDF 受限处理**：`pdfs/` 放 `_NOTES_<机构>_<标题>.md` 占位，明示「直链被 Cloudflare 拦截、已尝试 curl 与 WebFetch」+ 记录 SERP 摘要与 press briefing 等替代 source。draft.qmd 引用时 footnote 内联标注 `^[<机构>, <标题>（press briefing）, YYYY-MM-DD. URL. 注：直链 PDF 被 Cloudflare 拦截，引用来自 press briefing 转述]`，引用降级为「press briefing」（不写「据 IMF WEO Apr 2026 figure X」，改「据 IMF WEO Apr 2026（press briefing）」）。

**交付物**：`research.md` 含 20-30 条资料台账（按 6 类组织）+ `pdfs/` 含 5-8 份核心 PDF 全文。

落盘后立即进 step 3。

---

### 步骤 3：plan（无停点）

**目标**：一段话 outline，纯文字，无图清单。

**结构**：

```markdown
# Outline

**Hypothesis**：<复述 step 1 问题>

**BLUF 摘要**（80-150 字）：<结论 + 关键数字 + so-what>

**支撑论点**（3-5 个）：
1. <论点 1>：<一句话 take-away + 关键数字 + 引用 source>
2. <论点 2>：...
3. <论点 3>：...

**Caveat / Open questions**：
- <未闭合的问题 1>
- <未闭合的问题 2>
```

不写「方法论」段。不写 TOC。不预留章节编号。

**自检**：

- 每个支撑论点必须有至少 1 个 source 来自 step 2 的 `research.md` 或 `pdfs/`
- 论点之间不重叠
- Caveat 段必须存在（即使只 1 条），明示未闭合的不确定性

落盘后立即进 step 4。

---

### 步骤 4：draft（无停点）

**目标**：5 页一气连写整稿。

**结构**：

```markdown
---
title: "<题目，从 hypothesis.md 派生>"
author: "<onboarding 阶段从 ~/.claude/CLAUDE.md 读到的 author 字符串，如 'Ligen'>"
date: today                # Quarto 内置 keyword，渲染时自动填当天日期
---

# Executive Summary

<BLUF 单段 80-150 字。给结论 + 关键数字 + so-what。不分要点>

# <第一节标题，直接写主旨，不写「背景」>

<正文>

# <第二节标题>

<正文>

...

# Bottom Line

<再次拎结论 + 给决策者的下一步建议>
```

**模板里不写 `format:` 段**——`_quarto.yml` 已完整定义了 pdf / docx 格式与 include-in-header，draft.qmd 重写 format 段虽然 Quarto deep-merge 多数 OK，但碰到嵌套字段边界时可能丢失 _quarto.yml 的 include-in-header 关键设置，让标题字号 / 段间距 / 中文字体全部回退到 Quarto default。

**`{.unnumbered}` 不需要**——_quarto.yml 已 `number-sections: false`，全文无编号，加 `{.unnumbered}` 是冗余且容易误传染。

**写作纪律**（继承 heavy §7.1 全部，本节不重复——见本文件 §四「写作规范」）：

- 文风：陈述性、紧凑、专家受众，**不写科普背景**
- 标点：无破折号 `——`、少用中文冒号、统一「」中文引号、无 emoji
- 引用：内联 footnote `^[机构名, 《标题》, YYYY-MM-DD. URL.]`，**不用 references.bib**
- ppts 改「个百分点」
- 不要技术符号代连词（`→ + / vs`）
- 不要抒情铺垫（「实际上 / 事实上 / 值得指出的是 / 众所周知」）
- 不要 meta-language（「本研究不」「本节将」「本研究为... 而设」）

**time-lock 数字实拉纪律**：

正文引用任何 time-lock 快照数字（股价 / 股指 / 收益率 / 估值倍数 / 央行政策利率 / 公司季度数据未走 10-K 一手）前，必须先用 `financial-data-sources` skill（FRED / yfinance / SEC EDGAR / AKShare 等）或 iFinD MCP 实拉一次，以实拉数据为准。step 2 transmitted 数字仅作 sanity check 对照——差异 > 5% 必须查清原因后再决定取舍。

这条与 heavy §步骤 7 的「time-lock 数字 step 7 实拉」精神一致，只是 light 没有 step 7（无图），实拉时机移到 draft 引用前。

**Executive Summary 写法（BLUF style）**：

- **B**ottom **L**ine **U**p **F**ront：第一句话就是结论
- 单段，80-150 字，不分要点（不写 markdown bullet，但段内可有 2-3 个完整短句承担结论 / 数字 / so-what 三件事）
- 含：结论 + 关键数字（1-2 个最 critical 的）+ so-what（决策含义）
- 反面例：「本文研究了 X 的 Y 问题，发现…」（这是 academic 写法，不是 BLUF）
- 正面例（~75 字）：「Fed 9 月降 50bp 概率 < 30%。当前 SOFR 3M 利率隐含 25bp 降幅，与 Powell Jackson Hole 措辞一致。利率衍生品多头建仓节奏可保守 2-3 周。」

落盘后立即进 step 5。

---

### 步骤 5：self-check（无停点）

**目标**：3 类 critique + caveat 核 + §7.4 grep 文字红线，落定稿。

**3 类 critique**（heavy 的 6 类压缩到 3 类——5 页内跨节一致 / 论证流 / 三方一致都不存在或好抓）：

1. **事实与数据**：每个数字、年份、人名、机构名都能定位到原始来源（research.md 或 pdfs/ 或实拉数据）。time-lock 数字已实拉。
2. **引用支撑**：每条 footnote `^[...]` 真支持文中陈述，不挂羊头卖狗肉。URL 可达，日期注明。
3. **语言规范**：跑 §7.4 grep self-check 全量清单，粘实际输出数字到 commit message 或对话回复。

**Caveat 核**：

step 3 outline 列的「Caveat / Open questions」是否都在 draft 末尾或相关段落以明示态度处理。能闭合就闭合（再调 `verifying` skill 核一次），不能闭合就保留 caveat 进 draft 终稿。

**绝对不允许**：以「light 是短稿、self-check 走过场」为由跳过 §7.4 grep。短稿照样要 grep，且声明必须粘数字（详见 §6 grep self-check）。

**self-check 失败的回退路径**：

§6 grep 任一红线超标（如破折号 ≥ 1、冒号 / 句号比例 > 15%、正文加粗 > 2、emoji ≥ 1、抒情铺垫词命中等）：

1. **回 step 4** 改写 draft.qmd 触发的具体段落
2. 重渲 `quarto render draft.qmd`
3. **回 step 5** 重跑 §6 grep 全量清单
4. **直到全过才进 step 6**——0 硬停 ≠ 0 自检门。light 没有用户审 PDF 的硬停 gate，self-check 失败就裸进 step 6 等于把红线甩给用户

无限循环兜底：同一条红线连续 3 轮回退都改不掉，向用户报「self-check 第 X 条反复失败，建议人工介入」，停下等用户裁定。

落盘后立即进 step 6。

---

### 步骤 6：freeze（无停点）

**目标**：PDF 冻结 + docx 派生。

```bash
quarto render draft.qmd                  # → draft.pdf
quarto render draft.qmd --to docx        # → draft.docx
```

无 git tag 要求（light 项目不强制版本号管理；用户想 tag 就 tag）。无 publication-style HTML，无公众号 JPG 切页。

**完成判据**：

- `draft.pdf` 与 `draft.docx` 都生成
- PDF 翻一下肉眼看：无 ctex / xelatex 错、无 figure caption 残留（light 没图，若有 figure 引用残留是 bug）、页数在 4-6 范围内（超 7 强警告，详见下方）

**超页处置**：

- **< 4 页：过薄，回补内容或加子问题深度后重渲，不交差**
- 4-5 页：目标区间，正常结案
- 6 页：OK
- 7-9 页：强警告「内容超 light 边界」，建议精简 1-2 个最弱论点；用户认可超页时可正常交付
- 10+ 页：告诉用户「内容量级已接近 mini-report，请重新评估是继续 light 路径精简到 6 页内，还是转 heavy 模式重新规划」，由用户裁定，AI 不强行硬截

---

## 四、写作规范

### 4.1 文风

- 陈述性优先，**不写科普背景**（专家受众假设）
- 句子短促，单句信息密度高
- 主谓宾结构，少嵌套从句
- 数字精确（具体数字 + 单位 + 时点）

### 4.2 标点与字符（与 heavy §7.2 等价，本段重申红线）

- **绝对不用破折号 `——`**
- **半角连字符 `-` 仅限范围号与复合词使用**（`30-90%` / `2026-2030` / `single-bar`）。禁止 `-` 替代破折号
- **少用中文冒号 `：`**。能用句号断句就用句号
- 中文引号统一用「」角引号
- **不用 emoji 与特殊符号**

### 4.3 引用

light 不用 references.bib，统一用 Pandoc footnote 内联：

```markdown
SOFR 3M 利率最新 4.51%^[FRED, SOFR 3-Month Term Rate, 2026-05-15. https://fred.stlouisfed.org/series/SOFR3M.]，与 Powell 措辞一致。
```

- footnote 内容：`机构名, 标题或字段名, YYYY-MM-DD. URL.`（英文字段名 / 数据库 series 名直接写，不套《》；中文书 / 报告标题加《》）
- URL 必须可达（self-check step 5 时抽检 3-5 条）
- 同一来源在文中多次引用就重复写，**不引入 bib 共享 key**

### 4.4 BLUF Executive Summary

详见 §步骤 4 的 BLUF 写法段。要点：

- 单段 80-150 字
- 结论 + 关键数字 + so-what
- 第一句话就给结论

### 4.5 不写的内容（light 红线）

- **不写方法论段**（不解释「本研究采用什么方法」）
- **不写 TOC**（_quarto-light.yml 默认 `toc: false`）
- **不写章节编号**（`number-sections: false`）
- **不写「背景」「研究意义」**类 academic 框口段
- **不写 meta-language**（「本研究将」「本节将探讨」「本研究不」）
- **不写图表**（light 设计上就是纯文字）

---

## 五、贯穿性纪律

### 5.1 来源可追溯（不可砍）

任何数字都必须能定位到原始来源（research.md 条目 / pdfs/ PDF 名 / 实拉数据系列）。不能定位的标 ⚠️ 或剔除，**不要写进结论**。

### 5.2 不造数（不可砍）

宁可写「未公开」「待核实」，也不要给一个看似合理的猜测。

### 5.3 区分三态（不可砍）

事实（「据 IMF」）/ 估算（「据市场估算 ~X」）/ 推断（「推测可能…」）—— 三者用不同措辞标注。

### 5.4 AI 输出 ≠ 结论（不可砍）

AI 提供素材和初稿，最终结论由人决定。light 0 硬停意味用户「随时可叫停」，不意味 AI 写完用户就盲签。

### 5.5 verifying skill 调用（不可砍）

step 5 self-check 时对未闭合 caveat 必须调 `market-research-skills:verifying` skill 严格核一次。light 没有 heavy 的独立 9c verifying 子步，但 verifying 调用本身不允许跳过。

---

## 六、§7.4 grep self-check 文字红线

draft v1 完成、修订版交付前**必须** grep 核对。命令以 `draft.qmd` 为例。

**证据要求（反「自检走过场」纪律）**：声明 self-check 全过时**必须粘最后一次实际 grep 输出的数字**，不允许只口头声明「全过」。详见 heavy workflow §7.4 同名段——light 同样适用。

| 红线 | 检查命令 | 应为 |
|---|---|---|
| 破折号 `——` | `grep -c "——" draft.qmd` | 0 |
| 标题手写编号前缀 | `grep -nE "^#{1,3} (§\|A\.\|[0-9]\|[一二三四五六七八九十]、)" draft.qmd` | 0 行 |
| Emoji | `grep -cP "[\x{1F300}-\x{1F9FF}\x{2600}-\x{27BF}]" draft.qmd` | 0 |
| 未转义美元号 `$`（**英文稿必查**，LaTeX 把 `$` 当数学定界符，未转义即渲染失败） | `grep -nP "(?<!\\\\)\\$" draft.qmd` | 0（正文金额一律写 `\$`，如 `\$1.5 billion`） |
| h3 及更深标题（light 仅 h1 + h2） | `grep -nE "^#{3,}" draft.qmd` | 0 行 |
| 正文粗体 | `grep -c "\*\*" draft.qmd` | ≤ 2（仅引领词例外）|
| 中文冒号「：」对句号比例 | 总冒号 `grep -c "：" draft.qmd` 除以句号数 `grep -c "。" draft.qmd` | 5-15%（light 短稿无 figsource/tblsource 占用，可直接算比例不扣除） |
| 抒情铺垫高频词 | `grep -nE "实际上\|事实上\|值得指出\|值得注意\|众所周知\|不可否认\|毫无疑问\|需要指出\|客观地讲\|不难看出\|在此背景下\|在这一过程中" draft.qmd` | 命中即抽检删 |
| h2 空标题反模式（学术造作） | `grep -nE "^## .*(关于\|讨论\|探究\|浅析\|思考\|现状与挑战\|视角$)" draft.qmd` | 0 行 |
| 半角 `-` 当破折号 | `grep -nE " - " draft.qmd` | 抽检，合法只剩范围号与英文复合词 |
| 技术符号代连词 | `grep -nE "→\|∴" draft.qmd` + 抽检 `+` `/` `vs` | 替换为完整书面表达 |
| 学术腔与口语腔 | `grep -nE "使得\|进行了\|做出了\|具有重要意义\|一定程度上\|综上所述\|总而言之" draft.qmd` | 命中即按对照表替换 |
| 模糊量化词（无数字支撑） | `grep -nE "很大程度上\|相对较高\|相对较低\|大致\|大约\|一些\|部分" draft.qmd` | 抽检，无数字支撑全删或替换为具体数字 |
| meta-language / 元命令 | `grep -nE "本研究不\|本章不\|本研究将\|本研究为.*而设\|本章构造\|研究边界明确\|需要明示\|本节将\|本章将\|本节强调\|本章强调" draft.qmd` | 0 行（light 没有「本章」「本节」概念，命中即改写） |
| 页数 | 渲染 PDF 后翻一下 | 4-5 目标,< 4 过薄需回补,6 OK,7-9 强警告 + 建议精简,10+ 请用户裁定继续精简还是转 heavy |
| Quarto 渲染 | `quarto render draft.qmd` | 成功，无 mathtext / dimension 错误 |

**对比 heavy §7.4**：light 砍掉了 5 项与图 / publication / bib 相关的红线（`_quarto.yml` lof / lot 对齐、未引用 fig/tbl label、框口段二轮重写、bib 字段、figsource/tblsource 占用）。其余 12 项保留。

---

## 七、与 heavy 模式的边界

不要混用。下表给清晰区分：

| 维度 | light | heavy |
|---|---|---|
| 步骤数 | 6 | 11 |
| 时间预算 | 约 15 分钟 | >1 小时 |
| 篇幅 | 5 页 / 2500-3000 字 | 1.5 万字+ |
| 图表 | 0 | 通常 15+ 张，一图一脚本 |
| 引用机制 | footnote 内联 | references.bib |
| LLM | 单 LLM only | 单 / 多 LLM 可选 |
| 硬停 | 0 | 2（step 4 / 9d）|
| 派生形态 | PDF + Word | PDF + Word + HTML + 公众号 |
| 复盘 | 无 | 必做（§11.2 audit）|
| _state.md | 无 | 必有 |
| 目录结构 | 平铺 + pdfs/ 一个子目录 | 11 步骨架 9 个子目录 |
| 摘要形态 | BLUF 单段 | 三段式（含关键词行）|
| 受众 | 专家 / 决策者 | 双兼（专家 + 非专业）|
| TOC / 章节编号 | 无 | 有 |
| 升级路径 | 无（重跑 heavy）| n/a |

**触发判定示例**：

| 用户原话 | skill |
|---|---|
| 「给我写个 5 页 memo 看 Fed 9 月会不会降息」 | light |
| 「做个深度研究看美股 AI 泡沫风险」 | heavy |
| 「1 小时内出一份 brief 给老板看」 | light |
| 「写一份公众号长稿讲沙特 Vision 2030」 | heavy |
| 「快速分析下中东主权基金最近持仓」 | light |
| 「行业研报：中国电池产业链全景」 | heavy |

判定不清楚时**首选 light**——short 是短稿的最大优势，写完不够再升级（重跑 heavy）成本可控；反过来 heavy 跑到一半发现题目其实只够 5 页就尴尬。
