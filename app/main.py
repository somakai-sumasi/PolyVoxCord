from dotenv import load_dotenv
import os
import asyncio
import discord
from discord.ext import commands
from service.read_service import ReadService

INITIAL_EXTENSIONS = [
    "cogs.guide",
    "cogs.connection",
    "cogs.user_setting",
    "cogs.guild_setting",
]

intents = discord.Intents.all()
activity = discord.Activity(name="MyBot", type=discord.ActivityType.custom)
bot = commands.Bot(command_prefix="!", intents=intents, activity=activity)
queue = asyncio.Queue()


# cogの呼び出し
async def load_extension():
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)


# botを起動
async def main(token):
    async with bot:
        await load_extension()
        await bot.start(token)


# 起動時のイベント
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


# メッセージ受信時のイベント
@bot.event
async def on_message(message: discord.Message):
    await ReadService.read(message)


load_dotenv()
TOKEN = os.getenv("TOKEN")
asyncio.run(main(TOKEN))
