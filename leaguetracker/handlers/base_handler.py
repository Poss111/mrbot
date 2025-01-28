from abc import ABC, abstractmethod

class BaseHandler(ABC):
    """Base class for all handlers"""
    
    @abstractmethod
    async def handle(self, request):
        """Handle the request"""
        pass