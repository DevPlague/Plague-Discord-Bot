import os
import asyncio
import logging
import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from pretty_help import AppMenu, PrettyHelp, AppNav

load_dotenv()
logging.basicConfig(level=logging.INFO)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
logger = logging.getLogger("Discord-Bot")

if DISCORD_TOKEN is None:
    logger.error(" No Discord token found, bot will not start. Please create a .env file with the DISCORD_TOKEN variable.")


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


@bot.event
async def on_connect():
    logger.warning(f" {bot.user} has connected to Discord!\n")
    for guild in bot.guilds:
        logger.warning(f" Connected to {guild.name}")

@bot.event
async def on_ready():
    """Ready to interact with Discord."""
    logger.warning(f" {bot.user} has come to repel some bugs 🐛!\n")
    logger.info(f" Environment variables\nDISCORD_TOKEN: {DISCORD_TOKEN}\nVT_API_KEY: {os.getenv('VT_API_KEY')}\n")
    await bot.change_presence(activity=discord.Game(name="🐛🔥 Repelling bugs!"))


# Help Menu
ending_note = "To list available commands from a specific group, type {help.clean_prefix}{help.invoked_with} <group>. To show a specific command's syntax, type {help.clean_prefix}{help.invoked_with} <command>."
menu = AppMenu(timeout=120)
bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note,
                            show_index=True,
                            no_category="General",
                            thumbnail_url="https://play.pokemonshowdown.com/sprites/gen5ani/dugtrio-alola.gif",
                            index_title="Commands' Groups",
                            case_insensitive=True,
                            color=discord.Colour.from_rgb(21, 214, 18))


cogs = [
    "cogs.general_commands",
    "cogs.vt_commands",
    "cogs.rs_commands",
    "cogs.cod_commands",
    "cogs.passwd_commands",
    "cogs.qr_commands",
    "cogs.cli_commands",
    "cogs.dns_commands"
]

async def load_cogs(bot):
    for cog in cogs:
        await bot.load_extension(cog)

async def main():
    async with bot:
        bot.add_view(AppNav())
        await load_cogs(bot)
        await bot.start(str(DISCORD_TOKEN))

if __name__ == "__main__":
    asyncio.run(main())