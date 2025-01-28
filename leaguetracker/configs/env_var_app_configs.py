import os
from leaguetracker.configs.app_configs import AppConfigs
from dotenv import load_dotenv

from leaguetracker.configs.environment_variables import EnvVariables


class EnvVarAppConfigs(AppConfigs):
    """An implementation of AppConfigs that uses environment variables."""
    
    def __init__(self):
        print("Loading configurations from environment variables.")
        load_dotenv()
    
    def get_footer_msg(self):
        return os.getenv(EnvVariables.FOOTER_MSG.name)
    
    def get_author(self):
        return os.getenv(EnvVariables.AUTHOR.name)
    
    def get_guild_id(self):
        return os.getenv(EnvVariables.DISCORD_GUILD_ID.name)
    
    def get_app_version(self):
        return os.getenv(EnvVariables.APP_VERSION.name)
            