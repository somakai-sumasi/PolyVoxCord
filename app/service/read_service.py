import asyncio
import os
import re
from typing import Dict, List

import discord
from common.assign_kana import get_pronunciation
from entity.read_limit_entity import ReadLimitEntity
from entity.voice_setting_entity import VoiceSettingEntity
from repository.guild_voice_setting_repository import GuildVoiceSettingRepository
from repository.read_limit_repository import ReadLimitRepository
from repository.reading_dict_repository import ReadingDictRepository
from repository.voice_setting_repository import VoiceSettingRepository
from voice_model.meta_voice_model import MetaVoiceModel
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


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

            guild_id = message.guild.id
            content = cls.conv_discord_object(content)
            content = cls.omit_url(content)
            content = cls.match_with_dictionary(guild_id, content)
            content = cls.limit_length(guild_id, content)
            content = get_pronunciation(content)

            path = cls.make_voice(message.guild.id, message.author.id, content)
            voice_client = message.guild.voice_client
            # 他の音声が再生されていないか確認
            while voice_client.is_playing():
                await asyncio.sleep(0.5)

            # ファイルが出来るまで待つ
            while not (os.access(path, os.W_OK)):
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
    async def read_file(cls, message: discord.Message):
        """ファイルを読み上げる

        Parameters
        ----------
        message : discord.Message
            discord.Message
        """
        try:
            guild_id = message.guild.id

            attachments = message.attachments
            for attachment in attachments:
                name, ext = os.path.splitext(attachment.filename)
                if ext != ".txt":
                    continue

                byte_content = await attachment.read()
                content = byte_content.decode("utf-8")
                content = cls.omit_url(content)
                content = cls.match_with_dictionary(guild_id, content)
                content = get_pronunciation(content)

                path = cls.make_voice(message.guild.id, message.author.id, content)
                voice_client = message.guild.voice_client
                # 他の音声が再生されていないか確認
                while voice_client.is_playing():
                    await asyncio.sleep(0.5)

                # ファイルが出来るまで待つ
                while not (os.access(path, os.W_OK)):
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
    def make_voice(cls, guild_id: int, user_id: int, text: str) -> str:
        """音声を作成する

        Parameters
        ----------
        guild_id : int
            guild_id
        user_id : int
            user_id
        text : str
            読み上げ文字

        Returns
        -------
        str
            ファイルのパス
        """
        voice_setting = GuildVoiceSettingRepository.get_by_user_id(guild_id, user_id)
        # サーバー別の設定がない場合はこちらを使う
        if voice_setting == None:
            voice_setting = VoiceSettingRepository.get_by_user_id(user_id)

        # 登録されていない場合は~で読み上げ
        if voice_setting == None:
            voice_setting = VoiceSettingEntity(
                user_id=user_id,
                voice_type="Softalk",
                voice_name_key="/T:7/U:0",
                speed=120,
                pitch=100,
            )

        voice_type = voice_setting.voice_type

        voice_model: MetaVoiceModel = None
        if voice_type == "VOICEROID":
            voice_model = Voiceroid()

        if voice_type == "VOICEVOX":
            voice_model = Voicevox()

        if voice_type == "Softalk":
            voice_model = Softalk()

        return voice_model.create_voice(voice_setting, text)

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
    def omit_url(cls, text: str) -> str:
        """URLがある場合省略する

        Parameters
        ----------
        text : str
            変換する文字

        Returns
        -------
        str
            変換後の文字
        """
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        replace_text = "\nユーアールエル省略\n"
        return re.sub(pattern, replace_text, text)

    @classmethod
    def limit_length(cls, guild_id: int, text: str) -> str:
        """最大文字数を超える場合カット

        Parameters
        ----------
        guild_id : int
            guild_id
        text : str
            変換する文字

        Returns
        -------
        str
            変換後の文字
        """
        read_limit = ReadLimitRepository.get_by_guild_id(guild_id)
        if read_limit == None:
            read_limit = ReadLimitEntity(guild_id=guild_id, upper_limit=250)
        upper_limit = read_limit.upper_limit

        if len(text) > upper_limit:
            text = text[:upper_limit] + "\n以下略\n"
        return text

    @classmethod
    def match_with_dictionary(cls, guild_id: int, text: str) -> str:
        """読みを反映した、読み上げ文字にする

        Parameters
        ----------
        guild_id : int
            guild_id
        text : str
            変換する文字

        Returns
        -------
        str
            変換後の文字
        """

        reading_dicts = ReadingDictRepository.get_by_guild_id(guild_id)
        result_text = text

        read_list = []  # あとでまとめて変換するときの読み仮名リスト
        for i, reading_dict in enumerate(reading_dicts):
            result_text = result_text.replace(
                reading_dict.character, "{" + str(i) + "}"
            )
            read_list.append(reading_dict.reading)  # 変換が発生した順に読みがなリストに追加

        result_text = result_text.format(*read_list)  # 読み仮名リストを引数にとる

        return result_text

    @classmethod
    def conv_discord_object(cls, text: str) -> str:
        text = re.sub("\<:.+:\d+\>", "サーバー絵文字", text)
        return text
