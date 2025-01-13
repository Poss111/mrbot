
import os
import discord
from discord.ext import commands
import structlog


class MrBotClient(commands.Bot):
    """Discord client for Mr. Bot"""

    def __init__(self, intents: discord.Intents, logger: structlog.BoundLogger):
        """Initialize the client"""
        super().__init__(intents=intents)
        self.log = logger

    async def on_ready(self):
        """Event listener for when the bot is ready"""
        print(f"Bot is ready! Logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        """Event listener for when a message is received"""
        if message.author == self.user:
            return

        if message.content == "ping":
            await message.channel.send("pong")
    
    async def on_interaction(self, interaction: discord.Interaction):
        """Event listener for when an interaction occurs"""
        print(f"Interaction received: {interaction}")

    async def load_cogs(self) -> None:
        """Load cogs for the bot"""

        # Load cogs dynamically
        for filename in os.listdir("leaguetracker/commands"):
            if filename.endswith('.py') and filename != "__init__.py":
                self.log.info(f"Loading cog: {filename}")
                self.load_extension(f"leaguetracker.commands.{filename[:-3]}")

    async def setup_hook(self) -> None:
        """Setup hook for the bot"""

        # Load cogs dynamically, passing the injector
        for filename in os.listdir("leaguetracker/commands"):
            if filename.endswith('.py') and filename != "__init__.py":
                try:
                    await self.load_extension(f"leaguetracker.commands.{filename[:-3]}")
                except Exception as e:
                    self.log.error(f"Failed to load cog: {filename}", error=e)
                
        
            guild = discord.Object(id=460520499680641035)
            log.info("Syncing commands...", commands=list(map(lambda command: command.name, bot.tree.get_commands())), guild=guild.id)
            synced = await bot.tree.sync(
                guild=guild
            )
            log.info(f"Synced {len(synced)} command(s).")
        except Exception as e:
            log.error(f"Failed to sync commands: {e}")