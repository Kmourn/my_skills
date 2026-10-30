# 跨机器部署与核对

框架跟随当前用户指定的仓库、客户端安装位置和实际工具环境，不绑定账户、主机或目录名。根索引按通用、工程、科研、汇报组织；各 Skill 按任务加载。

## 路径与迁移范围

- 仓库根从当前工作树或用户指定位置确认；推送目标从已核实的 SSH remote 或用户明确目标确认，不从目录名、历史提交或来源记录推断。
- 当前可用 Skill 清单提供的路径优先。Codex 主目录使用非空 `CODEX_HOME`，否则当前真实主目录下 `.codex`；先展开环境变量与 `~`，核对客户端实际发现的位置和允许写入范围。
- 迁移 `codex/AGENTS.md` 到客户端 `AGENTS.md`，以及本次采用的 `skills/<name>/` 完整必要文件。许可、来源、引用、模板和脚本随包保留。
- `ieee-polishing` 还依赖同级 `skills/_shared/` 中的共享参考与许可，须一起部署；`_shared` 是支持目录，不作为独立 Skill 调用。DeepSeek 写作协作复用目标机器现有 API 配置，不迁移凭据或机器绑定的调用脚本。
- `ieee-polishing` 的人主导修稿入口引用同级 `scientific-writing/references/human-directed-revision.md`，须保留该参考及其 MIT 许可。沿用目标环境已有的 VS Code、LaTeX Workshop 和项目编译入口；部署 Skill 不安装扩展或 TeX 工具，也不表示已通过论文编译验收。
- `research-cycle`、`hypothesis-generation`、`literature-review`、`scientific-critical-thinking`、`experiment-plan` 共用 `skills/_shared/references/research-value-and-differentiation.md`，采用其中任何一个 Skill 时须随包部署这份共享文件。保留 `_shared` 中其他已部署的参考与许可，不整目录覆盖目标。
- 同步前比较目标。存在本地补充或修改时核对来源与当前用户决定；保留无关 Skill、客户端配置、系统 Skill 和插件，不整体覆盖客户端目录。
- 个人记忆、会话、凭据、registry 绑定、旧机器 `hooks.json` 和信任状态是本机状态，不作为可迁移框架文件。

框架当前采用真实用户主目录写入政策、不使用 sudo。它是运行策略，不是用户名；`CODEX_HOME` 不能自行扩大边界。目标在允许范围外时保留仓库成果，说明具体冲突，不能用伪造 HOME 绕过检查。

## 环境与平台

先检查实际任务所需工具，复用项目已有环境。`python3`、Bash、`<venv>/bin/python` 是 POSIX 示例；其他平台使用实际可用的 Python 启动器、解释器路径和 shell。平台上没有名为 `python3` 的命令不等于没有 Python。

- planning helper 核心要求 Python 3.10+ 标准库。POSIX 真实主目录来自账户记录；非 POSIX 路径分支尚未实机验收。
- planning 的 `hooks-template`／`configure-hooks` 只生成 POSIX shell 命令；非 POSIX 明确报错且不写配置。Windows 原生 Hook 不属于当前支持范围，不能把 shell 引号差异当成客户端已兼容。
- 本地 command hooks 还需要客户端实际支持本地编排、配置发现、协议和正常信任流程。获准接入时，从目标机器最终安装路径和实际 Python 解释器重新生成，不复制旧机器的绝对命令或信任状态。
- 科研 helper 的核心 Python 要求与可选格式／统计库要求分别看各包 metadata。日期版本表和 pins 是当时核对的快照，不是所有机器的强制安装清单，也不是完整跨平台锁文件。沿用已有受支持环境；确有安装需要时使用项目可用管理器和允许目录。
- PDF／Slides 依赖按任务选择 Poppler、LibreOffice、字体、Python 库、Node／PptxGenJS。调用前把工具所需临时目录与缓存放进允许的任务目录：POSIX 可用 `TMPDIR`，Windows 按工具使用 `TEMP`／`TMP`。确认子进程行为，不能仅设置 Python 临时目录就宣称全部依赖不会另写缓存。
- DataLad Skill 的说明与方法不等于运行依赖已安装。数据操作需要可用 DataLad、Git 和 git-annex；容器扩展可选。按平台和项目核对版本、后端及实际数据权限，安装 Skill 不增加 clone/get/run/rerun/publish 的授权。

## 交付与同步

1. 先在框架仓库完成本次改动和相称检查，保留必要来源与许可。
2. 提交本次相关文件，通过已核实的 SSH remote 推送任务子分支，核对远端提交；失败时保留仓库成果。
3. 成功后仅按本次范围同步客户端 AGENTS.md 和框架 Skill。临时文件与备份位于允许目录；不覆盖未核对的本地变化。
4. 逐文件比较内容和必要执行权限，特别核对仓库 `codex/AGENTS.md` 与客户端 `AGENTS.md`。检查所引用的本地资源仍随包存在。
5. 在客户端实际重新加载后核对发现与调用；“已复制”不作为客户端功能或数据运行验收。

文档整理只需路径、链接与结构检查；修改可执行代码则验证受影响行为。Linux 回归、模拟平台分支和历史宿主验收分别报告，均不能冒称 macOS／Windows 或第二机器实测。

## 信息清理范围

仓库当前文件使用通用路径和任务目标，必要的公开上游署名、版权、许可和来源继续保留。删除当前文件中的个人标识不会抹除已有 Git 历史或改变本地 `.git` 的推送配置；历史重写和远端清理需独立确定范围，不能混入普通同步。
