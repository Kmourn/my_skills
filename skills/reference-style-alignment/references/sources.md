# 来源与本地改写

核对日期：2026-10-01。本 Skill 的共同入口、数据图及 PPT 分支由本地编写；写作与图像分支借鉴下列已固定的许可方法。原包正文仅保存在本机审核缓存，未部署为可执行 Skill，也未采用其生成服务、依赖路由或后台任务。

| 方法来源与固定提交 | 实际参考文件 | 使用范围 | 完整许可 |
| --- | --- | --- | --- |
| synthesisengineering/synthesis-skills，`78a73089390816df0e859b34f0251fffa36125e6` | [synthesis-voice-profiler/SKILL.md](https://github.com/synthesisengineering/synthesis-skills/blob/78a73089390816df0e859b34f0251fffa36125e6/skills/synthesis-voice-profiler/SKILL.md) | 跨文体观察词汇、句法、结构、修辞与口吻；本地改为任务内规范，去除样稿字数／数量要求和自动写入 AGENTS.md。作者 Rajiv Pant。 | [CC0-1.0](../licenses/synthesis-CC0.txt)，原文件 `LICENSE-CC0` |
| social-media-skills/skills，`6e30eeb2f6736bda8683b6bbaa674af3641d7945` | [voice-builder/SKILL.md](https://github.com/social-media-skills/skills/blob/6e30eeb2f6736bda8683b6bbaa674af3641d7945/skills/voice-builder/SKILL.md)、[validation.md](https://github.com/social-media-skills/skills/blob/6e30eeb2f6736bda8683b6bbaa674af3641d7945/skills/voice-builder/references/validation.md) | 观察必须有样稿依据，生成新内容后逐特征对照；去品牌依赖、私人身份推断、固定通过次数和不可辨识承诺。 | [MIT](../licenses/voice-builder-MIT.txt)，保留 Frank Heijdenrijk 的完整版权和许可 |
| indigokarasu/imagine，`495b9867ef71181f32c385c8a32691dcf8a8873a` | [SKILL.md](https://github.com/indigokarasu/imagine/blob/495b9867ef71181f32c385c8a32691dcf8a8873a/SKILL.md)、[style_prompt_guide.md](https://github.com/indigokarasu/imagine/blob/495b9867ef71181f32c385c8a32691dcf8a8873a/references/style_prompt_guide.md) | 分开参考风格与目标主体，观察构图、光影、配色、媒介与平衡；取消固定字符数、强制跨会话测试、风格库及日志路由。 | [MIT](../licenses/imagine-MIT.txt)，保留 Indigo Karasu 的完整版权和许可 |

适配正文为重新编写的任务方法，不照搬上游运行入口。本地制作接口为当前可用的 `imagegen`、`scientific-visualization`、`presentation-making`、`slides`，以及确有科研写作需求时的 `scientific-writing`；每次核对是否实际可用，再加载相关 Skill。上游许可不增加未来样稿外发、全局指令修改或付费服务使用权限。

核心不新增运行依赖、脚本、自动 hook 或生成引擎。样稿全文、个人画像、试用产物和下载缓存留在任务允许的本地位置，不进入本包。检查与行为试用证据由框架维护记录保存，不能将静态入口校验描述成所有模态生成效果已验证。
