"""Module for base discord command"""
import discord
from discord.ext import commands

from injector import inject

import structlog

from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.services.riot_ddragon_service import RiotDDragonService

class Champions(commands.Cog):
    
    @inject
    def __init__(self, bot: commands.Bot, riot_ddragon_service: RiotDDragonService):
        self.bot = bot
        self.riot_ddragon_service = riot_ddragon_service
        
    @discord.app_commands.command(
        name="get_champion",
        description="Get champion information",
    )
    @discord.app_commands.describe(champion="Champion name to search for")
    @discord.app_commands.choices(
        champion=[
            discord.app_commands.Choice(name="Aatrox", value="Aatrox"),
            discord.app_commands.Choice(name="Annie", value="Annie")
        ]
    )
    async def get_champion(self, interaction : discord.Interaction, champion: str):
        """Get champion information"""
        log = structlog.getLogger().bind(command=interaction.command.name, id=interaction.id, user=interaction.user.id, guild=interaction.guild.id)
        log.info("Retrieving champion information...")
        championData: RiotDDragonChampion = await self.riot_ddragon_service.retrieve_champion(champion)
        
        embed = discord.Embed(
            title=champion,
            description=championData.data[champion].lore,
            color=discord.Color.blue()
        )
        embed.set_author(name="@299370234228506627")
        embed.set_footer(text="Made with discord.py")
        tips_embed = discord.Embed(
            title="Tips",
            description="\n".join(championData.data[champion].allytips),
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embeds=[embed, tips_embed])

async def setup(bot):
    riot_ddragon_service: RiotDDragonService = bot.injector.get(RiotDDragonService)
    await bot.add_cog(Champions(bot, riot_ddragon_service))