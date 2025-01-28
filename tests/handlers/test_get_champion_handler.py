from unittest.mock import AsyncMock, Mock
import pytest

from leaguetracker.handlers.get_champion_handler import GetChampionHandler
from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.services.riot_ddragon_service import RiotDDragonService


class TestGetChampionHandler:
    """Test class for GetChampionHandler"""

    class TestHandle:
        """Test method for handle"""

        aatrox_sample_payload = {
                "type": "champion",
                "format": "standAloneComplex",
                "version": "14.24.1",
                "data": {
                    "Aatrox": {
                        "version": "14.24.1",
                        "id": "Aatrox",
                        "key": "266",
                        "name": "Aatrox",
                        "title": "the Darkin Blade",
                        "blurb": "Once honored defenders of Shurima against the Void, Aatrox and his brethren would eventually become an even greater threat to Runeterra, and were defeated only by cunning mortal sorcery. But after centuries of imprisonment, Aatrox was the first to find...",
                        "info": {
                            "attack": 8,
                            "defense": 4,
                            "magic": 3,
                            "difficulty": 4
                        },
                        "image": {
                            "full": "Aatrox.png",
                            "sprite": "champion0.png",
                            "group": "champion",
                            "x": 0,
                            "y": 0,
                            "w": 48,
                            "h": 48
                        },
                        "tags": ["Fighter"],
                        "partype": "Blood Well",
                        "stats": {
                            "hp": 650,
                            "hpperlevel": 114,
                            "mp": 0,
                            "mpperlevel": 0,
                            "movespeed": 345,
                            "armor": 38,
                            "armorperlevel": 4.8,
                            "spellblock": 32,
                            "spellblockperlevel": 2.05,
                            "attackrange": 175,
                            "hpregen": 3,
                            "hpregenperlevel": 0.5,
                            "mpregen": 0,
                            "mpregenperlevel": 0,
                            "crit": 0,
                            "critperlevel": 0,
                            "attackdamage": 60,
                            "attackdamageperlevel": 5,
                            "attackspeedperlevel": 2.5,
                            "attackspeed": 0.651
                        }
                    }
                }
            }

        @pytest.mark.asyncio
        async def test_handle(self):
            """Test method for verifying champion is retrieved successfully"""
            riot_ddragon_service: RiotDDragonService = AsyncMock()  # or provide a suitable mock or instance
            handler = GetChampionHandler(riot_ddragon_service)
            cham_name = "Aatrox"  
            model = RiotDDragonChampion.model_construct(**self.aatrox_sample_payload)
            riot_ddragon_service.retrieve_champion = AsyncMock(return_value=model)
            print(model)
            result = await handler.handle(cham_name)
            assert result is not None
            assert result == model