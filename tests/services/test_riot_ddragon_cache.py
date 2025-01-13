import pytest
from leaguetracker.services.riot_ddragon_cache import RiotDDragonCache

class TestRiotDDragonCache:
    """Test the RiotDDragonCache class"""
    
    def test_initial_cache_is_empty(self):
        """Test that the initial cache is empty"""
        cache = RiotDDragonCache()
        assert cache.get() == {}

    def test_set_and_get_cache(self):
        """Test setting and getting the cache"""
        cache = RiotDDragonCache()
        champions = {"Aatrox": "The Darkin Blade", "Ahri": "The Nine-Tailed Fox"}
        cache.set(champions)
        assert cache.get() == champions

    def test_get_a_champ(self):
        """Test getting a single champion from the cache"""
        cache = RiotDDragonCache()
        champions = {"Aatrox": "The Darkin Blade", "Ahri": "The Nine-Tailed Fox"}
        cache.set(champions)
        assert cache.get_a_champ("Aatrox") == "The Darkin Blade"
        assert cache.get_a_champ("Ahri") == "The Nine-Tailed Fox"
        assert cache.get_a_champ("NonExistentChamp") is None