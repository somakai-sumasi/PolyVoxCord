import discord
from discord.ext import commands
from service.read_service import ReadService
from cogs.base_cog import BaseUserCog


class Read(BaseUserCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    # メッセージ受信時のイベント
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await ReadService.read(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Read(bot))
