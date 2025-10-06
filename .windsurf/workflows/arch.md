---
description: 项目架构
---

# 架构描述

1. 本项目使用PyO3+Maturin将Vector项目中的VRL模块（VRL也是独立项目）开发Python可用接口
2. Python使用uv管理环境，Rust则使用Cargo管理
3. 使用bump-my-version管理版本
4. 使用github actions管理CI/CD流程

# 文档规范

1. 除了README.md与CHANGELOG.md外，其它使用文档放在 @docs 目录下

# 测试规范

1. 重点测试Python暴露的端口。
2. 使用pytest进行测试
3. 注意使用uv虚拟环境。