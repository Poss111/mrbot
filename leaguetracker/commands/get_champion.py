"""Module for base discord command"""
import discord
from discord.ext import commands

from injector import inject

import structlog

from leaguetracker.handlers.get_champion_handler import GetChampionHandler
from leaguetracker.models.logger_details import LoggerDetails
from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions
from leaguetracker.services.riot_ddragon_service import RiotDDragonService

class Champions(commands.Cog):
    
    @inject
    def __init__(self, bot: commands.Bot, get_champion_handler: GetChampionHandler, riot_ddragon_service: RiotDDragonService):
        self.bot = bot
        self.get_champion_handler = get_champion_handler
        self.riot_ddragon_service = riot_ddragon_service


    async def champion_autocomplete(self, interaction: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
        champions: RiotDDragonChampions = await self.riot_ddragon_service.retrieve_champion_list()

        champion_names = champions.data.keys()

        matches = [name for name in champion_names if name.startswith(current)]

        structlog.get_logger().info(f"Filtering for {current}", matches=matches)

        return [
            discord.app_commands.OptionChoice(name=name, value=name)
            for name in matches
        ]
        
    @discord.app_commands.command(
        name="get_champion",
    description="Get champion information",
    )
    @discord.app_commands.describe(champion="Champion name to search for")
    @discord.app_commands.autocomplete(champion=champion_autocomplete)
    @discord.app_commands.guilds(460520499680641035)
    async def get_champion(self, interaction : discord.Interaction, champion: str):
        """Get champion information"""
        log = structlog.getLogger().bind()
        log.info("Retrieving champion information...")
        championData: RiotDDragonChampion = await self.get_champion_handler.handle(champion)
        
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
    get_champion_handler: GetChampionHandler = bot.injector.get(GetChampionHandler)
    await bot.add_cog(Champions(bot, get_champion_handler, riot_ddragon_service))