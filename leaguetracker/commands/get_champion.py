"""Module for base discord command"""
import discord
from discord.ext import commands

from injector import inject

import structlog

from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions
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
    @discord.app_commands.autocomplete(name=champion_autocomplete)
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

    async def champion_autocomplete(self, interaction: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
        champions: RiotDDragonChampions = await self.riot_ddragon_service.retrieve_champion_list()

        champion_names = champions.data.keys()

        matches = [name for name in champion_names if name.startswith(current)]

        structlog.get_logger().info(f"Filtering for {current}", matches=matches)

        return [
            discord.app_commands.OptionChoice(name=name, value=name)
            for name in matches
        ]


async def setup(bot):
    riot_ddragon_service: RiotDDragonService = bot.injector.get(RiotDDragonService)
    await bot.add_cog(Champions(bot, riot_ddragon_service))