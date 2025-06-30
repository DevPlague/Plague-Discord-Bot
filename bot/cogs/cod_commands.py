import logging
import discord
from discord.ext import commands
from utils.encrypter.coders import encode, decode
from utils.encrypter.hashers import MD5, SHA_256, SHA_3, SHA_512, Argon2, Bcrypt, verify_hash

logger = logging.getLogger("CYPHER")
CODER_TYPES = ["b", "o", "x", "X", "b64", "url", "rot13"]
HASHER_TYPES = ["md5", "sha256", "sha3", "sha512"]

class Encoder(commands.Cog):
    """Encodes the given text into a given format and decodes the given text into its corresponding text."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Encodes the given text into a given format. Possible formats: \n - `b: binary` \n - `o: octal` \n - `x: hex` \n - `X: uppercase hex` \n - `b64: base64` \n - `url: URL` \n - `rot13: ROT13`.")
    async def encode(self, ctx, format: str, *args: str):
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

        if len(encoded_text) > 1900:
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
            colour = discord.Colour.from_rgb(135, 206, 235)
        )
        embed.set_footer(text="This job is boring as hell 🧮")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/porygonz.gif")
        embed.set_author(name="0xCipher 🧩", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/6/64/latest/20231218184557/Necroluna_EP.png")
        logger.info(f" Sent decoded text to {ctx.author.name}\n")
        await ctx.send(embed=embed)


    @commands.command(help="Decodes the given text into its corresponding text. Possible formats: \n - `b: binary` \n - `o: octal` \n - `d: decimal` \n - `x: hex` \n - `X: uppercase hex` \n - `b64: base64` \n - `url: URL` \n - `rot13: ROT13`.")
    async def decode(self, ctx, format: str, *args: str):
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

        if decoded_text is str and len(decoded_text) > 1900:
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
            colour = discord.Colour.from_rgb(135, 206, 235)
        )
        embed.set_footer(text="This job is boring as hell 🧮")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/porygonz.gif")
        embed.set_author(name="0xCipher 🧩", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/5/54/latest/20231218183826/Necrosol_EP.png") 
        logger.info(f" Sent decoded text to {ctx.author.name}\n")
        await ctx.send(embed=embed)



class Hasher(commands.Cog):
    """Hashes the given text using the specified algorithm. Custom hash functions have there own commands. Also, there is a function to verify if a given text matches the given hash."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Hashes the given text using the specified algorithm (`md5`, `sha256`, `sha3`, `sha512`). Only available in DMs.")
    async def hash(self, ctx, algorithm: str, *args: str):
        text = " ".join(args)
        if not isinstance(ctx.channel, discord.DMChannel):
            logger.warning(f" Invoked hashing in a non-DM channel\n")
            return await ctx.message.add_reaction("🙅‍♂️")


        logger.info(f" Received request for hashing: {algorithm}, \nUser: {ctx.author.name}")
        await ctx.message.add_reaction("🔄")

        # Pre-Conditions
        if algorithm not in HASHER_TYPES:
            logger.error(f" Invalid algorithm: {algorithm}\n")
            return await ctx.send("Invalid algorithm. See the help message for the list of valid algorithms.")
        
        if text is None:
            logger.error(f" Invalid text given")
            return await ctx.send("Empty or invalid text.")


        match algorithm:
            case "md5":
                hashed_text = MD5(text)
            case "sha256":
                hashed_text = SHA_256(text)
            case "sha3":
                hashed_text = SHA_3(text)
            case "sha512":
                hashed_text = SHA_512(text)


        #Post-Conditions
        if hashed_text is None:
            logger.error(f" Error while hashing: {algorithm} - {text}\n")
            return await ctx.send("Error while hashing.")

        if len(hashed_text) > 1900:
            logger.error(f" Hashed text is too long: {len(hashed_text)}\n")
            return await ctx.send("Hashed text is too long (message length limit: 2000 characters).")


        embed = discord.Embed(
            title = f"Hashed Text 🔄",
            description = f"""◈ **Algorithm**: {algorithm}\n\n◈ **Hashed Text**: ```{hashed_text}``` \n\n""",
            colour = discord.Colour.from_rgb(135, 206, 235)
        )
        embed.set_footer(text="Somehow better than encoding 🕹️")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/porygonz.gif")
        embed.set_author(name="0xCipher 🧩", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/8/8b/latest/20221213211136/Dado_trucado_EP.png") 
        logger.info(f" Sent {algorithm} hashed text to {ctx.author.name}\n")
        await ctx.send(embed=embed)


    @commands.command(help="Hashes given password using Argon2. Only available in DMs. Don't use whitespaces in the password.\nPossible values for: \n - iterations (1-20) \n - memory_cost (80-1000000) \n - parallelism (1-10) \n - hash_len (4-100) \n - type (`id`, `i`, `d`)")
    async def argon2(self, ctx, password: str, iterations: int = 3, memory_cost: int = 65536, parallelism: int = 4, hash_len: int = 32, type: str = "id"):
        if not isinstance(ctx.channel, discord.DMChannel):
            logger.warning(f" Invoked Argon2 hashing in a non-DM channel\n")
            return await ctx.message.add_reaction("🙅‍♂️")

        logger.info(f" Received request for Argon2 hashing: \n Iterations: {iterations} - Memory Cost: {memory_cost} - Parallelism: {parallelism} - Hash Length: {hash_len} - Type: {type} \nUser: {ctx.author.name}")
        await ctx.message.add_reaction("🔄")

        # Pre-Conditions
        if password is None:
            logger.error(f" Invalid password given")
            return await ctx.send("Empty or invalid password.")


        hashed_password = Argon2(password, iterations, memory_cost, parallelism, hash_len, type)


        # Post-Conditions
        if hashed_password is None:
            logger.error(f" Error while hashing with Argon2\n")
            return await ctx.send("Error while hashing.  Check if you have used whitespaces, or the given parameters are under/over the limits established.")


        embed = discord.Embed(
            title = f"Argon2 Hashed Password 🔄",
            description = f"""◈ **Password**: {password}\n\n◈ **Hashed Password**: ```{hashed_password}``` \n\n""",
            colour = discord.Colour.from_rgb(135, 206, 235)
        )
        embed.set_footer(text="Somehow better than encoding 🕹️")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/porygonz.gif")
        embed.set_author(name="0xCipher 🧩", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/8/8b/latest/20221213211136/Dado_trucado_EP.png") 
        logger.info(f" Sent Argon2 hashed password to {ctx.author.name}\n")
        await ctx.send(embed=embed)


    @commands.command(help="Hashes the given password using Bcrypt. Only available in DMs. Don't use whitespaces in the password. Possible value for: \n - rounds(1-20)")
    async def bcrypt(self, ctx, password: str, rounds: int = 12):
        logger.info(f" Received request for Bcrypt hashing (Rounds: {rounds})\nUser: {ctx.author.name}")
        await ctx.message.add_reaction("🔄")

        # Pre-Conditions
        if password is None:
            logger.error(f" Invalid password given")
            return await ctx.send("Empty or invalid password.")


        hashed_password = Bcrypt(password, rounds)


        # Post-Conditions
        if hashed_password is None:
            logger.error(f" Error while hashing with Bcrypt\n")
            return await ctx.send("Error while hashing.  Check if you have used whitespaces, or the given parameters are under/over the limits established.")

        if len(hashed_password) > 1900:
            logger.error(f" Hashed password is too long: {len(hashed_password)}\n")
            return await ctx.send("Hashed password is too long (message length limit: 2000 characters).")


        embed = discord.Embed(
            title = f"Bcrypt Hashed Password 🔄",
            description = f"""◈ **Password**: {password}\n\n◈ **Hashed Password**: ```{hashed_password}``` \n\n""",
            colour = discord.Colour.from_rgb(135, 206, 235)
        )
        embed.set_footer(text="Somehow better than encoding 🕹️")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/porygonz.gif")
        embed.set_author(name="0xCipher 🧩", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/8/8b/latest/20221213211136/Dado_trucado_EP.png")
        logger.info(f" Sent Bcrypt hashed password to {ctx.author.name}\n")
        await ctx.send(embed=embed)


    @commands.command(help="Verify if the given text matches the given hash.\nAvailable hash functions: `md5`, `sha256`, `sha3`, `sha512`, `bcrypt`, `argon2`")
    async def vhash(self, ctx, type: str, hash: str, *args: str):
        HASHER_TYPESv2 = HASHER_TYPES + ["bcrypt", "argon2"]
        text = " ".join(args)
        logger.info(f" Received request for verifying hash: \nHash Function: {type} - Hash: {hash} - Original Text: {text} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("🔑✅")


        # Pre-Conditions
        if hash is None:
            logger.error(f" Invalid hash given")
            return await ctx.send("Empty or invalid hash.")

        if text is None:
            logger.error(f" Invalid text given")
            return await ctx.send("Empty or invalid text.")

        if type not in HASHER_TYPESv2:
            logger.error(f" Invalid hash function\n")
            return await ctx.send("Invalid hash function. See the help message for the list of valid hash functions.")


        valid = verify_hash(type, text, hash)


        if valid:
            logger.info(f" Hash {type} matched the given text\n")
            return await ctx.send(f"Hash {type} matched the given text 🔑✅")
        else:
            logger.info(f" Hash {type} did not match the given text\n")
            return await ctx.send(f"Hash {type} did not match the given text 🔑❌")



async def setup(bot):
    await bot.add_cog(Encoder(bot))
    await bot.add_cog(Hasher(bot))