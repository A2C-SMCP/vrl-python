# Makefile for VRL-Python
# 作者 / Author: JQQ

.PHONY: help install dev build test clean examples format lint check all version bump-patch bump-minor bump-major check-version

# 显示帮助信息 / Show help information
help:
	@echo "可用的命令 / Available commands:"
	@echo ""
	@echo "开发命令 / Development:"
	@echo "  make install      - 安装开发环境 / Install development environment"
	@echo "  make dev          - 开发模式构建 / Development build"
	@echo "  make build        - 发布模式构建 / Release build"
	@echo "  make test         - 运行所有测试 / Run all tests"
	@echo "  make clean        - 清理构建文件 / Clean build files"
	@echo "  make format       - 格式化所有代码 / Format all code"
	@echo "  make lint         - 检查所有代码 / Lint all code"
	@echo ""
	@echo "版本管理 / Version Management:"
	@echo "  make version       - 查看当前版本 / Show current version"
	@echo "  make check-version - 检查版本一致性 / Check version consistency"
	@echo "  make bump-dev      - 升级 dev 版本 (0.1.0 -> 0.1.1-dev1)"
	@echo "  make bump-rc       - 升级到 RC 版本 (0.1.1-dev4 -> 0.1.1-rc1)"
	@echo "  make bump-release  - 发布正式版本 (0.1.1-rc1 -> 0.1.1)"
	@echo "  make bump-patch    - 升级补丁版本 (0.1.0 -> 0.1.1)"
	@echo "  make bump-minor    - 升级次版本 (0.1.0 -> 0.2.0)"
	@echo "  make bump-major    - 升级主版本 (0.1.0 -> 1.0.0)"
	@echo "  make all        - 完整构建和测试 / Full build and test"

# 安装开发环境 / Install development environment
install:
	@echo "📦 安装开发环境 / Installing development environment..."
	uv pip install maturin pytest pytest-cov

# 开发模式构建 / Build in development mode
dev:
	@echo "🔨 开发模式构建 / Building in development mode..."
	uv run maturin develop

# 发布模式构建 / Build in release mode
build:
	@echo "🚀 发布模式构建 / Building in release mode..."
	uv run maturin build --release

# 运行测试 / Run tests
test:
	@echo "🧪 运行测试 / Running tests..."
	uv run pytest tests/ -v

# 运行测试并生成覆盖率报告 / Run tests with coverage
test-cov:
	@echo "📊 运行测试并生成覆盖率 / Running tests with coverage..."
	uv run pytest tests/ -v --cov=vrl_python --cov-report=html --cov-report=term

# 运行示例 / Run examples
examples:
	@echo "📚 运行示例 / Running examples..."
	uv run python examples/basic_usage.py

# 快速测试 / Quick test
quick-test:
	@echo "⚡ 快速测试 / Quick test..."
	uv run python test_quick.py

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
	find . -type f -name "*.pyd" -delete
	@echo "清理完成 / Cleaning completed"

# 格式化 Python 代码 / Format Python code
format-py:
	@echo "格式化 Python 代码 / Formatting Python code..."
	uv run ruff format python/ tests/ examples/ *.py
	uv run ruff check python/ tests/ examples/ *.py --fix

# 格式化 Rust 代码 / Format Rust code
format-rs:
	@echo "格式化 Rust 代码 / Formatting Rust code..."
	cargo fmt

# 格式化所有代码 / Format all code
format: format-py format-rs
	@echo "✅ 代码格式化完成 / Code formatting completed"

# Python 代码检查 / Lint Python code
lint-py:
	@echo "🔍 检查 Python 代码 / Linting Python code..."
	uv run ruff check python/ tests/ examples/

# Rust 代码检查 / Lint Rust code
lint-rs:
	@echo "🔍 检查 Rust 代码 / Linting Rust code..."
	cargo clippy -- -D warnings

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

# ============================================
# 版本管理 / Version Management
# ============================================

# 查看当前版本 / Show current version
version:
	@echo "📌 当前版本 / Current Version:"
	@uv run bump-my-version show current_version

# 检查版本一致性 / Check version consistency
check-version:
	@echo "🔍 检查版本一致性 / Checking version consistency..."
	@CARGO_VERSION=$$(grep '^version = ' Cargo.toml | head -1 | cut -d'"' -f2); \
	PYPROJECT_VERSION=$$(grep '^version = ' pyproject.toml | head -1 | cut -d'"' -f2); \
	INIT_VERSION=$$(grep '^__version__ = ' python/vrl_python/__init__.py | cut -d'"' -f2); \
	echo "  Cargo.toml:     $$CARGO_VERSION"; \
	echo "  pyproject.toml: $$PYPROJECT_VERSION"; \
	echo "  __init__.py:    $$INIT_VERSION"; \
	if [ "$$CARGO_VERSION" = "$$PYPROJECT_VERSION" ] && [ "$$CARGO_VERSION" = "$$INIT_VERSION" ]; then \
		echo "✅ 所有版本号一致 / All versions match!"; \
	else \
		echo "❌ 版本号不一致 / Version mismatch!"; \
		exit 1; \
	fi

# 升级补丁版本 / Bump patch version (0.1.0 -> 0.1.1)
bump-patch:
	@echo "⬆️  升级补丁版本 / Bumping patch version..."
	@uv run bump-my-version bump patch
	@echo "✅ 版本已升级 / Version bumped"
	@make check-version

# 升级次版本 / Bump minor version (0.1.0 -> 0.2.0)
bump-minor:
	@echo "⬆️  升级次版本 / Bumping minor version..."
	@uv run bump-my-version bump minor
	@echo "✅ 版本已升级 / Version bumped"
	@make check-version

# 升级主版本 / Bump major version (0.1.0 -> 1.0.0)
bump-major:
	@echo "⬆️  升级主版本 / Bumping major version..."
	@uv run bump-my-version bump major
	@echo "✅ 版本已升级 / Version bumped"
	@make check-version

# 预览版本升级（不实际执行）/ Preview version bump (dry-run)
bump-preview:
	@echo "👀 预览版本升级 / Previewing version bump..."
	@uv run bump-my-version bump patch --dry-run --verbose

# 升级 dev 版本 / Bump dev version (0.1.0 -> 0.1.1-dev1)
bump-dev:
	@echo "⬆️  升级 dev 版本 / Bumping dev version..."
	@CURRENT=$$(uv run bump-my-version show current_version); \
	if echo "$$CURRENT" | grep -q "dev"; then \
		uv run bump-my-version bump pre_n; \
	else \
		uv run bump-my-version bump patch --new-version $$(echo $$CURRENT | awk -F. '{print $$1"."$$2"."$$3+1"-dev1"}'); \
	fi
	@echo "✅ Dev 版本已升级 / Dev version bumped"
	@make check-version

# 升级到 rc 版本 / Bump to rc version (0.1.1-dev4 -> 0.1.1-rc1)
bump-rc:
	@echo "⬆️  升级到 RC 版本 / Bumping to RC version..."
	@uv run bump-my-version bump pre_l
	@echo "✅ RC 版本已升级 / RC version bumped"
	@make check-version

# 发布正式版本（从 rc 或 dev）/ Release final version (from rc or dev)
bump-release:
	@echo "⬆️  发布正式版本 / Releasing final version..."
	@uv run bump-my-version bump pre_l
	@echo "✅ 正式版本已发布 / Final version released"
	@make check-version
