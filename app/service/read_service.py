import discord
from data_model.voice_setting_model import VoiceSettingModel
from data_model.read_limit import ReadLimit
from decimal import Decimal


class ReadService:
    # 音声データ作成
    def read(message: discord.Message):
        # メッセージの送信者がbotだった場合は無視
        if message.author.bot:
            return
        # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
        if message.guild.voice_client is None:
            return

    def read_txt():
        ...

    def read_file():
        ...

    def make_voice(user_id: int, txt: str):
        voice_model = VoiceSettingModel({"user_id": user_id})
        voice_type = voice_model.voice_type

        # 登録されていない場合は~で読み上げ
        if voice_type == None:
            voice_model.voice_type = "SofTalk"
            voice_model.voice_name_key = ""
            voice_model.speed = Decimal("100")
            voice_model.pitch = Decimal("100")

        if voice_type == "VOICEROID":
            ...
        if voice_type == "VOICEVOX":
            ...
        if voice_type == "SofTalk":
            ...
