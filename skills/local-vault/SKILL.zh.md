# local-vault（中文参考）

> 本文件是 SKILL.md 的中文参考，**不被加载**；canonical 以 SKILL.md（英文）为准。

把一堆原始文件转成一个 LLM 能 grep 的 **Markdown vault**,再负责任地基于这个 vault 回答问题。

**心智模型**:`SOURCE` = 原始文件(source of truth);`VAULT` = 每个原始文件对应一个 `.md`,带检索 frontmatter(abstract / tags / synonyms)+ `source` 双链回原文。vault 是 LLM 读的层,原始文件是用户回溯校对的地方。

**两件不同的事**——先判断用户要哪个:
- **A. 转换 / 同步**:用户拖了文件进来要进 vault → 跑 `scripts/sync.py`。
- **B. 检索 / 回答**:用户要从已有 vault 拿答案 → 走下面的「检索与反馈协议」,**别为此跑管线**。

---

## A. 转换 / 同步

### 一次性设置(没配过就替用户做)

1. **Python 依赖**(用户级,不建 venv):
   ```
   python3 -m pip install --user requests python-dotenv pypdf pymupdf4llm openpyxl python-pptx
   ```
2. **pandoc**(docx/rtf/odt/epub):`brew install pandoc`。
3. **PATH 上要有 `claude` CLI** —— 管线 shell out `claude -p` 做 frontmatter 富化和 PPT 图片 OCR;没有就跳过这两步(不致命)。
4. **配路径**——两种方式:
   - **向导(推荐给用户):** 直接在终端 `python3 scripts/sync.py`。首次运行(还没配)会弹**交互向导**:问原始文件目录 + vault 目录(+ 可选 MinerU token),自动建目录、写 `scripts/.env`、并打印用法;然后再跑一次就开始转换。
   - **手动:** `scripts/.env.example` 复制成 `scripts/.env`,填 `KB_SOURCE_DIR` / `KB_TARGET_DIR`(绝对路径)。`MINERU_TOKEN` 可选(只在老 .doc/.ppt、.html、扫描件、图片时需要,https://mineru.net 拿)。
   - **Claude 替用户配时走手动**:向导只在交互 TTY 触发,而 `claude -p` 子进程不是 TTY——所以你(Claude)应直接问两个目录再写 `scripts/.env`。

### 运行

```
python3 scripts/sync.py          # 或双击 sync.command
```

- **增量**:只处理 SOURCE 里 VAULT 还没有对应 `.md` 的文件。要重转先删那个 `.md` 再跑。
- 本地路径(xlsx/csv/docx/pptx/md/txt/code + 数字 PDF)**不需要 MinerU token**;token 懒校验,只在真要调 MinerU 时才验。
- **孤儿暂存**:原始文件被删 → 它的工具生成 `.md` 移到 `orphaned/<日期>/`(不硬删,用户可能加过笔记);用户手写的 `.md`(无 converter marker)永不碰。

### 路由(按文件类型)

| 类型 | 工具 | 说明 |
|---|---|---|
| `.xlsx` | openpyxl 双读 | 每 sheet:带 A/B/C + 行号坐标的值表 **+ 公式清单** |
| `.csv` / `.tsv` | csv → Markdown 表 | 超 `CSV_MAX_ROWS` 截断 |
| `.pdf`(数字) | pymupdf4llm | 本地、秒级、无 quota |
| `.pdf`(扫描) | MinerU vlm(兜底) | 字符密度过低时触发 |
| `.docx`/`.rtf`/`.odt`/`.epub` | pandoc | 图片抽到 `attachments/` |
| `.pptx` | python-pptx | 标题/正文/表格/**图表**/**备注** + 图片;智能 OCR(见下) |
| `.md`/`.markdown`/`.txt` | 直拷 | 逐字拷贝,只加 frontmatter,**正文不动** |
| `.json`/`.yaml`/`.py`/… | 代码直拷 | 包进代码块 + frontmatter |
| 老 `.doc`/`.ppt`、`.html`、图片 | MinerU(云) | 本地库读不了 |
| 其他(mp3/numbers/zip/…) | **跳过** | 末尾醒目报告 + 处理建议,绝不静默丢 |

### PPT 智能 OCR

幻灯片里的图片用 `claude -p`(Read 工具读图)OCR,但为避免每张装饰 logo 都起一个慢 claude:同图去重(只 OCR 一次)、跳过 < `OCR_MIN_IMAGE_BYTES` 的小图、唯一内容图 `OCR_MAX_WORKERS` 并发。原生 PowerPoint **图表对象**直接读(类别 + series 数值 → 表)。`OCR_PPTX_IMAGES = False` 可整个关掉 OCR(图片仍抽取 + 引用)。

### Frontmatter

```yaml
---
source: "[[…/<file>.<ext>]]"   # 回原文件双链
source_type: pdf | xlsx | docx | pptx | md | …
converted_by: pymupdf4llm | pandoc | python-pptx | excel-openpyxl | csv | passthrough | "MinerU vlm" | …
# enrich（claude -p 尽力而为，失败可能缺）:
abstract: |
  3 句话总结。
auto_tags: [..]
synonyms: [中英文同义词]   # 任何说法都能 grep 到
key_data: ["关键数字/事实"]
---
```

### 可调旋钮(`scripts/config.py`)

`PYMUPDF4LLM_MIN_CHARS_PER_PAGE`(扫描件阈值)·`OCR_PPTX_IMAGES` / `OCR_MIN_IMAGE_BYTES` / `OCR_MAX_WORKERS`·`EXCEL_MAX_CELLS_PER_SHEET`·`CSV_MAX_ROWS`·`ENRICH_FRONTMATTER`。

---

## B. 检索与反馈协议(基于 vault 回答)

用户让你基于 vault 回答 / 跨文档比较时,**直接读 vault**(grep + 读 `.md`)。读的过程中自我监测、主动报告问题,别只闷头答。

### 启动体检(每个会话第一次问 vault)

```
find "$KB_TARGET_DIR" -name "*.md" -not -path "*/.obsidian/*" | wc -l
```

按规模心里设档(有问题才说):小(<100)agentic grep 够用;中(100–500)注意关键词命中数;大(500–2000)建议上语义检索(如 Smart Connections);超大(>2000)建议真正的 RAG。

### 复杂查询后自检(命中才提醒)

| 信号 | 提醒 |
|---|---|
| 一次 grep 命中 >30 文件 | 关键词太宽,给更具体的,或上语义检索 |
| 读了 5+ 文件还答不上 | 可能 synonym 没覆盖,或 vault 里确实没有——列出读过哪些 |
| 同一主题反复问 | 提议建索引 / MOC |
| 「第几章讲 X」要通读 | 提议给那本 enrich 一份章节索引 |
| 某文档缺 abstract | enrich 当时可能失败,提议补 |
| 问题涉及精确数字/公式 | 提醒点 source 双链回原文校对 |

### 主题查询 → MOC 入口顺序 + 演化

**MOC**(Map of Content)= 用户某主题的入口笔记,frontmatter `type: moc`,放 `<vault>/索引/`。

1. 主题型跨文档问题,先找有没有相关 MOC;有就先读它、当回答骨架。
2. 没有且用户反复问这主题 → **提议**建一份极简 MOC(frontmatter + `## 相关文件` 清单,就这些)。
3. MOC 结构从真实使用里**长出来**,不是预先设计。观察到可沉淀的模式(反复问的子题、反复得出的判断、未解疑问)就**提议**沉淀——用户拍板,你起草。

**频率约束(防骚扰)**:单会话最多 1 次 MOC 演化提议;同 MOC 距上次提议 <7 天跳过;要多源信号成模式,不是一次随口问;提议就一段 `> 💡 …` 引用块。

### 不要做

- 不在每个回答末尾堆「tips」——只在信号真触发时说。
- 不为了回答问题去跑转换管线。
- 不批量编辑 vault 的 `.md`(用户笔记和工具产出共存)。
- grep 没找到别瞎编——「vault 里没有」好过猜一个。
- 别把原文复制进 MOC——只放 wiki-link + 一行注解。

---

## 备注

- 管线**不依赖** Claude 会话运行——它是 CLI,只在可选的 enrich/OCR 步 shell out `claude -p`。
- 永不改文档**正文**——所有自动化只动 frontmatter,工具本身零内容丢失风险。
- 有测试覆盖的 canonical 源码在作者的 dev 项目里;这里的 `scripts/` 是打包快照。
