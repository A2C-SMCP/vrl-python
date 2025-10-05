/**
 * 文件名: runtime.rs
 * 作者: JQQ
 * 创建日期: 2025/10/05
 * 最后修改日期: 2025/10/05
 * 版权: 2023 JQQ. All rights reserved.
 * 依赖: pyo3, vrl
 * 描述: VRL运行时核心实现 / VRL runtime core implementation
 */

use pyo3::prelude::*;
use std::collections::BTreeMap;
use std::time::Instant;
use vrl::compiler::{
    CompileConfig, Program, TargetValue, TimeZone, TypeState,
    compile_with_state,
    runtime::{Runtime, Terminate},
};
use vrl::diagnostic::{DiagnosticList, Formatter};
use vrl::value::{Secrets, Value};

use crate::types::{VRLResult, VRLDiagnostic, py_to_vrl_value, vrl_value_to_py};

/// VRL运行时 / VRL Runtime
/// 
/// 用于编译和执行VRL程序的主要类
/// Main class for compiling and executing VRL programs
#[pyclass]
pub struct VRLRuntime {
    /// 时区配置 / Timezone configuration
    timezone: TimeZone,
    
    /// 已编译的程序缓存 / Compiled program cache
    compiled_program: Option<Program>,
    
    /// 缓存的程序源码 / Cached program source
    cached_source: Option<String>,
}

#[pymethods]
impl VRLRuntime {
    /// 创建新的VRL运行时实例 / Create a new VRL runtime instance
    /// 
    /// Args:
    ///     timezone: 时区名称，如"UTC"、"Asia/Shanghai"等 / Timezone name like "UTC", "Asia/Shanghai"
    #[new]
    #[pyo3(signature = (timezone=None))]
    pub fn new(timezone: Option<String>) -> PyResult<Self> {
        let tz = match timezone.as_deref() {
            None | Some("") | Some("local") => TimeZone::default(),
            Some(tz_str) => match tz_str.parse() {
                Ok(tz) => TimeZone::Named(tz),
                Err(_) => {
                    return Err(pyo3::exceptions::PyValueError::new_err(
                        format!("Invalid timezone identifier: '{}'", tz_str)
                    ));
                }
            },
        };
        
        Ok(VRLRuntime {
            timezone: tz,
            compiled_program: None,
            cached_source: None,
        })
    }
    
    /// 编译VRL程序 / Compile VRL program
    /// 
    /// Args:
    ///     source: VRL程序源码 / VRL program source code
    /// 
    /// Returns:
    ///     编译成功返回True，失败抛出异常 / Returns True on success, raises exception on failure
    pub fn compile(&mut self, source: String) -> PyResult<bool> {
        let functions = vrl::stdlib::all();
        let state = TypeState::default();
        let config = CompileConfig::default();
        
        match compile_with_state(&source, &functions, &state, config) {
            Ok(result) => {
                self.compiled_program = Some(result.program);
                self.cached_source = Some(source);
                Ok(true)
            }
            Err(diagnostics) => {
                let diagnostic = create_diagnostic(&source, diagnostics);
                Err(pyo3::exceptions::PyValueError::new_err(
                    diagnostic.formatted_message
                ))
            }
        }
    }
    
    /// 执行VRL程序 / Execute VRL program
    /// 
    /// Args:
    ///     source: VRL程序源码 / VRL program source code
    ///     event: 输入事件数据（Python字典）/ Input event data (Python dict)
    /// 
    /// Returns:
    ///     VRLResult: 包含处理结果的对象 / Object containing processing results
    pub fn execute(&mut self, py: Python, source: String, event: &Bound<'_, PyAny>) -> PyResult<VRLResult> {
        // 如果源码与缓存不同，重新编译 / Recompile if source differs from cache
        if self.cached_source.as_ref() != Some(&source) {
            self.compile(source.clone())?;
        }
        
        let program = self.compiled_program.as_ref()
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err("Program not compiled"))?;
        
        // 转换输入事件 / Convert input event
        let event_value = py_to_vrl_value(py, event)?;
        
