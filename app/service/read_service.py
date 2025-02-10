import asyncio
import os
from typing import Dict, List

import discord
from service.make_voice_service import MakeVoiceService


class ReadService:
    # 読み上げ管理キュー
    queue_map = {}
    text_channel_list: Dict[int, List[int]] = {}

    @classmethod
    async def read(cls, message: discord.Message):
        """読み上げイベントを管理

        Parameters
        ----------
        message : discord.Message
            discord.Message
        """
        # メッセージの送信者がbotだった場合は無視
        if message.author.bot:
            return
        # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
        if message.guild.voice_client is None:
            return

        # 読み上げ対象でないチャンネルは無視
        if not cls.has_channel(message.guild.id, message.channel.id):
            return

        guild_id = message.guild.id
        message_id = message.id
        # ギルドごとのキューが存在しない場合は作成
        if guild_id not in cls.queue_map:
            cls.queue_map[guild_id] = asyncio.Queue()
        # メッセージとメッセージIDをキューに追加
        await cls.queue_map[guild_id].put((message_id, message))

        while True:
            next_message_id, next_message = await cls.queue_map[guild_id].get()
            if next_message_id == message_id:
                # メッセージ,添付ファイルの順番に読み上げ
                await asyncio.gather(
                    cls.read_message(next_message),
                    cls.read_file(next_message),
                )

                break
            else:
                # 自分の番でない場合、キューを戻す
                await cls.queue_map[guild_id].put((next_message_id, next_message))

    @classmethod
    async def read_message(cls, message: discord.Message):
        """メッセージを読み上げる

        Parameters
        ----------
        message : discord.Message
           discord.Message
        """
        try:
            content = message.clean_content
            if len(content) < 1:
                return

            make_voice_service = MakeVoiceService(message.guild.id, message.author.id)
            path = await make_voice_service.make_voice(
                content, is_omit_url=True, is_read_limit=True
            )

            voice_client: discord.VoiceClient = message.guild.voice_client

            # 他の音声が再生されていないか確認
            while voice_client.is_playing():
                await asyncio.sleep(0.5)

            # 明示的に再生をストップ
            voice_client.stop()

            # 音声を再生
            voice_client.play(discord.FFmpegPCMAudio(path))

        except Exception as e:
            print("=== エラー内容 ===")
            print("type:" + str(type(e)))
            print("args:" + str(e.args))
            print("message:" + e.message)
            print("e自身:" + str(e))

    @classmethod
    async def read_file(cls, message: discord.Message):
        """ファイルを読み上げる

        Parameters
        ----------
        message : discord.Message
            discord.Message
        """
        try:
            attachments = message.attachments
            for attachment in attachments:
                _, ext = os.path.splitext(attachment.filename)
                if ext != ".txt":
                    continue

                byte_content = await attachment.read()
                content = byte_content.decode("utf-8")
                if len(content) < 1:
                    return

                make_voice_service = MakeVoiceService(
                    message.guild.id, message.author.id
                )

                path = await make_voice_service.make_voice(
                    content, is_omit_url=True, is_read_limit=True
                )

                voice_client: discord.VoiceClient = message.guild.voice_client

                # 他の音声が再生されていないか確認
                while voice_client.is_playing():
                    await asyncio.sleep(0.5)

                # 音声を再生
                voice_client.play(discord.FFmpegPCMAudio(path))

        except Exception as e:
            print("=== エラー内容 ===")
            print("type:" + str(type(e)))
            print("args:" + str(e.args))
            print("message:" + e.message)
            print("e自身:" + str(e))

    @classmethod
    def add_text_channel(cls, guild_id: int, channel_id: int):
        """指定されたguild_idにchannel_idを追加する。

        Parameters
        ----------
        guild_id : int
            ギルドid
        channel_id : int
            チャンネルid
        """

        if guild_id not in cls.text_channel_list:
            cls.text_channel_list[guild_id] = []

        if channel_id not in cls.text_channel_list[guild_id]:
            cls.text_channel_list[guild_id].append(channel_id)

    @classmethod
    def has_channel(cls, guild_id: int, channel_id: int) -> bool:
        """指定されたguild_idにchannel_idが存在するかを確認する。

        Parameters
        ----------
        guild_id : int
            ギルドid
        channel_id : int
            チャンネルid

        Returns
        -------
        bool
            存在する場合True
        """
        return (
            guild_id in cls.text_channel_list
            and channel_id in cls.text_channel_list[guild_id]
        )

    @classmethod
    def remove_guild(cls, guild_id: int) -> None:
        """指定されたguild_id（と紐づくchannel_id）を削除する。

        Parameters
        ----------
        guild_id : int
            ギルドid
        """
        if guild_id in cls.text_channel_list:
            del cls.text_channel_list[guild_id]
