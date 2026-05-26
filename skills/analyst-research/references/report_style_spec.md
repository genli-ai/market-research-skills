# 研报视觉规范 v1.0

> 跨项目通用的报告与图表视觉规范。本文件与 `workflow.md`（过程纪律）+ `chart_template.py`（实现代码）三件套配套使用。
>
> 与 `chart_template.py` 的边界：本文件讲「为什么这么定 + 接口契约」，code 讲「具体怎么实现」。HEX 与 rcParams 的真值在 code 里（`PALETTE` dict + `setup_style()` rcParams），本文件 §5 的对照表仅为人工速查，**真值漂移时以 code 为准**。
>
> 设计灵感：**Financial Times chart-doctor**（github.com/Financial-Times/chart-doctor）开源规范。FT 的金融研报视觉化是行业标杆，原则简洁可复刻。本文档吸收其设计哲学，结合中文研报场景调整。
>
> 项目级 CLAUDE.md 可覆盖本文档默认值（覆盖时需在「与框架的偏离」段登记理由）。
>
> 本文档同时作为 `heavy-research` skill 的 `references/report_style_spec.md`。在 skill 中三件套分层位于 `references/`（本文档、workflow.md）与 `scripts/`（chart_template.py）；在用户研报项目里三件套扁平位于 `heavy-research/`。下方所有引用其他两个三件套文件时按文件名直引，不带路径，两种结构都能解析。

---

## Quick start

**给新项目脚手架阶段的 AI 与人**：本节是「开始画图前必读」摘要。完整规则在 §一-§六。

### 三件套关系

| 文件 | 位置 | 角色 |
|---|---|---|
| `SKILL.md` | `heavy-research/` | skill 入口（frontmatter + 加载顺序） |
| `workflow.md` | `heavy-research/references/` | 过程纪律：十一步骨架、多 LLM 分工、复盘格式 |
| `report_style_spec.md` | `heavy-research/references/` | 视觉规范（本文档）+ chart_template 接口契约 |
| `chart_template.py` | `heavy-research/scripts/` | 绘图实现 single source of truth：`PALETTE`、`setup_style`、`save_fig`、`legend_above` |
| `publication-style-template.html` | `heavy-research/scripts/` | publication HTML 模板（10c 可选派生用） |
| `author.jpg` | `heavy-research/scripts/` | 作者头像 placeholder（10c 可选派生用） |
| `_path.py` | `5_scripts/` | 4 行 sys.path 注入到 `../heavy-research/scripts/`。新项目脚手架阶段必须先建（内容见 §6.4 末尾） |

### 绘图脚本硬规则

每个 `5_scripts/make_fig_*.py` 顶部 5 行 boilerplate 不可省：

```python
import _path  # noqa: F401  -- 把 heavy-research/scripts/ 加进 sys.path
from chart_template import setup_style, save_fig, PALETTE, FIG_W, DATA_PROC

setup_style()
```

落地约束：

1. **不允许在脚本里硬写 HEX 颜色**。颜色一律 `PALETTE["primary" / "secondary" / "tertiary" / "accent" / ...]` 引用（语义见 §5.3）
2. **不允许在脚本里 override matplotlib rcParams**。字体、字号、spine、网格、tick 全部由 `setup_style()` 统一设定
3. **figsize 宽度必须锁定 `FIG_W`**：`figsize=(FIG_W, h)`，h 自由（一般 3-4 inch）。手写 `figsize=(10, 5)` 等会让图被 Quarto 缩到 textwidth、字号一并缩水（§3.12）
4. **一图一 plot，禁止并列子图**：`plt.subplots(1, 2, ...)` 等任何并列布局都禁止（§3.7）。多 plot 需求拆成多张独立图
5. **Legend 放 plot 上方水平排开、以 image 为基准居中**：默认用 `legend_above(ax, ncol=N, mode="centered")`（**不要**直接写 `bbox_to_anchor=(0.5, 1.02)`——那是 plot 中点不是 image 中点）；项多 / 单 accent 突出图用 `mode="image_left"`。不允许 legend 覆盖 plot / 与图形元素重叠 / 垂直堆叠（§3.8）
6. **出图只走 `save_fig` 接口**。它自动产 PDF（嵌 Quarto）+ JPG（带烧入 title / source / note，独立分发）+ `_clean.jpg`（裸图栅格，供 publication-style HTML 嵌入）**三格式**，JPG 长边自动 ≤ 2000px（§3.11）。**表格不走图片管线、直接写 markdown 表（§3.9）**
7. **PDF 是裸图 / JPG 自包含 / `_clean.jpg` 是裸图栅格**，三者承载不同内容（§3.3）。`save_fig(fig, fig_id, title=, source=, note=)` 一次调用同时管三份

完整 boilerplate 模板见 §6.4，接口契约见 §六。

### 文档导航

- §一 **文档版式**：QMD / 标题层级 / 字号统一 / 换页 / 加粗等
- §二 **图表设计原则**：FT chart-doctor 五条（typography 两层 / chrome 最小 / single accent / 标题承担论点 / 数据 - 油墨比）
- §三 **图表制作规则**：一图一脚本 / 三格式输出（PDF + JPG + _clean.jpg）/ 调色板 / 图例 / 子图 / 不重叠 / 2000px 上限
- §四 **视觉检查**：AI 不做，用户自查
- §五 **默认值速查**：Quarto YAML 标准头 / 字号字体表 / 调色板 HEX 表
- §六 **chart_template 接口契约**：`setup_style` / `PALETTE` / `save_fig` / `legend_above` 怎么调 + 完整调用模板 + `_path.py` 内容
- §七 **publication-style HTML 派生稿**（步骤 10 可选）：consulting / FT 长稿风格的 HTML → PDF 模板规范，1 div = 1 A4、in-HTML 页码、`_clean.jpg` 嵌入、手动平衡分页、浏览器手动保存 PDF、公众号 JPG 切页等

---

## 一、文档版式

### 1.1 默认格式

主报告默认 **QMD**（Quarto markdown）渲染 PDF。MD 仅用于复盘、过程笔记、状态文件。MD 不进入主报告交付路径。

**HTML 派生**（consulting / FT 长稿风格）按需做，规范见 §七；HTML 不替代 qmd 主报告，qmd 始终是真相之源。

### 1.2 标题层级

**适用对象**：**仅研报主报告 PDF**（`7_draft/draft.qmd` 渲染版）。

**不适用**：

1. **任何派生稿**（Word docx / 公众号长稿 / 邮件简报 / 推文 / Slack 长贴等）。派生平台有自己的层级和折叠机制（Word 受众接受多级编号，公众号目录靠加粗 + 编号，推文靠分段；不能套用主报告的 h1/h2 严格两级规则）
2. **方法论文档**（`workflow.md` / `report_style_spec.md` 本文档 / 项目级 `CLAUDE.md`）
3. **状态文件**（`_state.md`）
4. **各阶段成果 md**（`topic.md` / `research.md` / `outline.md` / `data.md` / `scripts.md` / `figures.md` / `retrospective.md`）
5. **过程材料**（`_process/` 下任何文件）

以上这些都需要 h3+ 做跳读骨架，不受本规则约束。

**研报正文仅两级：h1 大节 / h2 小节**。**禁止 h3 及更深**。三级标题让目录冗长、读者迷路。如果一节有多个子点，让段首结论句承担分层。

如果一节确实点多到需要 h3 才说清，那是结构问题，应该把这一节拆成两个 h2，而不是开 h3。

### 1.3 标题文字

- **主标题 ≤ 15 字**。可读性优先，完整性靠副标题补
- **副标题字号 = 主标题字号**，副标题内容不重复主标题已有限定词
- **节标题（h1）≤ 12 字**。论点性短句，不抒情，不堆砌「评估 / 探究 / 浅析」
- 节标题不要重复主标题。主报告题为「X 政策真效果评估」时，§1 再写「X 政策中的真效果问题」就是反例
- **不要手写 §N / N.N / A.N 前缀**。Quarto `number-sections` 自动加，手写叠加变「2 §1 真依赖度」

### 1.4 字号统一

