# 固定来源与本地适配

- 上游：[OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files)。固定提交 `51c1caa27f9fefe259e45a7cc92fa79ee8787cd7`，上游版本 `3.21.0`，核对日期 2026-10-01。
- 原路径：`skills/planning-with-files/`。三个模板保留上游目标／下一步／阶段、发现／决定、进展／检查的结构并按本地协作约定改写；入口是本地适配。
- `scripts/planning.py` 与回归检查为本地编写，受上游显式计划绑定、阶段解析和只读注入思路启发；未声称与上游脚本行为等价。完整上游 MIT 许可（Copyright (c) 2026 Ahmad Adi）保留在本包 `LICENSE`。
- 原包通过系统 `skill-installer` helper 的固定提交下载模式取得，下载与临时解包均置于真实用户主目录内。复制前检查目标路径和符号链接依赖。
- 审读原入口、三个模板、`resolve-plan-dir.sh`、`phase-status.sh` 与 `inject-plan.py` 后，保留对本地需求有用的机制；没有执行这些候选上游脚本。
- 不复制整套多宿主发行包装、共享 active pointer、自动账号服务、停止门禁、会话库回放及缓存注入链。入口不声明客户端专有的 hooks 或 allowed-tools 字段。
- hooks 是另外的可选集成；本包不自动改用户配置或授予信任。客户端核对结果和真实检查范围由仓库来源记录随交付更新，不以文本声明冒充已部署或已验证。
