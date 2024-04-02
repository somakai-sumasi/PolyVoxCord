import discord
from discord import app_commands
from discord.ext import commands
from service.presence_service import PresenceService
from service.read_service import ReadService


class connection(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        print("sync:" + self.__class__.__name__)

    @app_commands.guild_only
    @app_commands.command(name="read_start", description="読み上げ開始")
    async def read_start(self, interaction: discord.Interaction):
        """読み上げを開始する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        user = interaction.user
        if user.voice is None:
            await interaction.followup.send("接続してません")
            return

        if user.guild.voice_client is None:
            await user.voice.channel.connect()

        await interaction.followup.send("接続しました")

        ReadService.add_text_channel(user.guild.id, interaction.channel.id)
        await PresenceService.set_presence(self.bot)

    @app_commands.guild_only
    @app_commands.command(name="read_end", description="読み上げ終了")
    async def read_end(self, interaction: discord.Interaction):
        """読み上げを終了する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        user = interaction.user
        if user.guild.voice_client is None:
            await interaction.followup.send("接続してません")
            return

        await user.guild.voice_client.disconnect()
        await interaction.followup.send("切断しました")

        ReadService.remove_guild(user.guild.id)
        await PresenceService.set_presence(self.bot)

    # ボイスチャンネル更新時
    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        before_members = before.channel.members if before.channel is not None else []

        if self.bot.user.id not in list(map(lambda member: member.id, before_members)):
            return

        # 自身以外のメンバーを絞り込み
        members = list(
            filter(lambda member: member.id != self.bot.user.id, before_members)
        )
        if len(members) != 0:
            # 他のユーザに切断されていた場合、表示をリセット
            await PresenceService.set_presence(self.bot)
            return

        await before.channel.guild.voice_client.disconnect()

        ReadService.remove_guild(before.channel.guild.id)
        await PresenceService.set_presence(self.bot)


async def setup(bot: commands.Bot):
    await bot.add_cog(connection(bot))
