# -*- coding: utf-8 -*-
# filename: test_basic.py
# @Time    : 2025/10/05 23:34
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: RustRover

"""
基础功能测试 / Basic functionality tests
"""

import pytest
from vrl_python import VRLRuntime, VRLResult


def test_simple_assignment():
    """测试简单的字段赋值 / Test simple field assignment"""
    runtime = VRLRuntime()
    
    program = '.new_field = "hello world"'
    event = {"existing_field": "value"}
    
    result = runtime.execute(program, event)
    
    assert isinstance(result, VRLResult)
    assert result.processed_event["new_field"] == "hello world"
    assert result.processed_event["existing_field"] == "value"
    assert result.elapsed_ms is not None
    assert result.elapsed_ms > 0


def test_json_parsing():
    """测试JSON解析 / Test JSON parsing"""
    runtime = VRLRuntime()
    
    program = '.parsed = parse_json!(.message)'
    event = {
        "message": '{"key": "value", "number": 42}'
    }
    
    result = runtime.execute(program, event)
    
    assert result.processed_event["parsed"]["key"] == "value"
    assert result.processed_event["parsed"]["number"] == 42


def test_field_deletion():
    """测试字段删除 / Test field deletion"""
    runtime = VRLRuntime()
    
    program = 'del(.old_field)'
    event = {
        "old_field": "to_be_deleted",
        "keep_field": "keep_this"
    }
    
    result = runtime.execute(program, event)
    
    assert "old_field" not in result.processed_event
    assert result.processed_event["keep_field"] == "keep_this"


def test_type_conversion():
    """测试类型转换 / Test type conversion"""
    runtime = VRLRuntime()
    
    program = '''
    .number = to_int!(.string_number)
    .float = to_float!(.string_float)
    '''
    event = {
        "string_number": "123",
        "string_float": "45.67"
    }
    
    result = runtime.execute(program, event)
    
    assert result.processed_event["number"] == 123
    assert abs(result.processed_event["float"] - 45.67) < 0.01


def test_static_run_method():
    """测试静态run方法 / Test static run method"""
    program = '.result = "from static method"'
    event = {}
    
    result = VRLRuntime.run(program, event, None)
    
    assert isinstance(result, VRLResult)
    assert result.processed_event["result"] == "from static method"


def test_compilation_cache():
    """测试编译缓存 / Test compilation cache"""
    runtime = VRLRuntime()
    
    program = '.field = "test"'
    event1 = {"id": 1}
    event2 = {"id": 2}
    
    # 第一次执行会编译 / First execution compiles
    result1 = runtime.execute(program, event1)
    assert result1.processed_event["field"] == "test"
    assert result1.processed_event["id"] == 1
    
    # 第二次执行使用缓存 / Second execution uses cache
    result2 = runtime.execute(program, event2)
    assert result2.processed_event["field"] == "test"
    assert result2.processed_event["id"] == 2


def test_clear_cache():
    """测试清除缓存 / Test cache clearing"""
    runtime = VRLRuntime()
    
    program = '.field = "test"'
    event = {}
    
    runtime.execute(program, event)
    runtime.clear_cache()
    
    # 缓存清除后应该能正常执行 / Should work normally after cache clear
    result = runtime.execute(program, event)
    assert result.processed_event["field"] == "test"


def test_compilation_error():
    """测试编译错误处理 / Test compilation error handling"""
    runtime = VRLRuntime()
    
    # 故意写错的VRL语法 / Intentionally wrong VRL syntax
    program = '.field = invalid syntax here'
    event = {}
    
    with pytest.raises(ValueError):
        runtime.execute(program, event)


def test_runtime_error():
    """测试运行时错误处理 / Test runtime error handling"""
    runtime = VRLRuntime()
    
    # 尝试解析无效的JSON / Try to parse invalid JSON
    program = '.parsed = parse_json!(.message)'
    event = {
        "message": "not a valid json"
    }
    
    with pytest.raises(RuntimeError):
        runtime.execute(program, event)


def test_timezone_configuration():
    """测试时区配置 / Test timezone configuration"""
    runtime_utc = VRLRuntime(timezone="UTC")
    runtime_shanghai = VRLRuntime(timezone="Asia/Shanghai")
    
    # 两个运行时应该都能正常工作 / Both runtimes should work
    program = '.field = "test"'
    event = {}
    
    result_utc = runtime_utc.execute(program, event)
    result_shanghai = runtime_shanghai.execute(program, event)
    
    assert result_utc.processed_event["field"] == "test"
    assert result_shanghai.processed_event["field"] == "test"


def test_invalid_timezone():
    """测试无效时区 / Test invalid timezone"""
    with pytest.raises(ValueError):
        VRLRuntime(timezone="Invalid/Timezone")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
