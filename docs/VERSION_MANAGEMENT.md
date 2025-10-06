# 版本管理指南 / Version Management Guide

本项目使用 `bump-my-version` 管理版本号，确保 Rust 和 Python 版本号保持同步。

This project uses `bump-my-version` to manage version numbers, ensuring Rust and Python versions stay in sync.

---

## 📋 版本号位置 / Version Number Locations

版本号需要在以下文件中保持一致：

1. **Cargo.toml** - Rust 包版本
2. **pyproject.toml** - Python 包版本
3. **python/vrl_python/__init__.py** - Python 模块版本
4. **CHANGELOG.md** - 变更日志

`bump-my-version` 会自动更新所有这些文件。

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# 使用 uv 安装
uv pip install bump-my-version

# 或使用 pip
pip install bump-my-version
```

### 基本用法 / Basic Usage

```bash
# 查看当前版本
bump-my-version show current_version

# 补丁版本 (0.1.0 -> 0.1.1)
bump-my-version bump patch

# 次版本 (0.1.0 -> 0.2.0)
bump-my-version bump minor

# 主版本 (0.1.0 -> 1.0.0)
bump-my-version bump major
```

---

## 📖 版本号规范 / Version Number Convention

本项目遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)：

```
主版本号.次版本号.修订号[-预发布版本.预发布号]
MAJOR.MINOR.PATCH[-PRERELEASE.NUMBER]
```

### 版本号含义 / Version Meaning

- **MAJOR (主版本)**: 不兼容的 API 变更
- **MINOR (次版本)**: 向后兼容的功能新增
- **PATCH (修订号)**: 向后兼容的问题修复
- **PRERELEASE**: 预发布标识 (alpha, beta, rc)

### 示例 / Examples

| 版本号 | 类型 | 说明 |
|--------|------|------|
| `0.1.0` | 初始版本 | 首次发布 |
| `0.1.1` | 补丁版本 | Bug 修复 |
| `0.2.0` | 次版本 | 新功能 |
| `1.0.0` | 主版本 | 稳定版本 |
| `1.0.0-alpha.1` | Alpha | 内部测试 |
| `1.0.0-beta.1` | Beta | 公开测试 |
| `1.0.0-rc.1` | RC | 发布候选 |

---

## 🔧 常用命令 / Common Commands

### 1. 补丁版本 (Bug 修复)

```bash
# 0.1.0 -> 0.1.1
bump-my-version bump patch

# 查看将要做的更改（不实际执行）
bump-my-version bump patch --dry-run --verbose
```

**使用场景**:
- 修复 bug
- 文档更新
- 性能优化（不改变 API）

### 2. 次版本 (新功能)

```bash
# 0.1.0 -> 0.2.0
bump-my-version bump minor
```

**使用场景**:
- 添加新功能
- 向后兼容的 API 变更
- 废弃旧功能（但仍保留）

### 3. 主版本 (破坏性变更)

```bash
# 0.2.0 -> 1.0.0
bump-my-version bump major
```

**使用场景**:
- 不兼容的 API 变更
- 移除废弃的功能
- 重大架构调整

### 4. 预发布版本

```bash
# 创建 alpha 版本: 0.1.0 -> 0.2.0-alpha.1
bump-my-version bump minor --new-version 0.2.0-alpha.1

# 增加 alpha 版本号: 0.2.0-alpha.1 -> 0.2.0-alpha.2
bump-my-version bump pre_number

# 升级到 beta: 0.2.0-alpha.2 -> 0.2.0-beta.1
bump-my-version bump pre_release

# 发布正式版: 0.2.0-beta.1 -> 0.2.0
bump-my-version bump pre_release
```

---

## 📝 完整发布流程 / Complete Release Process

### 准备发布 / Prepare Release

```bash
# 1. 确保在正确的分支
git checkout develop
git pull origin develop

# 2. 确保所有测试通过
make test
make lint

# 3. 更新 CHANGELOG.md
# 手动编辑 CHANGELOG.md，添加本次发布的变更

# 4. 提交未完成的更改
git add .
git commit -m "docs: update changelog for v0.2.0"
```

### 升级版本 / Bump Version

```bash
# 5. 升级版本号（自动提交和打标签）
bump-my-version bump minor  # 或 patch/major

# 这会自动：
# - 更新所有文件中的版本号
# - 创建 git commit
# - 创建 git tag (v0.2.0)
```

### 推送和发布 / Push and Release

```bash
# 6. 推送到远程仓库
git push origin develop
git push origin --tags

# 7. 合并到 main 分支
git checkout main
git merge develop
git push origin main

# 8. 在 GitHub 创建 Release
# - 访问: https://github.com/A2C-SMCP/vrl-python/releases/new
# - 选择 tag: v0.2.0
# - 填写 Release 说明
# - 发布（触发自动发布到 PyPI）
```

---

## 🎯 Makefile 集成 / Makefile Integration

在 Makefile 中添加版本管理命令：

```makefile
# 查看当前版本
.PHONY: version
version:
	@echo "Current version:"
	@bump-my-version show current_version

