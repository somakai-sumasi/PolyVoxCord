from dotenv import load_dotenv
import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from service.read_service import ReadService


load_dotenv()
GUILD = int(os.getenv("GUILD"))
intents = discord.Intents.all()
activity = discord.Activity(name="MyBot", type=discord.ActivityType.custom)
bot = commands.Bot(command_prefix="!", intents=intents, activity=activity)
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


@bot.tree.command(name="help", description="help: use walk_commands")
@app_commands.guilds(GUILD)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("help")

    for cmd in bot.walk_commands():
        print(cmd.name)
        print(cmd.description)

    cogs = bot.cogs

    for key, val in cogs.items():
        for cmd in val.walk_app_commands():
            print(cmd.name)
            print(cmd.description)


# メッセージ受信時のイベント
@bot.event
async def on_message(message: discord.Message):
    await ReadService.read(message)

# TODO WAVを消す処理を書く

TOKEN = os.getenv("TOKEN")
asyncio.run(main(TOKEN))
