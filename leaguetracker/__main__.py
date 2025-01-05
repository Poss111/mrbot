import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands
from dotenv import load_dotenv
from injector import Injector, Module, inject, singleton
import structlog
import random

from leaguetracker.configs.logging_config import setup_logging

from leaguetracker.services.riot_ddragon_service import RiotDDragonService

load_dotenv()
setup_logging()

log = structlog.get_logger()

class BotModule(Module):
    def configure(self, binder):
        binder.bind(RiotDDragonService, to=RiotDDragonService("https://ddragon.leagueoflegends.com"), scope=singleton)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

@inject
def create_bot(riot_ddragon_service: RiotDDragonService, injector: Injector) -> commands.Bot:
    """Create the bot instance"""
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
    log.info(f"Setting activity to {random_activity_type} {random_activity_msg}...")
    bot = commands.Bot(
        command_prefix="!mrbot",
        intents=intents,
        activity=discord.Activity(
            type=random_activity_type,
            name=random_activity_msg
        )
    )
    bot.injector = injector
            
    @bot.event
    async def setup_hook() -> None:
        """Setup hook for the bot"""

        # Load cogs dynamically, passing the injector
        for filename in os.listdir("leaguetracker/commands"):
            if filename.endswith('.py') and filename != "__init__.py":
                await bot.load_extension(f"leaguetracker.commands.{filename[:-3]}")
                
        try:
            guild = discord.Object(id=460520499680641035)
            log.info("Syncing commands...", commands=list(map(lambda command: command.name, bot.tree.get_commands())), guild=guild.id)
            synced = await bot.tree.sync(
                guild=guild
            )
            log.info(f"Synced {len(synced)} command(s).")
        except Exception as e:
            log.error(f"Failed to sync commands: {e}")
            

    return bot

if __name__ == "__main__":
    injector = Injector([BotModule()])
    bot_instance = injector.call_with_injection(create_bot)
    bot_instance.run(os.getenv('DISCORD_TOKEN'))