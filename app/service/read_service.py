import os
import re
import asyncio
import discord
from voice_model.meta_voice_model import MetaVoiceModel
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox
from entity.voice_setting_entity import VoiceSettingEntity
from entity.read_limit_entity import ReadLimitEntity
from repository.voice_setting_repository import VoiceSettingRepository
from repository.read_limit_repository import ReadLimitRepository
from repository.reading_dict_repository import ReadingDictRepository


class ReadService:
    # 読み上げ管理キュー
    queue_map = {}

    @classmethod
    async def read(cls, message: discord.Message):
        # メッセージの送信者がbotだった場合は無視
        if message.author.bot:
            return
        # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
        if message.guild.voice_client is None:
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
                    cls.read_text(next_message),
                    cls.read_file(next_message),
                )

                break
            else:
                # 自分の番でない場合、キューを戻す
                await cls.queue_map[guild_id].put((next_message_id, next_message))

    @classmethod
    async def read_text(cls, message: discord.Message):
        try:
            content = message.content
            guild_id = message.guild.id
            content = cls.omit_url(content)
            content = cls.match_with_dictionary(content, guild_id)
            content = cls.limit_length(content, guild_id)

            path = cls.make_voice(message.author.id, content)
            voice_client = message.guild.voice_client
            # 他の音声が再生されていないか確認
            while voice_client.is_playing():
                await asyncio.sleep(0.5)

# ファイルが出来るまで待つ
            while not(os.access(path, os.W_OK)):
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
        content = message.content
        guild_id = message.guild.id
        content = cls.omit_url(content)
        content = cls.match_with_dictionary(content, guild_id)
        ...

    @classmethod
    def make_voice(cls, user_id: int, text: str) -> str:
        voice_setting = VoiceSettingRepository.get_by_user_id(user_id)

        # 登録されていない場合は~で読み上げ
        if voice_setting == None:
            voice_setting = VoiceSettingEntity(
                user_id=user_id,
                voice_type="Softalk",
                voice_name_key="",
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
    def omit_url(cls, text: str) -> str:
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        replace_text = "\nユーアールエル省略\n"
        return re.sub(pattern, replace_text, text)

    @classmethod
    def limit_length(cls, text: str, guild_id: int) -> str:
        read_limit = ReadLimitRepository.get_by_guild_id(guild_id)
        if read_limit == None:
            read_limit = ReadLimitEntity(guild_id=guild_id, upper_limit=250)
        upper_limit = read_limit.upper_limit

        if len(text) > upper_limit:
            text = text[:upper_limit] + "\n以下略\n"
        return text

    @classmethod
    def match_with_dictionary(cls, text: str, guild_id: int) -> str:
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
