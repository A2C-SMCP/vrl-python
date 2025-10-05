# VRL 语法诊断功能 / VRL Syntax Diagnostics Feature

## 概述 / Overview

VRL-Python SDK 现在提供了完整的 VRL 语法检查和诊断功能，可以在不执行程序的情况下检查 VRL 代码的语法正确性。

VRL-Python SDK now provides complete VRL syntax checking and diagnostics functionality, allowing you to check VRL code syntax without executing the program.

---

## 功能特性 / Features

### ✅ 已实现 / Implemented

1. **静态语法检查** / Static Syntax Checking
   - 无需执行即可检查语法
   - 快速验证 VRL 程序正确性

2. **详细错误信息** / Detailed Error Messages
   - 错误类型和代码 (如 E103, E204)
   - 错误位置（行号和列号）
   - 具体的错误描述
   - 修复建议

3. **多种错误类型支持** / Multiple Error Types Support
   - 语法错误 (Syntax Errors)
   - 类型错误 (Type Errors)
   - 未定义函数 (Undefined Functions)
   - 未处理的可能失败操作 (Unhandled Fallible Operations)

---

## API 文档 / API Documentation

### VRLRuntime.check_syntax()

**签名 / Signature:**
```python
@staticmethod
def check_syntax(source: str) -> Optional[VRLDiagnostic]
```

**参数 / Parameters:**
- `source` (str): VRL 程序源码 / VRL program source code

**返回值 / Returns:**
- `None`: 语法正确，无错误 / Syntax is correct, no errors
- `VRLDiagnostic`: 包含错误信息的诊断对象 / Diagnostic object containing error information

**示例 / Example:**
```python
from vrl_python import VRLRuntime

program = '.field = "value"'
diagnostic = VRLRuntime.check_syntax(program)

if diagnostic is None:
    print("✅ 语法正确")
else:
    print(f"❌ 发现错误: {diagnostic.messages}")
```

---

## VRLDiagnostic 类 / VRLDiagnostic Class

### 属性 / Attributes

| 属性 / Attribute | 类型 / Type | 描述 / Description |
|-----------------|------------|-------------------|
| `messages` | `List[str]` | 错误消息列表 / List of error messages |
| `formatted_message` | `str` | 格式化的错误信息（包含位置和建议）/ Formatted error message with location and suggestions |
| `colored_message` | `str` | 带颜色的格式化信息（终端显示）/ Colored formatted message for terminal display |

### 示例 / Example

```python
diagnostic = VRLRuntime.check_syntax('.field = parse_json(.data)')

if diagnostic:
    # 简短错误消息
    print(diagnostic.messages)
    # ['unhandled fallible assignment']
    
    # 详细格式化信息
    print(diagnostic.formatted_message)
    # error[E103]: unhandled fallible assignment
    #   ┌─ :1:10
    #   │
    # 1 │ .field = parse_json(.data)
    #   │          ^^^^^^^^^^^^^^^^^
    #   │          this expression is fallible...
    
    # 字符串表示
    print(str(diagnostic))
    # 等同于 formatted_message
```

---

## 使用场景 / Use Cases

### 1. IDE 集成 / IDE Integration

在代码编辑器中实时检查 VRL 语法：

```python
def check_vrl_on_save(code: str):
    """保存时检查 VRL 代码 / Check VRL code on save"""
    diagnostic = VRLRuntime.check_syntax(code)
    
    if diagnostic:
        # 在编辑器中显示错误标记
        for msg in diagnostic.messages:
            show_error_marker(msg)
    else:
        clear_error_markers()
```

### 2. CI/CD 管道 / CI/CD Pipeline

在部署前验证 VRL 配置：

```python
def validate_vrl_configs(config_dir: str) -> bool:
    """验证所有 VRL 配置文件 / Validate all VRL config files"""
    all_valid = True
    
    for vrl_file in find_vrl_files(config_dir):
        with open(vrl_file) as f:
            code = f.read()
        
        diagnostic = VRLRuntime.check_syntax(code)
        if diagnostic:
            print(f"❌ {vrl_file}: {diagnostic.messages}")
            all_valid = False
    
    return all_valid
```

### 3. 在线代码验证器 / Online Code Validator

Web 应用中的实时语法检查：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/validate', methods=['POST'])
def validate_vrl():
    """API 端点：验证 VRL 代码 / API endpoint: Validate VRL code"""
    code = request.json.get('code', '')
    
    diagnostic = VRLRuntime.check_syntax(code)
    
    if diagnostic is None:
        return jsonify({'valid': True})
    else:
        return jsonify({
            'valid': False,
            'errors': diagnostic.messages,
            'details': diagnostic.formatted_message
        })
