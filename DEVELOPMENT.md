# VRL-Python 开发指南 / Development Guide

## 项目概述 / Project Overview

VRL-Python 是一个基于 PyO3 的 Vector Remap Language (VRL) Python SDK，提供了高性能的 Rust 底层实现和友好的 Python API。

## 开发环境设置 / Development Environment Setup

### 必需工具 / Required Tools

- **Rust**: 1.70+ (推荐使用 rustup 安装)
- **Python**: 3.8+ (推荐使用 pyenv 管理)
- **uv**: Python 包管理工具 (推荐使用 brew 安装)
- **RustRover**: JetBrains IDE (推荐用于开发)

### 初始化项目 / Initialize Project

```bash
# 克隆仓库 / Clone repository
git clone <repository-url>
cd vrl-python

# 创建虚拟环境 / Create virtual environment
uv venv

# 激活虚拟环境 / Activate virtual environment
source .venv/bin/activate

# 安装开发依赖 / Install development dependencies
uv pip install maturin pytest pytest-cov

# 构建项目（开发模式）/ Build project (development mode)
maturin develop

# 或构建发布版本 / Or build release version
maturin develop --release
```

## 项目结构 / Project Structure

```
vrl-python/
├── src/                    # Rust 源代码 / Rust source code
│   ├── lib.rs             # 主入口 / Main entry point
│   ├── runtime.rs         # VRL 运行时实现 / VRL runtime implementation
│   ├── types.rs           # 类型定义和转换 / Type definitions and conversions
│   └── error.rs           # 错误处理 / Error handling
├── python/                 # Python 包装层 / Python wrapper
│   └── vrl_python/
│       └── __init__.py    # Python 模块入口 / Python module entry
├── tests/                  # 测试用例 / Test cases
│   └── test_basic.py      # 基础功能测试 / Basic functionality tests
├── examples/               # 示例代码 / Example code
│   └── basic_usage.py     # 基础使用示例 / Basic usage examples
├── Cargo.toml             # Rust 项目配置 / Rust project configuration
├── pyproject.toml         # Python 项目配置 / Python project configuration
└── README.md              # 项目说明 / Project documentation
```

## 核心组件说明 / Core Components

### 1. VRLRuntime (runtime.rs)

主要的运行时类，负责：
- VRL 程序的编译和缓存
- 事件数据的处理
- 时区配置管理
- 错误处理和诊断

**关键方法 / Key Methods:**
- `new(timezone)`: 创建运行时实例
- `compile(source)`: 编译 VRL 程序
- `execute(source, event)`: 执行 VRL 程序
- `run(source, event, timezone)`: 静态方法，一次性执行

### 2. 类型转换 (types.rs)

处理 Python 和 VRL 之间的类型转换：
- `py_to_vrl_value()`: Python → VRL Value
- `vrl_value_to_py()`: VRL Value → Python
- `json_to_vrl_value()`: JSON → VRL Value

**支持的类型 / Supported Types:**
- 基础类型：null, bool, int, float, string
- 复合类型：array, object
- 特殊类型：timestamp, regex

### 3. 错误处理 (error.rs)

自定义异常类型：
- `VRLCompileError`: 编译时错误
- `VRLRuntimeError`: 运行时错误

## 开发工作流 / Development Workflow

### 1. 修改代码 / Modify Code

在 `src/` 目录下修改 Rust 代码，或在 `python/` 目录下修改 Python 代码。

### 2. 重新构建 / Rebuild

```bash
# 开发模式（快速编译）/ Development mode (fast compilation)
maturin develop

# 发布模式（优化编译）/ Release mode (optimized compilation)
maturin develop --release
```

### 3. 运行测试 / Run Tests

```bash
# 运行所有测试 / Run all tests
pytest tests/ -v

# 运行特定测试 / Run specific test
pytest tests/test_basic.py::test_simple_assignment -v

# 生成覆盖率报告 / Generate coverage report
pytest tests/ --cov=vrl_python --cov-report=html
```

### 4. 运行示例 / Run Examples

```bash
# 运行基础示例 / Run basic examples
python examples/basic_usage.py

# 快速测试 / Quick test
python test_quick.py
```