主报告 PDF **6 档字号：18 / 16 / 14 / 12 / 11 / 10 pt**。中文字体一律 Songti SC，英文字体一律 Times New Roman，阿拉伯字体一律 Noto Sans Arabic。

| 元素 | 字号 | 字重 |
|---|---|---|
| 主标题（封面） | 18pt | 加粗 |
| 副标题（封面） | 16pt | 常规 |
| 目录 / 图目录 / 表目录 标题 | 14pt | 加粗 |
| h1 节标题 | 14pt | 加粗 |
| h2 小节标题 | 12pt | 加粗 |
| 正文段落 | 11pt | 常规 |
| 作者 / 日期 | 11pt | 常规 |
| 摘要标题「摘要」 | 14pt | 加粗居中（与目录三标题同档）|
| 摘要正文 | 11pt | 常规 |
| 关键词行（abstract 末尾「**关键词**：...」） | 11pt | 「关键词」三字加粗，列表常规 |
| 目录 / 图目录 / 表目录 条目 | 11pt | 常规 |
| 行内引用 `[@key]` 渲染后 | 11pt | 常规 |
| 图 caption / 表 caption | 11pt | 常规 italic |
| 表头 | 11pt | 加粗 |
| 表体 | 11pt | 常规 |
| 行内注 / 脚注 | 11pt | 常规 italic |
| 参考文献条目 | 11pt | 常规 |
| **图下来源 / 注** (`::: {.figure-source}`) | **10pt** | 常规，灰度 |
| **表下来源 / 注** (`::: {.table-source}`) | **10pt** | 常规，灰度 |

**字号选型逻辑**：

- **11pt 是基线**。所有 body-like 元素（正文 / 摘要 / 作者 / 目录条目 / 引用 / 表 caption / 表头 / 表体 / 脚注 / 参考文献）一律 11pt。视觉上跨元素读起来等同正文一档，简化层级
- **12pt = h2 小节标题**，唯一小节级强调
- **14pt = h1 节标题 + 目录 / 图目录 / 表目录标题**，大节级强调
- **18pt = 主标题**，唯一封面顶级，加粗
- **16pt = 副标题**，仅次于主标题，常规字重；与主标题用「字号差 2pt + 字重」两层手段共同区分
- **10pt = 图下 / 表下来源与注**。专供 `::: {.figure-source}` 与 `::: {.table-source}` 块，比正文小一档实现视觉降级。图 / 表 caption（出现在图 / 表上方）仍 11pt 与正文齐平，只有 source / note（出现在图 / 表下方）降到 10pt
- **不引入 9pt**。9pt 在 PDF 阅读尺寸下接近可读极限，不必要的层级

实现见 §5.1 YAML 头与 include-in-header；本表是目标值，渲染后用 PDF reader 抽样校验。

**关键词约定**：

**不使用** Quarto / pandoc 的 YAML 顶层 `keywords:` 字段——它只写到 PDF 元数据（hyperref 的 `pdfkeywords`，仅 Acrobat 文件属性面板可见），**不渲染为可见文本**，对内部投研报告无价值。保留它反而引起误解（看到 YAML 写了 keywords 但 PDF 上没显示）。

**做法**：在 `abstract:` YAML 字段的摘要文本末尾另起一段加内联关键词行：

```yaml
abstract: |
  ... 摘要正文 ...

  **关键词**：核心主题 | 国家或地区 | 关键政策 | 关键机构 | ...
```

关键词之间用 ` | ` 分隔，避免与中文顿号、英文逗号在视觉上混淆。「关键词」三字加粗，列表常规。

**关键词选择规范**：

- **数量**：5-7 个
- **必含五类**（按顺序）：① 研究对象（如某政策名、某主权基金）② 核心议题或事件 ③ 关键机构 ④ 研究方法或视角 ⑤ 地域或时间锚点
- **全部具体名词**，避免抽象词（如「经济」「分析」「研究」「问题」「挑战」「思考」）
- **避免概括性词组**（如「经济多元化」可接受，「全球经济一体化」太宽泛）
- **首字母大小写**：英文专名按官方写法（IMF、PIF 全大写，NEOM 全大写，Vision 2030 含数字）；中文专名按通用译法

**例外**：若研报要进学术数据库 / 检索系统，需要 PDF 元数据 indexing 时再补 YAML `keywords:` 字段，并接受「YAML + 内联」两份要手动同步的代价。

### 1.5 段首缩进与段间距

**全文统一无首段缩进，包括摘要与正文**。覆盖 ctexart 的默认 `\parindent=2em`，显式设 `\parindent=0pt`。

无缩进时段间必须加视觉空白，否则段落粘成一团。默认 `\parskip=0.5em`（半行高，自动跟字号缩放）。

ctexart 摘要环境也跟随同一规则，不另设例外。实现见 §5.1 YAML 头。

### 1.6 页边距

全文统一。**摘要 / 目录 / 索引页页边距 = 正文页边距**。标准上下 25mm、左右 20mm。

### 1.7 换页规则

以下位置**强制换页**（其他位置按 LaTeX 自然分页流动）：

| 位置 | 实现方式 |
|---|---|
| 封面 | `\maketitle` 默认 `\thispagestyle{empty}` |
| **目录开始前** | LaTeX `\AtBeginDocument` + `\pretocmd{\tableofcontents}{\clearpage}`（见 §5.1）|
| **图索引开始前** | LaTeX `\AtBeginDocument` + `\pretocmd{\listoffigures}{\clearpage}`（见 §5.1）|
| **表索引开始前** | LaTeX `\AtBeginDocument` + `\pretocmd{\listoftables}{\clearpage}`（见 §5.1）|
| **表索引结束后**（进入正文前） | LaTeX `\AtBeginDocument` + `\apptocmd{\listoftables}{\clearpage}`（见 §5.1）|
| **附录开始前** | qmd 正文里在附录 H1 标题前手写 `{{< pagebreak >}}` |
| **参考文献开始前** | qmd 正文里在 `# 参考文献` 前手写 `{{< pagebreak >}}` |

**布局结果**：封面 + 摘要（合页）→ 目录（独立）→ 图索引（独立）→ 表索引（独立）→ 正文 → 附录（独立）→ 参考文献（独立）。每个「导航类」区块都独立成页，避免标题与内容分离。

**为什么图索引 / 表索引前需要强制换页**：tocloft 用 `\begin{center}...\end{center}` 居中标题时（见 §1.8），标题在垂直模式下作为独立段落，LaTeX 会按分页规则把「孤立标题」推到前一页底部、内容到下一页，导致标题与条目分离。`\clearpage` 强制 LoF / LoT 从新页开始，保证标题与条目同页。这是工程上的妥协，不是审美选择。

### 1.8 图 / 表索引

- 图索引（List of Figures）和表索引（List of Tables）**两者都必须有**
- 编号**连续**：图 1 / 图 2 / ... / 图 N，表 1 / 表 2 / ... / 表 M
- **不允许节内编号**（图 1.1 / 表 6.1 这种）
- Quarto `lof: true` + `lot: true` 自动生成两索引
- **三个索引标题（目录 / 图目录 / 表目录）统一居中**——直接覆盖 tocloft 的 `\@cftmaketoctitle` / `\@cftmakeloftitle` / `\@cftmakelottitle` 三个 hook，标题用 `\begin{center}...\end{center}` 强制居中（见 §5.1）。**不要用 tocloft 自带的 `\hfill` 前后包夹法**——它在 article 模式 + 标题接在前文段落（如摘要）之后时不可靠，常偏移到右侧
- **图索引 / 表索引开始前强制换页**——`\begin{center}` 居中触发标题作为独立段落，LaTeX 会把孤立标题推到前一页底部、内容到下一页。`\clearpage` 在 LoF / LoT 前面强制换页，保证标题与条目同页（见 §1.7）
- **表索引结束后强制换页进正文**（与 §1.7 一致）
- 实现汇总——`\AtBeginDocument` + `\pretocmd{\listoffigures}{\clearpage}` + `\pretocmd{\listoftables}{\clearpage}` + `\apptocmd{\listoftables}{\clearpage}`（见 §5.1）

