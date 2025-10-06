# 发布指南 / Release Guide

快速参考：如何发布 vrl-python 到 PyPI

---

## 🚀 快速发布流程

### 测试发布 (TestPyPI)

```bash
# 1. 创建测试版本 tag
git tag v0.1.0-beta.1
git push origin v0.1.0-beta.1

# 2. 在 GitHub 创建 Release
# - 访问: https://github.com/A2C-SMCP/vrl-python/releases/new
# - 选择 tag: v0.1.0-beta.1
# - ✅ 勾选 "Set as a pre-release"
# - 点击 "Publish release"

# 3. 等待 GitHub Actions 完成
# - 访问: https://github.com/A2C-SMCP/vrl-python/actions
# - 查看 "Publish to PyPI" 工作流

# 4. 验证发布
pip install --index-url https://test.pypi.org/simple/ vrl-python
```

### 正式发布 (PyPI)

```bash
# 1. 创建正式版本 tag
git tag v0.1.0
git push origin v0.1.0

# 2. 在 GitHub 创建 Release
# - 访问: https://github.com/A2C-SMCP/vrl-python/releases/new
# - 选择 tag: v0.1.0
# - ❌ 不要勾选 "Set as a pre-release"
# - 点击 "Publish release"

# 3. 等待审核（如果配置了）
# - 在 Actions 页面批准部署

# 4. 验证发布
pip install vrl-python
```

---

## 📋 发布前检查清单

### 代码准备
- [ ] 所有测试通过 (`pytest tests/ -v`)
- [ ] 代码已格式化 (`cargo fmt`, `black .`)
- [ ] 无 Clippy 警告 (`cargo clippy`)
- [ ] 文档已更新
- [ ] CHANGELOG.md 已更新

### 版本号
- [ ] `Cargo.toml` 中的版本号已更新
- [ ] `pyproject.toml` 中的版本号已更新
- [ ] 版本号遵循语义化版本规范

### Git 操作
- [ ] 所有更改已提交
- [ ] 已推送到 `main` 分支
- [ ] 创建了对应的 tag

---

## 🏷️ 版本号规范

### 语义化版本 (SemVer)

格式：`MAJOR.MINOR.PATCH[-PRERELEASE]`

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复
- **PRERELEASE**: 预发布版本标识

### 示例

| 版本 | 类型 | 发布到 | Pre-release |
|------|------|--------|-------------|
| `v1.0.0-alpha.1` | 开发版 | TestPyPI | ✅ |
| `v1.0.0-beta.1` | 测试版 | TestPyPI | ✅ |
| `v1.0.0-rc.1` | 候选版 | TestPyPI | ✅ |
| `v1.0.0` | 正式版 | PyPI | ❌ |
| `v1.0.1` | 补丁版 | PyPI | ❌ |
| `v1.1.0` | 功能版 | PyPI | ❌ |
| `v2.0.0` | 重大版 | PyPI | ❌ |

---

## 🔄 工作流说明

### 自动触发的工作流

1. **test.yml** - 测试工作流
   - 触发：Push 到 main/develop，PR 到 main
   - 运行：多平台、多 Python 版本测试

2. **ci.yml** - 持续集成
   - 触发：Push 到 main/develop，PR 到 main
   - 运行：快速检查和构建

3. **publish.yml** - 发布工作流
   - 触发：创建 Release
   - 运行：构建 wheels 并发布

### 发布逻辑

```
创建 Release
    ↓
检查 pre-release 标志
    ↓
    ├─ pre-release = true  → 发布到 TestPyPI (environment: testpypi)
    └─ pre-release = false → 发布到 PyPI (environment: pypi)
```

---

## 🛠️ 常用命令

### 版本管理

