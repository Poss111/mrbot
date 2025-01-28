"""This module contains the GetChampionEmbed class."""
from typing import List
import discord
from leaguetracker.models.base_embed import MrBotEmbed
from leaguetracker.models.riot_ddragon_champion import Champion

class GetChampionEmbed(MrBotEmbed):
    """Embed for getting champion information."""
    
    def create_embed(self, champion: str, champion_data: Champion) -> discord.Embed:
        """Create the embed for the champion."""
        self.embed.title = champion
        self.embed.description = "> {0}".format(champion_data.lore)
        self.embed.set_image(url=f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_{champion_data.skins[0].num}.jpg")
        if champion_data.allytips:
            tips = ""
            for idx, tip in enumerate(champion_data.allytips):
                tips += f"**Tip {idx + 1}**\n\n> {tip}\n\n"
                
            self.embed.add_field(
                name=":trophy: Ally Tips",
                value=tips,
                inline=True
            )
        else:
            self.embed.add_field(
                name=":trophy: Ally Tips",
                value="No tips available :cry:",
                inline=True
            )
        if champion_data.enemytips:
            enemy_tips = ""
            for idx, tip in enumerate(champion_data.enemytips):
                enemy_tips += f"**Tip {idx + 1}**\n\n> {tip}\n\n"
                
            self.embed.add_field(
                name=":crossed_swords: Enemy Tips",
                value=enemy_tips,
                inline=True
            )
        else:
            self.embed.add_field(
                name=":crossed_swords: Enemy Tips",
                value="No tips available :cry:",
                inline=True
            )
        return self.embed