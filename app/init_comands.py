import os

import discord
from config.discord import TOKEN
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


# bot起動時
@bot.event
async def on_ready():
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync(guild=None)


bot.run(TOKEN)
