import datetime
import os
from abc import ABCMeta, abstractmethod

from config.voice import VOICE_OUTPUT_DIR
from entity.voice_setting_entity import VoiceSettingEntity


class MetaVoiceModel(metaclass=ABCMeta):
    """ボイスモデル用のメタクラス

    Parameters
    ----------
    metaclass : _type_, optional
        _description_, by default ABCMeta
    """

    @classmethod
    @abstractmethod
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
        pass

    @abstractmethod
    def voice_list() -> dict[str, str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        dict[str, str]
            ボイス名のリスト
        """
        pass

    @classmethod
    def file_path(cls, class_name: str) -> str:
        """ファイルのパスを作成する

        Parameters
        ----------
        class_name : str, optional
            クラス名, by default None

        Returns
        -------
        str
            ファイルのパス
        """

        now = datetime.datetime.now()
        fileTitle = now.strftime("%Y%m%d-%H%M%S%f") + class_name + ".wav"

        return os.path.join(VOICE_OUTPUT_DIR, fileTitle)
