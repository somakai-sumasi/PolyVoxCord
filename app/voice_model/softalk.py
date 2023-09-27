import os
import subprocess
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
from entity.voice_setting_entity import VoiceSettingEntity
from voice_model.meta_voice_model import MetaVoiceModel

load_dotenv()
SOFTALK = os.getenv("SOFTALK")


class Softalk(MetaVoiceModel):
    @classmethod
    def create_voice(cls, voice_setting: VoiceSettingEntity, text: str) -> str:
        """読み上げ音声を作成する

        Parameters
        ----------
        voice_setting : VoiceSettingEntity
            ボイスの設定
        text: str
            読み上げするテキスト

        Returns
        -------
        str
            音声ファイルのパス
        """

        fileTitle = cls.create_filename(__class__.__name__)
        SAVE_PASE = os.getcwd() + "\\wav\\" + fileTitle

        _start = "start " + SOFTALK
        _speed = "/S:" + str(int(voice_setting.speed))
        _pitch = "/O:" + str(int(voice_setting.pitch))
        _model = voice_setting.voice_name_key
        _word = "/W:" + text
        _save = "/R:" + SAVE_PASE

        _command = [_start, _speed, _pitch, _model, _save, _word]

        subprocess.run(" ".join(_command), shell=True)

        return SAVE_PASE

    @classmethod
    def voice_list(cls) -> list[str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        dict[str, str]
            ボイス名のリスト
        """

        _start = "start " + SOFTALK
        path = os.getcwd() + "\\softalk.xml"
        _xml = "/zz:" + path
        _command = [_start, _xml]

        # xml作成
        subprocess.run(" ".join(_command), shell=True)

        # xml解析
        voice_list: dict = {}
        tree = ET.parse(path)
        root = tree.getroot()
        for library in root:
            library_id = library.attrib["opt"]
            for voice in library:
                voice_id = voice.attrib["opt"]
                voice_list[library_id + voice_id] = voice.text

        return voice_list
