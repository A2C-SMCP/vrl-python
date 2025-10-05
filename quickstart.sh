#!/bin/bash
# 快速启动脚本 / Quick start script
# 作者 / Author: JQQ
# 创建日期 / Created: 2025-10-06

set -e

echo "🚀 VRL-Python 快速启动 / VRL-Python Quick Start"
echo "================================================"
echo ""

# 检查 uv 是否安装 / Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ 错误：uv 未安装 / Error: uv is not installed"
    echo "请运行：brew install uv / Please run: brew install uv"
    exit 1
fi

# 检查 Rust 是否安装 / Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ 错误：Rust 未安装 / Error: Rust is not installed"
    echo "请访问：https://rustup.rs / Please visit: https://rustup.rs"
    exit 1
fi

echo "✅ 环境检查通过 / Environment check passed"
echo ""

# 创建虚拟环境 / Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境 / Creating virtual environment..."
    uv venv
    echo "✅ 虚拟环境创建完成 / Virtual environment created"
else
    echo "✅ 虚拟环境已存在 / Virtual environment already exists"
fi
echo ""

# 激活虚拟环境并安装依赖 / Activate venv and install dependencies
echo "📦 安装依赖 / Installing dependencies..."
source .venv/bin/activate
uv pip install maturin pytest pytest-cov
echo "✅ 依赖安装完成 / Dependencies installed"
echo ""

# 构建项目 / Build project
echo "🔨 构建项目 / Building project..."
maturin develop --release
echo "✅ 项目构建完成 / Project built successfully"
echo ""

# 运行测试 / Run tests
echo "🧪 运行测试 / Running tests..."
pytest tests/ -v
echo ""

# 运行快速测试 / Run quick test
echo "⚡ 运行快速测试 / Running quick test..."
python test_quick.py
echo ""

echo "================================================"
echo "🎉 快速启动完成！/ Quick start completed!"
echo ""
echo "下一步 / Next steps:"
echo "  1. 激活虚拟环境 / Activate virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. 运行示例 / Run examples:"
echo "     python examples/basic_usage.py"
echo ""
echo "  3. 查看帮助 / View help:"
echo "     make help"
echo ""
echo "  4. 阅读文档 / Read documentation:"
echo "     - README.md"
echo "     - DEVELOPMENT.md"
echo "     - PROJECT_SUMMARY.md"
echo ""
