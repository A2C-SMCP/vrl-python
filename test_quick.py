# -*- coding: utf-8 -*-
# filename: test_quick.py
# @Time    : 2025/10/06 00:42
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: RustRover

"""
快速测试脚本 / Quick test script
"""

try:
    from vrl_python import VRLRuntime
    
    print("✓ VRL Python SDK 导入成功！/ VRL Python SDK imported successfully!")
    
    # 测试基本功能 / Test basic functionality
    runtime = VRLRuntime()
    print("✓ VRLRuntime 实例创建成功！/ VRLRuntime instance created successfully!")
    
    program = '.test_field = "hello from VRL"'
    event = {"original": "data"}
    
    result = runtime.execute(program, event)
    print(f"✓ VRL 程序执行成功！/ VRL program executed successfully!")
    print(f"  处理后的事件 / Processed event: {result.processed_event}")
    print(f"  执行时间 / Execution time: {result.elapsed_ms:.2f}ms")
    
    print("\n🎉 所有测试通过！/ All tests passed!")
    
except ImportError as e:
    print(f"✗ 导入失败 / Import failed: {e}")
    print("  请确保已运行 'maturin develop' / Please ensure 'maturin develop' has been run")
except Exception as e:
    print(f"✗ 测试失败 / Test failed: {e}")
    import traceback
    traceback.print_exc()
