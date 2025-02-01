import os
from venv import logger
import discord
from discord.ext import commands
from discord import Intents
from discord.errors import Forbidden

from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VT_API_KEY = os.getenv("VT_API_KEY")

if DISCORD_TOKEN is None:
    logger.error("No Discord token found. Please create a .env file with the DISCORD_TOKEN variable.")
if VT_API_KEY is None:
    logger.error("No VirusTotal API key found. Please create a .env file with the VT_API_KEY variable.")



# Permissions for the bot
intents = Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   case_insensitive=True,
                   max_messages=100,
                   heartbeat_timeout=150.0)

# Commands for testing
@bot.command(help="Test command to check if the bot is responsive")
async def ping(ctx):
    """Test command"""
    await ctx.send("Pong! 🏓")

@bot.command(help="Clear a specified number of messages in the channel (default is 5)")
async def purge(ctx, amount=5):
    """Clear messages in a channel (default: 5)."""
    if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
        await ctx.send("❌ I don't have permission to manage messages in this channel.")
        return
    if not ctx.channel.permissions_for(ctx.guild.me).read_message_history:
        await ctx.send("❌ I don't have permission to read message history in this channel.")
        return
    
    await ctx.channel.purge(limit=amount)


@bot.command(help="Displays a list of available commands and their descriptions.")
async def help(ctx, *args):
    help_embed = discord.Embed(title="Need help?", color=0x00fff0)
    command_names_list = [x.name for x in bot.commands]

    # If there are no arguments, just list the commands:
    help_embed.add_field(
        name="List of supported commands:",
        value="\n".join([f"{i+1}. {x.name} - {x.help}" for i, x in enumerate(bot.commands)]),
        inline=False
    )
    help_embed.add_field(
        name="Details",
        value="Type !help <command name> for more details about each command.",
        inline=False
    )

    await ctx.send(embed=help_embed)

# Start the bot
if __name__ == "__main__":
    bot.load_extension("cogs.listen")
    bot.run(DISCORD_TOKEN)
