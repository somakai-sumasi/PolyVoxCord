import discord
from discord.ext import commands
from service.presence_service import PresenceService


class BaseBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    def get_cogs(self) -> list[str]:
        """読み込むcogのリストを返す

        Returns
        -------
        list[str]
            読み込むcogのリスト
        """
        return [
            "cogs.guide",
            "cogs.ops",
            "cogs.read",
            "cogs.connection",
            "cogs.user_setting",
            "cogs.guild_setting",
            "cogs.task",
        ]

    async def setup_hook(self):
        for cog in self.get_cogs():
            await self.load_extension(cog)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        await PresenceService.set_presence(self)
