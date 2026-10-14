# 记录选择、路径与证据

## 调用与绑定

POSIX 示例：`python3 -I <skill-dir>/scripts/planning.py <command> [options]`。使用实际可用的 Python 3.10+ 解释器，标准库；`-I` 防止项目目录和 `PYTHONPATH` 替换依赖。其他平台按实际启动器调用核心 CLI；`hooks-template` / `configure-hooks` 只支持 POSIX shell，非 POSIX 提前退出 2 且不写配置。非 POSIX 核心路径未实机验收。

| 命令 | 行为 |
|------|------|
| `paths` | 打印实际用户主目录与展开后的 `CODEX_HOME`；不创建目录、不读会话库 |
| `list` | 只读列出当前项目根计划及 `.planning/<id>/task_plan.md` |
| `select` | 打印选定记录路径；不改变共享指针或父进程环境 |
| `init` | 显式创建命名任务的单个计划文件；存在时原样复用；`--record` 仅复用现有记录 |
| `status` | 打印阶段、下一步、记录 hash 与可选证据状态；始终保留 `task_completion: requires_review` |
| `print` | 打印选定记录；常规 `task_plan.md` 可附同目录已有 findings/progress |
| `bind` | 把当前或显式 `--session` 会话绑定到明确 record/task；只写该会话的本地元数据 |
| `unbind` | 删除当前或显式 `--session` 会话的绑定，不影响其他会话 |
| `hook` | 接收核实支持的客户端事件，只读打印结构化上下文；详见 hooks 说明 |
| `hooks-template` | 向 stdout 生成可选 JSON 片段；不写或启用任何配置 |
| `configure-hooks` | 从当前 helper 路径生成两事件，备份并幂等合并 HOME 内指定 hooks.json；不授予信任 |

项目根：显式 `--project` 优先，否则使用 `PWF_PLAN_ROOT`，再否则当前目录。`PWF_PLAN_ROOT` 必须能展开为绝对路径，不递归搜索任意子项目。记录绑定：显式 `--record` 或 `--task` 优先，未给时读取 `PWF_RECORD` 或 `PLAN_ID`，两者同时设置则报错。`--record` 可以是绝对路径或项目相对路径；文件必须存在且解析后位于所选项目内。

`--task <id>` 严格选择 `.planning/<id>/task_plan.md`，失败不选其他任务。ID 允许字母、数字、下划线开头，后接字母、数字、点、下划线或短横线，禁止路径分隔符。普通 `select` / `status` / `print` 无选择时，只有一个命名计划且无根计划才能自动选它；只有根 `task_plan.md` 时选根计划；多个候选要求显式选择。`.active_plan` 不参与选择。`bind` 不接受单份记录推断；`hook` 只接受 CLI/env 显式选择或 stdin 会话 ID 对应的既有绑定。

并行会话可在同一项目分别 `bind --task <id>` / `bind --record <path>`。省略 `--session` 时只接受唯一的 CODEX_SESSION_ID/CODEX_THREAD_ID 或两者相等的值；不同时必须显式指定目标 hook 的 session_id。绑定只保存会话 ID、项目与解析后的实际记录路径，默认位置为实际 CODEX_HOME 的 `planning-with-files/bindings/`，每会话独立文件。完整规则与命令见 [hooks.md](hooks.md)。`select` 和工具子进程里的 `export` 不会改变已运行客户端父进程环境。多人同一任务只有一人写共享记录。

`--session` 仅用于 bind/unbind。hook 不接受该参数：CLI/env record/task 仍优先；需要查 registry 时，会话 ID 只来自 stdin。当前全局模板不固定 record/task；非法 hook 参数会静默跳过。

## 写入与打印边界

仅显式 `init`、`bind` / `unbind`、`configure-hooks` 写文件，全部写入限真实用户主目录。`init` 同时核对项目范围，拒绝符号链接解析到边界外的目标；不覆盖已有记录，重复调用返回 `created: false`。`bind` 同记录重复调用返回 `changed: false`；改变记录只替换该会话元数据，`unbind` 无绑定返回 `removed: false`，不创建目录。hook 纯只读，不自动修复、写回或初始化 registry。

路径会展开变量及 `~`。`CODEX_HOME` 非空时用于实际客户端目录解析，为空取真实主目录下 `.codex`；它不扩大写入边界，也不是项目记录存储位置。`paths` 只读打印实际 HOME、CODEX_HOME 与默认 registry/hooks 文件路径。需要缓存隔离时显式传 `--registry <home-cache>/bindings`；配置试用使用 `configure-hooks --hooks-file <home-cache>/hooks.json`，不重定向 HOME/CODEX_HOME。POSIX 真实主目录来自当前 UID 的账户记录。非 POSIX 使用 `Path.home()`，未在本轮验证。

读取要求项目内普通文件，单份记录上限 4 MiB。`print` / hook 默认输出最多 16000 个字符；`--max-chars` 可设 512–65536，截断明确标记，续接时再读完整文件。自定义记录只打印自身，不猜测或读取周围的日志。标准库实现核对解析后的符号链接边界，并不承担抵御其他本地用户同时恶意替换路径的安全沙箱职责。

## 阶段解析与完成证据

结构化阶段识别 `### Phase 1: …` 或 `### 阶段1: …`，每阶段一行 `- **Status:** pending`（或 `in_progress` / `complete` / `blocked` / `unverified`）。无阶段、缺失或重复 status 返回 `unknown`；代码块里的示例不计入阶段。`## Next Step` 或 `## 下一步` 提供单一步。任意已有格式仍可直接 `print` 和人工读取，不要求迁移。

`phase_state: all_marked_complete` 仅是阶段标记结果。未勾选要求仍随 `unchecked` 暴露，实际完成判断由责任成员核对用户目标、结果与版本。没有证据 JSON 时 `evidence.state: unverified`，即使所有阶段 complete 也不能称为测试通过。

若需要可重算的证据快照，显式使用 `status --evidence checks.json`。不要为每个任务强制新增它；项目已有检查记录可以继续使用。最小 schema：

```json
{
  "checks": [
    {
      "name": "actual regression run",
      "result": "passed",
      "inputs": [{"path": "src/example.py", "sha256": "<64 lowercase hex characters>"}],
      "artifact": {"path": "validation/run-output.txt", "sha256": "<64 lowercase hex characters>"}
    }
  ]
}
```

`result` 为 `passed` / `failed` / `unverified`。`passed` 要求至少一个输入内容快照和输出产物快照；路径相对所选项目或为其内绝对路径。helper 核对当前内容 SHA-256，当前一致为 `current_recorded_pass`，变化或缺失为 `stale_or_missing`；任何失败／未验证仍原样保留。快照对应实际受检查的源码、测试及相关输入，不能只记计划自身或不相关文件。

这个机制验证**记录的快照仍匹配**，不证明产物里真的通过、检查覆盖充分或完整版本被枚举。责任成员仍须核对实际命令、输出、覆盖范围和没有登记的相关变化。`task_completion` 始终为 `requires_review`，避免把内容 hash 或阶段 complete 冒充自动验收。

普通 CLI 选择／读取／配置错误退出 2 并说明原因；hook 出错时 stdout/stderr 为空且退出 0，不阻挡正常工作，也不替换为另一任务。
