"""Environment variables for the bot"""
from enum import Enum

class EnvVariables(Enum):
    """Enum class to store environment variables"""
    
    DISCORD_TOKEN = "DISCORD_TOKEN",
    DISCORD_GUILD_ID = "DISCORD_GUILD_ID",
    FOOTER_MSG = "FOOTER_MSG",
    AUTHOR = "AUTHOR",
    APP_VERSION = "APP_VERSION",
    LOG_LEVEL = "LOG_LEVEL",
    LOGGING_FORMAT="LOGGING_FORMAT"