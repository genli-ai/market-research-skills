# analyst-research · medium 模式工作流

> 英文主文件为 `workflow_medium.md`（中文镜像）。

适用对象：12-15 页主题分析，6-10 张图，约 1 小时预算，单 LLM，1 硬停（step 7 用户 sign off 强制），可选第二硬停（step 2 广搜后，onboarding 时让用户决定）。

light 与 heavy 是同 skill 内的姐妹模式，分别处理 5 页内决策备忘与 1.5 万字+ 长篇研报。三档模式共用 hypothesis-lock 起点，下游各模式自治。

---

## 一、新项目 onboarding 流程

### 第 0 步：宣告

向用户简短确认：「我已读完 `~/.claude/skills/analyst-research/references/workflow.md` 与 `report_style_spec.md`，准备启动 analyst-research 8 步流程。」

### 第 1 步：onboarding 问题（一次 4 题，问完锁定不再追问）

**Q1 · 研究问题或 hypothesis（一句话）**：用户给出要研究的具体问题。

**Q2 · 目标读者**：

- 专家 / 决策者（与 light 对齐，不写科普背景）
- 双兼（受过本科教育的非专业读者 + 专业读者，需穿插必要的术语解释，与 heavy 对齐）
- 其他（用户描述）

**Q3 · step 2 广搜后是否硬停审查**：

- 否（default）：广搜完成后 AI 直接进 step 3 outline，跑到 step 7 sign off 才停。适合话题清晰、用户信任 AI 选材的场景
- 是：广搜完成 AI 出 `2_research/research.md` 后停下来等用户审 ledger，确认补漏后再进 step 3。适合话题可能跑偏、用户想提前把控选材方向的场景

**Q4 · 调色板 / 字体**：default 用 `report_style_spec.md §5.3 / §5.4` 的 FT 蓝调与 Songti SC / Times New Roman；项目要换的话用户现在说，AI 落到项目级 `CLAUDE.md`「图表 / 本项目确认的具体值」段。

**Q5 · 报告语言**：英文（default）/ 中文 / 其他。不指定即按英文写 draft（见 SKILL.md「Reply language」），锁定记入 CLAUDE.md。英文稿跳过中文冒号红线、强制执行 unescaped `$` 红线（金额写 `\$`）。

**不问的事项**（default 锁定）：

- 产出形态：PDF（主） + Word docx（派生），**不出 HTML、不出公众号 JPG、不出 slide**
- 篇幅：12-15 页目标（**< 12 页视为偏薄,回补内容或加图深度,不交差**；6-7 页强警告 + 建议转 light;16-20 页强警告 + 建议精简;20+ 页重新评估 medium / heavy)
- 图表：6-10 张，**图表前置**（先做图再写正文，沿用 heavy step 7 纪律）
- LLM：单 LLM only（Claude solo 全程），不调多 LLM critique
- 摘要形态：default 用「三段式摘要」（结论 + 关键数字 + so-what）。用户要 BLUF 单段就明说
- 时间预期：约 1 小时单 session 跑完
- 作者署名 / 邮箱：从全局 `~/.claude/CLAUDE.md`「作者署名」段读 default，无此段才显式问

### 第 2 步：搭建脚手架

cwd 切到项目根后跑：

```bash
mkdir -p 1_topic 2_research/pdfs 2_research/_process \
         3_outline 4_data/1_raw 4_data/2_processed \
         5_scripts 6_figures 7_draft && \
cp ~/.claude/skills/analyst-research/references/_quarto-medium.yml _quarto.yml && \
touch _state.md CLAUDE.md
```

7 个编号子目录（1_topic 到 7_draft），**砍掉 `8_publication/` 与 `9_retrospective/`**（medium 不做长篇派生与逐节复盘）。`pdfs/` 与 `_process/` 作为 `2_research/` 的子目录承担文献全文与原始过程稿留底。

`5_scripts/_path.py`（11 行）模板：

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "4_data" / "1_raw"
DATA_PROC = PROJECT_ROOT / "4_data" / "2_processed"
FIGURES = PROJECT_ROOT / "6_figures"

SKILL_SCRIPTS = Path.home() / ".claude" / "skills" / "analyst-research" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

