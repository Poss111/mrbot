"""Module for base application needs"""
from injector import Module, provider, singleton
from leaguetracker.handlers.get_champion_handler import GetChampionHandler
from leaguetracker.services.riot_ddragon_service import RiotDDragonService


class BotModule(Module):
    """Module for bot configuration"""
   
    @singleton
    @provider
    def provide_bot(self) -> RiotDDragonService:
        """Provide the RiotDDragonService"""
        return RiotDDragonService("https://ddragon.leagueoflegends.com")
    
    @singleton
    @provider
    def provide_get_champion_handler(self, riotDdragonService: RiotDDragonService) -> GetChampionHandler:
        """"""
        return GetChampionHandler(riotDdragonService)