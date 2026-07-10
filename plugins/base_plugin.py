from abc import ABC, abstractmethod
from models.schemas import PluginResponse

class BaseOSINTPlugin(ABC):
    """Abstract base class that all OSINT plugins must inherit from."""
    
    @abstractmethod
    async def execute(self, target: str) -> PluginResponse:
        """Execute the plugin's reconnaissance against the target."""
        pass