import chart_template
chart_template.FIGURES = FIGURES
```

`.claude/settings.json` 项目级权限（与 heavy / light 相同，签入 git）：

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

### 第 3 步：写第一份 CLAUDE.md + _state.md，启动 step 1

`CLAUDE.md` 模板包含：项目方向、目标读者、产出形态、与框架的偏离（初始为空）。`_state.md` 模板见 §十。

把第 1 步收到的 hypothesis 写到 `1_topic/topic.md` 初稿（一段话研究问题 + 关键约束）。软停推进到 step 1，告知用户。

---

## 二、8 步骨架

| 步骤 | 名称 | 停点 | 时间预算 | 与 heavy 对应 |
|---|---|---|---|---|
| 1 | 话题 + 思路 | 软停 | 15 min | 融合 heavy 1+3，砍 heavy 4 话题硬停 |
| 2 | 广搜（覆盖 4 类以上，规模 15 源左右） | 软停 / **用户可选硬停** | 45 min | 完整继承 heavy 2 + 附录 A，规模压缩 |
| 3 | outline draft（h1 + h2 + 图表清单） | 软停 | 20 min | heavy 6 精简 |
| 4 | 数据 + 图表 6-10 张（一图一脚本、双双落盘、视觉自检 4 项） | 软停 | 60-90 min | **完整继承 heavy 7 纪律**，张数压缩 |
| 5 | draft 一气连写 12-15 页 | 软停 | 45-60 min | heavy 8 default 路径 |
| 6 | self-critique + verifying（单 LLM 内一气走，调 `market-research-skills:verifying`） | 软停 | 20 min | heavy 9b + 9c 合并精简 |
| 7 | 用户 sign off（用户通读 v1 PDF 提意见，反复迭代） | **硬停** | 看用户节奏 | heavy 9d |
| 8 | 定稿 + Word 派生（quarto render + pandoc qmd→docx） | 软停 | 10 min | heavy 10 精简，砍 HTML / 公众号 |

**全部 0 硬停 ≠ 0 自检门**。AI 各步落盘后简短告知用户阶段产出，**软停就自动推进**。step 7 是唯一强制硬停。step 2 是否硬停由用户在 onboarding Q3 决定。用户随时可叫停、调整方向、要求回退。

砍掉的 heavy 步骤：3（AI 单独建议方向）/ 4（话题硬停）/ 5（补搜，融入 step 2）/ 9a（DS 润色）/ 9b 与 9c 拆分 / 10c (HTML 派生) / 10d (公众号派生) / 11（逐节复盘）。

---

## 三、各步骤细则

### 步骤 1：话题 + 思路（软停）

**关键问题**：用户的方向是否清晰？AI 能否一次性给一个站得住的研究思路？

**操作**：

1. 用户 onboarding Q1 给出 hypothesis 后，AI 直接写 `1_topic/topic.md`：
   ```markdown
   # 题目
   <一句话>

   # 研究问题
   <一段话，2-3 句>

   # 关键约束
   - 时间锁：<YYYY-MM-DD 快照>
   - 目标读者：<专家 / 双兼>
   - 输出形态：PDF + Word，12-15 页，6-10 图
   - 必须覆盖的子问题（3-5 个）：
     - ...

   # 研究思路（AI 提一版）
   <按子问题列章节骨架，4-6 个 h1。仅 h1 粗轮廓，h2 细化留到 step 3 outline。>
   ```

2. **模糊 hypothesis 的 nudge**：若用户给的 hypothesis 模糊（范围 / 时间锁 / 子主题边界不明），AI **自行给出 assumption 写入「关键约束」段**，告知用户「按以下假设推进，您可叫停修正」。**不停下来等用户确认**。软停设计下用 assumption 透明化代替硬停。

3. **章节骨架**：研报正文仅两级（h1 + h2），**禁止 h3**（详见 `report_style_spec.md §1.2`）。step 1 阶段只列 h1 粗轮廓。

**软停**：`topic.md` 落盘后告知用户「话题与思路初稿落盘，5 个 h1 章节，按此进 step 2 广搜」。自动进 step 2，不等用户确认。

**禁止**：不要在 step 1 阶段给多个候选方向让用户选（那是 heavy step 3 做的）。medium 假设话题在 onboarding 已成形，AI 一次性给一版思路推进。

---

### 步骤 2：广搜（软停，用户可选硬停）

**关键问题**：围绕话题，世界上**已经存在**哪些数据和资料？

**目标**：定话题方向（数量优先，覆盖面优先）。规模压到 15 源左右（heavy 通常 30-50 源）。

**操作**：Claude solo 走遍以下来源类别，配合 iFinD MCP 或 `financial-data-sources` skill 抓数据。Claude 综合到 `2_research/research.md`。

**关键纪律：来源覆盖（7 类至少 4 类必检）**

广搜阶段 AI 必须**主动检索以下 7 类来源**，至少 4 类有命中（heavy 是 7 类全覆盖，medium 是 4 类，按话题 / 受众情境）：

| 类别 | 代表 |
|---|---|
| A.1 国际机构 | IMF、World Bank、IEA、OECD、BIS、UN、地区开发银行 |
| A.2 主权 / 政府 / 央行 | 央行、统计局、财政部、主权基金、行业监管 |
| A.3 学术与智库 | NBER、SSRN、Google Scholar、Brookings、CSIS、Chatham House |
| A.4 投行 + 咨询 | GS / JPM / MS / Citi 等 Country Outlook，麦肯锡 / BCG 等行业报告 |
| A.5 主流财经媒体 | 中文：财新、华尔街见闻、FT 中文等；英文：Bloomberg、Reuters、FT、WSJ、Economist |
| A.6 公众号 / 行业社群 / 公共社交平台 | 财经 / 区域 / 垂直行业的中文公众号，LinkedIn / Substack / 公开 X 讨论 |
| A.7 数据库（程序化） | 项目可用的 MCP / API / skill：iFinD、`financial-data-sources` skill（FRED / yfinance / SEC EDGAR / AKShare 等） |

**类别选择参考**：

- 纯宏观议题通常 A.1 + A.2 + A.5 + A.7
- 公司议题通常 A.2 + A.4 + A.5 + A.7
- 政策议题通常 A.1 + A.2 + A.3 + A.5
- 区域议题通常 A.2 + A.5 + A.6 + A.7

**中英文并重**：国际机构、投行、学术英文为主，区域、政策、一手新闻中文常更准。

**关键纪律：「打开网页下载，再判断」**

数据侦察时**至少下载一个代表性时点的实际数据再判断可达性**，不要只看 SERP 摘要 / 印象 / 网站描述就下结论「数据不全」。

**关键纪律：核心 PDF 全文下载**

承担**结构性论证作用**的文献必须下载全文 PDF 到 `2_research/pdfs/`，统一编号 `<编号> <机构> <标题>.pdf`，下载后**优先用 pypdf 抽全文摘要**（结构化提取标题、章节、表格更稳）。pypdf 解析失败再用 Read 工具的 `pages` 参数限页读。

「结构性论证作用」的判断标准（任一即触发）：
- 一个章节的核心论点引用它
- 它提供了关键数字
- 它的方法论被本项目借鉴或对照

medium 的核心 PDF 量级约 3-5 份（heavy 通常 10-15 份）。

**关键纪律：IMF / Cloudflare 类 PDF 受限处理**

IMF eLibrary、BIS WP、ECB papers 等机构的直链 PDF 经常被 Cloudflare 拦截（返回 462 字节 HTML 重定向）。标准动作：

1. **NOTES 占位**：`2_research/pdfs/_NOTES_<机构>_<标题>.md` 写明「直链被 Cloudflare 拦截、已尝试 curl 与 WebFetch」+ 记录 SERP 摘要与 press briefing 替代 source
2. **引用降级**：研报正文写「据 IMF WEO Apr 2026（press briefing）」明示二手转述，不写「据 IMF WEO Apr 2026 figure X」
3. **挂用户补**：在 `research.md` 该条目重要性字段加 `⚠️ 待用户手动下载补全`，给用户清单在 step 7 sign off 之前补

**关键纪律：用户补充资料优先**

用户随时可把资料放到 `2_research/pdfs/`。这些文件优先级**高于 AI 自己搜的资料**：

- AI 必须主动**通读全文**（用 Read 全文，不只看摘要 / 目录）
- 在 `research.md` 标注「来源：用户补充」，重要性默认为「核心」
- 用户补充资料的内容如与 AI 自搜资料冲突，**以用户补充为准**

**交付物**：

- `2_research/research.md`：15 条左右资料台账（按 4-7 类组织），每条记录类型 / 机构 / 标题 / 年份 / URL / 关键数字 / 重要性 / 获取方式
- `2_research/pdfs/`：3-5 份核心 PDF 全文
- `2_research/_process/`：原始搜索记录（如有多轮 query）

**软停 / 硬停**：

- onboarding Q3 选「否」（default）：落盘后告知用户「广搜完成，15 源左右覆盖 X 类。按此进 step 3 outline」，自动进 step 3
- onboarding Q3 选「是」：**硬停**等用户审 `research.md` ledger，用户确认或补漏后进 step 3

**踩坑警示**：

- 单家 LLM 的关键判断必须对照另一类来源（如 IMF 估算对照官方主权方披露）才能成结论，**单一来源孤证不立**
- 「找不到」要谨慎下结论，可能是检索词不对，再换一两组关键词

---

### 步骤 3：outline draft（软停）

**关键问题**：基于完整资料库，详细 outline 长什么样？

**操作**：

1. 基于 step 2 资料库写 `3_outline/outline.md`
2. **章节骨架**：h1 / h2 标题本身就是结论性的（不写「财政视角」，写「财政视角：油气占财政收入 30%-90% 的三梯度」）。研报正文仅两级，**禁止 h3**
3. **每个 section 列出**：
   - 研究子问题（一句话）
   - 核心 take-away（一句话）
   - 计划用的图表（具体到图编号、底层数据来源）
   - 关键引用（具体到文献名 + 页码）
4. **强制段落**：「不做什么」+「不确定性边界」（数据缺口、口径限制、商业信息风险等）

**图表清单生成**：Claude 基于资料库给图表清单（每节建议哪些图能支撑论点），目标 **6-10 张**，**已按 step 4「加图判据 6 条」预筛**。

**outline 与 step 4「加图 / 删图判据」的关联**：

- outline 列图表清单时已逐张过加图判据
- step 4 commit 前过删图判据，触发即删
- 新增图清单变更（step 4 实施中发现需要加图）必须**回 step 3 同步 outline**，不能让正文与 outline 失同步

**Outline 即合同（地板锚点）**：outline 的章节数 + 图清单是 step 5 draft 与 step 8 定稿要被比对的合同。两项检查：（1）若计划的 outline 无法合理达到 12-15 页 / 6-10 图，说明太薄——在 `git tag outline-final` **前**加深，不要锁一份单薄合同、到 step 8 才发现缺口；（2）签字的数字成为 §六 计数门地板——终稿图比合同少即为违约（补回，或告诉用户哪个计划项被砍、为什么）。静默缩水是典型偷懒失败模式。

**outline 版本号**：

- **v1**：step 3 初稿落盘后软停，自动进 step 4
- **v2 / v3 / ...**：step 3 ↔ step 4 双向迭代后的修订版（step 4 图表做出来发现口径冲突、新论证角度等，回 step 3 改 outline）
- **final 版**：step 4 图表全部落盘后形成 outline final，AI 自动打 `git tag outline-final`，自动进 step 5

**软停**：`outline.md` v1 落盘后告知用户「outline draft 落盘，N 张图清单已列。进 step 4 完成图表」，自动进 step 4。用户随时可叫停审 outline。

---

### 步骤 4：数据 + 图表 6-10 张（软停）

**关键问题**：所有图表先做出来，看看论证站不站得住？

**为什么图表前置**：先做图再写正文是钻石级实战洞察。曾有项目先写了 outline 和正文「X 国某政策目标 65%」，画图时才发现这个数字根本不对应该指标。如果先做图，画图过程中口径不可比的问题立刻暴露。

**操作流程**：

0. **前置：chart_template pre-flight 自检**。开第一张图前先跑 chart_template 自检，出一张含 `$` 美元金额 / 多 plot 元素 / 横向柱图 / legend 的 dummy 图到 `/tmp/`，肉眼检查：① `$xxx` 显示是否带反斜杠字面量（chart_template `_wrap_text_precise` 应已加 parse_math guard）；② annotation 颜色是否与 plot 同色被吃掉；③ 长 y-tick label 是否被裁切。任一项触发，**先修 skill 全局 chart_template 再画正式图**

1. **数据落盘**：原始下载落 `4_data/1_raw/`、处理后版本落 `4_data/2_processed/`，命名 `<节号>_<主题>.csv`
2. **脚本落盘**：**一图一脚本**（详见 `report_style_spec.md §3.1`），命名 `make_fig_<节号>_<编号>_<topic>.py`，head docstring 写清用途 / 输入 / 输出。**每个脚本只画一个 plot，禁止并列子图**（spec §3.7）。脚本顶部 `import _path` + `from chart_template import ...`
3. **图表生成**：每张图输出 PDF + JPG 两格式到 `6_figures/`（**medium 砍 `_clean.jpg`**，不出 publication HTML 也不需要第三种栅格），命名 `fig_<节号>_<编号>_<topic>.{pdf,jpg}`。`save_fig` 接受 `title / source / note` 参数：PDF 裸图（Quarto caption 提供）；JPG 自包含烧入。JPG 长边 ≤ 2000px（spec §3.11）
4. **回填 outline**：每张图完成后回填到 `3_outline/outline.md` 对应 section（嵌入 `![]` 引用 + caption + 一段图下注预览）
5. **对照检查**：图能呈现的结论与 outline draft 的 take-away 是否一致？不一致回头修 outline

**关键纪律：双双落盘**

凡涉及数据处理的图 / 表，**底稿数据 + 完整脚本必须双双落盘**（reproducible）。即使图很简单也要留底稿。

**关键纪律：写图前判断（加图与删图判据）**

不规定图表总数上下限。每张图存在的唯一理由是「文字与表格无法或低效地表达某个具体释义」。每张图都要能回答测试问题：**没有这张图，读者能否同样高效地理解该段释义？** 能就不画，不能才画。

**加图判据**（写每节正文时逐节走一遍，满足任一即加）：

| 情境 | 为什么文字搞不定 |
|---|---|
| **多源对比**：同一指标 3 个以上来源数据并列 | 文字列举混乱，对比读者要心算 |
| **时序变化**：5 年以上趋势、拐点、节奏 | 文字给端点数字看不出走势形状 |
| **跨维度对比**：二维或多维（如国家 × 行业、年份 × 指标）| 文字描述失去结构 |
| **量级或分布**：分布形态、极值、quartile | 文字给统计量但失去 shape |
| **目标与实际对照**：两组数据视觉对比 | 表格能给但视觉对比速度更快 |
| **空间或流程关系**：地理、网络、流程图 | 文字描述读者脑中重建不出 |

**删图判据**（每张图 commit 前走一遍，满足任一即删）：

| 反模式 | 为什么不画 |
|---|---|
| 单一数字陈述（「某指标 = X%」） | 一句话能说清 |
| 2 至 3 项简单占比（「A 占 60%、B 占 40%」） | 饼图与文字等效，文字更紧凑 |
| 同节内对同一数据集多次切片 | 合并或选最强的一张 |
| 趋势性陈述但无具体节点数字 | 没有「在哪一年发生什么」，图无锚点 |
| 结论性、承接性、引言、结语段 | 这些段不锚定数据，不需要图 |

**step 4 「all-or-nothing」原则**：

step 3 outline 列的 N 张图清单已逐张过加图判据，**step 4 必须全部 N 张完成才能进 step 5**。不允许「先做 K 张代表图、剩余推到 step 5 文字 inline 替代」。step 4 实施中若发现某图过删图判据，**合规删图路径**：单独 commit 删图 + 同 commit 改 outline + 同 commit 把该图的数字与论点 inline 到正文。

**关键纪律：time-lock 快照数字必须 step 4 实拉**

凡涉及行情、估值、现金流、央行政策利率等 time-lock 快照数字，**step 4 出图前必须用 `financial-data-sources` skill 或 iFinD MCP 实拉一次**，以实拉数据为准。step 2 transmitted 数字仅作 sanity check 对照。差异 > 5% 必须查清原因后再决定取舍。

| 是 time-lock 快照 | 不是 time-lock 快照 |
|---|---|
| 股价、股指、汇率、收益率（当前快照） | 历史定值（如「2000 年 NASDAQ 峰值 5048」）|
| P/E、P/B、CAPE 等估值倍数（当前快照） | 公司年报披露的财年数据（10-K 一手） |
| 央行政策利率（当前 + 近期路径） | 学术论文的回归系数、弹性估计 |
| 公司财年披露但未走 10-K 一手 | 已下载 PDF 的关键数字 |

**关键纪律：title / source / note 字符串从 CSV 派生，不要 hardcode 数字**

`title` 引用具体数字时（如「财政赤字 \$32B」），脚本里**现场计算 max / min / argmax 再 f-string 插入**，不 hardcode。例：`title=f"私营女性 +{df.loc['private_female_growth'].max():.0%}"` 而非 `title="私营女性 +84%"`。

**fail-safe**：脚本顶部加一条 `assert` 校验 title 引用的数字与 CSV 计算结果一致，不一致即不允许 commit。

**关键纪律：source / note 字符串「3 处一改全核」**（medium 砍掉 references.bib 那一处）

同一图的 source / note 字符串在 **3 个位置**存在（heavy 是 4 处，medium 砍 bib 那处）：

1. `make_fig_*.py` 脚本里的 `save_fig(source=..., note=...)` 参数（JPG 自包含用）
2. `draft.qmd` 里对应 `![](fig.pdf)` 后的 `\begin{figsource}` 块（研报 PDF 用，spec §3.3）
3. 正文段落引用图时叙述的相关来源 / 时点 / 口径

**任意一处修订必须 3 处全核**。

**关键纪律：commit 前 AI 做逻辑自检，视觉自检留给用户**

按 spec §四 明文「AI 不做视觉检查」。AI 在 step 4 commit 前只做**逻辑一致性自检**，按 `report_style_spec.md §3.13 写图脚本自检 4 项`（title 数字与图内数据一致、annotation 颜色不与下方 plot 同色、横向柱图 y-tick label 完整显示、legend 居中且水平排开），任一不通过的图必须修脚本重渲再 commit。视觉自检本身留给 step 7 用户通读 PDF 时一次性做。

**软停加四条质量门**：图表全部落盘后告知用户，用户随时审 JPG 提修订意见，默认不阻塞进 step 5。四条质量门 AI 自检即可：

1. **outline 列的图全部完成或按合规删图路径已从 outline 同步删除**（不允许「待补」「分阶段」剩余推到 step 5）
2. spec §3.13 写图脚本逻辑自检 4 项全过
3. 每张已画的图过加图判据成立且过删图判据不触发
4. 自检中暴露的任何问题已修复重渲

**质量门 1 的具体核法**：grep `3_outline/outline.md` 列出的所有 fig 编号，对照 `6_figures/` 实际产出的 PDF 文件名清单，**两边数量与编号必须一一对应**。

**踩坑警示**：

- 「跨国 / 跨源对比」时必须显式记录口径差异。同一国在两种口径下相差 20+ 个百分点的情况常见
- 不要把口径不可比的指标强行画在一张「目标 vs 实际」图上，会误导读者
- 引用机构 KPI 时必须打开官方网站确认

---

### 步骤 5：draft 一气连写（软停）

**关键问题**：把图表与文献组织成研报语言。

**主导**：Claude solo 全程（初稿 + 自润色 + 格式 / 渲染调优）。critique 留到 step 6。

**写作纪律**：Claude 主笔时**严格按 §五 写作规范写**，目标是 step 5 终稿质量等同于经第三方文字润色。

**default 一气连写整稿**：Claude 按 outline 顺序写完全部章节，整稿 v1 完成后**自动进 step 6 self-critique**。理由是 outline 已经过 step 3 + step 4 双向迭代 final，take-away 已锁定，节内反复停审节奏代价远超价值，致命错误由 step 6 self-critique 与 step 7 sign off 兜住。

**fallback：节内硬停**（用户明确要求时启用）。每个 section 综合完成后停下来等用户审，下一节才写。适用场景：outline 未充分锁定、用户希望深度参与每节论证流校准。

**operating 顺序**：

1. Claude 按节写初稿（v1.0），**逐节自检 §五 写作纪律**（句号续接 / 列举冒号 / 嵌入 takeaway / ppts 改个百分点 / 书面化连接词 / 序号起头 / 不用技术符号代连词）。同时**对照 outline 合同逐节做深度检查**：每节都带上它计划的图，且不止 1-2 段一笔带过；比合同 takeaway 更薄的节回 step 2 / 4 补料，而不是用废话填充
2. 每节自检通过即立即写下一节（default 一气连写）
3. 整稿 v1.0 完成后做渲染 / 字体 / YAML 调优（v1.1 → v1.x），正文不动
4. step 5 终版 = Claude 纯版，**快照到 `7_draft/_process/draft_v1_claude.qmd`**（step 6 改文字前必须先落盘这一份，否则没有「纯 Claude 基线」可回溯）
5. 自动进 step 6

**写作前自检清单**：每节 v1 完成立刻跑轻量子集（破折号、emoji、meta-language、抒情铺垫）+「图脚本-CSV-正文三方一致」自检；整稿 v1 完成后跑 §六 全量清单。

**「图脚本-CSV-正文三方一致」自检**：每节正文引用某个图时，逐项核：

1. 正文数字是否真在 CSV 里？
2. `make_fig_*.py` 里 title / source / note 有没有也写这两个数？写的话是否一致？
3. 渲染后的 fig PDF（打开 JPG 看）轴值 / data label 是否对应？

任何一处不一致，**当节就改对**，不要拖到 step 6 让 self-critique catch。

**draft 结构模板**：

```markdown
---
title: "<题目，从 1_topic/topic.md 派生>"
author: "<onboarding 阶段从 ~/.claude/CLAUDE.md 读到的 author 字符串>"
date: today
---

