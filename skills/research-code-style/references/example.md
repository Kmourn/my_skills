# 可手算的数据变换例子

只在需要展示参数、单位和处理顺序时读此例。它使用 Python 标准库；实际项目已有 NumPy、表格或其他语言时沿用现有类型与接口。

问题：输入为 `(样本 ID, 摄氏温度)`；缺失值已约定为 `None`。先去掉缺失，再按摄氏阈值筛选，转换为开尔文后求算术平均。ID 随温度保留，原始输入不变。

```python
import math


def select_kelvin(rows, *, min_celsius):
    observed = [(sample_id, celsius) for sample_id, celsius in rows
                if celsius is not None]
    if not all(math.isfinite(celsius) for _, celsius in observed):
        raise ValueError("observed Celsius temperatures must be finite")
    selected = [(sample_id, celsius) for sample_id, celsius in observed
                if celsius >= min_celsius]
    return [(sample_id, celsius + 273.15) for sample_id, celsius in selected]


def mean_kelvin(rows):
    if not rows:
        raise ValueError("no temperature samples remain after filtering")
    return math.fsum(kelvin for _, kelvin in rows) / len(rows)


raw = [("a", -10.0), ("b", None), ("c", 10.0), ("d", 20.0), ("e", 30.0)]
min_celsius = 10.0
selected = select_kelvin(raw, min_celsius=min_celsius)
mean = mean_kelvin(selected)
print(min_celsius, selected, mean)
```

可手算的期望：阈值 10 保留 `c,d,e`，开尔文为 `283.15,293.15,303.15`，均值 `293.15 K`。只把 `min_celsius` 改为 20，保留 `d,e`，均值 `298.15 K`。保持阈值为 10 的两次运行应相同。将摄氏阈值误用于转换后的开尔文会连 `a` 也保留，这组数据能检查处理顺序。

如需验证此例，用上述手算值与 ID 检查：浮点结果可用 `math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-10)`。这里的绝对容差远大于约 300 K 数量级下的机器舍入量，又远小于 5 K 的参数变化；不能把它照搬为其他算法或测量误差的标准。数值采用 Python `float`，累加用 `math.fsum`；本例没有随机步骤或数据划分，不添加无作用的种子参数。

实际实验在已有记录中写入使用的阈值、单位、缺失处理、输入版本、代码版本和输出位置；无需为这段说明另建记录。此例只展示变换与参数，不证明真实数据的缺失机制、阈值选择或研究假设合理。
