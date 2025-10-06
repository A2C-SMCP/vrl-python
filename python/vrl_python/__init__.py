# -*- coding: utf-8 -*-
# filename: __init__.py
# @Time    : 2025/10/05 23:34
# @Author  : JQQ
# @Email   : jqq1716@gmail.com
# @Software: RustRover

"""
VRL Python SDK

基于PyO3封装的Vector Remap Language (VRL) Python SDK
Python SDK for Vector Remap Language (VRL) based on PyO3
"""

# 版本号 / Version - 由 bump-my-version 自动管理
__version__ = "0.1.0"

from ._vrl_python import (
    VRLCompileError,
    VRLDiagnostic,
    VRLResult,
    VRLRuntime,
    VRLRuntimeError,
)

__all__ = [
    "VRLRuntime",
    "VRLResult",
    "VRLDiagnostic",
    "VRLCompileError",
    "VRLRuntimeError",
    "__version__",
]
