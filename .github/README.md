# GitHub 配置文件 / GitHub Configuration Files

本目录包含 vrl-python 项目的 GitHub Actions 工作流和相关配置。

This directory contains GitHub Actions workflows and related configurations for the vrl-python project.

---

## 📁 文件结构 / File Structure

```
.github/
├── workflows/
│   ├── ci.yml          # 持续集成 / Continuous Integration
│   ├── test.yml        # 测试工作流 / Test Workflow
│   └── publish.yml     # 发布工作流 / Publish Workflow
├── ENVIRONMENT_SETUP.md  # Environment 配置教程
├── RELEASE_GUIDE.md      # 发布指南
└── README.md             # 本文件
```

---

## 🔄 工作流说明 / Workflows

### 1. ci.yml - 持续集成

**触发条件**:
- Push 到 `main` 或 `develop` 分支
- Pull Request 到 `main` 分支

**功能**:
- 快速编译检查
- 运行 Rust 测试
- 多平台构建验证

### 2. test.yml - 完整测试

**触发条件**:
- Push 到 `main` 或 `develop` 分支
- Pull Request 到 `main` 分支

**功能**:
- 多平台测试 (Ubuntu, macOS, Windows)
- 多 Python 版本测试 (3.8-3.12)
- 代码覆盖率报告
- 代码质量检查 (Clippy, Black, Ruff)

### 3. publish.yml - 自动发布

**触发条件**:
- 创建 GitHub Release

**功能**:
- 构建多平台 wheels
- 构建 source distribution
- 根据 pre-release 标志自动选择发布目标：
  - ✅ Pre-release → TestPyPI
  - ❌ Release → PyPI

---

## 🚀 快速开始 / Quick Start

### 首次配置

1. **阅读配置教程**
   ```bash
   cat .github/ENVIRONMENT_SETUP.md
   ```

2. **配置 PyPI Trusted Publishing**
   - 访问 PyPI 和 TestPyPI
   - 添加 Trusted Publisher 配置

3. **创建 GitHub Environments**
   - 在 GitHub Settings 中创建 `pypi` 和 `testpypi` environments
   - 配置保护规则（可选）

### 发布新版本

1. **阅读发布指南**
   ```bash
   cat .github/RELEASE_GUIDE.md
   ```

2. **测试发布**
   ```bash
   # 创建测试版本
   git tag v0.1.0-beta.1
   git push origin v0.1.0-beta.1
   
   # 在 GitHub 创建 pre-release
   ```

3. **正式发布**
   ```bash
   # 创建正式版本
   git tag v0.1.0
   git push origin v0.1.0
   
   # 在 GitHub 创建 release
   ```

---

## 📚 文档索引 / Documentation Index

| 文档 | 用途 | 适合人群 |
|------|------|---------|
| `ENVIRONMENT_SETUP.md` | 详细的 Environment 配置教程 | 首次配置者 |
| `RELEASE_GUIDE.md` | 快速发布参考指南 | 日常发布者 |
| `workflows/ci.yml` | CI 工作流配置 | 开发者 |
| `workflows/test.yml` | 测试工作流配置 | 开发者 |
| `workflows/publish.yml` | 发布工作流配置 | 维护者 |

---

## 🔐 安全说明 / Security Notes

### Trusted Publishing

本项目使用 PyPI 的 Trusted Publishing 功能，**不需要**在 GitHub 中存储 API Token。

This project uses PyPI's Trusted Publishing feature and **does not require** storing API tokens in GitHub.

### 优势 / Benefits

- ✅ 无需管理 API Token
- ✅ 自动轮换凭证
- ✅ 更安全的发布流程
- ✅ 审计日志完整

### 要求 / Requirements

- GitHub Actions 工作流必须有 `id-token: write` 权限
- PyPI/TestPyPI 必须配置 Trusted Publisher
- Environment 名称必须完全匹配

---

## 🐛 故障排查 / Troubleshooting

### 常见问题

1. **工作流未触发**
   - 检查触发条件是否满足
   - 查看 Actions 页面的日志

2. **发布失败**
   - 检查 Environment 配置
   - 验证 Trusted Publisher 设置
   - 查看详细错误日志

3. **测试失败**
   - 本地运行测试验证
   - 检查依赖版本
   - 查看特定平台的错误

### 获取帮助

- 查看 [ENVIRONMENT_SETUP.md](./ENVIRONMENT_SETUP.md) 的故障排查章节
- 提交 Issue: https://github.com/A2C-SMCP/vrl-python/issues
- 查看 GitHub Actions 日志

---

## 🔄 更新工作流 / Updating Workflows

### 修改工作流

1. 编辑 `.github/workflows/*.yml` 文件
2. 提交更改
3. 推送到仓库
4. GitHub Actions 会自动使用新配置

### 测试工作流

```bash
# 使用 act 在本地测试（可选）
act -l  # 列出所有工作流
act push  # 模拟 push 事件
```

---

## 📊 徽章 / Badges

在 README.md 中添加工作流状态徽章：

```markdown
![CI](https://github.com/A2C-SMCP/vrl-python/workflows/CI/badge.svg)
![Test](https://github.com/A2C-SMCP/vrl-python/workflows/Test/badge.svg)
![PyPI](https://img.shields.io/pypi/v/vrl-python-sdk)
![Python](https://img.shields.io/pypi/pyversions/vrl-python-sdk)
```

---

## 📝 维护清单 / Maintenance Checklist

### 定期检查

- [ ] 更新 GitHub Actions 版本
- [ ] 检查依赖安全更新
- [ ] 验证工作流正常运行
- [ ] 审查 Environment 保护规则

### 版本发布前

- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG 已更新
- [ ] 版本号已同步

---

**最后更新 / Last Updated**: 2025-10-06  
**维护者 / Maintainer**: JQQ
