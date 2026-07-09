from abc import ABC, abstractmethod
from models.schemas import PluginResponse

class BaseOSINTPlugin(ABC):
    @abstractmethod
    async def execute(self, target: str) -> PluginResponse:
        """Har plugin ko ab laazmi PluginResponse object return karna hoga."""
        pass
