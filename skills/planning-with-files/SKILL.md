---
name: planning-with-files
description: 用磁盘记录组织跨阶段、跨会话的长任务，续接已有计划、发现和进展，并隔离多个任务的记录；可选 helper 打印所选状态，客户端核实支持后可接入 hooks。小任务不强制新建记录。
metadata:
  upstream-version: "3.21.0"
  upstream-commit: "51c1caa27f9fefe259e45a7cc92fa79ee8787cd7"
---

# Planning with Files

把长任务的目标、阶段、决定、证据与下一步留在磁盘上，续接时以实际文件和产物恢复状态。来源为 [OthmanAdi/planning-with-files v3.21.0](https://github.com/OthmanAdi/planning-with-files/tree/51c1caa27f9fefe259e45a7cc92fa79ee8787cd7)，本地适配与保留范围见 [references/source.md](references/source.md)，完整 [MIT 许可](LICENSE) 随包保存。

## 选择与续接

1. 先读用户指定的进展文件、项目记录与当前任务产物。已有记录能够承载当前任务时直接复用；小任务可直接完成，不因工具调用次数增加流程。
2. 明确当前任务对应的记录。单份记录可以同时包含计划、发现和进展；发现或日志较多时再分开。独立任务使用不同记录或 `.planning/<task-id>/`，不让根目录计划覆盖已明确选定的任务。
3. 从记录恢复目标、已确认选择、当前阶段、完成证据、未完成项和**一个下一步**，核对实际修改与结果版本。状态过时就修正记录；未执行的检查仍是未验证。
4. 一名责任成员写共享记录；其他成员回报结果或写各自获分配的文件。hook 只读输出，不承担多人合并或写入锁。

项目已采用其他格式时保留格式、文件名和位置。helper 的结构化解析只支持下述模板中的阶段标题；无法识别的记录可以打印和人工续接，不将解析失败当成任务完成。

## 工作期间

- 按实际依赖组织阶段，不规定固定阶段数、查看次数或失败次数。出现有意义的决定、阶段成果、检查或交接时更新对应记录。
- 记录发现的来源和限制、实际执行及失败、产物路径与对应内容版本。重试由原因与授权决定；需要新的权限或关键输入时再向用户说明。
- 每次阶段切换同时更新下一步。用户追加工作时扩展同一任务的阶段；独立任务另选记录。
- 所有阶段标为 `complete` 仅表示计划中的阶段已标记完成。交付还须核对实际需求、产物和检查对应的内容版本；代码变化后，受影响的旧检查不能继续充作当前通过证据。
- 这些记录与脚本不增加安装、实验、设备、外发、推送或部署权限。写入边界遵循当前任务约定，`CODEX_HOME` 不改变真实用户主目录边界。

## 模板与 helper

只复制需要的模板，已有内容不覆盖：

- [templates/task_plan.md](templates/task_plan.md)：目标、阶段、单一步与完成依据。
- [templates/findings.md](templates/findings.md)：来源、发现与决定。
- [templates/progress.md](templates/progress.md)：执行、失败与对应版本的检查。

`scripts/planning.py` 仅依赖 Python 3.10+ 标准库。下面的 `<skill-dir>` 指当前 `SKILL.md` 所在目录，`<project>` 指明确选定的项目目录；先解析真实路径，不假定固定用户名。

```bash
# 只读查看任务清单；显式复用任意现有记录，绝不重写它
python3 -I "<skill-dir>/scripts/planning.py" list --project "<project>"
python3 -I "<skill-dir>/scripts/planning.py" print --project "<project>" --record records/progress.md

# 仅当需要新任务记录时：创建一个计划文件，不自动创建其余两份
python3 -I "<skill-dir>/scripts/planning.py" init --project "<project>" --task api-migration --title "API migration"
python3 -I "<skill-dir>/scripts/planning.py" status --project "<project>" --task api-migration
```

选定方式、路径约束、证据 schema 和命令细节见 [references/helpers.md](references/helpers.md)。helper 无网络调用、不读取会话库、不运行 Markdown 中的命令；除显式 `init` 外不写文件。

## 可选自动注入与历史

先核对实际客户端版本、事件、配置发现及输出协议，再决定是否使用 [references/hooks.md](references/hooks.md) 中的可选方案。安装 Skill 本身不启用 hooks。没有 hook 支持时直接读记录或调用 `print`；无需为普通任务安装 hook。

磁盘记录续接与历史回放是两项独立功能。本包不默认读取、扫描或合并 Codex/其他客户端会话库，也未分发上游历史回放脚本。只有用户明确要求查阅历史时，才另行确定实际客户端存储与授权范围；可先使用用户指定的导出文件，历史片段作为待核对材料，不作为已完成证据。
