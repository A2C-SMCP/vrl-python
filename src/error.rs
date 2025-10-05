/**
 * 文件名: error.rs
 * 作者: JQQ
 * 创建日期: 2025/10/05
 * 最后修改日期: 2025/10/06
 * 版权: 2023 JQQ. All rights reserved.
 * 依赖: pyo3
 * 描述: VRL错误类型定义 / VRL error type definitions
 */

use pyo3::{create_exception, exceptions::PyException};

// 创建自定义异常类型 / Create custom exception types
// 使用 create_exception! 宏而不是 pyclass
create_exception!(_vrl_python, VRLCompileError, PyException, "VRL compilation error");
create_exception!(_vrl_python, VRLRuntimeError, PyException, "VRL runtime error");
