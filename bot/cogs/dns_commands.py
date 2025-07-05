import logging
import discord
from discord.ext import commands
from utils.dns import dnslookup

logger = logging.getLogger("DNS")

class DNS(commands.Cog):
    """Commands to perform queries related to DNS"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Performs a DNS lookup for the given domain.")
    async def dnslookup(self, ctx, domain: str):
        logger.info(f" Lookup for {domain}\nUser: {ctx.author}\nServer: {ctx.guild}")
        await ctx.message.add_reaction("👓")

        try:
            results = dnslookup.lookup(domain)
            if not results:
                return await ctx.send("No DNS records found.")


            embed = discord.Embed(
                title=f"DNS Lookup Results for {domain}",
                color=discord.Color.dark_green()
            )


            chars = 0
            embeds = [embed]
            for type, records in results.items():
                field_value = "\n".join(records)
                


                if len(field_value) > 1024:
                    parts = [field_value[i:i+1000] for i in range(0, len(field_value), 1000)] #Split into different parts if the record is too long to fit in a single field
                    for p in parts:
                        embed.add_field(
                            name=f"{type}",
                            value=f"```\n{p}\n```",
                            inline=False
                        )
                else:
                    #If the record is short enough, add it to the field.
                    # Also check if adding this field would exceed the character limit or field count
                    if chars + len(field_value) > 5000 or len(embed.fields) >= 20:
                        embed = discord.Embed(color=discord.Color.blue())
                        embeds.append(embed)
                        chars = 0
                    embed.add_field(
                        name=type,
                        value=f"```\n{field_value}\n```",
                        inline=False
                    )
                    chars += len(field_value)


            for embed in embeds:
                embed.set_footer(text="Dumb Name Service")
                embed.set_author(name="The Resolver 🧙‍♂️", icon_url="https://play.pokemonshowdown.com/sprites/trainers/bryony.png")
                embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/shiftry.gif")
                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"DNS lookup error for `{domain}`: {e}")
            await ctx.send("An error occurred while performing the DNS lookup")


async def setup(bot):
    await bot.add_cog(DNS(bot))