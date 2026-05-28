# analyst-research · workflow 总览（中文镜像）

> 英文主文件为 `workflow.md`。

实际的逐步工作流住在三个 mode 专属文件里。用户在触发时选定 mode 后（见 `SKILL.md` 第 0 步），加载对应文件作为工作流文档：

| Mode | 工作流文件 | 步数 | 备注 |
|---|---|---|---|
| `light` | `workflow_light.md` | 6 | 仅软停。无图。纯 markdown 脚注引用。 |
| `medium` | `workflow_medium.md` | 8 | 一个硬停（draft 后 sign-off）。6-10 图。脚注引用。 |
| `heavy` | `workflow_heavy.md` | 11 | 三个硬停（outline / draft / final）。25-35+ 图。BibTeX + APA。可选多 LLM。 |

每个 mode 的工作流文件都是**自包含**的，含：

- scope 与边界段（何时用、何时不用）
- onboarding 流程（mode 专属问题集，如 light 只问 hypothesis + 语言，heavy 问约 4 个）
- 带停点语义（软 / 硬）的步骤骨架
- 写作纪律（文风红线、grep 自检表）
- 复盘规则（如何把项目经验上溯回 skill）

三个工作流文件共用同一份**视觉规范**（`report_style_spec.md`）做图 —— light 跳过（无图），medium 与 heavy 都消费它。

## 跨 mode 不变量

无论加载哪个工作流文件，以下规则对三档都适用：

1. **hypothesis 优先**：每个项目都从一句话 hypothesis lock 起步。hypothesis 从第一天起随项目文件走，永不从 draft 反推。
2. **来源可追溯**：终稿引用的每个数字都必须追溯到一手来源。边写边引，不写完再补引。
3. **三态标注**：事实（据来源）、估算（据市场共识）、推断（自己推导）用不同措辞标注，三者不混。
4. **不造数**：「未公开」「待核实」永远好过一个看似合理的猜测。
5. **回复跟随聊天语言；报告默认英文**。英文聊→英文回，中文聊→中文回。交付物 draft 默认英文（不论聊天语言）—— onboarding 时问「报告语言：英文（默认）/ 其他？」并锁进项目 CLAUDE.md。这覆盖旧的「draft 随 hypothesis 语言」规则（见 SKILL.md「语言策略」）。

## 项目中途升档

若 `light` 项目跑着发现需要更深，重新以 `medium` 触发 —— hypothesis lock 与早期来源工作可迁移，因为三档起步相同。`medium → heavy` 同理。降档通常不值得，砍交付物而非重跑。

## 给 AI 的文件加载指令

当你（AI）作为 analyst-research skill 加载序列的一部分读到本文件时：

1. 用户已选定 mode（见 SKILL.md 第 0 步）。确认是哪个。
2. 加载对应的 `workflow_<mode>.md` 作为权威流程文档。
3. 仅当 mode 为 `medium` 或 `heavy` 时加载 `report_style_spec.md`。
4. 进入所加载 `workflow_<mode>.md` 的 onboarding 段。

不要在运行时试图合并或对比三个工作流文件 —— 它们各自独立维护，步数、停点语义、交付物形态有意不同。

（英文主文件含相同内容，见 `workflow.md`。）