**重要踩坑**：tocloft 在 `\AtBeginDocument` 里重定义 `\listoffigures` / `\listoftables`，所以 patch 必须也包在 `\AtBeginDocument` 中、且依靠 hook FIFO 顺序在 tocloft 之后跑——否则 patch 会被 tocloft 的重定义覆盖。直接 preamble 里 `\let + \renewcommand` 或不包 `\AtBeginDocument` 的 `\apptocmd` / `\pretocmd` **不生效**。

### 1.9 节间无分割线

节与节之间不画 `---` / `\hrule` / `***` 等横线。章节由换页或空行分隔即可。

### 1.10 加粗使用

**理想是正文零加粗**。强调通过句首结论句、h2 标题、表格行高亮、图突出色承担。如必须加粗，仅限：术语首次定义、单点强调。**每段加粗 ≤ 1 处，每节加粗 ≤ 3 处**。

### 1.11 页眉页脚

**全文无页眉**。**页尾仅居中显示页码**。

实现：`\pagestyle{plain}` 覆盖 ctex `chinese-article` scheme 默认的 `\pagestyle{headings}`（后者会在页眉显示 `\rightmark` 即上一节标题名 + 页码，索引溢出页常出现「图索引 N」等遗留信息）。

封面页由 `\maketitle` 自动设 `\thispagestyle{empty}` 抑制页码，无需额外配置。

理由：① 中文投研报告读者扫的是结构（看目录与章节标题就够），不需要每页页眉重复章节名；② headings 样式在索引溢出页会显示上一章遗留的 `\rightmark`，造成「图索引」「目录」等字样错位出现；③ 简化即美。

---

## 二、图表设计原则（FT chart-doctor inspired）

五条原则按重要性排。具体 HEX 值统一在 §5.3 配色，本节只讲原则不列颜色。

### 2.1 typography 两层级差

字体层级靠**字号 + 颜色**承担，**不靠字重**（FT 标题用 regular 字重）：

| 元素 | 字号 | 字重 | 颜色 |
|---|---|---|---|
| 图标题（JPG 内） | 14pt | 常规（regular） | text |
| 轴标签 / 来源 / 注 | 9pt | 常规 | text_light |

**只有一级标题**，不要副标题。论点压进主标题（如「重新基期化后名义 +14% / 非油 +20%」）。

### 2.2 chrome minimalism

最大化数据 - 油墨比（Tufte 原则 + FT 实操）：

- 去 top / right spine
- **保留 bottom + left spine**（白底下需要可见横纵坐标）。FT 原版用 cream bg 配「无左 spine」，本项目用白底（嵌入 Quarto 白纸），恢复左 spine 提供视觉边界
- spine 颜色：axis 色（FT 暖深灰 `#66605C`，见 §5.3）
- 刻度线可见（white bg 上看得清）
- baseline（0 / 参考线，baseline 色）
- 网格仅 y 轴方向（FT 实际把 y 轴 tick line 拉满 plot 宽度形成横线），白底下略加深

### 2.3 single accent 原则

一张图**只允许一个数据元素用 accent 色突出**，其他元素全用 primary / neutral / tertiary。accent 用在「真正想让读者看的那个」。

反例：5 个柱用 5 个不同颜色，读者眼睛飘。正例：5 个柱全用 tertiary，最高那个用 accent，读者立刻知道你想强调谁。

FT 原话：「make sure the blue line is on top as this is the primary line colour」。

### 2.4 标题承担论点

- **标题写「事实 + 数字」**：「机构 A 与机构 B 的某增速在某年拐开 1.5 个百分点」「政策动作后名义 GDP +14%」
- 不写「X 国非油 GDP 增速」这种空泛标题
- 读者扫标题就能拿走主要 take-away，无需读图

### 2.5 数据 - 油墨比

- 5 ticks 优于 10 ticks（少而精）
- 整数优于小数（除非精度有意义）
- 网格极淡或省略
- 颜色饱和度低（饱和色让眼睛累）
- 不必要的标签 / 边框 / 阴影 / 渐变全删
- **不在柱间加变化率标签**（如「+14%」配箭头）。容易出错，且 FT 不这么做。变化率写进标题

---

## 三、图表制作规则

### 3.1 一图一脚本

每张图对应一个独立脚本，命名 `make_fig_<节号>_<编号>_<topic>.py`。

不允许「一节一脚本生成多图」。理由：

- 单图迭代时不必重跑整节
- 单图脚本 ≤ 150 行，可读
- 视觉问题定位精确
- 失败不连坐

例外：内容完全相同、仅参数不同的批量图（如各国分图）可合并到一个脚本循环出图。

### 3.2 共用样式模板（chart_template.py）

每个项目的 `heavy-research/scripts/chart_template.py` 是绘图样式 single source of truth。所有 `5_scripts/make_fig_*.py` 顶部 `import _path; from chart_template import setup_style, save_fig, PALETTE`（`_path.py` 见 §6.4）。保证字体、调色板、边距、网格、spine、字号、DPI、输出格式一致。**任何脚本不允许 override 这些样式**，除非用户明确批准。

接口契约见 §六。

### 3.3 PDF / JPG / clean-JPG 三输出 + 内容分离（核心）

三个输出**故意承载不同内容**，对应三种嵌入场景：

| 元素 | PDF 单图文件（裸图，给 qmd）| JPG（独立分发，自包含）| _clean.jpg（给 publication HTML）|
|---|---|---|---|
| 图表核心 | 是 | 是 | 是 |
| 标题（一级，承担论点）| 否（Quarto caption 提供）| 是。顶部 14pt 常规 text 色 | 否（HTML 模板提供）|
| 来源 | 否（`\begin{figsource}` 环境提供）| 是。底部 9pt「来源：...」 | 否（HTML `.exhibit-source` 提供）|
| 注 | 否（`\begin{figsource}` 环境提供）| 是。底部 9pt「注：...」 | 否（HTML `.exhibit-source` 提供）|
| 文件后缀 | `fig_*.pdf` | `fig_*.jpg` | `fig_*_clean.jpg` |

**关键纪律**：

- **单图 PDF 文件**（`6_figures/fig_*.pdf`）：永远是裸图。`chart_template.save_fig()` 不在 PDF 输出里嵌 title / source / note，避免与 Quarto caption 重复。**给 qmd 主报告嵌入**
- **qmd 渲染的研报 PDF**：每个 `![](fig.pdf)` 引用**必须紧跟 `\begin{figsource}` 环境**；每个表的 `: caption {#tbl-id}` 后**必须紧跟 `\begin{tblsource}` 环境**。环境内填 source + note，渲染为 10pt 灰度（见 §1.4）
- **JPG 独立分发**（`fig_*.jpg`）：自包含，title / source / note 一并嵌入，9pt 底部。**给公众号、社交分发等需要单图独立可读的场景**
- **_clean.jpg**（`fig_*_clean.jpg`）：与 PDF 同步落地的栅格版，无烧入。**专供 publication-style HTML 嵌入**——HTML 模板已经提供 `.exhibit-title` / `.exhibit-source`，再嵌带烧入的标准 JPG 会出现双标题
- **只有一级标题**，不要副标题。论点压进 title（如「重新基期化后名义 +14% / 非油 +20% / 油气 -5.7%」），符合 FT「标题承担论点」精神（§2.4）
- **三输出由 `save_fig()` 一次性产出**，调用方不需要关心；脚本作者写 `save_fig(fig, fig_id, title=..., source=..., note=...)` 一次，三个文件同时落地

**Quarto qmd 中的图引用范式**：

```markdown
![某指标 X 年与 Y 年对比](../6_figures/fig_1_1_topic.pdf){#fig-topic}

\begin{figsource}
来源：机构 A 年报 YYYY | 注：口径补充说明
\end{figsource}
```

**Quarto qmd 中的表引用范式**：

```markdown
| 指标 | 2016 | 2024 |
|---|---|---|
| 某指标 (%) | 19.3 | 35.85 |

: 某指标 2016 与 2024 对照 {#tbl-topic}

\begin{tblsource}
来源：机构 B 年度报告 YYYY Table 1 | 注：口径补充说明
\end{tblsource}
```

