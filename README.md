# Codex 协作框架与 Skill 清单

下列本地 Skill 由此仓库统一维护；只有明确标作候选的外部链接尚未部署。来源和本地适配见 [SOURCES.md](SOURCES.md)。

Codex 全局指令备份见 [codex/AGENTS.md](codex/AGENTS.md)，部署到当前 Codex 主目录下的 `AGENTS.md`；主目录优先使用 `CODEX_HOME`，未设置时为 `~/.codex`。默认 Skill 按当前环境提供的路径加载。

## 协作框架

首次任务确认场景（工程、科研、汇报）和模式（成长、穷举、爆破）；后续任务沿用已确认且仍适用的选择。默认由当前智能体直接完成工作，需要独立工作或独立判断时再提出团队分工。短任务形成成果后直接交接，长阶段按需商定排程。

| 机制 | 当前规则 | 详细说明 |
| --- | --- | --- |
| 记忆 | 项目记录支持续接；长期偏好按明确保存意图维护；原生记忆可选 | [记忆与续接](skills/scene-mode-collaboration/references/memory.md) |
| 子智能体 | 按明确派发请求或已选团队分工启用，约定范围并回收真实结果 | [子智能体派发与回收](skills/scene-mode-collaboration/references/subagents.md) |
| 思考强度 | 沿用用户配置；子智能体默认继承，按需明确覆盖并核对生效 | [思考强度](skills/scene-mode-collaboration/references/reasoning.md) |

三项机制由现有 `scene-mode-collaboration` 按需加载。安装这些规则不会自动启用 Codex 原生记忆、创建子智能体或改变模型与思考强度；可选配置示例见相应说明。

维护顺序：**修改本仓库 → 检查 → 提交并通过 SSH 推送 GitHub 子分支 → 同步本地 Codex**。推送成功后，按改动范围将 `codex/AGENTS.md` 和有关 `skills/<名称>/` 内容复制到实际 Codex 主目录的对应位置，备份被替换的文件并核对内容一致。重新加载后生效的指令在新会话中核对。个人记忆与运行状态留在本地。

## 通用

- [稳健推进](skills/steady-progress/SKILL.md)：测试请示、服务器修改边界与阶段代码推送。
- [场景与模式协作](skills/scene-mode-collaboration/SKILL.md)：按任务规模组织分工、Skill 与交接，按需管理记忆续接、子智能体和思考强度。
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
