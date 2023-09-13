from voice_model.meta_voice_model import MetaVoiceModel
from model.voice_setting_model import VoiceSettingModel
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()


class SofTalk(MetaVoiceModel):
    @classmethod
    def create_voice(cls, voice_setting: VoiceSettingModel, text: str) -> str:
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

        fileTitle = cls.create_filename (__class__.__name__)
        SAVE_PASE = os.getcwd() + "\\wav\\" + fileTitle
        SOF_TALK = os.getenv("SOF_TALK")

        _start = "start " + SOF_TALK
        _speed = "/S:120"
        _pitch = "/O:100"
        _model = "/T:7/U:1"
        _word = "/W:" + text
        _save = "/R:" + SAVE_PASE

        _command = [_start, _speed, _pitch, _model, _save, _word]

        subprocess.run(" ".join(_command), shell=True)
        return SAVE_PASE

    def voice_list(self) -> list[str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        list[str]
            ボイス名のリスト
        """
        pass
