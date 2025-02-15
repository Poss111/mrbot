"""Module for base discord command"""
import os
import discord
from discord.ext import commands
from discord import app_commands
from leaguetracker.configs.environment_variables import EnvVariables
from leaguetracker.configs.mr_bot_client import MrBotClient
from leaguetracker.services.ollama_service import OllamaService

class Health(commands.Cog):
    """Health check commands"""
    
    def __init__(self, bot: MrBotClient):
        """Initialize the Health cog"""
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Is bot alive? Wanna find out? :D"
    )
    @app_commands.guilds(int(os.getenv(EnvVariables.DISCORD_GUILD_ID.name)))
    async def ping(self, interaction: discord.Interaction):
        """Ping command to check bot availability"""
        self.bot.log.info("Pong!")
        await interaction.response.defer()
        
        ollama_service: OllamaService = self.bot.injector.get(OllamaService)
        
        response = ollama_service.generate_chat_response("Say hello! Like a gentlemen robot. Limit it to at most 10 words.", None, True)
        
        await interaction.followup.send(response)

async def setup(bot: MrBotClient):
    await bot.add_cog(Health(bot))