# Rust-Python 版本号同步管理 / Rust-Python Version Synchronization

## 🎯 核心问题 / Core Challenge

Rust-Python 混合项目需要在多个地方维护版本号：

1. **Cargo.toml** - Rust 包版本
2. **pyproject.toml** - Python 包版本  
3. **python/vrl_python/__init__.py** - Python 模块版本

**关键**: 这些版本号必须始终保持一致！

---

## ✅ 解决方案 / Solution

使用 `bump-my-version` 统一管理所有版本号，确保一次操作同步更新所有文件。

### 配置文件：`.bumpversion.toml`

```toml
[tool.bumpversion]
current_version = "0.1.0"

# 关键配置：同时更新 Rust 和 Python 文件
[[tool.bumpversion.files]]
filename = "Cargo.toml"              # Rust 版本
search = "version = \"{current_version}\""
replace = "version = \"{new_version}\""

[[tool.bumpversion.files]]
filename = "pyproject.toml"          # Python 包版本
search = "version = \"{current_version}\""
replace = "version = \"{new_version}\""

[[tool.bumpversion.files]]
filename = "python/vrl_python/__init__.py"  # Python 模块版本
search = "__version__ = \"{current_version}\""
replace = "__version__ = \"{new_version}\""
```

---

## 🔄 版本升级流程 / Version Bump Workflow

### 开发流程 / Development Workflow

```
0.1.0 (稳定版)
  ↓ make bump-dev
0.1.1-dev1 (开发版本 1)
  ↓ make bump-dev
0.1.1-dev2 (开发版本 2)
  ↓ make bump-dev
0.1.1-dev3 (开发版本 3)
  ↓ make bump-rc
0.1.1-rc1 (发布候选)
  ↓ make bump-release
0.1.1 (正式发布)
```

### 命令说明 / Command Explanation

| 命令 | 作用 | 示例 |
|------|------|------|
| `make bump-dev` | 创建/递增 dev 版本 | 0.1.0 → 0.1.1-dev1 |
| `make bump-rc` | 升级到 RC 版本 | 0.1.1-dev3 → 0.1.1-rc1 |
| `make bump-release` | 发布正式版本 | 0.1.1-rc1 → 0.1.1 |
| `make bump-patch` | 直接升级补丁版本 | 0.1.0 → 0.1.1 |
| `make bump-minor` | 升级次版本 | 0.1.0 → 0.2.0 |
| `make bump-major` | 升级主版本 | 0.1.0 → 1.0.0 |

---

## 🔍 验证同步 / Verify Synchronization

### 自动验证

```bash
make check-version
```

输出示例：
```
🔍 检查版本一致性 / Checking version consistency...
  Cargo.toml:     0.1.1-dev2
  pyproject.toml: 0.1.1-dev2
  __init__.py:    0.1.1-dev2
✅ 所有版本号一致 / All versions match!
```

### 手动验证

```bash
# 查看 Rust 版本
grep '^version = ' Cargo.toml | head -1

# 查看 Python 包版本
grep '^version = ' pyproject.toml | head -1

# 查看 Python 模块版本
grep '^__version__ = ' python/vrl_python/__init__.py
```

---

## 🚀 实际使用示例 / Practical Examples

### 示例 1: 日常开发

```bash
# 1. 开始新功能开发
git checkout -b feature/new-feature

# 2. 创建 dev 版本
make bump-dev
# 0.1.0 → 0.1.1-dev1
# 自动更新：Cargo.toml, pyproject.toml, __init__.py
# 自动 commit 和 tag

# 3. 继续开发，需要新的 dev 版本
make bump-dev
# 0.1.1-dev1 → 0.1.1-dev2

# 4. 开发完成，准备测试
make bump-rc
# 0.1.1-dev2 → 0.1.1-rc1

# 5. 测试通过，发布正式版
make bump-release
# 0.1.1-rc1 → 0.1.1
```

### 示例 2: 快速修复

```bash
# 直接升级补丁版本（跳过 dev/rc）
make bump-patch
# 0.1.0 → 0.1.1
```

### 示例 3: 新功能发布

```bash
# 升级次版本
make bump-minor
# 0.1.5 → 0.2.0
```

---

## 🔧 Rust 特殊考虑 / Rust-Specific Considerations

### Cargo.lock 文件

`Cargo.lock` 会自动更新，但不需要手动管理版本号。

```bash
# bump-my-version 会触发 Cargo.toml 更新
# 下次构建时 Cargo.lock 自动同步
cargo build
```

