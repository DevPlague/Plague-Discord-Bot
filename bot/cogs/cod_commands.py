import discord
from discord.ext import commands
import logging
from utils.encrypter.coders import encode, decode
from utils.encrypter.hashers import MD5, SHA_256, SHA_3, SHA_512, Argon2, Bcrypt, verify_hash

logger = logging.getLogger("Coder/Decoder-Commands")

CODER_TYPES = ["b", "o", "x", "X", "b64", "url", "rot13"]
HASHER_TYPES = ["md5", "sha256", "sha3", "sha512"]

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



class HasherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# SIMPLE HASHING
    @commands.command(help="Hashes the given text using the specified algorithm (`md5`, `sha256`, `sha3`, `sha512`).\nUsage: `!hash <algorithm> <text>`")
    async def hash(self, ctx, algorithm: str, *args: str):
        """Hashes the given text using the specified algorithm (`md5`, `sha256`, `sha3`, `sha512`).
        
        Args:
            algorithm (str): Hashing algorithm applied to the given text.
            *args (str): The text to be hashed.
        """
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


# ARGON2
    @commands.command(help="Hashes the given password using Argon2. Note: Don't use whitespaces in the password.\nUsage: `!argon2 <password> <iterations> <memory_cost> <parallelism> <hash_len> <type>`\nDefault values: iterations = `3` (1-20 min-max), memory_cost = `65536` (80-1000000 min-max), parallelism = `4` (1-10 min-max), hash_len = `32` (4-100 min-max), type = `id` (`id`, `i`, `d`)")
    async def argon2(self, ctx, password: str, iterations: int = 3, memory_cost: int = 65536, parallelism: int = 4, hash_len: int = 32, type: str = "id"):
        """Hashes the given password using Argon2. (Don't use whitespaces in the password)
        
        Args:
            password (str): The password to be hashed.
            iterations (int, optional): Defaults to `3`. Maximum value: `20`. Minimum value: `1`.
            memory_cost (int, optional): Defaults to `65536`. Maximum value: `1000000`. Minimum value: `80`.
            parallelism (int, optional): Defaults to `4`. Maximum value: `10`. Minimum value: `1`.
            hash_len (int, optional): Defaults to `32`. Maximum value: `100`. Minimum value: `4`.
            type (str, optional): Defaults to `id`. Available types: `id`, `i`, `d`.
        """
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


# BCRYPT
    @commands.command(help="Hashes the given password using Bcrypt. Note: Don't use whitespaces in the password.\nUsage: `!bcrypt <password> <rounds>`\nDefault value: rounds = `12` (1-20 min-max)")
    async def bcrypt(self, ctx, password: str, rounds: int = 12):
        """Hashes the given password using Bcrypt. (Don't use whitespaces in the password)
        
        Args:
            password (str): The password to be hashed.
            rounds (int, optional): Defaults to `12`. Maximum value: `20`. Minimum value: `1`.
        """
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


    # VERIFY HASH
    @commands.command(help="Verify if the given password matches the given hash.\nUsage: `!vhash <hash_func> <hash> <original_text>`\nAvailable hash functions: `md5`, `sha256`, `sha3`, `sha512`, `bcrypt`, `argon2`")
    async def vhash(self, ctx, type: str, hash: str, *args: str):
        """Verify if the given password matches the given hash.
        
        Args:
            hash_func (str): The name of the hash function to use ('md5', 'sha256', 'sha3', 'sha512', 'bcrypt', or 'argon2').
            hash (str): The hash to compare the original text against.
            args (str): The original text to compare with the given hash.
        """
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
    await bot.add_cog(CoderCommands(bot))
    await bot.add_cog(HasherCommands(bot))