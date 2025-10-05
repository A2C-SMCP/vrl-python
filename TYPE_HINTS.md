# 类型提示支持 / Type Hints Support

VRL-Python SDK 提供完整的类型提示支持，通过 `.pyi` stub 文件为 IDE 和静态类型检查器提供准确的类型信息。

VRL-Python SDK provides complete type hints support through `.pyi` stub files, offering accurate type information for IDEs and static type checkers.

---

## ✨ 功能特性 / Features

- ✅ **完整的类型注解** / Complete type annotations
- ✅ **IDE 智能提示** / IDE IntelliSense support
- ✅ **静态类型检查** / Static type checking (mypy, pyright)
- ✅ **文档字符串** / Docstrings with examples
- ✅ **中英文双语注释** / Bilingual comments (Chinese & English)

---

## 📦 包含的类型文件 / Included Type Files

```
python/vrl_python/
├── __init__.py          # 主模块 / Main module
├── _vrl_python.pyi      # 类型存根文件 / Type stub file
└── py.typed             # PEP 561 标记文件 / PEP 561 marker
```

---

## 🎯 支持的类型 / Supported Types

### 1. VRLRuntime

```python
from vrl_python import VRLRuntime

# 类型提示会自动推断 / Type hints are automatically inferred
runtime: VRLRuntime = VRLRuntime()
runtime_with_tz: VRLRuntime = VRLRuntime(timezone="Asia/Shanghai")

# 方法调用有完整的类型提示 / Method calls have complete type hints
result = runtime.execute('.field = "value"', {})  # Returns VRLResult
success = runtime.compile('.field = "value"')     # Returns bool
```

### 2. VRLResult

```python
from vrl_python import VRLResult
from typing import Dict, Any, Optional

result: VRLResult = runtime.execute('.field = "value"', {})

# 所有属性都有类型注解 / All properties have type annotations
event: Dict[str, Any] = result.processed_event
runtime_result: Any = result.runtime_result
elapsed: Optional[float] = result.elapsed_ms
```

### 3. VRLDiagnostic

```python
from vrl_python import VRLDiagnostic
from typing import List, Optional

diagnostic: Optional[VRLDiagnostic] = VRLRuntime.check_syntax('.field =')

if diagnostic is not None:
    messages: List[str] = diagnostic.messages
    formatted: str = diagnostic.formatted_message
    colored: str = diagnostic.colored_message
```

### 4. 异常类型 / Exception Types

```python
from vrl_python import VRLCompileError, VRLRuntimeError

try:
    runtime.execute('.invalid syntax', {})
except VRLCompileError as e:
    print(f"Compilation error: {e}")
except VRLRuntimeError as e:
    print(f"Runtime error: {e}")
```

---

## 🔧 IDE 支持 / IDE Support

### PyCharm / RustRover

✅ **完全支持** / Full support

- 自动补全 / Auto-completion
- 参数提示 / Parameter hints
- 类型检查 / Type checking
- 快速文档 / Quick documentation

**示例截图位置** / Screenshot location:
```
docs/screenshots/pycharm-type-hints.png
```

### VS Code

✅ **完全支持** / Full support (with Pylance)

安装 Pylance 扩展：
```bash
code --install-extension ms-python.vscode-pylance
```

配置 `settings.json`:
```json
{
    "python.analysis.typeCheckingMode": "basic"
}
```

### 其他 IDE / Other IDEs

任何支持 PEP 561 的 IDE 都可以使用类型提示。

Any IDE that supports PEP 561 can use type hints.

---

## 🔍 静态类型检查 / Static Type Checking

### 使用 mypy

```bash
# 安装 mypy
pip install mypy

# 检查类型
mypy your_script.py
```

**示例**:
```python
# good_types.py
from vrl_python import VRLRuntime

runtime = VRLRuntime()
result = runtime.execute('.field = "value"', {})
print(result.processed_event)  # ✅ OK
```

```bash
$ mypy good_types.py
Success: no issues found in 1 source file
```

### 使用 pyright

```bash
# 安装 pyright
npm install -g pyright

# 检查类型
pyright your_script.py
```

---

## 📝 使用示例 / Usage Examples

### 示例 1: 基本类型提示

```python
from vrl_python import VRLRuntime, VRLResult
from typing import Dict, Any

def process_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """处理事件 / Process event"""
    runtime: VRLRuntime = VRLRuntime()
    
    program: str = """
    .processed = true
    .timestamp = now()
    """
    
    result: VRLResult = runtime.execute(program, event)
    return result.processed_event

# IDE 会提供完整的类型提示和自动补全
processed = process_event({"data": "test"})
```

### 示例 2: 可选类型

```python
from vrl_python import VRLRuntime, VRLDiagnostic
from typing import Optional

def validate_vrl(program: str) -> Optional[str]:
    """验证 VRL 程序 / Validate VRL program"""
    diagnostic: Optional[VRLDiagnostic] = VRLRuntime.check_syntax(program)
    
    if diagnostic is None:
        return None
    
    # IDE 知道这里 diagnostic 不是 None
    return diagnostic.formatted_message

# 使用
error: Optional[str] = validate_vrl('.field = "value"')
if error:
    print(f"Error: {error}")
```

