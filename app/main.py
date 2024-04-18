import logging

import discord
from config.discord import TOKEN
from discord.ext import commands
from service.presence_service import PresenceService

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

INITIAL_EXTENSIONS = [
    "cogs.read",
    "cogs.connection",
    "cogs.guide",
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


@bot.tree.command(description="ヘルプコマンド")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()

    commands = {}
    for cmd in bot.tree.walk_commands():
        commands[cmd.name] = cmd.description

    cogs = bot.cogs
    for _, val in cogs.items():
        for cmd in val.walk_app_commands():
            commands[cmd.name] = cmd.description

    embed = discord.Embed(title="コマンド一覧")
    for name, description in commands.items():
        embed.add_field(name="`" + name + "`", value=description, inline=False)

    await interaction.followup.send(embed=embed, ephemeral=False)


handler = logging.FileHandler(filename="./logs/discord.log", encoding="utf-8", mode="a")
bot.run(TOKEN, log_handler=handler)
