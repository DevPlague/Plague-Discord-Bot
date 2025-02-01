# This command will show the user the available commands and their usage.

from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Show this message")
    async def help(self, ctx):
        """Show this message"""
        embed = self.bot.help_command.get_command_help(ctx)
        await ctx.send(embed=embed)