import logging

import discord
from config.discord import TOKEN
from discord.ext import commands
from service.presence_service import PresenceService

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

INITIAL_EXTENSIONS = [
    "cogs.guide",
    "cogs.ops",
    "cogs.read",
    "cogs.connection",
    "cogs.user_setting",
    "cogs.guild_setting",
    "cogs.task",
]


# discord接続時
@bot.event
async def setup_hook():
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)


# bot起動時
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await PresenceService.set_presence(bot)


handler = logging.FileHandler(filename="./logs/discord.log", encoding="utf-8", mode="a")
bot.run(TOKEN, log_handler=handler)
