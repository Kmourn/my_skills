# 可选 Codex hooks

本包提供只读注入 helper、显式会话绑定与配置命令。安装 Skill 不会启用 hooks。2026-10-02 核对的 [OpenAI Hooks 文档](https://learn.chatgpt.com/docs/hooks) 说明：本地 command hooks 适用于编排和执行均在本地的线程；云编排即使在本地执行工具，也不支持这类 hooks。先核对实际客户端的运行方式、配置发现与信任流程。

## 本轮核对的协议

2026-10-01 核对本机 bundled `codex-cli 0.159.2` 的 hooks feature/schema。MVP 使用 `SessionStart` 与 `UserPromptSubmit`；stdin 为单个 JSON，helper 只取 `cwd`、`hook_event_name` 和 `session_id`，忽略 `transcript_path`、用户 prompt 和工具参数。stdout 使用：

```json
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"selected planning content"}}
```

注入只来自明确选择的磁盘记录。hook 优先使用 `--record` / `--task`，其次使用宿主的 `PWF_RECORD` / `PLAN_ID`；没有这些选择时，只按 stdin 的 `session_id` 查显式绑定。即使磁盘上只有一份记录，未绑定也输出为空。错误选择不会回退到 registry 或其他记录。helper 不做 Stop 门控、不执行 Markdown 中的命令、不读会话库；hook 本身不创建目录、更新绑定或写回记录。记录是任务数据，不增加权限。

`--session` 仅适用于 bind/unbind；hook 不接受该参数，其 registry 会话来源只取 stdin。hook 的非法参数同样静默跳过。

## 同项目多会话绑定

在明确选择当前记录后，对每条会话分别执行：

```bash
python3 -I "<installed-skill-dir>/scripts/planning.py" bind --project "<project>" --record records/progress.md
# 也可以显式绑定已有命名任务
python3 -I "<installed-skill-dir>/scripts/planning.py" bind --project "<project>" --task api-migration
```

未给 `--session` 时，命令只接受 `CODEX_SESSION_ID` / `CODEX_THREAD_ID` 中唯一的非空值或两个相等值。主线程可能相等，子线程可能不同；两个值不同时报错，要求使用目标 hook 的 `session_id`，不猜父子身份：

```bash
python3 -I "<installed-skill-dir>/scripts/planning.py" bind --session "<hook-session-id>" --project "<project>" --record records/progress.md
python3 -I "<installed-skill-dir>/scripts/planning.py" unbind --session "<hook-session-id>"
```

`bind` 必须有明确的 record/task（也可来自 `PWF_RECORD` / `PLAN_ID`），不会从同项目单份记录自动绑定。`--task` 会解析成现有记录的真实绝对路径。每条会话在 `CODEX_HOME/planning-with-files/bindings/` 中使用独立文件，文件名为 ID 的 SHA-256；内容仅有版本、会话 ID、项目和记录路径。实际 `CODEX_HOME` 为空时取真实主目录下 `.codex`；registry 必须在真实用户主目录内。用 `paths` 可只读查看默认位置。

同一 ID 重复绑定相同记录不改文件；绑定其他记录只替换该 ID，解绑只删除该 ID。续接或 compact 仍用同一 ID 时复用绑定；fork 得到新 ID 时保持未绑定，不借用父会话或共享 active task。事件 cwd 必须位于绑定项目内；记录消失、路径变化、损坏元数据或跨项目事件均静默跳过。不要把工作仓库子目录当作项目根，除非实际事件 cwd 位于其中。

已采用且可信的本地任务，确定记录后绑定当前核实的会话；任务结束时解绑，避免下一项任务继续收到旧记录。普通 bind/unbind 不逐次增加审批；首次配置仍须有授权、支持核实与客户端正常信任审阅。

[OpenAI Hooks 文档](https://learn.chatgpt.com/docs/hooks) 明确子智能体 hooks 使用父 session_id。父会话映射由主控或指定责任成员 bind/unbind；子成员不自行重新绑定或解除父映射，以免子任务替换根任务。子任务记录仍按既有分工读写各自范围。

需要隔离试用时可用 `--registry "<home-cache>/bindings"`；生成模板、配置、绑定与 hook 调用都要选同一目录。自定义目录不要求改变 HOME 或 CODEX_HOME。子进程里 `export PLAN_ID=...` 或运行 `select` 不会改变已经运行的 IDE 父进程环境。

会话创建后的绑定无法补发已经结束的首次 SessionStart；后续 UserPromptSubmit 或同 ID 的续接事件才会读取绑定。

## 生成与幂等合并

先完成普通 `print` 与合成事件检查，再从最终部署路径生成片段：

```bash
python3 -I "<installed-skill-dir>/scripts/planning.py" hooks-template --python "<absolute-trusted-python>"
```

生成只打印 JSON，不写配置；当前默认全局模板不固定 record/task，使用每条会话的 registry 绑定（仍保留宿主显式选择的兼容能力），固定同一调用产生相同片段。确需项目专用模板可加 `--project <absolute-project>`；跨项目事件会跳过。静态 `--task` / `--record` 仍可用于明确固定任务的配置范围，但一个全局静态任务不能区分同项目并行会话。hook 命令通过 shell 参数引用生成，Python 与最终 helper 使用绝对路径及 `-I`。

模板 handler 使用 `additionalContextLimit: 0`。按本版本协议，这会关闭该 handler 的 additionalContext spill，而不是清空上下文；helper 自身把文本严格限制在 `--max-chars`（默认 16000）内，超限明确截断。它只避免这份 additionalContext 触发原生临时文件溢写，不证明宿主其他临时文件都在 HOME 内。若改为正值，先核对宿主溢写目录与当前写入边界。

已决定配置时，从最终部署的 helper 显式执行：

```bash
python3 -I "<installed-skill-dir>/scripts/planning.py" configure-hooks --python "<absolute-trusted-python>"
# 缓存中的合并试用；不改变真实客户端配置
python3 -I "<installed-skill-dir>/scripts/planning.py" configure-hooks --hooks-file "<home-cache>/hooks.json" --registry "<home-cache>/bindings"
```

默认合并实际 `CODEX_HOME/hooks.json`；`--hooks-file` 仅用于此命令，解析后的目标必须在真实用户主目录内。命令保留其他事件、其他 handler 与顶层配置，只替换两个 MVP 事件里可核验的本包未限定 matcher（空或 `*`）命令。识别要求同一 Python、`-I`、当前 helper 或 HOME 内字节完全一致的副本，以及本包生成的 hook 参数和 handler 字段；不按文件名或子串删除别家的命令。第一次改变现有配置前，备份其原始字节；重复调用不追加条目、不改文件、不新增备份。无法识别的配置结构、重复 JSON 键或解析错误会退出 2，保留原文件。

自定义 matcher、额外 handler 属性、shell 包装或不同内容的旧 helper 路径保持原样。若这些定义也注入同一记录，需在客户端核对重复项；本命令不替用户删除无法核验的定义。

本版本可从用户 `hooks.json`、可信项目的 `.codex/hooks.json` 或 inline `[hooks]` 发现配置；先查已有配置，选择一处集成，避免重复注入。`configure-hooks` 不修改 `config.toml` 或授予信任。新定义或定义变化通过客户端正常 `/hooks` 或 Hooks 设置审阅并信任；不生成 `trusted_hash`，不使用 bypass。[OpenAI Hooks 文档](https://learn.chatgpt.com/docs/hooks)

实际验收须在支持本地 command hooks 的客户端确认来源路径、事件、完整命令与信任状态，再用两条分别绑定的合成会话核对选定记录标记及 hook 完成结果。协议、helper 或原生 CLI 的通过不能证明另一条云编排线程已注入。

## 离线协议试用

将含 `cwd`、`hook_event_name`、`session_id` 的合成 JSON 通过 stdin 传给 `hook`，检查 stdout 的 `additionalContext` 只含该 ID 绑定的任务；CLI/env 直接选择也可单独验证。未知事件、损坏输入或绑定、失效记录均 stdout/stderr 为空且 exit 0，不阻断正常工作。stdin 上限 65536 字节，registry 单份上限 8192 字节，记录单份上限 4 MiB。普通记录续接始终可以直接 `print`，不依赖 hooks。
