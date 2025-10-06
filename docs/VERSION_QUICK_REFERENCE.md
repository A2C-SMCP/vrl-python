# 版本管理快速参考 / Version Management Quick Reference

## 🚀 常用命令 / Common Commands

```bash
# 查看当前版本
make version

# 检查版本一致性
make check-version

# 升级版本
make bump-patch    # 0.1.0 -> 0.1.1 (Bug 修复)
make bump-minor    # 0.1.0 -> 0.2.0 (新功能)
make bump-major    # 0.1.0 -> 1.0.0 (破坏性变更)

# 预览升级（不实际执行）
make bump-preview
```

## 📋 完整发布流程 / Complete Release Process

### 1. 准备发布

```bash
# 确保在 develop 分支
git checkout develop
git pull origin develop

# 运行测试
make test
make lint

# 更新 CHANGELOG.md
vim CHANGELOG.md
```

### 2. 升级版本

```bash
# 选择合适的版本类型
make bump-patch   # 或 bump-minor / bump-major

# 这会自动：
# ✅ 更新 Cargo.toml
# ✅ 更新 pyproject.toml  
# ✅ 更新 __init__.py
# ✅ 更新 CHANGELOG.md
# ✅ 创建 git commit
# ✅ 创建 git tag
```

### 3. 推送和发布

```bash
# 推送代码和标签
git push origin develop
git push origin --tags

# 合并到 main
git checkout main
git merge develop
git push origin main

# 在 GitHub 创建 Release
# → 自动触发 CI/CD 发布到 PyPI
```

## 🎯 版本号选择指南 / Version Selection Guide

| 变更类型 | 版本升级 | 示例 |
|---------|---------|------|
| Bug 修复 | `patch` | 0.1.0 → 0.1.1 |
| 新功能（兼容） | `minor` | 0.1.0 → 0.2.0 |
| 破坏性变更 | `major` | 0.1.0 → 1.0.0 |

## 📁 版本号位置 / Version Locations

所有版本号由 `bump-my-version` 自动同步：

- `Cargo.toml` - Rust 包版本
- `pyproject.toml` - Python 包版本
- `python/vrl_python/__init__.py` - Python 模块版本
- `CHANGELOG.md` - 变更日志

## 🔧 故障排查 / Troubleshooting

### 版本号不一致

```bash
# 检查不一致
make check-version

# 如果不一致，手动编辑 .bumpversion.toml
# 设置正确的 current_version，然后运行
bump-my-version bump patch --dry-run
```

### 标签冲突

```bash
# 删除本地标签
git tag -d v0.1.0

# 删除远程标签  
git push origin --delete v0.1.0

# 重新创建
make bump-patch
```

## 📚 更多信息 / More Information

详细文档：`VERSION_MANAGEMENT.md`

---

**快速提示**: 使用 `make help` 查看所有可用命令
