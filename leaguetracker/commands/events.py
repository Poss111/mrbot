from discord.ext import commands
import structlog

class Events(commands.Cog):
    """Events commands"""
        
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
            
async def setup(bot):
    await bot.add_cog(Events(bot))