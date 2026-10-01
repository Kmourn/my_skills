# 可选 Codex hooks

本包只提供只读注入 helper 与模板，安装 Skill 不会启用 hooks。以实际客户端的支持、配置发现与信任流程为准；不要把其他宿主的 frontmatter 自动 hooks 当作 Codex 功能。

## 本轮核对的协议

2026-10-01 核对本机 bundled `codex-cli 0.159.2` 的 hooks feature/schema，并读取 [OpenAI Hooks 文档](https://learn.chatgpt.com/docs/hooks)。MVP 使用 `SessionStart` 与 `UserPromptSubmit`；stdin 为单个 JSON，helper 只取 `cwd` 和 `hook_event_name`，忽略 `transcript_path`、用户 prompt 和工具参数。stdout 使用：

```json
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"selected planning content"}}
```

注入只来自明确选择的磁盘记录。hook 要求 `--record` / `--task` 或宿主的 `PWF_RECORD` / `PLAN_ID` 绑定；即使磁盘上只有一份记录，未绑定也输出为空。helper 不做 Stop/PreToolUse/PostToolUse 门控、不发继续请求、不执行 Markdown 中的命令、不创建缓存、不读取会话历史。未知事件与无法选择的记录不会注入其他任务。一个全局静态 `--task` 不能区分共享项目的并行会话。

## 生成与幂等合并

先完成普通 `print` 与合成事件检查，再从最终部署路径生成片段：

```bash
python3 -I "<installed-skill-dir>/scripts/planning.py" hooks-template --python "<absolute-trusted-python>"
```

生成只打印 JSON，不写配置；默认依事件 cwd 和宿主环境的显式绑定选择，固定同一调用产生相同片段。确需项目专用模板可加 `--project <absolute-project>`；跨项目事件会跳过。如果传 `--task` 或 `--record`，必须确认该配置范围内只有对应任务，或使用独立宿主配置。hook 命令通过 shell 参数引用生成，Python 与 helper 使用绝对路径及 `-I`。

模板 handler 使用 `additionalContextLimit: 0`。按本版本协议，这会关闭该 handler 的 additionalContext spill，而不是清空上下文；helper 自身把文本严格限制在 `--max-chars`（默认 16000）内，超限明确截断。它只避免这份 additionalContext 触发原生临时文件溢写，不证明宿主其他临时文件都在 HOME 内。若改为正值，先核对宿主溢写目录与当前写入边界。

应用模板属于另外的配置操作：先核对本机版本实际读取的 hooks 文件和开关及其信任机制，读取并保留已有 hook，再仅合并模板里的两个事件。同事件按 `type=command` 与**完整 command 字符串**去重；完全相同条目保留一次，其他条目原样保留。重跑不能重复追加，也不覆盖原有 hooks/其他配置。实际部署路径变化时移除或更新原有本包条目，不同时保留仓库与部署路径的两条注入器。

本版本可从 `CODEX_HOME/hooks.json`、可信项目的 `.codex/hooks.json` 或 inline `[hooks]` 发现配置；应先查已有配置，选择一处集成，避免重复注入。新命令或命令变化由用户在 `/hooks` 或宿主 Hooks 设置审阅并信任；不要生成 `trusted_hash` 或使用信任 bypass。Skill 不自行改 `config.toml` 或 hooks 文件。协议和模板的合成测试通过不等于真实客户端已加载或自动注入成功；本轮未执行真实宿主验收。

## 离线协议试用

将一个只含 `cwd` 与 `hook_event_name` 的合成 JSON 通过 stdin 传给 `hook`；在同项目多个任务时使用显式 `--task`，检查 stdout 的 `additionalContext` 只含选定任务。普通记录续接始终可以直接 `print`，不依赖 hooks。
