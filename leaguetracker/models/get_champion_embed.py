"""This module contains the GetChampionEmbed class."""
import discord
from leaguetracker.models.base_embed import MrBotEmbed
from leaguetracker.models.riot_ddragon_champion import Champion

class GetChampionEmbed(MrBotEmbed):
    """Embed for getting champion information."""
    
    def create_embed(self, champion: str, champion_data: Champion) -> discord.Embed:
        """Create the embed for the champion."""
        self.embed.title = champion
        self.embed.description = champion_data.lore
        self.embed.set_image(url=f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_{champion_data.skins[0].num}.jpg")
        if champion_data.allytips:
            self.embed.add_field(
                name="Ally Tips",
                value="",
                inline=False
            )
            for idx, tip in enumerate(champion_data.allytips):
                self.embed.add_field(
                    name=f"Tip {idx + 1}",
                    value=tip,
                    inline=True
                )
        else:
            self.embed.add_field(
                name="Ally Tips",
                value="No tips available",
                inline=False
            )
        if champion_data.enemytips:
            self.embed.add_field(
                name="Enemy Tips",
                value="",
                inline=False
            )
            for idx, tip in enumerate(champion_data.enemytips):
                self.embed.add_field(
                    name=f"Tip {idx + 1}",
                    value=tip,
                    inline=True
                )
        else:
            self.embed.add_field(
                name="Enemy Tips",
                value="No tips available",
                inline=False
            )
        return self.embed