**为什么用 raw LaTeX 而不是 `:::` div**：Pandoc 的 div 类映射在 LaTeX 输出端对带连字符的类名（如 `.figure-source`）有 escape 问题，且不同 Quarto / Pandoc 版本行为不一致。raw LaTeX 环境 100% 可靠。

**渲染规则实现**（在 `_quarto.yml` 的 `include-in-header` 区加 LaTeX）：

```latex
% figure-source / table-source 环境 10pt 灰度（spec §1.4 + §3.3）
\usepackage{xcolor}
\definecolor{sourcegray}{gray}{0.4}
\newenvironment{figsource}
  {\par\smallskip\noindent\begingroup\fontsize{10pt}{12pt}\color{sourcegray}\selectfont}
  {\par\endgroup\medskip}
\newenvironment{tblsource}
  {\par\smallskip\noindent\begingroup\fontsize{10pt}{12pt}\color{sourcegray}\selectfont}
  {\par\endgroup\medskip}
```

**source / note 信息来自哪里**：直接 copy 自对应 `make_fig_*.py` 脚本里 `save_fig(source=..., note=...)` 的参数值。脚本里已写好的 source / note 字符串就是该图对外承认的来源 / 注。draft.qmd 写入 figure-source 块时**字符串与脚本保持一致**，不要在 qmd 里重写一遍（避免双源不一致）。

一份数据，三种用途。chart_template 管单图与 JPG，Quarto 管研报 PDF 内嵌，互不干扰。

### 3.4 图片内字体

- 中文字体 = 正文中文字体（如 Songti SC）
- 英文字体 = 正文英文字体（如 Times New Roman）
- 字号 ≥ 9pt（FT 印刷版下限），最大 ≤ 节标题字号

### 3.5 调色板

每个项目**先确定调色板再画图**（workflow 步骤 7 启动前定）。默认 FT 配色（完整 HEX + 语义见 §5.3）。

不允许任意配色，**不允许「大红配大绿」、彩虹色**。脚本不允许直接写颜色字符串，必须通过 `PALETTE` 接口引用。

### 3.6 图例语言一致性

- 整个报告主语言决定图例语言（中文研报 → 中文图例）
- 例外：固定专业缩写（IMF / OECD / OPEC / GCC / GDP / FY / WACC / 各国央行与统计局 / 主权基金的常用缩写）保留英文
- **图例不与数据元素重叠**

### 3.7 一图一 plot（禁止并列子图）（硬规则）

**`make_fig_*.py` 一律单 axes，禁止 `plt.subplots(1, 2, ...)` 等任何并列布局。**

**理由**：

- 并列子图带来一连串边缘问题：(a)(b) 子标题高度对齐、legend 不重叠某子图、双子图字号缩水、单边长 y-label 导致整体右移、(a)(b) 与 suptitle 视觉混乱
- 单图获得完整 `FIG_W = 6.69 inch` 横向宽度，aspect ratio 更舒展，10pt 字号无需压缩
- 派生（公众号 / Slack / 邮件）时每图独立分发，无需切割
- chart_template 简化：去掉 multi-subplot 分支、`TOP_PAD_PDF_MULTI_IN`、`SUBPLOT_TITLE_EXTRA_IN`，跨项目零边缘 case

**表达「并列对比」的替代方案**：

| 原来想用并列子图 | 单图替代 |
|---|---|
| 前 vs 后 / A vs B 同指标对比 | 分组柱（两色并列 bars）或时序双线 |
| 不同指标的并列展示 | 拆成两张独立图，正文用「下图 ... 上图 ...」串联 |
| 多区域 / 多国小多图 | 选最关键 1-2 国画明细图，其余进表格 |
| 饼图 + 散点等异型组合 | 拆成两张独立图，各占一段 |

**实现约束**：`save_fig` 检测到 `len(fig.axes) > 1` 时会打印 warning，规范上不允许，强行运行虽然能渲染但视觉风险自担。

### 3.8 元素不重叠（硬规则）

- 数据标签不与坐标轴 / 数据线 / 柱重叠
- **数据标签 / annotation 文字颜色不与其下方任何 plot 元素同色**。同色会让文字字符落在同色柱内时直接「消失」（实战教训：accent 色注释正好压在 accent 色目标柱顶部、文字看不见）。两种合法处置：① 把文字挪到柱外的空白区；② 文字改成 `PALETTE["text"]`（黑）等中性色
- **图例（legend）硬规则**（无例外，跨所有图统一）：
  - 不覆盖在 plot 区域上（不占用数据空间）。**禁止** `loc="upper right" / "upper left" / "lower right" / "lower left" / "center" / "best"` 等任何把 legend 放进 plot 内的写法
  - 不与数据线 / 柱 / 散点等图形元素重叠
  - 不放在 plot 下方（`bbox_to_anchor` 的 y 不允许为负值）
  - **必须水平排开（horizontal layout）**：`ncol` 取「图例项数」让所有项一行排开，**禁止**垂直堆叠。**ncol fallback**：若项的总宽估算 > image 宽（最宽项 × 项数 + spacing），一行装不下，退回 `ncol = ceil(N / 2)` 两行布局（避免 legend 被截）。判断很糙，先写 `ncol=N`，渲染发现溢出再降。实战案例：7 项 legend 含长项「市场驱动 (旅游 + 消费)」时，`ncol=7` 溢出右边，改 `ncol=4` 两行布局后正常
  - **摆位以「整张图片」为基准、不是 plot 中点**。两种合法模式：
    - ① **居中（默认）**：legend 中心落在 figure-x = 0.5（image center）。**不要**直接写 `bbox_to_anchor=(0.5, 1.02)`——那是 plot 中点，带长 y-tick label 的横向柱图里 plot 中点会偏右、legend 视觉上歪向右。便捷封装：`legend_above(ax, ncol=N, mode="centered")`，等价于 `ax.legend(loc="lower center", bbox_to_anchor=((0.5-pos.x0)/pos.width, 1.02), ncol=N, frameon=False)`（pos = ax.get_position()）
    - ② **image-left（centered 装不下时的回退）**：项数极多 / 一行太宽时，居中会让 legend 在两边都超界；image-left 让 legend 从 figure 最左边开始（含 y-axis labels 区，**不**从 plot 内的 x=0 开始），把所有可用横向空间让给 legend。便捷封装：`legend_above(ax, ncol=N, mode="image_left")`，等价于 `ax.legend(loc="lower left", bbox_to_anchor=(-pos.x0/pos.width, 1.02), ncol=N, frameon=False)`。**默认仍用 centered，只在 centered 真的装不下时退到这里**
  - **title 与 legend 之间留约一行空隙**：`save_fig` 自动检测 plot 顶端 legend（用 `leg.get_window_extent()` 量 legend 底沿是否 ≥ plot 顶沿），命中后 extra_top 自动 +`LEGEND_ABOVE_EXTRA_IN = 0.30 inch`，让 title 与 legend 视觉分离。**脚本作者无需手动调整**，照常调 `ax.legend(...)` 即可
- 双 Y 轴的两组数据用不同 marker / 线型，且 legend 标 RHS / LHS
- caption / 标题文字与轴 tick 不重叠

### 3.9 表格直接写在正文里

**表格用 markdown / Quarto 原生表语法写在 qmd / md 里**，不走图片管线。读者可 ctrl+F 搜、可复制，Quarto 渲染 PDF 时跨页也按表格语义处理。

不再提供 `save_table` 把表渲成 PDF/JPG 图片——失去 ctrl+F / 复制、视觉一致性也不是足够强的理由让表脱离正文流。

### 3.10 不可用元素

- 不用 ±、∓、≈、≤、≥ 等数学符号在图标题、轴标签、tick label（PDF 后端 mathtext 易报错）
- 不用 emoji
- 不用方框 / 特殊几何符号代替 1/2/3。直接写 1 / 2 / 3 或中文「一、二、三」

### 3.11 JPG 像素上限（硬规则）

**单张 JPG 长边 ≤ 2000px**。Anthropic API 多图请求对单张图有 2000px 长边硬上限，超过会拒绝整个对话。PDF 矢量不受此约束，本规则仅适用 JPG。

