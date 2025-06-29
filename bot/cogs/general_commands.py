import logging
import urllib.request
import discord
from discord.ext import commands


logger = logging.getLogger("GENERAL")

class General(commands.Cog):
    """Commands that don't fit in any other category, like clean up channels, expand URLs, etc..."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Clears messages in a channel. Default: 10 messages.")
    async def purge(self, ctx, amount : int = 10):
        if not ctx.author.guild_permissions.manage_messages:
            return 

        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            return

        logger.info(f" Purging {amount} messages in {ctx.channel.name} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.channel.purge(limit=amount)


    @commands.command(help="Expands a shortened URL to show its final destination.")
    async def xpand(self, ctx, short_url: str):
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
    await bot.add_cog(General(bot))