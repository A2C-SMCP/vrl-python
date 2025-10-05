# vrl-python
VRL Python SDK Project

基于PyO3封装的Vector Remap Language (VRL) Python SDK

项目概述

本项目旨在为Vector的VRL语言提供一个Python SDK封装，使Python开发者能够直接在Python环境中使用VRL的强大数据处理能力。封装基于PyO3实现，提供高性能的Rust底层实现和友好的Python API。

功能特性

• ✅ 编译和执行VRL程序

• ✅ 支持事件数据处理和转换

• ✅ 完整的错误处理和诊断信息

• ✅ **VRL语法检查和诊断** (新增)

• ✅ 时区支持

• ✅ 性能监控（执行时间统计）

• ✅ 预编译和缓存支持

快速开始

安装

pip install vrl-python-sdk


基本用法

from vrl_sdk import VRLRuntime

# 初始化运行时
runtime = VRLRuntime()

# 定义VRL程序
program = """
.message = parse_json!(.message)
.new_field = "new value"
"""

# 准备输入事件
event = {
"message": '{"key": "value"}',
"timestamp": "2023-01-01T00:00:00Z"
}

# 执行VRL程序
result = runtime.execute(program, event)

print(result.processed_event)
# 输出: {'message': {'key': 'value'}, 'timestamp': '2023-01-01T00:00:00Z', 'new_field': 'new value'}


VRL语法检查

from vrl_sdk import VRLRuntime

# 检查VRL程序语法
program = """
.parsed = parse_json(.message)
"""

diagnostic = VRLRuntime.check_syntax(program)
if diagnostic is None:
    print("✅ 语法正确")
else:
    print(f"❌ 发现错误: {diagnostic.messages}")
    print(diagnostic.formatted_message)  # 详细的错误信息，包含位置和建议


开发计划

阶段1: 核心功能实现 ✅ (已完成)
• ✅ 项目初始化与PyO3配置

• ✅ 基本VRL编译执行功能

• ✅ 错误处理与诊断信息

• ✅ 单元测试框架搭建（11个测试全部通过）

• ✅ 示例代码和文档

阶段2: 高级功能扩展
自定义函数支持

时区配置支持

性能优化与缓存

文档生成

阶段3: 生产准备
CI/CD流水线

性能基准测试

PyPI发布准备

开发环境

• Rust 1.70+

• Python 3.8+

• RustRover IDE (推荐)

• maturin (构建工具)

CI/CD

• ✅ GitHub Actions 自动化测试

• ✅ 多平台支持 (Linux, macOS, Windows)

• ✅ 自动发布到 PyPI/TestPyPI

• ✅ Trusted Publishing (安全发布)

构建与测试

## 使用 Makefile（推荐）

# 查看所有可用命令
make help

# 安装开发环境
make install

# 开发模式构建
make dev

# 运行测试
make test

# 运行示例
make examples

# 完整检查（格式化 + 检查 + 测试）
make check


## 手动命令

# 创建虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv pip install maturin pytest pytest-cov

# 开发模式构建
maturin develop

# 发布模式构建
maturin develop --release

# 运行测试
pytest tests/ -v

# 运行示例
python examples/basic_usage.py


贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork仓库并创建分支
2. 提交代码变更
3. 添加/更新测试用例
4. 运行测试确保通过
5. 提交Pull Request

技术参考

• https://vector.dev/docs/reference/vrl/

• https://pyo3.rs/

• https://github.com/vectordotdev/vrl

许可证

MIT