实现：`save_fig` 内部按 `dpi = min(200, floor(2000 / max(fig_w_in, fig_h_in)))` 动态计算 JPG 的 dpi。脚本作者不需要手算，调 `save_fig` 即可。

校验：开发期任何脚本生成 JPG 后可 `sips -g pixelWidth -g pixelHeight 6_figures/*.jpg` 抽检长边。任何超过 2000 视为 bug，回 `chart_template.py` 修。

### 3.12 Figure 宽度锁定 FIG_W（硬规则）

**所有 `make_fig_*.py` 必须用 `figsize=(FIG_W, h)`**——`FIG_W` 是 `chart_template.py` 导出的常量，值为 **6.69 inch**（= A4 21cm − 20mm × 2 边距）。高度 `h` 由作者按图型自由选（一般 3-4 inch）。

**为什么必须锁定**：Quarto 把 PDF 矢量图嵌入正文时按 `\textwidth` 缩放。如果 `figsize.width > 6.69`，整张图（含字号）被等比缩小。matplotlib 里 10pt 字号到 PDF 上变 6-7pt，跟 §5.2 规范不符。锁定 `figsize.width = FIG_W = 6.69`，缩放比 = 1.0，**matplotlib rcParams 字号即 PDF 实际字号**。

**正例**：

```python
import _path  # noqa: F401
from chart_template import setup_style, save_fig, PALETTE, FIG_W

setup_style()
fig, ax = plt.subplots(figsize=(FIG_W, 3.5))
```

**反例**：`figsize=(10, 5)` / `figsize=(11, 4.8)` 等任何手写宽度。即使临时调试也不行——会在脚本里留下隐性 bug，下一次重渲染发现字号缩水。

**高度参考值**：

| 图型 | 推荐 h |
|---|---|
| 单子图柱 / 折线 | 3.0 - 3.5 |
| 双子图横排 | 3.0 - 3.5 |
| 时间线 / 多层结构图 | 3.5 - 4.5 |
| 信息密集的四象限 / 热力图 | 3.5 - 4.0 |

**subplots_adjust(left=…) 经验值**（带长 y-tick label 的横向柱图必须手动调，否则 label 被左边距切掉）：

| y-tick label 最长字符数 | 推荐 left |
|---|---|
| ≤ 3 字（"2024"、"日本"）| 0.10（默认，不用调）|
| 4-5 字（"建筑业"、"批零餐饮"）| 0.20 |
| 6-10 字（"教育与医疗"、"某基金 AUM USD Bn"）| 0.22-0.28 |
| 11+ 字 / 长英文项目名 | 0.30-0.34 |

调到刚好包住最长 label + 一字呼吸空间为止。**自检**：渲染后看 JPG 最左边的 y-tick label 是否完整（实战调试：从 0.22 开始切掉某 label 前缀，调到 0.34 才全显示）。

**PDF / JPG 尺寸关系**：

| 输出 | 宽 | 高 |
|---|---|---|
| 调用方 figsize | `FIG_W = 6.69` | `h`（脚本指定）|
| **PDF 输出** | `~6.4-6.7`（受 `bbox_inches='tight'` 影响略小于 6.69）| `~h ± 装饰` |
| **JPG 输出** | `FIG_W + 2 × 0.30 = 7.29` | `h + extra_top + extra_bottom`（按 suptitle / source / note 实际行数加高）|

**Plot 主体绝对尺寸在 PDF 与 JPG 中完全一致**——JPG 只是把 plot 整体右移 0.30 inch、下移 `extra_bottom`，不压缩。这一约束让脚本作者控制 plot 的 aspect ratio（`figsize=(FIG_W, h)` 里 h 决定 plot 长宽比），JPG 的额外尺寸由 save_fig 按内容自动算。

### 3.13 写图脚本自检 4 项

每个新写或修改的 `make_fig_*.py` 在 commit 前必须自检以下 4 项，不通过的修脚本后重渲再提交。这 4 项是跨项目反复踩过的高频坑点，**不属于视觉检查**（视觉检查见 §四，AI 不做），而是脚本逻辑一致性 self-check。

| 红线 | 应为 |
|---|---|
| title 引用的数字与图内数据一致 | title 引用具体数字时，现场用 `df.loc[...].max()` 或 `argmax()` 等 f-string 插入，不要凭印象写；可选 `assert` fail-safe |
| 数据标签 / annotation 颜色不与其下方 plot 元素同色 | accent 文字落在 accent 柱内会消失。annotation 默认走 text 色，accent 数据标签放白色或对比色 |
| 横向柱图 y-tick label 完整显示 | 长 label 必须配 `subplots_adjust(left=...)`，经验值表见 §3.12 |
| Legend 居中且水平排开 | 用 `legend_above(ax, ncol=N, mode="centered")`；ncol=N 装不下时回退 `ncol=ceil(N/2)` 两行 |

视觉自查仍由用户做，见 §四。

---

## 四、视觉检查

**AI 不做视觉检查**。图渲染完后 AI 仅列出 JPG / PDF 路径，用户自己开来看。原因：① AI 视觉模型对中文字体识别不稳定会误判；② 多张图累积会触发 API 多图像素上限（见 §3.11）；③ 用户审美与论点强调点比 AI 准。

不设 checklist 与硬停 gate。用户判定有问题再回退到具体脚本修。

---

## 五、默认值与模板

### 5.1 Quarto YAML 标准头（中文研报）

项目级 `_quarto.yml`：

```yaml
lang: zh
format:
  # 10b Word docx 派生 (workflow §步骤 10b)：default 用 Pandoc 风格化模板即可，
  # 如需项目品牌 Word 模板（字体 / 页眉 / 页脚），加：
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
        % === 字体 ===
        \usepackage{fontspec}
        \setmainfont{Times New Roman}
        \setCJKmainfont{Songti SC}
        \newfontfamily\arabicfont[Script=Arabic]{Noto Sans Arabic}

        % === 段首 / 段间距（见 §1.5）===
        \setlength{\parindent}{0pt}
        \setlength{\parskip}{0.5em}

        % === 字号 6 档强制对齐（18 / 16 / 14 / 12 / 11 / 10 pt，见 §1.4）===
        % 主标题 18pt 加粗，副标题 16pt 常规，作者 / 日期 11pt
        \usepackage{titling}
        % \droptitle 控制主标题距页顶的距离；不能用 \pretitle{\vskip ...} 因为
        % 页顶的 \vskip 会被 TeX 默认丢弃（vmode + 页起始处 glue 自动消化）
        \setlength{\droptitle}{4em}
        \pretitle{\begin{center}\fontsize{18}{22}\bfseries\selectfont}
        \posttitle{\par\end{center}\vskip 2em}
        \preauthor{\begin{center}\fontsize{11}{14}\selectfont}
        \postauthor{\par\end{center}}
        \predate{\begin{center}\fontsize{11}{14}\selectfont}
        \postdate{\par\end{center}\vskip 2em}
        % 覆盖 Quarto/pandoc 默认 \subtitle（默认 \large ≈ 12pt 会降字号）
        % \makeatletter 包必要，因 \@title 含 @ 需 letter catcode
        \usepackage{etoolbox}
        \makeatletter
        \providecommand{\subtitle}[1]{%
          \apptocmd{\@title}{\par\medskip {\normalfont\fontsize{16}{20}\selectfont #1 \par}}{}{}%
        }
        \makeatother

        % h1 节标题 14pt 加粗，h2 小节标题 12pt 加粗
        \usepackage{titlesec}
        \titleformat{\section}{\fontsize{14}{17}\bfseries\selectfont}{\thesection}{1em}{}
        \titleformat{\subsection}{\fontsize{12}{15}\bfseries\selectfont}{\thesubsection}{1em}{}

        % 目录 / 图目录 / 表目录：标题 14pt 加粗居中，条目 11pt 常规
        % 实现：直接覆盖 \@cftmake?title 三个 hook，用 \begin{center}...\end{center}
        % 包裹标题。理由：tocloft 自带的 \hfill 居中法在 article 模式 + 标题
        % 接在前文段落（如摘要）之后时不可靠，常偏移到右侧
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
        % 强制换页（§1.7 / §1.8）：
        % - 目录前 \clearpage（让目录独立成页，不接在摘要后）
        % - 图索引前 \clearpage（防标题孤立到上一页底部）
        % - 表索引前 \clearpage（同上）
        % - 表索引后 \clearpage（进入正文前）
        % 注意：tocloft 在 \AtBeginDocument 里重定义 \tableofcontents / \listoffigures
        % / \listoftables，所以 patch 必须也包在 \AtBeginDocument 中且在 tocloft 注册
        % 之后才生效
        \AtBeginDocument{%
          \pretocmd{\tableofcontents}{\clearpage}{}{}%
          \pretocmd{\listoffigures}{\clearpage}{}{}%
          \pretocmd{\listoftables}{\clearpage}{}{}%
          \apptocmd{\listoftables}{\clearpage}{}{}%
        }

        % 全文无页眉，页尾居中页码（§1.11）
        % 覆盖 ctex chinese-article scheme 默认的 \pagestyle{headings}
        \pagestyle{plain}

        % 摘要：标题 14pt 加粗居中（与目录/图目录/表目录标题同档），正文 11pt 常规
        \renewenvironment{abstract}
          {\par\medskip{\centering\fontsize{14}{17}\bfseries\selectfont 摘要\par}\medskip\normalsize}
          {\par\medskip}

        % 图 / 表 caption 11pt italic
        \usepackage{caption}
        \captionsetup{font={normalsize,it},labelfont={normalsize,bf,it}}

        % 脚注 11pt（覆盖 LaTeX 默认 \footnotesize=9pt）
        \renewcommand\footnotesize{\fontsize{11}{14}\selectfont}
execute:
  echo: false
  warning: false
  message: false
  freeze: auto
```

