import discord
from discord import app_commands
from discord.ext import commands
from service.connection_service import ConnectionService
from cogs.base_cog import BaseUserCog


class connection(BaseUserCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.guild_only
    @app_commands.command(name="read_start", description="読み上げ開始")
    async def read_start(self, interaction: discord.Interaction):
        """読み上げを開始する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await ConnectionService.read_start(interaction, self.bot)

    @app_commands.guild_only
    @app_commands.command(name="read_end", description="読み上げ終了")
    async def read_end(self, interaction: discord.Interaction):
        """読み上げを終了する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await ConnectionService.read_end(interaction, self.bot)

    # ボイスチャンネル更新時
    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        await ConnectionService.auto_disconnect(before, self.bot)


async def setup(bot: commands.Bot):
    await bot.add_cog(connection(bot))