# 摘要

<三段式：①结论 ②关键数字 ③so-what。默认三段；用户要 BLUF 单段就改单段>

# <第一节标题，结论性写法>

<正文……>

# <第二节标题>

...

# 结语

<拎结论 + 决策含义 + open questions>
```

**模板里不写 `format:` 段**。`_quarto.yml` 已完整定义 PDF / docx 格式与 include-in-header，draft.qmd 重写 format 段可能让某些设置回退到 Quarto default。

`{.unnumbered}` 不需要。_quarto.yml 已 `number-sections: true`，全文自动编号。

**过程稿落盘**：step 5 各小版本（v1.0 / v1.1 / …）只在 `draft.qmd` 原地迭代；大版本（v1 终版 → v2 → v3）按 `7_draft/_process/draft_<vX>_<who>.qmd` 命名落盘。**`draft.qmd` 永远只指向「当前可对外的最新版」**。

**软停**：v1 落盘 + 渲染成功后告知用户「draft v1 完成，约 X 页，进 step 6 self-critique + verifying」，自动进 step 6。

---

### 步骤 6：self-critique + verifying（软停）

**关键问题**：完整稿读起来站不站得住？所有 caveat 都核到位了吗？

**主导**：Claude self-critique（单 LLM，不调外部 GPT critique）。

**子步串行**：

#### 6a · self-critique（6 类视角，落 `7_draft/_process/critique_self.md`）

按以下 6 类视角对 draft v1 自评：

1. **事实与数据**：每个数字、年份、人名、机构名都能定位到原始来源（research.md / pdfs/ / 实拉数据）。time-lock 数字已实拉
2. **口径辨析**：跨国 / 跨源 / 跨时点的数字是否口径一致？显式标注口径差异？
3. **引用支撑**：每条 footnote `^[...]` 真支持文中陈述，不挂羊头卖狗肉。URL 可达，日期注明
4. **跨节一致**：同一数字在不同节出现，数值一致？口径一致？
5. **论证流**：每节的 take-away 是否承接 outline？每节之间衔接是否顺畅？
6. **语言规范**：跑 §六 grep self-check 全量清单

self-critique 输出落 `7_draft/_process/critique_self.md`，按 6 类分段记录发现的问题，每条带：所在段落 / 问题描述 / 修订建议 / 优先级（致命 / 严重 / 轻微）。

整合：致命 + 严重一律修，轻微视余力修。修订落 v1.1 / v1.2 等小版本。

#### 6b · verifying（调 `market-research-skills:verifying` skill）

对 step 3 outline 列的「不确定性边界」+ self-critique 抓出来的疑点，调 `verifying` skill 严格核一次。能闭合就闭合，不能闭合就保留 caveat 进 draft 终稿。

**verifying skill 调用纪律**（不可砍）：medium 没有 heavy 的独立 9c verifying 子步，但 verifying 调用本身不允许跳过。

#### 6c · 整合落 v2，进 step 7

self-critique 与 verifying 的修订整合后落 `7_draft/draft.qmd` v2 版本，**渲染成功**（quarto render 无错），**§六 grep self-check 全量过**。

落盘后告知用户「draft v2 完成（critique 修订 X 处 / verifying 闭合 Y 处疑点 / Z 处保留 caveat），进 step 7 sign off」，自动进 step 7。

---

### 步骤 7：用户 sign off（**硬停**）

**关键问题**：用户最终接受吗？

**硬停判据**：用户必须明确签字确认才进 step 8。

**操作**：

1. AI 把 v2 PDF 与 critique_self.md 一并交给用户
2. 用户通读 PDF 提修改意见
3. AI 反复迭代直到用户签字（v2.1 / v2.2 / ... 各小版本落 `7_draft/_process/`）
4. 用户签字后进 step 8

**用户审什么**：

- **视觉自检**（spec §四 明文 AI 不做视觉检查）：图字号、字体、调色板、annotation 位置、长 label 截断
- **事实最终核**：用户对领域熟悉，可能发现 AI 没 catch 的事实错误
- **论证流终判**：take-away 是否站得住、so-what 是否说服用户
- **caveat 完整性**：未闭合的不确定性是否充分披露

**用户回弹路径**：用户随时可叫 AI 回 step 5（重写某节）、step 4（重做某图）、step 3（改 outline）、step 2（补搜）。signed off 之后视为定稿，进 step 8 渲染派生。

---

### 步骤 8：定稿 + Word 派生（软停）

**关键问题**：PDF 与 Word 都生成、肉眼无误？

**操作**：

```bash
quarto render draft.qmd                    # → 7_draft/draft.pdf
quarto render draft.qmd --to docx          # → 7_draft/draft.docx
git tag v1.0                                # 定稿打 tag
```

**完成判据**：

- `draft.pdf` 与 `draft.docx` 都生成
- PDF 翻一下肉眼看：无 ctex / xelatex 错、无 figure caption 残留、页数在 12-15 目标区间（8-11 回补，见下方篇幅处理；跑 §六 计数门并贴出实测页数 / 图数）
- Word 翻一下：figure 嵌入正确、footnote 转换正确（Quarto 把 Pandoc footnote 转 Word 尾注的处理需肉眼复核）

**超页处置**：

- 12-15 页：目标区间，正常结案
- 8-11 页：偏薄，回补内容或加图深度后重渲(图清单目标 6-10 张)
- 6-7 页：强警告「内容偏薄，建议转 light」
- 16-20 页：强警告「内容偏厚，建议精简 1-2 个最弱节」
- 20+ 页：告诉用户「内容量级已接近 heavy，请重新评估是继续 medium 路径精简到 15 页内，还是转 heavy 模式重新规划」，由用户裁定，AI 不强行硬截

**完成提示**：「draft v1.0 定稿，PDF 与 Word 已生成，X 页 + Y 张图。git tag v1.0 已打。如有后续修订建议继续 v1.1 / v1.2 迭代」。

---

## 四、文档与图表规范

medium 与 heavy 共享同一份视觉规范（实文件均在 `~/.claude/skills/analyst-research/references/report_style_spec.md`）：

- 文档版式：§一
- 图表设计原则：§二
- 图表制作规则：§三（**重点：§3.1 一图一脚本、§3.7 禁止并列子图、§3.11 JPG 长边 ≤ 2000px、§3.13 写图脚本自检 4 项**）
- AI 不做视觉检查：§四
- 默认 YAML / 字体 / 调色板：§五（**调色板 §5.3、字体 §5.4**）
- chart_template 接口契约：§六

**medium 与 heavy 在 spec 上的两点偏离**：

1. **不出 `_clean.jpg`**：medium 砍 publication HTML 与公众号派生,调 `save_fig(..., clean=False)` 跳过 `_clean.jpg` 栅格,只出 PDF + JPG 两格式。(注:`clean` 参数 default 为 True;medium 脚本须显式传 `clean=False`,否则照常生成一份无害但不引用的 `_clean.jpg`)
2. **不出 references.bib + csl**：medium 用 inline footnote `^[源, 标题, YYYY-MM-DD. URL.]`，spec §3.3 提到的「figsource 块 + bib `[@cite]` 引用」简化为「figsource 块 + footnote」

两点偏离写在项目级 `CLAUDE.md`「与框架的偏离」段，不在 spec 文件本身改（spec 是 SoT，medium 与 heavy 各自项目按需偏离）。

---

## 五、写作规范

### 5.1 文风

- **陈述性优先**，目标读者按 onboarding Q2 锁定（专家 / 双兼）。专家受众假设下**不写科普背景**；双兼受众下首次术语简注一句
- 句子短促，单句信息密度高
- 主谓宾结构，少嵌套从句
- 数字精确（具体数字 + 单位 + 时点）

**句号续接**（同主题接续优先用句号断句而非逗号 / 分号）：

- ❌ 「沙特财政赤字 2024 年达 \$32B，主要受油价下跌影响，预计 2025 年扩大至 \$45B」
- ✅ 「沙特财政赤字 2024 年达 \$32B。主因油价下跌。2025 年预计扩大至 \$45B」

**列举展开**（列举三项以上用冒号引导 + 分号或句号分隔）：

- ❌ 「Vision 2030 的三个支柱包括充满活力的社会、繁荣的经济、雄心勃勃的国家」
- ✅ 「Vision 2030 三个支柱：充满活力的社会；繁荣的经济；雄心勃勃的国家」

**takeaway 嵌入**（每段开头给一句结论，再展开数据 / 引用支撑）：

- ❌ 「2024 年 GDP +2.7%，2025 年预测 +3.5%。这说明经济增长在加速」
- ✅ 「沙特经济增长在加速：2024 年 GDP +2.7%，IMF 2025 年预测 +3.5%」

**ppts 改「个百分点」**：「+45 ppts」改「+45 个百分点」（PDF 渲染稳定，不依赖 mathtext）。

**书面化用词**：

| ❌ 口语 / 学术腔 | ✅ 书面化 |
|---|---|
| 使得 | 致 / 让 |
| 进行了 | 做 / 完成 |
| 做出了 | 作出 / 给出 |
| 具有重要意义 | 重要 / 关键 |
| 一定程度上 | 部分 / 在 X 维度上 |
| 综上所述 | 综合上述 / （删去直接给结论） |
| 总而言之 | （删去直接给结论） |

**序号起头**（节内列举用编号起头，不用 bullet 与冒号混用）。

**不用技术符号代连词**（`→` `∴` `+` `/` `vs`）：

- ❌ 「PIF → 海外配置 + 国内 giga-projects」
- ✅ 「PIF 同时配置海外资产与国内 giga-projects」

### 5.2 标点与字符（红线）

- **绝对不用破折号 `——`**
- **半角连字符 `-` 仅限范围号与复合词**（`30-90%` / `2026-2030` / `single-bar`）。禁止 `-` 替代破折号
- **少用中文冒号 `：`**。能用句号断句就用句号。冒号:句号比例控制在 5-15%
- 中文引号统一用「」角引号
- **不用 emoji 与特殊符号**

### 5.3 引用

medium 不用 references.bib，统一用 Pandoc footnote 内联：

```markdown
SOFR 3M 利率最新 4.51%^[FRED, SOFR 3-Month Term Rate, 2026-05-15. https://fred.stlouisfed.org/series/SOFR3M.]，与 Powell 措辞一致。
```

- footnote 内容：`机构名, 标题或字段名, YYYY-MM-DD. URL.`（英文字段名 / 数据库 series 名直接写，不套《》；中文书 / 报告标题加《》）
- URL 必须可达（step 6 self-critique 时抽检 3-5 条）
- 同一来源在文中多次引用就重复写，**不引入 bib 共享 key**

### 5.4 摘要形态

**default：三段式摘要**（与 heavy 对齐，适合 12-15 页主题分析）：

```markdown
# 摘要

**核心结论**：<2-3 句给最强结论 + 1-2 个 critical 数字>

**关键发现**：
- <发现 1：数字 + so-what>
- <发现 2：数字 + so-what>
- <发现 3：数字 + so-what>

**决策含义**：<对目标读者的 so-what 一段话>
```

**可选：BLUF 单段**（用户明示要 BLUF style 时启用，与 light 对齐）：单段 80-150 字，第一句给结论 + 关键数字 + so-what，不分要点。

### 5.5 不写的内容（red flags）

- **不写方法论段**（除非数据处理涉及非公开口径需要说明）
- **不写 TOC 编号到 h3**（仅 h1 + h2 自动编号）
- **不写「背景」「研究意义」**类 academic 框口段
- **不写 meta-language**（「本研究将」「本节将探讨」「本研究不」）
- **不写自创比喻**（如「钢底 / 软底」类未定义术语），用方法论术语代替（「硬口径 / 软口径」）

---

## 六、grep self-check 文字红线

draft v1 完成、修订版交付前**必须** grep 核对。命令以 `7_draft/draft.qmd` 为例。

**证据要求（反「自检走过场」纪律）**：声明 self-check 全过时**必须粘最后一次实际 grep / 计数输出的数字**，不允许只口头声明「全过」。这条对计数门各行（页数 / 图数）与对语言红线同样适用。

| 红线 | 检查命令 | 应为 |
|---|---|---|
| 破折号 `——` | `grep -c "——" 7_draft/draft.qmd` | 0 |
| 标题手写编号前缀 | `grep -nE "^#{1,3} (§\|A\.\|[0-9]\|[一二三四五六七八九十]、)" 7_draft/draft.qmd` | 0 行 |
| Emoji | `grep -cP "[\x{1F300}-\x{1F9FF}\x{2600}-\x{27BF}]" 7_draft/draft.qmd` | 0 |
| 未转义美元号 `$`（**英文稿必查**，LaTeX 把 `$` 当数学定界符，未转义即渲染失败） | `grep -nP "(?<!\\\\)\\$" 7_draft/draft.qmd` | 0（正文金额一律写 `\$`） |
| h3 及更深标题 | `grep -nE "^#{3,}" 7_draft/draft.qmd` | 0 行（medium 仅 h1 + h2） |
| 正文粗体 | `grep -c "\*\*" 7_draft/draft.qmd` | ≤ 5（仅引领词例外）|
| 中文冒号「：」对句号比例 | 总冒号 ÷ 句号数，**先扣除 figsource / tblsource 块内的「来源：/注：」标签冒号**（与 heavy §7.4 一致；不扣的话 3 张图以上的报告会被强制标签冒号顶过 15%，实测 5 图正文 5.5% 但 naive 计 20%）。英文稿本项跳过(无中文冒号) | 5-15% |
| 抒情铺垫高频词 | `grep -nE "实际上\|事实上\|值得指出\|值得注意\|众所周知\|不可否认\|毫无疑问\|需要指出\|客观地讲\|不难看出\|在此背景下\|在这一过程中" 7_draft/draft.qmd` | 命中即抽检删 |
| h2 空标题反模式（学术造作） | `grep -nE "^## .*(关于\|讨论\|探究\|浅析\|思考\|现状与挑战\|视角$)" 7_draft/draft.qmd` | 0 行 |
| 半角 `-` 当破折号 | `grep -nE " - " 7_draft/draft.qmd` | 抽检，合法只剩范围号与英文复合词 |
| 技术符号代连词 | `grep -nE "→\|∴" 7_draft/draft.qmd` + 抽检 `+` `/` `vs` | 替换为完整书面表达 |
| 学术腔与口语腔 | `grep -nE "使得\|进行了\|做出了\|具有重要意义\|一定程度上\|综上所述\|总而言之" 7_draft/draft.qmd` | 命中即按 §5.1 对照表替换 |
| 模糊量化词 | `grep -nE "很大程度上\|相对较高\|相对较低\|大致\|大约\|一些\|部分" 7_draft/draft.qmd` | 抽检，无数字支撑全删或替换为具体数字 |
| meta-language | `grep -nE "本研究不\|本章不\|本研究将\|本研究为.*而设\|本章构造\|研究边界明确\|需要明示\|本节将\|本章将\|本节强调\|本章强调" 7_draft/draft.qmd` | 0 行 |
| 图脚本-CSV-正文三方一致 | 抽检 3 张图 | 数字一致 |
| outline-figures 对应 | `grep -oE "fig_[0-9]+_[0-9]+_[a-z_]+" 3_outline/outline.md` 对照 `ls 6_figures/*.pdf` | 一一对应 |
| **页数地板**（完整度） | `pdfinfo 7_draft/draft.pdf \| grep -i Pages`（poppler） | 12-15 目标；8-11 回补或加图深度；**< 8 转 light**；16-20 精简；20+ 用户裁定转 heavy |
| **图数地板** | 计数：`grep -cE "^!\[" 7_draft/draft.qmd` | 6-10，且 **≥ step 3 合同**；不足回 step 4 |
| Quarto 渲染 | `quarto render 7_draft/draft.qmd` | 成功，无 mathtext / dimension 错误 |

**计数门（反偷懒）**：页数 / 图数两行是完整度门，不是语言红线。汇报稿件完成时**贴出实测数字**。低于地板 = 没完成：用真实覆盖回补（step 2 补源、step 4 补图），**不准**用废话填充或编造。若话题确实只够 8-11 页，就说清并考虑转 light——但单薄稿通常意味着补搜 / outline 做得太浅。

**对比 heavy §7.4**：medium 砍掉 5 项与 references.bib 相关的红线（`_quarto.yml` lof / lot 对齐、未引用 fig/tbl label、框口段二轮重写、bib 字段、figsource/tblsource 占用）。其余 13 项保留。

**对比 light §六**：medium 多 2 项与图相关的（图脚本-CSV-正文三方一致、outline-figures 对应）。

---

## 七、贯穿性纪律

### 7.1 来源可追溯（不可砍）

任何数字都必须能定位到原始来源（research.md 条目 / pdfs/ PDF 名 / 实拉数据系列）。不能定位的标 ⚠️ 或剔除，**不要写进结论**。

### 7.2 不造数（不可砍）

宁可写「未公开」「待核实」，也不要给一个看似合理的猜测。

### 7.3 区分三态（不可砍）

事实（「据 IMF」）/ 估算（「据市场估算 ~X」）/ 推断（「推测可能…」），三者用不同措辞标注。

### 7.4 AI 输出 ≠ 结论（不可砍）

AI 提供素材和初稿，最终结论由人决定。medium 1 硬停（step 7 sign off）意味用户终审，AI 写完用户不能盲签。

### 7.5 verifying skill 调用（不可砍）

step 6b 必须调 `market-research-skills:verifying` skill 严格核未闭合 caveat。这是 medium 的 final verification gate，不允许跳过。

### 7.6 双双落盘（不可砍）

step 4 所有数据处理图：**底稿数据（CSV）+ 完整脚本必须双双落盘**。即使图很简单也要留底稿。

### 7.7 跨节数字硬一致性（不可砍）

同一数字在不同节出现时**数值与口径必须一致**。step 6a self-critique 第 4 类视角专核此项。

### 7.8 跨阶段决断由人做（不可砍）

step 1 话题方向、step 4 加图 / 删图边界 case、step 7 sign off 都是人做决断，AI 不强行替代。

---

## 八、复盘机制（可选）

medium **不强制逐节复盘**（heavy 是逐节追加 + 项目收尾一次性 audit）。

**可选**：项目结案后用户觉得有 cross-cutting 经验值得上溯到 skill 时，写一份 `9_retrospective/retrospective.md`（项目里临时建该目录），按 heavy §11.2 三段式格式（项目内事实 → 跨项目共性 → 应该沉淀到 skill 的内容）写。AI 协助梳理。

**触发条件**（满足任一）：

- 项目跑完用户主观觉得「这次有重要经验」
- 跑完发现 medium workflow.md / report_style_spec.md / chart_template.py 任一处有改进空间
- 跨多个 medium 项目后发现共性踩坑

不触发就跳过，medium 不为「complete」感强行做复盘。

---

## 九、与 light / heavy 的边界

不要混用。下表给清晰区分：

| 维度 | light | **medium** | heavy |
|---|---|---|---|
| 步骤数 | 6 | **8** | 11 |
| 时间预算 | 约 15 分钟 | **约 1 小时** | 约 2-3 小时 |
| 篇幅 | 5 页 / 2500-3000 字 | **12-15 页** | 1.5 万字+ / 35+ 页 |
| 图表 | 0 | **6-10 张** | 通常 15+ 张，常达 30+ |
| 引用机制 | footnote 内联 | **footnote 内联** | references.bib |
| LLM | 单 LLM only | **单 LLM only** | 单 / 多 LLM 可选 |
| 硬停 | 0 | **1（step 7 sign off）+ 可选 1（step 2 广搜后）** | 2（step 4 / 9d） |
| 派生形态 | PDF + Word | **PDF + Word** | PDF + Word + HTML + 公众号 |
| 复盘 | 无 | **可选** | 必做（§11.2 audit） |
| _state.md | 无 | **有** | 必有 |
| 目录结构 | flat + pdfs/ 一个子目录 | **7 个编号子目录（砍 8 / 9）** | 9 个编号子目录 |
| 摘要形态 | BLUF 单段 | **三段式（default）或 BLUF（可选）** | 三段式（含关键词行） |
| 受众 | 专家 / 决策者 | **专家 / 决策者 或 双兼（onboarding 选）** | 双兼（专家 + 非专业） |
| TOC / 章节编号 | 无 | **有（h1 + h2）** | 有 |
| 升级路径 | 重跑 medium / heavy | **重跑 heavy（不在原 medium 上 in-place 升级）** | n/a |

**触发判定示例**：

| 用户原话 | skill |
|---|---|
| 「给我写个 5 页 memo 看 Fed 9 月会不会降息」 | light |
| 「半天分析下 PIF 最近的海外配置变化」 | **medium** |
| 「8 页报告：中东主权基金 13F 季度变化」 | **medium** |
| 「带 3-5 张图的 X 行业季度复盘」 | **medium** |
| 「做个深度研究看美股 AI 泡沫风险」 | heavy |
| 「写一份公众号长稿讲沙特 Vision 2030」 | heavy |
| 「1 小时内出一份 brief 给老板看」 | light |
| 「快速分析下中东主权基金最近持仓」 | light |

判定不清楚时**首选轻档**（light → medium → heavy）。轻档不够再重跑下一档成本可控；反过来重档跑到一半发现题目其实只够轻档就尴尬。

**不在原 skill 上 in-place 升级**：medium 跑到一半发现题目其实够 heavy，重跑 heavy 从 step 1 开始，不要在 medium 项目目录里硬加 8_publication / 9_retrospective。reverse 同理。

---

## 十、_state.md 与项目级 CLAUDE.md

### 10.1 _state.md 模板

跨 session 进度面板，由 AI 维护，每个 session 结束前更新一次。

```markdown
# 项目级进度面板 · _state.md

> 单 source of truth，跨 session 工作的 cold-start anchor。每个 session 结束前 AI 更新。

## ▶ 当前位置（一眼可见）

- 当前 step：<step N>
- 当前子任务：<具体在做什么>
- 下一步：<即将做什么>
- 最近 session 时间：<YYYY-MM-DD HH:MM>

## 关键交付物索引

| step | 交付物 | 路径 | 状态 |
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
| 7 | sign off | (用户口头签字) | ... |
| 8 | PDF + Word | 7_draft/draft.{pdf,docx} | ... |

## 跨阶段悬而未决项

- [ ] <未闭合的 caveat 1>
- [ ] <未下载的核心 PDF X>
- [ ] <待用户裁定的边界 case Y>

## git 时间线（最近 10 commit）

<由 AI 在每次更新时贴 git log --oneline -10>

## 维护规则

- 每个 session 结束前更新一次（不是每个 commit）
- AI 把上述「当前位置」「跨阶段悬而未决项」段视为单 source of truth
- 与项目级 CLAUDE.md 的边界：本文件记**进度与状态**，CLAUDE.md 记**约定与决策**
```

### 10.2 项目级 CLAUDE.md 模板

```markdown
# 项目级 CLAUDE.md · <项目名>

> 项目级「宪法」。与全局 ~/.claude/CLAUDE.md 互补：全局放跨项目通用约定，本文件放本项目特定约定。
>
> **依赖 skill**：analyst-research（medium 模式）

## 项目基本面

- **题目方向**：<一句话>
- **产出形态**：PDF 主报告 + Word docx 派生（默认）
- **目标读者**：<专家 / 双兼>
- **工具栈**：Quarto + xelatex 渲染 PDF；Python 用户级安装（不建 venv）
- **LLM 模式**：单 LLM（Claude solo），按 medium workflow §一 onboarding 锁定

## 写作与排版

### 沿用默认

文风、标点、引用见 `~/.claude/skills/analyst-research/references/workflow.md §五`；文档版式见 `references/report_style_spec.md §一`；图表制作见 spec §二 / §三；YAML / 字体 / 调色板默认值见 spec §五。**全部继承不复述**。

### 本项目重申的红线

- 正文不用破折号 `——`
- 少用中文冒号 `：`（用句号断句）
- 中文引号统一用「」
- 标题不手写编号前缀
- h3 禁止（仅 h1 + h2）

## 图表

- 调色板：<本项目选定的调色板，引 spec §5.3 默认或本项目特化>
- 中文字体：<Songti SC 或本项目特化>
- 英文字体：Times New Roman
- 图脚本命名：`make_fig_<节号>_<编号>_<topic>.py`
- 图文件命名：`fig_<节号>_<编号>_<topic>.{pdf,jpg}`

## 领域约定

<本项目数据口径、术语翻译、信源约定>

## 与框架的偏离

<若本项目偏离 analyst-research workflow / spec 的某条规则，记在这里>
```

### 10.3 _state.md 与 CLAUDE.md 的边界

- `_state.md`：进度面板。**状态、位置、悬而未决项**。AI 高频更新（每 session 一次）
- `CLAUDE.md`：约定与决策。**调色板、口径、术语、偏离**。低频更新（决策时一次）

不要把进度信息写进 CLAUDE.md，也不要把约定写进 _state.md。

---

## 附录 A：广搜资源清单（压缩版）

7 类资源，每类列代表项。完整版见 heavy workflow.md 附录 A（medium 用户读 heavy 附录 A 不强制；本附录给的代表项已覆盖 medium 量级的 15 源需求）。

### A.1 国际机构与多边组织（英文）

- **IMF**：WEO（World Economic Outlook）/ GFSR / Article IV 国别报告 / Fiscal Monitor
- **World Bank**：Open Knowledge Repository / Global Economic Prospects / 各区域 outlook
- **IEA**：World Energy Outlook / Oil Market Report
- **OECD**：Economic Outlook / Statistics
- **BIS**：Quarterly Review / Working Papers
- **UN**：UNCTAD / UNDP / 各专项机构
- 地区开发银行：ADB / EBRD / AIIB / IsDB

### A.2 主权 / 政府 / 央行 / 监管机构

- 各国央行：Fed / ECB / BoE / BoJ / PBoC / SAMA / 等
- 各国统计局：BEA / Eurostat / NBS / GASTAT / 等
- 各国财政部 / 监管机构
- 主权基金：PIF / GIC / Temasek / ADQ / ADIA / Mubadala / 等的 Annual Report 与 13F 披露
- 行业监管：CSRC / FCA / SEC / 等

### A.3 学术与智库

- **NBER**：Working Papers
- **SSRN**：搜索 + 全文下载
- **Google Scholar**：搜索 + 引用网络追溯
- 智库：Brookings / CSIS / Chatham House / Atlantic Council / Carnegie / RAND / 等

### A.4 投行 Research 与咨询机构

- 国际投行：GS / JPM / MS / Citi / BofA / DB / Barclays / HSBC / 等的 Country Outlook、行业深度
- 咨询：McKinsey Global Institute / BCG / Bain / Deloitte / EY / KPMG / Roland Berger / 等
- 评级机构：Moody's / S&P / Fitch 主权评级与 commentary

### A.5 主流财经媒体

- 英文：Bloomberg / Reuters / FT / WSJ / The Economist / Nikkei Asia
- 中文：财新 / 华尔街见闻 / FT 中文 / 第一财经 / 21 财经
- 区域：Arab News / Gulf News / Saudi Gazette / 等

### A.6 公众号 / 行业社群（中文世界）

- 财经类：智本社 / 智堡 / 财经十一人 / 中金研究 / 中信证券 / 等
- 区域类：中东那些事儿 / 一带一路百人论坛 / 等
- 垂直行业类：根据项目话题选定
- 公共社交平台：LinkedIn 专业作者、Substack 独立分析师、公开 X/Twitter 帖子与回复。此类材料只用于发现线索和观察情绪，不是一手证据。记录 query、抓取日期、URL / post ID、作者 handle、抓取工具。可用 [TweetClaw](https://github.com/Xquik-dev/tweetclaw) 等工具抓取公开 X/Twitter 帖子与回复；任何事实性结论进入论证前，必须回到 A.1-A.5 或 A.7 交叉核实。

### A.7 数据库（程序化访问）

- **FRED**：美国宏观经济
- **yfinance**：美股 / 港股 / 全球行情
- **SEC EDGAR**：美股监管文件，含 13F
- **iFinD MCP**：A 股 / 港股 / 中国宏观
- **AKShare / Baostock / Tushare**：A 股 / 港股 / 中国宏观
- **CoinGecko**：加密货币
- **World Bank / IMF / OECD / Eurostat / ECB**：开放 API
- 通过 `financial-data-sources` skill 统一调用

### A.8 中英文并重原则

国际机构、投行、学术英文为主，区域、政策、一手新闻中文常更准。medium 单 LLM 模式下 Claude 一家走遍 4-7 类，中文区域类用 iFinD MCP 与公众号 WebFetch 补足。
