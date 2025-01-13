"""Environment variables for the bot"""
from enum import Enum

class EnvVariables(Enum):
    """Enum class to store environment variables"""
    
    DISCORD_TOKEN = "DISCORD_TOKEN",
    DISCORD_GUILD_ID = "DISCORD_GUILD_ID",
    FOOTER_MSG = "FOOTER_MSG",
    AUTHOR = "AUTHOR"