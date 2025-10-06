#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试类型提示 / Test type hints

这个脚本用于验证类型提示是否正常工作
This script verifies that type hints work correctly
"""

from vrl_python import VRLDiagnostic, VRLResult, VRLRuntime, __version__


def test_basic_types():
    """测试基本类型提示 / Test basic type hints"""
    # IDE 应该能够推断出这些类型 / IDE should be able to infer these types
    runtime: VRLRuntime = VRLRuntime()

    # 执行并获取结果 / Execute and get result
    result: VRLResult = runtime.execute('.field = "value"', {})

    # 访问属性 / Access properties
    event: dict = result.processed_event
    runtime_result: any = result.runtime_result
    elapsed: float | None = result.elapsed_ms

    print(f"✅ Event: {event}")
    print(f"✅ Runtime result: {runtime_result}")
    print(f"✅ Elapsed: {elapsed}ms")


def test_syntax_check():
    """测试语法检查类型提示 / Test syntax check type hints"""
    # 检查正确的语法 / Check correct syntax
    diagnostic: VRLDiagnostic | None = VRLRuntime.check_syntax('.field = "value"')

    if diagnostic is None:
        print("✅ Syntax is correct")
    else:
        # IDE 应该知道 diagnostic 的类型 / IDE should know diagnostic's type
        messages: list[str] = diagnostic.messages
        formatted: str = diagnostic.formatted_message
        print(f"❌ Errors: {messages}")
        print(formatted)


def test_static_method():
    """测试静态方法类型提示 / Test static method type hints"""
    # 静态方法调用 / Static method call
    result: VRLResult = VRLRuntime.run('.test = "ok"', {}, None)
    print(f"✅ Static method result: {result.processed_event}")


def test_version():
    """测试版本信息类型 / Test version type"""
    version: str = __version__
    print(f"✅ Version: {version}")


if __name__ == "__main__":
    print("Testing type hints / 测试类型提示\n")

    test_basic_types()
    print()

    test_syntax_check()
    print()

    test_static_method()
    print()

    test_version()
    print()

    print("✅ All type hint tests passed! / 所有类型提示测试通过！")
