# Skill 来源与本地适配

本仓库保留实际使用的 Skill 副本、来源与必要适配说明。第三方内容沿用各自许可证和署名；本表不对第三方内容重新授权，也不新增统一许可证。更新时按实际取得版本核对来源、许可和依赖。

| 来源 | 本地 Skill | 许可证 | 本地适配 |
| --- | --- | --- | --- |
| 本地编写 | `steady-progress`、`scene-mode-collaboration`、`research-cycle` | 本仓库自有 | 通用推进规则，以及按场景、模式和任务规模组织工作；协作 Skill 增加记忆续接、实际子智能体和思考强度规则。 |
| [lennney/stop-that-shit](https://github.com/lennney/stop-that-shit)（此前保存的本地副本） | `stop-that-shit`、`stss` | [MIT](licenses/stop-that-shit-LICENSE) | 按任务需要调用，允许自动选择。未安装 Guard 或 Hook。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `grill-me`、`grilling`、`improve-codebase-architecture` | [MIT](licenses/mattpocock-skills-LICENSE) | `grill-me` 改为读取已安装依赖；架构维护 Skill 去除未安装依赖、强制 HTML 报告和自动写入项目文档。 |
| [tyshkovskii/reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill) | `reviewing-code-modularity-skill` | [MIT](skills/reviewing-code-modularity-skill/LICENSE) | 保留上游 Skill 正文。 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `paper-lookup`、`hypothesis-generation`、`exploratory-data-analysis`、`statistical-analysis`、`scientific-visualization`、`scientific-writing`、`scientific-critical-thinking` | [MIT](licenses/K-Dense-scientific-agent-skills-LICENSE.md) | 假说 Skill 允许穷举模式下临时比较探索优先级，最终判断由人负责；批判性思维 Skill 去除未安装且可能另行计费的 OpenRouter 绘图入口。 |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | `experiment-plan` | [MIT](licenses/wanshuiyin-research-LICENSE) | 改为任务内研究记录，去除不存在的上游命令和输出协议依赖；规划不授权运行实验。 |
| [msimchowitz/writing-skills](https://github.com/msimchowitz/writing-skills) | `presentation-making` | [MIT](licenses/msimchowitz-writing-skills-LICENSE) | 反馈先作为当前任务规则；跨任务复用或长期记忆须另行确认。 |
| [JetBrains/skills](https://github.com/JetBrains/skills)（`slides` 元数据注明 OpenAI 来源） | `slides`、`slidev` | [Apache-2.0](skills/slides/LICENSE.txt)、[MIT](skills/slidev/LICENSE.md) | `slidev` 仅用于明确要求的网页演示；可编辑 PPTX 优先用 `slides`。 |

本地自编部分保留现有授权状态。Skill 文本不增加操作权限；部署方法见 [跨机器部署指南](codex/PORTABILITY.md)。阶段日志、临时审查与验收材料保留在各机器本地，不随框架分发。
