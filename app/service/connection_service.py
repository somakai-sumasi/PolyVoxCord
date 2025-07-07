import asyncio

import discord
from base.bot import BaseBot
from common.user_message import MessageType
from service.presence_service import PresenceService


class ConnectionService:
    @classmethod
    async def read_start(cls, interaction: discord.Interaction, bot: BaseBot):
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

        bot.add_text_channel(user.guild.id, interaction.channel.id)
        await PresenceService.set_presence(bot)

    @classmethod
    async def read_end(cls, interaction: discord.Interaction, bot: BaseBot):
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

        bot.remove_guild(user.guild.id)
        await PresenceService.set_presence(bot)

    @classmethod
    async def auto_disconnect(
        cls,
        before: discord.VoiceState,
        bot: BaseBot,
    ):
        """自動切断を行う

        Parameters
        ----------
        before : discord.VoiceState
            イベント前のVoiceState
        bot : BaseBot
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

        bot.remove_guild(before.channel.guild.id)

        # 正確な表示の為、1秒待機
        await asyncio.sleep(1)
        await PresenceService.set_presence(bot)
