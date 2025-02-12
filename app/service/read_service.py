import asyncio
import os

import discord
from service.make_voice_service import MakeVoiceService


class ReadService:
    # 読み上げ管理キュー
    queue_map: dict[int, asyncio.Queue] = {}
    text_channel_list: dict[int, list[int]] = {}

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

        paths = await cls.create_voice_files(message)
        if len(paths) < 1:
            return

        guild_id = message.guild.id
        message_id = message.id

        # ギルドごとのキューが存在しない場合は作成
        if guild_id not in cls.queue_map:
            cls.queue_map[guild_id] = asyncio.Queue()

        # 生成した音声ファイルをキューに追加
        await cls.queue_map[guild_id].put((message_id, paths))

        while True:
            next_message_id, paths = await cls.queue_map[guild_id].get()
            if next_message_id == message_id:
                # メッセージ,添付ファイルの順番に読み上げ
                await asyncio.gather(
                    *[
                        cls.play_audio(message.guild.voice_client, path)
                        for path in paths
                    ]
                )
                break
            else:
                # 自分の番でない場合、キューを戻す
                await cls.queue_map[guild_id].put((next_message_id, paths))

    @classmethod
    async def play_audio(cls, voice_client: discord.VoiceClient, path: str):
        """音声を再生する"""
        try:
            while voice_client.is_playing():
                await asyncio.sleep(0.5)

            voice_client.stop()
            voice_client.play(discord.FFmpegPCMAudio(path))
        except Exception:
            print("Error in play_audio", exc_info=True)

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

    @classmethod
    async def create_voice_files(cls, message: discord.Message) -> list[str]:
        """音声ファイルを作成

        Parameters
        ----------
        message : discord.Message
           discord.Message
        """

        make_voice_service = MakeVoiceService(message.guild.id, message.author.id)
        paths = []

        content = cls.__fetch_message_content(message)
        if len(content) > 0:
            paths.append(
                await make_voice_service.make_voice(
                    content, is_omit_url=True, is_read_limit=True
                )
            )

        for file_content in await cls.__fetch_file_content(message):
            if len(file_content) > 0:
                paths.append(
                    await make_voice_service.make_voice(
                        file_content, is_omit_url=True, is_read_limit=True
                    )
                )

        return paths

    @classmethod
    def __fetch_message_content(cls, message: discord.Message) -> str:
        """メッセージの内容を取得

        Parameters
        ----------
        message : discord.Message
            discord.Message

        Returns
        -------
        str
            読み上げ文字列
        """
        return message.clean_content

    @classmethod
    async def __fetch_file_content(cls, message: discord.Message) -> list[str]:
        """ファイルの内容を取得

        Parameters
        ----------
        message : discord.Message
            discord.Message

        Returns
        -------
        list[str]
            読み上げ文字列
        """
        contents: list = []
        attachments = message.attachments
        for attachment in attachments:
            _, ext = os.path.splitext(attachment.filename)
            if ext != ".txt":
                continue

            byte_content = await attachment.read()
            content = byte_content.decode("utf-8")
            if len(content) < 1:
                return

            contents.append(content)

        return contents