```

### 4. 学习工具 / Learning Tool

帮助用户学习 VRL 语法：

```python
def interactive_vrl_tutor():
    """交互式 VRL 教程 / Interactive VRL tutorial"""
    print("VRL 语法练习 / VRL Syntax Practice")
    
    while True:
        code = input("\n输入 VRL 代码 (或 'quit' 退出): ")
        if code == 'quit':
            break
        
        diagnostic = VRLRuntime.check_syntax(code)
        
        if diagnostic is None:
            print("✅ 太棒了！语法正确！")
        else:
            print("❌ 发现错误，让我们一起修复：")
            print(diagnostic.formatted_message)
```

---

## 错误类型详解 / Error Types Explained

### E103: Unhandled Fallible Assignment

**描述 / Description:**  
未处理可能失败的赋值操作

**示例 / Example:**
```python
# ❌ 错误
diagnostic = VRLRuntime.check_syntax('.parsed = parse_json(.data)')
# Error: unhandled fallible assignment

# ✅ 正确方式 1: 使用 ! 后缀
VRLRuntime.check_syntax('.parsed = parse_json!(.data)')

# ✅ 正确方式 2: 错误处理
VRLRuntime.check_syntax('.parsed, .error = parse_json(.data)')
```

### E105: Call to Undefined Function

**描述 / Description:**  
调用未定义的函数

**示例 / Example:**
```python
# ❌ 错误
diagnostic = VRLRuntime.check_syntax('.result = unknown_func(.data)')
# Error: call to undefined function
# Suggestion: did you mean "parse_duration"?
```

### E204: Syntax Error

**描述 / Description:**  
VRL 语法错误

**示例 / Example:**
```python
# ❌ 错误
diagnostic = VRLRuntime.check_syntax('.field =')
# Error: syntax error - unexpected end of program
```

---

## 性能特性 / Performance Characteristics

| 指标 / Metric | 值 / Value | 说明 / Note |
|--------------|-----------|------------|
| 检查速度 / Check Speed | < 1ms | 小型程序 / Small programs |
| 内存占用 / Memory Usage | 极小 / Minimal | 无需运行时状态 / No runtime state needed |
| 并发安全 / Thread Safety | ✅ 是 / Yes | 静态方法，无共享状态 / Static method, no shared state |

---

## 最佳实践 / Best Practices

### 1. 早期验证 / Early Validation

在执行前先检查语法：

```python
def safe_execute(runtime: VRLRuntime, program: str, event: dict):
    """安全执行：先检查语法 / Safe execution: check syntax first"""
    # 先检查语法
    diagnostic = VRLRuntime.check_syntax(program)
    if diagnostic:
        raise ValueError(f"VRL syntax error: {diagnostic.messages}")
    
    # 语法正确，执行程序
    return runtime.execute(program, event)
```

### 2. 缓存验证结果 / Cache Validation Results

对于不变的 VRL 程序，缓存验证结果：

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def is_valid_vrl(program: str) -> bool:
    """检查并缓存 VRL 程序有效性 / Check and cache VRL program validity"""
    return VRLRuntime.check_syntax(program) is None
```

### 3. 提供友好的错误信息 / Provide Friendly Error Messages

转换技术性错误为用户友好的消息：

```python
def user_friendly_error(diagnostic: VRLDiagnostic) -> str:
    """转换为用户友好的错误消息 / Convert to user-friendly error message"""
    if "unhandled fallible" in diagnostic.messages[0]:
        return "提示：某些函数可能失败，请添加 '!' 后缀或使用错误处理"
    elif "undefined function" in diagnostic.messages[0]:
        return "提示：函数名可能拼写错误，请检查函数名称"
    else:
        return diagnostic.formatted_message
```

---

## 限制和注意事项 / Limitations and Notes

### ⚠️ 注意事项 / Notes

1. **仅检查语法** / Syntax Only
   - 不执行程序，不验证运行时逻辑
   - 不检查数据类型的实际匹配

2. **性能考虑** / Performance Considerations
   - 每次调用都会重新编译
   - 对于频繁检查，考虑使用缓存

3. **错误信息语言** / Error Message Language
   - 错误信息为英文
   - 可以根据需要进行本地化

---

## 示例代码 / Example Code

完整示例请查看：
- `examples/basic_usage.py` - 示例 8
- `tests/test_basic.py` - `test_syntax_diagnostics()`

---

## 相关资源 / Related Resources

- [VRL 文档](https://vector.dev/docs/reference/vrl/)
- [VRL 错误代码](https://errors.vrl.dev/)
- [VRL REPL](https://vrl.dev/examples)

---

## 更新历史 / Update History

- **2025-10-06**: 初始实现 / Initial implementation
  - 添加 `check_syntax()` 方法
  - 添加示例和测试
  - 更新文档

---

**作者 / Author**: JQQ  
**最后更新 / Last Updated**: 2025-10-06
