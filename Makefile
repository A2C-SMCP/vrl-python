# Makefile for VRL-Python
# 作者 / Author: JQQ
# 创建日期 / Created: 2025-10-06

.PHONY: help install dev build test clean examples format lint check all

# 默认目标 / Default target
help:
	@echo "VRL-Python 开发工具 / VRL-Python Development Tools"
	@echo ""
	@echo "可用命令 / Available commands:"
	@echo "  make install    - 安装开发环境 / Install development environment"
	@echo "  make dev        - 开发模式构建 / Build in development mode"
	@echo "  make build      - 发布模式构建 / Build in release mode"
	@echo "  make test       - 运行测试 / Run tests"
	@echo "  make examples   - 运行示例 / Run examples"
	@echo "  make clean      - 清理构建文件 / Clean build files"
	@echo "  make format     - 格式化代码 / Format code"
	@echo "  make lint       - 代码检查 / Lint code"
	@echo "  make check      - 完整检查 / Full check (format + lint + test)"
	@echo "  make all        - 完整构建和测试 / Full build and test"

# 安装开发环境 / Install development environment
install:
	@echo "📦 安装开发环境 / Installing development environment..."
	uv venv
	. .venv/bin/activate && uv pip install maturin pytest pytest-cov black ruff mypy

# 开发模式构建 / Build in development mode
dev:
	@echo "🔨 开发模式构建 / Building in development mode..."
	. .venv/bin/activate && maturin develop

# 发布模式构建 / Build in release mode
build:
	@echo "🚀 发布模式构建 / Building in release mode..."
	. .venv/bin/activate && maturin develop --release

# 运行测试 / Run tests
test:
	@echo "🧪 运行测试 / Running tests..."
	. .venv/bin/activate && pytest tests/ -v

# 运行测试并生成覆盖率报告 / Run tests with coverage
test-cov:
	@echo "📊 运行测试并生成覆盖率 / Running tests with coverage..."
	. .venv/bin/activate && pytest tests/ -v --cov=vrl_python --cov-report=html --cov-report=term

# 运行示例 / Run examples
examples:
	@echo "📚 运行示例 / Running examples..."
	. .venv/bin/activate && python examples/basic_usage.py

# 快速测试 / Quick test
quick-test:
	@echo "⚡ 快速测试 / Quick test..."
	. .venv/bin/activate && python test_quick.py

# 清理构建文件 / Clean build files
clean:
	@echo "🧹 清理构建文件 / Cleaning build files..."
	rm -rf target/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf *.egg-info/
	rm -rf dist/
	rm -rf build/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.so" -delete
	find . -type f -name "*.pyd" -delete
	@echo "✨ 清理完成 / Cleaning completed"

# 格式化 Python 代码 / Format Python code
format-py:
	@echo "🎨 格式化 Python 代码 / Formatting Python code..."
	. .venv/bin/activate && black python/ tests/ examples/ *.py

# 格式化 Rust 代码 / Format Rust code
format-rs:
	@echo "🎨 格式化 Rust 代码 / Formatting Rust code..."
	cargo fmt

# 格式化所有代码 / Format all code
format: format-py format-rs
	@echo "✅ 代码格式化完成 / Code formatting completed"

# Python 代码检查 / Lint Python code
lint-py:
	@echo "🔍 检查 Python 代码 / Linting Python code..."
	. .venv/bin/activate && ruff check python/ tests/ examples/ || true

# Rust 代码检查 / Lint Rust code
lint-rs:
	@echo "🔍 检查 Rust 代码 / Linting Rust code..."
	cargo clippy -- -D warnings || true

# 所有代码检查 / Lint all code
lint: lint-py lint-rs
	@echo "✅ 代码检查完成 / Code linting completed"

# Rust 编译检查 / Rust compile check
check-rs:
	@echo "🔍 Rust 编译检查 / Rust compile check..."
	cargo check

# 完整检查 / Full check
check: format lint check-rs test
	@echo "✅ 完整检查通过 / Full check passed"

# 构建 wheel 包 / Build wheel package
wheel:
	@echo "📦 构建 wheel 包 / Building wheel package..."
	. .venv/bin/activate && maturin build --release

# 发布到 PyPI / Publish to PyPI
publish:
	@echo "🚀 发布到 PyPI / Publishing to PyPI..."
	. .venv/bin/activate && maturin publish

# 完整构建和测试 / Full build and test
all: clean install build test examples
	@echo "🎉 完整构建和测试完成 / Full build and test completed"

# 开发循环 / Development loop
watch:
	@echo "👀 监视文件变化并自动重新构建 / Watching for changes..."
	. .venv/bin/activate && cargo watch -x "build" -s "maturin develop"

# 显示项目信息 / Show project info
info:
	@echo "📋 项目信息 / Project Information"
	@echo "=================================="
	@echo "项目名称 / Project Name: vrl-python"
	@echo "版本 / Version: $$(grep '^version' Cargo.toml | head -1 | cut -d'"' -f2)"
	@echo "Rust 版本 / Rust Version: $$(rustc --version)"
	@echo "Python 版本 / Python Version: $$(python3 --version)"
	@echo "Cargo 版本 / Cargo Version: $$(cargo --version)"
	@echo ""
	@echo "依赖状态 / Dependency Status:"
	@echo "  Maturin: $$(. .venv/bin/activate && maturin --version 2>/dev/null || echo '未安装 / Not installed')"
	@echo "  Pytest: $$(. .venv/bin/activate && pytest --version 2>/dev/null || echo '未安装 / Not installed')"
