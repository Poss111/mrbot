"""A module for caching the champion list from the Riot DDragon API"""

from leaguetracker.models.riot_ddragon_champions import Champion, RiotDDragonChampions


class RiotDDragonCache:
    """A class to cache the champion list from the Riot DDragon API"""
    
    def __init__(self):
        """Initialize the cache"""
        self.champion_list: RiotDDragonChampions = RiotDDragonChampions(type="", format="", version="", data={})

    def get(self):
        """Get a value from the cache"""
        return self.champion_list.model_copy()
    
    def get_a_champ(self, key) -> Champion:
        """Get a value from the cache"""
        return self.champion_list.data.get(key)

    def set(self, champion_list):
        """Set the cache"""
        self.champion_list = champion_list