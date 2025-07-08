import logging
import discord
from discord.ext import commands
from utils.passwd.password_generator import random_password_generator, memorable_password_generator, MIN_PASS_LEN, MAX_PASS_LEN, MIN_PASS_WORDS, MAX_PASS_WORDS

logger = logging.getLogger("PASSWD")
CAPS = ["c1", "c0"]
NUMS = ["n1", "n0"]
SYM = ["s1", "s0"]

class Password(commands.Cog):
    """Commands to generate random passwords and memorable passwords with custom options.""" 
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Generates a random password.\nc0, n0, s0 to set them False and length must be 8-64.")
    async def randpasswd(self, ctx, length: int = 20, capital: str = "c1", numbers: str = "n1", symbols: str = "s1"):
        logger.info(f" Received request for random password: {length}, {capital}, {numbers}, {symbols} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔒")

        # Pre-Conditions
        if length < MIN_PASS_LEN or length > MAX_PASS_LEN:
            logger.error(f" Invalid length: {length}\n")
            return await ctx.send("Invalid length. Length must be between 8 and 64.")

        if capital not in CAPS or numbers not in NUMS or symbols not in SYM:
            logger.error(f" Invalid option")
            return await ctx.send("Options are invalid. See the help message for the list of valid options.")


        passwd, entropy = random_password_generator(length, capital == "c1", numbers == "n1", symbols == "s1")
        if entropy < 50: 
            strength = "Vulnerable"
        elif entropy < 75:
            strength = "Medium"
        elif entropy < 90:
            strength = "Strong"
        else:
            strength = "Very Strong"


        embed = discord.Embed(
            title = f"Random Password Generator 🔒",
            description = f"""◈ **Length**: {length}\n\n◈ **Capital letters**: {capital == "c1"}\n\n◈ **Numbers**: {numbers == "n1"}\n\n◈ **Symbols**: {symbols == "s1"}\n\n◈ **Password**: **{passwd}** \n\n❗ This password is ___\"{strength}\"___, it has an entropy of {entropy:.2f}.""",
            colour = discord.Colour.from_rgb(106, 71, 249)
        )
        embed.set_footer(text="Top Secret (Destroy this message after reading) 💼")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/honchkrow.gif")
        embed.set_author(name="Vault Keeper 🗝️", icon_url="https://play.pokemonshowdown.com/sprites/trainers/giovanni.png") 


        try:
            logger.info(f" Sent random password to {ctx.author.name}\n")
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            logger.error(f" Failed to send message to {ctx.author.name}\n")
            return await ctx.send("Failed to send message. Check your privacy settings ⚠️")


    @commands.command(help="Generates a random memorable password, consisting of random words and a number, separated by \"-\". Maximum value: 10.")
    async def mempasswd(self, ctx, words: int = 5):
        logger.info(f" Received request for random memorable password: {words} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔒")

        # Pre-Conditions
        if words < MIN_PASS_WORDS or words > MAX_PASS_WORDS:
            logger.error(f" Invalid number of words: {words}\n")
            return await ctx.send("Invalid number of words. Number of words must be between 4 and 10.")


        passwd, entropy = memorable_password_generator(words)
        if entropy < 50: 
            strength = "Vulnerable"
        elif entropy < 75:
            strength = "Medium"
        elif entropy < 90:
            strength = "Strong"
        else:
            strength = "Very Strong"


        embed = discord.Embed(
            title = f"Random Password Generator 🔒",
            description = f"""◈ **Words**: {words}\n\n◈ **Length**: {len(passwd)}\n\n◈ **Password**: **{passwd}** \n\n❗ This password is ___\"{strength}\"___, it has an entropy of {entropy:.2f}.""",
            colour = discord.Colour.from_rgb(106, 71, 249)
        )
        embed.set_footer(text="Top Secret (Destroy this message after reading) 💼")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/honchkrow.gif")
        embed.set_author(name="Vault Keeper 🗝️", icon_url="https://play.pokemonshowdown.com/sprites/trainers/giovanni.png") 


        try:
            logger.info(f" Sent memorable password to {ctx.author.name}\n")
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            logger.error(f" Failed to send message to {ctx.author.name}\n")
            return await ctx.send("Failed to send message. Check your privacy settings ⚠️")



async def setup(bot):
    await bot.add_cog(Password(bot))