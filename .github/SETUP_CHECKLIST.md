# GitHub Actions 配置检查清单 / Setup Checklist

逐步完成以下步骤，确保 GitHub Actions 正确配置。

---

## 📋 配置检查清单 / Configuration Checklist

### Phase 1: PyPI 配置 (30 分钟)

#### ☐ 1.1 配置 PyPI Trusted Publisher

- [ ] 访问 https://pypi.org/
- [ ] 登录你的 PyPI 账号
- [ ] 进入 Account Settings → Publishing
  - 直接链接: https://pypi.org/manage/account/publishing/
- [ ] 点击 "Add a new pending publisher"
- [ ] 选择 "GitHub"
- [ ] 填写以下信息：
  ```
  PyPI Project Name: vrl-python
  Owner: A2C-SMCP
  Repository name: vrl-python
  Workflow name: publish.yml
  Environment name: pypi
  ```
- [ ] 点击 "Add"
- [ ] 确认看到 "Pending publisher added" 消息

#### ☐ 1.2 配置 TestPyPI Trusted Publisher

- [ ] 访问 https://test.pypi.org/
- [ ] 登录你的 TestPyPI 账号
- [ ] 进入 Account Settings → Publishing
  - 直接链接: https://test.pypi.org/manage/account/publishing/
- [ ] 点击 "Add a new pending publisher"
- [ ] 选择 "GitHub"
- [ ] 填写以下信息：
  ```
  PyPI Project Name: vrl-python
  Owner: A2C-SMCP
  Repository name: vrl-python
  Workflow name: publish.yml
  Environment name: testpypi
  ```
- [ ] 点击 "Add"
- [ ] 确认看到 "Pending publisher added" 消息

---

### Phase 2: GitHub Environment 配置 (15 分钟)

#### ☐ 2.1 创建 `pypi` Environment

- [ ] 访问 https://github.com/A2C-SMCP/vrl-python
- [ ] 点击 "Settings" 标签
- [ ] 在左侧菜单找到 "Environments"
- [ ] 点击 "New environment"
- [ ] 名称输入：`pypi`
- [ ] 点击 "Configure environment"

**配置保护规则（推荐）**:
- [ ] ✅ 勾选 "Required reviewers"
  - [ ] 添加至少 1 个审核者（你自己）
- [ ] ✅ 勾选 "Wait timer"
  - [ ] 设置：5 分钟
- [ ] ✅ 勾选 "Deployment branches and tags"
  - [ ] 选择 "Selected branches and tags"
  - [ ] 添加规则：`main`
  - [ ] 或添加：`refs/tags/*`

- [ ] 点击 "Save protection rules"

#### ☐ 2.2 创建 `testpypi` Environment

- [ ] 返回 Environments 页面
- [ ] 点击 "New environment"
- [ ] 名称输入：`testpypi`
- [ ] 点击 "Configure environment"

**配置保护规则（可选）**:
- [ ] 可以不设置审核者（测试环境）
- [ ] 或设置较短的等待时间（1 分钟）

- [ ] 点击 "Save protection rules"（如果配置了）

---

### Phase 3: 验证工作流文件 (5 分钟)

#### ☐ 3.1 检查文件是否存在

```bash
cd /Users/jqq/RustroverProjects/vrl-python
ls -la .github/workflows/
```

应该看到：
- [ ] `ci.yml`
- [ ] `test.yml`
- [ ] `publish.yml`

#### ☐ 3.2 提交工作流文件

```bash
git add .github/
git commit -m "feat: add GitHub Actions workflows for CI/CD and publishing"
git push origin main
```

- [ ] 文件已提交到 GitHub

#### ☐ 3.3 验证工作流已识别

- [ ] 访问 https://github.com/A2C-SMCP/vrl-python/actions
- [ ] 应该看到 3 个工作流：
  - [ ] CI
  - [ ] Test
  - [ ] Publish to PyPI

---

### Phase 4: 测试发布流程 (30 分钟)

#### ☐ 4.1 准备测试版本

- [ ] 确保所有测试通过
  ```bash
  pytest tests/ -v
  ```

- [ ] 更新版本号（如果需要）
  - [ ] 编辑 `Cargo.toml`
  - [ ] 编辑 `pyproject.toml`
  - [ ] 确保版本号一致

- [ ] 提交更改
  ```bash
  git add Cargo.toml pyproject.toml
  git commit -m "chore: bump version to 0.1.0-beta.1"
  git push origin main
  ```

