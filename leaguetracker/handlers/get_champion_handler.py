"""This module contains the GetChampionHandler class"""
from injector import inject
import structlog
from leaguetracker.handlers.base_handler import BaseHandler
from leaguetracker.models.logger_details import LoggerDetails
from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.services.riot_ddragon_service import RiotDDragonService

class GetChampionHandler(BaseHandler):
    """Handler for getting champion information"""

    @inject 
    def __init__(self, riot_ddragon_service: RiotDDragonService):
        """Initialize the handler"""
        self.riot_ddragon_service = riot_ddragon_service

    async def handle(self, request, loggerDetails: LoggerDetails) -> RiotDDragonChampion:
        """Get champion information"""
        structlog.get_logger().info(f"Retrieving champion information for {request}...")
        champion_data = await self.riot_ddragon_service.retrieve_champion(request)
        return champion_data