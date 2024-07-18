import datetime

from discord.ext import commands, tasks
from service.task_service import TaskDictService
from cogs.base_cog import BaseCog

utc = datetime.timezone.utc
time = datetime.time(hour=4, minute=00, tzinfo=utc)


# 一定時間で管理する系
class Task(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.time_loop.start()

    @tasks.loop(time=time)
    async def time_loop(self):
        TaskDictService.remove_wav_files()


async def setup(bot: commands.Bot):
    await bot.add_cog(Task(bot))
