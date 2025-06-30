import json
import os

import requests
from config.voice_model import VOICEVOX_HOST, VOICEVOX_PORT
from entity.voice_setting_entity import VoiceSettingEntity
from voice_model.meta_voice_model import MetaVoiceModel


class Voicevox(MetaVoiceModel):
    PATH = f"http://{VOICEVOX_HOST}:{VOICEVOX_PORT}/"

    @classmethod
    def create_voice(cls, voice_setting: VoiceSettingEntity, text: str) -> str:
        """読み上げ音声を作成する

        Parameters
        ----------
        voice_setting : VoiceSettingEntity
            ボイスの設定
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

        audio_query = requests.post(
            cls.PATH + "audio_query", params=params, timeout=(1.0, 10.0)
        )

        audio_query_json = audio_query.json()

        audio_query_json["speedScale"] = voice_setting.speed
        audio_query_json["pitchScale"] = voice_setting.pitch

        synthesis = requests.post(
            cls.PATH + "synthesis",
            params=params,
            data=json.dumps(audio_query_json),
            timeout=(1.0, 10.0),
        )

        path = os.getcwd() + "/tmp/wav/" + cls.create_filename(__class__.__name__)
        with open(path, mode="wb") as f:
            f.write(synthesis.content)

        return path

    @classmethod
    def voice_list(cls) -> list[dict[str, str]]:
        """自身が持っているボイス名を返す

        Returns
        -------
        dict[str, str]
            ボイス名のリスト
        """
        speakers = requests.get(
            cls.PATH + "speakers",
        ).json()

        voices = [
            {"id": style["id"], "name": " ".join([speaker["name"], style["name"]])}
            for speaker in speakers
            for style in speaker["styles"]
        ]

        return voices
