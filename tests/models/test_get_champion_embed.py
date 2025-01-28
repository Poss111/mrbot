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
        assert embed.description == f"> {champion_data.data.get(champion_name).lore}"
        # Verify that the ally tips are in the embed
        assert embed.fields[0].name == ":trophy: Ally Tips"
        assert embed.fields[0].inline
        assert embed.fields[0].value == (
            f"**Tip 1**\n\n"
            f"> {champion_data.data.get(champion_name).allytips[0]}\n\n"
            f"**Tip 2**\n\n"
            f"> {champion_data.data.get(champion_name).allytips[1]}\n\n"
            f"**Tip 3**\n\n"
            f"> {champion_data.data.get(champion_name).allytips[2]}\n\n"
        )
        # Verify that the enemy tips are in the embed
        assert embed.fields[1].name == ":crossed_swords: Enemy Tips"
        assert embed.fields[1].inline
        assert embed.fields[1].value == (
            f"**Tip 1**\n\n"
            f"> {champion_data.data.get(champion_name).enemytips[0]}\n\n"
            f"**Tip 2**\n\n"
            f"> {champion_data.data.get(champion_name).enemytips[1]}\n\n"
            f"**Tip 3**\n\n"
            f"> {champion_data.data.get(champion_name).enemytips[2]}\n\n"
        )

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
        assert embed.description == "> {0}".format(champion_indepth_data.lore)
        # Verify that the ally tips are not in the embed
        assert embed.fields[0].name == ":trophy: Ally Tips"
        assert embed.fields[0].value == "No tips available :cry:"
        assert embed.fields[1].inline is True
        # Verify that the enemy tips are not in the embed
        assert embed.fields[1].name == ":crossed_swords: Enemy Tips"
        assert embed.fields[1].value == "No tips available :cry:"
        assert embed.fields[1].inline is True
    
    def test_create_embed_with_no_ally_tips_and_enemy_tips(self):
        """Test creating an embed with empty ally and enemy tips"""
        champion_name = "Aatrox"
        champion_data = indepth_aatrox_sample_payload
        champion_indepth_data = champion_data.data.get(champion_name).model_copy()
        champion_indepth_data.allytips = []
        embed_creator = GetChampionEmbed("Footer", "Author")
        embed = embed_creator.create_embed(champion_name, champion_indepth_data)
        
        assert embed.title == champion_name
        assert embed.description == "> {0}".format(champion_indepth_data.lore)
        # Verify that the ally tips are not in the embed
        assert embed.fields[0].name == ":trophy: Ally Tips"
        assert embed.fields[0].value == "No tips available :cry:"
        assert embed.fields[1].inline is True
        # Verify that the enemy tips are in the embed
        assert embed.fields[1].name == ":crossed_swords: Enemy Tips"
        assert embed.fields[1].inline
        assert embed.fields[1].value == (
            f"**Tip 1**\n\n"
            f"> {champion_data.data.get(champion_name).enemytips[0]}\n\n"
            f"**Tip 2**\n\n"
            f"> {champion_data.data.get(champion_name).enemytips[1]}\n\n"
            f"**Tip 3**\n\n"
            f"> {champion_data.data.get(champion_name).enemytips[2]}\n\n"
        )
        
    def test_create_embed_with_ally_tips_and_no_enemy_tips(self):
        """Test creating an embed with ally tips and no enemy tips"""
        champion_name = "Aatrox"
        champion_data = indepth_aatrox_sample_payload
        champion_indepth_data = champion_data.data.get(champion_name).model_copy()
        champion_indepth_data.enemytips = []
        embed_creator = GetChampionEmbed("Footer", "Author")
        embed = embed_creator.create_embed(champion_name, champion_indepth_data)
        
        assert embed.title == champion_name
        assert embed.description == "> {0}".format(champion_indepth_data.lore)
        # Verify that the ally tips are in the embed
        assert embed.fields[0].name == ":trophy: Ally Tips"
        assert embed.fields[0].inline
        assert embed.fields[0].value == (
            f"**Tip 1**\n\n"
            f"> {champion_data.data.get(champion_name).allytips[0]}\n\n"
            f"**Tip 2**\n\n"
            f"> {champion_data.data.get(champion_name).allytips[1]}\n\n"
            f"**Tip 3**\n\n"
            f"> {champion_data.data.get(champion_name).allytips[2]}\n\n"
        )
        # Verify that the enemy tips are not in the embed
        assert embed.fields[1].name == ":crossed_swords: Enemy Tips"
        assert embed.fields[1].value == "No tips available :cry:"
        assert embed.fields[1].inline is True
        