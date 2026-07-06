"""
memory/__init__.py
------------------

Public surface of the memory package.

Import :class:`~memory.memory_manager.MemoryManager` directly from
this package instead of reaching into the sub-module::

    from memory import MemoryManager
"""

from memory.memory_manager import MemoryManager

__all__ = ["MemoryManager"]
