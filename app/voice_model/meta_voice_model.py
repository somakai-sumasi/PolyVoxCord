from __future__ import annotations
from abc import ABCMeta, abstractmethod
from data_model.voice_model import VoiceModel


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

    @abstractmethod
    def create_voice(self, text: str) -> str:
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
    def voice_list(self) -> list[str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        list[str]
            ボイス名のリスト
        """
        pass
