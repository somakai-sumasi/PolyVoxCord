from voice_model.meta_voice_model import MetaVoiceModel
from entity.voice_setting_entity import VoiceSettingEntity
import os
from dotenv import load_dotenv
import requests
import json
import wave

load_dotenv()


class Voicevox(MetaVoiceModel):
    VOICEVOX_HOST = os.getenv("VOICEVOX_HOST")
    VOICEVOX_PORT = os.getenv("VOICEVOX_PORT")
    PATH = f"http://{VOICEVOX_HOST}:{VOICEVOX_PORT}/"

    @classmethod
    def create_voice(cls, voice_setting: VoiceSettingEntity, text: str) -> str:
        """読み上げ音声を作成する

        Parameters
        ----------
        text : str
            読み上げするテキスト

        Returns
        -------
        str
            音声ファイルのパス
        """
        params = (
            ("text", text),
            ("speaker", voice_setting.voice_name_key),
        )

        audio_query = requests.post(cls.PATH + "audio_query", params=params)
        synthesis = requests.post(
            cls.PATH + "synthesis", params=params, data=json.dumps(audio_query.json())
        )

        wf = wave.open( './wav/' + cls.create_filename(__class__.__name__), 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(synthesis.content)
        wf.close()

        pass

    @classmethod
    def voice_list(cls) -> dict[str, str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        list[str]
            ボイス名のリスト
        """
        speakers = requests.get(
            cls.PATH + "speakers",
        ).json()

        voice_list: dict = {}

        for speaker in speakers:
            speaker_name = speaker["name"]
            styles = speaker["styles"]
            for style in styles:
                voice_list[style["id"]] = " ".join([speaker_name, style["name"]])

        return voice_list
