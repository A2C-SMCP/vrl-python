/**
 * 文件名: types.rs
 * 作者: JQQ
 * 创建日期: 2025/10/05
 * 最后修改日期: 2025/10/05
 * 版权: 2023 JQQ. All rights reserved.
 * 依赖: pyo3, serde_json, vrl
 * 描述: VRL类型定义和Python类型转换 / VRL type definitions and Python type conversions
 */

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use serde_json::Value as JsonValue;
use vrl::value::Value as VrlValue;
use std::collections::BTreeMap;

/// VRL执行结果 / VRL execution result
#[pyclass]
#[derive(Clone)]
pub struct VRLResult {
    /// 处理后的事件数据 / Processed event data
    #[pyo3(get)]
    pub processed_event: PyObject,
    
    /// 运行时结果（最后一个表达式的值）/ Runtime result (value of last expression)
    #[pyo3(get)]
    pub runtime_result: PyObject,
    
    /// 执行时间（毫秒）/ Execution time (milliseconds)
    #[pyo3(get)]
    pub elapsed_ms: Option<f64>,
}

#[pymethods]
impl VRLResult {
    fn __repr__(&self) -> String {
        format!(
            "VRLResult(elapsed_ms={:?})",
            self.elapsed_ms
        )
    }
}

/// VRL诊断信息（错误/警告）/ VRL diagnostic information (errors/warnings)
#[pyclass]
#[derive(Clone)]
pub struct VRLDiagnostic {
    /// 错误消息列表 / Error message list
    #[pyo3(get)]
    pub messages: Vec<String>,
    
    /// 格式化的错误信息 / Formatted error message
    #[pyo3(get)]
    pub formatted_message: String,
    
    /// 带颜色的格式化信息 / Colored formatted message
    #[pyo3(get)]
    pub colored_message: String,
}

#[pymethods]
impl VRLDiagnostic {
    fn __repr__(&self) -> String {
        format!("VRLDiagnostic(messages={:?})", self.messages)
    }
    
    fn __str__(&self) -> String {
        self.formatted_message.clone()
    }
}

/// 将Python对象转换为VRL Value / Convert Python object to VRL Value
pub fn py_to_vrl_value(py: Python, obj: &PyAny) -> PyResult<VrlValue> {
    // 先转换为JSON，再转换为VRL Value / Convert to JSON first, then to VRL Value
    let json_str = if obj.is_none() {
        "null".to_string()
    } else if let Ok(b) = obj.extract::<bool>() {
        b.to_string()
    } else if let Ok(i) = obj.extract::<i64>() {
        i.to_string()
    } else if let Ok(f) = obj.extract::<f64>() {
        f.to_string()
    } else if let Ok(s) = obj.extract::<String>() {
        serde_json::to_string(&s).unwrap()
    } else if let Ok(dict) = obj.downcast::<PyDict>() {
        let mut map = serde_json::Map::new();
        for (key, value) in dict.iter() {
            let key_str = key.extract::<String>()?;
            let json_value = py_to_json_value(py, value)?;
            map.insert(key_str, json_value);
        }
        serde_json::to_string(&JsonValue::Object(map)).unwrap()
    } else if let Ok(list) = obj.downcast::<PyList>() {
        let mut vec = Vec::new();
        for item in list.iter() {
            vec.push(py_to_json_value(py, item)?);
        }
        serde_json::to_string(&JsonValue::Array(vec)).unwrap()
    } else {
        return Err(pyo3::exceptions::PyTypeError::new_err(
            "Unsupported Python type for VRL conversion"
        ));
    };
    
    let json_value: JsonValue = serde_json::from_str(&json_str)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
    
    Ok(json_to_vrl_value(json_value))
}

/// 将JSON Value转换为VRL Value / Convert JSON Value to VRL Value
fn json_to_vrl_value(json: JsonValue) -> VrlValue {
    match json {
        JsonValue::Null => VrlValue::Null,
        JsonValue::Bool(b) => VrlValue::Boolean(b),
        JsonValue::Number(n) => {
            if let Some(i) = n.as_i64() {
                VrlValue::Integer(i)
            } else if let Some(f) = n.as_f64() {
                // NotNan 需要特殊处理 / NotNan requires special handling
                match ordered_float::NotNan::new(f) {
                    Ok(nn) => VrlValue::Float(nn),
                    Err(_) => VrlValue::Null, // NaN 转换为 Null / Convert NaN to Null
                }
            } else {
                VrlValue::Null
            }
        }
        JsonValue::String(s) => VrlValue::Bytes(s.into()),
        JsonValue::Array(arr) => {
            VrlValue::Array(arr.into_iter().map(json_to_vrl_value).collect())
        }
        JsonValue::Object(obj) => {
            let mut map = BTreeMap::new();
            for (k, v) in obj {
                map.insert(k.into(), json_to_vrl_value(v));
            }
            VrlValue::Object(map)
        }
    }
}

/// 将VRL Value转换为Python对象 / Convert VRL Value to Python object
pub fn vrl_value_to_py(py: Python, value: &VrlValue) -> PyResult<PyObject> {
    match value {
        VrlValue::Null => Ok(py.None()),
        VrlValue::Boolean(b) => Ok(b.to_object(py)),
        VrlValue::Integer(i) => Ok(i.to_object(py)),
        VrlValue::Float(f) => Ok(f.into_inner().to_object(py)),
        VrlValue::Bytes(b) => {
            let s = String::from_utf8_lossy(b.as_ref());
            Ok(s.to_object(py))
        }
        VrlValue::Timestamp(ts) => {
            let s = ts.to_string();
            Ok(s.to_object(py))
        }
        VrlValue::Regex(r) => {
            let s = r.to_string();
            Ok(s.to_object(py))
        }
        VrlValue::Array(arr) => {
            let list = PyList::empty(py);
            for item in arr {
                list.append(vrl_value_to_py(py, item)?)?;
            }
            Ok(list.to_object(py))
        }
        VrlValue::Object(obj) => {
            let dict = PyDict::new(py);
            for (k, v) in obj {
                dict.set_item(k.as_ref(), vrl_value_to_py(py, v)?)?;
            }
            Ok(dict.to_object(py))
        }
    }
}

/// 辅助函数：将Python对象转换为JSON Value / Helper: Convert Python object to JSON Value
fn py_to_json_value(py: Python, obj: &PyAny) -> PyResult<JsonValue> {
    if obj.is_none() {
        Ok(JsonValue::Null)
    } else if let Ok(b) = obj.extract::<bool>() {
        Ok(JsonValue::Bool(b))
    } else if let Ok(i) = obj.extract::<i64>() {
        Ok(JsonValue::Number(i.into()))
    } else if let Ok(f) = obj.extract::<f64>() {
        Ok(JsonValue::Number(
            serde_json::Number::from_f64(f).unwrap_or(serde_json::Number::from(0))
        ))
    } else if let Ok(s) = obj.extract::<String>() {
        Ok(JsonValue::String(s))
    } else if let Ok(dict) = obj.downcast::<PyDict>() {
        let mut map = serde_json::Map::new();
        for (key, value) in dict.iter() {
            let key_str = key.extract::<String>()?;
            map.insert(key_str, py_to_json_value(py, value)?);
        }
        Ok(JsonValue::Object(map))
    } else if let Ok(list) = obj.downcast::<PyList>() {
        let mut vec = Vec::new();
        for item in list.iter() {
            vec.push(py_to_json_value(py, item)?);
        }
        Ok(JsonValue::Array(vec))
    } else {
        Err(pyo3::exceptions::PyTypeError::new_err(
            "Unsupported Python type"
        ))
    }
}