# 补丁版本
.PHONY: bump-patch
bump-patch:
	@echo "Bumping patch version..."
	bump-my-version bump patch

# 次版本
.PHONY: bump-minor
bump-minor:
	@echo "Bumping minor version..."
	bump-my-version bump minor

# 主版本
.PHONY: bump-major
bump-major:
	@echo "Bumping major version..."
	bump-my-version bump major

# 预发布版本
.PHONY: bump-alpha
bump-alpha:
	@echo "Creating alpha release..."
	bump-my-version bump minor --new-version $(shell bump-my-version show current_version | awk -F. '{print $$1"."$$2+1".0-alpha.1"}')
```

使用：

```bash
make version        # 查看当前版本
make bump-patch     # 升级补丁版本
make bump-minor     # 升级次版本
make bump-major     # 升级主版本
```

---

## ⚙️ 配置文件 / Configuration File

配置文件位于 `.bumpversion.toml`，包含：

```toml
[tool.bumpversion]
current_version = "0.1.0"
commit = true                    # 自动提交
tag = true                       # 自动打标签
tag_name = "v{new_version}"     # 标签格式
message = "chore: bump version {current_version} → {new_version}"

# 需要更新版本号的文件
[[tool.bumpversion.files]]
filename = "Cargo.toml"

[[tool.bumpversion.files]]
filename = "pyproject.toml"

[[tool.bumpversion.files]]
filename = "python/vrl_python/__init__.py"

[[tool.bumpversion.files]]
filename = "CHANGELOG.md"
```

---

## 🔍 验证版本一致性 / Verify Version Consistency

创建验证脚本：

```bash
#!/bin/bash
# scripts/check_version.sh

CARGO_VERSION=$(grep '^version = ' Cargo.toml | head -1 | cut -d'"' -f2)
PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | head -1 | cut -d'"' -f2)
INIT_VERSION=$(grep '^__version__ = ' python/vrl_python/__init__.py | cut -d'"' -f2)

echo "Cargo.toml:     $CARGO_VERSION"
echo "pyproject.toml: $PYPROJECT_VERSION"
echo "__init__.py:    $INIT_VERSION"

if [ "$CARGO_VERSION" = "$PYPROJECT_VERSION" ] && [ "$CARGO_VERSION" = "$INIT_VERSION" ]; then
    echo "✅ All versions match!"
    exit 0
else
    echo "❌ Version mismatch!"
    exit 1
fi
```

使用：

```bash
chmod +x scripts/check_version.sh
./scripts/check_version.sh
```

---

## 🐛 常见问题 / Troubleshooting

### 问题 1: 版本号不一致

**症状**: 不同文件中的版本号不同

**解决**:
```bash
# 手动同步版本号
# 编辑 .bumpversion.toml 设置正确的 current_version
# 然后运行
bump-my-version bump patch --dry-run
```

### 问题 2: Git 标签冲突

**症状**: `tag already exists`

**解决**:
```bash
# 删除本地标签
git tag -d v0.1.0

# 删除远程标签
git push origin --delete v0.1.0

# 重新创建
bump-my-version bump patch
```

### 问题 3: 需要回滚版本

**症状**: 版本号升级错误

**解决**:
```bash
# 回滚最后一次提交
git reset --hard HEAD~1

# 删除标签
git tag -d v0.2.0

# 重新升级
bump-my-version bump patch
```

---

## 📚 最佳实践 / Best Practices

### 1. 发布前检查清单

- [ ] 所有测试通过
- [ ] 代码已格式化
- [ ] CHANGELOG.md 已更新
- [ ] 文档已更新
- [ ] 无未提交的更改

### 2. 版本号选择

- **0.x.x**: 开发阶段，API 可能变化
- **1.0.0**: 第一个稳定版本
- **x.y.0**: 新功能发布
- **x.y.z**: Bug 修复

### 3. 预发布版本

```
开发流程:
0.1.0 (当前稳定版)
  ↓
0.2.0-alpha.1 (内部测试)
  ↓
0.2.0-alpha.2 (修复问题)
  ↓
0.2.0-beta.1 (公开测试)
  ↓
0.2.0-rc.1 (发布候选)
  ↓
0.2.0 (正式发布)
```

### 4. Git 工作流

```
develop (开发分支)
  ↓ 功能完成
  ↓ bump version
  ↓ push tags
  ↓
main (稳定分支)
  ↓ create release
  ↓
PyPI (自动发布)
```

---

## 🔗 相关资源 / Related Resources

- [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)
- [bump-my-version 文档](https://github.com/callowayproject/bump-my-version)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- [Git 标签](https://git-scm.com/book/zh/v2/Git-基础-打标签)

---

## 📊 版本历史 / Version History

查看所有版本：

```bash
# Git 标签
git tag -l

# 详细信息
git tag -l -n9

# 查看特定版本的更改
git show v0.1.0
```

---

**最后更新 / Last Updated**: 2025-10-06  
**维护者 / Maintainer**: JQQ
