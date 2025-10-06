# Environment 名称配置说明 / Environment Names Configuration

## ⚠️ 重要：名称必须完全一致

Environment 名称必须在以下**三个地方**保持**完全一致**（包括大小写）：

1. **PyPI/TestPyPI Trusted Publisher 配置**
2. **GitHub Settings → Environments**
3. **GitHub Actions 工作流文件** (`.github/workflows/publish.yml`)

---

## 📋 标准配置（推荐）

### 正式发布环境

| 位置 | 配置项 | 值 |
|------|--------|-----|
| PyPI Trusted Publisher | Environment name | `pypi` |
| GitHub Settings | Environment 名称 | `pypi` |
| publish.yml | environment.name | `pypi` |

### 测试发布环境

| 位置 | 配置项 | 值 |
|------|--------|-----|
| TestPyPI Trusted Publisher | Environment name | `testpypi` |
| GitHub Settings | Environment 名称 | `testpypi` |
| publish.yml | environment.name | `testpypi` |

---

## 🔍 如何检查当前配置

### 1. 检查 PyPI Trusted Publisher

**PyPI (正式环境)**:
- 访问：https://pypi.org/manage/account/publishing/
- 查找 `vrl-python` 项目
- 查看 "Environment name" 字段

**TestPyPI (测试环境)**:
- 访问：https://test.pypi.org/manage/account/publishing/
- 查找 `vrl-python` 项目
- 查看 "Environment name" 字段

### 2. 检查 GitHub Environments

- 访问：https://github.com/A2C-SMCP/vrl-python/settings/environments
- 查看已创建的 Environment 列表
- 记录每个 Environment 的名称

### 3. 检查工作流文件

```bash
# 查看 publish.yml 中的 environment 配置
grep -A 2 "environment:" .github/workflows/publish.yml
```

应该看到：
```yaml
environment:
  name: testpypi  # 测试环境
  
environment:
  name: pypi      # 正式环境
```

---

## ✏️ 如何修改 Environment 名称

### 场景 1: 你想使用不同的名称

例如，你想使用：
- `publish` 代替 `pypi`
- `test-publish` 代替 `testpypi`

**步骤**:

1. **修改 PyPI Trusted Publisher**
   - 删除旧的配置
   - 添加新的配置，使用新的 Environment name

2. **修改 GitHub Environments**
   - 创建新的 Environment（使用新名称）
   - 删除旧的 Environment（可选）

3. **修改 publish.yml**
   ```yaml
   environment:
     name: publish  # 改为你的新名称
   ```

### 场景 2: 名称不一致，需要统一

**推荐方案**：以 PyPI Trusted Publisher 的配置为准

1. 查看 PyPI/TestPyPI 中配置的 Environment name
2. 在 GitHub 创建对应名称的 Environment
3. 修改 `publish.yml` 使用相同的名称

---

## 🚨 常见错误

### 错误 1: Environment not found

**错误信息**:
```
Error: The environment 'pypi' was not found
```

**原因**: GitHub Settings 中没有创建名为 `pypi` 的 Environment

**解决**:
- 访问 Settings → Environments
- 创建名为 `pypi` 的 Environment

### 错误 2: Trusted publishing exchange failure

**错误信息**:
```
Error: Trusted publishing exchange failure
```

**原因**: PyPI Trusted Publisher 配置的 Environment name 与实际使用的不一致

**解决**:
- 检查 PyPI 配置中的 Environment name
- 确保与 publish.yml 中的 `environment.name` 一致

### 错误 3: 大小写不匹配

**错误信息**:
```
Error: Environment 'PyPI' not found
```

**原因**: Environment 名称大小写敏感

**解决**:
- 统一使用小写：`pypi`、`testpypi`
- 或统一使用你选择的大小写格式

---

## 📝 配置检查清单

使用此清单确保配置正确：

### PyPI 配置
- [ ] 访问 PyPI Trusted Publisher 设置
- [ ] 记录 Environment name: `__________`
- [ ] 确认配置已保存

### TestPyPI 配置
- [ ] 访问 TestPyPI Trusted Publisher 设置
- [ ] 记录 Environment name: `__________`
- [ ] 确认配置已保存

### GitHub Environments
- [ ] 访问 GitHub Settings → Environments
- [ ] 创建 Environment: `__________` (对应 PyPI)
- [ ] 创建 Environment: `__________` (对应 TestPyPI)
- [ ] 配置保护规则（可选）

### 工作流文件
- [ ] 打开 `.github/workflows/publish.yml`
- [ ] 检查 `publish-pypi` job 的 `environment.name`
- [ ] 检查 `publish-testpypi` job 的 `environment.name`
- [ ] 确认与上面的名称一致

---

## 🎯 推荐的命名规范

### 标准命名（推荐）
```yaml
pypi        # 正式环境
testpypi    # 测试环境
```

**优点**:
- 简洁明了
- 与 PyPI 平台名称对应
- 易于记忆

### 替代命名方案

```yaml
# 方案 1: 带前缀
prod-pypi
test-pypi

# 方案 2: 描述性
production
testing

# 方案 3: 项目特定
vrl-python-prod
vrl-python-test
```

**注意**: 无论选择哪种方案，确保三个地方使用相同的名称！

---

## 🔄 修改名称的完整流程

如果你需要修改 Environment 名称：

### 步骤 1: 更新 PyPI Trusted Publisher

1. 访问 PyPI/TestPyPI Trusted Publisher 设置
2. 删除现有的 publisher 配置
3. 添加新的配置，使用新的 Environment name

### 步骤 2: 更新 GitHub Environments

1. 访问 GitHub Settings → Environments
2. 创建新的 Environment（使用新名称）
3. 配置保护规则
4. 删除旧的 Environment（可选）

### 步骤 3: 更新工作流文件

```bash
# 编辑 publish.yml
vim .github/workflows/publish.yml

# 修改 environment.name 为新名称
# 保存并提交
git add .github/workflows/publish.yml
git commit -m "chore: update environment names"
git push
```

### 步骤 4: 验证配置

创建一个测试 release 验证配置是否正确。

---

## 📚 相关文档

- [ENVIRONMENT_SETUP.md](./ENVIRONMENT_SETUP.md) - 详细配置教程
- [RELEASE_GUIDE.md](./RELEASE_GUIDE.md) - 发布指南
- [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md) - 配置清单

---

## 💡 快速参考

**当前推荐配置**:

```yaml
# publish.yml
environment:
  name: pypi        # 正式发布
  
environment:
  name: testpypi    # 测试发布
```

**对应的 GitHub Environments**:
- `pypi`
- `testpypi`

**对应的 PyPI Trusted Publisher**:
- PyPI: Environment name = `pypi`
- TestPyPI: Environment name = `testpypi`

---

**最后更新**: 2025-10-06  
**维护者**: JQQ
