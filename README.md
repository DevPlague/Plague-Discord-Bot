<h1 align="center">Plague Discord-Bot</h1>

<div align="center">
    <br>
    <a href="https://www.docker.com/">
        <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="forthebadge docker"/>
    </a>
    <a href="https://www.python.org/downloads/release/python-3120/">
        <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="forthebadge python"/>
    </a>
    <a href="https://discord.com/">
        <img src="https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white" alt="forthebadge discord"/>
    </a>
    <h3>Bugs may cry 🐛🔥</h3>
</div>

  <p align="center">
<b>Plague</b> is a Discord bot built to assist with common tasks in penetration testing, CTF challenges, and cybersecurity workflows. While it was primarily designed for cybersecurity, Plague also includes features that are useful for regular users, such as scanning potentially malicious URLs, generating QR codes, and creating secure passwords. <b>Plague</b> currently supports 20 commands.
  </p>
</p>

## <img src="https://play.pokemonshowdown.com/sprites/gen5ani/snorlax.gif" width="50px" height="50px"> Showcase


https://github.com/user-attachments/assets/094883a9-dbcd-4d17-8b14-30340776ad7e

<div align="center">
    <video src="media/Bot Showcase First Release.mp4" alt="Bot Showcase Video">
</div>


## <img src="https://play.pokemonshowdown.com/sprites/gen5ani/klinklang.gif" width="50px" height="50px"> Prerequisites

Before cloning the repository, you should be aware that the following components are required for the bot to function:

- Discord Token.
- VirusTotal API key (Optional).

Also, if you want to deploy Plague locally ***without using Docker***, you will need:
- Python 3.11 or 3.12.
- Poetry 2.1.3 or higher.

## <img src="https://play.pokemonshowdown.com/sprites/gen5ani/alakazam-mega.gif" width="50px" height="50px"> Setup and Installation

Since Plague is intended to be deployed locally, we decided to provide two methods for the installation in a concise guide suitable for any user familiarized with Python3 or Docker. It is highly recommended to **install Plague via Docker**, due to its extreme ease; however, you can also install it manually using Poetry.

The Setup Guide for Plague can be found [here](https://github.com/DevPlague/Plague-Discord-Bot/blob/main/docs/Setup%20Guide%20for%20Plague-bot.pdf). 

_Note: **Links don't work on GitHub preview**, download the PDF for a better experience._


## <img src="https://play.pokemonshowdown.com/sprites/gen5ani/marowak-alola.gif" width="50px" height="50px"> Plague Features
- [x] Interactive help command.
- [x] Hash checksum verification and hashing functions.
- [x] QR Generation for both URL and WiFi data.
- [x] Encode/Decode functions for various formats.
- [x] DNS Lookup and Reverse DNS.
- [x] Short URLs Expand.
- [X] Customizable payloads for Reverse Shells, TTY cheatsheet and Web Shells. 
- [X] Memorable/Random Password Generations.
- [x] WAF Detection with [wafw00f](https://github.com/EnableSecurity/wafw00f).
- [x] Detect malicious URLs and IPs via [VirusTotal](https://www.virustotal.com/gui/home/upload) API (you'll need an API key to use the commands associated).
- [X] Clean messages from channels.


## <img src="https://play.pokemonshowdown.com/sprites/gen5ani/conkeldurr.gif" width="50px" height="50px"> Requested features and coming soon!
- [ ] Slash Commands.
- [ ] File Analysis.
- [ ] Extract metadata.
- [ ] CVE Searcher.
- [ ] More moderation and guild management commands.
