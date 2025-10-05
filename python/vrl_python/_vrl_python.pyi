"""
Type stubs for _vrl_python module.

This file provides type hints for the Rust-based _vrl_python module,
enabling better IDE support and static type checking.

本文件为基于 Rust 的 _vrl_python 模块提供类型提示，
以支持更好的 IDE 支持和静态类型检查。
"""

from typing import Optional, Dict, Any, List

# Version information / 版本信息
__version__: str

class VRLResult:
    """
    VRL execution result / VRL 执行结果
    
    Contains the processed event, runtime result, and execution time.
    包含处理后的事件、运行时结果和执行时间。
    """
    
    @property
    def processed_event(self) -> Dict[str, Any]:
        """
        Processed event data / 处理后的事件数据
        
        Returns:
            Dict[str, Any]: The event data after VRL processing
        """
        ...
    
    @property
    def runtime_result(self) -> Any:
        """
        Runtime result (value of last expression) / 运行时结果（最后一个表达式的值）
        
        Returns:
            Any: The result of the last expression in the VRL program
        """
        ...
    
    @property
    def elapsed_ms(self) -> Optional[float]:
        """
        Execution time in milliseconds / 执行时间（毫秒）
        
        Returns:
            Optional[float]: Execution time, or None if not measured
        """
        ...
    
    def __repr__(self) -> str:
        """String representation of the result / 结果的字符串表示"""
        ...

class VRLDiagnostic:
    """
    VRL diagnostic information (errors/warnings) / VRL 诊断信息（错误/警告）
    
    Contains error messages and formatted diagnostic output.
    包含错误消息和格式化的诊断输出。
    """
    
    @property
    def messages(self) -> List[str]:
        """
        Error message list / 错误消息列表
        
        Returns:
            List[str]: List of error messages
        """
        ...
    
    @property
    def formatted_message(self) -> str:
        """
        Formatted error message with location and suggestions / 
        格式化的错误信息（包含位置和建议）
        
        Returns:
            str: Detailed formatted diagnostic message
        """
        ...
    
    @property
    def colored_message(self) -> str:
        """
        Colored formatted message for terminal display / 
        带颜色的格式化信息（用于终端显示）
        
        Returns:
            str: Colored diagnostic message
        """
        ...
    
    def __repr__(self) -> str:
        """String representation of the diagnostic / 诊断信息的字符串表示"""
        ...
    
    def __str__(self) -> str:
        """String representation (same as formatted_message) / 字符串表示（等同于 formatted_message）"""
        ...

class VRLRuntime:
    """
    VRL Runtime / VRL 运行时
    
    Main class for compiling and executing VRL programs.
    用于编译和执行 VRL 程序的主类。
    
    Example:
        >>> runtime = VRLRuntime()
        >>> result = runtime.execute('.field = "value"', {})
        >>> print(result.processed_event)
        {'field': 'value'}
    """
    
    def __init__(self, timezone: Optional[str] = None) -> None:
        """
        Initialize VRL runtime / 初始化 VRL 运行时
        
        Args:
            timezone: Optional timezone string (e.g., "UTC", "America/New_York").
                     If None, uses UTC. / 可选的时区字符串（如 "UTC"、"America/New_York"）。
                     如果为 None，则使用 UTC。
        
        Raises:
            ValueError: If the timezone is invalid / 如果时区无效
        
        Example:
            >>> runtime = VRLRuntime()  # Uses UTC
            >>> runtime = VRLRuntime(timezone="Asia/Shanghai")
        """
        ...
    
    def compile(self, source: str) -> bool:
        """
        Compile VRL program / 编译 VRL 程序
        
        Compiles the VRL program and caches it for later execution.
        编译 VRL 程序并缓存以供后续执行。
        
        Args:
            source: VRL program source code / VRL 程序源码
        
        Returns:
            bool: True if compilation succeeds / 编译成功返回 True
        
        Raises:
            ValueError: If compilation fails / 如果编译失败
        
        Example:
            >>> runtime = VRLRuntime()
            >>> runtime.compile('.field = "value"')
            True
        """
        ...
    
    def execute(self, source: str, event: Dict[str, Any]) -> VRLResult:
        """
        Execute VRL program / 执行 VRL 程序
        
        Compiles (if needed) and executes the VRL program on the given event.
        编译（如需要）并在给定事件上执行 VRL 程序。
        
        Args:
            source: VRL program source code / VRL 程序源码
            event: Input event data (Python dict) / 输入事件数据（Python 字典）
        
        Returns:
            VRLResult: Object containing processing results / 包含处理结果的对象
        
        Raises:
            ValueError: If compilation fails / 如果编译失败
            RuntimeError: If execution fails / 如果执行失败
        
        Example:
            >>> runtime = VRLRuntime()
            >>> result = runtime.execute('.field = "value"', {})
            >>> print(result.processed_event)
            {'field': 'value'}
        """
        ...
    
    @staticmethod
    def run(source: str, event: Dict[str, Any], timezone: Optional[str] = None) -> VRLResult:
        """
        Quick execute (compile and execute in one call) / 
        快速执行（一次性编译并执行）
        
        This is a convenience method for one-time execution scenarios.
        这是一个便捷方法，适合一次性执行的场景。
        
        Args:
            source: VRL program source code / VRL 程序源码
            event: Input event data (Python dict) / 输入事件数据（Python 字典）
            timezone: Optional timezone string / 可选的时区字符串
        
        Returns:
            VRLResult: Object containing processing results / 包含处理结果的对象
        
        Raises:
            ValueError: If compilation or timezone is invalid / 如果编译失败或时区无效
            RuntimeError: If execution fails / 如果执行失败
        
        Example:
            >>> result = VRLRuntime.run('.field = "value"', {})
            >>> print(result.processed_event)
            {'field': 'value'}
        """
        ...
    
    def clear_cache(self) -> None:
        """
        Clear compilation cache / 清除编译缓存
        
        Clears the cached compiled program, forcing recompilation on next execution.
        清除缓存的编译程序，强制下次执行时重新编译。
        
        Example:
            >>> runtime = VRLRuntime()
            >>> runtime.compile('.field = "value"')
            >>> runtime.clear_cache()
        """
        ...
    
    @staticmethod
    def check_syntax(source: str) -> Optional[VRLDiagnostic]:
        """
        Check VRL program syntax / 检查 VRL 程序语法
        
        This method only checks syntax without execution, returns detailed diagnostics.
        这个方法只检查语法，不执行程序，返回详细的诊断信息。
        
        Args:
            source: VRL program source code / VRL 程序源码
        
        Returns:
            Optional[VRLDiagnostic]: Diagnostic object if errors found, None otherwise /
                                    如果有错误返回诊断信息，否则返回 None
        
        Example:
            >>> diagnostic = VRLRuntime.check_syntax('.field = "value"')
            >>> if diagnostic is None:
            ...     print("✅ Syntax is correct")
            ... else:
            ...     print(f"❌ Errors: {diagnostic.messages}")
        """
        ...
    
    def __repr__(self) -> str:
        """String representation of the runtime / 运行时的字符串表示"""
        ...

class VRLCompileError(Exception):
    """
    VRL compilation error / VRL 编译错误
    
    Raised when VRL program compilation fails.
    当 VRL 程序编译失败时抛出。
    """
    ...

class VRLRuntimeError(Exception):
    """
    VRL runtime error / VRL 运行时错误
    
    Raised when VRL program execution fails.
    当 VRL 程序执行失败时抛出。
    """
    ...
