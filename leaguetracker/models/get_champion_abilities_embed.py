import discord
from leaguetracker.models.base_embed import MrBotEmbed
from leaguetracker.models.riot_ddragon_champion import Champion


class GetChampionAbilitiesEmbed(MrBotEmbed):
    """Embed for getting champion information."""
    
    def create_embed(self, champion: str, champion_data: Champion) -> discord.Embed:
        """Create the embed for the champion."""
        self.embed.title = champion
        
        # Build a new field for each spell
        for spell in champion_data.spells:
            self.embed.add_field(
                name=spell.name,
                # Cooldown should be a list of strings with 's' suffixed after each item
                value=f"Cooldown: {" / ".join([f"{cooldown}s" for cooldown in spell.cooldown])}\n",
                inline=False
            )
            # If cost has 0 in all items, don't display it
            if all([cost == 0 for cost in spell.cost]):
                continue
            self.embed.add_field(
                name=spell.name,
                # Cooldown should be a list of strings with 's' suffixed after each item
                value=f"{spell.costType}: {" / ".join([f"{cooldown}s" for cooldown in spell.cost])}\n",
                inline=False
            )
            
        return self.embed
        
    