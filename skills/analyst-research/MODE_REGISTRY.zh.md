# Mode Registry · analyst-research（中文镜像）

> 英文主文件为 `MODE_REGISTRY.md`。三档 mode 的单一真相之源。SKILL.md、workflow.md、CHANGELOG 及下游工具都引用本文件。**mode 参数变更时先改本文件，再传播。**

---

## Mode 表

| 维度 | light | medium | heavy |
|---|---|---|---|
| **一句话定位** | 4-5 页决策备忘 | 12-15 页主题分析 | 30-40 页 / 1.5 万字+ 旗舰报告 |
| **篇幅** | 4-5 页（< 4 视为过薄，需补充） | 12-15 页（< 12 偏薄） | 30-40 页 / 1.5 万字+ |
| **图表数** | 0 | 6-10 | 25-35+ |
| **时间预算** | 约 15 分钟 | 约 1 小时 | 约 2-3 小时 |
| **LLM** | 单（Claude solo） | 单（Claude solo） | 单或多 LLM（可选 Claude + GPT critique） |
| **工作流步数** | 6 | 8 | 11 |
| **硬停** | 0（仅软停） | 1（draft 后 sign-off） | 3（outline / draft / final） |
| **引用方式** | Markdown 脚注（`^[机构, 标题, 日期. URL.]`） | Markdown 脚注（heavy 排期则可 .bib） | BibTeX（`references.bib`）+ APA via Quarto |
| **PDF 派生** | ✅ | ✅ | ✅ |
| **Word 派生** | ✅ | ✅ | ✅ |
| **公众号 md 派生** | ❌ | ❌ | ✅ |
| **HTML publication 派生** | ❌ | ❌ | ✅ |
| **脚手架深度** | 最小（4 文件） | 中（`5_scripts/_path.py` + 编号目录） | 完整 10 编号目录 + 本地 skill 副本 |
| **图模板** | n/a（无图） | 共用 `chart_template.py` | 共用 `chart_template.py` |
| **onboarding 问题数** | 2（hypothesis + 报告语言） | 3-5（hypothesis + 受众 + 可选硬停 + 调色板 + 报告语言） | 4（报告语言 + 多 LLM + Quarto 复用 + 话题） |

## 各 mode 文件依赖

| Mode | 工作流文件 | Quarto 模板 | spec 文件 | scripts |
|---|---|---|---|---|
| light | `references/workflow_light.md` | `references/_quarto-light.yml` | n/a（无图） | n/a |
| medium | `references/workflow_medium.md` | `references/_quarto-medium.yml` | `references/report_style_spec.md` | `scripts/chart_template.py` |
| heavy | `references/workflow_heavy.md` | spec §5.1（无独立 `.yml`） | `references/report_style_spec.md` | `scripts/{chart_template.py, publication-style-template.html, author.jpg}` |

## 使用场景（触发匹配）

| 用户信号 | 选 |
|---|---|
| 「5 页 memo」「exec brief」「1 小时简报」「决策摘要」「内部 memo」 | **light** |
| 「主题分析」「半天 brief」「12 页报告」「带数据的 board memo」「半天分析」 | **medium** |
| 「旗舰报告」「长篇研究」「行业深度」「政策评估」「投研报告」「深度报告」「长篇综述」 | **heavy** |

## 反匹配（不触发本 skill）

| 用户信号 | 改用 |
|---|---|
| 单条新闻评论 | `market-research-skills:topic-brief` |
| Slide deck / PPT | `deckster-slide-generator` |
| 一次性快问快答（无书面报告） | 直接答，不用 skill |
| 纯文学或营销文案 | 非本 skill 领域 |
| 只有工具脚本、无报告产出 | 非本 skill 领域 |

## 升降档路径

`light` 项目超出 scope 就重新以 `medium` 触发 —— 三档共用 **hypothesis lock 第一步**，早期工作可迁移。`medium → heavy` 同理。降档（`heavy → medium`）通常不值得，砍交付物而非重跑。

## 各 mode 复盘段

项目结案后跑 mode 专属复盘规则：

| Mode | 复盘段 |
|---|---|
| light | `workflow_light.md §6` |
| medium | `workflow_medium.md §8` |
| heavy | `workflow_heavy.md §9` |

每个复盘决定哪些项目经验上溯回 skill 本身（skill 版本化）。

## 何时修订本 registry

满足任一时编辑本文件（并 bump skill minor 版本）：

- 某 mode 的硬停数变化
- 某 mode 增删派生形态
- 某 mode 的工作流文件被拆 / 并 / 重命名
- 引入新 mode

编辑后传播顺序：
1. **MODE_REGISTRY.md / .zh.md**（本文件）—— 改真相之源
2. **SKILL.md / SKILL.zh.md**「Mode 速查对照」表 —— 重新同步
3. **CHANGELOG.md** —— 记 registry 变更
4. **workflow.md / .zh.md**（路由）—— mode 数或命名变了就更新路由指针
5. **README.md**（顶层）—— 用户可见描述变了就更新
