# 来源与适配范围

本 Skill 按已批准的六项科研代码规则重新编写；数值例子为本地原创。方法借鉴 [a-attia/scicomp-research-skills 的 research-software-engineering](https://github.com/a-attia/scicomp-research-skills/blob/8435b16d91972c4f31b006de7bcacf1f5eb47e8e/skills/research-software-engineering/SKILL.md)，固定提交 `8435b16d91972c4f31b006de7bcacf1f5eb47e8e`，以及 [Scientific Python 官方设计建议](https://learn.scientific-python.org/development/principles/design/)（2026-10-01 读取）。官方指南只作为方法参考，未复制其正文或代码。

借鉴范围：常见数据类型、直白函数、具名参数、I/O 与计算边界、数值正确性证据及有依据的预期值。触发收窄为研究脚本、仿真和数值变换；保留有效的现有类、模块、接口与实验记录，验证按实际行为影响选择。没有引入上游打包、CI、copier 模板、固定目录、自动记忆、强制提交或跨 Skill 自动加载流程；这些来源不扩张任务权限。

上游根 [LICENSE](../LICENSE) 与 [ATTRIBUTION.md](../ATTRIBUTION.md) 原字节保留；MIT 版权包括 Master-cai（上游）与 A. Attia（分支新增）。ATTRIBUTION 讲述上游仓库的历史及其引用，里面的仓库路径、命令和模板说明不表示本 Skill 也包含或运行这些资源。

固定源原始字节的 SHA256（文件通过 raw.githubusercontent.com 的固定提交地址获取）：

| 源文件 | SHA256 | 字节数 |
|---|---|---:|
| `upstream-SKILL.md` | `c42b7ebad417f966d3b7a02b65d8c6bfdeb186f85b746ef5def6e32b3418ade8` | 17335 |
| `LICENSE` | `1c985e9d9c2ad214011492456817aadcd4b678c3ce4d4c8460fb48095e4978e8` | 1151 |
| `ATTRIBUTION.md` | `3c58be76e733d882c3e5943aaecd88f1ae1eb8c3b446123c1ed1714b2ee6c2b8` | 10482 |

其中 `upstream-SKILL.md` 指固定提交内 `skills/research-software-engineering/SKILL.md`，仅用于来源审阅，未随本 Skill 分发全文。LICENSE 与 ATTRIBUTION 对应上游根目录同名文件。未引入上游数值参考示例中的 `np.fsum`；本地例子使用标准库 `math.fsum`。
