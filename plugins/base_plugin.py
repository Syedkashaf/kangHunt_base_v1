from abc import ABC, abstractmethod
from models.schemas import PluginResponse

class BaseOSINTPlugin(ABC):
    """Abstract base class for all OSINT plugins"""
    
    @abstractmethod
    async def execute(self, target: str) -> PluginResponse:
        """Execute the plugin against the target"""
        pass
