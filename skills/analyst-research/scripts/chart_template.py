"""
chart_template.py · v8 共用绘图样式

跨项目复用的种子代码。与 skill `references/workflow.md`（过程纪律）+
`references/report_style_spec.md`（视觉规范 + 接口契约）配套使用。规范的
真值在本文件（PALETTE dict + setup_style rcParams + save_fig 布局），
report_style_spec.md 的 §5 速查表是人工镜像，漂移时以本文件为准。

调用模板（5_scripts/make_fig_*.py 顶部）：
    import _path  # noqa: F401  -- 把 analyst-research/scripts/ 加进 sys.path
    from chart_template import setup_style, save_fig, PALETTE, FIG_W

完整接口契约见 report_style_spec.md §六。

设计精神（FT chart-doctor inspired）：
- 配色直接采用 FT g-chartcolour 实际开源 HEX
- 字号只有两档：suptitle 12pt + 其他元素 10pt（避免视觉碎片化）
- chrome minimalism（去 top/right spine，保 bottom/left + 极淡刻度）
- single accent 原则（一图一突出色）
- 标题承担论点（数字 + 事实压进 title）

PDF / JPG / clean-JPG 三输出 + 内容分离：
- PDF：保留 plot + (a)(b) 子标题 + 必要的轴装饰 / 底部 legend，不画 suptitle / 来源 / 注（Quarto caption + qmd 提供）。**用于 qmd 主报告嵌入**
- JPG（标准）：在 PDF 基础上左右各加 0.3 inch 白边距，顶部加 suptitle 区，底部加 source/note 区。**plot 主体绝对尺寸与 PDF 完全一致**，不被压缩。**用于公众号、社交分发等自包含场景**
- _clean.jpg：与 PDF 同步的纯栅格版（无烧入 title / source / note），**专供 publication-style HTML 嵌入**——HTML 模板自己提供 title 与 source，再嵌带烧入的 JPG 会出现双标题
- JPG 长边 ≤ 2000px（Anthropic API 多图请求硬上限，savefig dpi 动态算）
- _clean.jpg 用 dpi=200，FIG_W=6.69 下约 1338px 宽，远低于上限
- PDF 用 bbox_inches='tight' 自动包含 plot 下方 legend 等装饰

文字 wrap 规则（精确像素测量）：
- 三个文本（suptitle / 来源 / 注）统一 x 起点 = JPG 中 PDF 左边界位置
  （= JPG_HMARGIN_IN / fig_w_jpg），可用宽度 = PDF 整宽
- 用 matplotlib 渲染候选字串、量真实像素宽度，二分查找装得下的最长前缀
- 仅有一条断行约束：**英文单词 / 数字不可拆两半**（保护 [A-Za-z0-9.,%+\-]）。
  中文字符可在任意位置断
- 来源 / 注续行用全角空格悬挂缩进（来源 3 格、注 2 格），对齐到「来源：」「注：」后第一字位置

布局红线：
- figure 宽度统一 FIG_W = 6.69 inch（A4 - 20mm × 2 = textwidth）
- 表格不走图片管线（spec §3.9）：直接在正文 markdown / Quarto 表语法写，保留 ctrl+F / 复制
- **一图一 plot，禁止并列子图**（spec §3.7）。多 plot 需求拆成多张独立图
- PDF 顶部 padding 统一 0.10 inch
- **legend 必须放 plot 上方（无例外，spec §3.8）**。两种合法模式（都以「整张图片」为基准、不是 plot 中点）：
  ① **居中（默认）** legend 中心落在 figure-x = 0.5（image center）。带长 y-tick label 的横向柱图里 plot 中点偏右，纯 `bbox_to_anchor=(0.5, 1.02)` 会让 legend 歪。封装见 `legend_above(ax, ncol, mode="centered")`，等价于 `ax.legend(loc="lower center", bbox_to_anchor=((0.5-pos.x0)/pos.width, 1.02), ncol=N, frameon=False)`
  ② **image-left**（centered 装不下时的回退；项数极多 / 一行太宽溢出时用）`legend_above(ax, ncol, mode="image_left")`，等价于 `ax.legend(loc="lower left", bbox_to_anchor=(-pos.x0/pos.width, 1.02), ncol=N, frameon=False)`，让 legend 左边对齐到 figure 最左边（含 y-axis labels 区）
  **禁止** loc="upper right" / "upper left" / "best" / 直接 `bbox_to_anchor=(0.5, 1.02)`（这是 plot 中点不是 image 中点）；禁止 bbox_to_anchor y 为负（下方放置）
- save_fig 自动检测「上方 legend」并 +0.30 inch extra_top，让 title 与 legend 留一行空隙（脚本作者无需手动调整）

接口：
- setup_style()
- legend_above(ax, ncol=None, mode="centered"|"image_left", **kwargs)
- save_fig(fig, fig_id, title=None, source=None, note=None, subdir="")
- PALETTE：6 个语义色 (primary / secondary / tertiary / accent / accent_alt / neutral)
  适用于 5 类以内的分类图 + chrome 与文字色
- PALETTE_EXTENDED：7 个数据色，用于超出 PALETTE 5 类的分类图（如 7 国跨国对比）
- PALETTE_SEQUENTIAL：7 级蓝色梯度，用于连续数值映射（热图、密度图、有序分类）
- SEQUENTIAL_CMAP：mpl.colors.ListedColormap(PALETTE_SEQUENTIAL)，可直接传 cmap 参数
- FIG_W = 6.69 inch
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
from pathlib import Path

# chart_template.py 路径: <项目根>/analyst-research/scripts/chart_template.py
# 三次 parent 跳到项目根目录, 让 DATA_RAW / DATA_PROC / FIGURES 解析到 <项目根>/{4_data,6_figures}/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_RAW = PROJECT_ROOT / "4_data" / "1_raw"
DATA_PROC = PROJECT_ROOT / "4_data" / "2_processed"
FIGURES = PROJECT_ROOT / "6_figures"

# FT chart-doctor 数据色（来自 g-chartcolour）+ 白底（项目偏离 FT cream）
# 偏离理由：研报嵌入 Quarto white-paper PDF，cream bg 与纸张白色不协调
# 白底配置恢复左 spine + 加深 tick 色让横纵坐标可见
PALETTE = {
    # 数据色（FT 原色）
    "primary":    "#0F5499",  # Oxford blue
    "secondary":  "#208FCE",  # Medium blue
    "tertiary":   "#C2B7AF",  # Warm gray
    "accent":     "#7F062E",  # Claret
    "accent_alt": "#EB5E8D",  # Warm pink
    # 中性
    "neutral":    "#66605C",  # Warm dark gray
    # Chrome（白底适配版）
    "grid":       "#D6D0CA",  # 略加深的暖网格（白底要看得清）
    "axis":       "#66605C",  # 横纵坐标 spine + tick 颜色
    "baseline":   "#999999",  # 0 参考线
    "bg":         "#FFFFFF",  # 白底
    "bg_white":   "#FFFFFF",
    # 文字
    "text":       "#000000",  # 标题
    "text_light": "#66605C",  # 轴 / 来源 / 注
    # 表格 highlight
    "accent_light": "#FCE2D1",
}

PALETTE_EXTENDED = [
    "#0F5499", "#EB5E8D", "#70DCE6", "#9DBF57",
    "#208FCE", "#7F062E", "#C2B7AF",
]

PALETTE_SEQUENTIAL = [
    "#D6D3EA", "#ADB8E6", "#849CDB", "#5E82C8",
    "#3968AD", "#1B4F8D", "#0A3866",
]

# Sequential colormap helper：用法 `ax.imshow(data, cmap=SEQUENTIAL_CMAP)`
SEQUENTIAL_CMAP = mpl.colors.ListedColormap(PALETTE_SEQUENTIAL)


def setup_style():
    """设置 matplotlib 全局样式（完全 FT chart-doctor 风格）。

    脚手架阶段自动 detect CJK 字体是否可用，缺失时打 warning 防止 silent fail
    （CJK 渲染为方块是最常见的环境问题，部署到新机器要么装字体要么改 rcParams）。
    """
    cjk_fonts = ["Songti SC", "STSong", "SimSun", "Times New Roman", "DejaVu Sans"]
    # 字体可用性检测：任何一个 CJK 字体可用即视为 OK，全部缺失才警告
    primary_cjk_available = any(
        check_font_available(name) for name in cjk_fonts[:3]
    )
    if not primary_cjk_available:
        import warnings
        warnings.warn(
            "[chart_template] 未检测到任何主 CJK 字体（Songti SC / STSong / SimSun）。"
            "中文字符可能渲染为方块。macOS 装 Songti SC、Linux 装 wqy-microhei 或"
            "Noto Serif CJK SC、Windows 用 SimSun。或在 setup_style cjk_fonts 列表加你机器上有的字体。",
            stacklevel=2,
        )
    mpl.rcParams.update({
        # 字体（图内字号 = 正文 11pt -1 = 10pt；子标题 11pt 同正文；主标题 14pt）
        "font.family":     "serif",
        "font.serif":      cjk_fonts,
        "font.sans-serif": cjk_fonts,
        "font.size":       10,
        "axes.titlesize":  10,
        "axes.titleweight": "regular",
        "axes.labelsize":  10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "text.parse_math": False,
        "axes.unicode_minus": False,
        # 颜色
        "text.color":       PALETTE["text"],
        "axes.labelcolor":  PALETTE["text_light"],
        "xtick.color":      PALETTE["axis"],
        "ytick.color":      PALETTE["axis"],
        "axes.edgecolor":   PALETTE["axis"],
        "axes.facecolor":   PALETTE["bg"],
        "figure.facecolor": PALETTE["bg"],
        # 白底：恢复底边 + 左 spine，让横纵坐标可见
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "axes.spines.left":   True,
        "axes.spines.bottom": True,
        "axes.linewidth":     1.0,
        # 刻度（白底要可见）
        "xtick.major.size":  3.5,
        "xtick.major.width": 1.0,
        "ytick.major.size":  3.5,
        "ytick.major.width": 1.0,
        # 网格：仅 y 方向，略加深以在白底可见
        "axes.grid":      True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color":     PALETTE["grid"],
        "grid.linewidth": 0.7,
        "grid.linestyle": "-",
        # 线条
        "lines.linewidth":       2.5,
        "lines.solid_capstyle":  "butt",
        "lines.solid_joinstyle": "round",
        # 图例
        "legend.frameon":  False,
        # 输出
        "figure.dpi":         100,
        "savefig.dpi":        300,
        "savefig.bbox":       "standard",
        "savefig.pad_inches": 0.1,
        # 默认 subplot 边距
        "figure.subplot.bottom": 0.12,
        "figure.subplot.top":    0.88,
        "figure.subplot.left":   0.10,
        "figure.subplot.right":  0.96,
        "figure.constrained_layout.use": False,
    })


def legend_above(ax, ncol=None, mode="centered", **kwargs):
    """Place legend above plot per spec §3.8. 调用前确保 ax 的 plot/bar 已绘完。

    mode:
        "centered"   — **默认**。legend 居中于「整张图片」（不是 plot 中点）。
                       带长 y-tick label 的横向柱图里 plot 中点会偏右，纯
                       plot-centered 会让 legend 视觉上歪向右。本模式用 axes
                       坐标系换算让 legend 中心落在 figure-x = 0.5（image 中心）。
        "image_left" — **centered 装不下时的回退**。项数极多 / 一行太宽时，
                       居中会让 legend 在两边都超界；image-left 让 legend 从
                       figure 最左边开始（含 y-axis labels 区），把所有可用
                       横向空间让给 legend。除非 centered 真的溢出，否则不用。

    kwargs 透传 ax.legend（fontsize / handles / labels 等）。
    """
    base = dict(frameon=False, fontsize=10)
    if ncol is not None:
        base["ncol"] = ncol
    pos = ax.get_position()
    if mode == "centered":
        # 让 legend 中心点落在 figure-x = 0.5 (image center)。
        # axes 坐标系换算：x_axes 使得 pos.x0 + x_axes * pos.width = 0.5
        x_axes = (0.5 - pos.x0) / pos.width
        base.update(loc="lower center", bbox_to_anchor=(x_axes, 1.02))
    elif mode == "image_left":
        base.update(loc="lower left",
                    bbox_to_anchor=(-pos.x0 / pos.width, 1.02))
    else:
        raise ValueError(f"unknown legend mode: {mode!r}")
    base.update(kwargs)
    return ax.legend(**base)


def _get_renderer(fig):
    """获取一个可用于量文字宽度的 renderer。Agg backend 是首选。"""
    if hasattr(fig.canvas, "get_renderer"):
        try:
            return fig.canvas.get_renderer()
        except Exception:
            pass
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    return FigureCanvasAgg(fig).get_renderer()


_WORD_CHAR_RE = __import__("re").compile(r"[A-Za-z0-9.,%+\-]")


def _wrap_text_precise(fig, text: str, max_width_in: float,
                       fontsize: int, hang_indent: str = "",
                       **text_kwargs) -> str:
    """按真实渲染宽度精确 wrap。

    规则：① 二分查找当前行「装得下的最长前缀」；② 默认就在那个位置断行；
    ③ **唯一例外**：如果该位置切在英文 / 数字词中间（防止数字 / 单词被劈成两半），
    回退到词的开头，把整个词推到下一行。
    中文字符没有「词」概念，任何位置都可以断。

    每个续行（line 2+）前置 hang_indent（如全角空格）形成悬挂缩进。

    text_kwargs 传给 fig.text（影响渲染宽度）：fontweight / style / linespacing 等。
    """
    # 仅在 mathtext 解析开启时才转义 $；setup_style() 设 text.parse_math=False，
    # 此时 $ 是普通字面字符，转义会让图上多出一个反斜杠（pre-flight self-test 命中）。
    safe = text.replace("$", r"\$") if mpl.rcParams.get("text.parse_math", False) else text
    renderer = _get_renderer(fig)

    def width_in(s: str) -> float:
        """渲染 s 并量它的宽度（inch）。"""
        t = fig.text(0, 0, s, fontsize=fontsize, **text_kwargs)
        try:
            bbox = t.get_window_extent(renderer)
            return bbox.width / fig.dpi
        finally:
            t.remove()

    def is_word_char(c: str) -> bool:
        """英文字母 / 数字 / 小数点 / 千分位逗号 / 百分号 / 正负号——不可被分行。"""
        return bool(_WORD_CHAR_RE.match(c))

    # 整段能装下就一行返回
    if width_in(safe) <= max_width_in:
        return safe

    lines = []
    remaining = safe
    while remaining:
        prefix = hang_indent if lines else ""
        # 整体能装下，本行收尾
        if width_in(prefix + remaining) <= max_width_in:
            lines.append(prefix + remaining)
            break
        # 二分查找「装得下的最长前缀」
        lo, hi = 1, len(remaining)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if width_in(prefix + remaining[:mid]) <= max_width_in:
                lo = mid
            else:
                hi = mid - 1
        if lo == 0:
            lo = 1
        cut = lo
        # 唯一回退：cut 切在英文 / 数字词中间，回退到词首
        if 0 < cut < len(remaining):
            if is_word_char(remaining[cut - 1]) and is_word_char(remaining[cut]):
                i = cut - 1
                while i > 0 and is_word_char(remaining[i]):
                    i -= 1
                # 回退后至少留 1 字（避免整行被全部推走变空行）
                if i > 0 or not is_word_char(remaining[0]):
                    cut = i + 1
                # else: 整行就是一个超长词，没办法只能在 lo 处硬切
        chunk = remaining[:cut].rstrip()
        lines.append(prefix + chunk)
        remaining = remaining[cut:].lstrip()
    return "\n".join(lines)


def save_fig(fig, fig_id: str,
             title: str = None, source: str = None, note: str = None,
             subdir: str = "", lang: str = "zh", clean: bool = True):
    """PDF（裸图）+ JPG（含 title/source/note）+ _clean.jpg（与 PDF 同步的栅格版）三输出。

    设计（v9）：在 v8 的 PDF + JPG 基础上加了 `_clean.jpg`，专供 publication-style
    HTML 嵌入。HTML 模板自己提供 title 与 source，再嵌带烧入的 JPG 会出现双标题。

    - PDF：figsize = (FIG_W, h) 由调用方决定，纯 plot
    - JPG：figsize = (FIG_W, h + extra_top + extra_bottom)，plot 绝对尺寸与 PDF 相同
      只是上下额外加了「标题区」「来源/注区」
    - _clean.jpg：与 PDF 同步落地，dpi=200，bbox='tight'，纯 plot

    历史问题（v7）：JPG 与 PDF 同高，suptitle/source/note 通过 subplots_adjust
    挤占 plot 顶/底空间，导致 plot 被压扁。v8 改成 plot 不动、figure 加高。

    布局（JPG，自上而下）：
    - 顶部留白 → suptitle (14pt) → suptitle 与 plot 呼吸 → plot 顶（与 PDF 同位置）
    - plot 主体（与 PDF 完全一致）
    - plot 底（与 PDF 同位置）→ 呼吸 → source (10pt) → 间隔 → note (10pt) → 底部留白

    参数：
        title:  顶部一级标题（事实 + 数字，承担论点）
        source: 底部「来源：...」单独一行
        note:   底部「注：...」单独一行（source 下方）
    """
    out_dir = FIGURES / subdir if subdir else FIGURES
    out_dir.mkdir(parents=True, exist_ok=True)

    fig_w_pdf, fig_h_pdf = fig.get_size_inches()

    # 一图一 plot 硬规则（spec §3.7）：检测到多个 axes 时打印 warning
    if len(fig.axes) > 1:
        import warnings
        warnings.warn(
            f"[chart_template] {fig_id} 含 {len(fig.axes)} 个 axes，违反「一图一 plot」"
            f"硬规则（spec §3.7）。继续渲染会出现：① publication HTML 嵌入时 layout 错位"
            f"（_clean.jpg 含多 plot 在 HTML exhibit 框内显示挤压）；② JPG 的 suptitle / "
            f"source / note 与多 plot 视觉关系混乱。**正确做法**：拆成多张独立 fig，"
            f"每张单独调 save_fig。",
            stacklevel=2,
        )

    # 关键尺寸常量（inch）
    LINE_H_IN          = 0.18  # 10pt × 1.3 linespacing 单行高度
    TITLE_LINE_H_IN    = 0.22  # 12pt × 1.3 linespacing 单行高度
    PAD_BOTTOM_IN      = 0.15  # 最底部页边距
    SRC_NOTE_GAP_IN    = 0.06  # source 与 note 行之间间距
    PLOT_BOTTOM_GAP_IN = 0.45  # plot 底与 source 顶呼吸（含一行额外空白）
    SUPTITLE_TOP_IN    = 0.25  # suptitle 距 figure 顶部
    PLOT_TOP_GAP_IN    = 0.25  # suptitle 与 plot 之间呼吸
    JPG_HMARGIN_IN     = 0.30  # JPG 比 PDF 左右各多出的白边距
    TOP_PAD_PDF_IN     = 0.10  # PDF 顶部 padding（一图一 plot 后统一值）

    PDF_TOP_FRAC    = 1.0 - TOP_PAD_PDF_IN / fig_h_pdf
    PDF_BOTTOM_FRAC = 0.08

    # === 1) PDF：裸图（无 suptitle / 来源 / 注），Quarto caption 提供这些 ===
    # bbox_inches='tight' 自动扩到包含所有可见内容（含 plot 上方 legend、下方 legend、
    # 长 y-label 等装饰）。PDF 实际尺寸可能比 figsize 略小，Quarto 嵌入时按 textwidth 缩放
    fig.subplots_adjust(top=PDF_TOP_FRAC, bottom=PDF_BOTTOM_FRAC)
    pdf = out_dir / f"{fig_id}.pdf"
    fig.savefig(pdf, bbox_inches='tight', pad_inches=0.05)

    # === 1.5) CLEAN JPG：与 PDF 同步的栅格版（无 title/source/note），供 publication-style
    # HTML / 公众号 等需要纯图嵌入的场景。HTML 已经用模板提供 title 与 source，再嵌带 title 的
    # JPG 会重复。dpi=200 在 FIG_W=6.69 下给约 1338px 宽，远低于 2000px 上限
    # _clean.jpg 仅在 clean=True 时生成（heavy 的 publication HTML 需要；
    # medium / light 不出 publication，可传 clean=False 跳过，见 workflow_medium §四）
    if clean:
        jpg_clean = out_dir / f"{fig_id}_clean.jpg"
        fig.savefig(jpg_clean, bbox_inches='tight', pad_inches=0.05, dpi=200,
                    facecolor=PALETTE["bg"])

    # 记录 PDF 阶段的 plot 左/右 fig-fraction（用于后续把 plot 平移到 JPG 中）
    L_old = fig.subplotpars.left
    R_old = fig.subplotpars.right

    # === 2) JPG：在 PDF 基础上左右各加 HMARGIN 白边距、上下加内容区 ===

    # 文字 wrap 宽度 = PDF 整宽（覆盖 y-label 区 + plot 数据区），与 PDF 等宽
    usable_w_in = fig_w_pdf

    # 用 _wrap_text_precise 按真实像素宽度 wrap，不再用字数估算
    # source / note 续行用全角空格悬挂缩进，对齐「来源：」「注：」后第一字位置
    title_lines = src_lines = note_lines = 0
    title_text = src_text = note_text = ""
    if title:
        title_text = _wrap_text_precise(fig, title, max_width_in=usable_w_in,
                                         fontsize=12, fontweight="normal")
        title_lines = title_text.count("\n") + 1
    src_prefix = "Source: " if lang == "en" else "来源："
    note_prefix = "Note: " if lang == "en" else "注："
    src_hang = "        " if lang == "en" else "　　　"
    note_hang = "      " if lang == "en" else "　　"
    if source:
        src_text = _wrap_text_precise(fig, f"{src_prefix}{source}",
                                       max_width_in=usable_w_in, fontsize=10,
                                       hang_indent=src_hang, style="italic")
        src_lines = src_text.count("\n") + 1
    if note:
        note_text = _wrap_text_precise(fig, f"{note_prefix}{note}",
                                        max_width_in=usable_w_in, fontsize=10,
                                        hang_indent=note_hang, style="italic")
        note_lines = note_text.count("\n") + 1

    # 检测「上方 legend」：plot 顶端有 legend（如 bbox_to_anchor=(0,1.02)）。
    # 这种 legend 默认会贴近 suptitle 形成视觉压迫，需要额外留 0.30 inch 让 title 和 legend 分开
    has_legend_above_plot = False
    try:
        _det_renderer = _get_renderer(fig)
        for _ax in fig.axes:
            _leg = _ax.get_legend()
            if _leg is None:
                continue
            _leg_bb = _leg.get_window_extent(_det_renderer)
            _ax_bb = _ax.get_window_extent(_det_renderer)
            if _leg_bb.y0 >= _ax_bb.y1 - 1:  # legend 底沿在 plot 顶端及以上
                has_legend_above_plot = True
                break
    except Exception:
        pass

    # 计算 JPG 需要的额外 top / bottom 高度（基于 wrap 后的真实行数）
    LEGEND_ABOVE_EXTRA_IN = 0.30  # 上方 legend 时 title 与 legend 之间多留 ~一行空隙
    extra_top_in = 0.0
    if title:
        extra_top_in = SUPTITLE_TOP_IN + title_lines * TITLE_LINE_H_IN + PLOT_TOP_GAP_IN
        if has_legend_above_plot:
            extra_top_in += LEGEND_ABOVE_EXTRA_IN

    extra_bottom_in = 0.0
    if source or note:
        extra_bottom_in = PLOT_BOTTOM_GAP_IN + PAD_BOTTOM_IN
        if source:
            extra_bottom_in += src_lines * LINE_H_IN
        if note:
            extra_bottom_in += note_lines * LINE_H_IN
            if source:
                extra_bottom_in += SRC_NOTE_GAP_IN

    # JPG 新尺寸：宽 = PDF 宽 + 左右白边距 × 2；高 = PDF 高 + 上下内容区
    fig_w_jpg = fig_w_pdf + 2 * JPG_HMARGIN_IN
    fig_h_jpg = fig_h_pdf + extra_top_in + extra_bottom_in
    fig.set_size_inches(fig_w_jpg, fig_h_jpg)

    # 重新定位 plot 子图：保持 plot 绝对位置（与 PDF 一致），左右平移 HMARGIN
    # 注：plot top 用 PDF_TOP_FRAC（多子图时已为 (a)(b) 预留空间），不再用硬编码 0.96
    new_plot_left   = (JPG_HMARGIN_IN + L_old * fig_w_pdf) / fig_w_jpg
    new_plot_right  = (JPG_HMARGIN_IN + R_old * fig_w_pdf) / fig_w_jpg
    new_plot_top    = (extra_bottom_in + PDF_TOP_FRAC * fig_h_pdf) / fig_h_jpg
    new_plot_bottom = (extra_bottom_in + PDF_BOTTOM_FRAC * fig_h_pdf) / fig_h_jpg
    fig.subplots_adjust(top=new_plot_top, bottom=new_plot_bottom,
                        left=new_plot_left, right=new_plot_right)

    # 文字 x 起点 = JPG 中「PDF 左边界」位置 = HMARGIN inch / fig_w_jpg
    # 这样文字与原 PDF 最左边对齐，跟整图最左边一致
    text_x_frac = JPG_HMARGIN_IN / fig_w_jpg

    # title：用 fig.text 而非 fig.suptitle 以支持 wrap 多行
    if title:
        title_top_y = 1.0 - SUPTITLE_TOP_IN / fig_h_jpg
        fig.text(text_x_frac, title_top_y, title_text, fontsize=12, fontweight="normal",
                 color=PALETTE["text"], ha="left", va="top", linespacing=1.3)

    # source / note：从底向上画
    cursor_in = PAD_BOTTOM_IN
    if note:
        fig.text(text_x_frac, cursor_in / fig_h_jpg, note_text, fontsize=10,
                 color=PALETTE["text_light"], ha="left", va="bottom",
                 style="italic", linespacing=1.3)
        cursor_in += note_lines * LINE_H_IN
        if source:
            cursor_in += SRC_NOTE_GAP_IN
    if source:
        fig.text(text_x_frac, cursor_in / fig_h_jpg, src_text, fontsize=10,
                 color=PALETTE["text_light"], ha="left", va="bottom",
                 style="italic", linespacing=1.3)

    # === 3) 存 JPG（动态 dpi 保证长边 ≤ 2000px，对齐 §3.11）===
    jpg = out_dir / f"{fig_id}.jpg"
    jpg_dpi = min(200, int(2000 / max(fig_w_jpg, fig_h_jpg)))
    fig.savefig(jpg, dpi=jpg_dpi)
    print(f"Saved: {fig_id}.pdf ({fig_w_pdf:.2f}x{fig_h_pdf:.2f}) + "
          f"{fig_id}.jpg ({fig_w_jpg:.2f}x{fig_h_jpg:.2f}, dpi={jpg_dpi})")
    return pdf, jpg


# —— 全研报统一宽度常量（绝对 inch）——
# A4 21cm - 20mm × 2 边距 = 17cm = 6.69 inch。锁定 figsize.width = FIG_W 让所有
# 图嵌入 Quarto PDF 时缩放比 = 1.0，matplotlib rcParams 字号即 PDF 上量得的字号。
# 不锁定时，figsize 10 inch 宽会被 PDF 缩到 6.69 inch，字号也按 0.67 倍缩水。
FIG_W = 6.69           # 图 figsize 宽度（make_fig_*.py 用 figsize=(FIG_W, h)）


def annotate_value(ax, x, y, text, color=None, **kwargs):
    color = color or PALETTE["text_light"]
    ax.annotate(text, xy=(x, y), xytext=(0, 6), textcoords="offset points",
                ha="center", fontsize=9, color=color, **kwargs)


def check_font_available(name: str = "Songti SC") -> bool:
    return any(f.name == name for f in font_manager.fontManager.ttflist)


if __name__ == "__main__":
    setup_style()
    print(f"Songti SC: {check_font_available('Songti SC')}")
    print(f"PALETTE primary (FT Oxford blue): {PALETTE['primary']}")
    print(f"PALETTE accent (FT Claret):       {PALETTE['accent']}")
    print(f"PALETTE bg (white):               {PALETTE['bg']}")
    print(f"PALETTE axis (warm gray):         {PALETTE['axis']}")

    # 自检：FT 风格柱图（中性占位数据，不绑具体场景）
    fig, ax = plt.subplots(figsize=(FIG_W, 3.5))
    cats = ["分类 A", "分类 B（前）", "分类 C（后）"]
    vals = [20, 50, 75]
    colors = [PALETTE["tertiary"], PALETTE["tertiary"], PALETTE["accent"]]
    bars = ax.bar(cats, vals, color=colors, width=0.55)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1.5, f"{val}%",
                ha="center", fontsize=10, color=PALETTE["text"])
    ax.set_ylabel("占比（%）")
    ax.set_ylim(0, 90)
    save_fig(fig, "test_bar",
             title="某指标修订前后对照（占位示例）",
             source="机构 X 年报 YYYY",
             note="口径说明占位示例",
             subdir="_test")
    plt.close(fig)

    print("chart_template 自检完成。")
