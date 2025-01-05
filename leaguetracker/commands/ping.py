"""Module for base discord command"""
import discord
from discord.ext import commands

class Health(commands.Cog):
    """Health check commands"""

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="ping",
        description="Is bot alive? Wanna find out? :D"
    )
    async def ping(self, interaction):
        """Ping command to check bot availability"""
        await interaction.response.send_message("Pong!")

async def setup(bot):
    await bot.add_cog(Health(bot))