### Cargo 版本验证

```bash
# 验证 Cargo.toml 语法
cargo check

# 查看包信息
cargo metadata --format-version 1 | jq '.packages[] | select(.name == "vrl-python")'
```

---

## 📦 构建和发布 / Build and Release

### 本地构建

```bash
# 升级版本
make bump-minor

# 构建 Rust + Python
make build

# 验证构建产物
ls -lh target/wheels/
```

### CI/CD 自动发布

```yaml
# .github/workflows/publish.yml
on:
  release:
    types: [published]

jobs:
  publish:
    steps:
      # 版本号已经在 tag 中
      # Cargo.toml 和 pyproject.toml 已同步
      - name: Build wheels
        run: maturin build --release
      
      - name: Publish to PyPI
        run: maturin publish
```

---

## ⚠️ 常见问题 / Common Issues

### 问题 1: 版本号不一致

**症状**:
```
❌ 版本号不一致 / Version mismatch!
  Cargo.toml:     0.1.0
  pyproject.toml: 0.1.1
  __init__.py:    0.1.0
```

**原因**: 手动修改了某个文件的版本号

**解决**:
```bash
# 1. 检查 .bumpversion.toml 中的 current_version
vim .bumpversion.toml

# 2. 手动同步所有文件到正确版本
# 3. 或使用 bump-my-version 重新设置
bump-my-version bump patch --new-version 0.1.1
```

### 问题 2: Cargo.toml 未更新

**症状**: Python 版本更新了，但 Rust 版本没变

**原因**: `.bumpversion.toml` 配置错误

**解决**:
```toml
# 确保 Cargo.toml 在配置文件中
[[tool.bumpversion.files]]
filename = "Cargo.toml"
search = "version = \"{current_version}\""
replace = "version = \"{new_version}\""
```

### 问题 3: 构建时版本不匹配

**症状**: `maturin build` 报错版本不一致

**原因**: Cargo.lock 过时

**解决**:
```bash
# 更新 Cargo.lock
cargo update -p vrl-python

# 或删除重新生成
rm Cargo.lock
cargo build
```

---

## 🎯 最佳实践 / Best Practices

### 1. 永远使用 make 命令

❌ **不要**:
```bash
# 手动编辑版本号
vim Cargo.toml
vim pyproject.toml
```

✅ **应该**:
```bash
# 使用 make 命令
make bump-dev
make bump-patch
```

### 2. 发布前验证

```bash
# 发布前检查清单
make check-version  # 验证版本一致性
make test          # 运行所有测试
make lint          # 代码检查
make build         # 构建验证
```

### 3. Git 工作流

```bash
# 版本升级会自动 commit 和 tag
make bump-minor

# 推送时包含 tags
git push origin develop --tags
```

### 4. 使用 dev 版本开发

```bash
# 开发阶段使用 dev 版本
make bump-dev      # 0.1.0 → 0.1.1-dev1

# 测试阶段使用 rc 版本
make bump-rc       # 0.1.1-dev3 → 0.1.1-rc1

# 发布阶段使用正式版本
make bump-release  # 0.1.1-rc1 → 0.1.1
```

---

## 📊 版本号追踪 / Version Tracking

### 查看版本历史

```bash
# Git tags
git tag -l

# 详细信息
git log --oneline --decorate --tags

# 特定版本的更改
git show v0.1.0
```

### 版本对比

```bash
# 对比两个版本
git diff v0.1.0..v0.2.0

# 查看版本间的提交
git log v0.1.0..v0.2.0 --oneline
```

---

## 🔗 相关文档 / Related Documentation

- `VERSION_MANAGEMENT.md` - 完整版本管理指南
- `VERSION_QUICK_REFERENCE.md` - 快速参考
- `.bumpversion.toml` - 配置文件
- `Makefile` - 版本管理命令

---

## 📝 总结 / Summary

### 关键点

1. ✅ **统一管理**: 使用 `bump-my-version` 统一管理所有版本号
2. ✅ **自动同步**: 一次操作同时更新 Rust 和 Python 版本
3. ✅ **自动提交**: 版本升级自动 commit 和 tag
4. ✅ **验证机制**: `make check-version` 确保一致性
5. ✅ **开发流程**: dev → rc → release 清晰的版本流程

### 工作流程

```
开发 → make bump-dev → 测试 → make bump-rc → 发布 → make bump-release
```

**Rust 和 Python 版本号始终保持同步！** ✅

---

**最后更新**: 2025-10-06  
**作者**: JQQ
