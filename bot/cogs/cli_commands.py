import re
import logging
import subprocess
import discord
from discord.ext import commands

logger = logging.getLogger("CLI")

# Constants for wafw00f
WAF_FOUND = re.compile(r"\[\+\] The site (https?://[^\s]+) is behind (.+?)(?: and/or (.+?))? WAF\.")
WAF_NOT_FOUND = re.compile(r"\[\-\]")
TIMEOUT = 5
REQUESTS = re.compile(r"\[~\] Number of requests: \d+")


class CLI(commands.Cog):
    """CLI commands. Tools that the bot uses must be installed on the system employed by it. We strongly recommend using the Dockerfile to build and deploy a container rather than installing the tools in local."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Runs the wafw00f tool to detect the presence of WAFs on the given URL.")
    async def wafw00f(self, ctx, url: str):
        logger.info(f" (wafw00f) Received URL to analyze: {url} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔥")
        await ctx.message.add_reaction("🛡️")


        proc = subprocess.run(["wafw00f", "-a", f"-T {TIMEOUT}", "--no-colors", url], capture_output=True)
        output = proc.stdout.decode("utf-8")
        embed_desc = ""
        match = re.search(WAF_FOUND, output)
        requests = re.search(REQUESTS, output)

        if match:
            # Op1: Full match
            embed_desc = match.group(0)[4:]

            # Op2: Partial match
            url = match.group(1)
            waf1 = match.group(2)
            waf2 = match.group(3)
            if waf2 is not None:
                embed_desc = f"URL: {url}\n**WAF 1**: {waf1}\n**WAF 2**: {waf2}\n{requests.group(0)[4:]}" # type: ignore
            else:
                embed_desc = f"URL: {url}\n**WAF 1**: {waf1}\n{requests.group(0)}" # type: ignore


        elif re.search(WAF_NOT_FOUND, output):
            embed_desc = f"No WAF detected by the generic detection.\n{requests.group(0)[4:]}" # type: ignore
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
    await bot.add_cog(CLI(bot))