#### ☐ 4.2 创建测试版本 Tag

```bash
git tag v0.1.0-beta.1
git push origin v0.1.0-beta.1
```

- [ ] Tag 已推送到 GitHub

#### ☐ 4.3 创建 Pre-release

- [ ] 访问 https://github.com/A2C-SMCP/vrl-python/releases/new
- [ ] 选择 tag: `v0.1.0-beta.1`
- [ ] Release title: `v0.1.0-beta.1`
- [ ] 填写 Release 说明（可以简单写测试）
- [ ] ✅ **勾选 "Set as a pre-release"** ← 重要！
- [ ] 点击 "Publish release"

#### ☐ 4.4 监控工作流执行

- [ ] 访问 https://github.com/A2C-SMCP/vrl-python/actions
- [ ] 找到 "Publish to PyPI" 工作流
- [ ] 点击查看详情
- [ ] 等待 `build-wheels` 和 `build-sdist` 完成
- [ ] 如果配置了审核者，批准 `publish-testpypi` 部署
- [ ] 等待发布完成

#### ☐ 4.5 验证 TestPyPI 发布

- [ ] 访问 https://test.pypi.org/project/vrl-python/
- [ ] 应该看到 `0.1.0b1` 版本
- [ ] 测试安装：
  ```bash
  pip install --index-url https://test.pypi.org/simple/ \
      --extra-index-url https://pypi.org/simple/ \
      vrl-python
  ```
- [ ] 测试导入：
  ```bash
  python -c "from vrl_python import VRLRuntime; print('✅ OK')"
  ```

---

### Phase 5: 正式发布测试 (可选，30 分钟)

#### ☐ 5.1 创建正式版本 Tag

```bash
git tag v0.1.0
git push origin v0.1.0
```

- [ ] Tag 已推送到 GitHub

#### ☐ 5.2 创建 Release

- [ ] 访问 https://github.com/A2C-SMCP/vrl-python/releases/new
- [ ] 选择 tag: `v0.1.0`
- [ ] Release title: `v0.1.0`
- [ ] 填写详细的 Release 说明
- [ ] ❌ **不要勾选 "Set as a pre-release"** ← 重要！
- [ ] 点击 "Publish release"

#### ☐ 5.3 监控工作流执行

- [ ] 访问 Actions 页面
- [ ] 找到 "Publish to PyPI" 工作流
- [ ] 等待构建完成
- [ ] 如果配置了审核者，批准 `publish-pypi` 部署
- [ ] 等待发布完成

#### ☐ 5.4 验证 PyPI 发布

- [ ] 访问 https://pypi.org/project/vrl-python/
- [ ] 应该看到 `0.1.0` 版本
- [ ] 测试安装：
  ```bash
  pip install vrl-python
  ```
- [ ] 测试导入：
  ```bash
  python -c "from vrl_python import VRLRuntime; print('✅ OK')"
  ```

---

## 🎯 完成状态 / Completion Status

### 总体进度

- [ ] Phase 1: PyPI 配置 (0/2)
- [ ] Phase 2: GitHub Environment 配置 (0/2)
- [ ] Phase 3: 验证工作流文件 (0/3)
- [ ] Phase 4: 测试发布流程 (0/5)
- [ ] Phase 5: 正式发布测试 (0/4) - 可选

**总进度**: 0/16 (0%)

---

## 📸 配置截图保存位置

建议保存配置截图到：
```
docs/screenshots/
├── pypi-trusted-publisher.png
├── testpypi-trusted-publisher.png
├── github-environment-pypi.png
├── github-environment-testpypi.png
└── github-actions-workflows.png
```

---

## 🆘 遇到问题？

### 快速参考

- **详细教程**: `.github/ENVIRONMENT_SETUP.md`
- **发布指南**: `.github/RELEASE_GUIDE.md`
- **故障排查**: 查看教程中的 Troubleshooting 章节

### 获取帮助

1. 查看 GitHub Actions 日志
2. 检查 PyPI/TestPyPI 配置
3. 提交 Issue: https://github.com/A2C-SMCP/vrl-python/issues

---

## ✅ 配置完成确认

完成所有步骤后，在此签名确认：

```
配置完成日期: _______________
配置人员: _______________
验证人员: _______________
```

---

**祝配置顺利！🎉**
