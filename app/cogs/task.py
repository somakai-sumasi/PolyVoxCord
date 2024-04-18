import datetime
import os

from discord.ext import commands, tasks

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
        path = "./tmp/wav/"
        files = os.listdir(path)
        now = datetime.datetime.now()

        for file in files:
            _, ext = os.path.splitext(file)
            if ext != ".wav":
                continue

            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path + file))
            # 2日経った音声データを削除する
            if (now - mtime).days > 2:
                os.remove(path + file)


async def setup(bot: commands.Bot):
    await bot.add_cog(Task(bot))
