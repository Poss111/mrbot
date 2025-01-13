
import asyncio
import os
import random
import time
import discord
from discord.ext import commands
from injector import Injector, inject
import structlog

from leaguetracker.configs.environment_variables import EnvVariables


class MrBotClient(commands.Bot):
    """Discord client for Mr. Bot"""

    @inject
    def __init__(self, intents: discord.Intents, logger: structlog.BoundLogger, injector: Injector):
        """Initialize the client"""
        status_messages = {
            discord.ActivityType.watching: [
                "for commands",
                "the latest updates",
                "your messages",
                "the world burn",
                "the sunrise",
                "the world go by ( ͡° ͜ʖ ͡°)"
            ],
            discord.ActivityType.playing: [
                "League of Legends",
                "World of Warcraft",
                "Minesweeper",
                "Among Us",
                "Kingdom Hearts",
                "with your ❤️ ;)"
            ],
            discord.ActivityType.listening: [
                "Eminem",
                "Taylor Swift",
                "Queen",
                "The Beatles",
                "ACDC",
                "to your problems, tell Mr. Bot everything"
            ]
        }
        random_activity_type = random.choice(list(status_messages.keys()))
        random_activity_msg = random.choice(status_messages[random_activity_type])
        logger.info(f"Setting activity to {random_activity_type} {random_activity_msg}...")
        super().__init__(
            command_prefix="!mrbot",
            intents=intents,
            help_command=None,
            activity=discord.Activity(
                type=random_activity_type,
                name=random_activity_msg
            )
        )
        self.tree.on_error = MrBotClient.tree_on_error
        self.injector = injector
        self.log = logger
        

    async def on_ready(self):
        """Event listener for when the bot is ready"""
        self.log.info(f"Bot is ready! Logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        """Event listener for when a message is received"""
        if message.author == self.user:
            return

        if message.content == "ping":
            await message.channel.send("pong")
    
    async def on_interaction(self, interaction: discord.Interaction):
        """Event listener for when an interaction occurs"""
        self.log.info("Command completed successfully", id=interaction.id, guild=interaction.guild.id, user=interaction.user.id, command=interaction.command.name)

    async def setup_hook(self) -> None:
        """Setup hook for the bot"""

        # Load cogs dynamically, passing the injector
        for filename in os.listdir("leaguetracker/commands"):
            if filename.endswith('.py') and filename != "__init__.py":
                try:
                    await self.load_extension(f"leaguetracker.commands.{filename[:-3]}")
                except Exception as e:
                    self.log.error(f"Failed to load cog: {filename}", error=e)    
    
        # Sync commands
        self.log.info("Syncing commands...")
        guild = discord.Object(id=os.getenv(EnvVariables.DISCORD_GUILD_ID.name))
        synced = await self.tree.sync(guild=guild)
        self.log.info(f"Synced {len(synced)} commands to guild {guild}")

    async def _cog_watcher(self):
        self.log.info("Watching for changes...")
        last = time.time()
        while True:
            extensions: set[str] = set()
            for name, module in self.extensions.items():
                if module.__file__ and os.stat(module.__file__).st_mtime > last:
                    extensions.add(name)
            for ext in extensions:
                try:
                    await self.reload_extension(ext)
                    print(f"Reloaded {ext}")
                except commands.ExtensionError as e:
                    print(f"Failed to reload {ext}: {e}")
            last = time.time()
            await asyncio.sleep(1)
                    
    async def on_error(self, ctx: commands.Context, error: commands.CommandError):
        """Event listener for when an error occurs with an app command"""
        
        # Log the error
        self.log.error(f"Unhandled slash command error: {error}")

        # Send an error message to the user
        if ctx.interaction is not None:
            # If the response is already sent, use follow-up
            await ctx.interaction.followup.send(
                "Something went wrong. Please contact support.",
                ephemeral=True
            )
        else:
            # Otherwise, send the initial response
            await ctx.interaction.response.send_message(
                "Something went wrong. Please contact support.",
                ephemeral=True
            )

        # Optionally handle specific types of errors
        if isinstance(error, commands.MissingPermissions):
            await ctx.send.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
        elif isinstance(error, commands.CommandInvokeError):
            self.log.error(f"Invoke error details: {error.original}")
            
    @staticmethod
    async def tree_on_error(
        interaction: discord.Interaction, error: discord.app_commands.AppCommandError
    ) -> None:
        """
        The code in this event is executed every time a normal valid command catches an
        error.
        """
        log = structlog.get_logger()
        
        log.error(f"Unhandled slash command error", error=error)
        
        embed = discord.Embed(title="Error")
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, ZeroDivisionError):
            embed.description = "Division by zero attempt"
        else:
            embed.description = "Whoops! An error occurred, please try again later."
        await interaction.response.send_message(embed=embed)
        