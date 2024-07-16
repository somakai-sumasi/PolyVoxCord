import os
import platform
import subprocess
import xml.etree.ElementTree as ET

from config.voice_model import SOFTALK
from entity.voice_setting_entity import VoiceSettingEntity
from voice_model.meta_voice_model import MetaVoiceModel


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

        # Windows以外での動作の場合、エラー
        if platform.system() != "Windows":
            raise NotImplementedError("Voiceroid is only available on Windows.")

        fileTitle = cls.create_filename(__class__.__name__)
        SAVE_PASE = os.getcwd() + "\\tmp\\wav\\" + fileTitle

        _start = "start " + SOFTALK
        _speed = "/S:" + str(int(voice_setting.speed))
        _pitch = "/O:" + str(int(voice_setting.pitch))
        _model = voice_setting.voice_name_key
        _word = "/W:" + text.replace('"', "")
        _save = "/R:" + SAVE_PASE

        argument = " ".join([_speed, _pitch, _model, _save, _word])

        command = _start + ' "' + argument + '"'

        subprocess.run(command, shell=True)

        return SAVE_PASE

    @classmethod
    def voice_list(cls) -> list[dict[str, str]]:
        """自身が持っているボイス名を返す

        Returns
        -------
        dict[str, str]
            ボイス名のリスト
        """
        # Windows以外での動作の場合、何も返さない
        if platform.system() != "Windows":
            return {}

        _start = "start " + SOFTALK
        path = os.getcwd() + "\\softalk.xml"
        _xml = "/zz:" + path
        _command = [_start, _xml]

        # xml作成
        subprocess.run(" ".join(_command), shell=True)

        # xml解析
        tree = ET.parse(path)
        root = tree.getroot()

        voices = []
        for library in root:
            library_id = library.attrib["opt"]
            # 各ボイスをループ
            for voice in library:
                voice_id = voice.attrib["opt"]
                # ライブラリIDとボイスIDを結合し、ボイステキストと共に辞書に追加
                voices.append({"id": library_id + voice_id, "name": voice.text})

        return voices