### 示例 3: 泛型和联合类型

```python
from vrl_python import VRLRuntime, VRLResult
from typing import Dict, Any, Union, List

def batch_process(
    events: List[Dict[str, Any]], 
    program: str
) -> List[Union[VRLResult, Exception]]:
    """批量处理事件 / Batch process events"""
    runtime: VRLRuntime = VRLRuntime()
    results: List[Union[VRLResult, Exception]] = []
    
    for event in events:
        try:
            result: VRLResult = runtime.execute(program, event)
            results.append(result)
        except Exception as e:
            results.append(e)
    
    return results
```

### 示例 4: 类型守卫

```python
from vrl_python import VRLDiagnostic
from typing import Optional

def print_diagnostic(diagnostic: Optional[VRLDiagnostic]) -> None:
    """打印诊断信息 / Print diagnostic"""
    if diagnostic is None:
        print("✅ No errors")
        return
    
    # 类型守卫：这里 diagnostic 的类型是 VRLDiagnostic
    for message in diagnostic.messages:
        print(f"❌ {message}")
    
    print(diagnostic.formatted_message)
```

---

## 🎓 最佳实践 / Best Practices

### 1. 始终使用类型注解

```python
# ✅ 好 / Good
def process(event: Dict[str, Any]) -> VRLResult:
    runtime: VRLRuntime = VRLRuntime()
    return runtime.execute('.field = "value"', event)

# ❌ 不好 / Bad
def process(event):
    runtime = VRLRuntime()
    return runtime.execute('.field = "value"', event)
```

### 2. 使用 Optional 表示可能为 None 的值

```python
from typing import Optional

# ✅ 好 / Good
diagnostic: Optional[VRLDiagnostic] = VRLRuntime.check_syntax(program)

# ❌ 不好 / Bad
diagnostic = VRLRuntime.check_syntax(program)  # 类型不明确
```

### 3. 导入类型用于注解

```python
from vrl_python import VRLRuntime, VRLResult, VRLDiagnostic
from typing import Dict, Any, List, Optional

# 所有类型都明确定义
def my_function(
    runtime: VRLRuntime,
    events: List[Dict[str, Any]]
) -> List[VRLResult]:
    ...
```

### 4. 使用类型检查工具

```bash
# 在 CI/CD 中运行类型检查
mypy src/
pyright src/
```

---

## 🔧 配置 / Configuration

### mypy 配置

创建 `mypy.ini`:
```ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

[mypy-vrl_python.*]
# vrl_python 已经有完整的类型提示
ignore_missing_imports = False
```

### pyright 配置

创建 `pyrightconfig.json`:
```json
{
    "include": ["src", "tests"],
    "exclude": ["**/__pycache__"],
    "typeCheckingMode": "basic",
    "reportMissingTypeStubs": false,
    "pythonVersion": "3.8"
}
```

---

## 📚 参考资料 / References

### PEP 文档
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 561 - Distributing and Packaging Type Information](https://peps.python.org/pep-0561/)
- [PEP 585 - Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)

### 工具文档
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pyright Documentation](https://github.com/microsoft/pyright)
- [typing Module](https://docs.python.org/3/library/typing.html)

---

## 🐛 故障排查 / Troubleshooting

### 问题 1: IDE 不显示类型提示

**解决方案**:
1. 确保安装了最新版本的包
2. 重启 IDE
3. 清除 IDE 缓存
4. 检查 `py.typed` 文件是否存在

### 问题 2: mypy 报告缺少类型

**解决方案**:
```bash
# 重新安装包
pip uninstall vrl-python-sdk
pip install vrl-python-sdk

# 检查 .pyi 文件是否存在
python -c "import vrl_python; print(vrl_python.__file__)"
```

### 问题 3: 类型检查失败

**解决方案**:
```python
# 使用 TYPE_CHECKING 避免循环导入
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vrl_python import VRLRuntime
```

---

## ✅ 验证类型提示 / Verify Type Hints

运行测试脚本：
```bash
python test_type_hints.py
```

使用 mypy 检查：
```bash
mypy test_type_hints.py
```

---

## 🎉 总结 / Summary

VRL-Python SDK 提供了：

- ✅ **完整的类型注解** - 所有公共 API 都有类型提示
- ✅ **PEP 561 兼容** - 标准的类型分发格式
- ✅ **IDE 友好** - 完整的自动补全和文档
- ✅ **静态检查** - 支持 mypy 和 pyright
- ✅ **详细文档** - 每个类型都有说明和示例

**开始使用类型提示，享受更好的开发体验！**

**Start using type hints and enjoy a better development experience!**

---

**最后更新 / Last Updated**: 2025-10-06  
**作者 / Author**: JQQ
