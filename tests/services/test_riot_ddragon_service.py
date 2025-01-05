"""Module for testing the get champion command"""
from unittest.mock import patch
import pytest
from leaguetracker.models.riot_ddragon_champion import RiotDDragonChampion
from leaguetracker.models.riot_ddragon_champions import RiotDDragonChampions
from leaguetracker.services.riot_ddragon_service import RiotDDragonService

class TestGetListOfChampions:
    """Test class for the get champion command"""
    
    aatrox_sample_data = {
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
    
    @pytest.fixture
    def mock_response(self):
        """Fixture to create a mocked API response."""
        mock_response = patch('requests.request')
        return mock_response

    @pytest.mark.asyncio
    async def test_get_list_of_champions_use_latest_version_if_not_provided(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        # Set up the mock to return a successful response
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        
        expected_response = TestGetListOfChampions.aatrox_sample_data
        mock_instance.return_value.json.return_value = expected_response
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        latest_version = "14.24.1"
        service._versions_cache = {
            'data': [latest_version],
            'timestamp': None
        }
        # Execute the ping command
        response = await service.retrieve_champion_list()
        
        mock_instance.assert_called_once_with(
            "GET",
            f"{base}/{latest_version}/data/en_US/champion.json", 
            params=None, 
            data=None, 
            headers=None, 
            timeout=5
        )
        
        # Assert the expected interaction response
        assert response is not None
        assert response == RiotDDragonChampions(**expected_response)
        
        mock_instance.stop()

    @pytest.mark.asyncio
    async def test_get_list_of_champions_use_latest_version_execute_with_a_valid_version_passed(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        # Set up the mock to return a successful response
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        
        expected_response = TestGetListOfChampions.aatrox_sample_data
        mock_instance.return_value.json.return_value = expected_response
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        latest_version = "14.24.1"
        version_to_run_with = "14.23.1"
        service._versions_cache = {
            'data': [latest_version, version_to_run_with, "14.22.1"],
            'timestamp': None
        }
        # Execute the ping command
        response = await service.retrieve_champion_list(version_to_run_with)
        
        mock_instance.assert_called_once_with(
            "GET",
            f"{base}/{version_to_run_with}/data/en_US/champion.json", 
            params=None, 
            data=None, 
            headers=None, 
            timeout=5
        )
        
        # Assert the expected interaction response
        assert response is not None
        assert response == RiotDDragonChampions(**expected_response)
        
        mock_instance.stop()
        
    @pytest.mark.asyncio
    async def test_get_list_of_champions_should_return_exception_if_version_passed_is_not_valid(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        # Set up the mock to return a successful response
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        
        expected_response = TestGetListOfChampions.aatrox_sample_data
        mock_instance.return_value.json.return_value = expected_response
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        latest_version = "14.24.1"
        version_to_run_with = "14.23.1"
        service._versions_cache = {
            'data': [latest_version, "14.22.1"],
            'timestamp': None
        }
        # Execute the ping command
        try:
            await service.retrieve_champion_list(version_to_run_with)
            assert False, "Should have raised an exception"
        except Exception as e:
            assert str(e) == f"Version {version_to_run_with} is not available from Riot's DDragon API"
        
        mock_instance.stop()
        
    @pytest.mark.asyncio
    async def test_get_list_of_champions_responds_w_not_200(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        # Set up the mock to return a successful response
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 404
        expected_response = TestGetListOfChampions.aatrox_sample_data
        mock_instance.return_value.json.return_value = expected_response
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        latest_version = "14.24.1"
        service._versions_cache = {
            'data': [latest_version],
            'timestamp': None
        }
        
        # Execute the ping command
        try:
            response = await service.retrieve_champion_list()
        except Exception as e:
            assert str(e) == "Error sending request to https://localhost:8080/cdn/14.24.1/data/en_US/champion.json: 404"
        
        mock_instance.assert_called_once_with(
            "GET", 
            f"{base}/{latest_version}/data/en_US/champion.json", 
            params=None, 
            data=None, 
            headers=None, 
            timeout=5
        )
        
        mock_instance.stop()

class TestGetChampion:
    """Test class for the get champion command"""
    
    aatrox_sample_data = {
        "type": "champion",
        "format": "standAloneComplex",
        "version": "14.24.1",
        "data": {
            "Aatrox": {
            "id": "Aatrox",
            "key": "266",
            "name": "Aatrox",
            "title": "the Darkin Blade",
            "image": {
                "full": "Aatrox.png",
                "sprite": "champion0.png",
                "group": "champion",
                "x": 0,
                "y": 0,
                "w": 48,
                "h": 48
            },
            "skins": [
                {
                "id": "266000",
                "num": 0,
                "name": "default",
                "chromas": False
                },
                {
                "id": "266001",
                "num": 1,
                "name": "Justicar Aatrox",
                "chromas": False
                },
                {
                "id": "266002",
                "num": 2,
                "name": "Mecha Aatrox",
                "chromas": True
                },
                {
                "id": "266003",
                "num": 3,
                "name": "Sea Hunter Aatrox",
                "chromas": False
                },
                {
                "id": "266007",
                "num": 7,
                "name": "Blood Moon Aatrox",
                "chromas": False
                },
                {
                "id": "266008",
                "num": 8,
                "name": "Prestige Blood Moon Aatrox",
                "chromas": False
                },
                {
                "id": "266009",
                "num": 9,
                "name": "Victorious Aatrox",
                "chromas": True
                },
                {
                "id": "266011",
                "num": 11,
                "name": "Odyssey Aatrox",
                "chromas": True
                },
                {
                "id": "266020",
                "num": 20,
                "name": "Prestige Blood Moon Aatrox (2022)",
                "chromas": False
                },
                {
                "id": "266021",
                "num": 21,
                "name": "Lunar Eclipse Aatrox",
                "chromas": True
                },
                {
                "id": "266030",
                "num": 30,
                "name": "DRX Aatrox",
                "chromas": True
                },
                {
                "id": "266031",
                "num": 31,
                "name": "Prestige DRX Aatrox",
                "chromas": False
                },
                {
                "id": "266033",
                "num": 33,
                "name": "Primordian Aatrox",
                "chromas": True
                }
            ],
            "lore": "Once honored defenders of Shurima against the Void, Aatrox and his brethren would eventually become an even greater threat to Runeterra, and were defeated only by cunning mortal sorcery. But after centuries of imprisonment, Aatrox was the first to find freedom once more, corrupting and transforming those foolish enough to try and wield the magical weapon that contained his essence. Now, with stolen flesh, he walks Runeterra in a brutal approximation of his previous form, seeking an apocalyptic and long overdue vengeance.",
            "blurb": "Once honored defenders of Shurima against the Void, Aatrox and his brethren would eventually become an even greater threat to Runeterra, and were defeated only by cunning mortal sorcery. But after centuries of imprisonment, Aatrox was the first to find...",
            "allytips": [
                "Use Umbral Dash while casting The Darkin Blade to increase your chances of hitting the enemy.",
                "Crowd Control abilities like Infernal Chains or your allies' immobilizing effects will help you set up The Darkin Blade.",
                "Cast World Ender when you are sure you can force a fight."
            ],
            "enemytips": [
                "Aatrox's attacks are very telegraphed, so use the time to dodge the hit zones.",
                "Aatrox's Infernal Chains are easier to exit when running towards the sides or at Aatrox.",
                "Keep your distance when Aatrox uses his Ultimate to prevent him from reviving."
            ],
            "tags": [
                "Fighter"
            ],
            "partype": "Blood Well",
            "info": {
                "attack": 8,
                "defense": 4,
                "magic": 3,
                "difficulty": 4
            },
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
            },
            "spells": [
                {
                "id": "AatroxQ",
                "name": "The Darkin Blade",
                "description": "Aatrox slams his greatsword down, dealing physical damage. He can swing three times, each with a different area of effect.",
                "tooltip": "Aatrox slams his greatsword, dealing \u003CphysicalDamage\u003E{{ qdamage }} physical damage\u003C/physicalDamage\u003E. If they are hit on the edge, they are briefly \u003Cstatus\u003EKnocked Up\u003C/status\u003E and they take \u003CphysicalDamage\u003E{{ qedgedamage }}\u003C/physicalDamage\u003E instead. This Ability can be \u003Crecast\u003ERecast\u003C/recast\u003E twice, each one changing shape and dealing 25% more damage than the previous one.{{ spellmodifierdescriptionappend }}",
                "leveltip": {
                    "label": [
                    "Cooldown",
                    "Damage",
                    "Total AD Ratio"
                    ],
                    "effect": [
                    "{{ cooldown }} -\u003E {{ cooldownNL }}",
                    "{{ qbasedamage }} -\u003E {{ qbasedamageNL }}",
                    "{{ qtotaladratio*100.000000 }}% -\u003E {{ qtotaladrationl*100.000000 }}%"
                    ]
                },
                "maxrank": 5,
                "cooldown": [14, 12, 10, 8, 6],
                "cooldownBurn": "14/12/10/8/6",
                "cost": [0, 0, 0, 0, 0],
                "costBurn": "0",
                "datavalues": {

                },
                "effect": [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                "effectBurn": ["0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                "vars": [],
                "costType": "No Cost",
                "maxammo": "-1",
                "range": [25000, 25000, 25000, 25000, 25000],
                "rangeBurn": "25000",
                "image": {
                    "full": "AatroxQ.png",
                    "sprite": "spell0.png",
                    "group": "spell",
                    "x": 384,
                    "y": 48,
                    "w": 48,
                    "h": 48
                },
                "resource": "No Cost"
                },
                {
                "id": "AatroxW",
                "name": "Infernal Chains",
                "description": "Aatrox smashes the ground, dealing damage to the first enemy hit. Champions and large monsters have to leave the impact area quickly or they will be dragged to the center and take the damage again.",
                "tooltip": "Aatrox fires a chain, \u003Cstatus\u003ESlowing\u003C/status\u003E the first enemy hit by {{ wslowpercentage*-100 }}% for {{ wslowduration }} seconds and dealing \u003CmagicDamage\u003E{{ wdamage }} magic damage\u003C/magicDamage\u003E. Champions and large jungle monsters have {{ wslowduration }} seconds to leave the impact area or be \u003Cstatus\u003EPulled\u003C/status\u003E back to the center and damaged again for the same amount.{{ spellmodifierdescriptionappend }}",
                "leveltip": {
                    "label": [
                    "Cooldown",
                    "Damage",
                    "Slow"
                    ],
                    "effect": [
                    "{{ cooldown }} -\u003E {{ cooldownNL }}",
                    "{{ wbasedamage }} -\u003E {{ wbasedamageNL }}",
                    "{{ wslowpercentage*-100.000000 }}% -\u003E {{ wslowpercentagenl*-100.000000 }}%"
                    ]
                },
                "maxrank": 5,
                "cooldown": [20, 18, 16, 14, 12],
                "cooldownBurn": "20/18/16/14/12",
                "cost": [0, 0, 0, 0, 0],
                "costBurn": "0",
                "datavalues": {

                },
                "effect": [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                "effectBurn": ["0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                "vars": [],
                "costType": "No Cost",
                "maxammo": "-1",
                "range": [825, 825, 825, 825, 825],
                "rangeBurn": "825",
                "image": {
                    "full": "AatroxW.png",
                    "sprite": "spell0.png",
                    "group": "spell",
                    "x": 432,
                    "y": 48,
                    "w": 48,
                    "h": 48
                },
                "resource": "No Cost"
                },
                {
                "id": "AatroxE",
                "name": "Umbral Dash",
                "description": "Passively, Aatrox heals when damaging enemy champions. On activation, he dashes in a direction.",
                "tooltip": "\u003CspellPassive\u003EPassive:\u003C/spellPassive\u003E Aatrox heals for \u003ClifeSteal\u003E{{ totalevamp }}\u003C/lifeSteal\u003E of the damage he deals to Champions.\u003Cbr /\u003E\u003Cbr /\u003E\u003CspellActive\u003EActive:\u003C/spellActive\u003E Aatrox dashes. He can use this Ability while winding up his other Abilities.{{ spellmodifierdescriptionappend }}",
                "leveltip": {
                    "label": [
                    "Cooldown"
                    ],
                    "effect": [
                    "{{ cooldown }} -\u003E {{ cooldownNL }}"
                    ]
                },
                "maxrank": 5,
                "cooldown": [9, 8, 7, 6, 5],
                "cooldownBurn": "9/8/7/6/5",
                "cost": [0, 0, 0, 0, 0],
                "costBurn": "0",
                "datavalues": {

                },
                "effect": [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                "effectBurn": ["0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                "vars": [],
                "costType": "No Cost",
                "maxammo": "-1",
                "range": [25000, 25000, 25000, 25000, 25000],
                "rangeBurn": "25000",
                "image": {
                    "full": "AatroxE.png",
                    "sprite": "spell0.png",
                    "group": "spell",
                    "x": 0,
                    "y": 96,
                    "w": 48,
                    "h": 48
                },
                "resource": "No Cost"
                },
                {
                "id": "AatroxR",
                "name": "World Ender",
                "description": "Aatrox unleashes his demonic form, fearing nearby enemy minions and gaining attack damage, increased healing, and Move Speed. If he gets a takedown, this effect is extended.",
                "tooltip": "Aatrox reveals his true demonic form, \u003Cstatus\u003EFearing\u003C/status\u003E nearby minions for {{ rminionfearduration }} seconds and gaining \u003Cspeed\u003E{{ rmovementspeedbonus*100 }}% Move Speed\u003C/speed\u003E decaying over {{ rduration }} seconds. He also gains \u003CscaleAD\u003E{{ rtotaladamp*100 }}% Attack Damage\u003C/scaleAD\u003E and increases \u003Chealing\u003Eself-healing by {{ rhealingamp*100 }}%\u003C/healing\u003E for the duration.\u003Cbr /\u003E\u003Cbr /\u003EChampion takedowns extend the duration of this effect by {{ rextension }} seconds and refresh the \u003Cspeed\u003EMove Speed\u003C/speed\u003E effect.{{ spellmodifierdescriptionappend }}",
                "leveltip": {
                    "label": [
                    "Total Attack Damage Increase",
                    "Healing Increase",
                    "Move Speed",
                    "Cooldown"
                    ],
                    "effect": [
                    "{{ rtotaladamp*100.000000 }}% -\u003E {{ rtotaladampnl*100.000000 }}%",
                    "{{ rhealingamp*100.000000 }}% -\u003E {{ rhealingampnl*100.000000 }}%",
                    "{{ rmovementspeedbonus*100.000000 }}% -\u003E {{ rmovementspeedbonusnl*100.000000 }}%",
                    "{{ cooldown }} -\u003E {{ cooldownNL }}"
                    ]
                },
                "maxrank": 3,
                "cooldown": [120, 100, 80],
                "cooldownBurn": "120/100/80",
                "cost": [0, 0, 0],
                "costBurn": "0",
                "datavalues": {

                },
                "effect": [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]
                ],
                "effectBurn": [ "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0",
                    "0"
                ],
                "vars": [],
                "costType": "No Cost",
                "maxammo": "-1",
                "range": [25000, 25000, 25000],
                "rangeBurn": "25000",
                "image": {
                    "full": "AatroxR.png",
                    "sprite": "spell0.png",
                    "group": "spell",
                    "x": 48,
                    "y": 96,
                    "w": 48,
                    "h": 48
                },
                "resource": "No Cost"
                }
            ],
            "passive": {
                "name": "Deathbringer Stance",
                "description": "Periodically, Aatrox's next basic attack deals bonus \u003CphysicalDamage\u003Ephysical damage\u003C/physicalDamage\u003E and heals him, based on the target's max health. ",
                "image": {
                "full": "Aatrox_Passive.png",
                "sprite": "passive0.png",
                "group": "passive",
                "x": 0,
                "y": 0,
                "w": 48,
                "h": 48
                }
            },
            "recommended": []
            }
        }
    }
    
    @pytest.fixture
    def mock_response(self):
        """Fixture to create a mocked API response."""
        mock_response = patch('requests.request')
        return mock_response
    
    @pytest.mark.asyncio
    async def test_get_champion_use_latest_version_if_not_provided(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        # Set up the mock to return a successful response
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        
        expected_response = TestGetChampion.aatrox_sample_data
        mock_instance.return_value.json.return_value = expected_response
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        latest_version = "14.24.1"
        service._versions_cache = {
            'data': [latest_version],
            'timestamp': None
        }
        # Execute the ping command
        champion_to_search_for = "Aatrox"
        response = await service.retrieve_champion(champion_to_search_for)
        
        mock_instance.assert_called_once_with(
            "GET",
            f"{base}/{latest_version}/data/en_US/champion/{champion_to_search_for}.json", 
            params=None, 
            data=None, 
            headers=None, 
            timeout=5
        )
        
        # Assert the expected interaction response
        assert response is not None
        assert response == RiotDDragonChampion(**expected_response)
        
        mock_instance.stop()
    
    @pytest.mark.asyncio
    async def test_get_champion_should_throw_an_exception_if_version_is_not_valid(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        # Set up the mock to return a successful response
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        
        expected_response = TestGetChampion.aatrox_sample_data
        mock_instance.return_value.json.return_value = expected_response
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        latest_version = "14.24.1"
        service._versions_cache = {
            'data': [latest_version, "14.22.1"],
            'timestamp': None
        }
        # Execute the ping command
        champion_to_search_for = "Aatrox"
        try:
            await service.retrieve_champion(champion_to_search_for, "14.23.1")
            assert False, "Should have raised an exception"
        except Exception as e:
            assert str(e) == f"Version 14.23.1 is not available from Riot's DDragon API"
        
        mock_instance.stop()
        
    @pytest.mark.asyncio
    async def test_get_champion_should_use_version_passed_if_valid(self, mock_response):
        """Test retrieving list of champions from Riots DDragon API"""
        # Set up the mock to return a successful response
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        
        expected_response = TestGetChampion.aatrox_sample_data
        mock_instance.return_value.json.return_value = expected_response
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        latest_version = "14.24.1"
        version_to_run_with = "14.23.1"
        service._versions_cache = {
            'data': [latest_version, version_to_run_with, "14.22.1"],
            'timestamp': None
        }
        # Execute the ping command
        champion_to_search_for = "Aatrox"
        response = await service.retrieve_champion(champion_to_search_for, version_to_run_with)
        
        mock_instance.assert_called_once_with(
            "GET",
            f"{base}/{version_to_run_with}/data/en_US/champion/{champion_to_search_for}.json", 
            params=None, 
            data=None, 
            headers=None, 
            timeout=5
        )
        
        # Assert the expected interaction response
        assert response is not None
        assert response == RiotDDragonChampion(**expected_response)
        
        mock_instance.stop()
    
class TestGetVersion:
    
    version_sample_payload = [
        "14.24.1",
        "14.23.1",
        "14.22.1",
        "14.21.1",
        "lolpatch_4.21",
        "lolpatch_4.20",
        "lolpatch_4.19",
        "lolpatch_4.18",
        "lolpatch_4.17",
        "lolpatch_4.16",
        "lolpatch_4.15",
        "lolpatch_4.14",
        "lolpatch_4.13",
        "lolpatch_4.12",
        "lolpatch_4.11",
        "lolpatch_4.10",
    ]
    
    @pytest.fixture
    def mock_response(self):
        """Fixture to create a mocked API response."""
        mock_response = patch('requests.request')
        return mock_response
    
    @pytest.mark.asyncio
    async def test_get_available_versions(self, mock_response):
        """Test retrieving list of versions from Riots DDragon API"""
        
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        mock_instance.return_value.json.return_value = TestGetVersion.version_sample_payload
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        # Execute the ping command
        response = await service.retrieve_available_versions()
        
        mock_instance.assert_called_once_with(
            "GET", 
            f"{base}/api/versions.json",
            params=None,
            data=None,
            headers=None,
            timeout=5
        )
        
        # Assert the expected interaction response
        assert response is not None
        assert response == TestGetVersion.version_sample_payload
        assert service._versions_cache['data'] == TestGetVersion.version_sample_payload
        assert service._versions_cache['timestamp'] is not None
        assert response == TestGetVersion.version_sample_payload
        
        mock_instance.stop()
        
    @pytest.mark.asyncio
    async def test_get_available_versions_responds_w_not_200(self, mock_response):
        """Test retrieving list of versions from Riots DDragon API"""
        
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 404
        mock_instance.return_value.json.return_value = TestGetVersion.version_sample_payload
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        # Execute the ping command
        try:
            response = await service.retrieve_available_versions()
        except Exception as e:
            assert str(e) == "Error sending request to https://localhost:8080/api/cdn/versions.json: 404"
        
        mock_instance.assert_called_once_with(
            "GET", 
            f"{base}/versions.json",
            params=None,
            data=None,
            headers=None,
            timeout=5
        )
        
        mock_instance.stop()
        
    @pytest.mark.asyncio
    async def test_get_available_versions_cache_response_if_cached(self, mock_response):
        """Test retrieving list of versions from Riots DDragon API"""
        
        mock_instance = mock_response.start()
        mock_instance.return_value.status_code = 200
        mock_instance.return_value.json.return_value = TestGetVersion.version_sample_payload
        
        base = "https://localhost:8080/cdn"
        service = RiotDDragonService(base)
        # Execute the ping command
        response = await service.retrieve_available_versions()
        response = await service.retrieve_available_versions()
        
        mock_instance.assert_called_once_with(
            "GET", 
            f"{base}/api/versions.json",
            params=None,
            data=None,
            headers=None,
            timeout=5
        )
        
        # Assert the expected interaction response
        assert response is not None
        assert response == TestGetVersion.version_sample_payload
        
        mock_instance.stop()