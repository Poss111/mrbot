"""Main entry point for the bot. This file is responsible for setting up the bot and running it."""
import json
import logging
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from dotenv import load_dotenv
from injector import Injector, Module, provider, singleton
import structlog

from leaguetracker.configs.environment_variables import EnvVariables
from leaguetracker.configs.logging_config import setup_logging
from leaguetracker.services.riot_ddragon_cache import RiotDDragonCache
from leaguetracker.services.riot_ddragon_service import RiotDDragonService
from leaguetracker.handlers.get_champion_handler import GetChampionHandler
from leaguetracker.configs.mr_bot_client import MrBotClient
from leaguetracker.models.get_champion_embed import GetChampionEmbed

from leaguetracker.configs.app_configs import AppConfigs
from leaguetracker.configs.env_var_app_configs import EnvVarAppConfigs

load_dotenv()
setup_logging()

log = structlog.get_logger()

class BotModule(Module):
    """Module for the bot. This class is responsible for setting up the bot's dependencies."""
    
    @singleton
    @provider
    def configuration(self) -> AppConfigs:
        """Creates an AppConfigs instance."""
        return EnvVarAppConfigs()
    
    @singleton
    @provider
    def riot_ddargon_cache(self) -> RiotDDragonCache:
        """Creates a RiotDDragonCache instance."""
        return RiotDDragonCache()
    
    @singleton
    @provider
    def riot_ddragon_service(self) -> RiotDDragonService:
        """Creates a RiotDDragonService instance."""
        return RiotDDragonService("https://ddragon.leagueoflegends.com")
    
    @singleton
    @provider
    def get_champion_handler(self, riot_ddragon_service: RiotDDragonService) -> GetChampionHandler:
        """Creates a GetChampionHandler instance."""
        return GetChampionHandler(riot_ddragon_service)
    
    @singleton
    @provider
    def bot(self, injector: Injector) -> MrBotClient:
        """Creates a MrBotClient instance."""
        intents = discord.Intents.default()
        intents.message_content = True
        return MrBotClient(intents, log, injector)

    @provider
    def get_champion_embed(self, configuration: AppConfigs) -> GetChampionEmbed:
        """Creates a GetChampionEmbed instance."""
        return GetChampionEmbed(
            "{0} - {1}".format(configuration.get_footer_msg(), configuration.get_app_version()),
            configuration.get_author()
        )

if __name__ == "__main__":
    logging.basicConfig(
        format="%(message)s", stream=sys.stdout, level=logging.INFO
    )
    injector = Injector([BotModule()])
    # bot_instance = injector.call_with_injection(create_bot)
    mr_bot_instance = injector.get(MrBotClient)
    if (discord_token := os.getenv(EnvVariables.DISCORD_TOKEN.name)) is None:
        log.error("The DISCORD_TOKEN environment variable is not set. Exiting...")
        sys.exit(1)
    try:
        kv_secret = json.loads(os.getenv(EnvVariables.DISCORD_TOKEN.name))
        # Strip the token after 10 chars to avoid leaking it in logs
        log.info("Starting the bot...", token=kv_secret[EnvVariables.DISCORD_TOKEN.name][:10])
        mr_bot_instance.run(kv_secret[EnvVariables.DISCORD_TOKEN.name])
    except Exception as e:
        log.error("Whoops! Somethign went wrong when starting the bot.", error=e)
        sys.exit(1)