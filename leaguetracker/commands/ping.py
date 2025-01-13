"""Module for base discord command"""
import discord
from discord.ext import commands
from discord import app_commands

from leaguetracker.configs.mr_bot_client import MrBotClient

class Health(commands.Cog):
    """Health check commands"""
    
    def __init__(self, bot: MrBotClient):
        """Initialize the Health cog"""
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Is bot alive? Wanna find out? :D"
    )
    async def ping(self, interaction: discord.Interaction):
        """Ping command to check bot availability"""
        self.bot.log.info("Pong!")
        await interaction.response.send_message("Pong!")

async def setup(bot: MrBotClient):
    await bot.add_cog(Health(bot))