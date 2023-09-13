from __future__ import annotations
from abc import ABCMeta, abstractmethod
from model.voice_setting_model import VoiceSettingModel
import datetime

class MetaVoiceModel(metaclass=ABCMeta):
    """ボイスモデル用のメタクラス

    Parameters
    ----------
    metaclass : _type_, optional
        _description_, by default ABCMeta
    """

    def __init__(self) -> None:
        """init

        Parameters
        ----------
        """

    @classmethod
    @abstractmethod
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
        pass

    @abstractmethod
    def voice_list() -> list[str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        list[str]
            ボイス名のリスト
        """
        pass

    def create_filename(class_name = None):
        now = datetime.datetime.now()
        fileTitle = now.strftime("%Y%m%d-%H%M%S%f") + class_name + ".wav"
        return fileTitle
