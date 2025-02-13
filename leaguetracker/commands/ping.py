"""Module for base discord command"""
import os
import discord
from discord.ext import commands
from discord import app_commands
from transformers import AutoModelForCausalLM, AutoTokenizer
from leaguetracker.configs.environment_variables import EnvVariables
from leaguetracker.configs.mr_bot_client import MrBotClient

class Health(commands.Cog):
    """Health check commands"""
    
    def __init__(self, bot: MrBotClient):
        """Initialize the Health cog"""
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Is bot alive? Wanna find out? :D"
    )
    @app_commands.guilds(int(os.getenv(EnvVariables.DISCORD_GUILD_ID.name)))
    async def ping(self, interaction: discord.Interaction):
        """Ping command to check bot availability"""
        self.bot.log.info("Pong!")
        await interaction.response.defer()
        MODEL_NAME = "TinyLlama/TinyLlama-1.1B-step-50K-105b"

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
        
        inputs = tokenizer("Can you create a fantasy environment for me?", return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_length=100)
        await interaction.followup.send(tokenizer.decode(outputs[0], skip_special_tokens=True))

async def setup(bot: MrBotClient):
    await bot.add_cog(Health(bot))