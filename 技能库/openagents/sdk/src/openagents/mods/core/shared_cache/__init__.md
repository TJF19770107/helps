# __init__.py

原始格式: Python

```python
"""
Shared cache mod for OpenAgents.

This mod provides a shared caching system with agent group-based access control.
"""

from .mod import SharedCacheMod
from .adapter import SharedCacheAdapter

__all__ = ["SharedCacheMod", "SharedCacheAdapter"]

```
