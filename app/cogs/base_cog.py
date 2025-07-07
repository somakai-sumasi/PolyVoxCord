import discord
from base.bot import BaseBot
from common.args import args
from config.discord import MANAGEMENT_GUILD_ID
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: BaseBot, is_ops=False):
        self.bot: BaseBot = bot
        self.is_ops = is_ops

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        if self.is_ops:
            await self.bot.tree.sync(guild=discord.Object(id=MANAGEMENT_GUILD_ID))
        else:
            await self.bot.tree.sync(guild=None)
            if args.guild is not None:
                self.bot.tree.copy_global_to(guild=discord.Object(id=args.guild))
        print("sync:" + self.__class__.__name__)


class BaseUserCog(BaseCog):
    def __init__(self, bot: BaseBot):
        super().__init__(bot)


class BaseOpsCog(BaseCog):
    def __init__(self, bot: BaseBot):
        super().__init__(bot, is_ops=True)
