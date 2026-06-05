# 用户反馈记录

> 倒序，最新在上。每条三段：反馈 / 分析 / 方案。

---

## 2026-06-05 · HTML 满屏样式噪音 + PDF 抽图怕慢/没价值 · local-vault

**反馈**
> html 文件你建议怎么处理？html 中有很多无关信息。pdf 所有图片都保存感觉会变慢，而且有些图片好像没有价值？

**分析**
① `.html` 当时走 MinerU 云(要 token、慢、模型也不对口),且即便转出来,内联 `style=`/布局 `div` 等"无关信息"会污染正文。② 上一版给数字 PDF 开了无差别抽图,image-heavy PDF 会变慢、vault 长一堆装饰小图/重复 logo,"有没有价值"靠尺寸只能近似判断。

**方案**（v1.4.0）
- `.html`/`.htm` 改走**本地 pandoc**(零新增依赖):转换前正则剥掉 `style/class/id` 属性 + 布局 `div`/`section`/`span`,只留正文;保留 raw_html 以免复杂表格被降成 `[TABLE]` 丢内容。去掉 MinerU-html 路由
- PDF 抽图**保留但收紧**:阈值 5%→12%(`PYMUPDF4LLM_IMAGE_SIZE_LIMIT`);抽出后再过**最小字节**(`PYMUPDF4LLM_IMAGE_MIN_BYTES=6000`,装饰小图整条引用删)+ **内容去重**(每页重复 logo 只存一份);加全局开关 `PYMUPDF4LLM_WRITE_IMAGES`(`.env: KB_PDF_NO_IMAGES=1` 纯文字快跑)

---

## 2026-06-05 · 数字 PDF 丢图 + 双击入口落点错位/重复 · local-vault

**反馈**
> 数字版 PDF 里的图希望也抽进 attachments。另外 02 原始知识库里的 sync.command 和 09 本地知识库里的 sync.command 是不是重复了？新用户使用时我希望在本地知识库根建立 sync.command，不是在 02 原始知识库下面；如果之前有了，就提醒用户是跳过还是更新。

**分析**
两件事。① 数字 PDF 走 pymupdf4llm，`to_markdown` 默认 `write_images=False` → 图被直接丢弃,只剩文字;用户带图表的 PDF 转完丢了图。② launcher 历史上落在 SOURCE(`02 原始知识库`),而用户手里又有一个手写的落在知识库根(`09 本地知识库`),两个并存造成困惑;且每次运行静默覆盖/自愈,没给用户「跳过还是更新」的选择。

**方案**（v1.3.0）
- pymupdf4llm 开 `write_images=True`,图抽进 `attachments/<stem>/`,重命名为 ascii 安全名(`img-0.png`…,规避中文/空格源名破坏链接),改写引用;沿用 `image_size_limit=0.05`(<页面 5% 不抽),暴露成 `PYMUPDF4LLM_IMAGE_SIZE_LIMIT` 可调;稀疏→MinerU fallback 时丢弃已抽的图
- launcher 落点从 SOURCE 改到其父目录(知识库根);自动删除 SOURCE 里带标记的旧 launcher(用户手写的不碰)
- 根目录已有不同 launcher 时:TTY 提示「更新/跳过」;非交互+我们自己的旧版静默自愈,非交互+用户自定义保留不动

---

## 2026-05-13 · 时间窗口失守 · topic-brief

**反馈**
> 测试了一下，就是在时间维度上好像还有点混淆，比如过去一个月的观察，里边放入的内容可能会有更早期的，比如半年以前的。

**分析**
搜索 query 不带时间过滤词，引擎按相关性返回，半年前的"大事件"因 SEO 权重高被召回；JSON 没有 `event_date` 字段，自检 checklist 无法校验时效；阶段确认展示候选条目时不显示日期，用户也难发现 stale。

**方案**（v0.2.0）
- 步骤 1 把时间窗口固化为 `[period_start, period_end]` 两个日期
- 步骤 2 每次搜索 query 注入时间过滤（`after: before:`）
- 步骤 3 阶段确认展示候选条目时带上事件日期
- JSON item 新增必填 `event_date`，自检 checklist 加一条"每个 event_date 在窗口内"
- 显式区分：焦点正文允许引背景（标注更早时点），4 个子板块 items 必须严格 in-window

---
