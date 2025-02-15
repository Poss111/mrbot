"""Module for base discord command"""
import os
from typing import List
import discord
from discord.ext import commands
from discord import app_commands
from leaguetracker.configs.environment_variables import EnvVariables
from leaguetracker.configs.mr_bot_client import MrBotClient
from leaguetracker.models.context import Context
from leaguetracker.models.enums.theme_types import ThemeType
from leaguetracker.services.ollama_service import OllamaService

class Adventure(commands.Cog):
    """Adventure commands"""
    
    def __init__(self, bot: MrBotClient):
        """Initialize the Health cog"""
        self.bot = bot

    @app_commands.command(
        name="start_adventure",
        description="Start an adventure!"
    )
    @app_commands.guilds(int(os.getenv(EnvVariables.DISCORD_GUILD_ID.name)))
    @app_commands.describe(name="The name of your character")
    @app_commands.describe(theme="The theme of the adventure")
    async def adventure(self, interaction: discord.Interaction, name: str, theme: ThemeType):
        """Start an adventure!"""
        await interaction.response.defer()
        
        ollama_service: OllamaService = self.bot.injector.get(OllamaService)
        
        running_context: List[Context] = []
        
        adventure_options = "Generate a list of 3 options to proceed with from here."
        adventure_prompt = f"Generate an an adventure based on {theme.value} and the player's character name is {name} and leave out the options and it needs to be less than 2000 characters."
        adventure_name_prompt = "What is the name for this adventure in 5 words or less that are separated by newline characters?"
        
        self.bot.log.info(f"Creating an adventure based on {theme.value} for {name}")
        self.bot.log.info(f"Prompt: {adventure_prompt}")
        
        # Add the initial context
        running_context.append(Context(role="user", content=adventure_prompt))
        
        adventure = ollama_service.generate_chat_response(running_context, None, True)
        
        self.bot.log.info(f"Adventure: {adventure}")
        
        running_context.append(Context(role="system", content=adventure))
        running_context.append(Context(role="user", content=adventure_name_prompt))
        
        adventure_name = ollama_service.generate_chat_response(running_context, None, True)
        
        running_context.append(Context(role="system", content=adventure_name))
        running_context.append(Context(role="user", content=adventure_options))
        
        adventure_options = ollama_service.generate_chat_response(running_context, None, True)
        
        self.bot.log.info(f"Adventure name: {adventure_name}, creating thread...")
        self.bot.log.info(f"Adventure options: {adventure_options}")
        
        # trim the adventure name to 100 characters
        if len(adventure_name) > 100:
            adventure_name = adventure_name[:100]
        thread = await interaction.channel.create_thread(name=f"{adventure_name}", type=discord.ChannelType.public_thread)
        
        self.bot.log.info(f"Adding tags to thread {thread.name}")
        await thread.send(f"Theme: {theme.value}")
        await thread.send(f"Character: {name}")
        
        # Trim the adventure to 2000 characters
        if len(adventure) > 2000:
            adventure = adventure[:2000]
        self.bot.log.info(f"Sending adventure intro to thread {thread.name}")
        await thread.send(adventure)
        await thread.send(adventure_options)
        
        await interaction.followup.send(f"Adventure started! Check the thread '{thread.name}' for the adventure!")

async def setup(bot: MrBotClient):
    await bot.add_cog(Adventure(bot))