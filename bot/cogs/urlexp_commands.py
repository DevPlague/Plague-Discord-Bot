import discord
from discord.ext import commands
import logging
import urllib.request

logger = logging.getLogger("URL-Expander")

class URLExpanderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Expands a shortened URL to show its final destination. \nUsage: `!xpand <url>`")
    async def xpand(self, ctx, short_url: str):
        """Expands a shortened URL to show its final destination.

        Args:
            short_url (str): The shortened URL to expand.
        """
        logger.info(f" Received short URL to expand: {short_url} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🌐")

        try:
            expanded_url = None
            response = urllib.request.urlopen(short_url)
            expanded_url = response.geturl()
        except Exception:
            pass

        if expanded_url is None:
            logger.error(f" Error expanding '{short_url}'")
            return await ctx.send("Invalid URL. Verify that the format is correct or that it exists at all.")

        logger.info(f" Expanded URL obtained: {expanded_url}\nUser: {ctx.author.name}\n")

        embed = discord.Embed(
            title = f"URL Xpander ↔️",
            description = f"""Short URL: {short_url}\n**Expanded URL**: {expanded_url}\n""",
            colour = discord.Colour.from_rgb(205, 36, 151)
        )
        embed.set_footer(text="URL Big Bang Theory 💥")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/spiritomb.gif")
        embed.set_author(name="The Omniscient 🔮", icon_url="https://wiki.p-insurgence.com/images/b/bf/442.png")

        logger.info(f" Sent expanded URL to {ctx.author.name}\n")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(URLExpanderCog(bot))