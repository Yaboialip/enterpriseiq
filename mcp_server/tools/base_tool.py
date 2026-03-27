from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Base interface for all MCP tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        pass