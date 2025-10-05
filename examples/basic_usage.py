# -*- coding: utf-8 -*-
# filename: basic_usage.py
# @Time    : 2025/10/05 23:34
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: RustRover

"""
VRL Python SDK 基础使用示例 / Basic usage examples for VRL Python SDK
"""

from vrl_python import VRLRuntime


def example_1_simple_assignment():
    """示例1: 简单字段赋值 / Example 1: Simple field assignment"""
    print("\n=== 示例1: 简单字段赋值 / Example 1: Simple field assignment ===")
    
    runtime = VRLRuntime()
    
    program = """
    .new_field = "hello world"
    .number = 42
    """
    
    event = {
        "existing_field": "original value"
    }
    
    result = runtime.execute(program, event)
    
    print(f"处理后的事件 / Processed event: {result.processed_event}")
    print(f"执行时间 / Execution time: {result.elapsed_ms:.2f}ms")


def example_2_json_parsing():
    """示例2: JSON解析 / Example 2: JSON parsing"""
    print("\n=== 示例2: JSON解析 / Example 2: JSON parsing ===")
    
    runtime = VRLRuntime()
    
    program = """
    .parsed = parse_json!(.message)
    .status_code = to_int!(.parsed.status)
    """
    
    event = {
        "message": '{"status": "200", "data": {"user": "john"}}'
    }
    
    result = runtime.execute(program, event)
    
    print(f"原始消息 / Original message: {event['message']}")
    print(f"解析后的数据 / Parsed data: {result.processed_event['parsed']}")
    print(f"状态码 / Status code: {result.processed_event['status_code']}")


def example_3_field_manipulation():
    """示例3: 字段操作 / Example 3: Field manipulation"""
    print("\n=== 示例3: 字段操作 / Example 3: Field manipulation ===")
    
    runtime = VRLRuntime()
    
    program = """
    .user_name = del(.username)
    .full_name = string!(.first_name) + " " + string!(.last_name)
    del(.first_name)
    del(.last_name)
    """
    
    event = {
        "username": "jqq",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    }
    
    result = runtime.execute(program, event)
    
    print(f"原始事件 / Original event: {event}")
    print(f"处理后事件 / Processed event: {result.processed_event}")


def example_4_conditional_logic():
    """示例4: 条件逻辑 / Example 4: Conditional logic"""
    print("\n=== 示例4: 条件逻辑 / Example 4: Conditional logic ===")
    
    runtime = VRLRuntime()
    
    program = """
    if .level == "error" {
        .severity = "high"
        .alert = true
    } else if .level == "warn" {
        .severity = "medium"
        .alert = false
    } else {
        .severity = "low"
        .alert = false
    }
    """
    
    events = [
        {"level": "error", "message": "Critical error"},
        {"level": "warn", "message": "Warning message"},
        {"level": "info", "message": "Info message"}
    ]
    
    for event in events:
        result = runtime.execute(program, event)
        print(f"Level: {event['level']} -> Severity: {result.processed_event['severity']}, "
              f"Alert: {result.processed_event['alert']}")


def example_5_static_method():
    """示例5: 使用静态方法 / Example 5: Using static method"""
    print("\n=== 示例5: 使用静态方法 / Example 5: Using static method ===")
    
    program = """
    .timestamp = now()
    .processed = true
    """
    
    event = {"id": 1, "data": "test"}
    
    # 使用静态方法一次性执行 / Use static method for one-time execution
    result = VRLRuntime.run(program, event, timezone="Asia/Shanghai")
    
    print(f"处理结果 / Processed result: {result.processed_event}")


def example_6_array_operations():
    """示例6: 数组操作 / Example 6: Array operations"""
    print("\n=== 示例6: 数组操作 / Example 6: Array operations ===")
    
    runtime = VRLRuntime()
    
    program = """
.tags = push!(.tags, "processed")
.first_tag = .tags[0]
.tag_count = length!(.tags)
"""
    
    event = {
        "tags": ["important", "user-generated"]
    }
    
    result = runtime.execute(program, event)
    
    print(f"原始标签 / Original tags: {event['tags']}")
    print(f"处理后标签 / Processed tags: {result.processed_event['tags']}")
    print(f"第一个标签 / First tag: {result.processed_event['first_tag']}")
    print(f"标签数量 / Tag count: {result.processed_event['tag_count']}")


def example_7_error_handling():
    """示例7: 错误处理 / Example 7: Error handling"""
    print("\n=== 示例7: 错误处理 / Example 7: Error handling ===")
    
    runtime = VRLRuntime()
    
    # 使用可选的错误处理 / Use optional error handling
    program = """
    .parsed, .parse_error = parse_json(.message)
    if .parse_error != null {
        .status = "parse_failed"
    } else {
        .status = "parse_success"
    }
    """
    
    events = [
        {"message": '{"valid": "json"}'},
        {"message": 'invalid json'}
    ]
    
    for event in events:
        result = runtime.execute(program, event)
        print(f"Message: {event['message'][:20]}... -> Status: {result.processed_event['status']}")


def main():
    """运行所有示例 / Run all examples"""
    print("VRL Python SDK 使用示例 / VRL Python SDK Usage Examples")
    print("=" * 60)
    
    example_1_simple_assignment()
    example_2_json_parsing()
    example_3_field_manipulation()
    example_4_conditional_logic()
    example_5_static_method()
    example_6_array_operations()
    example_7_error_handling()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成！/ All examples completed!")


if __name__ == "__main__":
    main()
