# main.py
from dotenv import load_dotenv
import os
import asyncio
import discord
from discord.ext import commands


INITIAL_EXTENSIONS = [
    "cogs.connection",
    "cogs.setting",
]

intents = discord.Intents.all()
activity = discord.Activity(name="MyBot", type=discord.ActivityType.custom)

bot = commands.Bot(command_prefix="!", intents=intents, activity=activity)


async def load_extension():
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)


async def main(token):
    async with bot:
        await load_extension()
        await bot.start(token)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージの送信者がbotだった場合は無視
    if message.author.bot:
        return
    # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
    if message.guild.voice_client is None:
        return
    print(message.content)


load_dotenv()
TOKEN = os.getenv("TOKEN")
asyncio.run(main(TOKEN))
