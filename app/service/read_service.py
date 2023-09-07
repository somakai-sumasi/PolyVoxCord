import discord
from decimal import Decimal
from data_model.voice_setting_model import VoiceSettingModel
from data_model.read_limit import ReadLimit
from voice_model.meta_voice_model import MetaVoiceModel
from voice_model.sof_talk import SofTalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


class ReadService:
    # 音声データ作成
    def read(message: discord.Message):
        # メッセージの送信者がbotだった場合は無視
        if message.author.bot:
            return
        # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
        if message.guild.voice_client is None:
            return

    def read_text():
        ...

    def read_file():
        ...

    def make_voice(user_id: int, text: str):
        voice_setting = VoiceSettingModel({"user_id": user_id})
        voice_type = voice_setting.voice_type

        # 登録されていない場合は~で読み上げ
        if voice_type == None:
            voice_setting.voice_type = "SofTalk"
            voice_setting.voice_name_key = ""
            voice_setting.speed = Decimal("100")
            voice_setting.pitch = Decimal("100")

        voice_model: MetaVoiceModel = None
        if voice_type == "VOICEROID":
            voice_model = Voiceroid()

        if voice_type == "VOICEVOX":
            voice_model = Voicevox()

        if voice_type == "SofTalk":
            voice_model = SofTalk()

        voice_model.create_voice(voice_setting, text)
