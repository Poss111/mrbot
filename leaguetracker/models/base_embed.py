
import discord


class MrBotEmbed:
    """Base class for all embeds in the bot."""
    
    def __init__(self, footer_msg : str, author : str):
        super().__init__()
        embed = discord.Embed()
        embed.set_author(name=author)
        embed.set_footer(text=footer_msg)
        self.embed = embed