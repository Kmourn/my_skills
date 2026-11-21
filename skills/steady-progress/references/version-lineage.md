# 项目版本谱系

- **只画影响决策或结果解释的版本。** 沿用项目标识。种子、重跑和续训留在运行记录。
- **区分继承、借用和结果启发。** 实线表示继承，虚线注明借用或启发。每条关系链接依据，证据不足时标为待核实。
- **记录问题、改动和取舍。** 拟议方案写继续条件，完成后记结果与采用、暂缓或归档的依据。标出当前基准及论文或发布采用的版本。
- **复用已有 Markdown 索引。** 按需用 Mermaid 展示分叉，图下链接证据。核对边的方向和链接。[GitHub Mermaid 文档](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)

```mermaid
flowchart LR
    A["A｜当前基准"] --> B["B｜新模块"]
    A --> C["C｜替代损失"]
    A --> D["D｜精简结构"]
    D -->|从 D 派生| E["E｜组合候选，待验证"]
    B -. 借用模块 .-> E
    C -. 结果启发 .-> E
```