## 常见问题 / Common Issues

### 1. 编译错误：找不到 VRL

**问题 / Issue:** `error: failed to load manifest for dependency 'vrl'`

**解决方案 / Solution:**
```bash
# 更新 Cargo 依赖 / Update Cargo dependencies
cargo update
```

### 2. Python 导入错误

**问题 / Issue:** `ModuleNotFoundError: No module named 'vrl_python'`

**解决方案 / Solution:**
```bash
# 确保虚拟环境已激活 / Ensure virtual environment is activated
source .venv/bin/activate

# 重新构建 / Rebuild
maturin develop
```

### 3. 类型转换错误

**问题 / Issue:** NotNan 或 Float 类型转换失败

**解决方案 / Solution:**
- 使用 `ordered_float::NotNan::new()` 处理浮点数
- 使用 `into_inner()` 从 NotNan 获取 f64

### 4. VRL 语法错误

**问题 / Issue:** `error[E103]: unhandled fallible assignment`

**解决方案 / Solution:**
- 使用 `!` 后缀处理可能失败的函数：`parse_json!()`, `to_int!()`
- 或使用错误处理语法：`.result, .error = parse_json(.input)`

## 性能优化建议 / Performance Optimization Tips

1. **预编译程序 / Precompile Programs**
   ```python
   runtime = VRLRuntime()
   runtime.compile(program)  # 编译一次 / Compile once
   
   for event in events:
       result = runtime.execute(program, event)  # 重用编译结果 / Reuse compiled program
   ```

2. **使用发布模式 / Use Release Mode**
   ```bash
   maturin develop --release
   ```

3. **批量处理 / Batch Processing**
   - 重用 VRLRuntime 实例
   - 避免频繁创建和销毁对象

## 贡献指南 / Contributing Guidelines

1. **代码风格 / Code Style**
   - Rust: 遵循 `rustfmt` 标准
   - Python: 遵循 PEP 8 标准

2. **提交前检查 / Pre-commit Checklist**
   - [ ] 运行所有测试并通过
   - [ ] 添加必要的测试用例
   - [ ] 更新相关文档
   - [ ] 代码格式化

3. **测试要求 / Testing Requirements**
   - 新功能必须有对应的测试用例
   - 测试覆盖率应保持在 80% 以上
   - 所有测试必须通过

## 发布流程 / Release Process

### 1. 更新版本号 / Update Version

在 `Cargo.toml` 和 `pyproject.toml` 中更新版本号。

### 2. 构建发布包 / Build Release Package

```bash
# 构建 wheel 包 / Build wheel package
maturin build --release

# 查看生成的包 / View generated packages
ls target/wheels/
```

### 3. 发布到 PyPI / Publish to PyPI

```bash
# 使用 maturin 发布 / Publish using maturin
maturin publish
```

## 调试技巧 / Debugging Tips

### 1. 启用 Rust 日志 / Enable Rust Logging

```bash
RUST_LOG=debug maturin develop
```

### 2. Python 调试 / Python Debugging

```python
import traceback

try:
    result = runtime.execute(program, event)
except Exception as e:
    traceback.print_exc()
    print(f"Error details: {e}")
```

### 3. 查看 VRL 诊断信息 / View VRL Diagnostics

```python
from vrl_python import VRLRuntime

runtime = VRLRuntime()
try:
    runtime.compile(invalid_program)
except ValueError as e:
    print(e)  # 包含详细的错误位置和建议 / Contains detailed error location and suggestions
```

## 资源链接 / Resource Links

- **VRL 文档**: https://vector.dev/docs/reference/vrl/
- **PyO3 文档**: https://pyo3.rs/
- **VRL GitHub**: https://github.com/vectordotdev/vrl
- **Vector GitHub**: https://github.com/vectordotdev/vector
- **Maturin 文档**: https://www.maturin.rs/

## 联系方式 / Contact

- **作者 / Author**: JQQ
- **邮箱 / Email**: jqq1716@gmail.com
- **问题反馈 / Issue Tracker**: [GitHub Issues](https://github.com/yourusername/vrl-python/issues)
