import logging
import discord
from discord.ext import commands
from typing import Optional
from utils.qrcode.qr_str import generate_qr
from utils.qrcode.qr_wifi import generate_wifi_qr

logger = logging.getLogger("QR")

class QR(commands.Cog):
    """Generates a QR code image from the given data with an optional logo, avaible for text, URL and WiFi."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Generates a QR code image from the given data with an optional logo.")
    async def genQR(self, ctx, data, logo_url: Optional[str] = None):
        logger.info(f" QR generation asked \nData: {data} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("📷")

        if data is None:
            logger.error(f" Invalid data given")
            return await ctx.send("Empty or invalid data to include in the QR.")


        try:
            if logo_url:
                qr = generate_qr(data, logo_url)
            else:
                qr = generate_qr(data)

        except ValueError as e:
            logger.error(f"QR generation failed: {e}")
            await ctx.send(f"Couldn't load the given logo. Make sure that the URL points to a valid image format. Content-Type must starts with 'image/'.")
            return

        except Exception as e:
            logger.error(f"Unexpected error during QR generation: {e}")
            await ctx.send("Unexpected error while QR generation.")
            return


        file = discord.File(qr, filename="qr.png")
        embed = discord.Embed(
            title = f"QR Code 📷",
            description = f"""◈ **Data**: {data}""",
            colour = discord.Colour.from_rgb(255, 255, 255)
        )
        embed.set_footer(text="Real ones keep it square, no cap 📐")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/medicham-mega.gif")
        embed.set_author(name="The Bronx 📦", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/a/ab/latest/20230122133600/Periscopio_EP.png")
        embed.set_image(url="attachment://qr.png")


        logger.info(f" Sent QR to {ctx.author.name}\n")
        await ctx.send(embed=embed, file=file)


    @commands.command(help="Generates a WiFi QR code image that can be scanned to connect automatically. You can specify an unprotected network in security arg by passing \"nopass\" and skip the password arg. Command is only available in DMs.")
    async def wifiQR(self, ctx, *args):
        if not isinstance(ctx.channel, discord.DMChannel):
            return await ctx.send("Command only available in DMs.")

        if len(args) < 2:
            return await ctx.send("You must provide at least SSID and security type.")

        ssid = args[0]
        security = args[1].upper().strip()
        password = None
        logo_url = None


        if security == "nopass":
            if len(args) == 3:
                logo_url = args[2]
            elif len(args) > 3:
                return await ctx.send("Too many arguments for an open network.")
        else:
            if len(args) < 3:
                return await ctx.send("You must provide a password for secured networks.")
            password = args[2]
            if len(args) == 4:
                logo_url = args[3]
            elif len(args) > 4:
                return await ctx.send("Too many arguments.")
        if ctx.guild is not None:
            return await ctx.send("Command only available in DMs.")


        logger.info(f" Wifi QR generation asked \nSSID: {ssid} \nSecurity: {security} \nUser: {ctx.author.name}")
        await ctx.message.add_reaction("📶")
        if security == "nopass" and password:
            logger.error(f" Invalid data given")
            return await ctx.send("Password cannot be set for a network without security.")
        
        if security != "nopass" and not password:
            logger.error(f" Invalid data given")
            return await ctx.send("Password must be set for a network with security.")

        if security in ["WPA2", "WPA3", "WPA/WPA2", "WPA/WPA2/WPA3", "WPA3-PERSONAL", "WPA2-PERSONAL"]:
            security = "WPA"


        try:
            if logo_url:
                qr = generate_wifi_qr(ssid, security, password, logo_url)
            else:
                qr = generate_wifi_qr(ssid, security, password)

        except ValueError as e:
            logger.error(f"QR generation failed: {e}")
            return await ctx.send(f"Couldn't load the given logo. Make sure that the URL points to a valid image format. Content-Type must starts with 'image/'.")

        except Exception as e:
            logger.error(f"Unexpected error during QR generation: {e}")
            return await ctx.send("Unexpected error while QR generation.")


        file = discord.File(qr, filename="qr.png")
        embed = discord.Embed(
            title = f"QR Code 📷",
            description = f"""◈ **SSID**: {ssid}\n\n◈ **Security**: {security}\n""",
            colour = discord.Colour.from_rgb(255, 255, 255)
        )
        embed.set_footer(text="Real ones keep it square, no cap 📐")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/gen5ani/medicham-mega.gif")
        embed.set_author(name="The Bronx 📦", icon_url="https://images.wikidexcdn.net/mwuploads/wikidex/a/ab/latest/20230122133600/Periscopio_EP.png")
        embed.set_image(url="attachment://qr.png")


        logger.info(f" Sent Wifi QR to {ctx.author.name}\n")
        await ctx.send(embed=embed, file=file)



async def setup(bot):
    await bot.add_cog(QR(bot))