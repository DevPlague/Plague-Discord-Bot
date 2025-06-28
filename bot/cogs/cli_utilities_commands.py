import discord
from discord.ext import commands
import logging
import subprocess
import re

logger = logging.getLogger("URL-Expander")

# wafw00f COMMAND
TIMEOUT = 3     # 3 seconds timeout for the requests
WAF_FOUND = re.compile(r"\[\+\] The site (https?://[^\s]+) is behind (.+?)(?: and/or (.+?))? WAF\.")
WAF_NOT_FOUND = re.compile(r"\[\-\]")
REQUESTS = re.compile(r"\[~\] Number of requests: \d+")

class wafw00fCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Runs the wafw00f tool to detect the presence of a Web Application Firewall (WAF) on the given URL. \nUsage: `!wafw00f <url>`")
    async def wafw00f(self, ctx, url: str):
        """
        Runs the wafw00f tool to detect the presence of a Web Application Firewall (WAF)
        on the given URL.

        Args:
            url (str): The URL of the website to analyze.
        """
        logger.info(f" (wafw00f) Received URL to analyze: {url} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔥")
        await ctx.message.add_reaction("🛡️")

        proc = subprocess.run(["wafw00f", "-a", f"-T {TIMEOUT}", "--no-colors", url], capture_output=True)
        output = proc.stdout.decode("utf-8")

        embed_desc = ""
        match = re.search(WAF_FOUND, output)
        requests = re.search(REQUESTS, output)

        if match:
            # Opción 1: Linea del wafw00f entera (quitando el [+])
            embed_desc = match.group(0)[4:]

            # Opción 2: Cada apartado por separado
            url = match.group(1)
            waf1 = match.group(2)
            waf2 = match.group(3)
            if waf2 is not None:
                embed_desc = f"URL: {url}\n**WAF 1**: {waf1}\n**WAF 2**: {waf2}\n{requests.group(0)[4:]}"
            else:
                embed_desc = f"URL: {url}\n**WAF 1**: {waf1}\n{requests.group(0)}"

        elif re.search(WAF_NOT_FOUND, output):
            embed_desc = f"No WAF detected by the generic detection.\n{requests.group(0)[4:]}"

        else:
            embed_desc = f"Site **{url}** appears to be down (or does not exist)."

        logger.info(f" wafw00f analysis obtained: {output}\nUser: {ctx.author.name}\n")

        embed = discord.Embed(
            title = f"Block Block 🐕",
            description = f"""{embed_desc}\n""",
            colour = discord.Colour.from_rgb(233, 84, 32)
        )
        embed.set_footer(text="Set Fire to the Rain 🔥🌧️")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/houndoom.gif")
        embed.set_author(name="El Can Severo 🐶", icon_url="https://art.pixilart.com/d979e6a5010c076.png")

        logger.info(f" Sent wafw00f check to {ctx.author.name}\n")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(wafw00fCog(bot))