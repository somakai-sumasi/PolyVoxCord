import datetime

from discord.ext import commands, tasks
from service.task_service import TaskDictService

utc = datetime.timezone.utc
time = datetime.time(hour=4, minute=00, tzinfo=utc)


# 一定時間で管理する系
class Task(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.time_loop.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        print("sync:" + self.__class__.__name__)

    @tasks.loop(time=time)
    async def time_loop(self):
        TaskDictService.remove_wav_files()


async def setup(bot: commands.Bot):
    await bot.add_cog(Task(bot))