        // 创建目标值 / Create target value
        let mut target_value = TargetValue {
            value: event_value,
            metadata: Value::Object(BTreeMap::new()),
            secrets: Secrets::new(),
        };
        
        // 创建运行时并执行 / Create runtime and execute
        let mut runtime = Runtime::default();
        let start = Instant::now();
        
        let result = runtime.resolve(&mut target_value, program, &self.timezone);
        let elapsed = start.elapsed();
        
        match result {
            Ok(runtime_result) => {
                // 转换结果为Python对象 / Convert results to Python objects
                let processed_event = vrl_value_to_py(py, &target_value.value)?;
                let runtime_result_py = vrl_value_to_py(py, &runtime_result)?;
                
                Ok(VRLResult {
                    processed_event,
                    runtime_result: runtime_result_py,
                    elapsed_ms: Some(elapsed.as_secs_f64() * 1000.0),
                })
            }
            Err(terminate) => {
                let diagnostic = create_runtime_diagnostic(
                    self.cached_source.as_ref().unwrap(),
                    terminate
                );
                Err(pyo3::exceptions::PyRuntimeError::new_err(
                    diagnostic.formatted_message
                ))
            }
        }
    }
    
    /// 快速执行（一次性编译并执行）/ Quick execute (compile and execute in one call)
    /// 
    /// 这是一个便捷方法，适合一次性执行的场景
    /// This is a convenience method for one-time execution scenarios
    #[staticmethod]
    pub fn run(py: Python, source: String, event: &Bound<'_, PyAny>, timezone: Option<String>) -> PyResult<VRLResult> {
        let mut runtime = VRLRuntime::new(timezone)?;
        runtime.execute(py, source, event)
    }
    
    /// 清除编译缓存 / Clear compilation cache
    pub fn clear_cache(&mut self) {
        self.compiled_program = None;
        self.cached_source = None;
    }
    
    /// 检查VRL程序语法 / Check VRL program syntax
    /// 
    /// 这个方法只检查语法，不执行程序，返回详细的诊断信息
    /// This method only checks syntax without execution, returns detailed diagnostics
    /// 
    /// Args:
    ///     source: VRL程序源码 / VRL program source code
    /// 
    /// Returns:
    ///     Option[VRLDiagnostic]: 如果有错误返回诊断信息，否则返回None / Returns diagnostics if errors, None otherwise
    #[staticmethod]
    pub fn check_syntax(source: String) -> Option<VRLDiagnostic> {
        let functions = vrl::stdlib::all();
        let state = TypeState::default();
        let config = CompileConfig::default();
        
        match compile_with_state(&source, &functions, &state, config) {
            Ok(_) => None,
            Err(diagnostics) => Some(create_diagnostic(&source, diagnostics)),
        }
    }
    
    fn __repr__(&self) -> String {
        format!(
            "VRLRuntime(timezone={:?}, cached={})",
            self.timezone,
            self.compiled_program.is_some()
        )
    }
}

/// 创建诊断信息对象（编译错误）/ Create diagnostic object (compilation error)
fn create_diagnostic(source: &str, diagnostics: DiagnosticList) -> VRLDiagnostic {
    let messages: Vec<String> = diagnostics
        .iter()
        .map(|diag| diag.message().to_string())
        .collect();
    
    let formatted = Formatter::new(source, diagnostics.clone()).to_string();
    let colored = Formatter::new(source, diagnostics).colored().to_string();
    
    VRLDiagnostic {
        messages,
        formatted_message: formatted,
        colored_message: colored,
    }
}

/// 创建运行时诊断信息对象 / Create runtime diagnostic object
fn create_runtime_diagnostic(source: &str, terminate: Terminate) -> VRLDiagnostic {
    let error_msg = terminate.to_string();
    let error = terminate.get_expression_error();
    let formatted = Formatter::new(source, error.clone()).to_string();
    let colored = Formatter::new(source, error).colored().to_string();
    
    VRLDiagnostic {
        messages: vec![error_msg],
        formatted_message: formatted,
        colored_message: colored,
    }
}
