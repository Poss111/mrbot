from abc import ABC, abstractmethod

from leaguetracker.models.logger_details import LoggerDetails

class BaseHandler(ABC):
    
    @abstractmethod
    async def handle(self, request, loggerDetails: LoggerDetails):
        pass