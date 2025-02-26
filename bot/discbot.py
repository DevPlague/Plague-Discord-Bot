import asyncio
import logging
import os

import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Discord-Bot")

if DISCORD_TOKEN is None:
    logger.error("No Discord token found. Please create a .env file with the DISCORD_TOKEN variable.")


# Permissions for the bot
intents = Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   case_insensitive=True,
                   max_messages=100,
                   heartbeat_timeout=150.0) #heartbeat timeout is a variable that is used for the bot to know when to reconnect to discord

# Make sure the bot is deployed correctly
@bot.event
async def on_connect():
    """Event when the bot connects to Discord."""
    logger.warning(f"{bot.user} has connected to Discord!\n")
    for guild in bot.guilds:
        logger.warning(f"Connected to {guild.name}")

@bot.event
async def on_ready():
    """Event when the bot is ready to interact with Discord."""
    logger.warning(f"{bot.user} has come to repel some bugs 🐛!\n")
    logger.info(f"Environment variables\nDISCORD_TOKEN: {DISCORD_TOKEN}\nVT_API_KEY: {os.getenv('VT_API_KEY')}\n")
    await bot.change_presence(activity=discord.Game(name="🐛🔥 Repelling bugs!"))

# Commands
@bot.command(help="Clear a specified number of messages in the channel (default is 5)")
async def purge(ctx, amount=5):
    """Clear messages in a channel (default: 5)."""
    if not ctx.author.guild_permissions.manage_messages:
        return 

    if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
        return

    logger.info(f"Purging {amount} messages in {ctx.channel.name} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
    await ctx.channel.purge(limit=amount)

cogs = [
    "cogs.vt_commands",
    "cogs.rs_commands",
]


async def load_cogs(bot):
    for cog in cogs:
        await bot.load_extension(cog)

async def main():
        async with bot:
            await load_cogs(bot)
            await bot.start(str(DISCORD_TOKEN))

# Start the bot
if __name__ == "__main__":
    asyncio.run(main())