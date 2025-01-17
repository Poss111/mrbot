import os
import sys
from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions
from leaguetracker.services.riot_ddragon_cache import RiotDDragonCache

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.examples.data import champions_sample_payload

class TestRiotDDragonCache:
    """Test the RiotDDragonCache class"""
    
    def test_initial_cache_is_empty(self):
        """Test that the initial cache is empty"""
        cache = RiotDDragonCache()
        assert cache.get() == RiotDDragonChampions(type="", format="", version="", data={})

    def test_set_and_get_cache(self):
        """Test setting and getting the cache"""
        cache = RiotDDragonCache()
        champions = RiotDDragonChampions(type="", format="", version="", data=champions_sample_payload['data'])
        cache.set(champions)
        assert cache.get() == champions

    def test_get_a_champ(self):
        """Test getting a single champion from the cache"""
        cache = RiotDDragonCache()
        champions = RiotDDragonChampions(type="", format="", version="", data=champions_sample_payload['data'])
        cache.set(champions)
        assert cache.get_a_champ("Aatrox").name == champions_sample_payload['data']['Aatrox']['name']
        assert cache.get_a_champ("NonExistentChamp") is None