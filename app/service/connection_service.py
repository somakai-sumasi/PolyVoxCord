import discord
from common.user_message import MessageType
from discord.ext import commands
from service.presence_service import PresenceService
from service.read_service import ReadService


class ConnectionService:
    @classmethod
    async def read_start(cls, interaction: discord.Interaction, bot: commands.Bot):
        """読み上げを開始する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        bot : commands.Bot
            Discord bot
        """
        await interaction.response.defer()

        user = interaction.user
        if user.voice is None:
            await interaction.followup.send(
                embed=discord.Embed(title="接続してません", color=MessageType.WARNING)
            )
            return

        if user.guild.voice_client is None:
            await user.voice.channel.connect()

        await interaction.followup.send(
            embed=discord.Embed(title="接続しました", color=MessageType.SUCCESS)
        )

        ReadService.add_text_channel(user.guild.id, interaction.channel.id)
        await PresenceService.set_presence(bot)

    @classmethod
    async def ead_end(cls, interaction: discord.Interaction, bot: commands.Bot):
        """読み上げを終了する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        bot : commands.Bot
            Discord bot
        """

        await interaction.response.defer()

        user = interaction.user
        if user.guild.voice_client is None:
            await interaction.followup.send(
                embed=discord.Embed(title="接続してません", color=MessageType.WARNING)
            )
            return

        await user.guild.voice_client.disconnect()
        await interaction.followup.send(
            embed=discord.Embed(title="切断しました", color=MessageType.SUCCESS)
        )

        ReadService.remove_guild(user.guild.id)
        await PresenceService.set_presence(bot)

    @classmethod
    async def auto_disconnect(
        cls,
        before: discord.VoiceState,
        bot: commands.Bot,
    ):
        """自動切断を行う

        Parameters
        ----------
        before : discord.VoiceState
            イベント前のVoiceState
        bot : commands.Bot
            Discord bot
        """
        before_members = before.channel.members if before.channel is not None else []

        if bot.user.id not in list(map(lambda member: member.id, before_members)):
            return

        # 自身以外のメンバーを絞り込み
        members = list(filter(lambda member: member.id != bot.user.id, before_members))
        if len(members) != 0:
            # 他のユーザに切断されていた場合、表示をリセット
            await PresenceService.set_presence(bot)
            return

        await before.channel.guild.voice_client.disconnect()

        ReadService.remove_guild(before.channel.guild.id)
        await PresenceService.set_presence(bot)