```bash
# 查看当前版本
grep version Cargo.toml | head -1

# 更新版本号（手动编辑）
vim Cargo.toml
vim pyproject.toml

# 创建 tag
git tag v0.1.0
git tag -a v0.1.0 -m "Release v0.1.0"  # 带注释的 tag

# 推送 tag
git push origin v0.1.0
git push origin --tags  # 推送所有 tags

# 删除 tag
git tag -d v0.1.0  # 本地
git push origin --delete v0.1.0  # 远程
```

### 测试安装

```bash
# 从 TestPyPI 安装
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    vrl-python

# 从 PyPI 安装
pip install vrl-python

# 安装特定版本
pip install vrl-python==0.1.0

# 升级到最新版本
pip install --upgrade vrl-python
```

### 本地构建测试

```bash
# 构建 wheel
maturin build --release

# 查看生成的文件
ls -lh target/wheels/

# 本地安装测试
pip install target/wheels/vrl_python_sdk-*.whl

# 构建 sdist
maturin sdist
```

---

## 🐛 故障排查

### 问题：工作流未触发

**检查**:
- 是否通过 GitHub UI 创建了 Release？
- Release 是否已 "Published"？

### 问题：发布失败 - "Environment not found"

**检查**:
- GitHub Settings → Environments 中是否创建了对应的 environment？
- `publish.yml` 中的 environment 名称是否正确？

### 问题：发布失败 - "Trusted publishing exchange failure"

**检查**:
- PyPI/TestPyPI 中的 Trusted Publisher 配置是否正确？
- Owner、Repository、Workflow、Environment 名称是否完全匹配？

### 问题：需要审核但没有收到通知

**检查**:
- GitHub Settings → Environments → 对应 environment → Required reviewers
- 确保审核者有仓库访问权限
- 检查 GitHub 通知设置

---

## 📊 发布后验证

### 1. 检查 PyPI 页面

- TestPyPI: https://test.pypi.org/project/vrl-python/
- PyPI: https://pypi.org/project/vrl-python/

### 2. 测试安装

```bash
# 创建新的虚拟环境
python -m venv test_env
source test_env/bin/activate

# 安装包
pip install vrl-python

# 测试导入
python -c "from vrl_python import VRLRuntime; print('✅ Import successful')"

# 运行快速测试
python -c "
from vrl_python import VRLRuntime
runtime = VRLRuntime()
result = runtime.execute('.test = \"ok\"', {})
assert result.processed_event['test'] == 'ok'
print('✅ Basic test passed')
"
```

### 3. 检查包信息

```bash
# 查看包信息
pip show vrl-python

# 查看包文件
pip show -f vrl-python
```

---

## 📝 Release 说明模板

```markdown
## vrl-python v0.1.0

### ✨ 新增功能 / New Features
- 功能描述

### 🔄 变更 / Changes
- 变更描述

### 🐛 修复 / Bug Fixes
- 修复描述

### 📚 文档 / Documentation
- 文档更新

### ⚡ 性能 / Performance
- 性能改进

### 🔧 其他 / Other
- 其他变更

---

**完整变更日志 / Full Changelog**: https://github.com/A2C-SMCP/vrl-python/compare/v0.0.1...v0.1.0

**安装 / Installation**:
```bash
pip install vrl-python==0.1.0
```
\`\`

**文档 / Documentation**: https://github.com/A2C-SMCP/vrl-python#readme
```
---
{{ ... }}
## 🎯 最佳实践

1. **先测试后发布**
   - 总是先发布到 TestPyPI 测试
   - 验证安装和基本功能
   - 确认无误后再发布到 PyPI

2. **保持版本一致**
   - `Cargo.toml` 和 `pyproject.toml` 版本号必须一致
   - Git tag 版本号必须匹配

3. **详细的 Release 说明**
   - 列出所有重要变更
   - 包含升级指南（如有破坏性变更）
   - 添加示例代码

4. **及时更新文档**
   - CHANGELOG.md
   - README.md
   - API 文档

---

**需要帮助？**
- 查看详细教程：`.github/ENVIRONMENT_SETUP.md`
- 提交 Issue：https://github.com/A2C-SMCP/vrl-python/issues
