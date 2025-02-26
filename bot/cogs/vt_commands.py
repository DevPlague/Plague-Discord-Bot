import discord
from discord.ext import commands
from hashlib import sha256
from bot.utils.vt.VTApiHandler import VTApiHandler
import logging
import os

logger = logging.getLogger("VT-Commands")
VT_API_KEY = os.getenv("VT_API_KEY")

if VT_API_KEY is None:
    logger.error("No VirusTotal API key found. Please create a .env file with the VT_API_KEY variable.")

class VirusTotalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.apiHandler = VTApiHandler(logger, str(VT_API_KEY))

    @commands.command(help="Check if a URL is malicious using VirusTotal API and return a report if exists. \nUsage: !vt_url <url>")
    async def vt_url(self, ctx, url: str):
        """Check if a URL is malicious using VirusTotal API and return a report if exists."""
        logger.info(f"Report asked for URL: {url} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        result = await self.apiHandler.url_scan(url)

        if isinstance(result, dict):
            logger.info(f"Report acquired for URL: {url} \nUser: {ctx.author.name}\n")
            if result["malicious"] > 0 or result["suspicious"] > 2:
                color = discord.Colour.red()
                title = f"ALERT: <{url}> wants to ruin your day! 💢"
                image = "https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185508/Repelente_m%C3%A1ximo_EP.png"
            else:
                color = discord.Colour.green()
                title = f"<{url}> is safe! But stay sharp! 👀"
                image = "https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416"

            embed = discord.Embed(
                title=title,
                description=(
                    f":💀  **Malicious**: {result['malicious']}\n\n"
                    f"🚨 **Suspicious**: {result['suspicious']}\n\n"
                    f"✔️ **Harmless**: {result['harmless']}\n\n"
                    f"👻 **Undetected**: {result['undetected']}\n\n"
                    f"Click on the title to see more details on VirusTotal."
                ),
                colour=color
            )
            embed.set_footer(text="Powered by VirusTotal")
            embed.set_thumbnail(url=image)
            embed.set_author(name="URL Check 🔗", url=f"https://www.virustotal.com/gui/url/{sha256(url.encode()).hexdigest()}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

        else:
            logger.warning(f"No report acquired for URL: {url} \nUser: {ctx.author.name}\n")
            embed = discord.Embed(
                title=f"Looks like this URL doesn't have a report on VirusTotal. 🤔",
                description=f"◈ URL: {url}\n\nClick on the title to see more details on VirusTotal.",
                colour=discord.Colour.orange()
            )
            embed.set_footer(text="Powered by VirusTotal")
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/robloxpokemonbrickbronze/images/d/d8/Metal_Coat_DW.png/revision/latest?cb=20161009161420")
            embed.set_author(name="URL Check", url=f"https://www.virustotal.com/gui/url/{sha256(url.encode()).hexdigest()}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

        await ctx.send(embed=embed)

    @commands.command(help="Check if an IP is malicious using VirusTotal API and return a report if exists. \n Usage: !vt_ip <ip>")
    async def vt_ip(self, ctx, ip: str):
        """Check if an IP is malicious using VirusTotal API and return a report if exists."""
        result = await self.apiHandler.ip_scan(ip)
        logger.info(f"Report asked for IP: {ip} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        
        if isinstance(result, dict):
            logger.info(f"Report acquired for IP: {ip} \nUser: {ctx.author.name}\n")
            if result["malicious"] > 0 or result["suspicious"] > 2:
                color = discord.Colour.red()
                title = f"ALERT: {ip} wants to ruin your day! 💢"
                image = "https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185508/Repelente_m%C3%A1ximo_EP.png"
            else:
                color = discord.Colour.green()
                title = f"{ip} is safe! But stay sharp! 👀"
                image = "https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416"

            embed = discord.Embed(
                title=title,
                description=(
                    f":💀  **Malicious**: {result['malicious']}\n\n"
                    f"🚨 **Suspicious**: {result['suspicious']}\n\n"
                    f"✔️ **Harmless**: {result['harmless']}\n\n"
                    f"👻 **Undetected**: {result['undetected']}\n\n"
                    f"Click on the title to see more details on VirusTotal."
                ),
                colour=color
            )
            embed.set_footer(text="Powered by **VirusTotal**")
            embed.set_thumbnail(url=image)
            embed.set_author(name="IP Checker 🌐", url=f"https://www.virustotal.com/gui/ip-address/{ip}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

        else:
            logger.warning(f"No report acquired for IP: {ip} \nUser: {ctx.author.name}\n")
            embed = discord.Embed(
                title=f"Looks like this IP doesn't have a report on VirusTotal. 🤔",
                description=f"◈ IP: {ip}\n\nClick on the title to see more details on VirusTotal.",
                colour=discord.Colour.orange()
            )
            embed.set_footer(text="Powered by VirusTotal")
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/robloxpokemonbrickbronze/images/d/d8/Metal_Coat_DW.png/revision/latest?cb=20161009161420")
            embed.set_author(name="IP Check", url=f"https://www.virustotal.com/gui/ip-address/{ip}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VirusTotalCog(bot))
