# GitHub Environment 配置教程 / GitHub Environment Setup Guide

本教程将指导你如何在 GitHub 上创建和配置 Environments，用于 PyPI 的 Trusted Publishing。

This guide will walk you through creating and configuring GitHub Environments for PyPI Trusted Publishing.

---

## 📋 前置要求 / Prerequisites

1. ✅ GitHub 仓库：`A2C-SMCP/vrl-python`
2. ✅ PyPI 账号（用于正式发布）
3. ✅ TestPyPI 账号（用于测试发布）
4. ✅ 仓库管理员权限

---

## 🔧 步骤 1: 在 PyPI 配置 Trusted Publishing

### 1.1 配置 PyPI (正式环境)

1. **登录 PyPI**
   - 访问：https://pypi.org/
   - 使用你的账号登录

2. **进入 Publishing 设置**
   - 点击右上角头像 → "Your projects"
   - 如果项目已存在，点击项目名称
   - 如果是新项目，需要先手动上传一次（或跳过，直接配置）

3. **添加 Trusted Publisher**
   - 进入项目页面
   - 点击 "Manage" → "Publishing"
   - 或直接访问：https://pypi.org/manage/account/publishing/
   
4. **配置 GitHub Actions**
   - 点击 "Add a new publisher"
   - 选择 "GitHub"
   - 填写以下信息：
     ```
     PyPI Project Name: vrl-python
     Owner: A2C-SMCP
     Repository name: vrl-python
     Workflow name: publish.yml
     Environment name: pypi
     ```
   - 点击 "Add"

### 1.2 配置 TestPyPI (测试环境)

1. **登录 TestPyPI**
   - 访问：https://test.pypi.org/
   - 使用你的账号登录

2. **添加 Trusted Publisher**
   - 访问：https://test.pypi.org/manage/account/publishing/
   - 点击 "Add a new publisher"
   - 选择 "GitHub"
   - 填写以下信息：
     ```
     PyPI Project Name: vrl-python
     Owner: A2C-SMCP
     Repository name: vrl-python
     Workflow name: publish.yml
     Environment name: testpypi
     ```
   - 点击 "Add"

---

## 🌍 步骤 2: 在 GitHub 创建 Environments

### 2.1 访问 Environment 设置

1. 打开你的 GitHub 仓库：https://github.com/A2C-SMCP/vrl-python
2. 点击 "Settings" (设置) 标签
3. 在左侧菜单中找到 "Environments"
4. 如果看不到，确保你有仓库的管理员权限

### 2.2 创建 `pypi` Environment (正式发布)

1. **创建 Environment**
   - 点击 "New environment"
   - 名称输入：`pypi`
   - 点击 "Configure environment"

2. **配置保护规则（推荐）**
   - ✅ **Required reviewers**: 添加审核者（可选，建议至少1人）
     - 这样每次发布前需要人工审核
   - ✅ **Wait timer**: 设置等待时间（可选）
     - 例如：5 分钟，给你时间取消错误的发布
   - ✅ **Deployment branches**: 限制分支
     - 选择 "Selected branches"
     - 添加规则：`main` 或 `refs/tags/*`

3. **Environment secrets（不需要）**
   - 使用 Trusted Publishing 时，**不需要**添加 API Token
   - GitHub 会自动处理认证

4. **保存配置**
   - 点击 "Save protection rules"

### 2.3 创建 `testpypi` Environment (测试发布)

1. **创建 Environment**
   - 返回 Environments 页面
   - 点击 "New environment"
   - 名称输入：`testpypi`
   - 点击 "Configure environment"

2. **配置保护规则（可选）**
   - 测试环境可以不设置审核者
   - 或设置较短的等待时间（如 1 分钟）

3. **保存配置**

---

## 📸 配置截图参考 / Configuration Screenshots Reference

### PyPI Trusted Publisher 配置示例

```
┌─────────────────────────────────────────────────┐
│ Add a new pending publisher                     │
├─────────────────────────────────────────────────┤
│ PyPI Project Name: vrl-python                   │
│ Owner: A2C-SMCP                                 │
│ Repository name: vrl-python                     │
│ Workflow name: publish.yml                      │
│ Environment name: pypi                          │
│                                                 │
│ [Add] [Cancel]                                  │
└─────────────────────────────────────────────────┘
```

### GitHub Environment 配置示例

```
┌─────────────────────────────────────────────────┐
│ Environment: pypi                               │
├─────────────────────────────────────────────────┤
│ Environment protection rules                    │
│                                                 │
│ ☑ Required reviewers                           │
│   └─ @your-username                            │
│                                                 │
│ ☑ Wait timer                                   │
│   └─ 5 minutes                                 │
│                                                 │
│ ☑ Deployment branches                         │
│   └─ Selected branches: main                   │
│                                                 │
│ [Save protection rules]                         │
└─────────────────────────────────────────────────┘
```

---

## 🚀 步骤 3: 测试发布流程

### 3.1 创建 Pre-release (测试发布到 TestPyPI)

1. **创建 Git Tag**
   ```bash
   git tag v0.1.0-beta.1
   git push origin v0.1.0-beta.1
   ```

2. **在 GitHub 创建 Release**
   - 访问：https://github.com/A2C-SMCP/vrl-python/releases/new
   - 选择刚才创建的 tag：`v0.1.0-beta.1`
   - 填写 Release 标题：`v0.1.0-beta.1`
   - 填写 Release 说明
   - ✅ **勾选 "Set as a pre-release"** ← 重要！
   - 点击 "Publish release"

