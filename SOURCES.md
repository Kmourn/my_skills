# Skill 来源与本地适配

本仓库保留实际使用的 Skill 副本、来源与必要适配说明。第三方内容沿用各自许可证和署名；本表不对第三方内容重新授权，也不新增统一许可证。更新时按实际取得版本核对来源、许可和依赖。

| 来源 | 本地 Skill | 许可证 | 本地适配 |
| --- | --- | --- | --- |
| 本地编写 | `steady-progress`、`scene-mode-collaboration`、`research-cycle` | 本仓库自有 | 通用推进规则，以及按场景、模式和任务规模组织工作；记忆确认、Skill 沉淀、实际子智能体和人数强度规则统一归入 `steady-progress`。 |
| [lennney/stop-that-shit](https://github.com/lennney/stop-that-shit)（此前保存的本地副本） | `stop-that-shit`、`stss` | [MIT](licenses/stop-that-shit-LICENSE) | 按任务需要调用，允许自动选择。未安装 Guard 或 Hook。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `grill-me`、`grilling`、`improve-codebase-architecture` | [MIT](licenses/mattpocock-skills-LICENSE) | `grill-me` 改为读取已安装依赖；架构维护 Skill 去除未安装依赖、强制 HTML 报告和自动写入项目文档。 |
| [tyshkovskii/reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill) | `reviewing-code-modularity-skill` | [MIT](skills/reviewing-code-modularity-skill/LICENSE) | 保留上游 Skill 正文。 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `paper-lookup`、`hypothesis-generation`、`exploratory-data-analysis`、`statistical-analysis`、`scientific-visualization`、`scientific-writing`、`scientific-critical-thinking` | [MIT](licenses/K-Dense-scientific-agent-skills-LICENSE.md) | 假说 Skill 允许穷举模式下临时比较探索优先级，最终判断由人负责；批判性思维 Skill 去除未安装且可能另行计费的 OpenRouter 绘图入口。 |
| [K-Dense-AI/scientific-agent-skills，固定提交](https://github.com/K-Dense-AI/scientific-agent-skills/tree/91497e335489dcb544ec8ddc8f6b7ce5fd6d1121/skills/experimental-design) | `experimental-design` | [MIT](skills/experimental-design/LICENSE) | 明确与软件实验规划、统计分析的分工，复用授权与研究记录；修复交错分层的单位对应和零块大小循环，缺失分层标签明确报错。 |
| [K-Dense-AI/scientific-agent-skills，固定提交](https://github.com/K-Dense-AI/scientific-agent-skills/tree/91497e335489dcb544ec8ddc8f6b7ce5fd6d1121/skills/peer-review) | `peer-review` | [MIT](skills/peer-review/LICENSE.md) | 区分真实期刊审稿与获准内部预审，保留七个标准库 CLI 及必要资源；证据待审状态不因结构检查通过而清除。 |
| [msimchowitz/writing-skills，固定提交](https://github.com/msimchowitz/writing-skills/tree/214981fe02326f27b0fc8790d00eb4b731607073/for-agents/literature-review) | `literature-review` | [MIT](skills/literature-review/LICENSE) | 轻量技术／叙述综述，复用已有主张与来源记录，适配实际输出格式；不默认声称系统综述或强制 LaTeX 与未部署写作依赖。 |
| 本地编写；[固定方法来源](skills/research-code-style/references/provenance.md) | `research-code-style` | [MIT](skills/research-code-style/LICENSE)及 [ATTRIBUTION](skills/research-code-style/ATTRIBUTION.md) | 科研代码短小直白、参数可见、数据变换顺序明确，按数值行为选择必要检查；不引入方法来源的发行、CI、copier 或记忆流程。 |
| [openai/skills，固定提交](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf) | `pdf` | [Apache-2.0](skills/pdf/LICENSE.txt) | 按实际目标选用提取、生成、渲染；移除管理员安装示例和固定路径，使用现有工具，按改动范围检查页面。保留许可证与 UI 资源。 |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | `experiment-plan` | [MIT](licenses/wanshuiyin-research-LICENSE) | 改为任务内研究记录，去除不存在的上游命令和输出协议依赖；规划不授权运行实验。 |
| [msimchowitz/writing-skills](https://github.com/msimchowitz/writing-skills) | `presentation-making` | [MIT](licenses/msimchowitz-writing-skills-LICENSE) | 反馈先作为当前任务规则；跨任务复用或长期记忆须另行确认。 |
| [JetBrains/skills](https://github.com/JetBrains/skills)（`slides` 元数据注明 OpenAI 来源） | `slides`、`slidev` | [Apache-2.0](skills/slides/LICENSE.txt)、[MIT](skills/slidev/LICENSE.md) | `slidev` 仅用于明确要求的网页演示；可编辑 PPTX 优先用 `slides`。 |
| [OthmanAdi/planning-with-files，固定提交](https://github.com/OthmanAdi/planning-with-files/tree/51c1caa27f9fefe259e45a7cc92fa79ee8787cd7) | `planning-with-files` | [MIT](skills/planning-with-files/LICENSE) | 复用已有记录、隔离任务；本地标准库 helper 提供会话绑定和两个只读状态 Hook，接入方法见包内 helpers、hooks 和 source 参考。 |
| 本地编写；[固定方法来源](skills/reference-style-alignment/references/sources.md) | `reference-style-alignment` | [CC0-1.0](skills/reference-style-alignment/licenses/synthesis-CC0.txt)、[MIT／voice-builder](skills/reference-style-alignment/licenses/voice-builder-MIT.txt)、[MIT／imagine](skills/reference-style-alignment/licenses/imagine-MIT.txt) | 将参考特征转换为写作、图像、数据图、PPT 制作约束，复用现有生成能力；保留三个方法来源的完整许可，不引入其账号或服务路由。 |

本地自编部分保留现有授权状态。Skill 文本不增加操作权限；部署方法见 [跨机器部署指南](codex/PORTABILITY.md)。阶段日志、临时审查与验收材料保留在各机器本地，不随框架分发。
