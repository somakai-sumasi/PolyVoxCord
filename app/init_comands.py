import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


# bot起動時
@bot.event
async def on_ready():
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync(guild=None)


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
