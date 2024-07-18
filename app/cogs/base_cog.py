import discord
from common.args import args
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        if args.guild is not None:
            self.bot.tree.copy_global_to(guild=discord.Object(id=args.guild))

        print("sync:" + self.__class__.__name__)
