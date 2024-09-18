import discord
from common.args import args
from discord.ext import commands
from config.discord import MANAGEMENT_GUILD_ID


class BaseUserCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        if args.guild is not None:
            self.bot.tree.copy_global_to(guild=discord.Object(id=args.guild))

        print("sync:" + self.__class__.__name__)


class BaseOpsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=discord.Object(id=MANAGEMENT_GUILD_ID))
        print("sync:" + self.__class__.__name__)