非中文项目按需替换 CJK 字体段、`documentclass`、`lang`。字号 4 档强制覆盖见 §1.4 表与 LaTeX 头注释。

### 5.2 图表内字号（chart_template 速查）

文档版式字号见 §1.4，不在本节重复。本节**仅列图表 JPG 内自含元素**，真值由 `chart_template.setup_style()` 设置。

图内**仅两档字号**：12pt suptitle + 10pt 其它所有元素。简化层级，避免图内文字层次过多导致视觉碎片化。

| 元素 | 中文 | 英文 | 字号 | 字重 | 颜色（见 §5.3）|
|---|---|---|---|---|---|
| 图标题（JPG 内，suptitle）| Songti SC | Times New Roman | 12pt | **常规**（FT） | text |
| 图内数据标签 / 强调注 | Songti SC | Times New Roman | 10pt | 常规 | text |
| 轴文字 / 图例 / tick | Songti SC | Times New Roman | 10pt | 常规 | text_light |
| 图内表体 | Songti SC | Times New Roman | 10pt | 常规 | text |
| 图内表头 | Songti SC | Times New Roman | 10pt | 加粗 | text |
| 图内来源 / 注 | Songti SC | Times New Roman | 10pt | 常规 italic | text_light |

**字号对齐文档版式**：图标题 12pt = h2 小节标题；图内其它所有 10pt 与正文 11pt 拉开一档，避免图嵌入正文时图字喧宾夺主。中英文字体与正文严格一致。

**对齐与排版细节**（save_fig 实现，§6.3）：

- **三文本左对齐 PDF 左边缘**：title / 来源 / 注统一 `x_frac = JPG_HMARGIN_IN / fig_w_jpg`，即 JPG 中「PDF 原本左边界」位置。这条线 = 图最左可见内容（y-label 最左字）。可用宽度 = `fig_w_pdf = 6.69 inch`（PDF 整宽，覆盖 y-label 区 + plot 数据区），文字 wrap 到 PDF 右边缘
- **JPG 左右各加 `JPG_HMARGIN_IN = 0.30 inch` 白边距**：JPG 总宽 = PDF 宽 + 2 × 0.30 = 7.29 inch。plot 在 JPG 中相对 PDF 整体右移 0.30 inch，绝对尺寸不变
- **精确像素 wrap**（`_wrap_text_precise`）：用 matplotlib 渲染候选字串、量真实像素宽度，二分查找装得下的最长前缀。**唯一断行约束**是英文单词 / 数字不可拆两半（保护字符集 `[A-Za-z0-9.,%+\-]`）。中文字符可在任意位置断。**不再用字数估算 + 标点回断**——精确测量 + 仅词内保护，文字装到几乎贴 PDF 右边才换行
- **续行悬挂缩进**：来源 / 注 wrap 到第二行时，用全角空格缩进 3 格（来源）/ 2 格（注），让续行对齐到「来源：」「注：」后的第一字位置
- **plot 底 ↔ 来源之间多 1 行空白**（含在 save_fig 的常量 `PLOT_BOTTOM_GAP_IN = 0.45` 里）。一图一 plot 后不再需要为 (a)(b) 子标题预留额外顶部空间

ctexart 已默认 11pt + 中文标点压缩。**首段缩进被 §5.1 显式覆盖为零**，改用半行段间距分段（见 §1.5）。

### 5.3 调色板（FT 配色快查表）

**真值在 `chart_template.PALETTE` dict**。本表是 FT chart-doctor 默认值的人工速查，**项目级若覆盖 HEX 时，本表会与 code 漂移；以 code 为准**。

| 接口名 | HEX（FT 默认）| 用途 |
|---|---|---|
| `primary` | `#0F5499` Oxford blue | 数据序列主色 / 当前主体 |
| `secondary` | `#208FCE` Medium blue | 数据序列副色 / 对照 / 历史 |
| `tertiary` | `#C2B7AF` Warm gray | 数据序列弱化 / 第三组 / 背景柱 |
| `accent` | `#7F062E` Claret | **单点突出**（single accent 原则，§2.3）|
| `accent_alt` | `#EB5E8D` Warm pink | 备选 accent |
| `accent_light` | `#FCE2D1` Claret 浅化 | 表格 highlight 行底 |
| `neutral` | `#66605C` Warm dark gray | 参考线 / 平均值 |
| `grid` | `#D6D0CA` 浅暖灰 | y 轴横向网格线 |
| `axis` | `#66605C` 暖深灰 | 横纵坐标 spine + tick |
| `baseline` | `#999999` 中性灰 | 0 / 参考线 |
| `bg` | `#FFFFFF` 白 | 图表背景（嵌入 Quarto 白纸 PDF） |
| `text` | `#000000` 黑 | 主文字（标题） |
| `text_light` | `#66605C` 暖深灰 | 副文字（轴 label / 来源 / 注 / legend） |

多系列扩展 `PALETTE_EXTENDED` 7 色（按 FT categorical_line 顺序）+ 单色递进 `PALETTE_SEQUENTIAL` 7 色，HEX 直接读 `chart_template.py`。

接口名 `PALETTE` 跨项目保留。HEX 值可项目覆盖（需在项目级 CLAUDE.md「与框架的偏离」段登记理由），脚本**不允许直接写颜色字符串**，必须通过 `PALETTE['xxx']` 引用。

---

## 六、chart_template 接口契约

实现见同目录 `chart_template.py`。本节只讲「外部脚本怎么调」。脚本编写者只需读本节，不必读 chart_template 源码。

### 6.1 `setup_style()`

无参数。每个绘图脚本顶部调用一次，配置 matplotlib 全局 rcParams（字体、颜色、spine、网格、线宽、tick、legend、输出 dpi 等）。

```python
import _path  # noqa: F401  -- 见 §6.4
from chart_template import setup_style
setup_style()
```

### 6.2 `PALETTE` / `PALETTE_EXTENDED` / `PALETTE_SEQUENTIAL`

dict / list。颜色引用必须经此接口，不允许在脚本里硬写 HEX。

```python
from chart_template import PALETTE
ax.bar(x, y, color=PALETTE["primary"])
ax.axhline(0, color=PALETTE["baseline"])
```

另外两个常量也从 `chart_template` 导出：

