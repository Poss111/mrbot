"""Module for base application needs"""
from injector import Module, provider, singleton
from leaguetracker.services.riot_ddragon_service import RiotDDragonService


class BotModule(Module):
    """Module for bot configuration"""
   
    @singleton
    @provider
    def provide_bot(self) -> RiotDDragonService:
        """Provide the RiotDDragonService"""
        return RiotDDragonService("https://ddragon.leagueoflegends.com")