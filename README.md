# Codex 协作框架与 Skill 清单

下列本地 Skill 由此仓库统一维护；只有明确标作候选的外部链接尚未部署。来源和本地适配见 [SOURCES.md](SOURCES.md)。

Codex 全局指令备份见 [codex/AGENTS.md](codex/AGENTS.md)，部署到当前 Codex 主目录下的 `AGENTS.md`；主目录优先使用 `CODEX_HOME`，未设置时为 `~/.codex`。默认 Skill 按当前环境提供的路径加载。

## 协作框架

首次任务确认场景（工程、科研、汇报）和模式（成长、穷举、爆破）；后续任务沿用已确认且仍适用的选择。委派边界一次约定后，由 AI 根据独立工作或独立判断的价值按需派发，小任务直接完成。短任务形成成果后直接交接，长阶段按需商定排程。

| 机制 | 当前规则 | 详细说明 |
| --- | --- | --- |
| 记忆与 Skill 沉淀 | 个人偏好和可复用方法积累为候选，大段工作结束后统一确认再保存；通用经验优先更新稳健 Skill | [记忆与沉淀](skills/steady-progress/references/memory.md) |
| 子智能体 | 一次约定后按需委派，明确接口与写入范围，主线程统一回收、集成和交付 | [子智能体派发与回收](skills/steady-progress/references/subagents.md) |
| 思考强度 | 同一批同类任务：一名执行者 `max`，多名并行执行者各 `high`；不同类分别计数 | [high／max 指派规则](skills/steady-progress/references/reasoning.md) |

三项通用机制统一维护在 `steady-progress`，由场景 Skill 引用。个人偏好文件在首次具体条目获确认后建立；原生自动生成不代替确认流程。思考强度由实际调用或派发设置，本机主智能体现有 `max` 配置保留，安装规则不冒充已在运行时自动调参。

维护顺序：**修改本仓库 → 检查 → 提交并通过 SSH 推送 GitHub 子分支 → 同步本地 Codex**。推送成功后，按改动范围将 `codex/AGENTS.md` 和有关 `skills/<名称>/` 内容复制到实际 Codex 主目录的对应位置，备份被替换的文件并核对内容一致。重新加载后生效的指令在新会话中核对。个人记忆与运行状态留在本地。

## 通用

- [稳健推进](skills/steady-progress/SKILL.md)：测试与写入边界、阶段推送、记忆与 Skill 确认、按需委派及 high／max 指派。
- [场景与模式协作](skills/scene-mode-collaboration/SKILL.md)：按场景、模式和任务规模组织工作功能、Skill 与人机交接。
- [grill-me](skills/grill-me/SKILL.md) 与依赖 [grilling](skills/grilling/SKILL.md)：AI 主导追问。

## 工程

- [STS](skills/stop-that-shit/SKILL.md)、[STSS](skills/stss/SKILL.md)：小规模敏捷开发。
- [reviewing-code-modularity-skill](skills/reviewing-code-modularity-skill/SKILL.md)：大规模开发。
- [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md)：代码库维护。

## 科研

- [research-cycle](skills/research-cycle/SKILL.md)：科研全流程协作。
- [paper-lookup](skills/paper-lookup/SKILL.md)：论文检索与来源核对。
- [hypothesis-generation](skills/hypothesis-generation/SKILL.md)：假说生成。
- [experiment-plan](skills/experiment-plan/SKILL.md)：软件实验规划。
- [experimental-design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md)（候选，未部署）：一般实验设计。
- [exploratory-data-analysis](skills/exploratory-data-analysis/SKILL.md)、[statistical-analysis](skills/statistical-analysis/SKILL.md)（按需）：数据探索与统计分析。
- [scientific-visualization](skills/scientific-visualization/SKILL.md)、[scientific-writing](skills/scientific-writing/SKILL.md)（按需）：科研图表与论文／报告写作。
- [scientific-critical-thinking](skills/scientific-critical-thinking/SKILL.md)：研究方法与结论复核。

## 汇报

- [presentation-making](skills/presentation-making/SKILL.md)：汇报叙事与内容设计。
- [slides](skills/slides/SKILL.md)：可编辑 PPTX 制作。
- [slidev](skills/slidev/SKILL.md)（按需）：交互演示与代码讲解。
