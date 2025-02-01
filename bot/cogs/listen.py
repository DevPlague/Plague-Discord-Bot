from math import log
import urllib.parse as urlparse
import re
from venv import logger
import discord
from discord.ext import commands

class Listen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        """Event when the bot connects to Discord."""
        print(f"{self.bot.user} is preparing its weapons 🛠️!")
        await self.bot.change_presence(activity=discord.Game(name="🐛🔥 Repelling bugs!"))

    @commands.Cog.listener()
    async def on_ready(self):
        """Event when the bot is ready to interact with Discord."""
        print(f"{self.bot.user} has come to repel some bugs 🐛!")
        await self.bot.change_presence(activity=discord.Game(name="🐛🔥 Repelling bugs!"))

    @commands.Cog.listener() #Comprobar que el bot solo envía el mensaje una vez a un solo canal
    async def on_guild_join(self, guild):
        """Event when the bot joins a guild."""
        print(f"{self.bot.user} has joined {guild.name}!")
        if guild.system_channel:
            try:
                await guild.system_channel.send("Here's Jhonny!")
            except discord.Forbidden:
                return
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        def url_check(message: discord.Message):
            """Look for URLs in the message. Don't check if the URL is valid."""
            words = message.content.split()
            
            for w in words:
                parsed = w.urlparse(w)
                if parsed.scheme and parsed.netloc:
                    logger.info(f"URL found: {parsed.geturl()}")
                    return True, parsed.geturl()
                break
                    
        def ip_check(message):
            """Look for IPv4 addresses in the message. Don't check if the IP is public."""
            words = message.content.split()
            regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

            for w in words:
                if re.match(regex, w):
                    logger.info(f"IP address found: {w}")
                    return True, w
                break
        
        if message.author == self.bot.user:
            return
        
        if message.content.startswith("!"):
            await self.bot.process_commands(message)
        
        elif url_check(message):
            pass # Llamar a la clase de api handler
        
        elif ip_check(message):
            pass # Llamar a la clase de api handler