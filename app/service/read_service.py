import asyncio
import discord
from voice_model.meta_voice_model import MetaVoiceModel
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox
from repository.voice_setting_repository import VoiceSettingRepository
from entity.voice_setting_entity import VoiceSettingEntity


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
        path = cls.make_voice(message.author.id, message.content)
        voice_client = message.guild.voice_client
        # 他の音声が再生されていないか確認
        while voice_client.is_playing():
            await asyncio.sleep(0.5)

        # 音声を再生
        voice_client.play(discord.FFmpegPCMAudio(path))

    @classmethod
    async def read_file(cls, message: discord.Message):
        ...

    @classmethod
    def make_voice(cls, user_id: int, text: str):
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
