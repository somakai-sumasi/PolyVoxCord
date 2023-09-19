import discord
from voice_model.meta_voice_model import MetaVoiceModel
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox

from repository.voice_setting_repository import VoiceSettingRepository
from entity.voice_setting_entity import VoiceSettingEntity


class ReadService:
    @classmethod
    def read(cls, message: discord.Message):
        # メッセージの送信者がbotだった場合は無視
        if message.author.bot:
            return
        # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
        if message.guild.voice_client is None:
            return
        
        cls.read_text(message)

    @classmethod
    def read_text(cls, message: discord.Message):
        ...

    @classmethod
    def read_file(cls):
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

        voice_model.create_voice(voice_setting, text)