3. **查看工作流执行**
   - 访问：https://github.com/A2C-SMCP/vrl-python/actions
   - 找到 "Publish to PyPI" 工作流
   - 应该会执行 `publish-testpypi` job
   - 如果配置了审核者，需要先批准

4. **验证发布**
   - 访问：https://test.pypi.org/project/vrl-python/
   - 应该能看到新版本

### 3.2 创建正式 Release (发布到 PyPI)

1. **创建 Git Tag**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **在 GitHub 创建 Release**
   - 访问：https://github.com/A2C-SMCP/vrl-python/releases/new
   - 选择 tag：`v0.1.0`
   - 填写 Release 标题：`v0.1.0`
   - 填写 Release 说明
   - ❌ **不要勾选 "Set as a pre-release"** ← 重要！
   - 点击 "Publish release"

3. **查看工作流执行**
   - 应该会执行 `publish-pypi` job
   - 如果配置了审核者，需要先批准

4. **验证发布**
   - 访问：https://pypi.org/project/vrl-python/
   - 应该能看到新版本

---

## 🔍 故障排查 / Troubleshooting

### 问题 1: "Environment not found"

**原因**: Environment 名称不匹配

**解决**:
- 检查 `publish.yml` 中的 `environment.name` 是否为 `pypi` 或 `testpypi`
- 检查 GitHub Settings → Environments 中是否创建了对应的 environment

### 问题 2: "Trusted publishing exchange failure"

**原因**: PyPI Trusted Publisher 配置错误

**解决**:
- 检查 PyPI/TestPyPI 中的配置是否正确
- 确保 Owner、Repository、Workflow、Environment 名称完全匹配
- 注意大小写敏感

### 问题 3: "Permission denied"

**原因**: 缺少 OIDC token 权限

**解决**:
- 确保 `publish.yml` 中有：
  ```yaml
  permissions:
    contents: read
    id-token: write
  ```

### 问题 4: 工作流不触发

**原因**: Release 事件配置问题

**解决**:
- 确保是通过 GitHub UI 创建的 Release，而不是只推送 tag
- 检查 `on.release.types` 是否包含 `[published]`

---

## 📝 完整配置检查清单 / Complete Configuration Checklist

### PyPI 配置
- [ ] PyPI 账号已创建
- [ ] 在 PyPI 添加了 Trusted Publisher
  - [ ] Project Name: `vrl-python`
  - [ ] Owner: `A2C-SMCP`
  - [ ] Repository: `vrl-python`
  - [ ] Workflow: `publish.yml`
  - [ ] Environment: `pypi`

### TestPyPI 配置
- [ ] TestPyPI 账号已创建
- [ ] 在 TestPyPI 添加了 Trusted Publisher
  - [ ] Project Name: `vrl-python`
  - [ ] Owner: `A2C-SMCP`
  - [ ] Repository: `vrl-python`
  - [ ] Workflow: `publish.yml`
  - [ ] Environment: `testpypi`

### GitHub 配置
- [ ] 创建了 `pypi` environment
  - [ ] 配置了保护规则（可选）
  - [ ] 配置了审核者（可选）
- [ ] 创建了 `testpypi` environment
- [ ] 工作流文件已提交
  - [ ] `.github/workflows/publish.yml`
  - [ ] `.github/workflows/test.yml`
  - [ ] `.github/workflows/ci.yml`

### 测试
- [ ] 创建 pre-release 测试 TestPyPI 发布
- [ ] 验证 TestPyPI 上的包
- [ ] 创建正式 release 测试 PyPI 发布
- [ ] 验证 PyPI 上的包

---

## 🎯 最佳实践 / Best Practices

### 1. 版本号规范

使用语义化版本：
- **正式版本**: `v1.0.0`, `v1.1.0`, `v2.0.0`
- **测试版本**: `v1.0.0-beta.1`, `v1.0.0-rc.1`
- **开发版本**: `v1.0.0-alpha.1`

### 2. Release 说明模板

```markdown
## What's Changed

### Added
- 新功能描述

### Changed
- 变更描述

### Fixed
- 修复描述

**Full Changelog**: https://github.com/A2C-SMCP/vrl-python/compare/v0.0.1...v0.1.0
```

### 3. 发布流程

1. **开发阶段**: 在 `develop` 分支开发
2. **测试阶段**: 创建 pre-release，发布到 TestPyPI
3. **验证阶段**: 从 TestPyPI 安装并测试
4. **发布阶段**: 合并到 `main`，创建正式 release

### 4. 安全建议

- ✅ 始终使用 Trusted Publishing，不要使用 API Token
- ✅ 为 `pypi` environment 配置审核者
- ✅ 限制可以触发发布的分支
- ✅ 定期检查发布日志

---

## 📚 参考资料 / References

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Maturin Documentation](https://www.maturin.rs/)

---

## 💡 快速命令参考 / Quick Command Reference

```bash
# 创建测试版本
git tag v0.1.0-beta.1
git push origin v0.1.0-beta.1

# 创建正式版本
git tag v0.1.0
git push origin v0.1.0

# 查看所有 tags
git tag -l

# 删除本地 tag
git tag -d v0.1.0

# 删除远程 tag
git push origin --delete v0.1.0

# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ vrl-python

# 从 PyPI 安装正式版
pip install vrl-python
```

---

**最后更新 / Last Updated**: 2025-10-06  
**作者 / Author**: JQQ
