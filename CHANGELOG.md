# Changelog / 更新日志

All notable changes to this project will be documented in this file.

本文件记录项目的所有重要变更。

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed / 变更
- ⬆️ 升级 PyO3 到 0.26 (最新版本) / Upgraded PyO3 to 0.26 (latest version)
- 🔄 适配 PyO3 0.26 的新 API (`Bound<'py, T>`, `Py<PyAny>`) / Adapted to PyO3 0.26 new API
- 🔧 使用 ordered-float 4.6 以匹配 VRL 依赖 / Using ordered-float 4.6 to match VRL dependency
- ♻️ 移除未使用的依赖 (serde, chrono, chrono-tz) / Removed unused dependencies

## [0.1.0] - 2025-10-06

### Added / 新增

#### 核心功能 / Core Features
- ✨ 实现 VRLRuntime 类，支持 VRL 程序的编译和执行
- ✨ 完整的 Python ↔ VRL 类型转换系统
- ✨ 编译缓存机制，提升重复执行性能
- ✨ 时区配置支持（支持所有 IANA 时区）
- ✨ 静态方法 `VRLRuntime.run()` 用于一次性执行

#### 类型支持 / Type Support
- ✅ 基础类型：null, boolean, integer, float, string
- ✅ 复合类型：array, object
- ✅ 特殊类型：timestamp, regex
- ✅ 正确处理 VRL 的 NotNan 浮点数类型

#### 错误处理 / Error Handling
- 🔧 自定义异常类型：VRLCompileError, VRLRuntimeError
- 🔧 详细的编译错误诊断信息
- 🔧 运行时错误追踪和报告
- 🔧 友好的错误消息（包含位置和建议）

#### 测试 / Testing
- ✅ 11 个单元测试，覆盖核心功能
- ✅ 测试简单赋值、JSON 解析、字段操作
- ✅ 测试类型转换、缓存机制
- ✅ 测试错误处理、时区配置
- ✅ 所有测试通过，执行时间 < 0.02s

#### 示例 / Examples
- 📚 7 个完整的使用示例
- 📚 涵盖常见使用场景
- 📚 包含错误处理最佳实践

#### 文档 / Documentation
- 📖 README.md - 项目介绍和快速开始
- 📖 DEVELOPMENT.md - 详细开发指南
- 📖 PROJECT_SUMMARY.md - 项目总结
- 📖 CHANGELOG.md - 版本更新日志
- 📖 代码注释（中英文双语）

#### 开发工具 / Development Tools
- 🛠️ Makefile - 简化常用命令
- 🛠️ quickstart.sh - 快速启动脚本
- 🛠️ requirements-dev.txt - 开发依赖列表
- 🛠️ .gitignore - Git 忽略规则
- 🛠️ .gitattributes - Git 属性配置

#### 构建配置 / Build Configuration
- ⚙️ Cargo.toml - Rust 项目配置
- ⚙️ pyproject.toml - Python 项目配置
- ⚙️ 支持 Python 3.8+ (abi3)
- ⚙️ 优化的发布构建配置（LTO, opt-level=3）

### Technical Details / 技术细节

#### Dependencies / 依赖
- pyo3 0.20 - Python 绑定
- vrl (main branch) - VRL 核心库
- serde 1.0 - 序列化支持
- serde_json 1.0 - JSON 处理
- chrono 0.4 - 时间处理
- chrono-tz 0.8 - 时区支持
- ordered-float 4.0 - NotNan 类型支持

#### Performance / 性能
- ⚡ 编译时间：< 1ms（首次）
- ⚡ 执行时间：0.00-0.04ms（简单操作）
- ⚡ 内存占用：极小（Rust 零成本抽象）
- ⚡ 编译缓存避免重复编译开销

#### Code Quality / 代码质量
- ✅ 所有测试通过
- ✅ 无编译警告
- ✅ 遵循 Rust 和 Python 最佳实践
- ✅ 完整的错误处理
- ✅ 详细的代码注释

### Known Issues / 已知问题

- ⚠️ 暂不支持自定义 VRL 函数注册
- ⚠️ 暂不支持 enrichment tables
- ⚠️ 暂不支持异步执行

### Future Plans / 未来计划

#### v0.2.0 (计划中)
- 🔮 添加自定义函数支持
- 🔮 支持 enrichment tables
- 🔮 性能基准测试
- 🔮 更多示例和文档

#### v0.3.0 (计划中)
- 🔮 异步执行支持
- 🔮 批量处理优化
- 🔮 CLI 工具
- 🔮 发布到 PyPI

### Contributors / 贡献者

- JQQ (@jqq1716) - Initial implementation

---

## Version History / 版本历史

### [Unreleased]
- 待定 / TBD

### [0.1.0] - 2025-10-06
- 🎉 首次发布 / Initial release
- ✨ 核心功能实现完成
- ✅ 所有测试通过
- 📖 文档完善

---

## Legend / 图例

- ✨ Added / 新增
- 🔧 Fixed / 修复
- 🔄 Changed / 变更
- 🗑️ Deprecated / 废弃
- ❌ Removed / 移除
- 🔒 Security / 安全
- ⚡ Performance / 性能
- 📖 Documentation / 文档
- 🛠️ Development / 开发
- ⚙️ Configuration / 配置
- ✅ Testing / 测试
- 🔮 Future / 未来
- ⚠️ Warning / 警告
