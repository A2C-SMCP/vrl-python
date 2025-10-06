/**
 * 文件名: lib.rs
 * 作者: JQQ
 * 创建日期: 2025/10/05
 * 最后修改日期: 2025/10/05
 * 版权: 2023 JQQ. All rights reserved.
 * 依赖: pyo3, vrl
 * 描述: VRL Python SDK 主入口文件 / VRL Python SDK main entry point
 */
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::Bound;

mod error;
mod runtime;
mod types;

use error::{VRLCompileError, VRLRuntimeError};
use runtime::VRLRuntime;
use types::{VRLDiagnostic, VRLResult};

/// VRL Python SDK
///
/// 这个模块提供了Vector Remap Language (VRL)的Python绑定
/// This module provides Python bindings for Vector Remap Language (VRL)
#[pymodule]
fn _vrl_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // 注册主要类 / Register main classes
    m.add_class::<VRLRuntime>()?;
    m.add_class::<VRLResult>()?;
    m.add_class::<VRLDiagnostic>()?;

    // 注册异常类型 / Register exception types
    m.add("VRLCompileError", m.py().get_type::<VRLCompileError>())?;
    m.add("VRLRuntimeError", m.py().get_type::<VRLRuntimeError>())?;

    // 添加版本信息 / Add version information
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    Ok(())
}
