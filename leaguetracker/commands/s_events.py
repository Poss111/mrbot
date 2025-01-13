import discord
from discord import app_commands
from discord.ext import commands
import structlog

class Events(commands.Cog):
    """Events commands"""
    
    def __init__(self, bot):
        # self.process = psutil.Process(os.getpid())
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        """Event listener for when the bot is ready"""
        log = structlog.get_logger().bind()
        log.info("Bot is ready!")
        
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """Event listener for when an interaction occurs"""
        log = structlog.get_logger().bind()
        log.info("Interaction received")
        
    @commands.Cog.listener()
    async def on_error(self, ctx: commands.Context, error: commands.CommandError):
        """Event listener for when a command error occurs"""
        log = structlog.get_logger().bind()
        
        # Log the error
        log.error(f"Unhandled command error: {error}")

        # Send an error message to the user
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            print(f"Invoke error details: {error.original}")
        else:
            await ctx.send("Something went wrong. Please contact support.")
        
    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Event listener for when an error occurs with an app command"""
        log = structlog.get_logger().bind()
        
        # Log the error
        log.error(f"Unhandled slash command error: {error}")

        # Send an error message to the user
        if interaction.response.is_done():
            # If the response is already sent, use follow-up
            await interaction.followup.send(
                "Something went wrong. Please contact support.",
                ephemeral=True
            )
        else:
            # Otherwise, send the initial response
            await interaction.response.send_message(
                "Something went wrong. Please contact support.",
                ephemeral=True
            )

        # Optionally handle specific types of errors
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You don't have permission to use this command.", ephemeral=True
            )
        elif isinstance(error, app_commands.CommandInvokeError):
            print(f"Invoke error details: {error.original}")
            
async def setup(bot):
    await bot.add_cog(Events(bot))