- `FIG_W = 6.69`（float, inch）：所有 `make_fig_*.py` 的 figsize 宽度必须用此常量，详见 §3.12
- `DATA_PROC`（Path）：指向 `4_data/2_processed/`，避免脚本里硬写相对路径

### 6.3 `save_fig(fig, fig_id, title=None, source=None, note=None, subdir="")`

PDF（裸图，给 qmd）+ JPG（带烧入，独立分发）+ `_clean.jpg`（裸图栅格，给 publication-style HTML）三输出。一次调用全部落地。

| 参数 | 类型 | 说明 |
|---|---|---|
| `fig` | matplotlib Figure | 调用方组装好的 figure |
| `fig_id` | str | 文件名前缀，如 `"fig_1_1_topic"` |
| `title` | str / None | JPG 顶部一级标题；PDF 不写 |
| `source` | str / None | JPG 底部「来源：...」单独一行；PDF 不写 |
| `note` | str / None | JPG 底部「注：...」单独一行（来源下方）；PDF 不写 |
| `subdir` | str | 子目录（默认直接落 `6_figures/`） |

行为保证：

- **PDF 用调用方 figsize**（`figsize=(FIG_W, h)`），保留 plot + 必要轴装饰 + 上方 / 下方 legend，**不画** suptitle / 来源 / 注（这些由 Quarto caption + `{.figure-source}` 块在 qmd 中提供）。一图一 plot 后无 (a)(b) 子标题
- **PDF 顶部 padding 统一 0.10 inch**。一图一 plot（§3.7）后无 (a)(b) 子标题，不需要额外顶部预留
- **PDF 用 `bbox_inches='tight'` 保存**：自动扩到包含所有可见内容（如 plot 下方 legend、长 y-label）。代价是 PDF 实际尺寸可能比 `figsize` 略小，Quarto 嵌入时按 textwidth 缩放（约 5% 放大），字号也对应放大。这是为了保证「legend in plot bottom」一类图的 legend 不被裁切而做的取舍
- **JPG 三向扩展**：`figsize=(fig_w_pdf + 2 × JPG_HMARGIN_IN, fig_h_pdf + extra_top + extra_bottom)`，其中 `JPG_HMARGIN_IN = 0.30 inch` 是左右白边距，`extra_top` 容纳 suptitle 区，`extra_bottom` 容纳 source / note 区。**plot 主体绝对尺寸与 PDF 完全一致**——save_fig 通过 `fig.set_size_inches` + `subplots_adjust` 把 plot 整体右移、下移而非压缩
- **三个文本左对齐 PDF 左边缘，右边 wrap 到 PDF 右边缘**：title / 来源 / 注 全部 `x_frac = JPG_HMARGIN_IN / fig_w_jpg`（= JPG 中 PDF 左边界），可用宽度 = `fig_w_pdf`（覆盖 y-label 区 + plot 数据区）。文字框跟图最左 / 最右对齐
- **精确像素 wrap**：`_wrap_text_precise` 用 matplotlib 渲染候选文字、量真实像素宽度，二分查找装得下的最长前缀；**唯一断行约束**是英文单词 / 数字不可拆两半（保护 `[A-Za-z0-9.,%+\-]`）。中文字符可在任意位置断。续行悬挂缩进（来源 3 全角空格、注 2 全角空格）对齐到「来源：」「注：」后第一字位置
- 这样设计的理由：① 脚本作者只关心 plot 本身的 aspect ratio（写 `figsize=(FIG_W, 3.5)` 就是想 plot 长这样），suptitle / source / note 的纵向空间由 save_fig 按内容动态加高，不压扁 plot；② 三文本对齐 PDF 边线，视觉框定一致；③ 精确 wrap 避免字数估算的右锯齿，文字尽量装满 PDF 整宽才换行
- JPG 长边自动 ≤ 2000px（§3.11 硬规则）。在 fig_w_jpg ≈ 7.3 inch + dpi 动态计算下，长边 ~2000px 接近上限
- **`_clean.jpg` 在 PDF 落地之后、JPG 加文本之前一起保存**：用 PDF 此时的 figsize + `bbox_inches='tight'` + `dpi=200` + 白底。`FIG_W=6.69` 下约 1338px 宽，远低于 2000px 上限。供 publication-style HTML 直接 `<img src>` 嵌入

### 6.4 调用模板

每个 `5_scripts/make_fig_*.py` 顶部样板：

```python
"""make_fig_<节号>_<编号>_<topic>.py · <一句话用途>

输入：4_data/2_processed/<src>.csv
输出：6_figures/<fig_id>.{pdf,jpg} + <fig_id>_clean.jpg
"""
import pandas as pd
import matplotlib.pyplot as plt
import _path  # noqa: F401  -- 把 heavy-research/scripts/ 加进 sys.path
from chart_template import setup_style, save_fig, PALETTE, FIG_W, DATA_PROC

setup_style()


def main():
    df = pd.read_csv(DATA_PROC / "<src>.csv")
    # 宽度必须锁定 FIG_W（详见 §3.12）；高度按图型自由选，参考表见 §3.12
    fig, ax = plt.subplots(figsize=(FIG_W, 3.5))
    ax.bar(df["x"], df["y"], color=PALETTE["primary"])
    save_fig(fig, "fig_1_1_topic",
             title="<事实 + 数字承担论点>",
             source="<机构 + 年份 + 报告名>",
             note="<可选>")
    plt.close(fig)


if __name__ == "__main__":
    main()
```

**`_path.py` 必备**：路径见 `5_scripts/_path.py`，内容 4 行：

```python
"""把 heavy-research/scripts/ 加进 sys.path，让 5_scripts/ 的脚本能 import chart_template。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "heavy-research" / "scripts"))
```

新项目脚手架阶段必须先建 `5_scripts/_path.py` 才能 import `chart_template`。

---

## 七、publication-style HTML 派生稿（步骤 10 可选派生）

主报告 qmd → PDF 走完后，可选择再做一份「consulting / FT 长稿风格」的 HTML → PDF，用于公众号长稿、客户分发、社交分享等需要更强视觉识别的场景。本节是该 HTML 模板的**规范**。skill 自带一份中性长稿风格的 HTML template 在 `scripts/publication-style-template.html`，下方所有规范都以此 template 为参照实现。

### 7.1 什么时候做、什么时候不做

**做的条件**：

- 主报告已经走完步骤 9（用户已 sign off）
- 内容相对稳定，预期不再大改
- 受众或场景需要更强视觉识别（咨询风、杂志风、社交分享）

**不要做的情况**：

- 内容还在变（HTML 与 qmd 双源同步是隐性负担）
- 时间紧或不必要时
- 主报告 PDF 已满足受众期待

**重要原则**：

- **qmd 是真相之源**。HTML 是派生品，内容从已签字的 qmd 抄过来，不在 HTML 上做内容修订
- **HTML 模板不再用 builder 脚本反复重生成**。一次生成后转为手工维护，builder 脚本写完用过即删，避免重渲覆盖手工调整

**模板起点（两种路径）**：

- **路径 A（default，推荐）**：skill 自带的 `scripts/publication-style-template.html` 是中性长稿风格的 ready-to-use 模板。step 10c 启动时把它拷到项目 `8_publication/2_HTML/<project>-publication-style.html`，按 §7.8 内容映射表填充各 page 内容，按 §7.3 在 VS Code Live Preview 里手动调段
- **路径 B（替代风格）**：若要其他咨询风格的视觉差异化（如 BCG 绿色调、McKinsey 蓝调、Bain 红调等），可选调 `consulting-report-style` skill 生成替代模板，再按 §七 各子节微调（1 div = 1 A4、`_clean.jpg` 嵌入、页脚进 HTML 等纪律对所有风格通用）

skill 自带 template 仅一份，目的是「ready-to-use 的起点 + 风格参照实现」。不维护多套风格在 skill 内部。

### 7.2 核心模型：1 div = 1 A4 page（WYSIWYG）

HTML → PDF 链路的核心纪律是 **「所见即所得」**：浏览器里 HTML 长什么样，PDF 里就长什么样，PDF 转换器不再叠加任何视觉元素。

