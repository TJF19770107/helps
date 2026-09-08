# __init__.py

原始格式: Python

```python
"""
Shared artifact mod for OpenAgents.

This mod provides a shared artifact storage system with agent group-based access control.
Artifacts are stored as persistent files in the workspace.
"""

from .mod import SharedArtifactMod
from .adapter import SharedArtifactAdapter

__all__ = ["SharedArtifactMod", "SharedArtifactAdapter"]

```
