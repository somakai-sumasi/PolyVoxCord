import asyncio
import datetime
import os

import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from service.read_service import ReadService

load_dotenv()
GUILD = int(os.getenv("GUILD"))
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


# botを起動
async def main(token):
    async with bot:
        await load_extension()
        await bot.start(token)


# 起動時
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    time_loop.start()


# ボイスチャンネル更新時
@bot.event
async def on_voice_state_update(
    member: discord.Member, before: discord.VoiceState, after: discord.VoiceState
):
    if before == None:
        return

    # 自身以外のメンバーを絞り込み
    members = list(
        filter(lambda member: member.id != bot.user.id, before.channel.members)
    )
    if len(members) == 0:
        await before.channel.guild.voice_client.disconnect()


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


TOKEN = os.getenv("TOKEN")
asyncio.run(main(TOKEN))
