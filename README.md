# vrl-python
VRL Python SDK

基于 PyO3 的 Vector Remap Language (VRL) Python 绑定，面向第三方脚本直接调用。

## 安装 / Install

- **包名 / Package:** `vrl-python`
- **导入 / Import:** `vrl_python`

```bash
# pip
pip install vrl-python

# uv
uv add vrl-python

# Poetry
poetry add vrl-python
```

> 运行环境 / Requirements: Python >= 3.8

---

## 第三方脚本示例（核心）/ Third-party script example (core)

以下示例展示如何在你自己的脚本中编译与执行一段 VRL，对输入事件进行转换，并拿到执行结果与耗时。

```python
# 中文：在脚本中一次性编译并执行 VRL，并打印结果
# English: One-shot compile and execute VRL in your script and print results
from vrl_python import VRLRuntime

PROGRAM = ".greeting = upcase!(.name)"
EVENT = {"name": "vector"}

# 便捷方法：无需实例化，直接运行 / Convenience: run without creating an instance
result = VRLRuntime.run(PROGRAM, EVENT, timezone="UTC")

print("processed_event:", result.processed_event)  # {'greeting': 'VECTOR', 'name': 'vector'}
print("runtime_result:", result.runtime_result)    # 最后一个表达式的值 / value of last expression
print("elapsed_ms:", result.elapsed_ms)            # 执行耗时（毫秒）/ elapsed time in ms
```

如果你需要在同一个进程内多次处理事件（复用编译结果），可以实例化 `VRLRuntime`：

```python
# 中文：复用运行时以避免重复编译；English: reuse runtime to avoid recompilation
from vrl_python import VRLRuntime

runtime = VRLRuntime(timezone="Asia/Shanghai")  # 默认使用系统/UTC；Default is system/UTC
program = ".field = to_int!(.field)"

events = [{"field": "1"}, {"field": "2"}]
for e in events:
    r = runtime.execute(program, e)
    print(r.processed_event)
```

---

## 语法检查 / Syntax check

```python
from vrl_python import VRLRuntime

diagnostic = VRLRuntime.check_syntax(".parsed = parse_json(.message)")
if diagnostic is None:
    print("✅ 语法正确 / Syntax OK")
else:
    print("❌ 错误 / Errors:", diagnostic.messages)
    print(diagnostic.formatted_message)  # 详细定位 / detailed location
```

---

## 异常与返回类型 / Exceptions and return type

- **VRLResult 字段 / VRLResult fields**
  - `processed_event`: VRL 执行后的事件字典 / processed event dict
  - `runtime_result`: 最后一个表达式的值 / value of the last expression
  - `elapsed_ms`: 执行耗时（毫秒，可选）/ elapsed time in ms (optional)

- **异常 / Exceptions**
  - 语法错误或运行时错误会以 Python 异常抛出（如 `ValueError` / `RuntimeError`）。
  - 建议在脚本中使用通用捕获：

```python
try:
    res = VRLRuntime.run(".x = to_int!(.x)", {"x": "not-int"})
except Exception as e:
    print("执行失败 / failed:", e)
```

---

## 兼容性 / Compatibility

- Python >= 3.8
- macOS / Linux / Windows（随预编译轮子发布）

---

## 贡献 / Contribute

- **步骤 / Steps**
  - Fork 仓库并创建分支 / Fork and create a feature branch
  - 完成修改并补充/更新测试 / Implement changes with tests
  - 本地通过格式化、检查与测试 / Pass format, checks and tests locally
  - 提交 Pull Request（简述动机与变更）/ Open PR with motivation and changes

- **开发脚本 / Dev scripts**
  - `make install`：安装开发依赖 / install dev deps
  - `make dev`：本地开发构建 / local dev build
  - `make test`：运行测试 / run tests
  - `make check`：格式化+检查+测试 / fmt+lint+test

---

## 技术参考 / References

- https://vector.dev/docs/reference/vrl/
- https://pyo3.rs/
- https://github.com/vectordotdev/vrl

## 许可证 / License

MIT