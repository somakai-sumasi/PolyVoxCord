import asyncio
import os

import discord
from base.bot import BaseBot
from service.make_voice_service import MakeVoiceService


class ReadService:
    @classmethod
    async def read(cls, bot: BaseBot, message: discord.Message):
        """読み上げイベントを管理

        Parameters
        ----------
        message : discord.Message
            discord.Message
        """

        # 読み上げ対象チェック
        if not cls.__is_read_target_message(bot, message):
            return

        guild_id = message.guild.id
        message_id = message.id

        # 音声ファイル作成用のFutureを作成
        voice_future: asyncio.Future[list[str]] = asyncio.Future()

        # 非同期で音声ファイルを作成するタスクを開始
        task = asyncio.create_task(
            cls.__create_voice_files_async(message, voice_future)
        )

        # キューに追加（メッセージ順序を保証）
        await bot.add_to_read_queue(guild_id, message_id, voice_future)

        # タスクが完了していない場合は例外をログに記録
        def log_exception(t: asyncio.Task) -> None:
            if not t.cancelled() and t.exception():
                print(f"Voice creation task error: {t.exception()}")

        task.add_done_callback(log_exception)

    @classmethod
    def __is_read_target_message(cls, bot: BaseBot, message: discord.Message) -> bool:
        """読み上げ対象のメッセージかをチェック
        読み上げる内容があるかどうかなど具体的な内容までは見ない

        Parameters
        ----------
        bot : BaseBot
            Botインスタンス
        message : discord.Message
            discord.Message

        Returns
        -------
        bool
            読み上げるべきかどうかの真理値
        """
        # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
        if message.guild.voice_client is None:
            return False

        # メッセージの送信者がbotだった場合は無視
        if message.author.bot:
            return False

        # 読み上げ対象でないチャンネルは無視
        if not bot.has_channel(message.guild.id, message.channel.id):
            return False

        return True

    @classmethod
    async def __create_voice_files_async(
        cls, message: discord.Message, future: asyncio.Future[list[str]]
    ):
        """非同期で音声ファイルを作成してFutureに結果をセット

        Parameters
        ----------
        message : discord.Message
            discord.Message
        future : asyncio.Future
            結果を格納するFuture
        """
        try:
            paths = await cls.__create_voice_files(message)
            if not future.done():
                future.set_result(paths)
        except Exception as e:
            if not future.done():
                future.set_exception(e)
            print(f"Error creating voice files for message {message.id}: {e}")

    @classmethod
    async def __create_voice_files(cls, message: discord.Message) -> list[str]:
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
                continue

            contents.append(content)

        return contents
