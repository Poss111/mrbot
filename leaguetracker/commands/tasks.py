"""Background tasks for Mr. Bot"""
from discord.ext import (
    commands,
    tasks
)

from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions
from leaguetracker.services.riot_ddragon_cache import RiotDDragonCache
from leaguetracker.services.riot_ddragon_service import RiotDDragonService

class MrBotTasks(commands.Cog):
    """Background tasks for Mr. Bot"""
    
    def __init__(self, bot):
        """Initialize the cog"""
        self.bot = bot
        self.log = self.bot.log.bind(cog=self.__class__.__name__, type="task")
        
    async def cog_load(self):
        """Event listener for when the cog is loaded"""
        self.log.info("Starting background tasks...")
        await self.sync_champion_cache()
        
    @tasks.loop(minutes=5)
    async def sync_champ_list(self):
        """Background task to sync the champion list"""
        self.log.info("Syncing champion list...")
        await self.sync_champion_cache()
        
    async def sync_champion_cache(self):
        """Sync the champion cache"""
        riot_ddragon_service : RiotDDragonService = self.bot.injector.get(RiotDDragonService)
        riot_ddragon_cache : RiotDDragonCache = self.bot.injector.get(RiotDDragonCache)
        
        # Load the champion list
        self.log.info("Loading champion list...")
        champion_list : RiotDDragonChampions = await riot_ddragon_service.retrieve_champion_list()
        self.log.info("Retrieved %d champions", len(champion_list.data.keys()))
        
        # Cache the champion list
        self.log.info("Caching champion list...")
        riot_ddragon_cache.set(champion_list)
        self.log.info("Cached %d champions", len(champion_list.data.keys()))
        
async def setup(bot):
    """Setup the cog"""
    await bot.add_cog(MrBotTasks(bot))