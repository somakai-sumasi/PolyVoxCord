from dotenv import load_dotenv

load_dotenv()
import asyncio
import datetime
import logging
import os

import discord
from discord.ext import commands, tasks
from service.presence_service import PresenceService
from service.read_service import ReadService

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.all()
activity = discord.Activity(name="MyBot", type=discord.ActivityType.custom)
bot = commands.Bot(
    command_prefix="!", intents=intents, activity=activity, help_command=None
)
queue = asyncio.Queue()

INITIAL_EXTENSIONS = [
    "cogs.guide",
    "cogs.connection",
    "cogs.user_setting",
    "cogs.guild_setting",
]


# cogの呼び出し
async def load_extension():
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)


# discord接続時
@bot.event
async def setup_hook():
    await load_extension()


# bot起動時
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    time_loop.start()
    await PresenceService.set_presence(bot)


# ボイスチャンネル更新時
@bot.event
async def on_voice_state_update(
    member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
):
    if bot.user.id not in list(map(lambda member: member.id, before.channel.members)):
        return

    # 自身以外のメンバーを絞り込み
    members = list(
        filter(lambda member: member.id != bot.user.id, before.channel.members)
    )
    if len(members) != 0:
        # 他のユーザに切断されていた場合、表示をリセット
        ReadService.remove_guild(before.channel.guild.id)
        await PresenceService.set_presence(bot)
        return

    await before.channel.guild.voice_client.disconnect()

    ReadService.remove_guild(before.channel.guild.id)
    await PresenceService.set_presence(bot)


@bot.tree.command(description="ヘルプコマンド")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()

    commands = {}
    for cmd in bot.tree.walk_commands():
        commands[cmd.name] = cmd.description

    cogs = bot.cogs
    for key, val in cogs.items():
        for cmd in val.walk_app_commands():
            commands[cmd.name] = cmd.description

    embed = discord.Embed(title="コマンド一覧")
    for name, description in commands.items():
        embed.add_field(name="`" + name + "`", value=description, inline=False)

    await interaction.followup.send(embed=embed, ephemeral=False)


utc = datetime.timezone.utc
time = datetime.time(hour=4, minute=00, tzinfo=utc)


@tasks.loop(time=time)
async def time_loop():
    path = "./wav/"
    files = os.listdir(path)
    now = datetime.datetime.now()

    for file in files:
        name, ext = os.path.splitext(file)
        if ext != ".wav":
            continue

        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path + file))
        # 2日経った音声データを削除する
        if (now - mtime).days > 2:
            os.remove(path + file)


# メッセージ受信時のイベント
@bot.event
async def on_message(message: discord.Message):
    await ReadService.read(message)


bot.run(os.getenv("TOKEN"), log_handler=handler)