- 每个 `<div class="page">` 物理上就是一张 A4：`width: 210mm; height: 297mm; overflow: hidden`
- `@page { size: 210mm 297mm; margin: 0; }` 锁定 PDF 页面尺寸
- 页脚 / 页码 **必须放进 HTML 自己的 `<div class="page-footer">`**，不要用 `@page { @bottom-* }` 让 Chrome 在 PDF 阶段叠加
- 页码用 CSS counter（`counter-reset: pagenum`/`counter-increment: pagenum`/`::before { content: counter(pagenum) }`），自动递增，封面和封底跳过
- 浏览器手动保存 PDF 时（§7.6）必须关掉打印对话框的「页眉与页脚」选项，禁止浏览器自加

**铁律**：任何视觉 / 版面调整 → 改 HTML → 浏览器立刻见。**绝不在 PDF 转换脚本里加视觉逻辑**——脚本职责仅是「转格式」。

### 7.3 内容溢出的处理

固定高度 page div 没有自动分页，内容超界或留白都需要手动调。**没有可靠的自动重排办法**（paged.js 会改变页面模型且与 Chromium `--print-to-pdf` 偶有不一致，引入 JS 依赖不值）。

**操作流程**：

1. VS Code 装 **Live Preview** 扩展（`ms-vscode.live-server`），打开 HTML 右上角点「Open Preview to the Side」（`Cmd+Shift+V`），左边改代码 / 右边浏览器实时刷新
2. 浏览器里逐页看：哪页超界、哪页留白
3. VS Code 里 `Cmd+F` 搜该页特征文字，定位到对应 `<div class="page body-page">`
4. **剪一段 `<p>` 或 `<figure>` 到下一页开头**（或反向把下一页开头的段抽到本页末尾）
5. 保存 → 浏览器刷新 → 重新看
6. **从前往后扫**：前页改完会影响后页的拥挤度，按页序连锁推平一次定型

不推荐 WYSIWYG HTML 编辑器（如 BlueGriffon）：它们会重写你的 class 结构。**纯文本编辑器 + 浏览器预览**对这种自定义 CSS 模板最稳。

### 7.4 图表嵌入：用 `_clean.jpg` 不用 `.jpg`

publication-style HTML 模板自己提供 `.exhibit-title` / `.exhibit-source` 区块。**必须用 `fig_*_clean.jpg`**——`fig_*.jpg` 已经把 title / source 烧进去，再嵌会出现「双标题 + 双来源」。

```html
<figure class="exhibit">
  <div class="exhibit-label">Exhibit 1</div>
  <div class="exhibit-title">由 HTML 模板提供的标题</div>
  <div class="exhibit-figure">
    <img src="../../6_figures/fig_1_1_topic_clean.jpg" alt="...">
  </div>
  <div class="exhibit-source"><strong>来源：</strong>...</div>
</figure>
```

`_clean.jpg` 由 `chart_template.save_fig()` 自动产出（§3.3 / §6.3），脚本作者不需要额外操作。

### 7.5 封面 / 章节扉页 / 作者头像

- **封面**：full-bleed gradient / photo bg + 标题大字 + 副标题 + 日期；accent bar 右下角，建议放在「独立研究报告」类 corner-mark 上方
- **章节扉页**：banner 区放章中文 label（如「第一章」42pt）+ 英文 small-caps（「CHAPTER ONE」9pt）。不要在正文 body 里重复出现章号，banner 已经承担识别
- **作者头像**：本地放一张 `Gen.jpg`（或 author name），CSS `<img>` 嵌入 `.author-headshot { border-radius: 50% }` 圆形剪裁。压到 1MB 以内（建议长边 ≤ 1200px）
- **头像构图陷阱**：1:1 容器配 1:1 图时 CSS `object-fit` 无可裁剪空间。如果原图额头偏高被圆形剪掉，用 PIL 在图顶部加白边把脸下推：
  ```python
  from PIL import Image
  im = Image.open('Gen.jpg')
  new = Image.new('RGB', (im.width, im.height + 140), 'white')
  new.paste(im, (0, 140))
  new.save('Gen.jpg', 'JPEG', quality=85)
  ```

### 7.6 HTML → PDF 转换

直接在浏览器里手动保存即可，不要写脚本。Chrome 或 Safari 打开 HTML，Cmd+P 调出打印对话框，目标改「另存为 PDF」，关掉「页眉与页脚」，边距设「无」，保存到 `8_publication/2_HTML/`。配合 §7.2「页码进 HTML」与 §7.5「页脚 div」一起达到 WYSIWYG。

手动保存的好处是零配置、零环境依赖，单次出版用最稳。命令行渲染器（headless Chrome `--print-to-pdf` / prince / weasyprint 等）只有在需要批量自动化或 CI 集成时才值得引入，首次出版不要走这条路。

### 7.7 目录约定

publication-style HTML + PDF 落在 `8_publication/2_HTML/`。三子目录按生成顺序编号：

```
8_publication/
├── 1_word/                             10b Word docx 派生
│   └── <project>.docx                  Pandoc 自动生成，给客户审阅或批注
├── 2_HTML/                             10c publication-style HTML + PDF
│   ├── <project>-publication-style.html
│   ├── <project>-publication-style.pdf
│   └── author.jpg                      作者头像（skill 自带 placeholder，按 §7.5 替换）
└── 3_wechat_pages/                     10d 公众号 JPG 切页（10c PDF 切逐页）
    ├── page_01.jpg
    └── ...
```

**主报告 PDF 不放在此目录**：qmd 渲染产出的 `draft.pdf` 留在 `7_draft/` 直接查看分发，避免双份维护。冻结版本号通过 git tag 或文件名后缀（`draft_v3.pdf`）管理。

**铁律**：不要在 `2_HTML/` 留下 builder 脚本。一次性生成后转为手工维护，重复运行 builder 会覆盖手工调整。

### 7.8 内容映射：qmd 主报告 → publication HTML

参考 `workflow.md §九`（派生产出转换表）。HTML 模板需要额外承担：

| 元素 | HTML 模板里怎么写 |
|---|---|
| 章节扉页大字 | `.chapter-opener .banner .ch-label` |
| 章节英文 small-caps | `.chapter-opener .banner .ch-label-en` |
| Pull quote | `<div class="pull-quote">` |
| Exhibit 编号 | `<div class="exhibit-label">Exhibit N</div>` |
| 摘要页 | `.page.abstract` + eyebrow + accent-bar + h2 + body |
| 目录页 | `.page.contents` + `.toc-list` |
| 参考文献页 | `.page.references` + `.references-list` 用 hanging indent（`padding-left: 34mm; text-indent: -34mm`），ref-key 固定宽度 32mm 避免长 key 换行换错位 |
| 作者页 | `.page.authors` + author-card flex 布局 + 本地头像 img |
| 封面 / 封底 | `.page.cover` / `.page.back-cover`，全屏 padding: 0 |

**章节扉页类（abstract / contents / references / authors）的 h2 文本规则**：用 **plain section name**（如「摘要」「本期内容」「参考文献」「关于作者」），不用提炼性 hook 句。

- 反例：`<h2>三层会计加工叠加，让账面成就在叙事层面被系统性放大</h2>`
- 正例：`<h2>摘要</h2>`
- 原因：提炼性 hook 与 eyebrow（`ABSTRACT · 摘要`）功能重叠且抢夺正文焦点；plain section name 保留 h2 的视觉锚点（首行 30+pt 大字）作为页面结构定位，hook 应留给正文首句或 pull-quote 承担

### 7.9 公众号 JPG 切页（可选派生）

publication-style PDF 渲完后，公众号长稿渠道可把 PDF 切成逐页 JPG（公众号编辑器原生支持图序，不直接吃 PDF）。落 `8_publication/3_wechat_pages/`，命名 `page_NN.jpg`（zero-pad 两位数）。

具体切页工具与 DPI 由用户按场景定（常用 200 DPI 即可，公众号正文图宽自适应，对长边像素不敏感）。常见命令行选项：`pdftoppm -jpeg -r 200 input.pdf page` 或 macOS Automator 的「Render PDF Pages as Images」动作。

只在公众号长稿渠道需要时做，主报告 PDF 本身已分页，不需要这层派生。
