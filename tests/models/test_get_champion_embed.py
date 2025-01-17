import os
import sys
from leaguetracker.models.get_champion_embed import GetChampionEmbed

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.examples.data import indepth_aatrox_sample_payload

class TestGetChampionEmbed:
    """Test the GetChampionEmbed class"""

    def test_create_embed_with_tips(self):
        """Test creating an embed with ally and enemy tips"""
        champion_name = "Aatrox"
        champion_data = indepth_aatrox_sample_payload
        embed_creator = GetChampionEmbed("Footer", "Author")
        embed = embed_creator.create_embed("Aatrox", champion_data.data.get(champion_name))
        
        assert embed.title == champion_name
        assert embed.description == champion_data.data.get(champion_name).lore
        # Verify that the ally tips are in the embed
        assert embed.fields[0].name == "Ally Tips"
        assert embed.fields[1].name == "Tip 1"
        assert embed.fields[1].value == champion_data.data.get(champion_name).allytips[0]
        assert embed.fields[2].name == "Tip 2"
        assert embed.fields[2].value == champion_data.data.get(champion_name).allytips[1]
        assert embed.fields[3].name == "Tip 3"
        assert embed.fields[3].value == champion_data.data.get(champion_name).allytips[2]
        # Verify that the enemy tips are in the embed
        assert embed.fields[4].name == "Enemy Tips"
        assert embed.fields[5].name == "Tip 1"
        assert embed.fields[5].value == champion_data.data.get(champion_name).enemytips[0]
        assert embed.fields[6].name == "Tip 2"
        assert embed.fields[6].value == champion_data.data.get(champion_name).enemytips[1]
        assert embed.fields[7].name == "Tip 3"
        assert embed.fields[7].value == champion_data.data.get(champion_name).enemytips[2]

    def test_create_embed_without_tips(self):
        """Test creating an embed without ally and enemy tips"""
        champion_name = "Aatrox"
        champion_data = indepth_aatrox_sample_payload
        champion_indepth_data = champion_data.data.get(champion_name).model_copy()
        champion_indepth_data.allytips = []
        champion_indepth_data.enemytips = []
        embed_creator = GetChampionEmbed("Footer", "Author")
        embed = embed_creator.create_embed(champion_name, champion_indepth_data)
        
        assert embed.title == champion_name
        assert embed.description == champion_indepth_data.lore
        # Verify that the ally tips are not in the embed
        assert embed.fields[0].name == "Ally Tips"
        assert embed.fields[0].value == "No tips available"
        # Verify that the enemy tips are not in the embed
        assert embed.fields[1].name == "Enemy Tips"
        assert embed.fields[1].value == "No tips available"
    
    def test_create_embed_with_no_ally_tips_and_enemy_tips(self):
        """Test creating an embed with empty ally and enemy tips"""
        champion_name = "Aatrox"
        champion_data = indepth_aatrox_sample_payload
        champion_indepth_data = champion_data.data.get(champion_name).model_copy()
        champion_indepth_data.allytips = []
        embed_creator = GetChampionEmbed("Footer", "Author")
        embed = embed_creator.create_embed(champion_name, champion_indepth_data)
        
        assert embed.title == champion_name
        assert embed.description == champion_indepth_data.lore
        # Verify that the ally tips are not in the embed
        assert embed.fields[0].name == "Ally Tips"
        assert embed.fields[0].value == "No tips available"
        # Verify that the enemy tips are in the embed
        assert embed.fields[1].name == "Enemy Tips"
        assert embed.fields[2].name == "Tip 1"
        assert embed.fields[2].value == champion_indepth_data.enemytips[0]
        assert embed.fields[3].name == "Tip 2"
        assert embed.fields[3].value == champion_indepth_data.enemytips[1]
        assert embed.fields[4].name == "Tip 3"
        assert embed.fields[4].value == champion_indepth_data.enemytips[2]
        
    def test_create_embed_with_ally_tips_and_no_enemy_tips(self):
        """Test creating an embed with ally tips and no enemy tips"""
        champion_name = "Aatrox"
        champion_data = indepth_aatrox_sample_payload
        champion_indepth_data = champion_data.data.get(champion_name).model_copy()
        champion_indepth_data.enemytips = []
        embed_creator = GetChampionEmbed("Footer", "Author")
        embed = embed_creator.create_embed(champion_name, champion_indepth_data)
        
        assert embed.title == champion_name
        assert embed.description == champion_indepth_data.lore
        # Verify that the ally tips are in the embed
        assert embed.fields[0].name == "Ally Tips"
        assert embed.fields[1].name == "Tip 1"
        assert embed.fields[1].value == champion_indepth_data.allytips[0]
        assert embed.fields[2].name == "Tip 2"
        assert embed.fields[2].value == champion_indepth_data.allytips[1]
        assert embed.fields[3].name == "Tip 3"
        assert embed.fields[3].value == champion_indepth_data.allytips[2]
        # Verify that the enemy tips are not in the embed
        assert embed.fields[4].name == "Enemy Tips"
        assert embed.fields[4].value == "No tips available"
        