import discord
from discord.ext import commands
import logging
from utils.encrypter.coders import encode, decode

logger = logging.getLogger("Coder/Decoder-Commands")

CODER_TYPES = ["b", "o", "x", "X", "b64", "url", "rot13"]

class CoderCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# ENCODER COMMAND
    @commands.command(help="Encodes the given text into a given format (`b: binary`, `o: octal`, `x: hex`, `X: uppercase hex`, `b64: base64`, `url: URL`, `rot13: ROT13`).\nUsage: `!encode <format> <text>`")
    async def encode(self, ctx, format: str, *args: str):
        """Encodes the given text into a given format (`b: binary`, `o: octal`, `x: hex`, `X: uppercase hex`, `b64: base64`, `url: URL`, `rot13: ROT13`).

        Args:
            format (str): Encoding format. Available formats: `"b"`, `"o"`, `"x"`, `"X"`, `"b64"`, `"url"`, `"rot13"`.
            *args (str): The text to be encoded.
        """
        text = " ".join(args)
        logger.info(f" Received request for encoding: {format}, {text} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔢")

        # Pre-Conditions
        if format not in CODER_TYPES:
            logger.error(f" Invalid format: {format}\n")
            return await ctx.send("Invalid format. See the help message for the list of valid formats.")
        
        if text is None:
            logger.error(f" Invalid text given")
            return await ctx.send("Empty or invalid text.")


        encoded_text = encode(format, text)


        # Post-Conditions
        if encoded_text is None:
            logger.error(f" Error while encoding: {format} - {text}\n")
            return await ctx.send("Error while encoding.")

        if len(encoded_text) > 2000:
            logger.error(f" Encoded text is too long: {len(encoded_text)}\n")
            return await ctx.send("Encoded text is too long (message length limit: 2000 characters).")

        match format:
            case "b": format = "Binary"
            case "o": format = "Octal"
            case "x": format = "Hexadecimal"
            case "X": format = "Uppercase hexadecimal"
            case "b64": format = "Base64"
            case "url": format = "URL"
            case "rot13": format = "ROT13"

        embed = discord.Embed(
            title = f"Encoded Text 🔢",
            description = f"""◈ **Format**: {format}\n\n◈ **Encoded Text**: ```{encoded_text}``` \n\n""",
            colour = discord.Colour.from_rgb(106, 71, 249)
        )
        
        embed.set_footer(text="This job is boring as hell 🧮")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/trainers/clemont.png")
        embed.set_author(name="0xCipher 🧩", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/6/64/latest/20231218184557/Necroluna_EP.png") 
        
        logger.info(f" Sent decoded text to {ctx.author.name}\n")
        await ctx.send(embed=embed)


# DECODER COMMAND
    @commands.command(help="Decodes the given text into its corresponding text (`b`: binary, `o`: octal, `d`: decimal, `x`: hex, `X`: uppercase hex, `b64`: base64, `url`: URL, `rot13`: ROT13).\nUsage: !decode <format> <text>")
    async def decode(self, ctx, format: str, *args: str):
        """Decodes the given text into its corresponding text (`b: binary`, `o: octal`, `d: decimal`, `x: hex`, `X: uppercase hex`, `b64: base64`, `url: URL`).
        
        Args:
            format (str): Encoding format. Available formats: `"b"`, `"o"`, `"d"`, `"x"`, `"X"`, `"b64"`, `"url"`.
            *args (str): The text to be decoded.
        """
        text = " ".join(args)
        logger.info(f" Received request for decoding: {format}, {text} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔢")

        # Pre-Conditions
        if format not in CODER_TYPES:
            logger.error(f" Invalid format: {format}\n")
            return await ctx.send("Invalid format. See the help message for the list of valid formats.")

        if text is None:
            logger.error(f" Invalid text given")
            return await ctx.send("Empty or invalid text.")


        decoded_text = decode(format, text)


        # Post-Conditions
        if decoded_text is None:
            match format:
                case "b":
                    logger.error(f" Invalid binary string: {text}\n")
                    return await ctx.send("Invalid binary string. The string must be in groups of 8 digits (bytes), with or without spaces, and encoded characters must be in UTF-8.")

                case "o":
                    logger.error(f" Invalid octal string: {text}\n")
                    return await ctx.send("Invalid octal string. The string must be in groups of 3 digits, each representing a byte (with or without spaces), and encoded characters must be in UTF-8.")

                case "d":
                    logger.error(f" Invalid decimal string: {text}\n")
                    return await ctx.send("Invalid decimal string. The string must be in groups of digits between 0-127 (with spaces), and encoded characters must be in UTF-8.")

                case "x" | "X":
                    logger.error(f" Invalid hexadecimal string: {text}\n")
                    return await ctx.send("Invalid hexadecimal string. The string must be in groups of even length, and encoded characters must be in UTF-8.")

                case "b64":
                    logger.error(f" Invalid base64 string: {text}\n")
                    return await ctx.send("Invalid base64 string. The encoded characters must be in UTF-8.")

        if decoded_text is str and len(decoded_text) > 2000:
            logger.error(f" Decoded text is too long: {len(decoded_text)}\n")
            return await ctx.send("Decoded text is too long (message length limit: 2000 characters).")

        match format:
            case "b": format = "Binary"
            case "o": format = "Octal"
            case "d": format = "Decimal"
            case "x": format = "Hexadecimal"
            case "X": format = "Uppercase hexadecimal"
            case "b64": format = "Base64"
            case "url": format = "URL"
            case "rot13": format = "ROT13"

        embed = discord.Embed(
            title = f"Decoded Text 🔢",
            description = f"""◈ **Format**: {format}\n\n◈ **Decoded Text**: ```{decoded_text}``` \n\n""",
            colour = discord.Colour.from_rgb(106, 71, 249)
        )
        
        embed.set_footer(text="This job is boring as hell 🧮")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/trainers/clemont.png")
        embed.set_author(name="0xCipher 🧩", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/5/54/latest/20231218183826/Necrosol_EP.png") 
        
        logger.info(f" Sent decoded text to {ctx.author.name}\n")
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(CoderCommands(bot))