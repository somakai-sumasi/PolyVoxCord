import datetime
from abc import ABCMeta, abstractmethod

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

    def create_filename(class_name: str = None) -> str:
        """_summary_

        Parameters
        ----------
        class_name : str, optional
            クラス名, by default None

        Returns
        -------
        str
            ファイル名
        """
        now = datetime.datetime.now()
        fileTitle = now.strftime("%Y%m%d-%H%M%S%f") + class_name + ".wav"
        return fileTitle
