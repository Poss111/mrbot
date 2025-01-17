"""Module for base discord command"""
import os
import discord
from discord.ext import commands
from discord import app_commands

from structlog.contextvars import (
    clear_contextvars, 
    bind_contextvars
)

import structlog

from leaguetracker.configs.environment_variables import EnvVariables
from leaguetracker.configs.mr_bot_client import MrBotClient
from leaguetracker.handlers.get_champion_handler import GetChampionHandler
from leaguetracker.models.get_champion_embed import GetChampionEmbed
from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions
from leaguetracker.services.riot_ddragon_cache import RiotDDragonCache

class Champions(commands.Cog):
    
    def __init__(self, bot: MrBotClient):
        self.bot = bot
        self.log = self.bot.log

    async def champion_autocomplete(self, interaction: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
        """Autocomplete for champion names"""
        riot_ddragon_cache = self.bot.injector.get(RiotDDragonCache)
        champions: RiotDDragonChampions = riot_ddragon_cache.get()

        champion_names = champions.data.keys()

        matches = [name for name in champion_names if name.startswith(current)]

        structlog.get_logger().debug(f"Filtering for {current}", matches=matches, command=interaction.command.name)
        
        # Trim to 25 matches
        matches = matches[:25]

        return [
            app_commands.Choice(name=name, value=name)
            for name in matches
        ]
        
    @app_commands.command(
        name="get_champion",
        description="Get champion information",
    )
    @app_commands.describe(champion="Champion name to search for")
    @app_commands.autocomplete(champion=champion_autocomplete)
    @app_commands.guilds(int(os.getenv(EnvVariables.DISCORD_GUILD_ID.name)))
    async def get_champion(self, interaction : discord.Interaction, champion: str):
        """Get champion information"""
        clear_contextvars()
        bind_contextvars(id=interaction.id, guild=interaction.guild.id, user=interaction.user.id, command=interaction.command.name)
        self.bot.log.info("Retrieving champion information...")
        handler : GetChampionHandler = self.bot.injector.get(GetChampionHandler)
        if handler is None:
            self.bot.log.error("Missing get champion handler")
            return await interaction.response.send_message("Whoops! Something went wrong. Please try again later.")
        
        champion_data: RiotDDragonChampion = await handler.handle(champion)
        
        self.bot.log.info(f"Champion data retrieved for {champion}, creating embed...")
        
        get_champion_embed : GetChampionEmbed = self.bot.injector.get(GetChampionEmbed)
        if get_champion_embed is None:
            self.bot.log.error("Missing embed handler")
            return await interaction.response.send_message("Whoops! Something went wrong. Please try again later.")
        await interaction.response.send_message(embeds=[get_champion_embed.create_embed(champion, champion_data.data.get(champion))])

async def setup(bot):
    """Setup the cog"""
    await bot.add_cog(Champions(bot))