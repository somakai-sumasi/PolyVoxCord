import datetime

import discord
from discord.ext import commands
from service.read_service import ReadService


class Read(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        print("sync:" + self.__class__.__name__)

    # メッセージ受信時のイベント
    @commands.Cog.event
    async def on_message(message: discord.Message):
        await ReadService.read(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Read(bot))
