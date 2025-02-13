
import discord

from leaguetracker.models.base_embed_configuration import BaseEmbedConfiguration


class MrBotEmbed:
    """Base class for all embeds in the bot."""
        
    def __init__(self, base_embed_configuration: BaseEmbedConfiguration):
        super().__init__()
        embed = discord.Embed()
        embed.set_author(name=base_embed_configuration.author)
        embed.set_footer(text=base_embed_configuration.footer)
        self.embed = embed