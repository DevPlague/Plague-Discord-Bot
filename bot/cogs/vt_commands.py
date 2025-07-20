import logging
import os
import discord
from discord.ext import commands
from hashlib import sha256
from utils.vt.VTApiHandler import VTApiHandler


logger = logging.getLogger("VT")
VT_API_KEY = os.getenv("VT_API_KEY")
if VT_API_KEY is None:
    logger.error(" No VirusTotal API key found. Please create a .env file with the VT_API_KEY variable.")

class VT(commands.Cog):
    """They check if a URL or an IP is malicious using VirusTotal API and return a report if exists. Also, you can ask for a file analysis attaching it. The API key must be set in the .env file. Format for requests <https://domain> for URLs and <IP> only needed for IPs"""
    def __init__(self, bot):
        self.bot = bot
        self.apiHandler = VTApiHandler(logger, str(VT_API_KEY))

    @commands.command(help="Checks if a URL is malicious using VirusTotal API and returns a report if exists.")
    async def vt_url(self, ctx, url: str):
        logger.info(f" Report asked for URL: {url} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔍")

        result = await self.apiHandler.url_result(url)
        if result is False:
            logger.error(f" Invalid URL: {url}\n")
            return await ctx.send("Invalid URL or WAF is blocking the request. Verify if/that is a valid URL or check it manually on VirusTotal.")


        if isinstance(result, str) and (result.startswith("There was an error") or result.startswith("Request failed")):
            logger.error(f" Error while requesting report for: {url}\n")
            return await ctx.send(result)


        if isinstance(result, dict):
            logger.info(f" Report acquired for URL: {url} \nUser: {ctx.author.name}\n")
            if result["malicious"] > 0 or result["suspicious"] > 2:
                color = discord.Colour.red()
                title = f"ALERT: <{url}> wants to ruin your day! 💢"
                image = "https://play.pokemonshowdown.com/sprites/gen5ani/rotom-heat.gif"

            else:
                color = discord.Colour.green()
                title = f"<{url}> is safe! But stay sharp! 👀"
                image = "https://play.pokemonshowdown.com/sprites/gen5ani/rotom-mow.gif"


            embed = discord.Embed(
                title=title,
                description=(
                    f"💀 **Malicious**: {result['malicious']}\n\n"
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
            logger.warning(f" No report acquired for URL: {url} \nUser: {ctx.author.name}\n")
            embed = discord.Embed(
                title=f"Looks like this URL doesn't have a report on VirusTotal. 🤔",
                description=f"◈ URL: {url}\n\nClick on the title to see more details on VirusTotal.",
                colour=discord.Colour.orange()
            )
            embed.set_footer(text="Powered by VirusTotal")
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/robloxpokemonbrickbronze/images/d/d8/Metal_Coat_DW.png")
            embed.set_author(name="URL Check", url=f"https://www.virustotal.com/gui/url/{sha256(url.encode()).hexdigest()}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

        await ctx.send(embed=embed)


    @commands.command(help="Check if an IP is malicious using VirusTotal API and returns a report if exists.")
    async def vt_ip(self, ctx, ip: str):
        logger.info(f" Report asked for IP: {ip} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔍")

        result = await self.apiHandler.ip_result(ip)
        if result is False:
            logger.error(f" Invalid IP address: {ip}\n")
            return await ctx.send("Invalid IP address. Verify if/that is a public IP and it has a valid format. Maybe the WAF is blocking the request.")


        if isinstance(result, str) and (result.startswith("There was an error") or result.startswith("Request failed")):
            logger.error(f" Error while requesting report for: {ip}\n")
            return await ctx.send(result)


        if isinstance(result, dict):
            logger.info(f" Report acquired for IP: {ip} \nUser: {ctx.author.name}\n")
            if result["malicious"] > 0 or result["suspicious"] > 2:
                color = discord.Colour.red()
                title = f"ALERT: {ip} wants to ruin your day! 💢"
                image = "https://play.pokemonshowdown.com/sprites/gen5ani/rotom-heat.gif"

            else:
                color = discord.Colour.green()
                title = f"{ip} is safe! But stay sharp! 👀"
                image = "https://play.pokemonshowdown.com/sprites/gen5ani/rotom-mow.gif"


            embed = discord.Embed(
                title=title,
                description=(
                    f"💀 **Malicious**: {result['malicious']}\n\n"
                    f"🚨 **Suspicious**: {result['suspicious']}\n\n"
                    f"✔️ **Harmless**: {result['harmless']}\n\n"
                    f"👻 **Undetected**: {result['undetected']}\n\n"
                    f"Click on the title to see more details on VirusTotal."
                ),
                colour=color
            )
            embed.set_footer(text="Powered by VirusTotal")
            embed.set_thumbnail(url=image)
            embed.set_author(name="IP Checker 🌐", url=f"https://www.virustotal.com/gui/ip-address/{ip}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

        else:
            logger.warning(f" No report acquired for IP: {ip} \nUser: {ctx.author.name}\n")
            embed = discord.Embed(
                title=f"Looks like this IP doesn't have a report on VirusTotal. 🤔",
                description=f"◈ IP: {ip}\n\nClick on the title to see more details on VirusTotal.",
                colour=discord.Colour.orange()
            )
            embed.set_footer(text="Powered by VirusTotal")
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/robloxpokemonbrickbronze/images/d/d8/Metal_Coat_DW.png/revision/latest?cb=20161009161420")
            embed.set_author(name="IP Check", url=f"https://www.virustotal.com/gui/ip-address/{ip}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

        await ctx.send(embed=embed)



    @commands.command(help="Uploads a file to VirusTotal API to check if it is malicious and returns a detailed security report. Disclaimer: The file will be uploaded to VirusTotal public database and shared with third parties. Use at your own risk.")
    async def vt_file(self, ctx):
        logger.info(f" File Analysis asked \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔍")
        title = ctx.message.attachments[0].filename
        file = await ctx.message.attachments[0].read()
        

        result = await self.apiHandler.file_upload_and_analyze(file, title)
        if result is False:
            logger.error(f" File couldn't be uploaded: {title}\n")
            return await ctx.send(" File couldn't be uploaded. Max size for VirusTotal API is 32MB at the moment. Try to compress the file or upload it to the website directly.")


        if isinstance(result, str) and (result.startswith("There was an error") or result.startswith("Upload failed")):
            logger.error(f" Error while requesting report for: {title}\n")
            return await ctx.send(result)


        if isinstance(result, tuple):
            result, md5_hash = result
            logger.info(f" Report acquired for: {title} \nUser: {ctx.author.name}\n")
            if result["malicious"] > 0 or result["suspicious"] > 2:
                color = discord.Colour.red()
                title = f"ALERT: {title} wants to ruin your day! 💢"
                image = "https://play.pokemonshowdown.com/sprites/gen5ani/rotom-heat.gif"

            else:
                color = discord.Colour.green()
                title = f"{title} is safe! But stay sharp! 👀"
                image = "https://play.pokemonshowdown.com/sprites/gen5ani/rotom-mow.gif"


            embed = discord.Embed(
                title=title,
                description=(
                    f"💀 **Malicious**: {result['malicious']}\n\n"
                    f"🚨 **Suspicious**: {result['suspicious']}\n\n"
                    f"✔️ **Harmless**: {result['harmless']}\n\n"
                    f"👻 **Undetected**: {result['undetected']}\n\n"
                    f"Click on the title to see more details on VirusTotal."
                ),
                colour=color
            )
            embed.set_footer(text="Powered by VirusTotal")
            embed.set_thumbnail(url=image)
            embed.set_author(name="File Analyzer 📝", url=f"https://www.virustotal.com/gui/file/{md5_hash}", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/4/49/latest/20231030185416/Repelente_EP.png?20231030185416")

            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VT(bot))
